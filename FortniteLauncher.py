import os
import re
import subprocess
import sys

# Check for -s or --silent in command-line arguments
silent_mode = "-s" in sys.argv or "--silent" in sys.argv

# Define the fixed path to the log file
log_file_path = os.path.expandvars(r"%LOCALAPPDATA%\FortniteGame\Saved\Logs\FortniteLauncher.log")

# Function to log messages (only if not in silent mode)
def log_message(message):
    if not silent_mode:
        print(message)

# Check if the log file exists
if not os.path.exists(log_file_path):
    log_message(f"Log file not found: {log_file_path}")
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
    log_message(f"Changing working directory to: {working_dir}")
    os.chdir(working_dir)

    # Run the command
    log_message(f"Running command: {command}")
    try:
        subprocess.run(
            command,
            shell=True,
            stdout=subprocess.DEVNULL if silent_mode else None,
            stderr=subprocess.DEVNULL if silent_mode else None
        )
    except Exception as e:
        if not silent_mode:
            print(f"Failed to execute the command: {e}")
else:
    log_message("No match found for FortniteLauncher.exe in the log file.")
