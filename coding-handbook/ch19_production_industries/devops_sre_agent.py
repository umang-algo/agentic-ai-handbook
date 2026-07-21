"""
Chapter 19: Industry 5 — DevOps SRE Autonomous Incident Response Agent
=======================================================================
Production DevOps SRE agent performing automated log triage, root-cause diagnostics,
and human-in-the-loop remediation execution gates.

From: The Practitioner's Handbook of Agentic AI, Chapter 19.5
"""

import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class IncidentAlert:
    alert_id: str
    service_name: str
    severity: str  # "P1", "P2", "P3"
    error_log: str
    cpu_usage_percent: float
    memory_usage_percent: float


@dataclass
class RemediationPlan:
    alert_id: str
    root_cause: str
    proposed_action: str
    requires_human_approval: bool
    executed: bool = False


class DevOpsSREAgent:
    """DevOps SRE Autonomous Incident Response Agent."""
    def __init__(self):
        self.remediation_history: List[RemediationPlan] = []

    def diagnose_incident(self, alert: IncidentAlert) -> RemediationPlan:
        """Parses telemetry and error logs to determine root cause and remediation strategy."""
        log_lower = alert.error_log.lower()

        if "out of memory" in log_lower or "oom" in log_lower or alert.memory_usage_percent > 95.0:
            cause = "Memory Leak / Out of Memory (OOM) killer invoked."
            action = f"Restart pod/container for service '{alert.service_name}' and scale memory limit +50%."
            requires_approval = False if alert.severity != "P1" else True
        elif "connection refused" in log_lower or "database timeout" in log_lower:
            cause = "Database Connection Pool Exhaustion."
            action = f"Scale database connection pool size and restart service replica."
            requires_approval = True
        else:
            cause = "Unclassified high CPU load or unknown error."
            action = f"Trigger thread dump and escalate to on-call SRE engineer."
            requires_approval = True

        return RemediationPlan(
            alert_id=alert.alert_id,
            root_cause=cause,
            proposed_action=action,
            requires_human_approval=requires_approval
        )

    def execute_remediation(self, plan: RemediationPlan, human_approved: bool = False) -> Dict[str, Any]:
        """Executes remediation plan if auto-approved or approved by on-call engineer."""
        if plan.requires_human_approval and not human_approved:
            return {
                "alert_id": plan.alert_id,
                "status": "WAITING_FOR_SRE_APPROVAL",
                "action": plan.proposed_action,
                "executed": False
            }

        plan.executed = True
        self.remediation_history.append(plan)
        return {
            "alert_id": plan.alert_id,
            "status": "REMEDIATED_SUCCESSFULLY",
            "action": plan.proposed_action,
            "executed": True
        }


if __name__ == "__main__":
    sre_agent = DevOpsSREAgent()

    alert_p2 = IncidentAlert(
        alert_id="ALT-901",
        service_name="payment-gateway",
        severity="P2",
        error_log="java.lang.OutOfMemoryError: Java heap space",
        cpu_usage_percent=45.0,
        memory_usage_percent=98.5
    )

    plan1 = sre_agent.diagnose_incident(alert_p2)
    res1 = sre_agent.execute_remediation(plan1)
    print("Incident 1 (P2 OOM) Result:")
    print(json.dumps(res1, indent=2))

    alert_p1 = IncidentAlert(
        alert_id="ALT-902",
        service_name="auth-service",
        severity="P1",
        error_log="postgresql connection refused: max clients reached",
        cpu_usage_percent=88.0,
        memory_usage_percent=70.0
    )

    plan2 = sre_agent.diagnose_incident(alert_p1)
    res2 = sre_agent.execute_remediation(plan2, human_approved=False)
    print("\nIncident 2 (P1 DB Timeout - Unapproved):")
    print(json.dumps(res2, indent=2))

    res2_approved = sre_agent.execute_remediation(plan2, human_approved=True)
    print("\nIncident 2 (P1 DB Timeout - Approved):")
    print(json.dumps(res2_approved, indent=2))
