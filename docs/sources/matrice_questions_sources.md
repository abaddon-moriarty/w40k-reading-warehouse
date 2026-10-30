# Matrice questions × sources

## Matrice

| Question | Fichiers EPUB | Statistiques KOReader | `.sdr` (statut) | wiki.gg (exports) | Seeds manuels |
| --- | --- | --- | --- | --- | --- |
| Q1 — Livres où apparaît une entité, premier dans mon ordre de lecture | Principale : apparitions dans le texte | Complément : date de dernière session, pour l'ordre de lecture | Principale : livre fini | Principale : liste et type des entités | Complément : alias, exclusions, correspondance des livres |
| Q2 — Entités débloquées jusqu'ici, et celles qui restent verrouillées | Principale : apparitions | Complément : date de fin | Principale : livre fini | Principale : entités | Complément : alias, exclusions |
| Q3 — Livre non lu qui débloquerait le plus | Principale : livres possédés et apparitions | Complément : livres ouverts | Principale : livre non fini | Principale : entités | Complément |
| Q4 — Entités qui reviennent d'une série à l'autre | Principale : série (`calibre:series` dans 36 fichiers sur 46, `belongs-to-collection` dans 3) | Aucune | Aucune | Principale : entités ; catégories de série | Complément : correspondance des livres (séries manquantes) |
| Q5 (V2) — Informations déjà rencontrées à ma position | Principale : table des matières, position des apparitions | Principale : position de lecture | Complément : positions | Partielle ; Lexicanum (citations au chapitre) en V2, sous réserve d'accord | Aucune |

## Sources manquantes et sources écartées

- **Alias (noms courts)** : les redirections manquent dans les exports et le sitemap. v0.1 : seed `entity_alias` tenu à la main ; redirections en V2, avec l'accord du wiki.
- **Entités absentes du wiki lui-même** (Lowink, le vaisseau Essene dans Xenos) : ajout à la main, seule voie en v0.1.
- **Date de fin de lecture** : pas dans la base de statistiques. Statut « fini » lu dans les `.sdr` (champ à confirmer), date approchée par la dernière session.
- **Série des livres** : absente de 7 fichiers EPUB. Correction dans le seed `book_mapping`, contrôle par les catégories de série du wiki.
- **Contenu des omnibus et position des apparitions (Q5)** : table des matières des EPUB (V2) ; ISFDB, non évaluée, pour le contenu des omnibus.
- **Source à créer** : mes propres relevés pendant la lecture. En v0.1, ils prennent la forme des seeds `entity_alias` et `coverage_check`.
- **Écartées ou reportées** : Black Library, Vocabulary Builder, Fandom, Lexicanum (V2), pages de termes génériques de wiki.gg (glossaire en V+), sitemap comme lexique. Raisons et dates dans `excluded_sources.md`.

## Biais et limites connus

Ce que l'on sait faux ou incomplet et qu'on accepte pour avancer. Chaque ligne dit comment le corriger plus tard ; elle alimente la section « limites » du README et la définition de « fini » de la V1.

| Données | Biais / effet | Correction prévue | Concept |
| --- | --- | --- | --- |
| Périmètre EPUB = le dossier `W40K_FOLDER` | Un livre Warhammer rangé ailleurs sur la liseuse est ignoré ; le décompte des livres peut être sous-estimé | Parcourir `EREADER_ROOT`, garder le dossier comme une donnée et décider en staging à partir du dossier, du subject, de l'éditeur et de la série | C3 complétude de la population |
| Dates des OPF décalées d'un fuseau (`2004-12-02T23:00:00+00:00` pour un 3 décembre probable) | Tronquer à la date donne la veille | Convertir en heure de Paris avant de tronquer, en staging ; vérifier sur un livre dont la date est connue | C3 exactitude |
| `calibre:timestamp` n'est pas une date de publication | Risque de confondre date d'ajout dans Calibre et date de sortie | N'utiliser que `dc:date` pour la publication ; compter les livres qui n'en ont pas | C3 validité |
| Omnibus : un fichier contient plusieurs œuvres (ex. Eisenhorn Omnibus : Xenos, Malleus, Hereticus et deux nouvelles) | Le décompte « 37 livres » et la jointure avec KOReader ne parlent pas de la même unité | Découper à partir de la description de l'OPF ou de la table des matières ; décider l'unité (fichier ou œuvre) | C6, C7 grain |
| Série lue seulement dans `calibre:series` (EPUB 2) | Un EPUB 3 sans Calibre aura une série vide | Lire aussi `belongs-to-collection` et `group-position` ; vérifier combien de livres sont concernés | C3 complétude des valeurs |
| Fichiers `.kepub.epub` (format Kobo) | Métadonnées possiblement retouchées par Kobo | Comparer avec la copie locale en `.epub` sur quelques livres | C2 fiabilité de la source |
| KOReader ne connaît que les livres ouverts | Un livre possédé mais jamais ouvert est absent des statistiques | Comparer à la liste des EPUB, qui fait référence | C3 complétude de la population |
| Titre comme clé de jointure entre KOReader, EPUB et wiki | Rapprochements manqués ou faux | Mesurer les correspondances exactes au profilage ; essayer l'ISBN (`dc:identifier`, `scheme="ISBN"`) | C6 |
| `page_stat` non chargée (c'est une vue) ; `sqlite_sequence` chargée (table interne SQLite) | Raw ne reflète pas exactement la base KOReader | Documenter ; écarter `sqlite_sequence` en staging | C5 |
| Base Vocabulary Builder non chargée | Le vocabulaire relevé pendant la lecture n'est pas exploité | Issue à créer si une question en a besoin | C2 |
| Règle V1 : toute mention compte comme une apparition ; les pronoms sont ignorés | Surestime les rencontres (simple citation), sous-estime les scènes où le personnage est désigné par un pronom | Affiner en V2 (mention ou rencontre) | C7 grain |
| Homonymes (ex. « Blank » : nom commun et terme de l'univers) | Fausses apparitions | Table d'alias et règles de désambiguïsation | C6 |
| Couverture des wikis | Les personnages et lieux absents des wikis ne sont jamais reconnus | Mesurer la part de candidats sans correspondance ; recherche en ligne en V2 | C3, C6 |
| Ni le nom de fichier ni le `dc:title` ne sont fiables seuls (issue #8 : 19 écarts en comparaison exacte, 4 après normalisation) | Forme : article « , The » en fin de nom, « _ » à la place de « : » ou « ' », apostrophe typographique, casse. Fond : titres faux dans les métadonnées (« Warhammer 40,000 » pour The Alien Beast Within, auteur collé au titre) | Macro `normalize_title` appliquée aux deux côtés (apostrophe typographique, « _s » → « 's », «_ » → « : », « , The » ramené en tête, minuscules) : clé de comparaison uniquement, le titre affiché reste celui d'origine. Restent 4 titres faux (Pariah, Old Soldiers Never Die, The Alien Beast Within, Choose Your Enemies) → seed de correspondance tenu à la main | C3 exactitude, C6 |
| Dates bidon dans `dc:date` (`0101-01-01`) | Une date par défaut passe pour une vraie date de publication | Convertir en NULL en staging (règle : année avant la première parution Black Library = date invalide) | C3 validité |
| Séries inexploitables ou suspectes dans `calibre:series` | Valeurs techniques (« Warhammer.Grey Knights.Warhammer.99..ICBP », index 99), plage au lieu d'un nom (« Ultramarines #4-6 »), rattachements à vérifier (The Alien Beast Within en Ultramarines 11, Pariah en Eisenhorn 4) | Même seed de correspondance que les titres ; index 99 traité comme inconnu | C3 validité, C6 |
| Correspondance exacte : titres de page avec précision entre parenthèses (« Blank (Psyker) ») | Le titre n'apparaît jamais tel quel dans le texte : personnage jamais trouvé | Retirer la partie entre parenthèses avant la recherche | C6 |
| Correspondance exacte : nom complet en titre, nom court dans le texte (« Ciaphas Cain » / « Cain ») | Apparitions sous-estimées | Chercher aussi les redirections du wiki (alias), déjà extraites dans l'issue #5 | C3 complétude, C6 |
| Correspondance exacte : titres qui sont aussi des mots courants (« Blank », « Emperor », « Warp ») | Fausses apparitions | Liste d'exclusion ou exigence de majuscule ; mesurer les cas les plus fréquents | C3 exactitude, C6 |
| Correspondance exacte : variantes de forme (possessif « Cain's », majuscule en début de phrase, coupure de ligne au milieu d'un nom dans le HTML) | Apparitions manquées | Normaliser les espaces du texte extrait ; chercher le nom en début de mot, possessif accepté | C3 complétude |
| Les catégories du wiki contiennent aussi des listes, des pages de faction ou de concept ; une même page peut se trouver dans plusieurs branches (type ambigu) | Le lexique contient des entrées hors périmètre, ou une entité avec deux types | Filtrer (pages « List of », sous-catégories hors périmètre) ; règle de priorité entre types en cas de conflit ; mesurer la part d'entrées écartées | C2, C3 validité |

## Dette technique

- [ ] Les scripts se terminent avec le code 0 même en cas d'erreur (dossier non configuré, liseuse non branchée) : `make extract` et la CI croiront que tout s'est bien passé.
- [ ] Pas de vérification d'existence du dossier : liseuse débranchée = zéro livre, sans erreur.
- [ ] `LOG_LEVEL` est dans le `.env` mais n'est pas lu par les scripts.
- [ ] L'extraction EPUB dépend de la liseuse branchée ; la copie locale n'est pas encore utilisable comme référence.
- [ ] Idempotence du chargement KOReader non testée automatiquement (seulement à la main).
- [ ] Extension DuckDB de VS Code (`chuckjonas.duckdb 0.0.27`) : erreur Catalog `"home" does not exist` à l'ouverture du fichier ; contourné avec `duckdb -ui`.
- [ ] Les requêtes sont écrites dans l'interface DuckDB (brouillon) puis exportées à la main vers `analyses/` (le fichier versionné fait foi). Règle : dès qu'une requête convient, on exporte et on commit. Si l'export devient fréquent, l'ajouter au Makefile (`make export-notebook NAME=...`) avec la commande `duckdb -json` + `jq` qui ajoute les `;` manquants.
- [ ] Pas de test automatique de l'extraction EPUB (faux EPUB construit dans `tmp_path`), prévu dans l'issue #8 mais hors critères de fin.
