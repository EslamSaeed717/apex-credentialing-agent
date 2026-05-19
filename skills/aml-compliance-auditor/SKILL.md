---
name: aml-compliance-auditor
description: Advanced automated AML (Anti-Money Laundering) and KYC (Know Your Customer) compliance auditing. Use for: analyzing transaction patterns, screening against sanctions lists, risk scoring, and ensuring regulatory adherence using AI and Moov-io/Watchman.
---

# AML Compliance Auditor

This skill empowers the agent to function as a high-level compliance officer, utilizing AI-driven pattern recognition and real-time sanctions screening.

## Core Workflows

### 1. Sanctions Screening (Watchman Integration)
Perform real-time checks against global watchlists (OFAC, UN, EU, etc.).
- Use `moov-io/watchman` logic to screen names, entities, and countries.
- Analyze results for exact and fuzzy matches.

### 2. Transaction Pattern Recognition
Identify suspicious financial activity using ensemble machine learning principles.
- **Data Ingestion**: Process structured financial data (Banks, Amounts, Currencies, Payment Formats).
- **Pattern Analysis**: Detect red flags such as rapid movement of funds, structuring, and unusual cross-border activity.
- **Risk Scoring**: Assign a "Suspicion Score" based on behavioral anomalies.

### 3. Risk Management (NIST AI RMF)
Apply the NIST AI Risk Management Framework to compliance operations:
- **Map**: Identify context and risks of financial systems.
- **Measure**: Track performance metrics and false positive rates.
- **Manage**: Implement controls and reporting protocols.

## Procedural Knowledge

- **Regulatory Frameworks**: Adhere to FATF recommendations and local banking regulations.
- **XAI (Explainable AI)**: Ensure every flagged transaction has a clear, auditable reason for suspicion.

## Resources
- Scripts for data preprocessing and risk scoring are located in `scripts/`.
- Regulatory checklists and NIST RMF mappings are in `references/`.
