"""
Sharp Pages Selling Bot — Tool modules.
Each module exposes Python functions AND their JSON schema for Claude's tool_use API.
"""

from tools.product_tools import PRODUCT_TOOL_SCHEMAS, handle_product_tool
from tools.seo_tools import SEO_TOOL_SCHEMAS, handle_seo_tool
from tools.pricing_tools import PRICING_TOOL_SCHEMAS, handle_pricing_tool
from tools.marketing_tools import MARKETING_TOOL_SCHEMAS, handle_marketing_tool
from tools.analytics_tools import ANALYTICS_TOOL_SCHEMAS, handle_analytics_tool
from tools.gumroad_tools import GUMROAD_TOOL_SCHEMAS, handle_gumroad_tool
from tools.competitor_tools import COMPETITOR_TOOL_SCHEMAS, handle_competitor_tool

# All tool schemas merged — passed to anthropic client
ALL_TOOL_SCHEMAS: list[dict] = (
    PRODUCT_TOOL_SCHEMAS
    + SEO_TOOL_SCHEMAS
    + PRICING_TOOL_SCHEMAS
    + MARKETING_TOOL_SCHEMAS
    + ANALYTICS_TOOL_SCHEMAS
    + GUMROAD_TOOL_SCHEMAS
    + COMPETITOR_TOOL_SCHEMAS
)

# Dispatch table: tool name -> handler function
TOOL_HANDLERS: dict[str, callable] = {}
for _mod_handler in [
    handle_product_tool,
    handle_seo_tool,
    handle_pricing_tool,
    handle_marketing_tool,
    handle_analytics_tool,
    handle_gumroad_tool,
    handle_competitor_tool,
]:
    TOOL_HANDLERS[_mod_handler.__name__] = _mod_handler


def dispatch_tool(tool_name: str, tool_input: dict) -> dict:
    """Route a tool_use call from Claude to the correct handler."""
    for handler in [
        handle_product_tool,
        handle_seo_tool,
        handle_pricing_tool,
        handle_marketing_tool,
        handle_analytics_tool,
        handle_gumroad_tool,
        handle_competitor_tool,
    ]:
        result = handler(tool_name, tool_input)
        if result is not None:
            return result
    return {"error": f"Unknown tool: {tool_name}"}
