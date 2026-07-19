"""
Chapter 2: Dynamic Temperature Sampling
=========================================
Computes entropy of the output logit distribution and adjusts temperature
on the fly. Low entropy → force deterministic. High entropy → allow exploration.

From: The Practitioner's Handbook of Agentic AI, Chapter 2.2
"""

import numpy as np


def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    """Temperature-scaled softmax: P(x_i) = exp(z_i/T) / Σ exp(z_j/T)"""
    scaled = logits / max(temperature, 1e-8)
    exp_vals = np.exp(scaled - np.max(scaled))
    return exp_vals / np.sum(exp_vals)


def shannon_entropy(probs: np.ndarray) -> float:
    """H(P) = -Σ P(x_i) log P(x_i)"""
    return -np.sum(probs * np.log(probs + 1e-9))


def calculate_dynamic_temperature(logits: np.ndarray, base_temp: float = 0.7) -> float:
    """
    Computes entropy of the output logit distribution
    and adjusts temperature on the fly.

    - Low entropy (< 1.0): Model is confident → force T → 0 (deterministic)
    - High entropy (> 2.0): Model is uncertain → allow base_temp for exploration
    """
    probs = softmax(logits, temperature=1.0)
    entropy = shannon_entropy(probs)

    if entropy < 1.0:
        return 0.0  # Force deterministic output
    else:
        return min(base_temp, entropy * 0.3)


def apply_logit_bias(logits: np.ndarray, allowed_tokens: set) -> np.ndarray:
    """
    Forces the LLM to only pick from a subset of valid tokens.
    Used internally by JSON Schema-constrained decoding (Structured Outputs).
    """
    biased = logits.copy()
    for token_id in range(len(biased)):
        if token_id not in allowed_tokens:
            biased[token_id] = -float('inf')  # Impossible to sample
    return biased


# ─── Demo ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)
    vocab_size = 100

    print("=" * 65)
    print("Dynamic Temperature Sampling Demo")
    print("=" * 65)

    # Scenario 1: High confidence (closing bracket in JSON)
    confident_logits = np.random.randn(vocab_size) * 0.5
    confident_logits[42] = 15.0  # One token dominates
    temp1 = calculate_dynamic_temperature(confident_logits)
    print(f"\n🔒 Scenario 1: High confidence (e.g., closing bracket '}}' in JSON)")
    print(f"   Entropy: {shannon_entropy(softmax(confident_logits)):.3f}")
    print(f"   Dynamic Temperature: {temp1:.2f}")
    print(f"   → Deterministic mode: exact syntax guaranteed")

    # Scenario 2: Uncertain (choosing algorithm approach)
    uncertain_logits = np.random.randn(vocab_size) * 2.0
    temp2 = calculate_dynamic_temperature(uncertain_logits)
    print(f"\n🔓 Scenario 2: High uncertainty (e.g., choosing algorithm)")
    print(f"   Entropy: {shannon_entropy(softmax(uncertain_logits)):.3f}")
    print(f"   Dynamic Temperature: {temp2:.2f}")
    print(f"   → Exploration mode: allow alternative logic routes")

    # Demonstrate logit bias
    print(f"\n{'─' * 65}")
    print("Logit Bias Enforcement (Structured Output)")
    print("─" * 65)
    raw_logits = np.random.randn(10)
    allowed = {2, 5, 7}  # Only these token IDs are valid
    biased = apply_logit_bias(raw_logits, allowed)
    probs = softmax(biased)
    print(f"   Allowed tokens: {allowed}")
    print(f"   Probabilities after bias:")
    for i, p in enumerate(probs):
        marker = "✓" if i in allowed else "✗"
        print(f"     Token {i}: {p:.4f} {marker}")
