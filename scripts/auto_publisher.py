# encoding: utf-8
"""Auto Publisher: Publishes adapted U.S. viral memes to X/Twitter using official API or Playwright."""

import argparse
import json
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_config():
    config_path = Path(__file__).resolve().parent.parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load config.json: {e}")
    return {}


def publish_tweet_api(tweet_text, config):
    """Publish using official Twitter API v2 / Tweepy."""
    try:
        import tweepy
        tw_cfg = config.get("twitter", {})
        client = tweepy.Client(
            consumer_key=tw_cfg.get("api_key"),
            consumer_secret=tw_cfg.get("api_secret"),
            access_token=tw_cfg.get("access_token"),
            access_token_secret=tw_cfg.get("access_token_secret")
        )
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data.get("id")
        print(f"✅ Successfully posted tweet! ID: {tweet_id}")
        print(f"URL: https://x.com/user/status/{tweet_id}")
        return True
    except Exception as e:
        print(f"❌ Failed to publish via Twitter API: {e}")
        return False


def publish_tweet_playwright(tweet_text, auth_token):
    """Fallback: Publish via Playwright browser session with auth_token cookie."""
    try:
        from playwright.sync_api import sync_playwright
        print("Launching stealth browser for X/Twitter auto-publish...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            context.add_cookies([{
                "name": "auth_token",
                "value": auth_token,
                "domain": ".x.com",
                "path": "/"
            }])
            page = context.new_page()
            page.goto("https://x.com/compose/post")
            page.wait_for_timeout(3000)
            
            # Fill tweet content
            box = page.locator('[data-testid="tweetTextarea_0"]')
            box.fill(tweet_text)
            page.wait_for_timeout(1000)
            
            # Click post button
            post_btn = page.locator('[data-testid="tweetButton"]')
            post_btn.click()
            page.wait_for_timeout(5000)
            print("✅ Successfully posted tweet via Browser Automation!")
            browser.close()
            return True
    except Exception as e:
        print(f"❌ Failed to publish via Browser Automation: {e}")
        return False


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

    config = load_config()
    tw_cfg = config.get("twitter", {})

    print(f"Loaded {len(posts)} posts for platform '{args.platform}' (Dry-Run: {args.dry_run})...")
    
    for i, p in enumerate(posts, 1):
        tweet_text = p.get("adapted_tweet", "")
        print(f"\n--- Post #{i} ---")
        
        if args.dry_run:
            print("\n[DRY-RUN PREVIEW]")
            print("----------------------------------------")
            print(tweet_text)
            print("----------------------------------------")
            print("Status: Ready to publish (Dry-Run Mode)")
        else:
            # Check configured publish method
            if tw_cfg.get("api_key") and tw_cfg.get("access_token"):
                publish_tweet_api(tweet_text, config)
            elif tw_cfg.get("auth_token"):
                publish_tweet_playwright(tweet_text, tw_cfg.get("auth_token"))
            else:
                print("⚠️ No Twitter API Keys or auth_token found in config.json!")
                print("Please edit config.json to fill in your Twitter API keys or auth_token cookie.")


if __name__ == "__main__":
    main()
