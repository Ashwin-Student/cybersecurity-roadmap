#!/bin/bash
# ==============================================================================
# Script Name : 27_read_file_line_by_line.sh
# Description : Reads and processes a text file line-by-line using a while loop.
# Author      : Student / Contributor
# Github Repo : Shell-Scripting-Solutions
# Usage       : ./27_read_file_line_by_line.sh <filename>
# ==============================================================================

# Check if a filename argument was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename="$1"

# Check if the file exists and is a regular file
if [ ! -f "$filename" ]; then
    echo "Error: File '$filename' does not exist."
    exit 1
fi

# Line-by-line reading loop flags:
# - IFS=          : Prevents trimming leading/trailing whitespace
# - read -r line  : Reads raw line without processing backslash escapes
# - || [ -n ... ] : Guarantees processing of the last line even if missing EOF newline
while IFS= read -r line || [ -n "$line" ]; do
    # Process each line (printing with line context)
    echo "$line"
done < "$filename"
