# Chapter 3: The ReAct Paradigm — Code Lab

> 📖 **Book Chapter**: [Chapter 3 — The ReAct Paradigm](../../book/chapter_3_react.md)

Production-grade ReAct agent loop implementations with loop detection, cost tracking, self-healing code execution, and reasoning model integration.

---

## 🎯 Multi-Tier Learning Tracks

### 🎓 Student Track (Foundations)
- **Concept**: Understand the cyclic **Thought -> Action -> Observation** execution loop.
- **Lab Command**: `python react_orchestrator.py`
- **Exercise**: Trace how observations are appended to the conversation history for the next iteration.

### 🔬 Researcher Track (Empirical Benchmarks)
- **Experiment**: Run `reasoning_model_integration.py` to compare reasoning models (DeepSeek R1 / Claude Extended Thinking) vs standard ReAct prompts on multi-step logic.
- **Loop Induction**: Test how prompt loop detection prevents infinite agent execution loops.

### 🚀 AI Engineer Track (Production Systems)
- **Production Guardrail**: Enforce hard token and financial cost budgets (`max_cost_usd`) on every agent trajectory to prevent runaway billings.
- **Self-Healing**: Use `self_healing_executor.py` to catch execution errors and feed stack traces back into the model for automated recovery.

---

## 🛠️ Code Modules

| Module | Key Concept |
|--------|-------------|
| [`react_orchestrator.py`](./react_orchestrator.py) | Full ReAct loop, loop detection & cost tracking |
| [`self_healing_executor.py`](./self_healing_executor.py) | Automated error recovery loop |
| [`retry_with_backoff.py`](./retry_with_backoff.py) | Exponential backoff for API resilience |
| [`reasoning_model_integration.py`](./reasoning_model_integration.py) | Reasoning model (<thought> token) integration |
