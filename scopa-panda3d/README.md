# Scopa Panda3D - Complete Game

Complete Scopa card game with Java backend and Panda3D frontend.

## Quick Start

### Option 1: Using Scripts (Recommended)

**Terminal 1 - Start Backend:**
```bash
cd scopa
./run_server.sh
```

**Terminal 2 - Start Frontend:**
```bash
cd scopa-panda3d/frontend
./run_frontend.sh
```

### Option 2: Manual Setup

**1) Build and run the Java backend**

```bash
cd scopa
mvn clean compile
mvn exec:java -Dexec.mainClass="com.example.scopa.server.GameServer"
```

The GameServer listens on port 5000 and accepts JSON commands.

**2) Run the Panda3D frontend**

Install Panda3D (preferably in a virtualenv):

```bash
cd scopa-panda3d/frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scopa_game.py
```

## Game Files

- **Backend Server**: [src/com/example/scopa/server/GameServer.java](../../src/com/example/scopa/server/GameServer.java)
- **Complete Frontend**: [frontend/scopa_game.py](frontend/scopa_game.py)
- **Simple Example Frontend**: [frontend/main.py](frontend/main.py)
- **Simple Example Backend**: [backend/JavaBackend.java](backend/JavaBackend.java)

## How to Play

1. **Start Game**: Click the "Start Game" button
2. **Play Cards**: Use number keys 1-3 to play cards from your hand
   - Bottom row = Player 1's hand
   - Top row = Player 2's hand
   - Middle = Table cards
3. **Captures**: The game automatically selects captures based on Scopa rules
4. **Finalize**: Click "Finalize Round" when all cards are played
5. **Score**: Click "Show Score" to see the results

## Protocol

The GameServer uses a JSON-based protocol over TCP:

### Commands
- `START` - Start a new game, returns game state
- `STATE` - Get current game state
- `PLAY <handIndex> <captureIndex>` - Play a card from hand
- `CAPTURES <handIndex>` - Get possible captures for a card
- `FINALIZE` - Finalize the round
- `SCORE` - Get current score
- `HELLO` - Test connection
- `QUIT` - Disconnect

### Example Session
```
Client: START
Server: {"status":"ok","table":[...],"player1":{...},"player2":{...},...}

Client: CAPTURES 0
Server: {"status":"ok","captures":[[card1,card2],...]}

Client: PLAY 0 0
Server: {"status":"ok","table":[...],...}

Client: SCORE
Server: {"status":"ok","player1Score":5,"player2Score":3}
```

## Features

### Backend (Java)
- Complete Scopa game engine
- Capture logic with exact-match precedence
- Sum-based capture using backtracking algorithm
- Full scoring system (cards, coins, sette bello, primiera, scopas)
- Multi-threaded client handling
- JSON protocol

### Frontend (Python/Panda3D)
- 3D card rendering
- Interactive gameplay
- Real-time state updates
- Keyboard controls
- Status and score display
- Asynchronous communication

## Architecture

```
┌─────────────────────┐         TCP/JSON        ┌─────────────────────┐
│  Panda3D Frontend   │◄─────────────────────────►│   Java GameServer   │
│   (scopa_game.py)   │      Port 5000           │   (GameServer.java) │
│                     │                          │                     │
│  - 3D Rendering     │                          │  - Game Logic       │
│  - User Input       │                          │  - Rules Engine     │
│  - State Display    │                          │  - Scoring          │
└─────────────────────┘                          └─────────────────────┘
                                                           │
                                                           │
                                                  ┌────────▼────────┐
                                                  │   Scopa Core    │
                                                  │  - Model        │
                                                  │  - Rules        │
                                                  │  - Game         │
                                                  └─────────────────┘
```

## Development Notes

- The backend is fully tested with JUnit (see test-reports in target/)
- Card assets are 3D models in .egg format
- Frontend falls back to colored boxes if card models aren't found
- Multi-client support: each connection gets its own game instance

## Legacy Files

- `main.py` - Simple example frontend (ping/pong demo)
- `backend/JavaBackend.java` - Simple example backend
- These were the original starting point, kept for reference
