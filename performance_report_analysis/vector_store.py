import os
import json
from langchain_core.documents import Document
from langchain_chroma import Chroma
from embeddings import LocalONNXEmbeddings

def create_vector_store(processed_file_path: str, persist_dir: str, status_callback=None):
    if not os.path.exists(processed_file_path):
        print(f"Error: {processed_file_path} does not exist.")
        return None

    with open(processed_file_path, 'r', encoding='utf-8') as f:
        chunks_data = json.load(f)

    documents = []
    for chunk in chunks_data:
        doc = Document(
            page_content=chunk.get("page_content", ""),
            metadata=chunk.get("metadata", {})
        )
        documents.append(doc)

    msg = f"Loaded {len(documents)} chunks for embedding."
    print(msg)
    if status_callback:
        status_callback(msg)

    msg = "Initializing ONNX embeddings (local, no API calls)..."
    print(msg)
    if status_callback:
        status_callback(msg)

    embeddings = LocalONNXEmbeddings()

    msg = "Creating Chroma vector database..."
    print(msg)
    if status_callback:
        status_callback(msg)

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name="automobile_reports"
    )

    msg = f"✅ Vector DB ready! {len(documents)} chunks stored in ChromaDB."
    print(msg)
    if status_callback:
        status_callback(msg)

    return vectorstore

if __name__ == "__main__":
    processed_json = os.path.join(os.path.dirname(__file__), "data", "processed", "processed_chunks.json")
    persist_db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
    create_vector_store(processed_json, persist_db_dir)
