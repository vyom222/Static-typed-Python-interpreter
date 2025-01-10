from interpreter_token import *


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
        self.operators = {'+': Token(PLUS, '+'),
                          '-': Token(MINUS, '-'),
                          '*': Token(MUL, '*'),
                          '/': Token(FLOAT_DIV, '/'),
                          '%': Token(MOD, '%'),
                          '^': Token(BIT_XOR, '^'),
                          '&': Token(BIT_AND, '&'),
                          '|': Token(BIT_OR, '|'),
                          '~': Token(BIT_NOT, '~'),
                          '>': Token(GREATER, '>'),
                          '<': Token(SMALLER, '<'),
                          '=': Token(ASSIGN, '='),
                          '!': Token(NOT, '!'),
                          '(': Token(LPAREN, '('),
                          ')': Token(RPAREN, ')'),
                          ';': Token(SEMI, ';'),
                          '\n': Token(NEWLINE, '\n'),
                          ':': Token(COLON, ':'),
                          ',': Token(COMMA, ','),
                          '**': Token(EXP, '**'),
                          '//': Token(INT_DIV, '//'),
                          '<<': Token(BIT_LEFT_SHIFT, '<<'),
                          '>>': Token(BIT_RIGHT_SHIFT, '>>'),
                          '==': Token(EQUALS_TO, '=='),
                          '!=': Token(NOT_EQUALS_TO, '!='),
                          '+=': Token(PLUS_EQUALS, '+='),
                          '-=': Token(MINUS_EQUALS, '-='),
                          '*=': Token(MUL_EQUALS, '*='),
                          '/=': Token(FLOAT_DIV_EQUALS, '/='),
                          '%=': Token(MOD_EQUALS, '%='),
                          '^=': Token(BIT_XOR_EQUALS, '^='),
                          '&=': Token(BIT_AND_EQUALS, '&='),
                          '|=': Token(BIT_OR_EQUALS, '|='),
                          '<<=': Token(BIT_LEFT_SHIFT_EQUALS, '<<='),
                          '>>=': Token(BIT_RIGHT_SHIFT_EQUALS, '>>='),
                          '**=': Token(EXP_EQUALS, '**='),
                          '>=': Token(GREATER_OR_EQUALS, '>='),
                          '<=': Token(SMALLER_OR_EQUALS, '<=')}

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
        raise SyntaxError(f"invalid character '{character}' (U+{hex(ord(character))[2:].upper()})")

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

    def prev(self):
        """
        Returns the previous character in the input text without moving the `pos` pointer.

        Returns:
        -------
        str
            The previous character in the input text, or None if at the beginning of the text
        """
        prev_pos = self.pos - 1
        if prev_pos < 0:
            return None
        else:
            return self.text[prev_pos]

    def skip_whitespace(self):
        """
        Skips whitespace characters in the input text.
        """
        while self.current_char and self.current_char.isspace() and self.current_char != '\n':
            self.advance()

    def skip_comment(self):
        """
        Skips comments in the input text.
        """
        while self.current_char != '\n':
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
            token = Token(FLOAT_CONST, float(result))
        elif '.' not in result:
            token = Token(INT_CONST, int(result))
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
        token = Token(STR_CONST, result)
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

    def indent(self):
        """
        Returns an indent token consumed from the input.

        Returns:
        -------
        Token
            The indent token with the count of spaces / tabs
        """
        count = 0
        while self.current_char and self.current_char.isspace() and self.current_char != '\n':
            count += 1
            self.advance()

        token = Token(INDENT, count)
        return token

    def get_next_token(self):
        """
        Returns an identifier token or a reserved keyword token consumed from the input.

        Returns:
        -------
        Token
            A token representing an identifier or a reserved keyword
        """
        while self.current_char:
            if self.current_char.isspace() and self.current_char != '\n':
                if self.prev() != '\n' and self.prev() is not None:
                    self.skip_whitespace()
                    continue
                if self.prev() == '\n' or self.prev() is None:
                    return self.indent()
            if self.current_char == '#':
                self.advance()
                self.skip_comment()
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
                if self.current_char == '=':
                    self.advance()
                    return Token(PLUS_EQUALS, '+=')
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(MINUS_EQUALS, '-=')
                return Token(MINUS, '-')
            if self.current_char == '*':
                if self.peek() == '*':
                    self.advance()
                    self.advance()
                    if self.current_char == '=':
                        self.advance()
                        return Token(EXP_EQUALS, '**=')
                    return Token(EXP, '**')
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(MUL_EQUALS, '*=')
                return Token(MUL, '*')
            if self.current_char == '/':
                if self.peek() == '/':
                    self.advance()
                    self.advance()
                    if self.current_char == '=':
                        self.advance()
                        return Token(INT_DIV_EQUALS, '//=')
                    return Token(INT_DIV, '//')
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(FLOAT_DIV_EQUALS, '/=')
                return Token(FLOAT_DIV, '/')
            if self.current_char == '~':
                self.advance()
                return Token(BIT_NOT, '~')
            if self.current_char == '^':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(BIT_XOR_EQUALS, '^=')
                return Token(BIT_XOR, '^')
            if self.current_char == '&':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(BIT_AND_EQUALS, '&=')
                return Token(BIT_AND, '&')
            if self.current_char == '|':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(BIT_OR_EQUALS, '|=')
                return Token(BIT_OR, '|')
            if self.current_char == '%':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(MOD_EQUALS, '%=')
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
                    if self.current_char == '=':
                        self.advance()
                        return Token(BIT_RIGHT_SHIFT_EQUALS, '>>=')
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
                    if self.current_char == '=':
                        self.advance()
                        return Token(BIT_LEFT_SHIFT_EQUALS, '<<=')
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
                return Token(SEMI, ';')
            if self.current_char == '\n':
                self.advance()
                return Token(NEWLINE, '\n')
            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            if self.current_char.isalpha():
                return self._id()
            self.error(self.current_char)
        return Token(EOF, None)
