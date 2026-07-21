"""
Chapter 5: Asymmetric Embedding Search Engine
=============================================
Implementation of asymmetric query vs document embedding retrieval with cosine similarity scoring.

From: The Practitioner's Handbook of Agentic AI, Chapter 5.1
"""

import math
from typing import List, Dict, Any


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculates cosine similarity between two numeric vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class AsymmetricEmbeddingSearch:
    """Asymmetric embedding search engine for short user queries against long document passages."""
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def add_document(self, doc_id: str, content: str, embedding: List[float]):
        self.documents.append({
            "doc_id": doc_id,
            "content": content,
            "embedding": embedding
        })

    def search(self, query_embedding: List[float], top_k: int = 2) -> List[Dict[str, Any]]:
        """Ranks document passages by asymmetric vector similarity."""
        results = []
        for doc in self.documents:
            sim = cosine_similarity(query_embedding, doc["embedding"])
            results.append({
                "doc_id": doc["doc_id"],
                "content": doc["content"],
                "similarity_score": round(sim, 4)
            })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]


if __name__ == "__main__":
    search_engine = AsymmetricEmbeddingSearch()
    # Simulated passage embeddings (dimension 4 for demo)
    search_engine.add_document("doc1", "ReAct agents alternate between thought, action, and observation.", [0.8, 0.1, 0.5, 0.2])
    search_engine.add_document("doc2", "Vector databases index embeddings using HNSW graph algorithms.", [0.1, 0.9, 0.2, 0.7])

    query_emb = [0.75, 0.15, 0.45, 0.25]  # Query about ReAct agents
    top_docs = search_engine.search(query_emb, top_k=1)
    print("Top Matching Document:", top_docs)
