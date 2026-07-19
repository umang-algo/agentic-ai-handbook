"""
Model Cost Router

Demonstrates routing user prompts dynamically: sending low-complexity tasks to cheap,
fast models (e.g. GPT-4o-mini) and high-complexity reasoning tasks to expensive models (e.g. Claude 3.5 Sonnet / o1).
"""

class ModelRouter:
    def __init__(self, cheap_model: str = "gpt-4o-mini", premium_model: str = "claude-3-5-sonnet"):
        self.cheap_model = cheap_model
        self.premium_model = premium_model

    def route_query(self, prompt: str) -> str:
        """
        Determines target model based on prompt complexity features.
        In production, this might use classification, regex, or length metrics.
        """
        # Complex programming, reasoning, math, and system design indicators
        complexity_keywords = ["implement", "optimize", "refactor", "bug", "write tests", "mathematics", "prove"]
        
        # Determine model
        for word in complexity_keywords:
            if word in prompt.lower():
                print(f"[Router]: Detected keyword '{word}' -> Routing to Premium Model: {self.premium_model}")
                return self.premium_model
                
        print(f"[Router]: Simpler prompt -> Routing to Cheap Model: {self.cheap_model}")
        return self.cheap_model

if __name__ == "__main__":
    router = ModelRouter()
    
    # Simple query
    router.route_query("What is the capital of Spain?")
    
    # Complex programming query
    router.route_query("Optimize this SQL query by creating an AST parser and analyzing dependencies.")
