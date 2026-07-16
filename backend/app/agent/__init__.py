"""
The AGENT track — builds on top of the RAG pipeline. Four core concepts, YOUR job:

    7.  tools.py       → define tools the LLM can call (incl. your RAG retriever!)
    8.  agent.py       → instructions (system prompt) + the agent loop
    9.  mcp_tools.py   → load external tools from an MCP server
    10. callbacks.py   → hooks: observe the agent's reasoning as it runs

`agent_service.py` (already written) wires them together and is forgiving:
MCP (9) and callbacks (10) are OPTIONAL — the agent runs with just tools (7)
and the agent loop (8), and lights up more capability as you implement each one.
"""
