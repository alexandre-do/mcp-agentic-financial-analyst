from __future__ import annotations


class MetadataService:
    """Placeholder service for schema and metadata inspection."""

    def get_table_metadata(self, table_name: str) -> dict[str, object]:
        return {"table_name": table_name, "columns": []}
