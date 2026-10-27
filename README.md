# w40k-reading-warehouse
A local data warehouse built from my Warhammer 40k reading: KOReader reading statistics and wiki data loaded into DuckDB, modelled with dbt.

**Problem**: KOReader knows how long I read each page, but not what I read about: which characters, places and factions I have already met, and in which book. The actual problem is that the Warhammer 40k universe is DENSE and I'm getting lost. This warehouse joins the two so that a future KOReader plugin (a spoiler-free "Pokédex" of the 40k universe) can answer "what do I know so far?".

This is a personal learning project: each milestone practises one data engineering concept (source mapping, data quality, compliance, layered ELT, entity resolution, dimensional modelling, history tracking, governance).

## Stack

| Layer | Tool |
|---|---|
| Environment | Python 3.14, [uv](https://docs.astral.sh/uv/) |
| Storage and queries | [DuckDB](https://duckdb.org/) (with the `sqlite` extension) |
| Transformations | [dbt](https://www.getdbt.com/) *(planned, from the Pipeline milestone)* |
| Quality | pytest, ruff, sqlfluff, pre-commit |

## Architecture

```
KOReader (statistics.sqlite3) ─┐
EPUB metadata (OPF) ───────────┤
wiki.gg / Lexicanum ───────────┼─► data/raw/ ─► DuckDB raw ─► staging ─► marts ─► KOReader plugin
EPUB tables of contents ───────┘
```


| Source | Extract script | Raw file | Raw table(s) | Status |
|---|---|---|---|---|
| KOReader reading statistics | `extract/copy_database.py` | `data/raw/koreader_db.sqlite3` | `raw_koreader.book`, `raw_koreader.page_stat_data`, `raw_koreader.numbers`, `raw_koreader.sqlite_sequence` | Done |
| EPUB metadata (OPF) | `extract/book_list.py` | `data/raw/epub_metadata.jsonl` | `raw.epub_metadata` | Done |
| Wiki categories and redirects | *(to do)* | | | To do |
| EPUB tables of contents | *(to do)* | | | V2 |

- **raw**: sources loaded as they are, every column read as text (types are cast in staging, not before). EPUB metadata is stored in long format: one row per metadata tag (`file`, `namespace`, `key`, `value`, `attributes`).
- **staging**: cleaned, typed and renamed. *(to do)*
- **marts**: facts and dimensions for the plugin. *(to do)*

## Getting started

Requirements: [uv](https://docs.astral.sh/uv/), [DuckDB CLI](https://duckdb.org/docs/installation/) (to explore), and a KOReader device or a copy of its files.

```bash
git clone https://github.com/abaddon-moriarty/w40k-reading-warehouse.git
cd w40k-reading-warehouse
uv sync
uv run pre-commit install
cp .env.example .env   # then fill in the variables below
```

| Variable | What it points to |
|---|---|
| `KOREADER_SETTINGS_DIR` | Folder containing KOReader's `statistics.sqlite3` |
| `EREADER_ROOT` | Root of the e-reader (or of its local copy); stored file paths are relative to it |
| `W40K_FOLDER` | Folder holding the Warhammer 40k EPUBs, inside `EREADER_ROOT` |
| `LOG_LEVEL` | `INFO` by default, `DEBUG` to troubleshoot |

On a Kobo, KOReader keeps its database in `.adds/koreader/settings/`. On another device, find it with:

```bash
find /path/to/ereader -name statistics.sqlite3
```

## Usage

```bash
uv run python -m extract.copy_database   # copy the KOReader database and load it into raw_koreader
uv run python -m extract.book_list       # read the metadata of every EPUB and load it into raw.epub_metadata
uv run pytest                            # run the tests
duckdb -ui data/warehouse.duckdb         # explore the warehouse in the browser
```

Run an analysis and get the result as a Markdown table:

```bash
duckdb data/warehouse.duckdb -markdown -c ".read analyses/epub_title_check.sql"
```

Both extract scripts only read from the e-reader: the KOReader database is opened read-only and copied before loading, and EPUB files are opened as archives without being modified. Running a script twice gives the same result: `copy_database.py` drops and rebuilds the `raw_koreader` schema in a single transaction, so it always mirrors the source database (a table removed from the source disappears too), and `book_list.py` replaces `raw.epub_metadata` with `CREATE OR REPLACE`.

### Checking a branch from a clean clone

Before opening a pull request, check that the pushed branch works on a fresh copy: no `data/` folder, no local leftovers. Push first, since the clone only sees what is on GitHub. Run from the root of your working copy, which supplies the branch name and the `.env`:

```bash
deactivate 2>/dev/null || true   # otherwise uv warns that VIRTUAL_ENV points to the main project's .venv
REPO=$(pwd) BRANCH=$(git branch --show-current)
rm -rf /tmp/check && cd /tmp
git clone -b "$BRANCH" https://github.com/abaddon-moriarty/w40k-reading-warehouse.git check
cd check && uv sync && cp "$REPO/.env" .env
uv run python -m extract.book_list && uv run pytest
```


## Project layout

```
extract/   one Python module per source, plus config.py (paths and settings)
analyses/  exploration and profiling queries, kept as SQL files (the DuckDB UI is only a scratchpad)
tests/     unit tests on small hand-made fixtures (no real reading data, no book content)
docs/      source sheets, decision records, data contract
data/      local only, ignored by Git: raw copies and warehouse.duckdb
```

## Project management

Work is tracked in [GitHub Issues](https://github.com/abaddon-moriarty/w40k-reading-warehouse/issues) and a GitHub Project board. One milestone per concept, one issue per work session, one pull request per issue.

| Milestone | Status |
|---|---|
| 1. Questions | Done |
| 2. Sources | In progress |
| 3. Compliance | To do |
| 4. Quality | To do |
| 5. Pipeline | To do |
| 6. Consolidation | To do |
| 7. Modelling | To do |
| 8. History | To do |
| 9. Documentation | To do |

## Key decisions

- **Raw layer is all text.** SQLite does not enforce column types; DuckDB does. Reading everything as text in raw keeps the load from failing on a stray value, and casting happens in staging where it can be tested.
- **Copy first, then load.** The e-reader database is backed up to `data/raw/` with SQLite's backup API before DuckDB reads it, so the device file is only ever opened read-only.
- **EPUB metadata in long format.** Every tag of the OPF `<metadata>` block becomes one row, Dublin Core and `<meta>` alike (Calibre and EPUB 3). Nothing is lost at extraction, the schema never changes from one book to another, and multi-valued tags (several subjects or authors) need no special case. Pivoting to one row per book happens in staging.
- **Relative paths only.** File paths are stored relative to `EREADER_ROOT`, so the data never contains a user name or a mount point.
- **Titles are compared on a normalised key.** Neither the file name nor the `dc:title` is reliable on its own; both are compared after the same normalisation (apostrophes, `_`, trailing ", The", case). The displayed title stays the original one.

Full decision records: [`docs/decisions/`](docs/decisions/) *(to do)*.

## Known limitations

- Only `W40K_FOLDER` is scanned: a Warhammer book stored elsewhere on the e-reader is missed.
- EPUB metadata is uneven: placeholder dates (`0101-01-01`), dates shifted by one time zone, technical or empty series values, a few wrong titles. They are kept as they are in raw and handled in staging.
- KOReader only knows the books that have been opened.
- No automated test for the EPUB extraction yet.

The full list, with the planned fix for each, is kept in the project tracking document.

## Data and licences

- No data is distributed with this repository. Reading statistics and book files stay on my machine.
- Wiki data from [warhammer40k.wiki.gg](https://warhammer40k.wiki.gg/) is under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Other sources: licences to be checked (Compliance milestone).
- Code licence: [MIT or Apache 2.0, to be chosen].

*This is an unofficial fan project, not endorsed by Games Workshop. Warhammer 40,000 is a trademark of Games Workshop Ltd.*
