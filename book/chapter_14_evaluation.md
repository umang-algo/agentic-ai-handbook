# Chapter 14: Agent Evaluation & Red-Teaming

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch14_evaluation](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch14_evaluation)

> "You cannot improve what you cannot measure. In 2024, a team at a major enterprise deployed an AI procurement agent. In demos, it worked flawlessly. In production, it had a silent failure rate of 34%: one in three purchase orders either targeted the wrong vendor, specified the wrong quantity, or failed to apply contractual discounts. The team had been measuring the wrong thing — they measured 'did the agent respond?' not 'was the response correct?' They had a success metric, not an accuracy metric."


Evaluation is the discipline that separates amateur agentic systems from production-grade ones. This chapter gives you the complete framework: how to define what "correct" means for an agent, how to measure it systematically, and how to break your own agent before adversaries do.

## The Measurement Problem: Why Standard Metrics Fail

Traditional ML evaluation uses classification accuracy or BLEU scores — single-value metrics for single-step outputs. Agents are different: they produce a *trajectory* (a sequence of decisions) that is only partially observable, and the correctness of any individual step depends on the full context.

Consider an agent asked to "book a flight from NYC to SF on Friday under \$400." The agent might:

    - Search flights — (*correct tool, correct parameters*) 
    - Find a \$380 option on Spirit and a \$395 option on United, then book Spirit — (*is this correct? User didn't specify airline preference*)
    - Receive a confirmation — (*tool call succeeded, but did the agent meet the user's true intent?*)


Final output evaluation — "did the booking succeed?" — misses whether the agent made a good *decision* in step 2. Trajectory evaluation requires examining every step.

## The Four Evaluation Dimensions

### 1. Trajectory Correctness
Given a reference optimal trajectory $\tau^* = (a_1^*, a_2^*, \dots, a_n^*)$ and the agent's actual trajectory $\hat{\tau} = (\hat{a}_1, \hat{a}_2, \dots, \hat{a}_m)$, the trajectory score is:
\begin{equation}
\text{TrajectoryScore}(\hat{\tau}, \tau^*) = \frac{1}{n} \sum_{i=1}^n \mathbb{1}\!\left[\exists\, j: \hat{a}_j = a_i^* \wedge \text{order}(\hat{a}_j) \approx \text{order}(a_i^*)\right]
\end{equation}

This measures what fraction of the required steps were taken in approximately the right order.

### 2. Tool Precision and Recall
\begin{align}
\text{Tool Precision} &= \frac{|\text{Correct tool calls}|}{|\text{Total tool calls made}|} \\[4pt]
\text{Tool Recall} &= \frac{|\text{Correct tool calls}|}{|\text{Total required tool calls}|}
\end{align}

A high-precision agent rarely calls tools incorrectly. A high-recall agent rarely misses a required tool call. Production agents should target $P > 0.92$ and $R > 0.95$ for business-critical workflows.

### 3. Completion Rate
The fraction of benchmark tasks the agent completes without human intervention or error termination. A completion rate below 85% typically makes an agent unsuitable for unsupervised deployment.

### 4. Calibrated Cost per Task
\begin{equation}
\text{Cost}_{\text{task}} = \sum_{k=1}^{K} \frac{T_k^{\text{in}} \cdot P^{\text{in}} + T_k^{\text{out}} \cdot P^{\text{out}}}{10^6}
\end{equation}
where $K$ is the number of LLM calls, $T^{\text{in}}$ is input token count, $T^{\text{out}}$ is output token count, and $P^{\text{in}}, P^{\text{out}}$ are the per-million token prices.

## LLM-as-Judge: Automated Evaluation at Scale

Manual evaluation of agent trajectories is prohibitively expensive. The state-of-the-art alternative is using a second LLM as an automated evaluator — the "LLM-as-Judge" pattern.


*Architecture diagram visualizable in the companion handbook implementation.*






## Red-Teaming Playbook: Breaking Your Own Agent

Red-teaming is the discipline of attacking your own system before adversaries do. For agents, the attack surface is much larger than traditional software because the attack vector is *natural language* — infinitely flexible and poorly formalizable.

### Attack 1: Goal Hijacking via Specification Ambiguity

Many agent failures occur not through malicious injection but through *underspecification*. An attacker finds an ambiguous case in the task definition and exploits it.

**Example:** An agent is instructed to "delete all files older than 30 days that are no longer referenced by any project." An attacker creates a file named "`.30_days_ago_marker`" that causes the date parsing to return epoch time, making all files appear 30+ days old.

**Test:** Run your agent against edge cases in every parameter:

    - Dates: "yesterday," "last fiscal year," timezone ambiguities
    - Quantities: zero, negative numbers, extremely large values
    - Names: SQL injection strings, path traversal (`../../`), unicode homoglyphs


### Attack 2: Infinite Loop Induction

Craft a task that triggers the agent's error-handling loop repeatedly:





**Expected behavior:** The agent should detect the impossibility and terminate gracefully with a clear explanation — not burn tokens until hitting the max iteration limit.

### Attack 3: Multi-Turn Manipulation

The agent's system prompt defenses are evaluated on Turn 1. By Turn 5, the conversation history may have eroded them:





### Attack 4: Denial of Wallet

Craft requests that maximize token consumption per unit of legitimate value:
