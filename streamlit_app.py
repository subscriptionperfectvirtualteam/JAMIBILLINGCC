"""
JamiBilling - RDN Fee Scraper Application
Streamlit frontend for the Playwright version
"""

import os
import json
import pandas as pd
import streamlit as st
import asyncio
import datetime
import logging
import traceback
from app_playwright import (
    async_login, 
    async_extract_case_data, 
    lookup_repo_fee, 
    identify_fee_type, 
    identify_fee_status
)

# Configure logging
logging.basicConfig(
    filename='jami_billing.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize session state if not exists
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'case_data' not in st.session_state:
    st.session_state.case_data = None
if 'updates' not in st.session_state:
    st.session_state.updates = None
if 'db_data' not in st.session_state:
    st.session_state.db_data = None
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'password' not in st.session_state:
    st.session_state.password = ""
if 'security_code' not in st.session_state:
    st.session_state.security_code = ""
if 'case_id' not in st.session_state:
    st.session_state.case_id = ""
if 'cookies' not in st.session_state:
    st.session_state.cookies = None
if 'is_second_step' not in st.session_state:
    st.session_state.is_second_step = False
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = ""
if 'definitive_client_name' not in st.session_state:
    st.session_state.definitive_client_name = None

# Load application config
try:
    with open('config.json', 'r') as f:
        app_config = json.load(f)
    logging.info("Config loaded successfully")
except Exception as e:
    logging.error(f"Error loading config: {str(e)}")
    app_config = {
        "database": {
            "provider": "SQLOLEDB",
            "server": "localhost",
            "database": "RDN_Billing",
            "username": "admin",
            "password": "password"
        },
        "rdn": {
            "login_url": "https://secureauth.recoverydatabase.net/public/login",
            "case_url_template": "https://app.recoverydatabase.net/alpha_rdn/module/default/case2/?case_id={case_id}"
        }
    }

# Load fee categories from the JSON file
try:
    with open('backend/fee_categories.json', 'r') as f:
        fee_categories = json.load(f)
    logging.info("Fee categories loaded successfully")
except Exception as e:
    logging.error(f"Error loading fee categories: {str(e)}")
    fee_categories = {
        "Storage": {
            "keywords": ["storage fee", "daily storage", "impound fee", "lot fee"],
            "color": "#4e73df"
        },
        "Repossession": {
            "keywords": ["repo fee", "recovery fee", "tow fee", "involuntary repo"],
            "color": "#e74a3b"
        },
        "Other": {
            "keywords": ["other"],
            "color": "#858796"
        }
    }

# Ensure required directories exist
os.makedirs('debug', exist_ok=True)
os.makedirs(os.path.join('static', 'exports'), exist_ok=True)

# Global event loop for asyncio
loop = None

def get_event_loop():
    """Get or create the event loop for async operations"""
    global loop
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop

def login_to_rdn():
    """Handle login to RDN using Playwright"""
    logging.info("Login request received")
    
    # Create data dictionary for the original function
    data = {
        "username": st.session_state.username,
        "password": st.session_state.password,
        "securityCode": st.session_state.security_code,
        "caseId": st.session_state.case_id,
        "is_second_step": st.session_state.is_second_step,
        "verificationCode": st.session_state.verification_code
    }
    
    try:
        # Run the async login function in the event loop
        loop = get_event_loop()
        success, message = loop.run_until_complete(async_login(data))
        
        # If this looks like it might be waiting for a second factor, inform user
        if success is False and "multi-factor" in message.lower():
            st.session_state.is_second_step = True
            st.error("Multi-factor authentication required! Please enter verification code.")
            return False
        
        if success:
            st.session_state.logged_in = True
            st.success("Login successful!")
            return True
        else:
            st.error(f"Login failed: {message}")
            return False
            
    except Exception as e:
        logging.exception(f"Error during login: {str(e)}")
        st.error(f"Error during login: {str(e)}")
        return False

def extract_case_data():
    """Extract case data from RDN"""
    logging.info("Case data request received")
    
    case_id = st.session_state.case_id
    logging.info(f"Processing case ID: {case_id}")
    
    try:
        # Run the async case data extraction function in the event loop
        with st.spinner("Extracting case data..."):
            loop = get_event_loop()
            success, result = loop.run_until_complete(async_extract_case_data(case_id))
        
        if success:
            # Filter out fees with zero amounts before storing in session
            if "fees" in result["case_data"]:
                result["case_data"]["fees"] = [fee for fee in result["case_data"]["fees"] if fee.get('amount', 0) > 0]
                logging.info(f"Filtered fees to exclude zero amounts. Remaining fees: {len(result['case_data']['fees'])}")
                
            # Store case data and updates in session state
            st.session_state.case_data = result["case_data"]
            st.session_state.updates = result["updates"]
            
            # Auto-fetch database data for this case
            logging.info("Case data extraction successful, auto-fetching database data")
            try:
                db_data = auto_fetch_database_fees(result["case_data"])
                if db_data:
                    logging.info(f"Auto-fetched database fee: ${db_data['amount']:.2f}")
                    st.session_state.db_data = db_data
            except Exception as e:
                logging.error(f"Error during auto database fetch: {str(e)}")
                # This is non-blocking, so we continue even if db fetch fails
            
            st.success("Case data extracted successfully!")
            return True
        else:
            st.error(f"Failed to extract case data: {result}")
            return False
        
    except Exception as e:
        error_msg = str(e)
        logging.exception(f"Error extracting case data: {error_msg}")
        
        # Provide a more user-friendly message for timeout errors
        if "Timeout" in error_msg:
            st.error("The RDN system is taking too long to respond. Please try again or check RDN status.")
        else:
            st.error(f"Error extracting case data: {error_msg}")
        return False

def auto_fetch_database_fees(case_data=None):
    """
    Automatically fetch fee information from database using current case info
    This function will be called after case information is extracted
    
    Args:
        case_data (dict, optional): The case data containing client info. If None, uses session data.
        
    Returns:
        dict: The database fee data, or None if not found
    """
    # Get case data from session if not provided
    if case_data is None:
        if st.session_state.case_data is None:
            logging.error("Case data not available for auto database fetch")
            return None
        case_data = st.session_state.case_data
    
    client_name = case_data.get('clientName')
    lienholder_name = case_data.get('lienHolder')
    repo_type = case_data.get('repoType', 'Involuntary Repo')
    
    # Default to Involuntary Repo if not found or invalid
    if not repo_type or repo_type == 'Not Found':
        repo_type = 'Involuntary Repo'
    
    logging.info(f"Auto-fetching fee data from database using case information:")
    logging.info(f"Client: {client_name}")
    logging.info(f"Lienholder: {lienholder_name}")
    logging.info(f"Repo Type: {repo_type}")
    
    # Fetch matching fee records from database
    try:
        with st.spinner("Fetching database information..."):
            db_result = lookup_repo_fee(client_name, lienholder_name, repo_type)
        
        if db_result:
            logging.info(f"Successfully fetched repo fee from database: ${float(db_result['amount']):.2f}")
            
            # Format for frontend API
            api_result = {
                "fdId": db_result['fd_id'],
                "clientName": db_result['client_name'],
                "lienholderName": db_result['lienholder_name'],
                "feeTypeName": db_result['fee_type'],
                "amount": float(db_result['amount']) if isinstance(db_result['amount'], float) else db_result['amount'],
                "isFallback": db_result.get('is_fallback', False)
            }
            
            # If there's a message, include it
            if 'message' in db_result:
                api_result["message"] = db_result['message']
                
            return api_result
        else:
            logging.warning("No matching fee data found in database")
            
            # Create mock data when no database match
            mock_data = {
                "fdId": f"FD-{case_data.get('caseId', '0000')}",
                "clientName": client_name,
                "lienholderName": lienholder_name,
                "feeTypeName": repo_type,
                "amount": 350.00,
                "isFallback": True,
                "message": "No matching database record found. Using default amount."
            }
            
            return mock_data
            
    except Exception as e:
        logging.error(f"Error in auto database fetch: {str(e)}")
        logging.error(traceback.format_exc())
        
        # Create mock data for exception cases
        mock_data = {
            "fdId": f"FD-{case_data.get('caseId', '0000')}",
            "clientName": client_name,
            "lienholderName": lienholder_name,
            "feeTypeName": repo_type,
            "amount": 350.00,
            "isFallback": True,
            "message": f"Database error: {str(e)}. Using default amount."
        }
        
        return mock_data

def export_to_csv():
    """Export results to CSV files"""
    if st.session_state.case_data is None or st.session_state.updates is None:
        st.error("No data available to export")
        return None, None, None
    
    # Create directory if it doesn't exist
    export_dir = os.path.join('static', 'exports')
    os.makedirs(export_dir, exist_ok=True)
    
    # Generate timestamps and filenames
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    case_id = st.session_state.case_data.get('caseId', '0000')
    
    summary_file = f"JamiBilling_Summary_{case_id}_{timestamp}.csv"
    fees_file = f"JamiBilling_Fees_{case_id}_{timestamp}.csv"
    updates_file = f"JamiBilling_Updates_{case_id}_{timestamp}.csv"
    
    summary_path = os.path.join(export_dir, summary_file)
    fees_path = os.path.join(export_dir, fees_file)
    updates_path = os.path.join(export_dir, updates_file)
    
    # Export summary
    try:
        case_data = st.session_state.case_data
        db_data = st.session_state.db_data
        
        # Create summary data
        summary_data = [
            {"Item": "Case ID", "Value": case_data.get('caseId', '')},
            {"Item": "Client Name", "Value": case_data.get('clientName', '')},
            {"Item": "Lien Holder", "Value": case_data.get('lienHolder', '')},
            {"Item": "Order To", "Value": case_data.get('orderTo', '')},
            {"Item": "", "Value": ""},
            {"Item": "Database Information", "Value": ""},
            {"Item": "Fee ID", "Value": db_data.get('fdId', '') if db_data else ''},
            {"Item": "Fee Type", "Value": db_data.get('feeTypeName', '') if db_data else ''},
            {"Item": "Amount", "Value": db_data.get('amount', '') if db_data else ''},
            {"Item": "", "Value": ""},
            {"Item": "Total Fees", "Value": sum(fee.get('amount', 0) for fee in case_data.get('fees', []))}
        ]
        
        # Create DataFrame and export
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(summary_path, index=False)
        
        # Export fees
        fees = case_data.get('fees', [])
        if fees:
            # Add enhanced fields
            fees_data = []
            for fee in fees:
                fee_dict = {
                    "Description": fee.get('description', ''),
                    "Category": fee.get('category', ''),
                    "Amount": fee.get('amount', 0),
                    "Status": fee.get('status', ''),
                    "Source": fee.get('source', ''),
                    "Confidence": fee.get('confidence', '')
                }
                
                # Add any additional fee-specific data as Notes
                notes = []
                if 'dailyRate' in fee:
                    notes.append(f"Daily Rate: {fee['dailyRate']}")
                if 'storageDays' in fee:
                    notes.append(f"Storage Days: {fee['storageDays']}")
                if 'vehicleYear' in fee and 'vehicleMake' in fee:
                    notes.append(f"Vehicle: {fee['vehicleYear']} {fee['vehicleMake']}")
                
                fee_dict["Notes"] = "; ".join(notes)
                fees_data.append(fee_dict)
            
            fees_df = pd.DataFrame(fees_data)
            fees_df.to_csv(fees_path, index=False)
        
        # Export updates
        updates = st.session_state.updates
        if updates:
            # Add enhanced fields
            updates_data = []
            for update in updates:
                update_dict = {
                    "Date": update.get('date', ''),
                    "Details": update.get('details', ''),
                    "Fee Type": update.get('feeType', ''),
                    "Amount": update.get('amount', 0),
                    "Status": update.get('status', ''),
                    "Confidence": update.get('feeTypeConfidence', ''),
                    "Page": update.get('page', '')
                }
                
                # Add any additional fee-specific data
                notes = []
                if 'dailyRate' in update:
                    notes.append(f"Daily Rate: {update['dailyRate']}")
                if 'storageDays' in update:
                    notes.append(f"Storage Days: {update['storageDays']}")
                if 'vehicleYear' in update and 'vehicleMake' in update:
                    notes.append(f"Vehicle: {update['vehicleYear']} {update['vehicleMake']}")
                
                update_dict["Additional Info"] = "; ".join(notes)
                updates_data.append(update_dict)
            
            updates_df = pd.DataFrame(updates_data)
            updates_df.to_csv(updates_path, index=False)
        
        return summary_path, fees_path, updates_path
    
    except Exception as e:
        logging.exception(f"Error generating CSV exports: {str(e)}")
        st.error(f"Error generating CSV exports: {str(e)}")
        return None, None, None

def show_login_page():
    """Show the login form"""
    st.title("JamiBilling - RDN Fee Scraper")
    
    with st.form("login_form"):
        st.subheader("Login to RDN")
        
        # Get or set session values
        username = st.text_input("Username", value=st.session_state.username)
        password = st.text_input("Password", type="password", value=st.session_state.password)
        security_code = st.text_input("Security Code", value=st.session_state.security_code)
        case_id = st.text_input("Case ID", value=st.session_state.case_id)
        
        # Update session state
        st.session_state.username = username
        st.session_state.password = password
        st.session_state.security_code = security_code
        st.session_state.case_id = case_id
        
        # Handle second factor auth if needed
        if st.session_state.is_second_step:
            verification_code = st.text_input("Verification Code")
            st.session_state.verification_code = verification_code
        
        # Submit button
        submit = st.form_submit_button("Login & Process Case")
        
        if submit:
            if login_to_rdn():
                # Login successful, extract case data
                extract_case_data()

def show_results_page():
    """Show the results after successful login and data extraction"""
    st.title("JamiBilling - Results")
    
    # Add a logout button
    if st.button("Logout"):
        # Reset session state
        st.session_state.logged_in = False
        st.session_state.case_data = None
        st.session_state.updates = None
        st.session_state.db_data = None
        st.session_state.cookies = None
        st.session_state.is_second_step = False
        st.session_state.verification_code = ""
        st.experimental_rerun()
    
    case_data = st.session_state.case_data
    updates = st.session_state.updates
    db_data = st.session_state.db_data
    
    # Display case information
    st.header("Case Information")
    st.subheader("Client Details")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Case ID", case_data.get('caseId', 'N/A'))
        st.metric("Client Name", case_data.get('clientName', 'N/A'))
    with col2:
        st.metric("Lien Holder", case_data.get('lienHolder', 'N/A'))
        st.metric("Order To", case_data.get('orderTo', 'N/A'))
    
    # Display database information
    if db_data:
        st.subheader("Database Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Fee ID", db_data.get('fdId', 'N/A'))
            st.metric("Fee Type", db_data.get('feeTypeName', 'N/A'))
        with col2:
            st.metric("Amount", f"${db_data.get('amount', 0):.2f}")
            if db_data.get('isFallback'):
                st.info("Using fallback fee amount")
        
        if 'message' in db_data:
            st.info(db_data['message'])
    
    # Display fees
    if case_data and 'fees' in case_data and case_data['fees']:
        st.header("Extracted Fees")
        
        # Create DataFrame for fees
        fees_data = []
        total_amount = 0
        
        for fee in case_data['fees']:
            fee_dict = {
                "Description": fee.get('description', '')[:100] + '...' if len(fee.get('description', '')) > 100 else fee.get('description', ''),
                "Category": fee.get('category', 'Unknown'),
                "Amount": f"${fee.get('amount', 0):.2f}",
                "Status": fee.get('status', 'Unknown')
            }
            total_amount += fee.get('amount', 0)
            fees_data.append(fee_dict)
        
        # Display total
        st.metric("Total Fees", f"${total_amount:.2f}")
        
        # Display fees table
        st.dataframe(pd.DataFrame(fees_data))
    
    # Display updates
    if updates:
        st.header("Updates History")
        
        # Create DataFrame for updates
        updates_data = []
        
        for update in updates:
            # Truncate long descriptions
            details = update.get('details', '')
            if len(details) > 100:
                details = details[:100] + '...'
            
            update_dict = {
                "Date": update.get('date', 'Unknown'),
                "Details": details,
                "Fee Type": update.get('feeType', 'Unknown'),
                "Amount": f"${update.get('amount', 0):.2f}"
            }
            updates_data.append(update_dict)
        
        # Display updates table
        st.dataframe(pd.DataFrame(updates_data))
    
    # Export options
    st.header("Export Options")
    
    if st.button("Export to CSV"):
        summary_path, fees_path, updates_path = export_to_csv()
        
        if summary_path and fees_path and updates_path:
            st.success("Export successful!")
            
            # Create download links
            col1, col2, col3 = st.columns(3)
            
            with col1:
                with open(summary_path, 'rb') as f:
                    st.download_button(
                        label="Download Summary",
                        data=f,
                        file_name=os.path.basename(summary_path),
                        mime="text/csv"
                    )
            
            with col2:
                with open(fees_path, 'rb') as f:
                    st.download_button(
                        label="Download Fees",
                        data=f,
                        file_name=os.path.basename(fees_path),
                        mime="text/csv"
                    )
            
            with col3:
                with open(updates_path, 'rb') as f:
                    st.download_button(
                        label="Download Updates",
                        data=f,
                        file_name=os.path.basename(updates_path),
                        mime="text/csv"
                    )
    
    # Add a button to re-extract data for the same case
    if st.button("Re-Extract Data"):
        extract_case_data()
        st.experimental_rerun()

def main():
    """Main application flow"""
    st.set_page_config(
        page_title="JamiBilling - RDN Fee Scraper",
        page_icon="💰",
        layout="wide",
    )
    
    # Display appropriate page based on login status
    if not st.session_state.logged_in or st.session_state.case_data is None:
        show_login_page()
    else:
        show_results_page()

if __name__ == "__main__":
    main()