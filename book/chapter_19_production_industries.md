# Chapter 19: Production AI Systems — Five Industry Architectures

> 📝 **Coding Handbook**: Practice the code from this chapter → [`coding-handbook/ch19_production_industries`](../coding-handbook/ch19_production_industries/)

## Overview

This chapter presents five complete, production-hardened agentic architectures for industries with strict regulatory, safety, and operational requirements. Every architecture is designed around the constraints of its industry — not despite them.

## The Five Industries

### 1. Healthcare — Clinical Decision Support Agent
- **Constraint**: HIPAA, patient safety, human-in-the-loop
- **Architecture**: Patient intake → PHI redaction → Medical NER → RAG clinical guidelines → Physician review gate
- **Key Code**: PHI Redactor, Physician Review Gate

### 2. Finance — Autonomous Market Analysis Agent
- **Constraint**: SEC compliance, position limits, circuit breakers
- **Architecture**: Market data → Signal generator → Risk calculator → Trade executor → Compliance auditor
- **Key Code**: Circuit Breaker, Risk Level Classifier

### 3. Legal — Contract Analysis Agent
- **Constraint**: Attorney-client privilege, accuracy requirements
- **Architecture**: PDF intake → Clause extraction → Risk classification → Summary → Red-flag alerts
- **Key Code**: Structured ContractClause extraction, Missing clause detection

### 4. E-Commerce — Multi-Agent Customer Service
- **Constraint**: Response time SLOs, seamless human escalation
- **Architecture**: Query → Intent router → Product recommender | Order tracker | Returns handler
- **Key Code**: EcommerceRouter with escalation logic

### 5. DevOps/SRE — Incident Response Agent
- **Constraint**: Blast radius limits, mandatory rollback, escalation timer
- **Architecture**: Alert → Log analyzer → Root cause → Blast radius check → Remediation → Post-mortem
- **Key Code**: BlastRadiusGuard, EscalationTimer

## Key Principle

> The difference between a demo and a deployment is compliance layers, audit trails, human-in-the-loop gates, and the discipline to say "the agent cannot decide this alone."
