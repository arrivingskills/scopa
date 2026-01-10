#!/usr/bin/env python3
"""
Script to generate a complete set of Scopa cards (40 cards) with .egg files and textures.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_scopa_deck():
    suits = ["coins", "cups", "swords", "clubs"]
    ranks = ["ace", "2", "3", "4", "5", "6", "7", "jack", "knight", "king"]

    # Create directories if they don't exist
    cards_dir = "assets/cards"
    textures_dir = "assets/textures"
    os.makedirs(cards_dir, exist_ok=True)
    os.makedirs(textures_dir, exist_ok=True)

    # Generate cards for each suit and rank
    for suit in suits:
        for rank in ranks:
            card_name = f"{rank}_{suit}"
            generate_egg_file(card_name, cards_dir)
            generate_texture(card_name, suit, rank, textures_dir)

    # Generate the common card back texture
    generate_card_back_texture(textures_dir)

    print("Scopa deck generated successfully!")

def generate_egg_file(card_name, cards_dir):
    """Generate a .egg file for a card."""
    egg_content = f"""
<Texture> card_front_texture {{
  "assets/textures/{card_name}.png"
}}

<Texture> card_back_texture {{
  "assets/textures/card_back.png"
}}

<Group> {card_name} {{
  <VertexPool> front_vertices {{
    <Vertex> 0 {{
      -0.5 0.01 -0.7
      <UV> {{ 0.0 1.0 }}
      <Normal> {{ 0.0 1.0 0.0 }}
    }}
    <Vertex> 1 {{
      0.5 0.01 -0.7
      <UV> {{ 1.0 1.0 }}
      <Normal> {{ 0.0 1.0 0.0 }}
    }}
    <Vertex> 2 {{
      0.5 0.01 0.7
      <UV> {{ 1.0 0.0 }}
      <Normal> {{ 0.0 1.0 0.0 }}
    }}
    <Vertex> 3 {{
      -0.5 0.01 0.7
      <UV> {{ 0.0 0.0 }}
      <Normal> {{ 0.0 1.0 0.0 }}
    }}
  }}

  <VertexPool> back_vertices {{
    <Vertex> 0 {{
      -0.5 -0.01 -0.7
      <UV> {{ 1.0 1.0 }}
      <Normal> {{ 0.0 -1.0 0.0 }}
    }}
    <Vertex> 1 {{
      0.5 -0.01 -0.7
      <UV> {{ 0.0 1.0 }}
      <Normal> {{ 0.0 -1.0 0.0 }}
    }}
    <Vertex> 2 {{
      0.5 -0.01 0.7
      <UV> {{ 0.0 0.0 }}
      <Normal> {{ 0.0 -1.0 0.0 }}
    }}
    <Vertex> 3 {{
      -0.5 -0.01 0.7
      <UV> {{ 1.0 0.0 }}
      <Normal> {{ 0.0 -1.0 0.0 }}
    }}
  }}

  <Group> front_face {{
    <Polygon> {{
      <TRef> {{ card_front_texture }}
      <VertexRef> {{ 0 1 2 3 <Ref> {{ front_vertices }} }}
    }}
  }}

  <Group> back_face {{
    <Polygon> {{
      <TRef> {{ card_back_texture }}
      <VertexRef> {{ 0 1 2 3 <Ref> {{ back_vertices }} }}
    }}
  }}
}}
"""
    
    egg_file_path = os.path.join(cards_dir, f"{card_name}.egg")
    with open(egg_file_path, "w") as egg_file:
        egg_file.write(egg_content)

def generate_texture(card_name, suit, rank, textures_dir):
    """Generate a texture for a card."""
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

    # Save the texture
    texture_file_path = os.path.join(textures_dir, f"{card_name}.png")
    img.save(texture_file_path)

def generate_card_back_texture(textures_dir):
    """Generate the common card back texture."""
    width, height = 512, 512
    img = Image.new('RGBA', (width, height), (25, 25, 112, 255))  # Dark blue
    draw = ImageDraw.Draw(img)

    # Draw decorative border
    border_width = 20
    for i in range(5):
        draw.rectangle([border_width + i*3, border_width + i*3, width - border_width - i*3, height - border_width - i*3], outline=(255, 215, 0, 255), width=2)

    # Add "SCOPA" text in the center
    try:
        font = ImageFont.truetype("Arial", 24)
    except:
        font = ImageFont.load_default()

    text = "SCOPA"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

    texture_file_path = os.path.join(textures_dir, "card_back.png")
    img.save(texture_file_path)

if __name__ == "__main__":
    try:
        create_scopa_deck()
    except ImportError:
        print("Pillow is not installed. Install it with: pip install Pillow")