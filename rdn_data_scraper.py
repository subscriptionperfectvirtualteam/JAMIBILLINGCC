import json
import time
import re
import asyncio
from playwright.async_api import async_playwright

async def scrape_rdn_data():
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=False)
        
        # Create a new context and page
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to the URL
        print("Navigating to the URL...")
        await page.goto('https://app.recoverydatabase.net/alpha_rdn/module/default/case2/?case_id=2168698538')
        
        # Wait for manual login (maximum 30 seconds)
        print("Please log in manually. You have 30 seconds...")
        await asyncio.sleep(30)
        
        try:
            # Find and click on the "Updates" tab
            print("Looking for Updates tab...")
            try:
                # Try multiple methods to find the Updates tab
                updates_tab = await page.query_selector('a:text("Updates")')
                if updates_tab:
                    await updates_tab.click()
                else:
                    # Try alternate selector
                    await page.click('text=Updates', exact=True)
                print("Navigated to Updates tab")
            except Exception as e:
                print(f"Error clicking Updates tab: {e}. Trying alternate methods...")
                try:
                    # Try finding any tab/navigation elements
                    nav_items = await page.query_selector_all('a.nav-link, a.tab-link, li.nav-item a')
                    for item in nav_items:
                        text = await item.inner_text()
                        if "update" in text.lower():
                            await item.click()
                            print(f"Clicked on tab with text: {text}")
                            break
                except Exception as e2:
                    print(f"Failed to find Updates tab: {e2}")
            
            # Click on "ALL" in pagination if it exists
            print("Looking for the ALL pagination button...")
            try:
                # Wait for the pagination to be visible first
                await page.wait_for_selector('nav[aria-label="Updates pagination"]', timeout=5000)
                
                # Use the exact selector from the provided HTML
                all_link = await page.query_selector('li.page-item a.page-link[data-page="ALL"]')
                if all_link:
                    await all_link.click()
                    print("Clicked on 'ALL' pagination button")
                else:
                    # Try a more general selector
                    all_link = await page.query_selector('a.page-link[data-page="ALL"]')
                    if all_link:
                        await all_link.click()
                        print("Clicked on 'ALL' pagination link (second method)")
                    else:
                        # Try by text content
                        all_link = await page.query_selector('a.page-link:text("ALL")')
                        if all_link:
                            await all_link.click()
                            print("Clicked on 'ALL' pagination link (text method)")
                        else:
                            # Last attempt using a direct click
                            await page.click('text=ALL', exact=True)
                            print("Clicked on 'ALL' text (fallback method)")
                
                # Wait for page to update after clicking ALL
                await page.wait_for_load_state('networkidle')
                print("Page loaded after clicking ALL")
                
            except Exception as e:
                print(f"'ALL' pagination link not found or not clickable: {e}")
            
            # Wait for the updates to load
            await asyncio.sleep(3)
            
            # Wait a bit longer for all updates to load
            print("Waiting for all updates to load...")
            await asyncio.sleep(5)
            
            # Find all update sections
            print("Collecting update data...")
            dl_elements = await page.query_selector_all("dl")
            print(f"Found {len(dl_elements)} update sections")
            
            dollar_records = []
            
            # Process each update section
            for dl in dl_elements:
                try:
                    # Check if this dl contains details with dollar sign
                    details_element = await dl.query_selector(".update-text-black")
                    if not details_element:
                        # Try finding by ID that ends with _view_comments
                        details_elements = await dl.query_selector_all("dd[id]")
                        for element in details_elements:
                            element_id = await element.get_attribute('id')
                            if element_id and element_id.endswith('_view_comments'):
                                details_element = element
                                break
                                
                    if not details_element:
                        # Try finding by div.row containing dt with text "Details"
                        dt_elements = await dl.query_selector_all('dt')
                        for dt in dt_elements:
                            text = await dt.inner_text()
                            if text == "Details":
                                parent_row = await dt.evaluate_handle("node => node.closest('div.row')")
                                if parent_row:
                                    details_element = await parent_row.query_selector('dd')
                                    break
                        
                    if not details_element:
                        continue
                        
                    details_text = await details_element.inner_text()
                    
                    # Only process records containing dollar sign
                    if '$' in details_text:
                        # Create a record by extracting all required data
                        record = {
                            "details": details_text,
                            "dollar_amount": re.findall(r'\$\d+(?:\.\d+)?', details_text)
                        }
                        
                        # Try to get data from the structured rows
                        try:
                            row_elements = await dl.query_selector_all("div.row div.col")
                            for col in row_elements:
                                dt = await col.query_selector("dt")
                                if not dt:
                                    continue
                                    
                                label_text = await dt.inner_text()
                                dd = await col.query_selector("dd")
                                if dd:
                                    value_text = await dd.inner_text()
                                    
                                    # Convert label to snake_case for JSON keys
                                    key = label_text.lower().replace(' ', '_').replace('/', '_')
                                    record[key] = value_text
                        except Exception as row_error:
                            print(f"Error extracting from row structure: {row_error}")
                            
                            # Fallback: Extract other data points using dt/dd pairs directly
                            dt_elements = await dl.query_selector_all("dt")
                            for dt in dt_elements:
                                label_text = await dt.inner_text()
                                if label_text in ["Saved to RDN", "Last Updated By", "Update Date/Time", "Company", "Update Type"]:
                                    # Find corresponding dd element (next sibling)
                                    dd = await dt.evaluate_handle("node => node.nextElementSibling")
                                    if dd:
                                        value_text = await dd.inner_text()
                                        
                                        # Convert label to snake_case for JSON keys
                                        key = label_text.lower().replace(' ', '_').replace('/', '_')
                                        record[key] = value_text
                        
                        dollar_records.append(record)
                        print(f"Found record with dollar amount: {record.get('dollar_amount', 'unknown')}")
                
                except Exception as e:
                    print(f"Error processing a section: {e}")
                    continue
            
            # Save to JSON file
            with open("rdn_dollar_records.json", "w") as f:
                json.dump(dollar_records, f, indent=4)
            
            print(f"Saved {len(dollar_records)} records with dollar amounts to rdn_dollar_records.json")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Wait for user input before closing
        input("Press Enter to close the browser...")
        await browser.close()

if __name__ == "__main__":
    # Run the async function
    asyncio.run(scrape_rdn_data())