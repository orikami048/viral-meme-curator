# encoding: utf-8
"""Viral Meme & Traffic Engine Rewriter: Cold, Absurd & Deadpan Humorous Rewrite Engine for X/Twitter."""

import argparse
import json
import os
import random
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def download_meme_image(url, index=1):
    """Download the actual real Reddit visual meme scene image."""
    if not url or not (url.startswith("http://") or url.startswith("https://")):
        return None
    try:
        from curl_cffi import requests
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200 and len(r.content) > 2000:
            ext = ".png" if ".png" in url.lower() else ".jpg"
            out_file = Path(__file__).resolve().parent.parent / "temp" / f"scene_meme_{index}{ext}"
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, "wb") as f:
                f.write(r.content)
            print(f"🖼️ Downloaded real Reddit scene photo: {out_file}")
            return str(out_file)
    except Exception as e:
        print(f"Notice: Failed to download scene photo from {url}: {e}")
    return None


def generate_cold_absurd_tweet(raw_title):
    """Generate high-impression cold, deadpan & absurd tweets (ChatGPT/User Persona Style)."""
    clean_title = raw_title.strip()
    
    # 1. Check for specific topic matches
    if "lock in" in clean_title.lower() or "tiktok" in clean_title.lower() or "study" in clean_title.lower():
        return (
            "me: \"I'm locking in today to fix my life\"\n\n"
            "one minor inconvenience happens\n\n"
            "me: \"perhaps the universe is telling me to sleep 14 hours\"\n\n"
            "the universe: \"bro you just forgot your password\""
        )
    
    if "work" in clean_title.lower() or "job" in clean_title.lower() or "boss" in clean_title.lower():
        return (
            "We used to be afraid of global chaos.\n\n"
            "Now I'm afraid my Wi-Fi will disconnect while I'm pretending to work."
        )

    if "ai" in clean_title.lower() or "tech" in clean_title.lower() or "bot" in clean_title.lower():
        return (
            "POV: you finally realize nobody knows what they're doing\n\n"
            "You: 🗿\n"
            "Your boss: 🗿\n"
            "The engineer: 🗿\n"
            "The AI: 🗿\n\n"
            "everyone just clicking 'I agree' and hoping for the best"
        )

    if "self" in clean_title.lower() or "mind" in clean_title.lower() or "life" in clean_title.lower():
        return (
            "POV: you spent years trying to understand yourself\n\n"
            "Philosophy: 🗿\n"
            "Psychology: 🗿\n"
            "MBTI test: 🗿\n"
            "Astrology: 🗿\n\n"
            "“maybe I'm just hungry”"
        )

    # 2. Universal Cold/Absurd Viral Formats for any Reddit topic
    formats = [
        # Format A: Universal cluelessness 🗿 Grid
        (
            f"POV: {clean_title.lower()}\n\n"
            "You: 🗿\n"
            "The internet: 🗿\n"
            "The experts: 🗿\n"
            "The universe: 🗿\n\n"
            "everyone just pretending they saw nothing"
        ),
        # Format B: Monologue vs Mundane Reality
        (
            f"me: \"finally getting my life together\"\n\n"
            f"also me after encountering '{clean_title.lower()}':\n\n"
            "\"perhaps I should restart my router and pretend today didn't happen\""
        ),
        # Format C: Cold Contrast
        (
            f"Remember when life was simple?\n\n"
            f"Now we're out here dealing with: {clean_title.lower()}\n\n"
            "and everyone is just clicking 'Accept All Cookies' hoping it fixes everything"
        ),
        # Format D: Deadpan Realization
        (
            f"POV: {clean_title}\n\n"
            "overthinking level: 100%\n"
            "actual problem: bro forgot to drink water"
        )
    ]

    return random.choice(formats)


def rewrite_post_for_max_traffic(item, index=1):
    raw_title = (item.get("title") or item.get("raw_text") or "").strip()
    img_url = item.get("url")
    source = item.get("source", "r/memes")

    # Step 1: Download real visual scene image from Reddit
    scene_image_path = download_meme_image(img_url, index=index)

    # Step 2: Generate cold, absurd, deadpan viral tweet
    adapted = generate_cold_absurd_tweet(raw_title)

    return {
        "original_id": item.get("id"),
        "original_text": raw_title,
        "source": source,
        "adapted_tweet": adapted,
        "image_path": scene_image_path
    }


def main():
    parser = argparse.ArgumentParser(description="Rewrite Reddit posts in cold, absurd deadpan viral style")
    parser.add_argument("--input-file", default="temp/reddit_trending.json", help="Input scraped JSON file")
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

    print(f"🔥 Successfully converted {len(rewritten)} Reddit posts into cold absurd viral tweets -> {out_path}")


if __name__ == "__main__":
    main()
