"""
CORE CONCEPT 7 / 10 — TOOL CALLING
==================================

Goal: give the LLM a set of *tools* it can choose to call. A "tool" is just a
function plus a description. The magic: the LLM reads each tool's NAME, its
DOCSTRING, and its ARGUMENT TYPES, and decides on its own when to call which
one and with what arguments. So the docstring isn't a comment — it's the
prompt the model uses to pick the tool. Write it for the model, not for you.

You'll write `get_local_tools()` returning a list of two tools:

  1. A CALCULATOR tool
       - Takes a math expression string, returns the result.
       - This is the "hello world" of tool calling — easy to verify the loop works.

  2. A RETRIEVER tool (this is the cool one)
       - Wraps YOUR RAG pipeline so the agent can *choose* to search the docs.
       - Reuse what you already built:
             from app.rag.embeddings import get_embeddings
             from app.rag.vectorstore import get_vectorstore
             from app.rag.retriever import get_retriever
         Inside the tool: open the store, get the retriever, .invoke(query),
         and return the joined chunk text. Name it something the model will
         understand, e.g. `search_documents`, and describe WHEN to use it
         ("use this to answer questions about the user's uploaded documents").

Hints
-----
- from langchain_core.tools import tool
- The decorator turns a plain function into a BaseTool:

      @tool
      def calculator(expression: str) -> str:
          '''Evaluate a basic arithmetic expression like "47 * 13".'''
          ...

- Keep tool return values as strings (or simple JSON) — they get fed back to
  the model as text.
- For the calculator, avoid raw eval() on untrusted input. A safe option is
  Python's ast module, or a tiny allow-list. (Good security habit to build.)

Docs: https://python.langchain.com/docs/concepts/tools/
      https://python.langchain.com/docs/how_to/custom_tools/
"""
from langchain_core.tools import BaseTool


def get_local_tools() -> list[BaseTool]:
    """Return the agent's local tools: a calculator and a document-search tool.

    The document-search tool should wrap the RAG retriever you built in
    app/rag/ so the agent can decide to look things up in the indexed docs.
    """
    # TODO: implement me — define your @tool functions above/inline and return them.
    raise NotImplementedError("Implement get_local_tools in app/agent/tools.py")
