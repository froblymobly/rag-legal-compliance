cat > frontend/app.py << 'EOF'
import streamlit as st
import httpx
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Legal Compliance Assistant", page_icon="⚖️")
st.title("⚖️ Indian Legal Compliance Assistant")
st.caption("Ask about GST, Companies Act, Labour Laws, FEMA, and more.")

with st.sidebar:
    st.header("📊 System Stats")
    try:
        stats = httpx.get(f"{API_URL}/stats", timeout=10).json()
        st.metric("Documents Indexed", stats["total_chunks"])
    except:
        st.warning("API offline")

query = st.text_area("Your legal question:", height=100,
    placeholder="e.g. What is the GST threshold for small businesses?")

top_k = st.slider("Context chunks", 3, 10, 5)

if st.button("🔍 Get Answer", type="primary") and query:
    with st.spinner("Searching regulations..."):
        try:
            r = httpx.post(f"{API_URL}/query",
                json={"query": query, "top_k": top_k}, timeout=120)
            data = r.json()

            st.subheader("📋 Answer")
            st.write(data["answer"])

            st.subheader("📎 Legal Sources")
            for src in data.get("sources", []):
                st.code(src)

            with st.expander("🔬 Retrieved Chunks"):
                for i, chunk in enumerate(data.get("retrieved_chunks", [])):
                    st.markdown(f"**Chunk {i+1}** | Score: `{chunk['score']}`")
                    st.caption(chunk.get('legal_address', ''))
                    st.text(chunk["text"][:300] + "...")
        except Exception as e:
            st.error(f"Error: {e}")
EOF
