#!/bin/bash
# ==============================================================================
# Script 25: Calculate the Factorial of a Number
# ==============================================================================

echo "--- Script 25: Factorial Calculator ---"

# Prompt the user for an integer
read -p "Enter a non-negative integer: " num

# Initialize accumulator variable to 1 (identity value for multiplication)
factorial=1

# Input Validation: Ensure the number is not negative
if [ "$num" -lt 0 ]; then
    echo "Error: Factorial is undefined for negative numbers."
    exit 1
fi

# C-style for loop to multiply numbers from 1 up to 'num'
for ((i=1; i<=num; i++)); do
    # Multiply current factorial accumulator by loop counter
    factorial=$((factorial * i))
done

# Print final computed result
echo "The factorial of $num ($num!) is: $factorial"
