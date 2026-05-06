# Step 2 — Requirement Analysis
## Phase: Requirement Analysis
**Guideline:** Define scope, assumptions, and constraints

---

## 2.1 Project Scope

**In Scope:**
- Ingestion and analysis of automobile performance PDFs, manuals, and structured datasets
- Building a RAG (Retrieval-Augmented Generation) pipeline
- Natural language Q&A interface for performance queries
- Multi-document comparison capability
- Basic analytics dashboard showing key performance metrics

**Out of Scope:**
- Real-time vehicle telemetry integration (IoT/CAN bus)
- Mobile application development
- Multilingual support (beyond English)
- Live OBD-II hardware connectivity

---

## 2.2 Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | System shall accept PDF/text documents as input | High |
| FR-02 | System shall chunk and embed documents | High |
| FR-03 | System shall retrieve relevant context for user queries | High |
| FR-04 | System shall generate accurate, grounded answers via LLM | High |
| FR-05 | System shall support multi-turn conversation | Medium |
| FR-06 | System shall display source document references | Medium |
| FR-07 | System shall allow document upload via UI | Medium |
| FR-08 | System shall handle tabular performance data (CSV) | Low |

---

## 2.3 Non-Functional Requirements

| Requirement | Target |
|---|---|
| Response Latency | < 5 seconds per query |
| Accuracy (Relevance) | > 80% on test query set |
| Hallucination Rate | < 10% |
| Supported File Types | PDF, TXT, CSV |
| Concurrent Users | Up to 5 (prototype scope) |

---

## 2.4 Assumptions
- Documents are in English
- PDFs are text-based (not scanned images — no OCR required in base version)
- Performance reports follow standard formats (dyno test results, ARAI/EPA certifications)
- OpenAI or open-source LLM API access is available

---

## 2.5 Constraints
- Budget: Free-tier or low-cost API usage (OpenAI / HuggingFace)
- Compute: Local machine or Google Colab (no GPU cluster)
- Time: 4–6 week academic project timeline
- Data: Publicly available automobile documents only

---

## 2.6 Technology Stack

| Layer | Technology |
|---|---|
| LLM | GPT-3.5-turbo / LLaMA-3 / Gemini |
| Embeddings | OpenAI `text-embedding-3-small` / `all-MiniLM-L6-v2` |
| Vector DB | ChromaDB / FAISS |
| Framework | LangChain / LlamaIndex |
| Frontend/UI | Streamlit |
| Data Handling | Python, PyMuPDF, pandas |
| Version Control | Git + GitHub |

---

## Checklist
- [ ] Scope defined (in-scope and out-of-scope)
- [ ] Functional requirements listed with priority
- [ ] Non-functional requirements listed with measurable targets
- [ ] Assumptions written down
- [ ] Constraints identified (budget, compute, time, data)
- [ ] Technology stack selected and justified
