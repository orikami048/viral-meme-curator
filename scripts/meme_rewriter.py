# encoding: utf-8
"""Viral Meme & Traffic Engine Rewriter: Converts Reddit & Toutiao hot topics into high-impression U.S. tweets & visual cards."""

import argparse
import json
import random
import sys
from pathlib import Path

try:
    from scripts.viral_card_generator import generate_viral_card, THEMES
except ImportError:
    from viral_card_generator import generate_viral_card, THEMES

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def rewrite_post_for_max_traffic(item, index=1):
    raw_title = (item.get("title") or item.get("raw_text") or "").strip()
    source = item.get("source", "Toutiao/Reddit")
    theme_keys = list(THEMES.keys())
    selected_theme = theme_keys[(index - 1) % len(theme_keys)]

    # High-impression viral hooks & English card titles
    if "Robotaxi" in raw_title or "无人驾驶" in raw_title:
        adapted = (
            "Unpopular opinion: Driverless taxis are about to destroy legacy ride-hailing overnight 💀\n\n"
            "• 100,000+ daily rides in China\n"
            "• 66% cheaper than Uber/Lyft\n"
            "• 0 awkward small talk with drivers\n\n"
            "No cap, Western taxi companies are cooked fr fr 🗿"
        )
        card_title = "Driverless Taxis Take Over 100,000+ Daily Rides"
        card_sub = "100k daily autonomous rides at 1/3 the cost of Uber"
    elif "独角兽" in raw_title or "1人" in raw_title or "AI Agent" in raw_title or "App" in raw_title:
        adapted = (
            "The 2026 tech stack is officially unhinged 💀🚀\n\n"
            "• 1 solo founder\n"
            "• 5 AI Agents handling code, marketing & CS\n"
            "• $500k/mo revenue in 72 hours\n\n"
            "Traditional 50-person tech startups are officially cooked fr fr 🗿 (unspoken +10000 aura)"
        )
        card_title = "1 Solo Founder + 5 AI Agents = $500k/mo Revenue"
        card_sub = "Traditional 50-person tech startups are officially cooked"
    elif "买房" in raw_title or "游民" in raw_title or "极简" in raw_title:
        adapted = (
            "99% of Gen-Z are quitting the 30-year mortgage trap 💀\n\n"
            "Why buy a $500k house when you can:\n"
            "1. Work remotely from Bali / Tokyo\n"
            "2. Keep 90% of your paycheck\n"
            "3. Have 0 debt & total freedom\n\n"
            "Bro chose financial peace over pleasing boomers 🗿"
        )
        card_title = "99% of Gen-Z are Rejecting 30-Year Mortgages"
        card_sub = "Why Gen-Z chooses financial freedom over boomer debt"
    elif "lock in" in raw_title.lower() or "tiktok" in raw_title.lower():
        adapted = (
            "Me: Locks in for 5 mins to study 🗿\n"
            "Also me: Rewards myself with 4 hours of pure brainrot TikToks 💀\n\n"
            "No cap fr fr let him cook 👀"
        )
        card_title = "5 Mins Lock In -> 4 Hours TikTok Brainrot Reward"
        card_sub = "The ultimate 2026 study reward cycle"
    elif "thanos" in raw_title.lower() or "bro" in raw_title.lower() or "trusting" in raw_title.lower():
        adapted = (
            f"POV: {raw_title} 💀🔥\n\n"
            "Bro thought he was locked in but got caught in 4K fr fr 🗿\n"
            "No cap, internet never disappoints."
        )
        card_title = raw_title[:60]
        card_sub = "Caught in 4K on the timeline"
    else:
        # Dynamic English template for Reddit memes
        templates = [
            f"POV: {raw_title} 💀\n\nNo cap, this is literally every single one of us in 2026 🗿",
            f"Unpopular Opinion: {raw_title} 🚀\n\nBro really thought he could slip away unnoticed fr fr 👀",
            f"Nobody:\nAbsolutly nobody:\nMe after seeing '{raw_title}': 💀🔥",
            f"The reality of 2026 in 1 tweet: {raw_title} 🗿\n\nLet him cook fr fr!"
        ]
        adapted = random.choice(templates)
        card_title = raw_title[:60] if raw_title else "2026 Viral Reality Check"
        card_sub = "No cap fr fr let him cook"

    # Generate matching visual card with English title & CJK font fallback
    card_file = f"temp/card_{index}.jpg"
    generate_viral_card(card_title, card_sub, card_file, theme_name=selected_theme)

    return {
        "original_id": item.get("id"),
        "original_text": raw_title,
        "source": source,
        "adapted_tweet": adapted,
        "image_path": card_file
    }


def main():
    parser = argparse.ArgumentParser(description="Rewrite posts for maximum traffic & viral impressions")
    parser.add_argument("--input-file", required=True, help="Input scraped JSON file")
    parser.add_argument("--output", default="temp/rewritten_memes.json", help="Output path")
    args = parser.parse_args()

    in_path = Path(args.input_file)
    if not in_path.exists():
        print(f"Error: {in_path} does not exist.")
        return

    with open(in_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    rewritten = [rewrite_post_for_max_traffic(item, index=i+1) for i, item in enumerate(items)]
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rewritten, f, ensure_ascii=False, indent=2)

    print(f"🔥 Successfully converted {len(rewritten)} posts into high-impression viral tweets + visual cards -> {out_path}")


if __name__ == "__main__":
    main()
