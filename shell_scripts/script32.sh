#!/bin/bash
# Description: Parses positional arguments ($1, $2, $#, $@) passed from the command line and iterates through them.

# $# gives the total count of command-line arguments passed
echo "Total arguments passed (\$#): $#"

# $@ gives all arguments passed as a list
echo "All arguments combined (\"\$@\"): $@"
echo "-------------------------------------"

# Check if any arguments were provided before processing
if [ $# -eq 0 ]; then
    echo "No arguments provided. Usage: $0 <arg1> <arg2> ..."
    exit 1
fi

# Direct access to individual positional parameters using default fallbacks
echo "First argument (\$1): ${1:-(none)}"
echo "Second argument (\$2): ${2:-(none)}"
echo "-------------------------------------"

# Iterate over all positional parameters using a for loop
echo "Iterating through all arguments:"
index=1
for arg in "$@"; do
    echo "Argument $index: $arg"
    index=$((index + 1))
done
