#!/bin/bash
# ==============================================================================
# Script 21: Print numbers from 1 to 10 using a for loop
# ==============================================================================

echo "--- Script 21: Number Counter (1 to 10) ---"

# Use brace expansion {1..10} to iterate through the range sequentially
for i in {1..10}; do
    # Print the current loop index
    echo "Number: $i"
done

echo ""
