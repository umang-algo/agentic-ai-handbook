"""
Permission Scoping & Input Sanitization for Tools

Demonstrates a path traversal guard layer. When an agent calls file write/read tools,
this sandbox layer verifies permissions and isolates target paths inside the workspace.
"""

import os
from pathlib import Path
from typing import Union

class PathPermissionGuard:
    """Restricts file access tools to a specific workspace root directory."""
    def __init__(self, workspace_root: Union[str, Path]):
        self.workspace_root = Path(workspace_root).resolve()

    def verify_path(self, user_provided_path: str) -> Path:
        """
        Validates the path to ensure it does not escape the workspace root.
        Raises PermissionError if a path traversal attack is detected.
        """
        # Resolve full absolute path
        target_path = Path(user_provided_path).resolve()
        
        # Check if target is a subdirectory of workspace root
        if not target_path.is_relative_to(self.workspace_root):
            raise PermissionError(
                f"Access Denied: Path '{user_provided_path}' escapes workspace boundary "
                f"'{self.workspace_root}'"
            )
            
        return target_path

    def safe_read(self, path: str) -> str:
        verified = self.verify_path(path)
        if not verified.exists():
            raise FileNotFoundError(f"File not found: {path}")
        with open(verified, 'r', encoding='utf-8') as f:
            return f.read()

    def safe_write(self, path: str, content: str) -> None:
        verified = self.verify_path(path)
        # Create directories if they do not exist
        verified.parent.mkdir(parents=True, exist_ok=True)
        with open(verified, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    # Define a mock workspace directory
    mock_workspace = Path("./mock_sandbox").resolve()
    mock_workspace.mkdir(exist_ok=True)
    
    guard = PathPermissionGuard(mock_workspace)
    
    # 1. Valid Write
    try:
        guard.safe_write("src/utils.py", "print('hello')")
        print("✓ Valid write succeeded")
    except Exception as e:
        print("✗ Write failed:", e)
        
    # 2. Path Traversal Attempt (escapes sandbox root)
    try:
        print("\nAttempting file read on '../../etc/passwd'...")
        guard.safe_read("../../etc/passwd")
    except PermissionError as e:
        print("✓ Guard successfully caught path traversal:", e)
    except Exception as e:
        print("Unexpected error type:", e)
        
    # Cleanup
    if (mock_workspace / "src/utils.py").exists():
        (mock_workspace / "src/utils.py").unlink()
        (mock_workspace / "src").rmdir()
    mock_workspace.rmdir()
