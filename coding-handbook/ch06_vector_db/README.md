# Chapter 6: Building a Vector Database — Code Lab

> 📖 **Book Chapter**: [Chapter 6 — Building a Vector Database](../../book/chapter_6_vector_db.md)

HNSW graph indexing from scratch, AST code chunking, and Graph RAG memory structures.

---

## 🎯 Multi-Tier Learning Tracks

### 🎓 Student Track (Foundations)
- **Concept**: Understand why naive string splitting breaks code chunking and how AST parsing keeps functions intact.
- **Lab Command**: `python ast_code_chunker.py`

### 🔬 Researcher Track (Empirical Benchmarks)
- **Mathematical Complexity**: $O(\log N)$ HNSW graph search vs $O(N)$ brute-force vector search.
- **Experiment**: Run `python hnsw_from_scratch.py` to compare search latency across scaling vector counts ($N=100$ to $N=5,000$).

### 🚀 AI Engineer Track (Production Systems)
- **Graph RAG**: Combine vector embeddings with knowledge graph relationships using `graph_rag_memory.py` for structured code navigation.

---

## 🛠️ Code Modules

| Module | Key Concept |
|--------|-------------|
| [`hnsw_from_scratch.py`](./hnsw_from_scratch.py) | Hierarchical Navigable Small World (HNSW) graph index |
| [`ast_code_chunker.py`](./ast_code_chunker.py) | AST-aware python function & class scope chunker |
| [`graph_rag_memory.py`](./graph_rag_memory.py) | Graph RAG memory retriever |
