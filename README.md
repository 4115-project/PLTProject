# PLT Project (Multilinear Polynomial Calculator)

## Description
This repository contains the code for the COMS 4115 PLT Project, which implements a Multilinear Polynomial Calculator. For comprehensive details about the project, please refer to the [Project Proposal](https://github.com/4115-project/PLTProject/blob/main/assignments/proposal.pdf).

#### Team members: Caiwu Chen(cc4786), Khaliun Gerel(kg3159)

#### Current Stage: Optimization
The README will be updated to reflect the project's progress as it evolves.

#### Demo video: https://vimeo.com/1027472571

## Environment
This project is developed using Python. Run the associated shell scripts on a Linux/Unix operating system.

### Testing Environment
You can use Git bash to test or use Ubuntu and any compatible Linux system to run bash. <br />

### How to Run
To execute the lexer, navigate to the root directory of the project and run the following command:
```bash
pip install -r requirements.txt
./calculator.sh
```

## Context Free Grammar
### Grammar with Ambiguity
```bash
Expression -> Term = Term
Term       -> Term + Term | Term - Term | (Term) | - Term | + Term | Subterm
Subterm    -> Subterm + Subterm | Subterm - Subterm |  Subterm * Subterm | Subterm % Subterm
            | Subterm ^ Subterm | Subterm / Subterm | (Subterm) | Val
Val        -> int | id | decimal

```
### Left-Factored Grammar (Eliminated Left Recursion and Ambiguity)
```bash
Expression -> Term = Term
Term       -> Subterm Term'
Term'      -> + Subterm Term' | - Subterm Term' | ε
Subterm    -> Factor Subterm'
Subterm'   -> + Factor Subterm' | - Factor Subterm' | * Factor Subterm' | / Factor Subterm' 
            | % Factor Subterm' | ^ Factor Subterm' | ε
Factor     -> ( Term ) | - Factor | + Factor | Val
Val        -> int | id | decimal

```
### Terminals and non-terminals
```bash
Terminals: =, +, -, *, /, %, ^, (, ), int, id, decimal
Non-terminals: Expression, Term, Term', Subterm, Subterm', Factor, Val
```

## Lexical grammar
While we anticipate that users will provide valid equations, the calculator includes error handling for invalid symbols or operations. It also checks for correct use of parentheses.

#### Below are the defined tokens along with their corresponding rules:
1. INTEGER: ```[0-9]*```
2. DECIMAL: ```[0-9]*.[0-9]*```
3. IDENTIFIER: ```[a-zA-Z][a-zA-Z0-9]*```
4. OPERATORS: ``` + | - | * | / | ^ | % | = | ==```
   - PLUS: ```+```, MINUS: ```-```, MULTIPLY: ```*```, DIVIDE: ```/```, POWER: ```^```, MODULE: ```%```, EQUAL: ```=```, COMPARE: ```==```
5. LPAREN: ```(```
6. RPAREN: ```)```
7. WHITESPACE: ``` ```

## Code Generation

The Code Generation Phase transforms Abstract Syntax Trees (ASTs) into executable Python code. First, the input expression or AST is parsed and converted into valid Python syntax, supporting basic mathematical operations like addition, subtraction, multiplication, and more. Next, the translated expression is embedded into a predefined Python script template, which includes solver logic for evaluating and finding roots of equations. Finally, the generated Python script is written to a file, making it ready for execution and capable of handling both real and complex roots efficiently.
## Sample

#### Example 1
Input: ```x^2 - 4 = 0``` <br />
Output: 
```
Tokens: [["IDENTIFIER", "x"], ["POWER", "^"], ["INTEGER", "2"], ["MINUS", "-"], ["INTEGER", "4"], ["EQUAL", "="], ["INTEGER", "0"]]

AST Tree Representation:
EQUAL
├── MINUS
    ├── POWER
        ├── ID (x)
        └── VAL (2)
    └── VAL (4)
└── VAL (0)

Serialized AST for Solver:
{"type": "EQUAL", "value": null, "children": [{"type": "MINUS", "value": null, "children": [{"type": "POWER", "value": null, "children": [{"type": "ID", "value": "x", "children": []}, {"type": "VAL", "value": "2", "children": []}]}, {"type": "VAL", "value": "4", "children": []}]}, {"type": "VAL", "value": "0", "children": []}]}

Solver Output: Generated Python Code:

from solver import solve_equation

if __name__ == "__main__":
    python_expression = "(((x ** 2) - 4) - 0)"
    real_roots, complex_roots = solve_equation(python_expression)

    print("Solutions:")
    print(f"Real Roots: {real_roots}")
    print(f"Complex Roots: {complex_roots}")
            
Execution Output:
Stopping root finding: Muller's method did not converge.
Solutions:
Real Roots: [np.float64(-2.0), np.float64(2.0)]
Complex Roots: []
```

#### Example 2
Input: ```x^2-6*x^2+11*x-6=0``` <br />
Output: 
```
Tokens: [["IDENTIFIER", "x"], ["POWER", "^"], ["INTEGER", "2"], ["MINUS", "-"], ["INTEGER", "6"], ["MULTIPLY", "*"], ["IDENTIFIER", "x"], ["POWER", "^"], ["INTEGER", "2"], ["PLUS", "+"], ["INTEGER", "11"], ["MULTIPLY", "*"], ["IDENTIFIER", "x"], ["MINUS", "-"], ["INTEGER", "6"], ["EQUAL", "="], ["INTEGER", "0"]]

AST Tree Representation:
EQUAL
├── MINUS
    ├── PLUS
        ├── MINUS
            ├── POWER
                ├── ID (x)
                └── VAL (2)
            └── MULTIPLY
                ├── VAL (6)
                └── POWER
                    ├── ID (x)
                    └── VAL (2)
        └── MULTIPLY
            ├── VAL (11)
            └── ID (x)
    └── VAL (6)
└── VAL (0)

Serialized AST for Solver:
{"type": "EQUAL", "value": null, "children": [{"type": "MINUS", "value": null, "children": [{"type": "PLUS", "value": null, "children": [{"type": "MINUS", "value": null, "children": [{"type": "POWER", "value": null, "children": [{"type": "ID", "value": "x", "children": []}, {"type": "VAL", "value": "2", "children": []}]}, {"type": "MULTIPLY", "value": null, "children": [{"type": "VAL", "value": "6", "children": []}, {"type": "POWER", "value": null, "children": [{"type": "ID", "value": "x", "children": []}, {"type": "VAL", "value": "2", "children": []}]}]}]}, {"type": "MULTIPLY", "value": null, "children": [{"type": "VAL", "value": "11", "children": []}, {"type": "ID", "value": "x", "children": []}]}]}, {"type": "VAL", "value": "6", "children": []}]}, {"type": "VAL", "value": "0", "children": []}]}

Solver Output: Generated Python Code:

from solver import solve_equation

if __name__ == "__main__":
    python_expression = "(((((x ** 2) - (6 * (x ** 2))) + (11 * x)) - 6) - 0)"
    real_roots, complex_roots = solve_equation(python_expression)

    print("Solutions:")
    print(f"Real Roots: {real_roots}")
    print(f"Complex Roots: {complex_roots}")
            
Execution Output:
Solutions:
Real Roots: [np.float64(1.0)]
Complex Roots: []
```

#### Example 3
Input: ```3*x^4+2*x^2-10=0``` <br />
Output: 
```
Tokens: [["INTEGER", "3"], ["MULTIPLY", "*"], ["IDENTIFIER", "x"], ["POWER", "^"], ["INTEGER", "4"], ["PLUS", "+"], ["INTEGER", "2"], ["MULTIPLY", "*"], ["IDENTIFIER", "x"], ["POWER", "^"], ["INTEGER", "2"], ["MINUS", "-"], ["INTEGER", "10"], ["EQUAL", "="], ["INTEGER", "0"]]

AST Tree Representation:
EQUAL
├── MINUS
    ├── PLUS
        ├── MULTIPLY
            ├── VAL (3)
            └── POWER
                ├── ID (x)
                └── VAL (4)
        └── MULTIPLY
            ├── VAL (2)
            └── POWER
                ├── ID (x)
                └── VAL (2)
    └── VAL (10)
└── VAL (0)

Serialized AST for Solver:
{"type": "EQUAL", "value": null, "children": [{"type": "MINUS", "value": null, "children": [{"type": "PLUS", "value": null, "children": [{"type": "MULTIPLY", "value": null, "children": [{"type": "VAL", "value": "3", "children": []}, {"type": "POWER", "value": null, "children": [{"type": "ID", "value": "x", "children": []}, {"type": "VAL", "value": "4", "children": []}]}]}, {"type": "MULTIPLY", "value": null, "children": [{"type": "VAL", "value": "2", "children": []}, {"type": "POWER", "value": null, "children": [{"type": "ID", "value": "x", "children": []}, {"type": "VAL", "value": "2", "children": []}]}]}]}, {"type": "VAL", "value": "10", "children": []}]}, {"type": "VAL", "value": "0", "children": []}]}

Solver Output: Generated Python Code:

from solver import solve_equation

if __name__ == "__main__":
    python_expression = "((((3 * (x ** 4)) + (2 * (x ** 2))) - 10) - 0)"
    real_roots, complex_roots = solve_equation(python_expression)

    print("Solutions:")
    print(f"Real Roots: {real_roots}")
    print(f"Complex Roots: {complex_roots}")

Execution Output:
Stopping root finding: Muller's method did not converge.
Solutions:
Real Roots: [np.float64(-1.2339319758323726), np.float64(1.233931975819677)]
Complex Roots: [np.complex128(-6.369171856590583e-11-1.4796130534263663j), np.complex128(-1.3788192809727207e-11+1.479613053384749j)]
```

#### Example 4
Input: ```x^2 + = 4``` <br />
Output: 
```
Tokens: [["IDENTIFIER", "x"], ["POWER", "^"], ["INTEGER", "2"], ["PLUS", "+"], ["EQUAL", "="], ["INTEGER", "4"]]

AST Tree Representation:
Syntax error while parsing: Unexpected token: =
```

#### Example 5
Input: ```x^2 %% 4 = 0``` <br />
Output: 
```
"Error: '%%' is not a valid operator"
```


## Optimization

Input: ```(1 * x) + (x ^ 0) = 4``` <br />
Output: ```((x + 1) - 4)``` <br />
```
Tokens: [["LPAREN", "("], ["INTEGER", "1"], ["MULTIPLY", "*"], ["IDENTIFIER", "x"], ["RPAREN", ")"], ["PLUS", "+"], ["LPAREN", "("], ["IDENTIFIER", "x"], ["POWER", "^"], ["INTEGER", "0"], ["RPAREN", ")"], ["EQUAL", "="], ["INTEGER", "4"]]

AST Tree Representation:
EQUAL
├── PLUS
    ├── MULTIPLY
        ├── VAL (1)
        └── ID (x)
    └── POWER
        ├── ID (x)
        └── VAL (0)
└── VAL (4)

Solver Output: Generated Python Code:

from solver import solve_equation

if __name__ == "__main__":
    python_expression = "((x + 1) - 4)"
    real_roots, complex_roots = solve_equation(python_expression)

    print("Solutions:")
    print(f"Real Roots: {real_roots}")
    print(f"Complex Roots: {complex_roots}")
     
Execution Output:
Stopping root finding: Muller's method did not converge.
Solutions:
Real Roots: [np.float64(3.0)]
Complex Roots: []
```

Input: ```1 ^ 4 + 4 - 2 + x = 9``` <br />
Output: ```((3 + x) - 9)``` <br />
```
Tokens: [["INTEGER", "1"], ["POWER", "^"], ["INTEGER", "4"], ["PLUS", "+"], ["INTEGER", "4"], ["MINUS", "-"], ["INTEGER", "2"], ["PLUS", "+"], ["IDENTIFIER", "x"], ["EQUAL", "="], ["INTEGER", "9"]]

AST Tree Representation:
EQUAL
├── PLUS
    ├── MINUS
        ├── PLUS
            ├── POWER
                ├── VAL (1)
                └── VAL (4)
            └── VAL (4)
        └── VAL (2)
    └── ID (x)
└── VAL (9)

Solver Output: Generated Python Code:

from solver import solve_equation

if __name__ == "__main__":
    python_expression = "((3 + x) - 9)"
    real_roots, complex_roots = solve_equation(python_expression)

    print("Solutions:")
    print(f"Real Roots: {real_roots}")
    print(f"Complex Roots: {complex_roots}")

    
Execution Output:
Stopping root finding: Muller's method did not converge.
Solutions:
Real Roots: [np.float64(6.0)]
Complex Roots: []
```

Input: ```2 + x + y * 0 = 0```<br />
Output: ```((2 + x) - 0)```<br />
```
Tokens: [["INTEGER", "2"], ["PLUS", "+"], ["IDENTIFIER", "x"], ["PLUS", "+"], ["IDENTIFIER", "y"], ["MULTIPLY", "*"], ["INTEGER", "0"], ["EQUAL", "="], ["INTEGER", "0"]]

AST Tree Representation:
EQUAL
├── PLUS
    ├── PLUS
        ├── VAL (2)
        └── ID (x)
    └── MULTIPLY
        ├── ID (y)
        └── VAL (0)
└── VAL (0)

Solver Output: Generated Python Code:

from solver import solve_equation

if __name__ == "__main__":
    python_expression = "((2 + x) - 0)"
    real_roots, complex_roots = solve_equation(python_expression)

    print("Solutions:")
    print(f"Real Roots: {real_roots}")
    print(f"Complex Roots: {complex_roots}")
            
Execution Output:
Stopping root finding: Muller's method did not converge.
Solutions:
Real Roots: [np.float64(-2.0)]
Complex Roots: []
```
