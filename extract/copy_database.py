import logging
import sqlite3
import sys

from extract.common.warehouse import log_row_count, open_warehouse, transaction
from extract.config import RAW_DIR, WAREHOUSE_PATH, koreader_settings_dir


def copy_data_db(source_path, raw_output_path):
    src = sqlite3.connect(f"file:{source_path}?mode=ro", uri=True)

    raw_output_path.parent.mkdir(parents=True, exist_ok=True)
    dst = sqlite3.connect(raw_output_path)

    src.backup(dst)

    dst.execute("PRAGMA journal_mode=DELETE")

    src.close()
    dst.close()


def load_raw(sqlite_path, warehouse_path, schema="raw_koreader"):
    with open_warehouse(warehouse_path) as conn:
        conn.execute("INSTALL sqlite; LOAD sqlite;")
        conn.execute(f"ATTACH '{sqlite_path}' AS statistics (TYPE sqlite, READ_ONLY)")
        tables = conn.execute(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_catalog = 'statistics'
            AND table_type = 'BASE TABLE';
            """
        ).fetchall()
        with transaction(conn):
            conn.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE")
            conn.execute(f"CREATE SCHEMA {schema}")
            for (table,) in tables:
                conn.execute(
                    f'CREATE TABLE {schema}."{table}" AS SELECT * FROM statistics."{table}"'
                )
                log_row_count(conn, schema, table)


def run(source, raw_dir, warehouse_path):
    raw_copy = raw_dir / "koreader_db.sqlite3"
    logging.debug(raw_copy)
    copy_data_db(source, raw_copy)
    load_raw(raw_copy, warehouse_path, schema="raw_koreader")


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        source_path = koreader_settings_dir() / "statistics.sqlite3"
        source_path.resolve(strict=True)
        logging.info(source_path)
        run(source_path, RAW_DIR, WAREHOUSE_PATH)

    except FileNotFoundError:
        logging.exception(
            """Path does not exist.
            Make sure the eReader is plugged in and,
            the KOREADER_SETTINGS_DIR in your .env is correct."""
        )
        return 1
    except OSError:
        logging.exception("An OS error occurred (e.g., permission denied).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
