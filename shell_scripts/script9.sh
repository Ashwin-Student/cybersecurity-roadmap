#!/bin/bash
# Question 9: Define two numeric variables and print sum, difference, product, and quotient using $(( )).

NUM1=20
NUM2=5

SUM=$((NUM1 + NUM2))
DIFF=$((NUM1 - NUM2))
PROD=$((NUM1 * NUM2))
DIV=$((NUM1 / NUM2))

echo "Numbers: NUM1=$NUM1, NUM2=$NUM2"
echo "Sum: $SUM"
echo "Difference: $DIFF"
echo "Product: $PROD"
echo "Quotient: $DIV"
