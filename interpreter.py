# Token Types
(INTEGER, PLUS, MINUS, MUL, DIV, BIT_NOT, BIT_XOR, BIT_AND, BIT_OR, MOD, INT_DIV, EXP, BIT_LEFT_SHIFT, BIT_RIGHT_SHIFT,
 GREATER, SMALLER, GREATER_OR_EQUALS, SMALLER_OR_EQUALS, EQUALS_TO, EQUALS, NOT_EQUALS_TO, IS, IS_NOT, IN, NOT_IN, NOT,
 AND, OR, EOF) = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'BIT_NOT', 'BIT_XOR', 'BIT_AND', 'BIT_OR', 'MOD', 'INT_DIV', 'EXP',
    'BIT_LEFT_SHIFT', 'BIT_RIGHT_SHIFT', 'GREATER', 'SMALLER', 'GREATER_OR_EQUALS', 'SMALLER_OR_EQUALS', 'EQUALS_TO',
    'EQUALS', 'NOT_EQUALS_TO', 'IS', 'IS_NOT', 'IN', 'IN_NOT', 'NOT', 'AND', 'OR', 'EOF')

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def logical_operator(self):
        result = ''
        while self.current_char and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def logical_or_identity_or_membership(self):
        result = self.logical_operator()
        if result in ('is', 'not') and self.current_char == ' ':
            self.advance()
            result += self.logical_operator()
        tokens = {'is': IS, 'isnot': IS_NOT, 'in': IN, 'notin': NOT_IN, 'and': AND, 'or': OR, 'not': NOT}
        if result in tokens.keys():
            return Token(tokens[result], result)
        self.error()

    def comparison_or_shift(self, character):
        self.advance()
        if character == '<':
            if self.current_char == '<':
                self.advance()
                return Token(BIT_LEFT_SHIFT, '<<')
            if self.current_char == '=':
                self.advance()
                return Token(SMALLER_OR_EQUALS, '<=')
            return Token(SMALLER, '<')
        if character == '>':
            if self.current_char == '>':
                self.advance()
                return Token(BIT_RIGHT_SHIFT, '>>')
            if self.current_char == '=':
                self.advance()
                return Token(GREATER_OR_EQUALS, '>=')
            return Token(GREATER, '>')
        if character == '=':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(EQUALS_TO, '==')
            return Token(EQUALS, '=')
        if character == '!':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return Token(NOT_EQUALS_TO, '!=')
            self.error()
        self.error()

    def mul_or_exp(self):
        self.advance()
        if self.current_char == '*':
            self.advance()
            return Token(EXP, '**')
        return Token(MUL, '*')

    def div_or_int_div(self):
        self.advance()
        if self.current_char == '/':
            self.advance()
            return Token(INT_DIV, '//')
        return Token(DIV, '/')

    def get_next_token(self):
        while self.current_char:
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
            if self.current_char in ('<', '>', '=', '!'):
                return self.comparison_or_shift(self.current_char)
            if self.current_char in ('a', 'i', 'n', 'o'):
                return self.logical_or_identity_or_membership()
            self.error()
        return Token(EOF, None)

class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    @staticmethod
    def sgn(x):
        return (x > 0) - (x < 0)

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return self.exp()
        if token.type == MINUS:
            self.eat(MINUS)
            return -self.exp()
        if token.type == BIT_NOT:
            self.eat(BIT_NOT)
            return ~self.exp()
        if token.type == NOT:
            self.eat(NOT)
            return not self.comparison()
        self.eat(INTEGER)
        return token.value

    def exp(self):
        result = self.factor()
        while self.current_token.type == EXP:
            self.eat(EXP)
            result **= self.factor()
        return result

    def term(self):
        result = self.exp()
        while self.current_token.type in (MUL, DIV, MOD, INT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.term()
            elif token.type == DIV:
                self.eat(DIV)
                result /= self.term()
            elif token.type == MOD:
                self.eat(MOD)
                result %= self.term()
            elif token.type == INT_DIV:
                self.eat(INT_DIV)
                result //= self.term()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

    def shift(self):
        result = self.expr()
        while self.current_token.type in (BIT_LEFT_SHIFT, BIT_RIGHT_SHIFT):
            token = self.current_token
            if token.type == BIT_LEFT_SHIFT:
                self.eat(BIT_LEFT_SHIFT)
                result <<= self.expr()
            elif token.type == BIT_RIGHT_SHIFT:
                self.eat(BIT_RIGHT_SHIFT)
                result >>= self.expr()
        return result

    def bit_and(self):
        result = self.shift()
        while self.current_token.type == BIT_AND:
            self.eat(BIT_AND)
            result &= self.shift()
        return result

    def bit_xor(self):
        result = self.bit_and()
        while self.current_token.type == BIT_XOR:
            self.eat(BIT_XOR)
            result ^= self.bit_and()
        return result

    def bit_or(self):
        result = self.bit_xor()
        while self.current_token.type == BIT_OR:
            self.eat(BIT_OR)
            result |= self.bit_xor()
        return result

    def comparison(self):
        result = self.bit_or()
        while self.current_token.type in (
                EQUALS_TO, NOT_EQUALS_TO, SMALLER_OR_EQUALS, SMALLER, GREATER_OR_EQUALS, GREATER, IS, IS_NOT, IN, NOT_IN):
            token = self.current_token
            if token.type == EQUALS_TO:
                self.eat(EQUALS_TO)
                result = result == self.bit_or()
            elif token.type == NOT_EQUALS_TO:
                self.eat(NOT_EQUALS_TO)
                result = result != self.bit_or()
            elif token.type == SMALLER_OR_EQUALS:
                self.eat(SMALLER_OR_EQUALS)
                result = result <= self.bit_or()
            elif token.type == SMALLER:
                self.eat(SMALLER)
                result = result < self.bit_or()
            elif token.type == GREATER_OR_EQUALS:
                self.eat(GREATER_OR_EQUALS)
                result = result >= self.bit_or()
            elif token.type == GREATER:
                self.eat(GREATER)
                result = result > self.bit_or()
            elif token.type == IS:
                self.eat(IS)
                result = result is self.bit_or()
            elif token.type == IS_NOT:
                self.eat(IS_NOT)
                result = result is not self.bit_or()
            elif token.type == IN:
                self.eat(IN)
                result = result in self.bit_or()
            elif token.type == NOT_IN:
                self.eat(NOT_IN)
                result = result not in self.bit_or()
        return result

    def logical_not(self):
        result = self.comparison()
        while self.current_token.type == NOT:
            self.eat(NOT)
            result = not self.comparison()
        return result

    def logical_and(self):
        result = self.logical_not()
        while self.current_token.type == AND:
            self.eat(AND)
            result = result and self.logical_not()
        return result

    def logical_or(self):
        result = self.logical_and()
        while self.current_token.type == OR:
            self.eat(OR)
            result = result or self.logical_and()
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
        result = interpreter.logical_or()
        print(result)

if __name__ == '__main__':
    main()