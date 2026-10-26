import json
import logging
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from config import W40K_FOLDER

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

        filename = unzipped_epub.filename
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
                    "file": filename,
                    "namespace": namespace,
                    "key": key,
                    "value": value,
                    "attributes": attrs,
                }
            )

        logging.debug("%s", json.dumps(rows, indent=2, ensure_ascii=False))
        return rows
    except KeyError:
        logging.exception("content.opf file not found, skipping")
        return []


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    if not W40K_FOLDER:
        logging.error("W40K_FOLDER is not configured")
        return

    w40k_dir = Path(W40K_FOLDER)
    for epub_path in w40k_dir.rglob("*.epub"):
        # try:
        logging.debug(epub_path)
        with ZipFile(epub_path) as epub:
            logging.debug(epub.filename)
            _ = reading_metadata_from_opf(epub)
        break


if __name__ == "__main__":
    main()
