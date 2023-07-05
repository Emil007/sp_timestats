import mysql.connector
import configparser
import os
import glob

# Read the database credentials from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
host = config.get('mysql', 'host')
database = config.get('mysql', 'database')

# Establish a connection to the MySQL server
cnx = mysql.connector.connect(
    user=user,
    password=password,
    host=host,
    database=database
)

# Create a cursor object to interact with the database
cursor = cnx.cursor()

# Get the list of analyzed files in the stats/instances directory
file_pattern = os.path.join('stats', 'instances', 'analyzed_*.db')
file_list = glob.glob(file_pattern)

# Process each analyzed file
for file_path in file_list:
    file_name = os.path.basename(file_path)
    table_name = file_name[9:-3]  # Extract table name from the file name

    # Read the line from the analyzed file
    try:
        with open(file_path, 'r') as file:
            line = file.readline().strip()
    except Exception as e:
        print(f"Error reading from {file_path}: {e}")
        exit()

    # Check if the line is empty
    if not line:
        print(f"No data found in {file_path}.")
        continue

    # Split the line into values
    values = line.split('\t')[1:]  # Exclude the timestamp

    # Prepare the INSERT query for the specified table
    insert_query = f"""
        INSERT INTO {table_name} (
            s59, s58, s57, s56, s55, s54, s53, s52, s51, s50,
            s49, s48, s47, s46, s45, s44, s43, s42, s41, s40,
            s39, s38, s37, s36, s35, s34, s33, s32, s31, s30,
            s29, s28, s27, s26, s25, s24, s23, s22, s21, s20,
            s19, s18, s17, s16, s15, s14, s13, s12, s11, s10,
            s9, s8, s7, s6, s5, s4, s3, s2, s1, s0
        ) VALUES (
            {','.join(values)}
        )
    """

    # Execute the INSERT query
    try:
        cursor.execute(insert_query)
        cnx.commit()
    except Exception as e:
        print(f"Error executing INSERT query for {table_name}: {e}")
        exit()

    # Delete the analyzed file
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
        exit()

    print(f"Data uploaded successfully from {file_path} and file deleted.")

# Print a summary if no analyzed files were found
if not file_list:
    print("No analyzed files found in the stats/instances directory.")
