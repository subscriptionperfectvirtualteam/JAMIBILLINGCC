"""
ChromeDriver Manager - Downloads the appropriate ChromeDriver automatically
"""

import os
import platform
import zipfile
import shutil
import requests
import subprocess
import re
from io import BytesIO

def get_chrome_version():
    """Get the installed Chrome version"""
    system = platform.system()
    chrome_version = None
    
    try:
        if system == "Windows":
            # Use registry query on Windows
            try:
                # Method 1: Try registry query
                output = subprocess.check_output(
                    'reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version',
                    shell=True
                ).decode('utf-8')
                version_match = re.search(r'version\s+REG_SZ\s+([\d.]+)', output)
                if version_match:
                    chrome_version = version_match.group(1)
            except:
                # Method 2: Try program files location
                chrome_paths = [
                    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                ]
                for path in chrome_paths:
                    if os.path.exists(path):
                        try:
                            output = subprocess.check_output(f'wmic datafile where name="{path.replace("\\", "\\\\")}" get Version /value', shell=True).decode('utf-8')
                            version_match = re.search(r'Version=(.+)', output)
                            if version_match:
                                chrome_version = version_match.group(1)
                                break
                        except:
                            pass
                        
        elif system == "Darwin":  # macOS
            try:
                output = subprocess.check_output(
                    ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
                    stderr=subprocess.STDOUT
                ).decode('utf-8')
                version_match = re.search(r'Google Chrome ([\d.]+)', output)
                if version_match:
                    chrome_version = version_match.group(1)
            except:
                pass
        elif system == "Linux":
            try:
                output = subprocess.check_output(
                    ['google-chrome', '--version'],
                    stderr=subprocess.STDOUT
                ).decode('utf-8')
                version_match = re.search(r'Google Chrome ([\d.]+)', output)
                if version_match:
                    chrome_version = version_match.group(1)
            except:
                pass
    except Exception as e:
        print(f"Error detecting Chrome version: {e}")
    
    return chrome_version

def get_chromedriver_url(chrome_version):
    """Get the appropriate ChromeDriver download URL for the given Chrome version"""
    if not chrome_version:
        print("Could not determine Chrome version. Using latest ChromeDriver.")
        # Use a stable version as fallback
        return "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip"
    
    # Extract major version
    major_version = chrome_version.split('.')[0]
    
    # For Chrome version 136+, use a specific version that works
    if int(major_version) >= 136:
        print(f"Chrome version {major_version} detected. Using ChromeDriver for Chrome 114 as fallback.")
        # Need to use an older driver with special options for compatibility
        system = platform.system()
        if system == "Windows":
            return "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip"
        elif system == "Darwin":  # macOS
            if platform.machine() == "arm64":  # Apple Silicon
                return "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_mac64_m1.zip"
            else:
                return "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_mac64.zip"
        elif system == "Linux":
            return "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"
        else:
            return "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip"
    
    # For newer Chrome versions (>=115), use the new download location
    if int(major_version) >= 115:
        system = platform.system()
        architecture = platform.machine().lower()
        
        if system == "Windows":
            platform_name = "win32"
            if architecture == "amd64" or architecture == "x86_64":
                platform_name = "win64"
        elif system == "Darwin":  # macOS
            platform_name = "mac-x64"
            if architecture == "arm64":
                platform_name = "mac-arm64"
        elif system == "Linux":
            platform_name = "linux64"
        else:
            platform_name = "win32"  # Default fallback
        
        # Get latest driver version for this Chrome version
        version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        try:
            response = requests.get(version_url)
            response.raise_for_status()
            driver_version = response.text.strip()
            return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_{platform_name}.zip"
        except Exception as e:
            print(f"Error getting ChromeDriver version: {e}")
            # Fallback to a stable version
            return "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip"
    else:
        # For older Chrome versions, use the version-specific URL
        try:
            # Get latest driver version for this Chrome version
            version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
            response = requests.get(version_url)
            response.raise_for_status()
            driver_version = response.text.strip()
            
            system = platform.system()
            if system == "Windows":
                return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"
            elif system == "Darwin":  # macOS
                if platform.machine() == "arm64":  # Apple Silicon
                    return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_mac64_m1.zip"
                else:
                    return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_mac64.zip"
            elif system == "Linux":
                return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_linux64.zip"
            else:
                return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"
        except Exception as e:
            print(f"Error getting ChromeDriver version: {e}")
            # Fallback to a stable version
            return "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip"

def download_chromedriver():
    """Download and install ChromeDriver locally"""
    print("Detecting Chrome version...")
    chrome_version = get_chrome_version()
    if chrome_version:
        print(f"Detected Chrome version: {chrome_version}")
    else:
        print("Could not detect Chrome version")
    
    # Get major version
    major_version = int(chrome_version.split('.')[0]) if chrome_version else 0
    
    # Download ChromeDriver
    download_url = get_chromedriver_url(chrome_version)
    print(f"Downloading ChromeDriver from: {download_url}")
    
    try:
        # Create driver directory if it doesn't exist
        driver_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drivers")
        os.makedirs(driver_dir, exist_ok=True)
        
        # First, remove any existing ChromeDriver
        chromedriver_path = os.path.join(driver_dir, "chromedriver")
        if platform.system() == "Windows":
            chromedriver_path += ".exe"
            
        if os.path.exists(chromedriver_path):
            print(f"Removing existing ChromeDriver: {chromedriver_path}")
            os.remove(chromedriver_path)
        
        # Download the file
        response = requests.get(download_url)
        response.raise_for_status()
        
        # Extract from zip
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            # Find the ChromeDriver executable in the zip
            chromedriver_name = None
            
            # Standard search for regular ChromeDriver zips
            for name in zip_file.namelist():
                if "chromedriver" in name.lower() and not name.endswith('/'):
                    chromedriver_name = name
                    break
            
            if not chromedriver_name:
                print("ChromeDriver not found in standard locations, trying alternative search...")
                # Try harder to find any executable in the zip
                for name in zip_file.namelist():
                    if not name.endswith('/') and ('exe' in name.lower() or 'chromedriver' in name.lower()):
                        chromedriver_name = name
                        break
            
            if not chromedriver_name:
                raise Exception("ChromeDriver executable not found in the downloaded zip")
            
            print(f"Found ChromeDriver at path in zip: {chromedriver_name}")
            
            # Extract the ChromeDriver executable
            print(f"Extracting ChromeDriver from zip file: {chromedriver_name}")
            with open(chromedriver_path, 'wb') as f:
                f.write(zip_file.read(chromedriver_name))
        
        # Make the file executable (on Unix systems)
        if platform.system() != "Windows":
            os.chmod(chromedriver_path, 0o755)
        
        print(f"ChromeDriver installed successfully at: {chromedriver_path}")
        return chromedriver_path
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return None

if __name__ == "__main__":
    # Test the ChromeDriver downloader
    download_chromedriver()
