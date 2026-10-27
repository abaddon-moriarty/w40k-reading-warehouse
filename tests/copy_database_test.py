import sqlite3

from extract.copy_database import copy_data_db, main


def test_copy_keeps_every_row(fake_koreader_db, tmp_path):
    dest = tmp_path / "copy.sqlite3"

    copy_data_db(fake_koreader_db, dest)

    conn = sqlite3.connect(dest)
    assert conn.execute("SELECT count(*) FROM book").fetchone()[0] == 2
    assert conn.execute("SELECT count(*) FROM page_stat_data").fetchone()[0] == 3
    conn.close()


def test_main_fails_when_ereader_missing(monkeypatch, tmp_path):
    monkeypatch.setattr("extract.copy_database.koreader_settings_dir", lambda: tmp_path / "missing")
    assert main() == 1
