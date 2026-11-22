#!/usr/bin/env bash
echo "==================================================="
echo "Starting AI CareerPilot Server..."
echo "==================================================="
cd "$(dirname "$0")"
if [ -d "venv" ]; then
    echo "Using virtual environment..."
    source venv/bin/activate
    python3 app.py
else
    echo "Using system python3..."
    python3 app.py
fi
