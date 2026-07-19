"""
Synthetic Dialogue Dataset Generator

Demonstrates programmatically creating fine-tuning datasets by modifying prompts
and templates using standard user-assistant templates.
"""

import json
from typing import List, Dict

class SyntheticDataGenerator:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def generate_instruction_pair(self, user_query: str, target_sql: str) -> Dict[str, List[Dict[str, str]]]:
        """Formats a standard ChatML sequence for fine-tuning inputs."""
        return {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": f"```sql\n{target_sql}\n```"}
            ]
        }

if __name__ == "__main__":
    generator = SyntheticDataGenerator(
        system_prompt="You are a SQL database agent. Always respond with raw SQL code inside code blocks."
    )
    
    # Generate mock training samples
    sample_1 = generator.generate_instruction_pair(
        user_query="Fetch users older than 21",
        target_sql="SELECT * FROM users WHERE age > 21;"
    )
    
    sample_2 = generator.generate_instruction_pair(
        user_query="Find products in stock",
        target_sql="SELECT name FROM products WHERE stock_count > 0;"
    )
    
    print("Example Synthetic Training Token Sequence:")
    print(json.dumps(sample_1, indent=2))
