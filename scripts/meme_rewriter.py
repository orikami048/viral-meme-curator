# encoding: utf-8
"""Viral Meme & Traffic Engine Rewriter: Implements the English Internet Meme Generator Skill for native, effortless X/Twitter posts."""

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


def generate_native_meme_versions(title_text):
    """Generate 3 native meme variations adhering to the English Internet Meme Generator Skill:
       1. Safe / Universally Relatable
       2. Darker / More Cynical
       3. Weirder / More Absurd
    """
    clean_title = title_text.strip()
    
    # Version 1: Safe / Universally Relatable
    v1_safe = [
        f"POV: {clean_title.lower()}\n\n11:47 PM:\n\"Tomorrow I'm waking up early and fixing my life.\"\n\n3:16 AM:\n\"One more video.\"",
        f"Me: \"I'm protecting my peace today.\"\n\nAlso me:\nopens the exact same profile for the 17th time",
        f"POV: {clean_title.lower()}\n\none minor inconvenience happens\n\nme: \"perhaps the universe is trying to tell me something\"\n\nthe universe: \"bro you forgot your password\"",
        f"Everyone in 2026 trying to get their life together:\n\n{clean_title.lower()}\n\neveryone just clicking 'I agree' and hoping for the best"
    ]

    # Version 2: Darker / More Cynical
    v2_cynical = [
        f"Self improvement is crazy.\n\nYou spend 40 minutes reading about: {clean_title.lower()}\n\ninstead of doing the actual thing\n\nand somehow consider that research.",
        f"We used to be afraid of global disasters.\n\nNow I'm afraid my Wi-Fi will disconnect while I'm pretending to work.",
        f"POV: you finally realize nobody knows what they're doing\n\nYou: 🗿\nYour boss: 🗿\nThe doctor: 🗿\nThe government: 🗿\n\neveryone just clicking 'Accept All' and hoping nobody notices",
        f"You spend years trying to understand your life.\n\nJung: 🗿\nFreud: 🗿\nMBTI: 🗿\nAstrology: 🗿\n\n\"maybe I'm just hungry\""
    ]

    # Version 3: Weirder / More Absurd
    v3_absurd = [
        f"Me: \"I need to stop wasting my time.\"\n\nAlso me at 2:43 AM:\nresearching if {clean_title.lower()} is technically legal in international waters",
        f"Nobody:\n\nAbsolutely nobody:\n\nMe at 3 AM:\n\"Maybe I should completely delete my online footprint and move to a farm.\"",
        f"Top: Me saying everything is under control\n\nMiddle: One email arrives about '{clean_title.lower()}'\n\nBottom: The ancient survival instincts return 🗿",
        f"POV: {clean_title.lower()}\n\noverthinking level: 1000%\nactual problem: bro forgot to drink water"
    ]

    return {
        "safe": random.choice(v1_safe),
        "cynical": random.choice(v2_cynical),
        "absurd": random.choice(v3_absurd)
    }


def rewrite_post_for_max_traffic(item, index=1):
    raw_title = (item.get("title") or item.get("raw_text") or "").strip()
    img_url = item.get("url")
    source = item.get("source", "r/memes")

    # Step 1: Download real visual scene image from Reddit
    scene_image_path = download_meme_image(img_url, index=index)

    # Step 2: Generate 3 native meme variations
    versions = generate_native_meme_versions(raw_title)

    # Pick version based on rotation / index
    if index % 3 == 1:
        chosen_tweet = versions["safe"]
        variant_tag = "Safe/Relatable"
    elif index % 3 == 2:
        chosen_tweet = versions["cynical"]
        variant_tag = "Darker/Cynical"
    else:
        chosen_tweet = versions["absurd"]
        variant_tag = "Weirder/Absurd"

    return {
        "original_id": item.get("id"),
        "original_text": raw_title,
        "source": source,
        "variant": variant_tag,
        "adapted_tweet": chosen_tweet,
        "all_versions": versions,
        "image_path": scene_image_path
    }


def main():
    parser = argparse.ArgumentParser(description="Rewrite Reddit posts using native English Internet Meme Generator skill rules")
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

    print(f"🔥 Successfully converted {len(rewritten)} Reddit posts using English Internet Meme Generator Skill -> {out_path}")


if __name__ == "__main__":
    main()
