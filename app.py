#   cd C:\Users\himan\Documents\GitHub\AI-Based-Resume-Shortlisting-System
#  .\.venv\Scripts\python.exe -m streamlit run .\app.py
import streamlit as st
import streamlit.components.v1 as components

from constants import APP_NAME, APP_ICON, APP_VERSION, APP_DESCRIPTION, PAGE_LAYOUT, SIDEBAR_STATE
from skills_list import SKILLS
from ui_styles import build_css
from ui_components import (
    render_page_header,
    render_section_header,
    render_divider,
    render_metrics_row,
    render_rankings,
    render_chart,
    render_export,
    render_footer,
)
from processing import detect_skills_from_jd, process_resumes


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
        height=1,
        width=1,
    )

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(build_css(), unsafe_allow_html=True)
render_theme_toggle()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_NAME}")
    st.markdown(f"*{APP_DESCRIPTION}*\n")

    st.markdown("---")

    st.markdown("### How it works")

    steps = [
        ("Paste the job description in the left panel"),
        ("Select required skills (auto-detected from JD)"),
        ("Upload candidate resumes (PDF / DOCX)"),
        ("Click **Rank Resumes** to run the analysis"),
        ("View rankings, charts, and download CSV"),
    ]

    steps_html = ""
    for i, text in enumerate(steps, 1):
        steps_html += (
            f'<div class="sidebar-feature">'
            f'  <span class="sidebar-feature-number">{i}</span>'
            f'  <span class="sidebar-feature-text">{text}</span>'
            f'</div>'
        )
    st.markdown(steps_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Built with")
    badges_html = (
        '<span class="sidebar-badge">spaCy</span>'
        '<span class="sidebar-badge">scikit-learn</span>'
        '<span class="sidebar-badge">Streamlit</span>'
        '<span class="sidebar-badge">Plotly</span>'
    )
    st.markdown(badges_html, unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state["results"] = []
if "jd_text_state" not in st.session_state:
    st.session_state["jd_text_state"] = ""
if "detected_skills_state" not in st.session_state:
    st.session_state["detected_skills_state"] = []
if "selected_skills" not in st.session_state:
    st.session_state["selected_skills"] = []

# ── Main Content ──────────────────────────────────────────────────────────────
render_page_header()

# Two-column input layout
col_jd, col_upload = st.columns([3, 2])

# ── Left column: Job Description ──────────────────────────────────────────────
with col_jd:
    render_section_header("📋", "Job Description")

    jd_text = st.text_area(
        "Paste the Job Description here:",
        value=st.session_state["jd_text_state"],
        height=220,
        placeholder=(
            "Paste your job description here... "
            "(e.g., we need a Python developer with Machine Learning expertise, "
            "SQL, Django, and AWS experience...)"
        ),
        key="jd_input",
    )

    st.session_state["jd_text_state"] = jd_text

    # Auto-detect skills
    detected_skills = detect_skills_from_jd(jd_text) if jd_text else st.session_state["detected_skills_state"]

    if detected_skills:
        st.success(f"✅ Auto-detected {len(detected_skills)} skill(s) — pre-selected below")
        if st.session_state["detected_skills_state"] != detected_skills:
            st.session_state["selected_skills"] = detected_skills
    else:
        st.info("💡 Paste your job description above to auto-detect required skills")

    st.session_state["detected_skills_state"] = detected_skills

    skills_key = f"skills_select_{len(detected_skills)}_{hash(tuple(detected_skills))}"
    required_skills = st.multiselect(
        "Required Skills (pre-selected from your JD):",
        options=sorted(SKILLS),
        default=detected_skills if detected_skills else [],
        key=skills_key,
    )

# ── Right column: Upload Resumes ──────────────────────────────────────────────
with col_upload:
    render_section_header("📁", "Upload Resumes")

    uploaded_files = st.file_uploader(
        "Choose PDF or DOCX files:",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        max_upload_size=5,
        key="file_uploader",
    )

    if uploaded_files and len(uploaded_files) > 100:
        st.warning(f"⚠️ Only the first 100 files will be processed ({len(uploaded_files)} uploaded).")
        uploaded_files = uploaded_files[:100]

    st.metric("📄 Files Uploaded", len(uploaded_files))
    st.info("✅ Supports: PDF, DOCX formats\n💾 Max file size: 5MB\n📦 Max files: 100")

# ── Action Button ─────────────────────────────────────────────────────────────
render_divider()
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    process_button = st.button(
        "🚀  Rank Resumes",
        use_container_width=True,
        type="primary",
        key="process_btn",
    )

# ── Processing ────────────────────────────────────────────────────────────────
if process_button:
    if not jd_text.strip():
        st.error("❌ Please enter a Job Description")
    elif not uploaded_files:
        st.error("❌ Please upload at least one resume")
    elif not required_skills:

    
        st.error("❌ Please select at least one required skill")
    else:
        progress_bar = st.progress(0)
        status_placeholder = st.empty()

        def _update_progress(idx: int, total: int, filename: str):
            progress_bar.progress((idx + 1) / total)
            status_placeholder.write(f"📄 Analyzing: {filename} ({idx + 1}/{total})")

        ranked_results = process_resumes(
            jd_text, uploaded_files, required_skills,
            progress_callback=_update_progress,
        )

        st.session_state["results"] = ranked_results

        progress_bar.empty()
        status_placeholder.empty()

        st.success(f"✅ Successfully analyzed {len(ranked_results)} resume(s)")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state["results"]:
    results = st.session_state["results"]

    render_divider("Results")
    render_section_header("📊", "Analysis Results")
    render_metrics_row(results)

    tab_rankings, tab_chart = st.tabs(["📊 Rankings", "📈 Score Chart"])

    with tab_rankings:
        render_rankings(results)

    with tab_chart:
        render_chart(results)

    render_export(results)

# ── Footer ────────────────────────────────────────────────────────────────────
render_footer(APP_VERSION)
