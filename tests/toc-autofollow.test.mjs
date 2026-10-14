// Suite 2 — reading-position auto-follow: the collapsible TOC opens exactly
// the group containing the card currently on screen, swaps groups as the
// reading position moves, and lets manual interaction / search override.
// Runs the page's real inline <script> in jsdom; entries are delivered to
// the real IntersectionObserver callback via the mock in helpers.mjs.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  loadPage,
  pageHtml,
  groups,
  openGroupSecs,
  linkForCard,
  firstCardOfSection,
} from './helpers.mjs';

// zh ships with no preset filter (all cards visible); en ships with Grade A
// preselected, which exercises the other L10N count-form branch.
const zh = () => loadPage(pageHtml('zh'), { lang: 'zh' });

const settle = (ms = 150) => new Promise((r) => setTimeout(r, ms));

function sectionNumbers(doc, ...indices) {
  const secs = [...doc.querySelectorAll('main section[id^="sec"]')];
  return indices.map((i) => secs[i].id.slice(3));
}

test('initial state: only the first group is open, wiring is consistent', () => {
  const { document: doc } = zh();
  const grps = groups(doc);
  assert.ok(grps.length > 1, 'need >1 groups for accordion semantics');

  assert.deepEqual(openGroupSecs(doc), [grps[0].dataset.sec], 'only group 1 open on load');
  for (const g of grps) {
    const open = !g.classList.contains('closed');
    assert.equal(
      g.querySelector('.gt').getAttribute('aria-expanded'),
      String(open),
      `group ${g.dataset.sec}: aria-expanded must mirror .closed`,
    );
  }
  const gall = doc.getElementById('gall');
  assert.ok(gall, 'show-all button missing');
  assert.equal(gall.hidden, false, 'show-all button revealed once JS initialized');
});

test('reading position opens exactly the group of the card on screen', () => {
  const { document: doc, fire } = zh();
  const [target] = sectionNumbers(doc, 3); // a middle section
  const card = firstCardOfSection(doc, target);

  const invoked = fire(card);
  assert.equal(invoked, 1, 'synthetic entry must reach the page observer');

  assert.deepEqual(
    openGroupSecs(doc),
    [target],
    `card in section ${target} must open only its own group`,
  );
  const link = linkForCard(doc, card);
  assert.ok(link, 'TOC link for card missing');
  assert.ok(link.classList.contains('active'), 'card on screen gets the active link');
});

test('moving the reading position swaps the open group (auto-follow)', () => {
  const { document: doc, fire } = zh();
  const [a, b] = sectionNumbers(doc, 2, 9);

  fire(firstCardOfSection(doc, a));
  assert.deepEqual(openGroupSecs(doc), [a]);
  assert.ok(linkForCard(doc, firstCardOfSection(doc, a)).classList.contains('active'));

  fire(firstCardOfSection(doc, b));
  assert.deepEqual(openGroupSecs(doc), [b], 'new group opens…');
  assert.ok(
    !linkForCard(doc, firstCardOfSection(doc, a)).classList.contains('active'),
    '…and the active link follows the reading position',
  );
});

test('manual group click disables auto-follow for the visit', () => {
  const { document: doc, fire } = zh();
  const [manual, other, first] = sectionNumbers(doc, 4, 7, 0);

  // open `manual` by hand (its button starts closed -> click opens it);
  // the initially-open first group stays open — the page only toggles the
  // clicked group
  const btn = doc.querySelector(`.grp[data-sec="${manual}"] .gt`);
  btn.click();
  assert.deepEqual(
    openGroupSecs(doc).sort(),
    [first, manual].sort(),
    'manual click opens that group, initial group untouched',
  );

  // scrolling elsewhere must no longer rewire groups
  fire(firstCardOfSection(doc, other));
  assert.deepEqual(
    openGroupSecs(doc).sort(),
    [first, manual].sort(),
    'auto-follow stays off after a manual toggle',
  );
});

test('show-all button opens every group and also stops auto-follow', () => {
  const { document: doc, fire } = zh();
  const [other] = sectionNumbers(doc, 5);
  const all = groups(doc).map((g) => g.dataset.sec);

  doc.getElementById('gall').click();
  assert.deepEqual(openGroupSecs(doc).sort(), [...all].sort(), 'gall opens all groups');

  fire(firstCardOfSection(doc, other));
  assert.deepEqual(
    openGroupSecs(doc).sort(),
    [...all].sort(),
    'auto-follow stays off after gall',
  );
});

test('active search term suppresses auto-follow; it resumes after clearing', async () => {
  const { document: doc, fire } = zh();
  const [during, after] = sectionNumbers(doc, 6, 8);
  const q = doc.getElementById('q');
  const all = groups(doc).map((g) => g.dataset.sec);

  q.value = 'test-term';
  q.dispatchEvent(new doc.defaultView.Event('input'));
  await settle(); // debounce (90 ms) for apply()

  // searching expands all groups (filtered results must be visible)
  assert.deepEqual(openGroupSecs(doc).sort(), [...all].sort(), 'search expands all groups');

  fire(firstCardOfSection(doc, during));
  assert.deepEqual(
    openGroupSecs(doc).sort(),
    [...all].sort(),
    'auto-follow suppressed while a search term is active',
  );

  q.value = '';
  q.dispatchEvent(new doc.defaultView.Event('input'));
  await settle();

  assert.deepEqual(openGroupSecs(doc), [all[0]], 'clearing search restores the pre-search state');
  fire(firstCardOfSection(doc, after));
  assert.deepEqual(openGroupSecs(doc), [after], 'auto-follow resumes after search cleared');
});

test('hashchange always opens the target group (anchor jumps)', () => {
  const { document: doc, window } = zh();
  const [target] = sectionNumbers(doc, 10);
  const card = firstCardOfSection(doc, target);

  window.location.hash = `#${card.id}`;
  window.dispatchEvent(new window.HashChangeEvent('hashchange'));

  assert.ok(
    openGroupSecs(doc).includes(target),
    'hash jump opens the group containing the anchor',
  );
  assert.ok(linkForCard(doc, card).classList.contains('active') === false, 'no card is on screen yet');
});

test('[en] same auto-follow semantics with the Grade-A preset filter', () => {
  const { document: doc, fire } = loadPage(pageHtml('en'), { lang: 'en' });
  // en initializes with setMode('A'): reveal everything first, as a user would
  doc.getElementById('f-all').click();

  const [target] = sectionNumbers(doc, 3);
  fire(firstCardOfSection(doc, target));
  assert.deepEqual(openGroupSecs(doc), [target], 'en auto-follow matches zh behavior');
});
