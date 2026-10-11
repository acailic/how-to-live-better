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
`build.py` (LANGS block), `GLOSSARY.md` (end-of-file appends), and the generated
`*/index.html`. Resolution: keep every language's LANGS entry intact (dict order
zh, en, then new languages in merge order), concatenate glossary sections, take
either side of generated HTML, then run `python3 build.py` to regenerate all
outputs canonically. Parity gate: `python3 tools/check_translation.py <lang>`
must report 0 problems (digit warnings are a known Chinese-numeral class).

## Python formatter

`pyproject.toml` is authoritative: `ruff format --check .` must pass; it deliberately
excludes `build.py` and `tools/check_translation.py` (hand-wrapped compact style a
Black-style formatter cannot reproduce) and pins `line-length = 100` for any future
Python file. Do not reformat the two excluded files; do not widen the exclusion.
