# Chapter 18: End-to-End GitHub Code Review Agent — Code Lab

> 📖 **Book Chapter**: [Chapter 18 — GitHub Code Review Agent](../../book/chapter_18_github_agent.md)

## Files
| File | Description |
|------|-------------|
| `webhook_server.py` | FastAPI webhook handler with HMAC signature verification |
| `ast_chunker.py` | AST-aware diff chunker for PR review |
| `bug_retriever.py` | ChromaDB-backed similar bug history retriever |
| `reviewer_llm.py` | Structured LLM reviewer with cost cap |
| `github_poster.py` | GitHub API review comment poster |
