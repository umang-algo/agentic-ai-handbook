# Chapter 18: End-to-End Project: The GitHub Code Review Agent

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch18_github_agent](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch18_github_agent)

> "The true test of a system is not whether it works in a demo — it is whether it holds together at 3 AM on a Friday when the oncall engineer is asleep, the CI pipeline has a flaky test, and four developers have pushed PRs simultaneously. Engineering is about systems that work when you are not watching."


This final chapter builds a complete, production-hardened agent from scratch. We will not shortcut anything. By the end, you will have a deployable GitHub Code Review Agent that:

    - Receives GitHub Pull Request webhooks via a FastAPI server
    - Parses changed files and uses an AST-aware chunker to identify semantically meaningful code units
    - Queries a vector database to find *similar past bugs* from the project's history
    - Runs a specialized reviewer LLM that produces structured review comments
    - Posts comments directly to the GitHub PR using the GitHub API
    - Enforces a cost cap of \$0.05 per review and a latency SLO of P95 $< 30$ seconds


## Architecture Overview


*Architecture diagram visualizable in the companion handbook implementation.*


## Step 1: The Webhook Server





## Step 2: AST-Aware Code Chunking

Naive line-based chunking splits functions in half. AST-aware chunking respects Python syntax boundaries, producing semantically meaningful review units.





## Step 3: Semantic Bug Retrieval from History





## Step 4: The Reviewer LLM with Structured Output





## Step 5: Posting to GitHub & Full Pipeline Assembly





## Production Hardening Checklist

Before deploying this agent to handle real production PRs, verify:



**The two unchecked items** — idempotency and observability — are your homework. The patterns for both are fully covered in Chapter 3 (SHA hashing of action signatures) and Chapter 15 (OpenTelemetry tracing). A production-grade agent is an integration of all of the preceding chapters.
