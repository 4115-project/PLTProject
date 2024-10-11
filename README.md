# PLT Project (Multilinear Polynomial Calculator)

## Description
This is the Github Repository of COMS 4115 PLT Project, generating a Multilinear Polynomial Calculator. 
For the details of the project, please refer to [Proposal](https://github.com/4115-project/PLTProject/blob/main/assignments/proposal.pdf). <br />
README is changing according to the stage of the project. Current stage is Lexical analysis.

## Environment and details
The project is using python to generate the calculator. To run shell script please use Linux/unix operating system. <br />
I am using Git bash to test. You can also use Ubuntu or any related system to run bash. <br />
Go to the root directory of the project, run ./lexer:
```bash
$ ./lexer.sh
Enter a string for lexical analysis (type 'exit' to quit):
```

Even though we expect users to input valid equations, we still provide error descriptions if users input invalid symbols or operations. We also check if parentheses are used correctly.

### Lexical grammar
Here are the tokens we defined and their corresponding rules:
1. ('INTEGER', ' [0-9]* ')
2. ('PLUS', '+')
3. ('MINUS', '-')
4. ('MULTIPLY', '*')
5. ('DIVIDE', '/')
6. ('LPAREN', '(')
7. ('RPAREN', ')')
8. ('Whitespace', ' ')
9. ('POWER', '^')
10. ('MODULE', '%')
11. ('EQUAL', '=')
12. ('COMPARE', '==')
13. ('IDENTIFIER', '[a-zA-Z_][a-zA-Z_0-9]*')
14. ('DECIMAL', ' [0-9]* . [0-9]* ')


### Sample input strings:

1. ```4*x^3 +2.3y^2 -45=hello```
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

2. ```34x*26y + (hello +1 ) ^1=6 if*2```
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

3. ```(x+1=4```
   
```Error: Unbalanced parenthesis```

4.  ```3x^2 + $ =1```

```Error: '$' is not recognizable.```

5. ```3++3x^2%y-1=0```

```Error: '++' is not a valid operator```
