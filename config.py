"""
Configuration loader for Sharp Pages Selling Bot.
Loads environment variables from .env and validates required keys.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def get_anthropic_api_key() -> str:
    """Return ANTHROPIC_API_KEY or exit with a helpful message."""
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        print(
            "\n[ERROR] ANTHROPIC_API_KEY is not set.\n"
            "Create a .env file (copy .env.example) and add your Anthropic API key.\n"
        )
        sys.exit(1)
    return key


def get_gumroad_api_key() -> str | None:
    """Return GUMROAD_API_KEY or None (optional)."""
    key = os.environ.get("GUMROAD_API_KEY", "").strip()
    return key if key else None


# Exported constants used throughout the project
ANTHROPIC_API_KEY: str = get_anthropic_api_key()
GUMROAD_API_KEY: str | None = get_gumroad_api_key()

# Model used for the bot
MODEL = "claude-sonnet-4-6"

# System prompt that shapes the assistant personality
SYSTEM_PROMPT = """You are the Sharp Pages Selling Bot — an expert digital product business advisor \
specializing in selling on Gumroad and marketing on Pinterest.

You help creators:
- Write compelling product listings that convert
- Research high-traffic keywords and SEO strategies
- Set profitable pricing and fee-aware margins
- Plan Pinterest marketing campaigns and pin strategies
- Analyze sales data and forecast revenue
- Study competitors and find market gaps
- Build email sequences and launch plans

When answering, be specific and actionable. Use numbers, percentages, and concrete examples. \
Avoid generic advice — tailor every response to digital products (templates, guides, eBooks, \
presets, Notion dashboards, Canva templates, etc.) sold on Gumroad.

You have access to a suite of selling tools. Call them proactively whenever they would enrich \
your answer. Combine multiple tool calls in a single turn when the user's question touches \
several areas (e.g., pricing + SEO, or marketing + analytics)."""
