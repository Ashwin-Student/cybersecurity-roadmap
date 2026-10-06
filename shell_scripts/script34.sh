#!/bin/bash
# Description: Loops through the Linux distribution array and outputs the character length of each distro name.

# Declare the array of Linux distros
distros=("Ubuntu" "CentOS" "Fedora" "Debian" "Arch")

# Iterate over every element in the array
# "${distros[@]}" safely expands each array element
for distro in "${distros[@]}"; do
    # ${#variable} returns the length (character count) of the string variable
    echo "$distro: ${#distro} characters"
done
