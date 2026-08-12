from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agentic-data-analyst")


@mcp.tool()
def ping() -> str:
    return "MCP server is ready."


if __name__ == "__main__":
    mcp.run()
