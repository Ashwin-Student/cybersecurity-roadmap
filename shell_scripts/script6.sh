#!/bin/bash
# Question 6: Use printf to align and display a student's ID, Name, and Marks in a tabular format.

# Print table headers (%-10s means left-aligned string taking 10 character spaces)
printf "%-10s | %-20s | %-8s\n" "Student ID" "Name" "Marks"
printf "%s\n" "----------------------------------------"

# Print rows with exact formatting (%-20s = string, %-8d = integer)
printf "%-10s | %-20s | %-8d\n" "101" "Ashwin Kumar" 88
printf "%-10s | %-20s | %-8d\n" "102" "Rahul Sharma" 92
