#!/bin/bash

# Prompt the user to enter their age
read -p "Enter your age: " age

# Use the -ge flag (Greater than or Equal to) for numerical comparison
if [ "$age" -ge 18 ]; then
    echo "You are eligible to vote."
else
    echo "You are not eligible to vote yet."
fi
