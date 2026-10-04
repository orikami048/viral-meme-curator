# encoding: utf-8
"""Viral Meme & Traffic Engine Rewriter: Converts Reddit & Toutiao hot topics into high-impression U.S. tweets & visual cards."""

import argparse
import json
import sys
from pathlib import Path
try:
    from scripts.viral_card_generator import generate_viral_card
except ImportError:
    from viral_card_generator import generate_viral_card

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def rewrite_post_for_max_traffic(item, index=1):
    title = (item.get("title") or item.get("raw_text") or "").strip()
    source = item.get("source", "Toutiao/Reddit")

    # High-impression viral hooks & formatting
    if "Robotaxi" in title or "无人驾驶" in title:
        adapted = (
            "Unpopular opinion: Driverless taxis are about to destroy legacy ride-hailing overnight 💀\n\n"
            "• 100,000+ daily rides in China\n"
            "• 66% cheaper than Uber/Lyft\n"
            "• 0 awkward small talk with drivers\n\n"
            "No cap, Western taxi companies are cooked fr fr 🗿"
        )
        card_sub = "100k daily autonomous rides at 1/3 the cost of Uber"
    elif "独角兽" in title or "1人" in title or "AI Agent" in title or "App" in title:
        adapted = (
            "The 2026 tech stack is officially unhinged 💀🚀\n\n"
            "• 1 solo founder\n"
            "• 5 AI Agents handling code, marketing & CS\n"
            "• $500k/mo revenue in 72 hours\n\n"
            "Traditional 50-person tech startups are officially cooked fr fr 🗿 (unspoken +10000 aura)"
        )
        card_sub = "1 Solo Founder + 5 AI Agents = $500k/mo Revenue"
    elif "买房" in title or "游民" in title or "极简" in title:
        adapted = (
            "99% of Gen-Z are quitting the 30-year mortgage trap 💀\n\n"
            "Why buy a $500k house when you can:\n"
            "1. Work remotely from Bali / Tokyo\n"
            "2. Keep 90% of your paycheck\n"
            "3. Have 0 debt & total freedom\n\n"
            "Bro chose financial peace over pleasing boomers 🗿"
        )
        card_sub = "Why Gen-Z is rejecting 30-year mortgages for Digital Nomad freedom"
    elif "自动化" in title or "黑灯" in title or "工厂" in title:
        adapted = (
            "POV: You walk into a tech factory at 3 AM and there's 0 humans working 💀🔥\n\n"
            "• 99% automated robotics\n"
            "• 400% efficiency boost\n"
            "• 24/7 dark factory operations\n\n"
            "Lock in or get cooked in 2026 🔒"
        )
        card_sub = "24/7 Dark Factory: 99% Automated Robotics with 400% efficiency"
    elif "lock in" in title.lower() or "tiktok" in title.lower():
        adapted = (
            "Me: Locks in for 5 mins to study 🗿\n"
            "Also me: Rewards myself with 4 hours of pure brainrot TikToks 💀\n\n"
            "No cap fr fr let him cook 👀"
        )
        card_sub = "5 mins lock in -> 4 hours TikTok brainrot reward"
    else:
        adapted = (
            f"Nobody:\n{title} 💀\n\n"
            "No cap fr fr let him cook 👀"
        )
        card_sub = title[:50]

    # Automatically generate matching 1200x675 visual dark-mode card for X algorithm boost
    card_file = f"temp/card_{index}.jpg"
    generate_viral_card(title[:60], card_sub, card_file)

    return {
        "original_id": item.get("id"),
        "original_text": title,
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
