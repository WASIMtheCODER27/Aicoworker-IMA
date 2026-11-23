@echo off
echo ===================================================
echo Starting AI CareerPilot Server...
echo ===================================================
cd /d "%~dp0"

set PYTHON_CMD=python
if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe -c "import flask" >nul 2>&1
    if %errorlevel% equ 0 (
        echo Using virtual environment...
        set PYTHON_CMD=venv\Scripts\python.exe
    ) else (
        echo Virtual environment missing dependencies, using system python...
    )
)

%PYTHON_CMD% app.py
pause
