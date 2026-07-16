"""
CORE CONCEPT 4 / 6 — VECTOR STORE
=================================

Goal: store chunk-vectors so you can search them by similarity, and PERSIST
them to disk so you don't re-embed everything on every restart.

You'll write TWO functions:

  build_vectorstore(chunks, embeddings) -> Chroma
      Called during ingestion. Embeds every chunk and writes them to disk.

  get_vectorstore(embeddings) -> Chroma
      Called at query time. Opens the already-persisted store (no re-embedding).

Both point at the SAME on-disk location: settings.chroma_dir.

Hints
-----
- from langchain_chroma import Chroma
- To CREATE from documents:
      Chroma.from_documents(documents=chunks,
                            embedding=embeddings,
                            persist_directory=settings.chroma_dir)
- To OPEN an existing store:
      Chroma(persist_directory=settings.chroma_dir,
            embedding_function=embeddings)
- `count_chunks` is used by the /status endpoint. A Chroma store `vs` exposes
  vs._collection.count(), or you can call get_vectorstore() and count it.

Docs: https://python.langchain.com/docs/integrations/vectorstores/chroma/
"""
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from app.config import settings


def build_vectorstore(chunks: list[Document], embeddings: Embeddings) -> Chroma:
    """Embed chunks and persist them to settings.chroma_dir. Return the store."""
    # TODO: implement me
    raise NotImplementedError("Implement build_vectorstore in app/rag/vectorstore.py")


def get_vectorstore(embeddings: Embeddings) -> Chroma:
    """Open the already-persisted Chroma store at settings.chroma_dir."""
    # TODO: implement me
    raise NotImplementedError("Implement get_vectorstore in app/rag/vectorstore.py")


def count_chunks() -> int:
    """Return how many chunks are currently indexed (for the /status endpoint).

    Return 0 if the store doesn't exist yet. This one is a freebie helper —
    but it depends on get_vectorstore(), so it starts working once you've
    implemented the two functions above. Feel free to adjust.
    """
    import os

    if not os.path.isdir(settings.chroma_dir):
        return 0
    try:
        from app.rag.embeddings import get_embeddings

        vs = get_vectorstore(get_embeddings())
        return vs._collection.count()
    except Exception:
        return 0
