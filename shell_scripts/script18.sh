#!/bin/bash

# Prompt the user to enter any character or string
read -p "Enter a character or string: " input_str

# The -z flag returns true if the length of the string is zero (empty)
if [ -z "$input_str" ]; then
    echo "The entered string is EMPTY."
else
    echo "The entered string is NOT empty. Value: '$input_str'"
    echo "Length of input: ${#input_str} character(s)."
fi
