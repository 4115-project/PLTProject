from enum import Enum

class Tokens(Enum):
    INTEGER = 'INTEGER'
    DECIMAL = 'DECIMAL'
    IDENTIFIER = 'IDENTIFIER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    POWER = 'POWER'
    MODULE = 'MODULE'
    EQUAL = 'EQUAL'
    COMPARE = 'COMPARE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    WHITESPACE = 'WHITESPACE'

valid_operators = [
    Tokens.PLUS.value, Tokens.MINUS.value, Tokens.MULTIPLY.value, Tokens.DIVIDE.value, 
    Tokens.POWER.value, Tokens.MODULE.value, Tokens.EQUAL.value, Tokens.COMPARE.value
]

token_spec= [ 
    (Tokens.INTEGER, r'\d+'),
    (Tokens.DECIMAL, r'\d+\.\d+'),
    (Tokens.IDENTIFIER, r'\[a-zA-Z_][a-zA-Z_0-9]*'),
    (Tokens.PLUS, r'\+'),
    (Tokens.MINUS, r'\-'),
    (Tokens.MULTIPLY, r'\*'),
    (Tokens.DIVIDE, r'/'),
    (Tokens.POWER, r'\^'),
    (Tokens.MODULE, r'\%'),
    (Tokens.EQUAL, r'\='),
    (Tokens.COMPARE, r'\=='),
    (Tokens.LPAREN, r'\('),
    (Tokens.RPAREN, r'\)'),
    (Tokens.WHITESPACE, r'\s+'),
]
