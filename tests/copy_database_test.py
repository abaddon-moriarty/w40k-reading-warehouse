import sqlite3

from extract.copy_database import copy_data_db


def test_copy_keeps_every_row(fake_koreader_db, tmp_path):
    dest = tmp_path / "copy.sqlite3"

    copy_data_db(fake_koreader_db, dest)

    conn = sqlite3.connect(dest)
    assert conn.execute("SELECT count(*) FROM book").fetchone()[0] == 2
    assert conn.execute("SELECT count(*) FROM page_stat_data").fetchone()[0] == 3
    conn.close()
