import sqlite3

from extract.copy_database import copy_data_db, load_raw


def run_pipeline(source, tmp_path):
    raw_copy = tmp_path / "koreader_db.sqlite3"
    warehouse = tmp_path / "warehouse.duckdb"
    copy_data_db(source, raw_copy)
    load_raw(raw_copy, warehouse)
    return warehouse


def test_running_twice_gives_the_same_state(fake_koreader_db, tmp_path, snapshot):
    warehouse = run_pipeline(fake_koreader_db, tmp_path)
    first = snapshot(warehouse)

    run_pipeline(fake_koreader_db, tmp_path)
    second = snapshot(warehouse)

    assert second == first
    assert len(first["book"]) == 2
    assert len(first["page_stat_data"]) == 3


def test_rerun_reflects_source_exactly(fake_koreader_db, tmp_path, snapshot):
    """A table that disappears from the source should disappear from raw too."""
    warehouse = run_pipeline(fake_koreader_db, tmp_path)

    conn = sqlite3.connect(fake_koreader_db)
    conn.execute("DROP TABLE page_stat_data")
    conn.commit()
    conn.close()

    run_pipeline(fake_koreader_db, tmp_path)

    assert "page_stat_data" not in snapshot(warehouse)
