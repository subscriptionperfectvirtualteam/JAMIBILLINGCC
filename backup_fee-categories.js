/**
 * Fee Categories and Keywords for JamiBilling App
 * This file contains mappings for identifying fee types based on text content
 */

const feeCategories = {
    // Storage & Lot Fees category
    "Storage": {
        keywords: [
            "storage fee", "daily storage", "impound fee", "lot fee"
        ],
        color: "#4e73df"  // Blue
    },
    
    // Repossession & Recovery Fees category
    "Repossession": {
        keywords: [
            "repo fee", "recovery fee", "tow fee", "involuntary repo", 
            "voluntary repo", "close fee", "hook fee", "repossession charge"
        ],
        color: "#e74a3b"  // Red
    },
    
    // Transport & Delivery Fees category
    "Transport": {
        keywords: [
            "transport fee", "delivery fee", "tow-in charge", "relocation fee",
            "flatbed fee", "dolly fee", "mileage", "fuel", "fuel surcharge"
        ],
        color: "#1cc88a"  // Green
    },
    
    // Administrative & Processing Fees category
    "Administrative": {
        keywords: [
            "admin fee", "office fee", "processing fee", "key fee", "keys fee",
            "title fee", "mail fee", "redemption admin fee", "frontend"
        ],
        color: "#f6c23e"  // Yellow
    },
    
    // Agent & Labor Fees category
    "Agent": {
        keywords: [
            "agent fee", "labor charge", "field visit", "field visit fee", 
            "drive charge", "attempt fee", "service charge", "finder's fee",
            "bonus", "incentive"
        ],
        color: "#36b9cc"  // Light Blue
    },
    
    // Inspection & Condition Fees category
    "Inspection": {
        keywords: [
            "condition report", "vehicle condition fee", "photo", "photos", 
            "photo fee", "inspection fee", "cr and photos fee"
        ],
        color: "#6f42c1"  // Purple
    },
    
    // Compliance & Legal Fees category
    "Compliance": {
        keywords: [
            "personal property fee", "letter fee", "notification fee",
            "legal fee", "compliance fee"
        ],
        color: "#fd7e14"  // Orange
    },
    
    // Other/Miscellaneous Fees category
    "Other": {
        keywords: [
            "other", "lpr", "lpr involuntary repo", "lpr repossession", 
            "skip repossession"
        ],
        color: "#858796"  // Gray
    }
};

// Fee status keywords
const feeStatusKeywords = {
    "Paid": ["paid", "payment received", "payment complete"],
    "Not Paid": ["not paid", "unpaid", "payment pending"],
    "Approved": ["approved", "accepted", "authorized"],
    "Pending": ["pending", "awaiting", "in process"],
    "Denied": ["denied", "rejected", "declined"],
    "Waived": ["waived", "forgiven", "no charge"]
};

// General fee indicator keywords
const feeIndicatorKeywords = [
    "fee", "charge", "cost", "amount", "payment", "billed", "expense", "rate", "deducted"
];

/**
 * Determine the most likely fee category based on the description text
 * @param {string} description - The text to analyze
 * @return {object} - The detected category and confidence level
 */
function detectFeeCategory(description) {
    if (!description) return { category: "Unknown", confidence: 0 };
    
    const text = description.toLowerCase();
    let highestScore = 0;
    let detectedCategory = "Unknown";
    
    // Check each category's keywords against the text
    for (const [category, data] of Object.entries(feeCategories)) {
        for (const keyword of data.keywords) {
            if (text.includes(keyword.toLowerCase())) {
                // Found an exact match
                return { 
                    category: category, 
                    confidence: 1, 
                    color: data.color 
                };
            }
        }
        
        // No exact match, try partial matching with score
        let score = 0;
        for (const keyword of data.keywords) {
            const keywordParts = keyword.toLowerCase().split(" ");
            for (const part of keywordParts) {
                if (part.length > 3 && text.includes(part)) {
                    score += 0.5;
                }
            }
        }
        
        if (score > highestScore) {
            highestScore = score;
            detectedCategory = category;
        }
    }
    
    if (highestScore > 0) {
        return { 
            category: detectedCategory, 
            confidence: Math.min(highestScore, 0.9), // Cap at 0.9 for partial matches
            color: feeCategories[detectedCategory]?.color || "#858796"
        };
    }
    
    return { category: "Unknown", confidence: 0, color: "#858796" };
}

/**
 * Determine fee status based on the description text
 * @param {string} description - The text to analyze
 * @return {string} - The detected status
 */
function detectFeeStatus(description) {
    if (!description) return "Unknown";
    
    const text = description.toLowerCase();
    
    for (const [status, keywords] of Object.entries(feeStatusKeywords)) {
        for (const keyword of keywords) {
            if (text.includes(keyword.toLowerCase())) {
                return status;
            }
        }
    }
    
    return "Unknown";
}

/**
 * Extract potential fee amounts from text
 * @param {string} text - The text to analyze
 * @return {Array} - Array of extracted fee objects with amount and description
 */
function extractFeeAmounts(text) {
    if (!text) return [];
    
    const fees = [];
    const dollarAmountRegex = /\$(\d{1,3}(,\d{3})*(\.\d{2})?)/g;
    const match = text.match(dollarAmountRegex);
    
    if (match) {
        for (const amountStr of match) {
            const amount = amountStr.replace(/[$,]/g, '');
            const nearbyText = extractNearbyText(text, amountStr, 50);
            const categoryInfo = detectFeeCategory(nearbyText);
            const status = detectFeeStatus(nearbyText);
            
            fees.push({
                amount: parseFloat(amount),
                amountStr: amountStr,
                description: nearbyText.trim(),
                category: categoryInfo.category,
                categoryColor: categoryInfo.color,
                status: status
            });
        }
    }
    
    return fees;
}

/**
 * Extract text surrounding a target string
 * @param {string} fullText - The complete text
 * @param {string} targetText - The text to search for
 * @param {number} charCount - Number of characters to extract on each side
 * @return {string} - The extracted nearby text
 */
function extractNearbyText(fullText, targetText, charCount) {
    const index = fullText.indexOf(targetText);
    if (index === -1) return '';
    
    const start = Math.max(0, index - charCount);
    const end = Math.min(fullText.length, index + targetText.length + charCount);
    
    return fullText.substring(start, end);
}

/**
 * Check if text contains any fee indicator keywords
 * @param {string} text - The text to check
 * @return {boolean} - True if the text contains fee indicators
 */
function containsFeeIndicators(text) {
    if (!text) return false;
    
    const lowerText = text.toLowerCase();
    return feeIndicatorKeywords.some(keyword => lowerText.includes(keyword));
}
