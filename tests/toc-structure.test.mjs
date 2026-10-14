// Suite 1 — TOC structure: for every built language, the collapsible TOC
// groups must cover every chapter (section) and every entry (card) of the
// page, with correct accordion wiring. Static DOM checks, no scripts needed.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { JSDOM } from 'jsdom';
import { builtLanguages, pageHtml, groups, sections } from './helpers.mjs';

const langs = builtLanguages();

test('built languages are discovered (zh + at least one translation)', () => {
  assert.ok(langs.length >= 2, `expected >=2 languages, got ${langs.join(', ')}`);
  assert.ok(langs.includes('zh'), 'zh (source language) must be built');
});

for (const lang of langs) {
  test(`[${lang}] TOC groups cover all sections and every card has a link`, () => {
    const doc = new JSDOM(pageHtml(lang)).window.document;

    const grps = groups(doc);
    const secs = sections(doc);
    assert.ok(grps.length > 0, 'no TOC groups found');
    assert.ok(secs.length > 0, 'no content sections found');

    // 1) one group per section, data-sec <-> section id bijection
    assert.equal(
      grps.length,
      secs.length,
      `group count ${grps.length} != section count ${secs.length}`,
    );
    const secNos = secs.map((s) => s.id.slice(3)).sort((a, b) => a - b);
    assert.deepEqual(
      grps.map((g) => g.dataset.sec).sort((a, b) => a - b),
      secNos,
      'data-sec values must match section ids exactly',
    );

    // 2) per group: link hrefs == card ids of that section, in order
    for (const g of grps) {
      const sec = doc.getElementById(`sec${g.dataset.sec}`);
      assert.ok(sec, `group data-sec=${g.dataset.sec} has no matching section`);
      const links = [...g.querySelectorAll('a[href^="#s"]')];
      const cards = [...sec.querySelectorAll('.card')];
      assert.ok(cards.length > 0, `section sec${g.dataset.sec} has no cards`);
      assert.deepEqual(
        links.map((a) => a.getAttribute('href').slice(1)),
        cards.map((c) => c.id),
        `group ${g.dataset.sec}: TOC links must mirror the section's cards in order`,
      );

      // 3) accordion wiring: gt button controls the gl list inside this group
      const btn = g.querySelector('.gt');
      const list = g.querySelector('.gl');
      assert.ok(btn, `group ${g.dataset.sec}: missing .gt button`);
      assert.ok(list, `group ${g.dataset.sec}: missing .gl list`);
      assert.equal(
        btn.getAttribute('aria-controls'),
        list.id,
        `group ${g.dataset.sec}: aria-controls must point at its own list`,
      );
      assert.match(list.id, /^tocg\d+$/, 'gl id must be tocg<section-no>');
      assert.equal(
        btn.getAttribute('aria-expanded'),
        'true',
        'markup ships with groups expanded (JS collapses on load)',
      );

      // 4) count badge <small> agrees with the number of links
      const badge = g.querySelector('.gt small');
      assert.ok(badge, `group ${g.dataset.sec}: missing count badge`);
      const n = (badge.textContent.match(/\d+/) || [])[0];
      assert.equal(
        Number(n),
        links.length,
        `group ${g.dataset.sec}: badge says ${n}, has ${links.length} links`,
      );
    }
  });
}
