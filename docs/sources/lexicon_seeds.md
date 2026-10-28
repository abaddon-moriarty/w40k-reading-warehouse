# Fiche d'identité - Seeds du lexique d'entités

> **Métadonnées de la fiche**
> - Rédacteur : Marine Prost
> - Date de création / dernière mise à jour : 28/10/2026
> - Version : 3
> - Statut : brouillon (sources prévues, pas encore créées)
> - Questions servies : 1 à 4 (`docs/questions.md`), pour les éléments « nom cherché », « type de l'entité » et « couverture »
> - Décision : retenue : chaque correction du lexique est une règle explicite, tenue à la main, jamais une modification à la main des données

Une seule fiche pour cinq petites tables tenues à la main, parce qu'elles ont le même producteur, le même processus et les mêmes risques. Elles complètent les exports manuels de wiki.gg (`wiki_gg.md`). Elles restent en local : le dépôt ne contient que leur description et leurs tests.

## 1. Identité
| Champ | Valeur | Vérification |
|---|---|---|
| Nom | Seeds du lexique d'entités | |
| Identifiant unique | `wiki_exports`, `category_type_map`, `entity_alias`, `lexicon_exclusions`, `coverage_check` | |
| Type de source | Saisie manuelle (fichiers CSV locaux, chargés comme seeds dbt) | |
| URL ou emplacement | `data/seeds/` (local, ignoré par Git), déclaré dans `seed-paths` du projet dbt. Le dépôt contient seulement la description YAML, les tests et des exemples inventés pour la CI | Décision du 28/10/2026 |
| Description (1–2 phrases) | Tables tenues à la main qui journalisent les exports du wiki, attribuent un type aux entités, ajoutent les noms courts, excluent les formes trompeuses et listent les entités attendues par livre | |
| Domaine métier | Référentiel d'entités | |
| Langue(s) | Anglais (noms des entités et des catégories) | |

## 2. Accès et format
| Champ | Valeur | Vérification |
|---|---|---|
| Système / plateforme | Fichiers CSV locaux, chargés par `dbt seed` | |
| Format natif | CSV, UTF-8 | |
| Points d'accès disponibles | Le dossier local `data/seeds/` | |
| Authentification | Aucune | |
| Robots.txt | Sans objet | |
| Conditions d'utilisation | Sans objet (saisie personnelle). Les noms d'entités et de catégories viennent de wiki.gg : voir la licence en §8 | |
| Conditions d'accès automatisé (synthèse) | Sans objet | |
| Mode d'accès retenu | `dbt seed` | |
| Emplacement de la copie locale | Les fichiers eux-mêmes ; historique dans un dépôt Git local propre à `data/seeds/`, jamais poussé (proposé, voir §10) | |

## 3. Structure et clés
| Seed | Grain | Colonnes prévues | Clé |
|---|---|---|---|
| `wiki_exports` | Un export manuel | `export_file`, `category`, `export_date`, `page_count`, `trigger_book`, `note` | `export_file` |
| `category_type_map` | Une catégorie wiki qui donne un type | `category`, `entity_type`, `priority` | `category` |
| `entity_alias` | Un nom court ou une variante d'une entité | `page_title`, `alias`, `source` (`manual` en v0.1, `redirect` en V1/V2), `note` | (`page_title`, `alias`) |
| `lexicon_exclusions` | Une forme à ne pas chercher | `form`, `reason` (`work`, `common_word`, `out_of_scope`), `evidence`, `note` | `form` |
| `coverage_check` | Une entité attendue dans un livre | `file`, `page_title` | (`file`, `page_title`) |

| Champ | Valeur | Vérification |
|---|---|---|
| Clé de jointure avec les autres sources | `page_title` et `category` avec les tables raw du wiki ; `file` avec `raw.epub_metadata` | |
| Fuseau horaire / unités / encodage | Dates au format ISO (`AAAA-MM-JJ`) ; UTF-8 | |
| Dictionnaire ou documentation | Description des colonnes dans le YAML dbt des seeds | |

## 4. Provenance et propriété
| Champ | Valeur | Vérification |
|---|---|---|
| Système producteur | Moi, à partir des exports, du profilage du lexique et de mes lectures | |
| Processus de saisie | À la main. `wiki_exports` : une ligne à chaque export. `category_type_map` : une ligne par catégorie rencontrée dans les exports. `entity_alias` et `coverage_check` : à la lecture d'un livre. `lexicon_exclusions` : après la mesure des formes ambiguës. **Source d'erreur humaine** : faute de frappe dans un titre, oubli, jugement subjectif sur un type | |
| Date de création de la source | Prévue avec l'initialisation de dbt (milestone 5) | |
| Propriétaire (data owner) | Moi | |
| Responsable côté projet (data steward) | Marine Prost | |
| Contact | Sans objet | |

## 5. Volumétrie et fraîcheur
| Champ | Valeur | Vérification |
|---|---|---|
| Volumétrie | Attendue pour *Eisenhorn* : 2 exports, quelques dizaines de catégories, quelques dizaines d'alias, une quinzaine d'exclusions (dont les 12 œuvres de la catégorie de série), 5 entités attendues par livre | Catégorie *Eisenhorn*, 28/10/2026 |
| Profondeur d'historique | Celle du dépôt Git local de `data/seeds/` (proposé) ; la colonne `note` garde la raison de chaque ligne | |
| Fréquence de mise à jour de la source | À chaque nouvel export, nouveau livre lu ou nouvelle mesure | |
| Fraîcheur mesurable | `export_date` ; date de modification des fichiers | |
| Fréquence de rafraîchissement dans le projet | À chaque `dbt seed` | |
| Activité / maintenance | Dépend de moi : risque d'oubli | |

## 6. Couverture
| Champ | Valeur | Vérification |
|---|---|---|
| Population couverte | Les séries déjà exportées ; les livres déjà lus pour les alias et les entités attendues | |
| Période couverte | Sans objet | |
| Champs utiles et leur taux de remplissage | `note` et `evidence` facultatifs ; les autres obligatoires (test `not_null`) | |
| Couverture mesurée sur le besoin du projet | `coverage_check` : part des entités attendues effectivement trouvées dans chaque livre | À mesurer |

## 7. Qualité
| Dimension | Constat | Vérification |
|---|---|---|
| Complétude des valeurs | Contrôlée par des tests `not_null` | Tests prévus |
| Complétude de la population | Une catégorie absente de `category_type_map` laisse des entités sans type : test qui liste les pages sans type | Test prévu |
| Exactitude | Dépend de la vérification à la main | |
| Cohérence | `entity_alias.page_title` et `coverage_check.page_title` doivent exister dans le lexique ; `coverage_check.file` dans `raw.epub_metadata` | Tests `relationships` prévus |
| Unicité | Clés uniques ; un même alias ne doit pas pointer vers deux entités (sinon ambiguïté, à résoudre) | Tests prévus |
| Validité | `entity_type` et `reason` dans une liste fermée | Tests `accepted_values` prévus |
| Actualité | À revoir à chaque nouvel export ou livre | |
| Risques connus | Titre de page renommé sur le wiki, qui rend une ligne orpheline ; alias trop court, qui crée des fausses apparitions | |

## 8. Gouvernance et conformité
| Champ | Valeur | Vérification |
|---|---|---|
| Données personnelles présentes dans la source | Aucune | |
| Données personnelles collectées par le projet | `coverage_check.file` révèle une partie de ma bibliothèque : c'est une raison de plus de garder les seeds en local. Un hachage du titre ou du chemin ne l'anonymiserait pas (pseudonymisation : quelques centaines de titres Warhammer suffisent à retrouver chaque empreinte) | |
| Base légale et finalité (si données personnelles) | Sans objet | |
| Minimisation appliquée | Noms seulement, aucun texte d'article ni de livre | |
| Licence | Fichiers non publiés. Les noms d'entités et de catégories viennent de wiki.gg (CC BY-NC 4.0) ; la description YAML et les exemples inventés du dépôt sont sous MIT | |
| Restrictions d'usage | Pas d'usage commercial (CC BY-NC) ; collecte en risque assumé (`wiki_gg.md`, §10) | |
| Attribution à faire | Celle de wiki.gg dans le README, si un jour les seeds sont publiés | |
| Durée de conservation | Tant que le projet existe | |
| Redistribution | Aucune : seeds locaux. Seuls la structure, les tests et des exemples inventés sont publiés | Décision du 28/10/2026 |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | Exports manuels de wiki.gg ; profilage du lexique ; mes lectures |
| Extraction | Aucune : saisie directe |
| Tables raw | Seeds dbt (lus dans `data/seeds/`) `wiki_exports`, `category_type_map`, `entity_alias`, `lexicon_exclusions`, `coverage_check` |
| Transformations prévues | `stg_wiki_pages` (type et exclusions) ; `int_entity_lexicon` (titres nettoyés et alias, une ligne par forme cherchée) ; test de couverture sur les apparitions |
| Destinations aval | `int_entity_lexicon`, `dim_entity`, tests de couverture |

## 10. Décisions et questions ouvertes
| Date | Décision ou question | Statut |
|---|---|---|
| 28/10/2026 | Aucune correction à la main dans les données : chaque règle est une ligne de seed ou du code | Décidé |
| 28/10/2026 | Seeds gardés en local (`data/seeds/`), car tirés d'une collecte en risque assumé et révélant ma bibliothèque. Clé des livres : chemin relatif, comme `raw.epub_metadata` ; pas de hachage (pseudonymisation sans bénéfice, puisque rien n'est publié). Aucune exception au hook `no-ereader-paths` | Décidé |
| 28/10/2026 | Conséquence des seeds locaux : hors du dépôt, on ne sait plus quand ni pourquoi une ligne a changé, alors que le README promet des corrections « explicit and replayable ». Proposé : un dépôt Git local dans `data/seeds/` (`git init`, aucun remote, jamais poussé ; `data/` est déjà ignoré par le dépôt principal), un commit par lot de corrections ; à défaut, une sauvegarde datée du dossier | À valider |
| 28/10/2026 | Exemples inventés (`dbt/seeds_example/`) pour la CI et les tests, avec des noms et des chemins fictifs | À faire |
| 28/10/2026 | Les formes trompeuses sont exclues sur mesure (nombre de livres, apparitions en minuscule), pas à l'œil | Décidé |
| 28/10/2026 | Groupes et organisations : sixième type ou exclusion ? | Ouverte |

## Historique de la fiche
| Version | Date | Modification |
|---|---|---|
| 1 | 28/10/2026 | Création (sources prévues) |
| 2 | 28/10/2026 | Seeds en local, pas de publication, pas de hachage |
| 3 | 28/10/2026 | « Règle explicite » au lieu de « règle versionnée » ; historique par un dépôt Git local proposé |
