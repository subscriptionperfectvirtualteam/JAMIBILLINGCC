# Improved Updates Tab Extraction
# This code snippet replaces the existing pagination handling in app_playwright.py

async def extract_updates_from_page(page_num=1):
    """
    Extract updates from the current page
    Returns a list of update entries found on the page
    """
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
    
    # Initialize list for this page's updates
    page_updates = []

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
    
    # Process update elements found with direct selectors
    if update_elements:
        logging.info(f"Processing {len(update_elements)} update elements")
        for element in update_elements:
            element_text = element.get_text()
            
            # Process update element...
            # (existing processing code for update elements)
            
            # Example update entry creation (customize based on your app logic)
            update_entry = {
                "date": extract_date(element_text),
                "details": extract_details(element_text),
                "amount": extract_amount(element_text),
                "type": categorize_update(element_text)
            }
            page_updates.append(update_entry)
    
    # Process dt/dd elements separately since they have a different structure
    if update_details_elements:
        logging.info(f"Processing {len(update_details_elements)} detail elements")
        for dd_element in update_details_elements:
            details_text = dd_element.get_text()
            
            # Process details element...
            # (existing processing code for detail elements)
            
            # Example update entry creation
            update_entry = {
                "date": extract_date_from_details(details_text),
                "details": details_text,
                "amount": extract_amount_from_details(details_text),
                "type": categorize_update(details_text)
            }
            page_updates.append(update_entry)
    
    # If no elements found with specific selectors, try broader approaches
    if not page_updates:
        # Try broader approaches to find updates...
        # (existing fallback code)
        pass
    
    return page_updates

# ----------------
# MAIN PAGINATION LOGIC
# ----------------

# Instead of looking for "All" button first, prioritize page-by-page extraction
async def handle_updates_extraction():
    updates = []
    
    # Extract updates from the first page
    first_page_updates = await extract_updates_from_page(1)
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
                                    page_updates = await extract_updates_from_page(page_num)
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
                                        page_updates = await extract_updates_from_page(page_num)
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

# Example usage in async_extract_case_data function
# Replace the existing updates extraction code with this call:
updates = await handle_updates_extraction()