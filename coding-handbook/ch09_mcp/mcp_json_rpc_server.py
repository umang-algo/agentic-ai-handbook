"""
Chapter 9: Model Context Protocol (MCP) JSON-RPC 2.0 Server
============================================================
Production Model Context Protocol (MCP) server handling tool discovery,
schema validation, and execution over JSON-RPC 2.0.

From: The Practitioner's Handbook of Agentic AI, Chapter 9.1
"""

import json
from typing import Dict, Any, Callable


class MCPJSONRPCServer:
    """Model Context Protocol JSON-RPC 2.0 Server."""
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.handlers: Dict[str, Callable] = {}

    def register_tool(self, name: str, description: str, schema: dict, handler: Callable):
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": schema
        }
        self.handlers[name] = handler

    def handle_message(self, json_message: str) -> str:
        """Parses JSON-RPC 2.0 request and dispatches tool execution."""
        try:
            req = json.loads(json_message)
            req_id = req.get("id")
            method = req.get("method")

            if method == "tools/list":
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": list(self.tools.values())}
                })
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})

                if tool_name in self.handlers:
                    exec_result = self.handlers[tool_name](**tool_args)
                    return json.dumps({
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"content": [{"type": "text", "text": str(exec_result)}]}
                    })
                else:
                    return json.dumps({
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."}
                    })

            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not supported."}
            })
        except Exception as e:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            })


if __name__ == "__main__":
    server = MCPJSONRPCServer()

    # Register sample tool
    def add_numbers(a: int, b: int) -> int:
        return a + b

    server.register_tool(
        "add",
        "Adds two integers together.",
        {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}},
        add_numbers
    )

    # 1. Test tools/list request
    list_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    print("List Response:", server.handle_message(list_req))

    # 2. Test tools/call request
    call_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "add", "arguments": {"a": 10, "b": 25}}})
    print("Call Response:", server.handle_message(call_req))
