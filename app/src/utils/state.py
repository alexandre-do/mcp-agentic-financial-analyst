from typing import NotRequired
from lanchain.agents.middleware import AgentState


class CustomState(AgentState):
    skills_loaded: NotRequired[list[str]]  # Track which skills have been loaded
