#!/bin/bash
echo "Starting JamiBilling Streamlit version..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Python virtual environment not found. Running installer first..."
    bash ./install_streamlit.sh
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Set environment variable for browser visibility
read -p "Do you want to show the browser during automation? (y/n): " show_browser
if [[ $show_browser == "y" || $show_browser == "Y" ]]; then
    export JAMI_HIDE_BROWSER=False
    echo "Browser will be visible during automation."
else
    export JAMI_HIDE_BROWSER=True
    echo "Browser will run in headless mode."
fi

# Start Streamlit application
echo "Starting Streamlit application..."
streamlit run streamlit_app.py

# Make this script executable
chmod +x run_streamlit.sh