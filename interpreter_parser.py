from interpreter_AST import *
from interpreter_token import *

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
        nodes = self.statement_list()
        root = Program()
        for node in nodes:
            root.children.append(node)
        return root

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
            self.eat(INT)
        elif self.current_token.type == "FLOAT":
            self.eat(FLOAT)
        elif self.current_token.type == "STR":
            self.eat(STR)
        elif self.current_token.type == "BOOL":
            self.eat(BOOL)
        elif self.current_token.type == "NONETYPE":
            self.eat(NONETYPE)
        elif self.current_token.type == "VAR":
            self.eat(VAR)
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

        while self.current_token.type in (SEMI, NEWLINE):
            self.eat(self.current_token.type)
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
        if self.current_token.type in (DEF):
            node = self.function_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def function_statement(self):
        """
        Parses a function statement node.

        Returns:
        -------
        Func
            The function statement node
        """
        self.eat(DEF)
        func_name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)
        # func_params = self.function_parameters()
        self.eat(RPAREN)
        self.eat(COLON)
        node = Func(func_name, None)
        target_indent_value, current_indent_value = self.current_token.value, self.current_token.value
        self.eat(INDENT)
        while current_indent_value == target_indent_value:
            pass
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
        elif token.type == INT_CONST:
            self.eat(INT_CONST)
            return Integer(token)
        elif token.type == FLOAT_CONST:
            self.eat(FLOAT_CONST)
            return Float(token)
        elif token.type == STRING_CONST:
            self.eat(STRING_CONST)
            return String(token)
        elif token.type == BOOLEAN_CONST:
            self.eat(BOOLEAN_CONST)
            return Boolean(token)
        elif token.type == NONETYPE_CONSTANT:
            self.eat(NONETYPE_CONSTANT)
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