
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.retriever import Retriever
from backend.generator import generate_answer
from backend.ingestor import ingest_pdf

app = FastAPI(title="RAG Legal Compliance API")
retriever = Retriever()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class IngestRequest(BaseModel):
    pdf_path: str

@app.get("/health")
def health():
    return {"status": "ok", "chunks": retriever.count()}

@app.post("/query")
def query(req: QueryRequest):
    try:
        chunks = retriever.query(req.query, req.top_k)
        if not chunks:
            raise HTTPException(status_code=404, detail="No relevant documents found")
        result = generate_answer(req.query, chunks)
        result["retrieved_chunks"] = chunks
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def ingest(req: IngestRequest):
    try:
        chunks = ingest_pdf(req.pdf_path)
        retriever.add_chunks(chunks)
        return {"status": "success", "chunks_added": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def stats():
    return {"total_chunks": retriever.count(), "collection": COLLECTION_NAME}
EOF
