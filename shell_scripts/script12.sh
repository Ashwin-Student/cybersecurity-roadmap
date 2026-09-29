#!/bin/bash

# Prompt the user to input an integer
read -p "Enter an integer: " num

# Arithmetic expansion $(( ... )) is used to perform mathematical operations in Bash.
# The modulus operator (%) calculates the remainder of division by 2.
# -eq checks if the result is equal to 0.
if [ $((num % 2)) -eq 0 ]; then
    echo "$num is even."
else
    echo "$num is odd."
fi
