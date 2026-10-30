"""Tests for extract/book_list.py."""

import json
import logging
import zipfile
from pathlib import Path

import pytest

from extract import book_list, config

# --- helpers ---------------------------------------------------------------

CONTAINER_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
              media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def _build_epub(path: Path, metadata_xml: str, opf_path: str = "OEBPS/content.opf") -> None:
    opf = f"""\
<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
{metadata_xml}
  </metadata>
</package>
"""
    container = CONTAINER_XML.replace('full-path="OEBPS/content.opf"', f'full-path="{opf_path}"')
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip")
        zf.writestr("META-INF/container.xml", container)
        zf.writestr(opf_path, opf)


def _read(path: Path):
    with zipfile.ZipFile(path) as epub:
        return book_list.read_opf_metadata(epub)


def patch_config(monkeypatch, name: str, value):
    """Patch `name` in config and in book_list, wherever it exists.

    Raises AttributeError if it exists in neither — catches typos and
    survives the migration from `from extract.config import X` to
    `from extract import config; config.X`.
    """
    targets = [mod for mod in (config, book_list) if hasattr(mod, name)]
    if not targets:
        raise AttributeError(f"{name} not found in config or book_list")
    for mod in targets:
        monkeypatch.setattr(mod, name, value)


@pytest.fixture
def fake_epub(tmp_path, monkeypatch):
    """Return a factory that builds an EPUB under a temp EREADER_ROOT."""
    root = tmp_path / "ereader"
    root.mkdir()
    patch_config(monkeypatch, "EREADER_ROOT", root)

    def _make(metadata_xml: str, name: str | Path = "book.epub") -> Path:
        path = root / name
        _build_epub(path, metadata_xml)
        return path

    return _make


# --- main(): configuration guard ------------------------------------------


class TestMain:
    def test_main_fails_when_w40k_folder_is_not_configured(self, monkeypatch, caplog):
        patch_config(monkeypatch, "W40K_FOLDER", None)
        caplog.set_level(logging.ERROR)
        assert book_list.main() == 1
        assert any(
            "W40K_FOLDER" in r.message or "W40K_FOLDER" in str(r.args) for r in caplog.records
        ), "main() should log which config value is missing"

    def test_main_writes_jsonl_and_loads_epub_metadata(
        self, fake_epub, monkeypatch, tmp_path, snapshot
    ):
        """Regression: main() once called write_jsonl with an undefined name."""
        epub = fake_epub("<dc:title>Xenos</dc:title>", Path("w40k", "book.epub"))
        patch_config(monkeypatch, "W40K_FOLDER", epub.parent)
        patch_config(monkeypatch, "RAW_DIR", tmp_path / "raw")

        assert book_list.main() == 0

        assert (tmp_path / "raw" / "epub_metadata.jsonl").exists()
        (row,) = snapshot(config.WAREHOUSE_PATH, "raw")["epub_metadata"]
        assert (row[2], row[3]) == ("title", "Xenos")


# --- read_opf_metadata: regression str(element) → element.tag -------------


class TestTagHandling:
    def test_key_comes_from_local_name(self, fake_epub):
        rows = _read(fake_epub("<dc:title>Xenos</dc:title>"))
        assert rows[0]["key"] == "title"

    def test_namespace_comes_from_tag(self, fake_epub):
        rows = _read(fake_epub("<dc:title>Xenos</dc:title>"))
        assert rows[0]["namespace"] == "http://purl.org/dc/elements/1.1/"

    def test_no_element_repr_leaks_into_output(self, fake_epub):
        rows = _read(fake_epub("<dc:title>Xenos</dc:title>"))
        row = rows[0]
        for field in ("key", "namespace", "value"):
            assert "Element" not in str(row[field]), f"{field} leaked str(Element)"
            assert "0x" not in str(row[field]), f"{field} leaked element address"

    def test_value_comes_from_element_text(self, fake_epub):
        rows = _read(fake_epub("<dc:title>Xenos</dc:title>"))
        assert rows[0]["value"] == "Xenos"

    def test_plain_element_has_empty_attributes_json(self, fake_epub):
        rows = _read(fake_epub("<dc:title>Xenos</dc:title>"))
        assert rows[0]["attributes"] == "{}"


# --- read_opf_metadata: the `meta` branch --------------------------------


class TestMetaBranch:
    def test_meta_with_name_and_content(self, fake_epub):
        rows = _read(fake_epub('<meta name="calibre:series" content="Eisenhorn"/>'))
        assert len(rows) == 1
        assert rows[0]["key"] == "calibre:series"
        assert rows[0]["value"] == "Eisenhorn"

    def test_meta_with_property_and_text_body(self, fake_epub):
        rows = _read(fake_epub('<meta property="dcterms:modified">2020-01-01T00:00:00Z</meta>'))
        assert rows[0]["key"] == "dcterms:modified"
        assert rows[0]["value"] == "2020-01-01T00:00:00Z"

    def test_meta_prefers_content_over_text(self, fake_epub):
        rows = _read(fake_epub('<meta name="k" content="from-content">ignored</meta>'))
        assert rows[0]["value"] == "from-content"

    def test_meta_prefers_name_over_property(self, fake_epub):
        rows = _read(fake_epub('<meta name="n" property="p" content="v"/>'))
        assert rows[0]["key"] == "n"

    def test_meta_extra_attributes_are_kept(self, fake_epub):
        rows = _read(fake_epub('<meta name="n" content="v" id="x" scheme="y"/>'))
        assert json.loads(rows[0]["attributes"]) == {"id": "x", "scheme": "y"}

    def test_meta_excludes_reserved_attributes(self, fake_epub):
        rows = _read(fake_epub('<meta name="n" property="p" content="v"/>'))
        attrs = json.loads(rows[0]["attributes"])
        assert not {"name", "property", "content"} & set(attrs)

    def test_meta_branch_triggers_on_local_name_only(self, fake_epub):
        rows = _read(fake_epub('<meta name="calibre:series" content="Eisenhorn"/>'))
        # If the branch hadn't fired, key would be "meta" and value None.
        assert rows[0]["key"] != "meta"
        assert rows[0]["key"] == "calibre:series"
        assert rows[0]["value"] == "Eisenhorn"


# --- read_opf_metadata: filenames ----------------------------------------


class TestFilename:
    def test_filename_is_relative_to_ereader_root(self, fake_epub):
        rows = _read(fake_epub("<dc:title>T</dc:title>", name="book.epub"))
        assert rows[0]["file"] == "book.epub"

    def test_filename_keeps_subdirectories(self, fake_epub):
        nested = Path("a", "b", "book.epub")
        rows = _read(fake_epub("<dc:title>T</dc:title>", name=nested))
        assert rows[0]["file"] == str(nested)

    def test_filename_has_no_leading_separator(self, fake_epub):
        rows = _read(fake_epub("<dc:title>T</dc:title>", name="book.epub"))
        assert not rows[0]["file"].startswith("/")


# --- read_opf_metadata: multiple rows ------------------------------------


class TestMultipleRows:
    def test_preserves_order_of_metadata_elements(self, fake_epub):
        rows = _read(
            fake_epub(
                "<dc:title>T</dc:title>"
                "<dc:creator>C</dc:creator>"
                '<meta name="calibre:series" content="Eisenhorn"/>'
                '<meta property="dcterms:modified">2020-01-01</meta>'
            )
        )
        assert [r["key"] for r in rows] == [
            "title",
            "creator",
            "calibre:series",
            "dcterms:modified",
        ]

    def test_all_rows_share_same_file(self, fake_epub):
        rows = _read(fake_epub("<dc:title>T</dc:title><dc:creator>C</dc:creator>"))
        assert {r["file"] for r in rows} == {"book.epub"}

    def test_attributes_is_valid_json(self, fake_epub):
        rows = _read(
            fake_epub(
                '<dc:title id="t1">T</dc:title><meta name="n" content="v" id="m1" scheme="s"/>'
            )
        )
        for row in rows:
            assert isinstance(json.loads(row["attributes"]), dict)


# --- read_opf_metadata: error handling -----------------------------------


class TestErrorHandling:
    def test_missing_metadata_element_returns_empty(self, tmp_path, monkeypatch, caplog):
        root = tmp_path / "ereader"
        root.mkdir()
        patch_config(monkeypatch, "EREADER_ROOT", root)

        path = root / "book.epub"
        opf = (
            '<?xml version="1.0"?>'
            '<package xmlns="http://www.idpf.org/2007/opf" version="3.0">'
            "<manifest/></package>"
        )
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("META-INF/container.xml", CONTAINER_XML)
            zf.writestr("OEBPS/content.opf", opf)

        caplog.set_level(logging.WARNING)
        assert _read(path) == []
        assert any("No metadata" in r.message for r in caplog.records)

    def test_malformed_opf_returns_empty(self, fake_epub, caplog):
        path = fake_epub("<dc:title>T</dc:title>")
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("META-INF/container.xml", CONTAINER_XML)
            zf.writestr("OEBPS/content.opf", '<?xml version="1.0"?><package><oops>')

        caplog.set_level(logging.ERROR)
        assert _read(path) == []
        assert any("invalid" in r.message.lower() for r in caplog.records)

    def test_missing_container_xml_returns_empty(self, fake_epub, caplog):
        """EPUB with no META-INF/container.xml at all."""
        path = fake_epub("<dc:title>T</dc:title>")
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("mimetype", "application/epub+zip")
            zf.writestr("OEBPS/content.opf", "<package/>")
        caplog.set_level(logging.WARNING)
        assert _read(path) == []

    def test_container_without_rootfile_returns_empty(self, fake_epub, caplog):
        """container.xml exists but has no <rootfile full-path=...>."""
        path = fake_epub("<dc:title>T</dc:title>")
        empty_container = (
            '<?xml version="1.0"?>'
            '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            "<rootfiles/></container>"
        )
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("mimetype", "application/epub+zip")
            zf.writestr("META-INF/container.xml", empty_container)
            zf.writestr("OEBPS/content.opf", "<package/>")
        caplog.set_level(logging.WARNING)
        assert _read(path) == []

    def test_rootfile_points_to_missing_opf_returns_empty(self, fake_epub, caplog):
        """container.xml points to an OPF that isn't in the archive.

        Requires read_opf_metadata to catch KeyError in addition to
        ET.ParseError — otherwise ZipFile.read raises and this test fails.
        """
        path = fake_epub("<dc:title>T</dc:title>")
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("mimetype", "application/epub+zip")
            zf.writestr("META-INF/container.xml", CONTAINER_XML)
            # NOTE: no OEBPS/content.opf entry
        caplog.set_level(logging.ERROR)
        assert _read(path) == []
