import streamlit as st
import httpx

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Legal Compliance Assistant", page_icon="⚖️")
st.title("⚖️ Indian Legal Compliance Assistant")
st.caption("Ask about GST, Companies Act, Labour Laws, FEMA, and more.")

# Sidebar stats
with st.sidebar:
    st.header("📊 System Stats")
    try:
        stats = httpx.get(f"{API_URL}/stats").json()
        st.metric("Documents Indexed", stats["total_chunks"])
    except:
        st.warning("API offline")

    st.header("📥 Ingest Document")
    pdf_path = st.text_input("PDF Path", placeholder="data/raw/your_doc.pdf")
    if st.button("Ingest"):
        with st.spinner("Ingesting..."):
            r = httpx.post(f"{API_URL}/ingest", json={"pdf_path": pdf_path}, timeout=120)
            if r.status_code == 200:
                st.success(f"Added {r.json()['chunks_added']} chunks!")
            else:
                st.error(r.text)

# Main chat
query = st.text_area("Your legal question:", height=100,
    placeholder="e.g. What are the GST registration thresholds for service providers?")

top_k = st.slider("Context chunks", 3, 10, 5)

if st.button("🔍 Get Answer", type="primary") and query:
    with st.spinner("Searching regulations..."):
        try:
            r = httpx.post(f"{API_URL}/query",
                json={"query": query, "top_k": top_k}, timeout=120)
            data = r.json()

            st.subheader("📋 Answer")
            st.write(data["answer"])

            st.subheader("📎 Sources")
            for src in data.get("sources", []):
                st.badge(src)

            with st.expander("🔬 Retrieved Chunks"):
                for i, chunk in enumerate(data.get("retrieved_chunks", [])):
                    st.markdown(f"**Chunk {i+1}** | Source: `{chunk['source']}` | Score: `{chunk['score']:.3f}`")
                    st.text(chunk["text"][:300] + "...")
        except Exception as e:
            st.error(f"Error: {e}")
