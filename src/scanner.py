from token_type import TokenType
from tokens import Token

class Scanner:
    def __init__(self, interpreter, source):
        self._interpreter = interpreter
        self._source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1


        self.token_strings = {
            '(': lambda c: TokenType.LEFT_PAREN,
            ')': lambda c: TokenType.RIGHT_PAREN,
            '{': lambda c: TokenType.LEFT_BRACE,
            '}': lambda c: TokenType.RIGHT_BRACE,
            ',': lambda c: TokenType.COMMA,
            '.': lambda c: TokenType.DOT,
            '-': lambda c: TokenType.MINUS,
            '+': lambda c: TokenType.PLUS,
            ';': lambda c: TokenType.SEMICOLON,
            '*': lambda c: TokenType.STAR,
            '!': lambda c: TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG,
            '=': lambda c: TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL,
            '<': lambda c: TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS,
            '>': lambda c: TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER,
            '/': lambda c: self._slash_logic(),
            # Ignore whitespace
            ' ': lambda c: None,
            '\r': lambda c: None,
            '\t': lambda c: None,
            '\n': lambda c: self._advance_line(),
            '"': lambda c: self._string_logic(),
        }


        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'False': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'not': TokenType.NOT,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'True': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE,
        }


    def scan_tokens(self):
        while not self._at_EOF():
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF,'', None, self.line))
        return self.tokens

    def _scan_token(self):
        c = self._advance()
        if c in self.token_strings:
            c = self.token_strings[c](c) #second '(c)' is to actually call the lambda function
            if c:
                self._add_token(c)
        elif c.isdigit():
            self._number_logic()
        elif c.isalpha() or c == '_':
            self._identifier()
        else:
            self._interpreter.error(line=self.line, message="Unexpected character.")
    
    '''
    Moves forward one character
    '''
    def _advance(self):
        self.current += 1
        return self._source[self.current - 1]

    def _add_token(self, TokenType, literal=None):
        raw_string_token = self._source[self.start:self.current]
        self.tokens.append(Token(TokenType, raw_string_token, literal, self.line))


    def _slash_logic(self):
        if self._match('/'): # if the next char is also '/', marking a single line comment:
            # A comment goes until the end of the line so we just keep advancing until we reach the end of the comment
            while (self._peek() != '\n') and not self._at_EOF(): self._advance()
        elif self._match('*'): # if the next char is a '*', marking a multiline comment:
            while not self._is_at_end():
                if self._match('\n'):
                    self.line += 1
                elif self._match('*') and self._match('/'):
                    break
                else:
                    self._advance()
        else:
            self._add_token(TokenType.SLASH)

    def _number_logic(self):
        while(self._peek().isdigit()):
            self._advance()
        
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit(): self._advance()

        self._add_token(TokenType.NUMBER, float(self._source[self.start:self.current]))

    def _string_logic(self):
        while self._peek() != '"' and not self._at_EOF():
            if self._peek() == '\n': self._advance_line()
            self._advance()
        if self._at_EOF():
            self._interpreter.error(line=self.line, message='Unterminated string.')
            return #return needed to avoid throwing out of bounds index when accesing source thru index
        
        self._advance() #consume closing quote char

        value = self._source[self.start+1:self.current-1]
        self._add_token(TokenType.STRING, value)


    def _advance_line(self):
        self.line += 1

    def _peek(self, i=0):
        if self._at_EOF(): return '\0'
        return self._source[self.current + i]         


    def _peek_next(self):
        if self.current + 1 >= len(self._source): return '\0'
        return self._source[self.current + 1]

    '''
    Checks to see if the next character matches expected
    '''
    def _match(self, expected):
        if self._at_EOF():
            return False
        elif self._source[self.current] != expected:
            return False
        else:
            self.current += 1
            return True
    
    def _identifier(self):
        while self._peek().isalnum() or self._peek() == '_': self._advance()

        # if the lexeme is not a keyword, the lexeme is an identifier. Otherwise, return the keyword token type
        text = self._source[self.start:self.current]
        t_type = self.keywords.get(text) # t_type means token type
        if not t_type:
           t_type = TokenType.IDENTIFIER
        
        self._add_token(t_type)

    def _at_EOF(self):
        return self.current >= len(self._source)
    
if __name__ == "__main__":
    with open("/Users/abemankavil/Desktop/toll.txt") as f:
        source = f.read()
    scn = Scanner("fex", source)
    scn.scan_tokens()