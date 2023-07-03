import datetime
import os

# Read the pkmn.db file
with open('pkmn.db', 'r') as file:
    lines = file.readlines()

# Create a dictionary to store the count for each category
category_counts = {i: 0 for i in range(59, -1, -1)}

# Process each line in the pkmn.db file
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

# Create a line for the stats.db file
line = current_timestamp + '\t' + '\t'.join(str(category_counts[i]) for i in range(59, -1, -1)) + '\n'

# Write the line to the stats.db file
try:
    with open('stats.db', 'a') as file:
        file.write(line)
except Exception as e:
    print(f"Error writing to stats.db: {e}")
    exit()

# Move the analyzed lines to archive.db
try:
    with open('archive.db', 'a') as file:
        for line in analyzed_lines:
            file.write(line)
except Exception as e:
    print(f"Error writing to archive.db: {e}")
    exit()

# Remove the analyzed lines from pkmn.db
try:
    with open('pkmn.db', 'w') as file:
        file.writelines(lines[len(analyzed_lines):])
except Exception as e:
    print(f"Error removing lines from pkmn.db: {e}")
    exit()

# Get the number of lines analyzed and archived
lines_analyzed = len(analyzed_lines)
lines_archived = len(analyzed_lines)

# Print the summary
print(f"Lines Analyzed: {lines_analyzed}")
print(f"Lines Archived to archive.db: {lines_archived}")
print("New entry added successfully to stats.db, and lines archived.")
