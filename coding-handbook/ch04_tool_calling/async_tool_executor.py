"""
Chapter 4: Parallel Async Tool Executor
=========================================
Executes multiple tool calls concurrently. A single tool failure does NOT
abort the others — each result is captured independently.

Performance: 3 tools at (1.2s, 0.1s, 0.8s) completes in ~1.2s, not 2.1s.

From: The Practitioner's Handbook of Agentic AI, Chapter 4.1
"""

import asyncio
import json
import time
from typing import Callable, Any

# Tool registry: maps function name -> async function
TOOL_REGISTRY: dict[str, Callable] = {}


def tool(name: str):
    """Decorator to register an async function as a callable tool."""
    def decorator(fn):
        TOOL_REGISTRY[name] = fn
        return fn
    return decorator


@tool("search_web")
async def search_web(query: str, num_results: int = 5) -> dict:
    await asyncio.sleep(1.2)  # Simulates 1.2s network latency
    return {"query": query, "results": [f"Result {i}" for i in range(num_results)]}


@tool("read_file")
async def read_file(path: str) -> dict:
    await asyncio.sleep(0.1)  # Fast local I/O
    return {"path": path, "content": "...file content..."}


@tool("query_database")
async def query_database(sql: str) -> dict:
    await asyncio.sleep(0.8)  # Database latency
    return {"sql": sql, "rows": [{"id": 1, "name": "Example"}]}


async def execute_parallel_tools(tool_calls: list[dict]) -> list[dict]:
    """
    Executes all tool calls concurrently. A single tool failure
    does NOT abort the others -- each result is captured independently.
    """
    async def run_one(call: dict) -> dict:
        name = call["function"]["name"]
        args = json.loads(call["function"]["arguments"])
        call_id = call["id"]
        try:
            fn = TOOL_REGISTRY[name]
            result = await asyncio.wait_for(fn(**args), timeout=30.0)
            return {"tool_call_id": call_id, "role": "tool",
                    "name": name, "content": json.dumps(result)}
        except asyncio.TimeoutError:
            return {"tool_call_id": call_id, "role": "tool",
                    "name": name, "content": f"Error: Tool '{name}' timed out after 30s"}
        except Exception as e:
            return {"tool_call_id": call_id, "role": "tool",
                    "name": name, "content": f"Error: {str(e)}"}

    tasks = [run_one(call) for call in tool_calls]
    return await asyncio.gather(*tasks)


# ─── Demo ───────────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("Parallel Tool Execution Demo")
    print("=" * 60)

    # Simulate 3 parallel tool calls from the LLM
    tool_calls = [
        {"id": "call_1", "function": {"name": "search_web",
         "arguments": '{"query": "latest AI news", "num_results": 3}'}},
        {"id": "call_2", "function": {"name": "read_file",
         "arguments": '{"path": "src/main.py"}'}},
        {"id": "call_3", "function": {"name": "query_database",
         "arguments": '{"sql": "SELECT * FROM users LIMIT 5"}'}},
    ]

    # Sequential timing estimate
    print(f"\nSequential estimate: 1.2 + 0.1 + 0.8 = 2.1 seconds")

    t0 = time.monotonic()
    results = await execute_parallel_tools(tool_calls)
    elapsed = time.monotonic() - t0

    print(f"Parallel actual:    {elapsed:.2f} seconds")
    print(f"Speedup:            {2.1/elapsed:.1f}x\n")

    for r in results:
        print(f"  {r['name']}: {r['content'][:60]}...")


if __name__ == "__main__":
    asyncio.run(main())
