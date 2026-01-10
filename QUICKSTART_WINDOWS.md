# Quick Start Guide for Windows 10

## Prerequisites Check

1. **Java 17 or Higher**

   ```cmd
   java -version
   ```

   If not installed: Download from <https://adoptium.net/>

2. **Python 3.8 or Higher**

   ```cmd
   python --version
   ```

   If not installed: Download from <https://www.python.org/downloads/>

3. **Maven**

   ```cmd
   mvn -version
   ```

   If not installed: Download from <https://maven.apache.org/download.cgi>

## One-Time Setup

### Step 1: Build the Backend

Open Command Prompt or PowerShell:

```cmd
cd C:\path\to\scopa
mvn clean package
```

Wait for "BUILD SUCCESS" message.

### Step 2: Install Python Dependencies

```cmd
cd C:\path\to\scopa\scopa-panda3d\frontend
pip install panda3d
```

Or if `pip` is not recognized:

```cmd
python -m pip install panda3d
```

## Running the Game (Every Time)

### Method 1: Using Batch Files (Easiest)

#### Terminal 1 - Backend Server

```cmd
cd C:\path\to\scopa
run_server.bat
```

Leave this window open while playing.

#### Terminal 2 - Frontend (New Window)

```cmd
cd C:\path\to\scopa\scopa-panda3d\frontend
run_frontend.bat
```

The game window will open!

---

### Method 2: Manual Commands

#### Terminal 1 - Backend

```cmd
cd C:\path\to\scopa
java -cp target\classes com.example.scopa.game.GameServer
```

#### Terminal 2 - Frontend

```cmd
cd C:\path\to\scopa\scopa-panda3d\frontend
python scopa_game.py
```

---

## Playing the Game

1. **Click "Start Game" button** in the game window
2. **Press keyboard keys to play cards:**
   - Press `1` to play first card
   - Press `2` to play second card
   - Press `3` to play third card
3. **Watch the game info** on the left side of screen
4. **Click "Finalize Round"** when all cards are played
5. **Click "Show Score"** to see current scores

## Troubleshooting

### Cards Not Showing?

**Run Debug Version:**

```cmd
cd C:\path\to\scopa\scopa-panda3d\frontend
run_debug.bat
```

Watch the console for error messages.

**Common Fix:**
Make sure you're in the `frontend` directory when running:

```cmd
# WRONG - won't find cards
cd C:\path\to\scopa\scopa-panda3d
python frontend\scopa_game.py

# CORRECT
cd C:\path\to\scopa\scopa-panda3d\frontend
python scopa_game.py
```

### Connection Refused Error?

1. Make sure backend server is running in Terminal 1
2. Check Windows Firewall - allow Java on port 5000
3. Try disabling antivirus temporarily

### Python Not Recognized?

Add Python to your PATH:

1. Search "Environment Variables" in Windows
2. Edit "Path" variable
3. Add: `C:\Python39` (or your Python installation path)
4. Restart Command Prompt

## Need More Help?

See the complete GUIDE.md for detailed troubleshooting and game rules.

---

**Quick Test:**

1. Open TWO Command Prompt windows
2. Window 1: `cd C:\path\to\scopa && run_server.bat`
3. Window 2: `cd C:\path\to\scopa\scopa-panda3d\frontend && run_frontend.bat`
4. Click "Start Game" button
5. Press `1`, `2`, or `3` to play cards

If you see cards (or colored boxes), it's working!
