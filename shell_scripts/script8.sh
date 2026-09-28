#!/bin/bash
# Question 8: Demonstrate difference between single quotes and double quotes with variables.

ROLE="CDAC Trainee"

# Double quotes (" "): Expand variables (replaces $ROLE with its actual value)
echo "Double Quotes Output: Welcome, $ROLE"

# Single quotes (' '): Treat everything literally (prints literal text '$ROLE')
echo 'Single Quotes Output: Welcome, $ROLE'
