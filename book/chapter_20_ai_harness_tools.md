# Chapter 20: AI Harness Tools — Mastering the Agentic Developer Toolkit

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch20_ai_harness_tools](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch20_ai_harness_tools)

## Overview

A practitioner's field guide to every major AI coding tool in the agentic ecosystem. For each tool: what it does, how it works under the hood, strengths, weaknesses, and when to use it.

## Tools Covered

| Tool | Type | Developer | Open Source |
|------|------|-----------|-------------|
| **Cursor** | IDE (VS Code fork) | Anysphere | No |
| **Claude Code** | CLI terminal agent | Anthropic | No |
| **GitHub Copilot** | IDE extension + cloud | GitHub/Microsoft | No |
| **Windsurf** | IDE (VS Code fork) | Codeium | No |
| **Aider** | CLI pair programmer | Paul Gauthier | Yes |
| **Roo Code** | VS Code extension | Community | Yes |
| **Cline** | VS Code extension | Community | Yes |
| **Continue** | VS Code/JetBrains ext | Continue.dev | Yes |
| **OpenHands** | Autonomous SWE agent | All Hands AI | Yes |
| **Devin** | Cloud autonomous agent | Cognition | No |
| **Amazon Q** | IDE extension + CLI | AWS | No |

## The Common Architecture Pattern

All agentic coding tools share a universal architecture:

1. **Context Engine** — Index + Retrieve relevant code
2. **LLM Reasoning** — ReAct loop for multi-step planning
3. **Diff Applicator** — Myers / Search-Replace for code edits
4. **Permission Gate** — User approval for actions
5. **Tool Executor** — Terminal, browser, filesystem access
6. **Observe + Loop** — Self-correction cycle

Understanding this shared architecture (covered in Chapters 3, 7, 8, 9, and 11) lets you evaluate any new tool that enters the market.

## Key Takeaway

> The tools differ in **implementation quality** of each component, **user experience** design, and **deployment model** (local vs. cloud) — not in fundamental architecture.
