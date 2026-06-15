"""
SEO tools for Sharp Pages Selling Bot.
Covers keyword research, listing analysis, tag generation, and content ideation.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def research_keywords(
    niche: str,
    product_type: str,
    platform: str = "gumroad",
) -> dict:
    """
    Return primary keywords, long-tail variants, search intent tags,
    and competition level estimates for the given niche and product type.
    """
    try:
        platform = platform.lower()

        # Base keyword sets by niche
        niche_lower = niche.lower()
        product_type_lower = product_type.lower()

        # Seed keywords
        seed_keywords = [
            f"{niche_lower} {product_type_lower}",
            f"digital {product_type_lower}",
            f"{niche_lower} template",
            f"printable {niche_lower}",
            f"{niche_lower} planner",
        ]

        # Long-tail variants (high intent, lower competition)
        long_tail_variants = [
            f"free {niche_lower} {product_type_lower} download",
            f"best {niche_lower} {product_type_lower} for beginners",
            f"aesthetic {niche_lower} {product_type_lower}",
            f"{niche_lower} {product_type_lower} notion",
            f"{niche_lower} {product_type_lower} google sheets",
            f"how to organize {niche_lower} {product_type_lower}",
            f"{niche_lower} tracker {product_type_lower}",
            f"minimalist {niche_lower} {product_type_lower}",
            f"{niche_lower} {product_type_lower} small business",
            f"{niche_lower} {product_type_lower} etsy",
            f"editable {niche_lower} {product_type_lower}",
            f"{niche_lower} spreadsheet {product_type_lower}",
        ]

        # Pinterest-specific keywords (visual + inspirational phrasing)
        pinterest_keywords = [
            f"{niche_lower} ideas",
            f"{niche_lower} inspiration",
            f"how to {niche_lower}",
            f"{niche_lower} tips and tricks",
            f"{niche_lower} for beginners",
            f"best {niche_lower} {product_type_lower}",
            f"{niche_lower} organization ideas",
            f"{niche_lower} printables free",
        ]

        # Gumroad-specific keywords
        gumroad_keywords = [
            f"{niche_lower} {product_type_lower} instant download",
            f"digital {niche_lower} {product_type_lower}",
            f"{niche_lower} template download",
            f"editable {niche_lower} {product_type_lower}",
        ]

        # Competition estimate by niche keyword length
        def estimate_competition(kw: str) -> str:
            word_count = len(kw.split())
            if word_count <= 2:
                return "High"
            elif word_count <= 4:
                return "Medium"
            else:
                return "Low"

        # Search intent classification
        def classify_intent(kw: str) -> str:
            kw_lower = kw.lower()
            if any(w in kw_lower for w in ["buy", "download", "get", "purchase", "free"]):
                return "Commercial/Transactional"
            elif any(w in kw_lower for w in ["how to", "tips", "guide", "tutorial", "learn"]):
                return "Informational"
            elif any(w in kw_lower for w in ["best", "top", "vs", "compare", "review"]):
                return "Commercial/Research"
            else:
                return "Navigational/Broad"

        primary_keywords = []
        for kw in seed_keywords[:4]:
            primary_keywords.append({
                "keyword": kw,
                "competition": estimate_competition(kw),
                "search_intent": classify_intent(kw),
                "priority": "High",
            })

        long_tail_list = []
        for kw in long_tail_variants[:10]:
            long_tail_list.append({
                "keyword": kw,
                "competition": estimate_competition(kw),
                "search_intent": classify_intent(kw),
                "priority": "Medium" if "best" in kw or "free" in kw else "Low",
            })

        platform_specific = pinterest_keywords if platform == "pinterest" else gumroad_keywords

        return {
            "niche": niche,
            "product_type": product_type,
            "platform": platform,
            "primary_keywords": primary_keywords,
            "long_tail_keywords": long_tail_list,
            "platform_specific_keywords": platform_specific,
            "recommended_focus_keywords": [
                seed_keywords[0],
                long_tail_variants[1],  # "best X for beginners"
                long_tail_variants[2],  # "aesthetic X"
                long_tail_variants[10], # "editable X"
            ],
            "keyword_strategy": {
                "title": f"Use '{seed_keywords[0]}' — this is your highest-priority primary keyword",
                "description": f"Naturally mention '{seed_keywords[0]}' 2-3 times in the first 100 words",
                "tags": f"Mix 3 high-competition + 7 long-tail tags for balanced reach",
                "pinterest_boards": f"Create boards named after '{pinterest_keywords[0]}' and '{pinterest_keywords[2]}'",
            },
            "seo_quick_wins": [
                f"Target '{long_tail_variants[1]}' — medium competition, high buyer intent",
                f"Pinterest: '{pinterest_keywords[3]}' is a perennial top-performer",
                "Include 'instant download' and 'editable' in your Gumroad listing — these are purchase-intent phrases",
                f"Seasonal angle: '{niche_lower} {product_type_lower} 2025' gets year-targeted traffic",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


def analyze_listing_seo(
    title: str,
    description: str,
    tags: list[str] | None = None,
) -> dict:
    """
    Analyze a product listing for SEO quality. Returns an SEO score (0-100),
    missing keywords, and actionable improvement suggestions.
    """
    try:
        tags = tags or []
        title_lower = title.lower()
        desc_lower = description.lower()
        combined = (title_lower + " " + desc_lower).lower()

        score = 0
        issues = []
        improvements = []
        strengths = []

        # Title analysis
        title_word_count = len(title.split())
        if 6 <= title_word_count <= 15:
            score += 15
            strengths.append("Title length is optimal (6-15 words)")
        elif title_word_count < 6:
            issues.append("Title is too short — add more descriptive keywords")
            improvements.append("Expand your title to 8-12 words with primary keyword first")
            score += 5
        else:
            issues.append("Title may be too long for mobile display")
            improvements.append("Trim title to under 12 words while keeping primary keyword")
            score += 10

        # Check for power words in title
        power_words = ["ultimate", "complete", "professional", "instant", "editable", "free", "best", "easy"]
        if any(pw in title_lower for pw in power_words):
            score += 10
            strengths.append("Title contains a power/conversion word")
        else:
            improvements.append(f"Add a power word to your title: {', '.join(power_words[:4])}")

        # Description length
        desc_word_count = len(description.split())
        if desc_word_count >= 150:
            score += 15
            strengths.append(f"Description has good depth ({desc_word_count} words)")
        elif desc_word_count >= 75:
            score += 8
            improvements.append("Expand description to 200+ words for better keyword coverage")
        else:
            issues.append("Description is too short — aim for 150-300 words")
            improvements.append("Rewrite description with 200+ words including benefits, features, and FAQs")
            score += 2

        # Keyword density check
        # Look for common high-value patterns
        value_phrases = ["instant download", "editable", "digital download", "template", "printable", "guide", "planner", "tracker"]
        found_phrases = [p for p in value_phrases if p in combined]
        if len(found_phrases) >= 3:
            score += 15
            strengths.append(f"Good keyword coverage: {', '.join(found_phrases[:3])}")
        elif len(found_phrases) >= 1:
            score += 7
            missing = [p for p in value_phrases[:4] if p not in combined]
            improvements.append(f"Add these high-value phrases: {', '.join(missing[:2])}")
        else:
            issues.append("Description lacks key purchase-intent phrases")
            improvements.append("Include 'instant download', 'editable', and your product type keyword")

        # Tags analysis
        if len(tags) >= 10:
            score += 15
            strengths.append(f"Good tag coverage ({len(tags)} tags)")
        elif len(tags) >= 5:
            score += 8
            improvements.append(f"Add more tags — aim for 13 (you have {len(tags)})")
        else:
            issues.append(f"Too few tags ({len(tags)}) — you're missing search traffic")
            improvements.append("Add at least 10 tags mixing broad and specific keywords")
            score += 2

        # Check if title keyword appears in description
        title_first_word = title.split()[0].lower() if title else ""
        if title_first_word and title_first_word in desc_lower:
            score += 10
            strengths.append("Primary keyword from title appears in description")
        else:
            improvements.append("Mention your product name/primary keyword in the first paragraph of your description")

        # CTA check
        cta_phrases = ["buy now", "get", "download", "grab", "add to cart", "purchase", "instant access"]
        if any(cta in desc_lower for cta in cta_phrases):
            score += 10
            strengths.append("Description includes a call-to-action")
        else:
            improvements.append("Add a clear CTA at the end of your description: 'Click Buy Now for instant access'")

        # Clamp score 0-100
        score = min(score, 100)

        # SEO grade
        if score >= 85:
            grade = "A — Excellent"
        elif score >= 70:
            grade = "B — Good"
        elif score >= 55:
            grade = "C — Needs Work"
        elif score >= 40:
            grade = "D — Poor"
        else:
            grade = "F — Critically Underoptimized"

        return {
            "seo_score": score,
            "grade": grade,
            "title_analyzed": title,
            "description_word_count": desc_word_count,
            "tags_count": len(tags),
            "tags_analyzed": tags,
            "strengths": strengths,
            "issues": issues,
            "improvements": improvements,
            "priority_fixes": improvements[:3] if improvements else ["Your listing looks well-optimized!"],
            "estimated_impact": (
                f"Fixing priority issues could boost search visibility by 20-40%. "
                f"Listings scoring 80+ receive significantly more organic traffic on Gumroad and Google."
            ),
        }
    except Exception as e:
        return {"error": str(e)}


def generate_tags(
    product_name: str,
    category: str,
    platform: str = "gumroad",
) -> dict:
    """
    Return an optimal tag list for a given platform.
    """
    try:
        platform = platform.lower()
        name_lower = product_name.lower()
        category_lower = category.lower()

        # Universal high-value tags
        universal_tags = [
            product_name.lower(),
            category_lower,
            f"digital {category_lower}",
            f"{category_lower} download",
            "instant download",
            "digital product",
            "editable template",
        ]

        # Extract key words from product name
        stop_words = {"the", "a", "an", "and", "or", "for", "in", "of", "to", "with"}
        name_words = [w for w in name_lower.split() if w not in stop_words and len(w) > 2]

        # Platform-specific tag strategies
        if platform == "gumroad":
            platform_tags = [
                f"{category_lower} template",
                "gumroad digital product",
                f"downloadable {category_lower}",
                "digital download",
                f"{' '.join(name_words[:2])} template" if len(name_words) >= 2 else f"{category_lower}",
                f"commercial use {category_lower}",
            ]
            max_tags = 10
            tag_tip = "Gumroad supports up to 10 tags — use all of them"

        elif platform == "etsy":
            platform_tags = [
                f"digital {category_lower}",
                f"printable {category_lower}",
                f"editable {category_lower}",
                "instant download",
                f"{category_lower} printable",
                "digital planner",
                f"{' '.join(name_words[:3])}" if len(name_words) >= 3 else category_lower,
                f"small business {category_lower}",
                "svg file",
                f"{category_lower} pdf",
                f"commercial use",
                f"digital file",
                f"etsy digital",
            ]
            max_tags = 13
            tag_tip = "Etsy allows 13 tags — use multi-word phrases (up to 20 chars each)"

        elif platform == "pinterest":
            platform_tags = [
                f"#{name_words[0]}{name_words[1] if len(name_words) > 1 else 'template'}",
                f"#{category_lower.replace(' ', '')}",
                "#digitalproduct",
                "#instantdownload",
                "#freeprintable",
                f"#{name_words[0]}ideas" if name_words else "#templateideas",
                "#smallbusiness",
                "#entrepreneur",
                "#digitaldownload",
                "#sidehustle",
                "#passiveincome",
                "#creatoreconomy",
                "#notiontemplate" if "notion" in name_lower or "notion" in category_lower else "#productivity",
            ]
            max_tags = 5
            tag_tip = "Pinterest works best with 3-5 hashtags per pin — less is more"
        else:
            platform_tags = []
            max_tags = 10
            tag_tip = "Use descriptive, specific tags"

        # Combine and deduplicate
        all_tags = list(dict.fromkeys(universal_tags + platform_tags))
        selected_tags = all_tags[:max_tags]

        # Also generate some long-tail tags
        long_tail_tags = [
            f"best {category_lower} for beginners",
            f"aesthetic {category_lower}",
            f"minimalist {category_lower}",
            f"{category_lower} for small business",
            f"{category_lower} 2025",
        ]

        return {
            "product_name": product_name,
            "platform": platform,
            "recommended_tags": selected_tags,
            "tag_count": len(selected_tags),
            "max_tags_allowed": max_tags,
            "long_tail_bonus_tags": long_tail_tags,
            "platform_tip": tag_tip,
            "tag_strategy": {
                "broad_tags": selected_tags[:2],
                "mid_range_tags": selected_tags[2:5],
                "specific_tags": selected_tags[5:],
                "explanation": "Balance broad (high traffic) with specific (high conversion) tags",
            },
        }
    except Exception as e:
        return {"error": str(e)}


def generate_blog_content_ideas(
    niche: str,
    audience: str,
) -> dict:
    """
    Return blog/content ideas with target keywords and content angles.
    These drive SEO traffic to your Gumroad store.
    """
    try:
        niche_lower = niche.lower()
        audience_lower = audience.lower()

        content_ideas = [
            {
                "title": f"The Ultimate Guide to {niche} for {audience.title()}",
                "content_type": "Ultimate Guide",
                "target_keyword": f"{niche_lower} guide for beginners",
                "angle": "Comprehensive how-to that establishes authority",
                "estimated_word_count": 2500,
                "cta_opportunity": f"Download our {niche} template to get started faster",
                "pinterest_board": f"{niche} Tips & Guides",
            },
            {
                "title": f"10 {niche} Mistakes {audience.title()} Make (And How to Fix Them)",
                "content_type": "Listicle / Problem-Solution",
                "target_keyword": f"{niche_lower} mistakes to avoid",
                "angle": "Empathy-driven content that shows you understand the audience's pain",
                "estimated_word_count": 1800,
                "cta_opportunity": f"Avoid mistake #7 permanently with our {niche} template",
                "pinterest_board": f"{niche} Advice",
            },
            {
                "title": f"How I Organized My Entire {niche} System in One Weekend",
                "content_type": "Personal Story / Case Study",
                "target_keyword": f"how to organize {niche_lower}",
                "angle": "Personal narrative builds trust and relatability",
                "estimated_word_count": 1200,
                "cta_opportunity": "Get the exact template I used — linked below",
                "pinterest_board": f"My {niche} Journey",
            },
            {
                "title": f"Free {niche} Template vs. Paid: Is It Worth It?",
                "content_type": "Comparison / Decision Helper",
                "target_keyword": f"free {niche_lower} template vs paid",
                "angle": "Objection handling — addresses the #1 hesitation before buying",
                "estimated_word_count": 1000,
                "cta_opportunity": "See what a professional-grade template looks like here",
                "pinterest_board": f"{niche} Tools & Resources",
            },
            {
                "title": f"The Best {niche} Tools for {audience.title()} in 2025",
                "content_type": "Resource Roundup",
                "target_keyword": f"best {niche_lower} tools 2025",
                "angle": "High-traffic 'best tools' format — great for SEO and affiliation",
                "estimated_word_count": 2000,
                "cta_opportunity": f"Our {niche} template works perfectly with these tools",
                "pinterest_board": f"{niche} Resources",
            },
            {
                "title": f"{niche} 101: Everything {audience.title()} Need to Know",
                "content_type": "Beginner's Guide",
                "target_keyword": f"{niche_lower} for beginners",
                "angle": "Targets the largest segment — beginners searching for fundamentals",
                "estimated_word_count": 2200,
                "cta_opportunity": f"Skip the learning curve: get our ready-made {niche} template",
                "pinterest_board": f"Start Here: {niche}",
            },
            {
                "title": f"30-Day {niche} Challenge: Week-by-Week Plan",
                "content_type": "Challenge / Action Plan",
                "target_keyword": f"30 day {niche_lower} challenge",
                "angle": "Highly shareable, encourages repeat visits, great for email capture",
                "estimated_word_count": 1500,
                "cta_opportunity": f"Download the tracking template to stay on track",
                "pinterest_board": f"{niche} Challenges",
            },
            {
                "title": f"What Nobody Tells You About {niche} (I Learned the Hard Way)",
                "content_type": "Contrarian / Surprising Facts",
                "target_keyword": f"{niche_lower} tips no one tells you",
                "angle": "Curiosity-driven headline with high Pinterest click-through rate",
                "estimated_word_count": 900,
                "cta_opportunity": f"Save yourself months of trial and error with our {niche} kit",
                "pinterest_board": f"{niche} Secrets",
            },
        ]

        return {
            "niche": niche,
            "target_audience": audience,
            "content_ideas": content_ideas,
            "total_ideas": len(content_ideas),
            "content_calendar_tip": (
                "Publish 2x/week minimum for 90 days to build SEO momentum. "
                "Each post should link to your Gumroad store product."
            ),
            "pinterest_strategy": {
                "create_boards": list({idea["pinterest_board"] for idea in content_ideas}),
                "pin_each_post": "Create 3-5 pins per blog post with different images and titles",
                "posting_frequency": "Pin 5-10 times per day (schedule with Tailwind or Pinterest scheduler)",
            },
            "seo_tips": [
                "Start with keyword-rich titles that match how your audience searches",
                "Each blog post = one article + 3-5 Pinterest pins = traffic compound effect",
                "Internal link every post to your store product page",
                "Build an email list CTA into every post to capture repeat visitors",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# JSON Schemas for Claude tool_use
# ---------------------------------------------------------------------------

SEO_TOOL_SCHEMAS: list[dict] = [
    {
        "name": "research_keywords",
        "description": (
            "Research SEO keywords for a niche and product type. Returns primary keywords, "
            "long-tail variants with competition levels, search intent classifications, and "
            "platform-specific keyword recommendations. Essential for any listing or content strategy."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "niche": {
                    "type": "string",
                    "description": "The market niche (e.g., 'productivity', 'budgeting', 'social media', 'wedding planning')",
                },
                "product_type": {
                    "type": "string",
                    "description": "Type of product (e.g., 'Notion template', 'eBook', 'Canva template', 'spreadsheet')",
                },
                "platform": {
                    "type": "string",
                    "description": "Platform to optimize for: gumroad, etsy, or pinterest",
                    "enum": ["gumroad", "etsy", "pinterest"],
                },
            },
            "required": ["niche", "product_type"],
        },
    },
    {
        "name": "analyze_listing_seo",
        "description": (
            "Analyze an existing product listing for SEO quality. Returns a score from 0-100, "
            "letter grade, identified issues, strengths, and specific improvement recommendations. "
            "Use this to audit listings the user has already written."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The product listing title",
                },
                "description": {
                    "type": "string",
                    "description": "The product listing description text",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of tags/keywords currently on the listing",
                },
            },
            "required": ["title", "description"],
        },
    },
    {
        "name": "generate_tags",
        "description": (
            "Generate an optimal tag list for a product on a given platform. "
            "Returns recommended tags, a tag strategy breakdown, long-tail bonus tags, "
            "and platform-specific tips. Tailored for Gumroad (10 tags), Etsy (13), or Pinterest (5)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product",
                },
                "category": {
                    "type": "string",
                    "description": "Product category (e.g., 'Notion Template', 'eBook', 'Canva Template')",
                },
                "platform": {
                    "type": "string",
                    "description": "Platform: gumroad, etsy, or pinterest",
                    "enum": ["gumroad", "etsy", "pinterest"],
                },
            },
            "required": ["product_name", "category"],
        },
    },
    {
        "name": "generate_blog_content_ideas",
        "description": (
            "Generate blog and content ideas that drive SEO traffic to a Gumroad store. "
            "Returns 8+ content ideas with target keywords, content angles, word counts, "
            "CTA opportunities, and Pinterest board recommendations."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "niche": {
                    "type": "string",
                    "description": "The content niche (e.g., 'Notion templates', 'budget planning', 'social media marketing')",
                },
                "audience": {
                    "type": "string",
                    "description": "The target audience (e.g., 'freelancers', 'small business owners', 'college students')",
                },
            },
            "required": ["niche", "audience"],
        },
    },
]


# ---------------------------------------------------------------------------
# Handler dispatcher
# ---------------------------------------------------------------------------

def handle_seo_tool(tool_name: str, tool_input: dict) -> dict | None:
    """Route SEO tool calls to the right function."""
    if tool_name == "research_keywords":
        return research_keywords(**tool_input)
    elif tool_name == "analyze_listing_seo":
        return analyze_listing_seo(**tool_input)
    elif tool_name == "generate_tags":
        return generate_tags(**tool_input)
    elif tool_name == "generate_blog_content_ideas":
        return generate_blog_content_ideas(**tool_input)
    return None
