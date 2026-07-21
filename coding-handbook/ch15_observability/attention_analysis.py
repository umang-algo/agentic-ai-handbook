"""
Chapter 15: Agent Attention & Token Activation Debugger
======================================================
Observability module tracking token activation patterns, prompt entropy, and cost breakdown across agent trajectories.

From: The Practitioner's Handbook of Agentic AI, Chapter 15.1
"""

import json
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class TokenActivation:
    token: str
    activation_score: float
    is_tool_call: bool


class AgentAttentionDebugger:
    """Observability debugger analyzing agent reasoning steps and attention distribution."""
    def __init__(self):
        self.step_logs: List[Dict[str, Any]] = []

    def compute_prompt_entropy(self, token_probs: List[float]) -> float:
        """Calculates Shannon entropy over model output token probability distributions."""
        entropy = 0.0
        for p in token_probs:
            if p > 0.0:
                entropy -= p * math.log2(p)
        return round(entropy, 4)

    def log_agent_step(self, step_number: int, prompt: str, generated_text: str, token_probs: List[float]) -> Dict[str, Any]:
        """Logs step trajectory with token entropy metrics."""
        entropy = self.compute_prompt_entropy(token_probs)
        log_entry = {
            "step_number": step_number,
            "prompt_length_chars": len(prompt),
            "generated_text": generated_text,
            "shannon_entropy": entropy,
            "uncertainty_level": "HIGH" if entropy > 2.5 else "NORMAL"
        }
        self.step_logs.append(log_entry)
        return log_entry


if __name__ == "__main__":
    debugger = AgentAttentionDebugger()
    
    # Step 1: Low entropy / confident decision
    log1 = debugger.log_agent_step(
        step_number=1,
        prompt="Execute SQL query for order ORD-9021.",
        generated_text="Action: execute_sql_query(order_id='ORD-9021')",
        token_probs=[0.95, 0.98, 0.92, 0.96]
    )
    print("Step 1 Log:", json.dumps(log1, indent=2))

    # Step 2: High entropy / uncertain decision
    log2 = debugger.log_agent_step(
        step_number=2,
        prompt="User query ambiguous.",
        generated_text="Thought: I am unsure whether to refund or issue store credit.",
        token_probs=[0.35, 0.40, 0.25, 0.30]
    )
    print("\nStep 2 Log:", json.dumps(log2, indent=2))
