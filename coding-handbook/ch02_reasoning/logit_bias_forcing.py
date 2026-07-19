"""
Logit Bias Forcing & Schema Enforcement

Demonstrates how LLM providers allow forcing token sampling by adding a large positive
or negative logit bias value to specific token IDs.
"""

import numpy as np

def apply_logit_bias(logits: np.ndarray, allowed_tokens: list[int], bias_value: float = 100.0) -> np.ndarray:
    """
    Applies logit bias to restrict token generation.
    Tokens in allowed_tokens get boosted, others get heavily penalized.
    """
    biased_logits = np.copy(logits)
    
    # Apply a massive negative bias to all tokens except those allowed
    for token_id in range(len(biased_logits)):
        if token_id not in allowed_tokens:
            biased_logits[token_id] -= bias_value
            
    return biased_logits

if __name__ == "__main__":
    # Simulating a vocabulary of 10 tokens
    # Output token target must be token 3 ("{") or token 5 ("[") for starting JSON/lists
    vocab = ["the", "quick", "brown", "{", "fox", "[", "jumps", "over", "lazy", "dog"]
    print("Vocabulary:", {i: word for i, word in enumerate(vocab)})
    
    # Mock logits from the model
    mock_logits = np.array([2.1, 1.5, 0.2, -1.5, 3.1, -2.0, 0.5, 0.9, -0.4, 1.1])
    print("\nOriginal Logits:", mock_logits)
    
    # Force JSON start
    allowed_start_tokens = [3, 5] # "{" or "["
    biased = apply_logit_bias(mock_logits, allowed_start_tokens, bias_value=10.0)
    print("Biased Logits (forcing JSON):", biased)
    
    # Probabilities
    orig_probs = np.exp(mock_logits) / np.sum(np.exp(mock_logits))
    biased_probs = np.exp(biased) / np.sum(np.exp(biased))
    
    print("\nOriginal Probs:", [f"{p:.4f}" for p in orig_probs])
    print("Biased Probs:  ", [f"{p:.4f}" for p in biased_probs])
    
    selected_token = np.argmax(biased_probs)
    print(f"\nForced next token selection: '{vocab[selected_token]}'")
