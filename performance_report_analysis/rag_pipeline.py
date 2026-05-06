import os

# Directly parse .env file
_ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_ENV_FILE):
    with open(_ENV_FILE, "r") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                _val = _val.strip().strip('"').strip("'").strip()
                os.environ[_key.strip()] = _val

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from embeddings import LocalONNXEmbeddings

SYSTEM_PROMPT = """You are an expert Automobile Performance Analyst AI assistant.
Use the context below to answer as accurately and completely as possible.
If a specific value is mentioned anywhere in the context, extract and state it clearly.
Only say "This information is not available in the provided documents" if the context truly contains no relevant information at all.

Always cite the source document. Use technical units correctly (Nm, kW, PS, km/l).
For OBD fault codes, provide: code, description, probable cause, and fix.

Context:
{context}

Question: {question}
Answer:"""

def format_docs(docs):
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source','unknown')}]\n{doc.page_content}"
        for doc in docs
    )

class RAGPipeline:
    def __init__(self, persist_dir: str = "chroma_db"):
        self.persist_dir = persist_dir
        self.init_pipeline()

    def init_pipeline(self):
        print("Loading ONNX embeddings model...")
        embeddings = LocalONNXEmbeddings()

        print("Loading Chroma Vector Store...")
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=embeddings,
            collection_name="automobile_reports"
        )

        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 8}
        )

        print("Initializing Mistral LLM...")
        mistral_api_key = os.getenv("mistral_api")
        if not mistral_api_key:
            raise ValueError(
                "mistral_api not found. "
                "Add to .env as: mistral_api=..."
            )

        self.llm = ChatMistralAI(
            model="mistral-small-latest",
            api_key=mistral_api_key,
            max_tokens=512,
        )


        self.prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

        self.chain = (
            {
                "context": self.retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        print("RAG pipeline ready.")

    def _hybrid_retrieve(self, question: str):
        # Semantic search
        semantic_docs = self.retriever.invoke(question)

        # Keyword search: extract tokens 3+ chars and search directly in ChromaDB
        import re
        tokens = re.findall(r'[A-Za-z0-9]{3,}', question)
        keyword_docs = []
        for token in tokens:
            try:
                results = self.vectorstore.get(
                    where_document={"$contains": token},
                    limit=5
                )
                for content, meta in zip(results["documents"], results["metadatas"]):
                    from langchain_core.documents import Document
                    keyword_docs.append(Document(page_content=content, metadata=meta))
            except Exception:
                pass

        # Merge, deduplicate by content
        seen = set()
        merged = []
        for doc in semantic_docs + keyword_docs:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                merged.append(doc)
        return merged

    def query(self, question: str):
        try:
            source_docs = self._hybrid_retrieve(question)
            context = format_docs(source_docs)
            prompt_val = self.prompt.format_messages(context=context, question=question)
            answer = self.llm.invoke(prompt_val)
            answer_text = answer.content if hasattr(answer, "content") else str(answer)
            return {
                "answer": answer_text,
                "source_documents": source_docs
            }
        except Exception as e:
            return {
                "answer": f"Error: {e}",
                "source_documents": []
            }
