import logging
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from extract.common.jsonl_helper import write_jsonl
from extract.common.warehouse import load_jsonl
from extract.common.xml_ns import get_namespace
from extract.config import XML_SOURCE


def extraction_from_xml(xml_file):
    tree = ET.parse(xml_file)

    root = tree.getroot()
    logging.debug(root.attrib)

    pages_rows = []
    cat_rows = []

    namespaces = {"root": get_namespace(root.tag)}

    for page in root.findall("root:page", namespaces):
        page_info = {}
        page_info["title"] = page.find("root:title", namespaces).text
        page_info["namespace"] = page.find("root:ns", namespaces).text
        page_info["page_id"] = page.find("root:id", namespaces).text
        page_info["export_file"] = xml_file.name

        pages_rows.append(page_info)

        text_el = page.find("root:revision/root:text", namespaces)
        text = text_el.text if text_el is not None and text_el.text else ""
        raw_categories = re.findall(r"\[\[Category:(?P<category>.*?)(?:\||]])", text)
        cleaned_categories = [cat.strip() for cat in raw_categories]
        for category in cleaned_categories:
            cat_rows.append(
                {
                    "title": page_info["title"],
                    "category": category,
                    "page_id": page_info["page_id"],
                    "export_file": page_info["export_file"],
                }
            )

    logging.info(len(pages_rows))
    logging.info(len(cat_rows))
    return pages_rows, cat_rows


def export_to_jsonl(source, raw_dir):
    output_page_path = raw_dir / f"{source.stem}_page.jsonl"
    output_category_path = raw_dir / f"{source.stem}_cat.jsonl"
    logging.debug(output_page_path)
    logging.debug(output_category_path)
    pages_rows, cat_rows = extraction_from_xml(source)

    write_jsonl(pages_rows, output_page_path, key="export_file")
    if cat_rows:
        write_jsonl(cat_rows, output_category_path, key="title")
    else:
        # Remove the file of a previous run, or its categories would still be loaded.
        output_category_path.unlink(missing_ok=True)
        logging.warning(
            "No categories found in %s; skipping %s",
            source.name,
            output_category_path.name,
        )


def load_exports(raw_dir, warehouse_path=None):
    load_jsonl(raw_dir / "*_page.jsonl", "raw", "wiki_pages", warehouse_path)
    if any(raw_dir.glob("*_cat.jsonl")):
        load_jsonl(raw_dir / "*_cat.jsonl", "raw", "wiki_page_categories", warehouse_path)
    else:
        logging.warning("No category file in %s; skipping wiki_page_categories", raw_dir)


def run(source, raw_dir, warehouse_path=None):
    export_to_jsonl(source, raw_dir)
    load_exports(raw_dir, warehouse_path)


def main():
    if not XML_SOURCE:
        logging.error("XML_SOURCE is not configured")
        return 1

    try:
        input_path = Path(XML_SOURCE)
        input_path.resolve(strict=True)
        all_files = [file for file in input_path.rglob("*.xml") if file.is_file()]
        if not all_files:
            logging.error("No XML files found under %s (check XML_SOURCE in .env)", input_path)
            return 1
        for file_path in all_files:
            export_to_jsonl(file_path, input_path)
        load_exports(input_path)

    except FileNotFoundError:
        logging.exception("Path does not exist. Make sure the XML_SOURCE in your .env is correct.")
        return 1
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    sys.exit(main())
