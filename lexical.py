import sys
import json
from constants import valid_operators, Tokens

class lexical:
    def __init__(self, input_string):
        self.string=input_string
        self.length=len(input_string)
        self.tokens= []
        self.position=-1
        self.pre=None
        self.curtoken=None
        self.error=False
        self.error_msg=None
        self.checkparen=0

    def advance(self):
        self.position+=1
        if self.position >= self.length:
            return False
        else:
            return True

    def tokenAdvance(self, token): 
        if self.curtoken and self.pre:
            self.tokens.append((self.curtoken,self.pre))
        self.curtoken=token
        self.pre=self.string[self.position]

    def run(self):
        while self.advance():
            # Whitespace
            if self.string[self.position].isspace():
                if self.curtoken and self.pre:
                    self.tokens.append((self.curtoken,self.pre))
                self.curtoken=None
                self.pre=None
            # number
            elif self.string[self.position].isdigit():
                if self.curtoken==Tokens.IDENTIFIER.value:
                    self.pre+=self.string[self.position]
                elif self.curtoken==Tokens.INTEGER.value or self.curtoken==Tokens.DECIMAL.value:
                    self.pre+=self.string[self.position]
                else:
                    self.tokenAdvance(Tokens.INTEGER.value)
            # letter
            elif self.string[self.position].isalpha():
                if self.curtoken==Tokens.IDENTIFIER.value:
                    self.pre+=self.string[self.position]
                else:
                    if self.curtoken and self.pre:
                        if self.curtoken in valid_operators:
                            self.tokens.append((self.curtoken,self.pre))
                        else:
                            self.error_msg=f"{self.string[self.position]} is not an operator"
                            self.error=True
                            break
                    self.curtoken=Tokens.IDENTIFIER.value
                    self.pre=self.string[self.position]
            # Dot [.]
            elif self.string[self.position]== '.':
                if self.curtoken==Tokens.INTEGER.value:
                    self.curtoken=Tokens.DECIMAL.value
                    self.pre+=self.string[self.position]
                else:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid presentation"
                    self.error=True
                    break
            # Operator considerations:
            # Plus [+]
            elif self.string[self.position]=='+':
                if self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    self.tokenAdvance(Tokens.PLUS.value)
            # Minus [-]
            elif self.string[self.position]=='-':
                if self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    self.tokenAdvance(Tokens.MINUS.value)
            # Multiply [*]
            elif self.string[self.position]=='*':
                if self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    self.tokenAdvance(Tokens.MULTIPLY.value)
            # Power [^]
            elif self.string[self.position]=='^':
                if self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    self.tokenAdvance(Tokens.POWER.value)
            # Equal [=]
            elif self.string[self.position]=='=':
                if self.curtoken==Tokens.EQUAL.value:
                    self.curtoken=Tokens.COMPARE.value
                    self.pre+=self.string[self.position]
                elif self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    self.tokenAdvance(Tokens.EQUAL.value)
            # Divide [/]
            elif self.string[self.position]=='/':
                if self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    self.tokenAdvance(Tokens.DIVIDE.value)
            # Module [%]
            elif self.string[self.position]=='%':
                if self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    self.tokenAdvance(Tokens.MODULE.value)
            # LPAREN [(]
            elif self.string[self.position]=='(':
                if self.curtoken and self.pre:
                    self.tokens.append((self.curtoken,self.pre))
                self.tokens.append((Tokens.LPAREN.value,'('))
                self.checkparen+=1
                self.curtoken=None
                self.pre=None
            # LPAREN [)]
            elif self.string[self.position]==')':
                if self.curtoken and self.pre:
                    self.tokens.append((self.curtoken,self.pre))
                self.tokens.append((Tokens.RPAREN.value,')'))
                self.checkparen-=1
                if self.checkparen<0:
                    self.error=True
                    self.error_msg="There is a right parenthesis before left parenthesis."
                    break
                self.curtoken=None
                self.pre=None
            else:
                self.error_msg=f"'{self.string[self.position]}' is not recognizable."
                self.error=True
                break

        if self.curtoken and self.pre:
            self.tokens.append((self.curtoken,self.pre))
            self.curtoken=None
            self.pre=None
        if self.checkparen!=0 and self.error==False:
            self.error_msg="Unbalanced parenthesis"
            self.error=True

    def get_tokens(self):
        if not self.error:
            return self.tokens
        else:
            return "Error: " + self.error_msg


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_string = ' '.join(sys.argv[1:])
    else:
        input_string = input("Enter a string for lexical analysis: ")

    dfa = lexical(input_string)
    dfa.run()
    tokens = dfa.get_tokens()
    
    print(json.dumps(tokens))