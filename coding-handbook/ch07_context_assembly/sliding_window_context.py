"""
Token-Budgeted Sliding Window Context Assembly

Demonstrates dynamic context assembly. When the conversation history exceeds
the model's token limits, older messages are pruned, summarized, or removed.
"""

from typing import List, Dict

class SlidingWindowContext:
    def __init__(self, max_token_budget: int = 100):
        self.max_token_budget = max_token_budget
        self.messages: List[Dict[str, str]] = []

    def _estimate_tokens(self, message: Dict[str, str]) -> int:
        # Simple token estimation: 1 word ~ 1.3 tokens
        word_count = len(message.get("content", "").split())
        return int(word_count * 1.3) + 4 # base overhead per message

    def add_message(self, role: str, content: str) -> None:
        new_msg = {"role": role, "content": content}
        self.messages.append(new_msg)
        self.prune_context()

    def prune_context(self) -> None:
        """Removes oldest messages until current tokens are within the max budget."""
        while self.get_total_tokens() > self.max_token_budget and len(self.messages) > 1:
            # We keep the system prompt (first message) if it's there, prune the second one
            if self.messages[0]["role"] == "system":
                pruned = self.messages.pop(1)
            else:
                pruned = self.messages.pop(0)
            print(f"[Pruning context]: removed '{pruned['role']}' message: '{pruned['content'][:20]}...'")

    def get_total_tokens(self) -> int:
        return sum(self._estimate_tokens(m) for m in self.messages)

if __name__ == "__main__":
    ctx = SlidingWindowContext(max_token_budget=50)
    
    # 1. System Prompt
    ctx.add_message("system", "You are a database helper.")
    
    # 2. Iterations of dialogue
    ctx.add_message("user", "Explain SQL indexes.")
    ctx.add_message("assistant", "Indexes make lookups faster by organizing columns.")
    print("Current tokens:", ctx.get_total_tokens())
    
    # 3. Add heavy context that forces pruning
    ctx.add_message("user", "What is HNSW and is it related to SQL B-trees?")
    print("Final token count:", ctx.get_total_tokens())
    print("Active messages:")
    for m in ctx.messages:
        print(f"- {m['role']}: {m['content']}")
