"use client";

import { useEffect, useRef, useState } from "react";
import {
  agent,
  AgentStep,
  getStatus,
  ingest,
  query,
  Source,
  Status,
} from "@/lib/api";

type Mode = "rag" | "agent";

interface ChatMsg {
  role: "user" | "bot" | "err";
  text: string;
  sources?: Source[];
  steps?: AgentStep[];
  mode?: Mode;
}

export default function Home() {
  const [status, setStatus] = useState<Status | null>(null);
  const [mode, setMode] = useState<Mode>("rag");
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadNote, setUploadNote] = useState<string>("");
  const fileRef = useRef<HTMLInputElement>(null);

  async function refreshStatus() {
    try {
      setStatus(await getStatus());
    } catch {
      setStatus(null);
    }
  }

  useEffect(() => {
    refreshStatus();
  }, []);

  async function handleUpload() {
    const files = fileRef.current?.files;
    if (!files || files.length === 0) return;
    setUploading(true);
    setUploadNote("");
    try {
      const res = await ingest(files);
      setUploadNote(res.message);
      await refreshStatus();
    } catch (e) {
      setUploadNote(`⚠️ ${(e as Error).message}`);
    } finally {
      setUploading(false);
    }
  }

  async function handleAsk() {
    const q = question.trim();
    if (!q || asking) return;
    setMessages((m) => [...m, { role: "user", text: q }]);
    setQuestion("");
    setAsking(true);
    try {
      if (mode === "rag") {
        const res = await query(q);
        setMessages((m) => [
          ...m,
          { role: "bot", text: res.answer, sources: res.sources, mode },
        ]);
      } else {
        const res = await agent(q);
        setMessages((m) => [
          ...m,
          { role: "bot", text: res.answer, steps: res.steps, mode },
        ]);
      }
    } catch (e) {
      setMessages((m) => [...m, { role: "err", text: (e as Error).message }]);
    } finally {
      setAsking(false);
    }
  }

  const placeholder =
    mode === "rag"
      ? "Ask something about your documents…"
      : "Ask the agent (it can search docs + use tools)…";

  return (
    <div className="container">
      <div className="header">
        <div>
          <h1>RAG with LangChain</h1>
          <div className="subtitle">Learning project — you implement the core concepts.</div>
        </div>
        {status ? (
          <span className={`badge ${status.ready ? "ready" : "empty"}`}>
            {status.ready ? `${status.indexed_chunks} chunks indexed` : "no documents indexed"}
            {" · "}
            {status.llm_model}
          </span>
        ) : (
          <span className="badge empty">backend offline</span>
        )}
      </div>

      <div className="panel">
        <h2>1 · Add documents</h2>
        <div className="row">
          <input ref={fileRef} type="file" multiple accept=".pdf,.txt,.md" />
          <button onClick={handleUpload} disabled={uploading}>
            {uploading ? "Indexing…" : "Upload & index"}
          </button>
        </div>
        {uploadNote ? (
          <div className="hint" style={{ marginTop: 10 }}>{uploadNote}</div>
        ) : (
          <div className="hint" style={{ marginTop: 10 }}>
            A sample file (<span className="filename">langchain-rag-primer.txt</span>) is already in
            backend/data — upload it, or drop your own PDFs / text files.
          </div>
        )}
      </div>

      <div className="panel">
        <div className="panelhead">
          <h2 style={{ margin: 0 }}>2 · Ask</h2>
          <div className="toggle">
            <button
              className={`toggle-btn ${mode === "rag" ? "active" : ""}`}
              onClick={() => setMode("rag")}
            >
              RAG
            </button>
            <button
              className={`toggle-btn ${mode === "agent" ? "active" : ""}`}
              onClick={() => setMode("agent")}
            >
              Agent
            </button>
          </div>
        </div>

        <div className="hint" style={{ marginBottom: 12 }}>
          {mode === "rag"
            ? "RAG mode: retrieve chunks → stuff into the prompt → answer. One shot."
            : "Agent mode: the LLM decides which tools to call (search docs, calculator, MCP…) and loops until done. Try: “What's the secret passphrase in the primer, and what is 47*13?”"}
        </div>

        <div className="messages">
          {messages.length === 0 && (
            <div className="hint">
              {mode === "rag"
                ? "Try: “What is RAG?” or “What is the secret passphrase in the primer?”"
                : "The agent should call both the document-search tool and the calculator to answer the sample question."}
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>
              {m.text || (m.role === "bot" ? "(no answer text)" : "")}

              {m.steps && m.steps.length > 0 && (
                <details className="sources" open>
                  <summary>🧭 agent trace · {m.steps.length} step(s)</summary>
                  {m.steps.map((s, j) => (
                    <div className="step" key={j}>
                      <span className="step-type">{s.type}</span>
                      {s.tool && <span className="step-tool"> {s.tool}</span>}
                      {s.input && <div className="step-io">in: {s.input}</div>}
                      {s.output && <div className="step-io">out: {s.output.slice(0, 240)}</div>}
                    </div>
                  ))}
                </details>
              )}

              {m.mode === "agent" && (!m.steps || m.steps.length === 0) && m.role === "bot" && (
                <div className="hint" style={{ marginTop: 8 }}>
                  No trace captured — implement <span className="filename">app/agent/callbacks.py</span> to
                  see which tools the agent called.
                </div>
              )}

              {m.sources && m.sources.length > 0 && (
                <details className="sources">
                  <summary>{m.sources.length} source chunk(s)</summary>
                  {m.sources.map((s, j) => (
                    <div className="source" key={j}>
                      <div className="meta">
                        {(s.metadata?.source as string) ?? "source"}
                        {s.metadata?.page != null ? ` · p.${s.metadata.page}` : ""}
                      </div>
                      {s.content.slice(0, 300)}
                      {s.content.length > 300 ? "…" : ""}
                    </div>
                  ))}
                </details>
              )}
            </div>
          ))}
          {asking && <div className="spinner">{mode === "agent" ? "Agent thinking…" : "Thinking…"}</div>}
        </div>

        <div className="row">
          <input
            type="text"
            placeholder={placeholder}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          />
          <button onClick={handleAsk} disabled={asking || !question.trim()}>
            Ask
          </button>
        </div>
      </div>
    </div>
  );
}
