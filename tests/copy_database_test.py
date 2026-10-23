import sqlite3

import pytest

from extract.copy_database import copy_data_db


@pytest.fixture
def fake_koreader_db(tmp_path):
    """A tiny SQLite file shaped like KOReader's statistics database."""
    path = tmp_path / "statistics.sqlite3"
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE book (id INTEGER PRIMARY KEY, title TEXT);
        INSERT INTO book (title) VALUES ('Fake Book One'), ('Fake Book Two');
        CREATE TABLE page_stat_data (id_book INTEGER, page INTEGER, duration INTEGER);
        INSERT INTO page_stat_data VALUES (1, 1, 30), (1, 2, 45), (2, 1, 12);
        CREATE VIEW page_stat AS SELECT * FROM page_stat_data;
        """
    )
    conn.commit()
    conn.close()
    return path


def test_copy_keeps_every_row(fake_koreader_db, tmp_path):
    dest = tmp_path / "copy.sqlite3"

    copy_data_db(fake_koreader_db, dest)

    conn = sqlite3.connect(dest)
    assert conn.execute("SELECT count(*) FROM book").fetchone()[0] == 2
    assert conn.execute("SELECT count(*) FROM page_stat_data").fetchone()[0] == 3
    conn.close()
