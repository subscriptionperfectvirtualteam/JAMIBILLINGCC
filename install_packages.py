"""
Run this script to install the application requirements individually
"""

import subprocess
import sys
import os

# Define packages to install
packages = [
    "beautifulsoup4==4.11.2",  # bs4 module comes from this package
    "openpyxl==3.1.2",
    "Flask==2.2.3",
    "Flask-Session==0.4.0",
    "selenium==4.8.2",
    "pypyodbc==1.3.6",
    "xlsxwriter==3.0.9",
    "Werkzeug==2.2.3", 
    "Jinja2==3.1.2",
    "requests==2.28.2"
]

def install_package(package):
    """Install a single package and handle errors"""
    print(f"Installing {package}...")
    try:
        # For beautifulsoup4, also ensure bs4 module works
        if package.startswith("beautifulsoup4"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("Testing bs4 import...")
            try:
                import bs4
                print("✅ bs4 import successful!")
            except ImportError:
                print("⚠️ bs4 module not working, trying alternative install...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", "beautifulsoup4"])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}. Error: {e}")
        return False

# Create necessary directories
print("Creating directories...")
os.makedirs("static/exports", exist_ok=True)
os.makedirs("flask_session", exist_ok=True)
os.makedirs("drivers", exist_ok=True)

# Install packages one by one
print("\n=== Installing packages ===\n")
all_success = True
for package in packages:
    success = install_package(package)
    if not success:
        all_success = False

# Final message
if all_success:
    print("\n✅ All packages installed successfully!")
else:
    print("\n⚠️ Some packages failed to install. Please check the errors above.")

print("\nNow downloading ChromeDriver...")
try:
    subprocess.check_call([sys.executable, "chromedriver_manager.py"])
    print("✅ ChromeDriver setup complete!")
except Exception as e:
    print(f"❌ ChromeDriver setup failed: {e}")

print("\nSetup complete! You can now run the application with: python app.py")
