# Fiche d'identité - Warhammer 40k Wiki (wiki.gg)

> **Métadonnées de la fiche**
>
> - Rédacteur : Marine Prost
> - Date de création / dernière mise à jour : 28/10/2026
> - Version : 4
> - Statut : brouillon (conditions d'utilisation vérifiées le 28/10/2026)
> - Décision : **retenue pour la v0.1, sous forme restreinte et avec un risque assumé** (voir §10) : une dizaine d'exports XML manuels par catégorie de série (Special:Export dans le navigateur), dans l'ordre de lecture ; l'entrepôt ne charge que le titre, l'identifiant et les catégories de chaque page ; aucun texte d'article chargé ni affiché ; rien de publié ; pas de collecte automatisée. Demande d'accord en V1/V2
> - Questions servies : 1 à 4 (`docs/questions.md`), pour les éléments « nom de l'entité », « type » et « alias »

## 1. Identité

| Champ | Valeur |
| --- | --- |
| Nom | Warhammer 40k Wiki |
| Identifiant unique (slug) | `warhammer40k_en` (identifiant renvoyé par l'API, `wikiid`) |
| URL principale | <https://warhammer40k.wiki.gg/wiki/> (alias : <https://40k.wiki/>) |
| Description (1–2 phrases) | Warhammer 40k Wiki is a community-built encyclopedia dedicated to four decades of Warhammer 40,000 lore, from 1987's Rogue Trader right up to today's games, models, books and shows. |
| Domaine métier | Univers fictionnel / jeu de figurines / produits dérivés (romans, jeux vidéo) |
| Langue(s) | Anglais (`lang: en`) |
| Public cible | Fans de Warhammer 40k, lecteurs de lore, joueurs |

## 2. Technique

| Champ | Valeur |
| --- | --- |
| Plateforme | MediaWiki 1.43.6, hébergé par wiki.gg (vérifié par `meta=siteinfo` le 28/10/2026) |
| Format natif | Wikitext ; HTML rendu |
| API | Oui : MediaWiki Action API, <https://warhammer40k.wiki.gg/api.php>, sans authentification. **Interdite aux robots par le robots.txt** (voir §5). `Special:ApiSandbox` n'est qu'une interface pour composer les requêtes à la main |
| Dumps / exports | Pas de dump public identifié. `Special:Export` disponible (vérifié le 28/10/2026 : export de `Category:Background`, puis de `Category:Eisenhorn (Novel Series)`). L'export d'une catégorie ne prend que ses membres directs, pas ses sous-catégories. Le fichier XML contient, pour chaque page : titre, espace de noms, `page_id`, dernière révision avec le wikitext complet et le nom du contributeur |
| Sitemap | Index : <https://warhammer40k.wiki.gg/sitemaps/sitemap-index-warhammer40k_en.xml>. Autorisé aux robots. Chaque URL a sa date de dernière modification. L'index liste 3 fichiers (téléchargés à la main le 28/10/2026) : `NS_0-0` (50 000 pages) et `NS_0-1` (562 pages, de « Yored Massak » à « Λ-34-Eliptyka ») pour l'espace principal, soit **50 561 pages** ; `NS_14-0` pour les **2 940 catégories** (liste des noms, sans leurs membres). 6 715 titres ont une précision entre parenthèses (1 260 « disambiguation », 804 « Short Story », 485 « Novel », 68 « Novel Series »…). La liste des catégories contient 17 catégories `(Novel Series)` et, par faction, des catégories nommées `<Faction> characters`, `weapons`, `vehicles`, `equipment`, `fleet`, `troops`, `battles`, `images`, `miniatures`, `formations`, `sources` (les lettres C, W, V… de l'arbre des catégories). **Usage retenu : référentiel de contrôle de la couverture** (titres sans type ni catégorie, avec œuvres et désambiguïsations, donc inutilisable seul comme lexique) ; fichiers téléchargés à la main, datés |
| Localisation | URL de type `https://warhammer40k.wiki.gg/wiki/{Titre}` (espaces remplacés par `_`, caractères spéciaux encodés) |
| Clés disponibles | Via l'API : `page_id` (stable), `revision_id` (stable). Via le sitemap : **le titre seulement** (non stable, soumis aux renommages) et `lastmod`. `max-page-id` = 123 392 au 28/10/2026 |
| Structure | Infoboxes via templates, catégories MediaWiki, pages de contenu, pages de désambiguïsation (suffixe « (disambiguation) »), pages méta (`Meta:`) |
| Fuseau horaire | UTC (`timezone: UTC`) |

## 3. Provenance

| Champ | Valeur |
| --- | --- |
| Système producteur | Communauté de bénévoles (éditeurs, administrateurs, bots) |
| Date de création | À vérifier. Le sitemap contient des dates de modification remontant à 2012, et la page d'accueil daterait du 2 mai 2005 : ces dates viennent probablement d'un historique importé d'un wiki antérieur, et ne disent pas quand ce wiki a ouvert sur wiki.gg |
| Origine | Créé par des éditeurs venus de Lexicanum (page `Meta:Why_we_are_moving_from_Lexicanum`) ; lien avec le Total War Wiki à vérifier |

## 4. Propriété

| Champ | Valeur |
| --- | --- |
| Data owner | Équipe d'administration du wiki et sa communauté ; wiki.gg comme hébergeur (société exploitante à vérifier) |
| Data steward (projet) | Marine Prost |
| Équipe responsable | Bénévoles, administrateurs du wiki |
| Contact | À identifier : page de discussion des administrateurs ou Discord du wiki (pour la demande d'autorisation d'accès automatisé) |

## 5. Opérationnel

| Champ | Valeur |
| --- | --- |
| Mode d'accès retenu (v0.1) | Exports XML manuels par catégorie (`Special:Export`, dans le navigateur), en nombre limité, chacun daté et noté dans le Journal des décisions. Les fichiers vont dans `data/raw/` et sont lus en local. Le script de chargement ne garde que le titre, l'identifiant de page, l'espace de noms, la catégorie d'export et les catégories de la page (lues dans les liens `[[Category:…]]` du wikitext, puis le texte est ignoré) ; le texte des articles et les contributeurs ne sont jamais chargés. Les fichiers XML restent dans `data/raw/wiki_gg/`, non commités. Chaque export est noté dans le seed local `wiki_exports.csv` (catégorie, date, nombre de pages, livre déclencheur). Aucun script ne contacte le wiki |
| Robots.txt (vérifié le 28/10/2026) | Bloc wiki.gg : `Disallow` sur `/api.php`, `/index.php`, `/rest.php`, `/wiki/Special:`, `/wiki/User:`, et sur les paramètres `?action=`, `?pagefrom=`, `?limit=`… Bloc Cloudflare : `Allow: /` avec le signal de contenu `search=yes, ai-train=no, use=reference`, présenté comme réserve de droits (article 4, directive UE 2019/790). Avertissement : accès restreint en cas de trafic automatisé abusif |
| Demande d'autorisation | Reportée en V1/V2 (décision du 28/10/2026, §10) : extraction ponctuelle via l'API (volume, User-Agent identifiable, requêtes une par une). Date d'envoi : non envoyée |
| Conditions d'utilisation (Terms of Service de Freedom Games / indie.io, couvrant wiki.gg, modifiées le 01/04/2026, consultées le 28/10/2026) | Section *Restrictions* : interdiction d'« use manual or automated software, devices, or other processes to "crawl," "scrape," or "spider" any part of the Services ». Section *Usage Rights* : « You may not use content from our Services unless otherwise agreed in writing, as explicitly communicated on a Service by Company, or as otherwise permitted by law » ; la licence CC BY-NC affichée par le wiki relève du « explicitly communicated on a Service ». **Le texte est réutilisable sous CC BY-NC, mais sa collecte, automatisée ou par un procédé manuel systématique, est interdite sans accord écrit.** Une lecture stricte de « manual (…) processes » peut viser une série d'exports manuels. Le projet assume ce risque pour une dizaine d'exports, dans les conditions décrites au §10 |
| Fréquence de mise à jour | Continue (éditions communautaires) |
| Fraîcheur | `lastmod` par page dans le sitemap (dernière modification observée : 27/10/2026) |
| Volumétrie au 28/10/2026 | 117 926 pages tous espaces de noms confondus, 856 486 éditions depuis la création (Special:Statistics) ; 50 561 pages dans l'espace principal et 2 940 catégories (sitemap complet) |
| SLA / limites | Aucun SLA. Limite de débit de l'API non documentée publiquement (à vérifier dans les conditions de wiki.gg) |

## 6. Couverture

| Champ | Valeur |
| --- | --- |
| Granularité | Page (article) ; section ou champ d'infobox accessibles en analysant le wikitext |
| Catégories de série | Les entités d'une série de romans sont rangées dans une catégorie dédiée, ex. `Category:Eisenhorn (Novel Series)` : 102 pages le 28/10/2026, dont 12 œuvres (romans, nouvelles, livre audio, numéro d'*Inferno!*) et 90 entités candidates. Elle couvre toute la série, pas un seul livre. Les 102 pages sont toutes dans le sitemap. Absents du wiki lui-même (ni page ni titre au sitemap, 28/10/2026) : Lowink, le vaisseau *Essene* ; ils ne peuvent venir que d'un ajout manuel ou d'une autre source |
| Profondeur d'historique | MediaWiki conserve toutes les révisions ; accessibles par l'API (`prop=revisions`) et par l'historique de chaque page, mais ces deux voies sont interdites aux robots. Hors besoin pour la v0.1 |
| Couverture thématique | Lore Warhammer 40,000 (depuis Rogue Trader, 1987), jeux de plateau, jeux vidéo, romans (pages « (Novel) », « (Short Story) », « (Anthology) »…), médias |
| Couverture temporelle (in-universe) | 30k (Horus Heresy), 40k et ères associées |
| Couverture des personnages de ma bibliothèque (sondage, 28/10/2026) | Présents dans le sitemap : Ciaphas Cain, Amberley Vail, Gregor Eisenhorn, Gideon Ravenor, Alizebeth Bequin, Uriel Ventris, Valhallan 597th, Ferik Jurgen, Uber Aemos. Absents sous leur nom court (« Cain », « Eisenhorn », « Jurgen », « Heldane », « Aemos ») : le sitemap n'inclut pas les redirections. Absents du wiki lui-même : Lowink, *Essene* (voir la ligne Catégories de série) |

## 7. Qualité

| Champ | Valeur |
| --- | --- |
| Complétude | 50 561 pages dans l'espace principal (sitemap complet, 28/10/2026 ; 117 926 pages tous espaces de noms confondus d'après Special:Statistics). Ce chiffre inclut des pages qui ne sont pas des entités : 6 715 titres ont une précision entre parenthèses, dont 1 260 pages de désambiguïsation, 804 nouvelles et 485 romans. Ordre de grandeur comparable à Lexicanum (50 220 articles, `meta=siteinfo`, 28/10/2026). Sondage sur ma bibliothèque et entités absentes du wiki : voir §6. Part des entités de mes livres présentes : à mesurer |
| Alias | **Ni le sitemap ni les exports ne contiennent les redirections** : les noms courts (« Cain ») manquent, alors qu'ils sont essentiels à la correspondance exacte. Les titres sont souvent des noms complets jamais écrits tels quels dans les livres (`Golesh Constantine Pheppos Heldane`, `Uber Aemos`, `Plebas Alessandro Rorken`) ; *Xenos* est narré à la première personne, « Gregor Eisenhorn » y est rare. Palliatif v0.1 : seed d'alias manuel `entity_alias.csv` |
| Titres avec précision entre parenthèses | 6 715 titres sur 50 561 (sitemap complet), dont 1 260 pages de désambiguïsation, 804 « (Short Story) », 485 « (Novel) », 68 « (Novel Series) » : à retirer avant la recherche, et à filtrer du lexique pour les pages qui ne sont pas des entités |
| Mots courants en titre | Présents (ex. « Blank » ; dans la catégorie *Eisenhorn* : « Hubris », « Distaff », « Pylon », « Loki », « Xenophile ») : risque de fausses apparitions, mesuré après la correspondance (nombre de livres, apparitions en minuscule) |
| Types hors périmètre | Les catégories de série mélangent personnages, lieux, objets, mais aussi groupes (`House Glaw`, `Divine Fratery`, `Gudrunite 50th Rifles`) et concepts (`Meme-Virus`) : décision à prendre (sixième type « groupe » ou exclusion) |
| Cohérence | Politique éditoriale centrée sur le lore canon et les médias (à vérifier sur les pages de règles du wiki) |
| Risque | Vandalisme, guerres d'édition, renommages de pages (le titre n'est pas une clé stable) |
| Citations | Les articles citent généralement leurs sources (codex, romans, White Dwarf) ; à vérifier article par article |

## 8. Gouvernance

| Champ | Valeur |
| --- | --- |
| Données personnelles | Présentes dans l'historique des pages (noms d'utilisateurs, adresses IP des éditions anonymes). Les fichiers d'export contiennent, pour chaque page, le nom du dernier contributeur et le wikitext complet : ils restent dans `data/raw/wiki_gg/` (local, non commité) et **ne sont jamais chargés dans l'entrepôt** (minimisation au chargement). Ni l'historique ni les contributeurs ne sont collectés au-delà de ces fichiers |
| Sensibilité | Contenu de fans dérivé de la propriété intellectuelle de Games Workshop ; noms, marques et images appartiennent à Games Workshop et à ses licenciés |
| Licence | **CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial 4.0), déclarée par le wiki lui-même (`meta=siteinfo`, `rightsinfo`, 28/10/2026) |
| Restrictions d'usage | Pas d'usage commercial ; attribution obligatoire ; accès automatisé à l'API interdit par le robots.txt ; signal `ai-train=no` |
| Durée de conservation | Copie locale conservée tant que le projet existe ; régénérable à partir de la source |
| Redistribution | Aucune : exports, sitemap et seeds tirés du wiki (types, alias, exclusions) restent dans `data/` (ignoré par Git). La licence CC BY-NC permettrait de publier les noms avec attribution, mais la méthode de collecte relève d'un risque assumé : rien n'est publié tant que l'accord n'est pas obtenu. Le README cite la source et sa licence |
| Conformité RGPD | Noms de contributeurs présents dans les fichiers d'export locaux, jamais chargés ni publiés. Option : retirer les balises `<contributor>` des fichiers juste après l'export |

## 9. Lineage

| Champ | Valeur |
| --- | --- |
| Sources amont | Codex Games Workshop, romans Black Library, White Dwarf ; wikis antérieurs (Lexicanum), dont viennent une partie des éditeurs |
| Destinations aval | `data/raw/wiki_gg/` (exports XML, sitemap) → `raw.wiki_pages`, `raw.wiki_page_categories` → `stg_wiki_pages` → `int_entity_lexicon` (avec les seeds `category_type_map`, `entity_alias`, `lexicon_exclusions`) → correspondance avec le texte EPUB → `dim_entity`, `fact_entity_appearance` → plugin Pokédex KOReader |
| Transformations | Underscores remplacés par des espaces ; précision entre parenthèses retirée du nom cherché et gardée à part (`qualifier`) ; œuvres et pages hors entités marquées (`is_work`, seed d'exclusions), jamais supprimées ; type attribué par le seed `category_type_map` à partir des catégories de la page, avec une règle de priorité ; alias ajoutés par le seed manuel (redirections en V1/V2) |

## 10. Décisions et questions ouvertes

| Date | Décision ou question | Statut |
| --- | --- | --- |
| 28/10/2026 | v0.1 : lexique tiré de quelques exports XML manuels, noms seulement ; demande d'accès automatisé en V1/V2 | Décidé |
| 28/10/2026 | **Risque assumé.** Les conditions interdisent de « crawl, scrape, spider » le service, y compris par des procédés manuels ; une lecture stricte peut viser une série d'exports. Le projet estime qu'une dizaine d'exports faits à la main avec une fonction prévue par le site (`Special:Export`), sans script, à un rythme humain, pour un usage personnel non commercial, n'est pas du crawl, sans en avoir la certitude. Conditions : nombre d'exports limité et journalisé (`wiki_exports`) ; aucun automatisme ; titres et catégories seulement chargés ; rien de publié ; arrêt et suppression des exports si le wiki ou l'éditeur le demande ; demande d'accord en V1/V2 | Décidé |
| 28/10/2026 | Seeds tirés du wiki (types, alias, exclusions, journal des exports) gardés en local dans `data/seeds/`, non versionnés ; seuls leur structure, leurs tests et des exemples inventés sont dans le dépôt | Décidé |
| 28/10/2026 | Exporter par catégorie de série, dans l'ordre de lecture (*Eisenhorn* en premier), plutôt que par faction | Décidé |
| 28/10/2026 | Sitemap complet : référentiel de contrôle de la couverture, pas lexique | Décidé |
| 28/10/2026 | Séries de ma bibliothèque couvertes par une catégorie `(Novel Series)` : Eisenhorn, Ravenor, Bequin, Ciaphas Cain, Inquisitor, Ultramarines, Iron Warriors, Grey Knights, Soul Drinkers, Tome of Fire ; une dizaine d'exports suffit pour la v0.1 | Constat, à confirmer série par série |
| 28/10/2026 | Pages de termes génériques (Generic Terms, Titles and Ranks, Tactics, Languages, List of Terms) exclues du lexique d'entités ; glossaire en V+ | Décidé |
| 28/10/2026 | Aucune correction à la main dans les données : chaque règle (type, alias, exclusion) est une règle explicite, tenue à la main dans un seed, ou du code | Décidé |
| 28/10/2026 | Groupes et organisations : sixième type ou exclusion ? | Ouverte |

## Historique de la fiche

| Version | Date | Modification |
| --- | --- | --- |
| 1 | 28/10/2026 | Création |
| 2 | 28/10/2026 | Conditions d'utilisation vérifiées ; export par catégorie de série, sitemap comme référentiel de contrôle, constats sur la catégorie *Eisenhorn*, seeds du lexique |
| 3 | 28/10/2026 | Risque assumé documenté ; chiffres du sitemap complet partout ; contributeurs présents dans les fichiers locaux ; seeds en local |
| 4 | 28/10/2026 | Sondage regroupé au §6 ; « règle explicite » au lieu de « seed versionné » |
