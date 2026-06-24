import os
from dotenv import load_dotenv
load_dotenv()

QDRANT_URL        = os.getenv("https://346fdb2c-6534-4265-840c-c05ce1b940c5.sa-east-1-0.aws.cloud.qdrant.io")
QDRANT_API_KEY    = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6ODUxM2Q2YjItOGVhYi00N2Q2LThiNGQtYmFk>")
COLLECTION_NAME   = os.getenv("COLLECTION_NAME", "legal_compliance_india")
EMBED_MODEL       = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY")
GROQ_MODEL        = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
CHUNK_SIZE        = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP     = int(os.getenv("CHUNK_OVERLAP", 50))
TOP_K             = int(os.getenv("TOP_K", 5))

