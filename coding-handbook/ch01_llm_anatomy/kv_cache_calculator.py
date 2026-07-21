"""
Chapter 1: KV Cache & VRAM Calculator
======================================
Production VRAM and KV Cache memory footprint calculator for LLM inference.
Calculates weights VRAM, KV Cache VRAM, and total memory footprint across model architectures,
context lengths (4k to 1M tokens), and quantization precisions (FP16, INT8, INT4).

From: The Practitioner's Handbook of Agentic AI, Chapter 1.2
"""

import sys
import os
from dataclasses import dataclass

# Add coding-handbook root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.logger import AgentLogger, Colors
from common.metrics import calculate_model_vram, VRAMEstimate


@dataclass
class ModelProfile:
    name: str
    params_b: float
    num_layers: int
    hidden_dim: int
    num_heads: int


def run_kv_cache_benchmark():
    AgentLogger.title("KV Cache & VRAM Footprint Empirical Benchmark")

    models = [
        ModelProfile("Llama-3-8B", 8.0, 32, 4096, 32),
        ModelProfile("Llama-3-70B", 70.0, 80, 8192, 64),
        ModelProfile("DeepSeek-R1-671B", 671.0, 128, 14336, 128),
    ]

    contexts = [4096, 32768, 131072, 1048576]
    precisions = [("FP16", 16), ("INT8", 8), ("INT4", 4)]

    for model in models:
        AgentLogger.section(f"Model Architecture: {model.name} ({model.params_b}B Parameters)")
        for ctx in contexts:
            for prec_name, prec_bits in precisions:
                vram = calculate_model_vram(
                    params_b=model.params_b,
                    context_tokens=ctx,
                    precision_bits=prec_bits,
                    num_layers=model.num_layers,
                    hidden_dim=model.hidden_dim,
                    num_heads=model.num_heads
                )
                print(
                    f"  Ctx: {ctx:>7,d} tok | Precision: {prec_name:>4} -> "
                    f"Weights: {vram.weights_vram_gb:>6.1f} GB | "
                    f"KV Cache: {vram.kv_cache_vram_gb:>6.1f} GB | "
                    f"{Colors.BOLD}Total: {vram.total_vram_gb:>6.1f} GB{Colors.ENDC}"
                )
        print()


if __name__ == "__main__":
    run_kv_cache_benchmark()
