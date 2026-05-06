# Step 6 — LLM / RAG Design
## Phase: LLM / RAG Design
**Guideline:** Design prompts, RAG pipeline, or agent flow

---

## 6.1 RAG Architecture Overview
```
User Query
    |
[Query Embedding]
    |
[Vector DB Similarity Search] -> Top-K relevant chunks
    |
[Context Assembly] -> Prompt Construction
    |
[LLM Generation] -> Answer + Source Citations
    |
User Response
```

---

## 6.2 System Prompt Design

```python
SYSTEM_PROMPT = """
You are an expert Automobile Performance Analyst AI assistant.
You help engineers, technicians, and automotive enthusiasts understand 
vehicle performance reports, technical specifications, and diagnostic information.

RULES:
1. Answer ONLY based on the provided context documents
2. If information is not in the context, say "This information is not available 
   in the provided documents"
3. Always cite the source document and page when referencing data
4. When comparing vehicles, present data in a structured table format
5. For diagnostic fault codes, provide: code, description, probable cause, and fix
6. Use technical units correctly (Nm, kW, PS, km/l, g/km CO2)
7. Never hallucinate numerical performance data

Context Documents:
{context}
"""
```

---

## 6.3 RAG Pipeline Implementation

```python
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1,   # Low temp for factual accuracy
    max_tokens=1000
)

# Create retriever with metadata filtering
retriever = vectorstore.as_retriever(
    search_type="mmr",          # Maximal Marginal Relevance (diversity)
    search_kwargs={
        "k": 5,                 # Top 5 chunks
        "fetch_k": 20,          # Fetch 20, re-rank to 5
    }
)

# Build RAG chain
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=SYSTEM_PROMPT + "\n\nQuestion: {question}\nAnswer:"
)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)
```

---

## 6.4 Sample Query & Response Flow

**Query:** *"What is the maximum torque and at what RPM does the Tata Nexon petrol engine produce it?"*

**Step 1 — Retrieval:**
```
Retrieved chunks from: tata_nexon_performance_report.pdf
- Chunk 47 (page 12): "...the 1.2L Revotron turbo-petrol produces 170Nm of torque at 1750-4000 RPM..."
- Chunk 48 (page 13): "...compared to competitors in the sub-4m SUV segment..."
```

**Step 2 — Generated Answer:**
```
The Tata Nexon's 1.2L Revotron turbocharged petrol engine produces a maximum 
torque of 170 Nm, available across a wide RPM band of 1750-4000 RPM. This flat 
torque curve ensures strong mid-range performance suitable for both city and 
highway driving.

Source: tata_nexon_performance_report.pdf, Page 12
```

---

## 6.5 Conversation Memory (Multi-turn)

```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,                        # Remember last 5 exchanges
    return_messages=True
)
```

---

## Checklist
- [ ] System prompt written with grounding rules
- [ ] LLM initialized (GPT-3.5-turbo, temperature=0.1)
- [ ] Retriever configured with MMR (k=5, fetch_k=20)
- [ ] RAG chain assembled and tested end-to-end
- [ ] Multi-turn memory added
- [ ] At least 3 sample queries tested manually
