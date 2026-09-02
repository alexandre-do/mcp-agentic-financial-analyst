from typing import Literal

import plotly.express as px
from langchain_core.tools import tool

ChartType = Literal["bar", "line", "scatter", "pie"]


@tool
def create_chart(
    chart_type: ChartType,
    x: list[str],
    y: list[float],
    title: str = "",
    x_label: str = "",
    y_label: str = "",
) -> str:
    """Build a chart from data and return it as a Plotly figure JSON spec.

    Args:
        chart_type: Kind of chart to build - "bar", "line", "scatter", or "pie".
        x: Category/label values for the x-axis (or pie slice labels).
        y: Numeric values for the y-axis (or pie slice sizes). Must be the
            same length as x.
        title: Optional chart title.
        x_label: Optional label for the x-axis (ignored for "pie").
        y_label: Optional label for the y-axis (ignored for "pie").
    """
    if len(x) != len(y):
        return "Error: x and y must have the same length."

    data = {"x": x, "y": y}

    if chart_type == "bar":
        fig = px.bar(data, x="x", y="y", title=title)
    elif chart_type == "line":
        fig = px.line(data, x="x", y="y", title=title)
    elif chart_type == "scatter":
        fig = px.scatter(data, x="x", y="y", title=title)
    elif chart_type == "pie":
        fig = px.pie(data, names="x", values="y", title=title)
    else:
        return f"Error: unsupported chart_type '{chart_type}'."

    if chart_type != "pie":
        fig.update_layout(xaxis_title=x_label or None, yaxis_title=y_label or None)

    return fig.to_json()
