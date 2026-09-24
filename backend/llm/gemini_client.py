import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = None
        self.enabled = False
        self.error = None

        if not self.api_key:
            self.error = "GEMINI_API_KEY is not set."
            return

        try:
            import google.generativeai as genai  # type: ignore
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model_name)
            self.enabled = True
        except Exception as exc:  # pragma: no cover - runtime dependency only
            self.error = str(exc)
            self.enabled = False

    def generate(self, prompt: str) -> str:
        if not self.enabled or self.client is None:
            return ""
        try:
            response = self.client.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "max_output_tokens": 900,
                },
            )
            return getattr(response, "text", "") or ""
        except Exception as exc:  # pragma: no cover - runtime dependency only
            self.error = str(exc)
            return ""

    def build_policy_prompt(self, query: str, chunks: List[Dict[str, Any]], role: str) -> str:
        docs = []
        for idx, chunk in enumerate(chunks[:6], 1):
            docs.append(
                f"[{idx}] Document: {chunk.get('document_name', 'Unknown')} | "
                f"Section: {chunk.get('section', 'Overview')}\n"
                f"{chunk.get('content', '').strip()}\n"
            )
        context = "\n\n".join(docs) if docs else "No retrieval context found."

        return (
            "You are the enterprise policy assistant for Acme. "
            "Answer only from the provided context. Never invent policy language, policy numbers, or document wording. "
            "If the answer is not present in the citations, say you do not have enough evidence.\n\n"
            f"User role: {role}\n"
            f"Question: {query}\n\n"
            "Retrieval context:\n"
            f"{context}\n\n"
            "Return: 1) a concise answer in plain language, 2) the exact policy/doc citations used, 3) a short evidence note."
        )


def get_gemini_client() -> GeminiClient:
    return GeminiClient()
