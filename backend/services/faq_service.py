"""
FAQ auto-update.

Every question asked in the chat is counted (all users and all roles together, so an admin's
question and an employee's identical question add up). When the same question has been asked
MORE THAN 15 times it is added to the FAQ page automatically.

Because the FAQ is visible to everyone, an answer is published only if it is safe for everyone:
the question is re-run on its own as the lowest-privilege role (Employee), and it is skipped when
that run is access-denied, is an action request, involves an individual employee's data, has no
verified citations, or relies on a document Employee cannot read. Published entries are also
hidden again if a source document is later deleted or restricted.
"""

import hashlib
import json
import os
import re
from typing import Any, Dict, List, Optional

from backend.database.repositories import FaqRepository

FAQ_THRESHOLD = int(os.getenv("FAQ_AUTO_THRESHOLD", "15"))   # published when asked MORE than this many times
RECHECK_EVERY = 15                                          # a skipped question is re-checked after this many more asks
FAQ_CATEGORY = "Most asked (auto-updated)"
PUBLIC_ROLE = "employee"                                    # the FAQ must be safe for the least-privileged role
MAX_ANSWER_CHARS = 6000

QUESTION_WORDS = {"what", "how", "when", "where", "who", "why", "which", "can", "could", "do", "does", "is", "are", "will", "should", "may"}

_repo: Optional[FaqRepository] = None


def _faq_repo() -> FaqRepository:
    global _repo
    if _repo is None:
        _repo = FaqRepository()
    return _repo


def normalize_question(text: str) -> str:
    """Lower-case, drop punctuation and extra spaces so 'Password policy?' and 'password  policy' match."""
    return " ".join(re.sub(r"[^\w\s]", " ", (text or "").lower()).split())[:300]


def question_key(text: str) -> str:
    return hashlib.sha1(normalize_question(text).encode("utf-8")).hexdigest()


def _tidy_question(text: str) -> str:
    """Readable heading for the FAQ: single spaces, no repeated '?', no ALL-CAPS shouting."""
    q = re.sub(r"\s+([?!.,])", r"\1", " ".join(text.split()))
    q = re.sub(r"([?!.])\1+", r"\1", q).strip()
    if q.isupper():
        q = q.lower()
    q = q[:1].upper() + q[1:]
    if q and q[-1] not in "?.!" and q.split()[0].lower() in QUESTION_WORDS:
        q += "?"
    return q[:300]


def _clean_answer(markdown: str) -> str:
    """Drop the per-answer 'Evidence Verification Summary' footer; keep the answer itself."""
    body = re.split(r"\n+#### Evidence Verification Summary", markdown or "")[0].strip()
    return body[:MAX_ANSWER_CHARS]


def _evaluate(question: str) -> Dict[str, Any]:
    """Run the question on its own as the public role and decide whether it is safe to publish."""
    from backend.graph.workflow import get_workflow   # imported late: avoids a circular import at start-up
    result = get_workflow().run(query=question, user_role=PUBLIC_ROLE, user_id="FAQ-AUTO", conversation_history=[])

    agents = [t.get("agent") for t in result.get("execution_trace", [])]
    citations = result.get("citations") or []

    if result.get("is_permission_denied"):
        return {"ok": False, "reason": "restricted for the public role"}
    if result.get("is_action_request"):
        return {"ok": False, "reason": "action request"}
    if "Employee Agent" in agents:
        return {"ok": False, "reason": "involves an individual employee's data"}
    if result.get("evidence_status") != "Verified" or not citations:
        return {"ok": False, "reason": "no verified answer with citations"}

    titles: List[str] = []
    sources: List[Dict[str, Any]] = []
    seen = set()
    for c in citations:
        title = c.get("document_name")
        if title and title not in titles:
            titles.append(title)
        key = (c.get("document_name"), c.get("section"))
        if key not in seen:
            seen.add(key)
            sources.append({"document_name": c.get("document_name"), "section": c.get("section"),
                            "version": c.get("version", "v1.0")})
    return {"ok": True, "answer": _clean_answer(result.get("final_response", "")), "sources": sources, "titles": titles}


def record_question(query: str) -> Optional[Dict[str, Any]]:
    """Count one ask of `query`; publish it to the FAQ once it has been asked more than the threshold."""
    key = question_key(query)
    if len(normalize_question(query)) < 3:
        return None
    repo = _faq_repo()
    row = repo.increment(key)
    count = row["ask_count"]

    if row["status"] == "published" or count <= FAQ_THRESHOLD:
        return row
    first_check = row["status"] == "counting"
    recheck = row["status"] == "skipped" and count >= row["last_evaluated_count"] + RECHECK_EVERY
    if not (first_check or recheck):
        return row

    verdict = _evaluate(query.strip())
    if verdict["ok"]:
        repo.mark_published(key, _tidy_question(query), verdict["answer"], verdict["sources"], verdict["titles"], count)
    else:
        repo.mark_skipped(key, verdict["reason"], count)
    return row


def get_auto_faq_items() -> List[Dict[str, Any]]:
    """Published entries for the FAQ page, minus any whose source documents are gone or no longer public."""
    from backend.rag.ingestion import get_ingestion_pipeline
    manifest = {m["title"]: m for m in get_ingestion_pipeline().ingested_manifest}
    items = []
    for row in _faq_repo().get_published():
        titles = json.loads(row.get("source_titles") or "[]")
        if not titles or any(t not in manifest or PUBLIC_ROLE not in manifest[t]["access_roles"] for t in titles):
            continue
        items.append({
            "category": FAQ_CATEGORY,
            "q": row["display_question"],
            "a": row["answer"],
            "auto": True,
            "asked": row["ask_count"],
            "sources": json.loads(row.get("sources") or "[]"),
        })
    return items
