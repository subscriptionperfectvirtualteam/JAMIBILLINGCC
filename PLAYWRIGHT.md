# JamiBilling Playwright Implementation

## Overview

This version of JamiBilling uses Playwright instead of Selenium for web automation. Playwright is a newer, more powerful browser automation library that provides better compatibility with modern browsers and improved resistance to automation detection.

## Advantages of Playwright

1. **Better Browser Compatibility**: Works well with latest Chrome/Edge/Firefox versions
2. **Improved Automation Detection Avoidance**: Less likely to be detected and blocked as a bot
3. **Faster and More Reliable**: More stable element selection and interaction
4. **No Need for Browser Drivers**: No ChromeDriver compatibility issues
5. **Powerful Selectors**: More flexible ways to locate elements on the page
6. **Built-in Wait Mechanisms**: Better handling of dynamic content loading

## Installation

To use the Playwright version:

1. Run the Playwright installation script:
   - On Windows: `install_playwright.bat`
   - On Linux/macOS: `./install_playwright.sh`

This will:
- Create a Python virtual environment if it doesn't exist
- Install all required packages including Playwright
- Download the Chromium browser that Playwright will use

## Running the Application

After installation, you can run the Playwright version with:
- On Windows: `run_playwright.bat`
- On Linux/macOS: `./run_playwright.sh`

You'll be prompted to choose whether to show the browser windows during automation.

## Technical Implementation

The Playwright version differs from the Selenium version in these key ways:

1. **Asynchronous Operation**:
   - Uses Python's `asyncio` for asynchronous browser automation
   - More efficient handling of multiple operations

2. **Browser Management**:
   - Uses Playwright's built-in browser management
   - No need for external browser drivers

3. **Element Selection**:
   - Uses Playwright's powerful CSS and text-based selectors
   - Multiple fallback strategies for finding elements

4. **Error Handling**:
   - More robust error handling with try/except blocks
   - Screenshots captured at critical points for debugging

## Troubleshooting

If you encounter issues:

1. Check the debug directory for screenshots and HTML dumps
2. Review the `jami_billing.log` file for detailed logs
3. Access the `/debug-logs` endpoint in the web application

## Comparison with Selenium

| Feature | Selenium | Playwright |
|---------|----------|------------|
| Browser Support | Requires specific drivers for each browser version | Built-in browser management |
| Automation Detection | More easily detected | Better evasion capabilities |
| Speed | Slower | Faster |
| Async Support | Limited | Full async/await support |
| Element Selection | Basic selectors | Advanced selectors including text content |
| Stability | Can be flaky with dynamic content | More stable with dynamic content |
| Error Recovery | Limited | Better error handling capabilities |

## Fallback to Selenium

If you need to use the Selenium version for any reason, you can still run:
- `run.bat` or `run_enhanced.bat` (Windows)
- `./start.sh` (Linux/macOS)