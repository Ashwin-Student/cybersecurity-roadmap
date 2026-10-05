#!/bin/bash
# ==============================================================================
# Script Name : 28_loop_control_break_continue.sh
# Description : Demonstrates 'continue' (skips 5) and 'break' (stops at 8) in a loop.
# Author      : Student / Contributor
# Github Repo : Shell-Scripting-Solutions
# Target Output: 1 2 3 4 6 7
# ==============================================================================

echo "Demonstrating loop execution from 1 to 10:"

for (( i=1; i<=10; i++ ))
do
    # Stop execution when counter reaches 8
    if [ $i -eq 8 ]; then
        echo "Loop stopped at 8 using 'break'."
        break
    fi

    # Skip current iteration when counter equals 5
    if [ $i -eq 5 ]; then
        echo "Skipped number 5 using 'continue'."
        continue
    fi

    # Output current counter value
    echo "Number: $i"
done
