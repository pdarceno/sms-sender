import pyodbc
from datetime import datetime
from constants import (
    CONNECTION_STRING_WRITE_TEST, CONNECTION_STRING_WRITE
)

def execute_sql_from_file(connection_string, sql_file, params):
    # Connect to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Read SQL from file
    with open(sql_file, 'r') as file:
        sql_query = file.read()

    # Execute the SQL query
    cursor.execute(sql_query, params)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()


def diary_write(sql_file, params, test_flag):
    # Since its writing, it should enforce the test and prod, unlike reading
    if test_flag:
        connect_string = CONNECTION_STRING_WRITE_TEST
    else:
        connect_string = CONNECTION_STRING_WRITE

    # insert current date
    params_tuple = list(params)
    params_tuple.insert(1, datetime.now().strftime('%d-%b-%Y'))
    execute_sql_from_file(connect_string, sql_file, params_tuple)
