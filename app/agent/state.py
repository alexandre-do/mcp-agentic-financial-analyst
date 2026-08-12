from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    question: str = ""
    context: str | None = None
    sql_query: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    chart_spec: dict[str, Any] | None = None
    answer: str = ""
    is_valid: bool = True
