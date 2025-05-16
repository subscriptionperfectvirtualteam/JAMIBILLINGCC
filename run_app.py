"""
Smart runner script for JamiBilling
- Checks dependencies and installs if missing
- Runs the application
"""

import subprocess
import sys
import importlib.util
import os

# List of required packages
REQUIRED_PACKAGES = {
    "flask": "Flask==2.2.3",
    "flask_session": "Flask-Session==0.4.0",
    "selenium": "selenium==4.8.2",
    "bs4": "beautifulsoup4==4.11.2",
    "openpyxl": "openpyxl==3.1.2",
    "pypyodbc": "pypyodbc==1.3.6",
    "werkzeug": "Werkzeug==2.2.3",
    "jinja2": "Jinja2==3.1.2",
    "requests": "requests==2.28.2"
}

def is_package_installed(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_spec):
    """Install a Python package using pip"""
    print(f"Installing {package_spec}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_spec])
        return True
    except subprocess.CalledProcessError:
        return False

def download_chromedriver():
    """Download ChromeDriver if needed"""
    try:
        driver_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers")
        os.makedirs(driver_dir, exist_ok=True)
        
        if not os.path.exists(os.path.join(driver_dir, "chromedriver.exe")) and not os.path.exists(os.path.join(driver_dir, "chromedriver")):
            print("ChromeDriver not found. Downloading...")
            # Import here to avoid dependency issues
            chromedriver_module = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver_manager.py")
            if os.path.exists(chromedriver_module):
                subprocess.check_call([sys.executable, chromedriver_module])
            else:
                print("ChromeDriver manager not found!")
    except Exception as e:
        print(f"Error setting up ChromeDriver: {e}")

def create_directories():
    """Create required directories"""
    os.makedirs("static/exports", exist_ok=True)
    os.makedirs("flask_session", exist_ok=True)
    os.makedirs("drivers", exist_ok=True)

def main():
    print("=== JamiBilling Smart Runner ===\n")
    
    # Check for Python version
    if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 6):
        print("❌ Python 3.6 or higher required!")
        sys.exit(1)
    
    # Create directories
    print("Setting up directories...")
    create_directories()
    
    # Check dependencies
    print("\nChecking dependencies...")
    missing_packages = []
    
    for package, install_spec in REQUIRED_PACKAGES.items():
        if not is_package_installed(package):
            missing_packages.append(install_spec)
    
    # Install missing packages
    if missing_packages:
        print(f"\nNeed to install {len(missing_packages)} missing packages...")
        
        for package_spec in missing_packages:
            success = install_package(package_spec)
            if not success:
                print(f"❌ Failed to install {package_spec}")
                print("Please run the installation script: install_direct.bat")
                sys.exit(1)
    else:
        print("✅ All required packages are installed")
    
    # Set up ChromeDriver
    print("\nSetting up ChromeDriver...")
    download_chromedriver()
    
    # Ask about browser visibility
    print("\nHow would you like to run the browser?")
    print("1. Show browser windows (default)")
    print("2. Minimize browser windows")
    print("3. Try to hide browser windows (may not work with all setups)")
    
    try:
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "2":
            print("Running with minimized browser windows...")
            os.environ["JAMI_MINIMIZE_BROWSER"] = "true"
        elif choice == "3":
            print("Running with hidden browser windows...")
            os.environ["JAMI_MINIMIZE_BROWSER"] = "true"
            os.environ["JAMI_HIDE_BROWSER"] = "true"
        else:
            print("Running with visible browser windows...")
            os.environ["JAMI_MINIMIZE_BROWSER"] = "false"
    except:
        # Default to visible if error
        print("Running with visible browser windows (default)...")
        os.environ["JAMI_MINIMIZE_BROWSER"] = "false"
    
    # Run the application
    print("\n=== Starting JamiBilling Application ===")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.check_call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == "__main__":
    main()
