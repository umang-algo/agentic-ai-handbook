"""
Chapter 6: AST-Aware Code Chunker
===================================
Parses Python source into semantically meaningful chunks at function/class
granularity. Never splits a function in half — garbage vectors eliminated.

From: The Practitioner's Handbook of Agentic AI, Chapter 6.3
"""

import ast


class CodeChunker(ast.NodeVisitor):
    """AST visitor that extracts class and function scopes."""

    def __init__(self, source_code: str):
        self.source_lines = source_code.splitlines()
        self.chunks = []

    def visit_ClassDef(self, node):
        class_code = "\n".join(self.source_lines[node.lineno-1 : node.end_lineno])
        self.chunks.append({
            "type": "class",
            "name": node.name,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "code": class_code
        })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func_code = "\n".join(self.source_lines[node.lineno-1 : node.end_lineno])
        self.chunks.append({
            "type": "function",
            "name": node.name,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
            "code": func_code
        })
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef


def get_ast_chunks(source: str) -> list[dict]:
    """Parse Python source and return AST-aware chunks."""
    tree = ast.parse(source)
    chunker = CodeChunker(source)
    chunker.visit(tree)
    return chunker.chunks


# ─── Graph RAG Memory ──────────────────────────────────────────────────────

class MemoryNode:
    """A node in the Graph RAG knowledge graph."""

    def __init__(self, node_id: str, content: str, node_type: str):
        self.node_id = node_id
        self.content = content
        self.node_type = node_type
        self.vector = None
        self.edges = []

    def add_relationship(self, target_node, relationship: str):
        self.edges.append((target_node, relationship))


def find_transitive_imports(start_node: MemoryNode,
                            target_relation: str = "imports") -> list:
    """Recursively walks graph edges to build full dependency paths."""
    visited = set()
    dependencies = []

    def walk(node):
        for neighbor, relation in node.edges:
            if relation == target_relation and neighbor.node_id not in visited:
                visited.add(neighbor.node_id)
                dependencies.append(neighbor)
                walk(neighbor)

    walk(start_node)
    return dependencies


# ─── Demo ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("AST-Aware Code Chunker Demo")
    print("=" * 60)

    sample_code = '''
import os
from typing import Optional

class DatabaseManager:
    """Manages database connections."""

    def __init__(self, connection_string: str):
        self.conn_str = connection_string
        self.pool = None

    def connect(self) -> bool:
        """Establishes connection pool."""
        self.pool = create_pool(self.conn_str)
        return self.pool is not None

    async def query(self, sql: str) -> list:
        """Executes a SQL query."""
        async with self.pool.acquire() as conn:
            return await conn.fetch(sql)

def helper_function(x: int) -> int:
    """A standalone utility."""
    return x * 2

class AuthHelper:
    def validate(self, token: str) -> bool:
        return len(token) > 10
'''

    chunks = get_ast_chunks(sample_code)

    for chunk in chunks:
        print(f"\n{'─' * 60}")
        print(f"Type: {chunk['type']} | Name: {chunk['name']} | "
              f"Lines: {chunk['start_line']}-{chunk['end_line']}")
        print(f"Code preview: {chunk['code'][:80]}...")

    print(f"\n{'=' * 60}")
    print(f"Total chunks: {len(chunks)}")
    print(f"→ Each chunk is a semantically complete unit for embedding")

    # Graph RAG demo
    print(f"\n{'=' * 60}")
    print("Graph RAG: Transitive Import Resolution")
    print("=" * 60)

    main_file = MemoryNode("main.py", "import db", "file")
    db_file = MemoryNode("db.py", "import auth", "file")
    auth_file = MemoryNode("auth.py", "import crypto", "file")
    crypto_file = MemoryNode("crypto.py", "base module", "file")

    main_file.add_relationship(db_file, "imports")
    db_file.add_relationship(auth_file, "imports")
    auth_file.add_relationship(crypto_file, "imports")

    deps = find_transitive_imports(main_file)
    print(f"  main.py transitively imports: {[d.node_id for d in deps]}")
