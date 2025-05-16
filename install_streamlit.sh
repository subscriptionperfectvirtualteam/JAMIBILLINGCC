#!/bin/bash
echo "Installing JamiBilling Streamlit version..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements_streamlit.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
python -m playwright install chromium

# Make the file executable
chmod +x streamlit_app.py

echo "Setup complete!"
echo "To run the Streamlit application, use: streamlit run streamlit_app.py"

# Make this script executable
chmod +x install_streamlit.sh