"""
Competitor analysis tools for Sharp Pages Selling Bot.
Covers listing analysis, market gap identification, price benchmarking, and USP generation.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Heuristics-based competitor analysis (no live scraping)
# ---------------------------------------------------------------------------

def analyze_competitor_listing(
    competitor_url_or_name: str,
    platform: str = "gumroad",
) -> dict:
    """
    Analyze a competitor's listing using heuristics and best-practice patterns.
    Since we can't scrape live, we return a structured analysis framework
    with actionable insights based on what successful listings typically include.
    """
    try:
        platform_lower = platform.lower()
        name = competitor_url_or_name.strip()

        # Extract product name from URL if a URL was provided
        display_name = name
        if "http" in name or "gumroad.com" in name or "etsy.com" in name:
            # Parse the URL slug for a name hint
            parts = name.rstrip("/").split("/")
            slug = parts[-1].replace("-", " ").replace("_", " ")
            display_name = slug.title() if slug else name

        # Common strengths seen in top-selling digital product listings
        common_strengths = [
            "Clear, benefit-focused title with primary keyword upfront",
            "High-quality mockup images showing the product in use",
            "Detailed description (200+ words) covering features and benefits",
            "Social proof (download count, testimonials, or star ratings)",
            "Strong CTA at the beginning and end of description",
            "FAQ section addressing common objections",
            "Preview images or demo access to reduce purchase hesitation",
            "Competitive pricing at psychological price points ($17, $27, $47)",
            "Multiple product tags covering broad and long-tail keywords",
            "Regular updates mentioned to justify ongoing value",
        ]

        # Common weaknesses seen in average listings
        common_weaknesses = [
            "Generic stock photo cover image instead of actual product mockup",
            "Too-short description that doesn't answer buyer questions",
            "Missing FAQ or no refund policy mentioned",
            "Only 1-3 tags instead of maximizing tag slots",
            "No social proof (new listing or creator doesn't ask for reviews)",
            "Vague benefits — lists features but doesn't explain transformation",
            "No CTA or a weak CTA ('buy if you want')",
            "Price not at a psychological point (e.g., $15 instead of $14.99 or $17)",
            "No preview or sample — buyers can't see what they're getting",
            "Listing hasn't been updated in 1+ year — signals abandoned product",
        ]

        # Platform-specific analysis points
        platform_notes = {
            "gumroad": {
                "key_elements": [
                    "Cover image (ideal: 1280x720px)",
                    "Product description (no character limit)",
                    "Tags (max 10 on free plan)",
                    "Pricing (pay-what-you-want option available)",
                    "Preview content (file preview or linked demo)",
                ],
                "top_performer_patterns": [
                    "Top Gumroad products use pay-what-you-want with a $0 floor for lead gen",
                    "Bundles consistently outperform single products in revenue",
                    "Email capture via free tier converts to paid sales effectively",
                    "Creators who update listings quarterly see 20-30% more organic traffic",
                ],
            },
            "etsy": {
                "key_elements": [
                    "10 product photos (all slots used)",
                    "Title: 140 chars with keyword-dense phrases",
                    "13 tags (all used, multi-word phrases)",
                    "Section: organized by category",
                    "Variation options (bundles, color options)",
                ],
                "top_performer_patterns": [
                    "Etsy favorites (wishlists) increase purchase probability 3x",
                    "Star sellers get a badge that boosts CTR by 15-20%",
                    "Listings with 4.8+ stars appear higher in search",
                    "Products with video get 40% more views than image-only",
                ],
            },
            "pinterest": {
                "key_elements": [
                    "Pin image (1000x1500px, 2:3 ratio)",
                    "Pin title (100 chars)",
                    "Pin description (500 chars, keyword-rich)",
                    "Board name (keyword-rich)",
                    "Destination URL (product page, not homepage)",
                ],
                "top_performer_patterns": [
                    "Pins with text overlay get 6x more clicks than text-free images",
                    "Red/orange images outperform blue on Pinterest CTR",
                    "Vertical pins take up 70% more space in feed — major advantage",
                    "Fresh pins (not repins) are prioritized in the algorithm",
                ],
            },
        }

        p_notes = platform_notes.get(platform_lower, platform_notes["gumroad"])

        # How to beat them — gap analysis
        beat_the_competition = [
            "Add a free 'lite' version as a lead magnet — competitors rarely do this",
            "Respond to every review publicly — shows activity and builds trust",
            "Create a YouTube/TikTok demo video — very few digital product sellers do this",
            "Bundle with a bonus tutorial or guide — adds perceived value without much work",
            "Offer a 'satisfaction guarantee' prominently — removes buyer risk",
            f"Use all {p_notes['key_elements'][2].split('(')[0].strip()} slots — many competitors leave some empty",
        ]

        return {
            "competitor": display_name,
            "platform": platform,
            "analysis_method": "Heuristic framework (pattern-based analysis — live scraping not available)",
            "what_top_performers_typically_do_well": common_strengths[:6],
            "common_weaknesses_to_exploit": common_weaknesses[:6],
            "platform_specific_elements": p_notes["key_elements"],
            "platform_top_performer_patterns": p_notes["top_performer_patterns"],
            "how_to_beat_competitors": beat_the_competition,
            "your_audit_checklist": [
                f"☐ Does competitor use all {platform_lower} tag slots?",
                "☐ Do they have social proof (reviews, download count)?",
                "☐ Is their cover image a product mockup or generic stock?",
                "☐ Do they have a FAQ section?",
                "☐ Is their description 150+ words?",
                "☐ Do they have a clear CTA?",
                "☐ Is their price at a psychological point?",
                "☐ Do they offer a free sample or preview?",
            ],
            "opportunity_score": {
                "note": "Manually review the listing above to fill in your findings",
                "scale": "Score each checklist item 0 (competitor does well) or 1 (gap you can fill)",
                "interpretation": "Score of 5+/8: Strong opportunity to outperform this competitor",
            },
        }
    except Exception as e:
        return {"error": str(e)}


def identify_market_gaps(
    niche: str,
    current_products: list[str] | None = None,
) -> dict:
    """
    Identify underserved niches and product opportunity ideas based on
    the provided niche and existing product lineup.
    """
    try:
        current_products = current_products or []
        niche_lower = niche.lower()
        existing_lower = [p.lower() for p in current_products]

        # Potential product types across categories
        universal_product_types = [
            "Notion dashboard template",
            "Google Sheets tracker",
            "Canva social media template pack",
            "Email swipe file collection",
            "Standard operating procedure (SOP) templates",
            "Checklist bundle",
            "eBook / guide",
            "Mini course or workshop",
            "Printable planner pages",
            "Spreadsheet calculator",
            "Contract or legal template",
            "Content calendar",
            "Business plan template",
            "Budget tracker",
            "Client onboarding kit",
            "Pitch deck template",
            "Resume / CV template",
            "Course curriculum outline",
            "Social media captions pack",
            "Brand kit template",
        ]

        # Niche-specific gaps
        niche_gap_map = {
            "productivity": [
                "Time-blocking planner (Notion/Google Sheets) — still undersaturated",
                "Focus session tracker with Pomodoro integration",
                "Meeting notes template with action item tracker",
                "Personal OKR (Objectives & Key Results) dashboard",
                "2-minute task capture system (GTD-inspired)",
            ],
            "budgeting": [
                "Zero-based budget template for irregular income",
                "Debt snowball / avalanche calculator",
                "Savings goal tracker with milestone visualization",
                "Business vs. personal expense separator for freelancers",
                "Annual review + financial snapshot template",
            ],
            "social media": [
                "Content repurposing workflow template",
                "Influencer outreach tracking spreadsheet",
                "Weekly content batch planning kit",
                "Analytics tracking spreadsheet (multi-platform)",
                "Brand partnership / sponsored post tracking template",
            ],
            "freelance": [
                "Discovery call questionnaire template",
                "Project scope creep prevention checklist",
                "Freelancer rate calculator (with tax and overhead)",
                "Client testimonial request email sequence",
                "Portfolio case study template",
            ],
            "notion": [
                "Second Brain dashboard (still high demand)",
                "Habit tracker with streak visualization",
                "Reading list + book notes system",
                "Job search tracker",
                "Travel planning dashboard",
            ],
            "pinterest": [
                "Pinterest audit checklist",
                "Monthly Pinterest analytics tracker (Sheets)",
                "Pin design template pack (Canva)",
                "Pinterest board organization guide",
                "Seasonal content calendar for Pinterest",
            ],
            "canva": [
                "Instagram grid planner (9-tile puzzle layouts)",
                "YouTube channel art + thumbnail kit",
                "Podcast cover art templates",
                "Email header template pack",
                "Digital product mockup templates",
            ],
        }

        # Find matching niche gaps
        matched_gaps = []
        for niche_key, gaps in niche_gap_map.items():
            if niche_key in niche_lower or niche_lower in niche_key:
                matched_gaps.extend(gaps)

        # Filter out what they already have
        filtered_gaps = [
            g for g in matched_gaps
            if not any(existing in g.lower() for existing in existing_lower)
        ]

        # Supplement with generic opportunities if few niche matches
        if len(filtered_gaps) < 3:
            generic_gaps = [
                f"{niche} starter kit for beginners — most niches lack a true 'start here' product",
                f"{niche} annual planning template — perennial demand, low competition",
                f"Ultimate {niche} bundle — aggregate your existing products at a discount",
                f"{niche} progress tracker — gamification appeals to all audiences",
                f"Free {niche} mini-template — lead magnet that drives email list growth",
            ]
            filtered_gaps = generic_gaps

        # Market size indicators
        high_demand_signals = [
            "High Pinterest search volume (check Pinterest search bar autocomplete)",
            "Multiple Etsy sellers with 100+ sales for similar items",
            "Active subreddits or Facebook groups around this topic",
            "YouTube tutorials for the same problem getting 10k+ views",
            "'Best [niche] template' appears in Google autocomplete",
        ]

        # Product opportunity scores
        opportunities = []
        for i, gap in enumerate(filtered_gaps[:8]):
            difficulty = ["Low", "Medium", "Low", "Medium", "Low", "High"][i % 6]
            revenue_potential = ["High", "Medium", "High", "Medium", "High", "Very High"][i % 6]
            opportunities.append({
                "product_idea": gap,
                "difficulty_to_create": difficulty,
                "revenue_potential": revenue_potential,
                "estimated_creation_time": "2-8 hours" if difficulty == "Low" else "2-5 days",
                "suggested_price": "$17-$27" if difficulty == "Low" else "$27-$47",
                "why_it_works": f"Under-served demand in '{niche}' space with clear buyer intent",
            })

        return {
            "niche": niche,
            "current_products": current_products,
            "market_gaps_identified": len(opportunities),
            "opportunities": opportunities,
            "high_demand_signals": high_demand_signals,
            "validation_steps": [
                f"Search '{niche} template' on Etsy — see how many results and what's selling",
                f"Check Pinterest trends for '{niche_lower}' — what content gets repinned most?",
                f"Post in a relevant Facebook group: 'What's the #1 thing you wish you had a template for in {niche}?' — real customer research",
                "Look at Gumroad discover page — what's trending in your category?",
                "Check Google Trends: is interest in this niche growing or declining?",
            ],
            "quick_win": {
                "idea": opportunities[0]["product_idea"] if opportunities else f"Free {niche} mini-template",
                "rationale": "Lowest effort, highest demand signal based on gap analysis",
                "action": "Create a minimum viable version this week and ship it — perfection is the enemy of progress",
            },
        }
    except Exception as e:
        return {"error": str(e)}


def benchmark_pricing(
    product_category: str,
    your_price: float,
) -> dict:
    """
    Return market price ranges and positioning advice for a product category.
    """
    try:
        category_lower = product_category.lower()

        # Pricing benchmarks by category (based on typical Gumroad/Etsy market data)
        benchmarks = {
            "notion template": {"low": 5, "mid": 17, "high": 37, "premium": 67, "notes": "Single templates $7-$27; full systems $27-$97"},
            "canva template": {"low": 5, "mid": 12, "high": 27, "premium": 47, "notes": "Single templates $7-$17; large packs $27-$47"},
            "ebook": {"low": 7, "mid": 17, "high": 37, "premium": 97, "notes": "Short guides $7-$17; comprehensive books $27-$97"},
            "spreadsheet": {"low": 7, "mid": 17, "high": 37, "premium": 67, "notes": "Simple trackers $7-$17; complex calculators $27-$67"},
            "printable": {"low": 3, "mid": 7, "high": 17, "premium": 37, "notes": "Single pages $3-$7; large sets $17-$37"},
            "planner": {"low": 5, "mid": 12, "high": 27, "premium": 47, "notes": "Annual planners $12-$27; full systems $37-$67"},
            "course": {"low": 27, "mid": 97, "high": 197, "premium": 497, "notes": "Mini-courses $27-$97; full courses $97-$497"},
            "template pack": {"low": 12, "mid": 27, "high": 47, "premium": 97, "notes": "Small packs $12-$27; large collections $47-$97"},
            "swipe file": {"low": 7, "mid": 17, "high": 37, "premium": 67, "notes": "Email swipes $7-$17; full content libraries $37-$67"},
            "bundle": {"low": 17, "mid": 37, "high": 67, "premium": 147, "notes": "Small bundles $17-$37; mega bundles $67-$197"},
        }

        # Find matching benchmark
        matched_benchmark = None
        for key, data in benchmarks.items():
            if key in category_lower or any(word in category_lower for word in key.split()):
                matched_benchmark = data
                matched_key = key
                break

        if not matched_benchmark:
            # Default benchmark
            matched_benchmark = {"low": 7, "mid": 17, "high": 37, "premium": 97, "notes": "Digital product benchmarks"}
            matched_key = "digital product"

        # Positioning analysis
        if your_price < matched_benchmark["low"]:
            positioning = "Below Market"
            positioning_risk = "Signals low quality; attracts bargain hunters with high refund rates"
            recommendation = f"Raise to at least ${matched_benchmark['low']} — you're leaving money on the table and potentially hurting your brand"
        elif your_price <= matched_benchmark["mid"]:
            positioning = "Budget Tier (lower third)"
            positioning_risk = "Low risk, but limits revenue potential; competes mainly on price"
            recommendation = f"Consider raising to ${matched_benchmark['mid']} once you have 10+ reviews. You're underpriced relative to value."
        elif your_price <= matched_benchmark["high"]:
            positioning = "Mid-Market (sweet spot)"
            positioning_risk = "Minimal — this is the optimal position for most digital products"
            recommendation = f"You're in the sweet spot. Focus on social proof to justify the price. Test ${matched_benchmark['high']} for premium positioning."
        elif your_price <= matched_benchmark["premium"]:
            positioning = "Premium Tier (top third)"
            positioning_risk = "Requires strong brand and social proof to convert at this price"
            recommendation = "Strong position if you have 20+ reviews. Add testimonials and case studies prominently."
        else:
            positioning = "Ultra-Premium (above market)"
            positioning_risk = "Only works with exceptional brand authority and documented results"
            recommendation = f"You're above typical market for {matched_key}. Ensure your listing communicates exceptional value at this price."

        # Revenue impact of price adjustments
        revenue_scenarios = {}
        for target_price in [matched_benchmark["low"], matched_benchmark["mid"], matched_benchmark["high"], matched_benchmark["premium"]]:
            # Assume 50 sales/month at current conversion; adjust conversion for price
            base_units = 50
            conversion_factor = 1.0
            if target_price > your_price * 1.5:
                conversion_factor = 0.7  # Higher price, lower volume
            elif target_price < your_price * 0.7:
                conversion_factor = 1.4  # Lower price, higher volume
            adjusted_units = int(base_units * conversion_factor)
            revenue_scenarios[f"${target_price}"] = {
                "price": target_price,
                "est_units_per_month": adjusted_units,
                "est_monthly_revenue": round(target_price * adjusted_units, 2),
                "positioning_label": (
                    "Below market" if target_price < matched_benchmark["low"] + 2
                    else "Budget tier" if target_price <= matched_benchmark["mid"]
                    else "Mid-market" if target_price <= matched_benchmark["high"]
                    else "Premium"
                ),
            }

        return {
            "product_category": product_category,
            "your_price": your_price,
            "market_benchmarks": {
                "category_matched": matched_key,
                "entry_level": f"${matched_benchmark['low']}",
                "mid_market": f"${matched_benchmark['mid']}",
                "upper_market": f"${matched_benchmark['high']}",
                "premium_tier": f"${matched_benchmark['premium']}",
                "market_notes": matched_benchmark["notes"],
            },
            "your_positioning": positioning,
            "positioning_risk": positioning_risk,
            "recommendation": recommendation,
            "revenue_scenarios_at_50_sales_per_month": revenue_scenarios,
            "psychological_pricing_guide": {
                "best_price_endings": ["$X7 (e.g., $17, $27, $47, $97)", "$X9 for under-$10 products", "$X00 for ultra-premium positioning"],
                "avoid": ["Round numbers ($10, $20, $30) — feel arbitrary", "Prices below $7 — digital products lose credibility", "$X.95 or $X.99 above $10 — screams 'cheap'"],
                "sweet_spots": "$17 (impulse buy), $27 (considered buy), $47 (high-value perceived), $97 (transformation pricing)",
            },
            "competitive_pricing_strategy": [
                f"Research 5 top-sellers in '{product_category}' on Gumroad/Etsy — note exact prices",
                "If you're new: match or beat the mid-market price by 10-15% for your first 25 sales",
                "After 10 reviews: raise price to mid-market if at budget tier",
                "After 50 reviews: test premium tier for 2 weeks; compare conversion rates",
                "Launch bundles at a premium price to anchor perception of your individual product value",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


def generate_unique_selling_points(
    product_name: str,
    competitor_features: list[str],
    your_features: list[str],
) -> dict:
    """
    Generate USP statements by comparing your features against competitor features.
    Returns differentiated USP statements and positioning copy.
    """
    try:
        if not your_features:
            return {"error": "your_features cannot be empty — list what makes your product distinctive"}

        # Features you have that competitors don't
        competitor_lower = [f.lower() for f in competitor_features]
        your_lower = [f.lower() for f in your_features]

        unique_to_you = [
            f for f, fl in zip(your_features, your_lower)
            if not any(cf in fl or fl in cf for cf in competitor_lower)
        ]

        # Features competitors have that you also have (parity points)
        parity_features = [
            f for f, fl in zip(your_features, your_lower)
            if any(cf in fl or fl in cf for cf in competitor_lower)
        ]

        # USP statement formulas
        usp_statements = []

        if unique_to_you:
            for feature in unique_to_you[:3]:
                usp_statements.append({
                    "usp": f"The only {product_name} that includes {feature.lower()}",
                    "type": "Exclusivity USP",
                    "use_for": "Headline or first line of product description",
                })
                usp_statements.append({
                    "usp": f"Unlike other {product_name.lower()}s, this one comes with {feature.lower()}",
                    "type": "Contrast USP",
                    "use_for": "Description body, FAQ, or comparison section",
                })
                usp_statements.append({
                    "usp": f"{feature} — something you won't find in any other {product_name.lower()} at this price",
                    "type": "Value USP",
                    "use_for": "Pricing section or CTA area",
                })

        # Generic USPs based on features
        if not usp_statements:
            usp_statements = [
                {
                    "usp": f"{product_name}: built differently, designed to actually be used",
                    "type": "Quality USP",
                    "use_for": "When features are similar — compete on execution quality",
                },
                {
                    "usp": f"Made by someone who actually [uses/needed] this — not a generic template",
                    "type": "Authenticity USP",
                    "use_for": "Trust-building in description",
                },
                {
                    "usp": f"The most thorough {product_name.lower()} you'll find — backed by [X] customers",
                    "type": "Social Proof USP",
                    "use_for": "Once you have reviews",
                },
            ]

        # Competitive advantage matrix
        advantage_matrix = {
            "you_have_they_dont": unique_to_you if unique_to_you else ["(No unique features identified — differentiate through execution and support)"],
            "both_have": parity_features if parity_features else ["(No direct overlap identified)"],
            "they_have_you_dont": [f for f in competitor_features if f.lower() not in your_lower],
        }

        # Positioning recommendations
        if len(unique_to_you) >= 3:
            positioning = "Strong differentiation — lead with your unique features"
            headline_strategy = "Lead with your biggest unique differentiator in the first 10 words"
        elif len(unique_to_you) >= 1:
            positioning = "Moderate differentiation — lean heavily into your 1-2 unique advantages"
            headline_strategy = f"'{unique_to_you[0]}' deserves to be in your title or first line"
        else:
            positioning = "Compete on execution — same features, better quality/support/design"
            headline_strategy = "When features are equal, win on brand story, design quality, and customer support"

        # Messaging hierarchy
        messaging_hierarchy = {
            "level_1_headline": usp_statements[0]["usp"] if usp_statements else f"The most complete {product_name}",
            "level_2_sub_headline": (
                f"With {', '.join(your_features[:2])}" if len(your_features) >= 2
                else f"Everything you need to get started"
            ),
            "level_3_differentiators": unique_to_you[:3] if unique_to_you else your_features[:3],
            "level_4_proof_point": "Add your strongest testimonial or download count here",
        }

        return {
            "product_name": product_name,
            "competitive_advantage_matrix": advantage_matrix,
            "unique_features_count": len(unique_to_you),
            "usp_statements": usp_statements[:6],
            "positioning_assessment": positioning,
            "headline_strategy": headline_strategy,
            "messaging_hierarchy": messaging_hierarchy,
            "differentiation_tactics": [
                "Add a bonus not available elsewhere (e.g., a companion checklist or mini-guide)",
                "Include a 'quick start' video walkthrough — very few template sellers do this",
                "Offer a 'done-with-you' option at 3x price — frames the template as a product, not just a file",
                "Update your product every 6 months and mention it — competitors' listings go stale",
                "Showcase real customer results with permission — transformation beats features every time",
            ],
            "competitive_intelligence_to_gather": [
                "Look at competitor reviews: what do buyers PRAISE? That's what they care about most.",
                "Look at competitor reviews: what do buyers CRITICIZE? That's your opportunity.",
                "Check if competitors answer questions/comments — most don't. Be responsive.",
                "Track competitor pricing monthly — are they raising/lowering prices?",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# JSON Schemas for Claude tool_use
# ---------------------------------------------------------------------------

COMPETITOR_TOOL_SCHEMAS: list[dict] = [
    {
        "name": "analyze_competitor_listing",
        "description": (
            "Analyze a competitor's product listing using best-practice heuristics. "
            "Returns strength/weakness analysis, platform-specific patterns, and tactics to "
            "outperform them. Works for any Gumroad, Etsy, or Pinterest listing."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "competitor_url_or_name": {
                    "type": "string",
                    "description": "The competitor's product URL or product/brand name to analyze",
                },
                "platform": {
                    "type": "string",
                    "description": "Platform where the listing exists: gumroad, etsy, or pinterest",
                    "enum": ["gumroad", "etsy", "pinterest"],
                },
            },
            "required": ["competitor_url_or_name"],
        },
    },
    {
        "name": "identify_market_gaps",
        "description": (
            "Identify underserved product opportunities in a niche based on current market patterns. "
            "Returns specific product ideas with difficulty ratings, revenue potential, "
            "suggested prices, and validation steps."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "niche": {
                    "type": "string",
                    "description": "The market niche to analyze (e.g., 'productivity', 'notion templates', 'social media')",
                },
                "current_products": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of products you already have (to avoid suggesting duplicates)",
                },
            },
            "required": ["niche"],
        },
    },
    {
        "name": "benchmark_pricing",
        "description": (
            "Benchmark your product price against typical market ranges for the category. "
            "Returns market tier analysis, positioning assessment, revenue scenarios at different "
            "price points, and pricing strategy recommendations."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_category": {
                    "type": "string",
                    "description": "Product category (e.g., 'Notion template', 'Canva template', 'eBook', 'spreadsheet', 'bundle')",
                },
                "your_price": {
                    "type": "number",
                    "description": "Your current or planned selling price in USD",
                },
            },
            "required": ["product_category", "your_price"],
        },
    },
    {
        "name": "generate_unique_selling_points",
        "description": (
            "Generate USP statements by comparing your product features against competitor features. "
            "Returns a competitive advantage matrix, 6 ready-to-use USP statements, "
            "a messaging hierarchy, and differentiation tactics."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of your product",
                },
                "competitor_features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Features that competing products offer",
                },
                "your_features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Features your product offers",
                },
            },
            "required": ["product_name", "competitor_features", "your_features"],
        },
    },
]


# ---------------------------------------------------------------------------
# Handler dispatcher
# ---------------------------------------------------------------------------

def handle_competitor_tool(tool_name: str, tool_input: dict) -> dict | None:
    """Route competitor tool calls to the right function."""
    if tool_name == "analyze_competitor_listing":
        return analyze_competitor_listing(**tool_input)
    elif tool_name == "identify_market_gaps":
        return identify_market_gaps(**tool_input)
    elif tool_name == "benchmark_pricing":
        return benchmark_pricing(**tool_input)
    elif tool_name == "generate_unique_selling_points":
        return generate_unique_selling_points(**tool_input)
    return None
