@echo off
echo JamiBilling - Direct Package Installation
echo ==============================
echo.

rem Install the packages directly without virtual environment
echo Installing required packages...
echo.

echo Installing beautifulsoup4 (bs4)...
python -m pip install beautifulsoup4==4.11.2

echo Installing openpyxl...
python -m pip install openpyxl==3.1.2

echo Installing Flask and dependencies...
python -m pip install Flask==2.2.3 Flask-Session==0.4.0 Werkzeug==2.2.3 Jinja2==3.1.2

echo Installing other dependencies...
python -m pip install selenium==4.8.2 pypyodbc==1.3.6 xlsxwriter==3.0.9 requests==2.28.2

echo.
echo Creating required directories...
if not exist "static\exports" mkdir static\exports
if not exist "flask_session" mkdir flask_session
if not exist "drivers" mkdir drivers

echo.
echo Installing ChromeDriver...
python chromedriver_manager.py

echo.
echo Installation completed!
echo You can now run the application with: python app.py
echo.

pause
