"""
GitHub PR Webhook Listener Server

A mock FastAPI listener that accepts incoming GitHub webhook triggers
when a pull_request event is opened or edited.
"""

from typing import Dict, Any

class MockWebhookServer:
    def __init__(self, port: int = 8080):
        self.port = port

    def receive_payload(self, headers: Dict[str, str], payload: Dict[str, Any]) -> dict:
        """Processes incoming webhook event payloads."""
        event_type = headers.get("X-GitHub-Event", "unknown")
        
        if event_type == "pull_request":
            action = payload.get("action")
            pr_number = payload.get("number")
            repo_name = payload.get("repository", {}).get("full_name")
            print(f"[Webhook Server]: PR #{pr_number} {action} in repo '{repo_name}'")
            return {"status": "processing", "pr": pr_number, "action": action}
            
        print("[Webhook Server]: Event ignored:", event_type)
        return {"status": "ignored"}

if __name__ == "__main__":
    server = MockWebhookServer()
    
    mock_headers = {"X-GitHub-Event": "pull_request"}
    mock_payload = {
        "action": "opened",
        "number": 42,
        "repository": {"full_name": "user/repo"}
    }
    
    response = server.receive_payload(mock_headers, mock_payload)
    print("Server Response:", response)
