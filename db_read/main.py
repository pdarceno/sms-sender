import pandas as pd
from sqlalchemy import create_engine
import os
import traceback

# Function to load the SQL query from a file
def load_sql_query(file_path):
    with open(file_path, 'r') as file:
        query = file.read()
    return query

# Function to run SQL query for account numbers
def fetch_additional_details(account_numbers, test_flag):
    # Set up the connection string (adjust for your database configuration)
    if test_flag:
        # connection_string = "mssql+pyodbc://devsqlraf01/IA_RB2?driver=SQL+Server&trusted_connection=yes"
        connection_string = "mssql+pyodbc://SYDSQLRAF/IA?driver=SQL+Server&trusted_connection=yes"
    else:
        connection_string = "mssql+pyodbc://SYDSQLRAF/IA?driver=SQL+Server&trusted_connection=yes"
    
    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)

    # Convert list of account numbers into a string formatted for SQL IN clause
    formatted_account_numbers = ', '.join(f"'{account}'" for account in account_numbers)
    
    # Load the query from the SQL file, always relative to this script's directory
    sql_path = os.path.join(os.path.dirname(__file__), 'select_all.sql')
    query = load_sql_query(sql_path)
    
    # Inject the account numbers into the query
    query = query.replace('{account_numbers_placeholder}', formatted_account_numbers)
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
        if 'Account No' not in df_accounts.columns:
            raise Exception("Excel file must contain a column named 'Account No'.")
        df_accounts = df_accounts[['Account No']]

        # Normalize the Account No column (strip spaces, ensure strings)
        df_accounts['Account No'] = df_accounts['Account No'].astype(str).str.strip()

        # Remove duplicates
        df_accounts_unique = df_accounts.drop_duplicates()

        # Extract normalized unique account numbers
        account_numbers = df_accounts_unique['Account No'].tolist()

        # Fetch additional details using the SQL query
        df_additional_details = fetch_additional_details(account_numbers, test_flag)

        # Normalize the Account No column in df_additional_details
        df_additional_details['Account No'] = df_additional_details['Account No'].astype(str).str.strip()

        # Print the fetched data for debugging
        print("Merged DataFrame Preview Before Saving:")
        print(df_additional_details.head())

        # Merge the original Excel data with the SQL query results after normalization
        df_merged = pd.merge(df_accounts, df_additional_details, on='Account No', how='left')

        # Save the updated DataFrame back to Excel
        df_merged.to_excel(excel_file, index=False)

        print(f"Successfully updated {excel_file}")
        
    except Exception as e:
        print(f"An error occurred while populating: {e}")
        traceback.print_exc()  # Print full traceback for debugging
