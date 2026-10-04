# encoding: utf-8
"""Meme Rewriter: Transforms scraped Chinese X & Reddit content into viral U.S. Zoomer/Gen-Z slang posts."""

import argparse
import json
from pathlib import Path


GENZ_MEME_SYSTEM_PROMPT = """
You are a viral U.S. Gen-Z social media creator and meme lord.
Your task is to take raw posts (from Chinese X or Reddit) and rewrite them into authentic American internet humor.

Rules:
1. Use U.S. Gen-Z & Zoomer slang naturally: "no cap", "let him cook", "crash out", "glaze", "fr fr", "main character energy", "brainrot", "skibidi", "lock in", "aura", "L/W".
2. Adapt local Chinese/Reddit metaphors to American pop culture (Super Bowl, Chipotle, CostCo, NBA, WallStreetBets, Crypto, Silicon Valley).
3. Apply viral Twitter/X structures: "POV:", "Bro really thought...", "Nobody:", "My honest reaction: 🗿".
4. Output concise, punchy tweets with maximum viral potential.
"""


def rewrite_post(item, style="genz_zoomer"):
    text = item.get("title") or item.get("raw_text") or ""
    source = item.get("source", "Reddit/X")

    # Sample rule-based transformation demo for dry-run
    if "程序员" in text or "code" in text.lower():
        adapted = "POV: You coded for 12 hours straight without testing, and the first compile passes with 0 errors 💀🔥 (bro unlocked unspoken aura)"
    elif "暴跌" in text or "抄底" in text or "crypto" in text.lower():
        adapted = "Bro bought the dip at 3 AM thinking he was the next Jordan Belfort 💀\n\nIt's so over... 🗿"
    else:
        adapted = f"Nobody:\nMe reading this post: {text[:60]}... 💀\n\nNo cap fr fr let him cook 👀"

    return {
        "original_id": item.get("id"),
        "original_text": text,
        "source": source,
        "style": style,
        "adapted_tweet": adapted
    }


def main():
    parser = argparse.ArgumentParser(description="Rewrite posts into U.S. viral memes")
    parser.add_argument("--input-file", required=True, help="Input scraped JSON file")
    parser.add_argument("--style", default="genz_zoomer", help="Humor style")
    parser.add_argument("--output", default="temp/rewritten_memes.json", help="Output path")
    args = parser.parse_args()

    in_path = Path(args.input_file)
    if not in_path.exists():
        print(f"Error: {in_path} does not exist.")
        return

    with open(in_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    rewritten = [rewrite_post(item, style=args.style) for item in items]
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rewritten, f, ensure_ascii=False, indent=2)

    print(f"Successfully rewritten {len(rewritten)} posts into U.S. viral memes -> {out_path}")


if __name__ == "__main__":
    main()
