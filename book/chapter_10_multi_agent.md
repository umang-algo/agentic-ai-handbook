# Chapter 10: Multi-Agent State Machines (DAGs & Checkpointing)

> 📝 **Coding Handbook**: Practice the code from this chapter → [`coding-handbook/ch10_multi_agent`](../coding-handbook/ch10_multi_agent/)

When a workflow requires multiple specialized LLM calls (e.g., Coder -> Reviewer -> Tester -> Deployer), wrapping them in a simple Python `while` loop (as seen in Chapter 3) becomes impossible to debug. The state becomes entangled, and failure recovery is nonexistent.

Production systems use **Directed Acyclic Graphs (DAGs)** to manage Multi-Agent state. 

## 10.1 The DAG Architecture (LangGraph)

A DAG ensures that data flows in specific directions and defines rigid boundaries for what each Agent is allowed to access and mutate.

```mermaid
graph TD
    A([Start State]) --> B[Router Node (LLM)]
    
    B -->|Intent: Write Code| C[Coder Agent]
    B -->|Intent: Write Tests| D[Tester Agent]
    
    C --> E[Reviewer Agent]
    E -->|Pass| F[Deploy Agent]
    E -->|Fail| C
    
    D --> E
    
    F --> G([End State])
```

## 10.2 Memory Checkpointing (Postgres)

The true power of a State Machine is the ability to pause, inspect, and resume an agent workflow. This is known as **Checkpointing**, and it is crucial for "Human-in-the-loop" approval gates.

To achieve this, the global state of the workflow must be serialized to a database (like PostgreSQL) after every node execution.

### Code: Abstract State Checkpointing Architecture

```python
import json
import psycopg2

class AgentStateMachine:
    def __init__(self, db_connection_string):
        self.conn = psycopg2.connect(db_connection_string)
        self._init_db()

    def _init_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS workflow_checkpoints (
                    thread_id VARCHAR PRIMARY KEY,
                    current_node VARCHAR,
                    global_state JSONB
                )
            """)
        self.conn.commit()

    def save_checkpoint(self, thread_id, current_node, global_state):
        """Serializes the exact state of the Multi-Agent workflow to Postgres."""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO workflow_checkpoints (thread_id, current_node, global_state)
                VALUES (%s, %s, %s)
                ON CONFLICT (thread_id) DO UPDATE 
                SET current_node = EXCLUDED.current_node,
                    global_state = EXCLUDED.global_state
            """, (thread_id, current_node, json.dumps(global_state)))
        self.conn.commit()

    def resume_workflow(self, thread_id):
        """Fetches the state from Postgres and resumes execution from the exact stopped node."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT current_node, global_state FROM workflow_checkpoints WHERE thread_id = %s", (thread_id,))
            record = cur.fetchone()
            
        if not record:
            return "No checkpoint found."
            
        current_node, state_json = record
        global_state = state_json
        
        print(f"Resuming workflow from node: {current_node}")
        # Transition logic based on current_node goes here...
        return self._execute_node(current_node, global_state, thread_id)
        
    def _execute_node(self, node, state, thread_id):
        # Implementation of LLM nodes...
        pass
```

### The Human-in-the-Loop Gateway
By pausing the graph at the `Deploy Agent` node and saving the checkpoint to Postgres, a human engineer can open a web dashboard, review the `global_state["code"]`, click "Approve", and call `resume_workflow()`. 

The agent wakes back up with perfect context and completes the deployment.

This concludes the Definitive Guide to Agentic AI. You have transitioned from prompt engineering to rigorous systems architecture.
