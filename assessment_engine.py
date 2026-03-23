from llm_router import get_llm_response
import json

DIMENSIONS = [
    {
        'key': 'govern',
        'name': 'Govern',
        'source': 'NIST AI RMF · ISO 42001 Cl.4-5 · ISO 38507',
        'description': 'Organisational accountability, AI policy structures, and board-level oversight',
        'questions': [
            'AI governance accountability is owned at C-suite or Board level — not delegated entirely to IT, Legal, or a standalone compliance function.',
            'AI governance policies are actively enforced and regularly tested against real deployment scenarios — not confined to a policy document that predates your current AI portfolio.',
            'Your AI governance committee has genuine decision-making authority — it can halt, modify, or reject AI deployments, and has exercised that authority in practice.'
        ]
    },
    {
        'key': 'map',
        'name': 'Map & Identify',
        'source': 'NIST AI RMF · ISO 42001 Cl.6 · EU AI Act Annex III',
        'description': 'AI risk identification, system classification, and stakeholder impact assessment',
        'questions': [
            'Senior leadership can state with confidence how many AI systems are in production, what decisions they influence, and which carry the highest regulatory or patient risk.',
            'AI systems are assessed for unintended consequences — including cascading failures, misuse scenarios, and second-order impacts on patients or populations — before and after deployment.',
            'Regulatory classification of AI use cases is completed proactively by people who understand the frameworks — not reactively when a regulator or auditor asks the question.'
        ]
    },
    {
        'key': 'measure',
        'name': 'Measure & Evaluate',
        'source': 'NIST AI RMF · ISO 42001 Cl.9 · EU AI Act Art.9+72',
        'description': 'Quantification, monitoring, and executive reporting of AI risk and performance',
        'questions': [
            'When an AI system in production begins to underperform or drift, the governance function — not just the technical team — is informed and has a defined response protocol.',
            'Executives and board members who rely on AI-informed decisions can articulate the confidence level, known limitations, and failure modes of those systems — not just their outputs.',
            'AI governance has defined KPIs that appear on leadership dashboards alongside financial
and operational metrics — treated as a business performance indicator, not a compliance exercise.'
        ]
    },
    {
        'key': 'manage',
        'name': 'Manage & Mitigate',
        'source': 'NIST AI RMF · ISO 42001 Cl.8 · EU AI Act Art.17 · FDA PCCP',
        'description': 'Risk treatment, lifecycle management, and post-deployment surveillance',
        'questions': [
            'AI risks are managed with the same rigour as financial or operational risks — with named owners, board visibility, and consequences for non-remediation.',
            'Changes to AI systems after deployment go through a governed change control process — the organisation does not rely on vendor assurances or assume prior validation remains valid.',
            'Post-deployment surveillance of AI systems is treated as a strategic obligation — with findings fed back into governance reviews, not siloed within technical or quality functions.'
        ]
    },
    {
        'key': 'ethics',
        'name': 'Ethics & Responsible AI',
        'source': 'UNESCO AI Ethics · EU HLEG · OECD AI Principles · IEEE 7000',
        'description': 'Operationalised ethics, bias accountability, and enforced human oversight',
        'questions': [
            'AI ethics commitments are visible in actual deployment decisions — the organisation has declined, modified, or halted an AI initiative on ethical grounds, not just documented its principles.',
            'The organisation can demonstrate — with evidence — that its AI systems do not produce systematically different outcomes for different patient populations, demographic groups, or geographies.',
            'Human oversight of high-stakes AI decisions is genuinely enforced — not a rubber-stamp process where AI recommendations are accepted without meaningful review.'
        ]
    },
    {
        'key': 'compliance',
        'name': 'Compliance & Transparency',
        'source': 'EU AI Act Art.13-14 · ISO 42001 Cl.7-8 · FDA SaMD · UK AI Framework',
        'description': 'Regulatory readiness, audit preparedness, and disclosure obligations',
        'questions': [
            'The organisation knows precisely which of its AI systems fall within the scope of the EU AI Act, FDA SaMD guidance, or equivalent national regulations — and has a board-approved plan for each.',
            'Transparency obligations are treated as a trust and reputational imperative — not merely a legal checkbox — with disclosures designed for the actual comprehension level of the end user or patient.',
            'If FDA, EMA, or a Notified Body requested your AI governance documentation tomorrow, your organisation could respond with confidence — not spend weeks reconstructing records.'
        ]
    }
]

MATURITY_LEVELS = {
    1: 'Ad Hoc',
    2: 'Developing',
    3: 'Defined',
    4: 'Managed',
    5: 'Optimised'
}

MATURITY_BANDS = [
    {'min': 0, 'max': 1.5, 'label': 'Initial',
     'headline': 'Governance foundations are absent or ad hoc',
     'summary': 'AI governance exists in isolated pockets without institutional structure. Significant regulatory and operational exposure. Immediate board-level prioritisation required across all six dimensions.'},
    {'min': 1.5, 'max': 2.5, 'label': 'Developing',
     'headline': 'Early governance structures are forming but lack consistency',
     'summary': 'Some mechanisms exist but are inconsistently applied and rarely tested. Accountability gaps remain. The organisation is building awareness but has not yet embedded governance into operational decision-making.'},
    {'min': 2.5, 'max': 3.5, 'label': 'Defined',
     'headline': 'Governance is documented and partially operationalised',
     'summary': 'Formal policies and accountabilities are in place. The critical shift now is from documentation to consistent enforcement — and from compliance to competitive governance advantage.'},
    {'min': 3.5, 'max': 4.5, 'label': 'Managed',
     'headline': 'Governance is actively enforced and continuously improved',
     'summary': 'AI governance is embedded into operational and strategic decisions with measurable outcomes. Leadership is engaged. The organisation is well-positioned for regulatory scrutiny and building a genuine governance differentiator.'},
    {'min': 4.5, 'max': 5.1, 'label': 'Optimised',
     'headline': 'Governance is a board-level strategic differentiator',
     'summary': 'AI governance is mature, proactive, and demonstrably aligned to international standards. The organisation is positioned as a benchmark for peers, regulators, and partners — governance as competitive advantage.'}
]

REMEDIATION = {
    'govern': 'Establish named C-suite AI governance accountability and a cross-functional governance committee with genuine authority to halt or modify AI deployments. Align policies to ISO 42001 Clause 5 leadership requirements.',
    'map': 'Commission a complete AI system inventory with risk classification. Implement proactive regulatory mapping against EU AI Act Annex III and FDA SaMD categories before your next board cycle.',
    'measure': 'Build an AI governance KPI dashboard visible to C-suite and board alongside financial metrics. Define escalation protocols that bring governance — not just technical — teams into performance incidents.',
    'manage': 'Implement a governed AI change control process. Elevate post-deployment surveillance to a board-reported strategic obligation with named executive ownership.',
    'ethics': 'Operationalise ethics principles beyond documentation — establish a bias evaluation standard with demographic evidence requirements and enforce genuine human oversight for all high-stakes AI decisions.',
    'compliance': 'Complete an EU AI Act and FDA SaMD scope assessment with board-approved remediation plans. Build audit-ready documentation infrastructure capable of responding to regulatory requests within 48 hours.'
}

def calculate_scores(responses: dict) -> dict:
    scores = {}
    for dim in DIMENSIONS:
        key = dim['key']
        if key in responses:
            qs = responses[key]
            avg = sum(qs) / len(qs)
            scores[key] = {
                'average': round(avg, 2),
                'questions': qs,
                'maturity': MATURITY_LEVELS.get(round(avg), 'Ad Hoc')
            }
    return scores

def get_overall(scores: dict) -> float:
    avgs = [v['average'] for v in scores.values()]
    return round(sum(avgs) / len(avgs), 2) if avgs else 0

def get_band(overall: float) -> dict:
    for band in MATURITY_BANDS:
        if band['min'] <= overall <= band['max']:
            return band
    return MATURITY_BANDS[0]

def generate_narrative(org: str, scores: dict, overall: float) -> str:
    band = get_band(overall)
    score_summary = '\n'.join([
        f"{k.upper()} ({scores[k]['maturity']}): {scores[k]['average']}/5.0"
        for k in scores
    ])
    system = """You are Ashish Yadav, a Senior AI Governance Executive and Dual ISO Lead Auditor 
(ISO 42001 AI Management Systems · ISO 13485 Medical Devices QMS) with 20 years of experience 
in life sciences, CDx co-development, and regulated AI deployments at Tier 1 pharma companies 
including AstraZeneca, Pfizer, BMS, and Amgen. You founded PrecisionPulse Consulting LLC and 
created the SIGFOC™ AI Governance Framework. Write in a direct, board-presentable voice that 
reflects deep practitioner knowledge — not generic consulting language."""

    prompt = f"""An organisation named "{org}" has completed an AI Governance Readiness Assessment.

Overall score: {overall}/5.0 — Maturity level: {band['label']}

Dimension scores:
{score_summary}

Write a concise executive gap analysis for each of the 6 dimensions. For each dimension provide:
1. What the score reveals about the organisation's actual governance state (not just the number)
2. The single most consequential gap or risk implied by the score
3. One specific, board-level actionable recommendation

Write in first person as Ashish Yadav. Be direct and specific — reference ISO 42001, EU AI Act, 
FDA SaMD, or OECD principles where relevant. Each dimension analysis should be 60-80 words.
Avoid generic statements — every sentence should reflect practitioner knowledge.

Respond ONLY with valid JSON, no markdown, no preamble:
{{"dimensions": [{{"key": "govern", "text": "..."}}, {{"key": "map", "text": "..."}}, {{"key": "measure", "text": "..."}}, {{"key": "manage", "text": "..."}}, {{"key": "ethics", "text": "..."}}, {{"key": "compliance", "text": "..."}}]}}"""

    try:
        response = get_llm_response(prompt, system=system)
        clean = response.replace('```json', '').replace('```', '').strip()
        parsed = json.loads(clean)
        return parsed
    except Exception as e:
        return {'dimensions': [
            {'key': d['key'], 'text': f'Analysis unavailable for {d["name"]}. Please retry.'}
            for d in DIMENSIONS
        ]}
