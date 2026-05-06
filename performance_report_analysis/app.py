import sys
import streamlit as st
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Directly parse .env file — always overwrite to ensure fresh values
_ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_ENV_FILE):
    with open(_ENV_FILE, "r") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                _val = _val.strip().strip('"').strip("'").strip()
                os.environ[_key.strip()] = _val  # always override

RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")
PROCESSED_JSON = os.path.join(PROCESSED_DIR, "processed_chunks.json")
DB_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

st.set_page_config(
    page_title="AutoAnalyst AI — Automobile Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------- Custom CSS --------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #0d1117; color: #e6edf3; }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid #30363d;
        text-align: center;
    }
    .main-header h1 { color: #58a6ff; font-size: 2.2rem; font-weight: 700; margin: 0; }
    .main-header p  { color: #8b949e; margin: 0.5rem 0 0; font-size: 1rem; }

    /* Pipeline activity box */
    .pipeline-log {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        color: #39d353;
        max-height: 200px;
        overflow-y: auto;
    }
    .log-line { padding: 2px 0; }
    .log-dim  { color: #6e7681; }
    .log-ok   { color: #39d353; }
    .log-warn { color: #d29922; }
    .log-info { color: #58a6ff; }

    /* Chat messages */
    .stChatMessage { border-radius: 12px !important; margin: 0.4rem 0 !important; }

    /* Source expander */
    .stExpander { border: 1px solid #21262d !important; border-radius: 8px !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #21262d;
    }

    /* Metrics */
    .metric-box {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        text-align: center;
    }
    .metric-box .label { color: #8b949e; font-size: 0.75rem; text-transform: uppercase; }
    .metric-box .value { color: #58a6ff; font-size: 1.4rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# -------- Logging State --------
if "pipeline_logs" not in st.session_state:
    st.session_state.pipeline_logs = []

def log(msg: str, level: str = "ok"):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.pipeline_logs.append({"time": timestamp, "msg": msg, "level": level})

# -------- Auto Init --------
def auto_initialize():
    from document_processor import process_files
    from vector_store import create_vector_store

    need_process = not os.path.exists(PROCESSED_JSON)
    need_index   = not os.path.exists(DB_PATH) or len(os.listdir(DB_PATH)) == 0

    if not need_process and not need_index:
        if not st.session_state.pipeline_logs:
            log("✅ Pre-built index found — skipping preprocessing.", "ok")
            log("🚀 System ready for queries.", "info")
        return

    progress_placeholder = st.empty()
    log("🔧 Initializing pipeline...", "info")

    if need_process:
        log("📂 Scanning data/raw/ for documents...", "info")
        files = os.listdir(RAW_DIR) if os.path.exists(RAW_DIR) else []
        log(f"   Found {len(files)} file(s): {', '.join(files)}", "dim")

        with progress_placeholder.status("⚙️ Processing documents...", expanded=True) as s:
            for fname in files:
                st.write(f"📄 Chunking `{fname}`...")
                time.sleep(0.1)
            s.update(label="Documents processed!", state="complete")

        def cb(msg):
            log(f"   {msg}", "ok")

        process_files(RAW_DIR, PROCESSED_DIR, status_callback=cb)

        import json
        with open(PROCESSED_JSON) as f:
            chunks = json.load(f)
        log(f"✅ Chunking complete — {len(chunks)} chunks generated.", "ok")

    if need_index:
        log("🔍 Embedding chunks into ChromaDB...", "info")
        with progress_placeholder.status("🔍 Building vector database...", expanded=True) as s:
            st.write("Embedding chunks using ONNX (local, free)...")
            def vcb(msg):
                st.write(msg)
                log(f"   {msg}", "dim")
            from vector_store import create_vector_store
            create_vector_store(PROCESSED_JSON, DB_PATH, status_callback=vcb)
            s.update(label="Vector database ready!", state="complete")

        log("✅ ChromaDB index built successfully.", "ok")

    log("🚀 System fully initialized. Ready!", "info")
    progress_placeholder.empty()

def get_pipeline():
    if "pipeline" not in st.session_state:
        log("⚡ Loading RAG pipeline (Mistral + ChromaDB)...", "info")
        from rag_pipeline import RAGPipeline
        st.session_state.pipeline = RAGPipeline(persist_dir=DB_PATH)
        log("✅ RAG pipeline loaded.", "ok")
    return st.session_state.pipeline

# -------- Header --------
st.markdown("""
<div class="main-header">
    <h1>🚗 AutoAnalyst AI</h1>
    <p>Automobile Performance Intelligence — Powered by Mistral + RAG</p>
</div>
""", unsafe_allow_html=True)

# -------- Sidebar --------
with st.sidebar:
    # API Key input
    api_key_in_env = os.environ.get("mistral_api", "").strip()
    if not api_key_in_env:
        st.warning("⚠️ Mistral API key not found")
        st.markdown("Get your key at [console.mistral.ai](https://console.mistral.ai)")
        manual_key = st.text_input("🔑 Enter Mistral API Key", type="password", placeholder="...")
        if manual_key:
            os.environ["mistral_api"] = manual_key.strip()
            if "pipeline" in st.session_state:
                del st.session_state["pipeline"]
            st.success("✅ Key set! Ask your question now.")
    else:
        st.success(f"✅ Mistral API key loaded ({api_key_in_env[:8]}...)")


    st.markdown("### ⚙️ Pipeline Activity")

    # Live log display
    log_html = "<div class='pipeline-log'>"
    for entry in st.session_state.pipeline_logs[-30:]:
        css = entry.get("level", "ok")
        log_html += f"<div class='log-line log-{css}'>[{entry['time']}] {entry['msg']}</div>"
    if not st.session_state.pipeline_logs:
        log_html += "<div class='log-dim'>Waiting for initialization...</div>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Add PDF, TXT or CSV files",
        type=["pdf", "txt", "csv"],
        accept_multiple_files=True
    )
    if uploaded_files and st.button("🔄 Index New Documents"):
        from document_processor import process_files
        from vector_store import create_vector_store
        os.makedirs(RAW_DIR, exist_ok=True)
        for uf in uploaded_files:
            with open(os.path.join(RAW_DIR, uf.name), "wb") as f:
                f.write(uf.getbuffer())
            log(f"📥 Saved {uf.name}", "info")
        with st.spinner("Processing..."):
            process_files(RAW_DIR, PROCESSED_DIR)
            create_vector_store(PROCESSED_JSON, DB_PATH)
        if "pipeline" in st.session_state:
            del st.session_state.pipeline
        log("✅ New documents indexed.", "ok")
        st.success("Done!")
        st.rerun()

    st.divider()
    if st.button("🗑️ Clear Chat & Reload Pipeline"):
        st.session_state.messages = []
        if "pipeline" in st.session_state:
            del st.session_state["pipeline"]
        st.rerun()

    # Stats
    if os.path.exists(PROCESSED_JSON):
        import json
        with open(PROCESSED_JSON) as f:
            chunks = json.load(f)
        files = set(c["metadata"].get("source","?") for c in chunks)
        st.markdown("### 📊 Index Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-box'><div class='label'>Chunks</div><div class='value'>{len(chunks)}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box'><div class='label'>Files</div><div class='value'>{len(files)}</div></div>", unsafe_allow_html=True)

# -------- Auto-Initialize --------
auto_initialize()

# -------- Chat --------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.messages:
    st.info("💡 Try asking: *'What is the peak power of the Tata Nexon EV?'* or *'Explain OBD code P0301'*")

if query := st.chat_input("Ask about vehicle performance, specs, or diagnostics..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Retrieving documents & generating answer..."):
            try:
                log(f"🔎 Query: {query[:60]}...", "info")
                rag = get_pipeline()
                result = rag.query(query)
                answer = result.get("answer", "")
                sources = result.get("source_documents", [])
                log(f"✅ Answer generated ({len(sources)} source(s) retrieved).", "ok")

                st.markdown(answer)

                if sources:
                    with st.expander(f"📄 {len(sources)} Source Documents"):
                        for doc in sources:
                            src = doc.metadata.get("source", "Unknown")
                            dtype = doc.metadata.get("document_type", "")
                            st.markdown(f"**📁 {src}** `{dtype}`")
                            st.caption(doc.page_content[:300] + "...")
                            st.divider()

                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                err = f"❌ Error: {str(e)}\n\nEnsure `mistral_api` is set in your `.env` file."
                st.error(err)
                log(f"❌ Error: {str(e)[:80]}", "warn")
                st.session_state.messages.append({"role": "assistant", "content": err})

    st.rerun()
