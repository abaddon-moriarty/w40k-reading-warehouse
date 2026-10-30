"""Tests for extract/wiki_export.py."""

import json
import logging
from xml.sax.saxutils import escape

import pytest

from extract import config, wiki_export

EXPORT_FILE_NAME = "Eisenhorn_Novel_Series).xml"

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


def _extract_one(tmp_path, text):
    path = _write_export(tmp_path / "export.xml", _page(text=text))
    (row,) = wiki_export.extraction_from_xml(path)
    return row


# --- extraction_from_xml: page fields --------------------------------------


class TestPageFields:
    def test_row_holds_the_expected_values(self, tmp_path):
        path = _write_export(
            tmp_path / "export.xml",
            _page(title="56-Izar", page_id="965", text="[[Category:Xenos Worlds]]"),
        )

        assert wiki_export.extraction_from_xml(path) == [
            {
                "title": "56-Izar",
                "ns": "0",
                "id": "965",
                "category": ["Xenos Worlds"],
                "source_file": "export.xml",
            }
        ]

    def test_article_text_is_never_kept(self, tmp_path):
        """docs/sources/wiki_gg.md: the text is ignored once categories are read."""
        row = _extract_one(tmp_path, "Secret article body [[Category:A]]")

        assert "text" not in row
        assert "Secret article body" not in json.dumps(row)

    def test_source_file_is_a_bare_file_name(self, tmp_path):
        row = _extract_one(tmp_path, "Body")

        assert row["source_file"] == "export.xml"

    def test_row_can_be_serialized_to_json(self, tmp_path):
        row = _extract_one(tmp_path, "[[Category:A]]")

        assert json.loads(json.dumps(row)) == row

    def test_ns_keeps_the_page_namespace(self, tmp_path):
        path = _write_export(tmp_path / "export.xml", _page(ns="14"))

        (row,) = wiki_export.extraction_from_xml(path)

        assert row["ns"] == "14"

    def test_every_page_gives_one_row_in_order(self, tmp_path):
        path = _write_export(
            tmp_path / "export.xml",
            _page(title="First", page_id="1"),
            _page(title="Second", page_id="2"),
        )

        rows = wiki_export.extraction_from_xml(path)

        assert [r["title"] for r in rows] == ["First", "Second"]

    def test_export_without_pages_gives_no_rows(self, tmp_path):
        path = _write_export(tmp_path / "export.xml")

        assert wiki_export.extraction_from_xml(path) == []

    def test_namespace_is_read_from_the_file(self, tmp_path):
        """Another export schema version must not need a code change."""
        path = _write_export(tmp_path / "export.xml", _page(title="Old"), version="0.10")

        (row,) = wiki_export.extraction_from_xml(path)

        assert row["title"] == "Old"


# --- extraction_from_xml: categories ---------------------------------------


class TestCategories:
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
        assert _extract_one(tmp_path, text)["category"] == expected

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
        assert _extract_one(tmp_path, text)["category"] == expected


# --- run -------------------------------------------------------------------


class TestRun:
    def test_loads_pages_into_raw_wiki_pages(
        self, fake_wiki_xml, tmp_path, warehouse_path, snapshot
    ):
        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)

        assert snapshot(warehouse_path, "raw")["wiki_pages"] == [
            ("Fake Page One", "0", "1", ["Fake One", "Fake Two"], "fake_export.xml"),
            ("Fake Page Two", "0", "2", ["Fake One"], "fake_export.xml"),
        ]

    def test_writes_jsonl_named_after_the_export(self, fake_wiki_xml, tmp_path, warehouse_path):
        raw_dir = tmp_path / "raw"

        wiki_export.run(fake_wiki_xml, raw_dir, warehouse_path)

        assert (raw_dir / "fake_export.jsonl").exists()

    def test_article_text_reaches_neither_jsonl_nor_warehouse(
        self, fake_wiki_xml, tmp_path, warehouse_path, snapshot
    ):
        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)

        jsonl = (tmp_path / "fake_export.jsonl").read_text(encoding="utf-8")
        assert "Article body" not in jsonl
        assert "Article body" not in str(snapshot(warehouse_path, "raw"))

    def test_keeps_the_source_xml(self, fake_wiki_xml, tmp_path, warehouse_path):
        before = fake_wiki_xml.read_bytes()

        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)

        assert fake_wiki_xml.read_bytes() == before

    def test_does_not_touch_other_raw_tables(
        self, fake_wiki_xml, tmp_path, warehouse_path, snapshot
    ):
        from extract.common.warehouse import open_warehouse

        with open_warehouse(warehouse_path) as conn:
            conn.execute("CREATE SCHEMA raw")
            conn.execute("CREATE TABLE raw.epub_metadata AS SELECT 1 AS id")

        wiki_export.run(fake_wiki_xml, tmp_path, warehouse_path)

        assert snapshot(warehouse_path, "raw")["epub_metadata"] == [(1,)]


# --- main ------------------------------------------------------------------


class TestMain:
    def test_fails_when_xml_source_is_not_configured(self, monkeypatch, caplog):
        monkeypatch.setattr(wiki_export, "XML_SOURCE", None)
        caplog.set_level(logging.ERROR)

        assert wiki_export.main() == 1
        assert "XML_SOURCE is not configured" in [r.message for r in caplog.records]

    def test_fails_when_export_file_is_missing(self, monkeypatch, tmp_path, caplog):
        monkeypatch.setattr(wiki_export, "XML_SOURCE", str(tmp_path))
        caplog.set_level(logging.ERROR)

        assert wiki_export.main() == 1
        assert any("XML_SOURCE" in r.message for r in caplog.records)
        assert not config.WAREHOUSE_PATH.exists()

    def test_succeeds_and_loads_the_default_warehouse(self, monkeypatch, tmp_path, snapshot):
        _write_export(tmp_path / EXPORT_FILE_NAME, _page(title="Loaded"))
        monkeypatch.setattr(wiki_export, "XML_SOURCE", str(tmp_path))

        assert wiki_export.main() == 0

        (row,) = snapshot(config.WAREHOUSE_PATH, "raw")["wiki_pages"]
        assert row[0] == "Loaded"
        assert (tmp_path / EXPORT_FILE_NAME).with_suffix(".jsonl").exists()
