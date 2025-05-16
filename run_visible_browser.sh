#!/bin/bash
echo "Starting JamiBilling application with visible browser..."
export JAMI_HIDE_BROWSER=False
python app_playwright.py