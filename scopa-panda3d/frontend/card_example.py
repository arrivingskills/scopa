#!/usr/bin/env python3
"""
Example usage of the 7 of coins card model in Panda3D
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class CardExample(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Load the 7 of coins card model
        self.card_model = self.loader.loadModel("assets/cards/7_coins_complete.egg")
        
        if self.card_model:
            # Parent it to render so it appears in the scene
            self.card_model.reparentTo(self.render)
            
            # Position the card
            self.card_model.setPos(0, 5, 0)  # Move it 5 units away from camera
            
            # Optional: Set up some basic lighting
            self.setup_lighting()
            
            # Optional: Add some rotation animation
            self.card_model.hprInterval(3, (360, 0, 0)).loop()
            
            print("7 of Coins card loaded successfully!")
        else:
            print("Failed to load card model")
    
    def setup_lighting(self):
        # Add ambient light
        ambient_light = AmbientLight('ambient')
        ambient_light.setColor((0.3, 0.3, 0.3, 1))
        ambient_light_np = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_light_np)
        
        # Add directional light
        directional_light = DirectionalLight('directional')
        directional_light.setDirection((-1, -1, -1))
        directional_light.setColor((0.8, 0.8, 0.8, 1))
        directional_light_np = self.render.attachNewNode(directional_light)
        self.render.setLight(directional_light_np)

if __name__ == "__main__":
    app = CardExample()
    app.run()