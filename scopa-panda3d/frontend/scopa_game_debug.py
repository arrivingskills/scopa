#!/usr/bin/env python3
"""
Debug version of the Scopa frontend with verbose output.
Run this if cards are not displaying properly.
"""

import socket
import threading
import json
import sys
import os
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

print("=" * 60)
print("SCOPA GAME DEBUG MODE")
print("=" * 60)
print(f"Working directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print("")


class ScopaGameDebug(ShowBase):
    def __init__(self):
        print("Initializing Panda3D...")
        ShowBase.__init__(self)

        # Set window title
        self.windowProperties = WindowProperties()
        self.windowProperties.setTitle("Scopa Card Game [DEBUG MODE]")
        self.win.requestProperties(self.windowProperties)

        # Camera setup
        print("Setting up camera...")
        self.camera.setPos(0, -20, 8)
        self.camera.lookAt(0, 0, 0)

        # Game state
        self.game_state = None
        self.sock = None
        self.lock = threading.Lock()
        self.state_changed = False

        # Card tracking for rendering
        self.table_cards = []
        self.player1_cards = []
        self.player2_cards = []

        # UI setup
        self.setup_ui()

        # Test card loading
        self.test_card_loading()

        # Connect to backend
        threading.Thread(target=self.connect_backend, daemon=True).start()

    def setup_ui(self):
        """Setup the UI elements."""
        print("Setting up UI...")
        self.title = OnscreenText(
            text="Scopa Game [DEBUG]", pos=(0, 0.95), scale=0.08, fg=(1, 0, 0, 1)
        )

        self.status_text = OnscreenText(
            text="Status: Initializing...", pos=(0, 0.85), scale=0.05, fg=(1, 1, 1, 1)
        )

        # Game info text
        self.info_text = OnscreenText(
            text="", pos=(-1.3, 0.7), scale=0.04, align=TextNode.ALeft, fg=(1, 1, 1, 1)
        )

        self.btn_start = DirectButton(
            text="Start Game", scale=0.08, pos=(-0.5, 0, -0.9), command=self.start_game
        )

        self.taskMgr.add(self.update_task, "update_task")

        # Setup keyboard controls
        self.accept("1", self.play_card, [0])
        self.accept("2", self.play_card, [1])
        self.accept("3", self.play_card, [2])

        print("UI setup complete")

    def test_card_loading(self):
        """Test loading a sample card."""
        print("\n" + "=" * 60)
        print("TESTING CARD LOADING")
        print("=" * 60)

        test_path = "assets/cards/ace_coins.egg"
        print(f"Attempting to load: {test_path}")
        print(f"Full path: {os.path.abspath(test_path)}")
        print(f"File exists: {os.path.exists(test_path)}")

        if os.path.exists(test_path):
            try:
                card = self.loader.loadModel(test_path)
                if card and not card.isEmpty():
                    print("✓ Successfully loaded test card!")
                    card.reparentTo(self.render)
                    card.setPos(0, 0, 0)
                    card.setScale(0.3)
                    print(f"  Card node: {card}")
                    print(f"  Children: {card.getChildren()}")
                else:
                    print("✗ Card loaded but is empty")
            except Exception as e:
                print(f"✗ Failed to load card: {e}")
                import traceback

                traceback.print_exc()
        else:
            print("✗ Card file not found!")
            print(f"  Looking in: {os.path.abspath('.')}")
            print(f"  Assets folder exists: {os.path.exists('assets')}")
            print(f"  Cards folder exists: {os.path.exists('assets/cards')}")
            if os.path.exists("assets/cards"):
                print(f"  Files in assets/cards: {os.listdir('assets/cards')[:5]}...")

        print("=" * 60 + "\n")

    def update_task(self, task):
        """Update UI from background threads."""
        with self.lock:
            if self.game_state and self.state_changed:
                print("\n>>> Rendering game state...")
                self.render_game_state()
                self.update_info_text()
                self.state_changed = False
        return task.cont

    def connect_backend(self):
        """Connect to the GameServer backend."""
        print("\n" + "=" * 60)
        print("CONNECTING TO SERVER")
        print("=" * 60)
        try:
            print("Connecting to 127.0.0.1:5000...")
            self.sock = socket.create_connection(("127.0.0.1", 5000), timeout=10)
            print("✓ Connected to server")
            self.set_status("Connected to server")

            print("Sending HELLO...")
            self.sock.sendall(b"HELLO\n")
            response = self.sock.makefile("r").readline()
            data = json.loads(response)
            print(f"✓ Server response: {data}")
            print("=" * 60 + "\n")

        except Exception as e:
            print(f"✗ Connection failed: {e}")
            self.set_status(f"Connection failed: {e}")
            import traceback

            traceback.print_exc()

    def start_game(self):
        """Start a new game."""
        print("\n>>> START GAME button clicked")
        self.set_status("Starting game...")
        threading.Thread(target=self._start_game_thread, daemon=True).start()

    def _start_game_thread(self):
        print("Sending START command...")
        try:
            self.sock.sendall(b"START\n")
            response = self.sock.makefile("r").readline()
            data = json.loads(response)

            print(f"Server response status: {data.get('status')}")

            if data.get("status") == "ok":
                print(f"✓ Game started successfully!")
                print(f"  Table cards: {len(data.get('table', []))}")
                print(
                    f"  Player 1 hand: {len(data.get('player1', {}).get('hand', []))}"
                )
                print(
                    f"  Player 2 hand: {len(data.get('player2', {}).get('hand', []))}"
                )
                print(f"  Current player: {data.get('currentPlayer')}")

                with self.lock:
                    self.game_state = data
                    self.state_changed = True

                self.set_status("Game started!")
            else:
                print(f"✗ Game start failed: {data}")
                self.set_status("Failed to start game")
        except Exception as e:
            print(f"✗ Error starting game: {e}")
            import traceback

            traceback.print_exc()

    def render_game_state(self):
        """Render the current game state."""
        print("render_game_state() called")
        if not self.game_state:
            print("  No game state!")
            return

        print(
            f"  Rendering game with {len(self.game_state.get('table', []))} table cards"
        )

        # Clear old cards
        print("  Clearing old cards...")
        for card in self.table_cards:
            card.removeNode()
        for card in self.player1_cards:
            card.removeNode()
        for card in self.player2_cards:
            card.removeNode()
        self.table_cards.clear()
        self.player1_cards.clear()
        self.player2_cards.clear()

        # Render table cards
        table_cards = self.game_state.get("table", [])
        for i, card_data in enumerate(table_cards):
            print(f"  Creating table card {i}: {card_data}")
            x = -3 + i * 1.5
            card_node = self.create_card_visual(card_data, (x, 0, 0))
            if card_node:
                self.table_cards.append(card_node)
                print(f"    ✓ Card created at position ({x}, 0, 0)")
            else:
                print("    ✗ Failed to create card")

        # Render player 1 hand (bottom)
        p1_data = self.game_state.get("player1", {})
        p1_hand = p1_data.get("hand", [])
        print(f"  Rendering Player 1 hand: {len(p1_hand)} cards")
        for i, card_data in enumerate(p1_hand):
            x = -2 + i * 1.5
            card_node = self.create_card_visual(card_data, (x, 0, -3))
            if card_node:
                self.player1_cards.append(card_node)
                print(f"    ✓ P1 card {i+1} at ({x}, 0, -3)")

        # Render player 2 hand (top)
        p2_data = self.game_state.get("player2", {})
        p2_hand = p2_data.get("hand", [])
        print(f"  Rendering Player 2 hand: {len(p2_hand)} cards")
        for i, card_data in enumerate(p2_hand):
            x = -2 + i * 1.5
            card_node = self.create_card_visual(card_data, (x, 0, 3))
            if card_node:
                self.player2_cards.append(card_node)
                print(f"    ✓ P2 card {i+1} at ({x}, 0, 3)")

        print(
            f"  Rendering complete! Table: {len(self.table_cards)}, P1: {len(self.player1_cards)}, P2: {len(self.player2_cards)} cards visible"
        )

    def create_card_visual(self, card_data, position):
        """Create a visual representation of a card."""
        suit = card_data.get("suit", "").lower()
        rank_name = card_data.get("rank", "").lower()

        rank_map = {
            "ace": "ace",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "jack": "jack",
            "knight": "knight",
            "king": "king",
        }

        rank_file = rank_map.get(rank_name, "ace")
        card_name = f"{rank_file}_{suit}"
        card_path = f"assets/cards/{card_name}.egg"

        print(f"    Attempting to load: {card_path}")

        try:
            card_node = self.loader.loadModel(card_path)
            if card_node and not card_node.isEmpty():
                card_node.reparentTo(self.render)
                card_node.setPos(*position)
                card_node.setScale(0.3)
                print(f"    ✓ Loaded {card_name}")
                return card_node
        except Exception as e:
            print(f"    ✗ Failed to load {card_path}: {e}")

        # Fallback
        print(f"    Using fallback geometry")
        cm = CardMaker("card")
        cm.setFrame(-0.5, 0.5, -0.7, 0.7)
        card_node = self.render.attachNewNode(cm.generate())
        card_node.setPos(*position)

        colors = {
            "coins": (1, 0.84, 0, 1),
            "cups": (0, 0, 1, 1),
            "swords": (0.5, 0.5, 0.5, 1),
            "clubs": (0, 1, 0, 1),
        }
        card_node.setColor(colors.get(suit, (1, 1, 1, 1)))

        return card_node

    def play_card(self, hand_index):
        """Play a card from hand."""
        print(f"\n>>> Playing card at index {hand_index}")
        if not self.game_state:
            print("  No game state!")
            return

        self.set_status(f"Playing card {hand_index + 1}...")
        threading.Thread(
            target=self._play_card_thread, args=(hand_index,), daemon=True
        ).start()

    def _play_card_thread(self, hand_index):
        try:
            # Get possible captures first
            print(f"  Getting captures for card {hand_index}...")
            self.sock.sendall(f"CAPTURES {hand_index}\n".encode())
            response = self.sock.makefile("r").readline()
            captures_data = json.loads(response)

            if captures_data.get("status") == "ok":
                captures = captures_data.get("captures", [])
                print(f"  Found {len(captures)} possible capture(s)")

                # Select capture (0 if available, -1 if none)
                capture_index = 0 if len(captures) > 0 else -1

                # Play the card
                print(f"  Playing card {hand_index} with capture index {capture_index}")
                self.sock.sendall(f"PLAY {hand_index} {capture_index}\n".encode())
                response = self.sock.makefile("r").readline()
                play_data = json.loads(response)

                if play_data.get("status") == "ok":
                    print("  ✓ Card played successfully!")
                    with self.lock:
                        self.game_state = play_data
                        self.state_changed = True
                    self.set_status("Card played")
                else:
                    print(f"  ✗ Play failed: {play_data}")
                    self.set_status("Failed to play card")
            else:
                print(f"  ✗ Failed to get captures: {captures_data}")
        except Exception as e:
            print(f"  ✗ Error playing card: {e}")
            import traceback

            traceback.print_exc()

    def update_info_text(self):
        """Update the information text display."""
        if not self.game_state:
            self.info_text.setText("")
            return

        p1_data = self.game_state.get("player1", {})
        p2_data = self.game_state.get("player2", {})
        current_player = self.game_state.get("currentPlayer", "")
        deck_size = self.game_state.get("deckSize", 0)
        round_over = self.game_state.get("roundOver", False)

        info = []
        info.append(f"=== {p1_data.get('name', 'Player 1')} ===")
        info.append(f"  Cards in hand: {len(p1_data.get('hand', []))}")
        info.append(f"  Captured: {p1_data.get('captured', 0)}")
        info.append(f"  Scopas: {p1_data.get('scopas', 0)}")
        info.append("")
        info.append(f"=== {p2_data.get('name', 'Player 2')} ===")
        info.append(f"  Cards in hand: {len(p2_data.get('hand', []))}")
        info.append(f"  Captured: {p2_data.get('captured', 0)}")
        info.append(f"  Scopas: {p2_data.get('scopas', 0)}")
        info.append("")
        info.append(f"Table cards: {len(self.game_state.get('table', []))}")
        info.append(f"Deck remaining: {deck_size}")
        info.append(f"Current turn: {current_player}")
        info.append(f"Round over: {'Yes' if round_over else 'No'}")
        info.append("")
        info.append("=== Controls ===")
        info.append("Press 1-3: Play card")

        self.info_text.setText("\n".join(info))

    def set_status(self, text):
        """Update status text."""
        with self.lock:
            self.status_text.setText(f"Status: {text}")
        print(f"STATUS: {text}")


if __name__ == "__main__":
    print("Starting Scopa Game in DEBUG mode...")
    print("Watch the console output for detailed information.")
    print("")
    app = ScopaGameDebug()
    app.run()
