"""
Flask web frontend for the AI Resume Shortlister.

Serves the 3-page website (Landing -> Auth -> Dashboard) with Jinja2
templates and exposes the existing Python matching pipeline
(processing.py / parser.py / ner.py / scorer.py) as an API route the
"Run Match" button calls.

This is a demo-grade auth layer (see auth_store.py). Run with:
    .venv\\Scripts\\python.exe webapp.py
"""

import os
import json
import re
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import auth_store
from constants import ALLOWED_EXTENSIONS, APP_DESCRIPTION, APP_ICON, APP_NAME
from processing import detect_skills_from_jd, process_resumes
from skills_list import SKILLS

app = Flask(__name__)
# Fixed dev secret is fine for a local tool; override with SECRET_KEY in prod.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "ars-dev-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB total upload cap
MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB per resume, matching the old Streamlit app
auth_store.init_db()


# ── Session / auth helpers ────────────────────────────────────────────────────
def current_user() -> dict | None:
    """Return the logged-in user dict from the session, or None."""
    uid = session.get("user_id")
    if not uid:
        return None
    return {
        "id": uid,
        "name": session.get("user_name"),
        "email": session.get("user_email"),
    }


def login_required(view):
    """Gate a view behind a logged-in session; bounce to /auth otherwise."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("auth"))
        return view(*args, **kwargs)

    return wrapped


def _log_in(user: dict) -> None:
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]
    session.permanent = True


# ── Validation helpers ────────────────────────────────────────────────────────
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_signup(name: str, email: str, password: str, confirm: str) -> dict:
    errors = {}
    if not name or len(name.strip()) < 2:
        errors["name"] = "Please enter your full name."
    if not email or not _EMAIL_RE.match(email.strip()):
        errors["email"] = "Please enter a valid email address."
    if not password or len(password) < 6:
        errors["password"] = "Password must be at least 6 characters."
    elif password != confirm:
        errors["confirm"] = "Passwords do not match."
    return errors


def _validate_login(email: str, password: str) -> dict:
    errors = {}
    if not email:
        errors["email"] = "Please enter your email."
    if not password:
        errors["password"] = "Please enter your password."
    return errors


# ── File adapter for the existing pipeline ────────────────────────────────────
class _NamedFile:
    """
    processing.process_resumes() expects file objects exposing `.name` and
    `.read()`. Flask's FileStorage uses `.filename`, so we wrap each upload
    in this shim and leave the pipeline untouched.
    """

    def __init__(self, name: str, read):
        self.name = name
        self._read = read

    def read(self):
        return self._read()


def _collect_files() -> tuple[list, str | None]:
    """Pull valid resume uploads out of the request, returning (files, error)."""
    files = []
    for fs in request.files.getlist("files"):
        if not fs or not fs.filename:
            continue
        ext = fs.filename.rsplit(".", 1)[-1].lower() if "." in fs.filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            return [], f"Unsupported file type: {fs.filename} (PDF/DOCX only)."
        raw = fs.read()
        if not raw:
            continue
        if len(raw) > MAX_FILE_BYTES:
            return [], f"File too large (max 5 MB): {fs.filename}."
        files.append(_NamedFile(fs.filename, lambda raw=raw: raw))
    return files, None


# ── Routes ────────────────────────────────────────────────────────────────────
@app.before_request
def _load_user():
    g.user = current_user()


@app.context_processor
def _inject_globals():
    return {
        "app_name": APP_NAME,
        "app_icon": APP_ICON,
        "app_description": APP_DESCRIPTION,
        "current_user": g.get("user"),
        "current_year": datetime.now().year,
        "skill_catalog": sorted(SKILLS),
    }


@app.get("/")
def landing():
    return render_template("landing.html", page="landing")


@app.get("/auth")
def auth():
    if current_user():
        return redirect(url_for("dashboard"))
    return render_template("auth.html", page="auth", mode=request.args.get("mode", "signin"))


@app.post("/auth/signup")
def auth_signup():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "")
    email = data.get("email", "")
    password = data.get("password", "")
    confirm = data.get("confirm", "")
    errors = _validate_signup(name, email, password, confirm)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 422
    try:
        user = auth_store.create_user(name, email, password)
    except ValueError as exc:
        return jsonify({"ok": False, "errors": {"email": str(exc)}}), 409
    _log_in(user)
    return jsonify({"ok": True, "redirect": url_for("dashboard")})


@app.post("/auth/login")
def auth_login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "")
    password = data.get("password", "")
    errors = _validate_login(email, password)
    if errors:
        return jsonify({"ok": False, "errors": errors}), 422
    user = auth_store.verify_user(email, password)
    if user is None:
        return jsonify(
            {"ok": False, "errors": {"form": "Invalid email or password."}}
        ), 401
    _log_in(user)
    return jsonify({"ok": True, "redirect": url_for("dashboard")})


@app.post("/auth/logout")
def auth_logout():
    session.clear()
    return jsonify({"ok": True, "redirect": url_for("landing")})


@app.get("/app")
@login_required
def dashboard():
    return render_template("app.html", page="app")


@app.post("/api/match")
@login_required
def api_match():
    jd_text = request.form.get("job_description", "").strip()
    files, file_error = _collect_files()
    try:
        candidate_limit = max(1, int(request.form.get("candidate_limit", "1")))
    except (TypeError, ValueError):
        candidate_limit = 1

    if not jd_text:
        return jsonify({"ok": False, "error": "Please paste a job description first."}), 400
    if file_error:
        return jsonify({"ok": False, "error": file_error}), 400
    if not files:
        return jsonify({"ok": False, "error": "Please add at least one resume."}), 400

    jd_skills = detect_skills_from_jd(jd_text)
    try:
        requested_skills = json.loads(request.form.get("skills", "[]"))
    except (TypeError, json.JSONDecodeError):
        requested_skills = []
    selected_skills = sorted({
        str(skill).strip()
        for skill in requested_skills
        if str(skill).strip() in SKILLS
    })
    required_skills = sorted(set(jd_skills).union(selected_skills))

    if not required_skills:
        return jsonify(
            {
                "ok": False,
                "error": (
                    "No known skills detected in the job description. "
                    "Add a skill below the job description or include keywords "
                    "such as Python, SQL, or AWS."
                ),
            }
        ), 422

    results = process_resumes(jd_text, files, required_skills)[:candidate_limit]

    if not results:
        return jsonify(
            {"ok": False, "error": "None of the uploaded files could be read as resumes."}
        ), 422

    return jsonify(
        {
            "ok": True,
            "results": results,
            "jd_skills": required_skills,
            "total_files": len(files),
            "processed": len(results),
            "candidate_limit": candidate_limit,
        }
    )


if __name__ == "__main__":
    auth_store.init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)