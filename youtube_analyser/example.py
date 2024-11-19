import sqlite3
import pandas as pd

# Connect to the SQLite database
DATABASE_NAME = 'youtube_data.db'
conn = sqlite3.connect(DATABASE_NAME)

query1 = "SELECT published_at FROM videos;"
tables1 = pd.read_sql_query(query1, conn)
print(tables1)
# Query to get the list of all tables
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(query, conn)

# Check if tables exist
if not tables.empty:
    print("Tables and their records in the database:\n")
    for table in tables['name']:
        print(f"Table: {table}")
        # Query to fetch all records from the current table
        table_data = pd.read_sql_query(f"SELECT * FROM {table};", conn)
        if table_data.empty:
            print("  No records found in this table.")
        else:
            print(table_data)
        print("\n" + "-"*50 + "\n")
else:
    print("No tables found in the database.")

# Close the connection
conn.close()
