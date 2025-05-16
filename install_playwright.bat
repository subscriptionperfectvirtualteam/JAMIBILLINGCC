@echo off
echo JamiBilling - Installing Playwright
echo ===============================
echo.

rem Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or later and make sure it's in your PATH.
    pause
    exit /b 1
)

echo Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Using existing virtual environment.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing pip requirements...
pip install -r requirements_playwright.txt

echo Installing Playwright browsers...
python -m playwright install chromium

echo.
echo Creating required directories...
if not exist "debug" mkdir debug
if not exist "static\exports" mkdir static\exports
if not exist "flask_session" mkdir flask_session

echo.
echo Installation complete!
echo.
echo You can now run the application with: python app_playwright.py
echo.

pause