# Token Types
(INTEGER, PLUS, MINUS, MUL, FLOAT_DIV, BIT_NOT, BIT_XOR, BIT_AND, BIT_OR, MOD, INT_DIV, EXP, BIT_LEFT_SHIFT,
 BIT_RIGHT_SHIFT,
 GREATER, SMALLER, GREATER_OR_EQUALS, SMALLER_OR_EQUALS, EQUALS_TO, EQUALS, NOT_EQUALS_TO, IS, IS_NOT, IN, NOT_IN, NOT,
 AND, OR, LPAREN, RPAREN, EOF) = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'FLOAT_DIV', 'BIT_NOT', 'BIT_XOR', 'BIT_AND', 'BIT_OR', 'MOD', 'INT_DIV', 'EXP',
    'BIT_LEFT_SHIFT', 'BIT_RIGHT_SHIFT', 'GREATER', 'SMALLER', 'GREATER_OR_EQUALS', 'SMALLER_OR_EQUALS', 'EQUALS_TO',
    'EQUALS', 'NOT_EQUALS_TO', 'IS', 'IS_NOT', 'IN', 'IN_NOT', 'NOT', 'AND', 'OR', '(', ')', 'EOF')


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
            self.skip_whitespace()
            result += self.logical_operator()
        tokens = {'is ': IS, 'isnot': IS_NOT, 'in': IN, 'notin': NOT_IN, 'and': AND, 'or': OR, 'not': NOT}
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
            if self.current_char == '=':
                self.advance()
                return Token(EQUALS_TO, '==')
            return Token(EQUALS, '=')
        if character == '!':
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
        return Token(FLOAT_DIV, '/')

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
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            if self.current_char in ('<', '>', '=', '!'):
                return self.comparison_or_shift(self.current_char)
            if self.current_char in ('a', 'i', 'n', 'o'):
                return self.logical_or_identity_or_membership()
            self.error()
        return Token(EOF, None)


class AST:
    pass


class BinaryOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
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

    def factor(self):
        token = self.current_token
        unary = (PLUS, MINUS, BIT_NOT, NOT)
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.logical_or()
            self.eat(RPAREN)
            return node
        elif token.type in unary:
            self.eat(token.type)
            node = UnaryOp(op=token, expr=self.factor())
            return node
        return token.value

    def exp(self):
        node = self.factor()

        while self.current_token.type == EXP:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.factor())

        return node

    def term(self):
        node = self.exp()
        binary = (MUL, FLOAT_DIV, MOD, INT_DIV)

        while self.current_token.type in (MUL, FLOAT_DIV, MOD, INT_DIV):
            token = self.current_token
            if token.type in binary:
                self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.exp())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.term())

        return node

    def shift(self):
        node = self.expr()

        while self.current_token.type in (BIT_LEFT_SHIFT, BIT_RIGHT_SHIFT):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.expr())

        return node

    def bit_and(self):
        node = self.shift()

        while self.current_token.type == BIT_AND:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.shift())

        return node

    def bit_xor(self):
        node = self.bit_and()

        while self.current_token.type == BIT_XOR:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.bit_and())

        return node

    def bit_or(self):
        node = self.bit_xor()
        while self.current_token.type == BIT_OR:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.bit_xor())
        return node

    def comparison(self):
        node = self.bit_or()

        while self.current_token.type in (
                EQUALS_TO, NOT_EQUALS_TO, SMALLER_OR_EQUALS, SMALLER, GREATER_OR_EQUALS, GREATER, IS, IS_NOT, IN,
                NOT_IN):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.bit_or())

        return node

    def logical_not(self):
        node = self.comparison()

        while self.current_token.type == NOT:
            token = self.current_token
            self.eat(token.type)
            node = UnaryOp(op=token, expr=self.comparison())

        return node

    def logical_and(self):
        node = self.logical_not()

        while self.current_token.type == AND:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.logical_not())

        return node

    def logical_or(self):
        node = self.logical_and()

        while self.current_token.type == OR:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.logical_and())

        return node

    def parse(self):
        return self.logical_or()


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinaryOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == INT_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == EXP:
            return self.visit(node.left) ** self.visit(node.right)
        elif node.op.type == BIT_LEFT_SHIFT:
            return self.visit(node.left) << self.visit(node.right)
        elif node.op.type == BIT_RIGHT_SHIFT:
            return self.visit(node.left) >> self.visit(node.right)
        elif node.op.type == GREATER:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == SMALLER:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == GREATER_OR_EQUALS:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == SMALLER_OR_EQUALS:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == EQUALS_TO:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == NOT_EQUALS_TO:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == IS:
            return self.visit(node.left) is self.visit(node.right)
        elif node.op.type == IS_NOT:
            return self.visit(node.left) is not self.visit(node.right)
        elif node.op.type == IN:
            return self.visit(node.left) in self.visit(node.right)
        elif node.op.type == NOT_IN:
            return self.visit(node.left) not in self.visit(node.right)
        elif node.op.type == BIT_AND:
            return self.visit(node.left) & self.visit(node.right)
        elif node.op.type == BIT_XOR:
            return self.visit(node.left) ^ self.visit(node.right)
        elif node.op.type == BIT_OR:
            return self.visit(node.left) | self.visit(node.right)
        elif node.op.type == AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == OR:
            return self.visit(node.left) or self.visit(node.right)

    def visit_UnaryOp(self, node):
        if node.op.type == NOT:
            return not self.visit(node.expr)
        elif node.op.type == BIT_NOT:
            return ~self.visit(node.expr)
        elif node.op.type == PLUS:
            return self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr)

    @staticmethod
    def visit_Num(node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            try:
                text = input('spi> ')
            except NameError:
                text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()
