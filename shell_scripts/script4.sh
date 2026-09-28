#!/bin/bash
# Question 4: Create a read-only (constant) variable named VERSION set to 1.0.0 and attempt to change its value.

# 'readonly' makes the variable immutable (constant)
readonly VERSION="1.0.0"
echo "Current Version: $VERSION"

echo "Attempting to change VERSION to 2.0.0..."
# This assignment will throw a read-only variable error and exit/fail
VERSION="2.0.0"

echo "This line will not execute if the script fails above."
