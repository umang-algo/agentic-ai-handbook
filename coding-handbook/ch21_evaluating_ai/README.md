# Chapter 21: How to Evaluate AI — Code Lab

> 📖 **Book Chapter**: [Chapter 21 — How to Evaluate AI](../../book/chapter_21_evaluating_ai.md)

Benchmark suites and evaluation harnesses for measuring repository-level issue resolution, unbiased pass@k code completion metrics, and AI safety red-teaming.

---

## 🛠️ Included Code Modules

| Module | Benchmark Suite | Primary Metric |
|--------|-----------------|----------------|
| [`swe_bench_runner.py`](./swe_bench_runner.py) | SWE-bench Evaluation Harness | Resolution Pass Rate (%) |
| [`human_eval_harness.py`](./human_eval_harness.py) | HumanEval Pass@k Estimator | Unbiased pass@k ($k=1, 5, 10$) |
| [`safety_benchmark.py`](./safety_benchmark.py) | Red-Teaming & Safety Benchmark | Safety Score (%) & Vulnerability Rate |

---

## 🚀 Running the Examples

```bash
python3 swe_bench_runner.py
python3 human_eval_harness.py
python3 safety_benchmark.py
```
