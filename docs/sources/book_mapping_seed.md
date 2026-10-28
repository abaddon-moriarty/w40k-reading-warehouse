# Fiche d'identité - Seed de correspondance des livres

> **Métadonnées de la fiche**
> - Rédacteur : Marine Prost
> - Date de création / dernière mise à jour : 28/10/2026
> - Version : 3
> - Statut : brouillon (source prévue, pas encore créée)
> - Questions servies : 1 à 4 (`docs/questions.md`), pour l'élément « identité du livre »
> - Décision : retenue : corrige ce que la normalisation automatique des titres ne peut pas corriger

## 1. Identité
| Champ | Valeur | Vérification |
|---|---|---|
| Nom | Seed de correspondance des livres | |
| Identifiant unique | `book_mapping` | |
| Type de source | Saisie manuelle (fichier CSV local, chargé comme seed dbt) | |
| URL ou emplacement | `data/seeds/book_mapping.csv` (prévu, local, ignoré par Git) | Décision du 28/10/2026 |
| Description (1–2 phrases) | Table tenue à la main qui, pour chaque fichier EPUB à corriger, donne le titre de référence et signale les doublons et les parties d'omnibus | |
| Domaine métier | Référentiel de livres | |
| Langue(s) | Anglais (titres) | |

## 2. Accès et format
| Champ | Valeur | Vérification |
|---|---|---|
| Système / plateforme | Fichier CSV local, chargé par `dbt seed` | |
| Format natif | CSV | |
| Points d'accès disponibles | Le dossier local `data/seeds/` | |
| Authentification | Aucune | |
| Robots.txt | Sans objet (fichier local) | |
| Conditions d'utilisation | Sans objet (saisie personnelle) | |
| Conditions d'accès automatisé (synthèse) | Sans objet | |
| Mode d'accès retenu | `dbt seed` | |
| Emplacement de la copie locale | Le fichier lui-même, sauvegardé hors du dépôt | |

## 3. Structure et clés
| Champ | Valeur | Vérification |
|---|---|---|
| Grain | Un fichier EPUB qui demande une correction | |
| Objets ou tables utiles | Colonnes prévues : `file`, `canonical_title`, `duplicate_of`, `part_of`, `note` | Décision du 27/10/2026 |
| Clés disponibles | `file` (chemin relatif à `EREADER_ROOT`), unique | |
| Clé de jointure avec les autres sources | `file`, identique à celle de `raw.epub_metadata` | |
| Fuseau horaire / unités / encodage | UTF-8 | |
| Dictionnaire ou documentation | Description des colonnes dans le YAML dbt du seed | |

## 4. Provenance et propriété
| Champ | Valeur | Vérification |
|---|---|---|
| Système producteur | Moi, à partir des constats du profilage | |
| Processus de saisie | À la main, après contrôle du livre (couverture, page de titre, page wiki du roman). **Source d'erreur humaine** : faute de frappe, chemin mal recopié, oubli après l'ajout d'un livre | |
| Date de création de la source | Prévue au milestone 6 (Consolidation) | |
| Propriétaire (data owner) | Moi | |
| Responsable côté projet (data steward) | Marine Prost | |
| Contact | Sans objet | |

## 5. Volumétrie et fraîcheur
| Champ | Valeur | Vérification |
|---|---|---|
| Volumétrie | Attendue au départ : les 4 titres faux, 2 doublons, les parties de *Eisenhorn Omnibus* (environ 10 lignes) | Issue #8, 27/10/2026 |
| Profondeur d'historique | Celle du dépôt Git local de `data/seeds/` (proposé, voir `lexicon_seeds.md`) ; colonne `note` | |
| Fréquence de mise à jour de la source | À chaque nouveau cas trouvé, ou à l'ajout d'un livre | |
| Fraîcheur mesurable | Date de modification du fichier | |
| Fréquence de rafraîchissement dans le projet | À chaque `dbt seed` | |
| Activité / maintenance | Dépend de moi : risque d'oubli | |

## 6. Couverture
| Champ | Valeur | Vérification |
|---|---|---|
| Population couverte | Uniquement les fichiers à corriger, pas toute la bibliothèque | |
| Période couverte | Sans objet | |
| Champs utiles et leur taux de remplissage | `canonical_title` rempli pour les titres faux ; `duplicate_of` et `part_of` seulement quand ils s'appliquent | |
| Couverture mesurée sur le besoin du projet | Après application : nombre de titres qui diffèrent encore entre KOReader, EPUB et le wiki (objectif : 0 écart non expliqué) | À mesurer |

## 7. Qualité
| Dimension | Constat | Vérification |
|---|---|---|
| Complétude des valeurs | À contrôler par un test dbt | |
| Complétude de la population | Un cas oublié reste un écart silencieux : à détecter par un test sur les titres non rapprochés | |
| Exactitude | Dépend de la vérification à la main | |
| Cohérence | `duplicate_of` et `part_of` doivent pointer vers un fichier existant | Test `relationships` prévu |
| Unicité | `file` unique | Test `unique` prévu |
| Validité | Chemins au même format que `raw.epub_metadata.file` | Test prévu |
| Actualité | À revoir à chaque ajout de livre | |
| Risques connus | Erreur de saisie ; fichier renommé ou déplacé, qui rend la ligne orpheline | |

## 8. Gouvernance et conformité
| Champ | Valeur | Vérification |
|---|---|---|
| Données personnelles présentes dans la source | Aucune | |
| Données personnelles collectées par le projet | La liste des fichiers révèle une partie de ma bibliothèque (voir `epub.md`, §8) : le seed reste local | |
| Base légale et finalité (si données personnelles) | Sans objet | |
| Minimisation appliquée | Seulement les lignes qui demandent une correction | |
| Licence | Sans objet (fichier local, non publié) ; titres de livres, données factuelles | |
| Restrictions d'usage | Aucune | |
| Attribution à faire | Sans objet | |
| Durée de conservation | Tant que le projet existe | |
| Redistribution | Aucune : seed local. Le dépôt contient sa description YAML, ses tests et un exemple inventé | |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | Constats du profilage (issue #8) ; vérification à la main dans les livres |
| Extraction | Aucune : saisie directe |
| Tables raw | Seed dbt `book_mapping` |
| Transformations prévues | Jointure sur `file` dans le staging EPUB : titre de référence, marquage `is_duplicate`, lien vers l'omnibus |
| Destinations aval | `dim_book` ; rapprochement des titres avec KOReader et le wiki |

## 10. Décisions et questions ouvertes
| Date | Décision ou question | Statut |
|---|---|---|
| 27/10/2026 | Les doublons et les parties d'omnibus sont marqués, jamais supprimés | Décidé |
| 28/10/2026 | Seed gardé en local (`data/seeds/`), clé = chemin relatif ; pas de hachage, pas d'exception au hook | Décidé |

## Historique de la fiche
| Version | Date | Modification |
|---|---|---|
| 1 | 28/10/2026 | Création (source prévue) |
| 2 | 28/10/2026 | Seed en local |
| 3 | 28/10/2026 | Lignes Robots.txt et Conditions d'utilisation du modèle ; historique local proposé |
