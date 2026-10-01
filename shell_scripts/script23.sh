#!/bin/bash
# ==============================================================================
# Script 23: Rocket Launch Countdown from 10 to 1
# ==============================================================================

echo "--- Script 23: Rocket Launch Countdown ---"

# Initialize the counter variable
count=10

# Execute the loop as long as count is Greater than or Equal to (-ge) 1
while [ $count -ge 1 ]; do
    echo "T-minus $count..."
    
    # Decrement the counter by 1 using arithmetic expansion
    count=$((count - 1))
    
    # Optional: Pause execution for 1 second between ticks
    sleep 1
done

# Output final trigger message after loop completes
echo "🚀 Blastoff!"

echo ""
