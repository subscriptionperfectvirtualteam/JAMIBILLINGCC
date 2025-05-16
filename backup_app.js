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
    fees: [],
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
function handleLoginSubmit(event) {
    event.preventDefault();
    
    // Get form values
    const formData = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        securityCode: document.getElementById('security-code').value,
        caseId: document.getElementById('case-id').value,
        dbConnection: document.getElementById('db-connection').value
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
        appState.fees = [];
        appState.updates = [];
        
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
        appState.caseData = await extractCaseData(formData.caseId);
        updateProgress(40);
        
        // Step 3: Query database
        updateStep(2);
        updateStatus('Querying database for fee information...');
        appState.dbData = await queryDatabase(formData.dbConnection, appState.caseData);
        updateProgress(60);
        
        // Step 4: Extract updates
        updateStep(3);
        updateStatus('Extracting updates and fee history...');
        appState.updates = await extractUpdates(formData.caseId);
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

// Simulate login to RDN (in a real app, this would use fetch API or similar)
async function loginToRdn(formData) {
    updateStatus('Logging in to RDN...');
    
    // Simulate login process with a delay
    return new Promise(resolve => {
        setTimeout(() => {
            // In a real implementation, this would make an actual API call
            updateStatus('Login successful!');
            resolve(true);
        }, 2000);
    });
}

// Simulate extracting case data (in a real app, this would scrape the actual RDN page)
async function extractCaseData(caseId) {
    updateStatus('Retrieving case information...');
    
    // Simulate data extraction with a delay
    return new Promise(resolve => {
        setTimeout(() => {
            // Mock data - in a real app, this would come from web scraping
            const data = {
                caseId: caseId,
                clientName: 'Primeritus Specialized - IBEAM',
                lienHolder: 'Global CU fka Alaska USA FCU',
                orderTo: 'Recovery Agent',
                vehicleInfo: {
                    make: 'Toyota',
                    model: 'Camry',
                    year: '2020',
                    vin: '1HGCM82633A123456'
                }
            };
            
            updateStatus('Case information retrieved successfully!');
            resolve(data);
        }, 2500);
    });
}

// Simulate database query (in a real app, this would connect to your database)
async function queryDatabase(connectionString, caseData) {
    updateStatus('Connecting to database...');
    
    // Simulate database query with a delay
    return new Promise(resolve => {
        setTimeout(() => {
            // Mock data - in a real app, this would come from your Azure SQL database
            const data = {
                fdId: 'FD-' + Math.floor(1000 + Math.random() * 9000),
                clientName: caseData.clientName,
                lienholderName: caseData.lienHolder,
                feeTypeName: 'Involuntary Repo',
                amount: 350.00
            };
            
            updateStatus('Database query complete!');
            
            // Also populate fees array based on fee type
            appState.fees.push({
                description: 'Involuntary Repo Fee',
                amount: 350.00,
                amountStr: '$350.00',
                category: 'Repossession',
                categoryColor: feeCategories['Repossession'].color,
                status: 'Approved'
            });
            
            // Add a storage fee as well
            appState.fees.push({
                description: 'Storage Fee (5 days)',
                amount: 125.00,
                amountStr: '$125.00',
                category: 'Storage',
                categoryColor: feeCategories['Storage'].color,
                status: 'Pending'
            });
            
            resolve(data);
        }, 2000);
    });
}

// Simulate extracting updates (in a real app, this would scrape the updates tab)
async function extractUpdates(caseId) {
    updateStatus('Retrieving updates and fee history...');
    
    // Simulate updates extraction with a delay
    return new Promise(resolve => {
        setTimeout(() => {
            // Mock data - in a real app, this would come from web scraping
            const updates = [
                {
                    date: '01/12/2025',
                    details: 'Case assigned to recovery agent',
                    amount: 0,
                    amountStr: '$0.00',
                    feeType: 'N/A'
                },
                {
                    date: '01/15/2025',
                    details: 'Vehicle located at debtor residence',
                    amount: 0,
                    amountStr: '$0.00',
                    feeType: 'N/A'
                },
                {
                    date: '01/18/2025',
                    details: 'Vehicle recovered and transported to storage facility',
                    amount: 350.00,
                    amountStr: '$350.00',
                    feeType: 'Repossession'
                },
                {
                    date: '01/18/2025 - 01/23/2025',
                    details: 'Storage fee for 5 days',
                    amount: 125.00,
                    amountStr: '$125.00',
                    feeType: 'Storage'
                },
                {
                    date: '01/20/2025',
                    details: 'Condition report and photos taken',
                    amount: 45.00,
                    amountStr: '$45.00',
                    feeType: 'Inspection'
                }
            ];
            
            // Add one more fee that gets detected from the update text
            const additionalText = "Paid field visit fee of $75.00 for earlier location attempt";
            const extractedFees = extractFeeAmounts(additionalText);
            if (extractedFees.length > 0) {
                updates.push({
                    date: '01/14/2025',
                    details: additionalText,
                    amount: extractedFees[0].amount,
                    amountStr: extractedFees[0].amountStr,
                    feeType: extractedFees[0].category
                });
                
                // Also add to fees array
                appState.fees.push({
                    description: 'Field Visit Fee',
                    amount: 75.00,
                    amountStr: '$75.00',
                    category: 'Agent',
                    categoryColor: feeCategories['Agent'].color,
                    status: 'Paid'
                });
            }
            
            // Add one more fee for inspection
            appState.fees.push({
                description: 'Condition Report & Photos',
                amount: 45.00,
                amountStr: '$45.00',
                category: 'Inspection',
                categoryColor: feeCategories['Inspection'].color,
                status: 'Approved'
            });
            
            updateStatus('Updates retrieved successfully!');
            resolve(updates);
        }, 2500);
    });
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
    
    appState.fees.forEach(fee => {
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
    updatesTableBody.appendChild(document.createElement('tr'));
    updatesTableBody.innerHTML = ''; // Clear existing data
    
    appState.updates.forEach(update => {
        let feeTypeDisplay = update.feeType;
        let feeTypeColor = '#858796'; // Default gray
        
        if (update.feeType !== 'N/A') {
            feeTypeColor = feeCategories[update.feeType]?.color || feeTypeColor;
            feeTypeDisplay = `<span class="category-tag" style="background-color: ${feeTypeColor}">${update.feeType}</span>`;
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
        appState.fees.forEach(fee => {
            doc.text(fee.description, 20, yPos);
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
        appState.updates.forEach(update => {
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
            const detailLines = doc.splitTextToSize(update.details, 75);
            doc.text(detailLines, 50, yPos);
            
            doc.text(update.feeType, 130, yPos);
            doc.text(update.amountStr, 165, yPos);
            
            // Increase y position based on number of lines in details
            yPos += Math.max(7, detailLines.length * 5);
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
function exportToExcel() {
    try {
        const XLSX = window.XLSX;
        
        // Create workbook
        const wb = XLSX.utils.book_new();
        
        // Create fees worksheet
        const feesData = [
            ['Description', 'Category', 'Amount', 'Status'] // Headers
        ];
        
        // Add fee rows
        appState.fees.forEach(fee => {
            feesData.push([
                fee.description,
                fee.category,
                fee.amount,
                fee.status
            ]);
        });
        
        const feesWs = XLSX.utils.aoa_to_sheet(feesData);
        
        // Create updates worksheet
        const updatesData = [
            ['Date', 'Details', 'Fee Type', 'Amount'] // Headers
        ];
        
        // Add update rows
        appState.updates.forEach(update => {
            updatesData.push([
                update.date,
                update.details,
                update.feeType,
                update.amount
            ]);
        });
        
        const updatesWs = XLSX.utils.aoa_to_sheet(updatesData);
        
        // Create summary worksheet
        const summaryData = [
            ['JamiBilling - Case Summary'],
            [''],
            ['Case ID', appState.caseData.caseId],
            ['Client Name', appState.caseData.clientName],
            ['Lien Holder', appState.caseData.lienHolder],
            ['Order To', appState.caseData.orderTo],
            [''],
            ['Database Information'],
            ['Fee ID', appState.dbData.fdId],
            ['Fee Type', appState.dbData.feeTypeName],
            ['Amount', appState.dbData.amount],
            [''],
            ['Total Fees', appState.fees.reduce((sum, fee) => sum + fee.amount, 0)]
        ];
        
        const summaryWs = XLSX.utils.aoa_to_sheet(summaryData);
        
        // Add worksheets to workbook
        XLSX.utils.book_append_sheet(wb, summaryWs, 'Summary');
        XLSX.utils.book_append_sheet(wb, feesWs, 'Fees');
        XLSX.utils.book_append_sheet(wb, updatesWs, 'Updates');
        
        // Save the Excel file
        XLSX.writeFile(wb, `JamiBilling_Case_${appState.caseData.caseId}.xlsx`);
        
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

// Add some styling for category tags
document.head.insertAdjacentHTML('beforeend', `
<style>
.category-tag {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
}
</style>
`);
