"""
Model Context Protocol (MCP) JSON-RPC Message Handler

Demonstrates standard JSON-RPC 2.0 messages used by MCP servers and clients.
"""

import json
from typing import Dict, Optional

class MCPMessageHandler:
    """Encodes and decodes Model Context Protocol JSON-RPC 2.0 messages."""
    
    @staticmethod
    def create_request(method: str, params: dict, request_id: int) -> str:
        """Creates a standard JSON-RPC request payload."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id
        }
        return json.dumps(payload)

    @staticmethod
    def create_response(result: dict, request_id: int) -> str:
        """Creates a standard JSON-RPC success response."""
        payload = {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }
        return json.dumps(payload)

    @staticmethod
    def create_error(code: int, message: str, request_id: Optional[int] = None) -> str:
        """Creates a standard JSON-RPC error response."""
        payload = {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": request_id
        }
        return json.dumps(payload)

    @staticmethod
    def parse_message(raw_json: str) -> Dict:
        """Parses and validates incoming JSON-RPC payloads."""
        data = json.loads(raw_json)
        if "jsonrpc" not in data or data["jsonrpc"] != "2.0":
            raise ValueError("Invalid JSON-RPC version")
        return data

if __name__ == "__main__":
    # Simulate client requesting list of available tools
    req = MCPMessageHandler.create_request("tools/list", {}, 1)
    print("Client Tool List Request:")
    print(req)
    
    # Parse request
    parsed_req = MCPMessageHandler.parse_message(req)
    
    # Simulate server responding with tools list
    tools_list = {
        "tools": [
            {"name": "read_file", "description": "Read file content"},
            {"name": "write_file", "description": "Write file content"}
        ]
    }
    resp = MCPMessageHandler.create_response(tools_list, parsed_req["id"])
    print("\nServer Tool List Response:")
    print(resp)
