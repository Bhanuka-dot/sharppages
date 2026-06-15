"""
Marketing tools for Sharp Pages Selling Bot.
Covers Pinterest pin generation, email sequences, social captions, and launch planning.
"""

from __future__ import annotations

from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def generate_pinterest_pins(
    product_name: str,
    key_benefit: str,
    target_audience: str,
    style: str = "inspirational",
) -> dict:
    """
    Generate 5 Pinterest pin title + description combos with keyword-rich text
    optimized for saves, click-throughs, and search visibility.
    """
    try:
        style_map = {
            "inspirational": ("dream", "transform", "finally", "imagine"),
            "educational": ("learn", "discover", "step-by-step", "how to"),
            "minimalist": ("simple", "clean", "effortless", "streamlined"),
            "bold": ("stop", "never again", "the secret", "what nobody tells you"),
            "curiosity": ("surprising", "this changed", "you won't believe", "hidden"),
        }
        style_words = style_map.get(style.lower(), style_map["inspirational"])

        audience_lower = target_audience.lower()
        product_lower = product_name.lower()
        benefit_lower = key_benefit.lower()

        pins = [
            {
                "pin_number": 1,
                "pin_type": "Problem-Solution",
                "title": f"The {product_name} That {audience_lower.title()} Are Obsessed With",
                "description": (
                    f"Tired of [pain point]? This {product_lower} is exactly what you need. "
                    f"Designed for {audience_lower} who want to {benefit_lower} without spending hours on setup. "
                    f"✨ Instant download — use it today. Save this pin to find it later! "
                    f"#digitalproduct #{product_name.replace(' ', '').lower()} #instantdownload "
                    f"#{audience_lower.replace(' ', '')} #productivitytips #digitaldownload"
                ),
                "visual_suggestion": "Before/after split image — cluttered desk vs. clean organized workspace",
                "cta": "Click to get instant access",
                "estimated_saves": "High",
            },
            {
                "pin_number": 2,
                "pin_type": "How-To / Educational",
                "title": f"How to {key_benefit.title()} (Even If You're a Complete Beginner)",
                "description": (
                    f"Step 1: Download {product_name} ✅\n"
                    f"Step 2: Customize it to your brand in minutes ✅\n"
                    f"Step 3: {key_benefit.title()} starting today ✅\n\n"
                    f"Perfect for {audience_lower} who want results without the learning curve. "
                    f"📥 Link in bio to download. "
                    f"#howto #{product_lower.replace(' ', '')} #{audience_lower.replace(' ', '')} "
                    f"#beginnerguide #digitaltemplate #worksmarternotharder"
                ),
                "visual_suggestion": "Clean step-by-step infographic with numbered icons on white/light background",
                "cta": "Save this to remember the steps",
                "estimated_saves": "Very High",
            },
            {
                "pin_number": 3,
                "pin_type": "Transformation / Result",
                "title": f"{style_words[2].title()} — I Used This {product_name} to {key_benefit.title()}",
                "description": (
                    f"\"{style_words[0].title()} about {benefit_lower} — it changed everything.\" "
                    f"Real {audience_lower} are using {product_name} to {benefit_lower} in record time. "
                    f"This isn't just another template — it's a complete system that actually works. "
                    f"🔗 Download link in bio. Save this pin! "
                    f"#testimonial #digitalproduct #{product_lower.replace(' ', '')} "
                    f"#successstory #{audience_lower.replace(' ', '')}wins"
                ),
                "visual_suggestion": "Mockup of the product on a laptop/iPad with clean background and text overlay showing result",
                "cta": "Click to see what's inside",
                "estimated_saves": "Medium-High",
            },
            {
                "pin_number": 4,
                "pin_type": "Value / Tips List",
                "title": f"7 Ways {audience_lower.title()} Use {product_name} to {key_benefit.title()}",
                "description": (
                    f"You can use {product_name} to:\n"
                    f"→ {benefit_lower.capitalize()}\n"
                    f"→ Save hours every week\n"
                    f"→ Look more professional immediately\n"
                    f"→ Stay consistent with less effort\n"
                    f"→ Track progress at a glance\n"
                    f"→ Scale without the chaos\n"
                    f"→ Impress clients/followers from day one\n\n"
                    f"📌 Save this + click to download. "
                    f"#tips #{product_lower.replace(' ', '')} #digitaltemplates "
                    f"#productivity #{audience_lower.replace(' ', '')}life"
                ),
                "visual_suggestion": "Text-heavy pin with bullet points, branded colors, clean font on solid background",
                "cta": "Save this checklist",
                "estimated_saves": "Very High",
            },
            {
                "pin_number": 5,
                "pin_type": "Curiosity / Intrigue",
                "title": f"What {style_words[2].title()} About {product_name} for {audience_lower.title()}",
                "description": (
                    f"{style_words[3].title()}: {product_name} is the one tool most {audience_lower} "
                    f"wish they'd found sooner. It's the difference between struggling with [pain] "
                    f"and actually {benefit_lower} — on your own terms. "
                    f"⚡ Under $30. Instant download. No fluff. "
                    f"Click the link to see what you've been missing. "
                    f"#musthave #{product_lower.replace(' ', '')} #digitaltool "
                    f"#smallbusinesses #passiveincome #creatortools"
                ),
                "visual_suggestion": "Eye-catching typography pin with bold statement and minimalist design",
                "cta": "See what's inside →",
                "estimated_saves": "Medium",
            },
        ]

        return {
            "product_name": product_name,
            "key_benefit": key_benefit,
            "target_audience": target_audience,
            "style": style,
            "pins": pins,
            "total_pins": len(pins),
            "pinterest_best_practices": [
                "Pin size: 1000x1500px (2:3 ratio) performs best — use Canva",
                "Post fresh pins daily — Pinterest rewards new content",
                "Use all 5 pins across different boards and times for maximum reach",
                "Best posting times: Tuesday-Thursday, 8-11pm EST",
                "Add your Gumroad link in pin destination URL and in bio",
                "Rich pins with proper Open Graph tags get 50% more engagement",
            ],
            "board_strategy": {
                "primary_board": f"{target_audience.title()} Resources & Tools",
                "secondary_boards": [
                    "Digital Downloads",
                    f"For {target_audience.title()}",
                    "Productivity Tips",
                    "Digital Products I Love",
                ],
                "tip": "Pin each image to 3-5 relevant boards for 3x the exposure",
            },
            "scheduling_tip": "Schedule pins 2-3 weeks in advance using Tailwind or Pinterest's native scheduler",
        }
    except Exception as e:
        return {"error": str(e)}


def create_email_sequence(
    product_name: str,
    sequence_type: str = "welcome",
    brand_voice: str = "friendly",
) -> dict:
    """
    Generate a multi-email sequence (welcome, nurture, or promotional).
    Returns subject lines and full email bodies for each email.
    """
    try:
        voice_style = {
            "friendly": ("Hey!", "Hope you're having an amazing day", "Cheers"),
            "professional": ("Hello,", "I hope this message finds you well", "Best regards"),
            "casual": ("Hey there,", "Quick one from me today", "Talk soon"),
            "inspirational": ("Hello, creator!", "Today I want to share something powerful", "Keep creating"),
        }.get(brand_voice.lower(), ("Hi!", "Hope you're doing well", "Best"))

        greeting, warmup, sign_off = voice_style

        sequences = {
            "welcome": [
                {
                    "email_number": 1,
                    "send_timing": "Immediately after signup/purchase",
                    "subject": f"You're in! Here's your {product_name} download 🎉",
                    "preview_text": "Your instant access is ready — plus a quick start tip",
                    "body": f"""{greeting}

Welcome to the Sharp Pages community — I'm so glad you're here!

Your download link for {product_name} is below:

[DOWNLOAD LINK]

**Getting started in 3 steps:**
1. Download the file and save it somewhere you can find easily
2. Follow the included setup guide (takes under 10 minutes)
3. Hit reply and let me know you're in — I read every message

{product_name} was created specifically for people like you who want to [main benefit] without the overwhelm.

One quick tip: The most common mistake people make when they first open it is trying to customize everything at once. Start with just the core section first — you can always customize more later.

Any questions? Just hit reply.

{sign_off},
[Your Name]

P.S. Tomorrow I'll send you my top 3 tips for getting the most out of {product_name}. Watch for it!""",
                },
                {
                    "email_number": 2,
                    "send_timing": "Day 2",
                    "subject": f"3 things to do with {product_name} first",
                    "preview_text": "Don't skip #2 — it's the game-changer",
                    "body": f"""{greeting}

Yesterday you downloaded {product_name} — by now you've probably opened it and started poking around.

Here are the 3 things I recommend doing first:

**1. Set up the main framework**
Don't customize colors yet. Get the core structure working for your situation first. This takes 15-20 minutes and makes everything else easier.

**2. Do a 'test run' with one real example** ← don't skip this
Use real data/content from your actual work. This is where it clicks. Templates feel abstract until you see YOUR information inside them.

**3. Identify your 'quick win'**
What's the one thing {product_name} can solve for you THIS WEEK? Focus there first. The rest can wait.

Most people try to set up everything on day one and then never actually use what they built. Resist that urge.

Let me know where you're at — reply with "set up" or "haven't started yet" and I'll send you the right next steps.

{sign_off},
[Your Name]""",
                },
                {
                    "email_number": 3,
                    "send_timing": "Day 5",
                    "subject": "How's it going with [product name]?",
                    "preview_text": "Three days in — a quick check-in",
                    "body": f"""{greeting}

You've had {product_name} for a few days now. How's it going?

If you've been using it: amazing! I'd love to hear what's working for you. Reply and tell me — your feedback genuinely helps me improve it.

If you haven't opened it yet: totally normal! Life gets busy. Here's a 5-minute mini-challenge:

Open {product_name}, pick ONE section, and fill in just 3 pieces of information. That's it. Just 5 minutes.

You'll be surprised how much clarity that gives you.

By the way — a few customers have been asking about [related topic]. I'm thinking about creating something around that. Would that be useful to you?

Just reply "yes" or "no" — takes 2 seconds and helps me a lot.

{sign_off},
[Your Name]""",
                },
            ],
            "nurture": [
                {
                    "email_number": 1,
                    "send_timing": "Week 1",
                    "subject": "The honest truth about [niche]",
                    "preview_text": "What took me way too long to figure out",
                    "body": f"""{greeting}

I want to share something I wish someone had told me earlier about [niche].

The truth is: [most people's approach] doesn't work. And here's why...

[Insert your genuine insight/lesson — 2-3 short paragraphs]

The shortcut I found? Using a system like {product_name} to [main benefit] instead of figuring it all out from scratch.

If you don't have it yet: [LINK TO PRODUCT]

More good stuff coming your way next week.

{sign_off},
[Your Name]""",
                },
                {
                    "email_number": 2,
                    "send_timing": "Week 2",
                    "subject": "Quick tip: [specific tactic]",
                    "preview_text": "Takes 2 minutes, makes a noticeable difference",
                    "body": f"""{greeting}

Today's tip is quick but powerful:

**[Specific actionable tip related to your niche]**

Here's how to do it in under 2 minutes:
→ Step 1: [action]
→ Step 2: [action]
→ Step 3: [result]

This one thing can [specific improvement] — I see it work for customers of {product_name} all the time.

Try it today and let me know how it goes.

{sign_off},
[Your Name]""",
                },
                {
                    "email_number": 3,
                    "send_timing": "Week 3",
                    "subject": "Behind the scenes: how I built [product name]",
                    "preview_text": "The story behind what you downloaded",
                    "body": f"""{greeting}

I built {product_name} because I was frustrated.

[Tell a 2-3 sentence genuine story about why you created the product]

It took me [time] to get it right. And I want you to benefit from all of that effort without the same trial and error.

Here's what's inside that most people don't notice at first:
→ [Hidden feature/benefit 1]
→ [Hidden feature/benefit 2]
→ [Hidden feature/benefit 3]

If you haven't tried [specific feature] yet — start there. Most people say it's their favorite part.

{sign_off},
[Your Name]""",
                },
            ],
            "promotional": [
                {
                    "email_number": 1,
                    "send_timing": "5 days before sale ends",
                    "subject": f"🚨 {product_name} is on sale — but only until [date]",
                    "preview_text": f"Save [X]% before the price goes back up",
                    "body": f"""{greeting}

I have an announcement: {product_name} is on sale for the next 5 days.

**Here's the deal:**
→ Regular price: $[regular_price]
→ Sale price: $[sale_price] — you save $[savings]
→ Sale ends: [DATE] at midnight

Why am I running this sale? [Brief genuine reason — anniversary, new product launch, etc.]

This is a rare discount. I don't run sales often because I want {product_name} to retain its value.

→ [GRAB IT HERE at the sale price]

If you've been on the fence, now is the time.

{sign_off},
[Your Name]""",
                },
                {
                    "email_number": 2,
                    "send_timing": "2 days before sale ends",
                    "subject": "48 hours left (then it's back to full price)",
                    "preview_text": "Just a heads up — clock is ticking",
                    "body": f"""{greeting}

Quick heads up: the {product_name} sale ends in 48 hours.

After that, it goes back to $[regular_price].

If you're still thinking about it — here's what customers are saying:

"[Customer testimonial or result]" — [First name, role]

"[Customer testimonial or result]" — [First name, role]

Still have questions? Just reply — I'll answer personally.

→ [LAST CHANCE: Get it at $[sale_price]]

{sign_off},
[Your Name]

P.S. The price goes back up at [TIME] on [DATE]. No extensions.
""",
                },
                {
                    "email_number": 3,
                    "send_timing": "Day of sale end",
                    "subject": "⏰ Final hours — [product name] sale closes tonight",
                    "preview_text": "Last chance. For real this time.",
                    "body": f"""{greeting}

Today's the last day to grab {product_name} at the discounted price.

At midnight tonight, the price returns to $[regular_price].

This is your last reminder — I won't spam you after this.

**If you're ready:** → [CLAIM SALE PRICE NOW]

**If you're still unsure:** The only way to know if {product_name} is right for you is to try it. And with my 7-day satisfaction guarantee, you have nothing to lose.

The sale closes tonight. After that, no exceptions.

{sign_off},
[Your Name]""",
                },
            ],
        }

        selected_sequence = sequences.get(sequence_type, sequences["welcome"])

        return {
            "product_name": product_name,
            "sequence_type": sequence_type,
            "brand_voice": brand_voice,
            "email_count": len(selected_sequence),
            "emails": selected_sequence,
            "sequence_tips": {
                "open_rate_benchmarks": "Digital products: 35-50% open rate is excellent; 20-35% is typical",
                "send_frequency": "For nurture: weekly. For promo: every 2 days. For welcome: daily first 3 days",
                "best_send_times": "Tuesday-Thursday, 9-11am local time for highest open rates",
                "subject_line_tips": [
                    "Under 50 characters for mobile preview",
                    "Use numbers ('3 tips', '48 hours left')",
                    "Create curiosity or urgency — not both",
                    "Test lowercase vs. capitalized subjects",
                ],
                "tools": "ConvertKit, MailerLite, and Beehiiv all integrate well with Gumroad",
            },
            "placeholder_guide": "[BRACKETS] indicate text you need to customize with your specific details",
        }
    except Exception as e:
        return {"error": str(e)}


def generate_social_captions(
    product_name: str,
    platform: str,
    content_type: str = "promotional",
    tone: str = "conversational",
) -> dict:
    """
    Generate platform-specific captions with hashtags for social media posts.
    """
    try:
        platform_lower = platform.lower()
        tone_lower = tone.lower()

        tone_openers = {
            "conversational": ["Real talk —", "Honest question:", "Not gonna lie,", "Story time:"],
            "professional": ["Introducing", "Announcing", "Excited to share:", "For professionals:"],
            "humorous": ["POV:", "Nobody:", "Me at 2am:", "The thing about"],
            "inspirational": ["Imagine", "What if you could", "The moment everything changes:", "Your future self will thank you:"],
        }
        openers = tone_openers.get(tone_lower, tone_openers["conversational"])

        captions = []

        if platform_lower == "instagram":
            captions = [
                {
                    "caption_type": "Product Showcase",
                    "text": (
                        f"{openers[0]} {product_name} just saved me hours of [pain point] this week.\n\n"
                        f"I kept doing [manual/inefficient process] every single time I needed to [task]. "
                        f"Until I finally built a system for it — and now I'm sharing it with you.\n\n"
                        f"↓ Swipe to see what's inside ↓\n\n"
                        f"Get it via the link in my bio 🔗\n\n"
                        f"#digitalproduct #instantdownload #{product_name.replace(' ', '').lower()} "
                        f"#notiontemplate #smallbusiness #sidehustle #passiveincome #digitalcreator"
                    ),
                    "recommended_format": "Carousel (swipe images of product screenshots)",
                    "hashtag_count": 8,
                },
                {
                    "caption_type": "Value / Tip",
                    "text": (
                        f"Save this if you want to [key benefit] 📌\n\n"
                        f"The secret? {product_name} — a digital tool I created for [target audience].\n\n"
                        f"Here's what's inside:\n"
                        f"✅ [Feature 1]\n"
                        f"✅ [Feature 2]\n"
                        f"✅ [Feature 3]\n\n"
                        f"Instant download. Under $30. Link in bio.\n\n"
                        f"#tips #productivity #digitaltools #{product_name.replace(' ', '').lower()}"
                    ),
                    "recommended_format": "Single image with clean text overlay or infographic",
                    "hashtag_count": 4,
                },
                {
                    "caption_type": "Social Proof",
                    "text": (
                        f"\"[Customer quote about how {product_name} helped them]\" — @[customer]\n\n"
                        f"This is why I created {product_name}. Knowing it's making a real difference "
                        f"for [target audience] is everything.\n\n"
                        f"If you want the same results → link in bio ✨\n\n"
                        f"#testimonial #customerlove #{product_name.replace(' ', '').lower()} #digitaldownload"
                    ),
                    "recommended_format": "Testimonial graphic or screenshot with your branding",
                    "hashtag_count": 4,
                },
            ]

        elif platform_lower == "tiktok":
            captions = [
                {
                    "caption_type": "POV Hook",
                    "text": (
                        f"POV: You finally found a system to [key benefit] 🙌\n\n"
                        f"{product_name} — digital download in bio ⬇️\n\n"
                        f"#{product_name.replace(' ', '').lower()} #fyp #digitalproduct #smallbusiness #productivityhack"
                    ),
                    "recommended_format": "30-60 second video showing the product in use",
                    "hashtag_count": 5,
                    "tiktok_note": "Keep captions short — TikTok is video-first",
                },
                {
                    "caption_type": "Tutorial Teaser",
                    "text": (
                        f"How I [achieved result] using one digital tool 👇\n\n"
                        f"Link to {product_name} in bio!\n\n"
                        f"#tutorial #howto #{product_name.replace(' ', '').lower()} #digitaltools #fyp #tiktokfinds"
                    ),
                    "recommended_format": "Screen-recording walkthrough of the product",
                    "hashtag_count": 6,
                },
            ]

        elif platform_lower == "twitter" or platform_lower == "x":
            captions = [
                {
                    "caption_type": "Thread Starter",
                    "text": (
                        f"I built {product_name} after spending [X hours] doing [task] manually.\n\n"
                        f"Now it takes [X minutes].\n\n"
                        f"Here's everything inside (and why it works):"
                    ),
                    "recommended_format": "Thread — first tweet hooks, subsequent tweets reveal value",
                    "hashtag_count": 0,
                    "note": "Twitter/X threads drive more engagement than single promo tweets",
                },
                {
                    "caption_type": "Quick Value",
                    "text": (
                        f"If you're [target audience] and you're still doing [manual task] by hand,\n\n"
                        f"I made something for you: {product_name}\n\n"
                        f"[LINK]\n\n"
                        f"Instant download. Worth every penny."
                    ),
                    "recommended_format": "Single tweet with image attachment",
                    "hashtag_count": 2,
                },
            ]

        else:  # Default / LinkedIn
            captions = [
                {
                    "caption_type": "Professional Announcement",
                    "text": (
                        f"Excited to share something I've been working on: {product_name}\n\n"
                        f"As a [your role] working with [target audience], I kept seeing the same problem: "
                        f"[pain point]. So I built a solution.\n\n"
                        f"{product_name} helps [target audience] to [key benefit] without [common struggle].\n\n"
                        f"It's now available for download — link in comments (LinkedIn buries external links 😅)\n\n"
                        f"Would love your feedback if you try it!"
                    ),
                    "recommended_format": "Post with product screenshot + story-driven text",
                    "hashtag_count": 3,
                },
            ]

        return {
            "product_name": product_name,
            "platform": platform,
            "content_type": content_type,
            "tone": tone,
            "captions": captions,
            "posting_frequency": {
                "instagram": "1x/day for Reels, 3-5x/week for feed posts",
                "tiktok": "1-3x/day (TikTok rewards volume)",
                "twitter": "3-5x/day (threads 1-2x/week)",
                "linkedin": "1x/day, weekdays only",
                "pinterest": "5-10 pins/day (use a scheduler)",
            }.get(platform_lower, "Research platform-specific best practices"),
            "visual_tips": [
                "Use Canva to create consistent branded visuals",
                "Show the product in use (mockups, screenshots, screen recordings)",
                "Faces and authentic lifestyle images outperform product-only graphics",
                "Maintain consistent colors/fonts across all platforms for brand recognition",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


def create_launch_plan(
    product_name: str,
    launch_date: str,
    budget: float = 0,
    platforms: list[str] | None = None,
) -> dict:
    """
    Create a day-by-day launch checklist and content calendar for a product launch.
    """
    try:
        platforms = platforms or ["gumroad", "pinterest", "instagram"]
        platforms_lower = [p.lower() for p in platforms]

        # Parse launch date
        try:
            launch_dt = datetime.strptime(launch_date, "%Y-%m-%d")
        except ValueError:
            try:
                launch_dt = datetime.strptime(launch_date, "%m/%d/%Y")
            except ValueError:
                launch_dt = datetime.now() + timedelta(days=14)

        pre_launch_start = launch_dt - timedelta(days=14)

        # Pre-launch phase (14 days before)
        pre_launch = [
            {
                "day": "Day -14",
                "date": (launch_dt - timedelta(days=14)).strftime("%b %d"),
                "phase": "Pre-Launch Prep",
                "tasks": [
                    f"Finalize {product_name} and do a thorough quality check",
                    "Write your Gumroad listing: title, description, tags",
                    "Create 3-5 product mockup images for marketing",
                    "Set up your Gumroad product page (draft mode)",
                    "Write your launch email sequence (welcome, day 2, day 5)",
                ],
                "content": None,
            },
            {
                "day": "Day -10",
                "date": (launch_dt - timedelta(days=10)).strftime("%b %d"),
                "phase": "Audience Building",
                "tasks": [
                    "Start 'teaser' content hinting at the upcoming product",
                    "Create 5 Pinterest boards related to your niche",
                    "Start pinning 10x/day (non-promotional content to build board authority)",
                    "Email your existing list: 'Something big is coming...'",
                    "Set up a pre-launch landing page or waitlist if possible",
                ],
                "content": {
                    "email_subject": f"[Sneak peek] Something I've been working on for you...",
                    "pinterest_action": "Create boards: start pinning 3rd-party content + your own teasers",
                    "instagram": "Post a 'coming soon' teaser with blurred/partial product preview",
                },
            },
            {
                "day": "Day -7",
                "date": (launch_dt - timedelta(days=7)).strftime("%b %d"),
                "phase": "Content Blitz",
                "tasks": [
                    f"Publish a blog post related to {product_name}'s topic",
                    "Pin 10 new pins per day — mix of tips and product teasers",
                    "Create 3 Instagram/TikTok posts around the problem your product solves",
                    "Reach out to 3-5 potential affiliates or collaborators",
                    "Prepare your launch-day email (ready to send)",
                ],
                "content": {
                    "blog_post_idea": f"'The #1 mistake people make with [topic]' — CTA teases {product_name}",
                    "social_post": "Behind-the-scenes of building the product — people love process content",
                },
            },
            {
                "day": "Day -3",
                "date": (launch_dt - timedelta(days=3)).strftime("%b %d"),
                "phase": "Final Countdown",
                "tasks": [
                    f"Send email: '{product_name} launches in 3 days — here's what's inside'",
                    "Test your Gumroad purchase flow end-to-end",
                    "Prepare all social posts for launch day (schedule in advance)",
                    "Pin 5 product-specific pins (can go live on launch day)",
                    "Draft all social captions for launch day, get them approved",
                ],
                "content": {
                    "email_subject": f"Launching in 3 days: {product_name} — sneak peek inside",
                    "pinterest_pins": f"Schedule 5 {product_name} pins to go live on launch day",
                },
            },
            {
                "day": "Day -1",
                "date": (launch_dt - timedelta(days=1)).strftime("%b %d"),
                "phase": "Eve Preparation",
                "tasks": [
                    "Send 'tomorrow is the day!' email to your list",
                    "Double-check all links, downloads, and automations",
                    "Set your Gumroad product to 'published' (or schedule it)",
                    "Prepare yourself — respond to launch-day messages quickly",
                ],
                "content": {
                    "email_subject": f"Tomorrow: {product_name} goes live (early bird price included)",
                },
            },
        ]

        # Launch day
        launch_day = {
            "day": "LAUNCH DAY 🚀",
            "date": launch_dt.strftime("%b %d"),
            "phase": "Launch",
            "tasks": [
                f"Send launch email at 9am: '{product_name} is LIVE — your exclusive link'",
                "Post across all platforms simultaneously",
                "Go LIVE on Instagram/TikTok if possible — even 10 minutes boosts reach",
                "Reply to every comment and DM within 1 hour",
                f"Pin 5-10 new {product_name} pins",
                "Monitor Gumroad dashboard hourly",
                "Post a 'it's live!' story/update mid-day",
                "Send a 'final hours of launch price' email at 8pm",
            ],
            "launch_email": {
                "subject": f"🎉 It's here! {product_name} is now live",
                "preview": "Your link + early bird price — only available today",
            },
        }

        # Post-launch
        post_launch = [
            {
                "day": "Day +1",
                "date": (launch_dt + timedelta(days=1)).strftime("%b %d"),
                "tasks": [
                    "Share first results/reactions (social proof while momentum is fresh)",
                    "Reply to all customer emails and questions",
                    "Send 'thank you' post to social media",
                    "Check analytics: which platform sent the most traffic?",
                ],
            },
            {
                "day": "Day +7",
                "date": (launch_dt + timedelta(days=7)).strftime("%b %d"),
                "tasks": [
                    "Send first 'week 1 results' email to your list",
                    "Ask early buyers for testimonials/reviews",
                    "Analyze what worked: traffic sources, conversion rate, top-performing pins",
                    "Continue pinning daily on Pinterest — consistency compounds",
                ],
            },
            {
                "day": "Day +30",
                "date": (launch_dt + timedelta(days=30)).strftime("%b %d"),
                "tasks": [
                    "Review month 1 analytics and revenue",
                    "Update listing based on customer feedback",
                    "Plan first price increase or bundle",
                    "Plan next product based on what customers keep asking for",
                ],
            },
        ]

        # Budget allocation (if budget provided)
        budget_plan = None
        if budget > 0:
            budget_plan = {
                "total_budget": budget,
                "allocation": {
                    "pinterest_ads": round(budget * 0.40, 2),
                    "canva_pro_or_design": round(budget * 0.20, 2),
                    "email_platform": round(budget * 0.15, 2),
                    "affiliate_payouts": round(budget * 0.15, 2),
                    "miscellaneous": round(budget * 0.10, 2),
                },
                "note": "Pinterest ads have excellent ROI for digital product launches — prioritize them",
            }

        return {
            "product_name": product_name,
            "launch_date": launch_dt.strftime("%B %d, %Y"),
            "platforms": platforms,
            "pre_launch_phases": pre_launch,
            "launch_day": launch_day,
            "post_launch_phases": post_launch,
            "budget_plan": budget_plan,
            "kpis_to_track": {
                "day_1_goal": "10+ sales",
                "week_1_goal": "25+ sales, 3+ reviews",
                "month_1_goal": "100+ sales, 4.5+ star rating",
                "email_open_rate_target": "35%+",
                "pinterest_click_target": "50+ clicks/day by week 4",
            },
            "launch_checklist": [
                "Gumroad product published with cover image",
                "Thank-you page set up",
                "Download file tested",
                "Email automation connected",
                "Analytics tracking in place",
                "Social profiles link to Gumroad store",
                "Pinterest boards active",
                "Launch email sequence ready",
            ],
        }
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# JSON Schemas for Claude tool_use
# ---------------------------------------------------------------------------

MARKETING_TOOL_SCHEMAS: list[dict] = [
    {
        "name": "generate_pinterest_pins",
        "description": (
            "Generate 5 Pinterest pin title + description combos for a product. "
            "Covers Problem-Solution, How-To, Transformation, Tips List, and Curiosity styles. "
            "Includes visual suggestions, CTA, and Pinterest best practices."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product to create pins for",
                },
                "key_benefit": {
                    "type": "string",
                    "description": "The primary benefit or transformation (e.g., 'save 5 hours per week', 'organize your finances', 'grow your email list')",
                },
                "target_audience": {
                    "type": "string",
                    "description": "Who the product is for (e.g., 'small business owners', 'freelancers', 'students')",
                },
                "style": {
                    "type": "string",
                    "description": "Pin style: inspirational, educational, minimalist, bold, or curiosity",
                    "enum": ["inspirational", "educational", "minimalist", "bold", "curiosity"],
                },
            },
            "required": ["product_name", "key_benefit", "target_audience"],
        },
    },
    {
        "name": "create_email_sequence",
        "description": (
            "Generate a multi-email sequence for a product. Types: welcome (post-purchase onboarding), "
            "nurture (relationship-building), or promotional (sale/launch). Returns full subject lines "
            "and email bodies ready to customize."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product",
                },
                "sequence_type": {
                    "type": "string",
                    "description": "Type of email sequence: welcome, nurture, or promotional",
                    "enum": ["welcome", "nurture", "promotional"],
                },
                "brand_voice": {
                    "type": "string",
                    "description": "Tone of voice: friendly, professional, casual, or inspirational",
                    "enum": ["friendly", "professional", "casual", "inspirational"],
                },
            },
            "required": ["product_name"],
        },
    },
    {
        "name": "generate_social_captions",
        "description": (
            "Generate platform-specific social media captions for a product. "
            "Supports Instagram, TikTok, Twitter/X, and LinkedIn. Returns 2-3 caption "
            "variants per platform with hashtags and format recommendations."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product",
                },
                "platform": {
                    "type": "string",
                    "description": "Social platform: instagram, tiktok, twitter, or linkedin",
                    "enum": ["instagram", "tiktok", "twitter", "linkedin"],
                },
                "content_type": {
                    "type": "string",
                    "description": "Type of content: promotional, educational, social_proof, or behind_the_scenes",
                    "enum": ["promotional", "educational", "social_proof", "behind_the_scenes"],
                },
                "tone": {
                    "type": "string",
                    "description": "Caption tone: conversational, professional, humorous, or inspirational",
                    "enum": ["conversational", "professional", "humorous", "inspirational"],
                },
            },
            "required": ["product_name", "platform"],
        },
    },
    {
        "name": "create_launch_plan",
        "description": (
            "Create a complete day-by-day product launch plan with content calendar. "
            "Covers 14 days pre-launch through 30 days post-launch. Returns tasks, "
            "email subjects, and social content for each phase. Includes budget allocation."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Name of the product being launched",
                },
                "launch_date": {
                    "type": "string",
                    "description": "Launch date in YYYY-MM-DD or MM/DD/YYYY format",
                },
                "budget": {
                    "type": "number",
                    "description": "Marketing budget in USD (0 for organic-only launch)",
                },
                "platforms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Platforms to launch on (e.g., ['gumroad', 'pinterest', 'instagram'])",
                },
            },
            "required": ["product_name", "launch_date"],
        },
    },
]


# ---------------------------------------------------------------------------
# Handler dispatcher
# ---------------------------------------------------------------------------

def handle_marketing_tool(tool_name: str, tool_input: dict) -> dict | None:
    """Route marketing tool calls to the right function."""
    if tool_name == "generate_pinterest_pins":
        return generate_pinterest_pins(**tool_input)
    elif tool_name == "create_email_sequence":
        return create_email_sequence(**tool_input)
    elif tool_name == "generate_social_captions":
        return generate_social_captions(**tool_input)
    elif tool_name == "create_launch_plan":
        return create_launch_plan(**tool_input)
    return None
