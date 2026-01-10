@echo off
REM Scopa Game Frontend - Windows Launch Script

echo ========================================
echo Scopa Card Game - Frontend (Panda3D)
echo ========================================
echo.

REM Check if assets exist
if not exist "assets\cards" (
    echo ERROR: Card assets not found!
    echo Expected: assets\cards\*.egg files
    echo.
    pause
    exit /b 1
)

REM Check Python installation
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo Checking Panda3D installation...
python -c "import panda3d" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Panda3D not installed!
    echo Installing Panda3D...
    python -m pip install panda3d
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Failed to install Panda3D. Please run manually:
        echo    pip install panda3d
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Testing connection to backend server...
python -c "import socket; sock = socket.create_connection(('127.0.0.1', 5000), timeout=2); print('Backend server is running'); sock.close()" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Cannot connect to backend server on port 5000
    echo Make sure the backend server is running first!
    echo.
    pause
)

echo.
echo Starting Scopa Frontend...
echo Working directory: %CD%
echo.

python scopa_game.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Frontend exited with error code: %ERRORLEVEL%
    echo.
    pause
)
