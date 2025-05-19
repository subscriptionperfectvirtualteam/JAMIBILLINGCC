"""
JamiBilling - Updates Extraction Test Script
Test the improved updates extraction logic
"""

import os
import json
import re
import logging
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Ensure required directories exist
os.makedirs('debug', exist_ok=True)

async def extract_updates_from_page(page, case_id, page_num=1):
    """
    Extract updates from the current page
    Returns a list of update entries found on the page
    """
    # Initialize an empty list for this page's updates
    page_updates = []
    # Extract page content
    updates_content = await page.content()
    
    # Save the content to a debug file for this page
    with open(os.path.join('debug', f'updates_{case_id}_page{page_num}.html'), 'w', encoding='utf-8') as f:
        f.write(updates_content)
    
    # Take screenshot of the current page
    await page.screenshot(path=os.path.join('debug', f'updates_{case_id}_page{page_num}.png'))
    
    # Add detailed information about the current state
    current_url = page.url
    logging.info(f"Extracting updates from URL: {current_url} (Page {page_num})")
    
    # Parse the page content
    updates_soup = BeautifulSoup(updates_content, 'html.parser')
    
    # Define the dollar pattern for extracting amounts
    dollar_pattern = r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    
    # List already initialized at the beginning of the function
    # page_updates = []

    # DIRECT SELECTION: Try multiple selectors to find update elements
    update_elements = []
    update_details_elements = []  # To store dt/dd pairs with Details
    
    # Direct element selection for common update patterns
    common_update_selectors = [
        "tr.update-row",
        "div.update-entry",
        "div.history-entry",
        ".update-list > div",
        ".update-list > li",
        ".update-container .row",
        ".history-list tr",
        "table.updates-table tr:not(:first-child)",  # Skip header row
        ".tab-content tr:not(.header-row)",  # Skip header row
        "dl.update-details",  # For dt/dd structured content
        ".update-item"
    ]
    
    logging.info("Looking for update elements with direct selectors")
    direct_elements_found = 0
    
    for selector in common_update_selectors:
        try:
            elements = updates_soup.select(selector)
            if elements:
                update_elements.extend(elements)
                direct_elements_found += len(elements)
                logging.info(f"Found {len(elements)} update elements with selector: {selector}")
        except Exception as e:
            logging.warning(f"Error finding elements with selector {selector}: {str(e)}")
    
    logging.info(f"Total direct elements found: {direct_elements_found}")
    
    # Look for dt/dd pairs where dt contains "Details"
    dt_elements = updates_soup.find_all('dt', string=lambda s: s and 'Details' in s)
    for dt in dt_elements:
        # Try to find corresponding dd element
        next_elem = dt
        while next_elem and next_elem.name != 'dd':
            next_elem = next_elem.next_sibling
        
        if next_elem and next_elem.name == 'dd':
            update_details_elements.append(next_elem)
            logging.info(f"Found details dd element as sibling of dt")
            continue
            
        # If not found as sibling, try parent
        if dt.parent:
            dd_elements = dt.parent.find_all('dd')
            if dd_elements:
                update_details_elements.append(dd_elements[0])
                logging.info(f"Found details dd element via parent")
                continue
                
        # Try grandparent if still not found
        if dt.parent and dt.parent.parent:
            dd_elements = dt.parent.parent.find_all('dd')
            if dd_elements:
                update_details_elements.append(dd_elements[0])
                logging.info(f"Found details dd element via grandparent")
    
    logging.info(f"Found {len(update_details_elements)} dd elements with details content")
    
    # Process update elements
    for element in update_elements:
        element_text = element.get_text()
        
        # Look for dollar amounts in the element text
        amount = 0.00
        amount_str = "$0.00"
        
        # Extract dollar amounts
        dollar_matches = re.finditer(dollar_pattern, element_text)
        for match in dollar_matches:
            amount_str = match.group(0)
            amount = float(match.group(1).replace(',', ''))
            break  # Take the first amount found
        
        # Skip updates with zero amount
        if amount <= 0:
            logging.info("Skipping update with zero amount")
            continue
            
        # Create update entry
        update_entry = {
            "date": extract_date_from_text(element_text),
            "details": element_text[:150].strip(),  # First 150 chars
            "amount": amount,
            "amountStr": amount_str,
            "type": categorize_update(element_text)
        }
        page_updates.append(update_entry)
    
    # Process details elements
    for dd_element in update_details_elements:
        details_text = dd_element.get_text()
        
        # Look for dollar amounts in the details text
        amount = 0.00
        amount_str = "$0.00"
        
        # Extract dollar amounts
        dollar_matches = re.finditer(dollar_pattern, details_text)
        for match in dollar_matches:
            amount_str = match.group(0)
            amount = float(match.group(1).replace(',', ''))
            break  # Take the first amount found
        
        # Skip updates with zero amount
        if amount <= 0:
            logging.info("Skipping update with zero amount")
            continue
            
        # Create update entry
        update_entry = {
            "date": extract_date_from_text(details_text),
            "details": details_text[:150].strip(),  # First 150 chars
            "amount": amount,
            "amountStr": amount_str,
            "type": categorize_update(details_text)
        }
        page_updates.append(update_entry)
        
# Helper functions for update processing
def extract_date_from_text(text):
    """Extract date from update text"""
    # Look for common date patterns (MM/DD/YYYY)
    date_pattern = r'(\d{1,2}/\d{1,2}/\d{4})'
    date_match = re.search(date_pattern, text)
    if date_match:
        return date_match.group(1)
    
    # Look for ISO format date (YYYY-MM-DD)
    iso_pattern = r'(\d{4}-\d{2}-\d{2})'
    iso_match = re.search(iso_pattern, text)
    if iso_match:
        return iso_match.group(1)
    
    return "Unknown Date"

def categorize_update(text):
    """Categorize update based on text content"""
    text_lower = text.lower()
    
    # Fee categories
    if any(term in text_lower for term in ["storage", "lot fee", "daily fee"]):
        return "Storage"
    elif any(term in text_lower for term in ["repo", "repossession", "recovery", "tow"]):
        return "Repossession"
    elif any(term in text_lower for term in ["transport", "delivery", "mileage"]):
        return "Transport"
    elif any(term in text_lower for term in ["admin", "processing", "documentation"]):
        return "Administrative"
    elif any(term in text_lower for term in ["key", "condition", "inspection"]):
        return "Inspection"
    elif any(term in text_lower for term in ["legal", "compliance", "court"]):
        return "Legal"
    
    return "Other"

async def handle_updates_extraction(page, case_id):
    """
    Handle page-by-page extraction of updates, skipping 'All' view
    """
    updates = []
    
    # Extract updates from the first page
    first_page_updates = await extract_updates_from_page(page, case_id, 1)
    updates.extend(first_page_updates)
    logging.info(f"Extracted {len(first_page_updates)} updates from page 1")
    
    # Check for pagination elements
    pagination_found = False
    try:
        # Various selectors for pagination
        pagination_selectors = [
            "ul.pagination", 
            ".pagination", 
            "nav[aria-label='pagination']", 
            ".pager",
            "div.pages",
            ".page-numbers"
        ]
        
        for selector in pagination_selectors:
            pagination = await page.query_selector(selector)
            if pagination:
                pagination_found = True
                logging.info(f"Found pagination with selector: {selector}")
                
                # Take a screenshot of the pagination area
                await page.screenshot(path=os.path.join('debug', f'pagination_{case_id}.png'))
                
                # Check for presence of 'All' button but DON'T click it
                all_link_selectors = [
                    f"{selector} a:has-text('All')",
                    f"{selector} button:has-text('All')",
                    f"{selector} [data-page='all']",
                    f"{selector} a[href*='all']",
                    f"{selector} li:has-text('All') a",
                    ".view-all-link",
                    ".show-all"
                ]
                
                has_all_link = False
                for all_selector in all_link_selectors:
                    all_link = await page.query_selector(all_selector)
                    if all_link:
                        has_all_link = True
                        logging.info(f"Found 'All' link with selector: {all_selector} but skipping it")
                        break
                
                # Process pages sequentially
                page_num = 2  # Start from page 2 since we already processed page 1
                max_pages = 20  # Safety limit to prevent infinite loops
                
                while page_num <= max_pages:
                    # Find and click next page
                    next_page_clicked = False
                    
                    # Try various ways to find the next page link
                    # 1. Try numbered page links
                    page_link_selectors = [
                        f"{selector} a:has-text('{page_num}')",
                        f"{selector} button:has-text('{page_num}')",
                        f"{selector} [data-page='{page_num}']",
                        f"{selector} li:has-text('{page_num}') a"
                    ]
                    
                    for link_selector in page_link_selectors:
                        try:
                            page_link = await page.query_selector(link_selector)
                            if page_link:
                                # Check if this link is already active/current
                                is_active = await page_link.get_attribute("class")
                                if is_active and ("active" in is_active or "current" in is_active):
                                    logging.info(f"Already on page {page_num}, not clicking")
                                    next_page_clicked = True  # Mark as clicked for pagination to continue
                                    break
                                
                                # Click the link
                                await page_link.click()
                                logging.info(f"Clicked link to page {page_num}")
                                
                                # Wait for content to update
                                try:
                                    await page.wait_for_load_state("networkidle", timeout=10000)
                                    logging.info(f"Pagination to page {page_num} successful")
                                except Exception as e:
                                    logging.warning(f"Timeout waiting for networkidle during pagination, continuing anyway: {str(e)}")
                                    # Wait a reasonable time anyway
                                    await page.wait_for_timeout(2000)
                                
                                # Check if we landed on an "All" page after clicking (to avoid processing it)
                                post_click_is_all = False
                                try:
                                    for all_indicator in [
                                        "a.active:has-text('All')", 
                                        "button.active:has-text('All')",
                                        "li.active:has-text('All')",
                                        ".pagination .active[href*='all']"
                                    ]:
                                        all_active = await page.query_selector(all_indicator)
                                        if all_active:
                                            post_click_is_all = True
                                            logging.info("We've landed on an 'All' page after clicking - skipping extraction")
                                            break
                                except Exception:
                                    pass
                                
                                # Only extract if this isn't an "All" page
                                if not post_click_is_all:
                                    # Extract updates from this page
                                    page_updates = await extract_updates_from_page(page, case_id, page_num)
                                    updates.extend(page_updates)
                                    logging.info(f"Extracted {len(page_updates)} updates from page {page_num}")
                                else:
                                    logging.info(f"Skipping extraction of 'All' page that we landed on")
                                
                                next_page_clicked = True
                                break
                        except Exception as e:
                            logging.debug(f"Error clicking page {page_num} link with selector {link_selector}: {str(e)}")
                    
                    # 2. If numbered pagination didn't work, try Next button
                    if not next_page_clicked:
                        next_btn_selectors = [
                            f"{selector} a:has-text('Next')",
                            f"{selector} button:has-text('Next')",
                            ".next a", 
                            ".next-page",
                            ".pagination .next",
                            "a[rel='next']",
                            "a:has-text('»')"
                        ]
                        
                        for next_btn in next_btn_selectors:
                            try:
                                btn = await page.query_selector(next_btn)
                                if btn:
                                    # Check if disabled
                                    disabled = await btn.get_attribute("disabled")
                                    aria_disabled = await btn.get_attribute("aria-disabled")
                                    
                                    if disabled == "true" or disabled == "" or aria_disabled == "true":
                                        logging.info("Next button is disabled, reached last page")
                                        break
                                    
                                    # Check if the parent element is disabled
                                    parent_elem = await btn.evaluate("el => el.parentElement")
                                    if parent_elem:
                                        parent_class = await page.evaluate("el => el.className", parent_elem)
                                        if parent_class and ("disabled" in parent_class):
                                            logging.info("Next button's parent is disabled, reached last page")
                                            break
                                    
                                    # Click the next button
                                    await btn.click()
                                    logging.info(f"Clicked Next button for page {page_num}")
                                    
                                    # Wait for content to update
                                    try:
                                        await page.wait_for_load_state("networkidle", timeout=10000)
                                        logging.info(f"Navigation to next page successful")
                                    except Exception as e:
                                        logging.warning(f"Timeout waiting for networkidle during Next button pagination, continuing anyway: {str(e)}")
                                        # Wait a reasonable time anyway
                                        await page.wait_for_timeout(2000)
                                    
                                    # Check if we landed on an "All" page after clicking Next
                                    post_next_is_all = False
                                    try:
                                        for all_indicator in [
                                            "a.active:has-text('All')", 
                                            "button.active:has-text('All')",
                                            "li.active:has-text('All')",
                                            ".pagination .active[href*='all']"
                                        ]:
                                            all_active = await page.query_selector(all_indicator)
                                            if all_active:
                                                post_next_is_all = True
                                                logging.info("We've landed on an 'All' page after clicking Next - skipping extraction")
                                                break
                                    except Exception:
                                        pass
                                    
                                    # Extract updates if this isn't an All page
                                    if not post_next_is_all:
                                        # Extract updates from this page
                                        page_updates = await extract_updates_from_page(page, case_id, page_num)
                                        updates.extend(page_updates)
                                        logging.info(f"Extracted {len(page_updates)} updates from page {page_num} via Next button")
                                    else:
                                        logging.info(f"Skipping extraction of 'All' page that we landed on via Next button")
                                    
                                    next_page_clicked = True
                                    break
                            except Exception as e:
                                logging.debug(f"Error clicking Next button with selector {next_btn}: {str(e)}")
                    
                    # If we couldn't click any pagination element, we're done
                    if not next_page_clicked:
                        logging.info(f"No more pagination links available after page {page_num-1}")
                        break
                    
                    # Move to next page
                    page_num += 1
                
                break  # Exit the pagination selector loop once we've found and processed pagination
        
        if not pagination_found:
            logging.info("No pagination controls found, all updates are on a single page")
    
    except Exception as e:
        logging.warning(f"Error handling pagination: {str(e)}")
    
    return updates

async def test_updates_extraction():
    """
    Test the updates extraction by loading a test page or URL
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()
        
        # Test URL with your specific case ID
        test_url = "https://app.recoverydatabase.net/alpha_rdn/module/default/case2/?case_id=2168698538"
        case_id = "2168698538"
        
        # Option 1: Use an actual URL
        try:
            logging.info(f"Navigating to test URL: {test_url}")
            await page.goto(test_url)
            
            # Pause for manual login
            logging.info("WAITING FOR MANUAL LOGIN - Please log in to the RDN system in the browser window")
            logging.info("After login, please navigate to the Updates tab manually")
            await page.wait_for_timeout(60000)  # Wait 60 seconds for manual login
            logging.info("Resuming automation - assuming you have logged in and navigated to the Updates tab")
            
            # Take screenshot to verify current state
            await page.screenshot(path=os.path.join('debug', 'before_extraction_start.png'))
            
            # Analyze the current page to see if we're on the Updates tab
            content = await page.content()
            if "update" not in content.lower() and "history" not in content.lower():
                logging.warning("It doesn't appear we're on the Updates tab yet. Attempting to find and click it.")
                
                # Try to find and click the Updates tab
                update_tab_selectors = [
                    "a:has-text('Updates')",
                    "a:has-text('History')",
                    "#updates-tab", 
                    "a[href*='updates']",
                    "a[href*='history']",
                    "ul.nav-tabs a:nth-child(2)",  # Often the second tab
                    ".nav-link:has-text('Updates')",
                    ".tab:has-text('Updates')"
                ]
                
                for selector in update_tab_selectors:
                    try:
                        update_link = await page.query_selector(selector)
                        if update_link:
                            await update_link.click()
                            logging.info(f"Clicked Updates tab using selector: {selector}")
                            await page.wait_for_load_state("networkidle", timeout=10000)
                            await page.wait_for_timeout(2000)  # Additional wait to ensure content loads
                            await page.screenshot(path=os.path.join('debug', 'after_updates_tab_click.png'))
                            break
                    except Exception as e:
                        logging.debug(f"Failed to click Updates tab with selector {selector}: {str(e)}")
            
            # Enhanced pagination detection and handling
            logging.info("Looking for pagination elements on the page")
            await page.screenshot(path=os.path.join('debug', 'before_pagination_detection.png'))
            
            # Save HTML for analysis
            content = await page.content()
            with open(os.path.join('debug', 'page_before_pagination.html'), 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Dump information about all potential pagination elements for debugging
            pagination_info = await page.evaluate("""() => {
                const results = [];
                
                // Look for pagination elements
                const paginationElements = document.querySelectorAll('.pagination, .pager, .page-numbers, .pages, nav[aria-label="pagination"]');
                
                // Look for potential page number links
                const pageLinks = document.querySelectorAll('a[href*="page="], button[data-page], a.page-link, .pagination a, .pager a');
                
                // Look for Next buttons - using standard CSS selectors only
                const nextButtons = document.querySelectorAll('a.next, button.next, a[rel="next"], a:contains("Next"), a:contains(">"), a:contains("»")');
                
                results.push(`Found ${paginationElements.length} pagination containers`);
                results.push(`Found ${pageLinks.length} potential page links`);
                results.push(`Found ${nextButtons.length} potential Next buttons`);
                
                // Get text content of page links
                if (pageLinks.length > 0) {
                    results.push('Page link texts:');
                    for (let i = 0; i < Math.min(pageLinks.length, 20); i++) {
                        results.push(`  ${i+1}: "${pageLinks[i].textContent.trim()}" (class="${pageLinks[i].className}")`);
                    }
                }
                
                // Additional analysis
                results.push('All potential pagination-related elements:');
                // Get all links that might be pagination
                const allLinks = Array.from(document.querySelectorAll('a, button'))
                    .filter(el => {
                        const text = el.textContent.trim();
                        const href = el.getAttribute('href') || '';
                        // Look for numbers, page indicators, or navigation symbols
                        return /^\d+$/.test(text) || 
                               /page/.test(href) || 
                               ['next', 'prev', 'previous', '>>', '<<', '»', '«'].includes(text.toLowerCase());
                    });
                
                for (let i = 0; i < Math.min(allLinks.length, 20); i++) {
                    const el = allLinks[i];
                    results.push(`  ${i+1}: "${el.textContent.trim()}" (tag=${el.tagName}, href="${el.getAttribute('href') || ''}")`);
                }
                
                return results.join('\\n');
            }""")
            
            logging.info(f"Pagination detection results:\n{pagination_info}")
            
            # Once on the updates tab, call our extraction function
            updates = await handle_updates_extraction(page, case_id)
            
            logging.info(f"Extracted {len(updates)} total updates")
            
            # Save the results to a JSON file for analysis
            results_file = os.path.join('debug', f'extracted_updates_{case_id}.json')
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(updates, f, indent=2)
            logging.info(f"Saved {len(updates)} updates to {results_file}")
            
            # Display the first few updates
            logging.info("First few updates:")
            for i, update in enumerate(updates[:5]):
                logging.info(f"Update {i+1}: {update}")
            
        except Exception as e:
            logging.error(f"Error testing with URL: {str(e)}")
            # Save error screenshot
            try:
                await page.screenshot(path=os.path.join('debug', 'error_state.png'))
                content = await page.content()
                with open(os.path.join('debug', 'error_page.html'), 'w', encoding='utf-8') as f:
                    f.write(content)
            except:
                pass
        
        # Option 2: Load from a local HTML file (if available)
        try:
            # Check if we have a sample HTML file - either a specific updates page or any page from debug folder
            sample_files = [
                os.path.join('debug', 'updates_sample.html'),
                os.path.join('debug', 'updates_2168698538_page1.html')
            ]
            
            sample_file = None
            for file_path in sample_files:
                if os.path.exists(file_path):
                    sample_file = file_path
                    break
                    
            if sample_file:
                logging.info(f"Loading sample HTML file: {sample_file}")
                
                # Load the HTML content
                with open(sample_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Set the page content
                await page.set_content(html_content)
                await page.wait_for_timeout(1000)  # Brief wait to ensure content loads
                
                # First, extract just from the current page to test our parsing
                logging.info("First testing single page extraction from the sample file")
                direct_updates = await extract_updates_from_page(page, "sample", 1)
                logging.info(f"Direct extraction from sample page found {len(direct_updates)} updates")
                
                # Check if any elements were found in the HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                common_update_selectors = [
                    "tr.update-row", "div.update-entry", "div.history-entry",
                    ".update-list > div", ".update-list > li", ".update-container .row",
                    ".history-list tr", "table.updates-table tr:not(:first-child)",
                    ".tab-content tr:not(.header-row)", "dl.update-details", ".update-item"
                ]
                
                logging.info("Analyzing sample HTML structure:")
                for selector in common_update_selectors:
                    elements = soup.select(selector)
                    if elements:
                        logging.info(f"  Found {len(elements)} elements with selector: {selector}")
                
                # Look for any table in the HTML
                tables = soup.find_all('table')
                logging.info(f"Found {len(tables)} tables in the sample HTML")
                for i, table in enumerate(tables):
                    rows = table.find_all('tr')
                    logging.info(f"  Table {i+1}: contains {len(rows)} rows")
                    
                    # Check the first row for header information
                    if rows and len(rows) > 0:
                        header_cells = rows[0].find_all(['th', 'td'])
                        if header_cells:
                            headers = [cell.get_text().strip() for cell in header_cells]
                            logging.info(f"    Headers: {', '.join(headers)}")
                
                # Now try full extraction with pagination
                try:
                    sample_updates = await handle_updates_extraction(page, "sample")
                    
                    logging.info(f"Extracted {len(sample_updates)} total updates from sample file")
                    
                    # Save sample results to a JSON file
                    sample_results_file = os.path.join('debug', 'extracted_updates_sample.json')
                    with open(sample_results_file, 'w', encoding='utf-8') as f:
                        json.dump(sample_updates, f, indent=2)
                    logging.info(f"Saved {len(sample_updates)} sample updates to {sample_results_file}")
                    
                    # Show first few sample updates
                    if sample_updates:
                        logging.info("First few sample updates:")
                        for i, update in enumerate(sample_updates[:5]):
                            logging.info(f"Sample Update {i+1}: {update}")
                except Exception as e:
                    logging.error(f"Error with sample file full extraction: {str(e)}")
        except Exception as e:
            logging.error(f"Error testing with sample file: {str(e)}")
        
        # Close browser
        await browser.close()

# Main execution
if __name__ == "__main__":
    print("Starting updates extraction test...")
    
    # Create event loop and run the test
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_updates_extraction())
    
    print("Test completed. Check the logs for results.")