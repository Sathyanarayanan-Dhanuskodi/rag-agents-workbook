"""
AGENT ORCHESTRATION — already written for you. Read it to see the flow.

Assembles tools → builds the agent → runs it (capturing a trace) → returns the
final answer plus the step-by-step trace of tool calls.

Graceful degradation (so the app is usable while you're still coding stubs):
  - REQUIRED: get_local_tools (concept 7), build_agent (concept 8), get_llm
    (RAG concept 6). If any of these is unimplemented, the /api/agent endpoint
    returns a helpful 501 telling you which file to write.
  - OPTIONAL: MCP tools (concept 9) and the trace callback (concept 10). If those
    aren't implemented yet, they're skipped — the agent still answers.
"""
import logging

from langchain_core.messages import BaseMessage

from app.agent.agent import build_agent
from app.agent.tools import get_local_tools
from app.config import settings
from app.rag.chain import get_llm

logger = logging.getLogger("agent")


def _extract_answer(result) -> str:
    """Pull the final answer out of whatever the agent returned."""
    if isinstance(result, dict):
        msgs = result.get("messages")
        if msgs:
            last = msgs[-1]
            return getattr(last, "content", str(last))
        if "output" in result:
            return str(result["output"])
    if isinstance(result, BaseMessage):
        return result.content
    return str(result)


async def _gather_tools() -> list:
    """Local tools always; MCP tools too if enabled AND implemented."""
    tools = get_local_tools()  # required — NotImplementedError bubbles up to a 501

    if settings.mcp_enabled:
        try:
            from app.agent.mcp_tools import get_mcp_tools

            mcp_tools = await get_mcp_tools()
            tools = tools + list(mcp_tools)
            logger.info("Loaded %d MCP tool(s).", len(mcp_tools))
        except NotImplementedError:
            logger.warning(
                "MCP_ENABLED=true but get_mcp_tools() isn't implemented yet — "
                "skipping MCP (implement app/agent/mcp_tools.py to enable it)."
            )
        except Exception as exc:  # bad server config, npx missing, etc.
            logger.warning("MCP tools failed to load (%s) — continuing without them.", exc)

    return tools


def _make_trace_handler():
    """Return a TraceCallbackHandler if concept 10 is implemented, else None."""
    try:
        from app.agent.callbacks import TraceCallbackHandler

        return TraceCallbackHandler()
    except NotImplementedError:
        logger.info(
            "callbacks.py not implemented yet — running without a reasoning trace "
            "(implement app/agent/callbacks.py to see the agent's tool calls)."
        )
        return None


async def run_agent(question: str) -> dict:
    """Run the agent on a question. Returns {"answer": str, "steps": list[dict]}."""
    tools = await _gather_tools()            # concept 7 (+9 if enabled)
    llm = get_llm()                          # RAG concept 6 (reused)
    agent = build_agent(llm, tools)          # concept 8 (+ instructions)

    handler = _make_trace_handler()          # concept 10 (optional)
    config = {"callbacks": [handler]} if handler else {}
    payload = {"messages": [("user", question)]}

    if hasattr(agent, "ainvoke"):
        result = await agent.ainvoke(payload, config=config)
    else:  # a hand-rolled sync agent still works
        result = agent.invoke(payload, config=config)

    return {
        "answer": _extract_answer(result),
        "steps": handler.steps if handler else [],
    }
