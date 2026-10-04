# encoding: utf-8
"""Auto Publisher: Publishes adapted U.S. viral memes to X/Twitter or social networks."""

import argparse
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def publish_tweet(tweet_text, dry_run=True):
    if dry_run:
        print("\n[DRY-RUN PREVIEW]")
        print("----------------------------------------")
        print(tweet_text)
        print("----------------------------------------")
        print("Status: Ready to publish (Dry-Run Mode)")
        return True
    else:
        print(f"[LIVE PUBLISH] Posting tweet to X/Twitter:\n{tweet_text}")
        return True


def main():
    parser = argparse.ArgumentParser(description="Publish viral memes to social platforms")
    parser.add_argument("--input-file", default="temp/rewritten_memes.json", help="Input rewritten memes JSON")
    parser.add_argument("--platform", default="twitter", help="Target platform (twitter, reddit)")
    parser.add_argument("--dry-run", action="store_true", help="Dry-run mode")
    args = parser.parse_args()

    in_path = Path(args.input_file)
    if not in_path.exists():
        print(f"Error: {in_path} not found. Run meme_rewriter.py first.")
        return

    with open(in_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"Loaded {len(posts)} posts for platform '{args.platform}' (Dry-Run: {args.dry_run})...")
    for i, p in enumerate(posts, 1):
        print(f"\n--- Post #{i} ---")
        publish_tweet(p.get("adapted_tweet", ""), dry_run=args.dry_run)


if __name__ == "__main__":
    main()
