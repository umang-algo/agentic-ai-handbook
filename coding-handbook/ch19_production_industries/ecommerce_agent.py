"""
Chapter 19: Industry 4 — E-Commerce Dynamic Pricing & Inventory Agent
======================================================================
Production e-commerce agent managing real-time price optimization, inventory monitoring,
and automated fraud detection gates for high-volume transactions.

From: The Practitioner's Handbook of Agentic AI, Chapter 19.4
"""

import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class ProductItem:
    sku: str
    name: str
    current_price: float
    unit_cost: float
    stock_qty: int
    competitor_price: float


@dataclass
class TransactionOrder:
    order_id: str
    user_id: str
    total_amount: float
    items: List[str]
    shipping_country: str
    ip_risk_score: float


class EcommerceAgent:
    """Dynamic pricing engine and fraud detection pipeline for e-commerce systems."""
    def __init__(self, min_margin_percent: float = 15.0):
        self.min_margin_percent = min_margin_percent

    def optimize_price(self, item: ProductItem) -> float:
        """Determines optimal selling price considering competitor pricing and minimum margin bounds."""
        min_allowed_price = item.unit_cost * (1.0 + (self.min_margin_percent / 100.0))
        target_price = item.competitor_price * 0.98  # Undercut competitor by 2%

        return max(target_price, min_allowed_price)

    def evaluate_fraud_risk(self, order: TransactionOrder) -> (bool, str):
        """Fraud detection gate evaluating transaction risk factors."""
        if order.ip_risk_score > 0.85:
            return True, "HIGH_RISK_IP: Proxy/VPN fraud signal detected."
        if order.total_amount > 5000.0 and order.shipping_country not in ["US", "CA", "GB", "DE"]:
            return True, "HIGH_RISK_GEO: Unverified high-value international transaction."
        return False, "CLEARED: Transaction passes fraud verification."

    def process_inventory_check(self, item: ProductItem, reorder_threshold: int = 10) -> Optional[int]:
        """Triggers automated inventory reorder recommendations when stock drops below threshold."""
        if item.stock_qty <= reorder_threshold:
            reorder_units = max(50, reorder_threshold * 5)
            return reorder_units
        return None


if __name__ == "__main__":
    agent = EcommerceAgent(min_margin_percent=20.0)

    item = ProductItem(
        sku="SKU-8812",
        name="Wireless Ergonomic Mouse",
        current_price=49.99,
        unit_cost=25.00,
        stock_qty=5,
        competitor_price=45.00
    )

    optimized_price = agent.optimize_price(item)
    reorder_amount = agent.process_inventory_check(item)

    print(f"Product: {item.name}")
    print(f"Optimized Price: ${optimized_price:.2f} (Competitor: ${item.competitor_price:.2f})")
    print(f"Reorder Triggered: {reorder_amount} units")

    order = TransactionOrder(
        order_id="ORD-771",
        user_id="USR-440",
        total_amount=1200.0,
        items=["SKU-8812"],
        shipping_country="US",
        ip_risk_score=0.92
    )

    is_fraud, msg = agent.evaluate_fraud_risk(order)
    print(f"Fraud Check Result: Is Fraud={is_fraud}, Rationale='{msg}'")
