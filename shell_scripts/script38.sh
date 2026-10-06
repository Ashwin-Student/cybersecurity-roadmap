#!/bin/bash
# Description: Validates whether a backup directory argument was provided on execution.

# Check if the number of passed arguments ($#) is less than 1 (-lt 1)
if [ $# -lt 1 ]; then
    echo "Usage: $0 <backup_directory_path>"
    exit 1
fi

# Assign the first argument ($1) to a variable
backup_dir=$1

# Check if the path actually exists and is a directory
if [ ! -d "$backup_dir" ]; then
    echo "Error: Directory '$backup_dir' does not exist."
    exit 1
fi

echo "Backup directory validated: $backup_dir"
