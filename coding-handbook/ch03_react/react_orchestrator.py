"""
Chapter 3: Production ReAct Orchestrator
==========================================
Complete ReActState with loop detection, cost tracking, offline mock execution, and full audit trail.

From: The Practitioner's Handbook of Agentic AI, Chapter 3.3
"""

import os
import sys
import json
import hashlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# Add coding-handbook root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.logger import AgentLogger, Colors
from common.mock_llm import MockLLMProvider
from common.metrics import CostTracker


@dataclass
class AgentStep:
    """A single step in the agent's trajectory."""
    thought: str
    action_name: str
    action_args: dict
    observation: Optional[str] = None
    error: Optional[str] = None
    tokens_used: int = 0


class ReActState:
    """
    Production-grade agent state manager with loop detection,
    cost tracking, and full audit trail.
    """
    def __init__(self, user_prompt: str, system_prompt: str,
                 max_iterations: int = 10, max_cost_usd: float = 1.0):
        self.user_prompt = user_prompt
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.max_cost_usd = max_cost_usd
        self.steps: list[AgentStep] = []
        self.history = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ]
        self.total_tokens = 0
        self.estimated_cost_usd = 0.0
        self._action_hashes: set[str] = set()

    def add_thought_and_action(self, thought: str, action_name: str,
                               action_args: dict, tokens: int) -> None:
        """Records an LLM reasoning step and enforces loop detection."""
        action_signature = hashlib.sha256(
            json.dumps({"n": action_name, "a": action_args}, sort_keys=True).encode()
        ).hexdigest()

        if action_signature in self._action_hashes:
            raise RuntimeError(
                f"Loop detected! Agent proposed identical action '{action_name}' again. Terminating."
            )

        self._action_hashes.add(action_signature)
        self.total_tokens += tokens
        self.estimated_cost_usd = CostTracker.calculate_cost("gpt-4o", input_tokens=self.total_tokens, output_tokens=100)

        if self.estimated_cost_usd > self.max_cost_usd:
            raise RuntimeError(f"Cost limit exceeded! ${self.estimated_cost_usd:.4f} > ${self.max_cost_usd:.4f}")

        step = AgentStep(thought=thought, action_name=action_name, action_args=action_args, tokens_used=tokens)
        self.steps.append(step)

    def add_observation(self, observation: str) -> None:
        """Appends tool execution observation to latest step."""
        if self.steps:
            self.steps[-1].observation = observation
            self.history.append({"role": "user", "content": f"Observation: {observation}"})


class ProductionReActOrchestrator:
    """Production ReAct Agent loop using offline Mock LLM Provider."""

    def __init__(self, mock_llm: Optional[MockLLMProvider] = None):
        self.llm = mock_llm or MockLLMProvider("mock-gpt-4o")

    def run(self, user_query: str) -> str:
        AgentLogger.title(f"ReAct Execution Loop: '{user_query}'")
        state = ReActState(user_query, "You are a helpful ReAct assistant.")

        # Simulate ReAct trajectory
        step_1_thought = "I need to check the weather in Tokyo to answer the user."
        step_1_action = "get_weather"
        step_1_args = {"location": "Tokyo"}

        state.add_thought_and_action(step_1_thought, step_1_action, step_1_args, tokens=120)
        obs_1 = '{"temperature": "25C", "condition": "Sunny"}'
        state.add_observation(obs_1)

        AgentLogger.trajectory_box(1, step_1_thought, f"{step_1_action}({step_1_args})", obs_1)

        final_response = "The weather in Tokyo is currently 25C and Sunny."
        AgentLogger.success(f"Final Answer: {final_response}")
        AgentLogger.info(f"Trajectory Cost: ${state.estimated_cost_usd:.6f} | Total Tokens: {state.total_tokens}")

        return final_response


if __name__ == "__main__":
    orchestrator = ProductionReActOrchestrator()
    orchestrator.run("What is the weather in Tokyo right now?")
