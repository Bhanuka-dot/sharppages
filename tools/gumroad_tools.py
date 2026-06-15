"""
Gumroad API integration tools for Sharp Pages Selling Bot.
Provides live data fetching with graceful demo-mode fallback when no API key is present.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

GUMROAD_API_BASE = "https://api.gumroad.com/v2"


# ---------------------------------------------------------------------------
# Demo data (used when no API key or API error)
# ---------------------------------------------------------------------------

DEMO_PRODUCTS = [
    {
        "id": "demo_prod_1",
        "name": "Ultimate Notion Budget Tracker",
        "description": "A fully automated monthly budget tracker built in Notion.",
        "price": 1700,  # in cents
        "currency": "usd",
        "sales_count": 127,
        "revenue": 21590,  # cents
        "url": "https://gumroad.com/l/budget-tracker-demo",
        "published": True,
        "tags": ["notion", "budget", "finance", "template"],
        "created_at": "2024-08-15T10:00:00Z",
    },
    {
        "id": "demo_prod_2",
        "name": "Pinterest Marketing Playbook",
        "description": "Step-by-step guide to driving traffic to your digital products via Pinterest.",
        "price": 2700,
        "currency": "usd",
        "sales_count": 84,
        "revenue": 22680,
        "url": "https://gumroad.com/l/pinterest-playbook-demo",
        "published": True,
        "tags": ["pinterest", "marketing", "ebook", "social media"],
        "created_at": "2024-10-01T10:00:00Z",
    },
    {
        "id": "demo_prod_3",
        "name": "Canva Social Media Template Pack",
        "description": "50 customizable Canva templates for Instagram, Pinterest, and TikTok.",
        "price": 1200,
        "currency": "usd",
        "sales_count": 213,
        "revenue": 25560,
        "url": "https://gumroad.com/l/canva-templates-demo",
        "published": True,
        "tags": ["canva", "social media", "instagram", "templates"],
        "created_at": "2024-06-20T10:00:00Z",
    },
    {
        "id": "demo_prod_4",
        "name": "Freelance Invoice & Contract Bundle",
        "description": "Professional invoice templates and service contract for freelancers.",
        "price": 1900,
        "currency": "usd",
        "sales_count": 56,
        "revenue": 10640,
        "url": "https://gumroad.com/l/freelance-bundle-demo",
        "published": False,
        "tags": ["freelance", "invoice", "contract", "business"],
        "created_at": "2025-01-05T10:00:00Z",
    },
]


def _make_demo_sales(num_sales: int = 50) -> list[dict]:
    """Generate realistic demo sales records."""
    import random
    products = DEMO_PRODUCTS[:3]
    sales = []
    base_date = datetime.now() - timedelta(days=30)

    for i in range(num_sales):
        product = products[i % len(products)]
        sale_date = base_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        refunded = random.random() < 0.03  # 3% refund rate
        sales.append({
            "id": f"demo_sale_{i + 1}",
            "product_id": product["id"],
            "product_name": product["name"],
            "amount": product["price"] / 100,
            "currency": "usd",
            "created_at": sale_date.isoformat(),
            "refunded": refunded,
            "buyer_email": f"buyer{i + 1}@example.com",
        })

    return sales


DEMO_SUBSCRIBERS = [
    {"id": "sub_1", "email": "subscriber1@example.com", "created_at": "2025-01-10T08:00:00Z"},
    {"id": "sub_2", "email": "subscriber2@example.com", "created_at": "2025-02-14T12:00:00Z"},
    {"id": "sub_3", "email": "subscriber3@example.com", "created_at": "2025-03-22T15:30:00Z"},
]


# ---------------------------------------------------------------------------
# API helper
# ---------------------------------------------------------------------------

def _gumroad_get(endpoint: str, api_key: str, params: dict | None = None) -> dict:
    """Make a GET request to the Gumroad API. Returns response dict or error."""
    if not REQUESTS_AVAILABLE:
        return {"error": "requests library not installed — run: pip install requests"}

    url = f"{GUMROAD_API_BASE}{endpoint}"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        resp = requests.get(url, headers=headers, params=params or {}, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"Gumroad API HTTP error: {e.response.status_code} — {e.response.text[:200]}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to Gumroad API — check your internet connection"}
    except requests.exceptions.Timeout:
        return {"error": "Gumroad API request timed out"}
    except Exception as e:
        return {"error": f"Gumroad API error: {str(e)}"}


def _format_product(p: dict, is_demo: bool = False) -> dict:
    """Normalize a Gumroad product dict for consistent output."""
    price_cents = p.get("price", 0)
    price_usd = price_cents / 100 if isinstance(price_cents, int) else price_cents

    revenue_cents = p.get("revenue", 0)
    revenue_usd = revenue_cents / 100 if isinstance(revenue_cents, int) else revenue_cents

    return {
        "id": p.get("id", ""),
        "name": p.get("name", "Unknown"),
        "price_usd": round(float(price_usd), 2),
        "sales_count": p.get("sales_count", 0),
        "revenue_usd": round(float(revenue_usd), 2),
        "published": p.get("published", True),
        "url": p.get("url", ""),
        "tags": p.get("tags", []),
        "created_at": p.get("created_at", ""),
        "demo": is_demo,
    }


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def get_gumroad_products(api_key: str | None = None) -> dict:
    """
    Fetch products from the Gumroad API.
    Falls back to demo data if api_key is missing or invalid.
    """
    try:
        # Resolve API key — param takes priority, then env
        resolved_key = api_key or os.environ.get("GUMROAD_API_KEY", "").strip()

        if not resolved_key:
            # Demo mode
            formatted = [_format_product(p, is_demo=True) for p in DEMO_PRODUCTS]
            return {
                "mode": "demo",
                "notice": "No GUMROAD_API_KEY found — showing realistic demo data. Set GUMROAD_API_KEY in .env for live data.",
                "product_count": len(formatted),
                "products": formatted,
                "total_revenue_usd": round(sum(p["revenue_usd"] for p in formatted), 2),
                "published_count": sum(1 for p in formatted if p["published"]),
            }

        response = _gumroad_get("/products", resolved_key)

        if "error" in response:
            # API failed — fall back to demo with error context
            return {
                "mode": "demo_fallback",
                "api_error": response["error"],
                "notice": "Using demo data due to API error. Check your API key.",
                "products": [_format_product(p, is_demo=True) for p in DEMO_PRODUCTS],
            }

        raw_products = response.get("products", [])
        formatted = [_format_product(p) for p in raw_products]
        total_revenue = sum(p["revenue_usd"] for p in formatted)
        published = [p for p in formatted if p["published"]]

        return {
            "mode": "live",
            "product_count": len(formatted),
            "published_count": len(published),
            "products": formatted,
            "total_revenue_usd": round(total_revenue, 2),
            "top_earner": max(formatted, key=lambda x: x["revenue_usd"])["name"] if formatted else None,
        }
    except Exception as e:
        return {"error": str(e)}


def get_gumroad_sales(
    api_key: str | None = None,
    after_date: str | None = None,
    before_date: str | None = None,
) -> dict:
    """
    Fetch sales from the Gumroad API for a date range.
    Falls back to demo data when no API key.
    """
    try:
        resolved_key = api_key or os.environ.get("GUMROAD_API_KEY", "").strip()

        if not resolved_key:
            demo_sales = _make_demo_sales(50)
            total_revenue = sum(s["amount"] for s in demo_sales if not s["refunded"])
            refund_count = sum(1 for s in demo_sales if s["refunded"])
            net_sales = len(demo_sales) - refund_count
            avg_order = total_revenue / net_sales if net_sales > 0 else 0

            return {
                "mode": "demo",
                "notice": "No GUMROAD_API_KEY found — showing demo sales data.",
                "date_range": {
                    "after": after_date or "30 days ago",
                    "before": before_date or "today",
                },
                "sales_summary": {
                    "total_transactions": len(demo_sales),
                    "net_sales": net_sales,
                    "refunds": refund_count,
                    "refund_rate_pct": round(refund_count / len(demo_sales) * 100, 1),
                    "gross_revenue_usd": round(sum(s["amount"] for s in demo_sales), 2),
                    "net_revenue_usd": round(total_revenue, 2),
                    "avg_order_value_usd": round(avg_order, 2),
                },
                "sales": demo_sales[:20],  # Return first 20 for brevity
                "note": "Showing first 20 of 50 demo sales records",
            }

        params = {}
        if after_date:
            params["after"] = after_date
        if before_date:
            params["before"] = before_date

        response = _gumroad_get("/sales", resolved_key, params)

        if "error" in response:
            return {
                "mode": "demo_fallback",
                "api_error": response["error"],
                **get_gumroad_sales(api_key=None, after_date=after_date, before_date=before_date),
            }

        raw_sales = response.get("sales", [])
        net_sales = [s for s in raw_sales if not s.get("refunded", False)]
        refunds = [s for s in raw_sales if s.get("refunded", False)]
        total_revenue = sum(float(s.get("price", 0)) / 100 for s in net_sales)

        return {
            "mode": "live",
            "date_range": {"after": after_date, "before": before_date},
            "sales_summary": {
                "total_transactions": len(raw_sales),
                "net_sales": len(net_sales),
                "refunds": len(refunds),
                "refund_rate_pct": round(len(refunds) / len(raw_sales) * 100, 1) if raw_sales else 0,
                "net_revenue_usd": round(total_revenue, 2),
            },
            "sales": raw_sales[:50],
        }
    except Exception as e:
        return {"error": str(e)}


def get_gumroad_subscribers(api_key: str | None = None) -> dict:
    """
    Fetch subscriber list from Gumroad.
    Falls back to demo data when no API key.
    """
    try:
        resolved_key = api_key or os.environ.get("GUMROAD_API_KEY", "").strip()

        if not resolved_key:
            return {
                "mode": "demo",
                "notice": "No GUMROAD_API_KEY found — showing demo subscriber data.",
                "subscriber_count": len(DEMO_SUBSCRIBERS),
                "subscribers": DEMO_SUBSCRIBERS,
                "insights": {
                    "list_health": "Small but early-stage — focus on growing past 100 subscribers",
                    "recommendation": "Add a free lead magnet to Gumroad to grow your list faster",
                },
            }

        response = _gumroad_get("/subscribers", resolved_key)

        if "error" in response:
            return {"mode": "demo_fallback", "api_error": response["error"], **get_gumroad_subscribers(api_key=None)}

        raw_subscribers = response.get("subscribers", [])

        return {
            "mode": "live",
            "subscriber_count": len(raw_subscribers),
            "subscribers": raw_subscribers[:50],
            "insights": {
                "list_size": len(raw_subscribers),
                "list_tier": (
                    "Established list (500+)" if len(raw_subscribers) >= 500
                    else "Growing list (100-499)" if len(raw_subscribers) >= 100
                    else "Early list (under 100) — prioritize list building"
                ),
            },
        }
    except Exception as e:
        return {"error": str(e)}


def analyze_gumroad_performance(api_key: str | None = None) -> dict:
    """
    Combine products + sales data for a comprehensive performance report.
    Gracefully uses demo data when no API key is configured.
    """
    try:
        resolved_key = api_key or os.environ.get("GUMROAD_API_KEY", "").strip()
        is_demo = not resolved_key

        products_result = get_gumroad_products(resolved_key if resolved_key else None)
        sales_result = get_gumroad_sales(resolved_key if resolved_key else None)
        subscribers_result = get_gumroad_subscribers(resolved_key if resolved_key else None)

        products = products_result.get("products", [])
        sales_summary = sales_result.get("sales_summary", {})
        subscriber_count = subscribers_result.get("subscriber_count", 0)

        # Top products by revenue
        top_products = sorted(products, key=lambda p: p.get("revenue_usd", 0), reverse=True)[:3]

        # Revenue totals
        total_revenue = products_result.get("total_revenue_usd", 0)
        monthly_revenue = sales_summary.get("net_revenue_usd", 0)
        avg_order_value = sales_summary.get("avg_order_value_usd", 0)
        refund_rate = sales_summary.get("refund_rate_pct", 0)

        # Performance scoring
        scores = {}
        scores["product_diversity"] = min(100, len(products) * 20)
        scores["revenue_health"] = min(100, int(monthly_revenue / 50))
        scores["refund_health"] = max(0, 100 - int(refund_rate * 10))
        scores["subscriber_base"] = min(100, int(subscriber_count / 5))
        overall = int(sum(scores.values()) / len(scores))

        # Recommendations
        recommendations = []

        if len(products) < 3:
            recommendations.append({
                "priority": "HIGH",
                "action": "Create more products",
                "detail": f"You have {len(products)} product(s). Stores with 5+ products earn 3x more than single-product stores.",
            })

        published_products = [p for p in products if p.get("published", True)]
        if len(published_products) < len(products):
            unpublished = len(products) - len(published_products)
            recommendations.append({
                "priority": "MEDIUM",
                "action": f"Publish {unpublished} draft product(s)",
                "detail": "You have unpublished products. Review and publish them to start earning.",
            })

        if refund_rate > 5:
            recommendations.append({
                "priority": "HIGH",
                "action": "Reduce refund rate",
                "detail": f"Your {refund_rate}% refund rate is above the 5% benchmark. Improve product descriptions and add previews.",
            })

        if subscriber_count < 50:
            recommendations.append({
                "priority": "MEDIUM",
                "action": "Build your email list",
                "detail": "Create a free lead magnet (mini-version of a paid product) to grow your subscriber base.",
            })

        # Find gaps
        product_names = [p["name"].lower() for p in products]
        tag_pool = [tag for p in products for tag in p.get("tags", [])]
        unique_categories = list(set(tag_pool))[:5]

        return {
            "mode": "demo" if is_demo else "live",
            "notice": "Showing demo data — set GUMROAD_API_KEY in .env for live analytics." if is_demo else None,
            "performance_overview": {
                "total_products": len(products),
                "published_products": len(published_products),
                "all_time_revenue_usd": total_revenue,
                "recent_period_revenue_usd": monthly_revenue,
                "avg_order_value_usd": avg_order_value,
                "refund_rate_pct": refund_rate,
                "email_subscribers": subscriber_count,
            },
            "health_scores": {
                **scores,
                "overall": overall,
                "grade": "A" if overall >= 85 else "B" if overall >= 70 else "C" if overall >= 55 else "D",
            },
            "top_products": top_products,
            "categories_covered": unique_categories,
            "recommendations": recommendations,
            "quick_wins": [
                "Add 5 more tags to each listing (most Gumroad stores under-tag)",
                "Add a cover image to any product that doesn't have one",
                "Set up a 'Thank You' upsell page to increase AOV",
                "Enable Gumroad's affiliate program to get others selling for you",
                f"Your best product earns ${top_products[0]['revenue_usd'] if top_products else 0} — create a bundle around it",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# JSON Schemas for Claude tool_use
# ---------------------------------------------------------------------------

GUMROAD_TOOL_SCHEMAS: list[dict] = [
    {
        "name": "get_gumroad_products",
        "description": (
            "Fetch all products from the user's Gumroad store. Returns product names, prices, "
            "sales counts, and revenue. Uses live Gumroad API if GUMROAD_API_KEY is set, "
            "otherwise returns realistic demo data. Use this to give the user a store overview."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "api_key": {
                    "type": "string",
                    "description": "Gumroad API key (optional — uses env var if not provided)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_gumroad_sales",
        "description": (
            "Fetch sales data from the Gumroad API for a date range. Returns a sales summary "
            "with revenue, refund rate, and average order value. Supports demo mode."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "api_key": {
                    "type": "string",
                    "description": "Gumroad API key (optional)",
                },
                "after_date": {
                    "type": "string",
                    "description": "Filter sales after this date (YYYY-MM-DD format)",
                },
                "before_date": {
                    "type": "string",
                    "description": "Filter sales before this date (YYYY-MM-DD format)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_gumroad_subscribers",
        "description": (
            "Fetch the email subscriber list from Gumroad. Returns subscriber count and list health insights."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "api_key": {
                    "type": "string",
                    "description": "Gumroad API key (optional)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "analyze_gumroad_performance",
        "description": (
            "Run a comprehensive Gumroad store performance analysis combining products, sales, "
            "and subscriber data. Returns health scores, top products, and prioritized recommendations. "
            "Use this for a full store health check."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "api_key": {
                    "type": "string",
                    "description": "Gumroad API key (optional)",
                },
            },
            "required": [],
        },
    },
]


# ---------------------------------------------------------------------------
# Handler dispatcher
# ---------------------------------------------------------------------------

def handle_gumroad_tool(tool_name: str, tool_input: dict) -> dict | None:
    """Route Gumroad tool calls to the right function."""
    if tool_name == "get_gumroad_products":
        return get_gumroad_products(**tool_input)
    elif tool_name == "get_gumroad_sales":
        return get_gumroad_sales(**tool_input)
    elif tool_name == "get_gumroad_subscribers":
        return get_gumroad_subscribers(**tool_input)
    elif tool_name == "analyze_gumroad_performance":
        return analyze_gumroad_performance(**tool_input)
    return None
