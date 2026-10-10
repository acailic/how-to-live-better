# How to Live Better · 高性价比人生指南 — multilingual reader

Single-file HTML reading pages for the open-content book
《高性价比人生指南》 ("How to Live Better"), rendered in Chinese, English,
German, Russian, and Serbian (see TRANSLATING.md).

**Read online:** https://acailic.github.io/how-to-live-better/
(landing auto-redirects to your browser language; every page also links every
other language in its header).

- [English edition](https://acailic.github.io/how-to-live-better/en/)
- [中文版](https://acailic.github.io/how-to-live-better/zh/)
- [Deutsche Ausgabe](https://acailic.github.io/how-to-live-better/de/)
- [Русская версия](https://acailic.github.io/how-to-live-better/ru/)
- [Srpsko izdanje](https://acailic.github.io/how-to-live-better/sr/)

## What this is

The source book is maintained at [eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter).
It ranks life decisions by cost-effectiveness: every entry states what it
costs you, what it gets you, and how strong the evidence is — citing only
journal papers and official documents.

This repository renders that book into **self-contained single-file web
pages** (one HTML file per language, zero external dependencies, works
offline), adds a fully localized UI (search, filters, TOC, theme), and adds
translations. Each language page is content-complete: all 34 sections and all
676 entries.

## Page features

- **Zero external resources**: no CDN, no web fonts, no fetches — reads offline
- Card per entry: title, evidence grade (A/B/C), value tier, cost tags
- The **"In plain terms" highlight block** — the book's signature column, made the most prominent element
- Full-text search with highlighting, "Grade A only" and "plain terms only" filters
  (the English page opens with the Grade A filter active)
- Left TOC with value-tier color dots, scroll-synced
- Language switcher on every page
- Mobile: full-width search row, collapsing header, back-to-top
- Light/dark theme; print-ready

## License & attribution

- **Book content** — © the [eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter) authors, licensed
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This repository
  vendors a **pinned snapshot** (commit `bb25081`, 2026-10-09; see
  [content/VENDORED.txt](content/VENDORED.txt)). License text copy:
  [licenses/HowToLiveBetter-CONTENT-LICENSE.txt](licenses/HowToLiveBetter-CONTENT-LICENSE.txt).
- **Renderer** — the single-file builder (`build.py`) originates from
  [cdyforever/how-to-live-better](https://github.com/cdyforever/how-to-live-better), which claims no rights
  reserved. This repository's modifications are likewise released without
  rights reserved.
- **Translations** — English, German, Russian, and Serbian translations are
  produced by this repository and offered under CC BY 4.0 (consistent with
  the upstream license).
- Each rendered page carries an equivalent attribution line in its footer.

## Repository layout

```
build.py                  i18n-aware single-file renderer (all UI strings per language)
content/
  VENDORED.txt            pinned upstream snapshot record
  zh/NN-*.md              vendored Chinese original (byte-identical snapshot)
  en/NN-*.md              English translation
  de/NN-*.md ru/NN-*.md sr/NN-*.md   German, Russian, Serbian translations
index.html                landing: language selection + auto-redirect
zh/ en/ de/ ru/ sr/ index.html      generated pages (committed)
GLOSSARY.md               canonical terminology table (all languages)
TRANSLATING.md            how to translate a new language / refresh the snapshot
tools/check_translation.py  verifies grade/tag/link/number parity vs zh
```

## Build

```bash
python3 build.py             # all languages + landing page
python3 build.py --lang en   # one language
python3 build.py --lang en 1 # one language, one section (dev)

python3 tools/check_translation.py en   # parity check vs the Chinese original
```

## Automatic rebuild — deliberately disabled

`.github/workflows/rebuild.yml.disabled` is the original daily auto-rebuild.
It is disabled because this repository now holds **translations pinned to the
vendored snapshot**: a rebuild would pull the latest Chinese upstream and
overwrite every translated page with untranslated Chinese.

**How a refresh works instead** (details in [TRANSLATING.md](TRANSLATING.md)):

1. Re-vendor: clone upstream at a new commit, copy `book/*.md` into
   `content/zh/`, update `content/VENDORED.txt`, rebuild `zh/index.html`.
2. Diff each language directory against the previous snapshot and re-translate
   only what changed (`tools/check_translation.py` reports drift).
3. Translate the diff, rebuild, commit.
