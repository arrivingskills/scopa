@echo off
REM Scopa Game Frontend DEBUG Version - Windows Launch Script

echo ========================================
echo Scopa Card Game - Frontend DEBUG MODE
echo ========================================
echo.
echo This version shows detailed debug output
echo Use this if cards are not displaying properly
echo.

REM Check if assets exist
if not exist "assets\cards" (
    echo ERROR: Card assets not found!
    echo Expected: assets\cards\*.egg files
    echo.
    pause
    exit /b 1
)

echo Starting Debug Frontend...
echo Watch the console output for detailed information
echo.

python scopa_game_debug.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Frontend exited with error code: %ERRORLEVEL%
    echo.
)

pause
