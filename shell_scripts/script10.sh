#!/bin/bash
# Question 10: Take user input for radius and calculate area of a circle using floating-point arithmetic (bc).

read -p "Enter the radius of the circle: " radius

# Bash cannot handle decimals directly, so we pipe math into 'bc' (Basic Calculator)
# 'scale=2' specifies 2 decimal places in the output
area=$(echo "scale=2; 3.14159 * $radius * $radius" | bc)

echo "The area of the circle with radius $radius is: $area"
