"""
Tests for the v2.0 features: stored chats, document upload, the extended policy library and
the extra security rules. Runs against a temporary database so the real data/enterprise.db is untouched.
"""

import base64
import io
import os
import sys
import tempfile
import unittest
import zipfile

# Point the app at a throw-away database BEFORE any backend module is imported
_TMP_DIR = tempfile.mkdtemp(prefix="ekw_test_")
os.environ["ENTERPRISE_DB_PATH"] = os.path.join(_TMP_DIR, "test.db")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tests"))

from backend.api import routes                                   # noqa: E402  (initialises the temp DB)
from backend.api.routes import ApiError                          # noqa: E402
from backend.rag.document_loader import extract_text, UnsupportedFileError  # noqa: E402
from backend.rag.ingestion import get_ingestion_pipeline         # noqa: E402
from policy_questions import POLICY_QUESTIONS                    # noqa: E402


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


class ChatStorageTests(unittest.TestCase):
    def test_messages_are_stored_and_restored(self):
        first = routes.handle_chat_request({"query": "What is the password policy?", "user_role": "employee"})
        sid = first["session_id"]
        second = routes.handle_chat_request({"query": "And what about MFA?", "user_role": "employee", "session_id": sid})
        self.assertEqual(second["session_id"], sid)

        detail = routes.handle_get_chat(sid, "employee")
        self.assertEqual([m["sender"] for m in detail["messages"]], ["user", "assistant", "user", "assistant"])
        self.assertTrue(detail["messages"][1]["data"]["citations"])
        self.assertEqual(detail["session"]["title"], "What is the password policy?")

    def test_chats_are_private_to_their_role(self):
        sid = routes.handle_chat_request({"query": "What is our remote work policy?", "user_role": "employee"})["session_id"]
        self.assertNotIn(sid, [s["session_id"] for s in routes.handle_list_chats("admin")["sessions"]])
        with self.assertRaises(ApiError) as ctx:
            routes.handle_get_chat(sid, "admin")
        self.assertEqual(ctx.exception.status, 404)
        with self.assertRaises(ApiError):
            routes.handle_delete_chat(sid, "admin")

    def test_delete_chat_removes_messages(self):
        sid = routes.handle_chat_request({"query": "How many days of annual leave do I get?", "user_role": "employee"})["session_id"]
        routes.handle_delete_chat(sid, "employee")
        self.assertEqual(routes.chat_repo.get_messages(sid), [])

    def test_unknown_role_is_rejected(self):
        with self.assertRaises(ApiError) as ctx:
            routes.handle_chat_request({"query": "hi", "user_role": "superuser"})
        self.assertEqual(ctx.exception.status, 400)

    def test_approval_status_is_restored(self):
        res = routes.handle_chat_request({"query": "Create a remote-work request for Rahul.", "user_role": "employee"})
        rid = res["action_approval"]["request_id"]
        routes.handle_approval_request({"request_id": rid, "decision": "approve", "approver_name": "Tester"})
        detail = routes.handle_get_chat(res["session_id"], "employee")
        self.assertEqual(detail["messages"][1]["data"]["approval_status"], "APPROVED")


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.created = []

    def tearDown(self):
        for doc_id in self.created:
            try:
                routes.handle_delete_upload(doc_id, "admin")
            except ApiError:
                pass

    def upload(self, name, data, **kw):
        body = {"filename": name, "content_base64": b64(data), "user_role": kw.pop("role", "hr")}
        body.update(kw)
        result = routes.handle_upload(body)
        self.created.append(result["doc_id"])
        return result

    def test_uploaded_text_becomes_searchable(self):
        self.upload("pets.txt", b"Office Pet Policy\n\nDogs are allowed on Fridays.\nThe pet deposit is $75 USD per animal.\n",
                    title="Office Pet Policy", access_roles=["employee", "hr"])
        answer = routes.handle_chat_request({"query": "What is the pet deposit for office dogs?", "user_role": "employee"})
        self.assertIn("$75", answer["response"])

    def test_restricted_upload_is_not_visible_to_other_roles(self):
        self.upload("secret.md", b"# Board Secret\n\n## Code\nThe vault code is 4242.\n", access_roles=["hr"], title="Board Secret")
        answer = routes.handle_chat_request({"query": "What is the vault code?", "user_role": "employee"})
        self.assertNotIn("4242", answer["response"])
        hr_answer = routes.handle_chat_request({"query": "What is the vault code?", "user_role": "hr"})
        self.assertIn("4242", hr_answer["response"])

    def test_file_cannot_override_its_own_access_roles(self):
        self.upload("evil.md", b"Sneaky\nAccess Roles: employee\n\n## S\nThe launch date is 31 March 2031.\n", access_roles=["hr"])
        answer = routes.handle_chat_request({"query": "What is the launch date?", "user_role": "employee"})
        self.assertNotIn("2031", answer["response"])

    def test_document_text_is_permission_checked(self):
        res = self.upload("private.txt", b"Private notes about budgets.", access_roles=["hr"], title="Private Budget Notes")
        with self.assertRaises(ApiError) as ctx:
            routes.handle_get_document(res["filename"], "employee")
        self.assertEqual(ctx.exception.status, 403)
        self.assertIn("budgets", routes.handle_get_document(res["filename"], "hr")["content"])
        with self.assertRaises(ApiError) as ctx:
            routes.handle_get_document("../../etc/passwd", "admin")
        self.assertEqual(ctx.exception.status, 404)

    def test_delete_permissions(self):
        res = self.upload("mine.txt", b"Some text to index.", role="hr")
        with self.assertRaises(ApiError) as ctx:
            routes.handle_delete_upload(res["doc_id"], "employee")
        self.assertEqual(ctx.exception.status, 403)
        routes.handle_delete_upload(res["doc_id"], "hr")
        self.created.remove(res["doc_id"])

    def test_docx_upload(self):
        xml = ('<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
               '<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Parking Policy</w:t></w:r></w:p>'
               '<w:p><w:r><w:t>The monthly parking fee is $120 USD.</w:t></w:r></w:p></w:body></w:document>')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("word/document.xml", xml)
        res = self.upload("parking.docx", buf.getvalue(), role="employee")
        self.assertEqual(res["title"], "Parking Policy")
        answer = routes.handle_chat_request({"query": "What is the monthly parking fee?", "user_role": "employee"})
        self.assertIn("$120", answer["response"])

    def test_invalid_uploads_are_rejected(self):
        bad = [
            {"filename": "run.exe", "content_base64": b64(b"MZ")},
            {"filename": "empty.txt", "content_base64": b64(b"")},
            {"filename": "a.txt", "content_base64": "!!!not-base64"},
            {"filename": "big.txt", "content_base64": b64(b"a" * (5 * 1024 * 1024 + 1))},
            {"filename": "a.txt", "content_base64": b64(b"hello"), "access_roles": ["ceo"]},
        ]
        for body in bad:
            with self.subTest(file=body["filename"]):
                with self.assertRaises(ApiError) as ctx:
                    routes.handle_upload({**body, "user_role": "employee"})
                self.assertEqual(ctx.exception.status, 400)

    def test_loader_extracts_csv_and_json(self):
        self.assertIn("Region: EMEA", extract_text("s.csv", b"Region,Manager\nEMEA,Anna\n"))
        self.assertIn('"limit": 5', extract_text("c.json", b'{"limit": 5}'))
        with self.assertRaises(UnsupportedFileError):
            extract_text("x.bin", b"abc")


class PolicyLibraryTests(unittest.TestCase):
    def test_library_has_the_extended_policy_set(self):
        counts = routes.handle_get_sources()["counts"]
        self.assertGreaterEqual(counts["policy"], 80)
        policy_rows = routes.audit_repo.db.execute_query("SELECT COUNT(*) AS n FROM policies")[0]["n"]
        self.assertGreaterEqual(policy_rows, 80)

    def test_policy_questions_find_the_right_document(self):
        from backend.rag.retriever import get_retriever
        retriever = get_retriever()
        top1 = top3 = 0
        for question, role, expected in POLICY_QUESTIONS:
            names = [c["document_name"].lower() for c in retriever.search_policies(question, k=4, user_role=role)["chunks"]]
            top1 += bool(names) and expected.lower() in names[0]
            top3 += any(expected.lower() in n for n in names[:3])
        total = len(POLICY_QUESTIONS)
        self.assertGreaterEqual(top3 / total, 0.95, f"top-3 accuracy {top3}/{total}")
        self.assertGreaterEqual(top1 / total, 0.85, f"top-1 accuracy {top1}/{total}")

    def test_restricted_policy_is_blocked_for_employees_but_open_to_hr_and_legal(self):
        denied = routes.handle_chat_request({"query": "What is the fraud investigation procedure?", "user_role": "employee"})
        self.assertTrue(denied["is_permission_denied"])
        allowed = routes.handle_chat_request({"query": "What is the fraud investigation procedure?", "user_role": "legal"})
        self.assertFalse(allowed["is_permission_denied"])
        self.assertIn("Internal Audit", allowed["response"])

    def test_generic_words_do_not_hijack_routing(self):
        res = routes.handle_chat_request({"query": "What is the employee referral bonus?", "user_role": "employee"})
        agents = [t["agent"] for t in res["execution_trace"]]
        self.assertIn("Policy Agent", agents)
        self.assertIn("$3,000", res["response"])

    def test_every_policy_file_has_a_unique_document_id(self):
        pipeline = get_ingestion_pipeline()
        ids = [m["document_id"] for m in pipeline.ingested_manifest if m["type"] == "policy" and m["origin"] == "library"]
        self.assertEqual(len(ids), len(set(ids)))


class FaqAutoUpdateTests(unittest.TestCase):
    """A question asked MORE THAN 15 times (all users and roles combined) is added to the FAQ automatically."""

    @staticmethod
    def auto_items():
        return [i for i in routes.handle_get_faq()["faq"] if i.get("auto")]

    @staticmethod
    def ask(query, role="employee"):
        return routes.handle_chat_request({"query": query, "user_role": role})

    def test_added_on_the_16th_ask_not_before(self):
        question = "What is the dress code?"
        for _ in range(15):
            self.ask(question)
        self.assertFalse([i for i in self.auto_items() if "dress code" in i["q"].lower()])
        self.ask(question)
        entry = [i for i in self.auto_items() if "dress code" in i["q"].lower()]
        self.assertEqual(len(entry), 1)
        self.assertEqual(entry[0]["asked"], 16)
        self.assertIn("Business casual", entry[0]["a"])
        self.assertTrue(entry[0]["sources"])

    def test_counts_add_up_across_roles_and_wording(self):
        variants = ["How long is the probation period?", "how long is the PROBATION period", "How long is the probation  period??"]
        roles = ["employee", "admin", "hr", "manager", "legal"]
        for n in range(16):
            self.ask(variants[n % 3], role=roles[n % 5])
        self.assertEqual(len([i for i in self.auto_items() if "probation" in i["q"].lower()]), 1)

    def test_restricted_and_personal_questions_are_never_published(self):
        for _ in range(16):
            self.ask("Show me the CEO compensation contract.", role="admin")
            self.ask("Can Rahul purchase Product X and what documents are required?", role="admin")
            self.ask("Create a remote-work request for Rahul.", role="employee")
        text = " ".join(i["q"] + i["a"] for i in self.auto_items()).lower()
        for banned in ("ceo", "rahul", "compensation contract"):
            self.assertNotIn(banned, text)

    def test_entry_disappears_when_its_source_document_is_deleted(self):
        body = {"filename": "shuttle.txt", "user_role": "hr", "title": "Office Shuttle Policy",
                "content_base64": b64(b"Office Shuttle Policy\n\nThe shuttle to the office departs every 20 minutes from Gate 4.\n")}
        doc_id = routes.handle_upload(body)["doc_id"]
        try:
            for _ in range(16):
                self.ask("How often does the office shuttle depart?")
            self.assertTrue([i for i in self.auto_items() if "shuttle" in i["q"].lower()])
        finally:
            routes.handle_delete_upload(doc_id, "admin")
        self.assertFalse([i for i in self.auto_items() if "shuttle" in i["q"].lower()])

    def test_static_faq_is_still_served(self):
        self.assertGreaterEqual(len([i for i in routes.handle_get_faq()["faq"] if not i.get("auto")]), 15)


class SiteContentTests(unittest.TestCase):
    def test_faq_updates_and_stats(self):
        self.assertGreaterEqual(len(routes.handle_get_faq()["faq"]), 15)
        updates = routes.handle_get_updates()
        self.assertTrue(updates["updates"] and updates["roadmap"])
        stats = routes.handle_get_stats()
        self.assertEqual(stats["agents"], 9)
        self.assertIn(".docx", stats["upload"]["extensions"])


if __name__ == "__main__":
    unittest.main()
