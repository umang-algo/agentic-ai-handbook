"""
Chapter 13: Financial Market Aggregator Pipeline
================================================
Enterprise architecture compiling financial filings, calculating stock metrics,
generating chart representations, and compiling multi-page market summaries.

From: The Practitioner's Handbook of Agentic AI, Chapter 13.3
"""

import json
import math
from dataclasses import dataclass, asdict
from typing import Dict, Any, List


@dataclass
class StockFinancials:
    ticker: str
    company_name: str
    revenue_m: float
    net_income_m: float
    eps: float
    pe_ratio: float


@dataclass
class MarketReport:
    title: str
    timestamp: str
    company_analyses: List[StockFinancials]
    market_sentiment: str
    key_takeaways: List[str]


class FinancialMarketAggregator:
    """
    Financial Market Analysis Agent fetching quarterly SEC data,
    computing portfolio valuations, and compiling structured markdown/LaTeX summaries.
    """
    def __init__(self):
        self.market_database: Dict[str, StockFinancials] = {
            "AAPL": StockFinancials("AAPL", "Apple Inc.", 385700.0, 96990.0, 6.42, 32.5),
            "NVDA": StockFinancials("NVDA", "NVIDIA Corp.", 60920.0, 29760.0, 1.19, 68.4),
            "MSFT": StockFinancials("MSFT", "Microsoft Corp.", 245100.0, 88100.0, 11.80, 35.1),
        }

    def fetch_financial_metrics(self, ticker: str) -> StockFinancials:
        """Retrieves financial statistics for a specified ticker."""
        ticker = ticker.upper()
        if ticker in self.market_database:
            return self.market_database[ticker]
        raise ValueError(f"Ticker {ticker} not found in market feed database.")

    def compute_valuation_multiples(self, financials: StockFinancials) -> Dict[str, float]:
        """Calculates margin and valuation ratios."""
        net_margin = (financials.net_income_m / financials.revenue_m) * 100.0
        return {
            "net_margin_percent": round(net_margin, 2),
            "pe_ratio": financials.pe_ratio,
            "eps": financials.eps
        }

    def generate_report(self, tickers: List[str]) -> MarketReport:
        """Compiles multi-ticker financial summary report."""
        analyses = []
        takeaways = []
        for t in tickers:
            fin = self.fetch_financial_metrics(t)
            mult = self.compute_valuation_multiples(fin)
            analyses.append(fin)
            takeaways.append(
                f"{fin.ticker} ({fin.company_name}): Net Margin of {mult['net_margin_percent']}%, P/E {mult['pe_ratio']}."
            )

        return MarketReport(
            title="Q3 Enterprise AI & Semiconductor Market Aggregator Report",
            timestamp="2026-07-21",
            company_analyses=analyses,
            market_sentiment="BULLISH",
            key_takeaways=takeaways
        )


if __name__ == "__main__":
    aggregator = FinancialMarketAggregator()
    report = aggregator.generate_report(["AAPL", "NVDA", "MSFT"])
    print("Compiled Financial Report:")
    print(f"Title: {report.title}")
    print(f"Sentiment: {report.market_sentiment}")
    print("Takeaways:")
    for t in report.key_takeaways:
        print(f" - {t}")
