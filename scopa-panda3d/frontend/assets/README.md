# 7 of Coins Card Assets

This directory contains the 3D model assets for the 7 of Coins card in the Panda3D Scopa game.

## Files Created

### Card Models
- `7_coins.egg` - Simple single-sided card model
- `7_coins_complete.egg` - Complete card model with front, back, and edges

### Textures (to be added)
You'll need to create these texture files in `assets/textures/`:
- `7_coins_front.png` - Front face texture showing the 7 of coins design
- `card_back.png` - Generic card back texture

## Card Model Features

The complete card model includes:
- **Front face**: Displays the 7 of coins design
- **Back face**: Shows the card back pattern
- **Edges**: Gives the card realistic thickness
- **Proper UV mapping**: Ready for texture application
- **Standard card proportions**: 2.5:3.5 ratio (like real playing cards)

## Usage in Panda3D

```python
# Load the card model
card = self.loader.loadModel("assets/cards/7_coins_complete.egg")
card.reparentTo(self.render)
card.setPos(x, y, z)
```

## Texture Requirements

Create texture images with these specifications:
- **Format**: PNG with transparency support
- **Size**: 512x512 or 1024x1024 pixels recommended
- **Card front**: Should show 7 coin symbols arranged in traditional pattern
- **Card back**: Generic decorative pattern

## Example

Run `card_example.py` to see the card model loaded with basic lighting and rotation animation.

## Customization

You can modify the egg files to:
- Adjust card dimensions by changing vertex coordinates
- Add rounded corners by modifying the vertex positions
- Change material properties (shininess, color, etc.)
- Add additional detail geometry

## Integration with Main Game

To integrate with your main Scopa game, modify `main.py` to load card models when needed:

```python
# In your Frontend class
self.cards = {}
self.cards['7_coins'] = self.loader.loadModel("assets/cards/7_coins_complete.egg")
```