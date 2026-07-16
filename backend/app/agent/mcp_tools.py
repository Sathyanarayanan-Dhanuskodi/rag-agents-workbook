"""
CORE CONCEPT 9 / 10 — MCP (Model Context Protocol)   [OPTIONAL]
==============================================================

MCP is an open standard for exposing tools/data to LLM apps. Instead of you
writing every tool by hand, you connect to an MCP *server* (there are hundreds:
filesystem, GitHub, Postgres, web search, ...) and it hands you tools your agent
can call. `langchain-mcp-adapters` converts those MCP tools into LangChain
tools, so they drop straight into the same agent you built in concept 8.

This is OPTIONAL: the agent works fine without it. It only runs when you set
MCP_ENABLED=true in .env. Until you implement this, agent_service.py just skips
MCP and uses your local tools.

What to write: `async get_mcp_tools() -> list[BaseTool]`

Hints
-----
- from langchain_mcp_adapters.client import MultiServerMCPClient
- Configure one or more servers by name. A stdio server launched via npx, e.g.
  the reference "everything" server (great for testing — has an `add` tool):

      client = MultiServerMCPClient({
          "everything": {
              "command": "npx",
              "args": ["-y", "@modelcontextprotocol/server-everything"],
              "transport": "stdio",
          }
      })
      tools = await client.get_tools()
      return tools

- Requires Node/npx installed (the server runs as a subprocess).
- Return an empty list (not an error) if you'd rather no-op when misconfigured —
  but raising NotImplementedError is fine too; agent_service.py catches it.
- Later: try a real server like "@modelcontextprotocol/server-filesystem" scoped
  to your data/ dir, and watch the agent read files through MCP.

Docs:
  - MCP:  https://modelcontextprotocol.io/
  - Adapters: https://github.com/langchain-ai/langchain-mcp-adapters
"""
from langchain_core.tools import BaseTool


async def get_mcp_tools() -> list[BaseTool]:
    """Connect to the configured MCP server(s) and return their tools.

    Called only when settings.mcp_enabled is True.
    """
    # TODO: implement me (or return [] to no-op)
    raise NotImplementedError("Implement get_mcp_tools in app/agent/mcp_tools.py")
