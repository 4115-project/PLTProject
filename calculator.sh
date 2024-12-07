#!/bin/bash

while true; do
    echo "Enter a string for lexical analysis (type 'exit' to quit):"
    read input_string

    if [ "$input_string" == "exit" ]; then
        echo "Exiting..."
        break
    fi

    tokens=$(python3 lexical.py "$input_string")

    if [[ "$tokens" =~ Error:* ]]; then
        echo "$tokens"
        continue
    fi

    echo ""
    echo "Tokens: $tokens"

    ast_output=$(python3 AST.py "$tokens")
    
    if [[ "$ast_output" =~ Error:* ]]; then
        echo "$ast_output"
        continue
    fi

    tree_output=$(echo "$ast_output" | awk '/---/{exit} {print}')
    json_output=$(echo "$ast_output" | awk '/---/{flag=1;next}flag')

    echo ""
    echo "AST Tree Representation:"
    echo "$tree_output"

    echo ""
    echo "Serialized AST for Solver:"
    echo "$json_output"

    solver_output=$(python3 code_generation.py "$json_output")

    if [[ "$solver_output" =~ Error:* ]]; then
        echo "$solver_output"
        continue
    fi

    echo ""
    echo "Solver Output: $solver_output"
done
