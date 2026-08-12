from app.agent.orchestrator import AgentOrchestrator


def test_agent_accepts_valid_question():
    agent = AgentOrchestrator()
    state = agent.process("What are the top sales by region?")
    assert state.is_valid is True
    assert "workflow is scaffolded" in state.answer.lower()


def test_agent_rejects_empty_question():
    agent = AgentOrchestrator()
    state = agent.process("   ")
    assert state.is_valid is False
    assert "invalid" in state.answer.lower()
