"""
Processing pipeline for the AI Resume Shortlisting System.
Handles the full analyze → score → rank workflow.
"""

import re
from pathlib import Path

from parser import parse_resume
from ner import analyze_resume
from scorer import compute_tfidf_score, compute_final_score, rank_candidates
from skills_list import SKILLS
from constants import JD_MIN_LENGTH


def resolve_candidate_name(extracted_name: str, filename: str) -> str:
    """
    Determine the best candidate name: prefer NER-extracted name, fall back
    to a cleaned-up version of the filename.
    """
    if extracted_name and extracted_name != "Unknown":
        return extracted_name.strip()

    stem = Path(filename).stem
    stem = re.sub(r"[_\-]+", " ", stem)
    stem = re.sub(
        r"\b(resume|cv|candidate|profile|final|updated|latest)\b",
        " ",
        stem,
        flags=re.IGNORECASE,
    )
    stem = re.sub(r"\s+", " ", stem).strip(" -_")

    return stem.title() if stem else "Unknown"


def detect_skills_from_jd(jd_text: str) -> list[str]:
    """
    Auto-detect required skills from a job description using keyword matching.
    Returns a sorted list of matched skill names.
    """
    if not jd_text or len(jd_text.strip()) < JD_MIN_LENGTH:
        return []

    jd_lower = jd_text.lower()
    detected = sorted(
        skill for skill in SKILLS
        if re.search(r"\b" + re.escape(skill) + r"\b", jd_lower)
    )
    return detected


def process_resumes(
    jd_text: str,
    uploaded_files: list,
    required_skills: list[str],
    progress_callback=None,
) -> list[dict]:
    """
    Process a batch of uploaded resumes against a JD and required skills.

    Args:
        jd_text: Full job description text.
        uploaded_files: List of Streamlit UploadedFile objects.
        required_skills: Skills extracted from the JD.
        progress_callback: Optional callable(index, total, filename) for progress updates.

    Returns a ranked list of candidate result dicts.
    """
    results = []

    for idx, uploaded_file in enumerate(uploaded_files):
        if progress_callback:
            progress_callback(idx, len(uploaded_files), uploaded_file.name)

        resume_text = parse_resume(uploaded_file)

        if not resume_text.strip():
            continue

        analysis = analyze_resume(resume_text, required_skills)
        tfidf_score = compute_tfidf_score(jd_text, resume_text)
        final_score = compute_final_score(
            tfidf_score,
            analysis["skill_match_pct"],
            analysis["experience_years"],
        )
        candidate_name = resolve_candidate_name(analysis["name"], uploaded_file.name)

        results.append({
            "filename": uploaded_file.name,
            "name": candidate_name,
            "education": analysis["education"],
            "experience_years": analysis["experience_years"],
            "skills_found": analysis["skills_found"],
            "skills_missing": analysis["skills_missing"],
            "skill_match_pct": analysis["skill_match_pct"],
            "tfidf_score": tfidf_score,
            "final_score": final_score,
        })

    return rank_candidates(results)
