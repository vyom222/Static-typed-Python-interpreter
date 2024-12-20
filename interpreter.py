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
    """
    A class to represent a token.

    Attributes:
    ----------
    type : str
        The type of the token (e.g., INTEGER, PLUS, etc.)
    value : any
        The value of the token (e.g., 3, '+', etc.)
    """

    def __init__(self, token_type: str, value):
        """
        Constructs all the necessary attributes for the token object.

        Parameters:
        ----------
        token_type : str
            The type of the token
        value : any
            The value of the token
        """
        self.type = token_type
        self.value = value

    def __repr__(self):
        """
        Returns a string representation of the token.

        Returns:
        -------
        str
            A string representation of the token
        """
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
    'NoneType': Token('NONE-TYPE', 'NoneType'),
    'True': Token('BOOLEAN_CONST', 'True'),
    'False': Token('BOOLEAN_CONST', 'False'),
    'None': Token('NONE-TYPE_CONST', 'None')
}


class Lexer:
    """
    A class to represent a lexer (lexical analyzer).

    Attributes:
    ----------
    text : str
        The input text to be tokenized
    pos : int
        The current position in the input text
    current_char : str
        The current character being processed
    """

    def __init__(self, text: str):
        """
        Constructs all the necessary attributes for the lexer object.

        Parameters:
        ----------
        text : str
            The input text to be tokenized
        """
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, character: str):
        """
        Raises a syntax error for an invalid character.

        Parameters:
        ----------
        character : str
            The invalid character that caused the error

        Raises:
        ------
        Exception
            An exception indicating a syntax error
        """
        raise Exception(f"SyntaxError: invalid character '{character}' (U+{hex(ord(character))[2:].upper()})")

    def advance(self):
        """
        Advances the `pos` pointer and updates the `current_char` attribute.
        """
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        """
        Peeks at the next character in the input text without advancing the `pos` pointer.

        Returns:
        -------
        str
            The next character in the input text
        """
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        """
        Skips whitespace characters in the input text.
        """
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self):
        """
        Returns a (multi-digit) integer or float consumed from the input.

        Returns:
        -------
        Token
            A token representing an integer or float
        """
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
            self.error(self.current_char)

        return token

    def string(self, target: str):
        """
        Returns a string token consumed from the input.

        Parameters:
        ----------
        target : str
            The delimiter character for the string (e.g., '"' or "'")

        Returns:
        -------
        Token
            A token representing a string
        """
        result = ''
        while self.current_char != target:
            result += self.current_char
            self.advance()
        self.advance()
        token = Token('STRING_CONST', result)
        return token

    def _id(self):
        """
        Returns an identifier token or a reserved keyword token consumed from the input.

        Returns:
        -------
        Token
            A token representing an identifier or a reserved keyword
        """
        result = ''
        while self.current_char and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        """
        Returns an identifier token or a reserved keyword token consumed from the input.

        Returns:
        -------
        Token
            A token representing an identifier or a reserved keyword
        """
        while self.current_char or self.current_char == '\n':
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.number()
            if self.current_char == '"':
                self.advance()
                return self.string('"')
            if self.current_char == "'":
                self.advance()
                return self.string("'")
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
            self.error(self.current_char)
        return Token(EOF, None)


class AST:
    """
    A base class for all nodes in the abstract syntax tree (AST).
    """
    pass


class BinaryOp(AST):
    """
    A class to represent a binary operation node in the AST.

    Attributes:
    ----------
    left : AST
        The left operand of the binary operation
    op : Token
        The operator token of the binary operation
    right : AST
        The right operand of the binary operation
    """

    def __init__(self, left, op, right):
        """
        Constructs all the necessary attributes for the binary operation node.

        Parameters:
        ----------
        left : AST
            The left operand of the binary operation
        op : Token
            The operator token of the binary operation
        right : AST
            The right operand of the binary operation
        """
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(AST):
    """
    A class to represent a unary operation node in the AST.

    Attributes:
    ----------
    op : Token
        The operator token of the unary operation
    expr : AST
        The operand of the unary operation
    """

    def __init__(self, op, expr):
        """
        Constructs all the necessary attributes for the unary operation node.

        Parameters:
        ----------
        op : Token
            The operator token of the unary operation
        expr : AST
            The operand of the unary operation
        """
        self.token = self.op = op
        self.expr = expr


class Float(AST):
    """
    A class to represent a float constant node in the AST.

    Attributes:
    ----------
    token : Token
        The token representing the float constant
    value : float
        The value of the float constant
    """

    def __init__(self, token):
        """
        Constructs all the necessary attributes for the float constant node.

        Parameters:
        ----------
        token : Token
            The token representing the float constant
        """
        self.token = token
        self.value = token.value


class Integer(AST):
    """
    A class to represent an integer constant node in the AST.

    Attributes:
    ----------
    token : Token
        The token representing the integer constant
    value : int
        The value of the integer constant
    """

    def __init__(self, token):
        """
        Constructs all the necessary attributes for the integer constant node.

        Parameters:
        ----------
        token : Token
            The token representing the integer constant
        """
        self.token = token
        self.value = token.value


class String(AST):
    """
    A class to represent a string constant node in the AST.

    Attributes:
    ----------
    token : Token
        The token representing the string constant
    value : str
        The value of the string constant
    """

    def __init__(self, token):
        """
        Constructs all the necessary attributes for the string constant node.

        Parameters:
        ----------
        token : Token
            The token representing the string constant
        """
        self.token = token
        self.value = token.value


class Boolean(AST):
    """
    A class to represent a boolean constant node in the AST.

    Attributes:
    ----------
    token : Token
        The token representing the boolean constant
    value : bool
        The value of the boolean constant
    """

    def __init__(self, token):
        """
        Constructs all the necessary attributes for the boolean constant node.

        Parameters:
        ----------
        token : Token
            The token representing the boolean constant
        """
        self.token = token
        self.value = bool(token.value)


class NoneType(AST):
    """
    A class to represent a NoneType constant node in the AST.

    Attributes:
    ----------
    token : Token
        The token representing the NoneType constant
    value : None
        The value of the NoneType constant
    """

    def __init__(self, token):
        """
        Constructs all the necessary attributes for the NoneType constant node.

        Parameters:
        ----------
        token : Token
            The token representing the NoneType constant
        """
        self.token = token
        self.value: None = None


class Compound(AST):
    """
    A class to represent a compound statement node in the AST.

    Attributes:
    ----------
    children : list
        A list of child nodes representing the statements in the compound statement
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the compound statement node.
        """
        self.children: list = []


class Assign(AST):
    """
    A class to represent an assignment statement node in the AST.

    Attributes:
    ----------
    left : Var
        The variable being assigned a value
    op : Token
        The assignment operator token
    right : AST
        The expression representing the value being assigned
    """

    def __init__(self, left, op, right):
        """
        Constructs all the necessary attributes for the assignment statement node.

        Parameters:
        ----------
        left : Var
            The variable being assigned a value
        op : Token
            The assignment operator token
        right : AST
            The expression representing the value being assigned
        """
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """
    A class to represent a variable node in the AST.

    Attributes:
    ----------
    token : Token
        The token representing the variable
    value : str
        The name of the variable
    """

    def __init__(self, token):
        """
        Constructs all the necessary attributes for the variable node.

        Parameters:
        ----------
        token : Token
            The token representing the variable
        """
        self.token = token
        self.value = token.value


class NoOp(AST):
    """
    A class to represent a no-operation (empty) statement node in the AST.
    """
    pass


class VarDeclaration(AST):
    """
    A class to represent a variable declaration node in the AST.

    Attributes:
    ----------
    var_node : Var
        The variable being declared
    type_node : Type
        The type of the variable being declared
    """

    def __init__(self, var_node, type_node):
        """
        Constructs all the necessary attributes for the variable declaration node.

        Parameters:
        ----------
        var_node : Var
            The variable being declared
        type_node : Type
            The type of the variable being declared
        """
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):
    """
    A class to represent a type node in the AST.

    Attributes:
    ----------
    token : Token
        The token representing the type
    value : str
        The name of the type
    """

    def __init__(self, token):
        """
        Constructs all the necessary attributes for the type node.

        Parameters:
        ----------
        token : Token
            The token representing the type
        """
        self.token = token
        self.value = token.value


class Parser:
    """
    A class to represent a parser (syntax analyzer).

    Attributes:
    ----------
    lexer : Lexer
        The lexer (lexical analyzer) to tokenize the input text
    current_token : Token
        The current token being processed
    """

    def __init__(self, lexer):
        """
        Constructs all the necessary attributes for the parser object.

        Parameters:
        ----------
        lexer : Lexer
            The lexer (lexical analyzer) to tokenize the input text
        """
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        """
        Raises a syntax error for an invalid syntax.

        Raises:
        ------
        Exception
            An exception indicating a syntax error
        """
        raise Exception('SyntaxError: invalid syntax')

    def eat(self, token_type: str):
        """
        Consumes the current token if it matches the expected token type and advances to the next token.

        Parameters:
        ----------
        token_type : str
            The expected type of the current token
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """
        Parses a program node.

        Returns:
        -------
        Compound
            The root node of the program
        """
        node = self.compound_statement()
        return node

    def variable_declaration(self):
        """
        Parses a variable declaration node.

        Returns:
        -------
        VarDeclaration
            The variable declaration node
        """
        var_node = Var(self.current_token)  # first ID
        self.eat(ID)
        self.eat(COLON)
        type_node = self.type_spec()
        var_declarations = VarDeclaration(var_node, type_node)

        return var_declarations

    def type_spec(self):
        """
        Parses a type specification node.

        Returns:
        -------
        Type
            The type specification node
        """
        token = self.current_token
        if self.current_token.type == "INT":
            self.eat('INT')
        elif self.current_token.type == "FLOAT":
            self.eat('FLOAT')
        elif self.current_token.type == "STR":
            self.eat('STR')
        elif self.current_token.type == "BOOL":
            self.eat('BOOL')
        elif self.current_token.type == "NONE-TYPE":
            self.eat('NONE-TYPE')
        elif self.current_token.type == "VAR":
            self.eat('VAR')
        node = Type(token)
        return node

    def compound_statement(self):
        """
        Parses a compound statement node.

        Returns:
        -------
        Compound
            The compound statement node
        """
        nodes = self.statement_list()
        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        """
        Parses a list of statements.

        Returns:
        -------
        list
            A list of statement nodes
        """
        node = self.statement()
        results = [node]

        while self.current_token.type == 'SEMI':
            self.eat('SEMI')
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        """
        Parses a statement node.

        Returns:
        -------
        AST
            The statement node
        """
        if self.current_token.type in (DEF, IF, WHILE, FOR):
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        Parses an assignment statement node.

        Returns:
        -------
        Assign
            The assignment statement node
        """
        left = self.variable_declaration()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.logical_or()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        Parses a variable node.

        Returns:
        -------
        Var
            The variable node
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    @staticmethod
    def empty():
        """
        Returns an empty (no-operation) node.

        Returns:
        -------
        NoOp
            The no-operation node
        """
        return NoOp()

    def factor(self):
        """
        Parses a factor node.

        Returns:
        -------
        AST
            The factor node
        """
        token = self.current_token
        unary = (PLUS, MINUS, BIT_NOT, NOT)
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.logical_or()
            self.eat(RPAREN)
            return node
        elif token.type == 'INT_CONST':
            self.eat('INT_CONST')
            return Integer(token)
        elif token.type == 'FLOAT_CONST':
            self.eat('FLOAT_CONST')
            return Float(token)
        elif token.type == 'STRING_CONST':
            self.eat('STRING_CONST')
            return String(token)
        elif token.type == 'BOOLEAN_CONST':
            self.eat('BOOLEAN_CONST')
            return Boolean(token)
        elif token.type == 'NONE-TYPE_CONST':
            self.eat('NONE-TYPE_CONST')
            return NoneType(token)
        elif token.type in unary:
            self.eat(token.type)
            node = UnaryOp(op=token, expr=self.factor())
            return node
        else:
            node = self.variable()
            return node

    def exp(self):
        """
        Parses an exponentiation expression node.

        Returns:
        -------
        BinaryOp
            The exponentiation expression node
        """
        node = self.factor()

        while self.current_token.type == EXP:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.factor())

        return node

    def term(self):
        """
        Parses a term node.

        Returns:
        -------
        BinaryOp
            The term node
        """
        node = self.exp()
        binary = (MUL, FLOAT_DIV, MOD, INT_DIV)

        while self.current_token.type in (MUL, FLOAT_DIV, MOD, INT_DIV):
            token = self.current_token
            if token.type in binary:
                self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.exp())

        return node

    def expr(self):
        """
        Parses an expression node.

        Returns:
        -------
        BinaryOp
            The expression node
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.term())

        return node

    def shift(self):
        """
        Parses a bitwise shift expression node.

        Returns:
        -------
        BinaryOp
            The bitwise shift expression node
        """
        node = self.expr()

        while self.current_token.type in (BIT_LEFT_SHIFT, BIT_RIGHT_SHIFT):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.expr())

        return node

    def bit_and(self):
        """
        Parses a bitwise AND expression node.

        Returns:
        -------
        BinaryOp
            The bitwise AND expression node
        """
        node = self.shift()

        while self.current_token.type == BIT_AND:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.shift())

        return node

    def bit_xor(self):
        """
        Parses a bitwise XOR expression node.

        Returns:
        -------
        BinaryOp
            The bitwise XOR expression node
        """
        node = self.bit_and()

        while self.current_token.type == BIT_XOR:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.bit_and())

        return node

    def bit_or(self):
        """
        Parses a bitwise OR expression node.

        Returns:
        -------
        BinaryOp
            The bitwise OR expression node
        """
        node = self.bit_xor()
        while self.current_token.type == BIT_OR:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.bit_xor())
        return node

    def comparison(self):
        """
        Parses a comparison expression node.

        Returns:
        -------
        BinaryOp
            The comparison expression node
        """
        node = self.bit_or()

        while self.current_token.type in (
                EQUALS_TO, NOT_EQUALS_TO, SMALLER_OR_EQUALS, SMALLER, GREATER_OR_EQUALS, GREATER, IS, IS_NOT, IN,
                NOT_IN):
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.bit_or())

        return node

    def logical_not(self):
        """
        Parses a logical NOT expression node.

        Returns:
        -------
        UnaryOp
            The logical NOT expression node
        """
        node = self.comparison()

        while self.current_token.type == NOT:
            token = self.current_token
            self.eat(token.type)
            node = UnaryOp(op=token, expr=self.comparison())

        return node

    def logical_and(self):
        """
        Parses a logical AND expression node.

        Returns:
        -------
        BinaryOp
            The logical AND expression node
        """
        node = self.logical_not()

        while self.current_token.type == AND:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.logical_not())

        return node

    def logical_or(self):
        """
        Parses a logical OR expression node.

        Returns:
        -------
        BinaryOp
            The logical OR expression node
        """
        node = self.logical_and()

        while self.current_token.type == OR:
            token = self.current_token
            self.eat(token.type)
            node = BinaryOp(left=node, op=token, right=self.logical_and())

        return node

    def parse(self):
        """
        Parses the input text and returns the root node of the AST.

        Returns:
        -------
        AST
            The root node of the AST
        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node


class NodeVisitor:
    """
    A base class for visiting nodes in the abstract syntax tree (AST).
    """

    def visit(self, node):
        """
        Visits a node in the AST.

        Parameters:
        ----------
        node : AST
            The node to visit

        Returns:
        -------
        any
            The result of visiting the node
        """
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        Raises an exception for nodes without a specific visit method.

        Parameters:
        ----------
        node : AST
            The node to visit

        Raises:
        ------
        Exception
            An exception indicating no visit method for the node
        """
        raise Exception(f'No visit_{type(node).__name__} method')


class Symbol:
    """
    A class to represent a symbol in the symbol table.

    Attributes:
    ----------
    name : str
        The name of the symbol
    type : str
        The type of the symbol
    """

    def __init__(self, name, var_type: str = 'NoneType'):
        """
        Constructs all the necessary attributes for the symbol object.

        Parameters:
        ----------
        name : str
            The name of the symbol
        var_type : str, optional
            The type of the symbol (default is 'NoneType')
        """
        self.name = name
        self.type = var_type


class VarSymbol(Symbol):
    """
    A class to represent a variable symbol in the symbol table.

    Attributes:
    ----------
    name : str
        The name of the variable
    type : str
        The type of the variable
    """

    def __init__(self, name, var_type: str):
        """
        Constructs all the necessary attributes for the variable symbol object.

        Parameters:
        ----------
        name : str
            The name of the variable
        var_type : str
            The type of the variable
        """
        super().__init__(name, var_type)

    def __str__(self):
        """
        Returns a string representation of the variable symbol.

        Returns:
        -------
        str
            A string representation of the variable symbol
        """
        return f"<class '{self.type}'>"

    __repr__ = __str__


class BuiltinTypeSymbol(Symbol):
    """
    A class to represent a built-in type symbol in the symbol table.

    Attributes:
    ----------
    name : str
        The name of the built-in type
    """

    def __init__(self, name: str):
        """
        Constructs all the necessary attributes for the built-in type symbol object.

        Parameters:
        ----------
        name : str
            The name of the built-in type
        """
        super().__init__(name)

    def __str__(self):
        """
        Returns a string representation of the built-in type symbol.

        Returns:
        -------
        str
            A string representation of the built-in type symbol
        """
        return f"<class '{self.name}'>"

    __repr__ = __str__


class SymbolTable:
    """
    A class to represent a symbol table.

    Attributes:
    ----------
    _symbols : dict
        A dictionary to store symbols
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the symbol table object.
        """
        self._symbols = {}
        self._init_builtins()

    def __str__(self):
        """
        Returns a string representation of the symbol table.

        Returns:
        -------
        str
            A string representation of the symbol table
        """
        return 'Symbols: \n' + '\n'.join(f"<'{i}' {j}>" for i,j in self._symbols.items())

    __repr__ = __str__

    def _init_builtins(self):
        """
        Initializes built-in type symbols in the symbol table.
        """
        self.define(BuiltinTypeSymbol('int'))
        self.define(BuiltinTypeSymbol('float'))
        self.define(BuiltinTypeSymbol('str'))
        self.define(BuiltinTypeSymbol('bool'))
        self.define(BuiltinTypeSymbol('NoneType'))

    def define(self, symbol):
        """
        Defines a symbol in the symbol table.

        Parameters:
        ----------
        symbol : Symbol
            The symbol to define
        """
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str):
        """
        Looks up a symbol in the symbol table.

        Parameters:
        ----------
        name : str
            The name of the symbol to look up

        Returns:
        -------
        Symbol
            The symbol if found, otherwise None
        """
        return self._symbols.get(name)


class Interpreter(NodeVisitor):
    """
    A class to represent an interpreter for the abstract syntax tree (AST).

    Attributes:
    ----------
    parser : Parser
        The parser to generate the AST
    symtable : SymbolTable
        The symbol table to store variable symbols
    GLOBAL_MEMORY : dict
        A dictionary to store variable values
    """

    def __init__(self, parser):
        """
        Constructs all the necessary attributes for the interpreter object.

        Parameters:
        ----------
        parser : Parser
            The parser to generate the AST
        """
        self.parser = parser
        self.symtable = SymbolTable()
        self.GLOBAL_MEMORY = {}

    def visit_BinaryOp(self, node):
        """
        Visits a binary operation node and evaluates the operation.

        Parameters:
        ----------
        node : BinaryOp
            The binary operation node to visit

        Returns:
        -------
        any
            The result of the binary operation
        """
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == INT_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == EXP:
            return self.visit(node.left) ** self.visit(node.right)
        elif node.op.type == BIT_AND:
            return self.visit(node.left) & self.visit(node.right)
        elif node.op.type == BIT_OR:
            return self.visit(node.left) | self.visit(node.right)
        elif node.op.type == BIT_XOR:
            return self.visit(node.left) ^ self.visit(node.right)
        elif node.op.type == BIT_LEFT_SHIFT:
            return self.visit(node.left) << self.visit(node.right)
        elif node.op.type == BIT_RIGHT_SHIFT:
            return self.visit(node.left) >> self.visit(node.right)
        elif node.op.type == EQUALS_TO:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == NOT_EQUALS_TO:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == GREATER:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == SMALLER:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == GREATER_OR_EQUALS:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == SMALLER_OR_EQUALS:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == OR:
            return self.visit(node.left) or self.visit(node.right)
        elif node.op.type == IS:
            return self.visit(node.left) is self.visit(node.right)
        elif node.op.type == IS_NOT:
            return self.visit(node.left) is not self.visit(node.right)
        elif node.op.type == IN:
            return self.visit(node.left) in self.visit(node.right)
        elif node.op.type == NOT_IN:
            return self.visit(node.left) not in self.visit(node.right)

    def visit_UnaryOp(self, node):
        """
        Visits a unary operation node and evaluates the operation.

        Parameters:
        ----------
        node : UnaryOp
            The unary operation node to visit

        Returns:
        -------
        any
            The result of the unary operation
        """
        if node.op.type == PLUS:
            return +self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr)
        elif node.op.type == BIT_NOT:
            return ~self.visit(node.expr)
        elif node.op.type == NOT:
            return not self.visit(node.expr)

    @staticmethod
    def visit_Float(node):
        """
        Visits a float constant node and returns its value.

        Parameters:
        ----------
        node : Float
            The float constant node to visit

        Returns:
        -------
        float
            The value of the float constant
        """
        return node.value

    @staticmethod
    def visit_Integer(node):
        """
        Visits an integer constant node and returns its value.

        Parameters:
        ----------
        node : Integer
            The integer constant node to visit

        Returns:
        -------
        int
            The value of the integer constant
        """
        return node.value

    @staticmethod
    def visit_String(node):
        """
        Visits a string constant node and returns its value.

        Parameters:
        ----------
        node : String
            The string constant node to visit

        Returns:
        -------
        str
            The value of the string constant
        """
        return node.value

    @staticmethod
    def visit_Boolean(node):
        """
        Visits a boolean constant node and returns its value.

        Parameters:
        ----------
        node : Boolean
            The boolean constant node to visit

        Returns:
        -------
        bool
            The value of the boolean constant
        """
        return node.value

    @staticmethod
    def visit_NoneType(node):
        """
        Visits a NoneType constant node and returns its value.

        Parameters:
        ----------
        node : NoneType
            The NoneType constant node to visit

        Returns:
        -------
        None
            The value of the NoneType constant
        """
        return node.value

    def visit_Compound(self, node):
        """
        Visits a compound statement node and processes all child nodes.

        Parameters:
        ----------
        node : Compound
            The compound statement node to visit
        """
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        """
        Visits a no-operation (empty) statement node. This method does nothing.

        Parameters:
        ----------
        node : NoOp
            The no-operation statement node to visit
        """
        pass

    def visit_Assign(self, node):
        """
        Visits an assignment statement node and assigns the value to the variable.

        Parameters:
        ----------
        node : Assign
            The assignment statement node to visit
        """
        var_name = node.left.var_node.value
        type_symbol = node.left.type_node.value
        var_value = self.visit(node.right)
        var_type = type(var_value).__name__
        if type_symbol == 'var':
            type_symbol = var_type
        elif (var_type, type_symbol) == ('int', 'float'):
            var_value = float(var_value)
            var_type = 'float'
        if var_type != type_symbol:
            raise TypeError(f"Cannot assign {var_type} to {type_symbol}")
        var_type = VarSymbol(var_name, type_symbol)
        self.symtable.define(var_type)
        self.GLOBAL_MEMORY[var_name] = var_value

    def visit_Var(self, node):
        """
        Visits a variable node and returns its value.

        Parameters:
        ----------
        node : Var
            The variable node to visit

        Returns:
        -------
        any
            The value of the variable
        """
        var_name = node.value
        val = self.GLOBAL_MEMORY.get(var_name)
        var_type = self.symtable.lookup(var_name)
        if var_type is None:
            raise NameError(repr(var_name))
        return val

    def interpret(self):
        """
        Interprets the abstract syntax tree (AST) and returns the result.

        Returns:
        -------
        any
            The result of interpreting the AST
        """
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    """
    The main function to run the interpreter.
    """
    with open('code.spy', 'r') as f:
        text = f.read()
    text = text.replace('\n', ';')
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_MEMORY)
    print(interpreter.symtable)


if __name__ == '__main__':
    main()
