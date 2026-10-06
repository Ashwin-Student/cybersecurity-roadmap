#!/bin/bash
# Description: Parses command-line flags (-u for username, -p for port) using getopts.

# Initialize default values
username=""
port=""

# Options u: and p: expect argument values after the flags
while getopts "u:p:" opt; do
    case "$opt" in
        u)
            username=$OPTARG
            ;;
        p)
            port=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            echo "Usage: $0 -u <username> -p <port>"
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

# Validate required flags were passed
if [ -z "$username" ] || [ -z "$port" ]; then
    echo "Error: Both -u <username> and -p <port> options are required."
    echo "Example: $0 -u admin -p 8080"
    exit 1
fi

echo "Successfully parsed arguments:"
echo "Username : $username"
echo "Port     : $port"
