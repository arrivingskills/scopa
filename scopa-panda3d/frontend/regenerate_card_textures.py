#!/usr/bin/env python3
"""
Regenerate Scopa card textures to match the style of 7_coins_front.png.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def regenerate_card_textures():
    suits = {
        "coins": {"symbol": "●", "color": (255, 215, 0, 255)},  # Gold
        "cups": {"symbol": "♤", "color": (0, 128, 255, 255)},  # Blue
        "swords": {"symbol": "†", "color": (192, 192, 192, 255)},  # Silver
        "clubs": {"symbol": "♣", "color": (0, 255, 0, 255)}  # Green
    }
    ranks = ["ace", "2", "3", "4", "5", "6", "7", "jack", "knight", "king"]

    textures_dir = "assets/textures"

    # Regenerate textures for each suit and rank
    for suit, details in suits.items():
        for rank in ranks:
            card_name = f"{rank}_{suit}"
            regenerate_texture(card_name, suit, rank, details["symbol"], details["color"], textures_dir)

    print("Card textures regenerated successfully!")

def regenerate_texture(card_name, suit, rank, symbol, color, textures_dir):
    """Regenerate a texture for a card with the correct style."""
    width, height = 512, 512
    img = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Draw border
    border_width = 10
    draw.rectangle([border_width, border_width, width-border_width, height-border_width], outline=(0, 0, 0, 255), width=3)

    # Draw rank and suit in the corners
    try:
        font = ImageFont.truetype("Arial", 36)
    except:
        font = ImageFont.load_default()

    draw.text((30, 30), rank.capitalize(), fill=(0, 0, 0, 255), font=font)
    draw.text((width-100, height-50), suit.capitalize(), fill=(0, 0, 0, 255), font=font)

    # Draw symbols in the center
    symbol_positions = calculate_symbol_positions(rank, width, height)
    for x, y in symbol_positions:
        draw.text((x, y), symbol, fill=color, font=font)

    # Save the texture
    texture_file_path = os.path.join(textures_dir, f"{card_name}.png")
    img.save(texture_file_path)

def calculate_symbol_positions(rank, width, height):
    """Calculate positions for symbols based on the rank."""
    positions = []
    center_x, center_y = width // 2, height // 2

    if rank == "ace":
        positions = [(center_x - 18, center_y - 18)]
    elif rank in ["2", "3", "4", "5", "6", "7"]:
        count = int(rank) if rank.isdigit() else 0
        spacing = 60
        start_y = center_y - (count // 2) * spacing
        for i in range(count):
            positions.append((center_x - 18, start_y + i * spacing))
    elif rank in ["jack", "knight", "king"]:
        positions = [(center_x - 18, center_y - 18)]

    return positions

if __name__ == "__main__":
    regenerate_card_textures()