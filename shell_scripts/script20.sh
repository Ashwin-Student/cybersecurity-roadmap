#!/bin/bash

# Prompt user for a number
read -p "Enter a number: " num

# Input validation: check if the input is an integer (positive or negative)
if ! [[ "$num" =~ ^-?[0-9]+$ ]]; then
    echo "Error: Please enter a valid integer."
    exit 1
fi

# Use logical AND (&&) to check if both condition 1 AND condition 2 are met.
# Use logical OR (||) for control flow execution depending on the outcome.

[ "$num" -ge 1 ] && [ "$num" -le 100 ] && echo "Success: $num is between 1 and 100 inclusive." || echo "Out of Range: $num is NOT between 1 and 100."
