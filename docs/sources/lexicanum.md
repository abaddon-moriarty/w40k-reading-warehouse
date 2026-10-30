# Fiche d'identité - Warhammer 40k Lexicanum

> **Métadonnées de la fiche**
>
> - Rédacteur : Marine Prost
> - Date de création / dernière mise à jour : 28/10/2026
> - Version : 3
> - Statut : brouillon (accès, version, volumétrie, licence et conditions d'utilisation vérifiés le 28/10/2026)
> - Décision : **reportée en V2** : les conditions d'utilisation interdisent l'usage prévu sans accord écrit préalable (§4 et §5) ; demande d'accord prévue en V2
> - Référence : modèle des fiches `warhammer40k.wiki.gg` et `warhammer40k.fandom.com`
> - Questions servies : 1 à 4 (`docs/questions.md`), pour les éléments « nom de l'entité », « type » et « alias »

## 1. Identité

| Champ | Valeur |
| --- | --- |
| Nom | Warhammer 40k - Lexicanum (`sitename`) |
| Identifiant unique (slug) | `wh40k_lexicanum` (identifiant renvoyé par l'API, `wikiid`) |
| URL principale | <https://wh40k.lexicanum.com/wiki/Main_Page> |
| Description (1–2 phrases) | Encyclopédie de fans dédiée à Warhammer 40,000, sur le modèle de Wikipédia, qui n'accepte que du matériel officiellement publié (pas de contenu de fans) |
| Domaine métier | Univers fictionnel Warhammer 40,000 |
| Langue(s) | Anglais (`lang: en`). Le réseau Lexicanum a d'autres éditions (allemande, française) et d'autres univers Warhammer ; la fiche porte sur le wiki 40k anglais |
| Public cible | Fans de Warhammer 40k, lecteurs de lore, recherche de sources officielles |

## 2. Technique

| Champ | Valeur |
| --- | --- |
| Plateforme | **MediaWiki 1.30.0**, PHP 7.1, MySQL 5.7 (vérifié par `meta=siteinfo` le 28/10/2026). Version ancienne : certains paramètres récents de l'API peuvent manquer, à tester |
| Format natif | Wikitext ; HTML rendu |
| API | Oui : MediaWiki Action API, **<https://wh40k.lexicanum.com/mediawiki/api.php>** (`scriptpath: /mediawiki`), et non `/api.php` à la racine. **Autorisée aux robots** par le robots.txt, avec un délai de 5 s entre deux requêtes |
| Dumps / exports | `Special:Export` (MediaWiki) ; aucun dump public régulier identifié |
| Localisation | Pages : `https://wh40k.lexicanum.com/wiki/<Titre>` ; API et scripts sous `https://wh40k.lexicanum.com/mediawiki/` |
| Clés disponibles | `page_id` (stable), `revision_id` (stable), titre (non stable), espace de noms, catégories. API : `list=allpages`, `list=allredirects`, `list=categorymembers`, `prop=categories` (disponibilité à confirmer sur la version 1.30) |
| Structure | Infoboxes, catégories, pages de contenu, pages de discussion, pages méta, pages de désambiguïsation |
| Fuseau horaire | UTC (`timezone: UTC`) |

## 3. Provenance

| Champ | Valeur |
| --- | --- |
| Système producteur | Communauté de bénévoles, encadrée par les administrateurs |
| Date de création | 2005 (date avancée par plusieurs sources ; à confirmer par l'historique de la page d'accueil) |
| Origine | Projet indépendant, antérieur à la refondation du wiki Fandom (2010) et au wiki.gg ; une partie des éditeurs de wiki.gg en vient |

## 4. Propriété

| Champ | Valeur |
| --- | --- |
| Data owner | BoLS Interactive LLC (Texas), propriétaire du site selon les conditions d'utilisation (§13, consultées le 28/10/2026) ; équipe d'administration du wiki (12 administrateurs, `statistics.admins`) |
| Data steward (projet) | Marine Prost |
| Équipe responsable | Éditeurs, administrateurs, bureaucrates |
| Contact | Administrateurs du wiki ou serveur Discord du Lexicanum (à identifier), pour la demande d'accord écrit. L'adresse de BoLS Interactive indiquée dans les conditions est réservée aux réclamations de droit d'auteur (DMCA) |

## 5. Opérationnel

| Champ | Valeur |
| --- | --- |
| Mode d'accès retenu | **Aucun en l'état.** L'extraction automatisée est interdite sans accord écrit préalable (conditions d'utilisation, §5). Si l'accord est obtenu : API MediaWiki, une requête toutes les 5 s au minimum (`Crawl-delay: 5`), `User-Agent` identifiant le projet avec un contact, réponses mises en cache dans `data/raw/` |
| Conditions d'utilisation (consultées le 28/10/2026) | §3(a) : le texte des articles ne passe sous CC BY-NC que 5 ans après sa dernière modification. §3(b) : les pages Special, les historiques et le contenu renvoyé par l'API ne sont pas sous CC BY-NC. §4(a) : interdiction de mettre le contenu dans une base de données, et de l'utiliser pour construire une base de données. §5 : extraction automatisée « in bulk or at scale » interdite sans accord écrit préalable, même si le contenu est public. §6 : entraînement de modèles de langage interdit. §13 : propriétaire BoLS Interactive LLC. **Le robots.txt autorise l'API, mais les conditions d'utilisation, qui engagent tout utilisateur du site, l'interdisent pour l'usage prévu** |
| Robots.txt (vérifié le 28/10/2026) | `User-agent: *` : `Crawl-delay: 5` ; `Disallow` uniquement sur les dossiers internes de MediaWiki (`/mediawiki/extensions`, `/maintenance`, `/includes`, `/docs`, `/bin`, `/cache`, `/languages`, `/mw-config`, `/serialized`, `/resources`, `/skins.bak`). `/mediawiki/api.php` n'est pas interdit. Quelques robots nommés sont exclus (TurnitinBot, SEOkicks-Robot, SimplePie, Speedy, jobs.de-Robot) |
| Whitelistage d'adresse IP | Non mentionné dans le robots.txt ni, à ce jour, dans les conditions d'utilisation lues ; question à poser avec la demande d'accord |
| Estimation de charge | À joindre à la demande d'accord : titres environ 100 requêtes (`list=allpages`, 500 par requête) ; redirections du même ordre ; catégories quelques centaines ; soit 30 à 60 min à 5 s par requête, une seule fois. C'est une extraction « in bulk » au sens du §5 |
| Fréquence de mise à jour | Continue (éditions communautaires) |
| Fraîcheur | Horodatage de dernière révision par page (`prop=revisions&rvprop=timestamp`) |
| Volumétrie au 28/10/2026 (`meta=siteinfo`) | **50 220 articles**, 121 567 pages tous espaces de noms confondus, 811 525 éditions, 34 974 images |
| Activité | 32 utilisateurs actifs, 12 administrateurs |
| SLA / limites | Aucun SLA. Délai de 5 s imposé par le robots.txt ; extraction automatisée soumise à accord écrit (§5) |

## 6. Couverture

| Champ | Valeur |
| --- | --- |
| Granularité | Page (article) ; section ou champ d'infobox accessibles via le wikitext |
| Profondeur d'historique | Révisions accessibles via l'API (`prop=revisions`) ; hors besoin pour la v0.1 |
| Couverture thématique | Lore Warhammer 40,000, matériel officiel uniquement (codex, romans Black Library, White Dwarf…) |
| Couverture temporelle (in-universe) | 30k (Horus Heresy), 40k et ères associées |
| Couverture des entités de ma bibliothèque | À mesurer sur un échantillon de 20 noms tirés de deux de mes livres (personnages principaux et secondaires, lieux, une arme) |

## 7. Qualité

| Champ | Valeur |
| --- | --- |
| Complétude | 50 220 articles, du même ordre que wiki.gg et environ sept fois plus que Fandom. Complétude pour mes livres à mesurer |
| Alias | Redirections accessibles via `list=allredirects` |
| Titres avec précision entre parenthèses | Attendus (désambiguïsations, œuvres) ; à mesurer et à filtrer |
| Cohérence | Politique éditoriale stricte : matériel officiel uniquement, sources exigées |
| Risque | Version de MediaWiki ancienne (comportement de l'API à tester) ; renommages de pages (le titre n'est pas une clé stable) |
| Citations | Les articles citent leurs sources (livre, souvent chapitre) : utilisables comme vérité de référence pour mesurer la qualité de la correspondance exacte |

## 8. Gouvernance

| Champ | Valeur |
| --- | --- |
| Données personnelles | Présentes dans l'historique (noms d'utilisateurs, adresses IP). **Non collectées** : le projet ne récupère ni l'historique ni les contributeurs |
| Sensibilité | Contenu de fans dérivé de la propriété intellectuelle de Games Workshop. La page *GW Copyright* du wiki précise que les noms, races, personnages, lieux, unités et images de l'univers sont ®, ™ ou © Games Workshop Ltd 2000-2026, « Used without permission », et que le site n'est en rien approuvé par Games Workshop (consultée le 28/10/2026). Le lexique d'entités du projet est donc fait de noms protégés : il reste local, et le README garde la mention Games Workshop |
| Licence | **CC BY-NC** par défaut : « Except where otherwise specified in the Terms of Service, the text on Lexicanum sites is licensed under the Creative Commons Attribution NonCommercial License (CC-BY-NC) » (*Lexicanum:General disclaimer*, <https://wh40k.lexicanum.com/wiki/Lexicanum:General_disclaimer>, consulté le 28/10/2026). Version de la licence non précisée. Le disclaimer prévoit aussi des wikis sous CC BY-SA ou CC BY-NC-ND : « The license used by an individual wiki is made clear in the footer and/or on the edit page of that wiki ». Le pied de page du wiki 40k ne mentionne aucune licence (liens seulement : Privacy policy, About, Disclaimers, Terms of Service ; vérifié le 28/10/2026). **Les conditions d'utilisation restreignent cette licence** : le texte d'un article n'est sous CC BY-NC que 5 ans après sa dernière modification (§3(a)), et le contenu renvoyé par l'API n'est pas sous CC BY-NC (§3(b)). Un article modifié récemment est donc sous tous droits réservés. La dérogation commerciale (« Commercial Use Waiver ») ne concerne que l'usage par Lexicanum lui-même, pas les réutilisateurs. L'API ne déclare pas de licence (`rightsinfo` vide). Les images n'ont pas forcément la même licence que le texte (non collectées) |
| Restrictions d'usage | Interdiction de construire une base de données à partir du contenu (§4(a)) et d'extraire en masse sans accord écrit (§5). Les noms de personnages ne sont pas protégés en eux-mêmes par le droit d'auteur, mais ces clauses sont contractuelles et visent aussi l'extraction de simples données. Pas d'usage commercial ; attribution obligatoire si du texte est réutilisé |
| Durée de conservation | Copie locale conservée tant que le projet existe ; régénérable à partir de la source |
| Redistribution | Aucune. Aucun contenu de Lexicanum n'est utilisé à ce jour : pas de phrase d'attribution dans le README tant que l'accord n'est pas obtenu |
| Conformité RGPD | Pas de donnée personnelle collectée, donc pas de traitement au sens du RGPD pour cette source |

## 9. Lineage

| Champ | Valeur |
| --- | --- |
| Sources amont | Matériel officiel Games Workshop : codex, romans Black Library, White Dwarf |
| Destinations aval | Aucune en l'état. Si l'accord est obtenu : `data/raw/` → `raw` dans DuckDB → staging (lexique normalisé, alias) → `dim_entity` → correspondance avec le texte EPUB → plugin Pokédex KOReader |
| Transformations | Titres via `list=allpages`, redirections via `list=allredirects`, catégories via `list=categorymembers` ; retrait des précisions entre parenthèses ; filtrage des pages hors entités ; type par branche de catégorie |

## 10. Décisions et questions ouvertes

| Date | Décision ou question | Statut |
| --- | --- | --- |
| 28/10/2026 | Lexicanum envisagé comme source du lexique v0.1 (couverture de 50 220 articles, API autorisée par le robots.txt) | Abandonné |
| 28/10/2026 | Les conditions d'utilisation (§4, §5) interdisent la construction d'une base et l'extraction en masse sans accord écrit : Lexicanum passe en attente | Décidé |
| 28/10/2026 | Demande d'accord écrit aux administrateurs (Discord ou page des administrateurs), avec l'estimation de charge et l'usage non commercial | Reportée en V2 (issue « Ask the wiki administrators for automated access ») ; non envoyée |
| 28/10/2026 | En parallèle : lire les conditions d'utilisation de Fandom et de wiki.gg avant d'en retenir un | Fait : Fandom non retenu, wiki.gg retenu sous forme restreinte |

## Historique de la fiche

| Version | Date | Modification |
| --- | --- | --- |
| 1 | 28/10/2026 | Création |
| 2 | 28/10/2026 | Conditions d'utilisation (§3, §4, §5, §6, §13) ; décision passée en attente ; propriétaire identifié |
| 3 | 28/10/2026 | Décision reportée en V2 ; demande d'accord non envoyée |
