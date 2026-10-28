# Fiche d'identité - Warhammer 40k Wiki (Fandom)

> **Métadonnées de la fiche**
> - Rédacteur : Marine Prost
> - Date : 28/10/2026
> - Version : 2
> - Statut : brouillon (accès, licence et conditions d'utilisation vérifiés le 28/10/2026)
> - Décision : **non retenue en l'état** — accès automatisé interdit sans autorisation écrite de Fandom, Inc.
> - Référence : modèle de la fiche `warhammer40k.wiki.gg`
> - Questions servies : 1 à 4 (`docs/questions.md`), pour les éléments « nom de l'entité », « type » et « alias »

## 1. Identité
| Champ | Valeur |
|---|---|
| Nom | Warhammer 40k Wiki |
| Identifiant unique (slug) | `warhammer40k` (identifiant renvoyé par l'API, `wikiid`) |
| URL principale | https://warhammer40k.fandom.com/wiki/Warhammer_40k_Wiki |
| Description | « collaborative project to create the most definitive, accurate, and accessible encyclopedia and reference for everything related to Warhammer 40,000 », avec un objectif affiché de qualité d'édition « uncommon on most other fan-based wikis » |
| Domaine métier | Univers fictionnel Warhammer 40,000 |
| Langue(s) | Anglais (`lang: en`). Des wikis Fandom distincts existent en allemand, espagnol, français, polonais et russe ; la fiche porte sur le wiki anglais |
| Public cible | Fans de Warhammer 40k, lecteurs de lore |

## 2. Technique
| Champ | Valeur |
|---|---|
| Plateforme | MediaWiki 1.43.9, hébergé par Fandom (vérifié par `meta=siteinfo` le 28/10/2026) |
| Format natif | Wikitext ; HTML rendu |
| API | Oui : MediaWiki Action API, https://warhammer40k.fandom.com/api.php. **Autorisée aux robots** par le robots.txt du wiki (`Allow: /api.php?`, `Allow: /api.php?action=` pour `User-agent: *`), vérifié le 28/10/2026 |
| Dumps / exports | `Special:Export` existe (MediaWiki) mais `/wiki/Special:` est interdit aux robots. Téléchargement de base sur demande (`dumpsondemand`) : à vérifier |
| Sitemap | https://warhammer40k.fandom.com/sitemap-newsitemapxml-index.xml (déclaré dans le robots.txt) |
| Localisation | https://warhammer40k.fandom.com/wiki/<Titre> |
| Clés disponibles | `page_id` (stable), `revision_id` (stable), titre (non stable), espace de noms, catégories. API : `list=allpages`, `list=allredirects`, `list=categorymembers`, `prop=categories` |
| Structure | Infoboxes via templates, catégories MediaWiki, pages de contenu, pages de discussion, pages méta (`Warhammer_40k_Wiki:`), pages de désambiguïsation |
| Fuseau horaire | UTC (`timezone: UTC`) |

## 3. Provenance
| Champ | Valeur |
|---|---|
| Système producteur | Communauté de bénévoles, sous supervision des administrateurs et modérateurs |
| Date de création | Juillet 2005 ; refondé en mai 2010 (page « About » du wiki) |
| Origine | Projet communautaire indépendant, hébergé sur Fandom. Pas un fork de Lexicanum ; Lexicanum cité comme source de recherche, copie interdite |

## 4. Propriété
| Champ | Valeur |
|---|---|
| Data owner | Équipe d'administration du wiki ; Fandom, Inc. comme hébergeur |
| Data steward (projet) | Marine Prost |
| Équipe responsable | Administrateurs et modérateurs (5 administrateurs, `statistics.admins`) |
| Contact | Page de discussion des administrateurs ou Discord du wiki (à identifier) |

## 5. Opérationnel
| Champ | Valeur |
|---|---|
| Mode d'accès retenu | **Aucun en l'état.** Les conditions d'utilisation interdisent tout accès automatisé sans autorisation écrite (voir ligne suivante), même si le robots.txt autorise l'API |
| Conditions d'utilisation (Fandom Terms of Use, révision du 19/12/2025, consultées le 28/10/2026) | Section *User conduct* : interdiction d'« use any robot, spider, site search and/or retrieval application, or other device to scrape, extract, retrieve or index any portion of the content » et de « use any robot, spider, scraper or other automated means to access the Services for any purpose without our express written permission ». Interdiction de « scrape (…) aggregate » le contenu, sauf ce que permet la page Licensing pour le texte des wikis (CC BY-SA). Interdiction d'utiliser le contenu pour développer un logiciel ou entraîner une IA sans accord écrit. **La licence CC BY-SA autorise la réutilisation du texte, mais pas l'accès automatisé pour le récupérer** |
| Robots.txt (vérifié le 28/10/2026) | `User-agent: *` : `Allow` sur `/api.php?` et `/api.php?action=` ; `Disallow` sur `/wiki/Special:`, `/wiki/User:`, `/wiki/Template:`, `/wiki/Help:`. Pas de signal de contenu. Des robots d'IA nommés sont exclus (GPTBot, ClaudeBot, CCBot…) |
| Fréquence de mise à jour | Continue (éditions communautaires) |
| Fraîcheur | Horodatage de dernière révision par page (`prop=revisions&rvprop=timestamp`) |
| Volumétrie au 28/10/2026 (`meta=siteinfo`) | **7 322 articles**, 88 328 pages tous espaces de noms confondus, 449 735 éditions, 27 777 images |
| Activité | **26 utilisateurs actifs**, 5 administrateurs : wiki maintenu par une petite équipe |
| SLA / limites | Aucun SLA. Limites de débit de l'API Fandom non documentées publiquement |

## 6. Couverture
| Champ | Valeur |
|---|---|
| Granularité | Page (article) ; section ou champ d'infobox accessibles via le wikitext |
| Profondeur d'historique | Révisions accessibles via l'API (`prop=revisions`) ; hors besoin pour la v0.1 |
| Couverture thématique | Lore Warhammer 40,000, jeux, romans, médias. Exclusions explicites : statistiques de jeu, fan-art, copie de Lexicanum |
| Couverture temporelle (in-universe) | 30k (Horus Heresy), 40k et ères associées |
| Couverture des entités de ma bibliothèque | À mesurer : 7 322 articles contre au moins 50 000 pages de contenu sur wiki.gg ; les personnages secondaires risquent d'être absents |

## 7. Qualité
| Champ | Valeur |
|---|---|
| Complétude | Beaucoup moins d'articles que wiki.gg (7 322 contre 50 000+), articles réputés plus longs et plus contrôlés. À mesurer sur un échantillon d'entités de mes livres |
| Alias | Redirections accessibles via `list=allredirects`. Lexicanum, évalué après cette fiche, offre le même accès par son API, autorisée aux robots |
| Titres avec précision entre parenthèses | Fréquents (« (Novel) », « (Short Story) », désambiguïsations) ; à filtrer |
| Cohérence | Politique éditoriale stricte : canon uniquement, anglais britannique, éditions relues par l'équipe |
| Risque | Petite équipe active (26 utilisateurs) : couverture qui progresse lentement ; renommages de pages |
| Citations | Les articles citent généralement leurs sources (codex, romans, White Dwarf) ; à vérifier article par article |

## 8. Gouvernance
| Champ | Valeur |
|---|---|
| Données personnelles | Présentes dans l'historique (noms d'utilisateurs, adresses IP). **Non collectées** : le projet ne récupère ni l'historique ni les contributeurs |
| Sensibilité | Contenu de fans dérivé de la propriété intellectuelle de Games Workshop |
| Licence | **CC BY-SA** (`rightsinfo` : « CC-BY-SA », renvoi vers https://www.fandom.com/licensing) ; version 3.0 Unported d'après la page Copyrights du wiki |
| Restrictions d'usage | Attribution obligatoire ; **partage à l'identique** : toute donnée dérivée redistribuée (par exemple un lexique embarqué dans le plugin) devrait l'être sous la même licence |
| Durée de conservation | Copie locale conservée tant que le projet existe ; régénérable à partir de la source |
| Redistribution | Aucune dans la v0.1 : données dans `data/` (ignoré par Git) ; le README cite la source et sa licence |
| Conformité RGPD | Pas de donnée personnelle collectée, donc pas de traitement au sens du RGPD pour cette source |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | Codex Games Workshop, romans Black Library, White Dwarf ; Wikipédia (copie autorisée sous CC BY-SA) |
| Destinations aval | `data/raw/` (réponses de l'API) → `raw` dans DuckDB → staging (lexique normalisé, alias) → `dim_entity` → correspondance avec le texte EPUB → plugin Pokédex KOReader |
| Transformations | Titres et catégories via l'API, redirections via `list=allredirects`, retrait des précisions entre parenthèses, filtrage des pages hors entités, type par branche de catégorie |

## 10. Décisions et questions ouvertes
| Date | Décision ou question | Statut |
|---|---|---|
| 28/10/2026 | Non retenue : les Terms of Use (19/12/2025) interdisent l'accès automatisé et l'extraction sans autorisation écrite | Décidé |
| 28/10/2026 | Deux projets publics collectent ce wiki ([w40k-explorer](https://github.com/guico33/w40k-explorer) : parcours de `Special:AllPages` puis HTML de chaque article ; [nosql-rag-azure](https://github.com/dacraw/nosql-rag-azure) : API `action=parse`). Aucun accord ni attribution mentionnés, User-Agent qui imite un navigateur. Ils ne constituent pas un précédent. Pratiques reprises pour notre pipeline : brut et transformé séparés, collecte reprenable, options `--dry-run` et `--retry-failed` ; `action=parse` avec `prop=categories` gardé pour le jour où un accès est accordé | Noté |
