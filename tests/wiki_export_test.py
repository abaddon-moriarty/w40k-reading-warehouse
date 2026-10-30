"""Tests for extract/wiki_export.py."""

import json
import logging
import shutil
from xml.sax.saxutils import escape

import duckdb
import pytest

from extract import config, wiki_export
from extract.common.warehouse import open_warehouse

WIKI_TABLES = ("wiki_page_categories", "wiki_pages")

# Values present in tests/fixtures/wiki_export.xml that must never be loaded.
FORBIDDEN_VALUES = [
    "Invented article body",
    "Invented Scribe",
    "Invented Archivist",
    "Invented edit comment",
]

# --- helpers ---------------------------------------------------------------


def _page(title="Page", ns="0", page_id="1", text="Body"):
    text_el = "" if text is None else f"<text>{escape(text)}</text>"
    return f"""\
  <page>
    <title>{escape(title)}</title>
    <ns>{ns}</ns>
    <id>{page_id}</id>
    <revision>{text_el}</revision>
  </page>
"""


def _write_export(path, *pages, version="0.11"):
    path.write_text(
        f'<mediawiki xmlns="http://www.mediawiki.org/xml/export-{version}/">\n'
        + "".join(pages)
        + "</mediawiki>\n",
        encoding="utf-8",
    )
    return path


def _categories_of(tmp_path, text):
    path = _write_export(tmp_path / "export.xml", _page(text=text))
    _, categories = wiki_export.extraction_from_xml(path)
    return [row["category"] for row in categories]


# --- extraction_from_xml: pages --------------------------------------------


class TestPages:
    def test_reads_the_hand_made_export(self, fake_wiki_xml):
        pages, _ = wiki_export.extraction_from_xml(fake_wiki_xml)

        assert pages == [
            {
                "title": "Invented Inquisitor",
                "namespace": "0",
                "page_id": "101",
                "export_file": "wiki_export.xml",
            },
            {
                "title": "Invented World",
                "namespace": "0",
                "page_id": "102",
                "export_file": "wiki_export.xml",
            },
        ]

    def test_namespace_keeps_the_page_value(self, tmp_path):
        path = _write_export(tmp_path / "export.xml", _page(ns="14"))

        (page,), _ = wiki_export.extraction_from_xml(path)

        assert page["namespace"] == "14"

    def test_export_without_pages_gives_no_rows(self, tmp_path):
        path = _write_export(tmp_path / "export.xml")

        assert wiki_export.extraction_from_xml(path) == ([], [])

    def test_namespace_is_read_from_the_file(self, tmp_path):
        """Another export schema version must not need a code change."""
        path = _write_export(tmp_path / "export.xml", _page(title="Old"), version="0.10")

        (page,), _ = wiki_export.extraction_from_xml(path)

        assert page["title"] == "Old"

    def test_rows_can_be_serialized_to_json(self, fake_wiki_xml):
        pages, categories = wiki_export.extraction_from_xml(fake_wiki_xml)

        assert json.loads(json.dumps(pages)) == pages
        assert json.loads(json.dumps(categories)) == categories


# --- extraction_from_xml: categories ---------------------------------------


class TestCategories:
    def test_reads_the_hand_made_export(self, fake_wiki_xml):
        _, categories = wiki_export.extraction_from_xml(fake_wiki_xml)

        assert categories == [
            {
                "title": "Invented Inquisitor",
                "category": "Invented Novels",
                "page_id": "101",
                "export_file": "wiki_export.xml",
            },
            {
                "title": "Invented Inquisitor",
                "category": "Invented Characters",
                "page_id": "101",
                "export_file": "wiki_export.xml",
            },
            {
                "title": "Invented World",
                "category": "Invented Novels",
                "page_id": "102",
                "export_file": "wiki_export.xml",
            },
        ]

    @pytest.mark.parametrize(
        "text, expected",
        [
            pytest.param("[[Category:Solo]]", ["Solo"], id="single"),
            pytest.param("[[Category:A]] text [[Category:B]]", ["A", "B"], id="several"),
            pytest.param("[[Category:A|sort key]]", ["A"], id="sort_key_dropped"),
            pytest.param("[[Category: Spaced ]]", ["Spaced"], id="spaces_stripped"),
            pytest.param(
                "[[Category:Eisenhorn (Novel Series)]]",
                ["Eisenhorn (Novel Series)"],
                id="parentheses_kept",
            ),
            pytest.param("[[Category:A]]\n[[Category:B]]", ["A", "B"], id="several_lines"),
            pytest.param("[[Regular link]] [[File:a.png]]", [], id="other_links_ignored"),
            pytest.param("No links at all", [], id="no_links"),
            pytest.param("", [], id="empty_text"),
            pytest.param(None, [], id="no_text_element"),
        ],
    )
    def test_reads_categories_from_wikitext(self, tmp_path, text, expected):
        assert _categories_of(tmp_path, text) == expected

    @pytest.mark.xfail(strict=True, reason="known limitation of the category regex")
    @pytest.mark.parametrize(
        "text, expected",
        [
            pytest.param("[[category:Lower]]", ["Lower"], id="lowercase_prefix"),
            pytest.param("[[ Category:Space]]", ["Space"], id="leading_space"),
            pytest.param("[[Category:Under_score]]", ["Under score"], id="underscore"),
            pytest.param("<!-- [[Category:Old]] -->", [], id="commented_out"),
        ],
    )
    def test_follows_mediawiki_category_rules(self, tmp_path, text, expected):
        assert _categories_of(tmp_path, text) == expected


# --- run -------------------------------------------------------------------


class TestRun:
    def test_loads_raw_wiki_pages(self, fake_wiki_xml, tmp_path, warehouse_path, snapshot):
        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)

        assert snapshot(warehouse_path, "raw")["wiki_pages"] == [
            ("Invented Inquisitor", "0", "101", "wiki_export.xml"),
            ("Invented World", "0", "102", "wiki_export.xml"),
        ]

    def test_loads_raw_wiki_page_categories(
        self, fake_wiki_xml, tmp_path, warehouse_path, snapshot
    ):
        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)

        assert snapshot(warehouse_path, "raw")["wiki_page_categories"] == [
            ("Invented Inquisitor", "Invented Characters", "101", "wiki_export.xml"),
            ("Invented Inquisitor", "Invented Novels", "101", "wiki_export.xml"),
            ("Invented World", "Invented Novels", "102", "wiki_export.xml"),
        ]

    def test_export_without_categories_still_loads_its_pages(
        self, tmp_path, warehouse_path, snapshot
    ):
        path = _write_export(tmp_path / "export.xml", _page(title="No category"))

        wiki_export.run(path, tmp_path, warehouse_path)

        state = snapshot(warehouse_path, "raw")
        assert [row[0] for row in state["wiki_pages"]] == ["No category"]
        assert "wiki_page_categories" not in state

    def test_rerun_drops_categories_removed_from_the_export(
        self, tmp_path, warehouse_path, snapshot
    ):
        """A category file left by the previous run must not be loaded again."""
        path = tmp_path / "export.xml"
        other = _write_export(tmp_path / "other.xml", _page(title="Other", text="[[Category:B]]"))
        wiki_export.export_to_jsonl(other, tmp_path)
        _write_export(path, _page(title="Page", text="[[Category:A]]"))
        wiki_export.run(path, tmp_path, warehouse_path)

        _write_export(path, _page(title="Page", text="No category any more"))
        wiki_export.run(path, tmp_path, warehouse_path)

        categories = snapshot(warehouse_path, "raw")["wiki_page_categories"]
        assert [row[:2] for row in categories] == [("Other", "B")]

    def test_keeps_one_jsonl_per_table(self, fake_wiki_xml, tmp_path, warehouse_path):
        """Each table needs its own file, or the second write erases the first."""
        raw_dir = tmp_path / "raw"

        wiki_export.run(fake_wiki_xml, raw_dir, warehouse_path)

        assert len(list(raw_dir.glob("*.jsonl"))) == len(WIKI_TABLES)

    def test_keeps_the_source_xml(self, fake_wiki_xml, tmp_path, warehouse_path):
        before = fake_wiki_xml.read_bytes()

        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)

        assert fake_wiki_xml.read_bytes() == before

    def test_does_not_touch_other_raw_tables(
        self, fake_wiki_xml, tmp_path, warehouse_path, snapshot
    ):
        with open_warehouse(warehouse_path) as conn:
            conn.execute("CREATE SCHEMA raw")
            conn.execute("CREATE TABLE raw.epub_metadata AS SELECT 1 AS id")

        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)

        assert snapshot(warehouse_path, "raw")["epub_metadata"] == [(1,)]


# --- no contributor name, no article text in any table ----------------------


class TestNothingForbiddenIsLoaded:
    """docs/sources/wiki_gg.md: article text and contributors are never loaded."""

    @pytest.fixture
    def loaded(self, fake_wiki_xml, tmp_path, warehouse_path):
        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)
        conn = duckdb.connect(str(warehouse_path), read_only=True)
        yield conn
        conn.close()

    def test_tables_only_have_the_allowed_columns(self, loaded):
        """An allow-list, so any new column has to be added here on purpose."""
        columns = loaded.execute(
            "SELECT table_name, column_name FROM information_schema.columns "
            "WHERE table_schema = 'raw' AND table_name LIKE 'wiki%' "
            "ORDER BY table_name, column_name"
        ).fetchall()

        assert columns == [
            ("wiki_page_categories", "category"),
            ("wiki_page_categories", "export_file"),
            ("wiki_page_categories", "page_id"),
            ("wiki_page_categories", "title"),
            ("wiki_pages", "export_file"),
            ("wiki_pages", "namespace"),
            ("wiki_pages", "page_id"),
            ("wiki_pages", "title"),
        ]

    @pytest.mark.parametrize("value", FORBIDDEN_VALUES)
    @pytest.mark.parametrize("table", WIKI_TABLES)
    def test_no_table_holds_a_forbidden_value(self, loaded, table, value):
        (count,) = loaded.execute(
            f'SELECT COUNT(*) FROM raw."{table}" AS t WHERE CAST(t AS VARCHAR) ILIKE ?',
            [f"%{value}%"],
        ).fetchone()

        assert count == 0

    @pytest.mark.parametrize("value", FORBIDDEN_VALUES)
    def test_no_jsonl_holds_a_forbidden_value(self, loaded, tmp_path, value):
        jsonl = "".join(p.read_text(encoding="utf-8") for p in tmp_path.glob("*.jsonl"))

        assert jsonl
        assert value not in jsonl


# --- main ------------------------------------------------------------------


class TestMain:
    def test_fails_when_xml_source_is_not_configured(self, monkeypatch, caplog):
        monkeypatch.setattr(wiki_export, "XML_SOURCE", None)
        caplog.set_level(logging.ERROR)

        assert wiki_export.main() == 1
        assert "XML_SOURCE is not configured" in [r.message for r in caplog.records]

    def test_fails_when_the_folder_is_missing(self, monkeypatch, tmp_path, caplog):
        monkeypatch.setattr(wiki_export, "XML_SOURCE", str(tmp_path / "missing"))
        caplog.set_level(logging.ERROR)

        assert wiki_export.main() == 1
        assert any("XML_SOURCE" in r.message for r in caplog.records)
        assert not config.WAREHOUSE_PATH.exists()

    def test_succeeds_and_loads_the_default_warehouse(
        self, monkeypatch, tmp_path, fake_wiki_xml, snapshot
    ):
        shutil.copy(fake_wiki_xml, tmp_path)
        monkeypatch.setattr(wiki_export, "XML_SOURCE", str(tmp_path))

        assert wiki_export.main() == 0

        assert set(WIKI_TABLES) <= set(snapshot(config.WAREHOUSE_PATH, "raw"))

    def test_loads_every_xml_file_of_the_folder(self, monkeypatch, tmp_path, snapshot):
        _write_export(tmp_path / "a.xml", _page(title="From A", text="[[Category:A]]"))
        _write_export(tmp_path / "b.xml", _page(title="From B", text="[[Category:B]]"))
        monkeypatch.setattr(wiki_export, "XML_SOURCE", str(tmp_path))

        assert wiki_export.main() == 0

        state = snapshot(config.WAREHOUSE_PATH, "raw")
        assert [row[0] for row in state["wiki_pages"]] == ["From A", "From B"]
        assert [row[:2] for row in state["wiki_page_categories"]] == [
            ("From A", "A"),
            ("From B", "B"),
        ]

    def test_loads_xml_files_from_subfolders(self, monkeypatch, tmp_path, snapshot):
        (tmp_path / "sub").mkdir()
        _write_export(tmp_path / "a.xml", _page(title="From A", text="[[Category:A]]"))
        _write_export(tmp_path / "sub" / "b.xml", _page(title="From B", text="[[Category:B]]"))
        monkeypatch.setattr(wiki_export, "XML_SOURCE", str(tmp_path))

        assert wiki_export.main() == 0

        state = snapshot(config.WAREHOUSE_PATH, "raw")
        assert [row[0] for row in state["wiki_pages"]] == ["From A", "From B"]

    def test_running_twice_does_not_duplicate_rows(self, monkeypatch, tmp_path, snapshot):
        _write_export(tmp_path / "a.xml", _page(title="From A", text="[[Category:A]]"))
        _write_export(tmp_path / "b.xml", _page(title="From B", text="[[Category:B]]"))
        monkeypatch.setattr(wiki_export, "XML_SOURCE", str(tmp_path))

        assert wiki_export.main() == 0
        first = snapshot(config.WAREHOUSE_PATH, "raw")
        assert wiki_export.main() == 0

        assert snapshot(config.WAREHOUSE_PATH, "raw") == first

    def test_fails_when_the_folder_has_no_xml_file(self, monkeypatch, tmp_path, caplog):
        monkeypatch.setattr(wiki_export, "XML_SOURCE", str(tmp_path))
        caplog.set_level(logging.ERROR)

        assert wiki_export.main() == 1
        assert not config.WAREHOUSE_PATH.exists()
