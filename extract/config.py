import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
WAREHOUSE_PATH = DATA_DIR / "warehouse.duckdb"


def koreader_settings_dir() -> Path:
    value = os.environ.get("KOREADER_SETTINGS_DIR")
    if not value:
        raise RuntimeError(
            "KOREADER_SETTINGS_DIR is not set: copy .env.example to .env and fill it in."
        )
    return Path(value)
