"""
Pydantic request/response models — the contract between frontend and backend.
Scaffolding: you shouldn't need to change these while learning RAG.
"""
from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class Source(BaseModel):
    content: str          # the chunk text that was retrieved
    metadata: dict = {}   # e.g. {"source": "data/handbook.pdf", "page": 3}


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source] = []


class IngestResponse(BaseModel):
    files: list[str]
    chunks: int
    message: str


class StatusResponse(BaseModel):
    indexed_chunks: int
    llm_model: str
    embedding_model: str
    ready: bool          # True once the vector store has documents in it


# --- Agent track ---
class AgentRequest(BaseModel):
    question: str


class AgentStep(BaseModel):
    """One event in the agent's reasoning trace (produced by your callback)."""
    type: str                 # e.g. "tool_start", "tool_end"
    tool: str | None = None   # which tool was called
    input: str | None = None  # the tool's input
    output: str | None = None # the tool's output


class AgentResponse(BaseModel):
    answer: str
    steps: list[AgentStep] = []   # the tool-call trace shown in the UI
