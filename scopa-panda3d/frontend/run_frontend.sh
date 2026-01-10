#!/bin/bash
# Script to run the Scopa Frontend

echo "====================================="
echo "Starting Scopa Game Frontend..."
echo "====================================="

cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -d "assets/cards" ]; then
    echo "ERROR: assets/cards directory not found!"
    echo "Current directory: $(pwd)"
    echo "Please run this script from the frontend directory:"
    echo "  cd scopa-panda3d/frontend"
    echo "  ./run_frontend.sh"
    exit 1
fi

echo "✓ Found assets/cards directory"

# Check if backend is running
if ! nc -z localhost 5000 2>/dev/null; then
    echo ""
    echo "⚠ WARNING: Cannot connect to backend on port 5000"
    echo "Make sure the GameServer is running:"
    echo "  cd scopa"
    echo "  ./run_server.sh"
    echo ""
    echo "Press Enter to continue anyway, or Ctrl+C to cancel..."
    read
fi

echo "✓ Backend is reachable on port 5000"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Installing requirements..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
    echo "✓ Virtual environment activated"
fi

echo ""
echo "Connecting to server at localhost:5000..."
echo ""
echo "Controls:"
echo "  - Click 'Start Game' to begin"
echo "  - Press 1, 2, or 3 to play cards from hand"
echo "  - Click 'Finalize Round' when done"
echo "  - Click 'Show Score' to see results"
echo ""
echo "If cards don't display, run: python scopa_game_debug.py"
echo ""

# Run the frontend
python scopa_game.py
