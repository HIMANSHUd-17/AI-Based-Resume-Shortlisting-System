"""
Configuration constants for the AI Resume Shortlisting System.
Centralizes UI config, scoring weights, and processing parameters.
"""

# ── App Metadata ──────────────────────────────────────────────────────────────
APP_NAME = "AI Resume Shortlister"
APP_ICON = "🧠"
APP_VERSION = "2.0"
APP_TAGLINE = "AI-Powered Candidate Ranking"
APP_DESCRIPTION = "Automatically shortlist candidates using AI-powered resume analysis. Combines NLP skill extraction with TF-IDF document similarity."

# ── Page Config ───────────────────────────────────────────────────────────────
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# ── Scoring Weights ───────────────────────────────────────────────────────────
WEIGHT_TFIDF = 0.5
WEIGHT_SKILL_MATCH = 0.4
EXPERIENCE_BONUS_HIGH = 0.10   # >= 3 years
EXPERIENCE_BONUS_LOW = 0.05    # >= 1 year
EXPERIENCE_THRESHOLD_HIGH = 3
EXPERIENCE_THRESHOLD_LOW = 1
SCORE_DECIMALS = 4
MAX_SCORE = 1.0

# ── Processing Parameters ─────────────────────────────────────────────────────
MAX_RESUME_CHARS = 1000        # chars used for NER name extraction
JD_MIN_LENGTH = 10             # minimum JD length for skill auto-detection

# ── Allowed File Types ────────────────────────────────────────────────────────
ALLOWED_EXTENSIONS = ["pdf", "docx"]

# ── Color Palette (for Plotly charts) ─────────────────────────────────────────
COLORS = {
    "primary": "#6366f1",
    "primary_dark": "#4f46e5",
    "primary_light": "#818cf8",
    "secondary": "#0ea5e9",
    "success": "#10b981",
    "success_dark": "#059669",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "surface": "#ffffff",
    "surface_alt": "#f8fafc",
    "background": "#f1f5f9",
    "text_primary": "#0f172a",
    "text_secondary": "#475569",
    "text_muted": "#94a3b8",
    "border": "#e2e8f0",
    "border_light": "#f1f5f9",
    "sidebar_bg": "#0f172a",
    "sidebar_text": "#f1f5f9",
    "gradient_start": "#6366f1",
    "gradient_mid": "#8b5cf6",
    "gradient_end": "#a78bfa",
}

CHART_COLORSCALE = [
    [0.0, "#ef4444"],
    [0.3, "#f59e0b"],
    [0.6, "#10b981"],
    [1.0, "#6366f1"],
]

# ── Education Mappings ────────────────────────────────────────────────────────
EDUCATION_LABELS = {
    "b.tech": "B.Tech",
    "b.e": "B.E.",
    "b.sc": "B.Sc",
    "m.tech": "M.Tech",
    "m.sc": "M.Sc",
    "mba": "MBA",
    "mca": "MCA",
    "bca": "BCA",
    "ph.d": "Ph.D",
    "phd": "Ph.D",
    "bachelor": "Bachelor's",
    "master": "Master's",
    "diploma": "Diploma",
    "b.com": "B.Com",
    "m.com": "M.Com",
    "be": "B.E.",
    "me": "M.E.",
}
