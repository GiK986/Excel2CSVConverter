import pandas as pd
import pyodbc

import utils
from logger import Logger

logger = Logger(log_file=utils.get_log_file())


def find_duplicate_first_column_rows(df):
    """Returns rows where the first column is duplicated"""
    first_col = df.iloc[:, 0]  # Assuming the first column is at index 0
    duplicate_mask = first_col.duplicated(keep=False)
    return df[duplicate_mask]


def log_duplicate_rows(df):
    logger.warning("Duplicate rows: \n" + df.to_string(index=True))


def find_special_second_column_rows(df):
    """Returns rows where the second column is 0, NaN or empty string"""
    second_col = df.iloc[:, 1]  # Assuming the second column is at index 1
    special_mask = (second_col == 0) | (pd.to_numeric(second_col, errors="coerce").isna()) | (second_col == "")
    return df[special_mask]


def log_special_rows(df):
    logger.warning("Rows where the second column is 0, NaN or empty string: \n" + df.to_string(index=True))


def get_connection_string():
    connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={utils.get_server_name()};Database={utils.get_database_name()};UID={utils.get_database_user()};PWD={utils.get_database_password()};TrustServerCertificate=yes;"
    return connection_string


def find_nonexistent_items(df):
    """Returns rows where the first column is not found in the database"""
    connection_string = get_connection_string()
    try:
        connection = pyodbc.connect(connection_string)
    except Exception as e:
        message = f"Error: connecting to the database: {e}"
        logger.error(message)
        return
    cursor = connection.cursor()

    # Create a temporary table to hold the Excel data
    temp_table_name = "#TempItems"
    create_temp_table_query = f"CREATE TABLE {temp_table_name} (ItemName NVARCHAR(255))"
    cursor.execute(create_temp_table_query)

    # Insert the Excel data into the temporary table
    insert_data_query = f"INSERT INTO {temp_table_name} (ItemName) VALUES (?)"
    for item in df.iloc[:, 0]:
        cursor.execute(insert_data_query, item)

    # Query to find nonexistent items
    query = f"""
    SELECT DISTINCT 
           t.ItemName
    FROM #TempItems t
         LEFT JOIN [TecCatDB_AutoBroker].[dbo].[Items] i 
            ON t.ItemName = i.Provider_Number AND i.IS_Type_ID = 2
    WHERE i.Article_Number IS NULL;
    """

    cursor.execute(query)
    nonexistent_items = [item[0] for item in cursor.fetchall()]

    # Drop the temporary table
    drop_temp_table_query = f"DROP TABLE {temp_table_name}"
    cursor.execute(drop_temp_table_query)

    cursor.close()
    connection.close()
    filtered_df = df[df.iloc[:, 0].isin(nonexistent_items)]

    return filtered_df


def log_nonexistent_items(not_existing_items):
    logger.warning("Nonexistent items: \n" + not_existing_items.to_string(index=True))
