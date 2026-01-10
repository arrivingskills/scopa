#!/usr/bin/env python3
"""
Scopa dealing implementation in Panda3D.
"""

import random
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class ScopaGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Adjust the camera position to better view the cards and table
        self.camera.setPos(0, 15, 5)  # Move the camera back and slightly up
        self.camera.lookAt(0, 0, 0)  # Ensure the camera is focused on the table

        # Initialize the deck
        self.deck = self.initialize_deck()
        random.shuffle(self.deck)

        # Deal cards
        self.player1_hand = []
        self.player2_hand = []
        self.table_cards = []

        self.deal_cards()

        # Display cards
        self.display_cards()

    def initialize_deck(self):
        """Load all 40 cards into the deck."""
        suits = ["coins", "cups", "swords", "clubs"]
        ranks = ["ace", "2", "3", "4", "5", "6", "7", "jack", "knight", "king"]
        deck = []

        for suit in suits:
            for rank in ranks:
                card_name = f"{rank}_{suit}"
                card_model = self.loader.loadModel(f"assets/cards/{card_name}.egg")
                deck.append(card_model)

        return deck

    def deal_cards(self):
        """Deal 3 cards to each player and 4 cards to the table."""
        for _ in range(3):
            self.player1_hand.append(self.deck.pop())
            self.player2_hand.append(self.deck.pop())

        for _ in range(4):
            self.table_cards.append(self.deck.pop())

    def display_cards(self):
        """Display the dealt cards in the scene."""
        # Display player 1's hand
        for i, card in enumerate(self.player1_hand):
            card.reparentTo(self.render)
            card.setPos(-2 + i * 1.5, 5, -2)  # Spread cards horizontally

        # Display player 2's hand
        for i, card in enumerate(self.player2_hand):
            card.reparentTo(self.render)
            card.setPos(-2 + i * 1.5, 5, 2)  # Spread cards horizontally

        # Display table cards
        for i, card in enumerate(self.table_cards):
            card.reparentTo(self.render)
            card.setPos(-3 + i * 2, 5, 0)  # Spread cards horizontally

if __name__ == "__main__":
    game = ScopaGame()
    game.run()