import json
import logging
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import duckdb
from config import EREADER_ROOT, RAW_DIR, W40K_FOLDER, WAREHOUSE_PATH

OPF_NS = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def _strip_ns(name: str) -> str:
    return name.partition("}")[2] or name


def finding_content_opf(zip_file: ZipFile):
    container_path = "META-INF/container.xml"
    if container_path not in zip_file.namelist():
        return None

    with zip_file.open(container_path) as f:
        root = ET.parse(f).getroot()
        full_path = [
            element.attrib.get("full-path")
            for element in root.iter()
            if element.tag.endswith("rootfile")
        ]
        if not full_path:
            logging.warning("No rootfile found in container.xml of %s", zip_file.filename)
            return None
        full_path = full_path[0]
        if full_path not in zip_file.namelist():
            logging.warning("%s not found in container.xml, skipping", full_path)
            return None
    return full_path


def reading_metadata_from_opf(unzipped_epub):
    full_path = finding_content_opf(unzipped_epub)
    if not full_path:
        logging.warning("container.xml of %s book not found, skipping.", unzipped_epub.filename)
        return []

    try:
        opf_content = unzipped_epub.read(full_path)
        # logging.debug(opf_content)
        root = ET.fromstring(opf_content)
        metadata = root.find("opf:metadata", OPF_NS)
        if metadata is None:
            logging.warning("No metadata tags were found.")
            return []

        filename = Path(unzipped_epub.filename).relative_to(EREADER_ROOT)
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
    except KeyError:
        logging.exception("content.opf file not found, skipping")
        return []


def upload_metadata_to_warehouse(output_path):
    conn = duckdb.connect(str(WAREHOUSE_PATH), config={"storage_compatibility_version": "v1.5.0"})

    conn.execute("CREATE SCHEMA IF NOT EXISTS warehouse.raw")
    conn.execute(
        f"""CREATE OR REPLACE TABLE warehouse.raw.epub_metadata AS
            SELECT * FROM read_json('{output_path}');"""
    )
    row_count = conn.execute("SELECT COUNT(*) FROM warehouse.raw.epub_metadata").fetchone()[0]
    logging.info("Loaded raw.epub_metadata (%s rows)", row_count)

    conn.close()


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    if not W40K_FOLDER:
        logging.error("W40K_FOLDER is not configured")
        return
    rows = []
    output_path = RAW_DIR / "epub_metadata.jsonl"

    w40k_dir = Path(W40K_FOLDER)
    for epub_path in w40k_dir.rglob("*.epub"):
        # try:
        logging.debug(epub_path)
        with ZipFile(epub_path) as epub:
            rows.extend(reading_metadata_from_opf(epub))
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    logging.info(
        "Wrote %d rows for %d files to %s",
        len(rows),
        len({r["file"] for r in rows}),
        output_path,
    )

    upload_metadata_to_warehouse(output_path)


if __name__ == "__main__":
    main()
