# RDN Fee Scraper - Project Overview

## 🧠 Purpose

Automate the extraction, classification, and display of fee-related data from the Recovery Database Network (RDN), using optimized scraping and database-backed enrichment for case review.

---

## 🧩 Modules

### 1. Authentication & Session
- Logs into RDN using user credentials.
- Maintains session for navigation and scraping.

### 2. Case Navigator
- Accepts Case ID post-login.
- Navigates directly to the RDN case page.

### 3. Metadata Extractor
- Extracts:
  - Client Name
  - Lien Holder
  - Repo Type
  - Involuntary Repo Fee (from DB if available)

### 4. Fee Extractors
#### ➤ My Summary Tab:
- Fee label, amount, approval status, and notes.

#### ➤ Updates Tab:
- Parses narratives using regex to identify fees.

### 5. Fee Classifier
- Matches to:
  - Pre-approved Non-Repo Fee Whitelist
  - Repo Fee Matrix
- Unmatched entries go to “Other Fees”

### 6. Output Renderer
- Fee summaries shown by tab (My Summary, Updates)
- Cards for metadata and DB-derived fee
- HTML and JSON report outputs

---

## 🚀 Performance Enhancements

| Feature | Optimization |
|--------|--------------|
| JavaScript scraping | Direct DOM queries |
| Timing logs | Timestamped section-wise timers |
| Fee Parsing | Pre-compiled regex, capped iteration |
| Updates tab | Async load and limit scope |

---

## 🧾 Pre-approved Non-Repo Fee Whitelist

```text
Field Visit, Flatbed Fees, Dolly Fees, Mileage/ Fuel, Incentive,
Frontend (for Impound), LPR Invoulantry Repo, Finder's fee,
CR AND PHOTOS FEE, Fuel Surcharge, LPR REPOSSESSION, OTHER,
SKIP REPOSSESSION, Bonus, Keys Fee
