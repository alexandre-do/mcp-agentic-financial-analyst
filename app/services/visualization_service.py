from __future__ import annotations


class VisualizationService:
    """Placeholder visualization service for result rendering."""

    def create_chart(self, chart_type: str, data: list[dict[str, object]]) -> dict[str, object]:
        return {"type": chart_type, "data": data}
