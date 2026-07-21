"""
Chapter 16: Model Router & Production Economics Engine
======================================================
Hierarchical cost-latency router evaluating query complexity, routing simple requests
to fast models (GPT-4o-mini / Llama 3 8B) and complex requests to heavy models (GPT-4o / DeepSeek R1).

From: The Practitioner's Handbook of Agentic AI, Chapter 16.1
"""

import os
import sys
from dataclasses import dataclass
from typing import Dict, Any, List

# Add coding-handbook root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.logger import AgentLogger, Colors
from common.metrics import CostTracker


@dataclass
class QueryRequest:
    query_id: str
    prompt: str
    complexity_score: float  # 0.0 (Simple) to 1.0 (Complex Reasoning)


class TieredModelRouter:
    """Production Model Router balancing latency, cost, and accuracy thresholds."""

    def __init__(self):
        self.fast_model = "llama-3-8b"
        self.heavy_model = "gpt-4o"
        self.routing_threshold = 0.65

    def route_query(self, request: QueryRequest) -> Dict[str, Any]:
        """Routes query based on complexity score."""
        if request.complexity_score >= self.routing_threshold:
            chosen_model = self.heavy_model
            reason = "High complexity query requires deep reasoning model."
        else:
            chosen_model = self.fast_model
            reason = "Low complexity query routed to fast model for cost/latency optimization."

        input_tokens = len(request.prompt.split()) * 4
        output_tokens = 150
        cost = CostTracker.calculate_cost(chosen_model, input_tokens, output_tokens)

        return {
            "query_id": request.query_id,
            "chosen_model": chosen_model,
            "complexity_score": request.complexity_score,
            "estimated_cost_usd": cost,
            "routing_reason": reason
        }


def run_model_router_benchmark():
    AgentLogger.title("Production Tiered Model Router & Cost Simulation")

    router = TieredModelRouter()

    queries = [
        QueryRequest("Q-1", "What is the capital of France?", 0.15),
        QueryRequest("Q-2", "Prove the convergence of gradient descent under L-smooth loss.", 0.92),
        QueryRequest("Q-3", "Summarize this 10-line text snippet.", 0.30),
        QueryRequest("Q-4", "Debug this complex distributed deadlock in C++ multi-threading.", 0.88),
    ]

    total_tiered_cost = 0.0
    total_heavy_only_cost = 0.0

    for q in queries:
        res = router.route_query(q)
        total_tiered_cost += res["estimated_cost_usd"]

        # Calculate cost if ALL queries were routed to GPT-4o
        heavy_cost = CostTracker.calculate_cost("gpt-4o", len(q.prompt.split()) * 4, 150)
        total_heavy_only_cost += heavy_cost

        print(
            f"Query {q.query_id} (Complexity {q.complexity_score:.2f}) -> "
            f"Model: {Colors.OKGREEN}{res['chosen_model']:<15}{Colors.ENDC} | "
            f"Cost: ${res['estimated_cost_usd']:.6f}"
        )

    savings_percent = ((total_heavy_only_cost - total_tiered_cost) / total_heavy_only_cost) * 100.0
    AgentLogger.section("Economics & Savings Summary")
    print(f"Tiered Router Total Cost:    ${total_tiered_cost:.6f}")
    print(f"All-GPT-4o Unoptimized Cost: ${total_heavy_only_cost:.6f}")
    print(f"{Colors.BOLD}Total Savings Ratio:         {savings_percent:.1f}% Savings{Colors.ENDC}")


if __name__ == "__main__":
    run_model_router_benchmark()
