from interpreter_lexer import Lexer
from interpreter_parser import Parser
from interpreter import Interpreter


def main():
    """
    The main function to run the interpreter.
    """
    with open('code.spy', 'r') as f:
        text = f.read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_MEMORY)
    print(interpreter.symtable)

if __name__ == '__main__':
    main()
