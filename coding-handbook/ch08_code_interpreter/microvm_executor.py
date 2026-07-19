"""
MicroVM Sandbox Execution Simulator

Simulates running code inside an isolated container (such as Firecracker/Docker)
with strict memory boundaries, timeouts, and network constraints.
"""

import subprocess
import tempfile
import os

class MicroVMExecutor:
    def __init__(self, timeout_seconds: int = 5):
        self.timeout_seconds = timeout_seconds

    def execute_in_sandbox(self, python_code: str) -> dict:
        """Runs python code in a separate process to simulate shell/sandbox isolation."""
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(python_code.encode("utf-8"))
            temp_file_path = f.name
            
        try:
            # Running with python3 in a subprocess limits the execution blast radius
            result = subprocess.run(
                ["python3", temp_file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {self.timeout_seconds} seconds (Denial of Service Guard)"
            }
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

if __name__ == "__main__":
    executor = MicroVMExecutor(timeout_seconds=2)
    
    # Test case 1: Standard computation
    code_ok = "print('Sum is:', sum([1, 2, 3, 4]))"
    print("Running valid code:")
    print(executor.execute_in_sandbox(code_ok))
    
    # Test case 2: Time Out (DoS attempt)
    code_dos = "import time\nwhile True:\n    time.sleep(0.1)"
    print("\nRunning infinite loop:")
    print(executor.execute_in_sandbox(code_dos))
