"""
Direct Preference Optimization (DPO) Dataset Builder

Demonstrates building preference dataset pairs (prompt, chosen response, rejected response)
used to align agent behaviors (such as structured tool-calling format compliance).
"""

import json
from typing import Dict, List

class DPODatasetBuilder:
    def __init__(self):
        self.samples: List[Dict[str, str]] = []

    def add_preference_sample(self, prompt: str, chosen: str, rejected: str) -> None:
        """Adds a chosen/rejected preference pair."""
        self.samples.append({
            "prompt": prompt,
            "chosen": chosen,
            "rejected": rejected
        })

    def save_to_jsonl(self, filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as f:
            for sample in self.samples:
                f.write(json.dumps(sample) + "\n")
        print(f"[DPO Builder]: Saved {len(self.samples)} samples to '{filepath}'")

if __name__ == "__main__":
    builder = DPODatasetBuilder()
    
    # Sample 1: Force JSON instead of conversational text
    builder.add_preference_sample(
        prompt="Call tool read_file for path 'src/main.py'",
        chosen='{"name": "read_file", "arguments": {"path": "src/main.py"}}',
        rejected="Sure, I'll help you call that. read_file(path='src/main.py')"
    )
    
    # Save the synthetic preference dataset
    builder.save_to_jsonl("./dpo_dataset.jsonl")
    
    # Cleanup
    import os
    if os.path.exists("./dpo_dataset.jsonl"):
        os.remove("./dpo_dataset.jsonl")
