from __future__ import annotations

from app.agent.guardrails import validate_question
from app.agent.state import AgentState


class AgentOrchestrator:
    """Minimal orchestrator placeholder for a future agent workflow."""

    def process(self, question: str, context: str | None = None) -> AgentState:
        state = AgentState(question=question, context=context)
        state.is_valid = validate_question(question)

        if not state.is_valid:
            state.answer = "The question is empty or invalid. Please provide a clearer request."
            return state

        state.answer = (
            "The workflow is scaffolded. Connect SQL tools, metadata tooling, and the model "
            "orchestrator to answer this question in production."
        )
        return state
