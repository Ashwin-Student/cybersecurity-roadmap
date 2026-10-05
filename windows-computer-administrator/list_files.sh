#!/bin/bash
# ==============================================================================
# Script Name : 30_list_sh_files.sh
# Description : Loops through current directory and prints only files ending in .sh.
# Author      : Student / Contributor
# Github Repo : Shell-Scripting-Solutions
# ==============================================================================

echo "Searching for '.sh' files in current directory..."
echo "------------------------------------------------"

# Enable nullglob so loop doesn't evaluate literal '*.sh' if no files exist
shopt -s nullglob

found=0

# Loop through all files matching .sh extension pattern
for file in *.sh; do
    # Verify it is a regular file
    if [ -f "$file" ]; then
        echo "Found script: $file"
        found=1
    fi
done

# Output message if no .sh files were located
if [ $found -eq 0 ]; then
    echo "No .sh files found in the current directory."
fi
