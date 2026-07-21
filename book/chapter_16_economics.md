# Chapter 16: Production Economics & Latency Engineering

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch16_economics](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch16_economics)

> "A startup built a beautiful multi-agent customer support system. It could handle complex queries, retrieve relevant policies, escalate to specialists, and draft professional responses. In the beta, users loved it. Then they ran the numbers. Each query cost \$0.47 on average — across 800 support tickets a day, that was \$11,000 per month in API costs, compared to \$3,200 per month for the human agents they were replacing. The agent was technically superior and economically unviable. They had solved the AI problem and failed the business problem."


No matter how brilliant your agent's architecture, it will be shut down if it costs too much or responds too slowly. This chapter provides the quantitative framework for designing agents that fit within real business constraints.

## The Economics of LLM Token Costs

### Pricing Landscape (Mid-2025)


### Task Cost Formula
For a ReAct agent that makes $K$ LLM calls, with iteration $k$ having input token count $T_k^{\text{in}}$ and output $T_k^{\text{out}}$:
\begin{equation}
C_{\text{task}} = \sum_{k=1}^{K} \left( \frac{T_k^{\text{in}} \cdot P^{\text{in}} + T_k^{\text{out}} \cdot P^{\text{out}}}{10^6} \right)
\end{equation}

Note that in a ReAct loop, the system prompt is repeated on every call. For a 5,000-token system prompt with $K=6$ iterations:
\begin{equation}
C_{\text{system}} = K \cdot 5000 \cdot \frac{P^{\text{in}}}{10^6} = 6 \times 5000 \times \frac{2.50}{10^6} = \$0.075 \text{ per task (GPT-4o)}
\end{equation}

With prompt caching (90% hit rate), this drops to $\$0.0075$ — a 10$\times$ cost reduction from a single infrastructure change.

## The Latency Budget: Where Time Is Spent

Every user-facing agent has an end-to-end latency that must fit within a Service Level Objective (SLO). A typical SLO for a responsive assistant is P95 $< 8$ seconds. Let us decompose where that time goes:

\begin{equation}
T_{\text{total}} = T_{\text{orchestration}} + \sum_{k=1}^{K} (T_{\text{prefill},k} + T_{\text{decode},k}) + \sum_{j=1}^{J} T_{\text{tool},j}
\end{equation}



## The Short-Circuit Pattern: Hierarchical Model Routing

The most impactful architectural optimization in production agentic systems is *hierarchical model routing*: use a cheap, fast model to classify and route requests, and only escalate to an expensive model when necessary.


*Architecture diagram visualizable in the companion handbook implementation.*






## Streaming Architecture for Perceived Latency

Even if your agent takes 6 seconds to produce a complete response, users perceive it as fast if the first token arrives quickly. Streaming is the most impactful UX optimization for conversational agents.





## The ROI Framework: Building the Business Case

Before deploying any agent, compute its break-even point:

\begin{equation}
\text{Break-even Queries/Month} = \frac{C_{\text{infra}} + C_{\text{engineering}}}{C_{\text{human}} - C_{\text{agent per query}}}
\end{equation}

**Example calculation** for a customer support agent:

    - Human agent cost: \$0.85 per query (hourly rate / queries per hour)
    - AI agent cost: \$0.047 per query (with short-circuit routing + caching)
    - Monthly infra + engineering overhead: \$4,000
    - **Break-even**: $4000 / (0.85 - 0.047) \approx 4,980$ queries/month
    - At 800 queries/day (24,000/month): Net savings = $24000 \times (0.85 - 0.047) - 4000 = \mathbf{\$15,272}$/month
