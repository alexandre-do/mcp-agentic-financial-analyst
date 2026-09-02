from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

if __package__ in (None, ""):
    # Allow running this file directly (e.g. `python info_agent.py` or an
    # IDE "Run" button) in addition to `python -m app.src.agents.info_agent`.
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    __package__ = "app.src.agents"

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StreamableHttpConnection

from ..prompt_template import PROMPT_SYS_AGENT_INFO

load_dotenv()

MODEL = init_chat_model(model=os.environ.get("MODEL_ID"))

# External MCP servers this agent is allowed to pull tools from. Add another
# entry here to give the agent access to more external data providers.
MCP_SERVERS: dict[str, StreamableHttpConnection] = {
    "alphavantage": {
        "transport": "streamable_http",
        "url": f"https://mcp.alphavantage.co/mcp?apikey={os.environ.get('ALPHA_VANTAGE_API_KEY', '')}",
    },
}

mcp_client = MultiServerMCPClient(MCP_SERVERS)  # type: ignore[arg-type]


async def build_info_agent(server_name: str | None = None):
    """Discover tools from the configured external MCP server(s) and build the info agent.

    Tool discovery requires an MCP handshake, so the agent must be built
    with `await build_info_agent()` instead of at import time.

    Args:
        server_name: Restrict tool discovery to a single server from
            `MCP_SERVERS` (e.g. "alphavantage"). Defaults to all configured
            servers.
    """
    tools = await mcp_client.get_tools(server_name=server_name)
    return create_agent(model=MODEL, tools=tools, system_prompt=PROMPT_SYS_AGENT_INFO)


if __name__ == "__main__":

    async def _main() -> None:
        agent = await build_info_agent()
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "What is the latest quote for IBM?"}]}
        )
        print(result["messages"][-1].content)

    asyncio.run(_main())
