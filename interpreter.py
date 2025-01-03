from interpreter_token import *


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
        return 'Symbols: \n' + '\n'.join(f"<'{i}' {j}>" for i, j in self._symbols.items())

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

    def visit_Program(self, node):
        """
        Visits Program node and processes all child nodes.

        Parameters:
        ----------
        node : Program
            The Program node to visit
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
