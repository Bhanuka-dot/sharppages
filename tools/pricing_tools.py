"""
Pricing tools for Sharp Pages Selling Bot.
Covers profit margin calculation, pricing strategy, Gumroad fees, and tier structures.
"""

from __future__ import annotations

import math


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def calculate_profit_margin(
    cost: float,
    selling_price: float,
    platform_fee_pct: float = 10.0,
    payment_processing_pct: float = 3.0,
) -> dict:
    """
    Calculate net profit, margin percentage, and break-even units for a product.
    For digital products, 'cost' is typically the time/tool cost amortized per unit.
    """
    try:
        if selling_price <= 0:
            return {"error": "Selling price must be greater than 0"}

        platform_fee = selling_price * (platform_fee_pct / 100)
        processing_fee = selling_price * (payment_processing_pct / 100)
        total_fees = platform_fee + processing_fee
        net_revenue = selling_price - total_fees
        net_profit = net_revenue - cost
        gross_margin_pct = (net_profit / selling_price) * 100
        net_margin_pct = (net_profit / selling_price) * 100  # same for digital

        # Break-even analysis
        if net_profit <= 0:
            break_even_units = "Not applicable — product is not profitable at this price"
            monthly_units_for_1k = "N/A"
            monthly_units_for_5k = "N/A"
        else:
            break_even_units = math.ceil(cost / net_profit) if cost > 0 else 0
            monthly_units_for_1k = math.ceil(1000 / net_profit)
            monthly_units_for_5k = math.ceil(5000 / net_profit)

        # ROI multiple
        roi_multiple = (net_profit / cost) if cost > 0 else float("inf")

        # Annual projections at different sales volumes
        projections = {}
        for units_per_month in [10, 25, 50, 100, 200]:
            monthly = units_per_month * net_profit
            annual = monthly * 12
            projections[f"{units_per_month}_units/month"] = {
                "monthly_profit": round(monthly, 2),
                "annual_profit": round(annual, 2),
            }

        return {
            "selling_price": round(selling_price, 2),
            "cost_per_unit": round(cost, 2),
            "platform_fee": round(platform_fee, 2),
            "platform_fee_pct": platform_fee_pct,
            "processing_fee": round(processing_fee, 2),
            "processing_fee_pct": payment_processing_pct,
            "total_fees": round(total_fees, 2),
            "net_revenue_per_sale": round(net_revenue, 2),
            "net_profit_per_sale": round(net_profit, 2),
            "gross_margin_pct": round(gross_margin_pct, 1),
            "roi_multiple": round(roi_multiple, 1) if isinstance(roi_multiple, float) and roi_multiple != float("inf") else "Infinite (zero cost)",
            "break_even_units": break_even_units,
            "units_needed_for_1k_monthly": monthly_units_for_1k,
            "units_needed_for_5k_monthly": monthly_units_for_5k,
            "revenue_projections": projections,
            "margin_assessment": (
                "Excellent (80%+)" if gross_margin_pct >= 80
                else "Good (60-80%)" if gross_margin_pct >= 60
                else "Acceptable (40-60%)" if gross_margin_pct >= 40
                else "Poor — consider raising price or reducing costs"
            ),
        }
    except Exception as e:
        return {"error": str(e)}


def suggest_pricing_strategy(
    product_type: str,
    competitor_price_range: str,
    perceived_value: str = "medium",
    target_margin: float = 75.0,
) -> dict:
    """
    Return recommended price points, tiering suggestions, and psychological pricing tips.
    """
    try:
        # Parse competitor price range (e.g., "$9-$27" or "9-27")
        price_range_clean = competitor_price_range.replace("$", "").replace(",", "")
        try:
            parts = [p.strip() for p in price_range_clean.split("-")]
            comp_low = float(parts[0])
            comp_high = float(parts[1]) if len(parts) > 1 else float(parts[0]) * 2
        except (ValueError, IndexError):
            comp_low = 15.0
            comp_high = 47.0

        comp_mid = (comp_low + comp_high) / 2

        # Perceived value multipliers
        value_multipliers = {
            "low": 0.8,
            "medium": 1.0,
            "high": 1.3,
            "premium": 1.7,
        }
        multiplier = value_multipliers.get(perceived_value.lower(), 1.0)

        # Psychological price points (end in 7, 9, or .00 for premium)
        def psych_price(raw: float) -> float:
            """Round to the nearest psychological price point."""
            if raw < 5:
                return round(raw, 2)
            elif raw < 10:
                return min([4.99, 7.00, 9.00, 9.99], key=lambda x: abs(x - raw))
            elif raw < 20:
                return min([12.00, 14.99, 17.00, 19.00], key=lambda x: abs(x - raw))
            elif raw < 30:
                return min([22.00, 24.99, 27.00, 29.00], key=lambda x: abs(x - raw))
            elif raw < 50:
                return min([37.00, 39.00, 44.99, 47.00, 49.00], key=lambda x: abs(x - raw))
            elif raw < 100:
                return min([57.00, 67.00, 77.00, 87.00, 97.00], key=lambda x: abs(x - raw))
            else:
                return min([97.00, 127.00, 147.00, 197.00, 247.00], key=lambda x: abs(x - raw))

        # Price point recommendations
        budget_price = psych_price(comp_low * multiplier)
        standard_price = psych_price(comp_mid * multiplier)
        premium_price = psych_price(comp_high * 1.2 * multiplier)

        # Positioning strategies
        positioning = {
            "penetration": {
                "price": budget_price,
                "rationale": f"Enter at ${budget_price} — below market average to build reviews and sales velocity",
                "when_to_use": "New product with no social proof; prioritize reviews over profit",
                "risk": "May attract bargain hunters who don't value your work",
            },
            "competitive": {
                "price": standard_price,
                "rationale": f"Price at ${standard_price} — in line with market, compete on quality",
                "when_to_use": "Established niche, you have at least 5 reviews",
                "risk": "Competing head-to-head requires strong differentiation",
            },
            "premium": {
                "price": premium_price,
                "rationale": f"Price at ${premium_price} — above market average to signal premium quality",
                "when_to_use": "Strong brand, 20+ reviews, demonstrable superiority over competitors",
                "risk": "Higher price requires stronger social proof and better listing copy",
            },
        }

        # Recommended strategy based on perceived value
        if perceived_value.lower() in ["high", "premium"]:
            recommendation = "premium"
            recommended_price = premium_price
        elif perceived_value.lower() == "low":
            recommendation = "penetration"
            recommended_price = budget_price
        else:
            recommendation = "competitive"
            recommended_price = standard_price

        return {
            "product_type": product_type,
            "competitor_price_range": competitor_price_range,
            "perceived_value": perceived_value,
            "price_points": positioning,
            "recommended_strategy": recommendation,
            "recommended_price": recommended_price,
            "psychological_pricing_tips": [
                "Prices ending in 7 (e.g., $17, $47) convert better than round numbers for digital products",
                "$X.99 feels 'cheap' — use $X.00 or $X7 for positioning above $10",
                "Showing a crossed-out 'original price' increases conversions by 15-25%",
                "A middle price tier makes the top tier feel like better value (decoy effect)",
                f"$27 is a sweet spot for digital templates — impulse buy threshold",
                "Avoid pricing below $9 — it signals low quality and attracts refund-seekers",
            ],
            "pricing_test_plan": [
                f"Week 1-2: Launch at ${budget_price} to generate first sales + reviews",
                f"Week 3-4: Raise to ${standard_price} once you have 3+ reviews",
                f"Month 2+: Test ${premium_price} if reviews are strong and sales are consistent",
                "A/B test: Run the same product at two prices for 2 weeks, compare conversion rate",
            ],
            "launch_discount_strategy": {
                "launch_price": budget_price,
                "regular_price": standard_price,
                "discount_pct": round((1 - budget_price / standard_price) * 100),
                "duration": "First 7-14 days only",
                "messaging": f"Launch price: ${budget_price} (regularly ${standard_price}) — grab it before the price goes up!",
            },
        }
    except Exception as e:
        return {"error": str(e)}


def calculate_gumroad_fees(price: float) -> dict:
    """
    Calculate Gumroad's fee structure and net earnings at a given price.
    Uses Gumroad's current fee structure (as of 2024-2025).
    """
    try:
        if price <= 0:
            return {"error": "Price must be greater than 0"}

        # Gumroad's current fee structure (as of 2025)
        # Gumroad charges a flat 10% on all sales
        # Plus payment processing (Stripe/PayPal): ~3% + $0.30
        gumroad_fee_pct = 10.0
        gumroad_fee = price * (gumroad_fee_pct / 100)

        # Payment processing
        stripe_pct = 2.9
        stripe_fixed = 0.30
        stripe_fee = (price * (stripe_pct / 100)) + stripe_fixed

        # PayPal (slightly different)
        paypal_pct = 3.49
        paypal_fixed = 0.49
        paypal_fee = (price * (paypal_pct / 100)) + paypal_fixed

        # Net earnings
        net_stripe = price - gumroad_fee - stripe_fee
        net_paypal = price - gumroad_fee - paypal_fee

        # Compare to Gumroad Pro (if they had it - $10/mo) - now just the flat 10%
        # Etsy comparison
        etsy_listing_fee = 0.20
        etsy_transaction_fee = price * 0.065
        etsy_payment_pct = price * 0.03 + 0.25
        net_etsy = price - etsy_listing_fee - etsy_transaction_fee - etsy_payment_pct

        # Volume projections
        volume_projections = {}
        for units in [10, 25, 50, 100, 200, 500]:
            gross = price * units
            total_gumroad = gumroad_fee * units
            total_processing = stripe_fee * units
            net = net_stripe * units
            volume_projections[f"{units}_sales"] = {
                "gross_revenue": round(gross, 2),
                "gumroad_fees_total": round(total_gumroad, 2),
                "processing_fees_total": round(total_processing, 2),
                "net_earnings": round(net, 2),
            }

        return {
            "product_price": round(price, 2),
            "gumroad_fee_structure": {
                "platform_fee": f"10% flat on all sales",
                "gumroad_cut": round(gumroad_fee, 2),
            },
            "payment_processing": {
                "stripe": {
                    "rate": f"{stripe_pct}% + ${stripe_fixed}",
                    "fee": round(stripe_fee, 2),
                    "net_earnings": round(net_stripe, 2),
                },
                "paypal": {
                    "rate": f"{paypal_pct}% + ${paypal_fixed}",
                    "fee": round(paypal_fee, 2),
                    "net_earnings": round(net_paypal, 2),
                },
            },
            "best_case_net": round(net_stripe, 2),
            "total_fee_pct_stripe": round(((price - net_stripe) / price) * 100, 1),
            "platform_comparison": {
                "gumroad_net": round(net_stripe, 2),
                "etsy_net": round(net_etsy, 2),
                "winner": "Gumroad" if net_stripe > net_etsy else "Etsy",
                "difference": round(abs(net_stripe - net_etsy), 2),
                "note": "Etsy has listing fees per item; Gumroad is free to list",
            },
            "volume_projections": volume_projections,
            "tax_reminder": (
                "Remember: These are pre-tax figures. Set aside 25-30% of net earnings "
                "for self-employment taxes (US) or your local equivalent."
            ),
            "tips_to_maximize_net": [
                "At prices above $5, Gumroad's 10% is competitive vs Etsy (6.5% + more fees)",
                "Use Stripe (not PayPal) for slightly lower processing fees above $10",
                "Gumroad handles VAT/sales tax collection automatically — a big time saver",
                "Bundle products to increase average order value and reduce per-unit fee impact",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


def create_pricing_tiers(
    base_product: str,
    add_ons: list[str],
) -> dict:
    """
    Create a Good / Better / Best pricing tier structure with add-ons.
    Returns tier structure, psychological rationale, and implementation tips.
    """
    try:
        if not add_ons:
            return {"error": "Please provide at least 1-3 add-on items to create tiers"}

        # Build tier contents
        good_tier_items = [base_product]
        better_tier_items = [base_product] + add_ons[:min(2, len(add_ons))]
        best_tier_items = [base_product] + add_ons

        # Pricing logic
        # Good: baseline impulse buy
        # Better: ~65% of Good+Better value (25% discount)
        # Best: ~55% of all items (35-40% discount)
        good_price = 17.0
        better_add_value = 12.0 * len(better_tier_items[1:])
        better_raw = good_price + better_add_value
        better_price = max(27.0, round(better_raw * 0.8 / 10) * 10 - 3)

        best_add_value = 10.0 * len(best_tier_items[1:])
        best_raw = good_price + best_add_value * 1.5
        best_price = max(47.0, round(best_raw * 0.75 / 10) * 10 - 3)

        tiers = {
            "good": {
                "tier_name": "Starter",
                "price": good_price,
                "includes": good_tier_items,
                "target_buyer": "Budget-conscious buyers or those unsure about buying",
                "positioning": "The essentials — everything you need to get started",
                "conversion_role": "Entry point — converts hesitant buyers",
                "percentage_of_buyers": "30-40% typically choose this tier",
            },
            "better": {
                "tier_name": "Professional",
                "price": better_price,
                "includes": better_tier_items,
                "savings_vs_individual": round(good_price + better_add_value - better_price, 2),
                "target_buyer": "Serious buyers who want more without paying top dollar",
                "positioning": "The smart choice — most popular for good reason",
                "conversion_role": "Most popular tier — should be your 'best value' pick",
                "percentage_of_buyers": "45-55% typically choose this tier",
                "recommended_label": "MOST POPULAR",
            },
            "best": {
                "tier_name": "Ultimate",
                "price": best_price,
                "includes": best_tier_items,
                "savings_vs_individual": round(good_price + best_add_value * 1.5 - best_price, 2),
                "target_buyer": "Power users and those who want everything",
                "positioning": "The complete package — zero compromises",
                "conversion_role": "High-ticket anchor — makes middle tier look affordable",
                "percentage_of_buyers": "15-25% typically choose this tier",
                "recommended_label": "BEST VALUE",
            },
        }

        # Gumroad implementation
        gumroad_implementation = [
            f"Create 3 separate Gumroad listings: '{base_product} Starter', '{base_product} Pro', '{base_product} Ultimate'",
            "OR use Gumroad's 'Variants' feature to offer tiers within one listing",
            "Clearly list included items in each tier's description",
            "Put 'MOST POPULAR' badge next to the middle tier to guide buyers",
            "Use the 'Suggested Price' feature to anchor buyers toward higher tiers",
        ]

        avg_revenue_per_buyer = (
            good_price * 0.35 + better_price * 0.50 + best_price * 0.15
        )

        return {
            "base_product": base_product,
            "add_ons": add_ons,
            "tiers": tiers,
            "expected_avg_revenue_per_buyer": round(avg_revenue_per_buyer, 2),
            "vs_single_price_at_good": {
                "single_price_per_buyer": good_price,
                "tiered_price_per_buyer": round(avg_revenue_per_buyer, 2),
                "revenue_uplift": round(avg_revenue_per_buyer - good_price, 2),
                "uplift_pct": round((avg_revenue_per_buyer / good_price - 1) * 100),
            },
            "gumroad_implementation": gumroad_implementation,
            "psychological_principles": [
                "Anchoring: The 'Best' tier makes 'Better' look like a deal",
                "Decoy effect: Middle tier is designed to win",
                "Loss aversion: 'MOST POPULAR' triggers fear of missing out",
                "Price bracketing: Low entry creates less resistance than a single medium price",
                "Choice architecture: Three options is the optimal number — four+ causes paralysis",
            ],
            "upsell_copy_template": (
                f"Most customers upgrade to {base_product} Pro — it includes "
                f"{', '.join(add_ons[:2])} for only ${better_price - good_price} more. "
                f"Click here to upgrade before you download."
            ),
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# JSON Schemas for Claude tool_use
# ---------------------------------------------------------------------------

PRICING_TOOL_SCHEMAS: list[dict] = [
    {
        "name": "calculate_profit_margin",
        "description": (
            "Calculate net profit, gross margin percentage, break-even units, and revenue "
            "projections for a digital product. Use this when a user wants to understand "
            "their profitability at a given price point."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "cost": {
                    "type": "number",
                    "description": "Cost per unit in USD (for digital products: amortized creation cost, e.g., $2 if you spent 2 hours creating it and value your time at $1/hr amortized over 100 sales)",
                },
                "selling_price": {
                    "type": "number",
                    "description": "Selling price in USD",
                },
                "platform_fee_pct": {
                    "type": "number",
                    "description": "Platform fee percentage (default 10 for Gumroad)",
                },
                "payment_processing_pct": {
                    "type": "number",
                    "description": "Payment processing fee percentage (default 3 for Stripe)",
                },
            },
            "required": ["cost", "selling_price"],
        },
    },
    {
        "name": "suggest_pricing_strategy",
        "description": (
            "Suggest optimal price points and a pricing strategy based on competitor prices "
            "and perceived value. Returns three positioning strategies (penetration/competitive/premium), "
            "psychological pricing tips, and a launch discount plan."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_type": {
                    "type": "string",
                    "description": "Type of product (e.g., 'Notion template', 'eBook', 'Canva template bundle')",
                },
                "competitor_price_range": {
                    "type": "string",
                    "description": "Price range of competing products, e.g. '$9-$27' or '$15-$47'",
                },
                "perceived_value": {
                    "type": "string",
                    "description": "How valuable your product is vs competitors: low, medium, high, or premium",
                    "enum": ["low", "medium", "high", "premium"],
                },
                "target_margin": {
                    "type": "number",
                    "description": "Your target profit margin percentage (default 75)",
                },
            },
            "required": ["product_type", "competitor_price_range"],
        },
    },
    {
        "name": "calculate_gumroad_fees",
        "description": (
            "Calculate Gumroad's exact fee structure and your net earnings at a given price. "
            "Compares Stripe vs PayPal processing, volume projections, and Gumroad vs Etsy. "
            "Use this when a user wants to know how much they'll actually earn per sale."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "price": {
                    "type": "number",
                    "description": "Product selling price in USD",
                },
            },
            "required": ["price"],
        },
    },
    {
        "name": "create_pricing_tiers",
        "description": (
            "Create a Good/Better/Best (Starter/Professional/Ultimate) pricing tier structure. "
            "Returns tier contents, prices, buyer percentages, conversion rationale, and "
            "Gumroad implementation tips. Use this to maximize average order value."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "base_product": {
                    "type": "string",
                    "description": "The core product that goes in every tier (e.g., 'Monthly Budget Tracker')",
                },
                "add_ons": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Additional items to include in higher tiers (e.g., ['Weekly Review Template', 'Year-in-Review Dashboard', 'Video Tutorial'])",
                },
            },
            "required": ["base_product", "add_ons"],
        },
    },
]


# ---------------------------------------------------------------------------
# Handler dispatcher
# ---------------------------------------------------------------------------

def handle_pricing_tool(tool_name: str, tool_input: dict) -> dict | None:
    """Route pricing tool calls to the right function."""
    if tool_name == "calculate_profit_margin":
        return calculate_profit_margin(**tool_input)
    elif tool_name == "suggest_pricing_strategy":
        return suggest_pricing_strategy(**tool_input)
    elif tool_name == "calculate_gumroad_fees":
        return calculate_gumroad_fees(**tool_input)
    elif tool_name == "create_pricing_tiers":
        return create_pricing_tiers(**tool_input)
    return None
