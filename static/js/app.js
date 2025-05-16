/**
 * JamiBilling - RDN Fee Scraper
 * Main application script
 */

// DOM Elements
const loginSection = document.getElementById('login-section');
const processSection = document.getElementById('process-section');
const resultsSection = document.getElementById('results-section');
const loginForm = document.getElementById('login-form');
const progressFill = document.getElementById('progress-fill');
const statusMessage = document.getElementById('status-message');
const cancelProcessBtn = document.getElementById('cancel-process');
const exportPdfBtn = document.getElementById('export-pdf');
const exportExcelBtn = document.getElementById('export-excel');
const newSearchBtn = document.getElementById('new-search');
const resultCaseId = document.getElementById('result-case-id');

// Process steps elements
const steps = [
    document.getElementById('step-login'),
    document.getElementById('step-case'),
    document.getElementById('step-database'),
    document.getElementById('step-updates'),
    document.getElementById('step-complete')
];

// Application state
const appState = {
    currentSection: 'login',
    currentStep: 0,
    processing: false,
    caseData: null,
    dbData: null,
    updates: []
};

// Initialize the application
function initApp() {
    // Add event listeners
    loginForm.addEventListener('submit', handleLoginSubmit);
    cancelProcessBtn.addEventListener('click', cancelProcess);
    exportPdfBtn.addEventListener('click', exportToPdf);
    exportExcelBtn.addEventListener('click', exportToExcel);
    newSearchBtn.addEventListener('click', startNewSearch);
    
    // Set initial UI state
    showSection('login');
}

// Handle login form submission
async function handleLoginSubmit(event) {
    event.preventDefault();
    
    // Get form values
    const formData = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        securityCode: document.getElementById('security-code').value,
        caseId: document.getElementById('case-id').value
    };
    
    // Validate input
    if (!formData.username || !formData.password || !formData.securityCode || !formData.caseId) {
        alert('Please fill in all required fields');
        return;
    }
    
    // Start processing
    appState.processing = true;
    showSection('process');
    startProcessing(formData);
}

// Process the data extraction workflow
async function startProcessing(formData) {
    try {
        // Reset state
        appState.currentStep = 0;
        
        // Update progress indicators
        updateProgress(0);
        updateStatus('Starting login process...');
        
        // Step 1: Login to RDN
        updateStep(0);
        const loginSuccess = await loginToRdn(formData);
        if (!loginSuccess) throw new Error('Login failed');
        updateProgress(20);
        
        // Step 2: Extract case data
        updateStep(1);
        updateStatus('Accessing case information...');
        appState.caseData = await extractCaseData();
        updateProgress(40);
        
        // Step 3: Query database
        updateStep(2);
        updateStatus('Querying database for fee information...');
        appState.dbData = await queryDatabase();
        updateProgress(60);
        
        // Step 4: Extract updates
        updateStep(3);
        updateStatus('Extracting updates and fee history...');
        appState.updates = await extractUpdates();
        updateProgress(80);
        
        // Step 5: Complete
        updateStep(4);
        updateStatus('Processing complete!');
        updateProgress(100);
        
        // Display results
        setTimeout(() => {
            displayResults();
            showSection('results');
            appState.processing = false;
        }, 1000);
    } catch (error) {
        console.error('Processing error:', error);
        updateStatus(`Error: ${error.message}`);
        
        // Allow retry or cancel
        if (confirm('An error occurred during processing. Would you like to try again?')) {
            startProcessing(formData);
        } else {
            cancelProcess();
        }
    }
}

// Login to RDN via API
async function loginToRdn(formData) {
    updateStatus('Logging in to RDN...');
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateStatus('Login successful!');
            return true;
        } else {
            updateStatus(`Login failed: ${data.message}`);
            throw new Error(data.message);
        }
    } catch (error) {
        updateStatus(`Login error: ${error.message}`);
        throw error;
    }
}

// Extract case data via API
async function extractCaseData() {
    updateStatus('Retrieving case information...');
    
    try {
        const response = await fetch('/api/case-data');
        const data = await response.json();
        
        if (data.success) {
            updateStatus('Case information retrieved successfully!');
            return data.data;
        } else {
            updateStatus(`Failed to retrieve case data: ${data.message}`);
            throw new Error(data.message);
        }
    } catch (error) {
        updateStatus(`Case data error: ${error.message}`);
        throw error;
    }
}

// Query database via API
async function queryDatabase() {
    updateStatus('Connecting to database...');
    
    try {
        const response = await fetch('/api/query-database');
        const data = await response.json();
        
        if (data.success) {
            updateStatus('Database query complete!');
            if (data.warning) {
                console.warn(data.warning);
                updateStatus(`Database query complete with warning: ${data.warning}`);
            }
            return data.data;
        } else {
            updateStatus(`Database query failed: ${data.message}`);
            throw new Error(data.message);
        }
    } catch (error) {
        updateStatus(`Database error: ${error.message}`);
        throw error;
    }
}

// Extract updates via API
async function extractUpdates() {
    updateStatus('Retrieving updates and fee history...');
    
    try {
        const response = await fetch('/api/updates');
        const data = await response.json();
        
        if (data.success) {
            updateStatus('Updates retrieved successfully!');
            return data.data;
        } else {
            updateStatus(`Failed to retrieve updates: ${data.message}`);
            throw new Error(data.message);
        }
    } catch (error) {
        updateStatus(`Updates error: ${error.message}`);
        throw error;
    }
}

// Display the results in the UI
function displayResults() {
    // Set case ID in the header
    resultCaseId.textContent = appState.caseData.caseId;
    
    // Populate client information
    document.getElementById('client-name').textContent = appState.caseData.clientName;
    document.getElementById('lienholder-name').textContent = appState.caseData.lienHolder;
    document.getElementById('order-to').textContent = appState.caseData.orderTo;
    
    // Populate database information
    document.getElementById('fee-id').textContent = appState.dbData.fdId;
    document.getElementById('db-client-name').textContent = appState.dbData.clientName;
    document.getElementById('db-lienholder-name').textContent = appState.dbData.lienholderName;
    document.getElementById('fee-type-name').textContent = appState.dbData.feeTypeName;
    document.getElementById('db-amount').textContent = `$${appState.dbData.amount.toFixed(2)}`;
    
    // Populate fees table
    const feesTableBody = document.querySelector('#fees-table tbody');
    feesTableBody.innerHTML = ''; // Clear existing data
    
    // Filter out fees with zero amounts
    const nonZeroFees = appState.caseData.fees.filter(fee => {
        const amount = parseFloat(fee.amount) || 0;
        return amount > 0;
    });
    
    nonZeroFees.forEach(fee => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${fee.description}</td>
            <td><span class="category-tag" style="background-color: ${fee.categoryColor}">${fee.category}</span></td>
            <td>${fee.amountStr}</td>
            <td>${fee.status}</td>
        `;
        feesTableBody.appendChild(row);
    });
    
    // Populate updates table
    const updatesTableBody = document.querySelector('#updates-table tbody');
    updatesTableBody.innerHTML = ''; // Clear existing data
    
    // Filter updates with dollar amounts in the details text
    const updatesWithDollarAmounts = appState.updates.filter(update => {
        // Check if amount field has a non-zero value
        const amount = parseFloat(update.amount) || 0;
        if (amount > 0) return true;
        
        // If amount field doesn't have a value, check the details text for dollar amounts
        if (update.details) {
            // Look for dollar amount pattern in details
            const dollarPattern = /\$\s*([0-9,]+(\.[0-9]{2})?)/;
            const match = update.details.match(dollarPattern);
            if (match) {
                // If there's a dollar amount in the details, extract and save it
                const extractedAmount = parseFloat(match[1].replace(',', ''));
                if (extractedAmount > 0) {
                    // If we found a valid amount in the text but it wasn't in the amount field,
                    // we'll update the display value
                    update.amountStr = match[0]; // Use the full match including $ sign
                    update.amount = extractedAmount;
                    return true;
                }
            }
        }
        
        return false;
    });
    
    updatesWithDollarAmounts.forEach(update => {
        let feeTypeDisplay = update.feeType;
        
        if (update.feeType !== 'N/A') {
            // Find color for this fee type
            const categoryColor = getCategoryColor(update.feeType);
            feeTypeDisplay = `<span class="category-tag" style="background-color: ${categoryColor}">${update.feeType}</span>`;
        }
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${update.date}</td>
            <td>${update.details}</td>
            <td>${update.feeType !== 'N/A' ? feeTypeDisplay : 'N/A'}</td>
            <td>${update.amountStr}</td>
        `;
        updatesTableBody.appendChild(row);
    });
    
    // Add category tag styles if not already added
    if (!document.getElementById('category-tag-style')) {
        const style = document.createElement('style');
        style.id = 'category-tag-style';
        style.textContent = `
            .category-tag {
                display: inline-block;
                padding: 0.25rem 0.5rem;
                border-radius: 0.25rem;
                color: white;
                font-size: 0.75rem;
                font-weight: 600;
            }
        `;
        document.head.appendChild(style);
    }
}

// Helper function to get category color
function getCategoryColor(category) {
    const categoryColors = {
        'Storage': '#4e73df',
        'Repossession': '#e74a3b',
        'Transport': '#1cc88a',
        'Administrative': '#f6c23e',
        'Agent': '#36b9cc',
        'Inspection': '#6f42c1',
        'Compliance': '#fd7e14',
        'Other': '#858796',
        'Unknown': '#858796'
    };
    
    return categoryColors[category] || '#858796';
}

// Export results to PDF
function exportToPdf() {
    const { jsPDF } = window.jspdf;
    
    try {
        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.getWidth();
        
        // Add title
        doc.setFontSize(18);
        doc.setTextColor(44, 123, 229);
        doc.text(`JamiBilling - Case #${appState.caseData.caseId}`, pageWidth / 2, 15, { align: 'center' });
        
        // Add client information
        doc.setFontSize(14);
        doc.setTextColor(0, 0, 0);
        doc.text('Client Information', 15, 30);
        
        doc.setFontSize(10);
        doc.text(`Client Name: ${appState.caseData.clientName}`, 20, 40);
        doc.text(`Lien Holder: ${appState.caseData.lienHolder}`, 20, 45);
        doc.text(`Order To: ${appState.caseData.orderTo}`, 20, 50);
        
        // Add database information
        doc.setFontSize(14);
        doc.text('Database Information', pageWidth / 2 + 15, 30);
        
        doc.setFontSize(10);
        doc.text(`Fee ID: ${appState.dbData.fdId}`, pageWidth / 2 + 20, 40);
        doc.text(`Fee Type: ${appState.dbData.feeTypeName}`, pageWidth / 2 + 20, 45);
        doc.text(`Amount: $${appState.dbData.amount.toFixed(2)}`, pageWidth / 2 + 20, 50);
        
        // Add fees table
        doc.setFontSize(14);
        doc.text('Fees Summary', 15, 70);
        
        // Table headers
        doc.setFontSize(10);
        doc.setTextColor(100, 100, 100);
        doc.text('Description', 20, 80);
        doc.text('Category', 80, 80);
        doc.text('Amount', 130, 80);
        doc.text('Status', 165, 80);
        
        // Table rows
        doc.setTextColor(0, 0, 0);
        let yPos = 85;
        
        // Filter out fees with zero amounts
        const nonZeroFees = appState.caseData.fees.filter(fee => {
            const amount = parseFloat(fee.amount) || 0;
            return amount > 0;
        });
        
        nonZeroFees.forEach(fee => {
            const descriptionShort = fee.description.length > 30 
                ? fee.description.substring(0, 27) + '...' 
                : fee.description;
                
            doc.text(descriptionShort, 20, yPos);
            doc.text(fee.category, 80, yPos);
            doc.text(fee.amountStr, 130, yPos);
            doc.text(fee.status, 165, yPos);
            yPos += 7;
        });
        
        // Add updates table
        yPos += 10;
        doc.setFontSize(14);
        doc.text('Updates History', 15, yPos);
        yPos += 10;
        
        // Check if we need a new page
        if (yPos > 250) {
            doc.addPage();
            yPos = 20;
        }
        
        // Table headers
        doc.setFontSize(10);
        doc.setTextColor(100, 100, 100);
        doc.text('Date', 20, yPos);
        doc.text('Details', 50, yPos);
        doc.text('Fee Type', 130, yPos);
        doc.text('Amount', 165, yPos);
        
        // Table rows
        doc.setTextColor(0, 0, 0);
        yPos += 5;
        
        // Filter updates with dollar amounts in the details text (using same logic as in display)
        const updatesWithDollarAmounts = appState.updates.filter(update => {
            // Check if amount field has a non-zero value
            const amount = parseFloat(update.amount) || 0;
            if (amount > 0) return true;
            
            // If amount field doesn't have a value, check the details text for dollar amounts
            if (update.details) {
                // Look for dollar amount pattern in details
                const dollarPattern = /\$\s*([0-9,]+(\.[0-9]{2})?)/;
                const match = update.details.match(dollarPattern);
                if (match) {
                    // If there's a dollar amount in the details, extract and save it
                    const extractedAmount = parseFloat(match[1].replace(',', ''));
                    if (extractedAmount > 0) {
                        // If we found a valid amount in the text but it wasn't in the amount field,
                        // we'll update the display value
                        update.amountStr = match[0]; // Use the full match including $ sign
                        update.amount = extractedAmount;
                        return true;
                    }
                }
            }
            
            return false;
        });
        
        updatesWithDollarAmounts.forEach(update => {
            // Check if we need a new page
            if (yPos > 270) {
                doc.addPage();
                yPos = 20;
                // Repeat headers on new page
                doc.setTextColor(100, 100, 100);
                doc.text('Date', 20, yPos);
                doc.text('Details', 50, yPos);
                doc.text('Fee Type', 130, yPos);
                doc.text('Amount', 165, yPos);
                doc.setTextColor(0, 0, 0);
                yPos += 5;
            }
            
            doc.text(update.date, 20, yPos);
            
            // Handle multi-line text for details
            const detailsShort = update.details.length > 40 
                ? update.details.substring(0, 37) + '...' 
                : update.details;
                
            doc.text(detailsShort, 50, yPos);
            doc.text(update.feeType, 130, yPos);
            doc.text(update.amountStr, 165, yPos);
            
            yPos += 7;
        });
        
        // Add footer
        const footerText = `Generated by JamiBilling on ${new Date().toLocaleDateString()}`;
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(footerText, pageWidth / 2, 285, { align: 'center' });
        
        // Save the PDF
        doc.save(`JamiBilling_Case_${appState.caseData.caseId}.pdf`);
        
    } catch (error) {
        console.error('PDF export error:', error);
        alert('An error occurred while exporting to PDF. Please try again.');
    }
}

// Export results to Excel
async function exportToExcel() {
    try {
        const response = await fetch('/api/export/excel');
        const data = await response.json();
        
        if (data.success) {
            // Create a temporary link to download the file
            const link = document.createElement('a');
            link.href = data.file_url;
            link.download = `JamiBilling_Case_${appState.caseData.caseId}.xlsx`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert(`Export failed: ${data.message}`);
        }
    } catch (error) {
        console.error('Excel export error:', error);
        alert('An error occurred while exporting to Excel. Please try again.');
    }
}

// Show a specific section of the app
function showSection(sectionName) {
    loginSection.classList.remove('active');
    processSection.classList.remove('active');
    resultsSection.classList.remove('active');
    
    switch (sectionName) {
        case 'login':
            loginSection.classList.add('active');
            break;
        case 'process':
            processSection.classList.add('active');
            break;
        case 'results':
            resultsSection.classList.add('active');
            break;
    }
    
    appState.currentSection = sectionName;
}

// Update the progress bar
function updateProgress(percentage) {
    progressFill.style.width = `${percentage}%`;
}

// Update the status message
function updateStatus(message) {
    statusMessage.textContent = message;
    console.log('Status:', message);
}

// Update the current step indicator
function updateStep(stepIndex) {
    // Reset all steps
    steps.forEach((step, index) => {
        step.classList.remove('active', 'complete');
        if (index < stepIndex) {
            step.classList.add('complete');
        }
    });
    
    // Set active step
    if (stepIndex >= 0 && stepIndex < steps.length) {
        steps[stepIndex].classList.add('active');
        appState.currentStep = stepIndex;
    }
}

// Cancel the current process
function cancelProcess() {
    if (appState.processing && !confirm('Are you sure you want to cancel the current process?')) {
        return;
    }
    
    appState.processing = false;
    showSection('login');
}

// Start a new search
function startNewSearch() {
    showSection('login');
}

// Initialize the app when the DOM is ready
document.addEventListener('DOMContentLoaded', initApp);
