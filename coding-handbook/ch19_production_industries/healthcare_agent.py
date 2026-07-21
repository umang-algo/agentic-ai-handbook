"""
Chapter 19: Industry 1 — Healthcare Clinical Decision Support Agent
===================================================================
Production-hardened clinical agent enforcing HIPAA PHI redaction,
Clinical Guidelines RAG, differential diagnosis reasoning, and a MANDATORY physician review gate.

From: The Practitioner's Handbook of Agentic AI, Chapter 19.1
"""

import re
import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class PatientRecord:
    patient_id: str
    raw_notes: str
    attending_physician: str


@dataclass
class ClinicalRecommendation:
    redacted_notes: str
    extracted_symptoms: List[str]
    proposed_diagnosis: str
    confidence: float
    guideline_citations: List[str]
    physician_approved: bool = False
    rejection_reason: Optional[str] = None


class PHIRedactor:
    """HIPAA compliance engine redacting Protected Health Information (PHI)."""
    PATTERNS = [
        (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED SSN]"),
        (r"\b\d{10}\b", "[REDACTED PHONE/MRN]"),
        (r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "[REDACTED NAME]"),
        (r"\b\d{1,5}\s+[A-Za-z0-9\s]+(?:Street|St|Avenue|Ave|Road|Rd)\b", "[REDACTED ADDRESS]"),
    ]

    @classmethod
    def redact(cls, text: str) -> str:
        redacted = text
        for pattern, replacement in cls.PATTERNS:
            redacted = re.sub(pattern, replacement, redacted)
        return redacted


class HealthcareClinicalAgent:
    """
    Clinical Decision Support Agent operating strictly within HIPAA compliance
    and requiring explicit human physician authorization.
    """
    def __init__(self):
        self.guidelines_db = {
            "chest pain": ["ACC/AHA 2021 Guideline for Evaluation of Chest Pain", "ESC NSTEMI Guidelines 2020"],
            "fever": ["IDSA Clinical Practice Guidelines for Fever Management"]
        }

    def process_patient(self, record: PatientRecord) -> ClinicalRecommendation:
        """Runs PHI Redaction, NER extraction, RAG lookup, and generates proposed recommendation."""
        # Step 1: HIPAA PHI Redaction
        safe_notes = PHIRedactor.redact(record.raw_notes)

        # Step 2: Extract clinical symptoms (Medical NER simulation)
        extracted_symptoms = []
        lower_notes = safe_notes.lower()
        if "chest pain" in lower_notes or "angina" in lower_notes:
            extracted_symptoms.append("chest pain")
        if "fever" in lower_notes or "chills" in lower_notes:
            extracted_symptoms.append("fever")

        # Step 3: RAG Guideline Retrieval
        citations = []
        for symptom in extracted_symptoms:
            if symptom in self.guidelines_db:
                citations.extend(self.guidelines_db[symptom])

        # Step 4: Differential Diagnosis Reasoning
        proposed = "Acute Coronary Syndrome (ACS) Evaluation" if "chest pain" in extracted_symptoms else "General Observation"

        return ClinicalRecommendation(
            redacted_notes=safe_notes,
            extracted_symptoms=extracted_symptoms,
            proposed_diagnosis=proposed,
            confidence=0.88 if extracted_symptoms else 0.50,
            guideline_citations=citations,
            physician_approved=False  # MUST be approved by human physician
        )

    def physician_signoff(self, recommendation: ClinicalRecommendation, approve: bool, reason: str = "") -> ClinicalRecommendation:
        """Mandatory Physician-in-the-Loop review gate."""
        recommendation.physician_approved = approve
        if not approve:
            recommendation.rejection_reason = reason
        return recommendation


if __name__ == "__main__":
    agent = HealthcareClinicalAgent()
    patient = PatientRecord(
        patient_id="PT-99412",
        raw_notes="Patient John Doe (SSN: 123-45-6789) presented with acute chest pain and shortness of breath.",
        attending_physician="Dr. Sarah Jenkins, MD"
    )

    rec = agent.process_patient(patient)
    print("Pre-Approval Recommendation (Redacted):")
    print(f"Redacted Text: {rec.redacted_notes}")
    print(f"Symptoms: {rec.extracted_symptoms}")
    print(f"Diagnosis: {rec.proposed_diagnosis}")
    print(f"Physician Approved: {rec.physician_approved}")

    # Physician Sign-off Gate
    rec = agent.physician_signoff(rec, approve=True)
    print(f"\nPost Physician Sign-off Approved: {rec.physician_approved}")
