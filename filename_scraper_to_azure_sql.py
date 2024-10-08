"""This script runs a single instance extracting all file names that are IDs and inserting into an SQL database for storage"""


# Import the necessary libraries
import pyodbc
import os

# Connect to the Azure SQL Database
def connect_to_azure_sql_database():
  server = 'industry-project-database-sever.database.windows.net'
  database = 'Industry-Project-Database'
  username = 'TeamAdmin'
  password = 'P@ssw0rd'   
  driver= '{ODBC Driver 18 for SQL Server}'
  
  connection_string = 'Driver='+driver+';Server=tcp:'+server+',1433;Database='+database+';Uid='+username+';PWD='+password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
  connection = pyodbc.connect(connection_string)
  return connection

# Several SQL functions to interact with the database
def show_records(connection, mytable):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + mytable)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# INSERT each record individually
# def insert_sql_statement(connection, sql_insert_statement, myrecord):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(sql_insert_statement, (myrecord,))
#             connection.commit()
#     except Exception as e:
#         print(f"Error inserting record: {myrecord}. Error: {e}.")

# INSERT multiple records at once
def batch_insert(connection, insert_sql_statement, myrecords, batch_size=250, prefix=""):
    try:
        with connection.cursor() as cursor:
            for i in range(0, len(myrecords), batch_size):
                batch = myrecords[i:i + batch_size]
                cursor.executemany(insert_sql_statement, [(record,) for record in batch])
                print(f"\nBatch {i // batch_size} inserted ({prefix}): {len(batch)} records.")
                connection.commit()
    except Exception as e:
        print(f"Error inserting records: {myrecords}. Error: {e}.")

# Function to get the file names from a directory
def get_file_names(directory):
    try:
        file_names = os.listdir(directory)
        return file_names
    except Exception as e:
        print(f"Error accessing directory: {e}")
        return []

def remove_file_extension(file_name):
    return os.path.splitext(file_name)[0]

# SQL INSERT STATEMENTS [ADD more when needed]
insert_statements = {
    "t_id": "INSERT INTO dbo.[Turtle] (secondaryTurtleID) VALUES (?);",
    "id": "INSERT INTO dbo.[Image] (secondaryImageID) VALUES (?);"
}

# Script for scraping word document file names
def file_scraping(directory_path):
    list_of_files = get_file_names(directory_path)
    # print(list_of_files)

    if not list_of_files:
        print("No files found in the directory.")
        return
    
    records = []
    skipped_files = []

    with connect_to_azure_sql_database() as connection:
        for file_name in list_of_files:
            clean_file_name = remove_file_extension(file_name)
            lowercase_file_name = clean_file_name.lower()

            inserted = False
            for prefix, insert_sql in insert_statements.items():
                if lowercase_file_name.startswith(prefix):
                    records.append((insert_sql, clean_file_name))
                    inserted = True
                    #print(f"Inserted ({prefix}): {clean_file_name}")
                    break
            if not inserted:
                skipped_files.append(clean_file_name)
                print(f"Skipped: {clean_file_name}")
        
        for prefix in insert_statements.keys():
            batch_records = [record for sql, record in records if sql == insert_statements[prefix]]
            if batch_records:
                batch_insert(connection, insert_statements[prefix], batch_records, prefix=prefix)
      
            # ALTERNATE CODE TO INSERT ONE RECORD AT A TIME
            # if lowercase_file_name.startswith("t_id"):
            #     insert_sql_statement(connection, insert_turtleID, clean_file_name)
            #     print(f"Inserted (t_id): {clean_file_name}")
            # elif lowercase_file_name.startswith("id"):
            #     insert_sql_statement(connection, insert_imageID, clean_file_name)
            #     print(f"Inserted (id): {clean_file_name}")
            # else:
            #     skipped_files.append(clean_file_name)
            #     print(f"Skipped: {clean_file_name}")
            
    # Print the list of skipped files
    if skipped_files:
        print(f"\nSkipped files:")
        for skipped in skipped_files:
            print(skipped)
    else:
        print("No files were skipped.")
    print("\n")

if __name__ == "__main__":
    directory_path = r"C:\Users\Patst\OneDrive\Documents\[1] University 2.0\2024 Sem 2\ICT342\testDocumentsForScraping"
    file_scraping(directory_path)


# TO DO:
# 1. CHANGE THE DIRECTORY PATH TO THE CORRECT PATH BEFORE USE (line 121)
# 2. REMOVE PRINT STATEMENTS IF NOT NEEDED
# 3. RUN THE SCRIPT

#READ EXCEL FILE