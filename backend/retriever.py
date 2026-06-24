from backend.embedder import Embedder
import uuid

class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.store = []  # in-memory fallback

    def add_chunks(self, chunks: list[dict]):
        # Just store locally (NO QDRANT)
        for c in chunks:
            self.store.append({
                "id": str(uuid.uuid4()),
                "text": c["text"],
                "metadata": c.get("metadata", {})
            })

        print(f"[retriever] Stored {len(chunks)} chunks in memory")

    def query(self, query: str, top_k: int = 5):
        # Simple fallback: return all stored chunks (no vector search)
        results = self.store[:top_k]

        return [
            {
                "text": r["text"],
                "legal_address": r["metadata"].get("legal_address", "unknown"),
                "score": 1.0
            }
            for r in results
        ]

    def count(self):
        return len(self.store)from backend.embedder import Embedder
import uuid

class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.store = []  # in-memory fallback

    def add_chunks(self, chunks: list[dict]):
        # Just store locally (NO QDRANT)
        for c in chunks:
            self.store.append({
                "id": str(uuid.uuid4()),
                "text": c["text"],
                "metadata": c.get("metadata", {})
            })

        print(f"[retriever] Stored {len(chunks)} chunks in memory")

    def query(self, query: str, top_k: int = 5):
        # Simple fallback: return all stored chunks (no vector search)
        results = self.store[:top_k]

        return [
            {
                "text": r["text"],
                "legal_address": r["metadata"].get("legal_address", "unknown"),
                "score": 1.0
            }
            for r in results
        ]

    def count(self):
        return len(self.store)
