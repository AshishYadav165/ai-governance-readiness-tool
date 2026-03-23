import streamlit as st
import uuid
import json
import math
from assessment_engine import (
    DIMENSIONS, MATURITY_LEVELS, MATURITY_BANDS,
    REMEDIATION, calculate_scores, get_overall,
    get_band, generate_narrative
)
from audit_log import log_assessment

st.set_page_config(
    page_title='AI Governance Readiness Assessment',
    page_icon='◈',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400&family=IBM+Plex+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; font-weight: 300; }
.main { background-color: #0d0d0d; }
.stApp { background-color: #0d0d0d; color: #e8e4dc; }
h1, h2, h3 { font-family: 'IBM Plex Sans', sans-serif !important; font-weight: 400 !important; }
.dim-header { border-left: 3px solid #b87333; padding-left: 16px; margin-bottom: 24px; }
.score-card { background: #1a1a1a; border: 1px solid rgba(255,255,255,0.08); border-radius: 4px; padding: 16px; margin-bottom: 12px; }
.maturity-badge { background: rgba(184,115,51,0.15); border: 1px solid #b87333; color: #b87333; padding: 4px 12px; border-radius: 2px; font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; }
.governance-notice { background: rgba(184,115,51,0.08); border: 1px solid rgba(184,115,51,0.3); border-radius: 4px; padding: 12px 16px; font-size: 12px; color: rgba(232,228,220,0.6); margin-bottom: 24px; }
.source-tag { font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: rgba(232,228,220,0.3); letter-spacing: 0.08em; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

DIM_COLORS = ['#6ba3be', '#8fbc8f', '#b8a0c8', '#c8b870', '#a888c8', '#c89878']

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'org' not in st.session_state:
    st.session_state.org = ''
if 'current_dim' not in st.session_state:
    st.session_state.current_dim = 0
if 'narrative' not in st.session_state:
    st.session_state.narrative = None

def render_intro():
    st.markdown("## ◈ AI Governance Readiness Assessment")
    st.markdown("##### Hybrid Framework · NIST AI RMF · ISO 42001:2023 · EU AI Act 2024")
    st.markdown("""
<div class="governance-notice">
This tool benchmarks AI governance maturity across six dimensions through 18 executive-level 
diagnostic questions. Built on a hybrid of NIST AI RMF, ISO 42001, and EU AI Act frameworks. 
The production version of this tool powers the proprietary 
<strong>SIGFOC™ AI Governance Framework</strong> used in client engagements at 
<a href="https://precisionpulseconsulting.com" style="color:#b87333;">PrecisionPulse Consulting LLC</a>.
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**6 Dimensions**")
        st.caption("Govern · Map · Measure · Manage · Ethics · Compliance")
    with col2:
        st.markdown("**18 Questions**")
        st.caption("Executive-level maturity diagnostic")
    with col3:
        st.markdown("**AI Gap Analysis**")
        st.caption("Claude-generated narrative with remediation roadmap")

    st.divider()
    org = st.text_input(
        'Organisation name (optional)',
        placeholder='e.g. AstraZeneca, Roche Diagnostics, J&J MedTech…',
        max_chars=80
    )
    if st.button('Begin Assessment →', type='primary'):
        st.session_state.org = org or 'Your Organisation'
        st.session_state.page = 'assess'
        st.session_state.current_dim = 0
        st.session_state.responses = {}
        st.rerun()

def render_assessment():
    dim_idx = st.session_state.current_dim
    dim = DIMENSIONS[dim_idx]
    color = DIM_COLORS[dim_idx]

    with st.sidebar:
        st.markdown(f"**◈ {st.session_state.org}**")
        st.divider()
        for i, d in enumerate(DIMENSIONS):
            done = d['key'] in st.session_state.responses
            status = '✓' if done else f'{i+1}'
            label = f"{status} {d['name']}"
            if i == dim_idx:
                st.markdown(f"**→ {label}**")
            else:
                st.markdown(label)
        st.divider()
        completed = len(st.session_state.responses)
        st.progress(completed / 6)
        st.caption(f"{completed} of 6 dimensions complete")

    st.markdown(f"<div class='dim-header'><h3 style='color:{color};margin:0'>{dim['name']}</h3><div class='source-tag'>{dim['source']}</div></div>", unsafe_allow_html=True)
    st.caption(dim['description'])
    st.markdown("---")

    existing = st.session_state.responses.get(dim['key'], [None, None, None])
    responses = []
    all_answered = True

    for qi, q in enumerate(dim['questions']):
        st.markdown(f"**Q{qi+1}** {q}")
        current_val = existing[qi] if existing[qi] is not None else 0
        val = st.select_slider(
            f"Rate Q{qi+1}",
            options=[1, 2, 3, 4, 5],
            value=current_val if current_val > 0 else 1,
            format_func=lambda x: f"{x} — {MATURITY_LEVELS[x]}",
            key=f"q_{dim['key']}_{qi}",
            label_visibility='collapsed'
        )
        responses.append(val)
        st.markdown("")

    col1, col2 = st.columns([1, 4])
    with col1:
        if dim_idx > 0:
            if st.button('← Back'):
                st.session_state.current_dim -= 1
                st.rerun()
    with col2:
        is_last = dim_idx == len(DIMENSIONS) - 1
        btn_label = 'Generate Report →' if is_last else 'Next →'
        if st.button(btn_label, type='primary'):
            st.session_state.responses[dim['key']] = responses
            if is_last:
                st.session_state.page = 'results'
            else:
                st.session_state.current_dim += 1
            st.rerun()

def render_results():
    scores = calculate_scores(st.session_state.responses)
    overall = get_overall(scores)
    band = get_band(overall)
    org = st.session_state.org

    st.markdown(f"## ◈ AI Governance Assessment Report")
    st.markdown(f"**{org.upper()}** · {__import__('datetime').date.today().strftime('%d %B %Y')}")
    st.divider()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Overall Score", f"{overall}/5.0")
        st.markdown(f"<span class='maturity-badge'>{band['label']}</span>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"**{band['headline']}**")
        st.caption(band['summary'])

    st.divider()

    st.markdown("#### Six-Dimension Profile")
    dim_keys = [d['key'] for d in DIMENSIONS]
    dim_names = [d['name'] for d in DIMENSIONS]
    dim_scores = [scores[k]['average'] for k in dim_keys]

    try:
        import streamlit as _st
        radar_html = generate_radar_html(dim_names, dim_scores)
        st.components.v1.html(radar_html, height=380)
    except:
        pass

    st.markdown("#### Dimension Scores")
    cols = st.columns(3)
    for i, dim in enumerate(DIMENSIONS):
        k = dim['key']
        avg = scores[k]['average']
        mat = scores[k]['maturity']
        pct = int((avg / 5) * 100)
        with cols[i % 3]:
            st.markdown(f"""
<div class="score-card">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
    <span style="color:{DIM_COLORS[i]};font-size:13px;font-weight:500">{dim['name']}</span>
    <span style="color:{DIM_COLORS[i]};font-family:'IBM Plex Mono',monospace;font-size:18px">{avg}</span>
  </div>
  <div style="height:2px;background:rgba(255,255,255,0.06);border-radius:2px;margin-bottom:8px">
    <div style="height:100%;width:{pct}%;background:{DIM_COLORS[i]};border-radius:2px"></div>
  </div>
  <span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:rgba(232,228,220,0.3);text-transform:uppercase;letter-spacing:0.1em">{mat}</span>
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("#### AI Governance Gap Analysis")
    st.caption("Generated by Claude (Anthropic) · Authored in the voice of Ashish Yadav, PrecisionPulse Consulting LLC")

    if st.session_state.narrative is None:
        with st.spinner('Generating executive gap analysis via Claude…'):
            narrative = generate_narrative(org, scores, overall)
            st.session_state.narrative = narrative
            log_assessment(
                st.session_state.session_id, org, 
                {k: scores[k]['average'] for k in scores},
                overall,
                str(narrative)
            )

    if st.session_state.narrative:
        dims_narrative = st.session_state.narrative.get('dimensions', [])
        for i, dim in enumerate(DIMENSIONS):
            item = next((x for x in dims_narrative if x['key'] == dim['key']), {})
            avg = scores[dim['key']]['average']
            mat = scores[dim['key']]['maturity']
            with st.expander(f"{dim['name']} — {avg}/5.0 · {mat}", expanded=True):
                st.markdown(item.get('text', 'Analysis unavailable.'))

    st.divider()
    st.markdown("#### Prioritised Remediation Roadmap")
    sorted_dims = sorted(DIMENSIONS, key=lambda d: scores[d['key']]['average'])

    def get_priority(avg):
        if avg < 2:
            return '🔴 Critical — Act Immediately', '0–90 days'
        elif avg < 3:
            return '🟠 High Priority', '90–180 days'
        elif avg < 4:
            return '🟡 Medium Priority', '180–365 days'
        else:
            return '🟢 Maintain & Optimise', '12–24 months'

    for rank, dim in enumerate(sorted_dims):
        avg = scores[dim['key']]['average']
        priority_label, horizon = get_priority(avg)
        with st.container():
            st.markdown(f"**{rank+1}. {dim['name']}** · Score: {avg}/5.0")
            st.caption(f"{priority_label} · {horizon}")
            st.markdown(REMEDIATION[dim['key']])
            st.markdown("---")

    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('New Assessment'):
            st.session_state.page = 'intro'
            st.session_state.responses = {}
            st.session_state.narrative = None
            st.rerun()
    with col2:
        report = generate_report_text(org, scores, overall, band)
        st.download_button(
            'Export Report',
            data=report,
            file_name=f'AI_Governance_Assessment_{org.replace(" ", "_")}_{__import__("datetime").date.today()}.txt',
            mime='text/plain'
        )
    with col3:
        st.markdown(
            '[View on GitHub](https://github.com/AshishYadav165/ai-governance-readiness-tool)',
            unsafe_allow_html=False
        )

    st.markdown("""
---
*AI Governance Readiness Assessment · Hybrid Framework: NIST AI RMF · ISO 42001:2023 · EU AI Act 2024*  
*© 2025 Ashish Yadav · [PrecisionPulse Consulting LLC](https://precisionpulseconsulting.com) · [ashish-yadav.com](https://ashish-yadav.com)*  
*The production version of this tool uses the proprietary SIGFOC™ AI Governance Framework*
""")

def generate_radar_html(names, scores):
    N = len(names)
    cx, cy, R = 180, 180, 130
    points_data = []
    for i in range(N):
        angle = (i / N) * 2 * math.pi - math.pi / 2
        r = (scores[i] / 5) * R
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points_data.append(f"{x},{y}")
    polygon_points = ' '.join(points_data)
    grid_lines = ''
    for ring in range(1, 6):
        ring_points = []
        for i in range(N):
            angle = (i / N) * 2 * math.pi - math.pi / 2
            r = (ring / 5) * R
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            ring_points.append(f"{x},{y}")
        grid_lines += f'<polygon points="{" ".join(ring_points)}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>'
    spokes = ''
    for i in range(N):
        angle = (i / N) * 2 * math.pi - math.pi / 2
        x = cx + R * math.cos(angle)
        y = cy + R * math.sin(angle)
        spokes += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>'
    labels = ''
    colors = ['#6ba3be', '#8fbc8f', '#b8a0c8', '#c8b870', '#a888c8', '#c89878']
    for i in range(N):
        angle = (i / N) * 2 * math.pi - math.pi / 2
        lx = cx + (R + 30) * math.cos(angle)
        ly = cy + (R + 30) * math.sin(angle)
        labels += f'<text x="{lx}" y="{ly}" text-anchor="middle" dominant-baseline="middle" fill="{colors[i]}" font-size="11" font-family="IBM Plex Sans,sans-serif">{names[i].split()[0]}</text>'
        sx = cx + ((scores[i]/5)*R) * math.cos(angle)
        sy = cy + ((scores[i]/5)*R) * math.sin(angle)
        labels += f'<circle cx="{sx}" cy="{sy}" r="4" fill="{colors[i]}"/>'
    return f"""
<div style="background:#111;border:1px solid rgba(255,255,255,0.08);border-radius:4px;padding:16px;display:flex;justify-content:center">
<svg width="360" height="360" viewBox="0 0 360 360" xmlns="http://www.w3.org/2000/svg">
  {grid_lines}{spokes}
  <polygon points="{polygon_points}" fill="rgba(184,115,51,0.1)" stroke="rgba(184,115,51,0.6)" stroke-width="1.5"/>
  {labels}
</svg>
</div>"""

def generate_report_text(org, scores, overall, band):
    from datetime import date
    lines = [
        'AI GOVERNANCE READINESS ASSESSMENT',
        'Hybrid Framework: NIST AI RMF · ISO 42001:2023 · EU AI Act 2024',
        '© 2025 Ashish Yadav · PrecisionPulse Consulting LLC',
        'https://precisionpulseconsulting.com',
        '',
        f'Organisation: {org}',
        f'Date: {date.today().strftime("%d %B %Y")}',
        f'Overall Score: {overall}/5.0 — {band["label"]}',
        '',
        'DIMENSION SCORES',
        '─' * 40,
    ]
    for dim in DIMENSIONS:
        k = dim['key']
        lines.append(f'{dim["name"]}: {scores[k]["average"]}/5.0 — {scores[k]["maturity"]}')
    lines += [
        '',
        band['headline'],
        band['summary'],
        '',
        'The production version of this assessment uses the proprietary SIGFOC™ framework.',
        'Contact: https://precisionpulseconsulting.com',
        'GitHub: https://github.com/AshishYadav165/ai-governance-readiness-tool',
    ]
    return '\n'.join(lines)

def main():
    if st.session_state.page == 'intro':
        render_intro()
    elif st.session_state.page == 'assess':
        render_assessment()
    elif st.session_state.page == 'results':
        render_results()

if __name__ == '__main__':
    main()
