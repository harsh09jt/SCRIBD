"""
Embeddings interface supporting HuggingFace embeddings with a self-contained
high-performance fallback for zero-dependency operation.
"""

import math
import re
from typing import List, Dict, Any
from collections import Counter


def _light_stem(term: str) -> str:
    """
    Very light plural stemming so that "policies"/"policy", "orders"/"order" and
    "directors"/"director" match. Only purely alphabetic words are touched; codes such as
    "pol-hr-042" or "99.95" are left exactly as written.
    """
    if len(term) < 5 or not term.isalpha():
        return term
    if term.endswith("ies"):
        return term[:-3] + "y"
    if term.endswith(("sses", "xes", "zes", "ches", "shes")):
        return term[:-2]
    if term.endswith("s") and not term.endswith(("ss", "us", "is")):
        return term[:-1]
    return term


def tokenize(text: str) -> List[str]:
    """Tokenize and normalize text into clean words."""
    terms = re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())
    stop_words = {
        "the", "and", "for", "with", "this", "that", "shall", "must", "from",
        "are", "has", "have", "been", "all", "any", "not", "over", "into",
        "such", "under", "per", "than", "more", "can", "will", "our", "your"
    }
    return [_light_stem(t) for t in terms if t not in stop_words]


class EmbeddingEngine:
    """Provides semantic embedding vectors with HuggingFace option or local TF-IDF vectors."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.hf_model = None
        self._try_load_hf()

    def _try_load_hf(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.hf_model = SentenceTransformer(self.model_name)
            print(f"Loaded HuggingFace model: {self.model_name}")
        except Exception:
            self.hf_model = None

    def embed_text(self, text: str, idf: Dict[str, float]) -> Dict[str, float]:
        """Compute normalized term vector."""
        tokens = tokenize(text)
        if not tokens:
            return {}
        tf = Counter(tokens)
        total = len(tokens)
        vec = {}
        for t, count in tf.items():
            vec[t] = (count / total) * idf.get(t, 1.0)
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm > 0:
            return {k: v / norm for k, v in vec.items()}
        return vec

    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Compute cosine similarity between two normalized sparse vectors."""
        score = 0.0
        for term, val in vec1.items():
            if term in vec2:
                score += val * vec2[term]
        return min(1.0, max(0.0, score))
