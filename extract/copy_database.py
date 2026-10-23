import logging
import sqlite3

import duckdb

from extract.config import RAW_DIR, WAREHOUSE_PATH, koreader_settings_dir


def copy_data_db(raw_copy_path, raw_output_path):
    src = sqlite3.connect(f"file:{raw_copy_path}?mode=ro", uri=True)

    dst = sqlite3.connect(raw_output_path)

    src.backup(dst)

    dst.execute("PRAGMA journal_mode=DELETE")

    src.close()
    dst.close()


def load_raw(sqlite_path, warehouse_path):
    conn = duckdb.connect(str(warehouse_path))

    conn.execute("INSTALL AND LOAD sqlite;")
    conn.execute(f"ATTACH '{sqlite_path}' AS statistics (TYPE sqlite, READ_ONLY);")

    conn.execute("CREATE SCHEMA IF NOT EXISTS warehouse.raw")
    tables = conn.execute(
        """
        SELECT table_name FROM information_schema.tables
        WHERE table_catalog = 'statistics'
        AND table_type = 'BASE TABLE';
        """
    ).fetchall()

    for (table,) in tables:
        conn.execute(
            f'CREATE OR REPLACE TABLE warehouse.raw."{table}" AS SELECT * FROM statistics."{table}"'
        )
        row_count = conn.execute(f'SELECT COUNT(*) FROM warehouse.raw."{table}"').fetchone()[0]

        logging.info("Loaded raw.%s (%s rows)", table, row_count)

    conn.close()


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        raw_copy_path = koreader_settings_dir() / "statistics.sqlite3"
        raw_copy_path.resolve(strict=True)

        sqlite_dest_path = RAW_DIR / "koreader_db.sqlite3"

        logging.info(raw_copy_path)
        copy_data_db(raw_copy_path, sqlite_dest_path)

        load_raw(sqlite_dest_path, WAREHOUSE_PATH)

    except FileNotFoundError:
        logging.exception(
            """Path does not exist.
            Make sure the eReader is plugged in and,
            the KOREADER_SETTINGS_DIR in your .env is correct."""
        )
    except OSError:
        logging.exception("An OS error occurred (e.g., permission denied).")


if __name__ == "__main__":
    main()
