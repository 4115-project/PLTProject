import re
import sys
import json
from constants import valid_operators, Tokens

sys.stdout.reconfigure(encoding='utf-8')
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
        """Consume the current token and move to the next."""
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
        if token and token[0] == Tokens.EQUAL.value:
            self.consume()
            right = self.parse_expression()
            return ASTNode(Tokens.EQUAL.value, children=[left, right])
        return left

    def parse_term(self):
        left = self.parse_subterm()
        while True:
            token = self.get_current_token()
            if token and token[0] in (Tokens.PLUS.value, Tokens.MINUS.value):
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
            if token and token[0] in (Tokens.MULTIPLY.value, Tokens.DIVIDE.value, Tokens.MODULE.value):
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
            if token and token[0] == Tokens.POWER.value:
                self.consume()
                right = self.parse_factor()
                left = ASTNode(Tokens.POWER.value, children=[left, right])
            else:
                break
        return left

    def parse_factor(self):
        token = self.get_current_token()
        if token and token[0] == Tokens.LPAREN.value:
            self.consume()
            expr = self.parse_expression()
            if not self.match(Tokens.RPAREN.value):
                raise SyntaxError("Expected ')'")
            return expr

        elif token and token[0] in (Tokens.MINUS.value, Tokens.PLUS.value):
            self.consume()
            return ASTNode(token[0], children=[self.parse_factor()])

        elif token and token[0] in (Tokens.INTEGER.value, Tokens.DECIMAL.value):
            self.consume()
            return ASTNode('VAL', value=token[1])
            
        elif token and token[0] in (Tokens.IDENTIFIER.value):
            self.consume()
            return ASTNode('ID', value=token[1])

        raise SyntaxError("Unexpected token: " + str(token[1]))
    
    
    def parse_multiple_expressions(self):
        """Parses multiple expressions separated by whitespace."""
        asts = []
        while self.current_token_index < len(self.tokens):
            ast = self.parse_expression()
            asts.append(ast)
        return asts


def main():
    """Main function for running the parser."""
    if len(sys.argv) > 1:
        token_string = sys.argv[1]
        try:
            # Convert JSON string to list of tokens
            tokens = json.loads(token_string)
            if not isinstance(tokens, list):
                raise ValueError("Tokens must be in a list format.")
            # if sum(1 for token in tokens if token[0] == Tokens.EQUAL.value) != 1:
            #     raise ValueError("Not an equation.")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing tokens: {e}")
            sys.exit(1)
    else:
        print("No tokens provided. Exiting...")
        sys.exit(1)

    parser = Parser(tokens)
    try:
        asts = parser.parse_multiple_expressions()
        combined_tree_representation = ""
        serialized_ast_list = "["
        
        for i, ast in enumerate(asts):
            combined_tree_representation += f"AST {i + 1}:\n"
            combined_tree_representation += f"{ast}\n"
            serialized_ast_list += json.dumps(ast, default=lambda o: o.__dict__)
            if i < len(asts) - 1: 
                serialized_ast_list += ","
            
        print("Combined AST Tree Representation:")
        print(combined_tree_representation.strip()) 
        
        print("---")

        print(serialized_ast_list + "]")
        
    except SyntaxError as e:
        print(f"Syntax error while parsing: {e}")
        sys.exit(1)



if __name__ == "__main__":
    main()
