# RDN Fee Scraper - Playwright Integration

This document describes the Playwright integration that has been added to the RDN Fee Scraper application.

## Overview

Playwright has been added as an alternative browser automation engine alongside Selenium. Playwright provides better performance, reliability, and modern web capabilities compared to Selenium in many scenarios.

## Features

- **Dual Engine Support**: Use either Playwright or Selenium for browser automation
- **Auto Detection**: Automatically uses Playwright if available, falls back to Selenium
- **Configurable**: Can be explicitly configured to use a specific engine
- **Enhanced Performance**: Faster page loading and interaction with Playwright
- **Better Stability**: More reliable handling of dynamic content and modern web apps

## Configuration

The configuration has been updated to support Playwright:

```python
# Browser settings
"browser": {
    "headless": False,
    "slow_mo": 50,
    "default_timeout": 300000,  # 5 minutes timeout
    "engine": "auto"  # Can be "selenium", "playwright", or "auto"
},

# Playwright-specific settings
"playwright": {
    "browser_type": "chromium",  # can be "chromium", "firefox", or "webkit"
    "headless": False,
    "slow_mo": 50,
    "viewport": {"width": 1920, "height": 1080},
    "timeout": 300000,  # 5 minutes timeout
    "record_video": False,
    "record_har": False,
    "screenshots": "only-on-failure",
    "trace": "off"
}
```

## Usage

### Installation

To use Playwright, install it with:

```bash
pip install playwright
playwright install
```

### Running the Server

The server will automatically use Playwright if it's installed:

```bash
python server-upgradedv2.py
```

To explicitly choose an engine, set the `engine` option in the config:

```python
config["browser"]["engine"] = "playwright"  # Force use of Playwright
config["browser"]["engine"] = "selenium"    # Force use of Selenium
```

## Implementation Details

- **PlaywrightDriver Class**: A dedicated wrapper class that provides similar API to Selenium
- **Engine Detection**: Automatic detection and fallback mechanism
- **Dual API Support**: All browser automation functions support both engines
- **Enhanced Extraction**: JavaScript-based extraction for better performance

## Performance Benefits

- **Faster Navigation**: Playwright's network idle detection is more reliable
- **Better JavaScript Support**: Direct JavaScript execution is more robust
- **Enhanced Stability**: Better handling of modern web components
- **Parallel Contexts**: Can run multiple browser contexts in parallel

## Debugging

Playwright offers enhanced debugging features:

- **Tracing**: Record and playback browser interactions
- **Video Recording**: Capture video of test runs
- **Screenshots**: Capture screenshots at various points
- **Console Logs**: Access browser console logs

## File Structure

The following files are related to the Playwright integration:

- `playwright_driver.py`: The PlaywrightDriver implementation
- `server-upgradedv2.py`: Updated to support both engines
- `README_PLAYWRIGHT.md`: This documentation file