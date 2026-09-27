1. Print Statements
To output text to the console, use echo (adds a newline by default) or printf (for formatted output).
# Basic echo
echo "Hello, World!"

# Echo without a trailing newline
echo -n "Loading... "

# Formatted printing using printf
printf "Name: %s | Age: %d\n" "Ashwin" 22

2. Variable Declaration
Variables store data. Important: Do not put spaces around the equals sign (=) when assigning values.
# Declaring string and numeric variables
NAME="Linux User"
COUNT=10

# Accessing variables using a dollar sign
echo "Welcome, $NAME. Count is $COUNT."

# Read-only (constant) variable
readonly API_KEY="secret_123"

# Command substitution (storing command output in a variable)
CURRENT_DATE=$(date +%Y-%m-%d)
echo "Today's date is $CURRENT_DATE"


3. Conditional Statements
Use if, elif, and else to control the flow of execution based on conditions.
AGE=20

if [ $AGE -ge 18 ]; then
    echo "You are an adult."
elif [ $AGE -eq 17 ]; then
    echo "Almost there!"
else
    echo "You are a minor."
fi

Common comparison operators:

Numbers: -eq (equal), -ne (not equal), -gt (greater than), -lt (less than)

Strings: = (equal), != (not equal), -z (is empty)

4. Loops
Automate repetitive tasks using for, while, and until loops.

# For loop over a list
for fruit in apple banana cherry; do
    echo "I like $fruit"
done

# For loop with a range
for i in {1..5}; do
    echo "Number: $i"
done

# While loop
COUNTER=1
while [ $COUNTER -le 3 ]; do
    echo "Counter is $COUNTER"
    ((COUNTER++))
done

5. Functions
Encapsulate reusable blocks of code inside functions. Arguments are accessed via $1, $2, etc.

# Defining a function
greet_user() {
    local USER=$1
    echo "Hello, $USER! Welcome aboard."
}

# Calling the function
greet_user "Ashwin"

6. Arithmetic Operations
Perform math operations using double parentheses $(( ... )).

A=10
B=5

SUM=$((A + B))
DIFF=$((A - B))
PROD=$((A * B))
DIV=$((A / B))

echo "Sum: $SUM, Difference: $DIFF, Product: $PROD, Division: $DIV"


8. Command-Line Arguments & Special Variables
Scripts often need inputs passed directly from the terminal when execution begins. Shell provides special built-in variables to handle these:

#!/bin/bash

echo "Script Name: $0"
echo "First Argument: $1"
echo "Second Argument: $2"

echo "Total number of arguments: $# "
echo "All arguments passed: $@"

Special Exit Status ($?): Captures whether the previous command succeeded (0) or failed (non-zero value).

cp file.txt /backup/
if [ $? -eq 0 ]; then
    echo "Copy successful!"
else
    echo "Copy failed!"
fi

9. Error Handling & Strict Mode
Writing robust scripts means failing fast when something goes wrong.

set -e (Exit on Error): Forces the script to immediately exit if any command fails.

set -u (Unset Variables): Treats unset variables as errors and aborts execution.

set -x (Debug Mode): Prints each command before executing it (great for troubleshooting).

#!/bin/bash
set -euo pipefail # Best practice header for robust scripts

echo "Running critical task..."
# If this command fails, the script stops immediately thanks to 'set -e'

10. Arrays
Store multiple values in a single variable.

# Declaring an array
SERVERS=("web-01" "web-02" "db-01")

# Accessing elements
echo "First server: ${SERVERS[0]}"

# Getting all elements
echo "All servers: ${SERVERS[@]}"

# Getting array length
echo "Total servers: ${#SERVERS[@]}"

# Looping through an array
for server in "${SERVERS[@]}"; do
    echo "Pinging $server..."
done

11. File & Directory Checks
Before reading, writing, or deleting files, always verify their existence and permissions using conditional flags:

-e file: True if the file/directory exists.

-f file: True if it is a regular file.

-d dir: True if it is a directory.

-r / -w / -x: True if readable, writable, or executable.

CONFIG_FILE="/etc/myapp.conf"

if [ -f "$CONFIG_FILE" ]; then
    echo "Configuration file found."
else
    echo "Error: Configuration file missing!" >&2
    exit 1
fi
