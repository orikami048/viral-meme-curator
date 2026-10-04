# encoding: utf-8
"""Viral Meme & Traffic Engine Rewriter: Rewrites Reddit memes & downloads real visual scene photos for maximum X engagement."""

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


def rewrite_post_for_max_traffic(item, index=1):
    raw_title = (item.get("title") or item.get("raw_text") or "").strip()
    img_url = item.get("url")
    source = item.get("source", "r/memes")

    # Step 1: Download the ACTUAL real visual meme scene photo from Reddit
    scene_image_path = download_meme_image(img_url, index=index)

    # Step 2: High-impression US Gen-Z viral hooks & caption adaptations
    if "lock in" in raw_title.lower() or "tiktok" in raw_title.lower():
        adapted = (
            "Me: Locks in for 5 mins to study 🗿\n"
            "Also me: Rewards myself with 4 hours of pure brainrot TikToks 💀\n\n"
            "No cap fr fr let him cook 👀"
        )
    elif "thanos" in raw_title.lower() or "bro" in raw_title.lower() or "trusting" in raw_title.lower():
        adapted = (
            f"POV: {raw_title} 💀🔥\n\n"
            "Bro thought he was locked in but got caught in 4K fr fr 🗿\n"
            "No cap, internet never fails."
        )
    else:
        # Dynamic viral templates matching Reddit meme titles
        templates = [
            f"POV: {raw_title} 💀\n\nNo cap, this is literally every single one of us in 2026 🗿",
            f"Unpopular Opinion: {raw_title} 🚀\n\nBro really thought he could slip away unnoticed fr fr 👀",
            f"Nobody:\nAbsolutely nobody:\nMe looking at this: '{raw_title}' 💀🔥",
            f"The timeline wasn't ready for this 🗿: {raw_title}\n\nLet him cook fr fr!"
        ]
        adapted = random.choice(templates)

    return {
        "original_id": item.get("id"),
        "original_text": raw_title,
        "source": source,
        "adapted_tweet": adapted,
        "image_path": scene_image_path
    }


def main():
    parser = argparse.ArgumentParser(description="Rewrite Reddit posts & download real scene images")
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

    print(f"🔥 Successfully converted {len(rewritten)} Reddit posts with real scene images -> {out_path}")


if __name__ == "__main__":
    main()
