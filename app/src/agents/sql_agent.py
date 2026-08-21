import os
from dotenv import load_dotenv
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage

from ..prompt_template import PROMPT_SYS_AGENT_SQL, PROMPT_SYS_AGENT_SQL_ONDEMANDE
from ..tools.sql_tools import (
    load_skill,
    write_sql_query,
    SKILLS,
    sql_db_list_tables,
    sql_db_schema,
    sql_db_query,
    create_sql_db_checker,
)
from ..utils.state import CustomState

load_dotenv()


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


MODEL = init_chat_model(model=os.environ.get("MODEL_ID"))

agent_sql_on_demande = create_agent(
    MODEL,
    system_prompt=PROMPT_SYS_AGENT_SQL_ONDEMANDE,
    middleware=[SkillMiddleware()],
    checkpointer=InMemorySaver(),
)

sql_db_query_check = create_sql_db_checker(MODEL)
tools = [sql_db_list_tables, sql_db_schema, sql_db_query, sql_db_query_check]
prompt_system = PROMPT_SYS_AGENT_SQL.format(dialect="sqlite", top_k=5)
agent_sql = create_agent(model=MODEL, tools=tools, system_prompt=prompt_system)
