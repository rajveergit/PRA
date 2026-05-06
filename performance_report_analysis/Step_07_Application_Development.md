# Step 7 — Application Development
## Phase: Application Development
**Guideline:** Build UI using Streamlit or Flask

---

## 7.1 Architecture Diagram
```
+--------------------------------------------------+
|              STREAMLIT FRONTEND                  |
|  +----------+  +----------+  +--------------+   |
|  | Doc Upload|  |  Chat UI |  |  Analytics   |   |
|  |  Panel   |  |          |  |  Dashboard   |   |
|  +----------+  +----------+  +--------------+   |
+---------------------+----------------------------+
                       |
+---------------------+----------------------------+
|               BACKEND (Python)                   |
|  +----------+  +----------+  +--------------+   |
|  | Document |  |  RAG     |  |  LLM API     |   |
|  | Processor|  | Retriever|  |  (OpenAI)    |   |
|  +----------+  +----------+  +--------------+   |
+---------------------+----------------------------+
                       |
+---------------------+----------------------------+
|            VECTOR DATABASE (ChromaDB)            |
|         Stored Embeddings + Metadata             |
+--------------------------------------------------+
```

---

## 7.2 Project File Structure
```
automobile-performance-analyzer/
├── app.py                      # Main Streamlit application
├── rag_pipeline.py             # RAG chain setup
├── document_processor.py       # PDF ingestion + chunking
├── vector_store.py             # ChromaDB operations
├── config.py                   # API keys, settings
├── data/
│   ├── raw/                    # Original uploaded documents
│   └── processed/              # Cleaned text chunks
├── chroma_db/                  # Persistent vector store
├── utils/
│   └── helpers.py              # Utility functions
├── evaluation/
│   ├── test_queries.json       # Evaluation query set
│   └── eval_report.py          # Scoring script
├── requirements.txt
└── README.md
```

---

## 7.3 Streamlit Application (app.py)

```python
import streamlit as st
from rag_pipeline import AutoPerformanceRAG
from document_processor import process_and_index_documents

st.set_page_config(
    page_title="AutoAnalyst AI",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Automobile Performance Report Analyzer")
st.caption("Ask questions about vehicle specs, performance, emissions, and diagnostics")

# Sidebar - Document Management
with st.sidebar:
    st.header("📁 Document Manager")
    uploaded_files = st.file_uploader(
        "Upload Performance Reports",
        type=["pdf", "txt", "csv"],
        accept_multiple_files=True
    )
    if uploaded_files and st.button("Index Documents"):
        with st.spinner("Processing and indexing..."):
            process_and_index_documents(uploaded_files)
        st.success(f"✅ {len(uploaded_files)} documents indexed!")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if query := st.chat_input("Ask about vehicle performance, specs, diagnostics..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing reports..."):
            rag = AutoPerformanceRAG()
            result = rag.query(query)
            answer = result["result"]
            sources = result["source_documents"]

        st.markdown(answer)

        # Show source references
        with st.expander("📄 Source Documents"):
            for doc in sources:
                st.info(f"**{doc.metadata.get('source', 'Unknown')}** "
                        f"— Page {doc.metadata.get('page_number', 'N/A')}")
                st.caption(doc.page_content[:300] + "...")

    st.session_state.messages.append({"role": "assistant", "content": answer})
```

---

## 7.4 Key Features Built

| Feature | Implementation |
|---|---|
| Document Upload | Streamlit file_uploader -> auto-indexed |
| Natural Language Q&A | RAG chain with GPT-3.5-turbo |
| Source Citations | Source documents displayed per answer |
| Multi-turn Chat | LangChain ConversationBufferWindowMemory |
| Performance Comparison | Structured prompt for tabular output |
| OBD Code Lookup | CSV-based fault code retrieval |

---

## Checklist
- [ ] `app.py` created with Streamlit layout
- [ ] Sidebar document upload panel working
- [ ] Chat interface displays messages correctly
- [ ] Source citations shown in expander
- [ ] Session state maintains chat history
- [ ] App runs locally on `http://localhost:8501`
- [ ] All files organized per project structure
