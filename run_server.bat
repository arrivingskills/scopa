@echo off
REM Scopa Game Backend Server - Windows Launch Script

echo ========================================
echo Scopa Card Game - Backend Server
echo ========================================
echo.

REM Check if target/classes exists
if not exist "target\classes" (
    echo ERROR: Backend not compiled!
    echo Please run: mvn clean package
    echo.
    pause
    exit /b 1
)

echo Starting GameServer on port 5000...
echo Press Ctrl+C to stop the server
echo.

java -cp target\classes com.example.scopa.game.GameServer

pause
