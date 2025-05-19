"""
Test script for database connection
"""

import logging
import json
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Try to import pypyodbc
try:
    import pypyodbc as pyodbc
    HAS_PYODBC = True
except ImportError:
    logging.warning("pypyodbc module not found, database functionality will be limited")
    pyodbc = None
    HAS_PYODBC = False

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
            "server": "pvtserver.database.windows.net",
            "database": "RDN_Billing",
            "username": "pvtadmin@perfectvirtualteam.com@pvtserver",
            "password": "Sunny$hill9"
        }
    }

def test_database_connection():
    """Test the database connection with our improved code"""
    if not HAS_PYODBC:
        logging.warning("Cannot test database connection without pypyodbc module")
        return False

    # Get database config
    try:
        db_config = app_config['database']
        
        # Build connection string from config
        server = db_config['server']
        database = db_config['database']
        username = db_config['username']
        password = db_config['password']
        
        # Try several possible driver names that might exist on the system
        driver_names = [
            "{ODBC Driver 18 for SQL Server}",
            "{ODBC Driver 17 for SQL Server}",
            "{SQL Server Native Client 11.0}",
            "{SQL Server}",
            "{FreeTDS}"
        ]
        
        # Default connection string in case all attempts fail
        conn_str = None
        
        # Try connection with each driver
        for driver in driver_names:
            try:
                test_conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"
                logging.info(f"Attempting connection with driver: {driver}")
                pyodbc.connect(test_conn_str)
                conn_str = test_conn_str
                logging.info(f"Successfully connected using driver: {driver}")
                break
            except Exception as driver_e:
                logging.warning(f"Failed to connect with driver {driver}: {str(driver_e)}")
        
        # If none of the drivers worked, use the last attempted connection string
        if conn_str is None:
            conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};"
            logging.warning("All driver attempts failed. Using basic connection string as last resort.")
            
        # Log the final connection attempt
        logging.info(f"Attempting final database connection to: {server}/{database}")
        
        # Connect to the database using the most appropriate connection string found
        conn = pyodbc.connect(conn_str)
        
        # If we get here, connection was successful
        logging.info("DATABASE CONNECTION SUCCESSFUL!")
        
        # Try to inspect the schema
        cursor = conn.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        logging.info(f"Database tables found: {', '.join(table_names[:10])}")
        
        # Check if required tables exist
        required_tables = ['RDN_Client', 'Lienholder', 'FeeType', 'FeeDetails2']
        missing_tables = [table for table in required_tables if table not in table_names]
        if missing_tables:
            logging.error(f"Required tables missing: {', '.join(missing_tables)}")
        else:
            logging.info("All required tables found in database")
        
        # Close the connection
        conn.close()
        return True
    
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logging.info("Starting database connection test")
    success = test_database_connection()
    if success:
        logging.info("DATABASE CONNECTION TEST PASSED!")
    else:
        logging.error("DATABASE CONNECTION TEST FAILED!")