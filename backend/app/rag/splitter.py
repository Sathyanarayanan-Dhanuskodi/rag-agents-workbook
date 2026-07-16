"""
CORE CONCEPT 2 / 6 — TEXT SPLITTING (CHUNKING)
==============================================

Goal: break large Documents into smaller, overlapping chunks.

Why? Two reasons:
  1. Embedding models & LLM context windows have size limits.
  2. Retrieval is more precise on small chunks — a question usually maps to a
     paragraph, not a whole 50-page PDF.

Overlap (settings.chunk_overlap) keeps a sentence that straddles a chunk
boundary from being cut in half and losing meaning.

Hints
-----
- from langchain_text_splitters import RecursiveCharacterTextSplitter
  (this is the sensible default — it tries to split on paragraphs, then lines,
   then words, so chunks stay semantically whole)
- Configure it with chunk_size and chunk_overlap from `settings`.
- splitter.split_documents(docs) returns a new list[Document], preserving
  (and extending) each chunk's metadata for you.

Docs: https://python.langchain.com/docs/concepts/text_splitters/
"""
from langchain_core.documents import Document

from app.config import settings


def split_documents(docs: list[Document]) -> list[Document]:
    """Split Documents into overlapping chunks.

    Use settings.chunk_size and settings.chunk_overlap so the values stay
    tunable from the .env file.
    """
    # TODO: implement me
    raise NotImplementedError("Implement split_documents in app/rag/splitter.py")
