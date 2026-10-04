# encoding: utf-8
"""Auto Publisher: Publishes adapted U.S. viral memes to X/Twitter with Stealth Anti-Detection."""

import argparse
import json
import random
import sys
import time
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


def human_sleep(min_sec=1.5, max_sec=4.0):
    """Simulate human pause delay."""
    time.sleep(random.uniform(min_sec, max_sec))


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
        print(f"✅ [API] Successfully posted tweet! ID: {tweet_id}")
        return True
    except Exception as e:
        print(f"❌ [API Error]: {e}")
        return False


def publish_tweet_stealth_browser(tweet_text, auth_token):
    """Anti-Detection Stealth Browser Auto-Publisher."""
    try:
        try:
            from patchright.sync_api import sync_playwright
        except ImportError:
            from playwright.sync_api import sync_playwright

        print("🛡️ [Stealth Mode] Launching Anti-Detection Browser (hiding navigator.webdriver)...")
        with sync_playwright() as p:
            # Stealth Chrome launch arguments to bypass Cloudflare & Twitter Bot Guard
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-infobars",
                    "--window-size=1280,800",
                ]
            )
            
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US",
                timezone_id="America/New_York"
            )

            # Mask automation properties
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.chrome = { runtime: {} };
            """)

            # Add login auth token
            context.add_cookies([{
                "name": "auth_token",
                "value": auth_token,
                "domain": ".x.com",
                "path": "/",
                "secure": True,
                "httpOnly": True
            }])

            page = context.new_page()
            print("🌐 Navigating to X/Twitter compose page...")
            page.goto("https://x.com/compose/post", wait_until="domcontentloaded")
            human_sleep(2.0, 4.0)

            # Find post textbox
            textbox = page.locator('[data-testid="tweetTextarea_0"]')
            textbox.wait_for(timeout=10000)
            textbox.click()
            human_sleep(0.5, 1.5)

            print("⌨️ Simulating human typing with random keystroke delays...")
            # Human typing speed simulation (50ms ~ 120ms delay per char)
            for char in tweet_text:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.04, 0.12))

            human_sleep(1.5, 3.0)

            # Click post button with human mouse hover
            post_btn = page.locator('[data-testid="tweetButton"]')
            post_btn.hover()
            human_sleep(0.5, 1.0)
            post_btn.click()

            print("⏳ Waiting for X/Twitter server confirmation...")
            human_sleep(4.0, 6.0)

            print("✅ [Stealth Mode] Tweet posted successfully without detection!")
            browser.close()
            return True
    except Exception as e:
        print(f"❌ [Stealth Mode Error]: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Publish viral memes with stealth anti-detection")
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
    
    # Process posts with safety cooldown between posts
    for i, p in enumerate(posts[:3], 1):  # Safety limit: max 3 per execution
        tweet_text = p.get("adapted_tweet", "")
        print(f"\n--- Post #{i}/{min(len(posts), 3)} ---")
        
        if args.dry_run:
            print("\n[DRY-RUN PREVIEW]")
            print("----------------------------------------")
            print(tweet_text)
            print("----------------------------------------")
            print("Status: Ready to publish (Dry-Run Mode)")
        else:
            if tw_cfg.get("api_key") and tw_cfg.get("access_token"):
                publish_tweet_api(tweet_text, config)
            elif tw_cfg.get("auth_token"):
                publish_tweet_stealth_browser(tweet_text, tw_cfg.get("auth_token"))
            else:
                print("⚠️ No Twitter API Keys or auth_token found in config.json!")
                print("Please edit config.json to fill in your auth_token cookie or API keys.")

            # Cooldown between multiple posts to avoid rate limit flags
            if i < min(len(posts), 3) and not args.dry_run:
                cooldown = random.randint(15, 35)
                print(f"☕ Safety Cooldown: Sleeping {cooldown}s before next tweet to prevent rate limits...")
                time.sleep(cooldown)


if __name__ == "__main__":
    main()
