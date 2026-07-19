"""
Chapter 1: KV Cache Memory Calculator
======================================
Calculate the exact VRAM requirements for the KV Cache of any LLM
architecture. This is the hard infrastructure constraint that determines
how much context your agent can actually use.

From: The Practitioner's Handbook of Agentic AI, Chapter 1.2
"""


def calculate_kv_cache_per_token(
    num_layers: int,
    num_heads: int,
    head_dim: int,
    precision_bytes: int = 2,  # FP16/BF16 = 2 bytes, FP32 = 4 bytes
) -> float:
    """
    Calculate KV cache memory per token in bytes.

    Formula: 2 × num_layers × num_heads × head_dim × precision_bytes
    (2 accounts for storing both K and V matrices)
    """
    return 2 * num_layers * num_heads * head_dim * precision_bytes


def calculate_total_kv_cache(
    num_layers: int,
    num_heads: int,
    head_dim: int,
    context_length: int,
    precision_bytes: int = 2,
    batch_size: int = 1,
) -> dict:
    """
    Calculate total KV cache memory for a given context length.

    Returns a dict with memory in bytes, MB, and GB.
    """
    per_token = calculate_kv_cache_per_token(
        num_layers, num_heads, head_dim, precision_bytes
    )
    total_bytes = per_token * context_length * batch_size

    return {
        "per_token_bytes": per_token,
        "per_token_mb": per_token / (1024 ** 2),
        "total_bytes": total_bytes,
        "total_mb": total_bytes / (1024 ** 2),
        "total_gb": total_bytes / (1024 ** 3),
    }


# ─── Well-known model configurations ────────────────────────────────────────

MODEL_CONFIGS = {
    "Llama-3-70B": {
        "num_layers": 80,
        "num_heads": 64,
        "head_dim": 128,
    },
    "Llama-3-8B": {
        "num_layers": 32,
        "num_heads": 32,
        "head_dim": 128,
    },
    "GPT-4o (estimated)": {
        "num_layers": 120,
        "num_heads": 96,
        "head_dim": 128,
    },
    "Claude-3.5 Sonnet (estimated)": {
        "num_layers": 80,
        "num_heads": 64,
        "head_dim": 128,
    },
    "Gemini-1.5 Pro (estimated)": {
        "num_layers": 64,
        "num_heads": 48,
        "head_dim": 256,
    },
}


if __name__ == "__main__":
    print("=" * 72)
    print("KV Cache Memory Calculator — Agentic AI Infrastructure Planning")
    print("=" * 72)

    context_lengths = [4_096, 32_000, 128_000, 200_000, 1_000_000]

    for model_name, config in MODEL_CONFIGS.items():
        print(f"\n{'─' * 72}")
        print(f"Model: {model_name}")
        print(f"  Layers={config['num_layers']}, "
              f"Heads={config['num_heads']}, "
              f"HeadDim={config['head_dim']}")
        print(f"  {'Context':>12}  {'Per Token':>12}  {'Total KV Cache':>15}")

        for ctx_len in context_lengths:
            result = calculate_total_kv_cache(
                context_length=ctx_len,
                **config
            )
            print(
                f"  {ctx_len:>12,}  "
                f"{result['per_token_mb']:.4f} MB  "
                f"{result['total_gb']:>12.1f} GB"
            )

    print(f"\n{'─' * 72}")
    print("\n⚠️  Agentic Implication:")
    print("   Context Assembly (Chapter 7) is NOT just about prompt quality.")
    print("   It is a HARD INFRASTRUCTURE CONSTRAINT.")
    print("   Sending irrelevant files to the LLM will OOM your servers.")
