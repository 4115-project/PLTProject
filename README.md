# PLT Project (Multilinear Polynomial Calculator)

## Description
This repository contains the code for the COMS 4115 PLT Project, which implements a Multilinear Polynomial Calculator. For comprehensive details about the project, please refer to the [Project Proposal](https://github.com/4115-project/PLTProject/blob/main/assignments/proposal.pdf).

#### Team members: Caiwu Chen(cc4786), Khaliun Gerel(kg3159)

#### Current Stage: Parser
The README will be updated to reflect the project's progress as it evolves.

#### Demo video: https://vimeo.com/1027472571

## Context-Free Grammar
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

## Environment
This project is developed using Python. Run the associated shell scripts on a Linux/Unix operating system.

### Testing Environment
You can use Git bash to test or use Ubuntu and any compatible Linux system to run bash. <br />

### How to Run
To execute the lexer, navigate to the root directory of the project and run the following command:
```bash
$ ./lexer.sh
```

## Lexical grammar
While we anticipate that users will provide valid equations, the calculator includes error handling for invalid symbols or operations. It also checks for correct use of parentheses.
#### Below are the defined tokens along with their corresponding rules:
1. INTEGER: ```[0-9]*```
2. DECIMAL: ```[0-9]*.[0-9]*```
3. IDENTIFIER: ```[a-zA-Z][a-zA-Z0-9]*```
4. OPERATORS: ``` + | - | * | / | ^ | % | = | ==```
   - PLUS: ```+```
   - MINUS: ```-```
   - MULTIPLY: ```*```
   - DIVIDE: ```/```
   - POWER: ```^```
   - MODULE: ```%```
   - EQUAL: ```=```
   - COMPARE: ```==```
5. LPAREN: ```(```
6. RPAREN: ```)```
7. WHITESPACE: ``` ```

## Sample Input Strings:

#### Example 1
Input: ```4*x^3 +2.3*y^2 -45=hello``` <br />
Output: 
```
('INTEGER', '4')
('MULTIPLY', '*')
('IDENTIFIER', 'x')
('POWER', '^')
('INTEGER', '3')
('PLUS', '+')
('DECIMAL', '2.3')
('MULTIPLY', '*')
('IDENTIFIER', 'y')
('POWER', '^')
('INTEGER', '2')
('MINUS', '-')
('INTEGER', '45')
('EQUAL', '=')
('IDENTIFIER', 'hello')
```
#### Example 2
Input: ```34^(x*26%y) + (hello +1 ) ^1=6+if*2``` <br />
Output: 
```
('INTEGER', '34')
('POWER', '^')
('LPAREN', '(')
('IDENTIFIER', 'x')
('MULTIPLY', '*')
('INTEGER', '26')
('MODULE', '%')
('IDENTIFIER', 'y')
('RPAREN', ')')
('PLUS', '+')
('LPAREN', '(')
('IDENTIFIER', 'hello')
('PLUS', '+')
('INTEGER', '1')
('RPAREN', ')')
('POWER', '^')
('INTEGER', '1')
('EQUAL', '=')
('INTEGER', '6')
('PLUS', '+')
('IDENTIFIER', 'if')
('MULTIPLY', '*')
('INTEGER', '2')
```
#### Example 3 
Input: ```(x+1=4``` <br />
Output: 
```
('LPAREN', '(')
('IDENTIFIER', 'x')
('PLUS', '+')
('INTEGER', '1')
('EQUAL', '=')
('INTEGER', '4')
```
#### Example 4 
Input: ```3^2 + $ =1``` <br />
Output: 
```Error: '$' is not recognizable.```
#### Example 5 
Input: ```3++3x^2%y-1=0``` <br />
Output: 
```Error: '++' is not a valid operator```

## Sample Input Programs (AST):

#### Example 1
Input: ```4*x^3 +2.3*y^2 -45=hello``` <br />
AST: 
```
EQUAL
├── MINUS
    ├── PLUS
        ├── MULTIPLY
            ├── VAL (4)
            └── POWER
                ├── VAL (x)
                └── VAL (3)
        └── MULTIPLY
            ├── VAL (2.3)
            └── POWER
                ├── VAL (y)
                └── VAL (2)
    └── VAL (45)
└── VAL (hello)
```
#### Example 2
Input: ```34^(x*26%y) + (hello +1 ) ^1=6+if*2``` <br />
AST:
```
EQUAL
├── PLUS
    ├── POWER
        ├── VAL (34)
        └── MODULE
            ├── MULTIPLY
                ├── VAL (x)
                └── VAL (26)
            └── VAL (y)
    └── POWER
        ├── PLUS
            ├── VAL (hello)
            └── VAL (1)
        └── VAL (1)
└── PLUS
    ├── VAL (6)
    └── MULTIPLY
        ├── VAL (if)
        └── VAL (2)
```
#### Example 3
Input: ```x+10^2.2``` <br />
AST: 
```
Error parsing tokens: Not an equation.
```
### Example 4
Input: ```2*10=y-1^3``` <br />
AST:
```
EQUAL
├── MULTIPLY
    ├── VAL (2)
    └── VAL (10)
└── MINUS
    ├── VAL (y)
    └── POWER
        ├── VAL (1)
        └── VAL (3)
```

### Example 5
Input: ```(2+3)*(4+x)=(10*(4%y)+8)``` <br />
AST:
```
EQUAL
├── MULTIPLY
    ├── PLUS
        ├── VAL (2)
        └── VAL (3)
    └── PLUS
        ├── VAL (4)
        └── VAL (x)
└── PLUS
    ├── MULTIPLY
        ├── VAL (10)
        └── MODULE
            ├── VAL (4)
            └── VAL (y)
    └── VAL (8)
```

### Example 6
Input: ```(x+y+z^(x+1)=1``` <br />
AST: 
```
SyntaxError: Expected ')'
```
