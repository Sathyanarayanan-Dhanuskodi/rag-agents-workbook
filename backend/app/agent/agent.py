"""
CORE CONCEPT 8 / 10 — AGENTS + INSTRUCTIONS
===========================================

An *agent* is an LLM in a loop with tools:

    ┌─ LLM reads the question + the available tools
    │   ├─ decides: answer directly, OR call a tool
    │   ├─ if it calls a tool → run it → feed the result back to the LLM
    │   └─ repeat until the LLM produces a final answer
    └─ (bounded by a max number of steps so it can't loop forever)

Two things to write:

--------------------------------------------------------------------------
A) SYSTEM_PROMPT  — the "instructions" concept
--------------------------------------------------------------------------
The system prompt is how you shape the agent's behavior: its persona, its
rules, when to use which tool, how to format answers. This IS "instructions"
in LangChain terms. Write a short, direct prompt, e.g.:

    - "You are a helpful research assistant."
    - "When the user asks about their documents, use the search_documents tool."
    - "When a calculation is needed, use the calculator tool — don't do mental math."
    - "If the documents don't contain the answer, say so."

Good instructions are the difference between an agent that uses its tools and
one that guesses. Iterate on this — it's the highest-leverage text you'll write.

--------------------------------------------------------------------------
B) build_agent(llm, tools) -> a runnable agent
--------------------------------------------------------------------------
CONTRACT (agent_service.py depends on this):
    The returned object is invoked as:
        agent.invoke({"messages": [("user", question)]}, config=...)
    and its result exposes the conversation as result["messages"], where the
    LAST message's .content is the final answer. (This is exactly the shape
    LangGraph's prebuilt ReAct agent uses — see the easy path below.)

Easy path (recommended first):
    from langgraph.prebuilt import create_react_agent
    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

Understand-the-mechanics path (do this once it works, to see under the hood):
    - llm_with_tools = llm.bind_tools(tools)
    - loop: call the model; if the reply has .tool_calls, execute each tool,
      append ToolMessage(result) to the message list, and call the model again;
      otherwise return. Cap iterations with settings.agent_max_steps.
    (If you go this route, keep the same invoke/return contract above, or adapt
     agent_service.py — it's yours.)

Hints
-----
- The llm is passed in already configured (Ollama). Make sure your model
  supports tool calling — llama3.2 does; qwen2.5 is even better at it.
- settings.agent_max_steps caps the loop.

Docs:
  - Agents:  https://langchain-ai.github.io/langgraph/agents/agents/
  - create_react_agent: https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent
"""
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool

from app.config import settings

# TODO: write the agent's instructions here.
SYSTEM_PROMPT = ""  # ← YOU: replace with real instructions (see section A above)


def build_agent(llm: BaseChatModel, tools: list[BaseTool]):
    """Build and return an agent (LLM + tools + instructions) as a runnable.

    See the CONTRACT in this module's docstring for the invoke/return shape
    that agent_service.py expects.
    """
    # TODO: implement me
    raise NotImplementedError("Implement build_agent in app/agent/agent.py")
