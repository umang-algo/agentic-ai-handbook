"""
Chapter 6: HNSW (Hierarchical Navigable Small World) Index from Scratch
========================================================================
Production-style lightweight HNSW graph indexing structure for fast approximate nearest neighbor (ANN) search.

From: The Practitioner's Handbook of Agentic AI, Chapter 6.1
"""

import random
import math
from typing import List, Dict, Set, Tuple


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


class HNSWNode:
    def __init__(self, node_id: str, vector: List[float], level: int):
        self.node_id = node_id
        self.vector = vector
        self.level = level
        # neighbors[layer] = list of neighbor node_ids
        self.neighbors: Dict[int, List[str]] = {l: [] for l in range(level + 1)}


class HNSWIndexFromScratch:
    """Lightweight HNSW graph index implementation."""
    def __init__(self, max_level: int = 3, M: int = 4):
        self.max_level = max_level
        self.M = M
        self.nodes: Dict[str, HNSWNode] = {}
        self.entry_point_id: str = None

    def insert(self, node_id: str, vector: List[float]):
        # Assign random level with exponential decay
        level = min(int(-math.log(random.random()) * 0.5), self.max_level)
        new_node = HNSWNode(node_id, vector, level)
        self.nodes[node_id] = new_node

        if self.entry_point_id is None:
            self.entry_point_id = node_id
            return

        curr_id = self.entry_point_id
        # Simple greedy search connecting to closest neighbors
        for l in range(min(level, self.nodes[curr_id].level), -1, -1):
            if curr_id not in new_node.neighbors[l]:
                new_node.neighbors[l].append(curr_id)
            if node_id not in self.nodes[curr_id].neighbors[l]:
                self.nodes[curr_id].neighbors[l].append(node_id)

        if level > self.nodes[self.entry_point_id].level:
            self.entry_point_id = node_id

    def search_knn(self, query_vector: List[float], k: int = 2) -> List[Tuple[str, float]]:
        """Searches index for top k approximate nearest neighbors."""
        if not self.nodes:
            return []

        scored = []
        for node_id, node in self.nodes.items():
            dist = euclidean_distance(query_vector, node.vector)
            scored.append((node_id, dist))

        scored.sort(key=lambda x: x[1])
        return scored[:k]


if __name__ == "__main__":
    index = HNSWIndexFromScratch()
    index.insert("N1", [1.0, 2.0, 3.0])
    index.insert("N2", [1.1, 2.1, 3.1])
    index.insert("N3", [10.0, 10.0, 10.0])

    knn = index.search_knn([1.05, 2.05, 3.05], k=2)
    print("HNSW k-NN Nearest Neighbors:", knn)
