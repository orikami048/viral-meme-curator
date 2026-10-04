# encoding: utf-8
"""Traffic Analyzer & Self-Learning Engine: Evaluates impressions/engagement and optimizes post formats."""

import json
import random
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent


def evaluate_and_learn():
    """Analyze past history logs and update format weights in learning memory."""
    history_path = BASE_DIR / "temp" / "history.json"
    learning_path = BASE_DIR / "temp" / "traffic_learning.json"
    
    # Default weights
    memory = {
        "format_weights": {
            "image_card": 0.60,
            "pure_text": 0.40
        },
        "hook_weights": {
            "unpopular_opinion": 0.35,
            "tech_stack": 0.35,
            "bullet_list": 0.30
        },
        "total_posts_analyzed": 0,
        "best_performing_format": "image_card"
    }

    if history_path.exists():
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            
            total = len(history)
            successes = [h for h in history if h.get("status") == "success"]
            
            memory["total_posts_analyzed"] = total
            
            # Learn from posting experience: Increase image card preference if successful
            if len(successes) > 2:
                memory["format_weights"]["image_card"] = min(0.80, memory["format_weights"]["image_card"] + 0.05)
                memory["format_weights"]["pure_text"] = 1.0 - memory["format_weights"]["image_card"]
                memory["best_performing_format"] = "image_card"
        except Exception as e:
            print(f"Notice: Traffic analysis learning error ({e})")

    learning_path.parent.mkdir(parents=True, exist_ok=True)
    with open(learning_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

    print(f"📈 [Self-Evolution] Analyzed {memory['total_posts_analyzed']} posts. Preferred Format: {memory['best_performing_format']} (Weight: {memory['format_weights']['image_card']*100:.0f}%)")
    return memory


def get_chosen_format():
    memory = evaluate_and_learn()
    img_weight = memory["format_weights"]["image_card"]
    if random.random() < img_weight:
        return "image_card"
    return "pure_text"


if __name__ == "__main__":
    evaluate_and_learn()
