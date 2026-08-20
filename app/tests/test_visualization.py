from app.mcp.tools.visualization_tools import build_chart_spec


def test_build_chart_spec_returns_type_and_data():
    chart = build_chart_spec("bar", [{"label": "A", "value": 10}])
    assert chart["type"] == "bar"
    assert len(chart["data"]) == 1
