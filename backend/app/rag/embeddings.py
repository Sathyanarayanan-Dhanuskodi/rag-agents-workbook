"""
CORE CONCEPT 3 / 6 — EMBEDDINGS
===============================

Goal: return an Embeddings object that converts text -> vectors (lists of floats).

Semantically similar text produces vectors that are close together. That's the
whole trick behind retrieval: embed the question, find chunks whose vectors are
nearest to it.

You do NOT call it directly here — you just build and return the object.
The vector store (concept 4) uses it under the hood to embed every chunk,
and the retriever uses it to embed the incoming question.

Hints
-----
- from langchain_ollama import OllamaEmbeddings
- Configure it with:
      model=settings.embedding_model      (e.g. "nomic-embed-text")
      base_url=settings.ollama_base_url
- IMPORTANT: the embedding model used to BUILD the index must be the SAME one
  used to QUERY it. That's why this is a single shared function.

Docs: https://python.langchain.com/docs/concepts/embedding_models/
"""
from langchain_core.embeddings import Embeddings

from app.config import settings


def get_embeddings() -> Embeddings:
    """Return the embedding model (Ollama), configured from `settings`."""
    # TODO: implement me
    raise NotImplementedError("Implement get_embeddings in app/rag/embeddings.py")
