"""
Production AI Cost & ROI Calculator

Demonstrates calculating token savings, prompt caching hits, and comparing
operational costs between direct API models and routed pipelines.
"""

class ROICalculator:
    def __init__(self, cost_per_input_million: float = 3.0, cost_per_output_million: float = 15.0):
        self.cost_per_input_million = cost_per_input_million
        self.cost_per_output_million = cost_per_output_million

    def calculate_cost(self, input_tokens: int, output_tokens: int, cached_input_tokens: int = 0) -> float:
        """Computes cost in USD, applying 50% discount on cached input prefix tokens."""
        non_cached_input = input_tokens - cached_input_tokens
        
        input_cost = (non_cached_input / 1000000.0) * self.cost_per_input_million
        cached_cost = (cached_input_tokens / 1000000.0) * (self.cost_per_input_million * 0.5)
        output_cost = (output_tokens / 1000000.0) * self.cost_per_output_million
        
        return input_cost + cached_cost + output_cost

if __name__ == "__main__":
    calc = ROICalculator(cost_per_input_million=3.0, cost_per_output_million=15.0) # E.g., Claude 3.5 pricing
    
    # 1. Standard execution without prompt cache
    cost_raw = calc.calculate_cost(input_tokens=1000000, output_tokens=200000)
    print(f"Cost without cache: ${cost_raw:.2f}")
    
    # 2. Execution with 80% prompt cache hit
    cost_cached = calc.calculate_cost(input_tokens=1000000, output_tokens=200000, cached_input_tokens=800000)
    print(f"Cost with 80% prompt cache: ${cost_cached:.2f}")
    print(f"Savings: {((cost_raw - cost_cached)/cost_raw)*100:.1f}%")
