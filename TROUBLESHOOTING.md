# JamiBilling Troubleshooting Guide

## Common Issues and Solutions

### Installation Problems

1. **Missing Python Dependencies**
   - **Symptom**: Error mentioning a missing module when starting the application
   - **Solution**: Run `pip install -r requirements.txt` or use the individual installation scripts
   - **Advanced**: Check the logs for specific error messages

2. **ChromeDriver Issues**
   - **Symptom**: Browser fails to start with a message about ChromeDriver
   - **Solution**:
     - Delete the `/drivers` directory and let the app download a fresh ChromeDriver
     - Manually download ChromeDriver matching your Chrome version from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
     - Place it in the `drivers` directory

### Login Problems

1. **RDN Login Failures**
   - **Symptom**: "Login failed" or "Login timed out" error
   - **Solution**:
     - Verify your RDN credentials are correct
     - Check your internet connection
     - Try running the enhanced version with `run_enhanced.bat` or `start_enhanced.sh` for better debugging
     - Check if RDN has changed their login page structure

2. **Security Code Issues**
   - **Symptom**: "Security code field not found" error
   - **Solution**:
     - RDN may have changed their login form format
     - Check the saved HTML in the debug directory to inspect the form structure
     - Update the security code field detection in the app.py file

### Database Connection Issues

1. **Database Connection Failures**
   - **Symptom**: Warning about database connection and using mock data
   - **Solution**:
     - Verify your database credentials in `config.json`
     - Check if the database server is accessible from your network
     - Ensure that the database driver is properly installed
     - Test connection with a separate tool to confirm access rights

### Scraping Issues

1. **Data Extraction Problems**
   - **Symptom**: Missing or incorrect information in results
   - **Solution**:
     - Check if RDN has updated their website layout
     - Run the enhanced version and check debug screenshots and saved HTML
     - Update the scraping patterns in the app.py file based on the new layout

2. **Browser Automation Detection**
   - **Symptom**: Browser is detected as automated and blocked by RDN
   - **Solution**:
     - Do not use headless mode (this is already handled)
     - Try option 1 (visible browser) when starting the app
     - If persistent, add more anti-detection measures to the Chrome options

## Debug Mode Utilities

For advanced troubleshooting, the enhanced version provides debugging tools:

1. **Debug Log Files**
   - Location: `jami_billing.log` in the application directory
   - Contains detailed logging information about all operations

2. **HTML Snapshots**
   - Location: `debug/*.html` files
   - Contain the HTML of key pages for inspection

3. **Screenshots**
   - Location: `debug/*.png` files
   - Visual snapshots of the automation process

4. **Debug Endpoint**
   - URL: `http://localhost:5000/debug-logs`
   - Only available when running in debug mode
   - Provides access to logs and debug files through the web interface

## Getting Help

If you continue to experience issues:

1. Check the detailed logs in `jami_billing.log`
2. Run the enhanced version for better diagnostics
3. Take screenshots of any error messages
4. Document the steps to reproduce the issue