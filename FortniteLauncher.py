import os
import re
import subprocess

# Define the fixed path to the log file
log_file_path = os.path.expandvars(r"%LOCALAPPDATA%\FortniteGame\Saved\Logs\FortniteLauncher.log")

# Check if the log file exists
if not os.path.exists(log_file_path):
    print(f"Log file not found: {log_file_path}")
    exit(1)

# Read the log file content
with open(log_file_path, "r", encoding="utf-8") as log_file:
    log_content = log_file.read()

# Search for the relevant line containing FortniteLauncher.exe
match = re.search(r'\[([A-Za-z]:.*?FortniteLauncher\.exe.*?)\]', log_content)

if match:
    # Extract the full command from the log file
    command = match.group(1)

    # Remove unwanted characters: " and []
    command = command.replace('"', '').replace('[', '').replace(']', '')

    # Extract the directory and executable
    executable_path = command.split(" ")[0]
    working_dir = os.path.dirname(executable_path)

    # Set the working directory
    print(f"Changing working directory to: {working_dir}")
    os.chdir(working_dir)

    # Run the command
    print(f"Running command: {command}")
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Failed to execute the command: {e}")
else:
    print("No match found for FortniteLauncher.exe in the log file.")
