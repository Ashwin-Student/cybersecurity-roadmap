#!/bin/bash

# Check if a file argument was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

file="$1"

# Verify that the file actually exists first
if [ ! -e "$file" ]; then
    echo "Error: File '$file' does not exist."
    exit 1
fi

echo "Permissions for '$file':"

# -r checks if the file has read permission for the current user
if [ -r "$file" ]; then
    echo "  [✓] Readable (-r)"
else
    echo "  [✗] Not Readable"
fi

# -w checks if the file has write permission for the current user
if [ -w "$file" ]; then
    echo "  [✓] Writable (-w)"
else
    echo "  [✗] Not Writable"
fi

# -x checks if the file has execute permission for the current user
if [ -x "$file" ]; then
    echo "  [✓] Executable (-x)"
else
    echo "  [✗] Not Executable"
fi
