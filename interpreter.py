# Token Types

(INTEGER, PLUS, MINUS, MUL, FLOAT_DIV, BIT_NOT, BIT_XOR, BIT_AND, BIT_OR, MOD, INT_DIV, EXP, BIT_LEFT_SHIFT,
 BIT_RIGHT_SHIFT,
 GREATER, SMALLER, GREATER_OR_EQUALS, SMALLER_OR_EQUALS, EQUALS_TO, NOT_EQUALS_TO, IS, IS_NOT, IN, NOT_IN, NOT,
 AND, OR, LPAREN, RPAREN, ASSIGN, ID, SEMI, DOT, NEWLINE, IF, WHILE, FOR, DEF, COLON, COMMA, EOF) = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'FLOAT_DIV', 'BIT_NOT', 'BIT_XOR', 'BIT_AND', 'BIT_OR', 'MOD', 'INT_DIV', 'EXP',
    'BIT_LEFT_SHIFT', 'BIT_RIGHT_SHIFT', 'GREATER', 'SMALLER', 'GREATER_OR_EQUALS', 'SMALLER_OR_EQUALS', 'EQUALS_TO',
    'NOT_EQUALS_TO', 'IS', 'IS_NOT', 'IN', 'NOT_IN', 'NOT', 'AND', 'OR', '(', ')', 'ASSIGN', 'ID', 'SEMI',
    'DOT', 'NEWLINE', 'IF', 'WHILE', 'FOR', 'DEF', 'COLON', 'COMMA', 'EOF')


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


RESERVED_KEYWORDS = {
    'and': Token(AND, 'and'),
    'or': Token(OR, 'or'),
    'not': Token(NOT, 'not'),
    'is': Token(IS, 'is'),
    'is not': Token(IS_NOT, 'is not'),
    'in': Token(IN, 'in'),
    'not in': Token(NOT_IN, 'not in'),
    'if': Token(IF, 'if'),
    'while': Token(WHILE, 'while'),
    'for': Token(FOR, 'for'),
    'def': Token(DEF, 'def'),
    'int': Token('INT', 'int'),
    'float': Token('FLOAT', 'float'),
    'var': Token('VAR', 'var'),
    'str': Token('STR', 'str'),
    'bool': Token('BOOL', 'bool'),
}


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

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a (multi-digit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while (
                    self.current_char is not None and
                    self.current_char.isdigit()
            ):
                result += self.current_char
                self.advance()
        if self.current_char == 'f':
            self.advance()
            token = Token('FLOAT_CONST', float(result))
        elif '.' not in result:
            token = Token('INT_CONST', int(result))
        else:
            token = None
            self.error()

        return token

    def _id(self):
        result = ''
        while self.current_char and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        while self.current_char or self.current_char == '\n':
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.number()
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                if self.peek() == '*':
                    self.advance()
                    self.advance()
                    return Token(EXP, '**')
                self.advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                if self.peek() == '/':
                    self.advance()
                    self.advance()
                    return Token(INT_DIV, '//')
                self.advance()
                return Token(FLOAT_DIV, '/')
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
            if self.current_char == '>':
                if self.peek() == '>':
                    self.advance()
                    self.advance()
                    return Token(BIT_RIGHT_SHIFT, '>>')
                elif self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(GREATER_OR_EQUALS, '>=')
                self.advance()
                return Token(GREATER, '>')
            if self.current_char == '<':
                if self.peek() == '<':
                    self.advance()
                    self.advance()
                    return Token(BIT_LEFT_SHIFT, '<<')
                elif self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(SMALLER_OR_EQUALS, '<=')
                self.advance()
                return Token(SMALLER, '<')
            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(EQUALS_TO, '==')
                self.advance()
                return Token(ASSIGN, '=')
            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(NOT_EQUALS_TO, '!=')
            if self.current_char == ';':
                self.advance()
                return Token('SEMI', ';')
            if self.current_char == ':':
                self.advance()
                return Token('COLON', ':')
            if self.current_char == ',':
                self.advance()
                return Token('COMMA', ',')
            if self.current_char.isalpha():
                return self._id()

            # if self.current_char in ('<', '>', '=', '!'):
            #     return self.comparison_or_shift(self.current_char)
            # if self.current_char in ('a', 'i', 'n', 'o'):
            #     return self.logical_or_identity_or_membership()
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


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class VarDeclaration(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):
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

    def program(self):
        node = self.compound_statement()
        return node

    def variable_declaration(self):
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_node = Var(self.current_token)  # first ID
        self.eat(ID)
        self.eat(COLON)
        type_node = self.type_spec()
        var_declarations = VarDeclaration(var_node, type_node)

        return var_declarations

    def type_spec(self):
        """type_spec : INT
                     | FLOAT
        """
        token = self.current_token
        if self.current_token.type == "INT":
            self.eat('INT')
        elif self.current_token.type == "FLOAT":
            self.eat('FLOAT')
        elif self.current_token.type == "VAR":
            self.eat('VAR')
        node = Type(token)
        return node

    def compound_statement(self):
        nodes = self.statement_list()
        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        """statement_list : statement (NEWLINE statement)*"""
        node = self.statement()
        results = [node]

        while self.current_token.type == 'SEMI':
            self.eat('SEMI')
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        """statement : compound_statement | simple_statement"""
        if self.current_token.type in (DEF, IF, WHILE, FOR):
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable_declaration()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.logical_or()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    @staticmethod
    def empty():
        """An empty production"""
        return NoOp()

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
        elif token.type == 'INT_CONST':
            self.eat('INT_CONST')
            return Num(token)
        elif token.type == 'FLOAT_CONST':
            self.eat('FLOAT_CONST')
            return Num(token)
        elif token.type in unary:
            self.eat(token.type)
            node = UnaryOp(op=token, expr=self.factor())
            return node
        else:
            node = self.variable()
            return node

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
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')


class Symbol(object):
    def __init__(self, name, var_type=None):
        self.name = name
        self.type = var_type


class VarSymbol(Symbol):
    def __init__(self, name, var_type):
        super().__init__(name, var_type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('int'))
        self.define(BuiltinTypeSymbol('float'))

    def __str__(self):
        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self._symbols.values()]
        )
        return s

    __repr__ = __str__

    def define(self, symbol):
        # print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        # print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        # 'symbol' is either an instance of the Symbol class or 'None'
        return symbol


# class SymbolTableBuilder(NodeVisitor):
#     def __init__(self):
#         self.symtab = SymbolTable()
#
#     def visit_Program(self, node):
#         self.visit(node.block)
#
#     def visit_BinaryOp(self, node):
#         self.visit(node.left)
#         self.visit(node.right)
#
#     def visit_Num(self, node):
#         pass
#
#     def visit_UnaryOp(self, node):
#         self.visit(node.expr)
#
#     def visit_Compound(self, node):
#         for child in node.children:
#             self.visit(child)
#
#     def visit_NoOp(self, node):
#         pass
#
#     def visit_Assign(self, node):
#         var_name = node.left.var_node.value
#         type_symbol = node.left.type_node.value
#         var_type = VarSymbol(var_name, type_symbol)
#         if var_type == 'var':
#             var_type = type(var_value).__name__
#         self.symtab.define(var_type)
#         self.visit(node.right)
#
#     def visit_Var(self, node):
#         var_name = node.value
#         var_type = self.symtab.lookup(var_name)
#
#         if var_type is None:
#             raise NameError(repr(var_name))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_MEMORY = {}
        self.symtab = SymbolTable()

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

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.var_node.value
        type_symbol = node.left.type_node.value
        var_value = self.visit(node.right)
        if type_symbol == 'var':
            type_symbol = type(var_value).__name__
        var_type = VarSymbol(var_name, type_symbol)
        self.symtab.define(var_type)
        self.GLOBAL_MEMORY[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_MEMORY.get(var_name)
        var_type = self.symtab.lookup(var_name)
        if var_type is None:
            raise NameError(repr(var_name))
        return val

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    # while True:
        # try:
        #     try:
        #         text = input('spi> ')
        #     except NameError:
        #         text = input('spi> ')
        # except EOFError:
        #     break
        # if not text:
        #     continue
        text = '''a: var = 5f
        b: int = 5
        c: int = a + b / 5 * 10
        d: float = a // c'''
        text = text.replace('\n', ';')
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(interpreter.GLOBAL_MEMORY)
        print(interpreter.symtab._symbols)


if __name__ == '__main__':
    main()
