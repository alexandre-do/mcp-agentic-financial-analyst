from __future__ import annotations


def list_tables() -> list[str]:
    """Placeholder list of tables from the configured database."""
    return []


def run_sql_query(query: str) -> dict[str, str | list[dict[str, str]]]:
    """Placeholder method for executing a SQL query safely."""
    return {"query": query, "rows": []}
