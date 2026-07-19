# Chapter 3: The ReAct Paradigm — Code Lab

> 📖 **Book Chapter**: [Chapter 3 — The ReAct Paradigm](../../book/chapter_3_react.md)

## What You'll Build
- Production ReAct orchestrator with loop detection and cost caps
- Self-healing compiler diagnostic loop
- Exponential backoff with full jitter

## Files

| File | Description |
|------|-------------|
| `react_orchestrator.py` | Full ReActState with loop detection, cost tracking, and audit trail |
| `self_healing_executor.py` | Execute code with auto-repair on failure |
| `retry_with_backoff.py` | Full-jitter exponential backoff for rate limits |
| `reasoning_model_integration.py` | Parse DeepSeek-R1 <think> blocks & execute thoughtless loops |
