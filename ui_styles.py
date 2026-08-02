"""
UI Styles for the AI Resume Shortlisting System.
Complete CSS stylesheet with modern, polished design.
"""

from constants import COLORS


def build_css() -> str:
    """Return the full CSS stylesheet as a string."""
    return f"""
<style>
/* ── Fonts ──────────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Base ───────────────────────────────────────────────────────────── */
* {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}

/* ── Hide Streamlit branding ────────────────────────────────────────────────── */
#MainMenu {{visibility: hidden;}}
header {{visibility: hidden;}}
footer {{visibility: hidden;}}

/* ── Main container ─────────────────────────────────────────────────────────── */
:root {{
    --app-bg-start: {COLORS["background"]};
    --app-bg-mid: #e8ecf1;
    --app-bg-end: {COLORS["surface_alt"]};
    --app-surface: {COLORS["surface"]};
    --app-surface-alt: {COLORS["surface_alt"]};
    --app-text-primary: {COLORS["text_primary"]};
    --app-text-secondary: {COLORS["text_secondary"]};
    --app-text-muted: {COLORS["text_muted"]};
    --app-border: {COLORS["border"]};
    --app-border-light: {COLORS["border_light"]};
    color-scheme: light;
}}

:root[data-app-theme="dark"] {{
    --app-bg-start: #0b1220;
    --app-bg-mid: #111827;
    --app-bg-end: #1f2937;
    --app-surface: #111827;
    --app-surface-alt: #1f2937;
    --app-text-primary: #e2e8f0;
    --app-text-secondary: #cbd5e1;
    --app-text-muted: #94a3b8;
    --app-border: #334155;
    --app-border-light: #1e293b;
    color-scheme: dark;
}}

@media (prefers-color-scheme: dark) {{
    :root:not([data-app-theme="light"]) {{
        --app-bg-start: #0b1220;
        --app-bg-mid: #111827;
        --app-bg-end: #1f2937;
        --app-surface: #111827;
        --app-surface-alt: #1f2937;
        --app-text-primary: #e2e8f0;
        --app-text-secondary: #cbd5e1;
        --app-text-muted: #94a3b8;
        --app-border: #334155;
        --app-border-light: #1e293b;
        color-scheme: dark;
    }}
}}

.stApp {{
    background: linear-gradient(135deg, var(--app-bg-start) 0%, var(--app-bg-mid) 50%, var(--app-bg-end) 100%);
    color: var(--app-text-primary);
}}

/* ── Sidebar ────────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COLORS["sidebar_bg"]} 0%, #1e293b 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
    padding-top: 1rem;
}}

[data-testid="stSidebar"] .stMarkdown {{
    color: {COLORS["sidebar_text"]};
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li {{
    color: {COLORS["sidebar_text"]} !important;
}}

[data-testid="stSidebar"] .stMarkdown p {{
    color: #94a3b8;
    font-size: 0.85rem;
    line-height: 1.6;
}}

[data-testid="stSidebar"] .stMarkdown strong {{
    color: #ffffff;
}}

/* ── Sidebar feature list ───────────────────────────────────────────────────── */
.sidebar-feature {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 8px;
    transition: all 0.2s ease;
}}

.sidebar-feature:hover {{
    background: rgba(255,255,255,0.08);
    border-color: rgba(99,102,241,0.3);
    transform: translateX(3px);
}}

.sidebar-feature-number {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["primary_light"]});
    color: white;
    font-size: 11px;
    font-weight: 700;
    margin-right: 10px;
    flex-shrink: 0;
}}

.sidebar-feature-text {{
    color: #cbd5e1;
    font-size: 0.82rem;
    line-height: 1.5;
}}

/* ── Sidebar badges ─────────────────────────────────────────────────────────── */
.sidebar-badge {{
    display: inline-block;
    background: rgba(99,102,241,0.15);
    color: {COLORS["primary_light"]};
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 500;
    margin: 2px 3px;
    border: 1px solid rgba(99,102,241,0.2);
}}

/* ── Gradient title ─────────────────────────────────────────────────────────── */
.page-header {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 0.5rem;
}}

.page-header-main {{
    flex: 1;
    min-width: 0;
}}

.page-credit {{
    align-self: flex-start;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(99, 102, 241, 0.08);
    border: 1px solid rgba(99, 102, 241, 0.18);
    color: {COLORS["text_secondary"]};
    font-size: 0.82rem;
    font-weight: 600;
    white-space: nowrap;
}}

.page-credit strong {{
    color: {COLORS["primary"]};
    font-weight: 800;
}}

.gradient-title {{
    background: linear-gradient(135deg, {COLORS["gradient_start"]}, {COLORS["gradient_mid"]}, {COLORS["gradient_end"]});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 0.1rem;
    letter-spacing: -0.02em;
}}

.gradient-subtitle {{
    color: {COLORS["text_secondary"]};
    font-size: 1.05rem;
    font-weight: 400;
    margin-top: 0;
}}

/* ── Section headers ────────────────────────────────────────────────────────── */
.section-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}}

.section-header-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["primary_light"]});
    color: white;
    font-size: 16px;
    flex-shrink: 0;
}}

.section-header h3 {{
    margin: 0;
    font-weight: 700;
    color: {COLORS["text_primary"]};
}}

/* ── Glass card ─────────────────────────────────────────────────────────────── */
.glass-card {{
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.85);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow:
        0 1px 3px rgba(0,0,0,0.04),
        0 6px 16px rgba(0,0,0,0.04);
    transition: all 0.25s ease;
}}

.glass-card:hover {{
    box-shadow:
        0 4px 12px rgba(0,0,0,0.06),
        0 12px 32px rgba(0,0,0,0.06);
    transform: translateY(-2px);
}}

.glass-card-static {{
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.85);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow:
        0 1px 3px rgba(0,0,0,0.04),
        0 6px 16px rgba(0,0,0,0.04);
}}

/* ── Metric cards ───────────────────────────────────────────────────────────── */
.metric-card {{
    background: {COLORS["surface"]};
    border-radius: 14px;
    padding: 20px 22px;
    border: 1px solid {COLORS["border"]};
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}}

.metric-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}}

.metric-card-success::before {{ background: linear-gradient(90deg, #10b981, #34d399); }}
.metric-card-primary::before {{ background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["primary_light"]}); }}
.metric-card-warning::before {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}

.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}

.metric-label {{
    font-size: 0.78rem;
    font-weight: 600;
    color: {COLORS["text_muted"]};
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
}}

.metric-value {{
    font-size: 1.7rem;
    font-weight: 800;
    color: {COLORS["text_primary"]};
    line-height: 1.2;
}}

.metric-sub {{
    font-size: 0.82rem;
    color: {COLORS["text_secondary"]};
    margin-top: 4px;
}}

/* ── Candidate cards ────────────────────────────────────────────────────────── */
.candidate-card {{
    background: {COLORS["surface"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 16px;
    padding: 0;
    margin-bottom: 16px;
    overflow: hidden;
    transition: all 0.25s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}

.candidate-card:hover {{
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    transform: translateY(-2px);
    border-color: rgba(99,102,241,0.25);
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

.rank-1 {{
    background: linear-gradient(135deg, #f59e0b, #f97316);
    box-shadow: 0 4px 14px rgba(245,158,11,0.35);
}}

.rank-2 {{
    background: linear-gradient(135deg, #94a3b8, #64748b);
    box-shadow: 0 4px 14px rgba(148,163,184,0.3);
}}

.rank-3 {{
    background: linear-gradient(135deg, #b45309, #d97706);
    box-shadow: 0 4px 14px rgba(180,83,9,0.25);
}}

.rank-default {{
    background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["primary_light"]});
    box-shadow: 0 4px 14px rgba(99,102,241,0.2);
}}

.candidate-name {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {COLORS["text_primary"]};
    margin: 0;
}}

.candidate-meta {{
    font-size: 0.82rem;
    color: {COLORS["text_muted"]};
    margin-top: 2px;
}}

.candidate-score-badge {{
    margin-left: auto;
    text-align: center;
}}

.score-number {{
    font-size: 1.6rem;
    font-weight: 800;
    line-height: 1;
}}

.score-label {{
    font-size: 0.7rem;
    font-weight: 500;
    color: {COLORS["text_muted"]};
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

.candidate-card-body {{
    padding: 0 24px 20px;
}}

/* ── Score bar ──────────────────────────────────────────────────────────────── */
.score-bar-track {{
    height: 6px;
    background: {COLORS["border_light"]};
    border-radius: 3px;
    overflow: hidden;
    margin: 12px 0;
}}

.score-bar-fill {{
    height: 100%;
    border-radius: 3px;
    transition: width 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

.score-bar-high {{ background: linear-gradient(90deg, #10b981, #34d399); }}
.score-bar-mid  {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}
.score-bar-low  {{ background: linear-gradient(90deg, #ef4444, #f87171); }}

/* ── Skills pills ───────────────────────────────────────────────────────────── */
.skill-pill-found {{
    display: inline-block;
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    color: #065f46;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 500;
    margin: 2px 3px;
    border: 1px solid rgba(16,185,129,0.15);
    transition: all 0.15s ease;
}}

.skill-pill-found:hover {{
    background: linear-gradient(135deg, #a7f3d0, #6ee7b7);
    transform: scale(1.03);
}}

.skill-pill-missing {{
    display: inline-block;
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    color: #991b1b;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 500;
    margin: 2px 3px;
    border: 1px solid rgba(239,68,68,0.12);
    transition: all 0.15s ease;
}}

.skill-pill-missing:hover {{
    background: linear-gradient(135deg, #fecaca, #fca5a5);
    transform: scale(1.03);
}}

.skill-more-badge {{
    display: inline-block;
    background: {COLORS["border_light"]};
    color: {COLORS["text_muted"]};
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    margin: 2px 3px;
    border: 1px dashed {COLORS["border"]};
}}

/* ── Info pills (education, experience) ─────────────────────────────────────── */
.info-pill {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: {COLORS["surface_alt"]};
    border: 1px solid {COLORS["border"]};
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    color: {COLORS["text_secondary"]};
}}

/* ── Tabs ───────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: var(--app-surface);
    border-radius: 12px;
    padding: 6px;
    border: 1px solid {COLORS["border"]};
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 0.88rem;
    border: none;
    transition: all 0.2s ease;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["primary_light"]}) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.25);
}}

.stTabs [data-baseweb="tab-highlight"] {{
    display: none;
}}

.stTabs [data-baseweb="tab-border"] {{
    display: none;
}}

/* ── Tables ─────────────────────────────────────────────────────────────────── */
table {{
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}

table thead {{
    background: linear-gradient(135deg, {COLORS["sidebar_bg"]}, #1e293b);
    color: white;
}}

table th {{
    padding: 14px 16px;
    text-align: left;
    font-weight: 600;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}}

table td {{
    padding: 12px 16px;
    border-bottom: 1px solid {COLORS["border"]};
    font-size: 0.88rem;
}}

table tbody tr {{
    transition: background 0.15s ease;
}}

table tbody tr:hover {{
    background: rgba(99,102,241,0.03);
}}

table tbody tr:last-child td {{
    border-bottom: none;
}}

/* ── Buttons ────────────────────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["primary_light"]}) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em;
    box-shadow: 0 4px 14px rgba(99,102,241,0.3) !important;
    transition: all 0.25s ease !important;
}}

.stButton > button[kind="primary"]:hover {{
    box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
    transform: translateY(-1px);
}}

/* ── Progress bar ───────────────────────────────────────────────────────────── */
.stProgress > div > div {{
    background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["primary_light"]}) !important;
    border-radius: 4px !important;
}}

/* ── Download button ────────────────────────────────────────────────────────── */
.stDownloadButton > button {{
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: 2px solid {COLORS["primary"]} !important;
    color: {COLORS["primary"]} !important;
    transition: all 0.2s ease !important;
}}

.stDownloadButton > button:hover {{
    background: {COLORS["primary"]} !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.25) !important;
}}

/* ── Divider with label ─────────────────────────────────────────────────────── */
.divider-labeled {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 28px 0;
}}

.divider-labeled::before,
.divider-labeled::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, {COLORS["border"]}, transparent);
}}

.divider-labeled span {{
    font-size: 0.78rem;
    font-weight: 600;
    color: {COLORS["text_muted"]};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    white-space: nowrap;
}}

/* ── Empty state ────────────────────────────────────────────────────────────── */
.empty-state {{
    text-align: center;
    padding: 60px 24px;
    color: {COLORS["text_muted"]};
}}

.empty-state-icon {{
    font-size: 3rem;
    margin-bottom: 16px;
    opacity: 0.5;
}}

.empty-state h4 {{
    color: {COLORS["text_secondary"]};
    margin-bottom: 8px;
}}

/* ── Top candidate highlight ────────────────────────────────────────────────── */
.top-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: linear-gradient(135deg, #f59e0b, #f97316);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    box-shadow: 0 2px 8px rgba(245,158,11,0.3);
}}

/* ── JD preview ─────────────────────────────────────────────────────────────── */
.jd-preview {{
    background: {COLORS["surface_alt"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: {COLORS["text_secondary"]};
    line-height: 1.6;
    max-height: 80px;
    overflow: hidden;
    margin-top: 8px;
}}

/* ── Footer ─────────────────────────────────────────────────────────────────── */
.footer {{
    text-align: center;
    padding: 24px 0 12px;
    color: {COLORS["text_muted"]};
    font-size: 0.82rem;
}}

.footer-brand {{
    font-weight: 700;
    color: {COLORS["primary"]};
}}

.footer-credit {{
    margin-top: 16px;
    padding: 12px 24px;
    display: inline-block;
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08));
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 30px;
    font-size: 0.92rem;
    font-weight: 600;
    color: {COLORS["text_secondary"]};
    letter-spacing: 0.01em;
    transition: all 0.3s ease;
}}

.footer-credit:hover {{
    background: linear-gradient(135deg, rgba(99,102,241,0.14), rgba(139,92,246,0.14));
    border-color: rgba(99,102,241,0.35);
    box-shadow: 0 4px 18px rgba(99,102,241,0.15);
    transform: translateY(-2px);
}}

.footer-heart {{
    display: inline-block;
    font-size: 1.1em;
    animation: heartbeat 1.5s ease-in-out infinite;
}}

@keyframes heartbeat {{
    0%, 100% {{ transform: scale(1); }}
    15% {{ transform: scale(1.2); }}
    30% {{ transform: scale(1); }}
    45% {{ transform: scale(1.15); }}
    60% {{ transform: scale(1); }}
}}

.footer-author {{
    background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["primary_light"]}, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    font-size: 1.05em;
}}

/* ── Success / Info / Warning overrides ─────────────────────────────────────── */
.stAlert {{
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}}

/* ── File uploader ──────────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {{
    border-radius: 12px;
}}

[data-testid="stFileUploaderDropzone"] {{
    justify-content: center;
    text-align: center;
}}

[data-testid="stFileUploaderDropzone"] button {{
    width: 100%;
    justify-content: center;
}}

[data-testid="stFileUploaderDropzone"] button > div {{
    width: 100%;
    justify-content: center;
}}

[data-testid="stFileUploaderDropzone"] [data-testid="stIconMaterial"] {{
    display: none;
}}

[data-testid="stFileUploaderDropzone"] .stMarkdownContainer p {{
    margin: 0;
}}

/* ── Scrollbar styling ──────────────────────────────────────────────────────── */
::-webkit-scrollbar {{
    width: 6px;
}}

::-webkit-scrollbar-track {{
    background: transparent;
}}

::-webkit-scrollbar-thumb {{
    background: #cbd5e1;
    border-radius: 3px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: #94a3b8;
}}

/* ── Theme switcher + adaptive surfaces ─────────────────────────────────────── */
#ars-theme-toggle-btn {{
    position: fixed;
    top: 12px;
    right: 14px;
    z-index: 10000;
    border: 1px solid var(--app-border);
    border-radius: 999px;
    padding: 6px 12px;
    background: var(--app-surface);
    color: var(--app-text-primary);
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.14);
}}

#ars-theme-toggle-btn:hover {{
    border-color: {COLORS["primary"]};
}}

[data-testid="stAppViewContainer"] .main,
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main label,
[data-testid="stAppViewContainer"] .main h1,
[data-testid="stAppViewContainer"] .main h2,
[data-testid="stAppViewContainer"] .main h3,
[data-testid="stAppViewContainer"] .main h4 {{
    color: var(--app-text-primary);
}}

.metric-card,
.stTabs [data-baseweb="tab-list"],
[data-testid="stFileUploaderDropzone"] {{
    background: var(--app-surface) !important;
    border-color: var(--app-border) !important;
}}

.metric-label,
.score-label,
.divider-labeled span,
.empty-state,
.jd-preview {{
    color: var(--app-text-muted) !important;
}}

.metric-value,
.candidate-name,
.section-header h3,
.empty-state h4 {{
    color: var(--app-text-primary) !important;
}}

.metric-sub,
.gradient-subtitle,
.page-credit,
.info-pill,
.jd-preview {{
    color: var(--app-text-secondary) !important;
}}

.metric-card,
.candidate-card,
.info-pill,
.jd-preview,
table td {{
    border-color: var(--app-border) !important;
}}

.metric-card,
.candidate-card,
table tbody tr {{
    background: var(--app-surface);
}}

table thead {{
    background: linear-gradient(135deg, #1e293b, #334155);
}}

.stTextArea textarea,
.stMultiSelect div[data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] > div {{
    background: var(--app-surface) !important;
    color: var(--app-text-primary) !important;
    border-color: var(--app-border) !important;
}}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] div,
[data-testid="stTextArea"] label p,
[data-testid="stFileUploader"] label p,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] div,
[data-testid="stMarkdownContainer"] p {{
    color: var(--app-text-secondary) !important;
}}

[data-testid="stTextArea"] textarea,
[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] section,
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] * {{
    background: var(--app-surface) !important;
    color: var(--app-text-secondary) !important;
    border-color: var(--app-border) !important;
}}

[data-testid="stMetricValue"] div,
[data-testid="stMetricValue"] p {{
    color: var(--app-text-primary) !important;
}}

/* ── Responsive adjustments ─────────────────────────────────────────────────── */
@media (max-width: 768px) {{
    .gradient-title {{
        font-size: 1.6rem;
    }}
    .candidate-card-top {{
        flex-wrap: wrap;
    }}
}}
</style>
"""
