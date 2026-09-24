"""
Hybrid Reranker for Enterprise Expert Knowledge Worker.
Combines Dense Semantic Vector Scores, Lexical Exact Match, and Reciprocal Rank Fusion (RRF)
to optimize precision for enterprise domain queries.
"""

import math
from typing import List, Dict, Any
from backend.rag.embeddings import tokenize


class HybridReranker:
    """Reranks candidate retrieved chunks using hybrid semantic and lexical scoring."""

    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k

    def rerank(
        self,
        query: str,
        chunks: List[Dict[str, Any]],
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Rerank chunks with a stronger emphasis on exact query keywords and title/section matches.
        This prevents broad, weakly related policy fragments from outranking the true answer.
        """
        if not chunks:
            return []

        q_tokens = [t for t in tokenize(query) if len(t) > 2]
        q_set = set(q_tokens)
        if not q_set:
            return chunks[:top_n]

        scored_chunks = []
        for rank_idx, chunk in enumerate(chunks):
            semantic_score = chunk.get("similarity_score", 0.5)
            content = chunk.get("content", "").lower()
            section = chunk.get("section", "").lower()
            doc_name = chunk.get("document_name", "").lower()
            combined_text = f"{doc_name} {section} {content}"

            content_tokens = tokenize(content)
            overlap_count = sum(1 for t in q_tokens if t in content_tokens)
            lexical_score = overlap_count / max(len(q_tokens), 1)

            title_hits = sum(1 for t in q_tokens if t in doc_name or t in section)
            title_boost = 0.18 if title_hits > 0 else 0.0

            exact_phrase_hits = 0
            for token in q_tokens:
                if token in combined_text:
                    exact_phrase_hits += 1
            exact_phrase_score = min(0.25, exact_phrase_hits / max(len(q_tokens), 1) * 0.25)

            rrf_score = 1.0 / (self.rrf_k + rank_idx + 1)

            blended_score = (0.45 * semantic_score) + (0.35 * lexical_score) + title_boost + (0.15 * rrf_score) + exact_phrase_score
            blended_score = min(0.99, max(0.01, round(blended_score, 4)))

            if not q_set.intersection(set(content_tokens)) and title_hits == 0 and semantic_score < 0.22:
                blended_score *= 0.55

            chunk_copy = dict(chunk)
            chunk_copy["rerank_score"] = blended_score
            scored_chunks.append(chunk_copy)

        scored_chunks.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored_chunks[:top_n]


# Singleton
_reranker = None

def get_reranker() -> HybridReranker:
    global _reranker
    if _reranker is None:
        _reranker = HybridReranker()
    return _reranker
