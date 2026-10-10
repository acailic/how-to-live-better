#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cross-check a translation against the vendored Chinese original.

Verifies, per section and per entry:
  - same section set and same entry numbers/count
  - same evidence grade letter
  - same computed value tier and tag values
  - same link counts (Sources + Note) and same URL sets
  - same multiset of ASCII digit-runs in translated prose fields
    (Cost / In plain terms / Benefit / Note), after normalizing
    full-width digits and stripping thousands separators.
    Chinese-numeral prose (三成, 几十元...) will flag; eyeball those.

Usage: python tools/check_translation.py [lang] [sections...]
"""
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402

FW = str.maketrans("０１２３４５６７８９％，．", "0123456789%,.")


def norm_digits(s):
    s = s.translate(FW)
    s = re.sub(r"(\d),(?=\d{3}\b)", r"\1", s)
    return Counter(re.findall(r"\d+(?:\.\d+)?", s))


def urls(s):
    toks = re.findall(r"https?://[!-~]+", s or "")
    return Counter(t.rstrip(">,:;") for t in toks)


def load(lang):
    spec = build.LANGS[lang]
    field_re, kw2canon, parse_tags = build.compile_parsers(spec)
    data = {}
    for n in build.avail_sections(lang):
        title, intro, entries = build.parse(build.find_file(lang, n), field_re, kw2canon)
        data[n] = {"title": title, "entries": {e["no"]: e for e in entries},
                   "tags": {e["no"]: parse_tags(e["tags_raw"]) for e in entries}}
    return data


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    sections = [int(a) for a in sys.argv[2:]] or None
    zh, tr = load("zh"), load(lang)
    problems = []
    warns = []

    zsecs, tsecs = set(zh), set(tr)
    if sections is not None:
        zsecs &= set(sections)
        tsecs &= set(sections)
    if zsecs != tsecs:
        problems.append("section set differs: zh-only %s, %s-only %s"
                        % (sorted(zsecs - tsecs), lang, sorted(tsecs - zsecs)))

    for n in sorted(zsecs & tsecs):
        ze, te = zh[n]["entries"], tr[n]["entries"]
        if set(ze) != set(te):
            problems.append("s%d: entry numbers differ: zh %s vs %s %s"
                            % (n, sorted(ze), lang, sorted(te)))
            continue
        for no in sorted(ze):
            z, t = ze[no], te[no]
            tag = "s%d-%d" % (n, no)
            zg = (z["fields"].get("evidence") or "?").strip()[:1]
            tg = (t["fields"].get("evidence") or "?").strip()[:1]
            if zg != tg:
                problems.append("%s: grade %s != %s" % (tag, zg, tg))
            zt, tt = zh[n]["tags"][no], tr[n]["tags"][no]
            for k in ("money", "time", "will", "benefit", "metric"):
                if zt.get(k) != tt.get(k):
                    problems.append("%s: tag %s %r != %r" % (tag, k, zt.get(k), tt.get(k)))
            zr, trr = build.ratio_of(zt), build.ratio_of(tt)
            if zr != trr:
                problems.append("%s: ratio %s != %s" % (tag, zr, trr))
            zl = urls(z["fields"].get("source", "")) + urls(z["fields"].get("note", ""))
            tl = urls(t["fields"].get("source", "")) + urls(t["fields"].get("note", ""))
            if zl != tl:
                only_z, only_t = zl - tl, tl - zl
                problems.append("%s: URL multiset differs (+zh %d, +%s %d): %s | %s"
                                % (tag, sum(only_z.values()), lang, sum(only_t.values()),
                                   list(only_z)[:2], list(only_t)[:2]))
            for f in ("cost", "plain", "benefit", "note"):
                zd = norm_digits(z["fields"].get(f, ""))
                td = norm_digits(t["fields"].get(f, ""))
                if zd != td:
                    warns.append("%s [%s]: digits differ: zh-only %s, en-only %s"
                                 % (tag, f, dict(zd - td), dict(td - zd)))
            for f in ("cost", "plain", "benefit", "note"):
                if not (t["fields"].get(f) or "").strip() and (z["fields"].get(f) or "").strip():
                    problems.append("%s: missing field %s" % (tag, f))

    scope = "all" if sections is None else str(sections)
    print("checked %s (%s sections): %d problems, %d digit warnings"
          % (lang, scope, len(problems), len(warns)))
    for p in problems:
        print("PROBLEM:", p)
    for w in warns:
        print("digits :", w)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
