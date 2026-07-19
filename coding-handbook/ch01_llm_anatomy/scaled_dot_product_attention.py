"""
Chapter 1: Scaled Dot-Product Attention
========================================
The exact NumPy implementation of the attention mechanism used in every
Transformer-based LLM (GPT-4, Claude, Llama-3).

From: The Practitioner's Handbook of Agentic AI, Chapter 1.3
"""

import numpy as np


def scaled_dot_product_attention(Q, K, V, d_k, mask=None):
    """
    Computes masked scaled dot-product attention (Decoder-only behavior).

    Args:
        Q: Query matrix, shape (seq_length, d_k)
        K: Key matrix, shape (seq_length, d_k)
        V: Value matrix, shape (seq_length, d_v)
        d_k: Dimension of keys (for scaling)
        mask: Optional causal mask, shape (seq_length, seq_length)

    Returns:
        output: Attended values, shape (seq_length, d_v)
        attention_weights: Attention distribution, shape (seq_length, seq_length)
    """
    # QK^T gives the raw attention scores (Logits)
    # Shape: (seq_length, seq_length)
    scores = np.dot(Q, K.T) / np.sqrt(d_k)

    # Decoder Masking: Prevent looking into the future
    if mask is not None:
        # We add -infinity to future tokens so softmax turns them to 0
        scores = np.where(mask == 0, -1e9, scores)

    # Softmax normalizes the scores across the sequence to sum to 1
    # Shape: (seq_length, seq_length)
    attention_weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    attention_weights /= attention_weights.sum(axis=-1, keepdims=True)

    # Multiply by Value matrix
    # Shape: (seq_length, d_v)
    output = np.dot(attention_weights, V)

    return output, attention_weights


def create_causal_mask(seq_length):
    """Creates a lower-triangular causal mask for decoder-only attention."""
    return np.tril(np.ones((seq_length, seq_length)))


# ─── Demo ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)

    seq_length = 6
    d_k = 64
    d_v = 64

    # Random Q, K, V matrices (simulating token embeddings)
    Q = np.random.randn(seq_length, d_k)
    K = np.random.randn(seq_length, d_k)
    V = np.random.randn(seq_length, d_v)

    # Create causal mask (decoder-only: can't look ahead)
    mask = create_causal_mask(seq_length)

    output, weights = scaled_dot_product_attention(Q, K, V, d_k, mask)

    print("=" * 60)
    print("Scaled Dot-Product Attention Demo")
    print("=" * 60)
    print(f"\nSequence length: {seq_length}")
    print(f"Key dimension (d_k): {d_k}")
    print(f"\nAttention weights (each row sums to 1.0):")
    for i, row in enumerate(weights):
        print(f"  Token {i}: {np.round(row, 3)}")

    print(f"\nOutput shape: {output.shape}")
    print(f"\n--- The Dilution Problem ---")
    print(f"If we double the context with irrelevant tokens,")
    print(f"each token's attention budget gets spread thinner.")
    print(f"Max weight for Token 0: {weights[0].max():.4f}")

    # Demonstrate dilution with longer sequence
    long_seq = 24
    Q2 = np.random.randn(long_seq, d_k)
    K2 = np.random.randn(long_seq, d_k)
    V2 = np.random.randn(long_seq, d_v)
    mask2 = create_causal_mask(long_seq)
    _, weights2 = scaled_dot_product_attention(Q2, K2, V2, d_k, mask2)

    print(f"Max weight for Token 0 (4x context): {weights2[0].max():.4f}")
    print(f"  → Attention is diluted when irrelevant context is added")
