"""
CORE CONCEPT 5 / 6 — RETRIEVAL
==============================

Goal: turn a vector store into a `retriever` — an object that, given a question
string, returns the top-k most relevant chunks.

This is the "R" in RAG. The retriever is the bridge between concept 4 (storage)
and concept 6 (generation).

Hints
-----
- Any LangChain vector store gives you one for free:
      vectorstore.as_retriever(search_kwargs={"k": settings.retrieval_k})
- `k` = how many chunks to pull back. Too few → missing context;
  too many → noise and a bloated prompt. settings.retrieval_k is your knob.
- The returned object has .invoke(question) -> list[Document].
- Later, experiment: search_type="mmr" (diversity), or metadata filters.

Docs: https://python.langchain.com/docs/concepts/retrievers/
"""
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore

from app.config import settings


def get_retriever(vectorstore: VectorStore) -> BaseRetriever:
    """Return a retriever that fetches settings.retrieval_k chunks per query."""
    # TODO: implement me
    raise NotImplementedError("Implement get_retriever in app/rag/retriever.py")
