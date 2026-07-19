"""
Multimodal Vision Agent: Coordinate-based "Computer Use"

Demonstrates coordinate-based visual action spaces. Simulates screenshot-grounded click
and type tools used by visual web agents (like Claude Computer Use or OSWorld).
"""

from typing import Tuple, Dict

class MultimodalComputerUseAgent:
    def __init__(self, screen_resolution: Tuple[int, int] = (1920, 1080)):
        self.width, self.height = screen_resolution

    def parse_coordinate_from_box(self, normalized_bbox: Tuple[float, float, float, float]) -> Tuple[int, int]:
        """
        Translates a normalized bounding box [ymin, xmin, ymax, xmax] from a vision model
        (ranges 0-1000) to absolute screen coordinates (pixels).
        """
        ymin, xmin, ymax, xmax = normalized_bbox
        
        # Center of bounding box
        center_x_norm = (xmin + xmax) / 2.0
        center_y_norm = (ymin + ymax) / 2.0
        
        # Convert to pixels
        pixel_x = int((center_x_norm / 1000.0) * self.width)
        pixel_y = int((center_y_norm / 1000.0) * self.height)
        
        return pixel_x, pixel_y

    def click_coordinate(self, x: int, y: int) -> str:
        """Simulates physical mouse click action."""
        if not (0 <= x <= self.width) or not (0 <= y <= self.height):
            raise ValueError(f"Click coordinates ({x}, {y}) out of screen boundaries.")
        print(f"[OS Controller]: Mouse moved to ({x}, {y}) -> Click simulated.")
        return f"Clicked successfully at absolute position ({x}, {y})."

    def type_text(self, text: str) -> str:
        """Simulates physical keyboard key entry."""
        print(f"[OS Controller]: Keystroke event triggered -> Typing '{text}'")
        return f"Successfully typed text: '{text}'"

if __name__ == "__main__":
    agent = MultimodalComputerUseAgent(screen_resolution=(1920, 1080))
    
    # Simulating a vision model identifying a Submit Button box
    # Normalized bbox ranges 0-1000: [ymin, xmin, ymax, xmax]
    # Representing a button around the center of the screen
    button_bbox = (490.0, 480.0, 510.0, 520.0)
    
    print("Screen Resolution: 1920x1080")
    print(f"Detected Button Bounding Box (Normalized): {button_bbox}")
    
    # Calculate coordinate
    click_x, click_y = agent.parse_coordinate_from_box(button_bbox)
    print(f"Calculated Target Center Coordinate (Pixels): ({click_x}, {click_y})")
    
    # Execute actions
    click_res = agent.click_coordinate(click_x, click_y)
    type_res = agent.type_text("Umang")
    
    print("\nAction Status Outputs:")
    print(click_res)
    print(type_res)
