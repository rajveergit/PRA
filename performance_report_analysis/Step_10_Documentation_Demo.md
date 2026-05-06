# Step 10 — Documentation & Demo
## Phase: Documentation & Demo
**Guideline:** Prepare report, PPT, demo, and Git repository

---

## 10.1 How to Run the Project

### Prerequisites
```bash
Python 3.10+
pip install -r requirements.txt
```

### Installation
```bash
# Clone the repository
git clone https://github.com/[your-username]/automobile-performance-analyzer.git
cd automobile-performance-analyzer

# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="your-api-key-here"
```

### Running the App
```bash
streamlit run app.py
```
App will open at `http://localhost:8501`

---

## 10.2 requirements.txt
```
streamlit==1.32.0
langchain==0.1.16
langchain-openai==0.1.3
langchain-chroma==0.1.1
chromadb==0.4.24
openai==1.14.3
pymupdf==1.24.0
pandas==2.2.1
sentence-transformers==2.7.0
python-dotenv==1.0.1
```

---

## 10.3 Sample Queries for Demo

Use these queries to demonstrate the system during viva/presentation:

1. *"What is the maximum power and torque of the Tata Nexon EV?"*
2. *"Compare fuel efficiency between Maruti Swift petrol and diesel variants"*
3. *"What does OBD fault code P0420 mean and how do I fix it?"*
4. *"What safety rating did the Hyundai Creta receive in Bharat NCAP 2023?"*
5. *"Explain the BS6 emission standards and how they affect engine tuning"*
6. *"What are the service intervals for the Tata Nexon EV battery pack?"*

---

## 10.4 GitHub Repository Structure
```
README.md                    <- Project overview + setup guide
app.py                       <- Streamlit application
rag_pipeline.py              <- Core RAG logic
document_processor.py        <- Ingestion pipeline
requirements.txt             <- Dependencies
data/sample_docs/            <- Sample automobile PDFs
evaluation/                  <- Test queries + results
docs/
├── project_report.md        <- Full project report
└── demo_screenshots/        <- UI screenshots
```

---

## 10.5 Key Learnings
1. **RAG > Fine-tuning** for domain-specific knowledge — faster, cheaper, updatable
2. **Chunk size matters** — 512 tokens with overlap outperformed 1024 token chunks
3. **MMR retrieval** significantly reduces redundant context
4. **Metadata filtering** is critical for multi-document systems
5. **System prompt grounding** is the single most effective hallucination reducer
6. **Evaluation discipline** — without a test set, optimization is guesswork

---

## 10.6 Future Enhancements

| Enhancement | Benefit |
|---|---|
| OCR Integration (Tesseract) | Support scanned/image PDFs |
| Real-time OBD-II connectivity | Live vehicle diagnostics |
| Graph RAG | Relationship-aware retrieval |
| Fine-tuned domain LLM | Better automobile terminology understanding |
| Multi-language support | Regional language manuals |
| Vector DB upgrade to Pinecone | Cloud-scale deployment |

---

## 10.7 References
1. Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020.
2. LangChain Documentation — https://docs.langchain.com
3. ChromaDB Documentation — https://docs.trychroma.com
4. Automotive Research Association of India (ARAI) — https://www.araiindia.com
5. Global NCAP Safety Reports — https://www.globalncap.org
6. SAE International — OBD-II Standards (J1979) — https://www.sae.org
7. OpenAI API Documentation — https://platform.openai.com/docs

---

## Checklist
- [ ] README.md written with setup instructions
- [ ] requirements.txt complete and tested
- [ ] All code pushed to GitHub with clear commit messages
- [ ] Demo queries prepared and tested
- [ ] PPT prepared (project title, problem, architecture, results, demo)
- [ ] Report document finalized
- [ ] Demo screenshots taken and added to `docs/demo_screenshots/`
- [ ] Repository made public (or shared with evaluator)
