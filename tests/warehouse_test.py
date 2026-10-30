"""Tests for extract/common/warehouse.py."""

import json
import logging

import duckdb
import pytest

from extract import config
from extract.common.warehouse import (
    DUCKDB_CONFIG,
    load_jsonl,
    log_row_count,
    open_warehouse,
    transaction,
)


@pytest.fixture
def conn(tmp_path):
    """Fresh DuckDB connection on a temp file, closed after the test."""
    c = open_warehouse(tmp_path / "test.duckdb")
    yield c
    c.close()


class TestOpenWarehouse:
    def test_returns_usable_connection(self, conn):
        assert conn.execute("SELECT 1").fetchone() == (1,)

    def test_creates_file(self, tmp_path):
        path = tmp_path / "fresh.duckdb"
        c = open_warehouse(path)
        try:
            c.execute("CREATE TABLE t (x INTEGER)")
        finally:
            c.close()
        assert path.exists()

    def test_uses_provided_path(self, tmp_path):
        a = tmp_path / "a.duckdb"
        b = tmp_path / "b.duckdb"
        open_warehouse(a).close()
        open_warehouse(b).close()
        assert a.exists() and b.exists()

    def test_passes_config_to_duckdb(self, tmp_path, monkeypatch):
        from extract.common import warehouse as mod

        captured = {}
        original = mod.duckdb.connect

        def spy(path, config=None):
            captured["path"] = path
            captured["config"] = config
            return original(path, config=config)

        monkeypatch.setattr(mod.duckdb, "connect", spy)

        c = open_warehouse(tmp_path / "test.duckdb")
        c.close()

        assert captured["path"] == str(tmp_path / "test.duckdb")
        assert captured["config"] == DUCKDB_CONFIG

    def test_duckdb_config_contents(self):
        assert "storage_compatibility_version" in DUCKDB_CONFIG
        assert DUCKDB_CONFIG["storage_compatibility_version"] == "v1.5.0"


class TestTransaction:
    def test_commits_on_success(self, conn):
        conn.execute("CREATE TABLE t (x INTEGER)")
        with transaction(conn):
            conn.execute("INSERT INTO t VALUES (1)")
            conn.execute("INSERT INTO t VALUES (2)")
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone() == (2,)

    def test_rolls_back_on_exception(self, conn):
        conn.execute("CREATE TABLE t (x INTEGER)")
        with pytest.raises(RuntimeError, match="boom"):
            with transaction(conn):
                conn.execute("INSERT INTO t VALUES (1)")
                raise RuntimeError("boom")
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone() == (0,)

    def test_preserves_original_exception(self, conn):
        class CustomError(Exception):
            pass

        with pytest.raises(CustomError, match="specific message"):
            with transaction(conn):
                raise CustomError("specific message")

    def test_connection_usable_after_rollback(self, conn):
        conn.execute("CREATE TABLE t (x INTEGER)")
        with pytest.raises(RuntimeError):
            with transaction(conn):
                conn.execute("INSERT INTO t VALUES (1)")
                raise RuntimeError()
        conn.execute("INSERT INTO t VALUES (2)")
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone() == (1,)

    def test_repeated_use(self, conn):
        conn.execute("CREATE TABLE t (x INTEGER)")
        for i in range(3):
            with transaction(conn):
                conn.execute("INSERT INTO t VALUES (?)", [i])
        assert conn.execute("SELECT COUNT(*) FROM t").fetchone() == (3,)


class TestLogRowCount:
    def test_empty_table_returns_zero(self, conn, caplog):
        conn.execute("CREATE SCHEMA s")
        conn.execute("CREATE TABLE s.t (x INTEGER)")
        caplog.set_level(logging.INFO)
        assert log_row_count(conn, "s", "t") == 0

    def test_returns_row_count(self, conn, caplog):
        conn.execute("CREATE SCHEMA s")
        conn.execute("CREATE TABLE s.t (x INTEGER)")
        conn.execute("INSERT INTO s.t VALUES (1), (2), (3)")
        caplog.set_level(logging.INFO)
        assert log_row_count(conn, "s", "t") == 3

    def test_returns_integer(self, conn, caplog):
        conn.execute("CREATE SCHEMA s")
        conn.execute("CREATE TABLE s.t (x INTEGER)")
        caplog.set_level(logging.INFO)
        result = log_row_count(conn, "s", "t")
        assert isinstance(result, int)

    def test_logs_message_with_schema_and_table(self, conn, caplog):
        conn.execute("CREATE SCHEMA s")
        conn.execute("CREATE TABLE s.t (x INTEGER)")
        caplog.set_level(logging.INFO)
        log_row_count(conn, "s", "t")
        messages = [r.message for r in caplog.records]
        assert "Loaded s.t (0 rows)" in messages

    def test_logs_correct_row_count(self, conn, caplog):
        conn.execute("CREATE SCHEMA s")
        conn.execute("CREATE TABLE s.t (x INTEGER)")
        conn.execute("INSERT INTO s.t VALUES (1), (2), (3)")
        caplog.set_level(logging.INFO)
        log_row_count(conn, "s", "t")
        messages = [r.message for r in caplog.records]
        assert "Loaded s.t (3 rows)" in messages

    def test_log_level_is_info(self, conn, caplog):
        conn.execute("CREATE SCHEMA s")
        conn.execute("CREATE TABLE s.t (x INTEGER)")
        caplog.set_level(logging.INFO)
        log_row_count(conn, "s", "t")
        info_records = [r for r in caplog.records if r.levelno == logging.INFO]
        assert any("Loaded s.t" in r.message for r in info_records)

    def test_quotes_identifiers_with_dots(self, conn, caplog):
        """Schema and table names containing dots must not break the query."""
        conn.execute('CREATE SCHEMA "weird.schema"')
        conn.execute('CREATE TABLE "weird.schema"."weird.table" AS SELECT 1 AS x')
        caplog.set_level(logging.INFO)
        assert log_row_count(conn, "weird.schema", "weird.table") == 1

    def test_missing_table_raises(self, conn):
        with pytest.raises(duckdb.CatalogException):
            log_row_count(conn, "s", "t")


class TestLoadJsonl:
    @staticmethod
    def _jsonl(path, *rows):
        path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        return path

    def test_creates_schema_and_table(self, tmp_path, warehouse_path, snapshot):
        path = self._jsonl(tmp_path / "a.jsonl", {"x": 1}, {"x": 2})

        load_jsonl(path, "s", "t", warehouse_path)

        assert snapshot(warehouse_path, "s") == {"t": [(1,), (2,)]}

    def test_reload_replaces_the_table(self, tmp_path, warehouse_path, snapshot):
        load_jsonl(self._jsonl(tmp_path / "a.jsonl", {"x": 1}), "s", "t", warehouse_path)
        load_jsonl(self._jsonl(tmp_path / "b.jsonl", {"y": "new"}), "s", "t", warehouse_path)

        assert snapshot(warehouse_path, "s") == {"t": [("new",)]}

    def test_does_not_touch_other_tables(self, tmp_path, warehouse_path, snapshot):
        load_jsonl(self._jsonl(tmp_path / "a.jsonl", {"x": 1}), "s", "keep", warehouse_path)
        load_jsonl(self._jsonl(tmp_path / "b.jsonl", {"x": 2}), "s", "other", warehouse_path)

        assert snapshot(warehouse_path, "s") == {"keep": [(1,)], "other": [(2,)]}

    def test_logs_the_requested_table(self, tmp_path, warehouse_path, caplog):
        """Regression: the log used to name raw.epub_metadata for every load."""
        caplog.set_level(logging.INFO)

        load_jsonl(self._jsonl(tmp_path / "a.jsonl", {"x": 1}), "s", "t", warehouse_path)

        assert "Loaded s.t (1 rows)" in [r.message for r in caplog.records]

    def test_defaults_to_the_configured_warehouse(self, tmp_path, snapshot):
        load_jsonl(self._jsonl(tmp_path / "a.jsonl", {"x": 1}), "s", "t")

        assert snapshot(config.WAREHOUSE_PATH, "s") == {"t": [(1,)]}

    def test_glob_combines_every_matching_file(self, tmp_path, warehouse_path, snapshot):
        self._jsonl(tmp_path / "a.jsonl", {"x": 1})
        self._jsonl(tmp_path / "b.jsonl", {"x": 2})

        load_jsonl(tmp_path / "*.jsonl", "s", "t", warehouse_path)

        assert snapshot(warehouse_path, "s") == {"t": [(1,), (2,)]}

    def test_quotes_identifiers_with_dots(self, tmp_path, warehouse_path, snapshot):
        path = self._jsonl(tmp_path / "a.jsonl", {"x": 1})

        load_jsonl(path, "weird.schema", "weird.table", warehouse_path)

        assert snapshot(warehouse_path, "weird.schema") == {"weird.table": [(1,)]}

    def test_failed_load_keeps_the_previous_table(self, tmp_path, warehouse_path, snapshot):
        load_jsonl(self._jsonl(tmp_path / "a.jsonl", {"x": 1}), "s", "t", warehouse_path)

        with pytest.raises(duckdb.IOException):
            load_jsonl(tmp_path / "missing.jsonl", "s", "t", warehouse_path)

        assert snapshot(warehouse_path, "s") == {"t": [(1,)]}

    @pytest.mark.xfail(strict=True, reason="an empty file currently replaces a good table")
    def test_empty_file_keeps_the_previous_table(self, tmp_path, warehouse_path, snapshot):
        load_jsonl(self._jsonl(tmp_path / "a.jsonl", {"x": 1}), "s", "t", warehouse_path)

        load_jsonl(self._jsonl(tmp_path / "empty.jsonl"), "s", "t", warehouse_path)

        assert snapshot(warehouse_path, "s") == {"t": [(1,)]}
