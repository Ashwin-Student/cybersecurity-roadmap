#!/bin/bash
# Description: Accepts two numbers as arguments, calculates their sum using local scope variables, and prints the result.

add_numbers() {
    # Store passed arguments ($1 and $2) into local variables
    local num1=$1
    local num2=$2
    
    # Perform arithmetic expansion
    local sum=$((num1 + num2))
    
    # Output the result
    echo "The sum is: $sum"
}

# Call the function passing 1 and 2 directly as positional parameters
add_numbers 1 2
