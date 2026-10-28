# Fiche d'identité - Warhammer 40k Lexicanum

> **Métadonnées de la fiche**
> - Rédacteur : Marine Prost
> - Date : 28/10/2026
> - Version : 1
> - Statut : brouillon (accès, version, volumétrie et licence par défaut vérifiés le 28/10/2026 ; licence du pied de page 40k et whitelistage à confirmer)
> - Référence : modèle des fiches `warhammer40k.wiki.gg` et `warhammer40k.fandom.com`
> - Questions servies : 1 à 4 (`docs/questions.md`), pour les éléments « nom de l'entité », « type » et « alias »

## 1. Identité
| Champ | Valeur |
|---|---|
| Nom | Warhammer 40k - Lexicanum (`sitename`) |
| Identifiant unique (slug) | `wh40k_lexicanum` (identifiant renvoyé par l'API, `wikiid`) |
| URL principale | https://wh40k.lexicanum.com/wiki/Main_Page |
| Description (1–2 phrases) | Encyclopédie de fans dédiée à Warhammer 40,000, sur le modèle de Wikipédia, qui n'accepte que du matériel officiellement publié (pas de contenu de fans) |
| Domaine métier | Univers fictionnel Warhammer 40,000 |
| Langue(s) | Anglais (`lang: en`). Le réseau Lexicanum a d'autres éditions (allemande, française) et d'autres univers Warhammer ; la fiche porte sur le wiki 40k anglais |
| Public cible | Fans de Warhammer 40k, lecteurs de lore, recherche de sources officielles |

## 2. Technique
| Champ | Valeur |
|---|---|
| Plateforme | **MediaWiki 1.30.0**, PHP 7.1, MySQL 5.7 (vérifié par `meta=siteinfo` le 28/10/2026). Version ancienne : certains paramètres récents de l'API peuvent manquer, à tester |
| Format natif | Wikitext ; HTML rendu |
| API | Oui : MediaWiki Action API, **https://wh40k.lexicanum.com/mediawiki/api.php** (`scriptpath: /mediawiki`), et non `/api.php` à la racine. **Autorisée aux robots** par le robots.txt, avec un délai de 5 s entre deux requêtes |
| Dumps / exports | `Special:Export` (MediaWiki) ; aucun dump public régulier identifié |
| Localisation | Pages : `https://wh40k.lexicanum.com/wiki/<Titre>` ; API et scripts sous `https://wh40k.lexicanum.com/mediawiki/` |
| Clés disponibles | `page_id` (stable), `revision_id` (stable), titre (non stable), espace de noms, catégories. API : `list=allpages`, `list=allredirects`, `list=categorymembers`, `prop=categories` (disponibilité à confirmer sur la version 1.30) |
| Structure | Infoboxes, catégories, pages de contenu, pages de discussion, pages méta, pages de désambiguïsation |
| Fuseau horaire | UTC (`timezone: UTC`) |

## 3. Provenance
| Champ | Valeur |
|---|---|
| Système producteur | Communauté de bénévoles, encadrée par les administrateurs |
| Date de création | 2005 (date avancée par plusieurs sources ; à confirmer par l'historique de la page d'accueil) |
| Origine | Projet indépendant, antérieur à la refondation du wiki Fandom (2010) et au wiki.gg ; une partie des éditeurs de wiki.gg en vient |

## 4. Propriété
| Champ | Valeur |
|---|---|
| Data owner | Équipe d'administration du wiki (12 administrateurs, `statistics.admins`) ; hébergeur à confirmer (Bell of Lost Souls avancé, source non retrouvée) |
| Data steward (projet) | Marine Prost |
| Équipe responsable | Éditeurs, administrateurs, bureaucrates |
| Contact | Serveur Discord du Lexicanum (à identifier), pour annoncer l'extraction automatisée |

## 5. Opérationnel
| Champ | Valeur |
|---|---|
| Mode d'accès retenu | API MediaWiki, **une requête toutes les 5 s au minimum** (`Crawl-delay: 5`), `User-Agent` identifiant le projet avec un contact, paramètre `maxlag`, réponses mises en cache dans `data/raw/`. Extraction ponctuelle, pas de rafraîchissement automatique |
| Robots.txt (vérifié le 28/10/2026) | `User-agent: *` : `Crawl-delay: 5` ; `Disallow` uniquement sur les dossiers internes de MediaWiki (`/mediawiki/extensions`, `/maintenance`, `/includes`, `/docs`, `/bin`, `/cache`, `/languages`, `/mw-config`, `/serialized`, `/resources`, `/skins.bak`). `/mediawiki/api.php` n'est pas interdit. Quelques robots nommés sont exclus (TurnitinBot, SEOkicks-Robot, SimplePie, Speedy, jobs.de-Robot) |
| Whitelistage d'adresse IP | Avancé par une source non retrouvée ; non mentionné dans le robots.txt. L'API répond depuis un navigateur. À confirmer en annonçant l'extraction sur le Discord |
| Estimation de charge | Titres : environ 100 requêtes (`list=allpages`, 500 par requête) ; redirections : du même ordre ; catégories : quelques centaines. Soit 30 à 60 min à 5 s par requête, une seule fois |
| Fréquence de mise à jour | Continue (éditions communautaires) |
| Fraîcheur | Horodatage de dernière révision par page (`prop=revisions&rvprop=timestamp`) |
| Volumétrie au 28/10/2026 (`meta=siteinfo`) | **50 220 articles**, 121 567 pages tous espaces de noms confondus, 811 525 éditions, 34 974 images |
| Activité | 32 utilisateurs actifs, 12 administrateurs |
| SLA / limites | Aucun SLA. Délai de 5 s imposé par le robots.txt |

## 6. Couverture
| Champ | Valeur |
|---|---|
| Granularité | Page (article) ; section ou champ d'infobox accessibles via le wikitext |
| Profondeur d'historique | Révisions accessibles via l'API (`prop=revisions`) ; hors besoin pour la v0.1 |
| Couverture thématique | Lore Warhammer 40,000, matériel officiel uniquement (codex, romans Black Library, White Dwarf…) |
| Couverture temporelle (in-universe) | 30k (Horus Heresy), 40k et ères associées |
| Couverture des entités de ma bibliothèque | À mesurer sur un échantillon de 20 noms tirés de deux de mes livres (personnages principaux et secondaires, lieux, une arme) |

## 7. Qualité
| Champ | Valeur |
|---|---|
| Complétude | 50 220 articles, du même ordre que wiki.gg et environ sept fois plus que Fandom. Complétude pour mes livres à mesurer |
| Alias | Redirections accessibles via `list=allredirects` |
| Titres avec précision entre parenthèses | Attendus (désambiguïsations, œuvres) ; à mesurer et à filtrer |
| Cohérence | Politique éditoriale stricte : matériel officiel uniquement, sources exigées |
| Risque | Version de MediaWiki ancienne (comportement de l'API à tester) ; renommages de pages (le titre n'est pas une clé stable) |
| Citations | Les articles citent leurs sources (livre, souvent chapitre) : utilisables comme vérité de référence pour mesurer la qualité de la correspondance exacte |

## 8. Gouvernance
| Champ | Valeur |
|---|---|
| Données personnelles | Présentes dans l'historique (noms d'utilisateurs, adresses IP). **Non collectées** : le projet ne récupère ni l'historique ni les contributeurs |
| Sensibilité | Contenu de fans dérivé de la propriété intellectuelle de Games Workshop |
| Licence | **CC BY-NC** par défaut : « Except where otherwise specified in the Terms of Service, the text on Lexicanum sites is licensed under the Creative Commons Attribution NonCommercial License (CC-BY-NC) » (*General disclaimer*, consulté le 28/10/2026). Version de la licence non précisée. Certains wikis du réseau utilisent une autre licence, indiquée dans leur pied de page : **vérifier le pied de page du wiki 40k**. L'API ne déclare pas de licence (`rightsinfo` vide). Les images n'ont pas forcément la même licence que le texte (non collectées) |
| Restrictions d'usage | Pas d'usage commercial ; attribution obligatoire, selon l'une des formes prévues par le disclaimer : lien vers l'article, lien vers une copie stable, ou liste des auteurs. Délai de 5 s entre requêtes |
| Durée de conservation | Copie locale conservée tant que le projet existe ; régénérable à partir de la source |
| Redistribution | Aucune dans la v0.1 : données dans `data/` (ignoré par Git). Le README cite la source sur le modèle proposé par Lexicanum : « This project uses material from the Warhammer 40k Lexicanum (https://wh40k.lexicanum.com), licensed under the Creative Commons Attribution-NonCommercial License. » Si le plugin affiche un jour du texte d'article, chaque fiche devra pointer vers l'article source |
| Conformité RGPD | Pas de donnée personnelle collectée, donc pas de traitement au sens du RGPD pour cette source |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | Matériel officiel Games Workshop : codex, romans Black Library, White Dwarf |
| Destinations aval | `data/raw/` (réponses de l'API) → `raw` dans DuckDB → staging (lexique normalisé, alias) → `dim_entity` → correspondance avec le texte EPUB → plugin Pokédex KOReader |
| Transformations | Titres via `list=allpages`, redirections via `list=allredirects`, catégories via `list=categorymembers` ; retrait des précisions entre parenthèses ; filtrage des pages hors entités ; type par branche de catégorie |
