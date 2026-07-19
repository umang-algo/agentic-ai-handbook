"""
LoRA Fine-Tuning Setup Configuration

Demonstrates configuring target modules and rank parameters for parameter-efficient
fine-tuning (PEFT/LoRA) using standard training wrapper abstractions.
"""

from typing import List

class LoRATrainingConfig:
    def __init__(self, r: int = 8, lora_alpha: int = 16, target_modules: List[str] = None):
        self.r = r
        self.lora_alpha = lora_alpha
        self.target_modules = target_modules or ["q_proj", "v_proj"]
        self.scaling = lora_alpha / r

    def get_peft_parameters(self) -> dict:
        """Returns standard configuration dictionary for huggingface peft library."""
        return {
            "r": self.r,
            "lora_alpha": self.lora_alpha,
            "target_modules": self.target_modules,
            "lora_dropout": 0.05,
            "bias": "none",
            "task_type": "CAUSAL_LM"
        }

if __name__ == "__main__":
    config = LoRATrainingConfig(r=16, lora_alpha=32, target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    peft_args = config.get_peft_parameters()
    
    print("PEFT/LoRA Configuration Parameters:")
    for k, v in peft_args.items():
        print(f"  {k}: {v}")
    print(f"\nCalculated LoRA Scaling factor: {config.scaling}")
