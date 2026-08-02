"""
Reusable UI component renderers for the AI Resume Shortlisting System.
All functions return HTML strings rendered via st.markdown(unsafe_allow_html=True).
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from html import escape
from textwrap import dedent
from constants import COLORS, CHART_COLORSCALE


# ── Layout Helpers ────────────────────────────────────────────────────────────

def render_theme_toggle():
    """Render a top-right light/dark toggle with automatic system theme default."""
    components.html(
        """
        <script>
          (() => {
            const parentWindow = window.parent;
            const parentDoc = parentWindow.document;
            const root = parentDoc.documentElement;
            const storageKey = "ars-theme-preference";
            const media = parentWindow.matchMedia("(prefers-color-scheme: dark)");

            const getPreference = () => parentWindow.localStorage.getItem(storageKey) || "system";
            const resolveTheme = (pref) => (pref === "system" ? (media.matches ? "dark" : "light") : pref);

            const ensureButton = () => {
              let btn = parentDoc.getElementById("ars-theme-toggle-btn");
              if (btn) return btn;
              btn = parentDoc.createElement("button");
              btn.id = "ars-theme-toggle-btn";
              btn.type = "button";
              parentDoc.body.appendChild(btn);
              return btn;
            };

            const updateButton = (activeTheme) => {
              const btn = ensureButton();
              btn.textContent = activeTheme === "dark" ? "🌙 Dark" : "☀️ Light";
              btn.title = "Switch theme";
            };

            const applyPreference = (pref) => {
              const activeTheme = resolveTheme(pref);
              root.setAttribute("data-app-theme", activeTheme);
              parentWindow.localStorage.setItem(storageKey, pref);
              updateButton(activeTheme);
            };

            const btn = ensureButton();
            btn.onclick = () => {
              const currentTheme = resolveTheme(getPreference());
              applyPreference(currentTheme === "dark" ? "light" : "dark");
            };

            if (!parentWindow.__arsThemeMediaListenerBound) {
              media.addEventListener("change", () => {
                if (getPreference() === "system") applyPreference("system");
              });
              parentWindow.__arsThemeMediaListenerBound = true;
            }

            applyPreference(getPreference());
          })();
        </script>
        """,
        height=0,
        width=0,
    )


def render_page_header():
    """Render the main page title and subtitle."""
    st.markdown(
        '<div class="page-header">'
        '  <div class="page-header-main">'
        '    <div class="gradient-title">Resume Shortlisting System</div>'
        '    <p class="gradient-subtitle">AI-powered candidate ranking powered by NLP & TF-IDF</p>'
        '  </div>'
        '  <div class="page-credit">made with love by <strong>Himanshu Deshmukh</strong></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_section_header(icon: str, title: str):
    """Render a section header with icon badge."""
    st.markdown(
        f'<div class="section-header">'
        f'  <span class="section-header-icon">{icon}</span>'
        f'  <h3>{title}</h3>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_divider(label: str = ""):
    """Render a divider line, optionally with a centered label."""
    if label:
        st.markdown(
            f'<div class="divider-labeled"><span>{label}</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("---")


# ── Metric Cards ──────────────────────────────────────────────────────────────

def render_metric_card(label: str, value: str, sub: str = "", variant: str = "primary"):
    """Render a single metric card with a colored top border."""
    css_class = f"metric-card metric-card-{variant}"
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="{css_class}">'
        f'  <div class="metric-label">{label}</div>'
        f'  <div class="metric-value">{value}</div>'
        f'  {sub_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_metrics_row(results: list):
    """Render the three top-level metrics: candidates, avg score, top candidate."""
    col1, col2, col3 = st.columns(3)

    total = len(results)
    avg_score = sum(r["final_score"] for r in results) / total * 100 if total else 0
    top = results[0] if results else None

    with col1:
        render_metric_card("Total Candidates", str(total), f"{total} resume(s) processed", "success")
    with col2:
        render_metric_card("Avg Match Score", f"{avg_score:.1f}%", "Across all candidates", "primary")
    with col3:
        if top:
            render_metric_card(
                "Top Candidate",
                top["name"],
                f"{top['final_score'] * 100:.1f}% match score",
                "warning",
            )
        else:
            render_metric_card("Top Candidate", "—", "No candidates yet", "primary")


# ── Skill Pills ───────────────────────────────────────────────────────────────

def render_skill_pills(skills: list, pill_class: str, max_show: int = 8) -> str:
    """Return HTML string of skill pills with a '+N more' overflow badge."""
    shown = skills[:max_show]
    overflow = len(skills) - max_show

    pills = " ".join(f'<span class="{pill_class}">{s}</span>' for s in shown)
    if overflow > 0:
        pills += f' <span class="skill-more-badge">+{overflow} more</span>'
    return pills


# ── Score Bar ─────────────────────────────────────────────────────────────────

def render_score_bar(score_pct: float) -> str:
    """Return HTML string for a colored score bar."""
    if score_pct >= 65:
        bar_class = "score-bar-high"
    elif score_pct >= 40:
        bar_class = "score-bar-mid"
    else:
        bar_class = "score-bar-low"

    return (
        f'<div class="score-bar-track">'
        f'  <div class="score-bar-fill {bar_class}" style="width: {int(score_pct)}%;"></div>'
        f'</div>'
    )


# ── Candidate Card ────────────────────────────────────────────────────────────

def render_candidate_card(candidate: dict, rank: int):
    """Render a full candidate card with rank badge, name, score, skills."""
    score_pct = candidate["final_score"] * 100
    candidate_name = escape(str(candidate.get("name", "Unknown")))
    candidate_education = escape(str(candidate.get("education", "Not specified")))
    candidate_experience = candidate.get("experience_years", 0.0)

    # Score color
    if score_pct >= 65:
        score_color = COLORS["success"]
    elif score_pct >= 40:
        score_color = COLORS["warning"]
    else:
        score_color = COLORS["danger"]

    # Rank circle CSS class
    rank_cls = f"rank-{rank}" if rank <= 3 else "rank-default"

    # Top badge for rank 1
    top_badge = '<span class="top-badge">🏆 Best Match</span> ' if rank == 1 else ""

    # Skills HTML
    found_html = render_skill_pills(candidate["skills_found"], "skill-pill-found")
    missing_html = render_skill_pills(candidate["skills_missing"], "skill-pill-missing")

    # Missing section (only if there are missing skills)
    missing_section = ""
    if candidate["skills_missing"]:
        missing_section = dedent(f"""
                        <div class="skills-group">
                                <div class="skills-group-title">
                    Missing Skills
                </div>
                <div>{missing_html}</div>
            </div>
        """).strip()

        card_html = dedent(f"""
                <script>
                    (() => {{
                        const key = "ars-theme-preference";
                        const pref = localStorage.getItem(key) || "system";
                        const darkBySystem = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
                        const theme = pref === "system" ? (darkBySystem ? "dark" : "light") : pref;
                        document.documentElement.setAttribute("data-app-theme", theme);
                    }})();
                </script>
                <style>
                    * {{ box-sizing: border-box; }}
                    :root {{
                        --card-surface: {COLORS['surface']};
                        --card-surface-alt: {COLORS['surface_alt']};
                        --card-border: {COLORS['border']};
                        --card-border-light: {COLORS['border_light']};
                        --card-text-primary: {COLORS['text_primary']};
                        --card-text-secondary: {COLORS['text_secondary']};
                        --card-text-muted: {COLORS['text_muted']};
                    }}
                    :root[data-app-theme="dark"] {{
                        --card-surface: #111827;
                        --card-surface-alt: #1f2937;
                        --card-border: #334155;
                        --card-border-light: #1e293b;
                        --card-text-primary: #e2e8f0;
                        --card-text-secondary: #cbd5e1;
                        --card-text-muted: #94a3b8;
                    }}
                    body {{ margin: 0; font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif; color: var(--card-text-primary); }}
                    .candidate-card {{
                        background: var(--card-surface);
                        border: 1px solid var(--card-border);
                        border-radius: 16px;
                        padding: 0;
                        overflow: hidden;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
                    }}
                    .candidate-card-top {{
                        padding: 20px 24px 12px;
                        display: flex;
                        align-items: center;
                        gap: 16px;
                    }}
                    .rank-circle {{
                        width: 48px;
                        height: 48px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 800;
                        font-size: 1rem;
                        color: white;
                        flex-shrink: 0;
                    }}
                    .rank-1 {{ background: linear-gradient(135deg, #f59e0b, #f97316); box-shadow: 0 4px 14px rgba(245,158,11,0.35); }}
                    .rank-2 {{ background: linear-gradient(135deg, #94a3b8, #64748b); box-shadow: 0 4px 14px rgba(148,163,184,0.3); }}
                    .rank-3 {{ background: linear-gradient(135deg, #b45309, #d97706); box-shadow: 0 4px 14px rgba(180,83,9,0.25); }}
                    .rank-default {{ background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['primary_light']}); box-shadow: 0 4px 14px rgba(99,102,241,0.2); }}
                    .candidate-name {{ font-size: 1.15rem; font-weight: 700; color: var(--card-text-primary); line-height: 1.2; }}
                    .candidate-meta {{ font-size: 0.82rem; color: var(--card-text-muted); margin-top: 4px; display: flex; flex-wrap: wrap; gap: 8px; }}
                    .candidate-score-badge {{ margin-left: auto; text-align: center; min-width: 74px; }}
                    .score-number {{ font-size: 1.6rem; font-weight: 800; line-height: 1; }}
                    .score-label {{ font-size: 0.7rem; font-weight: 500; color: var(--card-text-muted); text-transform: uppercase; letter-spacing: 0.04em; }}
                    .candidate-card-body {{ padding: 0 24px 20px; }}
                    .score-bar-track {{ height: 6px; background: var(--card-border-light); border-radius: 3px; overflow: hidden; margin: 12px 0; }}
                    .score-bar-fill {{ height: 100%; border-radius: 3px; }}
                    .score-bar-high {{ background: linear-gradient(90deg, #10b981, #34d399); }}
                    .score-bar-mid {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}
                    .score-bar-low {{ background: linear-gradient(90deg, #ef4444, #f87171); }}
                    .skills-group {{ margin-top: 12px; }}
                    .skills-group-title {{ font-size: 0.78rem; font-weight: 600; color: var(--card-text-muted); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 8px; }}
                    .skill-pill-found {{ display: inline-block; background: linear-gradient(135deg, #d1fae5, #a7f3d0); color: #065f46; padding: 4px 12px; border-radius: 20px; font-size: 11.5px; font-weight: 500; margin: 2px 3px; border: 1px solid rgba(16,185,129,0.15); }}
                    .skill-pill-missing {{ display: inline-block; background: linear-gradient(135deg, #fee2e2, #fecaca); color: #991b1b; padding: 4px 12px; border-radius: 20px; font-size: 11.5px; font-weight: 500; margin: 2px 3px; border: 1px solid rgba(239,68,68,0.12); }}
                    .skill-more-badge {{ display: inline-block; background: var(--card-border-light); color: var(--card-text-muted); padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; margin: 2px 3px; border: 1px dashed var(--card-border); }}
                    .info-pill {{ display: inline-flex; align-items: center; gap: 5px; background: var(--card-surface-alt); border: 1px solid var(--card-border); padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; color: var(--card-text-secondary); }}
                    .top-badge {{ display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 999px; background: rgba(245,158,11,0.12); color: #b45309; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; white-space: nowrap; }}
                </style>
                <div class="candidate-card">
                    <div class="candidate-card-top">
                        <div class="rank-circle {rank_cls}">#{rank}</div>
                        <div style="flex: 1; min-width: 0;">
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                {top_badge}
                                <div class="candidate-name">{candidate_name}</div>
                            </div>
                            <div class="candidate-meta">
                                <span class="info-pill">🎓 {candidate_education}</span>
                                <span class="info-pill">💼 {candidate_experience:.1f} yrs exp</span>
                            </div>
                        </div>
                        <div class="candidate-score-badge">
                            <div class="score-number" style="color: {score_color};">{score_pct:.1f}%</div>
                            <div class="score-label">Match</div>
                        </div>
                    </div>
                    <div class="candidate-card-body">
                        {render_score_bar(score_pct)}
                        <div class="skills-group">
                            <div class="skills-group-title">Matched Skills</div>
                            <div>{found_html}</div>
                        </div>
                        {missing_section}
                    </div>
                </div>
        """).strip()

        components.html(card_html, height=420, scrolling=False)


# ── Rankings Tab ──────────────────────────────────────────────────────────────

def render_rankings(results: list):
    """Render the full rankings tab content."""
    if not results:
        st.markdown(
            '<div class="empty-state">'
            '  <div class="empty-state-icon">📊</div>'
            '  <h4>No results yet</h4>'
            '  <p>Upload resumes and click "Rank Resumes" to see results here.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    render_section_header("📊", "Candidate Rankings")

    for idx, candidate in enumerate(results):
        render_candidate_card(candidate, candidate["rank"])


# ── Chart Tab ─────────────────────────────────────────────────────────────────

def render_chart(results: list):
    """Render the score distribution chart and detailed table."""
    render_section_header("📈", "Score Distribution")

    names = [r["name"] for r in results]
    scores = [r["final_score"] * 100 for r in results]

    # Color each bar based on score
    bar_colors = []
    for s in scores:
        if s >= 65:
            bar_colors.append(COLORS["success"])
        elif s >= 40:
            bar_colors.append(COLORS["warning"])
        else:
            bar_colors.append(COLORS["danger"])

    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=scores,
            marker=dict(
                color=bar_colors,
                line=dict(color="rgba(255,255,255,0.8)", width=1),
                cornerradius=6,
            ),
            text=[f'{s:.1f}%' for s in scores],
            textposition="outside",
            textfont=dict(size=12, color=COLORS["text_secondary"], family="Inter"),
            hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}%<extra></extra>",
        )
    ])

    fig.update_layout(
        title=dict(
            text="Final Scores by Candidate",
            font=dict(size=16, color=COLORS["text_primary"], family="Inter"),
        ),
        xaxis=dict(
            title="",
            tickfont=dict(size=12, color=COLORS["text_secondary"]),
            showgrid=False,
        ),
        yaxis=dict(
            title=dict(text="Score (%)", font=dict(size=12, color=COLORS["text_muted"])),
            tickfont=dict(size=11, color=COLORS["text_muted"]),
            range=[0, 105],
            gridcolor=COLORS["border_light"],
        ),
        height=420,
        showlegend=False,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Inter",
            bordercolor=COLORS["border"],
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed results table
    render_section_header("📋", "Detailed Results")

    df = pd.DataFrame([
        {
            "Rank": r["rank"],
            "Name": r["name"],
            "Score %": f"{r['final_score'] * 100:.1f}%",
            "Education": r["education"],
            "Experience": f"{r['experience_years']:.1f}y",
            "Skills Found": f"{len(r['skills_found'])} / {len(r['skills_found']) + len(r['skills_missing'])}",
        }
        for r in results
    ])

    st.dataframe(df, use_container_width=True, hide_index=True)


# ── Export Section ────────────────────────────────────────────────────────────

def render_export(results: list):
    """Render the CSV download button."""
    render_divider("Export")

    csv_data = [
        {
            "Rank": r["rank"],
            "Name": r["name"],
            "Final Score": f"{r['final_score']:.4f}",
            "Score %": f"{r['final_score'] * 100:.1f}",
            "Education": r["education"],
            "Experience (Years)": r["experience_years"],
            "TF-IDF Score": f"{r['tfidf_score']:.4f}",
            "Skill Match %": f"{r['skill_match_pct'] * 100:.1f}",
            "Skills Found": ", ".join(r["skills_found"]),
            "Skills Missing": ", ".join(r["skills_missing"]),
        }
        for r in results
    ]

    csv_bytes = pd.DataFrame(csv_data).to_csv(index=False).encode("utf-8")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥  Download Results as CSV",
            data=csv_bytes,
            file_name="shortlisted_candidates.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ── Footer ────────────────────────────────────────────────────────────────────

def render_footer(version: str):
    """Render the app footer with credit line in an isolated iframe."""
    html = f"""
    <script>
      (() => {{
        const key = "ars-theme-preference";
        const pref = localStorage.getItem(key) || "system";
        const darkBySystem = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
        const theme = pref === "system" ? (darkBySystem ? "dark" : "light") : pref;
        document.documentElement.setAttribute("data-app-theme", theme);
      }})();
    </script>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
      :root {{
        --footer-text: #475569;
        --footer-muted: #94a3b8;
        --footer-chip-bg: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(168,85,247,0.10));
        --footer-chip-border: rgba(99,102,241,0.25);
      }}
      :root[data-app-theme="dark"] {{
        --footer-text: #cbd5e1;
        --footer-muted: #94a3b8;
        --footer-chip-bg: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(168,85,247,0.22));
        --footer-chip-border: rgba(129,140,248,0.45);
      }}
      body {{
        margin: 0; padding: 0; display: flex; justify-content: center;
        font-family: 'Inter', sans-serif;
      }}
      .footer-wrap {{
        text-align: center;
        padding: 30px 0 16px;
      }}
      .footer-brand {{
        font-size: 0.88rem;
        font-weight: 700;
        color: #6366f1;
        letter-spacing: 0.02em;
      }}
      .footer-version {{
        font-size: 0.78rem;
        color: var(--footer-muted);
        margin-top: 4px;
      }}
      .footer-credit {{
        margin-top: 20px;
        padding: 14px 32px;
        display: inline-block;
        background: var(--footer-chip-bg);
        border: 1.5px solid var(--footer-chip-border);
        border-radius: 40px;
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--footer-text);
        letter-spacing: 0.01em;
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
      }}
      .footer-credit:hover {{
        background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(168,85,247,0.18));
        border-color: rgba(99,102,241,0.45);
        box-shadow: 0 6px 24px rgba(99,102,241,0.18);
        transform: translateY(-2px);
      }}
      .heart {{
        display: inline-block;
        font-size: 1.15em;
        animation: heartbeat 1.4s ease-in-out infinite;
        filter: drop-shadow(0 0 4px rgba(239,68,68,0.3));
      }}
      .author {{
        background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 1.08em;
        letter-spacing: 0.02em;
      }}
      @keyframes heartbeat {{
        0%, 100% {{ transform: scale(1); }}
        14% {{ transform: scale(1.25); }}
        28% {{ transform: scale(1); }}
        42% {{ transform: scale(1.18); }}
        56% {{ transform: scale(1); }}
      }}
      @keyframes fadeInUp {{
        0% {{ opacity: 0; transform: translateY(16px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}
    </style>
    <div class="footer-wrap">
      <div class="footer-brand">AI Resume Shortlister</div>
      <div class="footer-version">v{version} · Built with Streamlit · spaCy · scikit-learn</div>
      <div class="footer-credit">
                Made with love by <span class="author">Himanshu Deshmukh</span>
      </div>
    </div>
    """
    components.html(html, height=180)
