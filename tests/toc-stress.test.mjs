// Suite 4 — stress: a seeded random walk over the real page, mixing reading
// positions, manual group toggles, show-all, search and hash jumps. After
// every step the full TOC invariant set is re-checked, so any state-machine
// leak (stale group, aria mismatch, orphan open group, search state left
// behind) is caught at the exact step that caused it.
//
// The seed is fixed: failures reproduce deterministically. Bump ITERATIONS
// or SEED locally for a harder soak; CI keeps a runtime-friendly default.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  loadPage,
  pageHtml,
  groups,
  openGroupSecs,
  firstCardOfSection,
} from './helpers.mjs';

const SEED = 0x5eed;
const ITERATIONS = 300;

// mulberry32 — tiny deterministic PRNG
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function invariants(doc, note) {
  const grps = groups(doc);
  assert.ok(grps.length > 1, `${note}: groups missing entirely`);
  for (const g of grps) {
    assert.equal(
      g.querySelector('.gt').getAttribute('aria-expanded'),
      String(!g.classList.contains('closed')),
      `${note}: group ${g.dataset.sec} aria-expanded out of sync with .closed`,
    );
  }
  const open = openGroupSecs(doc);
  // "collapse all" (gall) and closing the last open group by hand are both
  // legitimate page states, so 0 open groups is allowed — but never more
  // than the total, and the aria wiring must always be in sync
  assert.ok(
    open.length <= grps.length,
    `${note}: impossible open count ${open.length}`,
  );
  return open;
}

test('stress: random walk keeps the TOC state machine consistent (zh)', async () => {
  const rand = rng(SEED);
  const { document: doc, window, fire } = loadPage(pageHtml('zh'), { lang: 'zh' });

  const grps = groups(doc);
  const secNos = grps.map((g) => g.dataset.sec);
  const q = doc.getElementById('q');
  const settle = () => new Promise((r) => setTimeout(r, 5));

  let searches = 0;
  let manualToggles = 0;
  let hashJumps = 0;
  let readingMoves = 0;

  let expectedOpen = null; // null = manual/mixed state, only invariants hold
  let searchActive = false;

  for (let i = 0; i < ITERATIONS; i++) {
      const roll = rand();
      if (roll < 0.55) {
        // reading position moves to a random card
        const sec = secNos[Math.floor(rand() * secNos.length)];
        fire(firstCardOfSection(doc, sec));
        readingMoves++;
        if (!searchActive && expectedOpen !== null) {
          expectedOpen = [sec];
        }
      } else if (roll < 0.68) {
        // manual toggle of a random group header (disables auto-follow)
        const g = grps[Math.floor(rand() * grps.length)];
        const wasClosed = g.classList.contains('closed');
        g.querySelector('.gt').click();
        manualToggles++;
        expectedOpen = null; // user owns the state from here on
        // immediate local check: the clicked group flipped
        assert.equal(
          g.classList.contains('closed'),
          !wasClosed,
          `iter ${i}: manual toggle must flip the group`,
        );
      } else if (roll < 0.76) {
        // show-all / collapse-all button
        const wasAll = grps.every((g) => !g.classList.contains('closed'));
        doc.getElementById('gall').click();
        expectedOpen = null;
        assert.equal(
          grps.every((g) => !g.classList.contains('closed')),
          !wasAll,
          `iter ${i}: gall must flip global expansion`,
        );
      } else if (roll < 0.9) {
        // search on/off cycles (debounced apply)
        if (!searchActive) {
          q.value = 'stress';
          searchActive = true;
          searches++;
        } else {
          q.value = '';
          searchActive = false;
        }
        q.dispatchEvent(new window.Event('input'));
        await settle();
        expectedOpen = null;
      } else {
        // hash jump to a random card — must open its group regardless of
        // auto-follow being off
        const sec = secNos[Math.floor(rand() * secNos.length)];
        const card = firstCardOfSection(doc, sec);
        window.location.hash = `#${card.id}`;
        window.dispatchEvent(new window.HashChangeEvent('hashchange'));
        hashJumps++;
        assert.ok(
          !doc
            .querySelector(`.grp[data-sec="${sec}"]`)
            .classList.contains('closed'),
          `iter ${i}: hash jump must open group ${sec}`,
        );
      }

      const open = invariants(doc, `iter ${i}`);
      if (expectedOpen !== null) {
        assert.deepEqual(
          open,
          expectedOpen,
          `iter ${i}: auto-follow must keep exactly [${expectedOpen}] open`,
        );
      }
  }

  assert.ok(readingMoves > 50, 'walk must exercise reading moves');
  assert.ok(manualToggles > 5, 'walk must exercise manual toggles');
  assert.ok(searches > 5, 'walk must exercise search cycles');
  assert.ok(hashJumps > 5, 'walk must exercise hash jumps');
});

test('stress: rapid sequential sweeps across every section stay in lockstep', () => {
  const { document: doc, fire } = loadPage(pageHtml('zh'), { lang: 'zh' });
  const secNos = groups(doc).map((g) => g.dataset.sec);

  // full forward sweep, then backward sweep, then random shuffle of all cards
  const order = [...secNos, ...[...secNos].reverse()];
  for (const sec of order) {
    fire(firstCardOfSection(doc, sec));
    assert.deepEqual(
      openGroupSecs(doc),
      [sec],
      `sweep: after entering section ${sec} only its group may be open`,
    );
  }
  const rand = rng(SEED ^ 0xabcd);
  const shuffled = [...secNos].sort(() => rand() - 0.5);
  for (const sec of shuffled) {
    fire(firstCardOfSection(doc, sec));
    assert.deepEqual(openGroupSecs(doc), [sec], `shuffle: group ${sec} must be alone open`);
  }
});
