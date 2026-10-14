// Suite 3 — mutation checks: sabotage the built page's TOC interception
// logic and assert the *broken* behavior is observable. These tests guard
// the other suites against becoming vacuous: if jsdom ever stopped running
// the page script, or the mock stopped reaching the real observer callback,
// the sabotaged pages would behave like healthy ones and these tests would
// fail. Conversely, if build.py ever ships the sabotage for real, the
// auto-follow suite fails. Either way the break is caught.
//
// Sabotage targets are exact source strings from JS_CORE in build.py; if a
// refactor renames them, the count assertions fail loudly so the tests get
// updated in the same change.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  loadPage,
  pageHtml,
  openGroupSecs,
  firstCardOfSection,
} from './helpers.mjs';

function sabotage(html, from, to, what) {
  const count = html.split(from).length - 1;
  assert.equal(count, 1, `mutation target not found exactly once: ${what}`);
  return html.replaceAll(from, to);
}

test('mutation: killing the auto-follow branch stops group switching (detected)', () => {
  // Break the reading-position interception exactly the way a regression
  // would: the observer still fires, it just never re-opens groups.
  const mutate = (html) =>
    sabotage(html, 'if(autoFollow&&!q.value.trim()){', 'if(false){', 'autoFollow branch');

  const { document: doc, fire } = loadPage(pageHtml('zh'), { lang: 'zh', mutate });
  const [target, first] = (() => {
    const secs = [...doc.querySelectorAll('main section[id^="sec"]')];
    return [secs[3].id.slice(3), secs[0].id.slice(3)];
  })();

  const invoked = fire(firstCardOfSection(doc, target));
  assert.equal(invoked, 1, 'entry still reaches the (broken) observer');

  // Healthy page: [target]. Broken page: initial [first] survives untouched.
  // The auto-follow suite asserts the healthy outcome against the real page,
  // so a regression like this fails *there*; this test pins the difference.
  assert.deepEqual(
    openGroupSecs(doc),
    [first],
    'sabotaged page must NOT follow the reading position — if it does, the test harness is not exercising the page script',
  );
});

test('mutation: breaking the section->group mapping breaks hash jumps (detected)', () => {
  // groupFor() maps a card's section to the TOC group via data-sec; skew the
  // slice so the selector never matches (sec12 -> looks for data-sec="c12").
  const mutate = (html) =>
    sabotage(html, 's.id.slice(3)', 's.id.slice(2)', 'groupFor section slice');

  const { document: doc, window } = loadPage(pageHtml('zh'), { lang: 'zh', mutate });
  const secs = [...doc.querySelectorAll('main section[id^="sec"]')];
  const target = secs[4].id.slice(3);
  const card = firstCardOfSection(doc, target);

  window.location.hash = `#${card.id}`;
  window.dispatchEvent(new window.HashChangeEvent('hashchange'));

  assert.ok(
    !openGroupSecs(doc).includes(target),
    'sabotaged mapping must fail to open the hash target group — if it opens, the hashchange test is not exercising the real openHashGroup()',
  );
});
