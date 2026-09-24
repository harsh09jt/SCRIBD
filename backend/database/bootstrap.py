"""
Database bootstrap.
Runs on every start-up (safe to run repeatedly):
  1. creates any missing tables (including chat history and uploaded documents),
  2. seeds demo data the first time the database is empty,
  3. registers every policy file found in data/policies in the `policies` catalogue table.
"""

import os
from backend.database.connection import get_db, DATA_DIR
from backend.database.models import SCHEMA_SQL
from backend.database.repositories import PolicyRepository

POLICIES_DIR = os.path.join(DATA_DIR, "policies")


def _parse_policy_file(path: str):
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    title = ""
    meta = {}
    for idx, line in enumerate(lines[:20]):
        stripped = line.strip()
        if idx == 0 and stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        if not stripped or stripped.startswith("##"):
            break
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip().lower().replace(" ", "_")] = val.strip()
    return title, meta


def sync_policy_catalogue() -> int:
    """Add any policy file that is not yet listed in the policies table. Returns how many were added."""
    if not os.path.isdir(POLICIES_DIR):
        return 0
    repo = PolicyRepository()
    added = 0
    for fname in sorted(os.listdir(POLICIES_DIR)):
        if not fname.endswith(".md"):
            continue
        title, meta = _parse_policy_file(os.path.join(POLICIES_DIR, fname))
        policy_id = meta.get("document_id")
        if not policy_id or not title:
            continue
        version = meta.get("version", "1.0")
        if not version.lower().startswith("v"):
            version = f"v{version}"
        if repo.insert_if_missing(
            policy_id=policy_id,
            title=title,
            department=meta.get("department", "Corporate"),
            version=version,
            last_updated=meta.get("last_updated", "2026-08-01"),
            file_path=f"data/policies/{fname}",
        ):
            added += 1
    return added


def initialize() -> None:
    db = get_db()
    db.init_schema(SCHEMA_SQL)

    # First run on an empty database: load the demo employees / products / contracts
    if not db.execute_query("SELECT employee_id FROM employees LIMIT 1"):
        from backend.database.seed_data import seed_database
        seed_database()

    added = sync_policy_catalogue()
    if added:
        print(f"Policy catalogue: registered {added} new policy document(s).")
