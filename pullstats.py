import mysql.connector
import configparser
import os

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
    SELECT p.id, p.size, p.expire_timestamp, p.updated, p.pokemon_id, p.gender, p.cp, p.atk_iv,
    p.def_iv, p.sta_iv, p.form, p.level, p.weather, p.costume, p.first_seen_timestamp, p.changed,
    p.iv, p.expire_timestamp_verified, p.is_ditto, p.shiny, p.username, p.is_event, p.checked,
    d.uuid, d.instance_name
    FROM pokemon p
    JOIN device d ON p.username = d.account_username
    WHERE (p.checked = 0 OR p.checked IS NULL)
        AND p.expire_timestamp_verified = 1
        AND p.seen_type = "encounter"
"""

# Execute the query
cursor.execute(query)

# Fetch all the rows returned by the query
rows = cursor.fetchall()

# Check if there are any rows to process
if rows:
    print(f"Found {len(rows)} rows to download.")

    # Create the 'stats/instances' directory if it doesn't exist
    os.makedirs('stats/instances', exist_ok=True)

    # Get the instance configurations from the config.ini file
    instances = {}
    for section in config.sections():
        if section.startswith('instance'):
            instance_name = config[section]['name']
            table_name = config[section]['table']
            instances[instance_name] = table_name

    # Process each row
    for row in rows:
        # Get the instance name from the row
        instance_name = row[-1]

        # Check if the instance exists in the config.ini file
        if instance_name in instances:
            # Get the table name for the instance
            table_name = instances[instance_name]

            # Construct the file path
            file_path = os.path.join('stats/instances', f"{table_name}.db")

            # Open the instance-specific file in append mode
            with open(file_path, 'a') as file:
                # Convert the row values to a tab-separated string
                row_values = '\t'.join(str(value) for value in row)

                # Write the row values to the file
                file.write(row_values + '\n')

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
