#!/bin/bash
# Question 5: Use command substitution to store current date/time in a variable and print it.

# '$()' or backticks `` captures command output into a variable
CURRENT_DATE=$(date)

echo "System Report Generated At: $CURRENT_DATE"
