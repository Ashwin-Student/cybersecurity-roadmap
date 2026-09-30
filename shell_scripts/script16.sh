#!/bin/bash
# Shebang line to execute script with standard Bash shell

# Check if a positional argument ($1) was passed
if [ -z "$1" ]; then
    echo "Usage: $0 <file_or_directory_path>"
    exit 1
fi

target="$1"

# Check if path is a directory using -d
if [ -d "$target" ]; then
    echo "'$target' is a directory."

# Check if path is a regular file using -f
elif [ -f "$target" ]; then
    echo "'$target' is a regular file."

# Fallback check if path exists but is a special file (e.g., link, pipe, socket)
elif [ -e "$target" ]; then
    echo "'$target' exists, but is a special file type."
else
    echo "'$target' does not exist."
fi
