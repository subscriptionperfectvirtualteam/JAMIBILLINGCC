# JamiBilling - RDN Fee Scraper

## Overview
JamiBilling is a web-based application that automates the extraction and processing of fee information from the Recovery Database Network (RDN) system. The application streamlines the RDN workflow by providing a user-friendly interface to retrieve, categorize, and analyze billing information from RDN case pages.

## Features
1. **User Authentication**: Securely logs in to the RDN system with your credentials
2. **Automated Data Extraction**: Extracts client information, fee details, and update history from RDN case pages
3. **Database Integration**: Queries your Azure SQL database for fee structures and approved amounts
4. **Intelligent Fee Categorization**: Automatically categorizes fees based on descriptions using the included fee type reference
5. **Comprehensive Reporting**: Displays all fee information in an organized, user-friendly interface
6. **Export Options**: Export results to PDF or Excel for sharing and record-keeping

## Technology Stack
- **Backend**: Python with Flask web framework
- **Frontend**: HTML, CSS, JavaScript
- **Web Scraping**: Selenium WebDriver with Chrome in headless mode
- **Database**: Azure SQL (accessed via PyPyODBC)
- **Data Processing**: BeautifulSoup4, OpenPyXL
- **Export Functionality**: jsPDF, XLSX

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Chrome browser and ChromeDriver
- Access to the RDN system with valid credentials
- Connection to your Azure SQL database

### Easy Installation
1. Clone or download this repository
2. Run the startup script:
   - On Windows: Double-click `start.bat`
   - On Linux/macOS: Run `./start.sh`

The startup script will:
- Create a virtual environment
- Install all required dependencies
- Set up necessary directories
- Start the application

### Enhanced Version
For better debugging, logging, and error handling, use the enhanced version:
- On Windows: Run `run_enhanced.bat`
- On Linux/macOS: Run `./start_enhanced.sh`

The enhanced version includes:
- Detailed logging to `jami_billing.log`
- Saving HTML snapshots and screenshots to the `debug` directory
- Better error handling and fallbacks
- Debug endpoint at `/debug-logs` when running in debug mode
- Browser visibility options (show, minimize, or try to hide)

### Configuration
1. Edit the `config.json` file to set your database connection parameters:
   ```json
   {
       "database": {
           "provider": "SQLOLEDB",
           "server": "your-server.database.windows.net",
           "database": "your-database-name",
           "username": "your-username",
           "password": "your-password"
       },
       "rdn": {
           "login_url": "https://secureauth.recoverydatabase.net/public/login",
           "case_url_template": "https://app.recoverydatabase.net/alpha_rdn/module/default/case2/?case_id={case_id}"
       }
   }
   ```

2. Ensure ChromeDriver is installed and in your PATH or specify its location in the app.py file

## Usage

### Login and Credentials
1. Enter your RDN username, password, and security code
2. Enter the case ID you wish to analyze
3. Click "Start Process"

### Process Flow
The application will automatically:
1. Log in to the RDN system
2. Navigate to the specified case
3. Extract client and fee information from the summary page
4. Query your database for approved fee amounts
5. Extract update history from the Updates tab
6. Process and categorize all fee information
7. Display the results in a formatted dashboard

### Results and Reports
The results page includes:
- Client information card
- Database fee information card
- Table of extracted fees with categories
- Table of updates history
- Export options for PDF and Excel formats

## Fee Categorization
The application uses the included fee type reference to automatically categorize fees into the following groups:
- Storage & Lot Fees
- Repossession & Recovery Fees
- Transport & Delivery Fees
- Administrative & Processing Fees
- Agent & Labor Fees
- Inspection & Condition Fees
- Compliance & Legal Fees
- Other/Miscellaneous Fees

Fee categories are defined in the `backend/fee_categories.json` file and can be customized to match your organization's specific terminology.

## Troubleshooting

### Common Issues
- **Database Connection**: The application uses PyPyODBC for database connections, which is a pure Python implementation and does not require compilation. If you have connection issues, verify your credentials in config.json.
- **Chrome/ChromeDriver**: If you have issues with Chrome in headless mode, ensure you have the latest version of ChromeDriver installed.
- **Python Dependencies**: The startup scripts install all dependencies one by one to avoid compilation issues. If a dependency fails to install, you can try installing it manually.

For detailed troubleshooting guidance, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Debug Mode
The application runs with debug mode enabled (debug=True), which provides helpful error messages in the browser if something goes wrong.

The enhanced version also provides:
- Detailed logging to `jami_billing.log`
- Screenshots and HTML dumps in the `debug` directory 
- A web interface for viewing logs at `/debug-logs`

## Security Notes
- This application handles sensitive credentials, use it only on secure systems
- Credentials are not stored permanently, they are only held in the session
- The database connection string contains sensitive information, keep the config.json file secure

For detailed security recommendations, see [SECURITY.md](SECURITY.md)

## Development and Customization
To extend or customize the application:
- Modify the RDN web scraping in `app.py` to match any changes in the RDN webpage structure
- Add or modify fee categories in `backend/fee_categories.json`
- Customize the frontend appearance by editing the CSS in `static/css/styles.css`
- Add additional database queries in the `query_database` function in `app.py`
