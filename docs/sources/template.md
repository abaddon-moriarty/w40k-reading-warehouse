# Fiche d'identité - [Nom de la source]

<!--
Mode d'emploi
- Une fiche par source : base de données, API, fichier, site web, jeu open data, saisie manuelle.
- Colonne « Vérification » : d'où vient la valeur et quand elle a été constatée
  (ex. « meta=siteinfo, 28/10/2026 », « robots.txt, 28/10/2026 », « page About »).
  Une valeur sans vérification s'écrit « à vérifier », jamais comme un fait.
- Pas de chiffre sans source. Pas de référence qui ne renvoie à rien.
- Pour une source externe, trois documents se lisent ensemble : licence, robots.txt, conditions d'utilisation.
  Le robots.txt dit ce qu'un programme peut techniquement interroger ; seules les conditions disent ce qu'on a le droit d'en faire.
- Laisser « sans objet » plutôt que supprimer une ligne : l'absence est une information.
- Supprimer ces commentaires une fois la fiche remplie.
-->

> **Métadonnées de la fiche**
> - Rédacteur :
> - Date de création / dernière mise à jour :
> - Version :
> - Statut : brouillon | vérifiée | écartée
> - Questions servies : <!-- numéros des questions (docs/questions.md) et éléments de données couverts -->
> - Décision : retenue | écartée | en attente : <!-- une phrase : pourquoi -->

## 1. Identité
| Champ | Valeur | Vérification |
|---|---|---|
| Nom | | |
| Identifiant unique | <!-- slug, nom technique, identifiant renvoyé par le système --> | |
| Type de source | <!-- base opérationnelle, API, fichier, site web, open data, saisie manuelle --> | |
| URL ou emplacement | | |
| Description (1–2 phrases) | <!-- citer la source elle-même si possible --> | |
| Domaine métier | | |
| Langue(s) | | |

## 2. Accès et format
| Champ | Valeur | Vérification |
|---|---|---|
| Système / plateforme | <!-- logiciel et version --> | |
| Format natif | <!-- tables SQL, JSON, CSV, XML, HTML… --> | |
| Points d'accès disponibles | <!-- API (endpoint), export, dump, sitemap, fichier, connexion directe --> | |
| Authentification | <!-- aucune, clé, compte, autorisation préalable --> | |
| Robots.txt | <!-- ce qu'il autorise et interdit aux programmes ; le robots.txt ne dit rien des usages permis --> | |
| Conditions d'utilisation | <!-- lire les Terms of Service / Terms of Use EN ENTIER : extraction automatisée, constitution de base de données, licence réelle du contenu, contenu de l'API. Citer les paragraphes --> | |
| Conditions d'accès automatisé (synthèse) | <!-- autorisé / autorisé avec conditions / soumis à accord écrit / interdit, et pourquoi --> | |
| Mode d'accès retenu | <!-- comment le projet y accède réellement, et à quel rythme --> | |
| Emplacement de la copie locale | <!-- ex. data/raw/<source>/ --> | |

## 3. Structure et clés
| Champ | Valeur | Vérification |
|---|---|---|
| Grain | <!-- que représente une ligne / un enregistrement --> | |
| Objets ou tables utiles | | |
| Clés disponibles | <!-- naturelles, techniques ; stables ou non --> | |
| Clé de jointure avec les autres sources | <!-- laquelle, et sa fiabilité --> | |
| Fuseau horaire / unités / encodage | | |
| Dictionnaire ou documentation | <!-- lien, ou « absent » --> | |

## 4. Provenance et propriété
| Champ | Valeur | Vérification |
|---|---|---|
| Système producteur | <!-- qui ou quoi crée la donnée, et pourquoi --> | |
| Processus de saisie | <!-- qui saisit, avec quelle incitation : conditionne la fiabilité --> | |
| Date de création de la source | | |
| Propriétaire (data owner) | | |
| Responsable côté projet (data steward) | | |
| Contact | | |

## 5. Volumétrie et fraîcheur
| Champ | Valeur | Vérification |
|---|---|---|
| Volumétrie | <!-- nombre d'enregistrements utiles, avec la date --> | |
| Profondeur d'historique | | |
| Fréquence de mise à jour de la source | | |
| Fraîcheur mesurable | <!-- champ de date disponible pour la mesurer --> | |
| Fréquence de rafraîchissement dans le projet | <!-- ponctuelle, quotidienne, à la demande --> | |
| Activité / maintenance | <!-- la source est-elle encore entretenue ? --> | |

## 6. Couverture
| Champ | Valeur | Vérification |
|---|---|---|
| Population couverte | <!-- qui ou quoi est dedans ; qui ou quoi n'y est pas --> | |
| Période couverte | | |
| Champs utiles et leur taux de remplissage | <!-- renvoyer au profilage --> | |
| Couverture mesurée sur le besoin du projet | <!-- échantillon, méthode, résultat --> | |

## 7. Qualité
<!-- Une ligne par dimension. « À mesurer » tant que le profilage n'est pas fait. -->
| Dimension | Constat | Vérification |
|---|---|---|
| Complétude des valeurs | | |
| Complétude de la population | | |
| Exactitude | | |
| Cohérence (interne, avec les autres sources) | | |
| Unicité (doublons) | | |
| Validité (formats, domaines de valeurs) | | |
| Actualité | | |
| Risques connus | | |

## 8. Gouvernance et conformité
| Champ | Valeur | Vérification |
|---|---|---|
| Données personnelles présentes dans la source | | |
| Données personnelles collectées par le projet | <!-- lesquelles, ou « aucune » --> | |
| Base légale et finalité (si données personnelles) | | |
| Minimisation appliquée | <!-- ce qu'on écarte volontairement --> | |
| Licence | <!-- nom exact, version, où elle est déclarée ; vérifier que les conditions d'utilisation ne la restreignent pas (délai, contenu exclu) --> | |
| Restrictions d'usage | <!-- commercial, attribution, partage à l'identique, propriété intellectuelle --> | |
| Attribution à faire | <!-- texte et emplacement (README, interface) --> | |
| Durée de conservation | | |
| Redistribution | <!-- ce qui sort du projet, ou « aucune » --> | |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | <!-- d'où la source tire elle-même ses données --> |
| Extraction | <!-- script, commande, ou procédure manuelle --> |
| Tables raw | |
| Transformations prévues | <!-- staging, règles de nettoyage --> |
| Destinations aval | <!-- modèles, tables finales, usages --> |

## 10. Décisions et questions ouvertes
| Date | Décision ou question | Statut |
|---|---|---|
| | | |

## Historique de la fiche
| Version | Date | Modification |
|---|---|---|
| 1 | | Création |
