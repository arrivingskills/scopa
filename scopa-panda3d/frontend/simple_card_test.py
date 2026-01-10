#!/usr/bin/env python3
"""
Simple test of the 7 of coins card model
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class SimpleCardTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Try to load the simple card model
        self.card_model = self.loader.loadModel("assets/cards/7_coins_simple.egg")
        
        if self.card_model:
            self.card_model.reparentTo(self.render)
            self.card_model.setPos(0, 5, 0)
            
            # Enable automatic normal generation for lighting
            render.setRenderModeWireframe()
            render.setShaderAuto()
            
            print("Card loaded successfully!")
            print("Card vertices:", self.card_model.getNumChildren())
        else:
            print("Failed to load card model")
            
        # Set camera position
        self.camera.setPos(0, -10, 0)
        self.camera.lookAt(0, 0, 0)

if __name__ == "__main__":
    app = SimpleCardTest()
    app.run()