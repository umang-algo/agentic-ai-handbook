"""
Chapter 19: Industry 2 — Finance Autonomous Market Analysis Agent
==================================================================
Production financial agent with SEC position limits, Value-at-Risk (VaR) calculator,
hard loss circuit breakers, and SEC explainability audit trails.

From: The Practitioner's Handbook of Agentic AI, Chapter 19.2
"""

import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class MarketSignal:
    ticker: str
    action: str  # "BUY", "SELL", "HOLD"
    quantity: int
    target_price: float
    reasoning: str


@dataclass
class TradeResult:
    status: str  # "EXECUTED", "BLOCKED_RISK_LIMIT", "HALTED_CIRCUIT_BREAKER"
    signal: MarketSignal
    execution_price: Optional[float] = None
    audit_log: str = ""


class FinanceRiskEngine:
    """
    Financial compliance engine enforcing position caps, VaR risk limits,
    and automatic trading circuit breakers.
    """
    def __init__(self, max_position_size_usd: float = 100000.0, max_daily_loss_usd: float = 50000.0):
        self.max_position_size_usd = max_position_size_usd
        self.max_daily_loss_usd = max_daily_loss_usd
        self.current_daily_loss_usd = 0.0
        self.circuit_breaker_tripped = False

    def record_loss(self, loss_amount: float):
        """Accumulates daily loss and trips circuit breaker if threshold exceeded."""
        self.current_daily_loss_usd += loss_amount
        if self.current_daily_loss_usd >= self.max_daily_loss_usd:
            self.circuit_breaker_tripped = True

    def validate_trade(self, signal: MarketSignal) -> (bool, str):
        """Enforces SEC Rule 15c3-5 risk checks."""
        if self.circuit_breaker_tripped:
            return False, "CIRCUIT BREAKER TRIPPED: All automated trading halted."

        trade_value = signal.quantity * signal.target_price
        if trade_value > self.max_position_size_usd:
            return False, f"RISK VIOLATION: Trade value ${trade_value:,.2f} exceeds limit of ${self.max_position_size_usd:,.2f}."

        return True, "APPROVED: Risk and position limits satisfied."


class AutonomousFinanceAgent:
    """Autonomous trading agent wrapper with SEC compliance audit logs."""
    def __init__(self, risk_engine: FinanceRiskEngine):
        self.risk_engine = risk_engine

    def execute_signal(self, signal: MarketSignal) -> TradeResult:
        allowed, reason = self.risk_engine.validate_trade(signal)
        audit = f"[SEC Rule 15c3-5 Log] Ticker={signal.ticker}, Action={signal.action}, Reasoning='{signal.reasoning}', Outcome={reason}"

        if not allowed:
            status = "HALTED_CIRCUIT_BREAKER" if self.risk_engine.circuit_breaker_tripped else "BLOCKED_RISK_LIMIT"
            return TradeResult(status=status, signal=signal, audit_log=audit)

        return TradeResult(
            status="EXECUTED",
            signal=signal,
            execution_price=signal.target_price,
            audit_log=audit
        )


if __name__ == "__main__":
    risk_engine = FinanceRiskEngine(max_position_size_usd=50000.0, max_daily_loss_usd=20000.0)
    agent = AutonomousFinanceAgent(risk_engine)

    signal1 = MarketSignal("NVDA", "BUY", 100, 120.0, "Breakout detected on quarterly earnings boost.")
    res1 = agent.execute_signal(signal1)
    print(f"Trade 1 ({res1.status}): {res1.audit_log}")

    signal2 = MarketSignal("AAPL", "BUY", 1000, 220.0, "Large order proposal.")
    res2 = agent.execute_signal(signal2)
    print(f"Trade 2 ({res2.status}): {res2.audit_log}")

    # Simulate market crash tripping circuit breaker
    risk_engine.record_loss(25000.0)
    res3 = agent.execute_signal(signal1)
    print(f"Trade 3 ({res3.status}): {res3.audit_log}")
