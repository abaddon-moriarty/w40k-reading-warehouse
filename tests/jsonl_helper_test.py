"""Tests for extract/common/jsonl_helper.py."""

import json
import logging
from pathlib import Path

import pytest

from extract.common.jsonl_helper import write_jsonl


def _read_lines(path):
    return path.read_text(encoding="utf-8").splitlines()


class TestWriteJsonl:
    def test_writes_one_json_object_per_line(self, tmp_path):
        path = tmp_path / "out.jsonl"
        rows = [{"file": "a", "x": 1}, {"file": "b", "x": 2}]

        write_jsonl(rows, path, key="file")

        assert [json.loads(line) for line in _read_lines(path)] == rows

    def test_keeps_non_ascii_characters_readable(self, tmp_path):
        path = tmp_path / "out.jsonl"

        write_jsonl([{"file": "é", "title": "Horus Hérésie"}], path, key="file")

        assert "Horus Hérésie" in path.read_text(encoding="utf-8")

    def test_creates_missing_parent_directories(self, tmp_path):
        path = tmp_path / "a" / "b" / "out.jsonl"

        write_jsonl([{"file": "a"}], path, key="file")

        assert path.exists()

    def test_overwrites_previous_content(self, tmp_path):
        path = tmp_path / "out.jsonl"

        write_jsonl([{"file": "old"}], path, key="file")
        write_jsonl([{"file": "new"}], path, key="file")

        assert [json.loads(line) for line in _read_lines(path)] == [{"file": "new"}]

    def test_empty_rows_write_an_empty_file(self, tmp_path):
        path = tmp_path / "out.jsonl"

        write_jsonl([], path, key="file")

        assert path.read_text(encoding="utf-8") == ""

    def test_logs_row_and_distinct_file_counts(self, tmp_path, caplog):
        path = tmp_path / "out.jsonl"
        caplog.set_level(logging.INFO)

        write_jsonl([{"file": "a"}, {"file": "a"}, {"file": "b"}], path, key="file")

        assert f"Wrote 3 rows for 2 files to {path}" in [r.message for r in caplog.records]

    def test_key_selects_the_field_counted_as_file(self, tmp_path, caplog):
        path = tmp_path / "out.jsonl"
        caplog.set_level(logging.INFO)

        write_jsonl(
            [{"source_file": "a", "file": "x"}, {"source_file": "a", "file": "y"}],
            path,
            key="source_file",
        )

        assert f"Wrote 2 rows for 1 files to {path}" in [r.message for r in caplog.records]

    def test_key_missing_from_a_row_raises(self, tmp_path):
        with pytest.raises(KeyError):
            write_jsonl([{"other": "a"}], tmp_path / "out.jsonl", key="file")

    def test_non_serializable_value_raises(self, tmp_path):
        """A Path in a row must fail loudly: callers have to pass a string."""
        with pytest.raises(TypeError, match="PosixPath|WindowsPath"):
            write_jsonl([{"file": Path("a.xml")}], tmp_path / "out.jsonl", key="file")
