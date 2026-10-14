# Page tests (jsdom)

Covers the collapsible table of contents with reading-position auto-follow
and the dark-mode theme (system preference + remembered manual toggle) in
the built pages (`<lang>/index.html`): group/section coverage, the
auto-follow state machine, mutation checks proving the suite fails when
the interception logic is broken, and theme boot/toggle/persistence.

## Run

```sh
cd tests && npm install && npm test      # node --test, Node >= 18
```

## Files

- `helpers.mjs` — loads built pages into jsdom (scripts on) with an
  IntersectionObserver mock that delivers synthetic reading-position
  entries to the page's real observer callback.
- `toc-structure.test.mjs` — per language: every section has a TOC group,
  every card has a link (in order), accordion wiring, count badges.
  Languages are discovered from the repo dirs, so new ones are covered
  automatically.
- `toc-autofollow.test.mjs` — reading position opens exactly its group,
  swaps on movement, manual toggles / show-all / search override, hash
  jumps always open the target group, `en` preset-filter parity.
- `toc-mutation.test.mjs` — sabotages the interception logic on mutated
  copies and pins the *broken* behavior, guarding the suite against
  becoming vacuous. Sabotage strings are exact `JS_CORE` sources from
  `build.py`; a rename there fails these tests loudly so they get updated
  in the same change.
- `toc-stress.test.mjs` — seeded random walk (default 300 iterations) over
  all interactions with full invariant checks after every step, plus
  forward/backward/shuffled sweeps. Deterministic seed; bump
  `SEED`/`ITERATIONS` locally for a harder soak.
- `theme-toggle.test.mjs` — dark mode: per language the `#theme` toggle
  ships with a localized aria-label and the `THEME_BOOT` script sits in
  `<head>` before `<style>` (no flash of light for dark readers); runtime
  tests cover OS-preference detection via a scriptable `matchMedia` stub,
  stored choice beating the OS, toggle persistence, reload carry-over, and
  live OS theme changes. Landing page included.

## Contract

Tests run against the **committed build artifacts**, so they catch
regressions that ship. After changing `build.py` or content, run
`python3 build.py` (and commit the rebuilt pages) before the tests.
