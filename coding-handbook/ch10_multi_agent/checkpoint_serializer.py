"""
State Graph Checkpoint Serializer

Demonstrates how multi-agent state machines serialize thread checkpoints to disk
to allow process recovery and human-in-the-loop approvals.
"""

import json
from typing import Dict, Any

class StateCheckpointer:
    def __init__(self):
        self.db: Dict[str, str] = {} # thread_id -> serialized_state_json

    def save_checkpoint(self, thread_id: str, step: int, state: Dict[str, Any]) -> None:
        """Serializes current multi-agent state dictionary to the database."""
        checkpoint = {
            "step": step,
            "state": state
        }
        self.db[thread_id] = json.dumps(checkpoint)
        print(f"[Checkpointer]: Saved state for thread '{thread_id}' at step {step}")

    def load_checkpoint(self, thread_id: str) -> Dict[str, Any]:
        """Loads state checkpoint from the database, or returns empty dict if not found."""
        if thread_id not in self.db:
            return {}
        checkpoint = json.loads(self.db[thread_id])
        print(f"[Checkpointer]: Loaded state for thread '{thread_id}' from step {checkpoint['step']}")
        return checkpoint["state"]

if __name__ == "__main__":
    db = StateCheckpointer()
    
    # Initial state
    thread = "thread_123"
    state_0 = {"query": "Write tests", "active_agent": "planner", "messages": []}
    db.save_checkpoint(thread, 0, state_0)
    
    # State update
    state_1 = {
        "query": "Write tests",
        "active_agent": "coder",
        "messages": ["Plan: 1. Create file 2. Add test cases"]
    }
    db.save_checkpoint(thread, 1, state_1)
    
    # Simulate database retrieval after a crash / restart
    restored_state = db.load_checkpoint(thread)
    print("\nRestored state details:")
    print(restored_state)
