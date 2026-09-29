#!/bin/bash

# $1 represents the first positional command-line argument passed to the script.
# The -z flag checks if the string length is zero (i.e., no argument was provided).
if [ -z "$1" ]; then
    echo "Usage: $0 <filename>" # $0 holds the script's own file name
    exit 1                       # Terminate execution with an error status code
fi

# Store the provided command-line argument into a readable variable
filename="$1"

# The -e flag checks if the path/file exists (file, directory, link, etc.)
if [ -e "$filename" ]; then
    echo "File '$filename' exists."
else
    echo "File '$filename' does not exist."
fi
