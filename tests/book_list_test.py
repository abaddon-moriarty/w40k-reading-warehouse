from extract.book_list import main


def test_main_fails_when_w40k_folder_is_not_configured(monkeypatch):
    monkeypatch.setattr("extract.book_list.W40K_FOLDER", None)

    assert main() == 1
