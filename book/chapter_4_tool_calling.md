# Chapter 4: Tool Calling (Native Architecture & AsyncIO)

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch04_tool_calling](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch04_tool_calling)

Native Tool Calling (Function Calling) is not just a UI convenience; it is a structural change in how the LLM computes output. In Chapter 2, we discussed Logit Bias. Native Tool Calling uses similar exact-schema enforcement mechanisms on the inference provider's backend.

## 4.1 The Exact JSON Payload Over the Wire

To understand Tool Calling, you must inspect the raw HTTP payload sent to OpenAI or Anthropic. You are defining the tool schema using JSON Schema (Draft 7).

### The HTTP Request Payload

```json
{
  "model": "gpt-4-turbo",
  "messages": [
    {"role": "user", "content": "Get the weather in NYC and SF."}
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Fetches current weather for a specific city.",
        "parameters": {
          "type": "object",
          "properties": {
            "city": { "type": "string" },
            "unit": { "type": "string", "enum": ["C", "F"] }
          },
          "required": ["city"]
        }
      }
    }
  ],
  "tool_choice": "auto"
}
```

### The Model's Structured Response
When the model decides to use a tool, it halts text generation and returns a `tool_calls` array. Notice that it assigns a unique `id` to each call. This is crucial for matching the result back to the specific call when handling parallel execution.

```json
{
  "message": {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"city\":\"NYC\"}"
        }
      },
      {
        "id": "call_def456",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"city\":\"SF\"}"
        }
      }
    ]
  }
}
```

## 4.2 Parallel Tool Execution Architecture

In the example above, the model requested two cities simultaneously. Executing these sequentially is a massive performance bottleneck. If a database query takes 5 seconds, querying two takes 10 seconds. 

Production agents must execute tool calls concurrently using Python's `asyncio` event loop.

```python
import asyncio
import json

async def mock_get_weather(city):
    """A slow IO-bound tool."""
    await asyncio.sleep(2) # Simulate network latency
    return f"Weather in {city} is 70F"

async def execute_tool_calls_concurrently(tool_calls):
    """Executes multiple tool calls in parallel and maps results."""
    
    available_tools = {"get_weather": mock_get_weather}
    tasks = []
    
    for tool_call in tool_calls:
        func_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])
        
        # Create an asyncio Task for each tool call
        if func_name in available_tools:
            coro = available_tools[func_name](**arguments)
            # Store the task alongside its original call ID for matching later
            tasks.append((tool_call["id"], func_name, asyncio.create_task(coro)))
            
    # Wait for all tasks to complete concurrently
    results_list = []
    for call_id, func_name, task in tasks:
        try:
            result = await task
            # Format the output as an OpenAI 'tool' message
            results_list.append({
                "tool_call_id": call_id,
                "role": "tool",
                "name": func_name,
                "content": result
            })
        except Exception as e:
            results_list.append({
                "tool_call_id": call_id,
                "role": "tool",
                "name": func_name,
                "content": f"Error: {str(e)}"
            })
            
    return results_list

# Imagine `pending_calls` is the JSON array from the LLM response above
# results = asyncio.run(execute_tool_calls_concurrently(pending_calls))
```

By pushing tool execution to the asyncio event loop, you reduce the Agent's Wall-Clock Time (WCT) from $O(N \times \text{Latency})$ to $O(\max(\text{Latency}))$, which is critical for real-time user experiences like Cursor's Composer.
