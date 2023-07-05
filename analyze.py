import datetime
import os
import glob
import configparser

# Read the database configurations from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the instance configurations from the config.ini file
instances = {}
for section in config.sections():
    if section.startswith('instance'):
        instance_name = config[section]['name']
        table_name = config[section]['table']
        instances[table_name] = instance_name

# Get the list of files in the stats/instances directory
file_pattern = os.path.join('stats', 'instances', '*.db')
file_list = glob.glob(file_pattern)

# Process each file
for file_path in file_list:
    file_name = os.path.basename(file_path)
    table_name = os.path.splitext(file_name)[0]

    # Check if the table name exists in the instances configuration
    if table_name in instances:
        instance_name = instances[table_name]
        analyzed_file_path = os.path.join('stats', 'instances', f"analyzed_{table_name}.db")

        # Read the data from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Create a dictionary to store the count for each category
        category_counts = {i: 0 for i in range(59, -1, -1)}

        # Process each line in the file
        analyzed_lines = []
        for line in lines:
            values = line.strip().split('\t')
            if len(values) >= 16:
                first_seen_timestamp = int(values[14])
                expire_timestamp = int(values[2])

                # Calculate the difference in minutes
                diff_minutes = int((expire_timestamp - first_seen_timestamp) / 60)

                # Increment the count for the corresponding category
                if diff_minutes in category_counts:
                    category_counts[diff_minutes] += 1
                    analyzed_lines.append(line)

        # Get the current timestamp
        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a line for the analyzed file
        line = current_timestamp + '\t' + '\t'.join(str(category_counts[i]) for i in range(59, -1, -1)) + '\n'

        # Write the analyzed line to the analyzed file
        try:
            with open(analyzed_file_path, 'a') as file:
                file.write(line)
        except Exception as e:
            print(f"Error writing to {analyzed_file_path}: {e}")
            exit()

        # Delete the original file
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
            exit()

        # Print the summary
        lines_analyzed = len(analyzed_lines)
        print(f"Lines Analyzed in {file_name}: {lines_analyzed}")
        print(f"New entry added successfully to {analyzed_file_path}, and the original file deleted.")
    else:
        print(f"No instance configuration found for table '{table_name}'. Skipping analysis.")

# Print a summary if no files were found
if not file_list:
    print("No files found in the stats/instances directory.")
