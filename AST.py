import re
import sys
import json

# Class representing a node in the Abstract Syntax Tree
class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children else []


    def __repr__(self, level=0, is_last=False):
        prefix = "    " * (level - 1) + ("└── " if is_last else "├── " if level > 0 else "")
        ret = f"{prefix}{self.type}"
        if self.value:
            ret += f" ({self.value})"
        ret += "\n"
        
        for i, child in enumerate(self.children):
            ret += child.__repr__(level + 1, is_last=(i == len(self.children) - 1))
        return ret


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def get_current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def consume(self):
        #if self.current_token_index < len(self.tokens):
        #    print(f"Consuming token: {self.tokens[self.current_token_index]}")
        self.current_token_index += 1

    def match(self, token_type):
        token = self.get_current_token()
        if token and token[0] == token_type:
            self.consume()
            return token
        return None

    def parse_expression(self):
        left = self.parse_term()
        token = self.get_current_token()
        if token and token[0] == 'EQUAL':
            self.consume()  
            right = self.parse_expression()  
            return ASTNode('EQUAL', children=[left, right])
        return left  

    def parse_term(self):
        left = self.parse_subterm()
        while True:
            token = self.get_current_token()
            if token and token[0] in ('PLUS', 'MINUS'):
                self.consume()
                right = self.parse_subterm()
                left = ASTNode(token[0], children=[left, right])
            else:
                break
        return left

    def parse_subterm(self):
        left = self.parse_exponent()
        while True:
            token = self.get_current_token()
            if token and token[0] in ('MULTIPLY', 'DIV', 'MOD'):
                self.consume()
                right = self.parse_exponent()
                left = ASTNode(token[0], children=[left, right])
            else:
                break
        return left

    def parse_exponent(self):
        left = self.parse_factor()
        while True:
            token = self.get_current_token()
            if token and token[0] == 'POWER':
                self.consume()
                right = self.parse_factor()
                left = ASTNode('POWER', children=[left, right])
            else:
                break
        return left

    def parse_factor(self):
        token = self.get_current_token()
        
        if token and token[0] == 'LPAREN':
            self.consume()
            expr = self.parse_expression()
            if not self.match('RPAREN'):
                raise SyntaxError("Expected ')'")
            return expr

        elif token and token[0] in ('MINUS', 'PLUS'):
            self.consume()
            return ASTNode(token[0], children=[self.parse_factor()])

        elif token and token[0] in ('INTEGER', 'IDENTIFIER', 'DECIMAL'):
            self.consume()
            return ASTNode('VAL', value=token[1])

        raise SyntaxError("Unexpected token: " + str(token))

if __name__ == "__main__":
    test_tokens = [
    ('INTEGER', '34'),
    ('MULTIPLY', '*'),
('IDENTIFIER', 'x'),
('MULTIPLY', '*'),
('INTEGER', '26'),
('MULTIPLY', '*'),
('IDENTIFIER', 'y'),
('PLUS', '+'),
('LPAREN', '('),
('IDENTIFIER', 'hello'),
('PLUS', '+'),
('INTEGER', '1'),
('RPAREN', ')'),
('POWER', '^'),
('INTEGER', '1'),
('EQUAL', '='),
('INTEGER', '6'),
('IDENTIFIER', 'if'),
('MULTIPLY', '*'),
('INTEGER', '2'),
]
    if len(sys.argv) > 1:
        token_string = sys.argv[1]
        
        try:
            # Convert JSON string to list of tokens
            tokens = json.loads(token_string)
            if not isinstance(tokens, list):
                raise ValueError("Tokens must be in a list format.")
            if sum(1 for token in tokens if token[0] == 'EQUAL') != 1:
                raise ValueError("Not a Multilinear Polynomial Equation.")

        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing tokens: {e}")
            sys.exit(1)

    else:
        print("No tokens provided. Exiting...")
        sys.exit(1)

    parser = Parser(tokens)
    ast = parser.parse_expression()  
    print(ast)  