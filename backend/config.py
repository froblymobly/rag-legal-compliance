import os
from dotenv import load_dotenv
load_dotenv()

QDRANT_URL        = os.getenv("QDRANT_URL")
QDRANT_API_KEY    = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME   = os.getenv("COLLECTION_NAME", "legal_compliance_india")
EMBED_MODEL       = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY")
GROQ_MODEL        = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
CHUNK_SIZE        = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP     = int(os.getenv("CHUNK_OVERLAP", 50))
TOP_K             = int(os.getenv("TOP_K", 5))

