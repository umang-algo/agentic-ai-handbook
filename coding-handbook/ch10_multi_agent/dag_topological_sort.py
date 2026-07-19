"""
Chapter 10: DAG Topological Sort for Multi-Agent Orchestration
===============================================================
Computes the execution order of agents in a DAG using Kahn's Algorithm.
Agents without dependencies run in parallel.

From: The Practitioner's Handbook of Agentic AI, Chapter 10.2
"""

from collections import deque


def resolve_execution_order(graph: dict) -> list:
    """
    Computes topological order of agent nodes.
    Graph representation: { 'node': ['dependency1', 'dependency2'] }
    Returns: ordered list of node names for sequential execution.
    """
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1

    queue = deque([u for u in graph if in_degree[u] == 0])
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(order) != len(graph):
        raise ValueError("Cycle detected in Agent Graph!")

    return order


def get_parallel_groups(graph: dict) -> list[list[str]]:
    """
    Groups agents into parallel execution tiers.
    Agents in the same tier have no dependencies on each other.
    """
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1

    groups = []
    remaining = set(graph.keys())

    while remaining:
        # Find all nodes with in-degree 0 among remaining
        tier = [u for u in remaining if in_degree.get(u, 0) == 0]
        if not tier:
            raise ValueError("Cycle detected!")
        groups.append(tier)
        for u in tier:
            remaining.discard(u)
            for v in graph.get(u, []):
                in_degree[v] -= 1

    return groups


if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Agent DAG Execution Order")
    print("=" * 60)

    # Define the agent dependency graph
    agent_graph = {
        "router":   ["coder", "tester"],
        "coder":    ["reviewer"],
        "tester":   ["reviewer"],
        "reviewer": ["deploy"],
        "deploy":   [],
    }

    order = resolve_execution_order(agent_graph)
    print(f"\nSequential order: {' → '.join(order)}")

    groups = get_parallel_groups(agent_graph)
    print(f"\nParallel execution tiers:")
    for i, group in enumerate(groups):
        print(f"  Tier {i+1}: {group}  (run in parallel)")
