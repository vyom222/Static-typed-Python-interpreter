# Token Types
# Data Types
INT, FLOAT, STR, BOOL, VAR, NONETYPE = (
    'INT', 'FLOAT', 'STR', 'BOOL', 'VAR', 'NONETYPE'
)

# Arithmetic Operators
PLUS, MINUS, MUL, FLOAT_DIV, MOD, INT_DIV, EXP = (
    'PLUS', 'MINUS', 'MUL', 'FLOAT_DIV', 'MOD', 'INT_DIV', 'EXP'
)

# Bitwise Operators
BIT_NOT, BIT_XOR, BIT_AND, BIT_OR, BIT_LEFT_SHIFT, BIT_RIGHT_SHIFT = (
    'BIT_NOT', 'BIT_XOR', 'BIT_AND', 'BIT_OR', 'BIT_LEFT_SHIFT', 'BIT_RIGHT_SHIFT'
)

# Comparison Operators
GREATER, SMALLER, GREATER_OR_EQUALS, SMALLER_OR_EQUALS = (
    'GREATER', 'SMALLER', 'GREATER_OR_EQUALS', 'SMALLER_OR_EQUALS'
)
EQUALS_TO, NOT_EQUALS_TO = 'EQUALS_TO', 'NOT_EQUALS_TO'

# Logical Operators
NOT, AND, OR = 'NOT', 'AND', 'OR'

# Membership and Identity Operators
IS, IS_NOT, IN, NOT_IN = 'IS', 'IS_NOT', 'IN', 'NOT_IN'

# Punctuation and Delimiters
LPAREN, RPAREN, ASSIGN, SEMI, NEWLINE, DOT, COLON, COMMA = (
    'LPAREN', 'RPAREN', 'ASSIGN', 'SEMI', 'NEWLINE', 'DOT', 'COLON', 'COMMA'
)

# Keywords
IF, WHILE, FOR, DEF = 'IF', 'WHILE', 'FOR', 'DEF'

# Special Tokens
INDENT, EOF = 'INDENT', 'EOF'

# Constants
STR_CONST, INT_CONST, FLOAT_CONST, BOOLEAN_CONST, NONETYPE_CONSTANT = (
    'STR_CONST', 'INT_CONST', 'FLOAT_CONST', 'BOOLEAN_CONST', 'NONETYPE_CONSTANT'
)

# Identifiers
ID = 'ID'


# from enum import Enum
#
#
# class TokenType(Enum):
#     MINUS = '-'
#     MUL = '*'
#     FLOAT_DIV = '/'
#     BIT_NOT = '~'
#     BIT_XOR = '^'
#     BIT_AND = '&'
#     BIT_OR = '|'
#     MOD = '%'
#     INT_DIV = '//'
#     EXP = '**'
#     BIT_LEFT_SHIFT = '<<'
#     BIT_RIGHT_SHIFT = '>>'
#     GREATER = '>'
#     SMALLER = '<'
#     GREATER_OR_EQUALS = '>='
#     SMALLER_OR_EQUALS = '<='
#     EQUALS_TO = '=='
#     NOT_EQUALS_TO = '!='
#     LPAREN = '('
#     RPAREN = ')'
#     ASSIGN = '='
#     SEMI = ';'
#     NEWLINE = '\n'
#     DOT = '.'
#     COLON = ':'
#     COMMA = ','
#     ID = 'ID'
#     INDENT = 'INDENT'
#     EOF = 'EOF'


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

    def __init__(self, token_type: str, token_value):
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
        self.value = token_value

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
    'int': Token(INT, 'int'),
    'float': Token(FLOAT, 'float'),
    'var': Token(VAR, 'var'),
    'str': Token(STR, 'str'),
    'bool': Token(BOOL, 'bool'),
    'NoneType': Token(NONETYPE, 'NoneType'),
    'True': Token(BOOLEAN_CONST, 'True'),
    'False': Token(BOOLEAN_CONST, 'False'),
    'None': Token(NONETYPE_CONSTANT, 'None')
}
