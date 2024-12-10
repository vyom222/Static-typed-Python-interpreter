# Token Types
# EOF - End of File token
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


class Token(object):
    def __init__(self, token_type, value):
        # token type: INTEGER, PLUS, MINUS, or EOF
        self.type = token_type
        # token value: non-negative integer value, '+', '-', or None
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Interpreter(object):
    def __init__(self, text):
        # client string input
        self.text = text
        # index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    # Lexer code
    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            self.error()
        return Token(EOF, None)

    # Interpreter code
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        # return an INTEGER token value
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return self.term()
        if token.type == MINUS:
            self.eat(MINUS)
            return -self.term()
        self.eat(INTEGER)
        return token.value

    def expr(self):
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            match token.type:
                case "PLUS":
                    self.eat(PLUS)
                    result += self.term()
                case "MINUS":
                    self.eat(MINUS)
                    result -= self.term()
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
