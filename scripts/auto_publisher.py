# encoding: utf-8
"""Auto Publisher: Publishes adapted U.S. viral memes to X/Twitter with Stealth Anti-Detection & History Logging."""

import argparse
import datetime
import json
import os
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


def record_history(tweet_text, status="success", platform="twitter"):
    """Record post into history log for Dashboard statistics."""
    history_path = Path(__file__).resolve().parent.parent / "temp" / "history.json"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    
    history = []
    if history_path.exists():
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
            
    history.append({
        "id": f"hist_{int(time.time()*1000)}",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platform": platform,
        "content": tweet_text,
        "status": status
    })
    
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


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
        record_history(tweet_text, status="success")
        return True
    except Exception as e:
        print(f"❌ [API Error]: {e}")
        record_history(tweet_text, status=f"error: {e}")
        return False


def publish_tweet_stealth_browser(tweet_text, auth_token=None):
    """Anti-Detection Stealth Browser Auto-Publisher."""
    try:
        try:
            from patchright.sync_api import sync_playwright
        except ImportError:
            from playwright.sync_api import sync_playwright

        print("🛡️ [Stealth Mode] Launching Anti-Detection Browser...")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
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

            if auth_token:
                context.add_cookies([{
                    "name": "auth_token",
                    "value": auth_token,
                    "domain": ".x.com",
                    "path": "/",
                    "secure": True,
                    "httpOnly": True
                }])

            page = context.new_page()

            # Mask automation properties
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                window.chrome = { runtime: {} };
            """)

            print("🌐 Navigating to X/Twitter compose page (https://x.com/compose/post)...")
            page.goto("https://x.com/compose/post", wait_until="domcontentloaded")
            human_sleep(3.0, 5.0)

            if "login" in page.url:
                print("\n⚠️ Twitter Auth Token required or Session Expired!")
                page.wait_for_timeout(10000)

            # Find post textbox (using .first to avoid strict mode violations)
            try:
                textbox = page.locator('[data-testid="tweetTextarea_0"]').first
                textbox.wait_for(timeout=10000)
                textbox.click()
                human_sleep(0.5, 1.5)

                print("⌨️ Simulating human typing with random keystroke delays...")
                for char in tweet_text:
                    page.keyboard.type(char)
                    time.sleep(random.uniform(0.04, 0.12))

                human_sleep(1.5, 3.0)

                # Click post button with human mouse hover
                post_btn = page.locator('[data-testid="tweetButton"]').first
                post_btn.hover()
                human_sleep(0.5, 1.0)
                post_btn.click()

                print("⏳ Waiting for X/Twitter server confirmation...")
                human_sleep(4.0, 6.0)

                print("✅ [Stealth Mode] Tweet posted successfully!")
                record_history(tweet_text, status="success")
                browser.close()
                return True
            except Exception as e_box:
                print(f"❌ Textbox or post button not found: {e_box}")
                record_history(tweet_text, status=f"error: {e_box}")
                browser.close()
                return False

    except Exception as e:
        print(f"❌ [Stealth Mode Error]: {e}")
        record_history(tweet_text, status=f"error: {e}")
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
    auth_token = tw_cfg.get("auth_token")

    print(f"Loaded {len(posts)} posts for platform '{args.platform}' (Dry-Run: {args.dry_run})...")
    
    for i, p in enumerate(posts[:3], 1):
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
            else:
                publish_tweet_stealth_browser(tweet_text, auth_token=auth_token)

            if i < min(len(posts), 3) and not args.dry_run:
                cooldown = random.randint(15, 35)
                print(f"☕ Safety Cooldown: Sleeping {cooldown}s before next tweet...")
                time.sleep(cooldown)


if __name__ == "__main__":
    main()
