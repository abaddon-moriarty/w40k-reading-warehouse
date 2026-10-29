# extract/common/xml_ns.py

"""Helpers for Clark-notation XML tags: '{namespace}localname'."""


def get_namespace(tag: str) -> str:
    """Return the namespace URI of a tag, or '' if it has none."""
    ns, sep, _ = tag.partition("}")
    return ns.lstrip("{") if sep else ""


def get_local_name(tag: str) -> str:
    """Return the tag without its namespace."""
    return tag.partition("}")[2] or tag
