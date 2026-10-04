# encoding: utf-8
"""Viral Card Generator: Creates high-engagement dark-mode visual quote/meme images using PIL."""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def generate_viral_card(title_text, subtitle_text, output_path):
    """Generate a sleek 1200x675 dark-mode visual card for X/Twitter posts."""
    width, height = 1200, 675
    
    # Create dark gradient background image
    img = Image.new("RGB", (width, height), color="#0f172a")
    draw = ImageDraw.Draw(img)

    # Accent top border bar
    draw.rectangle([0, 0, width, 12], fill="#3b82f6")
    draw.rectangle([0, 12, width//2, 16], fill="#8b5cf6")

    # Inner glass card container
    margin = 50
    draw.rounded_rectangle(
        [margin, margin, width - margin, height - margin],
        radius=24,
        fill="#1e293b",
        outline="#334155",
        width=2
    )

    # Badge icon / tag
    draw.rounded_rectangle([margin + 40, margin + 40, margin + 220, margin + 85], radius=12, fill="#3b82f6")
    
    # Try loading default system fonts or PIL default
    try:
        font_tag = ImageFont.truetype("arial.ttf", 22)
        font_title = ImageFont.truetype("arial.ttf", 38)
        font_sub = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        font_tag = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Draw tag text
    draw.text((margin + 55, margin + 50), "🔥 VIRAL TREND", fill="#ffffff", font=font_tag)

    # Wrap title text
    words = title_text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 42:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    # Draw main text lines
    y_start = margin + 120
    for line in lines[:5]:
        draw.text((margin + 40, y_start), line, fill="#f8fafc", font=font_title)
        y_start += 52

    # Draw footer/subtext
    y_footer = height - margin - 60
    draw.line([margin + 40, y_footer - 20, width - margin - 40, y_footer - 20], fill="#334155", width=1)
    draw.text((margin + 40, y_footer), f"💡 {subtitle_text[:70]}", fill="#94a3b8", font=font_sub)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_file, "JPEG", quality=95)
    print(f"🎨 Generated visual card: {out_file}")
    return str(out_file)


if __name__ == "__main__":
    generate_viral_card(
        "POV: 1 Guy + 5 AI Agents Built a $10M Unicorn in 30 Days",
        "Traditional 50-person startups are officially cooked fr fr 💀",
        "temp/sample_card.jpg"
    )
