from app.src.mcp.tools.sql_tools import list_tables, run_sql_query


def test_list_tables_returns_list():
    result = list_tables()
    assert isinstance(result, list)


def test_run_sql_query_returns_structured_result():
    result = run_sql_query("SELECT 1")
    assert "query" in result
    assert "rows" in result
