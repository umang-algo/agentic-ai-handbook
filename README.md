# The Practitioner's Guide to Agentic AI: From First Principles to Production Systems

<p align="center">
  <img src="cover.png" width="450" alt="The Practitioner's Guide to Agentic AI Book Cover">
</p>

<p align="center">
  <a href="https://github.com/umang-algo/agentic-ai-handbook/stargazers"><img src="https://img.shields.io/github/stars/umang-algo/agentic-ai-handbook?style=for-the-badge&color=8A2BE2" alt="GitHub Stars"></a>
  <a href="https://github.com/umang-algo/agentic-ai-handbook/blob/main/LICENSE"><img src="https://img.shields.io/github/license/umang-algo/agentic-ai-handbook?style=for-the-badge&color=blue" alt="License"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.11+-green.svg?style=for-the-badge&logo=python" alt="Python 3.11+"></a>
  <a href="https://github.com/umang-algo/agentic-ai-handbook"><img src="https://img.shields.io/badge/Chapters-21%20Markdown-orange?style=for-the-badge" alt="21 Chapters"></a>
  <a href="https://github.com/umang-algo/agentic-ai-handbook/tree/main/coding-handbook"><img src="https://img.shields.io/badge/Code%20Labs-59%20Python%20Modules-brightgreen?style=for-the-badge" alt="59 Labs"></a>
</p>

---

## ⚡ Quick Resources & Cheat Cards

- ⚡ **[CHEATSHEET.md](./CHEATSHEET.md)**: 1-Page Agentic AI Visual Quick-Reference Card (KV Cache math, ReAct loop traps, HNSW vs Flat, MCP lifecycles).
- 🧠 **[INTERVIEW_PREP.md](./INTERVIEW_PREP.md)**: 50 Top System Design & Architecture Questions for AI Engineers & LLM Researchers.
- 🚀 **[LAUNCH_KIT.md](./LAUNCH_KIT.md)**: Open-Source Promotion & Launch Copy for Hacker News, Reddit, Twitter/X, and LinkedIn.
- 📄 **[agentic_ai_book.pdf](./agentic_ai_book.pdf)**: Download the compiled 91-page conceptual handbook PDF.

---

## 🚀 Overview

Welcome to the definitive companion repository for **The Practitioner's Guide to Agentic AI** by **Umang Yadav & Antigravity**. 

This repository implements a **multi-track learning & engineering framework**:
1. **Conceptual & Architectural Track (`book/` & `agentic_ai_book.pdf`)**: All 21 chapters covering deep learning internals, cyclic execution models, sandboxed virtual environments, distributed tracing, economics, fine-tuning alignment, and interview prep.
2. **Hands-on Lab Track (`coding-handbook/`)**: 59 self-contained, runnable Python code files implementing the core algorithms discussed in the book.
3. **Multi-Persona Engineering Tracks**:
   - 🎓 **Students**: Zero-config offline execution via built-in `MockLLMProvider`, clear mental models, and step-by-step walkthroughs.
   - 🔬 **Researchers**: Empirical benchmarks (VRAM math, attention entropy, HNSW search complexity $O(\log N)$ vs $O(N)$, LoRA rank trade-offs), equations, and experiment harnesses.
   - 🚀 **AI Engineers**: Async design patterns, fault-tolerant retries, model cost/latency routers, streaming JSON parsers, and enterprise safety guardrails.

---

## 💻 Master Interactive CLI Launcher

Run any chapter lab, launch empirical benchmarks, or execute the full 59-module test suite from a single terminal launcher:

```bash
cd coding-handbook

# List all 21 chapters & 59 code modules
python main.py list

# Run interactive lab for a chapter (e.g. ch01, ch03, ch19)
python main.py run ch01

# Run empirical benchmark experiments
python main.py bench ch06

# Run automated verification across all 59 code modules
python main.py test
```

---

## 📁 Repository Structure

```bash
├── book/                # Complete 21-chapter book in Markdown (.md)
├── agentic_ai_book.pdf  # Compiled 91-page book (PDF)
├── CHEATSHEET.md        # 1-page visual quick-reference card
├── INTERVIEW_PREP.md    # 50 System Design Interview Questions
├── LAUNCH_KIT.md        # Promotion & launch templates (HN, Reddit, X)
├── cover.png            # Front cover art
└── coding-handbook/     # Companion Python implementations & labs
    ├── main.py          # Master interactive CLI & lab runner
    ├── README.md        # Lab index and quickstart guide
    ├── requirements.txt # Python dependencies
    ├── common/          # Shared utilities (logger, offline mock LLM, metrics)
    ├── ch01_llm_anatomy/
    ├── ch02_reasoning/
    ├── ch03_react/
    ├── ch04_tool_calling/
    ├── ch05_embeddings/
    ├── ch06_vector_db/
    ├── ch07_context_assembly/
    ├── ch08_code_interpreter/
    ├── ch09_mcp/
    ├── ch10_multi_agent/
    ├── ch11_ai_ides/
    ├── ch12_agentic_sdks/
    ├── ch13_enterprise_architectures/
    ├── ch14_evaluation/
    ├── ch15_observability/
    ├── ch16_economics/
    ├── ch17_fine_tuning/
    ├── ch18_github_agent/
    ├── ch19_production_industries/
    ├── ch20_ai_harness_tools/
    └── ch21_evaluating_ai/
```

---

## 📚 Book Chapter Index

| Chapter | Title | Markdown Chapter | Companion Code |
|---------|-------|------------------|----------------|
| **Ch 1** | The Anatomy of an LLM | [chapter_1_anatomy.md](./book/chapter_1_anatomy.md) | [`ch01_llm_anatomy/`](./coding-handbook/ch01_llm_anatomy/) |
| **Ch 2** | From Completion to Reasoning | [chapter_2_reasoning.md](./book/chapter_2_reasoning.md) | [`ch02_reasoning/`](./coding-handbook/ch02_reasoning/) |
| **Ch 3** | The ReAct Paradigm | [chapter_3_react.md](./book/chapter_3_react.md) | [`ch03_react/`](./coding-handbook/ch03_react/) |
| **Ch 4** | Tool Calling, Security & AsyncIO | [chapter_4_tool_calling.md](./book/chapter_4_tool_calling.md) | [`ch04_tool_calling/`](./coding-handbook/ch04_tool_calling/) |
| **Ch 5** | Embeddings & Asymmetric Search | [chapter_5_embeddings.md](./book/chapter_5_embeddings.md) | [`ch05_embeddings/`](./coding-handbook/ch05_embeddings/) |
| **Ch 6** | Building a Vector Database | [chapter_6_vector_db.md](./book/chapter_6_vector_db.md) | [`ch06_vector_db/`](./coding-handbook/ch06_vector_db/) |
| **Ch 7** | Context Assembly | [chapter_7_context_assembly.md](./book/chapter_7_context_assembly.md) | [`ch07_context_assembly/`](./coding-handbook/ch07_context_assembly/) |
| **Ch 8** | The Code Interpreter | [chapter_8_code_interpreter.md](./book/chapter_8_code_interpreter.md) | [`ch08_code_interpreter/`](./coding-handbook/ch08_code_interpreter/) |
| **Ch 9** | Model Context Protocol | [chapter_9_mcp.md](./book/chapter_9_mcp.md) | [`ch09_mcp/`](./coding-handbook/ch09_mcp/) |
| **Ch 10** | Multi-Agent State Machines | [chapter_10_multi_agent.md](./book/chapter_10_multi_agent.md) | [`ch10_multi_agent/`](./coding-handbook/ch10_multi_agent/) |
| **Ch 11** | Modern AI IDE Architectures | [chapter_11_ai_ides.md](./book/chapter_11_ai_ides.md) | [`ch11_ai_ides/`](./coding-handbook/ch11_ai_ides/) |
| **Ch 12** | Agentic SDK Landscape | [chapter_12_agentic_sdks.md](./book/chapter_12_agentic_sdks.md) | [`ch12_agentic_sdks/`](./coding-handbook/ch12_agentic_sdks/) |
| **Ch 13** | Enterprise Architectures | [chapter_13_enterprise_architectures.md](./book/chapter_13_enterprise_architectures.md) | [`ch13_enterprise_architectures/`](./coding-handbook/ch13_enterprise_architectures/) |
| **Ch 14** | Agent Evaluation & Red-Teaming | [chapter_14_evaluation.md](./book/chapter_14_evaluation.md) | [`ch14_evaluation/`](./coding-handbook/ch14_evaluation/) |
| **Ch 15** | Observability, Tracing & Debugging | [chapter_15_observability.md](./book/chapter_15_observability.md) | [`ch15_observability/`](./coding-handbook/ch15_observability/) |
| **Ch 16** | Production Economics & Latency | [chapter_16_economics.md](./book/chapter_16_economics.md) | [`ch16_economics/`](./coding-handbook/ch16_economics/) |
| **Ch 17** | Fine-Tuning Agents | [chapter_17_fine_tuning.md](./book/chapter_17_fine_tuning.md) | [`ch17_fine_tuning/`](./coding-handbook/ch17_fine_tuning/) |
| **Ch 18** | End-to-End: GitHub Code Review Agent | [chapter_18_github_agent.md](./book/chapter_18_github_agent.md) | [`ch18_github_agent/`](./coding-handbook/ch18_github_agent/) |
| **Ch 19** | Production AI for 5 Industries | [chapter_19_production_industries.md](./book/chapter_19_production_industries.md) | [`ch19_production_industries/`](./coding-handbook/ch19_production_industries/) |
| **Ch 20** | AI Harness Tools | [chapter_20_ai_harness_tools.md](./book/chapter_20_ai_harness_tools.md) | [`ch20_ai_harness_tools/`](./coding-handbook/ch20_ai_harness_tools/) |
| **Ch 21** | How to Evaluate AI | [chapter_21_evaluating_ai.md](./book/chapter_21_evaluating_ai.md) | [`ch21_evaluating_ai/`](./coding-handbook/ch21_evaluating_ai/) |

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=umang-algo/agentic-ai-handbook&type=Date)](https://star-history.com/#umang-algo/agentic-ai-handbook&Date)

---

## 🎓 Mapped Course
This handbook is directly aligned with the **AI Agent Masterclass** repository:  
🔗 **[umang-algo/AI-Agent-Masterclass](https://github.com/umang-algo/AI-Agent-Masterclass)**

---

## ✍️ Authorship & Collaboration
- **Umang Yadav**: Creator & AI Architect
- **Antigravity**: Pair Programmer (Autonomous Agentic Coding Agent created by the Google DeepMind team)

Released under the **MIT License**.
