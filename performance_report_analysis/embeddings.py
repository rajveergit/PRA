"""
Custom embedding class that wraps ChromaDB's built-in ONNX-based
DefaultEmbeddingFunction, avoiding sentence-transformers/Keras conflicts.
"""
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from langchain_core.embeddings import Embeddings
from typing import List

_EF = None  # singleton to avoid reloading the model repeatedly

def get_ef():
    global _EF
    if _EF is None:
        _EF = DefaultEmbeddingFunction()
    return _EF

class LocalONNXEmbeddings(Embeddings):
    """Uses ChromaDB's ONNX-based embedding (all-MiniLM-L6-v2 via onnxruntime)."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        ef = get_ef()
        return ef(texts)

    def embed_query(self, text: str) -> List[float]:
        ef = get_ef()
        return ef([text])[0]
