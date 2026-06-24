
from groq import Groq
from backend.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a legal compliance assistant specialized in Indian business regulations.
Use ONLY the provided context to answer. If the answer is not in the context, say so clearly.
Always cite the Act, Chapter, and Section your answer is based on. Be concise and accurate."""

def generate_answer(query: str, context_chunks: list[dict]) -> dict:
    context = "\n\n".join(
        f"[{c.get('legal_address', c.get('source', 'unknown'))}]\n{c['text']}"
        for c in context_chunks
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ],
        max_tokens=1024,
        temperature=0.1
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": list({c.get("legal_address", c.get("source", "unknown")) for c in context_chunks})
    }
EOF
