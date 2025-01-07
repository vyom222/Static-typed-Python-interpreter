import sys
import argparse
import os
from interpreter_lexer import Lexer
from interpreter_parser import Parser
from interpreter import Interpreter


def main():
    """
    The main function to run the interpreter.
    Accepts only .spy files to execute.
    """
    # Argument parsing for the file and debug flag
    parser = argparse.ArgumentParser(description="Run the interpreter.")
    parser.add_argument('filename', help="The file to execute with the interpreter.")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Print the interpreter's global memory and symbol table.")
    args = parser.parse_args()

    # Check if the file exists
    if not os.path.isfile(args.filename):
        print(f"Error: The file '{args.filename}' was not found.")
        sys.exit(1)

    # Open the provided file
    with open(args.filename, 'r') as f:
        text = f.read()

    # with open('code.spy', 'r') as f:
    #     text = f.read()

    # Run the lexer, parser, and interpreter
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()

    # Print the interpreter's global memory and symbol table if debug is enabled
    if args.debug:
        print(interpreter.GLOBAL_MEMORY)
        print(interpreter.symtable)


if __name__ == '__main__':
    main()
