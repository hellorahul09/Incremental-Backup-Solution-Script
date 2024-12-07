import os
import shutil
import datetime

# Function to perform incremental backup
def incremental_backup(source_folder, backup_folder):
    # Get today's date for backup folder naming
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    backup_path = os.path.join(backup_folder, f"backup_{today}")

    # Check if the backup folder already exists, if not, create it
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    # If previous backup exists, get a list of modified or new files
    previous_backup = get_previous_backup(backup_folder)
    
    # Compare the source folder with the previous backup
    if previous_backup:
        print(f"Performing incremental backup based on {previous_backup}")
        new_files = compare_directories(source_folder, previous_backup)
    else:
        # If no previous backup, copy all files
        print("Performing initial full backup.")
        new_files = get_all_files(source_folder)
    
    # Perform the copy of changed/new files
    for file in new_files:
        source_file = os.path.join(source_folder, file)
        dest_file = os.path.join(backup_path, file)
        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        shutil.copy2(source_file, dest_file)  # copy2 to preserve timestamps
        print(f"Backed up: {file}")

# Function to get the most recent backup folder
def get_previous_backup(backup_folder):
    backups = [f for f in os.listdir(backup_folder) if f.startswith('backup_')]
    if not backups:
        return None
    backups.sort(reverse=True)  # Sort to get the most recent backup
    return os.path.join(backup_folder, backups[0])

# Function to compare directories and get changed/new files
def compare_directories(source_dir, backup_dir):
    diff_files = []
    source_files = get_all_files(source_dir)
    backup_files = get_all_files(backup_dir)
    
    # Get files that are new or modified
    for file in source_files:
        if file not in backup_files or file_is_modified(source_dir, backup_dir, file):
            diff_files.append(file)
    
    return diff_files

# Function to get a list of all files in a directory (recursively)
def get_all_files(directory):
    all_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(dirpath, filename), directory)
            all_files.append(file_path)
    return all_files

# Function to check if a file is modified
def file_is_modified(source_dir, backup_dir, file):
    source_file = os.path.join(source_dir, file)
    backup_file = os.path.join(backup_dir, file)
    
    # Compare modification times
    if not os.path.exists(backup_file):
        return True  # File is new
    return os.path.getmtime(source_file) > os.path.getmtime(backup_file)

# Main function to process multiple source-destination pairs
def backup_multiple_locations(pairs):
    for source, destination in pairs:
        print(f"Starting backup from {source} to {destination}")
        if not os.path.exists(source):
            print(f"Source folder {source} does not exist. Skipping.")
            continue
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)
        incremental_backup(source, destination)
        print(f"Backup from {source} to {destination} completed.\n")

# Example usage with multiple source-destination pairs
source_destination_pairs = [
    (r"\\192.168.1.1\DocumentServer", r"E:\Backup Files\DocumentServer"),
    (r"\\192.168.1.2\TallyServer", r"E:\Backup Files\TallyServer")
]


backup_multiple_locations(source_destination_pairs)
