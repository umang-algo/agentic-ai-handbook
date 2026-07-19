"""
Chapter 3: Production ReAct Orchestrator
==========================================
Complete ReActState with loop detection, cost tracking, and full audit trail.
This would have prevented the $312 runaway agent from the chapter opening.

From: The Practitioner's Handbook of Agentic AI, Chapter 3.3
"""

import json
import hashlib
from dataclasses import dataclass, field
from typing import Optional


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
        self._action_hashes: set[str] = set()  # for loop detection

    def add_thought_and_action(self, thought: str, action_name: str,
                               action_args: dict, tokens: int) -> None:
        """Records an LLM reasoning step."""
        # Loop detection: hash the (action_name, args) pair
        action_signature = hashlib.sha256(
            json.dumps({"n": action_name, "a": action_args},
                       sort_keys=True).encode()
        ).hexdigest()

        if action_signature in self._action_hashes:
            raise RuntimeError(
                f"Loop detected! Agent proposed identical action "
                f"'{action_name}' again. Terminating."
            )
        self._action_hashes.add(action_signature)

        step = AgentStep(thought=thought, action_name=action_name,
                         action_args=action_args, tokens_used=tokens)
        self.steps.append(step)
        self.total_tokens += tokens

        # Approximate cost at GPT-4o rates
        self.estimated_cost_usd += (tokens / 1_000_000) * 2.50
        if self.estimated_cost_usd > self.max_cost_usd:
            raise RuntimeError(
                f"Cost cap exceeded: ${self.estimated_cost_usd:.3f} "
                f"> ${self.max_cost_usd:.2f}. Terminating."
            )

        content = f"Thought: {thought}\nAction: {json.dumps({'name': action_name, 'args': action_args})}"
        self.history.append({"role": "assistant", "content": content})

    def add_observation(self, result: str, is_error: bool = False) -> None:
        """Appends a tool execution result to the conversation history."""
        if self.steps:
            self.steps[-1].observation = result
            self.steps[-1].error = result if is_error else None

        prefix = "Error: " if is_error else "Observation: "
        self.history.append({"role": "user", "content": prefix + result})

    def is_runnable(self) -> tuple[bool, str]:
        """Checks whether the agent should continue running."""
        if len(self.steps) >= self.max_iterations:
            return False, f"Max iterations ({self.max_iterations}) reached."
        if self.estimated_cost_usd >= self.max_cost_usd:
            return False, "Cost cap reached."
        return True, "ok"

    def get_audit_trail(self) -> list[dict]:
        """Returns the full audit trail for debugging."""
        return [
            {
                "step": i + 1,
                "thought": step.thought,
                "action": step.action_name,
                "args": step.action_args,
                "observation": step.observation,
                "error": step.error,
                "tokens": step.tokens_used,
            }
            for i, step in enumerate(self.steps)
        ]


# ─── Demo ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 65)
    print("ReAct Orchestrator State Demo")
    print("=" * 65)

    state = ReActState(
        user_prompt="Find the weather in NYC",
        system_prompt="You are a helpful assistant with tools.",
        max_iterations=5,
        max_cost_usd=0.01
    )

    # Simulate a successful agent run
    state.add_thought_and_action(
        thought="I need to search for NYC weather",
        action_name="search_web",
        action_args={"query": "NYC weather today"},
        tokens=500
    )
    state.add_observation("Temperature: 72°F, Sunny")

    print(f"\nSteps completed: {len(state.steps)}")
    print(f"Total tokens: {state.total_tokens}")
    print(f"Estimated cost: ${state.estimated_cost_usd:.4f}")
    print(f"Runnable: {state.is_runnable()}")

    # Demonstrate loop detection
    print(f"\n--- Loop Detection Demo ---")
    try:
        state.add_thought_and_action(
            thought="Let me search again",
            action_name="search_web",
            action_args={"query": "NYC weather today"},  # Same action!
            tokens=500
        )
    except RuntimeError as e:
        print(f"✅ Caught: {e}")

    # Show audit trail
    print(f"\n--- Audit Trail ---")
    for entry in state.get_audit_trail():
        print(f"  Step {entry['step']}: {entry['action']}({entry['args']}) → {entry['observation']}")
