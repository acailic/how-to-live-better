# TRANSLATING.md — adding a language, refreshing the snapshot

This is the in-repo guide for anyone translating the book into another
language and for refreshing the vendored snapshot. The English, German,
Russian, and Serbian translations all ship complete in this repository
(34 sections / 676 entries each); the English translation (`content/en/`) is
the primary reference implementation, with German (`content/de/`), Russian
(`content/ru/`), and Serbian (`content/sr/`) as further reference
implementations to follow.

## How the multilingual build works

- **One content directory per language**: `content/<lang>/NN-<slug>.md`,
  mirroring the Chinese section numbering (`01-` … `34-`). File names only
  need the leading `NN-`; the rest of the name is free (use your language's
  slug). Chinese is `content/zh/` — the vendored snapshot, never edited.
- **`build.py` LANGS** maps a language code to everything the renderer
  needs: which field keywords your `.md` files use, which tag tokens, every
  UI string, and how they display. Adding a language = adding one LANGS
  entry + a content directory; `python3 build.py` then builds
  `<lang>/index.html` automatically and lists the language in the landing
  page and the switcher.
- **Canonical values are English internally**: `money=low`, `benefit=large`,
  `metric=mortality`, value tiers `vhigh/high/avg`. The LANGS entry maps
  *your* file tokens (German `Geld=wenig`, …) to the canonical ones, and
  canonical ones to display strings. Never re-derive tiers — the build
  recomputes them from the tags, and `tools/check_translation.py` verifies
  the result matches the Chinese original per entry.

## Content file format (per entry)

Copy the Chinese grammar with your localized keywords:

```
### 1. Title
<!-- costs: money=none time=low will=no benefit=large metric=mortality -->
- Cost: ...
- In plain terms: ...
- Benefit: ...
- Evidence grade: A
- Sources: <citation> <https://doi.org/...>
- Note: ...
```

Tag tokens (the `<!-- costs: ... -->` comment) — pick yours in the LANGS
entry; these are the English ones:

| canonical | tokens |
|---|---|
| money | none / low / high |
| time | low / medium / high |
| will | no / some / yes |
| benefit | large / medium / small |
| metric | mortality / money / time / freedom |

Rules that keep parity with the Chinese original:

1. **Same entry numbers and section count** — 34 sections, 676 entries,
   numbering untouched. Anchor ids (`s16-9`) are shared across languages, so
   cross-references like "see Section 6, item 21" stay aligned.
2. **Evidence grades (A/B/C) copied verbatim**, including annotations like
   "A (disputed)" — the parser takes the first character.
3. **Sources (`Sources:`) kept verbatim, untranslated** — citations are
   bibliographic data, and this policy preserves every link and display URL
   exactly. If the Chinese field is a short prose line without any URL
   (e.g. `作者经验，无直接文献`), translate it.
4. **Numbers never altered, converted, or rounded.** Units written out in
   Chinese (万 = 10,000; 亿 = 100,000,000) may be expanded (61 万 → 610,000)
   but the value must be identical. Keep CIs, P values, sample sizes
   character-for-character.
5. **Never invent, soften, or harden a medical, financial, or legal claim** —
   translate the meaning exactly, including its hedges.
6. `**bold**`, escaped `\*`, markdown links keep working — the renderer's
   `inline()` handles them.

## Terminology — GLOSSARY.md

[GLOSSARY.md](GLOSSARY.md) holds the canonical zh→en table. Each new
language should add its own column (or copy the file per language). Key
invariants across all languages:

- The signature column 说人话 renders as something a person would actually
  say — this column must never read as translated jargon.
- Recurring phrases (打折看 = "discount this figure", the evidence-grade
  names, value-tier names) must be translated identically every time.
- Keep a small per-language glossary file from day one; consistency across
  676 entries is impossible without one.

## Verification

```bash
python3 build.py                      # must build with 0 errors
python3 tools/check_translation.py <lang>   # must report 0 problems
```

`check_translation.py` compares your directory against `content/zh/` per
entry: section/entry sets, grades, tag values, computed tiers, URL multisets
(Sources + Note), and a normalized digit-multiset diff on the four prose
fields. Digit warnings are advisory — read each one; the common benign causes
are 万/亿 expansion, Chinese-numeral prose (三成 → 30%), and date formats.
If a warning is not one of those, you likely dropped or altered a number.

## LANGS starter — as shipped for German / Russian / Serbian

Field keywords (pick natural terms, then map them in `tag_keys`/`fields_kw`):

- de: `Kosten:`, `Klartext:`, `Nutzen:`, `Evidenzgrad:`, `Quellen:`, `Hinweis:`
- ru: `Затраты:`, `Простыми словами:`, `Польза:`, `Уровень доказательности:`, `Источники:`, `Примечание:`
- sr: `Trošak:`, `Prostim jezikom:`, `Korist:`, `Nivo dokaza:`, `Izvori:`, `Napomena:`

Tag tokens must be short and unambiguous; the LANGS `fields_kw`/`tag_keys`
dicts are the only things the parser matches, so they must match your files
exactly. Copy the `zh` entry as a template and replace every string; the
build fails loudly if a tag token doesn't map.

**UI strings to translate carefully** (all in LANGS): book title, scope
phrases, search placeholder, the three filter buttons, theme button, empty
state, count format (a single string, or a plural-form list — a 2-form
`[one, other]` list selected by n == 1 for German, a 3-form
`[one, few, many]` list with the Slavic 11-14 exception for Russian and
Serbian; see `count_line` in build.py), footer attribution (keep the upstream + CC BY 4.0 + renderer credits + translation notice), meta description.
`html_lang` must be set (the shipped entries use `de`, `ru`, `sr`).

## Workflow checklist for a new language

1. `mkdir content/<code>` and copy `content/en/NN-*.md` as structural
   templates (or translate from `content/zh/` directly — recommended for
   meaning fidelity).
2. Add the LANGS entry; run `python3 build.py --lang <code>` after each section.
3. Translate section by section; run
   `python3 tools/check_translation.py <code> N` to verify section N before
   moving on.
4. When all 34 sections pass with 0 problems: `python3 build.py` (builds all
   languages + landing), commit, push — Pages publishes `<code>/index.html` and
   the switcher/landing pick it up automatically.
5. Attribution: your footer automatically includes the CC BY 4.0 notice and
   a translation credit; the book title in your language belongs in
   `book_title`, and the page `<title>` follows it.

## Refreshing the vendored snapshot (re-vendor + re-translate)

1. `git clone https://github.com/eternity4719/HowToLiveBetter` and note the
   commit hash.
2. Replace `content/zh/*.md` with `book/NN-*.md` from that clone
   (only `book/` — nothing else). Record the new hash/date in
   `content/VENDORED.txt`.
3. Rebuild zh: `python3 build.py --lang zh`.
4. For each other language: diff old vs new Chinese to find
   changed/new/removed entries, translate only those (renumbered entries
   must renumber), and keep everything else untouched.
5. `python3 tools/check_translation.py <lang>` must again report 0 problems
   for every language before commit.
6. Never re-enable the daily rebuild workflow — see README.md.
