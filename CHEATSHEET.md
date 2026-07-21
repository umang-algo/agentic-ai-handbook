# ⚡ The Ultimate Agentic AI Cheat Sheet

> **A 1-page quick-reference guide for AI Engineers, LLM Researchers, and System Architects.**
> Companion reference for [*The Practitioner's Handbook of Agentic AI*](https://github.com/umang-algo/agentic-ai-handbook).

---

## 1. 🧮 KV Cache & VRAM Math

### Memory Formula
$$\text{KV Cache (Bytes)} = 2 \times N_{\text{layers}} \times D_{\text{hidden}} \times L_{\text{ctx}} \times B \times P_{\text{bytes}}$$

### Quick Estimation Table (FP16 / 2 Bytes per parameter)

| Model Size | Model Weights VRAM | 4k Context KV Cache | 32k Context KV Cache | 128k Context KV Cache |
|------------|-------------------|----------------------|----------------------|-----------------------|
| **8B (Llama 3)** | ~16 GB | 0.25 GB | 2.0 GB | 8.0 GB |
| **70B (Llama 3)** | ~140 GB | 1.0 GB | 8.0 GB | 32.0 GB |
| **671B (DeepSeek R1)** | ~1,342 GB | 4.0 GB | 32.0 GB | 128.0 GB |

*Rule of Thumb:* At FP16, KV Cache requires **~0.25 MB per token** on a 70B model.

---

## 2. 🔄 The ReAct Loop Pattern

```
User Prompt --> [System Prompt + Tools Schema] --> LLM Reasoning (<thought>)
                                                        |
                                                        v
                                                [Action Proposed]
                                                        |
                                                        v
                                            [Execute Tool Sandbox]
                                                        |
                                                        v
User Response <-- [Final Answer] <-- [Append Observation to Context]
```

### Production Guardrails Checklist
- [x] **Loop Detection**: Hash `(action_name, action_args)`. Terminate if duplicate action appears $\ge 2$ times.
- [x] **Max Iteration Limit**: Set hard ceiling (e.g. `max_iterations = 10`).
- [x] **Financial Budget**: Set cost cap (e.g. `max_cost_usd = $1.00`).
- [x] **Self-Healing**: Catch tool exceptions and append stack trace back into context for automated repair.

---

## 3. 🔍 Vector Search: HNSW vs Flat vs IVF

| Index Type | Search Time Complexity | Memory Footprint | Recall Accuray | Best Used For |
|------------|------------------------|------------------|----------------|---------------|
| **Flat (Brute-Force)** | $O(N \cdot d)$ | Low | 100% (Exact) | Small sets ($N < 10k$) |
| **HNSW (Graph)** | $O(\log N)$ | High | 95-99% (ANN) | High-speed production ($N > 100k$) |
| **IVF (Inverted File)** | $O(\sqrt{N})$ | Medium | 90-95% (ANN) | Memory-constrained systems |

---

## 4. 🌐 Model Context Protocol (MCP) Lifecycle

```
Client (Agent)                                            Server (MCP Tool)
    |                                                            |
    |---- 1. JSON-RPC: initialize ------------------------------>|
    |<--- 2. Result (Server Capabilities) -----------------------|
    |---- 3. Notifications: initialized ------------------------>|
    |                                                            |
    |---- 4. tools/list ---------------------------------------->|
    |<--- 5. Result [{name: "query_db", schema: {...}}] --------|
    |                                                            |
    |---- 6. tools/call (name: "query_db", args: {...}) -------->|
    |<--- 7. Result {content: [{type: "text", text: "..."}]} ---|
```

---

## 5. 📊 Evaluation & Benchmark Metrics

### Pass@k Unbiased Estimator (HumanEval)
$$\text{pass}@k = 1 - \frac{\binom{n - c}{k}}{\binom{n}{k}}$$
*where $n$ = total samples per problem, $c$ = correct samples, $k$ = threshold.*

### Benchmark Distinction
- **HumanEval / MBPP**: Function-level docstring code completion.
- **SWE-bench**: Repository-level engineering (multi-file AST parsing, git diff patches, unit test suites).
- **LLM-as-Judge Bias Mitigation**: Swap model families (e.g. Claude judge for GPT-4 outputs), randomize position order, use multi-judge consensus.

---

## 🚀 Quick Command Reference

```bash
# Clone & install
git clone https://github.com/umang-algo/agentic-ai-handbook.git
cd agentic-ai-handbook/coding-handbook

# Run master CLI
python main.py list             # List all 21 chapters
python main.py run ch01         # Run interactive chapter lab
python main.py bench ch06       # Run empirical benchmark
python main.py test             # Verify all 59 modules
```
