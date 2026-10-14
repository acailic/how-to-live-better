// Suite 4 — dark-mode theme: the pages must respect the OS preference, offer
// a manual toggle that is remembered (localStorage 'hltb-theme'), and apply
// the theme before first paint (boot script inline in <head>, before the
// stylesheet — no white flash for dark readers). jsdom ships no matchMedia,
// so the loader below installs a scriptable stand-in; without it the pages'
// own `window.matchMedia&&` guards simply default to light.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { JSDOM, VirtualConsole } from 'jsdom';
import { ROOT, builtLanguages, pageHtml } from './helpers.mjs';

// Toggle aria-labels pinned from LANGS['<lang>'].theme_aria in build.py; a
// newly added language only needs a non-empty label (the map pins the five
// currently built languages so accidental English fallbacks fail loudly).
const ARIA = {
  zh: '切换明暗主题',
  en: 'Toggle light/dark theme',
  de: 'Zwischen hellem und dunklem Design wechseln',
  ru: 'Переключить светлую и тёмную тему',
  sr: 'Prebaci svetlu/tamnu temu',
};

// Every built page must ship these exact markers; the boot marker doubles as
// the no-FOUC contract (it must sit before <style> in the emitted <head>).
const BOOT_MARK = "<script>(function(){var d=document.documentElement;";
const DARK_VARS = '[data-theme=dark]{';
const STORE_KEY = 'hltb-theme';

// A scriptable matchMedia: `.matches` is the system preference, `.dispatch()`
// simulates the OS switching theme while the page is open.
function makeMq(initial) {
  const listeners = new Set();
  const mq = {
    matches: !!initial,
    media: '(prefers-color-scheme: dark)',
    addEventListener: (_type, fn) => listeners.add(fn),
    removeEventListener: (_type, fn) => listeners.delete(fn),
    addListener: (fn) => listeners.add(fn),
    removeListener: (fn) => listeners.delete(fn),
    dispatch(matches) {
      mq.matches = !!matches;
      for (const fn of [...listeners]) fn({ matches: mq.matches, media: mq.media });
    },
  };
  return mq;
}

// Load a built page with a scripted system preference and, optionally, a
// previously stored manual choice — i.e. exactly what a returning reader's
// browser looks like. IntersectionObserver is stubbed because the page script
// wires its reading-position observer at load time.
function loadThemePage(html, { lang = 'zh', systemDark = false, stored = null } = {}) {
  const mq = makeMq(systemDark);
  const dom = new JSDOM(html, {
    url: `http://localhost/${lang}/index.html`,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    beforeParse(window) {
      window.matchMedia = (q) =>
        String(q).includes('prefers-color-scheme')
          ? mq
          : { matches: false, media: String(q), addEventListener() {}, removeEventListener() {} };
      // jsdom has no IntersectionObserver; a no-op stand-in lets the whole
      // page script (theme toggle included) run as in a real browser.
      window.IntersectionObserver = class {
        observe() {}
        unobserve() {}
        disconnect() {}
      };
      if (stored != null) {
        window.localStorage.setItem(STORE_KEY, stored);
      }
    },
  });
  return { dom, window: dom.window, document: dom.window.document, mq };
}

const theme = (doc) => doc.documentElement.getAttribute('data-theme');
const storedTheme = (win) => {
  try {
    return win.localStorage.getItem(STORE_KEY);
  } catch {
    return null;
  }
};

// ---------------------------------------------------------------- structure

for (const lang of builtLanguages()) {
  test(`[${lang}] theme toggle ships, localized, and boots before first paint`, () => {
    const html = pageHtml(lang);

    // 1) <html> carries the light default; boot script + dark vars exist,
    //    and the boot script runs before the stylesheet (no flash of light).
    assert.match(html, /<html lang="[^"]+" data-theme="light">/);
    assert.ok(html.includes(BOOT_MARK), 'missing THEME_BOOT inline head script');
    assert.ok(html.includes(DARK_VARS), 'CSS has no [data-theme=dark] variable block');
    assert.ok(
      html.indexOf(BOOT_MARK) < html.indexOf('<style>'),
      'theme boot script must precede <style> so the first paint is already themed',
    );

    // 2) the manual toggle is a real button with a localized label
    const doc = new JSDOM(html).window.document;
    const btn = doc.getElementById('theme');
    assert.ok(btn, 'no #theme button in the top bar');
    assert.equal(btn.tagName, 'BUTTON');
    const label = btn.getAttribute('aria-label');
    assert.ok(label && label.trim(), 'toggle has no aria-label');
    if (ARIA[lang]) {
      assert.equal(label, ARIA[lang], `aria-label must be the localized string`);
      assert.equal(btn.getAttribute('title'), ARIA[lang]);
      assert.ok(btn.textContent.trim(), 'toggle has no visible text');
    }
  });
}

test('landing page applies the theme before first paint too', () => {
  const html = landingHtml();
  assert.ok(html.includes(BOOT_MARK), 'landing missing THEME_BOOT');
  assert.ok(html.includes(DARK_VARS), 'landing CSS has no dark block');
  assert.ok(html.indexOf(BOOT_MARK) < html.indexOf('<style>'));

  // The redirect IIFE calls location.replace(), which jsdom cannot follow —
  // swallow that known "not implemented" noise, then check the applied theme.
  const vc = new VirtualConsole(); // silently drop jsdom's navigation errors
  const mq = makeMq(true);
  const dom = new JSDOM(html, {
    url: 'http://localhost/index.html',
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(window) {
      window.matchMedia = () => mq;
    },
  });
  assert.equal(theme(dom.window.document), 'dark');
});

function landingHtml() {
  return readFileSync(join(ROOT, 'index.html'), 'utf-8');
}

// ------------------------------------------------------- runtime behaviour

test('OS dark preference is respected on load (no manual choice)', () => {
  const { document } = loadThemePage(pageHtml('zh'), { lang: 'zh', systemDark: true });
  assert.equal(theme(document), 'dark', 'system dark must apply without a stored choice');
});

test('OS light preference keeps the light default', () => {
  const { document } = loadThemePage(pageHtml('en'), { lang: 'en', systemDark: false });
  assert.equal(theme(document), 'light');
});

test('stored manual choice beats the OS preference', () => {
  const light = loadThemePage(pageHtml('zh'), { lang: 'zh', systemDark: true, stored: 'light' });
  assert.equal(theme(light.document), 'light', 'stored light must win over system dark');
  const dark = loadThemePage(pageHtml('zh'), { lang: 'zh', systemDark: false, stored: 'dark' });
  assert.equal(theme(dark.document), 'dark', 'stored dark must win over system light');
});

test('toggle flips the theme and persists the choice', () => {
  const { document, window } = loadThemePage(pageHtml('zh'), { lang: 'zh', systemDark: false });
  assert.equal(theme(document), 'light');
  assert.equal(storedTheme(window), null, 'no choice stored before first toggle');

  document.getElementById('theme').click();
  assert.equal(theme(document), 'dark');
  assert.equal(storedTheme(window), 'dark', 'toggle must persist dark');

  document.getElementById('theme').click();
  assert.equal(theme(document), 'light');
  assert.equal(storedTheme(window), 'light', 'toggle must persist the flip back');
});

test('toggle works from a system-dark start and stores the explicit light', () => {
  const { document, window } = loadThemePage(pageHtml('sr'), { lang: 'sr', systemDark: true });
  assert.equal(theme(document), 'dark');
  document.getElementById('theme').click();
  assert.equal(theme(document), 'light');
  assert.equal(storedTheme(window), 'light');
});

test('remembered choice survives a reload (new page load reads storage)', () => {
  // First visit: reader toggles to dark.
  const first = loadThemePage(pageHtml('zh'), { lang: 'zh', systemDark: false });
  first.document.getElementById('theme').click();
  const remembered = storedTheme(first.window);
  assert.equal(remembered, 'dark');

  // Second visit: fresh page object, OS still light — storage carries over.
  const second = loadThemePage(pageHtml('zh'), {
    lang: 'zh',
    systemDark: false,
    stored: remembered,
  });
  assert.equal(theme(second.document), 'dark', 'reload must come up dark');
});

test('page follows live OS theme changes until the reader toggles manually', () => {
  const { document, mq } = loadThemePage(pageHtml('en'), { lang: 'en', systemDark: false });
  assert.equal(theme(document), 'light');
  mq.dispatch(true); // OS switches to dark while reading
  assert.equal(theme(document), 'dark', 'no stored choice -> follow the OS live');
  mq.dispatch(false);
  assert.equal(theme(document), 'light');

  const pinned = loadThemePage(pageHtml('en'), { lang: 'en', systemDark: false, stored: 'dark' });
  assert.equal(theme(pinned.document), 'dark');
  pinned.mq.dispatch(false); // OS flips back to light — must NOT override
  assert.equal(theme(pinned.document), 'dark', 'manual choice must survive OS changes');
});
