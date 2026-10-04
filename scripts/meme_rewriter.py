# encoding: utf-8
"""Meme Rewriter: Transforms scraped content & target accounts (@Morris_LT) into viral U.S. Zoomer/Gen-Z slang posts."""

import argparse
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


GENZ_MEME_SYSTEM_PROMPT = """
You are a viral U.S. Gen-Z social media creator, tech influencer, and meme lord.
Your task is to take raw posts (from target accounts like @Morris_LT or Reddit) and rewrite them into authentic American internet tech humor.

Rules:
1. Use U.S. Gen-Z & Zoomer slang naturally: "no cap", "let him cook", "crash out", "glaze", "fr fr", "main character energy", "brainrot", "skibidi", "lock in", "aura", "L/W", "cooking".
2. Adapt local Chinese/tech metaphors to American pop culture & Silicon Valley indie hacker culture (AI Agents, One-person Unicorn, WallStreetBets, Y-Combinator, Tech Bros, Solana/Crypto, Chipotle).
3. Apply viral Twitter/X structures: "POV:", "Bro really thought...", "Nobody:", "My honest reaction: 🗿".
4. Output concise, complete, punchy tweets with maximum viral potential. Never truncate sentences with ellipses.
"""


def rewrite_post(item, style="genz_zoomer"):
    text = (item.get("title") or item.get("raw_text") or "").strip()
    source = item.get("source", "Reddit/X")

    # Complete, non-truncated viral templates for tech/AI indie hacker posts (@Morris_LT)
    if "独角兽" in text or "一人公司" in text or "1人" in text:
        adapted = "The 2026 tech stack:\n1 guy + 5 AI Agents + 0 sleep = A $10M One-Person Unicorn 💀🚀\n\nNo cap, traditional 50-person tech startups are cooked fr fr 🗿"
    elif "MVP" in text or "架构" in text or "完美" in text:
        adapted = "Stop spending 3 weeks building the 'perfect microservice architecture' for a project with 0 users 💀\n\nShip the MVP in 24h, let users roast it, then lock in 🗿"
    elif "Prompt" in text or "Agent" in text or "效率" in text:
        adapted = "Bro mastered AI Agent workflows and is now doing the work of a whole 10-person dev team while eating Chipotle 💀🔥\n\n(unspoken +10000 aura)"
    elif "教程" in text or "踩坑" in text or "动手" in text:
        adapted = "Nobody:\nJunior devs: Reading 45 hours of tutorials 🗿\nIndie hackers: Shipping raw buggy code directly to production at 3 AM 💀\n\nLet him cook fr fr 👀"
    elif "全栈" in text or "替代" in text:
        adapted = "AI isn't replacing devs.\nDevs who use AI Agents are replacing entire 20-person legacy engineering departments 💀\n\nLock in or get cooked 🔒"
    elif "lock in" in text.lower() or "tiktok" in text.lower():
        adapted = "Me: Locks in for 5 mins to study 🗿\nAlso me: Rewards myself with 4 hours of pure brainrot TikToks 💀\n\nNo cap fr fr let him cook 👀"
    elif "暴跌" in text or "抄底" in text or "crypto" in text.lower() or "dogecoin" in text.lower():
        adapted = "Bro bought $10 of Dogecoin at 3 AM thinking he was the next Jordan Belfort 💀\n\nIt's so over... (-5000 aura) 🗿"
    else:
        adapted = f"Nobody:\n{text} 💀\n\nNo cap fr fr let him cook 👀"

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
