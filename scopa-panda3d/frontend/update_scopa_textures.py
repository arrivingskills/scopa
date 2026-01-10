#!/usr/bin/env python3
"""
Script to regenerate Scopa card textures with correct symbols and counts.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def regenerate_scopa_textures():
    suits = {
        "coins": "●",
        "cups": "♤",
        "swords": "†",
        "clubs": "♣"
    }
    ranks = ["ace", "2", "3", "4", "5", "6", "7", "jack", "knight", "king"]

    textures_dir = "assets/textures"

    # Regenerate textures for each suit and rank
    for suit, symbol in suits.items():
        for rank in ranks:
            card_name = f"{rank}_{suit}"
            regenerate_texture(card_name, suit, rank, symbol, textures_dir)

    print("Scopa card textures updated successfully!")

def regenerate_texture(card_name, suit, rank, symbol, textures_dir):
    """Regenerate a texture for a card with correct symbols and counts."""
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
        draw.text((x, y), symbol, fill=(0, 0, 0, 255), font=font)

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
        count = int(rank)
        for i in range(count):
            angle = (360 / count) * i
            x = center_x + int(100 * (i % 2))
            y = center_y + int(100 * (i % 2))
            positions.append((x, y))
    elif rank in ["jack", "knight", "king"]:
        positions = [(center_x, center_y)]

    return positions

if __name__ == "__main__":
    regenerate_scopa_textures()