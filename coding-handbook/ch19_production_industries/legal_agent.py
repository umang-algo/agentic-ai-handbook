"""
Chapter 19: Industry 3 — Legal Contract Analysis & Redlining Agent
===================================================================
Production legal AI agent performing contract taxonomy extraction,
risk scoring, precedent clause matching, and automated redlining.

From: The Practitioner's Handbook of Agentic AI, Chapter 19.3
"""

import json
from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class ContractClause:
    clause_id: str
    category: str  # "INDEMNIFICATION", "TERMINATION", "GOVERNING_LAW"
    text: str
    risk_score: float  # 0.0 (Low) to 1.0 (High Risk)


@dataclass
class RedlineSuggestion:
    clause_id: str
    original_text: str
    suggested_text: str
    rationale: str


class LegalContractAgent:
    """Legal Contract Review & Redlining Agent enforcing company standard playbook policies."""
    def __init__(self):
        self.playbook_rules = {
            "INDEMNIFICATION": "Cap indemnification liability at 2x annual contract value.",
            "GOVERNING_LAW": "Must specify Delaware or California state jurisdiction."
        }

    def analyze_clause(self, clause: ContractClause) -> RedlineSuggestion:
        """Evaluates clause against playbook rules and generates redline recommendations."""
        category = clause.category.upper()
        
        if category == "INDEMNIFICATION" and "unlimited" in clause.text.lower():
            return RedlineSuggestion(
                clause_id=clause.clause_id,
                original_text=clause.text,
                suggested_text="Supplier's aggregate liability under this section shall not exceed 2x the annual fees paid.",
                rationale="Unlimited indemnification violates corporate risk policy."
            )
        elif category == "GOVERNING_LAW" and not any(loc in clause.text for loc in ["Delaware", "California"]):
            return RedlineSuggestion(
                clause_id=clause.clause_id,
                original_text=clause.text,
                suggested_text="This Agreement shall be governed by and construed under the laws of the State of Delaware.",
                rationale="Non-standard governing law jurisdiction requires alignment with legal playbook."
            )

        return RedlineSuggestion(
            clause_id=clause.clause_id,
            original_text=clause.text,
            suggested_text=clause.text,
            rationale="Clause satisfies company legal playbook guidelines."
        )

    def review_contract(self, clauses: List[ContractClause]) -> Dict[str, Any]:
        """Reviews full contract and compiles risk assessment & redlines."""
        redlines = [self.analyze_clause(c) for c in clauses]
        avg_risk = sum(c.risk_score for c in clauses) / len(clauses) if clauses else 0.0

        return {
            "total_clauses": len(clauses),
            "average_risk_score": round(avg_risk, 2),
            "high_risk_flag": avg_risk > 0.60,
            "redline_suggestions": [
                {
                    "clause_id": r.clause_id,
                    "original": r.original_text,
                    "suggested": r.suggested_text,
                    "rationale": r.rationale
                } for r in redlines if r.original_text != r.suggested_text
            ]
        }


if __name__ == "__main__":
    agent = LegalContractAgent()
    sample_clauses = [
        ContractClause("C-1", "INDEMNIFICATION", "Vendor provides unlimited indemnification for all claims.", 0.95),
        ContractClause("C-2", "GOVERNING_LAW", "This contract shall be governed by the laws of England and Wales.", 0.65),
    ]

    report = agent.review_contract(sample_clauses)
    print("Legal Contract Review Report:")
    print(json.dumps(report, indent=2))
