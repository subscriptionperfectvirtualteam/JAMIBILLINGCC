# Chrome Compatibility Guide

## Chrome Version Compatibility

JamiBilling uses Chrome and ChromeDriver for web automation. Chrome versions and ChromeDriver versions need to match for proper operation. The application has been enhanced to handle this compatibility automatically in most cases, but some Chrome versions may require special handling.

## Known Issues with Chrome 136+

If you're using Chrome version 136 or higher, you may encounter this error:

```
This version of ChromeDriver only supports Chrome version 114
Current browser version is 136.0.7103.94
```

### Solutions

1. **Use the enhanced version**: The `app_enhanced.py` includes fixes for Chrome 136+ compatibility, so run the application with:
   - On Windows: `run_enhanced.bat`
   - On Linux/macOS: `./start_enhanced.sh`

2. **Downgrade Chrome**: If you continue to have issues, consider installing Chrome version 114:
   - On Windows, download from: https://www.slimjet.com/chrome/download-chrome.php?file=files%2F114.0.5735.90%2FGoogleChromeEnterpriseBundle64.zip
   - On Mac, download from: https://www.slimjet.com/chrome/google-chrome-old-version.php

3. **Install a specific ChromeDriver version**:
   - Download ChromeDriver 114.0.5735.90 from: https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip
   - Extract and place the chromedriver.exe file in the `drivers` directory

## Automatic Compatibility Mode

The enhanced version of the application includes special compatibility modes:

1. **Browser options for newer Chrome versions**:
   - Added `--remote-debugging-port=9222` 
   - Added `--disable-gpu`
   - Added additional automation-detection prevention options

2. **Fallback mechanism**:
   - If the initial attempt to create the browser fails, alternative options are tried automatically
   - Older ChromeDriver version (114.0.5735.90) is used for compatibility with newer Chrome versions

## Manual Testing

If you need to test a specific Chrome/ChromeDriver combination, you can:

1. Close any running Chrome instances
2. Delete the existing `drivers/chromedriver.exe` file
3. Run the application with the enhanced version
4. Check the log file (`jami_billing.log`) for detailed browser startup information

## Using a Different Browser

If Chrome compatibility issues persist, you could modify the application to use Firefox or Edge instead, which would require changes to the automation code.