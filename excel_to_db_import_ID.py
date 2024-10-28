# Import the necessary libraries
import pyodbc
import pandas as pd

# Connect to the Azure SQL Database
def connect_to_azure_sql_database():
  server = 'industry-project-database-sever.database.windows.net'
  database = 'Industry-Project-Database'
  username = 'TeamAdmin'
  password = 'P@ssw0rd'   
  driver= '{ODBC Driver 17 for SQL Server}'
  
  connection_string = 'Driver='+driver+';Server=tcp:'+server+',1433;Database='+database+';Uid='+username+';PWD='+password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
  connection = pyodbc.connect(connection_string)
  return connection

# Read the Excel file
def read_excel_file(file_path, sheet_name):
    try:
        # Drop rows with missing essential columns + ensures correct data types
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df = df.dropna(subset=['image_id', 'turtle_id'])
        df = df.astype({'image_id': 'str', 'turtle_id': 'str'})
        return df 
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def insert_s_turtleID(df, connection):
    # SQL INSERT STATEMENTS
    insert_sql_secondaryTurtle = """INSERT INTO Turtle (secondaryTurtleID) VALUES (?);"""
    get_Identity_ID = """SELECT TurtleID FROM Turtle WHERE secondaryTurtleID = ?;""" # Get the IDENTITY turtleID value
    check_duplicate_turtleID = """SELECT COUNT(*) FROM Turtle WHERE secondaryTurtleID = ?;"""  # Check for duplicates

    # Iterate over the DataFrame and insert values into the Turtle table
    identity_image_tuple = []
    try:
        with connection.cursor() as cursor:
            for row in df.itertuples(index=False):
                cursor.execute(check_duplicate_turtleID, row.turtle_id)
                exists = cursor.fetchone()[0]

                
                # If the turtleID does not exist in the Turtle table, insert it
                if exists == 0:
                    cursor.execute(insert_sql_secondaryTurtle, row.turtle_id)
                    cursor.execute(get_Identity_ID, row.turtle_id)   
                    current_turtle_id = cursor.fetchone()[0]
                # If the turtleID exists in the Turtle table, dont insert it
                else:
                    cursor.execute(get_Identity_ID, row.turtle_id)   
                    current_turtle_id = cursor.fetchone()[0]

                # NOTE: Appending image_id with most recent IDENTITY turtleID regardless 
                identity_image_tuple.append((current_turtle_id, row.image_id))
                # print(f"Inserted Tuple: {current_turtle_id, row.image_id}")
        connection.commit()

    except pyodbc.Error as e:
        print(f"Error inserting into Turtle table: {e}")
        connection.rollback()

    # Return IDENTITY turtleID values to be used as a parameter for 'insert_s_imageID' function
    return identity_image_tuple 


def insert_s_imageID(identity_image_tuple, connection):
    insert_sql_secondaryImage = """INSERT INTO Image (turtleID, secondaryImageID) VALUES (?, ?);"""
    check_duplicate_imageID = """SELECT COUNT(*) FROM Image WHERE secondaryImageID = ?;"""  # Check for duplicates

    # Insert excel imageID and their respective turtleID into the Image table
    try:
        with connection.cursor() as cursor:
            for turtle_id, image_id in identity_image_tuple:
                cursor.execute(check_duplicate_imageID, image_id)
                exists = cursor.fetchone()[0]

                if exists == 0:
                    cursor.execute(insert_sql_secondaryImage, turtle_id, image_id)
                else:
                    # print(f"Image ID: {image_id} already exists in the Image table.")
                    pass
        connection.commit() 
    except pyodbc.Error as e:
        print(f"Error inserting into Image table: {e}")
        connection.rollback()

def main():
    file_path = r"C:\Users\Dylan\Documents\ml\data\train.xlsx"
    sheet_name = 'train'
    connection = None  # Initialize to avoid UnboundLocalError if connection fails

    try:
        connection = connect_to_azure_sql_database()

        # Read the Excel file
        df = read_excel_file(file_path, sheet_name=sheet_name)
        if df is not None:
            turtle_ids = insert_s_turtleID(df, connection)
            insert_s_imageID(turtle_ids, connection)

            connection.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()    

# TO DO
# 1. CHANGE FILE PATH TO CORRECT FILE PATH OF EXCEL FILE (LINE 89)
# 2. CHECK SHEET NAME AND COLUMN HEADERS ARE CORRECT (LINE 22, 23, 90)
# 3. RUN THE SCRIPT