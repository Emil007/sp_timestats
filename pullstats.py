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

# Define the MySQL query
query = """
    SELECT id, size, expire_timestamp, updated, pokemon_id, gender, cp, atk_iv,
    def_iv, sta_iv, form, level, weather, costume, first_seen_timestamp, changed,
    iv, expire_timestamp_verified, is_ditto, shiny, username, is_event, checked
    FROM pokemon
    WHERE (checked = 0 OR checked IS NULL) AND expire_timestamp_verified = 1 AND seen_type = "encounter"
"""

# Execute the query
cursor.execute(query)

# Fetch all the rows returned by the query
rows = cursor.fetchall()

# Check if there are any rows to process
if rows:
    print(f"Found {len(rows)} rows to download.")

    # Open the check.db file in append mode
    with open('pkmn.db', 'a') as file:
        # Process each row
        for row in rows:
            # Write the row values to the file separated by tabs
            file.write('\t'.join(str(value) for value in row) + '\n')

    # Get the IDs of the downloaded rows
    ids = [row[0] for row in rows]

    # Update the checked column for the downloaded rows
    update_query = f"""
        UPDATE pokemon
        SET checked = 1
        WHERE (checked = 0 OR checked IS NULL) AND id IN ({','.join('%s' for _ in ids)})
    """
    cursor.execute(update_query, ids)

    # Commit the changes to the database
    cnx.commit()

    print("Download completed and rows marked as checked.")
else:
    print("No rows found to download.")

# Close the cursor and connection
cursor.close()
cnx.close()
