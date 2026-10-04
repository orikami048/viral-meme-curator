# encoding: utf-8
"""Full-Auto Daemon: Autonomous viral Reddit content curation, self-learning traffic optimization & auto-publishing pipeline."""

import argparse
import datetime
import json
import random
import subprocess
import sys
import time
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent


def log_daemon(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] 🤖 [Full-Auto Daemon] {msg}")


def run_pipeline_cycle():
    log_daemon("Starting autonomous Reddit viral curation cycle...")

    # Step 1: 100% Exclusive Reddit Content Discovery
    log_daemon("Step 1/4: Scraping top live Reddit memes & hot topics (r/memes, r/dankmemes)...")
    subprocess.run([sys.executable, "scripts/fetch_reddit_trending.py", "--subreddit", "memes", "--limit", "5"], cwd=BASE_DIR)

    # Step 2: Self-Learning Traffic Analytics
    log_daemon("Step 2/4: Running Self-Learning Traffic Analyzer...")
    try:
        subprocess.run([sys.executable, "scripts/traffic_analyzer.py"], cwd=BASE_DIR)
    except Exception as e:
        log_daemon(f"Traffic analyzer notice: {e}")

    # Step 3: Meme Rewriting & Viral Hook Generation (Using Reddit JSON exclusively)
    log_daemon("Step 3/4: Rewriting Reddit posts into U.S. Gen-Z Viral Hooks...")
    subprocess.run([sys.executable, "scripts/meme_rewriter.py", "--input-file", "temp/reddit_trending.json"], cwd=BASE_DIR)

    # Step 4: Stealth Auto-Publishing to X/Twitter
    log_daemon("Step 4/4: Publishing to X/Twitter via Stealth Anti-Detection Browser...")
    subprocess.run([sys.executable, "scripts/auto_publisher.py"], cwd=BASE_DIR)

    log_daemon("✅ Autonomous cycle completed successfully!")


def start_daemon_loop(interval_hours=2.5, run_once=False):
    log_daemon("==================================================")
    log_daemon("🚀 FULL-AUTO REDDIT TRAFFIC EVOLUTION DAEMON STARTED")
    log_daemon(f"⏰ Target Interval: {interval_hours} hours between posting cycles")
    log_daemon("==================================================")

    cycle_count = 0
    while True:
        cycle_count += 1
        log_daemon(f"--- Starting Autonomous Cycle #{cycle_count} ---")
        
        try:
            run_pipeline_cycle()
        except Exception as e:
            log_daemon(f"❌ Cycle error: {e}")

        if run_once:
            log_daemon("Run-once flag detected. Exiting daemon.")
            break

        # Calculate randomized sleep time (interval +- 20%)
        base_seconds = int(interval_hours * 3600)
        jitter_seconds = random.randint(-600, 600)
        sleep_duration = max(1800, base_seconds + jitter_seconds)
        
        next_run_time = datetime.datetime.now() + datetime.timedelta(seconds=sleep_duration)
        log_daemon(f"☕ Cooldown: Daemon sleeping for {sleep_duration//60} mins.")
        log_daemon(f"⏰ Next automated cycle will trigger at: {next_run_time.strftime('%H:%M:%S')}")
        
        time.sleep(sleep_duration)


def main():
    parser = argparse.ArgumentParser(description="Full-Auto Traffic Evolution Daemon (Reddit Exclusive)")
    parser.add_argument("--interval", type=float, default=2.5, help="Interval in hours between cycles")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit")
    args = parser.parse_args()

    start_daemon_loop(interval_hours=args.interval, run_once=args.once)


if __name__ == "__main__":
    main()
