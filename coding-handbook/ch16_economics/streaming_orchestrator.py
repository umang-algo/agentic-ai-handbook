"""
Token Streaming Orchestrator

Demonstrates how to process streaming chunks from LLM endpoints to reduce
Time-To-First-Token (TTFT) latency for better user experience.
"""

import time
from typing import Generator

class StreamingOrchestrator:
    @staticmethod
    def simulate_stream(prompt: str) -> Generator[str, None, None]:
        """Simulates streaming chunks of an LLM completion response."""
        response_text = f"Here is your answer to: '{prompt}'. This response is streamed in chunks."
        chunks = [word + " " for word in response_text.split()]
        
        for chunk in chunks:
            time.sleep(0.08) # simulated token latency (80ms)
            yield chunk

if __name__ == "__main__":
    orchestrator = StreamingOrchestrator()
    print("Sending prompt and streaming response:")
    
    t0 = time.monotonic()
    first_token = True
    
    for token in orchestrator.simulate_stream("Describe LLM token budgets"):
        if first_token:
            ttft = (time.monotonic() - t0) * 1000
            print(f"(TTFT: {ttft:.1f}ms) ", end="", flush=True)
            first_token = False
        print(token, end="", flush=True)
    print("\n\nStream completed.")
