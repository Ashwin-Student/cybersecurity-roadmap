#!/bin/bash
# Description: Calculates base raised to the power of exponent using a recursive function.

power() {
    local base=$1
    local exp=$2

    # Base case: any number to the power of 0 is 1
    if [ "$exp" -le 0 ]; then
        echo 1
        return 0
    fi

    # Recursive step: base * power(base, exp - 1)
    local prev=$(power "$base" $((exp - 1)))
    echo $((base * prev))
}

# Function invocation & example usage
BASE=2
EXP=5

# Capture output using command substitution $()
RESULT=$(power $BASE $EXP)
echo "$BASE^$EXP = $RESULT"
