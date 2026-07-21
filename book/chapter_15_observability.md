# Chapter 15: Observability, Tracing, and the Agent Debugger

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch15_observability](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch15_observability)

> "A research team at a fintech company deployed a multi-agent system for automated compliance checks. After two weeks in production, they noticed that 12% of reports were being filed with incorrect risk scores. Debugging was a nightmare: each compliance check involved 6 agents, 40+ LLM calls, and hundreds of tool executions. The logs showed only final outputs — no intermediate states, no timing information, no record of which agent made which decision. The team could not identify the faulty agent without replaying the entire workflow, which was non-deterministic. They were blind. The system had no observability."


Observability is not debugging. Debugging is what you do when something has already gone wrong. Observability is the engineering infrastructure that lets you understand *why* something went wrong, without having to reproduce the failure. For agentic systems, this requires traces, metrics, and logs — structured, correlated, and agent-aware.

## The Three Pillars of Agentic Observability



## OpenTelemetry for Agents: Distributed Tracing

OpenTelemetry (OTel) is the CNCF standard for distributed tracing. A *trace* represents the complete journey of one user request through your system. A *span* represents a single unit of work within that trace.

For an agentic system, the trace spans an entire agent run, with child spans for each LLM call, tool execution, and memory retrieval.


*Architecture diagram visualizable in the companion handbook implementation.*






## The "Lost in the Middle" Failure Pattern

Research by Liu et al. (2023) demonstrated that LLMs show a U-shaped performance curve over long contexts: they attend well to information at the beginning and end of a prompt, but systematically ignore information in the middle. This is one of the most dangerous silent failures in production RAG-based agents.

### Detecting It: Attention Weight Analysis
When debugging an agent that fails to use context that you *know* is in the prompt, you can extract attention weights from an open-source model (Llama-3) to visualize where the model's attention is focused.





**The mitigation** is active context ordering: place the most critical context (the exact fact the agent needs to answer correctly) either at the very beginning or very end of the prompt — never bury it in the middle. This structural rule is more reliable than any prompt engineering trick.

## Metrics That Actually Matter in Production





**Alert rules to configure:** 

    - `agent_task\{outcome="failure"\` / agent_task_total > 0.15} — 15% failure rate is a P1 incident
    - P95 of `agent_llm_latency_seconds > 10` — degraded inference service
    - P95 of `agent_cost_usd > 1.0` — cost per task has blown out
