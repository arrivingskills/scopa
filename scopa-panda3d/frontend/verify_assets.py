#!/usr/bin/env python3
"""
Test script to verify the 7 of coins textures and model without GUI
"""

import os
from PIL import Image

def check_textures():
    """Check if texture files exist and are valid"""
    texture_files = [
        "assets/textures/7_coins_front.png",
        "assets/textures/card_back.png"
    ]
    
    print("=== Texture Check ===")
    for texture_file in texture_files:
        if os.path.exists(texture_file):
            try:
                img = Image.open(texture_file)
                print(f"✓ {texture_file}: {img.size[0]}x{img.size[1]} {img.mode}")
            except Exception as e:
                print(f"✗ {texture_file}: Error - {e}")
        else:
            print(f"✗ {texture_file}: File not found")

def check_models():
    """Check if model files exist"""
    model_files = [
        "assets/cards/7_coins.egg",
        "assets/cards/7_coins_complete.egg", 
        "assets/cards/7_coins_simple.egg"
    ]
    
    print("\n=== Model Check ===")
    for model_file in model_files:
        if os.path.exists(model_file):
            file_size = os.path.getsize(model_file)
            print(f"✓ {model_file}: {file_size} bytes")
        else:
            print(f"✗ {model_file}: File not found")

def main():
    print("7 of Coins Card Assets Verification")
    print("=" * 40)
    
    check_textures()
    check_models()
    
    print("\n=== Usage Instructions ===")
    print("1. Use '7_coins_simple.egg' for basic testing")
    print("2. Front texture shows 7 gold coins in traditional pattern")
    print("3. Back texture shows decorative SCOPA pattern")
    print("4. Load in Panda3D with: loader.loadModel('assets/cards/7_coins_simple.egg')")

if __name__ == "__main__":
    main()