"""
Chapter 20: AI Harness Tools — Architectural Comparative Matrix
================================================================
Comparative benchmark framework analyzing Cursor, Claude Code, Aider, and Devin
across architectural dimensions: context efficiency, edit latency, permission model, and diff accuracy.

From: The Practitioner's Handbook of Agentic AI, Chapter 20.1
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List


@dataclass
class HarnessToolProfile:
    name: str
    paradigm: str  # "IDE-Integrated", "CLI-Native", "Cloud-Sandboxed"
    context_indexing: str
    diff_engine: str
    permission_model: str
    typical_latency_ms: int
    context_window_utilization: float  # 0.0 to 1.0


class HarnessToolEvaluator:
    """Evaluation framework comparing modern AI developer tools."""
    def __init__(self):
        self.tools: List[HarnessToolProfile] = [
            HarnessToolProfile(
                name="Cursor",
                paradigm="IDE-Integrated",
                context_indexing="AST Tree-Sitter + BM25 Lexical",
                diff_engine="Speculative Myers Diff",
                permission_model="Editor Buffer Staging Review",
                typical_latency_ms=120,
                context_window_utilization=0.65
            ),
            HarnessToolProfile(
                name="Claude Code",
                paradigm="CLI-Native",
                context_indexing="Extended Thinking + File Search",
                diff_engine="Line Patch Applicator",
                permission_model="Client-Side Terminal Prompts",
                typical_latency_ms=850,
                context_window_utilization=0.88
            ),
            HarnessToolProfile(
                name="Aider",
                paradigm="CLI-Native",
                context_indexing="Repository Map (Universal Ctags)",
                diff_engine="Git Commit Diff Streamer",
                permission_model="Automatic Local Git Commits",
                typical_latency_ms=300,
                context_window_utilization=0.45
            ),
            HarnessToolProfile(
                name="Devin",
                paradigm="Cloud-Sandboxed",
                context_indexing="Full Workspace Cloud MicroVM Index",
                diff_engine="MicroVM Sandbox Patch",
                permission_model="Isolated Cloud Sandbox",
                typical_latency_ms=2500,
                context_window_utilization=0.95
            ),
        ]

    def rank_by_latency(self) -> List[HarnessToolProfile]:
        """Ranks tools by response latency (fastest first)."""
        return sorted(self.tools, key=lambda t: t.typical_latency_ms)

    def rank_by_token_efficiency(self) -> List[HarnessToolProfile]:
        """Ranks tools by context window utilization efficiency (lowest token overhead first)."""
        return sorted(self.tools, key=lambda t: t.context_window_utilization)

    def generate_comparison_matrix(self) -> Dict[str, Any]:
        """Generates comprehensive architectural comparative matrix."""
        return {
            "total_tools_evaluated": len(self.tools),
            "fastest_latency_tool": self.rank_by_latency()[0].name,
            "most_compact_context_tool": self.rank_by_token_efficiency()[0].name,
            "tool_profiles": [asdict(t) for t in self.tools]
        }


if __name__ == "__main__":
    evaluator = HarnessToolEvaluator()
    matrix = evaluator.generate_comparison_matrix()

    print("AI Developer Harness Architectural Comparison:")
    print(f"Fastest Latency: {matrix['fastest_latency_tool']}")
    print(f"Most Compact Context: {matrix['most_compact_context_tool']}")
    print("\nDetailed Tool Breakdown:")
    for profile in matrix["tool_profiles"]:
        print(f" - {profile['name']} ({profile['paradigm']}): Indexing='{profile['context_indexing']}', Latency={profile['typical_latency_ms']}ms")
