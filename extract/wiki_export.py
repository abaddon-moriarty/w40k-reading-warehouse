import logging
import re
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

    rows = []

    namespaces = {"root": get_namespace(root.tag)}

    for page in root.findall("root:page", namespaces):
        page_info = {}
        page_info["title"] = page.find("root:title", namespaces).text
        page_info["ns"] = page.find("root:ns", namespaces).text
        page_info["id"] = page.find("root:id", namespaces).text

        text_el = page.find("root:revision/root:text", namespaces)
        text = text_el.text if text_el is not None and text_el.text else ""

        raw_categories = re.findall(r"\[\[Category:(?P<category>.*?)(?:\||]])", text)
        cleaned_categories = [cat.strip() for cat in raw_categories]
        page_info["category"] = cleaned_categories
        page_info["source_file"] = xml_file.name
        rows.append(page_info)
    logging.info(len(rows))
    return rows


def main():
    file_name = "Eisenhorn_Novel_Series).xml"
    input_path = Path(XML_SOURCE, file_name)
    logging.debug(input_path)
    output_path = Path(XML_SOURCE, file_name).with_suffix(".jsonl")
    logging.debug(output_path)
    rows = extraction_from_xml(input_path)
    write_jsonl(rows, output_path, key="source_file")
    load_jsonl(output_path, "raw", "wiki_pages")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    main()
