# RDN Fee Extraction Keywords Reference

This document outlines the keywords and phrases used to identify, classify, and extract fee-related information from the RDN platform. These can be used for both structured and unstructured data scraping.

---

## 🔑 General Fee-Related Keywords

These keywords signal the presence of a fee or financial transaction:
- Fee
- Charge
- Cost
- Amount
- Payment
- Billed
- Expense
- Rate
- Deducted

---

## 💵 Specific Fee Types

### Storage & Lot Fees
- Storage Fee
- Daily Storage
- Impound Fee
- Lot Fee

### Repossession & Recovery Fees
- Repo Fee
- Recovery Fee
- Tow Fee
- Involuntary Repo
- Voluntary Repo
- Close Fee
- Hook Fee
- Repossession Charge

### Transport & Delivery Fees
- Transport Fee
- Delivery Fee
- Tow-In Charge
- Relocation Fee

### Administrative & Processing Fees
- Admin Fee
- Office Fee
- Processing Fee
- Key Fee
- Title Fee
- Mail Fee
- Redemption Admin Fee

### Agent & Labor Fees
- Agent Fee
- Labor Charge
- Field Visit Fee
- Drive Charge
- Attempt Fee
- Service Charge

### Inspection & Condition Fees
- Condition Report
- Vehicle Condition Fee
- Photos / Photo Fee
- Inspection Fee

### Compliance & Legal Fees
- Personal Property Fee
- Letter Fee
- Notification Fee
- Legal Fee
- Compliance Fee

---

## 🧠 Optional Tags for Fee Status

These are helpful for identifying payment status or decision-making logic:
- Paid
- Not Paid
- Approved
- Pending
- Denied
- Waived

---
## Pre-approved Non-Repo Fee Whitelist

The following fee types are considered pre-approved non-repo fees:
- Field Visit
- Flatbed Fees
- Dolly Fees
- Mileage/ Fuel
- Incentive
- Frontend (for Impound)
- LPR Invoulantry Repo
- Finder's fee
- CR AND PHOTOS FEE
- Fuel Surcharge
- LPR REPOSSESSION
- OTHER
- SKIP REPOSSESSION
- Bonus
- Keys Fee
## 🔍 Parsing Recommendations

To extract fees from RDN pages (e.g., "Updates" tab, summary tables), consider the following:

- Match currency patterns:
  - `$75 storage`
  - `paid $150 for repo`
- Match labeled patterns:
  - `storage fee: 75`
  - `charged 40 for keys`
- Normalize synonyms:
  - `"hook fee"` → `"repo fee"`

---

## 📦 Usage Suggestions

- Use keyword matching for structured fields (e.g., table labels).
- Use regex + NLP for parsing free-text fields like updates or notes.
- Use these keywords to classify into categories (e.g., transport, storage, labor).
