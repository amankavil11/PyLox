import token_type
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
            '(': lambda c: token_type.LEFT_PAREN,
            ')': lambda c: token_type.RIGHT_PAREN,
            '{': lambda c: token_type.LEFT_BRACE,
            '}': lambda c: token_type.RIGHT_BRACE,
            ',': lambda c: token_type.COMMA,
            '.': lambda c: token_type.DOT,
            '-': lambda c: token_type.MINUS,
            '+': lambda c: token_type.PLUS,
            ';': lambda c: token_type.SEMICOLON,
            '*': lambda c: token_type.STAR,
            '!': lambda c: token_type.BANG_EQUAL if self._match('=') else token_type.BANG,
            '=': lambda c: token_type.EQUAL_EQUAL if self._match('=') else token_type.EQUAL,
            '<': lambda c: token_type.LESS_EQUAL if self._match('=') else token_type.LESS,
            '>': lambda c: token_type.GREATER_EQUAL if self._match('=') else token_type.GREATER,
            '/': lambda c: self._slash_logic(),
            # Ignore whitespace
            ' ': lambda c: None,
            '\r': lambda c: None,
            '\t': lambda c: None,
            '\n': lambda c: self._advance_line(),
            '"': lambda c: self._string_logic(),
        }

    def scan_tokens(self):
        while not self._at_EOF():
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(token_type.EOF,'', None, self.line))

    def _scan_token(self):
        c = self._advance()
        if c in self.token_strings:
            c = self.token_strings[c](c)
            if c:
                self._add_token(c)
        else:
            self._interpreter.error(line=self.line, message="Unexpected character.")
    
    '''
    Moves forward one character
    '''
    def _advance(self):
        self.current += 1
        return self._source[self.current - 1]

    def _add_token(self, token_type, literal=None):
        raw_string_token = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, raw_string_token, literal, self.line))


    def _slash_logic(self):
        if self._match('/'): # if the next char is also '/', marking a single line comment:
            # A comment goes until the end of the line
            while (self._peek() != '\n') and not self._at_EOF():
                self._advance()            


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
    
    def _at_EOF(self):
        return self.current >= len(self.source)