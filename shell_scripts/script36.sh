#!/bin/bash
# Description: Function that checks the exit status ($?) of the previous command and exits on failure.

check_status() {
    # Capture exit status ($?) immediately before running any other command
    local last_status=$1
    local custom_message=$2

    # A non-zero exit status indicates failure in Linux commands
    if [ "$last_status" -ne 0 ]; then
        echo "[ERROR] $custom_message (Exit Code: $last_status)" >&2
        exit "$last_status"
    fi
}

# Example 1: Command that succeeds
ls /tmp > /dev/null
check_status $? "Failed to list /tmp directory"
echo "Success: /tmp checked successfully."

# Example 2: Command that fails (attempting to list a non-existent directory)
ls /non_existent_folder_123 2> /dev/null
check_status $? "Failed to access directory '/non_existent_folder_123'"

echo "This line will not execute because the script exits above."
