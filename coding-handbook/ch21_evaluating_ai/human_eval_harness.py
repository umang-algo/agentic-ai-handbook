"""
Chapter 21: HumanEval pass@k Evaluation Harness
================================================
Unbiased statistical estimation of pass@k metrics (k=1, 5, 10) for LLM code generation benchmarks.

From: The Practitioner's Handbook of Agentic AI, Chapter 21.2
"""

import json
import math
from typing import List, Dict, Any


def estimate_pass_at_k(num_samples: int, num_correct: int, k: int) -> float:
    """
    Unbiased estimator for pass@k based on the HumanEval paper formula:
    pass@k = 1 - C(n - c, k) / C(n, k)
    
    where n = num_samples, c = num_correct, k = k_threshold
    """
    if num_samples - num_correct < k:
        return 1.0

    return 1.0 - (math.comb(num_samples - num_correct, k) / math.comb(num_samples, k))


class HumanEvalHarness:
    """Evaluation harness calculating pass@k statistics over Python function samples."""
    def __init__(self, k_list: List[int] = None):
        self.k_list = k_list or [1, 5, 10]

    def evaluate_task_samples(self, task_id: str, sample_results: List[bool]) -> Dict[str, float]:
        """Calculates pass@k metrics for a single HumanEval task given sample pass/fail booleans."""
        n = len(sample_results)
        c = sum(1 for passed in sample_results if passed)
        
        metrics = {}
        for k in self.k_list:
            if n >= k:
                metrics[f"pass@{k}"] = round(estimate_pass_at_k(n, c, k), 4)
            else:
                metrics[f"pass@{k}"] = None
        return metrics

    def compute_suite_metrics(self, benchmark_results: Dict[str, List[bool]]) -> Dict[str, Any]:
        """Computes aggregate mean pass@k across all benchmark tasks."""
        task_metrics = []
        aggregates = {f"pass@{k}": [] for k in self.k_list}

        for task_id, samples in benchmark_results.items():
            metrics = self.evaluate_task_samples(task_id, samples)
            task_metrics.append({"task_id": task_id, **metrics})
            for k in self.k_list:
                val = metrics.get(f"pass@{k}")
                if val is not None:
                    aggregates[f"pass@{k}"].append(val)

        mean_scores = {}
        for k in self.k_list:
            vals = aggregates[f"pass@{k}"]
            mean_scores[f"mean_pass@{k}"] = round(sum(vals) / len(vals), 4) if vals else 0.0

        return {
            "total_tasks": len(benchmark_results),
            "aggregate_metrics": mean_scores,
            "task_breakdown": task_metrics
        }


if __name__ == "__main__":
    harness = HumanEvalHarness(k_list=[1, 5, 10])

    # Simulated model output samples (10 generations per task)
    sample_dataset = {
        "HumanEval/0": [True, True, True, False, True, True, False, True, True, True],   # 8/10 correct
        "HumanEval/1": [True, False, False, False, False, False, False, False, False, False], # 1/10 correct
        "HumanEval/2": [False, False, False, False, False, False, False, False, False, False] # 0/10 correct
    }

    results = harness.compute_suite_metrics(sample_dataset)
    print("HumanEval Pass@k Benchmark Results:")
    print(json.dumps(results, indent=2))
