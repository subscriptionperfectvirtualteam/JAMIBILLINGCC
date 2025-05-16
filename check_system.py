"""
JamiBilling - System Check Utility
This script checks if all required dependencies are installed and properly configured.
"""

import sys
import os
import shutil
import platform

def check_python_version():
    """Check if Python version is 3.6 or higher"""
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print("❌ Python version must be 3.6 or higher")
        print(f"   Current version: {platform.python_version()}")
        return False
    else:
        print(f"✅ Python version: {platform.python_version()}")
        return True

def check_chrome():
    """Check if Chrome is installed"""
    if platform.system() == "Windows":
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        chrome_path_x86 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path) or os.path.exists(chrome_path_x86):
            print("✅ Google Chrome is installed")
            return True
    elif platform.system() == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            print("✅ Google Chrome is installed")
            return True
    elif platform.system() == "Linux":
        chrome_path = shutil.which("google-chrome")
        if chrome_path:
            print("✅ Google Chrome is installed")
            return True
    
    print("❌ Google Chrome not found")
    print("   Please install Chrome from https://www.google.com/chrome/")
    return False

def check_chromedriver():
    """Check if ChromeDriver is in PATH"""
    chromedriver_path = shutil.which("chromedriver")
    if chromedriver_path:
        print(f"✅ ChromeDriver found at: {chromedriver_path}")
        return True
    else:
        print("❌ ChromeDriver not found in PATH")
        print("   Download ChromeDriver from: https://chromedriver.chromium.org/downloads")
        print("   Make sure to download the version that matches your Chrome version")
        return False

def check_config():
    """Check if config.json exists and has the required fields"""
    if not os.path.exists("config.json"):
        print("❌ config.json not found")
        return False
    
    try:
        import json
        with open("config.json", "r") as f:
            config = json.load(f)
        
        required_fields = [
            ("database", "server"),
            ("database", "database"),
            ("database", "username"),
            ("database", "password"),
            ("rdn", "login_url"),
            ("rdn", "case_url_template")
        ]
        
        missing_fields = []
        for section, field in required_fields:
            if section not in config or field not in config[section]:
                missing_fields.append(f"{section}.{field}")
        
        if missing_fields:
            print(f"❌ config.json is missing required fields: {', '.join(missing_fields)}")
            return False
        else:
            print("✅ config.json contains all required fields")
            
            # Check if using default values
            if config["database"]["server"] == "yourserver.database.windows.net":
                print("⚠️  Warning: You are using default database credentials")
                print("   Update config.json with your actual database credentials")
            
            return True
        
    except Exception as e:
        print(f"❌ Error reading config.json: {str(e)}")
        return False

def check_directories():
    """Check if required directories exist"""
    required_dirs = [
        "static",
        "static/css",
        "static/js",
        "static/exports",
        "templates",
        "backend",
        "flask_session"
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"❌ The following directories are missing: {', '.join(missing_dirs)}")
        return False
    else:
        print("✅ All required directories exist")
        return True

def check_required_files():
    """Check if essential files exist"""
    required_files = [
        "app.py",
        "templates/index.html",
        "static/css/styles.css",
        "static/js/app.js",
        "backend/fee_categories.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ The following files are missing: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
        return True

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        "flask",
        "flask_session",
        "selenium",
        "bs4",  # BeautifulSoup
        "openpyxl",
        "werkzeug",
        "jinja2",
        "requests"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ The following Python packages are missing: {', '.join(missing_packages)}")
        print("   Run the start script to install them automatically")
        return False
    else:
        print("✅ All required Python packages are installed")
        return True

def main():
    """Run all checks and report results"""
    print("\n===== JamiBilling System Check =====\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Google Chrome", check_chrome),
        ("ChromeDriver", check_chromedriver),
        ("Configuration", check_config),
        ("Directories", check_directories),
        ("Required Files", check_required_files),
        ("Python Dependencies", check_dependencies)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n--- {name} Check ---")
        if not check_func():
            all_passed = False
    
    print("\n===== Check Summary =====")
    if all_passed:
        print("\n✅ All checks passed! JamiBilling should work correctly.")
        print("   Run the application with: python app.py")
    else:
        print("\n❌ Some checks failed. Please fix the issues before running JamiBilling.")
    
    print("\n=============================\n")

if __name__ == "__main__":
    main()
