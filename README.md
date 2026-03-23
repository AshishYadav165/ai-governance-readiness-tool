# AI Governance Readiness Assessment Tool

**An executive-level AI governance maturity diagnostic built on a hybrid framework of NIST AI RMF · ISO 42001:2023 · EU AI Act 2024. Generates AI-powered gap analysis and prioritised remediation roadmaps via Anthropic Claude.**

---

## Overview

This tool benchmarks organisational AI governance maturity across six dimensions through 18 executive-level diagnostic questions. Each dimension is scored 1–5 across five maturity levels (Ad Hoc → Developing → Defined → Managed → Optimised), producing a comprehensive governance readiness report with an AI-generated narrative, radar profile, and prioritised remediation roadmap.

> **Note:** The production version of this tool powers the proprietary **SIGFOC™ AI Governance Framework** used in client engagements at [PrecisionPulse Consulting LLC](https://precisionpulseconsulting.com). The GitHub version uses a hybrid of publicly available frameworks to demonstrate the underlying technical architecture.

---

## Six Assessment Dimensions

| Dimension | Primary Frameworks | What It Measures |
|-----------|-------------------|-----------------|
| Govern | NIST AI RMF · ISO 42001 Cl.4-5 · ISO 38507 | C-suite accountability, AI policy enforcement, governance authority |
| Map & Identify | NIST AI RMF · ISO 42001 Cl.6 · EU AI Act Annex III | AI system inventory, risk classification, regulatory mapping |
| Measure & Evaluate | NIST AI RMF · ISO 42001 Cl.9 · EU AI Act Art.9+72 | Performance monitoring, executive KPIs, board reporting |
| Manage & Mitigate | NIST AI RMF · ISO 42001 Cl.8 · EU AI Act Art.17 · FDA PCCP | Risk treatment, change control, post-deployment surveillance |
| Ethics & Responsible AI | UNESCO AI Ethics · EU HLEG · OECD AI Principles · IEEE 7000 | Operationalised ethics, bias accountability, human oversight |
| Compliance & Transparency | EU AI Act Art.13-14 · ISO 42001 Cl.7-8 · FDA SaMD · UK AI | Regulatory readiness, audit preparedness, disclosure obligations |

---

## What the Tool Produces

- **Overall maturity score** (1.0–5.0) with band classification across 5 levels
- **Radar/spider chart** showing six-dimension governance profile
- **Per-dimension score cards** with maturity level indicators
- **AI-generated executive gap analysis** via Anthropic Claude Haiku — authored in the voice of a senior AI governance practitioner with ISO 42001 Lead Auditor expertise
- **Prioritised remediation roadmap** ranked by score with time horizons and board-level actions
- **Exportable plain-text report** with full scoring detail

---

## Architecture
```
User Input (18 questions) 
→ Streamlit interface 
→ assessment_engine.py (scoring + maturity logic) 
→ Anthropic Claude Haiku (narrative generation) 
→ audit_log.py (JSONL audit trail) 
→ Results: radar chart + gap analysis + roadmap
```

---

## Technology Stack

- **LLM:** Anthropic Claude Haiku — selected for instruction-following precision in governance narrative generation
- **Interface:** Streamlit
- **Audit logging:** JSON Lines format with SHA-256 response hashing
- **Frameworks referenced:** NIST AI RMF 1.0, ISO 42001:2023, EU AI Act 2024/1689, FDA SaMD guidance, OECD AI Principles, UNESCO AI Ethics, IEEE 7000, UK AI Framework

---

## Setup and Installation

**1. Clone the repository**
```bash
git clone https://github.com/AshishYadav165/ai-governance-readiness-tool.git
cd ai-governance-readiness-tool
```

**2. Create and activate virtual environment**
```bash
python -m venv venv && source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
# Add your Anthropic API key to .env
```

**5. Run the application**
```bash
python -m streamlit run app.py
```

---

## Governance Design

Questions are written at executive level — designed for Chief AI Officers, Chief Digital Officers, VP AI/Data, and Boards of Directors. Each question tests whether governance is genuinely operationalised rather than merely documented.

The narrative generation system prompt instructs Claude to respond as a senior AI governance practitioner with ISO 42001 and ISO 13485 Lead Auditor credentials — ensuring outputs reflect practitioner knowledge rather than generic consulting language.

Every assessment is logged to a local JSONL audit file with timestamp, session ID, dimension scores, and SHA-256 response hash — demonstrating governance-by-design in the tool architecture itself.

---

## Regulatory Context

- **EU AI Act:** Tool itself is likely limited-risk — transparency obligations apply
- **FDA:** Does not meet the definition of a medical device under current scope
- **HIPAA:** No protected health information processed
- **ISO 42001:** Governance architecture aligned to AI management system requirements

---

## Related Work

This tool is part of a broader AI portfolio for regulated life sciences environments:

- **[Regulatory Intelligence RAG Assistant](https://github.com/AshishYadav165/regulatory-intelligence-assistant)** — AI-powered Q&A over FDA guidance, EU AI Act, ISO 42001, and NIST AI RMF with source citations
- **SIGFOC™ AI Governance Framework** — Proprietary six-dimension governance operating model available through [PrecisionPulse Consulting LLC](https://precisionpulseconsulting.com)

---

## Author

**Ashish Yadav** | Senior Life Sciences Executive | AI Strategy & Governance  
Dual ISO Lead Auditor: ISO 42001 (AI Management Systems) · ISO 13485 (Medical Devices QMS)  
Founder, PrecisionPulse Consulting LLC  
[precisionpulseconsulting.com](https://precisionpulseconsulting.com) · [ashish-yadav.com](https://ashish-yadav.com)
