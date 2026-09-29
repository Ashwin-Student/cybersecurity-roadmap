#!/bin/bash
# The line above (shebang) tells the system to execute this script using the Bash shell.

# Prompt the user for input and save the response into the variable 'num'
read -p "Enter a number: " num

# Perform conditional checks using numerical comparison flags:
# -gt checks if $num is greater than 0
if [ "$num" -gt 0 ]; then
    echo "The number $num is positive."

# -lt checks if $num is less than 0
elif [ "$num" -lt 0 ]; then
    echo "The number $num is negative."

# If it is neither greater than nor less than zero, it must be zero
else
    echo "The number is zero."
fi
