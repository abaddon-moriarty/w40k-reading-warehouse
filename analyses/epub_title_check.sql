-- 1. Combien de fichiers, combien de lignes

SELECT
  count(DISTINCT file) AS nb_file,
  count(*) AS nb_line
FROM warehouse.raw.epub_metadata;

-- le fichier contient presque 1000 lignes pour 46 livres.
-- C'est parce que les données sont en format long,
-- une ligne par attribut et non une ligne par livre;

-- 2. Quelles balises, présentes dans combien de livres (complétude des valeurs)
SELECT
  key,
  count(DISTINCT file) AS files
FROM warehouse.raw.epub_metadata
GROUP BY key
ORDER BY files ASC;


-- cette requête nous permet de voir quelles balises ont les moins utilisées
-- Celles qu'il faudrait nettoyer ou pour lesquelles il faut trouver une correspondance
-- là toutes celles qui se trouve en dessous de 10 occurences sont à surveiller.
-- D'où elles viennent (quelles valeurs etc);

SELECT
  file,
  key,
  value
FROM warehouse.raw.epub_metadata
WHERE key IN (
  SELECT sub.key FROM warehouse.raw.epub_metadata AS sub
  GROUP BY sub.key
  HAVING count(DISTINCT sub.file) < 15
);

-- moyenne de balise par fichier
SELECT round(avg(nb_balises), 1) AS moyenne_balise FROM (
  SELECT count(key) AS nb_balises FROM warehouse.raw.epub_metadata
  GROUP BY file
) AS sub;

-- 3. Combien de balises en moyenne par fichier ? Quel fichier en a le plus, lequel en a le moins ?
SELECT
  file,
  count(DISTINCT key) AS nb_balises
FROM warehouse.raw.epub_metadata
GROUP BY file
ORDER BY nb_balises DESC;

-- Penitent	: 22 balises
-- Old Soldiers Never Die :	8 balises;

-- Quelles valeurs de `namespace` existent, et combien de lignes pour chacune ?
SELECT
  namespace,
  count(*) AS nb_lignes
FROM warehouse.raw.epub_metadata
GROUP BY namespace;

-- je fais count(*) comme ça si jamais un autre name space s'introduit on le verra aussi
-- (même si pour l'instant c'est hard-codé dans le script, ça fait une sécurité);

/* 2. **Mesurer la complétude des valeurs**
    - Pour chaque `key`, dans combien de fichiers apparaît-elle ?
    Triez du plus fréquent au moins fréquent.
*/

SELECT
  key,
  count(DISTINCT file) AS nb_occurence
FROM warehouse.raw.epub_metadata
GROUP BY key
ORDER BY nb_occurence DESC;

/* 2. **Mesurer la complétude des valeurs**
- Quelles clés apparaissent plusieurs fois **dans un même fichier** ?
(Indice : groupez par `file` et `key`, puis filtrez les groupes.) */

SELECT
  file,
  key,
  count(file) AS nb_occurence
FROM warehouse.raw.epub_metadata
GROUP BY file, key
HAVING count(*) > 1
ORDER BY nb_occurence DESC;

/* 3. **Pivoter**
    - Écrivez une requête qui renvoie une ligne par fichier
      avec les colonnes `title`, `creator`, `publisher`, `published` (clé `date`),
      `series` et `series_index` (clés `calibre:series` et `calibre:series_index`).
*/

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

--     - Combien de fichiers ont une série vide ? Listez-les.
-- SELECT DISTINCT series FROM pivot_table;

SELECT * FROM pivot_table
WHERE series IS NULL;

/* 4. Nom de fichier ou titre des métadonnées
**Objectif :** savoir si le nom du fichier pourrait servir de clé,
ou s'il faut absolument passer par les métadonnées
*/


/*
Différences rencontrées:
- ", The" at the end of the raw_title_from_file but at the beginning in the title
  - Swords of Calth, The
  - Soul Drinker_s Omnibus, The
  - Uriel Ventris Chronicles_ Volume Two, The
  - Inquisition War Omnibus, The
  - WARPED STARS, THE
  - Soul Drinkers Omnibus II, The
  - Alien Beast Within, The
  - Grey Knights Omnibus, The
- "_" replacing a ":" or a "'" in the file name
  - Ultramarines_ The Second Omnibus
  - Soul Drinker_s Omnibus, The
  - Assault on Black Reach_ The Novel
  - Uriel Ventris Chronicles_ Volume Two, The
  -
- Some titles are Just wrong because I updated the names at some points Those will be hard to clean
  - The Alien Beast Within -> Warhammer 40,000
  - Pariah ->Pariah - Bequin #1
  - Old Soldiers Never Die -> Old Soldiers Never Die by Mitchell Sandy
  - Choose Your Enemies ->	Ciaphas Cain: Choose Your Enemies
- UpperCase lowercase issues in Of/of
  - Warriors Of Ultramar -> Warriors of Ultramar
  - Chains Of Command -> 	Chains of Command
- Some encoding differences:
  - Cain’s Last Stand -> Cain's Last Stand: the appostrophe
  - The Traitor’s Hand	The Traitor's Hand
*/

-- One rule per line, in the order they are applied.
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
