import json
import logging
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

import duckdb

from extract.config import EREADER_ROOT, RAW_DIR, W40K_FOLDER, WAREHOUSE_PATH

OPF_NS = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def _strip_ns(name: str) -> str:
    return name.partition("}")[2] or name


def find_opf_path(zip_file: ZipFile):
    container_path = "META-INF/container.xml"
    if container_path not in zip_file.namelist():
        logging.warning("No container.xml in %s, skipping", zip_file.filename)
        return None

    with zip_file.open(container_path) as f:
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError:
            logging.exception("container.xml of %s is invalid, skipping", zip_file.filename)
            return None
        full_path = [
            element.attrib.get("full-path")
            for element in root.iter()
            if element.tag.endswith("rootfile")
        ]
        if not full_path:
            logging.warning("No rootfile in container.xml of %s, skipping", zip_file.filename)
            return None
        full_path = full_path[0]
        if full_path not in zip_file.namelist():
            logging.warning(
                "%s listed in container.xml but missing from %s, skipping",
                full_path,
                zip_file.filename,
            )
            return None
    return full_path


def read_opf_metadata(epub: ZipFile):
    full_path = find_opf_path(epub)
    if not full_path:
        return []

    try:
        opf_content = epub.read(full_path)
        root = ET.fromstring(opf_content)
        metadata = root.find("opf:metadata", OPF_NS)
        if metadata is None:
            logging.warning("No metadata tags were found.")
            return []

        filename = Path(epub.filename).relative_to(EREADER_ROOT)
        logging.debug("filename: %s", filename)
        rows = []
        for element in metadata.findall("*"):
            namespace, _, local_name = element.tag[1:].partition("}")

            if local_name == "meta":
                key = element.attrib.get("name") or element.attrib.get("property")
                value = element.attrib.get("content") or element.text
                attrs = {
                    _strip_ns(k): v
                    for k, v in element.attrib.items()
                    if _strip_ns(k) not in ("name", "property", "content")
                }
            else:
                key = local_name
                value = element.text
                attrs = {_strip_ns(k): v for k, v in element.attrib.items()}

            rows.append(
                {
                    "file": str(filename),
                    "namespace": namespace,
                    "key": key,
                    "value": value,
                    "attributes": json.dumps(attrs),
                }
            )

        logging.debug("%s", json.dumps(rows, indent=2, ensure_ascii=False))
        return rows
    except ET.ParseError:
        logging.exception("%s in %s is invalid, skipping", full_path, epub.filename)
        return []


def write_jsonl(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    logging.info(
        "Wrote %d rows for %d files to %s",
        len(rows),
        len({r["file"] for r in rows}),
        path,
    )


def upload_metadata_to_warehouse(output_path):
    conn = duckdb.connect(str(WAREHOUSE_PATH), config={"storage_compatibility_version": "v1.5.0"})

    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
    conn.execute(
        f"""CREATE OR REPLACE TABLE raw.epub_metadata AS
            SELECT * FROM read_json('{output_path}');"""
    )
    row_count = conn.execute("SELECT COUNT(*) FROM raw.epub_metadata").fetchone()[0]
    logging.info("Loaded raw.epub_metadata (%s rows)", row_count)

    conn.close()


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    if not W40K_FOLDER:
        logging.error("W40K_FOLDER is not configured")
        return 1
    if not EREADER_ROOT:
        logging.error("EREADER_ROOT is not configured")
        return 1
    w40k_dir = Path(W40K_FOLDER)
    if not w40k_dir.is_relative_to(EREADER_ROOT):
        logging.error("W40K_FOLDER must be inside EREADER_ROOT")
        return 1

    rows = []
    output_path = RAW_DIR / "epub_metadata.jsonl"

    for epub_path in w40k_dir.rglob("*.epub"):
        logging.debug(epub_path)
        try:
            with ZipFile(epub_path) as epub:
                rows.extend(read_opf_metadata(epub))
        except BadZipFile:
            logging.exception("%s is not a valid EPUB archive, skipping", epub_path)

    write_jsonl(rows, output_path)
    upload_metadata_to_warehouse(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
