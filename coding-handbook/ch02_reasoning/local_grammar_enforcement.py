"""
Local LLM Grammar Enforcement & Logit Masking

Demonstrates how local inference engines (such as Outlines or llama.cpp)
use Finite State Machines (FSMs) to mask token logits at each generation step,
enforcing strict JSON/regex formatting.
"""

import numpy as np
from typing import List, Dict

class LocalGrammarFSM:
    """Simulates an FSM that enforces a schema: '{"status": "PASS" | "FAIL"}'"""
    def __init__(self, vocab: List[str]):
        self.vocab = vocab
        # Define state transitions:
        # State 0: expects '{"status": "'
        # State 1: expects 'PASS' or 'FAIL'
        # State 2: expects '"}'
        # State 3: Terminal State (accepts nothing)
        self.state = 0

    def get_allowed_tokens(self) -> List[int]:
        """Returns the token IDs allowed in the current FSM state."""
        allowed = []
        for token_id, token in enumerate(self.vocab):
            if self.state == 0 and token == '{"status": "':
                allowed.append(token_id)
            elif self.state == 1 and token in ["PASS", "FAIL"]:
                allowed.append(token_id)
            elif self.state == 2 and token == '"}':
                allowed.append(token_id)
        return allowed

    def transition(self, token: str) -> None:
        """Transitions FSM based on the generated token."""
        if self.state == 0 and token == '{"status": "':
            self.state = 1
        elif self.state == 1 and token in ["PASS", "FAIL"]:
            self.state = 2
        elif self.state == 2 and token == '"}':
            self.state = 3
        else:
            raise ValueError(f"Invalid transition from state {self.state} with token '{token}'")

def mask_logits(logits: np.ndarray, allowed_token_ids: List[int]) -> np.ndarray:
    """Applies negative infinity masks to all disallowed token IDs."""
    masked = np.copy(logits)
    mask = np.ones_like(logits, dtype=bool)
    mask[allowed_token_ids] = False
    masked[mask] = -np.inf
    return masked

if __name__ == "__main__":
    vocab = ["the", "quick", "PASS", '{"status": "', "FAIL", '"}', "success", "error"]
    print("Inference Engine Vocabulary:")
    print({i: t for i, t in enumerate(vocab)})

    fsm = LocalGrammarFSM(vocab)
    
    # Let's run a 3-step generation simulation
    for step in range(3):
        print(f"\n--- Generation Step {step+1} (FSM State {fsm.state}) ---")
        
        # Mock model logits output
        logits = np.array([2.5, -1.0, 3.2, 0.5, 1.2, -0.4, 4.1, 0.9])
        
        # Get allowable tokens according to grammar
        allowed_ids = fsm.get_allowed_tokens()
        print("Grammar-allowed Token IDs:", allowed_ids, f"({[vocab[i] for i in allowed_ids]})")
        
        # Mask out-of-schema logits
        masked = mask_logits(logits, allowed_ids)
        print("Masked Logits (unallowed set to -inf):", masked)
        
        # Compute probabilities
        exp = np.exp(masked - np.max(masked)) # stabilized exp
        probs = exp / np.sum(exp)
        print("Filtered Sampling Probs:             ", [f"{p:.2f}" for p in probs])
        
        # Select highest probability token
        selected_id = np.argmax(probs)
        selected_token = vocab[selected_id]
        print(f"Sampled Token: '{selected_token}'")
        
        # Advance FSM
        fsm.transition(selected_token)
        
    print(f"\nFinal FSM State: {fsm.state} (Reached terminal output)")
