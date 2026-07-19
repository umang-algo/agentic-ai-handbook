"""
Graph State Serializer

Demonstrates state schema modeling and serialization using standard Python
dataclasses for transaction checkpoints.
"""

import json
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any

@dataclass
class GraphState:
    messages: List[Dict[str, str]] = field(default_factory=list)
    next_node: str = "init"
    variables: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def serialize(self) -> str:
        """Serializes dataclass to JSON string."""
        return json.dumps(asdict(self))

    @classmethod
    def deserialize(cls, raw_json: str):
        """Reconstructs state from JSON string."""
        data = json.loads(raw_json)
        return cls(
            messages=data.get("messages", []),
            next_node=data.get("next_node", "init"),
            variables=data.get("variables", {}),
            errors=data.get("errors", [])
        )

if __name__ == "__main__":
    # Create a state
    state = GraphState(
        messages=[{"role": "user", "content": "Fetch Q3 report"}],
        next_node="rag_retriever",
        variables={"query_ticker": "MSFT"}
    )
    
    # Serialize
    serialized = state.serialize()
    print("Serialized State:")
    print(serialized)
    
    # Restore
    restored = GraphState.deserialize(serialized)
    print("\nRestored Next Node:", restored.next_node)
    print("Restored Variables:", restored.variables)
