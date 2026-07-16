// Thin client for the FastAPI backend. Scaffolding — no need to edit.

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Source {
  content: string;
  metadata: Record<string, unknown>;
}

export interface QueryResponse {
  answer: string;
  sources: Source[];
}

export interface Status {
  indexed_chunks: number;
  llm_model: string;
  embedding_model: string;
  ready: boolean;
}

async function unwrap<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      if (body?.detail) detail = body.detail;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export async function getStatus(): Promise<Status> {
  return unwrap<Status>(await fetch(`${BASE}/api/status`, { cache: "no-store" }));
}

export async function ingest(files: FileList): Promise<{ chunks: number; message: string }> {
  const form = new FormData();
  Array.from(files).forEach((f) => form.append("files", f));
  return unwrap(await fetch(`${BASE}/api/ingest`, { method: "POST", body: form }));
}

export async function query(question: string): Promise<QueryResponse> {
  return unwrap<QueryResponse>(
    await fetch(`${BASE}/api/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })
  );
}

export interface AgentStep {
  type: string;
  tool?: string | null;
  input?: string | null;
  output?: string | null;
}

export interface AgentResponse {
  answer: string;
  steps: AgentStep[];
}

export async function agent(question: string): Promise<AgentResponse> {
  return unwrap<AgentResponse>(
    await fetch(`${BASE}/api/agent`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })
  );
}
