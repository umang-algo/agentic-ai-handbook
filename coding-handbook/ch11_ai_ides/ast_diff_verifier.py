"""
AST Diff Verifier

Uses python's built-in AST compiler to verify that applied code differences
do not result in syntax compilation errors before writing to disk.
"""

import ast
from typing import Tuple

def verify_ast_compilation(code: str) -> Tuple[bool, str]:
    """
    Attempts to compile code into Abstract Syntax Tree.
    Returns (success_boolean, status_message)
    """
    try:
        ast.parse(code)
        return True, "Code successfully compiled to valid Abstract Syntax Tree."
    except SyntaxError as e:
        return False, f"Syntax Error: {e.msg} at line {e.lineno}, col {e.offset}"

if __name__ == "__main__":
    # Test case 1: Syntactically sound code
    code_valid = """
def process_data(data):
    if not data:
        return []
    return [d * 2 for d in data]
"""
    success, msg = verify_ast_compilation(code_valid)
    print("Valid Code Test:", "PASSED" if success else "FAILED")
    print("Status:", msg)
    
    # Test case 2: Broken syntax code (missing close parenthesis)
    code_invalid = """
def process_data(data:
    return data
"""
    success, msg = verify_ast_compilation(code_invalid)
    print("\nBroken Code Test:", "PASSED" if not success else "FAILED")
    print("Status:", msg)
