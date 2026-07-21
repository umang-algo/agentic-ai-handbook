# Chapter 17: Fine-Tuning Agents for Domain Behaviour

> 📝 **Coding Handbook**: Practice the code from this chapter → [`coding-handbook/ch17_fine_tuning`](../coding-handbook/ch17_fine_tuning/)

> "A legal tech company deployed GPT-4o to extract structured data from contracts. The model was excellent at understanding English, but consistently misread their internal contract taxonomy — confusing 'Effective Date' with 'Execution Date,' and 'Counterparty' with 'Licensor.' After three months of prompt engineering with minimal improvement, they switched strategy: they collected 800 correct extraction examples from their own paralegals, trained a fine-tuned version of Llama-3-8B using DPO, and deployed it. The fine-tuned 8B model outperformed GPT-4o on their internal taxonomy by 23 percentage points, and cost 96% less per inference."


Fine-tuning is not about making a model "smarter" in general. It is about encoding domain-specific knowledge and behavioral preferences that cannot be expressed efficiently in a prompt. This chapter covers the three techniques that matter in production: DPO for behavioral alignment, LoRA for efficient training, and synthetic data generation for building training sets.

## When to Fine-Tune vs. Prompt Engineer

This is the most important decision in this chapter. Fine-tuning has a significant upfront cost (data collection, training, infrastructure). Prompt engineering has near-zero cost but limited ceiling.



**Rule of thumb:** If you have $>$500 examples of preferred behavior and the behavior is stable, fine-tuning will outperform any prompt.

## Direct Preference Optimization (DPO)

Standard supervised fine-tuning (SFT) trains the model to replicate correct outputs. DPO is different: it trains the model using *preference pairs* — examples of correct and incorrect behavior — and directly optimizes the model to *prefer* the correct behavior.

### The DPO Loss Function
Given a prompt $x$, a preferred response $y_w$ ("winner"), and a rejected response $y_l$ ("loser"):
\begin{equation}
\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \!\left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right) \right]
\end{equation}

where:

    - $\pi_\theta$ is the policy (model being trained)
    - $\pi_{\text{ref}}$ is the frozen reference model (the pre-trained base)
    - $\beta$ is the temperature parameter controlling how strongly to diverge from the reference (typically 0.1 -- 0.5)
    - $\sigma$ is the sigmoid function


**Intuition:** The loss increases the log-probability of $y_w$ relative to how the reference model rated it, while simultaneously decreasing the log-probability of $y_l$ — all while a KL penalty (implicit in the ratio terms) prevents the model from diverging catastrophically from the base.

### Building a Tool-Call DPO Dataset
For agent fine-tuning, preference pairs are tool-call trajectories:





## LoRA: Training Only What Matters

A 70B parameter model cannot be fine-tuned on a single GPU — the weights alone require 140GB of VRAM in FP16. LoRA (Low-Rank Adaptation) sidesteps this by *freezing* all original weights and training only small low-rank adapter matrices that are added to specific layers.

### LoRA Mathematics
For a pre-trained weight matrix $W_0 \in \mathbb{R}^{d \times k}$, LoRA adds a low-rank perturbation:
\begin{equation}
W = W_0 + \Delta W = W_0 + BA
\end{equation}
where $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$, and rank $r \ll \min(d, k)$.

**Parameter count comparison** for a single attention layer of Llama-3-8B ($d=4096$, $k=4096$):
\begin{align}
\text{Full fine-tune:} &\quad 4096 \times 4096 = 16{,}777{,}216 \text{ parameters} \\
\text{LoRA (r=16):} &\quad 4096 \times 16 + 16 \times 4096 = 131{,}072 \text{ parameters}
\end{align}

LoRA trains **128$\times$ fewer parameters** while achieving comparable performance for domain adaptation tasks.





## Synthetic Data Generation with a Teacher Model

Collecting 500+ high-quality preference pairs from human experts is expensive. A faster alternative is using a strong "teacher" model (GPT-4o) to generate training data for a weaker "student" model (Llama-3-8B).
