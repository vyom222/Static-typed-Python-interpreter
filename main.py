import sys
import argparse
import os
from interpreter_lexer import Lexer
from interpreter_parser import Parser
from interpreter import Interpreter


def run_file(filename, debug):
    """
    Execute a .spy file.
    """
    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"\033[31mcan't open file '{filename}': [Errno 2] No such file or directory\033[0m")
        sys.exit(1)

    # Open the provided file
    with open(filename, 'r') as f:
        text = f.read()

    try:
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()

        # Print the interpreter's global memory and symbol table if debug is enabled
        if debug:
            print("GLOBAL MEMORY:", interpreter.GLOBAL_MEMORY)
            print("SYMBOL TABLE:", interpreter.symtable)

    except Exception as e:
        print(f"\033[31m{e}\033[0m")


def run_cli(debug):
    """
    Enter CLI mode for the interpreter.
    """
    print("\033[38;2;147;146;147;48;2;64;62;65mSPython Console\033[0m")

    interpreter = None
    while True:
        try:
            line = input(">>> ")
            if line.strip().lower() == 'exit()':
                print("Process finished with exit code 0")
                sys.exit(0)

            if not interpreter:
                interpreter = Interpreter(Parser(Lexer(line)))
            else:
                interpreter.parser = Parser(Lexer(line))

            interpreter.interpret()

            if debug:
                print(f"GLOBAL MEMORY: {interpreter.GLOBAL_MEMORY}")
                print(f"SYMBOL TABLE: {interpreter.symtable}")
        except KeyboardInterrupt:
            print("\033[31mKeyboardInterrupt\033[0m")
        except Exception as e:
            print(f"\033[31m{e}\033[0m")


def main():
    """
    The main function to run the interpreter.
    Accepts only .spy files to execute or enters CLI mode.
    """
    # Argument parsing for the file and debug flag
    parser = argparse.ArgumentParser(description="Run the interpreter.")
    parser.add_argument('filename', nargs='?', help="The file to execute with the interpreter.", default=None)
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Print the interpreter's global memory and symbol table.")
    args = parser.parse_args()

    if args.filename:
        run_file(args.filename, args.debug)
    else:
        run_cli(args.debug)


if __name__ == '__main__':
    main()
