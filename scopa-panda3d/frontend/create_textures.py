#!/usr/bin/env python3
"""
Script to generate placeholder textures for the Scopa cards
Run this to create basic PNG textures for testing
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_card_textures():
    # Create assets/textures directory if it doesn't exist
    texture_dir = "assets/textures"
    os.makedirs(texture_dir, exist_ok=True)
    
    # Create 7 of Coins front texture
    create_7_coins_front(texture_dir)
    
    # Create generic card back texture
    create_card_back(texture_dir)
    
    print("Texture files created successfully!")

def create_7_coins_front(texture_dir):
    """Create the 7 of coins front texture"""
    width, height = 512, 512
    
    # Create white background
    img = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw border
    border_width = 10
    draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                  outline=(0, 0, 0, 255), width=3)
    
    # Draw "7" in top left and bottom right corners (rotated)
    try:
        font = ImageFont.truetype("Arial", 36)
    except:
        font = ImageFont.load_default()
    
    # Top left "7"
    draw.text((30, 30), "7", fill=(0, 0, 0, 255), font=font)
    
    # Bottom right "7" (rotated)
    temp_img = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((10, 10), "7", fill=(0, 0, 0, 255), font=font)
    rotated = temp_img.rotate(180)
    img.paste(rotated, (width-80, height-80), rotated)
    
    # Draw 7 coin symbols arranged in traditional pattern
    coin_positions = [
        (width//2, 80),           # Top center
        (width//3, 180),          # Left
        (2*width//3, 180),        # Right  
        (width//2, 256),          # Center
        (width//3, 332),          # Left
        (2*width//3, 332),        # Right
        (width//2, 432)           # Bottom center
    ]
    
    for x, y in coin_positions:
        draw_coin(draw, x, y, 25)
    
    # Draw suit symbol in corners
    draw.text((30, 70), "♦", fill=(255, 215, 0, 255), font=font)  # Gold color for coins
    temp_suit = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
    temp_suit_draw = ImageDraw.Draw(temp_suit)
    temp_suit_draw.text((10, 10), "♦", fill=(255, 215, 0, 255), font=font)
    rotated_suit = temp_suit.rotate(180)
    img.paste(rotated_suit, (width-80, height-120), rotated_suit)
    
    img.save(os.path.join(texture_dir, "7_coins_front.png"))
    print(f"Created 7_coins_front.png")

def draw_coin(draw, x, y, radius):
    """Draw a coin symbol"""
    # Outer circle (gold)
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                fill=(255, 215, 0, 255), outline=(184, 134, 11, 255), width=2)
    
    # Inner circle (darker gold)
    inner_radius = radius - 5
    draw.ellipse([x-inner_radius, y-inner_radius, x+inner_radius, y+inner_radius], 
                fill=(218, 165, 32, 255))

def create_card_back(texture_dir):
    """Create a generic card back texture"""
    width, height = 512, 512
    
    # Create blue background
    img = Image.new('RGBA', (width, height), (25, 25, 112, 255))  # Dark blue
    draw = ImageDraw.Draw(img)
    
    # Draw decorative border
    border_width = 20
    for i in range(5):
        draw.rectangle([border_width + i*3, border_width + i*3, 
                       width - border_width - i*3, height - border_width - i*3], 
                      outline=(255, 215, 0, 255), width=2)
    
    # Draw decorative pattern in center
    center_x, center_y = width//2, height//2
    
    # Draw diamond pattern
    diamond_size = 80
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = center_x + i * diamond_size
            y = center_y + j * diamond_size
            if (i + j) % 2 == 0:
                points = [(x, y-30), (x+30, y), (x, y+30), (x-30, y)]
                draw.polygon(points, fill=(255, 215, 0, 100))
    
    # Add "SCOPA" text in center
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
    
    img.save(os.path.join(texture_dir, "card_back.png"))
    print(f"Created card_back.png")

if __name__ == "__main__":
    try:
        import PIL
        create_card_textures()
    except ImportError:
        print("PIL (Pillow) not installed. Install it with: pip install Pillow")
        print("Or manually create the texture files as described in the README.")