# extract/common/warehouse.py
import logging
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import duckdb

from extract import config

DUCKDB_CONFIG = {"storage_compatibility_version": "v1.5.0"}


def open_warehouse(path: Path | None = None) -> duckdb.DuckDBPyConnection:
    target = path if path is not None else config.WAREHOUSE_PATH
    return duckdb.connect(str(target), config=DUCKDB_CONFIG)


@contextmanager
def transaction(conn: duckdb.DuckDBPyConnection) -> Generator[None]:
    conn.execute("BEGIN TRANSACTION")
    try:
        yield
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def log_row_count(conn: duckdb.DuckDBPyConnection, schema: str, table: str) -> int:
    (count,) = conn.execute(f'SELECT COUNT(*) FROM "{schema}"."{table}"').fetchone()
    logging.info("Loaded %s.%s (%s rows)", schema, table, count)
    return count


def load_jsonl(output_path: Path, schema: str, table: str, warehouse_path: Path | None = None):
    with open_warehouse(warehouse_path) as conn, transaction(conn):
        conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
        conn.execute(
            f'CREATE OR REPLACE TABLE "{schema}"."{table}" AS SELECT * FROM read_json(?)',
            [str(output_path)],
        )
        log_row_count(conn, schema, table)
