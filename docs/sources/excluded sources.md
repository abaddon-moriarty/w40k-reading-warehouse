# Sources écartées ou reportées

Sources inventoriées à l'étape 2 qui ne reçoivent pas de fiche complète pour la v0.1. Une source sans question à servir est écartée (minimisation) ; l'écart est documenté pour pouvoir y revenir.

| Source | Type | Décision | Raison | Date | À revoir quand |
|---|---|---|---|---|---|
| Black Library (site de l'éditeur) | Site web | Écartée | Contenu sous droits, sans licence ouverte ; aucune des questions de `docs/questions.md` n'en a besoin | 28/10/2026 | Si une question porte un jour sur les dates ou l'ordre de publication officiels |
| Vocabulary Builder (KOReader) | Base locale SQLite (`vocabulary`, `title`) | Écartée en v0.1 | Aucune des cinq questions ne l'utilise | 28/10/2026 | Si le Pokédex affiche un jour les mots relevés pendant la lecture |
| Métadonnées `.sdr` (KOReader) | Fichiers Lua par livre (surlignages, notes, signets, positions, statut de lecture) | Reportée en V2 | Nécessaire pour la position de lecture (question 5) | 28/10/2026 | V2. **Peut-être plus tôt** : le statut « fini » d'un livre s'y trouve peut-être, alors que la v0.1 en a besoin (voir la fiche KOReader) |
| Warhammer 40k Wiki (Fandom) | Wiki MediaWiki | Évaluée, non retenue en v0.1 | 7 322 articles contre 50 220 sur Lexicanum ; API autorisée, licence CC BY-SA | 28/10/2026 | V2, comme source d'alias complémentaire |
| Warhammer 40k Wiki (wiki.gg) | Wiki MediaWiki | Évaluée, non retenue en v0.1 | API interdite aux robots par le robots.txt ; seuls le sitemap et des exports manuels sont possibles | 28/10/2026 | Si les administrateurs autorisent un accès à l'API |

Fiches complètes de Fandom et wiki.gg : `fandom.md`, `wiki_gg.md` (gardées pour la traçabilité de la décision).
