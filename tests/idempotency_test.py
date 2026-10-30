import sqlite3

import duckdb
import pytest

from extract import wiki_export
from extract.copy_database import run

PIPELINES = [
    pytest.param(run, "fake_koreader_db", "raw_koreader", id="koreader_stats"),
    pytest.param(wiki_export.run, "fake_wiki_xml", "raw", id="wiki_export"),
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
    state = snapshot(warehouse, "raw_koreader")

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

    assert "page_stat_data" not in snapshot(warehouse, "raw_koreader")


def test_load_does_not_touch_other_sources(fake_koreader_db, tmp_path, snapshot):
    warehouse = tmp_path / "warehouse.duckdb"
    conn = duckdb.connect(str(warehouse), config={"storage_compatibility_version": "v1.5.0"})

    conn.execute("CREATE SCHEMA raw;")
    conn.execute("CREATE TABLE raw.epub_metadata AS SELECT 1 AS id, 'Fake EPUB' AS title")
    conn.close()
    run(fake_koreader_db, tmp_path, warehouse)
    assert snapshot(warehouse, "raw")["epub_metadata"] == [(1, "Fake EPUB")]


def test_different_base_name_accepted(fake_koreader_db, tmp_path, snapshot):
    warehouse = tmp_path / "other.duckdb"
    run(fake_koreader_db, tmp_path, warehouse)
    assert "book" in snapshot(warehouse, "raw_koreader")
