#!/bin/bash

# Prompt for username and store in variable 'username'
read -p "Username: " username

# The -s flag hides user input from displaying on the screen (ideal for passwords)
read -sp "Password: " password

# Print an empty line so subsequent output starts on a fresh line after the hidden password
echo ""

# Compare string values using '=' and combine logic using '&&' (AND operator)
if [ "$username" = "admin" ] && [ "$password" = "secret123" ]; then
    echo "Login successful! Welcome, $username."
else
    echo "Access denied: Invalid username or password."
fi
