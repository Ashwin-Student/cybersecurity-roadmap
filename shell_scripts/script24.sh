#!/bin/bash
# ==============================================================================
# Script 24: Loop until user types 'exit'
# ==============================================================================

echo "--- Script 24: Interactive Exit Loop ---"

# Initialize the input variable to prevent unexpected state
user_input=""

# An 'until' loop runs as long as the test condition remains FALSE.
# It terminates as soon as the condition evaluates to TRUE (when user inputs 'exit').
until [ "$user_input" = "exit" ]; do
    # Prompt user for input and save response in 'user_input' variable
    read -p "Type 'exit' to terminate the script: " user_input
done

echo "[+] Correct input received. Script terminated successfully."

echo ""
