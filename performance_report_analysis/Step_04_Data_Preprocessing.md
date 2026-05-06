# Step 4 — Data Preprocessing
## Phase: Data Preprocessing
**Guideline:** Clean text, chunk documents, remove noise

---

## 4.1 Preprocessing Pipeline Overview
```
Raw Documents (PDF/CSV/TXT)
        |
   Text Extraction
        |
   Noise Removal & Cleaning
        |
   Document Chunking
        |
   Metadata Tagging
        |
  Preprocessed Chunks (ready for embedding)
```

---

## 4.2 Text Extraction from PDF

```python
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract raw text from PDF documents."""
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        full_text += f"\n--- Page {page_num + 1} ---\n{text}"
    return full_text
```

---

## 4.3 Text Cleaning

```python
import re

def clean_text(text: str) -> str:
    """Remove noise from extracted automobile documents."""
    # Remove page headers/footers patterns
    text = re.sub(r'Page \d+ of \d+', '', text)
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove non-ASCII characters (OCR artifacts)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Remove table formatting artifacts
    text = re.sub(r'\|{2,}', ' ', text)
    # Normalize spaces
    text = ' '.join(text.split())
    return text.strip()
```

---

## 4.4 Document Chunking Strategy

**Strategy Used:** Recursive Character Text Splitter with overlap

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(text: str, source_name: str) -> list:
    """Chunk text into overlapping segments for optimal retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,        # tokens per chunk
        chunk_overlap=64,      # overlap to preserve context
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.create_documents(
        texts=[text],
        metadatas=[{"source": source_name}]
    )
    return chunks
```

**Why 512 tokens?**
- Balances specificity (not too broad) and context (not too narrow)
- Fits within embedding model input limits
- Provides enough content for meaningful retrieval

---

## 4.5 Metadata Tagging

Each chunk is tagged with structured metadata for filtered retrieval:

```python
metadata = {
    "source": "tata_nexon_performance_report.pdf",
    "document_type": "performance_report",
    "vehicle_brand": "Tata",
    "vehicle_model": "Nexon",
    "year": "2023",
    "page_number": 12,
    "category": "engine_specs"  # engine | safety | emission | service
}
```

---

## 4.6 Preprocessing Summary

| Step | Tool Used | Output |
|---|---|---|
| PDF Extraction | PyMuPDF (fitz) | Raw text strings |
| CSV Parsing | pandas | DataFrames -> text rows |
| Cleaning | Python `re` module | Cleaned text |
| Chunking | LangChain TextSplitter | List of Document objects |
| Metadata | Manual + rule-based tagging | Enriched Document objects |

---

## Checklist
- [ ] Text extraction function written and tested
- [ ] Cleaning function handles headers, extra whitespace, artifacts
- [ ] Chunk size set to 512 tokens with 64-token overlap
- [ ] Metadata schema defined for each document category
- [ ] All documents preprocessed into chunks and saved
