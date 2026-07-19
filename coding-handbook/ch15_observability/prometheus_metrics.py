"""
Prometheus Metrics Simulator

Simulates recording prometheus metrics for tool errors, agent execution latencies,
and token consumption rates in production.
"""

from typing import Dict

class PrometheusMetricStore:
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.histograms: Dict[str, list] = {}

    def increment_counter(self, name: str, labels: dict) -> None:
        key = f"{name}_{str(labels)}"
        self.counters[key] = self.counters.get(key, 0) + 1
        print(f"[Prometheus]: Counter '{name}' with labels {labels} incremented to {self.counters[key]}")

    def observe_histogram(self, name: str, value: float, labels: dict) -> None:
        key = f"{name}_{str(labels)}"
        if key not in self.histograms:
            self.histograms[key] = []
        self.histograms[key].append(value)
        print(f"[Prometheus]: Histogram '{name}' observed value {value}ms with labels {labels}")

if __name__ == "__main__":
    metrics = PrometheusMetricStore()
    
    # 1. Track token consumption
    metrics.increment_counter("agent_tokens_total", {"model": "claude-3.5-sonnet", "type": "input"})
    
    # 2. Track tool calls & potential execution failures
    metrics.increment_counter("agent_tool_calls_total", {"tool": "run_sandbox_code", "status": "failed"})
    
    # 3. Track latency
    metrics.observe_histogram("agent_response_latency_seconds", 1.85, {"agent": "coder"})
