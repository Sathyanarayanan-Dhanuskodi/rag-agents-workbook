"""
CORE CONCEPT 1 / 6 — DOCUMENT LOADING
=====================================

Goal: read raw files off disk and turn them into LangChain `Document` objects.

A `Document` has two important attributes:
    - .page_content : str   (the actual text)
    - .metadata     : dict  (e.g. {"source": "data/handbook.pdf", "page": 2})

Why metadata matters: later you'll show the user WHERE an answer came from.
Keep the source path in metadata and it flows all the way to the UI for free.

Hints
-----
- For PDFs:   from langchain_community.document_loaders import PyPDFLoader
- For .txt/.md: from langchain_community.document_loaders import TextLoader
- A loader's .load() returns a list[Document].
- You're given a list of paths — loop, pick a loader by file extension,
  and concatenate all the Documents into one list.

Docs: https://python.langchain.com/docs/concepts/document_loaders/
"""
from langchain_core.documents import Document


def load_documents(paths: list[str]) -> list[Document]:
    """Load the given files into a flat list of Documents.

    Args:
        paths: file paths, e.g. ["data/handbook.pdf", "data/notes.txt"]

    Returns:
        A list of Documents with .page_content and .metadata populated.
    """
    # TODO: implement me
    raise NotImplementedError("Implement load_documents in app/rag/loader.py")
