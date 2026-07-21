# Chapter 10: Multi-Agent State Machines — Code Lab

> 📖 **Book Chapter**: [Chapter 10 — Multi-Agent State Machines](../../book/chapter_10_multi_agent.md)

Directed Acyclic Graph (DAG) state machine orchestrators, topological sorting, and thread checkpoint serialization.

---

## 🎯 Multi-Tier Learning Tracks

### 🎓 Student Track (Foundations)
- **Concept**: Learn why multi-agent systems use state machine DAGs instead of nested `while` loops.
- **Lab Command**: `python dag_state_machine.py`

### 🔬 Researcher Track (Empirical Benchmarks)
- **Graph Algorithms**: Evaluate topological sorting ($O(V + E)$) for task dependency scheduling in `dag_topological_sort.py`.

### 🚀 AI Engineer Track (Production Systems)
- **Checkpointing & Recovery**: Serialize agent state to database backends using `checkpoint_serializer.py` for human-in-the-loop sign-offs and crash recovery.

---

## 🛠️ Code Modules

| Module | Key Concept |
|--------|-------------|
| [`dag_state_machine.py`](./dag_state_machine.py) | DAG multi-agent orchestrator |
| [`dag_topological_sort.py`](./dag_topological_sort.py) | Topological sort for task dependency graphs |
| [`checkpoint_serializer.py`](./checkpoint_serializer.py) | Workflow state checkpoint serialization |
