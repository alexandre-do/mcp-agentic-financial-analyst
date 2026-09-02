from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    __package__ = "app.src.agents"

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver

from ..prompt_template import PROMPT_SYS_AGENT_SQL, PROMPT_SYS_AGENT_SQL_ONDEMANDE
from ..tools.sql_tools import (
    SKILLS,
    create_sql_db_checker,
    load_skill,
    sql_db_list_tables,
    sql_db_query,
    sql_db_schema,
    write_sql_query,
)
from ..utils.state import CustomState

load_dotenv()

MODEL = init_chat_model(model=os.environ.get("MODEL_ID"))


class SkillMiddleware(AgentMiddleware[CustomState]):
    """Middleware that injects skill descriptions into the system prompt."""

    # Register the load_skill tool as a class variable
    state_schema = CustomState
    tools = [load_skill, write_sql_query]

    def __init__(self):
        """Initialize and generate the skills prompt from SKILLS."""
        # Build skills prompt from the SKILLS list
        skills_list = []
        for skill in SKILLS:
            skills_list.append(f"- **{skill['name']}**: {skill['description']}")
        self.skills_prompt = "\n".join(skills_list)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Sync: Inject skill descriptions into system prompt."""
        # Build the skills addendum
        skills_addendum = (
            f"\n\n## Available Skills\n\n{self.skills_prompt}\n\n"
            "Use the load_skill tool when you need detailed information "
            "about handling a specific type of request."
        )

        # Append to system message content blocks
        new_content = list(request.system_message.content_blocks) + [
            {"type": "text", "text": skills_addendum}
        ]
        new_system_message = SystemMessage(content=new_content)
        modified_request = request.override(system_message=new_system_message)
        return handler(modified_request)


async def build_sql_agent(dialect: str = "sqlite", top_k: int = 5):
    """Build the SQL agent that lists tables, inspects schema, and runs queries.

    Args:
        dialect: SQL dialect to mention in the system prompt.
        top_k: Default row limit the agent should apply to result sets.
    """
    sql_db_query_check = create_sql_db_checker(MODEL)
    tools = [sql_db_list_tables, sql_db_schema, sql_db_query, sql_db_query_check]
    prompt_system = PROMPT_SYS_AGENT_SQL.format(dialect=dialect, top_k=top_k)
    return create_agent(model=MODEL, tools=tools, system_prompt=prompt_system)


async def build_sql_agent_on_demand():
    """Build the skill-based agent that prepares (but does not execute) SQL queries."""
    return create_agent(
        MODEL,
        system_prompt=PROMPT_SYS_AGENT_SQL_ONDEMANDE,
        middleware=[SkillMiddleware()],
        checkpointer=InMemorySaver(),
    )


if __name__ == "__main__":

    async def _main() -> None:
        agent = await build_sql_agent()
        result = await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": "What tables are available in the database?"}
                ]
            }
        )
        print(result["messages"][-1].content)

    asyncio.run(_main())
