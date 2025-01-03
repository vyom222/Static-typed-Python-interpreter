import sys
import argparse
from interpreter_lexer import Lexer
from interpreter_parser import Parser
from interpreter import Interpreter

def main():
    """
    The main function to run the interpreter.
    Accepts a file as an argument to execute.
    """
    # Argument parsing for the file
    parser = argparse.ArgumentParser(description="Run the custom interpreter.")
    parser.add_argument('filename', help="The file to execute with the interpreter.")
    args = parser.parse_args()

    # Open the provided file
    try:
        with open(args.filename, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{args.filename}' was not found.")
        sys.exit(1)

    # Run the lexer, parser, and interpreter
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()

    # Print the interpreter's global memory and symbol table
    print(interpreter.GLOBAL_MEMORY)
    print(interpreter.symtable)

if __name__ == '__main__':
    main()
