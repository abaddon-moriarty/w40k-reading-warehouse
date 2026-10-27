# Analytical questions

The warehouse exists to answer these questions. Every source, table and test must serve at least one of them; a source or column that serves none is left out.

## Definitions (v0.1)

- **Entity**: a page title found in the category tree of the wikis (warhammer40k.wiki.gg, Lexicanum), plus its redirects as aliases. Its **type** (character, place, object, weapon, ship) comes from the branch of the category tree it was found in.
- **Appearance**: the entity's name (page title or alias) found exactly as written in the text of an EPUB file. This is dictionary matching, not NER: a mention counts as an appearance, pronouns are ignored.
- **Book**: one EPUB file. An omnibus is one book in v0.1; splitting it into works comes in V2.
- **Read**: a book is read when KOReader reports it as finished. Reading order is the order of the finishing dates.

## Questions

| # | Question | What it drives | Changes over time? | Answered in |
|---|---|---|---|---|
| 1 | In which books does an entity (character, place, object, weapon, ship) appear, and what is the **first book in my reading order** where it appears? | Unlock its card in the Pokédex | Yes: the list of books grows with each read; the book that introduced the entity is fixed once read | v0.1 |
| 2 | Which entities have I unlocked so far, and which remain locked? | State of the Pokédex: visible / greyed-out cards | Yes: each finished book unlocks new entities | v0.1 |
| 3 | Which unread book would unlock the most new entities? | Choosing the next book | Yes: depends on what I have read and on the books in my library | v0.1 |
| 4 | Which entities come back from one series to another? | Links between series | Yes, when a book is added; reading progress does not change it | v0.1 |
| 5 | At my current position in a book, what have I already met about an entity? | What the Pokédex may show without spoilers | Yes: the reading position is the clock | V2 |

## Scope of v0.1

- Grain: **entity × book**. An entity is unlocked when a book in which it appears is finished, not at the exact page.
- Entities: characters, places, objects, weapons and ships, all through the same method. An entity listed under several branches of the category tree gets one type by a priority rule.
- Out of scope, planned for V2: position inside a book (question 5), splitting omnibuses into works, a finer NER (coreference, short names without a redirect).

Known limits of exact matching (homonyms such as "Blank", names with a disambiguation in brackets, short names, possessives) are listed in the project tracking document with the planned fix for each.
