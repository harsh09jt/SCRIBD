"""
ChromaDB and Vector Store interface for Enterprise Expert Knowledge Worker.
Supports ChromaDB client if available, with robust persistent fallback.
"""

import os
import math
from typing import List, Dict, Any, Optional
from backend.rag.embeddings import EmbeddingEngine, tokenize

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
CHROMA_DIR = os.path.join(DATA_DIR, "chromadb_storage")


class EnterpriseVectorStore:
    def __init__(self, persist_dir: str = CHROMA_DIR):
        self.persist_dir = persist_dir
        self.embedding_engine = EmbeddingEngine()
        self.documents: List[Dict[str, Any]] = []
        self.doc_vectors: List[Dict[str, float]] = []
        self.idf: Dict[str, float] = {}
        self.chroma_client = None
        self._init_chroma()

    def _init_chroma(self):
        try:
            import chromadb
            os.makedirs(self.persist_dir, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=self.persist_dir)
            self.chroma_collection = self.chroma_client.get_or_create_collection("enterprise_knowledge")
            print("ChromaDB persistent client initialized successfully.")
        except Exception:
            self.chroma_client = None

    def reset(self):
        """Drop every indexed chunk (in memory and, when available, in ChromaDB) before a full re-index."""
        self.documents.clear()
        self.doc_vectors.clear()
        self.idf = {}
        if self.chroma_client is not None:
            try:
                self.chroma_client.delete_collection("enterprise_knowledge")
                self.chroma_collection = self.chroma_client.get_or_create_collection("enterprise_knowledge")
            except Exception as e:
                print(f"Warning: could not reset ChromaDB collection: {e}")

    def add_documents(self, docs: List[Dict[str, Any]]):
        """Index documents into the vector store."""
        for doc in docs:
            self.documents.append(doc)

        # Build IDF dictionary
        n_docs = len(self.documents)
        df = {}
        all_tokens = []
        for doc in self.documents:
            text = f"{doc.get('document_name', '')} {doc.get('section', '')} {doc.get('content', '')}"
            tokens = tokenize(text)
            all_tokens.append(tokens)
            for t in set(tokens):
                df[t] = df.get(t, 0) + 1

        self.idf = {t: math.log((n_docs + 1) / (cnt + 1)) + 1.0 for t, cnt in df.items()}

        # Build vectors
        self.doc_vectors = []
        for tokens in all_tokens:
            vec = self.embedding_engine.embed_text(" ".join(tokens), self.idf)
            self.doc_vectors.append(vec)

        # If ChromaDB is available, add documents there too
        if self.chroma_client is not None:
            try:
                ids = [d.get("chunk_id", f"chk_{i}") for i, d in enumerate(docs)]
                documents = [d.get("content", "") for d in docs]
                metadatas = [d.get("metadata", {}) for d in docs]
                self.chroma_collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            except Exception as e:
                print(f"Warning: ChromaDB indexing error: {e}")

    def search(
        self,
        query: str,
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Perform semantic search with metadata filtering and similarity scores."""
        q_tokens = tokenize(query)
        if not q_tokens or not self.doc_vectors:
            return []

        q_vec = self.embedding_engine.embed_text(query, self.idf)

        results = []
        for idx, doc in enumerate(self.documents):
            # Apply metadata filter
            if filter_dict:
                match = True
                meta = doc.get("metadata", {})
                for k_filt, v_filt in filter_dict.items():
                    if meta.get(k_filt) != v_filt:
                        match = False
                        break
                if not match:
                    continue

            sim = self.embedding_engine.cosine_similarity(q_vec, self.doc_vectors[idx])

            # Keyword occurrence boost
            content_lower = doc.get("content", "").lower()
            keyword_hits = sum(1 for t in q_tokens if t in content_lower)
            boost = (keyword_hits / len(q_tokens)) * 0.25
            final_score = min(1.0, round(sim + boost, 4))

            if final_score > 0.05:
                results.append({
                    "chunk_id": doc.get("chunk_id", f"chk_{idx}"),
                    "document_name": doc.get("document_name", ""),
                    "file_name": doc.get("file_name", ""),
                    "document_type": doc.get("document_type", ""),
                    "department": doc.get("department", ""),
                    "section": doc.get("section", ""),
                    "content": doc.get("content", ""),
                    "version": doc.get("version", "v1.0"),
                    "last_updated": doc.get("last_updated", "2026-08-01"),
                    "access_roles": doc.get("access_roles", ["employee", "admin"]),
                    "metadata": doc.get("metadata", {}),
                    "similarity_score": final_score
                })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:k]


# Singleton
_vector_store = None

def get_vector_store() -> EnterpriseVectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = EnterpriseVectorStore()
    return _vector_store
