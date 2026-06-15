"""
Analytics tools for Sharp Pages Selling Bot.
Covers sales performance analysis, revenue goal calculation, KPI dashboards, and forecasting.
"""

from __future__ import annotations

import math
from typing import Any


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def analyze_sales_performance(sales_data: list[dict]) -> dict:
    """
    Analyze a list of sales records and return revenue summary, best sellers,
    trends, and recommendations.

    sales_data: list of dicts with keys like:
        - product_name (str)
        - amount (float)
        - date (str, optional)
        - refunded (bool, optional)
    """
    try:
        if not sales_data:
            return {"error": "sales_data cannot be empty"}

        # Normalize and calculate
        total_sales = len(sales_data)
        refunds = sum(1 for s in sales_data if s.get("refunded", False))
        net_sales = total_sales - refunds

        amounts = [float(s.get("amount", 0)) for s in sales_data if not s.get("refunded", False)]
        gross_revenue = sum(float(s.get("amount", 0)) for s in sales_data)
        refund_amount = sum(float(s.get("amount", 0)) for s in sales_data if s.get("refunded", False))
        net_revenue = gross_revenue - refund_amount

        avg_order_value = net_revenue / net_sales if net_sales > 0 else 0
        refund_rate = (refunds / total_sales * 100) if total_sales > 0 else 0

        # Product breakdown
        product_sales: dict[str, dict] = {}
        for sale in sales_data:
            pname = sale.get("product_name", "Unknown Product")
            if pname not in product_sales:
                product_sales[pname] = {"units": 0, "revenue": 0.0, "refunds": 0}
            if sale.get("refunded", False):
                product_sales[pname]["refunds"] += 1
            else:
                product_sales[pname]["units"] += 1
                product_sales[pname]["revenue"] += float(sale.get("amount", 0))

        # Sort by revenue
        best_sellers = sorted(
            [
                {
                    "product": p,
                    "units_sold": d["units"],
                    "revenue": round(d["revenue"], 2),
                    "avg_price": round(d["revenue"] / d["units"], 2) if d["units"] > 0 else 0,
                    "refund_rate_pct": round(d["refunds"] / (d["units"] + d["refunds"]) * 100, 1) if (d["units"] + d["refunds"]) > 0 else 0,
                }
                for p, d in product_sales.items()
            ],
            key=lambda x: x["revenue"],
            reverse=True,
        )

        # Revenue tiers
        if net_revenue >= 5000:
            revenue_tier = "Strong ($5k+/period)"
        elif net_revenue >= 1000:
            revenue_tier = "Growing ($1k-$5k/period)"
        elif net_revenue >= 500:
            revenue_tier = "Early Stage ($500-$1k/period)"
        else:
            revenue_tier = "Starting Out (under $500/period)"

        # Recommendations
        recommendations = []

        # Refund rate check
        if refund_rate > 10:
            recommendations.append({
                "priority": "HIGH",
                "area": "Product Quality / Expectations",
                "issue": f"Refund rate of {refund_rate:.1f}% is too high (target: under 5%)",
                "action": "Review your product description — it may be setting wrong expectations. Add more screenshots and a demo.",
            })
        elif refund_rate > 5:
            recommendations.append({
                "priority": "MEDIUM",
                "area": "Customer Experience",
                "issue": f"Refund rate of {refund_rate:.1f}% is above target",
                "action": "Add a setup guide and FAQ to reduce buyer regret and confusion.",
            })
        else:
            recommendations.append({
                "priority": "INFO",
                "area": "Refund Rate",
                "issue": f"Refund rate of {refund_rate:.1f}% is healthy",
                "action": "Keep doing what you're doing — accurate product descriptions and good customer support.",
            })

        # AOV analysis
        if avg_order_value < 15:
            recommendations.append({
                "priority": "MEDIUM",
                "area": "Pricing / AOV",
                "issue": f"Average order value (${avg_order_value:.2f}) is below optimal",
                "action": "Introduce pricing tiers or bundles. Consider raising base price to $17-$27.",
            })
        elif avg_order_value > 40:
            recommendations.append({
                "priority": "INFO",
                "area": "AOV",
                "issue": f"Strong average order value (${avg_order_value:.2f})",
                "action": "You're well-positioned. Consider a premium tier at 2x current AOV.",
            })

        # Best seller insight
        if best_sellers:
            top = best_sellers[0]
            recommendations.append({
                "priority": "OPPORTUNITY",
                "area": "Product Strategy",
                "issue": f"'{top['product']}' is your top earner at ${top['revenue']}",
                "action": f"Create a sequel, bundle, or 'pro version' of '{top['product']}' — your proven winner.",
            })

        # Units needed for $5k/month
        units_for_5k = math.ceil(5000 / avg_order_value) if avg_order_value > 0 else "N/A"

        return {
            "summary": {
                "total_transactions": total_sales,
                "net_sales": net_sales,
                "refunds": refunds,
                "gross_revenue": round(gross_revenue, 2),
                "net_revenue": round(net_revenue, 2),
                "avg_order_value": round(avg_order_value, 2),
                "refund_rate_pct": round(refund_rate, 1),
                "revenue_tier": revenue_tier,
            },
            "best_sellers": best_sellers[:5],
            "recommendations": recommendations,
            "growth_targets": {
                "units_needed_for_1k_month": math.ceil(1000 / avg_order_value) if avg_order_value > 0 else "N/A",
                "units_needed_for_5k_month": units_for_5k,
                "units_needed_for_10k_month": math.ceil(10000 / avg_order_value) if avg_order_value > 0 else "N/A",
            },
            "data_limitations": "For trend analysis, provide sales with 'date' fields. This analysis covers the provided data as a single cohort.",
        }
    except Exception as e:
        return {"error": str(e)}


def calculate_monthly_revenue_goal(
    target_monthly_revenue: float,
    avg_product_price: float,
    conversion_rate: float = 2.0,
) -> dict:
    """
    Calculate how much traffic and how many units are needed to hit a monthly revenue goal.
    """
    try:
        if avg_product_price <= 0:
            return {"error": "avg_product_price must be greater than 0"}
        if conversion_rate <= 0 or conversion_rate > 100:
            return {"error": "conversion_rate must be between 0.01 and 100"}

        units_needed = math.ceil(target_monthly_revenue / avg_product_price)
        traffic_needed = math.ceil(units_needed / (conversion_rate / 100))
        daily_traffic = math.ceil(traffic_needed / 30)
        daily_sales = units_needed / 30

        # What-if scenarios at different conversion rates
        conversion_scenarios = {}
        for cr in [1.0, 2.0, 3.0, 5.0]:
            traffic = math.ceil(units_needed / (cr / 100))
            conversion_scenarios[f"{cr}%_conversion"] = {
                "monthly_traffic_needed": traffic,
                "daily_traffic_needed": math.ceil(traffic / 30),
                "monthly_sales_needed": units_needed,
            }

        # Traffic sources breakdown (suggested)
        traffic_sources = {
            "pinterest_organic": {
                "target_pct": 50,
                "monthly_visits": math.ceil(traffic_needed * 0.50),
                "how_to_achieve": f"Pin 5-10x/day for 90 days. Focus on '{avg_product_price:.0f}' price point keywords.",
                "timeline_to_results": "3-6 months for compound growth",
            },
            "google_seo": {
                "target_pct": 25,
                "monthly_visits": math.ceil(traffic_needed * 0.25),
                "how_to_achieve": "Publish 2x blog posts/week targeting long-tail keywords",
                "timeline_to_results": "6-12 months",
            },
            "email_list": {
                "target_pct": 15,
                "monthly_visits": math.ceil(traffic_needed * 0.15),
                "how_to_achieve": "Build list with a free lead magnet; nurture with weekly emails",
                "timeline_to_results": "Immediate (list converts at 3-5x higher than cold traffic)",
            },
            "social_media": {
                "target_pct": 10,
                "monthly_visits": math.ceil(traffic_needed * 0.10),
                "how_to_achieve": "Consistent Instagram/TikTok posting with clear CTA to bio link",
                "timeline_to_results": "1-3 months",
            },
        }

        # Action plan
        action_plan = [
            f"Step 1: Optimize your Gumroad listing for conversion — even 1% improvement = {math.ceil(units_needed * 0.01)} more sales/month",
            f"Step 2: Set up Pinterest account + start pinning daily — target {traffic_sources['pinterest_organic']['monthly_visits']:,} monthly Pinterest visits",
            f"Step 3: Create a free lead magnet to build your email list — email converts at 3-5% vs 1-2% cold",
            f"Step 4: Publish 2 SEO-targeted blog posts/week to compound organic traffic",
            f"Step 5: Once hitting 50% of goal, raise price by 20% — improves revenue without volume increase",
        ]

        # Financial projection
        current_monthly = avg_product_price * 0  # assume starting from 0 for now
        months_to_goal = {
            "optimistic": math.ceil(target_monthly_revenue / (avg_product_price * 10)),
            "realistic": math.ceil(target_monthly_revenue / (avg_product_price * 5)),
            "conservative": math.ceil(target_monthly_revenue / (avg_product_price * 2)),
        }

        return {
            "target_monthly_revenue": target_monthly_revenue,
            "avg_product_price": avg_product_price,
            "units_to_sell_per_month": units_needed,
            "units_per_day": round(daily_sales, 1),
            "conversion_rate_assumption": f"{conversion_rate}%",
            "traffic_needed_monthly": traffic_needed,
            "traffic_needed_daily": daily_traffic,
            "conversion_rate_scenarios": conversion_scenarios,
            "traffic_source_breakdown": traffic_sources,
            "action_plan": action_plan,
            "milestones": {
                "25_pct_goal": {
                    "target": round(target_monthly_revenue * 0.25, 2),
                    "units": math.ceil(units_needed * 0.25),
                    "celebration": "First milestone — you have proof of concept",
                },
                "50_pct_goal": {
                    "target": round(target_monthly_revenue * 0.50, 2),
                    "units": math.ceil(units_needed * 0.50),
                    "celebration": "Halfway there — time to raise price by 10%",
                },
                "100_pct_goal": {
                    "target": target_monthly_revenue,
                    "units": units_needed,
                    "celebration": "Goal achieved — now launch product #2",
                },
            },
        }
    except Exception as e:
        return {"error": str(e)}


def create_kpi_dashboard(
    product_count: int,
    monthly_revenue: float,
    avg_order_value: float,
    refund_rate: float = 3.0,
) -> dict:
    """
    Create a KPI health dashboard with scores and benchmarks.
    """
    try:
        # Scoring functions (0-100 each)
        def score_revenue(rev: float) -> tuple[int, str]:
            if rev >= 10000:
                return 100, "Excellent — $10k+/month"
            elif rev >= 5000:
                return 80, "Strong — $5k-$10k/month"
            elif rev >= 2000:
                return 60, "Growing — $2k-$5k/month"
            elif rev >= 500:
                return 40, "Early — $500-$2k/month"
            else:
                return 20, "Starting out — under $500/month"

        def score_aov(aov: float) -> tuple[int, str]:
            if aov >= 50:
                return 100, "Premium AOV (>$50)"
            elif aov >= 30:
                return 80, "Good AOV ($30-$50)"
            elif aov >= 15:
                return 60, "Moderate AOV ($15-$30)"
            elif aov >= 7:
                return 40, "Low AOV ($7-$15)"
            else:
                return 20, "Very Low AOV (<$7) — raise prices"

        def score_refund_rate(rate: float) -> tuple[int, str]:
            if rate <= 2:
                return 100, "Excellent (<2%)"
            elif rate <= 5:
                return 80, "Good (2-5%)"
            elif rate <= 8:
                return 60, "Acceptable (5-8%)"
            elif rate <= 12:
                return 40, "Concerning (8-12%)"
            else:
                return 20, "Critical (>12%) — investigate immediately"

        def score_product_count(count: int) -> tuple[int, str]:
            if count >= 10:
                return 100, "Diversified portfolio (10+ products)"
            elif count >= 5:
                return 75, "Good range (5-9 products)"
            elif count >= 2:
                return 50, "Starting range (2-4 products)"
            else:
                return 25, "Single product — high concentration risk"

        rev_score, rev_label = score_revenue(monthly_revenue)
        aov_score, aov_label = score_aov(avg_order_value)
        refund_score, refund_label = score_refund_rate(refund_rate)
        product_score, product_label = score_product_count(product_count)

        overall_score = int((rev_score + aov_score + refund_score + product_score) / 4)

        # Overall grade
        if overall_score >= 85:
            overall_grade = "A — Thriving Business"
        elif overall_score >= 70:
            overall_grade = "B — Growing Well"
        elif overall_score >= 55:
            overall_grade = "C — On Track, Needs Focus"
        elif overall_score >= 40:
            overall_grade = "D — Needs Significant Work"
        else:
            overall_grade = "F — Critical Issues to Address"

        # Revenue per product
        revenue_per_product = monthly_revenue / product_count if product_count > 0 else 0
        units_sold_est = math.ceil(monthly_revenue / avg_order_value) if avg_order_value > 0 else 0

        # Industry benchmarks
        benchmarks = {
            "monthly_revenue": {
                "your_value": monthly_revenue,
                "beginner_benchmark": "$0-$500",
                "intermediate_benchmark": "$500-$3,000",
                "advanced_benchmark": "$3,000-$10,000",
                "expert_benchmark": "$10,000+",
            },
            "avg_order_value": {
                "your_value": avg_order_value,
                "digital_templates": "$15-$30 typical",
                "ebooks_guides": "$10-$47 typical",
                "courses_premium": "$47-$297 typical",
                "notion_templates": "$9-$27 typical",
            },
            "refund_rate": {
                "your_value": f"{refund_rate}%",
                "excellent": "<2%",
                "good": "2-5%",
                "acceptable": "5-8%",
                "problem": ">8%",
            },
        }

        # Recommended focus areas (lowest-scoring KPIs first)
        kpi_priority = sorted([
            ("Monthly Revenue", rev_score, "Increase traffic and conversions"),
            ("Average Order Value", aov_score, "Raise prices or create bundles"),
            ("Refund Rate", refund_score, "Improve product quality and descriptions"),
            ("Product Portfolio", product_score, "Create additional products"),
        ], key=lambda x: x[1])

        recommendations = []
        for kpi, score, action in kpi_priority[:2]:  # Focus on bottom 2
            if score < 70:
                recommendations.append(f"Priority: {kpi} (score: {score}/100) — {action}")

        return {
            "overall_score": overall_score,
            "overall_grade": overall_grade,
            "kpis": {
                "monthly_revenue": {
                    "value": monthly_revenue,
                    "score": rev_score,
                    "label": rev_label,
                },
                "avg_order_value": {
                    "value": avg_order_value,
                    "score": aov_score,
                    "label": aov_label,
                },
                "refund_rate": {
                    "value": f"{refund_rate}%",
                    "score": refund_score,
                    "label": refund_label,
                },
                "product_count": {
                    "value": product_count,
                    "score": product_score,
                    "label": product_label,
                },
            },
            "derived_metrics": {
                "revenue_per_product": round(revenue_per_product, 2),
                "estimated_units_sold": units_sold_est,
                "annual_run_rate": round(monthly_revenue * 12, 2),
                "est_net_after_fees": round(monthly_revenue * 0.87, 2),
            },
            "benchmarks": benchmarks,
            "priority_recommendations": recommendations,
            "next_milestone": {
                "target_revenue": monthly_revenue * 2,
                "description": f"Double current revenue to ${monthly_revenue * 2:,.0f}/month",
                "key_lever": kpi_priority[0][2] if kpi_priority else "Keep optimizing",
            },
        }
    except Exception as e:
        return {"error": str(e)}


def forecast_revenue(
    historical_data: list[dict],
    growth_rate: float = 10.0,
    months_ahead: int = 6,
) -> dict:
    """
    Forecast revenue projections based on historical data and a growth rate.

    historical_data: list of dicts with keys:
        - month (str, e.g., "Jan 2025")
        - revenue (float)
    growth_rate: monthly growth rate percentage
    months_ahead: how many months to forecast
    """
    try:
        if not historical_data:
            return {"error": "historical_data cannot be empty"}

        if months_ahead < 1 or months_ahead > 24:
            return {"error": "months_ahead must be between 1 and 24"}

        revenues = [float(d.get("revenue", 0)) for d in historical_data]
        months = [d.get("month", f"Month {i+1}") for i, d in enumerate(historical_data)]

        avg_historical = sum(revenues) / len(revenues)
        latest_revenue = revenues[-1] if revenues else 0

        # Calculate actual growth rate from historical data (if 2+ points)
        if len(revenues) >= 2:
            calculated_growth = ((revenues[-1] / revenues[0]) ** (1 / len(revenues)) - 1) * 100
            actual_growth_display = f"{calculated_growth:.1f}%/month (calculated from your data)"
        else:
            calculated_growth = growth_rate
            actual_growth_display = f"{growth_rate}% assumed (insufficient data to calculate)"

        # Use the provided growth rate for forecasting
        growth_multiplier = 1 + (growth_rate / 100)

        # Forecast
        forecasted_months = []
        base = latest_revenue
        cumulative = 0

        # Try to determine next month name
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        for i in range(1, months_ahead + 1):
            projected = base * (growth_multiplier ** i)
            cumulative += projected

            # Scenarios
            optimistic = projected * 1.3
            conservative = projected * 0.7

            forecasted_months.append({
                "month_ahead": i,
                "label": f"Month +{i}",
                "projected_revenue": round(projected, 2),
                "optimistic_revenue": round(optimistic, 2),
                "conservative_revenue": round(conservative, 2),
                "vs_current": f"+{round((projected / latest_revenue - 1) * 100, 1)}%" if latest_revenue > 0 else "N/A",
            })

        total_forecasted = sum(m["projected_revenue"] for m in forecasted_months)
        total_optimistic = sum(m["optimistic_revenue"] for m in forecasted_months)
        total_conservative = sum(m["conservative_revenue"] for m in forecasted_months)

        # Milestones
        milestones = []
        for m in forecasted_months:
            for threshold in [1000, 2500, 5000, 10000]:
                if latest_revenue < threshold <= m["projected_revenue"]:
                    milestones.append({
                        "milestone": f"${threshold:,}/month",
                        "projected_month": m["label"],
                        "projected_revenue": m["projected_revenue"],
                    })

        # Revenue acceleration tips
        acceleration_tips = [
            f"At {growth_rate}% monthly growth, you'll earn ${total_forecasted:,.0f} over the next {months_ahead} months",
            "Adding a second product typically increases revenue 30-50% within 60 days",
            "Raising your price by 15% while maintaining volume boosts revenue 15% instantly",
            "A Pinterest traffic spike (from viral pin) can double a month's revenue temporarily",
            f"Email list of 1,000+ subscribers can add ${avg_historical * 0.3:,.0f}/month via promo emails",
        ]

        return {
            "historical_summary": {
                "months_analyzed": len(historical_data),
                "earliest_month": months[0] if months else "N/A",
                "latest_month": months[-1] if months else "N/A",
                "avg_monthly_revenue": round(avg_historical, 2),
                "latest_monthly_revenue": round(latest_revenue, 2),
                "historical_growth_rate": actual_growth_display,
            },
            "forecast_settings": {
                "growth_rate_applied": f"{growth_rate}% per month",
                "months_forecast": months_ahead,
                "methodology": "Compound monthly growth from latest baseline",
            },
            "monthly_forecast": forecasted_months,
            "totals": {
                "conservative_total": round(total_conservative, 2),
                "projected_total": round(total_forecasted, 2),
                "optimistic_total": round(total_optimistic, 2),
                "period": f"Next {months_ahead} months",
            },
            "milestones_projected": milestones if milestones else [{"note": "No new milestones at this growth rate in the forecast window"}],
            "acceleration_insights": acceleration_tips,
            "caveat": (
                f"Forecasts assume consistent {growth_rate}% monthly growth. "
                "Actual results depend on traffic, conversion rate, pricing changes, and new product launches."
            ),
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# JSON Schemas for Claude tool_use
# ---------------------------------------------------------------------------

ANALYTICS_TOOL_SCHEMAS: list[dict] = [
    {
        "name": "analyze_sales_performance",
        "description": (
            "Analyze a set of sales records to produce a revenue summary, best-seller rankings, "
            "refund rate, average order value, and actionable recommendations. "
            "Pass a list of sales with product_name, amount, and optional date/refunded fields."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sales_data": {
                    "type": "array",
                    "description": "List of sales records",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_name": {"type": "string"},
                            "amount": {"type": "number"},
                            "date": {"type": "string"},
                            "refunded": {"type": "boolean"},
                        },
                        "required": ["product_name", "amount"],
                    },
                },
            },
            "required": ["sales_data"],
        },
    },
    {
        "name": "calculate_monthly_revenue_goal",
        "description": (
            "Calculate traffic, daily sales, and action steps needed to hit a monthly revenue goal. "
            "Returns traffic breakdown by source, conversion scenarios, and a milestone plan. "
            "Use when a user sets a revenue target and wants to know how to reach it."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "target_monthly_revenue": {
                    "type": "number",
                    "description": "Monthly revenue goal in USD (e.g., 5000 for $5,000/month)",
                },
                "avg_product_price": {
                    "type": "number",
                    "description": "Average selling price of your products in USD",
                },
                "conversion_rate": {
                    "type": "number",
                    "description": "Expected conversion rate as a percentage (e.g., 2.0 for 2%). Default: 2.0",
                },
            },
            "required": ["target_monthly_revenue", "avg_product_price"],
        },
    },
    {
        "name": "create_kpi_dashboard",
        "description": (
            "Generate a KPI health dashboard scoring monthly revenue, AOV, refund rate, "
            "and product count against industry benchmarks. Returns an overall score, grades, "
            "and priority recommendations. Use to give a user a health check on their business."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_count": {
                    "type": "integer",
                    "description": "Number of active products in the store",
                },
                "monthly_revenue": {
                    "type": "number",
                    "description": "Current monthly revenue in USD",
                },
                "avg_order_value": {
                    "type": "number",
                    "description": "Average order value in USD",
                },
                "refund_rate": {
                    "type": "number",
                    "description": "Refund rate as a percentage (e.g., 3.0 for 3%). Default: 3.0",
                },
            },
            "required": ["product_count", "monthly_revenue", "avg_order_value"],
        },
    },
    {
        "name": "forecast_revenue",
        "description": (
            "Forecast future revenue based on historical monthly data and a growth rate. "
            "Returns monthly projections (base/optimistic/conservative), cumulative totals, "
            "milestone projections, and growth acceleration tips."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "historical_data": {
                    "type": "array",
                    "description": "List of past monthly revenue records",
                    "items": {
                        "type": "object",
                        "properties": {
                            "month": {"type": "string", "description": "Month label, e.g. 'Jan 2025'"},
                            "revenue": {"type": "number", "description": "Revenue for that month in USD"},
                        },
                        "required": ["revenue"],
                    },
                },
                "growth_rate": {
                    "type": "number",
                    "description": "Expected monthly growth rate as a percentage (e.g., 10 for 10%/month). Default: 10",
                },
                "months_ahead": {
                    "type": "integer",
                    "description": "How many months to forecast (1-24). Default: 6",
                },
            },
            "required": ["historical_data"],
        },
    },
]


# ---------------------------------------------------------------------------
# Handler dispatcher
# ---------------------------------------------------------------------------

def handle_analytics_tool(tool_name: str, tool_input: dict) -> dict | None:
    """Route analytics tool calls to the right function."""
    if tool_name == "analyze_sales_performance":
        return analyze_sales_performance(**tool_input)
    elif tool_name == "calculate_monthly_revenue_goal":
        return calculate_monthly_revenue_goal(**tool_input)
    elif tool_name == "create_kpi_dashboard":
        return create_kpi_dashboard(**tool_input)
    elif tool_name == "forecast_revenue":
        return forecast_revenue(**tool_input)
    return None
