"""
The RAG pipeline lives here. Six files, six core concepts — YOUR job to implement:

    1. loader.py      → load raw files into LangChain Documents
    2. splitter.py    → chop Documents into overlapping chunks
    3. embeddings.py  → turn text into vectors (Ollama)
    4. vectorstore.py → store & persist those vectors (Chroma)
    5. retriever.py   → fetch the most relevant chunks for a question
    6. chain.py       → the LLM + prompt that turns chunks into an answer

`service.py` (already written) wires them together. You don't touch it —
you just fill in the six stubs and the whole app works.
"""
