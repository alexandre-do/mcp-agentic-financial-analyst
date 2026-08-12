from __future__ import annotations


def validate_question(question: str) -> bool:
    """Basic validation for user-submitted questions."""
    if not question or not question.strip():
        return False
    if len(question.strip()) < 3:
        return False
    return True
