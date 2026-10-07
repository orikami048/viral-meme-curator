# encoding: utf-8
"""Unfiltered Story Rewriter: Rewrites raw Reddit stories into 100% Western/U.S. Unfiltered Viral Tweets."""

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
    """Download associated image if available."""
    if not url or not (url.startswith("http://") or url.startswith("https://")):
        return None
    try:
        from curl_cffi import requests
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200 and len(r.content) > 3000:
            ext = ".png" if ".png" in url.lower() else ".jpg"
            out_file = Path(__file__).resolve().parent.parent / "temp" / f"story_img_{index}{ext}"
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, "wb") as f:
                f.write(r.content)
            return str(out_file)
    except Exception:
        pass
    return None


def rewrite_to_western_unfiltered_story(item, index=1):
    raw_title = item.get("title", "").strip()
    img_url = item.get("url")
    img_path = download_meme_image(img_url, index=index)
    title_lower = raw_title.lower()

    # Pre-crafted high-converting Western Unfiltered Templates
    templates = [
        # SEC Southern Girls Archetype
        (
            "A hard truth:\n\n"
            "Southern SEC college girls are the least fake people on earth.\n\n"
            "5’10 in cowboy boots, wearing a tiny sundress, outdrinking every guy at the tailgate by 2 PM without even sweating.\n\n"
            "On the drinking table she'll put you under the floor, off the table she doesn't play games—if she likes you, she'll grab you by the collar and drag you back to her truck.\n\n"
            "Absolute chaos in bedroom, screaming loud enough to wake up the whole fraternity house, and when it's over she slaps your shoulder and asks if you need a Gatorade."
        ),
        # Vegas Strip Club Security Insider Gossip
        (
            "A buddy who runs security at a top Vegas strip club told me this.\n\n"
            "He said a massive wave of Eastern European girls just landed in town, and it’s completely wrecking the local market.\n\n"
            "Most critical part: they’re insanely affordable.\n\n"
            "Word is a few hundred bucks gets you a full VIP table experience that used to cost $5,000.\n\n"
            "Local promoters are losing their minds right now."
        ),
        # Miami Nightlife Unhinged Party Archetype
        (
            "A guy from Miami told me a fact about Florida girls.\n\n"
            "They don't do subtle.\n\n"
            "She shows up in a micro-bikini, drinks 4 shots of tequila before 1 PM, and drives a $90k lifted Bronco her ex-husband paid for.\n\n"
            "She'll argue with a cop at 3 AM, win the argument, and then drag you into the ocean at sunrise.\n\n"
            "Zero filter, zero apology, total unhinged perfection."
        ),
        # Texas Country Girl Hardcore Honesty
        (
            "Unfiltered reality:\n\n"
            "Texas country girls are built completely different.\n\n"
            "No 2-hour makeup routine, no fake Instagram personality—just short shorts, cowboy boots, and an engine she can fix herself.\n\n"
            "She'll out-drink your whole friend group, carry a 50lb feed bag like it's a purse, and when she wants you, there's zero guessing.\n\n"
            "Pure unhinged honesty from start to finish."
        ),
        # LA Influencer vs Reality
        (
            "An unspoken rule of LA dating:\n\n"
            "The girl preaching 'protecting my peace' on Instagram is always the most chaotic human in real life.\n\n"
            "Drinks $14 matcha oat lattes, has 3 spiritual coaches, and does 40-minute manifestation rituals.\n\n"
            "Then at 2 AM she texts her toxic ex, starts a 3-hour screaming match in a valet line, and blames it on Mercury in retrograde.\n\n"
            "Zero self-awareness, 100% comedy."
        ),
        # NYC Subway / East Coast Brutal Directness
        (
            "A guy from NYC told me the most honest thing I've ever heard.\n\n"
            "East Coast people aren't mean, they just don't have time for your fake polite routine.\n\n"
            "A guy in Queens will scream 'GET OUT OF THE WAY' at you, then immediately step in to help you carry a heavy suitcase up 4 flights of subway stairs.\n\n"
            "Brutally aggressive on the outside, 100% reliable on the inside."
        )
    ]

    # Dynamic adaptation based on raw_title topic
    if "tinder" in title_lower or "bio" in title_lower or "height" in title_lower:
        chosen_tweet = (
            "A hard truth about modern dating:\n\n"
            f"Why write '{raw_title[:60]}' in your bio when everyone already knows?\n\n"
            "No 2-hour fake personality routine—just state what you want and leave.\n\n"
            "People who play games in 2026 are just wasting their own time."
        )
    elif "anon" in title_lower or "greentext" in title_lower:
        chosen_tweet = (
            f"Unfiltered internet reality:\n\n"
            f"{raw_title[:100]}\n\n"
            "No filter, no sugarcoating.\n\n"
            "This is why late-night Twitter is still the funniest place on earth."
        )
    else:
        # Rotate through high-converting core templates
        chosen_tweet = templates[(index - 1) % len(templates)]

    return {
        "original_id": item.get("id"),
        "original_text": raw_title,
        "source": item.get("source", "r/Reddit"),
        "adapted_tweet": chosen_tweet,
        "image_path": img_path
    }


def main():
    parser = argparse.ArgumentParser(description="Rewrite Reddit posts into Western Unfiltered Storytelling tweets")
    parser.add_argument("--input-file", default="temp/unfiltered_raw_stories.json", help="Input scraped stories JSON")
    parser.add_argument("--output", default="temp/rewritten_memes.json", help="Output path for publisher")
    args = parser.parse_args()

    in_path = Path(args.input_file)
    if not in_path.exists():
        print(f"Error: {in_path} does not exist.")
        return

    with open(in_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    rewritten = [rewrite_to_western_unfiltered_story(item, index=i+1) for i, item in enumerate(items)]
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rewritten, f, ensure_ascii=False, indent=2)

    print(f"🔥 Successfully converted {len(rewritten)} stories into Western Unfiltered Viral Tweets -> {out_path}")


if __name__ == "__main__":
    main()
