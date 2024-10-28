import pyodbc
import json

# Load JSON data from a file
json_file_path = 'C:\\Users\\Dylan\\Documents\\ml\\working model files\\class_indices_fold3.json'

with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Azure SQL connection details
server = 'industry-project-database-sever.database.windows.net'
database = 'Industry-Project-Database'
username = 'TeamAdmin'
password = 'P@ssw0rd'   
driver= '{ODBC Driver 17 for SQL Server}'

# Establish connection to the Azure SQL Database
conn = pyodbc.connect(
    f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
)
cursor = conn.cursor()

# Create table (if not exists)
table_name = "class_indices"
create_table_query = f"""
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{table_name}')
BEGIN
    CREATE TABLE {table_name} (
        id VARCHAR(255) PRIMARY KEY,
        value INT
    )
END
"""
try:
    cursor.execute(create_table_query)
    print(f"Table '{table_name}' created successfully.")
except pyodbc.Error as e:
    print(f"Error creating table: {e}")

# Insert JSON data into the table
for key, value in json_data.items():
    insert_query = f"INSERT INTO {table_name} (id, value) VALUES (?, ?)"
    try:
        cursor.execute(insert_query, (key, value))
    except pyodbc.IntegrityError:
        print(f"Key '{key}' already exists. Skipping insert.")
    except pyodbc.Error as e:
        print(f"Error inserting data for key '{key}': {e}")

# Commit changes and close connection
conn.commit()
print("Data inserted successfully.")
cursor.close()
conn.close()