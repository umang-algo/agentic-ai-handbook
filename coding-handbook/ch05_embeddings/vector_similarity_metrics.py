"""
Chapter 5: Vector Similarity Metrics
======================================
Cosine Similarity, Dot Product, and L2 Distance with normalization
optimization. Demonstrates why normalized vectors make Cosine = Dot Product.

From: The Practitioner's Handbook of Agentic AI, Chapter 5.1
"""

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine(A, B) = (A · B) / (||A|| × ||B||)"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """Dot(A, B) = Σ A_i × B_i"""
    return np.dot(a, b)


def l2_distance(a: np.ndarray, b: np.ndarray) -> float:
    """L2(A, B) = ||A - B||_2 = sqrt(Σ (A_i - B_i)²)"""
    return np.linalg.norm(a - b)


def normalize(v: np.ndarray) -> np.ndarray:
    """Normalize to unit length: ||v|| = 1"""
    return v / np.linalg.norm(v)


if __name__ == "__main__":
    np.random.seed(42)
    print("=" * 60)
    print("Vector Similarity Metrics Demo")
    print("=" * 60)

    a = np.random.randn(1536)  # OpenAI embedding dimension
    b = np.random.randn(1536)

    print(f"\nRaw vectors:")
    print(f"  Cosine:      {cosine_similarity(a, b):.6f}")
    print(f"  Dot Product: {dot_product(a, b):.6f}")
    print(f"  L2 Distance: {l2_distance(a, b):.6f}")

    # Normalize
    a_norm = normalize(a)
    b_norm = normalize(b)

    print(f"\nNormalized vectors (||v|| = 1):")
    print(f"  Cosine:      {cosine_similarity(a_norm, b_norm):.6f}")
    print(f"  Dot Product: {dot_product(a_norm, b_norm):.6f}")
    print(f"  L2 Distance: {l2_distance(a_norm, b_norm):.6f}")
    print(f"\n  → Cosine == Dot Product for normalized vectors!")
    print(f"  → This lets vector DBs skip expensive sqrt/division ops")

    # VRAM calculation
    n_files = 10_000
    chunks_per_file = 5
    dim = 3072
    bytes_per_float = 4
    total = n_files * chunks_per_file * dim * bytes_per_float
    print(f"\n{'─' * 60}")
    print(f"VRAM for {n_files:,} files × {chunks_per_file} chunks × {dim}d:")
    print(f"  {total / 1024**2:.1f} MB — easily fits in RAM")
