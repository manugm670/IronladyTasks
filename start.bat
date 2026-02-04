@echo off
echo ============================================
echo    Sthree AI - Starting...
echo ============================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create a .env file with your credentials
    pause
    exit /b 1
)

REM Check if agent.py exists
if not exist agent.py (
    echo ERROR: agent.py not found!
    echo Please make sure agent.py is in this folder
    pause
    exit /b 1
)

REM Check if server.py exists
if not exist server.py (
    echo ERROR: server.py not found!
    pause
    exit /b 1
)

echo Starting Sthree AI Agent...
echo.
start "Sthree AI Agent" cmd /k python agent.py dev

timeout /t 3 /nobreak > nul

echo Starting Sthree AI Web Server...
echo.
start "Sthree AI Server" cmd /k python server.py

timeout /t 3 /nobreak > nul

echo.
echo ============================================
echo    Sthree AI is starting!
echo ============================================
echo.
echo Two windows have opened:
echo   1. Sthree AI Agent (don't close)
echo   2. Sthree AI Server (don't close)
echo.
echo Open your browser to:
echo   http://localhost:5000
echo.
echo Press any key to exit this window...
pause > nul
