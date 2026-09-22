"""Tools the agent is allowed to use, plus their JSON Schema descriptions."""
import ast
import operator
from config import BOOK_FINES

def get_book_fine(book_code: str) -> str:
    """Look up the fine for one book code."""
    fine = BOOK_FINES.get(book_code.strip().upper())
    return str(fine) if fine is not None else f"Unknown book code: {book_code}"

# A safe calculator: only numbers and + - * / ( ) are allowed. Never use eval().
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as (12000 + 18000) * 0.9."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"

TOOL_FUNCTIONS = {"get_book_fine": get_book_fine, "calculator": calculator}

# These descriptions are what the LLM reads when deciding which tool to call
TOOLS = [
    {"type": "function", "function": {
        "name": "get_book_fine",
        "description": "Get the daily fine in rupees for a single book code, for example B101.",
        "parameters": {"type": "object",
                        "properties": {"book_code": {"type": "string"}},
                        "required": ["book_code"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
                        "properties": {"expression": {"type": "string"}},
                        "required": ["expression"]}}},
]

if __name__ == "__main__":
    print("get_book_fine('b202') ->", get_book_fine("b202"))
    print("calculator('(5 + 10) * 3') ->", calculator("(5 + 10) * 3"))
    print("calculator('7 - 5') ->", calculator("7 - 5"))