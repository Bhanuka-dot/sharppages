"""
Sharp Pages Selling Bot — FastAPI web server.

Serves the mobile-first chat UI and exposes a streaming SSE endpoint
that runs the full agentic tool loop with Claude.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import anthropic
from config import ANTHROPIC_API_KEY, MODEL, SYSTEM_PROMPT
from tools import ALL_TOOL_SCHEMAS, dispatch_tool

app = FastAPI(title="Sharp Pages Selling Bot")

# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    messages: list[dict]
    system: str = SYSTEM_PROMPT


# ---------------------------------------------------------------------------
# SSE helpers
# ---------------------------------------------------------------------------

def _sse(payload: dict) -> str:
    """Format a dict as a Server-Sent Events data line."""
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


# ---------------------------------------------------------------------------
# Agentic loop SSE generator
# ---------------------------------------------------------------------------

async def run_agentic_loop(request: ChatRequest):
    """
    Full agentic tool loop that yields SSE events.

    Flow:
      1. Call Claude (sync, in thread pool) with current messages + tools
      2. If stop_reason == "tool_use":
         - Yield tool_start events
         - Execute each tool (sync, in thread pool)
         - Yield tool_result events
         - Append assistant + tool results to messages
         - Loop back to step 1
      3. If stop_reason == "end_turn":
         - Yield text events in small chunks to feel like streaming
         - Yield done event
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    # Deep-copy so we can mutate freely
    messages: list[dict] = [dict(m) for m in request.messages]
    system: str = request.system

    try:
        while True:
            # --- Synchronous Claude call, run in thread pool ---
            response = await asyncio.to_thread(
                client.messages.create,
                model=MODEL,
                max_tokens=4096,
                system=system,
                tools=ALL_TOOL_SCHEMAS,
                messages=messages,
            )

            if response.stop_reason == "tool_use":
                # Separate text and tool blocks
                text_blocks = [b for b in response.content if b.type == "text"]
                tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

                # Stream any text that arrived alongside tool calls
                for tb in text_blocks:
                    if tb.text.strip():
                        yield _sse({"type": "text", "content": tb.text})

                # Serialize assistant turn (SDK objects → plain dicts)
                assistant_content: list[dict] = []
                for block in response.content:
                    if block.type == "text":
                        assistant_content.append({"type": "text", "text": block.text})
                    elif block.type == "tool_use":
                        assistant_content.append({
                            "type": "tool_use",
                            "id": block.id,
                            "name": block.name,
                            "input": block.input,
                        })
                messages.append({"role": "assistant", "content": assistant_content})

                # Execute tools and collect results
                tool_results: list[dict] = []
                for tool_use in tool_use_blocks:
                    yield _sse({
                        "type": "tool_start",
                        "name": tool_use.name,
                        "input": tool_use.input,
                    })

                    result = await asyncio.to_thread(
                        dispatch_tool, tool_use.name, tool_use.input
                    )

                    yield _sse({
                        "type": "tool_result",
                        "name": tool_use.name,
                        "tool_use_id": tool_use.id,
                        "result": result,
                    })

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    })

                # Add tool results to messages and loop
                messages.append({"role": "user", "content": tool_results})
                # Continue while loop

            else:
                # stop_reason == "end_turn" (or max_tokens / stop_sequence)
                final_text = "".join(
                    block.text for block in response.content if hasattr(block, "text")
                )

                if final_text:
                    # Yield in small chunks to give the feel of streaming
                    chunk_size = 6
                    for i in range(0, len(final_text), chunk_size):
                        chunk = final_text[i : i + chunk_size]
                        yield _sse({"type": "text", "content": chunk})
                        await asyncio.sleep(0)  # yield control so chunks actually flush

                yield _sse({"type": "done"})
                break

    except anthropic.AuthenticationError:
        yield _sse({"type": "error", "message": "Authentication failed — check ANTHROPIC_API_KEY."})
    except anthropic.RateLimitError:
        yield _sse({"type": "error", "message": "Rate limit reached. Please wait a moment and try again."})
    except anthropic.APIConnectionError:
        yield _sse({"type": "error", "message": "Cannot connect to Anthropic API. Check your internet connection."})
    except anthropic.APIStatusError as e:
        yield _sse({"type": "error", "message": f"Anthropic API error {e.status_code}: {e.message}"})
    except Exception as e:
        yield _sse({"type": "error", "message": f"Unexpected error: {str(e)}"})


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
async def serve_index():
    """Serve the chat UI."""
    return FileResponse(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")
    )


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    SSE streaming endpoint.
    Accepts the full conversation history, runs the agentic tool loop,
    and streams SSE events back to the client.
    """
    return StreamingResponse(
        run_agentic_loop(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # disable nginx / proxy buffering
            "Connection": "keep-alive",
        },
    )


# ---------------------------------------------------------------------------
# Static files (registered after route declarations so / is not captured)
# ---------------------------------------------------------------------------

_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")
