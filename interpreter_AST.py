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
        self.value = 'True' == token.value


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


class Program(AST):
    """
    A class to represent program in the AST.

    Attributes:
    ----------
    children : list
        A list of child nodes representing the statements in the program
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the program node.
        """
        self.children: list = []


class Compound(AST):
    """
    A class to represent compound statements in the AST.

    Attributes:
    ----------
    children : list
        A list of child nodes representing the statements in the program
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the program node.
        """
        self.children: list = []


class Func(AST):
    """
    A class to represent a function node in the AST.

    Attributes:
    ----------
    func_name : str
        The name of the function
    func_params : list
        A list of the function parameters
    func_body : Compound
        The body of the function
    """

    def __init__(self, func_name, func_params):
        """
        Constructs all the necessary attributes for the function node.

        Parameters:
        ----------
        func_name : str
            The name of the function
        func_params : list
            A list of the function parameters
        func_body : Compound
            The body of the function
        """
        self.func_name = func_name
        self.func_params = func_params
        self.func_body: list = []


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
