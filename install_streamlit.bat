@echo off
echo Installing JamiBilling Streamlit version...

if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements_streamlit.txt

echo Installing Playwright browsers...
python -m playwright install chromium

echo Setup complete! 
echo To run the Streamlit application, use: streamlit run streamlit_app.py
echo.
echo Press any key to exit...
pause > nul