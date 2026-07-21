# Part IV: Sandboxing and Environments

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch08_code_interpreter](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch08_code_interpreter)
# Chapter 8: The Code Interpreter (MicroVMs & Firecracker)

Allowing an LLM to execute arbitrary Python code is fundamentally dangerous. Standard Docker containers are inadequate because they share the underlying Linux kernel with the host. A kernel exploit from AI-generated code could compromise the entire server rack.

To safely execute Agentic workflows at scale, companies use **MicroVMs** via **AWS Firecracker**.

## 8.1 The Firecracker Architecture

Firecracker provides KVM-based virtualization. Each Agent session gets its own dedicated Linux virtual machine that boots in ~125 milliseconds.

```mermaid
graph TD
    subgraph Host OS (Bare Metal Server)
        A[KVM /dev/kvm]
        
        subgraph MicroVM Process (Agent Session)
            B[Firecracker VMM]
            C[Guest Kernel]
            D[Python Interpreter executing AI Code]
            
            C --> D
            B --> C
        end
        
        A --> B
        
        E[Jailer] -.->|Chroot & Cgroup limits| B
        
        F[TAP Device] -->|Network Isolation| B
        G[Virtio Socket (AF_VSOCK)] -->|IPC| B
    end
```

### Key Security Components:
1. **The Jailer:** Firecracker processes are wrapped in a "jailer" that uses Linux `cgroups` and `namespaces` to enforce strict memory and CPU quotas (e.g., hard-capped at 512MB RAM).
2. **Virtio Sockets (`AF_VSOCK`):** The orchestrator (Host) communicates with the Python interpreter (Guest) via virtio sockets, entirely bypassing traditional network stacks for maximum security.
3. **No Network Tap:** By default, the `TAP Device` is unconfigured. The Python code cannot ping the internet, download packages, or execute curl requests, guaranteeing data exfiltration is impossible.

## 8.2 The Execution Loop over VSOCK

When the LLM outputs a tool call requesting to run code, the Orchestrator sends the code into the VM.

```python
import socket
import json

def execute_code_in_microvm(cid, port, code_string):
    """
    Sends code to a Firecracker MicroVM via Virtio Sockets (AF_VSOCK).
    Requires a Linux host with vsock kernel module enabled.
    """
    # Create a VSOCK socket (Address Family 40)
    s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    
    # Connect to the Guest VM's Context ID (CID) and listening port
    s.connect((cid, port))
    
    # Send payload
    payload = json.dumps({"command": "run_python", "code": code_string})
    s.sendall(payload.encode('utf-8'))
    
    # Wait for the Execution Result (stdout/stderr)
    response_data = s.recv(4096)
    s.close()
    
    return json.loads(response_data.decode('utf-8'))

# Example Usage
ai_code = "print('Hello from inside the secure MicroVM!')"
# result = execute_code_in_microvm(cid=3, port=8000, code_string=ai_code)
# print(result['stdout'])
```

By leveraging Firecracker, you can safely scale an Agentic platform to millions of users, spinning up and tearing down full Linux operating systems for every single tool call in milliseconds.
