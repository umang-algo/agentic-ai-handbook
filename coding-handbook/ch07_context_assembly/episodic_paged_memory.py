"""
MemGPT-Style Episodic Paged Memory Store

Demonstrates an OS-like memory hierarchy (Core, Recall, Archival) where the agent
uses functional tool calls to read and write to its own memory buffers.
"""

from typing import List, Dict, Any

class PagedAgentMemory:
    def __init__(self, core_capacity: int = 150):
        # 1. Core Memory (Always loaded in prompt context window)
        self.core_memory: Dict[str, str] = {
            "user_persona": "User name: Umang. Role: AI Architect.",
            "agent_persona": "You are Jarvis, an expert coding assistant."
        }
        self.core_capacity = core_capacity
        
        # 2. Recall Memory (Indexed dialogue logs, retrieved via tools)
        self.recall_store: List[Dict[str, str]] = []
        
        # 3. Archival Memory (Cold key-value files for facts/rules)
        self.archival_store: Dict[str, str] = {}

    def edit_core_memory(self, key: str, value: str) -> str:
        """Agent tool to modify core context values directly."""
        if key not in self.core_memory:
            return f"Error: Key '{key}' does not exist in core memory."
        self.core_memory[key] = value
        return f"Success: Core memory '{key}' updated."

    def search_recall_memory(self, query: str) -> List[Dict[str, str]]:
        """Agent tool to search historical conversational logs."""
        print(f"[Recall Tool]: Searching chat logs for keyword '{query}'...")
        results = [log for log in self.recall_store if query.lower() in log["content"].lower()]
        return results[:3]

    def write_to_archival(self, key: str, fact: str) -> str:
        """Agent tool to persist long-term cold facts."""
        self.archival_store[key] = fact
        return f"Success: Fact '{key}' saved to cold archival memory."

    def format_system_prompt(self) -> str:
        """Assembles prompt injecting Core Memory into the system window."""
        core_block = "\n".join([f"- {k.upper()}: {v}" for k, v in self.core_memory.items()])
        return (
            f"SYSTEM INSTRUCTIONS:\n"
            f"You are an agent with active paged memory.\n\n"
            f"=== CORE MEMORY ===\n"
            f"{core_block}\n"
            f"===================\n"
        )

if __name__ == "__main__":
    memory = PagedAgentMemory()
    
    # Pre-populate Recall History
    memory.recall_store.append({"role": "user", "content": "I like writing code in Rust and Python."})
    memory.recall_store.append({"role": "assistant", "content": "Recorded preference: Python and Rust."})
    memory.recall_store.append({"role": "user", "content": "Let's use AWS Firecracker for tool execution."})
    
    # 1. Render initial system prompt (contains core memory context)
    print("Initial System Context:")
    print(memory.format_system_prompt())
    
    # 2. Simulate agent calling tools during a run
    print("\n--- Agent Execution simulation ---")
    
    # Agent decides to update user profile
    result = memory.edit_core_memory("user_persona", "User name: Umang. Likes: Rust, Python. System: Firecracker.")
    print("Agent tool output:", result)
    
    # Agent searches history using recall tool
    recall_results = memory.search_recall_memory("Firecracker")
    print("Recall Search Results:", recall_results)
    
    # Agent archives a fact
    archive_result = memory.write_to_archival("preferred_tool_sandbox", "Firecracker MicroVMs")
    print("Archival Write Output:", archive_result)
    
    print("\nUpdated System Context:")
    print(memory.format_system_prompt())
