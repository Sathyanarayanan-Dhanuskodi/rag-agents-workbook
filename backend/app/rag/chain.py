"""
CORE CONCEPT 6 / 6 — THE RAG CHAIN (generation)
===============================================

This is the "A + G" of RAG: Augment the prompt with retrieved context, then
Generate an answer. Two functions to write.

--------------------------------------------------------------------------
get_llm() -> the Ollama chat model
--------------------------------------------------------------------------
Hints:
  - from langchain_ollama import ChatOllama
  - model=settings.llm_model, base_url=settings.ollama_base_url
  - Optionally temperature=0 for factual, less "creative" answers.

--------------------------------------------------------------------------
build_rag_chain(retriever, llm) -> a Runnable
--------------------------------------------------------------------------
CONTRACT (service.py depends on this):
    chain.invoke("some question")  MUST return a dict:
        {
          "answer":  "<the generated string answer>",
          "sources": [Document, Document, ...]   # the chunks you retrieved
        }
    Returning the sources is what powers the "where did this come from?" UI.

The classic LCEL recipe:
  1. Build a prompt that injects {context} and {question}. Instruct the model
     to answer ONLY from the context and to say "I don't know" if the answer
     isn't there — this is what stops hallucination:

        from langchain_core.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_template('''
        Answer the question using ONLY the context below.
        If the context doesn't contain the answer, say you don't know.

        Context:
        {context}

        Question: {question}
        ''')

  2. Retrieve docs, then format them into a single {context} string
     (e.g. "\n\n".join(d.page_content for d in docs)).

  3. Wire it with LCEL. One clean way to ALSO surface sources:

        from langchain_core.runnables import RunnableParallel, RunnablePassthrough
        from langchain_core.output_parsers import StrOutputParser

        def format_docs(docs): return "\n\n".join(d.page_content for d in docs)

        retrieve = RunnableParallel(
            context=retriever,          # question -> list[Document]
            question=RunnablePassthrough(),
        )
        generate = (
            RunnableParallel(
                context=lambda x: format_docs(x["context"]),
                question=lambda x: x["question"],
            )
            | prompt | llm | StrOutputParser()
        )
        chain = retrieve | RunnableParallel(
            answer=generate,
            sources=lambda x: x["context"],
        )
        return chain

  (Don't just copy this blindly — read the LCEL docs and understand each pipe.
   Getting the data to flow is the "aha" moment of LangChain.)

Docs:
  - LCEL:   https://python.langchain.com/docs/concepts/lcel/
  - RAG tutorial: https://python.langchain.com/docs/tutorials/rag/
"""
from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable

from app.config import settings


def get_llm() -> BaseChatModel:
    """Return the Ollama chat model, configured from `settings`."""
    # TODO: implement me
    raise NotImplementedError("Implement get_llm in app/rag/chain.py")


def build_rag_chain(retriever: BaseRetriever, llm: BaseChatModel) -> Runnable:
    """Return a Runnable whose .invoke(question) -> {"answer", "sources"}.

    See the CONTRACT and recipe in this module's docstring.
    """
    # TODO: implement me
    raise NotImplementedError("Implement build_rag_chain in app/rag/chain.py")
