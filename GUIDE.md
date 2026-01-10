# Scopa Card Game - Complete Setup and Run Guide

## Overview

This is a complete implementation of the Italian card game **Scopa** with:

- **Backend**: Java 17 with game logic and rules
- **Frontend**: Python 3 with Panda3D for 3D graphics
- **Communication**: JSON over TCP on port 5000

---

## System Requirements

### All Platforms

- **Java**: JDK 17 or higher
- **Maven**: 3.6 or higher
- **Python**: 3.8 or higher
- **Panda3D**: 1.10.0 or higher

### Windows 10 Specific Requirements

- Install Java JDK 17: <https://adoptium.net/>
- Install Python 3.8+: <https://www.python.org/downloads/>
- Install pip (usually comes with Python)
- Ensure Java and Python are in your system PATH

---

## Installation Steps

### 1. Install Java (if not already installed)

**Windows 10:**

```cmd
# Download and install from https://adoptium.net/
# Verify installation:
java -version
javac -version
```

**macOS/Linux:**

```bash
# macOS with Homebrew:
brew install openjdk@17

# Ubuntu/Debian:
sudo apt install openjdk-17-jdk maven

# Verify:
java -version
javac -version
```

### 2. Install Python Dependencies

**All Platforms:**

```bash
# Navigate to frontend directory
cd scopa-panda3d/frontend

# Install Panda3D
pip install panda3d

# Or use requirements.txt if available:
pip install -r requirements.txt
```

**Windows 10 Troubleshooting:**
If pip is not recognized, use:

```cmd
python -m pip install panda3d
```

---

## Building the Backend

### Step 1: Build the Java Backend

**Windows 10:**

```cmd
cd scopa
mvn clean package
```

**macOS/Linux:**

```bash
cd scopa
mvn clean package
```

**Expected Output:**

```
[INFO] BUILD SUCCESS
[INFO] Total time: X.XXX s
```

### Step 2: Verify Tests Passed

The build runs unit tests automatically. You should see:

```
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0
```

---

## Running the Game

### Method 1: Using Launch Scripts (Recommended)

#### Windows 10

**Terminal 1 - Start Backend Server:**

```cmd
cd scopa
run_server.bat
```

**Terminal 2 - Start Frontend:**

```cmd
cd scopa-panda3d\frontend
run_frontend.bat
```

#### macOS/Linux

**Terminal 1 - Start Backend Server:**

```bash
cd scopa
./run_server.sh
```

**Terminal 2 - Start Frontend:**

```bash
cd scopa-panda3d/frontend
./run_frontend.sh
```

---

### Method 2: Manual Startup

#### Start Backend Server

**Windows 10:**

```cmd
cd scopa
java -cp target\classes com.example.scopa.game.GameServer
```

**macOS/Linux:**

```bash
cd scopa
java -cp target/classes com.example.scopa.game.GameServer
```

**Expected Output:**

```
GameServer: Server started on port 5000
GameServer: Waiting for connections...
```

#### Start Frontend

**Windows 10:**

```cmd
cd scopa-panda3d\frontend
python scopa_game.py
```

**macOS/Linux:**

```bash
cd scopa-panda3d/frontend
python3 scopa_game.py
```

---

## Playing the Game

### Game Controls

1. **Start Game Button**: Click to start a new game
2. **Keyboard Controls**:
   - Press `1`: Play the first card in your hand
   - Press `2`: Play the second card in your hand
   - Press `3`: Play the third card in your hand
3. **Finalize Round Button**: Click when all cards are played
4. **Show Score Button**: Display current scores
5. **Refresh Button**: Refresh the game state
6. **Quit Button**: Exit the game

### Game Layout

```
┌─────────────────────────────────────────┐
│         Player 2 Hand (TOP)             │
│         [Card] [Card] [Card]            │
│                                         │
│         Table Cards (CENTER)            │
│     [Card] [Card] [Card] [Card]         │
│                                         │
│         Player 1 Hand (BOTTOM)          │
│         [Card] [Card] [Card]            │
│                                         │
│  [Start] [Finalize] [Score] [Refresh]  │
└─────────────────────────────────────────┘
```

### Game Info Panel (Left Side)

Displays:

- Player 1 stats: hand size, captured cards, scopas
- Player 2 stats: hand size, captured cards, scopas
- Table card count
- Deck remaining
- Current player's turn
- Round status

---

## Troubleshooting

### Issue 1: Cards Not Displaying

**Symptoms:**

- Window opens but no cards visible
- Only colored boxes appear instead of card images

**Solutions:**

1. **Verify Card Assets Exist:**

   ```bash
   # Check that .egg files are present
   cd scopa-panda3d/frontend/assets/cards
   ls *.egg
   # Should show 42 .egg files
   ```

2. **Run Debug Version:**

   ```bash
   cd scopa-panda3d/frontend
   python scopa_game_debug.py
   ```

   Watch console output for detailed error messages.

3. **Check Working Directory:**
   - **CRITICAL**: You MUST run from `scopa-panda3d/frontend` directory
   - Card paths are relative: `assets/cards/*.egg`

   **Wrong:**

   ```bash
   cd scopa-panda3d
   python frontend/scopa_game.py  # ❌ Won't find cards!
   ```

   **Correct:**

   ```bash
   cd scopa-panda3d/frontend
   python scopa_game.py  # ✅ Correct!
   ```

4. **Windows Path Issues:**
   - Ensure you're using backslashes OR forward slashes consistently
   - Python handles both on Windows, but be consistent

---

### Issue 2: Connection Refused

**Symptoms:**

```
Status: Connection failed: [Errno 111] Connection refused
```

**Solutions:**

1. **Verify Backend is Running:**

   ```bash
   # Check if server is listening on port 5000
   netstat -an | grep 5000      # macOS/Linux
   netstat -an | findstr 5000   # Windows
   ```

2. **Check Firewall:**
   - Windows: Allow Java through Windows Firewall
   - Ensure port 5000 is not blocked

3. **Verify Backend Started Successfully:**
   - Backend terminal should show: "Server started on port 5000"
   - If you see errors, rebuild: `mvn clean package`

---

### Issue 3: Python/Panda3D Not Found

**Windows 10:**

```cmd
# If "python: command not found"
python3 scopa_game.py

# Or use full path:
C:\Python39\python.exe scopa_game.py
```

**macOS/Linux:**

```bash
# If python points to Python 2.x:
python3 scopa_game.py
```

---

### Issue 4: Maven Build Fails

**Solutions:**

1. **Clean Maven Cache:**

   ```bash
   mvn clean
   rm -rf target/
   mvn package
   ```

2. **Verify Java Version:**

   ```bash
   java -version
   # Should show Java 17 or higher
   ```

3. **Check pom.xml:**
   - Ensure `<maven.compiler.source>17</maven.compiler.source>`
   - Ensure `<maven.compiler.target>17</maven.compiler.target>`

---

### Issue 5: Game Doesn't Start After Clicking "Start Game"

**Solutions:**

1. **Check Console Output:**
   - Backend terminal should show: "START command received"
   - Frontend should show: "Sending START command"

2. **Verify Communication:**

   ```python
   # Test connection manually (Python)
   import socket, json
   sock = socket.create_connection(("127.0.0.1", 5000))
   sock.sendall(b"HELLO\n")
   print(sock.makefile("r").readline())
   # Should print: {"status":"ok"}
   ```

3. **Check for Exceptions:**
   - Look for stack traces in both terminals
   - Common issue: JSON parsing errors

---

### Issue 6: Cards Show as Colored Boxes

**Explanation:**
This is the **fallback mode** - the game works, but .egg models aren't loading.

**Appearance:**

- Gold boxes = Coins suit
- Blue boxes = Cups suit
- Gray boxes = Swords suit
- Green boxes = Clubs suit

**Solutions:**

1. **Verify you're running from correct directory** (see Issue 1)

2. **Check Panda3D Installation:**

   ```bash
   python -c "from panda3d.core import loadPrcFileData; print('OK')"
   ```

3. **Test Loading One Card:**

   ```python
   from direct.showbase.ShowBase import ShowBase
   app = ShowBase()
   card = app.loader.loadModel("assets/cards/ace_coins.egg")
   if card.isEmpty():
       print("Card is empty!")
   else:
       print("Card loaded successfully!")
   ```

---

## Windows 10 Specific Notes

### Path Separators

Both work in Python on Windows:

```python
"assets/cards/ace_coins.egg"   # Forward slashes (recommended)
"assets\\cards\\ace_coins.egg"  # Backslashes (escaped)
```

### Command Prompt vs PowerShell

- Both work fine
- PowerShell may require `.\run_server.bat` instead of `run_server.bat`

### Antivirus Software

- Some antivirus may block Java server on port 5000
- Add exception for Java and Python if needed

### File Permissions

- Ensure .bat files have execute permissions
- Right-click → Properties → Unblock (if downloaded)

---

## Game Rules (Scopa)

### Objective

Capture cards from the table to score points.

### Scoring System (5 categories)

1. **Most Cards**: Player who captured most cards gets 1 point
2. **Most Coins**: Player who captured most coins suit gets 1 point
3. **Sette Bello**: Player who captured 7 of Coins gets 1 point
4. **Primiera**: Best set of one card per suit (complex calculation) gets 1 point
5. **Scopas**: Each time you clear the table (capture all cards) gets 1 point

### Card Values for Capturing

- Ace = 1
- Two = 2
- Three = 3
- Four = 4
- Five = 5
- Six = 6
- Seven = 7
- Jack = 8
- Knight = 9
- King = 10

### Capture Rules

1. **Exact Match**: If your card exactly matches a table card value, you must capture it
2. **Sum Capture**: If no exact match, you can capture multiple cards that sum to your card's value
3. **No Capture**: If no match or sum possible, your card stays on the table

### Game Flow

1. 4 cards dealt to table
2. 3 cards dealt to each player
3. Players alternate turns playing one card
4. When hands are empty, deal 3 more cards to each player
5. Continue until deck is exhausted
6. Last player to capture gets remaining table cards
7. Calculate scores
8. First to 11 points wins (play multiple rounds)

---

## Architecture Overview

### Backend (Java)

```
src/com/example/scopa/
├── Main.java              # Entry point (not used for server)
├── game/
│   ├── GameServer.java    # TCP server handling client connections
│   └── ScopaGame.java     # Main game logic and turn management
├── model/
│   ├── Card.java          # Card representation
│   ├── Deck.java          # Deck management
│   ├── Player.java        # Player state
│   └── Table.java         # Table state
├── player/
│   └── HumanPlayer.java   # Player implementation
└── rules/
    └── ScopaRules.java    # Capture logic and scoring
```

### Frontend (Python/Panda3D)

```
scopa-panda3d/frontend/
├── scopa_game.py          # Main frontend application
├── scopa_game_debug.py    # Debug version with verbose output
├── assets/
│   └── cards/             # 3D card models (.egg files)
│       ├── ace_coins.egg
│       ├── 2_coins.egg
│       └── ... (40 total)
└── requirements.txt       # Python dependencies
```

### Communication Protocol (JSON over TCP)

#### Commands

- `HELLO` → Server responds with `{"status":"ok"}`
- `START` → Start new game, returns initial state
- `STATE` → Get current game state
- `CAPTURES <hand_index>` → Get possible captures for card
- `PLAY <hand_index> <capture_index>` → Play card with optional capture
- `FINALIZE` → Finalize round (when all cards played)
- `SCORE` → Get current scores

#### Example Game State JSON

```json
{
  "status": "ok",
  "table": [
    {"suit": "Coins", "rank": "Ace", "value": 1},
    {"suit": "Cups", "rank": "Three", "value": 3},
    ...
  ],
  "player1": {
    "name": "Player 1",
    "hand": [
      {"suit": "Swords", "rank": "Five", "value": 5},
      ...
    ],
    "captured": 12,
    "scopas": 2
  },
  "player2": { ... },
  "currentPlayer": "Player 1",
  "deckSize": 24,
  "roundOver": false
}
```

---

## Development & Testing

### Run Backend Tests Only

```bash
cd scopa
mvn test
```

### Run Specific Test

```bash
mvn test -Dtest=ScopaGameTest
```

### Enable Debug Logging

Backend (add to GameServer.java):

```java
private static final boolean DEBUG = true;
```

Frontend (use debug version):

```bash
python scopa_game_debug.py
```

---

## Common Development Tasks

### Add New Card Graphics

1. Create .egg file with Blender/Maya/similar
2. Name format: `<rank>_<suit>.egg` (e.g., `ace_coins.egg`)
3. Place in `scopa-panda3d/frontend/assets/cards/`
4. Ranks: `ace`, `2`-`7`, `jack`, `knight`, `king`
5. Suits: `coins`, `cups`, `swords`, `clubs` (lowercase)

### Modify Game Rules

Edit `src/com/example/scopa/rules/ScopaRules.java`:

- `possibleCaptures()` - Capture logic
- `scoreRound()` - Scoring calculation
- `calculatePrimiera()` - Primiera points

### Change Server Port

Edit `GameServer.java`:

```java
private static final int PORT = 5000; // Change this
```

Also update frontend `scopa_game.py`:

```python
self.sock = socket.create_connection(("127.0.0.1", 5000))  # Match port
```

---

## Quick Reference

### Start Game (Full Commands)

**Windows 10:**

```cmd
REM Terminal 1:
cd C:\path\to\scopa
mvn clean package
java -cp target\classes com.example.scopa.game.GameServer

REM Terminal 2 (new window):
cd C:\path\to\scopa\scopa-panda3d\frontend
python scopa_game.py
```

**macOS/Linux:**

```bash
# Terminal 1:
cd /path/to/scopa
mvn clean package
java -cp target/classes com.example.scopa.game.GameServer

# Terminal 2 (new tab):
cd /path/to/scopa/scopa-panda3d/frontend
python3 scopa_game.py
```

---

## Support & Issues

### Check These First

1. ✅ Backend server is running (shows "Server started on port 5000")
2. ✅ Frontend runs from `scopa-panda3d/frontend` directory
3. ✅ Card asset files exist in `assets/cards/`
4. ✅ Java 17+ and Python 3.8+ installed
5. ✅ Panda3D installed (`pip install panda3d`)
6. ✅ Port 5000 is not blocked by firewall

### Still Having Issues?

Run the debug frontend:

```bash
cd scopa-panda3d/frontend
python scopa_game_debug.py
```

The debug version provides detailed console output showing:

- Card loading attempts and results
- Server communication
- Rendering operations
- Error messages with stack traces

---

## License & Credits

This is an educational implementation of the traditional Italian card game Scopa.

**Technologies Used:**

- Java 17
- Maven
- Python 3
- Panda3D Game Engine
- JSON for data exchange
- TCP/IP sockets for networking

---

**Last Updated:** January 10, 2026
**Version:** 1.0
