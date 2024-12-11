# Token Types
# EOF - End of File token
INTEGER, PLUS, MINUS, MUL, DIV, BIT_NOT, BIT_XOR, BIT_AND, BIT_OR, MOD, INT_DIV, EXP, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'BIT_NOT', 'BIT_XOR', 'BIT_AND', 'BIT_OR', 'MOD', 'INT_DIV', 'EXP', 'EOF')


class Token(object):
    def __init__(self, token_type, value):
        # token type: INTEGER, PLUS, MINUS, or EOF
        self.type = token_type
        # token value: non-negative integer value, or operates, or None
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

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

    def mul_or_exp(self):
        self.advance()
        if self.current_char == '*':
            self.advance()
            if self.current_char == '*':
                self.error()
                return Token(EOF, None)
            return Token(EXP, '**')
        return Token(MUL, '*')

    def div_or_int_div(self):
        self.advance()
        if self.current_char == '/':
            self.advance()
            if self.current_char == '/':
                self.error()
                return Token(EOF, None)
            return Token(INT_DIV, '//')
        return Token(DIV, '/')

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
            if self.current_char == '*':
                return self.mul_or_exp()
            if self.current_char == '/':
                return self.div_or_int_div()
            if self.current_char == '~':
                self.advance()
                return Token(BIT_NOT, '~')
            if self.current_char == '^':
                self.advance()
                return Token(BIT_XOR, '^')
            if self.current_char == '&':
                self.advance()
                return Token(BIT_AND, '&')
            if self.current_char == '|':
                self.advance()
                return Token(BIT_OR, '|')
            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')
            self.error()
        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # client string input
        # index into self.text
        # current token instance
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    @staticmethod
    def sgn(x):
        return (x > 0) - (x < 0)

    def factor(self):
        token = self.current_token
        match token.type:
            case "PLUS":
                self.eat(PLUS)
                return self.factor()
            case "MINUS":
                self.eat(MINUS)
                return -self.factor()
            case "BIT_NOT":
                self.eat(BIT_NOT)
                return ~self.factor()
        self.eat(INTEGER)
        return token.value

    def exp(self):
        result = self.factor()
        while self.current_token.type == EXP:
            self.eat(EXP)
            result = self.sgn(result) * abs(result) ** self.factor()
        return result

    def term(self):
        # return an INTEGER token value
        result = self.exp()
        while self.current_token.type in (MUL, DIV, MOD, INT_DIV):
            token = self.current_token
            match token.type:
                case "MUL":
                    self.eat(MUL)
                    result *= self.term()
                case "DIV":
                    self.eat(DIV)
                    result /= self.term()
                case "MOD":
                    self.eat(MOD)
                    result %= self.term()
                case "INT_DIV":
                    self.eat(INT_DIV)
                    result //= self.term()
        return result

    def expr(self):
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
        interpreter = Interpreter(Lexer(text))
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
