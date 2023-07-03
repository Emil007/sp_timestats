import subprocess

# Execute pullstats.py
print("Running pullstats.py...")
pullstats_process = subprocess.Popen(['python3', 'pullstats.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pullstats_output, pullstats_error = pullstats_process.communicate()

# Check for errors in pullstats.py
if pullstats_process.returncode != 0:
    print(f"Error running pullstats.py:\n{pullstats_error.decode()}")
    exit()

# Execute analyze.py
print("Running analyze.py...")
analyze_process = subprocess.Popen(['python3', 'analyze.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
analyze_output, analyze_error = analyze_process.communicate()

# Check for errors in analyze.py
if analyze_process.returncode != 0:
    print(f"Error running analyze.py:\n{analyze_error.decode()}")
    exit()

# Execute sendstats.py
print("Running sendstats.py...")
sendstats_process = subprocess.Popen(['python3', 'sendstats.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
sendstats_output, sendstats_error = sendstats_process.communicate()

# Check for errors in sendstats.py
if sendstats_process.returncode != 0:
    print(f"Error running sendstats.py:\n{sendstats_error.decode()}")
    exit()

print("Stats processing completed successfully.")
