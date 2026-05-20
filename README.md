# Apex Credentialing Agent

> **The Sovereign Credential Warfare System** — An autonomous AI agent that hunts, prices, and acquires professional certifications with maximum efficiency for financial compliance professionals.

## Overview

This system is designed for **Eslam Saeed Ahmed Al-Wajeeh**, a Senior AML & Financial Compliance Specialist from Yemen, to systematically build a world-class professional credential portfolio.

## Architecture

```
apex-credentialing-agent/
├── agents/              # Core AI agents (hunter, OSINT, pricing, portfolio)
├── scrapers/            # Stealth web scrapers (ACAMS, Coursera, Udemy, edX)
├── credential_engines/  # Pricing, scholarship, beta voucher engines
├── config/              # YAML configuration files
├── knowledge_base/      # Professional identity, resume, certifications
├── workflows/           # Automated daily scan workflows
├── dashboards/          # FastAPI REST API dashboard
├── templates/           # Email and LinkedIn post templates
└── memory/              # Vector store, embeddings, interaction history
```

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/EslamSaeed717/apex-credentialing-agent.git
cd apex-credentialing-agent

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 4. Run the agent
python workflows/daily_scan.py

# 5. Or use Docker
docker-compose up -d
```

## Target Credentials (Priority Order)

| Priority | Credential | Provider | ISR Score | Cost |
|----------|-----------|----------|-----------|------|
| 1 | CAMS | ACAMS | 9.8 | $1,695 (Scholarship Available) |
| 2 | CGSS | ACAMS | 9.2 | $1,295 (Scholarship Available) |
| 3 | CIPP/E | IAPP | 8.9 | $550 |
| 4 | CC | ISC2 | 8.5 | **FREE** |

## ISR Formula

```
ISR = (Impact × 10) / (Acquisition_Hours + 1)
```

Higher ISR = Better Return on Time Investment

---

*Built with obsessive precision for sovereign professional dominance.*
