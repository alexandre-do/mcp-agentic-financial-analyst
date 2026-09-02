from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

if __package__ in (None, ""):
    # Allow running this file directly (e.g. `python dataviz_agent.py` or an
    # IDE "Run" button) in addition to `python -m app.src.agents.dataviz_agent`.
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    __package__ = "app.src.agents"

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from ..prompt_template import PROMPT_SYS_AGENT_DATAVIZ
from ..tools.dataviz_tools import create_chart

load_dotenv()

MODEL = init_chat_model(model=os.environ.get("MODEL_ID"))


async def build_dataviz_agent():
    """Build the data visualization agent that turns tabular data into charts."""
    tools = [create_chart]
    return create_agent(model=MODEL, tools=tools, system_prompt=PROMPT_SYS_AGENT_DATAVIZ)


if __name__ == "__main__":

    async def _main() -> None:
        agent = await build_dataviz_agent()
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Plot quarterly revenue as a bar chart: Q1=120, Q2=150, Q3=135, Q4=180."
                        ),
                    }
                ]
            }
        )
        print(result["messages"][-1].content)

    asyncio.run(_main())
