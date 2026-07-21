"""
Common Offline Mock LLM Provider
================================
Deterministic, offline Mock LLM Provider supporting tool calling, reasoning/thinking tokens
(<thought>), token streaming, and simulated latency. Allows students and researchers to run
100% of labs offline without OpenAI/Anthropic API keys.

From: The Practitioner's Handbook of Agentic AI
"""

import time
import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Generator


@dataclass
class MockLLMResponse:
    content: str
    thought: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    prompt_tokens: int = 150
    completion_tokens: int = 45
    latency_ms: float = 120.0


class MockLLMProvider:
    """
    Offline LLM provider that simulates production model behavior (GPT-4o, Claude 3.5 Sonnet, DeepSeek R1).
    """

    def __init__(self, model_name: str = "mock-gpt-4o", simulate_latency: bool = False):
        self.model_name = model_name
        self.simulate_latency = simulate_latency

    def generate(self, prompt: str, system_prompt: str = "", tools: Optional[List[Dict[str, Any]]] = None) -> MockLLMResponse:
        """Generates a deterministic response based on prompt intent."""
        if self.simulate_latency:
            time.sleep(0.05)

        prompt_lower = prompt.lower()

        # 1. Reasoning / Thinking Model simulation (e.g. DeepSeek R1 / Claude Extended Thinking)
        if "think" in prompt_lower or "reason" in prompt_lower:
            thought = "Analyzed user query. Identifying key entities and optimal action sequence."
            content = "<thought>Analyzed user query. Identifying key entities and optimal action sequence.</thought>\nBased on analysis, the request is valid and optimal path selected."
            return MockLLMResponse(content=content, thought=thought, latency_ms=85.0)

        # 2. Tool calling simulation
        if tools or "weather" in prompt_lower or "search" in prompt_lower or "order" in prompt_lower:
            if "weather" in prompt_lower:
                tool_calls = [{"name": "get_weather", "arguments": {"location": "Tokyo", "unit": "celsius"}}]
                content = "Action: get_weather(location='Tokyo')"
            elif "order" in prompt_lower:
                tool_calls = [{"name": "lookup_order", "arguments": {"order_id": "ORD-9021"}}]
                content = "Action: lookup_order(order_id='ORD-9021')"
            else:
                tool_calls = [{"name": "search_database", "arguments": {"query": prompt[:30]}}]
                content = f"Action: search_database(query='{prompt[:30]}')"

            return MockLLMResponse(
                content=content,
                thought="Detected tool query. Emitting structured function call.",
                tool_calls=tool_calls,
                prompt_tokens=180,
                completion_tokens=30,
                latency_ms=110.0
            )

        # 3. Standard text response
        content = f"Mock LLM Response [{self.model_name}]: Processed request for '{prompt[:40]}...'"
        return MockLLMResponse(
            content=content,
            thought="Standard completion task.",
            prompt_tokens=120,
            completion_tokens=25,
            latency_ms=90.0
        )

    def stream_tokens(self, prompt: str) -> Generator[str, None, None]:
        """Simulates token-by-token streaming output."""
        response = self.generate(prompt)
        words = response.content.split(" ")
        for w in words:
            if self.simulate_latency:
                time.sleep(0.02)
            yield w + " "


if __name__ == "__main__":
    llm = MockLLMProvider("mock-claude-3.5-sonnet")
    res1 = llm.generate("What is the weather in Tokyo?")
    print("Tool Call Simulation:")
    print("Content:", res1.content)
    print("Tool Calls:", res1.tool_calls)

    print("\nStreaming Simulation:")
    for token in llm.stream_tokens("Explain KV Cache in LLMs"):
        print(token, end="", flush=True)
    print()
