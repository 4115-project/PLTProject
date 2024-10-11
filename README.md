# PLTProject

## Description
This is the Github Repository of COMS 4115 PLT Project, generating a Multilinear Polynomial Calculator. 
As for the details of the project, please refer to PLT proposal.pdf, which can be found in the root directory. The README is 
changing according to the stage of the project. Currently is lexical analysis task.

## Environment and details
The project is using python to generate the calculator. To run shell script please use Linux/unix system. 
I am using Git bash to test. You can also use Ubuntu or any related system to run bash.
In the directory where lexer.sh located, run ./lexer, you will see:
```bash
$ ./lexer.sh
Enter a string for lexical analysis (type 'exit' to quit):

```
Even though we expect users input valid equation, we still provide error description if users input invalid symbols or operations. If also check if parentheses are used correctly. 

Now You are able to input strings to testify. 

The tokens we define:
    ('INTEGER', '[0-9]*'),
    ('PLUS', '+'),
    ('MINUS', '-'),
    ('MULTIPLY', '*'),
    ('DIVIDE', '/'),
    ('LPAREN', '('),
    ('RPAREN', ')'),
    ('Whitespace', ' '),
    ('POWER', '^'),
    ('MODULE', '%'),
    ('EQUAL', '='),
    ('COMPARE', '=='),
    ('IDENTIFIER', '[a-zA-Z_][a-zA-Z_0-9]*'),
    ('DECIMAL', '[0-9]*.[0-9]*').

Five strings example:
1. 
4*x^3 +2.3y^2 -45=hello

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


2. 
34x*26y + (hello +1 ) ^1=6 if*2

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


3. 
(x+1=4

Error: Unbalanced parenthesis

4. 
3x^2 + $ =1

Error: '$' is not recognizable.

5.
3++3x^2%y-1=0

Error: '++' is not a valid operator
