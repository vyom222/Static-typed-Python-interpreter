# Static Typed Python Interpreter
### A python interpreter that is statically typed. Based on python 3.12 and Typings library.

#### How to run:
```bash
python main.py *filename.spy *args
```
- filename.spy: The file to interpret, enter CLI mode if empty
- args: The arguments to pass to the file | -d: Debug Mode

#### Syntax:
```python
# Assigning a variable

# identifier: type = value | expr
a: int = 10
b: str = "Hello World"
c: float = 10.5f
d: bool = True
e: NoneType = None
f: var = 5

# Expressions
10 + 5 * (6 / 2) % 3 ** 5 // 9 - 1
~4 ^ 6 & 2 | 1 << 3 