"""
Benchmark Runner Harness

Demonstrates compiling and running a custom test suite to evaluate target model outputs
against multiple test cases, calculating aggregate pass rates.
"""

from typing import List, Callable, Dict, Any

class BenchmarkRunner:
    def __init__(self, dataset: List[Dict[str, Any]]):
        self.dataset = dataset

    def run_suite(self, agent_fn: Callable[[str], str]) -> dict:
        results = []
        pass_count = 0
        
        for case in self.dataset:
            prompt = case["prompt"]
            expected = case["expected"]
            
            # Call model
            output = agent_fn(prompt)
            
            # Simple match evaluation
            passed = expected.lower() in output.lower()
            if passed:
                pass_count += 1
                
            results.append({
                "prompt": prompt,
                "output": output,
                "expected": expected,
                "passed": passed
            })
            
        return {
            "total_cases": len(self.dataset),
            "pass_rate": pass_count / len(self.dataset),
            "details": results
        }

if __name__ == "__main__":
    # Test dataset
    test_cases = [
        {"prompt": "Say hello", "expected": "hello"},
        {"prompt": "What is 2+2?", "expected": "4"},
    ]
    
    # Mock agent logic
    def mock_agent(prompt: str) -> str:
        if "hello" in prompt.lower():
            return "Hello there!"
        if "2+2" in prompt:
            return "2+2 is 4"
        return "unsupported"

    runner = BenchmarkRunner(test_cases)
    report = runner.run_suite(mock_agent)
    
    print("Benchmark Report:")
    print("Pass Rate:", f"{report['pass_rate'] * 100}%")
