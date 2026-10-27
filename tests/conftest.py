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
    """Return a function that captures every table of a DuckDB schema with its rows.

    Rows are sorted so that row order never makes two identical states look different.
    Reuse it in any idempotence test: run, snapshot, run again, snapshot, compare.
    """

    def _snapshot(warehouse_path, schema="raw"):
        conn = duckdb.connect(str(warehouse_path), read_only=True)
        tables = [
            name
            for (name,) in conn.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = ? ORDER BY table_name",
                [schema],
            ).fetchall()
        ]
        state = {
            t: sorted(conn.execute(f'SELECT * FROM {schema}."{t}"').fetchall()) for t in tables
        }
        conn.close()
        return state

    return _snapshot
