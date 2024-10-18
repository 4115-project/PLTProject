# PLT Project (Multilinear Polynomial Calculator)

## Description
This repository contains the code for the COMS 4115 PLT Project, which implements a Multilinear Polynomial Calculator. For comprehensive details about the project, please refer to the [Project Proposal](https://github.com/4115-project/PLTProject/blob/main/assignments/proposal.pdf).

#### Team members: Caiwu Chen(cc4786), Khaliun Gerel(kg3159)

#### Current Stage: Lexical Analysis
The README will be updated to reflect the project's progress as it evolves.

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
4. OPERATOR: ``` + | - | * | / | ^ | % | = | ==```
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
Input: ```4*x^3 +2.3y^2 -45=hello``` <br />
Output: 
```
('INTEGER', '4')
('MULTIPLY', '*')
('IDENTIFIER', 'x')
('POWER', '^')
('INTEGER', '3')
('PLUS', '+')
('DECIMAL', '2.3')
('IDENTIFIER', 'y')
('POWER', '^')
('INTEGER', '2')
('MINUS', '-')
('INTEGER', '45')
('EQUAL', '=')
('IDENTIFIER', 'hello')
```

#### Example 2
Input: ```34x*26y + (hello +1 ) ^1=6 if*2``` <br />
Output: 
```
('INTEGER', '34')
('IDENTIFIER', 'x')
('MULTIPLY', '*')
('INTEGER', '26')
('IDENTIFIER', 'y')
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
('IDENTIFIER', 'if')
('MULTIPLY', '*')
('INTEGER', '2')
```

#### Example 3
Input: ```(x+1=4``` <br />
Output: 
```Error: Unbalanced parenthesis```

#### Example 4
Input: ```3x^2 + $ =1``` <br />
Output: 
```Error: '$' is not recognizable.```

#### Example 5
Input: ```3++3x^2%y-1=0``` <br />
Output: 
```Error: '++' is not a valid operator```
