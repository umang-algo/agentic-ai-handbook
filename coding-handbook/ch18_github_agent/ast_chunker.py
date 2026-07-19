"""
AST Chunker for Codebase Parsing

Parses source code files using Abstract Syntax Trees (AST) to split files
cleanly at function or class definitions, preserving scope context.
"""

import ast
from typing import List, Dict

class ASTCodeChunker:
    @staticmethod
    def chunk_code(source_code: str) -> List[Dict[str, Any]]:
        """Parses python source code and chunks it into separate function/class bodies."""
        tree = ast.parse(source_code)
        chunks = []
        
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # Get the source lines of the node
                start_line = node.lineno
                end_line = getattr(node, "end_lineno", start_line)
                
                chunks.append({
                    "name": node.name,
                    "type": type(node).__name__,
                    "lines": (start_line, end_line)
                })
        return chunks

if __name__ == "__main__":
    code = """
import os

class DatabasePool:
    def connect(self):
        pass

def fetch_results(query: str):
    return [1, 2, 3]
"""
    chunks = ASTCodeChunker.chunk_code(code)
    print("Extracted AST Chunks:")
    for c in chunks:
        print(f"- {c['type']} '{c['name']}' spanning lines {c['lines']}")
