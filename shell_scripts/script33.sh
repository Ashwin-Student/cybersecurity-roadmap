#!/bin/bash
# Description: Declares an array of 5 Linux distributions and prints the first and last elements.

# Declare an indexed array containing 5 elements
distros=("Ubuntu" "CentOS" "Fedora" "Debian" "Arch")

# Access the first element using index 0
echo "First element: ${distros[0]}"

# Access the last element using negative indexing (-1)
echo "Last element: ${distros[-1]}"
