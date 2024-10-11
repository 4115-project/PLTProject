import sys
token_spec= [ 
    ('INTEGER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('Whitespace', r'\s+'),
    ('POWER', r'\^'),
    ('MODULE', r'\%'),
    ('EQUAL', r'\='),
    ('COMPARE', r'\=='),
    ('IDENTIFIER', r'\[a-zA-Z_][a-zA-Z_0-9]*'),
    ('DECIMAL', r'\d+\.\d+')
]

valid_operators = [
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 
    'POWER', 'MODULE', 'EQUAL', 'COMPARE'
]


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

    def run(self):
        while self.advance():
            if self.string[self.position].isspace():
                if self.curtoken and self.pre:
                    self.tokens.append((self.curtoken,self.pre))
                self.curtoken=None
                self.pre=None
            elif self.string[self.position].isdigit():
                if self.curtoken=='IDENTIFIER':
                    self.pre+=self.string[self.position]
                elif self.curtoken=='INTEGER' or self.curtoken=='DECIMAL':
                    self.pre+=self.string[self.position]
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='INTEGER'
                    self.pre=self.string[self.position]
            elif self.string[self.position].isalpha():
                if self.curtoken=='IDENTIFIER':
                    self.pre+=self.string[self.position]
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='IDENTIFIER'
                    self.pre=self.string[self.position]
            elif self.string[self.position]== '.':
                if self.curtoken=='INTEGER':
                    self.curtoken='DECIMAL'
                    self.pre+=self.string[self.position]
                else:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid presentation"
                    self.error=True
                    break

            #operator consideration:
            elif self.string[self.position]=='+':
                if self.curtoken=='IDENTIFIER':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='PLUS'
                    self.pre=self.string[self.position]
                elif self.curtoken=='INTEGER' or self.curtoken=='DECIMAL':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='PLUS'
                    self.pre=self.string[self.position]
                elif self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='PLUS'
                    self.pre=self.string[self.position]
            elif self.string[self.position]=='-':
                if self.curtoken=='IDENTIFIER':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MINUS'
                    self.pre=self.string[self.position]
                elif self.curtoken=='INTEGER' or self.curtoken=='DECIMAL':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MINUS'
                    self.pre=self.string[self.position]
                elif self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MINUS'
                    self.pre=self.string[self.position]
            elif self.string[self.position]=='*':
                if self.curtoken=='IDENTIFIER':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MULTIPLY'
                    self.pre=self.string[self.position]
                elif self.curtoken=='INTEGER' or self.curtoken=='DECIMAL':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MULTIPLY'
                    self.pre=self.string[self.position]
                elif self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MULTIPLY'
                    self.pre=self.string[self.position]

            elif self.string[self.position]=='^':
                if self.curtoken=='IDENTIFIER':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='POWER'
                    self.pre=self.string[self.position]
                elif self.curtoken=='INTEGER' or self.curtoken=='DECIMAL':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='POWER'
                    self.pre=self.string[self.position]
                elif self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='POWER'
                    self.pre=self.string[self.position]

            elif self.string[self.position]=='=':
                if self.curtoken=='IDENTIFIER':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='EQUAL'
                    self.pre=self.string[self.position]
                elif self.curtoken=='INTEGER' or self.curtoken=='DECIMAL':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='EQUAL'
                    self.pre=self.string[self.position]
                elif self.curtoken=='EQUAL':
                    self.curtoken='COMPARE'
                    self.pre+=self.string[self.position]
                elif self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='EQUAL'
                    self.pre=self.string[self.position]
            elif self.string[self.position]=='/':
                if self.curtoken=='IDENTIFIER':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='DIVIDE'
                    self.pre=self.string[self.position]
                elif self.curtoken=='INTEGER' or self.curtoken=='DECIMAL':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='DIVIDE'
                    self.pre=self.string[self.position]
                elif self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='DIVIDE'
                    self.pre=self.string[self.position]
            elif self.string[self.position]=='(':
                if self.curtoken and self.pre:
                    self.tokens.append((self.curtoken,self.pre))
                self.tokens.append(('LPAREN','('))
                self.checkparen+=1
                self.curtoken=None
                self.pre=None
            elif self.string[self.position]==')':
                if self.curtoken and self.pre:
                    self.tokens.append((self.curtoken,self.pre))
                self.tokens.append(('RPAREN',')'))
                self.checkparen-=1
                if self.checkparen<0:
                    self.error=True
                    self.error_msg="See right parenthesis before left."
                    break
                self.curtoken=None
                self.pre=None
            elif self.string[self.position]=='%':
                if self.curtoken=='IDENTIFIER':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MODULE'
                    self.pre=self.string[self.position]
                elif self.curtoken=='INTEGER' or self.curtoken=='DECIMAL':
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MODULE'
                    self.pre=self.string[self.position]
                elif self.curtoken in valid_operators:
                    self.error_msg=f"'{self.pre}{self.string[self.position]}' is not a valid operator"
                    self.error=True
                    break
                else:
                    if self.curtoken and self.pre:
                        self.tokens.append((self.curtoken,self.pre))
                    self.curtoken='MODULE'
                    self.pre=self.string[self.position]
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
    dfa=lexical(input_string)
    dfa.run()
    tokens=dfa.get_tokens()
    if dfa.error==False:
        for i in tokens:
            print(i)
    else:
        print(dfa.get_tokens())
            

