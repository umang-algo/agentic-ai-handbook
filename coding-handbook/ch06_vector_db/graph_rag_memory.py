"""
Graph RAG - Entity Relationship Knowledge Lookup

Demonstrates relationship traversal in a knowledge graph to augment vector search (Graph RAG).
"""

from typing import Dict, List, Set

class GraphRAGMemory:
    """Memory store holding entities (nodes) and relations (edges) for codebases."""
    def __init__(self):
        self.nodes: Dict[str, dict] = {} # symbol -> attributes
        self.edges: Dict[str, Set[str]] = {} # symbol -> set of target symbols (depends_on)

    def add_node(self, name: str, node_type: str, docstring: str) -> None:
        self.nodes[name] = {"type": node_type, "doc": docstring}
        if name not in self.edges:
            self.edges[name] = set()

    def add_relation(self, source: str, target: str) -> None:
        if source in self.edges:
            self.edges[source].add(target)

    def traverse_dependencies(self, start_node: str, max_depth: int = 2) -> List[str]:
        """BFS traversal to fetch all dependent code context."""
        visited = set()
        queue = [(start_node, 0)]
        retrieved_symbols = []

        while queue:
            node, depth = queue.pop(0)
            if node in visited or depth > max_depth:
                continue
                
            visited.add(node)
            if node in self.nodes:
                retrieved_symbols.append(node)
                
            for neighbor in self.edges.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
                    
        return retrieved_symbols

if __name__ == "__main__":
    graph = GraphRAGMemory()
    
    # Add files/classes as nodes
    graph.add_node("AuthService", "Class", "Handles user log-ins and token signing.")
    graph.add_node("DatabasePool", "Class", "Manages postgres connections.")
    graph.add_node("JWTVerifier", "Class", "Decodes HS256 tokens.")
    graph.add_node("UserModel", "Class", "Schema representing system user.")
    
    # Establish relations (imports/dependencies)
    graph.add_relation("AuthService", "JWTVerifier")
    graph.add_relation("AuthService", "DatabasePool")
    graph.add_relation("DatabasePool", "UserModel")
    
    # Traverse dependencies starting at AuthService
    print("Querying AuthService dependencies via Graph RAG...")
    dependencies = graph.traverse_dependencies("AuthService", max_depth=2)
    
    print("\nRetrieved Context:")
    for symbol in dependencies:
        print(f"- {symbol}: {graph.nodes[symbol]['doc']}")
