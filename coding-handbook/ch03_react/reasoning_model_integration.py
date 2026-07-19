"""
Reasoning Model Integration & Thoughtless Loops

Demonstrates how to integrate reasoning models (like o1, o3, or DeepSeek-R1) into agent
pipelines. Shows how to parse DeepSeek-R1's <think> tags for observability and how to
orchestrate "thoughtless" tool execution loops.
"""

import re
from typing import Dict, Tuple

class ReasoningModelAgent:
    """Orchestrates interaction with internal-reasoning models."""

    @staticmethod
    def parse_r1_response(raw_completion: str) -> Tuple[str, str]:
        """
        Parses a response from DeepSeek-R1.
        Returns a tuple: (reasoning_process, final_response)
        """
        # Search for content inside <think>...</think>
        match = re.search(r"<think>(.*?)</think>", raw_completion, re.DOTALL)
        if match:
            reasoning = match.group(1).strip()
            # Remove the think block to get the final response
            final_output = re.sub(r"<think>.*?</think>", "", raw_completion, flags=re.DOTALL).strip()
            return reasoning, final_output
        return "", raw_completion.strip()

    @staticmethod
    def run_thoughtless_tool_loop(prompt: str, mock_llm_fn) -> dict:
        """
        Executes a 'Thoughtless Loop'. Since the reasoning model does internal planning,
        the agent orchestrator skips prompting the model for a 'Thought' block and
        directly parses tool arguments from the output.
        """
        print(f"[Orchestrator]: Sending prompt to reasoning model...")
        response = mock_llm_fn(prompt)
        
        # Parse the reasoning phase and final output
        reasoning, final_output = ReasoningModelAgent.parse_r1_response(response)
        
        if reasoning:
            print(f"[Observability]: Captured hidden reasoning steps ({len(reasoning)} chars):\n{reasoning}\n")
            
        # Parse tool calls directly from final output (e.g. JSON markdown block)
        tool_call_match = re.search(r"```json\n(.*?)\n```", final_output, re.DOTALL)
        if tool_call_match:
            try:
                tool_data = json_loads_mock(tool_call_match.group(1).strip())
                print(f"[Orchestrator]: Executing tool '{tool_data['tool']}' with args: {tool_data['args']}")
                return {"status": "tool_executed", "tool": tool_data["tool"], "args": tool_data["args"]}
            except Exception as e:
                print(f"[Orchestrator]: Error parsing tool JSON:", e)
                
        return {"status": "final_response", "output": final_output}

def json_loads_mock(json_str: str) -> dict:
    # A simple mock parser to avoid import json overhead in this isolated demo
    import json
    return json.loads(json_str)

if __name__ == "__main__":
    # Simulated Raw Output from DeepSeek-R1
    mock_r1_output = (
        "<think>\n"
        "The user wants to read 'src/main.py'.\n"
        "I need to call the read_file tool with path='src/main.py'.\n"
        "Let me output this in JSON format for the parser.\n"
        "</think>\n"
        "```json\n"
        '{"tool": "read_file", "args": {"path": "src/main.py"}}\n'
        "```"
    )
    
    # Mock LLM API function
    def mock_deepseek_r1(prompt: str) -> str:
        return mock_r1_output

    print("--- Parsing DeepSeek-R1 Raw Response ---")
    reasoning, final_text = ReasoningModelAgent.parse_r1_response(mock_r1_output)
    print("Extracted Thought Stage:\n", reasoning)
    print("\nExtracted Final Text Stage:\n", final_text)
    
    print("\n--- Running Thoughtless Orchestration Loop ---")
    result = ReasoningModelAgent.run_thoughtless_tool_loop(
        prompt="Fetch content of src/main.py",
        mock_llm_fn=mock_deepseek_r1
    )
    print("\nResult:", result)
