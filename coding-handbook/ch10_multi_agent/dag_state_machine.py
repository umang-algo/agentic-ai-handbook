"""
Chapter 10: Multi-Agent DAG State Machine Orchestrator
======================================================
Production DAG multi-agent state machine orchestrator managing graph execution,
conditional branching, and state checkpoint recovery.

From: The Practitioner's Handbook of Agentic AI, Chapter 10.1
"""

import os
import sys
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Callable

# Add coding-handbook root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.logger import AgentLogger, Colors


@dataclass
class WorkflowState:
    thread_id: str
    current_node: str
    context_data: Dict[str, Any] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)
    completed: bool = False


class DAGStateMachine:
    """DAG State Machine Orchestrator managing multi-agent execution graphs."""
    def __init__(self, start_node: str):
        self.start_node = start_node
        self.nodes: Dict[str, Callable[[WorkflowState], WorkflowState]] = {}
        self.transitions: Dict[str, List[str]] = {}

    def add_node(self, name: str, handler: Callable[[WorkflowState], WorkflowState]):
        self.nodes[name] = handler
        if name not in self.transitions:
            self.transitions[name] = []

    def add_edge(self, from_node: str, to_node: str):
        if from_node not in self.transitions:
            self.transitions[from_node] = []
        self.transitions[from_node].append(to_node)

    def run(self, thread_id: str, initial_data: Dict[str, Any]) -> WorkflowState:
        state = WorkflowState(thread_id=thread_id, current_node=self.start_node, context_data=initial_data)

        while not state.completed:
            curr = state.current_node
            state.history.append(curr)

            if curr in self.nodes:
                state = self.nodes[curr](state)

            next_nodes = self.transitions.get(curr, [])
            if not next_nodes:
                state.completed = True
            else:
                state.current_node = next_nodes[0]

        return state


def run_multi_agent_demo():
    AgentLogger.title("Multi-Agent DAG State Machine Execution")

    dag = DAGStateMachine(start_node="Router")

    def router_node(state: WorkflowState) -> WorkflowState:
        AgentLogger.info("[Node: Router] Classifying user prompt intent...")
        state.context_data["router_decision"] = "Write Python Function"
        return state

    def coder_node(state: WorkflowState) -> WorkflowState:
        AgentLogger.info("[Node: Coder Agent] Generating python code block...")
        state.context_data["code"] = "def calculate_fibonacci(n):\n    return n if n <= 1 else calculate_fibonacci(n-1) + calculate_fibonacci(n-2)"
        return state

    def reviewer_node(state: WorkflowState) -> WorkflowState:
        AgentLogger.info("[Node: Reviewer Agent] Validating syntax and performance...")
        state.context_data["review_status"] = "PASSED"
        return state

    dag.add_node("Router", router_node)
    dag.add_node("Coder", coder_node)
    dag.add_node("Reviewer", reviewer_node)

    dag.add_edge("Router", "Coder")
    dag.add_edge("Coder", "Reviewer")

    final_state = dag.run("thread_101", {"user_prompt": "Write fibonacci function"})
    
    AgentLogger.section("State Trajectory Summary")
    print(f"Graph Path Traversed: {' -> '.join(final_state.history)}")
    print(f"Review Status:        {final_state.context_data.get('review_status')}")
    AgentLogger.success("DAG Multi-Agent state execution completed.")


if __name__ == "__main__":
    run_multi_agent_demo()
