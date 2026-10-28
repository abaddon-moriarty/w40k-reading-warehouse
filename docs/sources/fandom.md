# Fiche d'identité - Warhammer 40k Wiki (Fandom)

> **Métadonnées de la fiche**
> - Rédacteur : Marine Prost
> - Date : 28/10/2026
> - Version : 1
> - Statut : brouillon
> - Référence : modèle de la fiche `warhammer40k.wiki.gg`

## 1. Identité
| Champ | Valeur |
|---|---|
| Nom | Warhammer 40k Wiki |
| Identifiant unique (slug) | `warhammer40k` (sous-domaine Fandom : `warhammer40k.fandom.com`) |
| URL principale | https://warhammer40k.fandom.com/wiki/Warhammer_40k_Wiki |
| Description (1–2 phrases) | Encyclopédie collaborative dédiée à l'univers de Warhammer 40,000, créée en juillet 2005 puis refondée en mai 2010, visant une « accuracy and quality of editing uncommon on most other fan-based wikis ». |
| Domaine métier | Univers fictionnel / jeu de figurines / produits dérivés (romans, jeux vidéo) |
| Langue(s) | Anglais (wiki principal) ; déclinaisons espagnole, française, allemande… sont des wikis Fandom distincts |
| Public cible | Fans de Warhammer 40k, lecteurs de lore, joueurs |

## 2. Technique
| Champ | Valeur |
|---|---|
| Plateforme | MediaWiki, hébergé par Fandom (Wikia, Inc.) |
| Format natif | Wikitext ; HTML rendu |
| API | Oui : MediaWiki Action API, `https://warhammer40k.fandom.com/api.php`. Contrairement à wiki.gg, Fandom autorise généralement l'accès à `/api.php` (règles `Allow` dans le `robots.txt` de Fandom) |
| Dumps / exports | `Special:Statistics` et `Special:Export` disponibles. Téléchargement de base de données sur demande (`dumpsondemand`) pour les utilisateurs disposant des droits |
| Sitemap | Sitemap local disponible (`Special:LocalSitemap`), pages listées par ordre alphabétique |
| Localisation | URL de type `https://warhammer40k.fandom.com/wiki/<Titre>` (espaces remplacés par `_`, encodage standard MediaWiki) |
| Clés disponibles | Via l'API : `page_id` (stable), `revision_id` (stable), `page_title` (non stable:  soumis aux renommages), `namespace`, catégories. API supporte `prop=revisions`, `prop=categories`, `list=allpages`, `list=allredirects` |
| Structure | Infoboxes via templates, catégories MediaWiki, pages de contenu, pages de discussion, redirections nombreuses, pages méta (`Warhammer_40k_Wiki:`) |
| Fuseau horaire | À vérifier (`meta=siteinfo`) |

## 3. Provenance
| Champ | Valeur |
|---|---|
| Système producteur | Communauté de bénévoles (éditeurs, administrateurs, bots) |
| Date de création | Juillet 2005 ; refondé en mai 2010 sous une nouvelle direction |
| Origine | Projet communautaire indépendant, hébergé sur Fandom (ex-Wikia). Pas présenté comme un fork de Lexicanum, mais entretient des liens avec lui (Lexicanum cité comme « the largest repository of Warhammer 40,000-related information ») |

## 4. Propriété
| Champ | Valeur |
|---|---|
| Data owner | Administration du wiki et sa communauté ; Fandom, Inc. en tant qu'hébergeur et plateforme |
| Data steward (projet) | [vous / votre équipe] |
| Équipe responsable | Bénévoles, administrateurs du wiki (rôles `sysop`, `bureaucrat` sur Fandom) |
| Contact | Page de discussion des administrateurs ou Discord du wiki (à identifier pour toute demande d'accès) |

## 5. Opérationnel
| Champ | Valeur |
|---|---|
| Mode d'accès | API MediaWiki (`/api.php`), accessible et généralement autorisée par le `robots.txt` de Fandom. Scraping HTML possible mais moins fiable |
| Fréquence de mise à jour | Continue (éditions communautaires) |
| Fraîcheur | Timestamp de dernière révision par page, requêtable via l'API (`prop=revisions&rvprop=timestamp`) |
| Volumétrie | À récupérer sur `Special:Statistics` du wiki anglais. La page « About » de 2011 mentionnait 6 997 articles ; chiffre actuel à confirmer |
| SLA / limites | Aucun SLA public. Limites de débit de l'API Fandom non documentées publiquement de manière détaillée |
| Robots.txt | Hébergé par Fandom. Règles variables selon les wikis, mais `/api.php` généralement autorisé. À vérifier sur `https://warhammer40k.fandom.com/robots.txt` |

## 6. Couverture
| Champ | Valeur |
|---|---|
| Granularité | Page (article) ; section ou champ d'infobox accessibles en analysant le wikitext |
| Profondeur d'historique | MediaWiki conserve toutes les révisions par défaut ; accessibles via l'API (`prop=revisions`) et via l'historique de chaque page |
| Couverture thématique | Lore Warhammer 40,000 (depuis Rogue Trader, 1987), jeux de plateau, jeux vidéo, romans (pages suffixées « (Novel) », « (Short Story) », etc.), médias. Exclusion explicite des règles de jeu (statistiques de tabletop), considérées comme propriété intellectuelle de Games Workshop |
| Couverture temporelle (in-universe) | 30k (Horus Heresy), 40k et ères associées |
| Couverture des personnages de la bibliothèque (sondage) | À vérifier sur le wiki Fandom (les pages existent probablement, mais le sitemap local ne permet pas un sondage automatique immédiat) |

## 7. Qualité
| Champ | Valeur |
|---|---|
| Complétude | Wiki ancien (2005) et bien établi. La page « About » revendique une qualité d'édition supérieure à la moyenne des wikis de fans. Nombre d'articles inférieur à Lexicanum (~34 000), mais articles souvent plus longs et plus détaillés |
| Alias | Redirections nombreuses sur Fandom (contrairement au wiki.gg où le sitemap ne les inclut pas) ; accessibles via l'API (`list=allredirects`), ce qui facilite la correspondance des noms courts |
| Titres avec précision entre parenthèses | Fréquents (ex. « Space Wolf (Novel) », « Squats (Original) »), à filtrer pour la recherche d'entités |
| Cohérence | Politique éditoriale axée sur le lore canon ; exclusion des règles de jeu et du fan-art (sauf exceptions). Risque de spéculation fan à surveiller, moindre que sur des wikis moins modérés |
| Fraîcheur | Mise à jour communautaire continue |
| Risque | Vandalisme, guerres d'édition, renommages de pages (le titre n'est pas une clé stable) |
| Citations | Les articles citent généralement leurs sources (codex, romans, White Dwarf) ; vérification article par article |

## 8. Gouvernance
| Champ | Valeur |
|---|---|
| Données personnelles | Présentes dans l'historique des pages : noms d'utilisateurs et adresses IP des éditions anonymes archivés et affichés indéfiniment par conception sur Fandom. Si l'historique est ingéré, traitement de données personnelles au sens du RGPD |
| Sensibilité | Contenu de fans dérivé de la propriété intellectuelle de Games Workshop ; noms, marques et images appartiennent à Games Workshop et à ses licenciés. Règles de jeu explicitement exclues |
| Licence | Creative Commons Attribution-Share Alike 3.0 (Unported); CC BY-SA 3.0, déclarée sur les pages de contenu et de copyright du wiki |
| Restrictions d'usage | Attribution obligatoire ; partage à l'identique (Share Alike). La licence CC BY-SA 3.0 autorise théoriquement l'usage commercial, mais l'IP Games Workshop reste protégée. Vérifier les conditions de Fandom pour l'usage commercial |
| Durée de conservation | [à définir selon votre projet] |
| Conformité RGPD | Si collecte de l'historique : base légale à définir, minimisation (ne conserver que les champs nécessaires), durée de conservation limitée. Si collecte du contenu des pages uniquement (sans historique) : pas de donnée personnelle collectée |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | Codex Games Workshop, romans Black Library, White Dwarf ; Wikipédia (articles copiés sous CC BY-SA, avec procédure documentée) ; Lexicanum cité comme source de recherche mais pas comme source de copie (plagiat interdit) |
| Destinations aval | [votre base, votre index RAG, votre pipeline, etc.] |
| Transformations | Parsing du wikitext, extraction des infoboxes, normalisation des catégories, filtrage des pages hors entités (désambiguïsation, œuvres, listes), récupération des redirections via l'API pour les alias |
