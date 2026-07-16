# RAG with LangChain — a learn-by-building project

A full-stack RAG + agent app where **everything around the interesting parts is
already built** (Next.js UI, FastAPI backend, file upload, sources display, local
Ollama models, one-command setup) — and the **ten core concepts are left for you
to implement** as documented stubs. Fill them in and the app comes to life.

You learn by writing the code that matters, not by wiring up boilerplate or
fighting CORS.

**Who this is for:** you know Python, and you want to actually *understand* RAG
and agents rather than copy-paste a tutorial. No prior LangChain needed. No API
keys, no cloud bill — everything runs locally on Ollama.

**What you'll build:**

| Track | Concepts | You end up with |
|---|---|---|
| **1 · RAG** | loading, chunking, embeddings, vector stores, retrieval, the RAG chain | A chatbot that answers questions about your own documents, with sources |
| **2 · Agents** | tool calling, the agent loop, instructions, MCP, callbacks/hooks | An agent that decides when to search your docs, do math, or call MCP tools — with its reasoning visible |

**How it works:** every `← YOU` file below is a stub with a detailed docstring,
the exact signature, hints, and doc links — but it raises `NotImplementedError`.
The app runs from day one and tells you (via a 501 in the UI) which file to write
next. There are no solutions in this repo on purpose; the hints are designed to be
enough. Getting stuck for a bit *is* the exercise.

## Quick start

```bash
ollama pull llama3.2 && ollama pull nomic-embed-text   # one-time, see step 0 below
pnpm dev                                               # that's it
```

`pnpm dev` bootstraps whatever is missing (venv, Python deps, node deps,
`.env` files) and then runs **both** services together:

| | |
|---|---|
| backend | http://localhost:8000 (API docs at `/docs`) |
| frontend | http://localhost:3000 |

Ctrl+C stops both. Re-runs skip the bootstrap, so it starts in about a second.

```
rag-with-langchain/
├── package.json                 monorepo root — scripts
├── pnpm-workspace.yaml          declares `frontend` as a workspace
├── scripts/
│   ├── dev.sh                   starts backend + frontend together
│   └── setup.sh                 idempotent bootstrap (venv, deps, .env)
├── backend/                     FastAPI + LangChain
│   ├── app/
│   │   ├── main.py              HTTP endpoints            (done)
│   │   ├── config.py            settings from .env        (done)
│   │   ├── schemas.py           request/response models   (done)
│   │   ├── rag/
│   │   │   ├── service.py       orchestration / flow      (done — read it!)
│   │   │   ├── loader.py        ① document loading        ← YOU
│   │   │   ├── splitter.py      ② chunking                ← YOU
│   │   │   ├── embeddings.py    ③ embeddings              ← YOU
│   │   │   ├── vectorstore.py   ④ vector store            ← YOU
│   │   │   ├── retriever.py     ⑤ retrieval               ← YOU
│   │   │   └── chain.py         ⑥ the RAG chain           ← YOU
│   │   └── agent/
│   │       ├── agent_service.py orchestration / flow      (done — read it!)
│   │       ├── tools.py         ⑦ tool calling            ← YOU
│   │       ├── agent.py         ⑧ agent loop + instructions ← YOU
│   │       ├── mcp_tools.py     ⑨ MCP (optional)          ← YOU
│   │       └── callbacks.py     ⑩ hooks / callbacks (opt) ← YOU
│   ├── data/                    sample + uploaded docs
│   └── requirements.txt
└── frontend/                    Next.js chat + upload UI  (done)
```

## Your progress checklist

Work top to bottom — each concept builds on the ones above it.

**Track 1 — RAG** (`backend/app/rag/`)
- [ ] ① `loader.py` — load files into LangChain `Document`s
- [ ] ② `splitter.py` — split them into overlapping chunks
- [ ] ③ `embeddings.py` — turn text into vectors
- [ ] ④ `vectorstore.py` — store & persist the vectors (Chroma)
- [ ] → *checkpoint:* **Upload & index** the sample file; the badge shows a chunk count
- [ ] ⑤ `retriever.py` — fetch the top-k chunks for a question
- [ ] ⑥ `chain.py` — the prompt + LLM that turns chunks into an answer
- [ ] → *checkpoint:* ask **"What is the secret passphrase in the primer?"** → `orange elephant marmalade`

**Track 2 — Agents** (`backend/app/agent/`)
- [ ] ⑦ `tools.py` — define tools with `@tool` (incl. one wrapping your retriever)
- [ ] ⑧ `agent.py` — the system prompt (instructions) + the agent loop
- [ ] → *checkpoint:* in **Agent** mode, ask **"What's the secret passphrase in the primer, and what is 47*13?"** → it must call *both* tools to get `orange elephant marmalade` and `611`
- [ ] ⑩ `callbacks.py` — hooks that capture the agent's reasoning (optional)
- [ ] → *checkpoint:* the trace panel now shows every tool call
- [ ] ⑨ `mcp_tools.py` — load external tools from an MCP server (optional)

The data flow you're building (see `service.py` / `agent_service.py`):

```
INGEST:  files → load → split → embed → store in Chroma
QUERY:   question → retrieve top-k chunks → stuff into prompt → LLM → answer
AGENT:   question → LLM picks a tool → run it → feed result back → repeat → answer
```

## One-time setup

### 0. Install pnpm and Ollama
The only steps `pnpm dev` can't do for you. pnpm:
```bash
npm install -g pnpm            # or: https://pnpm.io/installation
```
Then Ollama and the models (local, free, no API key):
```bash
# Install: https://ollama.com/download
ollama pull llama3.2           # the chat model
ollama pull nomic-embed-text   # the embedding model
# Ollama serves on http://localhost:11434 automatically.
```
`setup.sh` warns you if Ollama isn't running or a model is missing.

### 1. Everything else
```bash
pnpm dev
```
On first run this creates `backend/.venv`, installs `requirements.txt` (a few
minutes), installs node deps, and copies `.env.example` → `.env` and
`.env.local.example` → `.env.local`. Edit those `.env` files afterwards; setup
never overwrites them.

## Root commands

| Command | What it does |
|---|---|
| `pnpm dev` | Bootstrap if needed, then run backend + frontend together |
| `pnpm setup` | Bootstrap only (no servers) |
| `pnpm dev:backend` | Backend alone, on :8000 |
| `pnpm dev:frontend` | Frontend alone, on :3000 |
| `pnpm build` | Production build of the frontend |
| `pnpm clean:index` | Wipe the Chroma index and start fresh |
| `pnpm clean` | Remove `node_modules`, `.next`, and the venv |

The frontend is a pnpm workspace (`pnpm-workspace.yaml`), so `pnpm install` at
the root installs it too, from the root `pnpm-lock.yaml`. To add a frontend
dependency: `pnpm --filter rag-frontend add <pkg>`. Python deps stay in
`backend/.venv` — setup reinstalls them only when `requirements.txt` changes.

## The learning loop

1. Open http://localhost:3000. The status badge shows the backend is up but
   "no documents indexed".
2. Implement `loader.py` → `splitter.py` → `embeddings.py` → `vectorstore.py`,
   then click **Upload & index** on the sample file. Watch the chunk count.
3. Implement `retriever.py` → `chain.py`, then ask a question.
4. Test that retrieval really works: ask *"What is the secret passphrase in the
   primer?"* — the answer (`orange elephant marmalade`) only appears if your
   pipeline retrieved the right chunk and grounded the answer in it.

## Track 2 — Agents (tool calling, agents, MCP, instructions, hooks)

Once RAG works, switch the UI to **Agent** mode (toggle in section 2). Now instead
of a fixed retrieve→answer chain, an LLM decides *which tools to call* and loops
until it has an answer. The best part: **your RAG retriever becomes one of its
tools**, so the agent can choose to search your documents.

Concepts you implement (they build on RAG ①–⑥):

| # | File | Concept | Required? |
|---|------|---------|-----------|
| ⑦ | `agent/tools.py` | **Tool calling** — `@tool` functions (a calculator + a `search_documents` tool wrapping your retriever) | required |
| ⑧ | `agent/agent.py` | **Agents + Instructions** — the `SYSTEM_PROMPT` and the agent loop (`create_react_agent`) | required |
| ⑨ | `agent/mcp_tools.py` | **MCP** — load tools from an MCP server into the agent | optional |
| ⑩ | `agent/callbacks.py` | **Hooks (callbacks)** — capture the agent's reasoning into the trace shown in the UI | optional |

Mapping to your original wishlist: **instructions** = the system prompt in ⑧;
**hooks** = the callback handler in ⑩. (Skills & plugins have no LangChain
equivalent — they're Claude Code / Agent SDK features, a separate track.)

Notes:
- The agent reuses `get_llm()` from RAG ⑥ and needs a built index (for its search
  tool), so finish Track 1 first.
- Tool calling depends on the model. `llama3.2` works; if the agent ignores its
  tools, try a stronger tool-user: `ollama pull qwen2.5` and set `LLM_MODEL=qwen2.5`.
- MCP is opt-in: implement `mcp_tools.py`, then set `MCP_ENABLED=true` in
  `backend/.env`. (It needs `npx`, which ships with the Node you already have.)
- **The test that proves it all works** (Agent mode): ask
  *"What's the secret passphrase in the primer, and what is 47*13?"* — a correct
  answer forces the agent to call **both** the document-search tool
  (`orange elephant marmalade`) and the calculator (`611`), and once you've done
  ⑩ the trace panel shows both calls.

## Tips
- No need to restart after editing a stub — the backend runs with `--reload`, and
  the frontend hot-reloads too.
- The `.env` knobs (`CHUNK_SIZE`, `RETRIEVAL_K`, models…) are yours to experiment with.
- If ingest/query returns a 500 mentioning connection refused, Ollama isn't running.
- `pnpm clean:index` wipes the Chroma index (`backend/chroma_db/`) to start fresh.
- Changed `requirements.txt`? Just `pnpm dev` — setup reinstalls deps when it
  detects the change.

## If you get stuck

1. **Read the error.** The 501s name the exact file to implement; the 500s are
   usually Ollama not running or a model not pulled.
2. **Re-read the stub's docstring** — the hints name the exact class or function
   you need, and every stub links to the relevant LangChain page.
3. **Poke at it in isolation.** `backend/.venv/bin/python -c "..."` beats guessing;
   or use the API docs at http://localhost:8000/docs to hit one endpoint at a time.
4. **Check the contract.** `service.py` and `agent_service.py` show exactly what
   shape each function must return.
5. Reference: the [official LangChain RAG tutorial](https://python.langchain.com/docs/tutorials/rag/)
   and [LangGraph agents](https://langchain-ai.github.io/langgraph/agents/agents/).

## License

MIT — see [LICENSE](LICENSE). Fork it, teach with it, break it.
