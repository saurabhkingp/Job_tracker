#!/bin/bash
set -e

echo "=== Local Job Tracker Setup ==="
# 1. Activate/Create Virtual Environment
if [ ! -d "job" ]; then
    echo "Creating virtual environment 'job'..."
    python3 -m venv job
fi
source job/bin/activate

# 2. Install dependencies
echo "Installing required Python dependencies..."
pip install --upgrade pip
pip install python-fasthtml fastlite pandas uvicorn

# 3. Launch App
echo "Starting development server on http://localhost:5001..."
# Launch app in background and wait for it to start
python main.py &
APP_PID=$!

# Wait 2 seconds for server to start, then open in system browser
sleep 2
if command -v xdg-open > /dev/null; then
    xdg-open "http://localhost:5001"
elif command -v gnome-open > /dev/null; then
    gnome-open "http://localhost:5051"
fi

# Keep script running to catch server output
wait $APP_PID
