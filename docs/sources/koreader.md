# Fiche d'identité - Statistiques de lecture KOReader

> **Métadonnées de la fiche**
> - Rédacteur : Marine Prost
> - Date de création / dernière mise à jour : 28/10/2026
> - Version : 1
> - Statut : brouillon
> - Questions servies : 1 à 3 (`docs/questions.md`), pour les éléments « livre fini, date de fin » et « ordre de lecture » ; 5 en V2 (position de lecture)
> - Décision : retenue (source de référence pour ce qui a été lu, et quand)

## 1. Identité
| Champ | Valeur | Vérification |
|---|---|---|
| Nom | Base de statistiques de lecture KOReader | |
| Identifiant unique | `statistics.sqlite3` | Fichier sur la liseuse, 23/10/2026 |
| Type de source | Base opérationnelle locale (SQLite), produite par une application | |
| URL ou emplacement | Sur la Kobo : `.adds/koreader/settings/statistics.sqlite3` (chemin dans `.env` : `KOREADER_SETTINGS_DIR`) | Script `copy_database.py`, 23/10/2026 |
| Description (1–2 phrases) | Base tenue par le module de statistiques de KOReader : livres ouverts, et temps passé sur chaque page à chaque session | |
| Domaine métier | Lecture personnelle | |
| Langue(s) | Sans objet (données techniques ; titres dans la langue du livre) | |

## 2. Accès et format
| Champ | Valeur | Vérification |
|---|---|---|
| Système / plateforme | KOReader sur liseuse Kobo ; SQLite | |
| Format natif | Tables SQLite | |
| Points d'accès disponibles | Fichier sur la liseuse, lisible quand elle est branchée en USB | |
| Authentification | Aucune | |
| Conditions d'accès automatisé | Sans objet (fichier local). Ne jamais écrire dans le fichier de la liseuse | |
| Mode d'accès retenu | Copie par l'API de sauvegarde SQLite, source ouverte en lecture seule (`mode=ro`), puis chargement dans DuckDB | `copy_database.py`, 23/10/2026 |
| Emplacement de la copie locale | `data/raw/koreader_db.sqlite3` ; tables chargées dans `warehouse.raw` | |

## 3. Structure et clés
| Champ | Valeur | Vérification |
|---|---|---|
| Grain | `book` : un livre ouvert dans KOReader. `page_stat_data` : une page lue pendant une session | Chargement du 23/10/2026 |
| Objets ou tables utiles | `book`, `page_stat_data`. `page_stat` est une vue (non chargée), `numbers` une table utilitaire, `sqlite_sequence` une table interne de SQLite | Chargement du 23/10/2026 |
| Clés disponibles | `book.id` (clé technique locale, stable tant que la base n'est pas réinitialisée) ; `page_stat_data.id_book` renvoie à `book.id`. Une empreinte du fichier (`md5`) est probablement présente dans `book` : à vérifier | |
| Clé de jointure avec les autres sources | Le titre, avec l'EPUB : fiabilité à mesurer après normalisation (issue #3). L'empreinte `md5`, si elle existe, serait plus fiable | À mesurer |
| Fuseau horaire / unités / encodage | Horodatages en secondes Unix (à convertir) ; durées en secondes | À vérifier au profilage |
| Dictionnaire ou documentation | Pas de dictionnaire officiel identifié ; schéma lu directement dans la base | |

## 4. Provenance et propriété
| Champ | Valeur | Vérification |
|---|---|---|
| Système producteur | Module de statistiques de KOReader, activé sur ma liseuse | Confirmé (Questions ouvertes, étape 1) |
| Processus de saisie | Automatique : enregistré à chaque changement de page. Les sessions sur une autre liseuse ou une autre application ne sont pas enregistrées | |
| Date de création de la source | 2025-12-27 13:04:39 | Chargement au 28/10/26 |
| Propriétaire (data owner) | Marine Prost | |
| Responsable côté projet (data steward) | Marine Prost | |
| Contact | Sans objet | |

## 5. Volumétrie et fraîcheur
| Champ | Valeur | Vérification |
|---|---|---|
| Volumétrie | `book` : 56 lignes ; `page_stat_data` : 5 853 lignes ; `numbers` : 1 000 ; `sqlite_sequence` : 1. Fichier de 372 736 octets | Chargement du 23/10/2026 |
| Profondeur d'historique | Depuis l'activation des statistiques | À mesurer (issue #3) |
| Fréquence de mise à jour de la source | À chaque séance de lecture | |
| Fraîcheur mesurable | Horodatage de début de chaque page lue | |
| Fréquence de rafraîchissement dans le projet | À la demande, liseuse branchée (`copy_database.py`) | |
| Activité / maintenance | Source vivante tant que je lis avec KOReader | |

## 6. Couverture
| Champ | Valeur | Vérification |
|---|---|---|
| Population couverte | Les livres **ouverts** dans KOReader, Warhammer ou non. Un livre possédé mais jamais ouvert est absent | |
| Période couverte | du 2025-12-27 à aujourd'hui 2026-10-26 | Mesure au 28/0/2026 | |
| Champs utiles et leur taux de remplissage | À mesurer (issue #3) | |
| Couverture mesurée sur le besoin du projet | Livres Warhammer présents par rapport à la liste des EPUB : à mesurer (issue #3) | |

## 7. Qualité
| Dimension | Constat | Vérification |
|---|---|---|
| Complétude des valeurs | À mesurer | |
| Complétude de la population | Partielle par construction : seuls les livres ouverts | |
| Exactitude | **« Livre fini » n'est pas une donnée de cette base** : il faut le déduire (pages lues / pages totales) ou le lire ailleurs (statut dans les métadonnées `.sdr`). Règle à décider | Point ouvert |
| Cohérence | Le nombre de pages dépend de la mise en page : il change si la police ou la taille change | Constat de l'étape 1 |
| Unicité | Un même livre peut apparaître deux fois s'il existe en deux fichiers | À mesurer |
| Validité | À mesurer (durées nulles ou très longues, dates impossibles) | |
| Actualité | Fraîche au moment de la copie | |
| Risques connus | Base réinitialisée si KOReader est réinstallé ; écriture accidentelle sur la liseuse (incident évité le 23/10/2026) | |

## 8. Gouvernance et conformité
| Champ | Valeur | Vérification |
|---|---|---|
| Données personnelles présentes dans la source | Oui : mes habitudes de lecture (titres, horaires, durées) | |
| Données personnelles collectées par le projet | Les mêmes, pour mon seul usage | |
| Base légale et finalité (si données personnelles) | Usage strictement personnel, sur mes propres données | |
| Minimisation appliquée | Seules les tables utiles aux questions sont utilisées ; les notes et surlignages (`.sdr`) ne sont pas collectés en v0.1 | |
| Licence | Sans objet (données personnelles) | |
| Restrictions d'usage | Jamais commitées ; la CI et les tests utilisent une base fabriquée à la main | `.gitignore`, hook `no-personal-data` |
| Attribution à faire | Sans objet | |
| Durée de conservation | Tant que le projet existe ; régénérable depuis la liseuse | |
| Redistribution | Aucune | |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | Mes sessions de lecture sur la liseuse |
| Extraction | `extract/copy_database.py` : copie en lecture seule, puis `CREATE OR REPLACE` de chaque table dans `warehouse.raw` |
| Tables raw | `raw.book`, `raw.page_stat_data`, `raw.numbers`, `raw.sqlite_sequence` |
| Transformations prévues | Staging : typage, conversion des horodatages, écart de `numbers` et `sqlite_sequence`, règle « livre fini », date de fin par livre |
| Destinations aval | `dim_book` (statut de lecture, date de fin), ordre de lecture, vue « entités débloquées » |

## 10. Décisions et questions ouvertes
| Date | Décision ou question | Statut |
|---|---|---|
| 23/10/2026 | Copier par l'API de sauvegarde SQLite avant de charger ; la liseuse n'est ouverte qu'en lecture seule | Décidé |
| 27/10/2026 | La liseuse est la source de référence, lue une seule fois par extraction | Décidé |
| 28/10/2026 | Comment définir « livre fini » : seuil de pages lues, ou statut des métadonnées `.sdr` ? | Ouvert |
| 28/10/2026 | Le README annonce une couche raw « tout en texte », mais `copy_database.py` ne lit pas encore les colonnes en texte | À corriger |

## Historique de la fiche
| Version | Date | Modification |
|---|---|---|
| 1 | 28/10/2026 | Création |
