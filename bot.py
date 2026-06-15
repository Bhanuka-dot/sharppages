#!/usr/bin/env python3
"""
Sharp Pages Selling Bot — Main CLI entry point.

Run with:
    python bot.py

Commands:
    /help   — Show help and example prompts
    /tools  — List all available selling tools
    /quit   — Exit the bot
"""

from __future__ import annotations

import json
import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    # ---------------------------------------------------------------------------
    # Imports (after path fix)
    # ---------------------------------------------------------------------------
    try:
        import anthropic
    except ImportError:
        print("\n[ERROR] 'anthropic' package not found.")
        print("Run: pip install -r requirements.txt\n")
        sys.exit(1)

    try:
        from config import ANTHROPIC_API_KEY, GUMROAD_API_KEY, MODEL, SYSTEM_PROMPT
    except SystemExit:
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Failed to load config: {e}")
        sys.exit(1)

    from tools import ALL_TOOL_SCHEMAS, dispatch_tool
    from utils.display import (
        console,
        print_welcome_banner,
        print_integration_status,
        print_help,
        print_tools_list,
        print_bot_message,
        print_user_message,
        print_tool_call,
        print_tool_result_summary,
        print_error,
        print_separator,
        spinner,
        BRAND_COLOR,
        USER_COLOR,
        DIM_COLOR,
    )

    # ---------------------------------------------------------------------------
    # Welcome
    # ---------------------------------------------------------------------------
    print_welcome_banner()
    print_integration_status(
        anthropic_key=bool(ANTHROPIC_API_KEY),
        gumroad_key=bool(GUMROAD_API_KEY),
    )
    console.print(f"[{DIM_COLOR}]Type your question or /help to get started. /quit to exit.[/{DIM_COLOR}]\n")

    # ---------------------------------------------------------------------------
    # Anthropic client
    # ---------------------------------------------------------------------------
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # ---------------------------------------------------------------------------
    # Conversation state
    # ---------------------------------------------------------------------------
    messages: list[dict] = []

    # ---------------------------------------------------------------------------
    # Tool execution
    # ---------------------------------------------------------------------------
    def execute_tool(tool_name: str, tool_input: dict) -> str:
        """Execute a tool and return its result as a JSON string."""
        print_tool_call(tool_name, tool_input)
        result = dispatch_tool(tool_name, tool_input)
        print_tool_result_summary(tool_name, result)
        return json.dumps(result, ensure_ascii=False, indent=2)

    # ---------------------------------------------------------------------------
    # Claude API call with tool loop
    # ---------------------------------------------------------------------------
    def chat(user_message: str) -> str:
        """Send a message to Claude, handle tool calls, and return the final text response."""
        messages.append({"role": "user", "content": user_message})

        with spinner("Thinking..."):
            response = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=ALL_TOOL_SCHEMAS,
                messages=messages,
            )

        # Agentic tool loop — keep calling until stop_reason is "end_turn"
        while response.stop_reason == "tool_use":
            # Collect all tool use blocks
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            text_blocks = [b for b in response.content if b.type == "text"]

            # Print any text that came alongside tool calls
            for tb in text_blocks:
                if tb.text.strip():
                    console.print(f"\n[{DIM_COLOR}]{tb.text.strip()}[/{DIM_COLOR}]")

            # Add assistant's response to history
            messages.append({"role": "assistant", "content": response.content})

            # Execute each tool and collect results
            tool_results = []
            console.print()  # Spacing before tool output
            for tool_use in tool_use_blocks:
                result_str = execute_tool(tool_use.name, tool_use.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result_str,
                })

            # Add tool results to messages
            messages.append({"role": "user", "content": tool_results})

            # Get Claude's next response
            console.print()
            with spinner("Processing results..."):
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    tools=ALL_TOOL_SCHEMAS,
                    messages=messages,
                )

        # Extract final text response
        final_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_text += block.text

        # Add final assistant response to history
        messages.append({"role": "assistant", "content": response.content})

        return final_text.strip()

    # ---------------------------------------------------------------------------
    # REPL loop
    # ---------------------------------------------------------------------------
    while True:
        try:
            # Prompt
            console.print(f"[bold {USER_COLOR}]You:[/bold {USER_COLOR}] ", end="")
            user_input = input().strip()
        except (EOFError, KeyboardInterrupt):
            console.print(f"\n[{DIM_COLOR}]Goodbye! Keep building great products. 👋[/{DIM_COLOR}]\n")
            break

        if not user_input:
            continue

        # Slash commands
        if user_input.startswith("/"):
            cmd = user_input.lower().split()[0]

            if cmd in ("/quit", "/exit", "/q"):
                console.print(f"\n[{DIM_COLOR}]Goodbye! Keep building great products.[/{DIM_COLOR}]\n")
                break

            elif cmd == "/help":
                print_help()
                continue

            elif cmd == "/tools":
                print_tools_list(ALL_TOOL_SCHEMAS)
                continue

            elif cmd == "/clear":
                messages.clear()
                console.print(f"[{DIM_COLOR}]Conversation history cleared.[/{DIM_COLOR}]\n")
                continue

            else:
                console.print(
                    f"[{DIM_COLOR}]Unknown command '{user_input}'. "
                    f"Try /help, /tools, or /quit.[/{DIM_COLOR}]\n"
                )
                continue

        # Regular chat message
        print_separator()
        try:
            response_text = chat(user_input)
            print_bot_message(response_text)
        except anthropic.APIConnectionError:
            print_error("Could not connect to Anthropic API. Check your internet connection.")
        except anthropic.AuthenticationError:
            print_error("Invalid ANTHROPIC_API_KEY. Check your .env file.")
        except anthropic.RateLimitError:
            print_error("Rate limit hit. Wait a moment and try again.")
        except anthropic.APIStatusError as e:
            print_error(f"Anthropic API error {e.status_code}: {e.message}")
        except Exception as e:
            print_error(f"Unexpected error: {e}")

        print_separator()
        console.print()


if __name__ == "__main__":
    main()
