# Chapter 7: Context Assembly (Token Budgeting & Speculative Decoding)

> 📝 **Coding Handbook**: Practice the code from this chapter → [GitHub: ch07_context_assembly](https://github.com/umang/agentic-ai-handbook/tree/main/coding-handbook/ch07_context_assembly)

Cursor is widely considered the best AI IDE in the world. Its secret is not a magical foundational model (it uses the same Claude 3.5 Sonnet available to everyone). Its secret is the **Orchestrator Backend**, which dynamically assembles a context window optimized to the exact token limit.

## 7.1 The Cursor Backend Architecture

```mermaid
graph TD
    subgraph Client (VS Code Fork)
        A[Active File Editor]
        B[Diagnostics/Linter]
        C[Recent Terminal Output]
    end

    subgraph Orchestrator (Backend)
        D[Token Budget Allocator]
        E[RAG Engine / Vector Search]
        F[Prompt Compiler]
    end

    subgraph Inference (LLM)
        G[Claude 3.5 / GPT-4o]
    end

    A --> D
    B --> D
    C --> D
    E --> D
    
    D -->|Prunes excess tokens| F
    F -->|System Prompt + XML Context| G
```

## 7.2 The Token Budget Allocator

LLMs have hard context limits (e.g., 200,000 tokens for Claude). If the Orchestrator gathers 250,000 tokens of related code, the API call will be rejected.

The Orchestrator runs a strict **Token Budgeting Algorithm**.

```python
import tiktoken

def allocate_token_budget(active_file, linter_errors, rag_results, max_tokens=150000):
    """
    Allocates tokens based on strict priority.
    """
    encoder = tiktoken.get_encoding("cl100k_base")
    budget_remaining = max_tokens
    
    final_context = ""
    
    # Priority 1: System Rules & Linter Errors (MUST FIT)
    system_rules = "You are a coding assistant. Fix the following linter errors:\n" + str(linter_errors)
    sys_tokens = len(encoder.encode(system_rules))
    budget_remaining -= sys_tokens
    final_context += system_rules
    
    # Priority 2: Active File (MUST FIT, OR TRUNCATE)
    file_tokens = len(encoder.encode(active_file))
    if file_tokens < budget_remaining:
        final_context += "\n<active_file>\n" + active_file + "\n</active_file>"
        budget_remaining -= file_tokens
    else:
        # Emergency: File is too big. Extract only the lines around the cursor.
        return fallback_cursor_radius_extraction(active_file, budget_remaining)
        
    # Priority 3: RAG Results (FILL REMAINING BUDGET)
    final_context += "\n<related_context>\n"
    for result in rag_results:
        result_tokens = len(encoder.encode(result['text']))
        if budget_remaining - result_tokens > 0:
            final_context += result['text'] + "\n---\n"
            budget_remaining -= result_tokens
        else:
            break # Budget exhausted, drop remaining RAG context
            
    final_context += "</related_context>"
    return final_context
```

## 7.3 Speculative Decoding (Fast Diffs)

When an agent generates a multi-file edit, the user is watching the UI. If the LLM generates 1000 lines of code at 20 tokens/second, the user waits 50 seconds.

Advanced editors use **Speculative Decoding**. 
Because 90% of a code edit involves rewriting identical lines of code, a smaller, faster "draft" model (e.g., a 7B parameter model) guesses the next 10 tokens instantly. The large model (Claude 3.5) then verifies all 10 tokens in a single forward pass. 

If they match, 10 tokens are generated in the time it usually takes to generate 1. This is how Cursor's Composer achieves "instantaneous" streaming speeds.
