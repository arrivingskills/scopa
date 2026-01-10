#!/usr/bin/env python3
"""
Complete Scopa game frontend using Panda3D.
Communicates with Java GameServer backend via JSON over TCP.
"""

import socket
import threading
import json
import sys
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import *


class ScopaGameFrontend(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Set window title
        self.windowProperties = WindowProperties()
        self.windowProperties.setTitle("Scopa Card Game")
        self.win.requestProperties(self.windowProperties)

        # Camera setup for better view
        self.camera.setPos(0, -20, 8)
        self.camera.lookAt(0, 0, 0)

        # Game state
        self.game_state = None
        self.sock = None
        self.selected_hand_index = None
        self.selected_capture_index = None
        self.available_captures = []
        self.card_models = {}  # Store loaded card models
        self.rendered_cards = {"table": [], "p1": [], "p2": []}
        self.lock = threading.Lock()

        # UI setup
        self.setup_ui()

        # Connect to backend
        threading.Thread(target=self.connect_backend, daemon=True).start()

    def setup_ui(self):
        """Setup the UI elements."""
        # Title
        self.title = OnscreenText(
            text="Scopa Card Game",
            pos=(0, 0.95),
            scale=0.08,
            fg=(1, 1, 0, 1),
            shadow=(0, 0, 0, 0.5),
        )

        # Status text
        self.status_text = OnscreenText(
            text="Status: Connecting...", pos=(0, 0.85), scale=0.05, fg=(1, 1, 1, 1)
        )

        # Game info text
        self.info_text = OnscreenText(
            text="", pos=(-1.3, 0.7), scale=0.04, align=TextNode.ALeft, fg=(1, 1, 1, 1)
        )

        # Control buttons
        button_scale = 0.06
        self.btn_start = DirectButton(
            text="Start Game",
            scale=button_scale,
            pos=(-0.9, 0, -0.9),
            command=self.start_game,
        )

        self.btn_finalize = DirectButton(
            text="Finalize Round",
            scale=button_scale,
            pos=(-0.5, 0, -0.9),
            command=self.finalize_round,
        )

        self.btn_score = DirectButton(
            text="Show Score",
            scale=button_scale,
            pos=(0, 0, -0.9),
            command=self.show_score,
        )

        self.btn_refresh = DirectButton(
            text="Refresh",
            scale=button_scale,
            pos=(0.5, 0, -0.9),
            command=self.refresh_state,
        )

        self.btn_quit = DirectButton(
            text="Quit", scale=button_scale, pos=(0.9, 0, -0.9), command=sys.exit
        )

        # Update task
        self.taskMgr.add(self.update_task, "update_task")

    def update_task(self, task):
        """Update UI from background threads."""
        with self.lock:
            if self.game_state:
                self.render_game_state()
                self.update_info_text()
        return task.cont

    def connect_backend(self):
        """Connect to the GameServer backend."""
        try:
            self.sock = socket.create_connection(("127.0.0.1", 5000), timeout=10)
            self.set_status("Connected to server")

            # Send HELLO
            self.send_command("HELLO")
            response = self.receive_response()
            print("Server response:", response)

        except Exception as e:
            self.set_status(f"Connection failed: {e}")
            print(f"Connection error: {e}")

    def send_command(self, cmd):
        """Send a command to the backend."""
        if not self.sock:
            self.set_status("Not connected to server")
            return None

        try:
            self.sock.sendall((cmd + "\n").encode("utf-8"))
            return self.receive_response()
        except Exception as e:
            self.set_status(f"Send failed: {e}")
            return None

    def receive_response(self):
        """Receive and parse JSON response from backend."""
        try:
            response = self.sock.makefile("r").readline()
            return json.loads(response)
        except Exception as e:
            print(f"Receive error: {e}")
            return None

    def start_game(self):
        """Start a new game."""
        self.set_status("Starting game...")
        threading.Thread(target=self._start_game_thread, daemon=True).start()

    def _start_game_thread(self):
        response = self.send_command("START")
        if response and response.get("status") == "ok":
            with self.lock:
                self.game_state = response
                self.selected_hand_index = None
                self.selected_capture_index = None
                self.available_captures = []
            self.set_status("Game started!")
        else:
            self.set_status("Failed to start game")

    def refresh_state(self):
        """Refresh game state from server."""
        threading.Thread(target=self._refresh_state_thread, daemon=True).start()

    def _refresh_state_thread(self):
        response = self.send_command("STATE")
        if response and response.get("status") == "ok":
            with self.lock:
                self.game_state = response
            self.set_status("State refreshed")
        else:
            self.set_status("Failed to refresh state")

    def play_card(self, hand_index):
        """Play a card from hand."""
        self.set_status(f"Playing card {hand_index}...")
        self.selected_hand_index = hand_index

        # Get possible captures
        threading.Thread(
            target=self._get_captures_thread, args=(hand_index,), daemon=True
        ).start()

    def _get_captures_thread(self, hand_index):
        response = self.send_command(f"CAPTURES {hand_index}")
        if response and response.get("status") == "ok":
            with self.lock:
                self.available_captures = response.get("captures", [])

            if len(self.available_captures) == 0:
                # No captures, play without capture
                self._play_card_thread(hand_index, -1)
            elif len(self.available_captures) == 1:
                # Only one capture option, automatically select it
                self._play_card_thread(hand_index, 0)
            else:
                # Multiple captures, let player choose (for now, auto-select first)
                self.set_status(
                    f"Multiple captures available ({len(self.available_captures)}), selecting first"
                )
                self._play_card_thread(hand_index, 0)
        else:
            self.set_status("Failed to get captures")

    def _play_card_thread(self, hand_index, capture_index):
        response = self.send_command(f"PLAY {hand_index} {capture_index}")
        if response and response.get("status") == "ok":
            with self.lock:
                self.game_state = response
                self.selected_hand_index = None
                self.selected_capture_index = None
                self.available_captures = []
            self.set_status("Card played successfully")
        else:
            self.set_status("Failed to play card")

    def finalize_round(self):
        """Finalize the round."""
        threading.Thread(target=self._finalize_thread, daemon=True).start()

    def _finalize_thread(self):
        response = self.send_command("FINALIZE")
        if response and response.get("status") == "ok":
            with self.lock:
                self.game_state = response
            self.set_status("Round finalized")
        else:
            msg = response.get("message", "Failed") if response else "Failed"
            self.set_status(f"Finalize: {msg}")

    def show_score(self):
        """Show the current score."""
        threading.Thread(target=self._show_score_thread, daemon=True).start()

    def _show_score_thread(self):
        response = self.send_command("SCORE")
        if response and response.get("status") == "ok":
            p1_score = response.get("player1Score", 0)
            p2_score = response.get("player2Score", 0)
            self.set_status(f"Score - Player 1: {p1_score}, Player 2: {p2_score}")
        else:
            self.set_status("Failed to get score")

    def render_game_state(self):
        """Render the current game state."""
        if not self.game_state:
            return

        # Clear previous cards
        for card_list in self.rendered_cards.values():
            for card_node in card_list:
                card_node.removeNode()

        self.rendered_cards = {"table": [], "p1": [], "p2": []}

        # Render table cards
        table_cards = self.game_state.get("table", [])
        for i, card_data in enumerate(table_cards):
            x = -3 + i * 1.5
            card_node = self.create_card_visual(card_data, (x, 0, 0))
            self.rendered_cards["table"].append(card_node)

        # Render player 1 hand (bottom)
        p1_data = self.game_state.get("player1", {})
        p1_hand = p1_data.get("hand", [])
        current_player = self.game_state.get("currentPlayer", "")
        is_p1_turn = current_player == p1_data.get("name", "Player 1")

        for i, card_data in enumerate(p1_hand):
            x = -2 + i * 1.5
            card_node = self.create_card_visual(card_data, (x, 0, -3))
            self.rendered_cards["p1"].append(card_node)

            # Add click handler if it's player 1's turn
            if is_p1_turn:
                self.add_card_click_handler(card_node, i)

        # Render player 2 hand (top)
        p2_data = self.game_state.get("player2", {})
        p2_hand = p2_data.get("hand", [])
        is_p2_turn = current_player == p2_data.get("name", "Player 2")

        for i, card_data in enumerate(p2_hand):
            x = -2 + i * 1.5
            card_node = self.create_card_visual(card_data, (x, 0, 3))
            self.rendered_cards["p2"].append(card_node)

            # Add click handler if it's player 2's turn
            if is_p2_turn:
                self.add_card_click_handler(card_node, i)

    def create_card_visual(self, card_data, position):
        """Create a visual representation of a card."""
        # Try to load the actual card model
        suit = card_data.get("suit", "").lower()
        rank_name = card_data.get("rank", "").lower()
        value = card_data.get("value", 0)

        # Map rank names to file names
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

        rank_file = rank_map.get(rank_name, str(value))
        card_name = f"{rank_file}_{suit}"
        card_path = f"scopa-panda3d/frontend/assets/cards/{card_name}.egg"

        try:
            card_node = self.loader.loadModel(card_path)
            if card_node:
                card_node.reparentTo(self.render)
                card_node.setPos(*position)
                card_node.setScale(0.3)
                return card_node
        except Exception as e:
            print(f"Failed to load card model {card_path}: {e}")

        # Fallback: create a simple colored box
        card_node = self.loader.loadModel("models/box")
        card_node.reparentTo(self.render)
        card_node.setPos(*position)
        card_node.setScale(0.5, 0.01, 0.7)

        # Color by suit
        colors = {
            "coins": (1, 0.84, 0, 1),  # Gold
            "cups": (0, 0, 1, 1),  # Blue
            "swords": (0.5, 0.5, 0.5, 1),  # Gray
            "clubs": (0, 1, 0, 1),  # Green
        }
        color = colors.get(suit, (1, 1, 1, 1))
        card_node.setColor(*color)

        return card_node

    def add_card_click_handler(self, card_node, hand_index):
        """Add click handler to a card."""
        # Simple collision detection for clicking
        card_node.setTag("clickable", "1")
        card_node.setTag("hand_index", str(hand_index))

        # Note: Full click handling would require collision rays
        # For simplicity, we'll bind keyboard numbers for now

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
        info.append("Press 1-3: Play card from hand")
        info.append("(Player 1 = bottom, Player 2 = top)")

        self.info_text.setText("\n".join(info))

        # Setup keyboard controls
        self.accept("1", self.play_card, [0])
        self.accept("2", self.play_card, [1])
        self.accept("3", self.play_card, [2])

    def set_status(self, text):
        """Update status text."""
        with self.lock:
            self.status_text.setText(f"Status: {text}")
        print(f"Status: {text}")


if __name__ == "__main__":
    app = ScopaGameFrontend()
    app.run()
