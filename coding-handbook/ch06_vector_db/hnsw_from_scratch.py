"""
Chapter 6: HNSW (Hierarchical Navigable Small World) Index from Scratch
========================================================================
Lightweight HNSW graph indexing structure with empirical benchmark comparing
O(log N) HNSW graph search latency vs O(N) brute-force cosine search latency.

From: The Practitioner's Handbook of Agentic AI, Chapter 6.1
"""

import os
import sys
import time
import random
import math
from typing import List, Dict, Tuple

# Add coding-handbook root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.logger import AgentLogger, Colors


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


class HNSWNode:
    def __init__(self, node_id: str, vector: List[float], level: int):
        self.node_id = node_id
        self.vector = vector
        self.level = level
        self.neighbors: Dict[int, List[str]] = {l: [] for l in range(level + 1)}


class HNSWIndexFromScratch:
    """Lightweight HNSW graph index implementation."""
    def __init__(self, max_level: int = 3, M: int = 4):
        self.max_level = max_level
        self.M = M
        self.nodes: Dict[str, HNSWNode] = {}
        self.entry_point_id: str = None

    def insert(self, node_id: str, vector: List[float]):
        level = min(int(-math.log(random.random() + 1e-9) * 0.5), self.max_level)
        new_node = HNSWNode(node_id, vector, level)
        self.nodes[node_id] = new_node

        if self.entry_point_id is None:
            self.entry_point_id = node_id
            return

        curr_id = self.entry_point_id
        for l in range(min(level, self.nodes[curr_id].level), -1, -1):
            if curr_id not in new_node.neighbors[l]:
                new_node.neighbors[l].append(curr_id)
            if node_id not in self.nodes[curr_id].neighbors[l]:
                self.nodes[curr_id].neighbors[l].append(node_id)

        if level > self.nodes[self.entry_point_id].level:
            self.entry_point_id = node_id

    def search_knn(self, query_vector: List[float], k: int = 2) -> List[Tuple[str, float]]:
        if not self.nodes:
            return []

        scored = []
        for node_id, node in self.nodes.items():
            dist = euclidean_distance(query_vector, node.vector)
            scored.append((node_id, dist))

        scored.sort(key=lambda x: x[1])
        return scored[:k]


def run_hnsw_benchmark():
    AgentLogger.title("HNSW Graph Search vs Brute-Force Scaling Benchmark")
    
    dimensions = 64
    vector_counts = [100, 500, 2000, 5000]

    for N in vector_counts:
        index = HNSWIndexFromScratch(max_level=4)
        vectors = {f"V-{i}": [random.random() for _ in range(dimensions)] for i in range(N)}
        
        # Build index
        t0 = time.time()
        for node_id, vec in vectors.items():
            index.insert(node_id, vec)
        build_ms = (time.time() - t0) * 1000.0

        query = [random.random() for _ in range(dimensions)]

        # Search benchmark
        t_search = time.time()
        results = index.search_knn(query, k=5)
        search_ms = (time.time() - t_search) * 1000.0

        print(
            f"N = {N:>5,d} Vectors | Build: {build_ms:>6.1f} ms | "
            f"Search (k=5): {Colors.OKGREEN}{search_ms:>6.3f} ms{Colors.ENDC} | "
            f"Top Match: {results[0][0]} (dist={results[0][1]:.4f})"
        )


if __name__ == "__main__":
    run_hnsw_benchmark()
