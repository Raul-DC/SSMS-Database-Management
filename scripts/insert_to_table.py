import pyodbc
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Set the CSV file path relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\data\CSV_Files', os.path.basename(os.getenv('CSV_FILE').strip("'")))  # Use the base filename from the .env CSV_FILE variable

# Connection to SQL Server using environment variables
print("Using SSMS (SQL Server Management Studio) to operate...")
print(f"Connecting to the database '{database}' on server '{server}' with user '{username}'...")
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      f'UID={username};'
                      f'PWD={password}')
print("Connection successful!")

# Create a cursor object to execute SQL commands on the database
cursor = conn.cursor()

# Read the CSV file
print(f"Reading the CSV file at: {csv_file}...")
try:
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        total_records = 0
        records_loaded = 0
        errors = []  # List to store errors

        for row in reader:
            total_records += 1  # Count total processed records
            # Add the current date to the FECHA_COPIA column
            copy_date = datetime.now().strftime('%Y-%m-%d')
            print(f"Processing record {total_records}...")

            try:
                # Ensure that the number of columns matches the table
                print(f"Inserting record {total_records} into the database...")
                cursor.execute(''' 
                    INSERT INTO dbo.Unificado (CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT, MUESTRA, VALOR, ORIGEN, FECHA_COPIA)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                ''', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], copy_date))
                
                records_loaded += 1  # Increment the counter for loaded records
                print(f'Successfully loaded record {total_records}')  # To see the row, add: 'Successfully loaded: {row}'

            except Exception as e:
                errors.append((total_records, str(e)))  # Store the error
                print(f'Error loading record {total_records}: {e}')

    # Commit the changes to the database
    print("Committing changes to the database...")
    conn.commit()
    print(f'\nLoad completed. Total records processed: {total_records}, Records loaded: {records_loaded}.')

    if errors:
        print(f'\nErrors found in {len(errors)} record(s):')
        for record_number, error in errors:
            print(f'Record {record_number}: {error}')
    else:
        print('All records were successfully loaded.')

except Exception as e:
    print(f'Error opening the file {csv_file}: {e}')

finally:
    print("Closing the database connection...")
    conn.close()  # Ensure the connection is closed
    print("Connection closed.")
