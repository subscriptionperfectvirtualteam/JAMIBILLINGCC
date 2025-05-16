@echo off
echo Starting JamiBilling Streamlit version...

if not exist venv (
    echo Python virtual environment not found. Running installer first...
    call install_streamlit.bat
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Streamlit application...
streamlit run streamlit_app.py

pause