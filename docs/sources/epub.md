# Fiche d'identité - Fichiers EPUB de ma bibliothèque Warhammer 40k

> **Métadonnées de la fiche**
> - Rédacteur : Marine Prost
> - Date de création / dernière mise à jour : 28/10/2026
> - Version : 2
> - Statut : brouillon
> - Questions servies : 1 à 4 (`docs/questions.md`). Métadonnées : « identité du livre », « série et rang », « livres possédés ». Texte : « présence de l'entité dans un livre »
> - Décision : retenue (référence pour la liste des livres possédés, et seule source du texte)

## 1. Identité
| Champ | Valeur | Vérification |
|---|---|---|
| Nom | Fichiers EPUB du dossier Warhammer 40k | |
| Identifiant unique | Chemin du fichier relatif à `EREADER_ROOT` | `book_list.py`, 26/10/2026 |
| Type de source | Fichiers (archives EPUB) | |
| URL ou emplacement | Dossier `W40K_FOLDER` sur la liseuse (dans `.env`) | Décision du 27/10/2026 |
| Description (1–2 phrases) | Romans, nouvelles et omnibus Warhammer 40k de ma collection personnelle, en `.epub` et `.kepub.epub` | |
| Domaine métier | Littérature (Black Library) | |
| Langue(s) | Anglais | Métadonnées `dc:language` |

## 2. Accès et format
| Champ | Valeur | Vérification |
|---|---|---|
| Système / plateforme | Fichiers gérés en partie par Calibre (métadonnées `calibre:*`), en partie retouchés par Sigil | Métadonnées, 26/10/2026 |
| Format natif | Archive ZIP : `META-INF/container.xml`, fichier OPF (métadonnées, manifeste, ordre de lecture), chapitres en XHTML | |
| Points d'accès disponibles | Fichiers sur la liseuse ; une copie locale existe aussi | |
| Authentification | Aucune | |
| Robots.txt | Sans objet (fichiers locaux) | |
| Conditions d'utilisation | Sans objet pour l'accès ; textes sous droits de l'éditeur (voir §8) | |
| Conditions d'accès automatisé (synthèse) | Sans objet (fichiers locaux) | |
| Mode d'accès retenu | Lecture des archives en place, sans les modifier. Métadonnées : `extract/book_list.py`. Texte : extraction à écrire (issue dédiée) | |
| Emplacement de la copie locale | `data/raw/epub_metadata.jsonl` (métadonnées) ; texte extrait à venir dans `data/raw/` | |

## 3. Structure et clés
| Champ | Valeur | Vérification |
|---|---|---|
| Grain | Métadonnées : une ligne par balise OPF (format long). Livre (unité de la v0.1) : un fichier | Décision du 27/10/2026 |
| Objets ou tables utiles | Bloc `<metadata>` de l'OPF (Dublin Core et `<meta>`) ; chapitres XHTML pour le texte ; ordre de lecture (`spine`) | |
| Clés disponibles | Chemin du fichier (unique dans le dossier). `dc:identifier` multiples, distingués par l'attribut `scheme` : `uuid`, `calibre`, `ISBN`, `GOOGLE`. ISBN présent dans 17 fichiers sur 46 | Profilage, 26/10/2026 |
| Clé de jointure avec les autres sources | Titre normalisé (`normalize_title`) avec KOReader ; seed de correspondance pour les titres faux | Issue #8, 27/10/2026 |
| Fuseau horaire / unités / encodage | Dates en UTC, décalées d'un fuseau (`2004-12-02T23:00:00+00:00` pour un 3 décembre probable) | Profilage, 26/10/2026 |
| Dictionnaire ou documentation | Spécifications EPUB 2 et EPUB 3 ; vocabulaire Dublin Core | |

## 4. Provenance et propriété
| Champ | Valeur | Vérification |
|---|---|---|
| Système producteur | Éditeur (Black Library), puis retouches : Calibre, Sigil, conversion Kobo (`.kepub.epub`), renommages à la main | Métadonnées, 26/10/2026 |
| Processus de saisie | Métadonnées saisies par l'éditeur puis modifiées à la main ou par les outils, sans règle constante | |
| Date de création de la source | Sans objet (collection constituée au fil du temps) | |
| Propriétaire (data owner) | Moi pour les fichiers ; les textes restent sous droits de l'éditeur | |
| Responsable côté projet (data steward) | Marine Prost | |
| Contact | Sans objet | |

## 5. Volumétrie et fraîcheur
| Champ | Valeur | Vérification |
|---|---|---|
| Volumétrie | 46 fichiers, 998 lignes de métadonnées (21,7 balises par fichier en moyenne) | Extraction et vérification depuis un clone propre, 27/10/2026 |
| Profondeur d'historique | Sans objet | |
| Fréquence de mise à jour de la source | À chaque ajout de livre | |
| Fraîcheur mesurable | Date de modification des fichiers ; `dcterms:modified` dans les EPUB 3 | |
| Fréquence de rafraîchissement dans le projet | À la demande | |
| Activité / maintenance | La bibliothèque grandit (37 livres au départ, 46 fichiers au 26/10/2026) | |

## 6. Couverture
| Champ | Valeur | Vérification |
|---|---|---|
| Population couverte | Les fichiers du dossier `W40K_FOLDER` uniquement : un livre rangé ailleurs est manqué | Biais connu |
| Période couverte | Sans objet | |
| Champs utiles et leur taux de remplissage | `title`, `creator`, `date`, `identifier` : 46 / 46. `calibre:series` : 36 ; `belongs-to-collection` (EPUB 3) : 3. `publisher`, `description` : 36. `subject` : 35 | Profilage, 26/10/2026 |
| Couverture mesurée sur le besoin du projet | Texte : à mesurer à l'extraction (chapitres lisibles, ordre de lecture) | |

## 7. Qualité
| Dimension | Constat | Vérification |
|---|---|---|
| Complétude des valeurs | Balises présentes mais vides (`source`, `relation`, `coverage`) ; 7 fichiers sans série | Profilage, 26/10/2026 |
| Complétude de la population | Dépend du rangement dans le dossier | Biais connu |
| Exactitude | 4 titres faux dans les métadonnées (« Warhammer 40,000 » pour *The Alien Beast Within*…) ; dates bidon `0101-01-01` ; dates décalées d'un fuseau ; `calibre:timestamp` (date d'ajout) à ne pas confondre avec la date de publication | Issue #8, 27/10/2026 |
| Cohérence | Nom de fichier et `dc:title` : 19 écarts en comparaison exacte, 4 après normalisation | Issue #8, 27/10/2026 |
| Unicité | Doublons (*Old Soldiers Never Die*, *The Alien Beast Within*) ; omnibus dont les parties existent aussi en fichiers séparés (*Eisenhorn Omnibus*) | Issue #8, 27/10/2026 |
| Validité | Valeurs de série inexploitables (« Warhammer.Grey Knights.Warhammer.99..ICBP », index 99 ; « Ultramarines #4-6 ») | Profilage, 27/10/2026 |
| Actualité | Sans objet | |
| Risques connus | Deux formats (EPUB 2 et 3, `.epub` et `.kepub.epub`) ; le texte d'un omnibus mélange plusieurs œuvres | |

## 8. Gouvernance et conformité
| Champ | Valeur | Vérification |
|---|---|---|
| Données personnelles présentes dans la source | Aucune dans le contenu ; la liste des fichiers révèle ma bibliothèque | |
| Données personnelles collectées par le projet | Aucune (chemins relatifs, sans nom d'utilisateur ni point de montage) | Décision du 26/10/2026 |
| Base légale et finalité (si données personnelles) | Sans objet | |
| Minimisation appliquée | Images et feuilles de style non extraites | |
| Licence | Textes sous droits (Black Library / Games Workshop) ; usage personnel de livres achetés | |
| Restrictions d'usage | **Aucun fichier, aucun extrait de texte dans le dépôt.** Tests sur un faux EPUB construit dans `tmp_path` | `.gitignore`, hook `no-personal-data` |
| Attribution à faire | Mention Games Workshop dans le README | |
| Durée de conservation | Texte extrait conservé dans `data/` tant que le projet existe ; régénérable | |
| Redistribution | Aucune | |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | Éditeur (Black Library) ; outils de gestion (Calibre, Sigil, Kobo) |
| Extraction | Métadonnées : `extract/book_list.py` (OPF → JSONL → `CREATE OR REPLACE`). Texte : script à écrire |
| Tables raw | `raw.epub_metadata` (format long) ; table du texte à venir |
| Transformations prévues | Pivot en une ligne par fichier ; normalisation des titres ; dates bidon en NULL et correction du fuseau ; série EPUB 3 ; seed de correspondance (titres faux, doublons, omnibus) |
| Destinations aval | `dim_book` ; correspondance exacte des noms d'entités dans le texte ; `fact_entity_appearance` |

## 10. Décisions et questions ouvertes
| Date | Décision ou question | Statut |
|---|---|---|
| 26/10/2026 | Métadonnées en format long en raw | Décidé |
| 26/10/2026 | Périmètre = dossier `W40K_FOLDER` uniquement | Décidé (biais connu) |
| 27/10/2026 | Unité de comptage v0.1 : le fichier | Décidé |
| 27/10/2026 | Doublons et omnibus : marqués dans un seed, jamais supprimés | Décidé |
| 27/10/2026 | Source du titre de référence : titre normalisé + seed pour les cas faux | Ouvert |
| 28/10/2026 | Les seeds qui citent des fichiers (`book_mapping`, `coverage_check`) restent en local (`data/seeds/`) : la liste des fichiers révèle ma bibliothèque. Clé = chemin relatif, sans hachage | Décidé |

## Historique de la fiche
| Version | Date | Modification |
|---|---|---|
| 1 | 28/10/2026 | Création |
| 2 | 28/10/2026 | Seeds qui citent des fichiers gardés en local ; lignes Robots.txt et Conditions d'utilisation du modèle |
