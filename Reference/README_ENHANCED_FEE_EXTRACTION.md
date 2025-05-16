# Enhanced Fee Extraction

This document describes the comprehensive improvements made to the fee extraction functionality in the RDN Fee Scraper application, based on the analysis of sample HTML files (samplev2-samplev7).

## Overview

The enhanced fee extraction adds support for:

1. Variable spacing after dollar signs (0-3 spaces)
2. Context-aware fee type detection
3. New specialized patterns for common fee formats
4. HTML structure-aware extraction for better accuracy

## Key Improvements

### 1. Dollar Amount Spacing Handling

The original extraction had issues with spaces after the $ symbol. We've enhanced all regex patterns to handle 0-3 spaces after the dollar sign:

```python
# Original pattern
r'\$\s*([0-9,]+(?:\.\d{1,2})?)'

# Enhanced pattern
r'\$\s{0,3}([0-9,]+(?:\.\d{1,2})?)'
```

### 2. Specialized Patterns

Based on analysis of the sample files, we've added specialized patterns for common fee formats:

```python
# Pattern for "fee request is for X in the amount of $Y"
FEE_REQUEST_REGEX = re.compile(r'fee\s+request\s+is\s+for\s+(.*?)\s+in\s+the\s+amount\s+of\s+\$\s{0,3}([0-9,.]+)', re.IGNORECASE)

# Pattern for storage fees with specific pricing structure
STORAGE_FEE_REGEX = re.compile(r'storage.*?\$\s{0,3}([0-9,.]+)(?:\s+per\s+day|\s+max)', re.IGNORECASE)

# Pattern for update-text-black class that often contains fee information
UPDATE_TEXT_REGEX = re.compile(r'<dd\s+class=["\']update-text-black["\'][^>]*id=["\'][^"\']+?["\']>(.*?)</dd>', re.DOTALL)
```

### 3. Context-Aware Fee Type Detection

The enhanced extraction now determines fee types from surrounding text:

```python
# Try to determine fee type from surrounding text
if 'flatbed' in details.lower():
    fee_type = "Flatbed Fees"
elif any(key_term in details.lower() for key_term in ['key', 'keys', 'computer key']):
    fee_type = "Keys Fee"
elif 'storage' in details.lower():
    fee_type = "Storage Fee"
```

### 4. JavaScript-Side Improvements

The JavaScript extraction code has been enhanced with the same patterns for browser-side extraction:

```javascript
// Check for specific "fee request is for X in the amount of $Y" pattern first
const feeRequestRegex = /fee\s+request\s+is\s+for\s+(.*?)\s+in\s+the\s+amount\s+of\s+\$\s{0,3}([0-9,.]+)/i;

// Function to determine fee type from content
function determineFeeType(text) {
    const lowerText = text.toLowerCase();
    if (lowerText.includes('flatbed') || lowerText.includes('dolly')) {
        return "Flatbed Fees";
    } else if (lowerText.includes('key') || lowerText.includes('computer')) {
        return "Keys Fee";
    } else if (lowerText.includes('storage')) {
        return "Storage Fee";
    }
    return "Unknown Fee";
}
```

## Files Created

1. `enhanced_fee_extraction.py` - Contains all the improved extraction patterns and functions
2. `test_enhanced_extraction.py` - Test script for the enhanced extraction on sample files
3. `integrate_fee_extraction_enhancements.py` - Script to integrate the improvements into the server code

## How to Use

### Testing the Enhanced Extraction

Test the enhanced extraction on the sample files:

```bash
python3 test_enhanced_extraction.py
```

This will analyze all samplev*.txt files and output the results to `enhanced_extraction_results.json`.

### Integrating the Enhancements

To integrate the enhancements into the server code:

```bash
# Apply to the main server file (creates a backup)
python3 integrate_fee_extraction_enhancements.py --server-file server-upgradedv2.py

# Apply to create a new server file
python3 integrate_fee_extraction_enhancements.py --server-file server-upgradedv2.py --output-file server-upgradedv3.py

# Apply without creating a backup (not recommended)
python3 integrate_fee_extraction_enhancements.py --server-file server-upgradedv2.py --no-backup
```

## Test Results

The enhanced extraction correctly identifies fees in all sample files:

1. **samplev2.txt**: Key Fee $250.00
2. **samplev3.txt**: Key Fee $250.00
3. **samplev4.txt**: Storage Fee $10
4. **samplev5.txt**: Flatbed Fees $110.00
5. **samplev6.txt**: Computer Keys Fee $250.00
6. **samplev7.txt**: Keys Fee $250.00

## Summary of Improvements

1. Correctly handles variable spacing after dollar signs (0-3 spaces)
2. Identifies specialized fee formats with high confidence
3. Determines fee types from context
4. Works with different HTML structures across all sample files
5. Provides more detailed fee information including fee types and confidence levels

All these improvements have been implemented while preserving the existing functionality, ensuring backward compatibility with the current system.