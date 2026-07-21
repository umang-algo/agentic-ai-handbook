# Chapter 11: The Architecture of Modern AI IDEs (Cursor, Claude Code, Canvas)

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch11_ai_ides](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch11_ai_ides)

AI coding platforms like Cursor, Claude Code, and ChatGPT Canvas differ from standard code generation APIs. They do not simply write code blocks on demand; they run continuous, background-driven coordination loops that monitor the workspace state, run AST indices, and apply edits directly to active file buffers.

## The AI IDE Execution Loop

When you ask Claude Code to "fix all linter warnings in this workspace," the client initiates a background execution loop:

    - **Workspace Observation:** The agent scans modified buffers, diagnostics (warnings, errors), and active terminal states.
    - **Action Selection:** The model chooses to read a file, run a bash command, or search for definitions via an LSP (Language Server Protocol) server.
    - **Self-Correction Gate:** If the compilation fails, the compiler errors are fed back into the context window, allowing the agent to self-heal.


## Line diffing: The Myers Diff Algorithm

If an agent wants to edit a 5,000-line codebase file, sending the entire file back and forth is cost-prohibitive and slow. Instead, the model outputs a search-and-replace block, and the IDE computes a line diff to apply the changes.

The standard diff engine is powered by the **Myers Diff Algorithm**, which resolves the Shortest Edit Script (SES) to transform sequence $A$ (length $N$) into sequence $B$ (length $M$) using $O(ND)$ time complexity, where $D$ is the edit distance.

### The Grid Search Graph
Myers Diff models the edit path as a search on a 2D grid:

    - A move to the right (x-axis) represents a **deletion** from sequence $A$.
    - A move down (y-axis) represents an **insertion** from sequence $B$.
    - A diagonal move represents a **match** between $A$ and $B$, which consumes no edit cost.


The algorithm searches for the path from $(0,0)$ to $(N,M)$ that minimizes the number of horizontal and vertical steps.


*Architecture diagram visualizable in the companion handbook implementation.*


## AST Diff Syntax Verification Pipeline

When the LLM outputs a diff patch, applying it blindly can corrupt active workspace files. Production engines execute an **AST Verification Pipeline** on code buffers in memory before saving them to disk.





If the AST validation returns `False`, the write is blocked, and the compiler diagnostic is fed back to the LLM to trigger a repair cycle.

### Python Implementation of Myers Diff
This algorithm uses a list $V$ where index $k = x - y$ tracks the furthest reaching path on diagonal $k$.
