# JamiBilling Non-Headless Browser Usage Guide

## Overview

The JamiBilling application has been updated to use a non-headless browser approach because the RDN website appears to be blocking automated headless browsers. This document explains how to use the application effectively with this change.

## Running Options

You now have several options for running the application with different browser visibility settings:

### Option 1: Full Browser Visibility
- Browser windows will be fully visible during automation
- You can see what's happening and debug more easily
- May be distracting with windows opening and closing

### Option 2: Minimized Browser Windows
- Browser windows will be minimized but still in the taskbar
- Less distracting than full visibility
- Still allows checking the browser if needed

### Option 3: Hidden Browser Windows
- Attempts to hide browser windows as much as possible
- May not work completely on all systems
- Best for running as a background process

## How to Choose Your Option

### Using the Batch Script
Run `run_with_options.bat` and select your preferred option:
```
JamiBilling - Run with Options
==============================

Choose how you want to run the browser:
1. Show browser windows (default)
2. Minimize browser windows
3. Try to hide browser windows (may not work with all setups)

Enter your choice (1-3):
```

### Using the Python Runner
Run `python run_app.py` and select your preferred option:
```
=== JamiBilling Smart Runner ===

How would you like to run the browser?
1. Show browser windows (default)
2. Minimize browser windows
3. Try to hide browser windows (may not work with all setups)

Enter your choice (1-3):
```

## Important Notes

1. **Browser Interaction**: Do not interact with the browser while the automation is running, as this may disrupt the process.

2. **Login Security**: The application uses special techniques to appear more like a regular browser than an automated tool, which helps bypass RDN's anti-automation measures.

3. **Performance**: Non-headless mode may be slightly slower and use more resources than headless mode.

4. **Browser Windows**: Multiple browser windows may appear during the process as the application navigates through different pages.

## Troubleshooting

If you experience issues with the non-headless browser:

1. **Try a different visibility option** - Some websites may work better with different settings.

2. **Ensure Chrome is up-to-date** - The application works best with the latest version of Chrome.

3. **Check for error messages** - The application will display error messages in the console that can help identify issues.

4. **Chrome crashes** - If Chrome crashes, make sure you don't have too many browser instances running simultaneously.

## Advanced Configuration

If you want to permanently set your browser visibility preference, you can create a `.env` file in the application directory with:

```
JAMI_MINIMIZE_BROWSER=true
```

This will set the browser to minimized mode by default.
