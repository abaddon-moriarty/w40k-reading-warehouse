# Fiche d'identité - Warhammer 40k Wiki (wiki.gg)

> **Métadonnées de la fiche**
> - Rédacteur : Marine Prost
> - Date : 28/10/2026
> - Version : 1
> - Statut : brouillon
> - Questions servies : 1 à 4 (`docs/questions.md`), pour les éléments « nom de l'entité », « type » et « alias »

## 1. Identité
| Champ | Valeur |
|---|---|
| Nom | Warhammer 40k Wiki |
| Identifiant unique (slug) | `warhammer40k_en` (identifiant renvoyé par l'API, `wikiid`) |
| URL principale | https://warhammer40k.wiki.gg/wiki/ (alias : https://40k.wiki/) |
| Description (1–2 phrases) | Warhammer 40k Wiki is a community-built encyclopedia dedicated to four decades of Warhammer 40,000 lore, from 1987's Rogue Trader right up to today's games, models, books and shows. |
| Domaine métier | Univers fictionnel / jeu de figurines / produits dérivés (romans, jeux vidéo) |
| Langue(s) | Anglais (`lang: en`) |
| Public cible | Fans de Warhammer 40k, lecteurs de lore, joueurs |

## 2. Technique
| Champ | Valeur |
|---|---|
| Plateforme | MediaWiki 1.43.6, hébergé par wiki.gg (vérifié par `meta=siteinfo` le 28/10/2026) |
| Format natif | Wikitext ; HTML rendu |
| API | Oui : MediaWiki Action API, https://warhammer40k.wiki.gg/api.php, sans authentification. **Interdite aux robots par le robots.txt** (voir §5). `Special:ApiSandbox` n'est qu'une interface pour composer les requêtes à la main |
| Dumps / exports | Pas de dump public identifié. `Special:Export` (export XML par catégorie, à la main dans le navigateur) : disponibilité à vérifier |
| Sitemap | Index : https://warhammer40k.wiki.gg/sitemaps/sitemap-index-warhammer40k_en.xml. Autorisé aux robots. Le fichier `sitemap-warhammer40k_en-NS_0-0.xml` (espace de noms principal) contient 50 000 URL avec leur date de dernière modification, de « "Blackblade" Wood » à « Yorac » : il y a donc au moins un fichier suivant pour la fin de l'alphabet |
| Localisation | URL de type https://warhammer40k.wiki.gg/wiki/<Titre> (espaces remplacés par `_`, caractères spéciaux encodés) |
| Clés disponibles | Via l'API : `page_id` (stable), `revision_id` (stable). Via le sitemap : **le titre seulement** (non stable, soumis aux renommages) et `lastmod`. `max-page-id` = 123 392 au 28/10/2026 |
| Structure | Infoboxes via templates, catégories MediaWiki, pages de contenu, pages de désambiguïsation (suffixe « (disambiguation) »), pages méta (`Meta:`) |
| Fuseau horaire | UTC (`timezone: UTC`) |

## 3. Provenance
| Champ | Valeur |
|---|---|
| Système producteur | Communauté de bénévoles (éditeurs, administrateurs, bots) |
| Date de création | À vérifier. Le sitemap contient des dates de modification remontant à 2012, et la page d'accueil daterait du 2 mai 2005 : ces dates viennent probablement d'un historique importé d'un wiki antérieur, et ne disent pas quand ce wiki a ouvert sur wiki.gg |
| Origine | Créé par des éditeurs venus de Lexicanum (page `Meta:Why_we_are_moving_from_Lexicanum`) ; lien avec le Total War Wiki à vérifier |

## 4. Propriété
| Champ | Valeur |
|---|---|
| Data owner | Équipe d'administration du wiki et sa communauté ; wiki.gg comme hébergeur (société exploitante à vérifier) |
| Data steward (projet) | Marine Prost |
| Équipe responsable | Bénévoles, administrateurs du wiki |
| Contact | À identifier : page de discussion des administrateurs ou Discord du wiki (pour la demande d'autorisation d'accès automatisé) |

## 5. Opérationnel
| Champ | Valeur |
|---|---|
| Mode d'accès retenu (v0.1) | **Sans accès automatisé à l'API.** Titres des pages : sitemap (téléchargement ponctuel, autorisé). Catégories et types : `Special:Export` par catégorie, à la main dans le navigateur, si disponible. Les fichiers obtenus sont rangés dans `data/raw/` et lus en local |
| Robots.txt (vérifié le 28/10/2026) | Bloc wiki.gg : `Disallow` sur `/api.php`, `/index.php`, `/rest.php`, `/wiki/Special:`, `/wiki/User:`, et sur les paramètres `?action=`, `?pagefrom=`, `?limit=`… Bloc Cloudflare : `Allow: /` avec le signal de contenu `search=yes, ai-train=no, use=reference`, présenté comme réserve de droits (article 4, directive UE 2019/790). Avertissement : accès restreint en cas de trafic automatisé abusif |
| Demande d'autorisation | À envoyer aux administrateurs, pour une extraction ponctuelle via l'API (volume, User-Agent identifiable, requêtes une par une). Date d'envoi : [à compléter] |
| Fréquence de mise à jour | Continue (éditions communautaires) |
| Fraîcheur | `lastmod` par page dans le sitemap (dernière modification observée : 27/10/2026) |
| Volumétrie au 28/10/2026 | 117 926 pages tous espaces de noms confondus, 856 486 éditions depuis la création (Special:Statistics) ; au moins 50 000 pages dans l'espace principal (sitemap) |
| SLA / limites | Aucun SLA. Limite de débit de l'API non documentée publiquement (à vérifier dans les conditions de wiki.gg) |

## 6. Couverture
| Champ | Valeur |
|---|---|
| Granularité | Page (article) ; section ou champ d'infobox accessibles en analysant le wikitext |
| Profondeur d'historique | MediaWiki conserve toutes les révisions ; accessibles par l'API (`prop=revisions`) et par l'historique de chaque page, mais ces deux voies sont interdites aux robots. Hors besoin pour la v0.1 |
| Couverture thématique | Lore Warhammer 40,000 (depuis Rogue Trader, 1987), jeux de plateau, jeux vidéo, romans (pages « (Novel) », « (Short Story) », « (Anthology) »…), médias |
| Couverture temporelle (in-universe) | 30k (Horus Heresy), 40k et ères associées |
| Couverture des personnages de ma bibliothèque (sondage) | Présents dans le sitemap : Ciaphas Cain, Amberley Vail, Gregor Eisenhorn, Gideon Ravenor, Alizebeth Bequin, Uriel Ventris, Valhallan 597th, Xenos (Novel). Absents sous leur nom court : « Cain », « Eisenhorn », « Jurgen » (probablement des redirections, que le sitemap n'inclut pas) |

## 7. Qualité
| Champ | Valeur |
|---|---|
| Complétude | Wiki récent (en construction). La complétude est probablement inférieure à Lexicanum (qui revendique ~34 000 articles) et au wiki Fandom, mais la qualité éditoriale se veut supérieure (équipe expérimentée). |
| Alias | **Le sitemap ne contient pas les redirections** : les noms courts (« Cain ») manquent, alors qu'ils sont essentiels à la correspondance exacte |
| Titres avec précision entre parenthèses | 6 807 titres sur 50 000 dans le premier fichier du sitemap, dont 1 247 pages de désambiguïsation, 802 « (Short Story) », 484 « (Novel) » : à retirer avant la recherche, et à filtrer du lexique pour les pages qui ne sont pas des entités |
| Mots courants en titre | Présents (ex. « Blank ») : risque de fausses apparitions |
| Cohérence | Politique éditoriale axée sur le lore canon et les médias, excluant les règles de jeu (comme sur Fandom). Risque de spéculation fan à surveiller. |
| Fraîcheur | Mise à jour communautaire continue. |
| Risque | Vandalisme, guerres d'édition, renommages de pages (le titre n'est pas une clé stable) |
| Citations | Les articles citent généralement leurs sources (codex, romans, White Dwarf) ; à vérifier article par article |

## 8. Gouvernance
| Champ | Valeur |
|---|---|
| Données personnelles | Présentes dans l'historique des pages (noms d'utilisateurs, adresses IP des éditions anonymes). **Non collectées** : le projet ne récupère ni l'historique ni les contributeurs (minimisation) |
| Sensibilité | Contenu de fans dérivé de la propriété intellectuelle de Games Workshop ; noms, marques et images appartiennent à Games Workshop et à ses licenciés |
| Licence | **CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial 4.0), déclarée par le wiki lui-même (`meta=siteinfo`, `rightsinfo`, 28/10/2026) |
| Restrictions d'usage | Pas d'usage commercial ; attribution obligatoire ; accès automatisé à l'API interdit par le robots.txt ; signal `ai-train=no` |
| Durée de conservation | Copie locale conservée tant que le projet existe ; régénérable à partir de la source |
| Redistribution | Aucune : les données extraites restent dans `data/` (ignoré par Git) ; le README cite la source et sa licence |
| Conformité RGPD | Pas de donnée personnelle collectée, donc pas de traitement au sens du RGPD pour cette source |

## 9. Lineage
| Champ | Valeur |
|---|---|
| Sources amont | Codex Games Workshop, romans Black Library, White Dwarf ; wikis antérieurs (Lexicanum), dont viennent une partie des éditeurs |
| Destinations aval | `data/raw/` (sitemap, exports XML) → `raw` dans DuckDB → staging (lexique normalisé : titres sans précision entre parenthèses, filtrage des pages hors entités) → `dim_entity` → correspondance avec le texte EPUB → plugin Pokédex KOReader |
| Transformations | Décodage des URL en titres, retrait des précisions entre parenthèses, filtrage (désambiguïsation, œuvres, listes), attribution du type par la branche de catégorie, ajout des alias (redirections, si une voie d'accès est trouvée) |
