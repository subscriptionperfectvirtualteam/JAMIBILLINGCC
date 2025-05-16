# GLOBAL_CONFIG.md - Global Configuration for Claude

This file serves as a central configuration for Claude AI interactions with this codebase, combining both project-specific instructions from CLAUDE.md and global standards from Global.md.

## 🔍 Project Overview (from CLAUDE.md)

**RDN Fee Scraper** is a web application that automates the extraction and categorization of fees from the Recovery Database Network (RDN) platform. It logs into RDN, navigates to case pages, extracts structured case and fee data, matches against fee matrices and whitelists, and outputs validated results.

## 📋 Global Coding Standards (from Global.md)

### Preferred Languages & Versions
- Python: 3.11+
- JavaScript: ES2022+
- HTML/CSS: Semantic HTML5, CSS Grid & Flexbox
- Node.js: LTS (20.x preferred); use ECMAScript Modules (ESM)

### Style Guides
- Python: PEP8
- JavaScript: Airbnb JavaScript Style Guide
- HTML/CSS: Google HTML/CSS Style Guide
- Markdown: CommonMark, linted with markdownlint

### Naming Conventions
- Variables/Functions: camelCase
- Components/Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Files/Directories: kebab-case

## 🛠️ Project-Specific Commands (from CLAUDE.md)

**Command to start the optimized scraper:**
```bash
python server-upgraded.py
```

### Standard Commands (from Global.md)
```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "lint": "eslint . --ext .ts,.tsx",
  "format": "prettier --write .",
  "test": "vitest run",
  "test:watch": "vitest watch",
  "type-check": "tsc --noEmit"
}
```

## 🧩 Project Modules (from CLAUDE.md)

1. **Login Module**  
   - Authenticates via username, password, security code  

2. **Case Access Module**  
   - Prompts for Case ID after successful login  

3. **Case Information Module**  
   - Extracts client name, lien holder name, repo type  

4. **Repo Fee Module**  
   - Looks up repo fees based on case metadata  
   - Uses fallback standard fee when needed

5. **My Summary Fees Module**  
   - Extracts all fee-type items from My Summary tab  

6. **Updates Fees Module**  
   - Parses narrative content to extract fee mentions  

7. **Fee Matching Module**  
   - Matches both repo and pre-approved non-repo fees  
   - Uses predefined whitelist for non-repo fee types  

8. **Other Fees Module**  
   - Tracks unmatched fees for auditing  

9. **Output Module**  
   - Generates reports and data files  

## 🧠 Integration with Claude (from Global.md)

### Interaction Rules
- Respect CLAUDE.md as the primary reference
- Use project context (e.g., configs) before generating code
- Never expose or suggest sharing secrets

### Behavioral Guidelines
| Scenario           | Claude's Behavior                               |
|--------------------|------------------------------------------------|
| Project Setup      | Use boilerplate and structure from CLAUDE.md    |
| Code Review        | Suggest changes based on coding standards       |
| Security           | Audit and recommend secure practices            |
| Docs               | Follow markdown and repo etiquette              |
| Conflicting        | Ask for clarification and flag deviation        |

## 🔐 Security Practices (from Global.md)

- **Credentials**: .env files only, never commit secrets
- **Dependencies**: Audit via npm audit, pip-audit
- **Access Control**: Role-based permissions, principle of least privilege

## 📚 Database Schema (Project-Specific)

### Tables and Columns
- **FeeDetails2**: fd_id, client_id, lh_id, ft_id, amount
- **RDN_Client**: id, client_name
- **Lienholder**: id, lienholder_name
- **FeeType**: id, fee_type_name
- **LienholderFeeType**: id, lienholder_id, fee_type_id

### Relationships
- FeeDetails2.client_id → RDN_Client.id
- FeeDetails2.lh_id → Lienholder.id
- FeeDetails2.ft_id → FeeType.id
- LienholderFeeType.lienholder_id → Lienholder.id
- LienholderFeeType.fee_type_id → FeeType.id

## 🔧 Common Issues & Solutions (from CLAUDE.md)

1. **Socket.IO Connection Problems**
   - Use CDN-hosted client: `<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>`
   - Configure with polling transport: `transports: ['polling', 'websocket']`

2. **Missing CSS & JS Files**
   - Set `static_url_path=''` in Flask app initialization
   - Check relative paths in HTML files

3. **Browser Automation Failures**
   - Use headless mode: `config["browser"]["headless"] = True`
   - Increase timeouts: `config["browser"]["default_timeout"] = 600000`

4. **Thread Management**
   - Use `async_mode='threading'` with Flask-SocketIO
   - Make threads daemon: `scrape_thread.daemon = True`

## 📊 Technologies Used

- **Web Framework & Server**:
  - Flask
  - Flask-SocketIO
  - Socket.IO

- **Database**:
  - Microsoft SQL Server/Azure SQL (via pyodbc)
  - ODBC Driver 17 for SQL Server

- **Browser Automation**:
  - Selenium WebDriver
  - Chrome browser

- **Python Libraries**:
  - Threading
  - JSON
  - Regular expressions
  - Type hints
  - Logging

- **Frontend**:
  - HTML/CSS
  - JavaScript
  - Socket.IO client
  - Bootstrap

- **Data Processing**:
  - Custom fee extraction algorithms
  - Fee categorization logic
  - Data normalization routines