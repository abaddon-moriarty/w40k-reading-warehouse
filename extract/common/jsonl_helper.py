import json
import logging
from pathlib import Path


def write_jsonl(rows, path: Path, *, key: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    logging.info(
        "Wrote %d rows for %d files to %s",
        len(rows),
        len({r[key] for r in rows}),
        path,
    )
