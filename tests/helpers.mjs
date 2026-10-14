// Shared helpers: load built pages into jsdom with scripts enabled and an
// IntersectionObserver stand-in so tests can fire synthetic "reading
// position" entries straight into the page's real observer callback.
//
// The pages under test are the committed build artifacts (<lang>/index.html).
// If content or build.py changes, run `python3 build.py` before the tests.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JSDOM } from 'jsdom';

export const ROOT = fileURLToPath(new URL('..', import.meta.url));

// Languages = repo dirs holding a built index.html with the TOC aside.
// Discovered dynamically so a newly merged language is covered for free.
export function builtLanguages() {
  return fs
    .readdirSync(ROOT, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .map((e) => e.name)
    .filter((name) => {
      const p = path.join(ROOT, name, 'index.html');
      if (!fs.existsSync(p)) return false;
      return fs.readFileSync(p, 'utf-8').includes('<aside class="toc">');
    })
    .sort();
}

export function pageHtml(lang) {
  return fs.readFileSync(path.join(ROOT, lang, 'index.html'), 'utf-8');
}

// jsdom has no IntersectionObserver; this mock records observed targets and
// lets tests deliver entries synchronously through the real page callback.
function makeIntersectionObserverMock() {
  const instances = [];
  class IntersectionObserver {
    constructor(callback, options) {
      this.callback = callback;
      this.options = options;
      this.targets = new Set();
      instances.push(this);
    }
    observe(target) {
      this.targets.add(target);
    }
    unobserve(target) {
      this.targets.delete(target);
    }
    disconnect() {
      this.targets.clear();
    }
  }
  return { IntersectionObserver, instances };
}

// Load a built (possibly mutated) page. `mutate` receives the raw HTML and
// returns a sabotaged copy — used by the mutation tests to prove the suite
// really depends on the page's interception logic.
export function loadPage(html, { lang = 'zh', mutate = null } = {}) {
  if (mutate) html = mutate(html);
  const { IntersectionObserver, instances } = makeIntersectionObserverMock();
  const dom = new JSDOM(html, {
    url: `http://localhost/${lang}/index.html`,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    beforeParse(window) {
      window.IntersectionObserver = IntersectionObserver;
    },
  });
  const { document } = dom.window;

  // Deliver a synthetic intersection entry for `el` to every observer that
  // watches it. Returns how many page callbacks were invoked, so tests can
  // assert they actually reached the page's observer.
  function fire(el, isIntersecting = true) {
    let invoked = 0;
    for (const io of instances) {
      if (!io.targets.has(el)) continue;
      io.callback(
        [{ target: el, isIntersecting, intersectionRatio: isIntersecting ? 1 : 0 }],
        io,
      );
      invoked++;
    }
    return invoked;
  }

  return { dom, window: dom.window, document, ioInstances: instances, fire };
}

// -------- small DOM query helpers shared by the test files --------

export function groups(doc) {
  return [...doc.querySelectorAll('.toc .grp')];
}

export function sections(doc) {
  return [...doc.querySelectorAll('main section[id^="sec"]')];
}

export function firstCardOfSection(doc, secNo) {
  return doc.querySelector(`#sec${secNo} .card`);
}

// Map of data-sec -> isOpen for the whole TOC.
export function groupState(doc) {
  const state = new Map();
  for (const g of groups(doc)) {
    state.set(g.dataset.sec, !g.classList.contains('closed'));
  }
  return state;
}

export function openGroupSecs(doc) {
  return [...groupState(doc)].filter(([, open]) => open).map(([sec]) => sec).sort();
}

export function linkForCard(doc, card) {
  return doc.querySelector(`.toc a[href="#${card.id}"]`);
}
