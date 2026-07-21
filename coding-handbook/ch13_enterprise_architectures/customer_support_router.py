"""
Chapter 13: Autonomous Customer Service Query Routing Pipeline
===============================================================
Production enterprise architecture that intercepts support requests, classifies intent,
executes sandboxed SQL queries, evaluates query results, and compiles responses.

From: The Practitioner's Handbook of Agentic AI, Chapter 13.1
"""

import sqlite3
import json
import re
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class SupportTicket:
    ticket_id: str
    user_id: str
    raw_email: str


@dataclass
class RoutingDecision:
    intent: str  # "ORDER_LOOKUP", "KNOWLEDGE_BASE", "ESCALATE"
    confidence: float
    reasoning: str


class CustomerSupportRouter:
    """
    Enterprise Support Router routing tickets between Sandboxed SQL Execution
    and RAG Knowledge Base Retrieval.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._setup_mock_db()

    def _setup_mock_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE orders (
                    order_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    status TEXT,
                    item_name TEXT,
                    shipping_date TEXT
                );
            """)
            self.conn.execute("""
                INSERT INTO orders VALUES 
                ('ORD-9021', 'USR-101', 'SHIPPED', 'Agentic AI Book (Hardcover)', '2026-07-20'),
                ('ORD-9022', 'USR-102', 'PROCESSING', 'Mechanical Keyboard', 'Pending');
            """)

    def classify_intent(self, ticket: SupportTicket) -> RoutingDecision:
        """Rule/LLM classifier for user support tickets."""
        text = ticket.raw_email.lower()
        if any(w in text for w in ["order", "status", "package", "tracking", "ord-"]):
            return RoutingDecision("ORDER_LOOKUP", 0.95, "Matches order query keywords.")
        elif any(w in text for w in ["refund", "return", "policy", "how to"]):
            return RoutingDecision("KNOWLEDGE_BASE", 0.90, "Matches policy query keywords.")
        return RoutingDecision("ESCALATE", 0.70, "Ambiguous request requires human agent.")

    def execute_sandboxed_sql(self, ticket: SupportTicket) -> Optional[Dict[str, Any]]:
        """Sandboxed SQL query generator and executor for order lookup."""
        order_match = re.search(r"ord-\d+", ticket.raw_email, re.IGNORECASE)
        if not order_match:
            return None
        
        order_id = order_match.group(0).upper()
        cur = self.conn.cursor()
        # Parameterized query to prevent SQL injection vulnerabilities
        cur.execute("SELECT order_id, user_id, status, item_name, shipping_date FROM orders WHERE order_id = ?", (order_id,))
        row = cur.fetchone()
        if row:
            return {
                "order_id": row[0],
                "user_id": row[1],
                "status": row[2],
                "item_name": row[3],
                "shipping_date": row[4]
            }
        return None

    def handle_ticket(self, ticket: SupportTicket) -> Dict[str, Any]:
        """Main routing pipeline execution."""
        decision = self.classify_intent(ticket)
        
        if decision.intent == "ORDER_LOOKUP":
            order_data = self.execute_sandboxed_sql(ticket)
            if order_data:
                response = (
                    f"Hello! Your order {order_data['order_id']} for '{order_data['item_name']}' "
                    f"is currently {order_data['status']}. Shipping date: {order_data['shipping_date']}."
                )
            else:
                response = "Hello! We could not locate the specified order ID in our system."
        elif decision.intent == "KNOWLEDGE_BASE":
            response = "Hello! Returns are accepted within 30 days of delivery with original packaging."
        else:
            response = "Your query has been escalated to a customer support specialist."

        return {
            "ticket_id": ticket.ticket_id,
            "routing_decision": decision.intent,
            "confidence": decision.confidence,
            "response": response
        }


if __name__ == "__main__":
    router = CustomerSupportRouter()
    ticket1 = SupportTicket("T-1", "USR-101", "Where is my package for order ORD-9021?")
    res1 = router.handle_ticket(ticket1)
    print("Ticket 1 Result:", json.dumps(res1, indent=2))
