"""
Quick dependency installer script for JamiBilling
"""

import subprocess
import sys
import importlib.util
import os

# List of required packages
REQUIRED_PACKAGES = [
    "flask",
    "flask_session",
    "selenium",
    "bs4",
    "openpyxl",
    "pypyodbc",
    "jinja2",
    "werkzeug",
    "requests"
]

def is_package_installed(package_name):
    """Check if a Python package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package_name):
    """Install a Python package using pip"""
    print(f"Installing {package_name}...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", package_name], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Successfully installed {package_name}")
        return True
    else:
        print(f"❌ Failed to install {package_name}")
        print(f"Error: {result.stderr}")
        return False

def create_directories():
    """Create required directories if they don't exist"""
    directories = [
        "static/exports",
        "flask_session",
        "drivers"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory exists or created: {directory}")

def main():
    """Main function to install dependencies"""
    print("\n===== JamiBilling Dependency Installer =====\n")
    
    # Create required directories
    print("Creating required directories...")
    create_directories()
    
    # Check and install required packages
    print("\nChecking and installing required packages...")
    
    all_installed = True
    for package in REQUIRED_PACKAGES:
        if is_package_installed(package):
            print(f"✅ {package} is already installed")
        else:
            success = install_package(package)
            if not success:
                all_installed = False
    
    print("\n===== Installation Summary =====")
    if all_installed:
        print("✅ All dependencies installed successfully!")
        print("   You can now run the application with: python app.py")
    else:
        print("❌ Some packages failed to install.")
        print("   Please install them manually using pip.")
    
    print("\n================================\n")

if __name__ == "__main__":
    main()
