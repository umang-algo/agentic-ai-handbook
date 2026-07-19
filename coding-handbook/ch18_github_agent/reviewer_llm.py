"""
LLM Code Reviewer Agent

Compiles findings from static bug analysis and prompts the model to generate
structured code review comments for pull requests.
"""

from typing import List, Dict

class CodeReviewerAgent:
    @staticmethod
    def compile_review_prompt(pr_metadata: dict, codebase_chunks: List[dict]) -> str:
        """Assembles review system prompt context."""
        prompt = (
            f"Review PR #{pr_metadata['id']}: '{pr_metadata['title']}' in repo '{pr_metadata['repo']}'.\n"
            f"Please analyze these codebase modification blocks:\n"
        )
        for chunk in codebase_chunks:
            prompt += f"- File: {chunk.get('file')} | Line {chunk.get('line')}: {chunk.get('content')}\n"
        prompt += "\nOutput your review comments in markdown format."
        return prompt

if __name__ == "__main__":
    metadata = {"id": 101, "title": "Add JWT verifying class", "repo": "user/api"}
    chunks = [
        {"file": "auth.py", "line": 24, "content": "except Exception: pass"}
    ]
    
    review_prompt = CodeReviewerAgent.compile_review_prompt(metadata, chunks)
    print("Compiled Reviewer System Prompt:")
    print(review_prompt)
