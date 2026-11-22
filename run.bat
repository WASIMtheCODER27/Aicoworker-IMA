@echo off
echo ===================================================
echo Starting AI CareerPilot Server...
echo ===================================================
cd /d "%~dp0"
if exist venv\Scripts\python.exe (
    echo Using virtual environment...
    venv\Scripts\python.exe app.py
) else (
    echo Virtual environment not found. Using system python...
    python app.py
)
pause
