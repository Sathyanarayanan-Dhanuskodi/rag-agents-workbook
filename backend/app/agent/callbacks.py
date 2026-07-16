"""
CORE CONCEPT 10 / 10 — HOOKS (Callbacks)   [OPTIONAL]
====================================================

"Hooks" in LangChain = the *callback* system. A callback handler is an object
with methods that LangChain calls automatically at key moments while a chain /
agent runs: when the LLM starts, when a tool is called, when it finishes, etc.
You hook into those events to log, trace, stream, or debug — WITHOUT changing
the agent's logic.

Here you'll use it to capture the agent's reasoning into a trace that the UI
displays: every tool the agent decided to call, its input, and its output.
That trace is the visible payoff — it makes the invisible agent loop visible.

This is OPTIONAL: if unimplemented, the agent still answers, just without the
step-by-step trace. agent_service.py falls back gracefully.

What to write: a `TraceCallbackHandler(BaseCallbackHandler)` that records steps.

    class TraceCallbackHandler(BaseCallbackHandler):
        def __init__(self):
            self.steps: list[dict] = []

        def on_tool_start(self, serialized, input_str, **kwargs):
            # append {"type": "tool_start", "tool": <name>, "input": input_str}
            ...

        def on_tool_end(self, output, **kwargs):
            # append {"type": "tool_end", "output": str(output)}
            ...

        # optional extras: on_llm_start / on_agent_action / on_agent_finish

CONTRACT: agent_service.py reads `handler.steps` after the run and returns it
to the UI. Each step should be a small dict with at least a "type" and enough
info to display (tool name, input, output). Keep it JSON-serializable.

Hints
-----
- from langchain_core.callbacks import BaseCallbackHandler
- The handler is passed to the agent at invoke time via
  config={"callbacks": [handler]} — agent_service.py already does this wiring.
- `serialized` is a dict describing the tool; the name is usually
  serialized.get("name").
- Method signatures vary by event; accept **kwargs to stay forward-compatible.

Docs: https://python.langchain.com/docs/concepts/callbacks/
      https://python.langchain.com/docs/how_to/custom_callbacks/
"""
from langchain_core.callbacks import BaseCallbackHandler


class TraceCallbackHandler(BaseCallbackHandler):
    """Records the agent's tool calls into self.steps for display in the UI."""

    def __init__(self) -> None:
        self.steps: list[dict] = []
        # TODO: implement the on_* hook methods below to fill self.steps.
        raise NotImplementedError(
            "Implement TraceCallbackHandler in app/agent/callbacks.py"
        )
