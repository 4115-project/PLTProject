#!/bin/bash


while true; do
    echo "Enter a string for lexical analysis (type 'exit' to quit):"
    read input_string

    if [ "$input_string" == "exit" ]; then
        echo "Exiting..."
        break
    fi

    # Capture tokens from lexical.py
    tokens=$(python3 lexical.py "$input_string")
    
    # Pass tokens to AST.py if no error
    if [[ "$tokens" =~ Error:* ]]; then
        echo "$tokens"
    else
        echo "Tokens: $tokens"
        python3 AST.py "$tokens"
    fi
done
