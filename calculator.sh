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
    
    #tree_output=$(echo "$ast_output" | head -n 1)  # Capture the tree-like output (first line)
    #json_output=$(echo "$ast_output" | tail -n 1)  # Capture the JSON output (second line)

    if [[ "$ast_output" =~ Error:* ]]; then
        echo "$ast_output"
        continue
    fi

    echo ""
    echo "AST Output: $ast_output"


    solver_output=$(python3 solver.py "$ast_output")

    if [[ "$solver_output" =~ Error:* ]]; then
        echo "$solver_output"
        continue
    fi

    echo ""
    echo "Solver Output: $solver_output"
done
