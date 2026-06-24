
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from backend.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, TOP_K
from backend.embedder import Embedder
import uuid

class Retriever:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.embedder = Embedder()
        self._init_collection()

    def _init_collection(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if COLLECTION_NAME not in existing:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"[retriever] Created collection: {COLLECTION_NAME}")

    def add_chunks(self, chunks: list[dict]):
        texts      = [c["text"] for c in chunks]
        embeddings = self.embedder.embed(texts)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=emb.tolist(),
                payload={
                    "text": c["text"],
                    **c.get("metadata", {})
                }
            )
            for c, emb in zip(chunks, embeddings)
        ]

        self.client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"[retriever] Added {len(points)} chunks to Qdrant")

    def query(self, query: str, top_k: int = TOP_K) -> list[dict]:
        q_embed = self.embedder.embed_query(query)

        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=q_embed.tolist(),
            limit=top_k,
            with_payload=True
        )

        return [
            {
                "text": r.payload.get("text", ""),
                "legal_address": r.payload.get("legal_address", r.payload.get("source", "unknown")),
                "score": round(r.score, 4)
            }
            for r in results
        ]

    def count(self):
        return self.client.get_collection(COLLECTION_NAME).points_count
