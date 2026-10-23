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
wiki.gg / Lexicanum ───────────┼─► data/raw/ ─► DuckDB raw ─► staging ─► marts ─► KOReader plugin
EPUB tables of contents ───────┘
```

- **raw**: sources loaded as they are, every column read as text (types are cast in staging, not before).
- **staging**: cleaned, typed and renamed. *(to do)*
- **marts**: facts and dimensions for the plugin. *(to do)*

## Getting started

Requirements: [uv](https://docs.astral.sh/uv/), and a KOReader device or a copy of its `statistics.sqlite3`.

```bash
git clone https://github.com/abaddon-moriarty/w40k-reading-warehouse.git
cd w40k-reading-warehouse
uv sync
uv run pre-commit install
cp .env.example .env   # then set KOREADER_SETTINGS_DIR
```

On a Kobo, KOReader keeps its database in `.adds/koreader/settings/`. On another device, find it with:

```bash
find /path/to/ereader -name statistics.sqlite3
```

## Usage

```bash
uv run python -m extract.copy_database   # copy the KOReader database and load it into data/warehouse.duckdb
uv run pytest                            # run the tests
duckdb -ui data/warehouse.duckdb         # explore the warehouse in the browser
```

The source database is opened read-only and copied before loading: the script never writes to the e-reader. Running it twice gives the same result.

## Project layout

```
extract/   one Python module per source, plus config.py (paths and settings)
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

Full decision records: [`docs/decisions/`](docs/decisions/) *(to do)*.

## Data and licences

- No data is distributed with this repository. Reading statistics and book files stay on my machine.
- Wiki data from [warhammer40k.wiki.gg](https://warhammer40k.wiki.gg/) is under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Other sources: licences to be checked (Compliance milestone).
- Code licence: [MIT or Apache 2.0, to be chosen].

*This is an unofficial fan project, not endorsed by Games Workshop. Warhammer 40,000 is a trademark of Games Workshop Ltd.*


Corpus: 37 English Warhammer 40k novels (personal collection)
Data sources: K-Readers stats DB, wiki.gg corpus (CC BY-NC 4.0)
