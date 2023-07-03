import mysql.connector
import configparser

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

# Read the line from stats.db
try:
    with open('stats.db', 'r') as file:
        line = file.readline().strip()
except Exception as e:
    print(f"Error reading from stats.db: {e}")
    exit()

# Check if the line is empty
if not line:
    print("No data found in stats.db.")
    exit()

# Split the line into values
values = line.split('\t')[1:]  # Exclude the timestamp

# Prepare the INSERT query for timestats table
insert_query = f"""
    INSERT INTO timestats (
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
    print(f"Error executing INSERT query: {e}")
    exit()

# Remove the line from stats.db
try:
    with open('stats.db', 'r') as file:
        lines = file.readlines()
    with open('stats.db', 'w') as file:
        file.writelines(lines[1:])
except Exception as e:
    print(f"Error removing line from stats.db: {e}")
    exit()

# Add a copy of the line to statsarchive.db
try:
    with open('statsarchive.db', 'a') as file:
        file.write(line + '\n')
except Exception as e:
    print(f"Error writing to statsarchive.db: {e}")
    exit()

print("Data uploaded successfully and line deleted from stats.db.")
