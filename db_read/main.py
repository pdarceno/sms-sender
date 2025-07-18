import pandas as pd
from sqlalchemy import create_engine
import os
import traceback
from constants import (
    CONNECTION_STRING_TEST, CONNECTION_STRING_TEST, 
    ACCOUNT_NO_COL, ARREARS_BALANCE_COL, BUSINESS_CODE_COL, 
    PHONE_COL, PHONE2_COL, CUSTOMER_NAME_COL
)

# Function to load the SQL query from a file
def load_sql_query(file_path):
    with open(file_path, 'r') as file:
        query = file.read()
    return query

# Function to run SQL query for account numbers
def fetch_additional_details(account_numbers, test_flag):
    # Set up the connection string (adjust for your database configuration)
    if test_flag:
        connect_string = CONNECTION_STRING_TEST
    else:
        connect_string = CONNECTION_STRING
    
    # Create the SQLAlchemy engine
    engine = create_engine(connect_string)

    # Convert list of account numbers into a string formatted for SQL IN clause
    formatted_account_numbers = ', '.join(f"'{account}'" for account in account_numbers)
    
    # Load the query from the SQL file, always relative to this script's directory
    sql_path = os.path.join(os.path.dirname(__file__), 'select_all.sql')
    query = load_sql_query(sql_path)
    # Inject the column names and account numbers into the query
    query = query.format(
        account_no_col=ACCOUNT_NO_COL,
        arrears_balance_col=ARREARS_BALANCE_COL,
        business_code_col=BUSINESS_CODE_COL,
        phone_col=PHONE_COL,
        phone2_col=PHONE2_COL,
        customer_name_col=CUSTOMER_NAME_COL,
        account_numbers_placeholder=formatted_account_numbers
    )
    print(query)

    # Execute the query and fetch the results into a DataFrame
    df = pd.read_sql(query, engine)

    # Close the engine (optional since SQLAlchemy handles it internally)
    engine.dispose()
    
    print(df)
    return df

# Function to run Populate excel
def populate_excel(excel_file, test_flag):
    try:
        # Load the Excel file that contains the Account No column
        df_accounts = pd.read_excel(excel_file, sheet_name='Sheet1')  # Adjust sheet_name if necessary

        # Keep only the 'Account No' column and drop all others
        if ACCOUNT_NO_COL not in df_accounts.columns:
            raise Exception(f"Excel file must contain a column named '{ACCOUNT_NO_COL}'.")
        df_accounts = df_accounts[[ACCOUNT_NO_COL]]

        # Normalize the Account No column (strip spaces, ensure strings)
        df_accounts[ACCOUNT_NO_COL] = df_accounts[ACCOUNT_NO_COL].astype(str).str.strip()

        # Remove duplicates
        df_accounts_unique = df_accounts.drop_duplicates()

        # Extract normalized unique account numbers
        account_numbers = df_accounts_unique[ACCOUNT_NO_COL].tolist()

        # Fetch additional details using the SQL query
        df_additional_details = fetch_additional_details(account_numbers, test_flag)

        # Normalize the Account No column in df_additional_details
        df_additional_details[ACCOUNT_NO_COL] = df_additional_details[ACCOUNT_NO_COL].astype(str).str.strip()

        # Print the fetched data for debugging
        print("Merged DataFrame Preview Before Saving:")
        print(df_additional_details.head())

        # Merge the original Excel data with the SQL query results after normalization
        df_merged = pd.merge(df_accounts, df_additional_details, on=ACCOUNT_NO_COL, how='left')

        # Save the updated DataFrame back to Excel
        df_merged.to_excel(excel_file, index=False)

        print(f"Successfully updated {excel_file}")
        
    except Exception as e:
        print(f"An error occurred while populating: {e}")
        traceback.print_exc()  # Print full traceback for debugging
