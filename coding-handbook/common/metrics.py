"""
Common Metrics, VRAM Estimator & Cost Accounting Engine
=======================================================
VRAM memory estimation formulas, latency metrics (TTFT, TPS), and token cost calculators.

From: The Practitioner's Handbook of Agentic AI
"""

import math
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class VRAMEstimate:
    model_params_billions: float
    context_length_tokens: int
    num_layers: int
    hidden_dim: int
    num_heads: int
    precision_bytes: int  # 2 for fp16, 1 for int8, 0.5 for int4
    
    weights_vram_gb: float
    kv_cache_vram_gb: float
    total_vram_gb: float


def estimate_kv_cache_vram(
    context_length: int,
    num_layers: int = 80,
    hidden_dim: int = 8192,
    num_heads: int = 64,
    precision_bytes: int = 2,
    batch_size: int = 1
) -> float:
    """
    Exact KV Cache Memory Formula:
    KV_bytes = 2 * num_layers * hidden_dim * context_length * batch_size * precision_bytes
    Returns size in Gigabytes (GB).
    """
    kv_bytes = 2 * num_layers * hidden_dim * context_length * batch_size * precision_bytes
    return kv_bytes / (1024 ** 3)


def calculate_model_vram(
    params_b: float,
    context_tokens: int,
    precision_bits: int = 16,
    num_layers: int = 80,
    hidden_dim: int = 8192,
    num_heads: int = 64,
    batch_size: int = 1
) -> VRAMEstimate:
    """Calculates model weights VRAM + KV Cache VRAM footprint."""
    precision_bytes = precision_bits / 8.0
    weights_gb = params_b * precision_bytes
    kv_cache_gb = estimate_kv_cache_vram(context_tokens, num_layers, hidden_dim, num_heads, precision_bytes, batch_size)
    total_gb = weights_gb + kv_cache_gb

    return VRAMEstimate(
        model_params_billions=params_b,
        context_length_tokens=context_tokens,
        num_layers=num_layers,
        hidden_dim=hidden_dim,
        num_heads=num_heads,
        precision_bytes=precision_bytes,
        weights_vram_gb=round(weights_gb, 2),
        kv_cache_vram_gb=round(kv_cache_gb, 2),
        total_vram_gb=round(total_gb, 2)
    )


class CostTracker:
    """Token cost tracking utility for OpenAI, Anthropic, and open-source models."""
    MODEL_RATES = {
        "gpt-4o": {"input": 2.50 / 1e6, "output": 10.00 / 1e6},
        "claude-3-5-sonnet": {"input": 3.00 / 1e6, "output": 15.00 / 1e6},
        "deepseek-r1": {"input": 0.55 / 1e6, "output": 2.19 / 1e6},
        "llama-3-70b": {"input": 0.70 / 1e6, "output": 0.90 / 1e6},
    }

    @classmethod
    def calculate_cost(cls, model: str, input_tokens: int, output_tokens: int) -> float:
        rates = cls.MODEL_RATES.get(model.lower(), {"input": 2.0 / 1e6, "output": 8.0 / 1e6})
        cost = (input_tokens * rates["input"]) + (output_tokens * rates["output"])
        return round(cost, 6)


if __name__ == "__main__":
    vram = calculate_model_vram(params_b=70.0, context_tokens=128000, precision_bits=16)
    print("70B Model VRAM Breakdown (128k context, FP16):")
    print(f"Weights VRAM:  {vram.weights_vram_gb} GB")
    print(f"KV Cache VRAM: {vram.kv_cache_vram_gb} GB")
    print(f"Total VRAM:    {vram.total_vram_gb} GB")

    cost = CostTracker.calculate_cost("gpt-4o", input_tokens=100000, output_tokens=2000)
    print(f"\nCost for 100k input / 2k output on GPT-4o: ${cost:.4f}")
