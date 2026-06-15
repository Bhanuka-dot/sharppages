"""
Product tools for Sharp Pages Selling Bot.
Covers product description writing, title optimization, bundle ideas, and FAQ generation.
"""

from __future__ import annotations

import json
from typing import Any


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------


def generate_product_description(
    product_name: str,
    category: str,
    key_features: list[str],
    target_audience: str,
    tone: str = "professional",
) -> dict:
    """
    Generate compelling sales copy for a digital product.
    Returns headline, hook, benefits bullets, body copy, and CTA.
    """
    try:
        tone_map = {
            "professional": ("authoritative and clear", "Transform", "Elevate"),
            "casual": ("friendly and conversational", "Upgrade", "Level up"),
            "urgent": ("urgent and results-focused", "Stop wasting time on", "Finally"),
            "inspirational": ("motivating and empowering", "Unlock", "Discover"),
            "minimalist": ("clean and direct", "Simplify", "Streamline"),
        }
        tone_desc, action_verb1, action_verb2 = tone_map.get(
            tone.lower(), tone_map["professional"]
        )

        features_str = ", ".join(key_features[:5]) if key_features else "key features"
        first_feature = key_features[0] if key_features else "streamlined workflow"

        headline_variants = [
            f"{action_verb1} Your {category} with {product_name}",
            f"The {target_audience}'s Complete {category} Solution",
            f"{product_name}: The Only {category} Resource You'll Ever Need",
        ]

        hook = (
            f"Struggling with {category.lower()} tasks that eat into your productive hours? "
            f"You're not alone — and {product_name} was built specifically for {target_audience} "
            f"who want to {first_feature.lower()} without the guesswork."
        )

        benefits = []
        for i, feature in enumerate(key_features):
            benefit_starters = [
                "Save hours every week by",
                "Instantly",
                "Never again struggle with",
                "Confidently",
                "Get professional results when you",
                "Eliminate confusion around",
                "Systematically",
            ]
            starter = benefit_starters[i % len(benefit_starters)]
            benefits.append(f"{starter} {feature.lower()}")

        body_copy = (
            f"{product_name} is a premium {category.lower()} resource designed for {target_audience}. "
            f"Unlike generic alternatives, this gives you exactly what you need: {features_str}. "
            f"Every element has been carefully crafted with a {tone_desc} approach so you can "
            f"get results from day one — no prior experience required."
        )

        what_you_get = [
            f"Fully editable {category.lower()} template/resource",
            "Step-by-step instructions included",
            "Lifetime access — download once, use forever",
            "Compatible with all major platforms",
            "Free updates included",
        ]

        cta_variants = [
            f"Get {product_name} Today — Instant Download",
            f"Download {product_name} Now & Start Immediately",
            f"Add to Cart — Instant Access After Purchase",
        ]

        return {
            "product_name": product_name,
            "headline_variants": headline_variants,
            "hook_paragraph": hook,
            "benefit_bullets": benefits,
            "body_copy": body_copy,
            "what_you_get": what_you_get,
            "cta_variants": cta_variants,
            "tone_used": tone,
            "word_count_estimate": len(hook.split()) + len(body_copy.split()) + len(benefits) * 8,
            "writing_tips": [
                "Lead with the transformation, not the product features",
                "Use 'you' 3x more than 'I' or 'we'",
                "Add social proof (e.g., '500+ downloads') once you have it",
                "Keep the first sentence under 12 words for mobile readers",
                f"Mirror your audience's exact language: '{target_audience}' use terms like...",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


def optimize_product_title(
    raw_title: str,
    platform: str = "gumroad",
    keywords: list[str] | None = None,
) -> dict:
    """
    Return SEO-optimized title variants for the given platform.
    """
    try:
        keywords = keywords or []
        platform = platform.lower()

        platform_rules = {
            "gumroad": {
                "max_chars": 100,
                "style": "Benefit-first, keyword-rich",
                "tips": [
                    "Put your most important keyword in the first 5 words",
                    "Include the format (Template, Guide, Bundle, Kit)",
                    "Use a colon to separate category from specifics",
                ],
            },
            "etsy": {
                "max_chars": 140,
                "style": "Keyword-stuffed with separators",
                "tips": [
                    "Etsy indexes first 40 chars most heavily",
                    "Use | or , to chain keyword phrases",
                    "Repeat core concept in different phrasings",
                ],
            },
            "pinterest": {
                "max_chars": 100,
                "style": "Curiosity + benefit, conversational",
                "tips": [
                    "Pinterest titles are pin descriptions — make them intriguing",
                    "Questions perform well ('How to...', 'The best...')",
                    "Include a number when possible ('5 Steps', '30-Day')",
                ],
            },
        }

        rules = platform_rules.get(platform, platform_rules["gumroad"])

        base_words = raw_title.strip()
        top_kw = keywords[0] if keywords else ""
        second_kw = keywords[1] if len(keywords) > 1 else ""

        # Detect product type from raw title
        product_type = "Template"
        for ptype in ["Guide", "eBook", "Bundle", "Kit", "Planner", "Tracker", "Course", "Preset", "Dashboard"]:
            if ptype.lower() in raw_title.lower():
                product_type = ptype
                break

        variants = [
            f"{base_words} | {top_kw} {product_type} for Instant Download" if top_kw else f"{base_words} — Instant Digital Download",
            f"Ultimate {base_words}: {top_kw} + {second_kw}".strip(": ") if second_kw else f"Ultimate {base_words} for Beginners & Pros",
            f"{base_words} ({product_type}) — {top_kw} Made Easy" if top_kw else f"{base_words} ({product_type}) — Fully Editable",
            f"How to {top_kw.lower()}: The {base_words}" if top_kw else f"Professional {base_words} — Ready to Use",
            f"{product_type}: {base_words} | {' | '.join(keywords[:3])}" if keywords else f"{product_type}: {base_words}",
        ]

        # Score each variant
        scored = []
        for v in variants:
            score = 0
            if any(kw.lower() in v.lower() for kw in keywords):
                score += 30
            if len(v) <= rules["max_chars"]:
                score += 20
            if any(w in v for w in ["Ultimate", "Complete", "Professional", "How to", "Best"]):
                score += 15
            if product_type in v:
                score += 10
            if "Instant" in v or "Ready" in v or "Download" in v:
                score += 10
            scored.append({"title": v, "score": score, "char_count": len(v)})

        scored.sort(key=lambda x: x["score"], reverse=True)

        return {
            "original_title": raw_title,
            "platform": platform,
            "platform_rules": rules,
            "optimized_variants": scored,
            "recommended": scored[0]["title"] if scored else raw_title,
            "keywords_detected": keywords,
            "optimization_notes": [
                f"Max characters for {platform}: {rules['max_chars']}",
                f"Your recommended title uses {len(scored[0]['title']) if scored else len(raw_title)} characters",
                *rules["tips"],
            ],
        }
    except Exception as e:
        return {"error": str(e)}


def create_product_bundle_ideas(
    products_list: list[str],
    niche: str,
) -> dict:
    """
    Generate bundle suggestions with pricing rationale and marketing angles.
    """
    try:
        if not products_list:
            return {"error": "products_list cannot be empty"}

        bundle_names = [
            f"The Ultimate {niche} Toolkit",
            f"{niche} Starter Bundle",
            f"Complete {niche} Success Pack",
            f"{niche} Pro Bundle",
            f"All-In-One {niche} Collection",
        ]

        products_str = ", ".join(products_list)

        bundles = []

        # Bundle 1: Starter (2-3 products)
        if len(products_list) >= 2:
            starter_items = products_list[:2]
            bundles.append({
                "bundle_name": f"{niche} Starter Pack",
                "included_products": starter_items,
                "target_buyer": "Beginners just getting started",
                "suggested_individual_prices": [17, 17],
                "individual_total": 34,
                "bundle_price": 27,
                "savings_for_buyer": 7,
                "discount_pct": 20,
                "pricing_rationale": (
                    "20% discount rewards commitment without devaluing individual products. "
                    "$27 hits the impulse-buy sweet spot for digital bundles."
                ),
                "marketing_angle": f"Everything a beginner needs to get started with {niche.lower()} — in one affordable package.",
            })

        # Bundle 2: Complete (all products)
        individual_prices = [17 + (i * 4) for i in range(len(products_list))]
        individual_total = sum(individual_prices)
        bundle_price_full = round(individual_total * 0.65, -1) + 7  # ~35% off, $X7 pricing
        bundles.append({
            "bundle_name": f"Complete {niche} Collection",
            "included_products": products_list,
            "target_buyer": "Serious creators wanting the full toolkit",
            "suggested_individual_prices": individual_prices,
            "individual_total": individual_total,
            "bundle_price": bundle_price_full,
            "savings_for_buyer": individual_total - bundle_price_full,
            "discount_pct": 35,
            "pricing_rationale": (
                "35% off for the complete bundle creates strong perceived value. "
                "Price ending in 7 (e.g., $47, $67) converts better than round numbers. "
                "Position as 'everything you need' to justify premium price."
            ),
            "marketing_angle": f"The only {niche.lower()} resource collection you'll ever need — save {round((1 - bundle_price_full/individual_total)*100)}% vs buying separately.",
        })

        # Bundle 3: Limited-time flash bundle
        flash_price = round(individual_total * 0.5 / 10) * 10 - 3  # ~50% off, ends in 7
        bundles.append({
            "bundle_name": f"{niche} Flash Sale Bundle (Limited Time)",
            "included_products": products_list[:3] if len(products_list) >= 3 else products_list,
            "target_buyer": "Deal seekers / email list subscribers",
            "suggested_individual_prices": individual_prices[:3] if len(products_list) >= 3 else individual_prices,
            "individual_total": sum(individual_prices[:3]) if len(products_list) >= 3 else individual_total,
            "bundle_price": flash_price,
            "savings_for_buyer": sum(individual_prices[:3]) - flash_price if len(products_list) >= 3 else individual_total - flash_price,
            "discount_pct": 50,
            "pricing_rationale": (
                "Flash sale bundles at 50% off create urgency and shift fence-sitters. "
                "Use only with deadline (24-72 hrs) and to existing audience — not as main pricing."
            ),
            "marketing_angle": f"For the next 48 hours only: get our top {niche.lower()} products at half price.",
        })

        upsell_ideas = [
            f"Offer the Complete Collection as an order bump when buying any single product",
            f"Create a 'VIP' tier with all bundles + future releases for a one-time fee",
            f"Use the Starter Pack as a loss leader to collect emails, then upsell the Complete",
        ]

        return {
            "niche": niche,
            "products_analyzed": products_list,
            "bundle_ideas": bundles,
            "upsell_strategy": upsell_ideas,
            "gumroad_tips": [
                "Use Gumroad's 'Suggested Products' to cross-sell bundles",
                "Create a separate Gumroad listing for each bundle",
                "Add a 'You might also like' section in your product description",
                "Offer bundle access via a single download ZIP or separate product links",
            ],
            "psychology_notes": [
                "Anchoring: Show individual total price crossed out next to bundle price",
                "Scarcity: 'Bundle available for a limited time only'",
                "Social proof: 'Our most popular package'",
                "Decoy pricing: Middle tier makes top tier look better value",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


def generate_faq_section(
    product_name: str,
    product_type: str,
    common_concerns: list[str] | None = None,
) -> dict:
    """
    Generate a comprehensive FAQ section for a product listing.
    """
    try:
        common_concerns = common_concerns or []

        base_faqs = [
            {
                "question": f"What format does {product_name} come in?",
                "answer": (
                    f"{product_name} is delivered as a digital download immediately after purchase. "
                    f"You'll receive a ZIP file containing the {product_type} files in all major formats. "
                    "No waiting — access it the moment payment clears."
                ),
            },
            {
                "question": "What software do I need to use this?",
                "answer": (
                    f"This {product_type} works with [specify your tool, e.g., Notion, Canva, Google Sheets, Adobe]. "
                    "A free account is all you need — no paid software required. "
                    "Full compatibility instructions are included in your download."
                ),
            },
            {
                "question": "Can I edit and customize it?",
                "answer": (
                    f"Yes! {product_name} is fully editable. You can change colors, fonts, text, and structure to match your brand. "
                    "It's designed to be your starting point, not a finished product."
                ),
            },
            {
                "question": "Do I get future updates?",
                "answer": (
                    "Absolutely. Gumroad automatically notifies you of any updates to this product. "
                    "Future versions are free for all existing customers — no repurchasing needed."
                ),
            },
            {
                "question": "Is there a refund policy?",
                "answer": (
                    "Due to the digital nature of this product, I offer refunds within 7 days if you're unsatisfied. "
                    "Just send a message with your order number and I'll make it right. "
                    "Your satisfaction is my priority."
                ),
            },
            {
                "question": "Can I use this for client projects?",
                "answer": (
                    f"The standard license covers personal and small business use. "
                    f"If you need a commercial license to use {product_name} for multiple clients or resell outputs, "
                    "check the license file included in your download or message me for a commercial license option."
                ),
            },
            {
                "question": "I'm a complete beginner — is this too advanced for me?",
                "answer": (
                    f"{product_name} was designed to be accessible at any skill level. "
                    "Detailed setup instructions are included, and you can reach me with any questions. "
                    "If you can open a file and follow steps, you can use this successfully."
                ),
            },
            {
                "question": "How is this different from free templates online?",
                "answer": (
                    f"Free {product_type.lower()}s are generic — built for everyone, which means optimized for no one. "
                    f"{product_name} has been carefully designed and tested specifically for [your niche/use case]. "
                    "The time you save in setup and customization is worth many times the price."
                ),
            },
        ]

        # Add concern-specific FAQs
        concern_faqs = []
        for concern in common_concerns:
            concern_faqs.append({
                "question": f"What about {concern}?",
                "answer": (
                    f"Great question about {concern}. {product_name} addresses this by providing "
                    f"[specific solution related to {concern}]. Many customers have found this resolves "
                    f"the {concern} issue immediately upon setup."
                ),
            })

        all_faqs = base_faqs + concern_faqs

        return {
            "product_name": product_name,
            "product_type": product_type,
            "faq_count": len(all_faqs),
            "faqs": all_faqs,
            "formatting_tips": [
                "Use bold for questions and normal text for answers on Gumroad",
                "Put the most common/important FAQ first",
                "Keep answers under 60 words each for skim-readability",
                "Add a 'Still have questions? Message me' at the end",
            ],
            "trust_builders": [
                "Mention your response time ('I reply within 24 hours')",
                "Link to a sample/preview of the product",
                "Add a money-back guarantee statement",
                "Show your total download count once you have 50+",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# JSON Schemas for Claude tool_use
# ---------------------------------------------------------------------------

PRODUCT_TOOL_SCHEMAS: list[dict] = [
    {
        "name": "generate_product_description",
        "description": (
            "Generate compelling sales copy for a digital product. Returns a headline, "
            "hook paragraph, benefit bullets, body copy, what-you-get list, and CTA variants. "
            "Use this whenever a user wants to write or improve a product listing."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product (e.g., 'Monthly Budget Tracker Notion Template')",
                },
                "category": {
                    "type": "string",
                    "description": "Product category (e.g., 'Notion Template', 'eBook', 'Canva Template', 'Planner')",
                },
                "key_features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of key features or what the product does (3-8 items)",
                },
                "target_audience": {
                    "type": "string",
                    "description": "Who the product is for (e.g., 'freelancers', 'small business owners', 'students')",
                },
                "tone": {
                    "type": "string",
                    "description": "Writing tone: professional, casual, urgent, inspirational, or minimalist",
                    "enum": ["professional", "casual", "urgent", "inspirational", "minimalist"],
                },
            },
            "required": ["product_name", "category", "key_features", "target_audience"],
        },
    },
    {
        "name": "optimize_product_title",
        "description": (
            "Return SEO-optimized title variants for a product on a given platform. "
            "Scores each variant and identifies the best option. Use this when a user wants "
            "to improve their product title for search visibility."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "raw_title": {
                    "type": "string",
                    "description": "The current product title to optimize",
                },
                "platform": {
                    "type": "string",
                    "description": "Platform to optimize for: gumroad, etsy, or pinterest",
                    "enum": ["gumroad", "etsy", "pinterest"],
                },
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Target keywords to include in the title (optional)",
                },
            },
            "required": ["raw_title"],
        },
    },
    {
        "name": "create_product_bundle_ideas",
        "description": (
            "Generate bundle suggestions for a set of digital products, including pricing "
            "rationale, discount percentages, and marketing angles. Also returns upsell strategies "
            "and psychological pricing tips."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "products_list": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of product names to bundle (2-10 products)",
                },
                "niche": {
                    "type": "string",
                    "description": "The niche/market these products serve (e.g., 'Productivity', 'Notion Templates', 'Social Media')",
                },
            },
            "required": ["products_list", "niche"],
        },
    },
    {
        "name": "generate_faq_section",
        "description": (
            "Generate a comprehensive FAQ section for a product listing page. "
            "Covers common digital product questions plus any specific concerns provided. "
            "Also returns trust-builder tips and formatting advice."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product",
                },
                "product_type": {
                    "type": "string",
                    "description": "Type of product (e.g., 'Notion Template', 'PDF Guide', 'Canva Template')",
                },
                "common_concerns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of specific concerns to address (e.g., ['compatibility', 'skill level required'])",
                },
            },
            "required": ["product_name", "product_type"],
        },
    },
]


# ---------------------------------------------------------------------------
# Handler dispatcher
# ---------------------------------------------------------------------------

def handle_product_tool(tool_name: str, tool_input: dict) -> dict | None:
    """Route product tool calls to the right function."""
    if tool_name == "generate_product_description":
        return generate_product_description(**tool_input)
    elif tool_name == "optimize_product_title":
        return optimize_product_title(**tool_input)
    elif tool_name == "create_product_bundle_ideas":
        return create_product_bundle_ideas(**tool_input)
    elif tool_name == "generate_faq_section":
        return generate_faq_section(**tool_input)
    return None
