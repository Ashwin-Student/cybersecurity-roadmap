#!/bin/bash
# Description: Appends a new element to an existing array and prints the updated total count.

# Declare an initial array of Linux distributions
distros=("Ubuntu" "CentOS" "Fedora" "Debian" "Arch")

# Print initial length using ${#array[@]}
echo "Initial total elements: ${#distros[@]}"

# Append a new element to the array using the += operator
distros+=("Manjaro")

# Print the newly added element and updated total count
echo "Appended element: ${distros[-1]}"
echo "Updated total elements: ${#distros[@]}"
