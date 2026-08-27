"""
Lightweight SQLite-backed user store for the Flask frontend.

This is a functional auth layer for the AI Resume Shortlister tool/demo —
it stores users in a local SQLite database with hashed passwords. It is NOT
production-grade: there is no email verification, password reset, or rate
limiting. For a real deployment swap this module for Flask-Login + a real
auth provider.

A demo account is pre-seeded on first run so the app is immediately usable:
    email:    demo@shortlister.app
    password: demo1234
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash

# DB lives next to this file so it is easy to find and easy to wipe.
DB_PATH = Path(__file__).resolve().parent / "resume_shortlister.db"

DEMO_EMAIL = "demo@shortlister.app"
DEMO_PASSWORD = "demo1234"
DEMO_NAME = "Demo User"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    created_at    TEXT    NOT NULL
);
"""


def _connect() -> sqlite3.Connection:
    """Open a connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the users table and seed the demo account if absent."""
    with _connect() as conn:
        conn.execute(_SCHEMA)
        if not _find_by_email(conn, DEMO_EMAIL):
            conn.execute(
                "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (
                    DEMO_NAME,
                    DEMO_EMAIL,
                    generate_password_hash(DEMO_PASSWORD),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )


def _find_by_email(conn: sqlite3.Connection, email: str):
    return conn.execute(
        "SELECT * FROM users WHERE email = ?", (email.strip().lower(),)
    ).fetchone()


def create_user(name: str, email: str, password: str) -> dict:
    """
    Create a new user. Raises ValueError if the email is already registered.
    Returns the new user as a dict.
    """
    email = email.strip().lower()
    with _connect() as conn:
        if _find_by_email(conn, email):
            raise ValueError("An account with this email already exists.")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (
                name.strip(),
                email,
                generate_password_hash(password),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        row = conn.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(row)


def verify_user(email: str, password: str) -> dict | None:
    """
    Return the user dict if email + password match, else None.
    """
    with _connect() as conn:
        row = _find_by_email(conn, email)
        if row is None or not check_password_hash(row["password_hash"], password):
            return None
        return dict(row)