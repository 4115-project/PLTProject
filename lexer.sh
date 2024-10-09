#!/bin/bash

while true; do
    echo "Enter a string for lexical analysis (type 'exit' to quit):"
    read input_string

    if [ "$input_string" == "exit" ]; then
        echo "Exiting..."
        break
    fi

    python3 lexical.py "$input_string"
done
