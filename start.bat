@echo off
echo Starting Report Generator Bot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
if not exist "reports" mkdir reports
if not exist "static" mkdir static

REM Start the application
echo.
echo Starting Flask application...
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause 