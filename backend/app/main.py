"""
FastAPI application — the HTTP layer. Fully written scaffolding.

Endpoints:
    GET  /api/status   -> is the index ready? which models?
    POST /api/ingest   -> upload files, run the ingestion pipeline
    POST /api/query    -> ask a question, get an answer + sources

While your RAG stubs are unimplemented, the /ingest and /query endpoints
catch NotImplementedError and return HTTP 501 with a helpful message telling
you which file to go implement. So you can run the whole app from day one.
"""
import os
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.agent import agent_service
from app.config import settings
from app.rag import service
from app.rag.vectorstore import count_chunks
from app.schemas import (
    AgentRequest,
    AgentResponse,
    AgentStep,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    StatusResponse,
)

app = FastAPI(title="RAG with LangChain — Learning Project")

# Let the Next.js dev server (localhost:3000) call us during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _not_implemented(exc: NotImplementedError) -> HTTPException:
    return HTTPException(
        status_code=501,
        detail=f"Not implemented yet 👉 {exc}. Go write the core RAG code!",
    )


@app.get("/api/status", response_model=StatusResponse)
def status() -> StatusResponse:
    indexed = count_chunks()
    return StatusResponse(
        indexed_chunks=indexed,
        llm_model=settings.llm_model,
        embedding_model=settings.embedding_model,
        ready=indexed > 0,
    )


@app.post("/api/ingest", response_model=IngestResponse)
async def ingest(files: list[UploadFile] = File(...)) -> IngestResponse:
    os.makedirs(settings.data_dir, exist_ok=True)
    saved_paths: list[str] = []

    for f in files:
        dest = os.path.join(settings.data_dir, os.path.basename(f.filename))
        with open(dest, "wb") as out:
            shutil.copyfileobj(f.file, out)
        saved_paths.append(dest)

    try:
        n_chunks = service.ingest(saved_paths)
    except NotImplementedError as exc:
        raise _not_implemented(exc)
    except Exception as exc:  # surface real errors (e.g. Ollama not running)
        raise HTTPException(status_code=500, detail=str(exc))

    return IngestResponse(
        files=[os.path.basename(p) for p in saved_paths],
        chunks=n_chunks,
        message=f"Indexed {n_chunks} chunks from {len(saved_paths)} file(s).",
    )


@app.post("/api/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty.")
    try:
        result = service.answer(req.question)
    except NotImplementedError as exc:
        raise _not_implemented(exc)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return QueryResponse(
        answer=result["answer"],
        sources=service.docs_to_sources(result["sources"]),
    )


@app.post("/api/agent", response_model=AgentResponse)
async def agent_endpoint(req: AgentRequest) -> AgentResponse:
    """Run the tool-calling agent (agent mode in the UI)."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty.")
    try:
        result = await agent_service.run_agent(req.question)
    except NotImplementedError as exc:
        raise _not_implemented(exc)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    # Be forgiving about the exact keys your callback produced.
    steps = [
        AgentStep(
            type=str(s.get("type", "step")),
            tool=(str(s["tool"]) if s.get("tool") is not None else None),
            input=(str(s["input"]) if s.get("input") is not None else None),
            output=(str(s["output"]) if s.get("output") is not None else None),
        )
        for s in result.get("steps", [])
        if isinstance(s, dict)
    ]
    return AgentResponse(answer=result["answer"], steps=steps)
