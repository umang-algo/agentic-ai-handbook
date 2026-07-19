"""
OpenTelemetry ReAct Tracing Loop

Demonstrates how to use structured transaction spans to log and monitor
the agent's ReAct plan-act-observe loops in production.
"""

import time
from typing import Dict, Any

class MockTracerSpan:
    """Mock implementation of OpenTelemetry span logging."""
    def __init__(self, name: str):
        self.name = name
        self.start_time = 0.0

    def __enter__(self):
        self.start_time = time.monotonic()
        print(f"[Span Start]: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (time.monotonic() - self.start_time) * 1000
        print(f"[Span End]: {self.name} took {duration:.2f}ms")

class OtelAgentTracer:
    @staticmethod
    def start_span(name: str) -> MockTracerSpan:
        return MockTracerSpan(name)

if __name__ == "__main__":
    # Simulate tracing a full agent execution session
    with OtelAgentTracer.start_span("agent_session"):
        
        # 1. LLM call step
        with OtelAgentTracer.start_span("llm_reasoning_call"):
            time.sleep(0.2) # simulated API latency
            
        # 2. Tool calling step
        with OtelAgentTracer.start_span("tool_execution_read_db"):
            time.sleep(0.05) # simulated database read latency
            
        # 3. Final answer compilation
        with OtelAgentTracer.start_span("llm_synthesis_call"):
            time.sleep(0.15)
