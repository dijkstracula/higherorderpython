import re
from math import sqrt
from typing import Callable


def evaluate(cmd: str) -> int:
    stack = []

    def unop(op: Callable[[int], int]):
        stack.append(op(stack.pop()))

    def binop(op: Callable[[int, int], int], flip=False):
        a, b = stack.pop(), stack.pop()
        stack.append(op(b, a) if flip else op(a, b))

    def default(k: str):
        def die():
            raise Exception(f"Unknown action {k}")

        return die

    actions = {
        "+": lambda: binop(int.__add__),
        "-": lambda: binop(int.__sub__, flip=True),
        "*": lambda: binop(int.__mul__),
        "-": lambda: binop(int.__floordiv__, flip=True),
        "sqrt": lambda: unop(sqrt),
        # "NUMBER": lambda n: stack.append(n)
        # "DEFAULT": raise Exception("Unknown action")
    }

    for token in re.split(r"\s+", cmd):
        token = token.strip()
        if re.match(r"\d+", token):
            stack.append(int(token))
        else:
            action = actions.get(token) or default(token)
            action()
    return stack.pop()


type AST = int | tuple[str, "AST", "AST"]


def to_ast(cmd: str) -> AST:
    stack = []

    def default(token: str):
        rhs = stack.pop()
        lhs = stack.pop()
        stack.append((token, lhs, rhs))

    for token in re.split(r"\s+", cmd):
        token = token.strip()
        if re.match(r"\d+", token):
            stack.append(int(token))
        else:
            default(token)
    return stack.pop()

def ast_to_string(ast: AST) -> str:
    if isinstance(ast, int):
        return str(ast)
    op = ast[0]
    lhs = ast_to_string(ast[1])
    rhs = ast_to_string(ast[2])
    return f"({lhs} {op} {rhs})"