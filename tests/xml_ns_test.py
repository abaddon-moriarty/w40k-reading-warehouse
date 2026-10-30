"""Tests for extract/common/xml_ns.py."""

import pytest

from extract.common.xml_ns import get_local_name, get_namespace


class TestGetNamespace:
    @pytest.mark.parametrize(
        "tag, expected",
        [
            (
                "{http://www.mediawiki.org/xml/export-0.11/}page",
                "http://www.mediawiki.org/xml/export-0.11/",
            ),
            ("{http://example.com}tag", "http://example.com"),
            ("{http://example.com}", "http://example.com"),  # no local name
            ("{}tag", ""),  # empty namespace
            ("tag", ""),  # no namespace at all
            ("", ""),
            ("{a}b}c", "a"),  # partition on first '}'
        ],
    )
    def test_returns_namespace(self, tag, expected):
        assert get_namespace(tag) == expected


class TestGetLocalName:
    @pytest.mark.parametrize(
        "tag, expected",
        [
            ("{http://www.mediawiki.org/xml/export-0.11/}page", "page"),
            ("{http://example.com}tag", "tag"),
            ("{}tag", "tag"),  # empty namespace
            ("tag", "tag"),  # no namespace
            ("", ""),
            ("{a}b}c", "b}c"),  # partition on first '}'
        ],
    )
    def test_returns_local_name(self, tag, expected):
        assert get_local_name(tag) == expected

    def test_returns_whole_tag_when_local_name_missing(self):
        """Edge case: '{ns}' with no local name — `partition` returns '',
        so the `or tag` fallback returns the input unchanged. Locked in."""
        assert get_local_name("{http://example.com}") == "{http://example.com}"
