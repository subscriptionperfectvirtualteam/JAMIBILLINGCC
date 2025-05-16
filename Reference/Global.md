1. Coding Standards
Preferred Languages & Versions
JavaScript: ES2022+
 
TypeScript: 5.x (strict mode enforced)
 
Python: 3.11+
 
HTML/CSS: Semantic HTML5, CSS Grid & Flexbox
 
React: v18+ (functional components + hooks only)
 
Node.js: LTS (20.x preferred); use ECMAScript Modules (ESM)
 
Style Guides
JavaScript/React: Airbnb JavaScript Style Guide
 
TypeScript: Airbnb + @typescript-eslint rules
 
Python: PEP8
 
HTML/CSS: Google HTML/CSS Style Guide
 
Markdown: CommonMark, linted with markdownlint
 
Formatting Tools
Prettier for JavaScript/TypeScript/Markdown/CSS
 
Black for Python
 
markdownlint, Stylelint, EditorConfig
 
2. Naming Conventions & Best Practices
General Guidelines
Descriptive, unambiguous names; no unnecessary abbreviations
 
Variables, Functions, Classes
camelCase for variables/functions
 
PascalCase for components/classes
 
UPPER_SNAKE_CASE for constants
 
Files & Directories
kebab-case for filenames
 
Feature-based file grouping
 
3. Common Commands
Scripts 
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "lint": "eslint . --ext .ts,.tsx",
  "format": "prettier --write .",
  "test": "vitest run",
  "test:watch": "vitest watch",
  "type-check": "tsc --noEmit"
}
Aliases
bash 
alias dev="npm run dev"
alias b="npm run build"
alias lint="npm run lint"
Setup
bash 
nvm use
npm install
cp .env.example .env
npm run dev
4. Tooling Preferences
Editors & IDEs
VSCode, Cursor AI, JetBrains IDEs
 
Terminal
iTerm2, zsh + Oh My Zsh, themes like Dracula, Gruvbox
 
Version Control
Git + GitHub
 
Feature branches
 
Commit messages using Conventional Commits
 
Squash and merge strategy
 
5. Testing Guidelines
Frameworks
Vitest, React Testing Library, Cypress, pytest, coverage.py
 
Coverage Requirements
90%+ lines/statements
 
Enforced in CI
 
CI/CD
GitHub Actions or CircleCI
 
Tests, linting, coverage checks in PR workflows
 
6. Repository Etiquette
Branch Naming
feature/, bugfix/, hotfix/, chore/, docs/
 
Commits
Use Conventional Commits (e.g., feat(auth): add login feature)
 
Pull Requests
Linked issues, screenshots, descriptive summaries
 
At least 1 approval, squash merge
 
7. Security Practices
Credentials
.env files only, never commit secrets
 
Use secrets managers
 
Dependencies
Audit via npm audit, snyk, pip-audit
 
Access Control
Role-based GitHub permissions
 
PoLP for cloud and CI access
 
8. Project Initialization
Setup Steps
Use Vite, Express, or FastAPI templates
 
Standard .eslintrc, .prettierrc, .env.example, etc.
 
Directory Structures
Feature-based, modular, colocated test files
 
Boilerplate Files
Preconfigured README, scripts, and linting rules
 
9. Integration with Claude
Interaction Rules
Respect CLAUDE.md as the primary reference
 
Use project context (e.g., configs) before generating code
 
Never expose or suggest sharing secrets
 
Example Prompts 
"Generate a React component using project standards"
"Review and refactor this file for clarity and performance"
Behavioral Guidelines
Scenario	Claude’s Behavior
Project Setup	Use boilerplate and structure from CLAUDE.md
Code Review	Suggest changes based on coding standards
Security	Audit and recommend secure practices
Docs	Follow markdown and repo etiquette
Conflicting Instructions	Ask for clarification and flag deviation
 