# Step 5 — Embedding & Vector Database
## Phase: Embedding & Vector DB
**Guideline:** Generate embeddings and store in vector database

---

## 5.1 What are Embeddings?
Embeddings convert text chunks into high-dimensional numerical vectors that capture semantic meaning. Similar content has vectors that are geometrically close — enabling similarity-based retrieval.

```
"torque at 3000 RPM"  ->  [0.23, -0.87, 0.45, ... 384 dims]
"engine twist force"  ->  [0.21, -0.84, 0.43, ... 384 dims]  <- semantically close
"fuel tank capacity"  ->  [-0.67, 0.12, -0.33, ...]          <- far away
```

---

## 5.2 Embedding Model Selection

| Model | Dimensions | Speed | Cost | Selected |
|---|---|---|---|---|
| `text-embedding-3-small` (OpenAI) | 1536 | Fast | Paid | Primary |
| `all-MiniLM-L6-v2` (HuggingFace) | 384 | Fast | Free | Fallback |
| `text-embedding-ada-002` (OpenAI) | 1536 | Fast | Paid | Legacy/Not used |

---

## 5.3 Generating Embeddings

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# OpenAI (production)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Free alternative (local)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

---

## 5.4 Vector Database — ChromaDB

**Why ChromaDB?**
- Lightweight, runs locally (no server needed)
- Persistent storage to disk
- Easy LangChain integration
- Supports metadata filtering

```python
from langchain_chroma import Chroma

# Create and persist vector store
vectorstore = Chroma.from_documents(
    documents=chunks,           # preprocessed document chunks
    embedding=embeddings,       # embedding model
    persist_directory="./chroma_db",
    collection_name="automobile_reports"
)

print(f"Total vectors stored: {vectorstore._collection.count()}")
```

---

## 5.5 Vector DB Architecture
```
ChromaDB (./chroma_db/)
  Collection: automobile_reports
    Chunk ID: uuid-001
      text: "The Nexon EV delivers 129PS peak power..."
      embedding: [0.23, -0.87, ...]
      metadata: {source, vehicle_model, category...}
    Chunk ID: uuid-002
      ...
    ... (~4800 chunks total)
```

---

## 5.6 Retrieval Testing

```python
# Test semantic retrieval
query = "What is the fuel efficiency of Maruti Swift petrol variant?"
results = vectorstore.similarity_search(query, k=5)

for doc in results:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:200]}\n")
```

---

## Checklist
- [ ] Embedding model selected (OpenAI or HuggingFace fallback)
- [ ] All chunks embedded and stored in ChromaDB
- [ ] ChromaDB persisted to disk (`./chroma_db/`)
- [ ] Collection name set to `automobile_reports`
- [ ] Retrieval test run — relevant chunks returned for sample queries
- [ ] Total chunk count verified
