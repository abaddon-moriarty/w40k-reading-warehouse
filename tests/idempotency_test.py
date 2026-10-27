import sqlite3

import pytest

from extract.copy_database import run

PIPELINES = [
    pytest.param(run, "fake_koreader_db", "raw", id="koreader_stats"),
    # pytest.param(vocabulary.run, "fake_vocab_db", "raw_vocabulary", id="vocabulary"),
]


@pytest.mark.parametrize("pipeline, source_fixture, schema", PIPELINES)
def test_pipeline_is_idempotent(pipeline, source_fixture, schema, request, tmp_path, snapshot):
    source = request.getfixturevalue(source_fixture)
    warehouse = tmp_path / "warehouse.duckdb"

    pipeline(source, tmp_path, warehouse)
    first = snapshot(warehouse, schema)

    pipeline(source, tmp_path, warehouse)

    assert snapshot(warehouse, schema) == first


def test_load_keeps_every_row(fake_koreader_db, tmp_path, snapshot):
    warehouse = tmp_path / "warehouse.duckdb"

    run(fake_koreader_db, tmp_path, warehouse)
    state = snapshot(warehouse)

    assert len(state["book"]) == 2
    assert len(state["page_stat_data"]) == 3


def test_rerun_reflects_source_exactly(fake_koreader_db, tmp_path, snapshot):
    """A table that disappears from the source should disappear from raw too."""
    warehouse = tmp_path / "warehouse.duckdb"
    run(fake_koreader_db, tmp_path, warehouse)

    conn = sqlite3.connect(fake_koreader_db)
    conn.execute("DROP TABLE page_stat_data")
    conn.commit()
    conn.close()

    run(fake_koreader_db, tmp_path, warehouse)

    assert "page_stat_data" not in snapshot(warehouse)
