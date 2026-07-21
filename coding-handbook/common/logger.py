"""
Common Terminal Logger & Agent Trajectory Formatter
==================================================
Rich terminal formatting with ANSI colors, step-by-step agent trajectory boxes,
execution timers, and structured logging.

From: The Practitioner's Handbook of Agentic AI
"""

import sys
import time
from typing import Any, Dict, Optional


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class AgentLogger:
    """Production logger providing formatted terminal output for agent execution steps."""

    @staticmethod
    def title(msg: str):
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== {msg} ==={Colors.ENDC}\n")

    @staticmethod
    def section(msg: str):
        print(f"\n{Colors.OKCYAN}{Colors.BOLD}--- {msg} ---{Colors.ENDC}")

    @staticmethod
    def info(msg: str):
        print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {msg}")

    @staticmethod
    def success(msg: str):
        print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {msg}")

    @staticmethod
    def warning(msg: str):
        print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} {msg}")

    @staticmethod
    def error(msg: str):
        print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {msg}")

    @staticmethod
    def thought(thought_text: str):
        print(f"{Colors.WARNING}🤔 [THOUGHT]{Colors.ENDC} {thought_text}")

    @staticmethod
    def action(action_name: str, args: Dict[str, Any]):
        print(f"{Colors.OKCYAN}⚡ [ACTION]{Colors.ENDC} {action_name}({args})")

    @staticmethod
    def observation(obs_text: str):
        print(f"{Colors.OKBLUE}👁️ [OBSERVATION]{Colors.ENDC} {obs_text}")

    @staticmethod
    def trajectory_box(step_num: int, thought: str, action: str, observation: str):
        border = "=" * 60
        print(f"\n{Colors.BOLD}{border}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD} STEP {step_num} TRAJECTORY{Colors.ENDC}")
        print(f"{Colors.BOLD}{border}{Colors.ENDC}")
        print(f"{Colors.WARNING}Thought:{Colors.ENDC}     {thought}")
        print(f"{Colors.OKCYAN}Action:{Colors.ENDC}      {action}")
        print(f"{Colors.OKBLUE}Observation:{Colors.ENDC} {observation}")
        print(f"{Colors.BOLD}{border}{Colors.ENDC}\n")


class Timer:
    """Execution timer utility."""
    def __init__(self):
        self.start_time = time.time()

    def elapsed_ms(self) -> float:
        return (time.time() - self.start_time) * 1000.0


if __name__ == "__main__":
    logger = AgentLogger()
    logger.title("Agent Logger Interactive Demo")
    logger.info("Initializing Agent Session...")
    logger.thought("I need to fetch user order details from the database.")
    logger.action("execute_sql", {"query": "SELECT * FROM orders WHERE id='ORD-101'"})
    logger.observation("Order Status: SHIPPED")
    logger.trajectory_box(1, "Parsed order ID successfully.", "execute_sql", "SHIPPED")
    logger.success("Completed Agent Trajectory Demo.")
