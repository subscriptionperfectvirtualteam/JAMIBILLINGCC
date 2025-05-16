# CLAUDE: Cloud-Level Fee Extraction and Presentation Logic

## 🧠 Objective
Extract, classify, and present fees from RDN case pages by applying structured logic for categorization, deduplication, and UI output.

---

## 🧩 Data Sources
- **Updates**: Parsed from `<div class="details">...</div>` blocks.
- **My Summary**: Parsed from My Summary screen content.
- **Database**: Static fees based on repossession type.

---

## 🛠️ Fee Classification Rules

### ✅ Source Display Normalization
- Always rename `"Case Page"` source to `"Updates"`.
- Only allow two source labels:
  - `"My Summary"`
  - `"Updates"`

---

## 📊 Fee Tables Structure

### 📌 Table 1: Predefined Categories
- Show only fees where the category matches one of the following:

Field Visit
Flatbed Fees
Dolly Fees
Mileage/ Fuel
Incentive
Frontend (for Impound)
LPR Invoulantry Repo
Finder's fee
CR AND PHOTOS FEE
Fuel Surcharge
LPR REPOSSESSION
OTHER
SKIP REPOSSESSION
Bonus

yaml
Copy
Edit

- Exclude database-derived and "Keys Fee".
- Source: `My Summary` or `Updates`.

---

### 📌 Table 2: Keys Fees
- Always include all `"Keys Fee"` entries here.
- Even if the category matches predefined, it must appear in this separate table.
- Styled with yellow background.

---

### 📌 Table 3: Other Categories
- Show fees where the **category is not in the predefined list** above.
- Use the **actual scraped category name**, like:
- `"Holding Fee"`
- `"Impound Storage"`
- `"Towing Fee"`
- Also styled with yellow background to show it’s a non-standard fee.

---

## 💡 Reference Sentence Handling
- Extract **entire sentence** from the `<div class="details">` block in the update section.
- Do not truncate or cut off mid-paragraph.
- Preserve full context such as:
A new fee request has been submitted... Flatbed Fee in the amount of $150.00

yaml
Copy
Edit

---

## 🔁 Deduplication Logic
- Use priority ordering:
1. Database
2. My Summary
3. Updates
- Normalize category and reference sentence before comparison.

```python
def deduplicate(fees):
  seen = set()
  unique = []
  for fee in sorted(fees, key=lambda f: priority_map[f["source"]]):
      key = (fee["amount"], normalize(fee["category"]), normalize(fee["reference"]))
      if key not in seen:
          seen.add(key)
          unique.append(fee)
  return unique
💳 Database Fee Display
If repo type is Involuntary, display:

html
Copy
Edit
<div class="card info-card">
  <h4>{{Fee Type Extracted from web}}</h4>
  <p>$385.00</p>
</div>
Never show this in the above fee tables.

🧾 Output Files
JSON Exports
raw_updates.json: All update entries.

summary_fees.json: All My Summary entries.

fee_table.json: Final classified fee output (predefined + keys + others).

HTML Report
Renders:

Table 1: Predefined Fees

Table 2: Keys Fee Table (yellow)

Table 3: Other Categories Table (yellow)

Repo Fee Card (if applicable)

✅ UI Rules
Field	Rule
Category	Use scraped name unless in Table 1
Table Split	Table 1: Predefined, Table 2: Keys, Table 3: Others
Styling	Yellow background for Tables 2 and 3
Reference	Full sentence from <div class="details">
Source	"My Summary" or "Updates" only

✅ Summary
🟢 Table 1: Only whitelist categories

🟡 Table 2: All "Keys Fee"

🟡 Table 3: All non-whitelist categories with original names

🔁 Deduplicate with source priority

💬 Use full detail sentence as reference

📦 Show database repo fee in a card

eparate Tables per Fee Category (Dynamic Table Generation)
Purpose:
Improve fee visibility by creating individual tables for each fee category that is not part of the predefined whitelist.

✅ Logic
Maintain a whitelist of standard categories:

arduino
Copy
Edit
[
  "Field Visit",
  "Flatbed Fees",
  "Dolly Fees",
  "Mileage/ Fuel",
  "Incentive",
  "Frontend (for Impound)",
  "LPR Invoulantry Repo",
  "Finder's fee",
  "CR AND PHOTOS FEE",
  "Fuel Surcharge",
  "LPR REPOSSESSION",
  "OTHER",
  "SKIP REPOSSESSION",
  "Bonus",
  "Keys Fee"
]
During fee processing:

If a fee category is not in the whitelist, classify it as Other.

For each unique Other category (e.g., "Holding Fee", "Towing", "Admin"):

Create a separate table in the output UI.

Table title format: Other Fee - [Category Name].

🖥️ UI Output Structure
For each Other category:

html
Copy
Edit
<h3>Other Fee - Holding Fee</h3>
<table>
  <thead>
    <tr>
      <th>Date</th>
      <th>Category</th>
      <th>Amount</th>
      <th>Status</th>
      <th>Source</th>
      <th>Reference Sentence</th>
    </tr>
  </thead>
  <tbody>
    <!-- List all entries for "Holding Fee" -->
  </tbody>
</table>
Repeat this structure for each additional category like "Towing", "Admin Fee", etc.

🧠 Considerations
Grouping is case-insensitive (holding fee, Holding Fee, HOLDING FEE → same group).

Use sanitized versions of category names for HTML element IDs if needed (e.g., replacing spaces with hyphens).

Ensure the reference sentence is complete and pulled from the "Details" section of the HTML case page.



 






