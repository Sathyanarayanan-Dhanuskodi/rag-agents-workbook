"""
ORCHESTRATION — this ties your six stubs together. Already written for you.

Read it to understand the *flow*, but you don't need to edit it. It calls the
functions you implement in the other files, in the right order.

    Ingestion:  load -> split -> embed -> store
    Query:      open store -> retriever -> llm -> chain -> answer + sources
"""
from langchain_core.documents import Document

from app.rag.chain import build_rag_chain, get_llm
from app.rag.embeddings import get_embeddings
from app.rag.loader import load_documents
from app.rag.retriever import get_retriever
from app.rag.splitter import split_documents
from app.rag.vectorstore import build_vectorstore, get_vectorstore


def ingest(paths: list[str]) -> int:
    """Full ingestion pipeline. Returns the number of chunks indexed."""
    docs = load_documents(paths)          # concept 1
    chunks = split_documents(docs)        # concept 2
    embeddings = get_embeddings()         # concept 3
    build_vectorstore(chunks, embeddings) # concept 4 (persists to disk)
    return len(chunks)


def answer(question: str) -> dict:
    """Full query pipeline. Returns {"answer": str, "sources": list[Document]}."""
    embeddings = get_embeddings()                 # concept 3 (same model as ingest!)
    vectorstore = get_vectorstore(embeddings)     # concept 4
    retriever = get_retriever(vectorstore)        # concept 5
    llm = get_llm()                               # concept 6
    chain = build_rag_chain(retriever, llm)       # concept 6
    result = chain.invoke(question)

    # Be forgiving about the shape the chain returns, so a partial
    # implementation still gives useful output while you're learning.
    if isinstance(result, dict):
        return {
            "answer": result.get("answer", ""),
            "sources": result.get("sources", []),
        }
    return {"answer": str(result), "sources": []}


def docs_to_sources(docs: list[Document]) -> list[dict]:
    """Convert retrieved Documents into the API's Source shape."""
    return [{"content": d.page_content, "metadata": d.metadata} for d in docs]
