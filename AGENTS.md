# Project agent memory

This file is the project's committed home for project-intrinsic agent knowledge: build, test, release, architecture, and sharp-edge notes that should travel with the code.

- Add durable project-specific notes here as they are discovered through real work.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.

## Merging parallel translation branches

Parallel per-language branches (one LANGS entry each) conflict mechanically in
`build.py` (LANGS block), `GLOSSARY.md` (end-of-file appends), and the generated `*/index.html`
(and `sitemap.xml`/`robots.txt`, same rule). Resolution: keep every language's LANGS
entry intact (dict order
zh, en, then new languages in merge order), concatenate glossary sections, take
either side of generated files, then run `python3 build.py` to regenerate all
outputs canonically. Parity gate: `python3 tools/check_translation.py <lang>`
must report 0 problems (digit warnings are a known Chinese-numeral class).

## Python formatter

`pyproject.toml` is authoritative: `ruff format --check .` must pass; it deliberately
excludes `build.py` and `tools/check_translation.py` (hand-wrapped compact style a
Black-style formatter cannot reproduce) and pins `line-length = 100` for any future
Python file. Do not reformat the two excluded files; do not widen the exclusion.

## JS test suite (tests/)

`cd tests && npm install && npm test` (Node >= 18, jsdom) covers the collapsible TOC:
group/section coverage per language, reading-position auto-follow, mutation
canaries, a seeded stress walk, and the dark-mode theme (boot order, OS
preference, toggle persistence — see `tests/theme-toggle.test.mjs`). Tests run
against the **committed build artifacts** (`<lang>/index.html`), not build.py
output — rebuild and commit before testing after content/build changes.
Mutation tests pin exact `JS_CORE` source strings; renaming those in build.py
fails them loudly so they get updated in the same change. See tests/README.md.

## Dark-mode theme architecture

Theming is JS-driven: `<html data-theme="light">` is the static default, the
`THEME_BOOT` inline script in build.py runs in `<head>` **before `<style>`**
(stored `hltb-theme` wins over `prefers-color-scheme`; without a stored choice
the page follows the OS, live), and JS_CORE only owns the `#theme` toggle.
Palettes live in the CSS custom-property blocks (`:root` / `[data-theme=dark]`
in CSS and LANDING_CSS). Tertiary text `--t3` is pinned to WCAG AA (≥4.5:1 on
its worst surface): keep light `.75` / dark `.54` alpha or re-audit —
`tests/theme-toggle.test.mjs` does not check contrast, so palette edits need
a manual pass.

## Verified TODO resolutions in content (2026-10-13 pass)

The zh snapshot was deliberately edited (captain-authorized pass) to resolve the
three TODO verification notes in ch 06 item 20, ch 20 item 10, ch 31 item 6 —
zh+sr notes rewritten, en/de/ru got only the new source URLs (their TODO note
text is still pending translation). A future upstream snapshot refresh per
TRANSLATING.md will clobber these fixes: re-check the three notes after any
refresh and re-apply or re-verify. Sources added in that pass:
tyjrswj.yibin.gov.cn (2026-09-17 policy Q&A, 4,500 yuan/year),
lcgdbzz.org (full-text repost of the 2021 gallbladder consensus),
news.china.com/海报新闻 (2026-10-12, diaper-probe non-disclosure).
