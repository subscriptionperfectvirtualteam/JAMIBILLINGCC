# RDN Fee Scraper

A comprehensive web application that automates fee extraction and categorization from the Recovery Database Network (RDN) platform. This tool streamlines the process of tracking, categorizing, and verifying fees associated with recovery cases.

## 🔍 Overview

RDN Fee Scraper automates the following workflow:

1. **Authentication** - Securely logs into the RDN platform
2. **Case Navigation** - Accesses specified case pages by ID
3. **Data Extraction** - Scrapes fee data from "My Summary" and "Updates" tabs
4. **Fee Processing** - Matches fees against approved matrices and whitelists
5. **Database Storage** - Saves verified fees to Azure SQL Database
6. **Reporting** - Generates structured reports and exports

## ⚙️ Features

- **Automated Web Scraping** - Uses Selenium to navigate and extract data from RDN
- **Multi-Tab Processing** - Scrapes both "My Summary" and "Updates" tabs for comprehensive fee data
- **Optimization** - Implements JavaScript-based extraction for faster performance
- **Fee Categorization** - Distinguishes between repo fees and pre-approved non-repo fees
- **Database Integration** - Connects with Azure SQL for persistent storage
- **Real-time Progress** - Provides live updates via Socket.IO
- **Export Options** - Generates CSV, JSON, and HTML reports
- **Error Resilience** - Multiple fallback strategies and error handling mechanisms

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser installed
- ODBC Driver 17 for SQL Server (for database functionality)
- Network access to RDN platform

### Installation

#### Windows

```batch
# Clone or download the repository
git clone https://github.com/yourusername/rdn-fee-scraper.git
cd rdn-fee-scraper

# Install dependencies using the batch file
install_dependencies.bat

# Or manually install requirements
pip install -r requirements.txt
```

#### Linux/macOS

```bash
# Clone or download the repository
git clone https://github.com/yourusername/rdn-fee-scraper.git
cd rdn-fee-scraper

# Install dependencies
pip install -r requirements.txt

# For database functionality on Linux, install ODBC Driver 17
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
apt-get install -y unixodbc-dev msodbcsql17
```

### Database Configuration

Create a `config.txt` file in the root directory with your Azure SQL Database credentials:

```
Server - your-server.database.windows.net
USername - your-username
Password - your-password
Database - your-database
```

## 💻 Usage

### Starting the Application

Run the optimized version of the scraper:

```bash
python server-upgraded.py
```

Or use the helper script:

```bash
python run_improved.py
```

On Windows, you can also use:

```batch
start_app.bat
```

The application will start a web server at http://localhost:5050 and automatically open your browser.

### Workflow

1. **Login** - Enter your RDN credentials (username, password, security code)
2. **Case Entry** - Input the case ID you want to analyze
3. **Scraping** - Watch real-time progress as the application:
   - Logs into RDN
   - Navigates to the case page
   - Extracts case information
   - Scrapes the My Summary tab
   - Loads and scrapes the Updates tab
   - Processes and categorizes fees
4. **Results** - Review the categorized fees, with options to:
   - Export to CSV
   - Save to database
   - View detailed breakdowns

## ⚡ Performance Optimization

The scraper has been optimized with these enhancements:

| Operation | Before | After | Improvement |
|-----------|--------|-------|-------------|
| My Summary Tab Scraping | ~400s | ~30s | 92% faster |
| Updates Tab Loading | ~60s | ~15s | 75% faster |
| Updates Tab Scraping | ~30s | ~5-10s | 70-83% faster |
| Fee Extraction | Variable | Fixed | More predictable |

### Performance Techniques

- **JavaScript-Based Extraction** - Direct DOM access for more efficient element finding
- **Reduced Wait Times** - Dynamic waiting based on page state
- **Efficient DOM Traversal** - Limited search depth and element processing
- **Optimized Regular Expressions** - Pre-compiled patterns for faster text processing
- **Memory Efficiency** - Limited context window size and content truncation

## 🧩 Architecture

The RDN Fee Scraper is organized into these modules:

1. **Web Server** - Flask application with Socket.IO for real-time communication
2. **Scraper Engine** - Selenium-based web automation with multiple extraction strategies
3. **Database Layer** - Azure SQL connectivity for storing and retrieving fee data
4. **Fee Processing** - Logic for categorizing and validating fees against whitelists
5. **Reporting** - Export and reporting functionality for various formats

## 📊 Fee Categorization

The scraper recognizes these fee types:

### Repo Fees
- Based on lienholder and repo type (looked up from database)
- Uses standard fees as fallback when specific matches aren't found

### Pre-approved Non-Repo Fees
The following fee types are automatically recognized as pre-approved:
- Field Visit
- Flatbed Fees
- Dolly Fees
- Mileage/Fuel
- Incentive
- Frontend (for Impound)
- LPR Involuntary Repo
- Finder's fee
- CR AND PHOTOS FEE
- Fuel Surcharge
- LPR REPOSSESSION
- OTHER
- SKIP REPOSSESSION
- Bonus
- Keys Fee

### Other Fees
- Any fees not matching repo or pre-approved categories
- Logged for manual review and analysis

## 🔧 Troubleshooting

### Socket.IO Connection Issues

If you experience connection problems:

- Use `transports: ['polling', 'websocket']` in client configuration
- Ensure Socket.IO client version matches server version
- Try setting `forceNew: true` to reset connections
- Set explicit path if needed: `path: '/socket.io'`

### Browser Automation Failures

If Selenium can't control Chrome:

- Verify Chrome is installed and up-to-date
- Try headless mode: Set `config["browser"]["headless"] = True`
- Increase timeouts: Set `config["browser"]["default_timeout"] = 600000`
- Check error screenshots in the `rdn_data` folder

### Database Connection Issues

If database connections fail:

- Verify ODBC Driver 17 for SQL Server is installed
- Check network connectivity to Azure SQL server
- Verify credentials in config.txt are correct
- Test connection with another tool like SQL Server Management Studio

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

## ⚠️ Important Notes

- This application is designed for authorized RDN users only
- All data processing should comply with your organization's data policies
- Database credentials should be kept secure and not committed to version control
- Schedule periodic maintenance to adapt to RDN platform changes

## 📄 License

[Specify your license here]

## 🙏 Acknowledgements

- Recovery Database Network platform
- Flask and Flask-SocketIO for the web framework
- Selenium for browser automation
- Socket.IO for real-time communication
- Azure SQL for database storage