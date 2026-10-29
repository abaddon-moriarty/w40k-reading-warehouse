import sqlite3

import duckdb
import pytest


@pytest.fixture
def fake_koreader_db(tmp_path):
    """A tiny SQLite file shaped like KOReader's statistics database."""
    path = tmp_path / "statistics.sqlite3"
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE book (id INTEGER PRIMARY KEY, title TEXT);
        INSERT INTO book (title) VALUES ('Fake Book One'), ('Fake Book Two');
        CREATE TABLE page_stat_data (id_book INTEGER, page INTEGER, duration INTEGER);
        INSERT INTO page_stat_data VALUES (1, 1, 30), (1, 2, 45), (2, 1, 12);
        CREATE VIEW page_stat AS SELECT * FROM page_stat_data;
        """
    )
    conn.commit()
    conn.close()
    return path


@pytest.fixture
def snapshot():
    """Capture every table of a DuckDB schema with its rows.

    Rows are ordered by DuckDB (ORDER BY ALL) so row order never makes two
    identical states differ; this also handles NULLs and nested types,
    which Python's sorted() cannot compare.
    """

    def _snapshot(warehouse_path, schema):
        conn = duckdb.connect(str(warehouse_path), read_only=True)
        try:
            tables = [
                name
                for (name,) in conn.execute(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = ? ORDER BY table_name",
                    [schema],
                ).fetchall()
            ]
            return {
                t: conn.execute(f'SELECT * FROM "{schema}"."{t}" ORDER BY ALL').fetchall()
                for t in tables
            }
        finally:
            conn.close()

    return _snapshot


@pytest.fixture
def warehouse_path(tmp_path):
    return tmp_path / "warehouse.duckdb"


@pytest.fixture(autouse=True)
def _isolate_warehouse(monkeypatch, tmp_path):
    """Force WAREHOUSE_PATH to tmp so no test ever touches the real warehouse."""
    from extract import config

    monkeypatch.setattr(config, "WAREHOUSE_PATH", tmp_path / "isolated.duckdb")
