# 💻 The Practitioner's Coding Handbook of Agentic AI

> **The companion code repository for *The Practitioner's Handbook of Agentic AI: From First Principles to Production Systems*.**

Every chapter of the book has a corresponding code directory here with **runnable, production-style Python implementations**. No pseudocode, no stubs — real code you can execute, modify, and deploy.

---

## 🌟 Interactive Master CLI Launcher

Launch any lab, run empirical benchmark experiments, or execute the full test suite with the master CLI tool:

```bash
# Navigate to coding-handbook
cd agentic-ai-handbook/coding-handbook

# List all 21 chapters & code modules
python main.py list

# Run interactive lab for a chapter (e.g. ch01, ch03, ch19)
python main.py run ch01

# Run empirical benchmark experiments (e.g. HNSW scaling, VRAM math)
python main.py bench ch06

# Run automated verification across all 59 code modules
python main.py test
```

---

## 🎯 3-Tier Learning Framework

This handbook is designed for three distinct personas:

- 🎓 **Students**: Core mental models, step-by-step code walkthroughs, and zero-config offline execution via our built-in `MockLLMProvider`.
- 🔬 **Researchers**: Mathematical formulations, empirical benchmarking (VRAM math, attention entropy, HNSW search complexity $O(\log N)$ vs $O(N)$, LoRA rank trade-offs), and experiment harnesses.
- 🚀 **AI Engineers**: Production async design patterns, fault-tolerant retry loops, model cost/latency routers, streaming JSON parsers, and enterprise safety guardrails.

---

## 🛠️ Shared Core Utilities (`coding-handbook/common/`)

- [`common/logger.py`](./common/logger.py): Rich terminal formatting with ANSI colors, execution timers, and formatted trajectory boxes.
- [`common/mock_llm.py`](./common/mock_llm.py): Deterministic, 100% offline Mock LLM provider supporting tool calling, reasoning tokens (`<thought>`), streaming, and simulated latency.
- [`common/metrics.py`](./common/metrics.py): VRAM memory calculator (Weights + KV Cache), TTFT/TPS latency measures, and token cost accounting.

---

## 📚 Chapter Index

### Part I: First Principles (The Engine)

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 1** | [The Anatomy of an LLM](../book/chapter_1_anatomy.md) | [`ch01_llm_anatomy/`](./ch01_llm_anatomy/) | `scaled_dot_product_attention.py`, `kv_cache_calculator.py`, `bpe_tokenizer_demo.py` |
| **Ch 2** | [From Completion to Reasoning](../book/chapter_2_reasoning.md) | [`ch02_reasoning/`](./ch02_reasoning/) | `temperature_sampling.py`, `logit_bias_forcing.py`, `local_grammar_enforcement.py` |

### Part II: The Agentic Loop

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 3** | [The ReAct Paradigm](../book/chapter_3_react.md) | [`ch03_react/`](./ch03_react/) | `react_orchestrator.py`, `retry_with_backoff.py`, `self_healing_executor.py`, `reasoning_model_integration.py` |
| **Ch 4** | [Tool Calling, Security & AsyncIO](../book/chapter_4_tool_calling.md) | [`ch04_tool_calling/`](./ch04_tool_calling/) | `async_tool_executor.py`, `security_input_sanitizer.py`, `permission_scoping.py`, `computer_use_agent.py` |

### Part III: Memory and Context (The RAG Pipeline)

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 5** | [Embeddings & Asymmetric Search](../book/chapter_5_embeddings.md) | [`ch05_embeddings/`](./ch05_embeddings/) | `vector_similarity_metrics.py`, `asymmetric_embedding_search.py` |
| **Ch 6** | [Building a Vector Database](../book/chapter_6_vector_db.md) | [`ch06_vector_db/`](./ch06_vector_db/) | `ast_code_chunker.py`, `graph_rag_memory.py`, `hnsw_from_scratch.py` |
| **Ch 7** | [Context Assembly](../book/chapter_7_context_assembly.md) | [`ch07_context_assembly/`](./ch07_context_assembly/) | `sliding_window_context.py`, `episodic_paged_memory.py` |

### Part IV: Sandboxing and Environments

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 8** | [The Code Interpreter](../book/chapter_8_code_interpreter.md) | [`ch08_code_interpreter/`](./ch08_code_interpreter/) | `microvm_executor.py` |

### Part V: Advanced Orchestration

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 9** | [Model Context Protocol](../book/chapter_9_mcp.md) | [`ch09_mcp/`](./ch09_mcp/) | `mcp_json_rpc_messages.py`, `mcp_json_rpc_server.py` |
| **Ch 10** | [Multi-Agent State Machines](../book/chapter_10_multi_agent.md) | [`ch10_multi_agent/`](./ch10_multi_agent/) | `dag_topological_sort.py`, `checkpoint_serializer.py`, `dag_state_machine.py` |

### Part VI: Modern Agentic SDKs & AI IDEs

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 11** | [Architecture of AI IDEs](../book/chapter_11_ai_ides.md) | [`ch11_ai_ides/`](./ch11_ai_ides/) | `myers_diff_algorithm.py`, `ast_diff_verifier.py` |
| **Ch 12** | [The Agentic SDK Landscape](../book/chapter_12_agentic_sdks.md) | [`ch12_agentic_sdks/`](./ch12_agentic_sdks/) | `graph_state_serializer.py` |

### Part VII: Production AI for Industry

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 13** | [Enterprise Architectures](../book/chapter_13_enterprise_architectures.md) | [`ch13_enterprise_architectures/`](./ch13_enterprise_architectures/) | `customer_support_router.py`, `devsecops_patcher.py`, `financial_market_aggregator.py` |
| **Ch 19** | [Production AI for 5 Industries](../book/chapter_19_production_industries.md) | [`ch19_production_industries/`](./ch19_production_industries/) | `healthcare_agent.py`, `finance_agent.py`, `legal_agent.py`, `ecommerce_agent.py`, `devops_sre_agent.py` |

### Part VIII: The AI Developer's Toolkit

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 20** | [AI Harness Tools](../book/chapter_20_ai_harness_tools.md) | [`ch20_ai_harness_tools/`](./ch20_ai_harness_tools/) | `tool_comparison_matrix.py` |

### Part IX: The Mastery Tier

| Chapter | Book Topic | Code Directory | Key Files |
|---------|-----------|---------------|-----------|
| **Ch 14** | [Agent Evaluation & Red-Teaming](../book/chapter_14_evaluation.md) | [`ch14_evaluation/`](./ch14_evaluation/) | `llm_as_judge.py`, `benchmark_runner.py`, `red_team_tests.py` |
| **Ch 21** | [How to Evaluate AI](../book/chapter_21_evaluating_ai.md) | [`ch21_evaluating_ai/`](./ch21_evaluating_ai/) | `swe_bench_runner.py`, `human_eval_harness.py`, `safety_benchmark.py` |
| **Ch 15** | [Observability & Tracing](../book/chapter_15_observability.md) | [`ch15_observability/`](./ch15_observability/) | `otel_react_orchestrator.py`, `prometheus_metrics.py`, `attention_analysis.py` |
| **Ch 16** | [Production Economics](../book/chapter_16_economics.md) | [`ch16_economics/`](./ch16_economics/) | `model_router.py`, `streaming_orchestrator.py`, `roi_calculator.py` |
| **Ch 17** | [Fine-Tuning Agents](../book/chapter_17_fine_tuning.md) | [`ch17_fine_tuning/`](./ch17_fine_tuning/) | `dpo_dataset_builder.py`, `lora_fine_tune.py`, `synthetic_data_generator.py` |
| **Ch 18** | [End-to-End: GitHub Code Review Agent](../book/chapter_18_github_agent.md) | [`ch18_github_agent/`](./ch18_github_agent/) | `webhook_server.py`, `ast_chunker.py`, `bug_retriever.py`, `reviewer_llm.py`, `github_poster.py` |

---
