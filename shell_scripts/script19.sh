#!/bin/bash

# Prompt user for input marks
read -p "Enter marks (0-100): " marks

# Input validation: check if input is a valid non-negative integer
if ! [[ "$marks" =~ ^[0-9]+$ ]]; then
    echo "Error: Please enter a valid non-negative integer."
    exit 1
fi

# Evaluate grades using numerical test flag -ge (Greater than or Equal to)
if [ "$marks" -ge 90 ]; then
    echo "Grade: A"
elif [ "$marks" -ge 75 ]; then
    echo "Grade: B"
elif [ "$marks" -ge 50 ]; then
    echo "Grade: C"
else
    echo "Grade: Fail"
fi


#!/bin/bash
# Shebang line to execute the script using the Bash shell

# Prompt user for input marks
read -p "Enter marks (0-100): " marks

# 1. Input Validation: Check if the input is a valid non-negative integer
if ! [[ "$marks" =~ ^[0-9]+$ ]]; then
    echo "Error: Please enter a valid non-negative integer."
    exit 1
fi

# 2. Case (Switch) Statement with Pattern Matching
case "$marks" in
    # Matches numbers 90 to 99, or 100
    9[0-9]|100)
        echo "Grade: A"
        ;;

    # Matches numbers 75 to 79, or 80 to 89
    7[5-9]|8[0-9])
        echo "Grade: B"
        ;;

    # Matches numbers 50 to 59, 60 to 69, or 70 to 74
    5[0-9]|6[0-9]|7[0-4])
        echo "Grade: C"
        ;;

    # Default Case (*): Matches all other valid integers (0-49 or >100)
    *)
        if [ "$marks" -gt 100 ]; then
            echo "Error: Marks cannot exceed 100."
        else
            echo "Grade: Fail"
        fi
        ;;
esac
