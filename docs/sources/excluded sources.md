# Sources écartées ou reportées

Sources inventoriées à l'étape 2 qui ne reçoivent pas de fiche complète pour la v0.1. Une source sans question à servir est écartée (minimisation) ; l'écart est documenté pour pouvoir y revenir.

| Source | Type | Décision | Raison | Date | À revoir quand |
|---|---|---|---|---|---|
| Black Library (site de l'éditeur) | Site web | Écartée | Contenu sous droits, sans licence ouverte ; aucune des questions de `docs/questions.md` n'en a besoin | 28/10/2026 | Si une question porte un jour sur les dates ou l'ordre de publication officiels |
| Vocabulary Builder (KOReader) | Base locale SQLite (`vocabulary`, `title`) | Écartée en v0.1 | Aucune des cinq questions ne l'utilise | 28/10/2026 | Si le Pokédex affiche un jour les mots relevés pendant la lecture |
| Métadonnées `.sdr` (KOReader) | Fichiers Lua par livre (surlignages, notes, signets, positions, statut de lecture) | **Partiellement retenue en v0.1** : seul le statut de lecture (« fini ») et sa date ; le reste reporté en V2 | Le statut « fini » est nécessaire aux questions 1 à 3 ; les positions servent la question 5 (V2) ; surlignages et notes écartés par minimisation | 28/10/2026 | V2, pour les positions de lecture |
| Warhammer 40k Wiki (Fandom) | Wiki MediaWiki | **Non retenue en l'état** | API autorisée par le robots.txt et texte sous CC BY-SA, mais les Terms of Use (19/12/2025) interdisent tout accès automatisé et toute extraction sans autorisation écrite | 28/10/2026 | Si Fandom, Inc. accorde une autorisation écrite |
| Warhammer 40k Lexicanum | Wiki MediaWiki | **Reportée en V2** | 50 220 articles et API autorisée par le robots.txt, mais les conditions d'utilisation interdisent de construire une base de données (§4(a)) et l'extraction en masse sans accord écrit (§5) ; le contenu de l'API n'est pas sous CC BY-NC (§3(b)) | 28/10/2026 | En V2, avec la demande d'accord écrit (non envoyée) |
| Pages de termes génériques de wiki.gg (Generic Terms, Titles and Ranks, Tactics, Languages, List of Terms) | Catégories et page de liste | **Reportées en V+** | Noms communs : en correspondance exacte, fausses apparitions partout. Utiles pour un glossaire (définitions affichées, pas d'entités débloquées), qui demande le texte des articles | 28/10/2026 | Quand l'accès aux wikis est accordé |
| Sitemap de wiki.gg comme lexique | Fichiers XML (titres et dates) | **Écarté comme lexique, retenu comme référentiel de contrôle** | Ni type ni catégorie, avec œuvres et désambiguïsations : inutilisable seul. Sert à mesurer la couverture des exports | 28/10/2026 | Sans objet |

Fiches complètes : `lexicanum.md`, `fandom.md` (gardées pour la traçabilité des décisions). wiki.gg est retenu sous forme restreinte pour la v0.1 : voir `wiki_gg.md`.

Lexique v0.1 : noms des pages d'une dizaine d'exports XML manuels de wiki.gg, sans texte d'article (`wiki_gg.md`, §10). Demande d'accès automatisé aux wikis en V1/V2.
