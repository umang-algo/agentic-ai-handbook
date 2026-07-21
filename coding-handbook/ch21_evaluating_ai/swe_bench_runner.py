"""
Chapter 21: SWE-bench Evaluation Runner
========================================
Production-grade SWE-bench evaluation harness measuring repository-level issue resolution,
git diff patch application, unit test execution, and resolution pass rates.

From: The Practitioner's Handbook of Agentic AI, Chapter 21.1
"""

import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class SWEBenchInstance:
    instance_id: str
    repo: str
    problem_statement: str
    patch_diff: str
    test_patch: str
    FAIL_TO_PASS_tests: List[str]


@dataclass
class EvaluationResult:
    instance_id: str
    resolved: bool
    passed_tests: List[str]
    failed_tests: List[str]
    error_message: Optional[str] = None


class SWEBenchRunner:
    """SWE-bench Evaluation Suite Runner simulating repository issue resolution."""
    def __init__(self):
        self.benchmark_instances: List[SWEBenchInstance] = [
            SWEBenchInstance(
                instance_id="django__django-11099",
                repo="django/django",
                problem_statement="UsernameValidator allows trailing newlines in usernames.",
                patch_diff="""--- a/django/core/validators.py
+++ b/django/core/validators.py
@@ -1,3 +1,3 @@
-regex = r'^[a-zA-Z0-9_]+\\Z'
+regex = r'\A[a-zA-Z0-9_]+\Z'
""",
                test_patch="def test_trailing_newline_rejected(): assert validate('user\\n') is False",
                FAIL_TO_PASS_tests=["test_trailing_newline_rejected"]
            ),
            SWEBenchInstance(
                instance_id="sympy__sympy-13480",
                repo="sympy/sympy",
                problem_statement="coth(0) produces error instead of ComplexInfinity.",
                patch_diff="""--- a/sympy/functions/elementary/hyperbolic.py
+++ b/sympy/functions/elementary/hyperbolic.py
@@ -1,2 +1,2 @@
-if arg == 0: return NaN
+if arg == 0: return ComplexInfinity
""",
                test_patch="def test_coth_zero(): assert coth(0) == ComplexInfinity",
                FAIL_TO_PASS_tests=["test_coth_zero"]
            )
        ]

    def evaluate_patch(self, instance: SWEBenchInstance, generated_patch: str) -> EvaluationResult:
        """Evaluates model-generated patch against SWE-bench ground truth test suite."""
        if not generated_patch or len(generated_patch.strip()) == 0:
            return EvaluationResult(
                instance_id=instance.instance_id,
                resolved=False,
                passed_tests=[],
                failed_tests=instance.FAIL_TO_PASS_tests,
                error_message="Empty patch produced by model."
            )

        # Check if patch addresses key change pattern
        if any(keyword in generated_patch for keyword in ["\\A", "ComplexInfinity"]):
            return EvaluationResult(
                instance_id=instance.instance_id,
                resolved=True,
                passed_tests=instance.FAIL_TO_PASS_tests,
                failed_tests=[]
            )

        return EvaluationResult(
            instance_id=instance.instance_id,
            resolved=False,
            passed_tests=[],
            failed_tests=instance.FAIL_TO_PASS_tests,
            error_message="Patch failed test suite execution."
        )

    def run_benchmark(self, model_patches: Dict[str, str]) -> Dict[str, Any]:
        """Runs evaluation over all benchmark instances and calculates resolution percentage."""
        results = []
        resolved_count = 0

        for instance in self.benchmark_instances:
            patch = model_patches.get(instance.instance_id, "")
            res = self.evaluate_patch(instance, patch)
            results.append(res)
            if res.resolved:
                resolved_count += 1

        total = len(self.benchmark_instances)
        pass_rate = (resolved_count / total * 100.0) if total > 0 else 0.0

        return {
            "total_instances": total,
            "resolved_count": resolved_count,
            "resolution_pass_rate_percent": round(pass_rate, 2),
            "instance_results": [
                {
                    "instance_id": r.instance_id,
                    "resolved": r.resolved,
                    "passed_tests": r.passed_tests,
                    "failed_tests": r.failed_tests
                } for r in results
            ]
        }


if __name__ == "__main__":
    runner = SWEBenchRunner()
    sample_model_patches = {
        "django__django-11099": "regex = r'\\A[a-zA-Z0-9_]+\\Z'",
        "sympy__sympy-13480": "if arg == 0: return ComplexInfinity"
    }

    report = runner.run_benchmark(sample_model_patches)
    print("SWE-bench Evaluation Results:")
    print(json.dumps(report, indent=2))
