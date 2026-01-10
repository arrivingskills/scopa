#!/bin/bash
# Script to run the Scopa Frontend

echo "====================================="
echo "Starting Scopa Game Frontend..."
echo "====================================="

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Installing requirements..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "Connecting to server at localhost:5000..."
echo "Make sure the GameServer is running!"
echo ""
echo "Controls:"
echo "  - Click 'Start Game' to begin"
echo "  - Press 1, 2, or 3 to play cards from hand"
echo "  - Click 'Finalize Round' when done"
echo "  - Click 'Show Score' to see results"
echo ""

# Run the frontend
python scopa_game.py
