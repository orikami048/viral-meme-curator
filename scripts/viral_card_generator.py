# encoding: utf-8
"""Viral Card Generator: Creates high-engagement multi-theme visual quote/meme images using PIL with CJK & Unicode font fallbacks."""

import os
import random
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 5 Distinct High-Impression Visual Themes
THEMES = {
    "cyber_dark": {
        "name": "Cyber Dark",
        "bg_color": "#0f172a",
        "card_bg": "#1e293b",
        "border_color": "#334155",
        "bar_color1": "#3b82f6",
        "bar_color2": "#8b5cf6",
        "tag_bg": "#3b82f6",
        "tag_text": "#ffffff",
        "title_color": "#f8fafc",
        "sub_color": "#94a3b8",
    },
    "clean_white": {
        "name": "Clean White",
        "bg_color": "#f1f5f9",
        "card_bg": "#ffffff",
        "border_color": "#cbd5e1",
        "bar_color1": "#ff5722",
        "bar_color2": "#f43f5e",
        "tag_bg": "#ff5722",
        "tag_text": "#ffffff",
        "title_color": "#0f172a",
        "sub_color": "#64748b",
    },
    "sunset_gradient": {
        "name": "Sunset Violet",
        "bg_color": "#1e1b4b",
        "card_bg": "#312e81",
        "border_color": "#4338ca",
        "bar_color1": "#ec4899",
        "bar_color2": "#f59e0b",
        "tag_bg": "#ec4899",
        "tag_text": "#ffffff",
        "title_color": "#ffffff",
        "sub_color": "#c7d2fe",
    },
    "retro_hacker": {
        "name": "Retro Terminal",
        "bg_color": "#050505",
        "card_bg": "#0d1117",
        "border_color": "#1f2937",
        "bar_color1": "#22c55e",
        "bar_color2": "#10b981",
        "tag_bg": "#22c55e",
        "tag_text": "#000000",
        "title_color": "#4ade80",
        "sub_color": "#9ca3af",
    },
    "amber_magazine": {
        "name": "Amber Editorial",
        "bg_color": "#0b132b",
        "card_bg": "#1c2541",
        "border_color": "#3a506b",
        "bar_color1": "#f59e0b",
        "bar_color2": "#d97706",
        "tag_bg": "#f59e0b",
        "tag_text": "#000000",
        "title_color": "#fef3c7",
        "sub_color": "#cbd5e1",
    },
}

TAG_OPTIONS = [
    "VIRAL TREND",
    "BREAKING HOOK",
    "TECH MATRIX",
    "UNPOPULAR OPINION",
    "2026 HOT TAKE",
    "REALITY CHECK"
]


def load_font(size):
    """Load font with CJK support (msyh.ttc) to guarantee zero tofu boxes."""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",       # Microsoft YaHei
        "C:/Windows/Fonts/segoeui.ttf",    # Segoe UI
        "C:/Windows/Fonts/arial.ttf",      # Arial
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def generate_viral_card(title_text, subtitle_text, output_path, theme_name=None):
    """Generate a 1200x675 visual card with dynamic multi-theme styling & zero tofu boxes."""
    width, height = 1200, 675

    if not theme_name or theme_name not in THEMES:
        theme_name = random.choice(list(THEMES.keys()))
    
    t = THEMES[theme_name]
    
    img = Image.new("RGB", (width, height), color=t["bg_color"])
    draw = ImageDraw.Draw(img)

    # Accent top border bar
    draw.rectangle([0, 0, width, 14], fill=t["bar_color1"])
    draw.rectangle([0, 14, width // 2, 18], fill=t["bar_color2"])

    # Inner card container
    margin = 48
    draw.rounded_rectangle(
        [margin, margin, width - margin, height - margin],
        radius=26,
        fill=t["card_bg"],
        outline=t["border_color"],
        width=2
    )

    # Load fonts
    font_tag = load_font(20)
    font_title = load_font(36)
    font_sub = load_font(24)

    # Dynamic badge tag width
    tag_str = random.choice(TAG_OPTIONS)
    tag_width = int(len(tag_str) * 13.5 + 36)
    draw.rounded_rectangle([margin + 40, margin + 40, margin + 40 + tag_width, margin + 88], radius=14, fill=t["tag_bg"])

    # Draw tag text
    draw.text((margin + 58, margin + 52), tag_str, fill=t["tag_text"], font=font_tag)

    # Wrap title text (clean English word wrap)
    words = str(title_text).split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 40:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    # Draw main title lines
    y_start = margin + 124
    for line in lines[:5]:
        draw.text((margin + 40, y_start), line, fill=t["title_color"], font=font_title)
        y_start += 52

    # Draw footer line & subtext
    y_footer = height - margin - 60
    draw.line([margin + 40, y_footer - 20, width - margin - 40, y_footer - 20], fill=t["border_color"], width=1)
    
    clean_sub = str(subtitle_text).replace("💡", "").replace("🔥", "").replace("💀", "").replace("🗿", "").strip()
    draw.text((margin + 40, y_footer), f"KEY TAKEAWAY: {clean_sub[:75]}", fill=t["sub_color"], font=font_sub)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_file, "JPEG", quality=95)
    print(f"🎨 Generated visual card ({t['name']} style): {out_file}")
    return str(out_file)


if __name__ == "__main__":
    generate_viral_card(
        "1 Solo Founder + 5 AI Agents = $500k/mo Revenue",
        "Traditional 50-person tech startups are officially cooked",
        "temp/card_2.jpg",
        theme_name="clean_white"
    )
