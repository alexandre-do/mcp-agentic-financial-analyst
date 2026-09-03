from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.backend.schemas import QueryRequest, QueryResponse

app = FastAPI(title="Agentic Data Analyst API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def run_query(payload: QueryRequest) -> QueryResponse:
    """Placeholder endpoint for the agentic data analysis workflow."""
    return QueryResponse(
        question=payload.question,
        answer="This is a template response. Connect your orchestrator and tools here.",
        sql_query=None,
        chart=None,
    )
