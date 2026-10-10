#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-process Russian content files: substitute @TAGS and @SOURCE:N@ placeholders
from the English reference, guaranteeing byte-exact Sources lines (URLs) and
correct tag-token mapping. No-URL author-experience source lines get translated."""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402

EN = build.LANGS["en"]
RU = build.LANGS["ru"]

TAG_KEY_RU = {"money": "деньги", "time": "время", "will": "воля",
              "benefit": "польза", "metric": "метрика"}
TAG_VAL_RU = {  # canonical -> ru token
    "money": {"none": "нет", "low": "мало", "high": "много"},
    "time": {"low": "мало", "mid": "средне", "high": "много"},
    "will": {"no": "нет", "some": "немного", "yes": "да"},
    "benefit": {"large": "большая", "mid": "средняя", "small": "малая"},
    "metric": {"mortality": "смертность", "money": "деньги",
               "time": "время", "freedom": "свобода"},
}
KEY_ORDER = ["money", "time", "will", "benefit", "metric"]

# English no-URL "author experience" source lines -> Russian translations.
NO_URL_TR = {
    "作者经验，无官方文件":
        "Опыт автора, официального документа нет",
    "作者经验，方法类建议；数据部分见本节前面各条":
        "Опыт автора, методическая рекомендация; данные — в предыдущих советах этого раздела",
    "作者经验，无直接文献":
        "Опыт автора, прямых публикаций нет",
    "作者经验，无直接文献；证据留存与转账备注同理见第 8 节关于彩礼和借条的两条":
        "Опыт автора, прямых публикаций нет; о сохранении доказательств и пометках к переводам — см. раздел 8, советы о калыме и расписках",
    "作者经验，无直接文献；相关证据见第 6 节":
        "Опыт автора, прямых публикаций нет; относящиеся сюда данные — в разделе 6",
    "作者经验，无直接文献；防骗通则见第 8 节和第 13 节":
        "Опыт автора, прямых публикаций нет; общие правила защиты от мошенничества — в разделах 8 и 13",
    "作者经验，无直接文献；口径见第 10 节":
        "Опыт автора, прямых публикаций нет; об используемом подходе — в разделе 10",
    "作者经验，无直接文献；同类分析见第 10 节":
        "Опыт автора, прямых публикаций нет; похожий разбор — в разделе 10",
    "作者经验，无直接文献；维权路径见第 7 节":
        "Опыт автора, прямых публикаций нет; пути защиты своих прав — в разделе 7",
    "作者经验，无直接文献；安全座椅的证据见第 1 节，冲动消费见第 5 节":
        "Опыт автора, прямых публикаций нет; данные об автокреслах — в разделе 1, об импульсивных тратах — в разделе 5",
    "作者经验，无直接文献；服务商资质与备案的法定要求见本节第 4 条，日志留存 6 个月和等级保护义务见第 11 节第 16 条":
        "Опыт автора, прямых публикаций нет; законные требования к квалификации и регистрации провайдера — в совете 4 этого раздела; о хранении логов 6 месяцев и обязательной защите уровня — см. раздел 11, совет 16",
}


def load_sources(path):
    field_re, kw2canon, _ = build.compile_parsers(EN)
    _, _, entries = build.parse(path, field_re, kw2canon)
    out = {}
    for e in entries:
        src = e["fields"].get("source", "")
        out[e["no"]] = ("<!-- costs: %s -->" % e["tags_raw"].replace("costs: ", "").strip()
                        if False else e["tags_raw"], src)
    return out


def ru_tags(tags_raw):
    _, _, parse_tags = build.compile_parsers(EN)
    t = parse_tags(tags_raw)
    parts = []
    for k in KEY_ORDER:
        if k in t:
            parts.append("%s=%s" % (TAG_KEY_RU[k], TAG_VAL_RU[k][t[k]]))
    return "затраты: " + " ".join(parts)


def process(ru_path):
    en_path = sorted((HERE / "content" / "en").glob(
        ru_path.name[:2] + "-*.md"))[0]
    _, _, en_entries = build.parse(en_path, *build.compile_parsers(EN)[:2])
    en_by_no = {e["no"]: e for e in en_entries}

    text = ru_path.read_text(encoding="utf-8")
    n_sub = 0

    m = re.search(r"^### (\d+)\.", text, re.M)
    cur_no = None
    out_lines = []
    for line in text.split("\n"):
        m = re.match(r"^###\s+(\d+)\.", line)
        if m:
            cur_no = int(m.group(1))
        if line.strip() == "<!-- @TAGS -->":
            en_tags = en_by_no[cur_no]["tags_raw"]
            out_lines.append("<!-- %s -->" % ru_tags(en_tags))
            n_sub += 1
            continue
        m = re.match(r"^- @SOURCE:(\d+)@$", line)
        if m:
            no = int(m.group(1))
            src = en_by_no[no]["fields"].get("source", "")
            stripped = src.strip()
            if stripped in NO_URL_TR:
                body = NO_URL_TR[stripped]
            elif "http" in src:
                body = src
            else:
                raise SystemExit("unmapped no-URL source in %s entry %d: %r"
                                 % (ru_path.name, no, stripped[:60]))
            out_lines.append("- Источники: %s" % body)
            n_sub += 1
            continue
        out_lines.append(line)

    ru_path.write_text("\n".join(out_lines), encoding="utf-8")
    return n_sub


def main():
    files = [Path(a) for a in sys.argv[1:]]
    total = 0
    for f in files:
        n = process(f)
        total += n
        print("%s: %d substitutions" % (f.name, n))
    print("total: %d" % total)
    leftovers = 0
    for f in files:
        t = f.read_text(encoding="utf-8")
        leftovers += t.count("@TAGS") + t.count("@SOURCE")
    if leftovers:
        print("WARNING: %d placeholders left!" % leftovers)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
