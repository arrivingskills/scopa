# Scopa Card Game

A complete implementation of the Italian card game Scopa with:

- **Backend**: Java game logic with TCP/JSON server
- **Frontend**: Python/Panda3D 3D graphical interface

## Project Structure

```
scopa/
├── src/com/example/scopa/          # Java backend
│   ├── game/ScopaGame.java         # Game orchestration
│   ├── model/                      # Card, Deck, Table, Rank, Suit
│   ├── player/                     # Player classes
│   ├── rules/ScopaRules.java       # Game rules and scoring
│   └── server/GameServer.java      # TCP server with JSON protocol
└── scopa-panda3d/
    ├── backend/JavaBackend.java    # Simple example backend
    └── frontend/
        ├── scopa_game.py           # Complete game frontend
        ├── main.py                 # Simple example frontend
        └── assets/cards/           # Card 3D models (.egg files)
```

## Features

### Backend (Java)

- Complete Scopa game rules implementation
- Capture logic with exact-match precedence
- Backtracking algorithm for sum-based captures
- Full scoring system:
  - Most cards (Carte)
  - Most coins (Denari)
  - Sette Bello (7 of Coins)
  - Primiera calculation
  - Scopa bonuses
- JSON-based TCP protocol for frontend communication
- Thread-safe multi-client support

### Frontend (Python/Panda3D)

- 3D card rendering using .egg models
- Interactive card playing (keyboard controls)
- Real-time game state display
- Turn management
- Score tracking
- Automatic capture selection

## Getting Started

### Prerequisites

- Java 17 or higher
- Maven
- Python 3.8+
- Panda3D

### Installation

1. **Build the Java backend:**

```bash
cd scopa
mvn clean compile
```

1. **Install Python dependencies:**

```bash
cd scopa-panda3d/frontend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Game

1. **Start the GameServer (in one terminal):**

```bash
cd scopa
mvn exec:java -Dexec.mainClass="com.example.scopa.server.GameServer"
```

The server will start on port 5000.

1. **Start the Frontend (in another terminal):**

```bash
cd scopa-panda3d/frontend
source venv/bin/activate  # If not already activated
python scopa_game.py
```

## How to Play

1. Click **"Start Game"** to begin a new round
2. Use **number keys 1-3** to play cards from your hand:
   - Player 1 (bottom) plays when it's their turn
   - Player 2 (top) plays when it's their turn
3. The game automatically handles capture selection
4. Click **"Finalize Round"** when all cards are played
5. Click **"Show Score"** to see round scores

## Game Rules

### Scopa Basics

- 40-card Italian deck (4 suits: Coins, Cups, Swords, Clubs)
- Ranks: Ace (1) through King (10)
- 3 cards dealt to each player, 4 to the table
- Players alternate turns playing one card
- Capture cards by matching value or sum of values
- **Exact match precedence**: If a single card matches, you must take it
- **Scopa**: Clearing the table (all cards captured)

### Scoring (per round)

- **Cards**: 1 point for most cards captured
- **Coins**: 1 point for most coin suit cards
- **Sette Bello**: 1 point for capturing 7 of Coins
- **Primiera**: 1 point for best primiera (special calculation)
- **Scopa**: 1 point per scopa

## Protocol

The backend communicates via JSON over TCP on port 5000.

### Commands

- `START` - Start a new game
- `STATE` - Get current game state
- `PLAY <handIndex> <captureIndex>` - Play a card
- `CAPTURES <handIndex>` - Get possible captures for a card
- `FINALIZE` - Finalize round (remaining cards to last capturer)
- `SCORE` - Calculate and return current score
- `QUIT` - Disconnect

### Response Format

All responses are JSON with at least a `status` field:

- `{"status": "ok", ...}` - Success with additional data
- `{"status": "error", "message": "..."}` - Error with description

## Development

### Running Tests

```bash
cd scopa
mvn test
```

### Project Architecture

The backend uses a clean separation of concerns:

- **Model**: Immutable card representations, deck management, table state
- **Rules**: Pure functions for capture logic and scoring
- **Game**: Stateful game orchestration
- **Server**: Network protocol and JSON serialization

The frontend uses Panda3D's task system for:

- Asynchronous backend communication
- 3D rendering and updates
- User input handling

## Future Enhancements

- AI opponent
- Multiplayer over network
- Game history and replay
- Custom card designs
- Tournament mode
- Mobile support

## License

Educational project - free to use and modify.
