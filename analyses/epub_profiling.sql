/*
================================================================================
epub_profiling.sql
--------------------------------------------------------------------------------
Purpose : profile the EPUB metadata extracted from the OPF files (issue #8,
          milestone 4. Quality).
Source  : warehouse.raw.epub_metadata
          long format, one row per metadata tag:
          file | namespace | key | value | attributes (JSON text)
Run     : duckdb data/warehouse.duckdb -markdown -c ".read analyses/epub_profiling.sql"
Note    : the DuckDB UI is a scratchpad; this file is the reference version.
================================================================================
*/


-- -----------------------------------------------------------------------------
-- Q1. Size of the table
-- Question : how many files and rows, how many tags per file on average?
-- Finding  : about 22 tags per file. The row count is high because the table
--            is in long format (one row per tag, not one row per book).
-- -----------------------------------------------------------------------------
SELECT
  count(DISTINCT file) AS nb_files,
  count(*) AS nb_rows,
  round(count(*) / count(DISTINCT file), 1) AS avg_tags_per_file
FROM warehouse.raw.epub_metadata;


-- -----------------------------------------------------------------------------
-- Q2. Tags per file
-- Question : which files carry the most and the fewest distinct tags?
-- Finding  : files rewritten by hand or by Sigil carry the most tags; old Kobo
--            files carry the fewest.
-- -----------------------------------------------------------------------------
SELECT
  file,
  count(DISTINCT key) AS nb_distinct_tags
FROM warehouse.raw.epub_metadata
GROUP BY file
ORDER BY nb_distinct_tags DESC;


-- -----------------------------------------------------------------------------
-- Q3. Namespaces
-- Question : which namespaces exist, and how many rows each?
-- Note     : count(*) rather than count(namespace), so that an unexpected
--            namespace (or a NULL one) still shows up.
-- Finding  : two namespaces only, Dublin Core (dc:) and OPF (<meta> tags).
-- -----------------------------------------------------------------------------
SELECT
  namespace,
  count(*) AS nb_rows
FROM warehouse.raw.epub_metadata
GROUP BY namespace
ORDER BY nb_rows DESC;


-- -----------------------------------------------------------------------------
-- Q4. Value completeness per key
-- Question : in how many files does each key appear, and in how many is it
--            actually filled?
-- Finding  : presence overstates completeness. source, relation and coverage
--            are present in a dozen files but empty. Rare keys fall into three
--            families: EPUB 3 equivalents of common keys (belongs-to-collection,
--            group-position, file-as, role), empty tags, and tool noise
--            (Sigil version, generator, calibre:user_categories...).
-- -----------------------------------------------------------------------------
SELECT
  key,
  count(DISTINCT file) AS files_present,
  count(DISTINCT file) FILTER (
    WHERE nullif(trim(value), '') IS NOT NULL
  ) AS files_filled,
  count(*) AS nb_occurrences
FROM warehouse.raw.epub_metadata
GROUP BY key
ORDER BY files_present DESC, key ASC;


-- -----------------------------------------------------------------------------
-- Q5. Keys repeated within a file
-- Question : which keys appear more than once in the same file?
-- Finding  : subject and identifier are multi-valued by design. date appears
--            twice in some files (see attributes for what each date is), and
--            creator twice for books with two authors: max() in a pivot would
--            silently drop one value.
-- -----------------------------------------------------------------------------
SELECT
  file,
  key,
  count(*) AS nb_occurrences
FROM warehouse.raw.epub_metadata
GROUP BY file, key
HAVING count(*) > 1
ORDER BY nb_occurrences DESC, file ASC;


-- -----------------------------------------------------------------------------
-- Q6. One row per book (pivot)
-- Question : can the long format be turned into one row per file, with the
--            columns title, creator, publisher, published (key date), series
--            and series_index (keys calibre:series and calibre:series_index)?
-- Known    : max() keeps a single value per key. For keys repeated within a
--            file (see Q5: creator, date), one value is silently dropped.
--            EPUB 3 files store their series in belongs-to-collection, not
--            read here.
-- -----------------------------------------------------------------------------
SELECT
  file,
  max(value) FILTER (WHERE key = 'title') AS title,
  max(value) FILTER (WHERE key = 'creator') AS creator,
  max(value) FILTER (WHERE key = 'publisher') AS publisher,
  max(value) FILTER (WHERE key = 'date') AS published,
  max(value) FILTER (WHERE key = 'calibre:series') AS series,
  max(value) FILTER (WHERE key = 'calibre:series_index') AS series_index
FROM warehouse.raw.epub_metadata
GROUP BY file;


-- -----------------------------------------------------------------------------
-- Q7. Files without a series
-- Question : how many files have an empty series? List them.
-- Note     : same pivot as Q6, wrapped in a CTE so it can be filtered.
-- -----------------------------------------------------------------------------
WITH pivot_table AS (
  SELECT
    file,
    max(value) FILTER (WHERE key = 'title') AS title,
    max(value) FILTER (WHERE key = 'creator') AS creator,
    max(value) FILTER (WHERE key = 'publisher') AS publisher,
    max(value) FILTER (WHERE key = 'date') AS published,
    max(value) FILTER (WHERE key = 'calibre:series') AS series,
    max(value) FILTER (WHERE key = 'calibre:series_index') AS series_index
  FROM warehouse.raw.epub_metadata
  GROUP BY file
)

-- SELECT DISTINCT series FROM pivot_table;

SELECT * FROM pivot_table
WHERE series IS NULL;
