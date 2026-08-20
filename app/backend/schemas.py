from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural language question to answer")
    context: Optional[str] = Field(default=None, description="Optional user context")


class QueryResponse(BaseModel):
    question: str
    answer: str
    sql_query: Optional[str] = None
    chart: Optional[str] = None
