"""
Self-Healing Compiler Diagnostic Loop

Demonstrates a ReAct self-healing execution pattern. When an agent outputs code that
fails compile or syntax verification, the runtime captures the error trace and automatically
passes it back to the agent for self-correction.
"""

import sys
import traceback
from typing import Callable, Optional

class SelfHealingExecutor:
    """Executes code blocks with compiler/syntax verification and retry limits."""
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts

    def execute_and_heal(self, code_generator_fn: Callable[[Optional[str]], str]) -> dict:
        """
        Runs the self-healing loop.
        code_generator_fn: Takes an optional traceback string, returns python code string.
        """
        error_feedback = None
        
        for attempt in range(1, self.max_attempts + 1):
            print(f"\n--- Attempt {attempt} of {self.max_attempts} ---")
            code = code_generator_fn(error_feedback)
            print("Generated Code:\n", code)
            
            try:
                # Compile code to verify syntax
                compiled_code = compile(code, "<string>", "exec")
                
                # Execute in an isolated scope
                local_scope = {}
                exec(compiled_code, {}, local_scope)
                
                # If execution succeeds
                print("✓ Execution successful!")
                return {
                    "status": "success",
                    "attempts": attempt,
                    "local_scope": local_scope,
                    "code": code
                }
                
            except Exception as e:
                # Format traceback to inject back into agent context
                exc_type, exc_value, exc_tb = sys.exc_info()
                formatted_tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
                print(f"✗ Execution failed with error:\n{formatted_tb}")
                
                error_feedback = (
                    f"Your previous code failed execution with the following traceback:\n"
                    f"{formatted_tb}\n"
                    f"Please identify the bug, repair the code, and output the entire corrected file."
                )
                
        return {
            "status": "failed",
            "attempts": self.max_attempts,
            "error": error_feedback
        }

if __name__ == "__main__":
    # Mock generator simulating an LLM correcting its own bugs
    buggy_codes = [
        # Attempt 1: NameError
        "def run():\n    print(result_value)\nrun()",
        # Attempt 2: ZeroDivisionError
        "def run():\n    result_value = 10 / 0\n    print(result_value)\nrun()",
        # Attempt 3: Fixed Code
        "def run():\n    result_value = 10 / 2\n    print('Result is:', result_value)\nrun()"
    ]
    
    attempts_made = 0
    def mock_llm_generator(error_msg: Optional[str]) -> str:
        global attempts_made
        if error_msg:
            print("\n[LLM received error feedback. Generating fix...]")
        code = buggy_codes[attempts_made]
        attempts_made += 1
        return code

    executor = SelfHealingExecutor(max_attempts=3)
    result = executor.execute_and_heal(mock_llm_generator)
    print("\nFinal Result:", result["status"])
