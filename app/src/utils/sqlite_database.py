import sqlite3
from pathlib import Path
from typing import Any, Iterable


class SqliteDatabase:
    def __init__(
        self,
        database_path: str | Path,
        timeout: float = 5.0,
        check_same_thread: bool = False,
    ) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(
            self.database_path,
            timeout=timeout,
            check_same_thread=check_same_thread,
        )
        self.connection.row_factory = sqlite3.Row

    def list_tables(self) -> list[str]:
        """Return the names of all user-created tables in the database."""
        cursor = self.connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )
        return [row["name"] for row in cursor.fetchall()]

    def list_tabs(self) -> list[str]:
        """Backward-compatible alias for :meth:`list_tables`."""
        return self.list_tables()

    def get_schema_data(self, table_name: str | None = None) -> dict[str, list[dict[str, Any]]]:
        """Return SQLite column metadata, optionally for one table.

        The returned mapping contains each table name and its ``PRAGMA
        table_info`` rows, including column name, type, nullability and
        primary-key information.
        """
        tables = [table_name] if table_name is not None else self.list_tables()
        schema: dict[str, list[dict[str, Any]]] = {}

        for name in tables:
            quoted_name = name.replace("'", "''")
            cursor = self.connection.execute(f"PRAGMA table_info('{quoted_name}')")
            schema[name] = [dict(row) for row in cursor.fetchall()]

        return schema

    def run_query(
        self,
        query: str,
        parameters: Iterable[Any] = (),
    ) -> list[dict[str, Any]]:
        """Execute a SQL query and return its result rows as dictionaries.

        ``parameters`` should be used for user-provided values instead of
        interpolating them into the SQL string. Non-SELECT statements are
        committed automatically and return an empty list.
        """
        cursor = self.connection.execute(query, tuple(parameters))
        if cursor.description is None:
            self.connection.commit()
            return []

        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()

    def __enter__(self) -> "SqliteDatabase":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if exc_type is not None:
            self.connection.rollback()
        self.close()
