/*
================================================================================
Q8-Q9. File name or metadata title?
--------------------------------------------------------------------------------
Goal     : can the title in the file name serve as a key, or is the metadata
           title (dc:title) needed?

Mismatches found with an exact comparison:
  - ", The" at the end of the file name, at the beginning in dc:title
      Swords of Calth, The
      Soul Drinker_s Omnibus, The
      Uriel Ventris Chronicles_ Volume Two, The
      Inquisition War Omnibus, The
      WARPED STARS, THE
      Soul Drinkers Omnibus II, The
      Alien Beast Within, The
      Grey Knights Omnibus, The
  - "_" replacing ":" or "'" in the file name
      Ultramarines_ The Second Omnibus
      Soul Drinker_s Omnibus, The
      Assault on Black Reach_ The Novel
      Uriel Ventris Chronicles_ Volume Two, The
  - Wrong titles in the metadata (files renamed by hand at some point;
    hard to clean, they go to a hand-maintained mapping)
      The Alien Beast Within  -> Warhammer 40,000
      Pariah                  -> Pariah - Bequin #1
      Old Soldiers Never Die  -> Old Soldiers Never Die by Mitchell Sandy
      Choose Your Enemies     -> Ciaphas Cain: Choose Your Enemies
  - Case (Of / of)
      Warriors Of Ultramar    -> Warriors of Ultramar
      Chains Of Command       -> Chains of Command
  - Apostrophe encoding (typographic vs straight)
      Cain’s Last Stand       -> Cain's Last Stand
      The Traitor’s Hand      -> The Traitor's Hand

Result   : 19 mismatches with an exact comparison, 4 after normalisation of
           both sides (the 4 wrong metadata titles above).
================================================================================
*/


-- -----------------------------------------------------------------------------
-- Q8. Normalisation macro
-- Purpose  : build a comparison key only; the displayed title stays the
--            original one. One rule per line, in the order they are applied.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TEMP MACRO normalize_title(t) AS
lower(
  regexp_replace(
    replace(
      regexp_replace(
        replace(trim(t), '’', ''''),   -- typographic apostrophe -> '
        '_s\b', '''s', 'g'
      ),           -- "Drinker_s" -> "Drinker's"
      '_', ':'
    ),                         -- remaining "_" -> ":"
    '^(.*), the$', 'the \1', 'i'
  )          -- "X, The" -> "The X"
);


-- -----------------------------------------------------------------------------
-- Q9. Titles that still differ after normalisation
-- Question : how many files have a title from the file name that differs from
--            dc:title once both go through normalize_title?
-- Finding  : 4, the wrong metadata titles listed above.
-- -----------------------------------------------------------------------------
WITH pivot_table AS (
  SELECT
    file,
    regexp_replace(string_split(file, '/')[-1], '\.k?epub$', '') AS file_name,
    string_split(regexp_replace(string_split(file, '/')[-1], '(\.kepub)?\.epub$', ''), ' - ')[1]
      AS raw_title_from_file,
    max(value) FILTER (WHERE key = 'title') AS title

  FROM warehouse.raw.epub_metadata
  GROUP BY file
)

SELECT count(*) AS non_normalised_names FROM pivot_table
WHERE normalize_title(raw_title_from_file) != normalize_title(title);
