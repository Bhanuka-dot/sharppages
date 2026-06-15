"""
Rich terminal UI helpers for Sharp Pages Selling Bot.
Provides panels, spinners, formatted output, and color themes.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text
from rich import box
from rich.live import Live
from rich.markdown import Markdown
from rich.rule import Rule

# Shared console instance — import this everywhere
console = Console()

# Brand colors
BRAND_COLOR = "bright_magenta"
BOT_COLOR = "bright_cyan"
USER_COLOR = "bright_green"
TOOL_COLOR = "bright_yellow"
ERROR_COLOR = "bright_red"
SUCCESS_COLOR = "bright_green"
DIM_COLOR = "grey62"


def print_welcome_banner() -> None:
    """Print the Sharp Pages Selling Bot welcome banner."""
    banner_text = Text()
    banner_text.append("Sharp Pages", style=f"bold {BRAND_COLOR}")
    banner_text.append(" Selling Bot", style="bold white")

    subtitle = Text("Your AI-powered digital product business advisor", style=DIM_COLOR)

    console.print()
    console.print(
        Panel(
            f"[bold {BRAND_COLOR}]Sharp Pages[/bold {BRAND_COLOR}] [bold white]Selling Bot[/bold white]\n"
            f"[{DIM_COLOR}]Your AI-powered digital product business advisor[/{DIM_COLOR}]\n\n"
            f"[{DIM_COLOR}]Specializing in Gumroad selling & Pinterest marketing[/{DIM_COLOR}]",
            border_style=BRAND_COLOR,
            padding=(1, 4),
            title="[bold white]v1.0[/bold white]",
            title_align="right",
        )
    )
    console.print()


def print_integration_status(anthropic_key: bool, gumroad_key: bool) -> None:
    """Show which integrations are active."""
    table = Table(
        show_header=False,
        box=box.SIMPLE,
        padding=(0, 1),
    )
    table.add_column("Integration", style="bold")
    table.add_column("Status")

    table.add_row(
        "Anthropic AI",
        f"[{SUCCESS_COLOR}]Connected[/{SUCCESS_COLOR}]" if anthropic_key else f"[{ERROR_COLOR}]Missing[/{ERROR_COLOR}]",
    )
    table.add_row(
        "Gumroad API",
        f"[{SUCCESS_COLOR}]Connected[/{SUCCESS_COLOR}]"
        if gumroad_key
        else f"[{DIM_COLOR}]Demo mode (no API key)[/{DIM_COLOR}]",
    )

    console.print(
        Panel(
            table,
            title="[bold]Integrations[/bold]",
            border_style=DIM_COLOR,
            padding=(0, 2),
        )
    )
    console.print()


def print_help() -> None:
    """Print the help message."""
    console.print(
        Panel(
            "[bold]Available commands:[/bold]\n\n"
            f"  [bold {USER_COLOR}]/help[/bold {USER_COLOR}]   — Show this help message\n"
            f"  [bold {USER_COLOR}]/tools[/bold {USER_COLOR}]  — List all available selling tools\n"
            f"  [bold {USER_COLOR}]/quit[/bold {USER_COLOR}]   — Exit the bot\n\n"
            "[bold]Example prompts:[/bold]\n\n"
            f"  [{DIM_COLOR}]\"Write a product description for my Notion budget tracker template\"[/{DIM_COLOR}]\n"
            f"  [{DIM_COLOR}]\"What keywords should I target for Canva social media templates?\"[/{DIM_COLOR}]\n"
            f"  [{DIM_COLOR}]\"How should I price my eBook? Competitors charge $9-$27\"[/{DIM_COLOR}]\n"
            f"  [{DIM_COLOR}]\"Create 5 Pinterest pin ideas for my productivity planner\"[/{DIM_COLOR}]\n"
            f"  [{DIM_COLOR}]\"Analyze my sales: 45 units @ $17 last month, 60 units this month\"[/{DIM_COLOR}]\n"
            f"  [{DIM_COLOR}]\"What gaps exist in the Notion template market?\"[/{DIM_COLOR}]",
            title="[bold]Help[/bold]",
            border_style=BOT_COLOR,
            padding=(1, 2),
        )
    )


def print_tools_list(all_schemas: list[dict]) -> None:
    """Print a formatted list of all available tools."""
    table = Table(
        title="Available Selling Tools",
        box=box.ROUNDED,
        border_style=TOOL_COLOR,
        header_style=f"bold {TOOL_COLOR}",
        show_lines=False,
        padding=(0, 1),
    )
    table.add_column("Tool Name", style="bold cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for schema in all_schemas:
        name = schema.get("name", "")
        desc = schema.get("description", "")
        # Truncate long descriptions
        if len(desc) > 70:
            desc = desc[:67] + "..."
        table.add_row(name, desc)

    console.print()
    console.print(table)
    console.print()


def print_user_message(text: str) -> None:
    """Display the user's message in the chat."""
    console.print(f"\n[bold {USER_COLOR}]You:[/bold {USER_COLOR}] {text}")


def print_bot_prefix() -> None:
    """Print the bot response label."""
    console.print(f"\n[bold {BOT_COLOR}]Sharp Pages Bot:[/bold {BOT_COLOR}]")


def print_bot_message(text: str) -> None:
    """Render the bot's markdown response."""
    print_bot_prefix()
    try:
        md = Markdown(text)
        console.print(md)
    except Exception:
        console.print(text)


def print_tool_call(tool_name: str, tool_input: dict) -> None:
    """Show which tool is being called."""
    params_str = ", ".join(
        f"{k}={repr(v)[:40]}" for k, v in tool_input.items()
    )
    console.print(
        f"  [{TOOL_COLOR}]Using tool:[/{TOOL_COLOR}] [bold]{tool_name}[/bold]"
        f"([{DIM_COLOR}]{params_str}[/{DIM_COLOR}])"
    )


def print_tool_result_summary(tool_name: str, result: dict) -> None:
    """Show a brief confirmation of tool result."""
    if "error" in result:
        console.print(
            f"  [{ERROR_COLOR}]Tool error:[/{ERROR_COLOR}] {result['error']}"
        )
    else:
        keys = list(result.keys())[:3]
        console.print(
            f"  [{SUCCESS_COLOR}]Tool result:[/{SUCCESS_COLOR}] {tool_name} returned "
            f"[{DIM_COLOR}]{{{', '.join(keys)}{'...' if len(result) > 3 else ''}}}[/{DIM_COLOR}]"
        )


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"\n[bold {ERROR_COLOR}]Error:[/bold {ERROR_COLOR}] {message}")


def print_separator() -> None:
    """Print a visual separator."""
    console.print(Rule(style=DIM_COLOR))


@contextmanager
def spinner(message: str = "Thinking..."):
    """Context manager that shows a spinner while work is happening."""
    with console.status(
        f"[{BOT_COLOR}]{message}[/{BOT_COLOR}]",
        spinner="dots",
        spinner_style=BRAND_COLOR,
    ):
        yield


def format_dict_as_panel(data: dict, title: str = "", border_color: str = DIM_COLOR) -> Panel:
    """Convert a dict to a formatted panel for display."""
    lines = []
    for key, value in data.items():
        key_fmt = key.replace("_", " ").title()
        if isinstance(value, list):
            lines.append(f"[bold]{key_fmt}:[/bold]")
            for item in value:
                lines.append(f"  • {item}")
        elif isinstance(value, dict):
            lines.append(f"[bold]{key_fmt}:[/bold]")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        else:
            lines.append(f"[bold]{key_fmt}:[/bold] {value}")

    content = "\n".join(lines)
    return Panel(content, title=f"[bold]{title}[/bold]" if title else "", border_style=border_color)
