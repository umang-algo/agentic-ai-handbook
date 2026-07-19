# Chapter 21: How to Evaluate AI — Benchmarks, Metrics, and Human Judgment

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch21_evaluating_ai](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch21_evaluating_ai)

## Overview

The complete framework for evaluating AI systems: major benchmarks and what they actually measure, building custom evaluation suites, LLM-as-Judge at scale, when human evaluation is irreplaceable, and continuous evaluation in production.

## Benchmark Landscape

### Code Generation
| Benchmark | Tasks | What It Measures |
|-----------|-------|-----------------|
| HumanEval | 164 | Function-level Python completion |
| MBPP | 974 | Simple Python programming |
| SWE-bench | 2,294 | Real GitHub issue resolution |
| SWE-bench Verified | 500 | Human-verified subset |
| LiveCodeBench | Rolling | Post-training competitive programming |

### Reasoning
| Benchmark | Tasks | Domain |
|-----------|-------|--------|
| MMLU | 15,908 | 57 academic subjects |
| GPQA | 448 | PhD-level science |
| MATH | 12,500 | Competition mathematics |

### Agent Benchmarks
| Benchmark | What It Measures |
|-----------|-----------------|
| WebArena | Web browsing tasks |
| OSWorld | Desktop OS tasks |
| GAIA | General AI assistant |

## Key Concepts

### LLM-as-Judge
- Known biases: position bias, verbosity bias, self-enhancement bias
- Mitigation: different model family as judge, randomize position, structured rubrics
- Multi-judge consensus with Cohen's Kappa

### Human Evaluation
- When LLM-as-Judge fails: novel domains, subjective quality, safety-critical
- Blind evaluation UI to eliminate bias
- Inter-annotator agreement measurement

### Continuous Evaluation in Production
- Online A/B testing for agents
- Regression detection pipelines
- Drift monitoring

## Key Takeaway

> A model scoring 92% on HumanEval does NOT mean it can write production code. The gap between benchmark performance and real-world utility is the most misunderstood concept in AI evaluation.
