# -*- coding: utf-8 -*-
"""Render the multilingual edition of 《高性价比人生指南》 / "How to Live Better"
into self-contained single-file HTML reading pages.

Usage:
    python build.py                     # build every language + the landing page
    python build.py --lang en           # build one language only
    python build.py --lang en 1 2 16    # dev: only these sections
    python build.py --lang en -o out.html

Content lives in content/<lang>/NN-*.md. content/zh is a byte-identical pinned
snapshot of the upstream book (see content/VENDORED.txt); every other language
directory is a translation pinned to that same snapshot.

Each language is configured in LANGS below: the field keywords and tag tokens
used in that language's .md files, plus every UI string. Adding a language
means adding a LANGS entry and a content directory — see TRANSLATING.md.

数字与标签的口径完全照抄上游仓库 tools/sync-stats.ps1 与 index.html 的
COST_W 与 e.ratio：上游改了那两行，这里也要同步改，否则性价比档会和官方
检索页对不上。产物为单个 .html，无任何外部依赖，双击即可打开、可离线读。
"""

import argparse
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTENT = HERE / "content"
UPSTREAM = "https://github.com/eternity4719/HowToLiveBetter"
RENDERER = "https://github.com/cdyforever/how-to-live-better"
CC_BY = "https://creativecommons.org/licenses/by/4.0/"


# ---------------------------------------------------------------- vendor pin

def load_vendor():
    """Read the pinned upstream commit recorded at vendor time (content/VENDORED.txt).

    Deliberately a static record instead of a build time or a live clone, so the
    same source state always rebuilds byte-identically.
    """
    rev, date = "", ""
    try:
        txt = (CONTENT / "VENDORED.txt").read_text(encoding="utf-8")
        m = re.search(r"^Commit:\s+(\S+)", txt, re.M)
        if m:
            rev = m.group(1)[:7]
        m = re.search(r"^Commit date:\s+(\S+)", txt, re.M)
        if m:
            date = m.group(1)
    except OSError:
        pass
    return rev, date


# ------------------------------------------------------- canonical taxonomy
# Internal keys are canonical English; LANGS maps them to/from each language's
# file tokens and display strings. Ratio tiers follow the upstream rules
# (COST_W + e.ratio in the upstream index.html).

COST_W = {
    "money": {"none": 0, "low": 1, "high": 2},
    "time": {"low": 0, "mid": 1, "high": 2},
    "will": {"no": 0, "some": 1, "yes": 2},
}
TIER_ORDER = {"vhigh": 0, "high": 1, "avg": 2}


def ratio_of(t):
    try:
        cs = sum(COST_W[k][t[k]] for k in ("money", "time", "will"))
    except KeyError:
        return None
    b = t.get("benefit")
    if b == "large":
        return "vhigh" if cs == 0 else ("high" if cs <= 2 else "avg")
    if b == "mid" and cs == 0:
        return "high"
    return "avg"


# ---------------------------------------------------------------- languages

LANGS = {
    "zh": {
        "label": "中文",
        "html_lang": "zh-CN",
        "book_title": "高性价比人生指南",
        # keywords used in this language's .md files -> canonical field keys
        "fields_kw": {"成本": "cost", "说人话": "plain", "收益": "benefit",
                      "证据等级": "evidence", "来源": "source", "备注": "note"},
        "tag_keys": {"钱": "money", "时间": "time", "毅力": "will",
                     "收益": "benefit", "口径": "metric"},
        "tag_vals": {  # file token -> canonical value
            "money": {"0": "none", "少": "low", "多": "high"},
            "time": {"少": "low", "中": "mid", "多": "high"},
            "will": {"否": "no", "些": "some", "是": "yes"},
            "benefit": {"大": "large", "中": "mid", "小": "small"},
            "metric": {"死亡率": "mortality", "金钱": "money",
                       "时间": "time", "自由": "freedom"},
        },
        "disp": {  # canonical value -> display
            "money": {"none": "0", "low": "少", "high": "多"},
            "time": {"low": "少", "mid": "中", "high": "多"},
            "will": {"no": "否", "some": "些", "yes": "是"},
            "benefit": {"large": "大", "mid": "中", "small": "小"},
            "metric": {"mortality": "死亡率", "money": "金钱",
                       "time": "时间", "freedom": "自由"},
            "tier": {"vhigh": "极高", "high": "高", "avg": "一般"},
        },
        "tag_disp": {"money": "钱", "time": "时间", "will": "毅力",
                     "benefit": "收益", "metric": "口径"},
        "chip_sep": " ",
        "grade_fmt": "%s 级",
        "tier_fmt": "性价比 %s",
        "toc_clip": 34,
        # ---- UI strings ----
        "scope_all": "全书 %d 节",
        "scope_sel": "第 %s 节",
        "meta_desc": "《高性价比人生指南》%s，共 %d 条建议，每条标注成本、收益、证据等级（A/B/C）"
                     "与原始文献链接。单文件、零依赖、可离线阅读。",
        "search_ph": "搜索标题、说人话、收益…",
        "btn_all": "全部",
        "btn_a": "只看 A 级",
        "btn_plain": "只看说人话",
        "btn_theme": "明/暗",
        "theme_aria": "切换明暗主题",
        "jump_aria": "跳转到某一节",
        "count_js": "%1 / %2 条",
        "empty": "没有匹配的条目",
        "top_title": "回到顶部",
        "toc_count": "%d 条",
        "toc_show_all": "显示全部",
        "toc_hide_all": "全部收起",
        "src_one": "来源",
        "src_many": "来源（%d 条文献）",
        "langs_aria": "切换语言",
        # ---- footer ----
        "foot_source": "数据来源：<a href=\"%s\" target=\"_blank\" rel=\"noopener\">"
                       "eternity4719/HowToLiveBetter</a>"
                       "（内容以 <a href=\"%s\" target=\"_blank\" rel=\"noopener\">CC BY 4.0</a> 授权）",
        "foot_snapshot": "，数据截至 <span style=\"font-family:var(--mono)\">%s</span>%s",
        "snap_date": "（%s）",
        "foot_excerpt": "「说人话」「收益」等栏目为原文摘录，未作改写；本页共 %d 条，"
                        "A 级 %d 条、B 级 %d 条、C 级 %d 条，含 %d 条文献外链。",
        "foot_self": "单文件自包含，不引用任何外部资源（正文中的文献链接除外），可离线阅读。"
                     "页面渲染器来自 <a href=\"%s\" target=\"_blank\" rel=\"noopener\">"
                     "cdyforever/how-to-live-better</a>（不作权利保留）；由 build.py 生成。",
        "foot_translated": None,  # zh is the original, not a translation
    },
    "en": {
        "label": "English",
        "html_lang": "en",
        "book_title": "How to Live Better",
        "fields_kw": {"Cost": "cost", "In plain terms": "plain", "Benefit": "benefit",
                      "Evidence grade": "evidence", "Sources": "source", "Note": "note"},
        "tag_keys": {"money": "money", "time": "time", "will": "will",
                     "benefit": "benefit", "metric": "metric"},
        "tag_vals": {
            "money": {"none": "none", "low": "low", "high": "high"},
            "time": {"low": "low", "medium": "mid", "high": "high"},
            "will": {"no": "no", "some": "some", "yes": "yes"},
            "benefit": {"large": "large", "medium": "mid", "small": "small"},
            "metric": {"mortality": "mortality", "money": "money",
                       "time": "time", "freedom": "freedom"},
        },
        "disp": {
            "money": {"none": "none", "low": "low", "high": "high"},
            "time": {"low": "low", "mid": "medium", "high": "high"},
            "will": {"no": "none", "some": "some", "yes": "yes"},
            "benefit": {"large": "large", "mid": "medium", "small": "small"},
            "metric": {"mortality": "mortality", "money": "money",
                       "time": "time", "freedom": "freedom"},
            "tier": {"vhigh": "very high", "high": "high", "avg": "average"},
        },
        "tag_disp": {"money": "Money", "time": "Time", "will": "Willpower",
                     "benefit": "Benefit", "metric": "Metric"},
        "chip_sep": ": ",
        "grade_fmt": "Grade %s",
        "tier_fmt": "Value: %s",
        "toc_clip": 46,
        "scope_all": "all %d sections",
        "scope_sel": "sections %s",
        "meta_desc": "How to Live Better (《高性价比人生指南》) — %s, %d recommendations in total. "
                     "Every entry lists its costs, benefits, evidence grade (A/B/C) and links to the "
                     "underlying research. Single file, zero dependencies, readable offline.",
        "search_ph": "Search titles, plain terms, benefits…",
        "btn_all": "All",
        "btn_a": "Grade A only",
        "btn_plain": "Plain terms only",
        # optional: which evidence-grade filter the page opens with
        # ('all' everywhere by default; the English page ships with 'A')
        "filter_init": "A",
        "btn_theme": "Theme",
        "theme_aria": "Toggle light/dark theme",
        "jump_aria": "Jump to a section",
        "count_js": "%1 / %2 entries",
        "empty": "No matching entries",
        "top_title": "Back to top",
        "toc_count": "%d entries",
        "toc_show_all": "Show all",
        "toc_hide_all": "Collapse all",
        "src_one": "Sources",
        "src_many": "Sources (%d references)",
        "langs_aria": "Language",
        "foot_source": "Content: <em>How to Live Better</em> (《高性价比人生指南》) by "
                       "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">eternity4719/HowToLiveBetter</a>, "
                       "licensed <a href=\"%s\" target=\"_blank\" rel=\"noopener\">CC BY 4.0</a>",
        "foot_snapshot": "; snapshot <span style=\"font-family:var(--mono)\">%s</span>%s",
        "snap_date": " (%s)",
        "foot_excerpt": "The “In plain terms” and “Benefit” columns are translated from the Chinese original; "
                        "%d entries on this page — Grade A: %d, Grade B: %d, Grade C: %d — "
                        "with %d outbound literature links.",
        "foot_self": "Self-contained single file: no external resources are loaded (apart from the "
                     "literature links inside the text), so it reads offline. Page rendered with the "
                     "single-file builder from <a href=\"%s\" target=\"_blank\" rel=\"noopener\">"
                     "cdyforever/how-to-live-better</a> (no rights reserved); generated by build.py.",
        "foot_translated": "English translation by the maintainers of this repository, offered under CC BY 4.0.",
    },
    "de": {
        "label": "Deutsch",
        "html_lang": "de",
        "book_title": "Besser leben",
        "fields_kw": {"Kosten": "cost", "Klartext": "plain", "Nutzen": "benefit",
                      "Evidenzgrad": "evidence", "Quellen": "source", "Hinweis": "note"},
        "tag_keys": {"Geld": "money", "Zeit": "time", "Wille": "will",
                     "Nutzen": "benefit", "Kennzahl": "metric"},
        "tag_vals": {  # file token -> canonical value (no ß in tokens)
            "money": {"0": "none", "wenig": "low", "viel": "high"},
            "time": {"wenig": "low", "mittel": "mid", "viel": "high"},
            "will": {"nein": "no", "etwas": "some", "ja": "yes"},
            "benefit": {"gross": "large", "mittel": "mid", "klein": "small"},
            "metric": {"Sterblichkeit": "mortality", "Geld": "money",
                       "Zeit": "time", "Freiheit": "freedom"},
        },
        "disp": {  # canonical value -> display
            "money": {"none": "0", "low": "wenig", "high": "viel"},
            "time": {"low": "wenig", "mid": "mittel", "high": "viel"},
            "will": {"no": "keiner", "some": "etwas", "yes": "ja"},
            "benefit": {"large": "groß", "mid": "mittel", "small": "klein"},
            "metric": {"mortality": "Sterblichkeit", "money": "Geld",
                       "time": "Zeit", "freedom": "Freiheit"},
            "tier": {"vhigh": "sehr hoch", "high": "hoch", "avg": "durchschnittlich"},
        },
        "tag_disp": {"money": "Geld", "time": "Zeit", "will": "Wille",
                     "benefit": "Nutzen", "metric": "Kennzahl"},
        "chip_sep": ": ",
        "grade_fmt": "Stufe %s",
        "tier_fmt": "Preis-Leistung: %s",
        "toc_clip": 52,
        "scope_all": "alle %d Abschnitte",
        "scope_sel": "Abschnitte %s",
        "meta_desc": "Besser leben (《高性价比人生指南》) — %s, insgesamt %d Empfehlungen. "
                     "Jeder Eintrag nennt Kosten, Nutzen, Evidenzgrad (A/B/C) und Links zu den "
                     "zugrunde liegenden Studien. Eine einzige Datei, keine externen Abhängigkeiten, offline lesbar.",
        "search_ph": "Titel, Klartext, Nutzen suchen …",
        "btn_all": "Alle",
        "btn_a": "Nur Stufe A",
        "btn_plain": "Nur Klartext",
        "btn_theme": "Hell/Dunkel",
        "theme_aria": "Zwischen hellem und dunklem Design wechseln",
        "jump_aria": "Zu einem Abschnitt springen",
        "count_js": ["%1 / %2 Eintrag", "%1 / %2 Einträge"],
        "empty": "Keine passenden Einträge",
        "top_title": "Nach oben",
        "toc_count": "%d Einträge",
        "toc_show_all": "Alles anzeigen",
        "toc_hide_all": "Alles einklappen",
        "src_one": "Quelle",
        "src_many": "Quellen (%d Literaturangaben)",
        "langs_aria": "Sprache",
        "foot_source": "Inhalt: <em>Besser leben</em> (《高性价比人生指南》) von "
                       "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">eternity4719/HowToLiveBetter</a>, "
                       "lizenziert unter <a href=\"%s\" target=\"_blank\" rel=\"noopener\">CC BY 4.0</a>",
        "foot_snapshot": "; Stand <span style=\"font-family:var(--mono)\">%s</span>%s",
        "snap_date": " (%s)",
        "foot_excerpt": "Die Spalten „Klartext“ und „Nutzen“ sind Übersetzungen aus dem chinesischen Original; "
                        "%d Einträge auf dieser Seite — Stufe A: %d, Stufe B: %d, Stufe C: %d — "
                        "mit %d Literatur-Verweisen.",
        "foot_self": "Eine einzige Datei ohne externe Ressourcen (abgesehen von den Literatur-Verweisen im Text), "
                     "daher offline lesbar. Seite gerendert mit dem Einzeldatei-Builder aus "
                     "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">cdyforever/how-to-live-better</a> "
                     "(ohne Rechtevorbehalt); erzeugt von build.py.",
        "foot_translated": "Deutsche Übersetzung durch die Pflegepersonen dieses Repositories, unter CC BY 4.0 angeboten.",
    },
    "ru": {
        "label": "Русский",
        "html_lang": "ru",
        "book_title": "Как жить лучше",
        "fields_kw": {"Затраты": "cost", "Простыми словами": "plain", "Польза": "benefit",
                      "Уровень доказательности": "evidence", "Источники": "source", "Примечание": "note"},
        "tag_keys": {"деньги": "money", "время": "time", "воля": "will",
                     "польза": "benefit", "метрика": "metric"},
        "tag_vals": {
            "money": {"нет": "none", "мало": "low", "много": "high"},
            "time": {"мало": "low", "средне": "mid", "много": "high"},
            "will": {"нет": "no", "немного": "some", "да": "yes"},
            "benefit": {"большая": "large", "средняя": "mid", "малая": "small"},
            "metric": {"смертность": "mortality", "деньги": "money",
                       "время": "time", "свобода": "freedom"},
        },
        "disp": {
            "money": {"none": "нет", "low": "мало", "high": "много"},
            "time": {"low": "мало", "mid": "средне", "high": "много"},
            "will": {"no": "нет", "some": "немного", "yes": "да"},
            "benefit": {"large": "большая", "mid": "средняя", "small": "малая"},
            "metric": {"mortality": "смертность", "money": "деньги",
                       "time": "время", "freedom": "свобода"},
            "tier": {"vhigh": "очень высокая", "high": "высокая", "avg": "средняя"},
        },
        "tag_disp": {"money": "Деньги", "time": "Время", "will": "Воля",
                     "benefit": "Польза", "metric": "Метрика"},
        "chip_sep": ": ",
        "grade_fmt": "Уровень %s",
        "tier_fmt": "Ценность: %s",
        "toc_clip": 50,
        "scope_all": "все %d раздела",
        "scope_sel": "разделы %s",
        "meta_desc": "«Как жить лучше» (《高性价比人生指南》) — %s, всего %d советов. "
                     "Для каждого совета указаны затраты, польза, уровень доказательности (A/B/C) "
                     "и ссылки на первоисточники. Один файл, без внешних зависимостей, можно читать офлайн.",
        "search_ph": "Искать в заголовках, простых словах, пользе…",
        "btn_all": "Все",
        "btn_a": "Только уровень A",
        "btn_plain": "Только «простыми словами»",
        "btn_theme": "Тема",
        "theme_aria": "Переключить светлую и тёмную тему",
        "jump_aria": "Перейти к разделу",
        "count_js": ["%1 / %2 совет", "%1 / %2 совета", "%1 / %2 советов"],
        "empty": "Подходящих записей нет",
        "top_title": "Наверх",
        "toc_count": "%d",
        "toc_show_all": "Показать все",
        "toc_hide_all": "Свернуть все",
        "src_one": "Источник",
        "src_many": "Источники (%d)",
        "langs_aria": "Язык",
        "foot_source": "Содержание: «Как жить лучше» (《高性价比人生指南》) — "
                       "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">eternity4719/HowToLiveBetter</a>, "
                       "лицензия <a href=\"%s\" target=\"_blank\" rel=\"noopener\">CC BY 4.0</a>",
        "foot_snapshot": "; снимок данных <span style=\"font-family:var(--mono)\">%s</span>%s",
        "snap_date": " (%s)",
        "foot_excerpt": "Колонки «Простыми словами» и «Польза» переведены с китайского оригинала; "
                        "на этой странице %d записей — уровень A: %d, уровень B: %d, уровень C: %d — "
                        "и %d внешних ссылок на литературу.",
        "foot_self": "Самодостаточный файл: никакие внешние ресурсы не загружаются (кроме ссылок на "
                     "литературу внутри текста), поэтому страницу можно читать офлайн. Рендерер страницы — "
                     "из <a href=\"%s\" target=\"_blank\" rel=\"noopener\">cdyforever/how-to-live-better</a> "
                     "(без сохранения прав); сгенерировано build.py.",
        "foot_translated": "Русский перевод — авторы этого репозитория; публикуется по лицензии CC BY 4.0.",
    },
    "sr": {
        "label": "Srpski",
        "html_lang": "sr",
        "book_title": "Kako živeti bolje",
        "fields_kw": {"Trošak": "cost", "Prostim jezikom": "plain", "Korist": "benefit",
                      "Nivo dokaza": "evidence", "Izvori": "source", "Napomena": "note"},
        "tag_keys": {"novac": "money", "vreme": "time", "volja": "will",
                     "korist": "benefit", "mera": "metric"},
        "tag_vals": {
            "money": {"nema": "none", "malo": "low", "puno": "high"},
            "time": {"malo": "low", "srednje": "mid", "puno": "high"},
            "will": {"ne": "no", "delimično": "some", "da": "yes"},
            "benefit": {"velika": "large", "srednja": "mid", "mala": "small"},
            "metric": {"smrtnost": "mortality", "novac": "money",
                       "vreme": "time", "sloboda": "freedom"},
        },
        "disp": {
            "money": {"none": "0", "low": "malo", "high": "puno"},
            "time": {"low": "malo", "mid": "srednje", "high": "puno"},
            "will": {"no": "ne", "some": "delimično", "yes": "da"},
            "benefit": {"large": "velika", "mid": "srednja", "small": "mala"},
            "metric": {"mortality": "smrtnost", "money": "novac",
                        "time": "vreme", "freedom": "sloboda"},
            "tier": {"vhigh": "vrlo visoka", "high": "visoka", "avg": "prosečna"},
        },
        "tag_disp": {"money": "Novac", "time": "Vreme", "will": "Volja",
                      "benefit": "Korist", "metric": "Mera"},
        "chip_sep": ": ",
        "grade_fmt": "Ocena %s",
        "tier_fmt": "Isplativost: %s",
        "toc_clip": 42,
        "scope_all": "svih %d odeljaka",
        "scope_sel": "odeljci %s",
        "meta_desc": "Kako živeti bolje (《高性价比人生指南》) — %s, ukupno %d preporuka. "
                     "Svaka stavka navodi troškove, korist, nivo dokaza (A/B/C) i linkove "
                     "ka istraživanjima na kojima se zasniva. Jedna datoteka, bez zavisnosti, "
                     "čitljivo i bez interneta.",
        "search_ph": "Pretraži naslove, prosta objašnjenja, koristi…",
        "btn_all": "Sve",
        "btn_a": "Samo ocena A",
        "btn_plain": "Samo prosta objašnjenja",
        "btn_theme": "Tema",
        "theme_aria": "Prebaci svetlu/tamnu temu",
        "jump_aria": "Skoči na odeljak",
        "count_js": ["%1 / %2 stavka", "%1 / %2 stavke", "%1 / %2 stavki"],
        "empty": "Nema stavki koje odgovaraju pretrazi",
        "top_title": "Nazad na vrh",
        "toc_count": "%d stavki",
        "toc_show_all": "Prikaži sve",
        "toc_hide_all": "Skupi sve",
        "src_one": "Izvori",
        "src_many": "Izvori (%d referenci)",
        "langs_aria": "Jezik",
        "foot_source": "Sadržaj: <em>Kako živeti bolje</em> (《高性价比人生指南》) autora "
                       "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">eternity4719/HowToLiveBetter</a>, "
                       "pod licencom <a href=\"%s\" target=\"_blank\" rel=\"noopener\">CC BY 4.0</a>",
        "foot_snapshot": "; snimka <span style=\"font-family:var(--mono)\">%s</span>%s",
        "snap_date": " (%s)",
        "foot_excerpt": "Kolone „Prostim jezikom“ i „Korist“ prevedene su iz kineskog originala; "
                        "%d stavki na ovoj stranici — ocena A: %d, B: %d, C: %d — "
                        "sa %d spoljnih linkova ka literaturi.",
        "foot_self": "Sve je u jednoj datoteci: ne učitava se nijedan spoljni resurs "
                      "(osim linkova na literaturu u samom tekstu), pa se može čitati i bez interneta. "
                      "Stranicu renderuje alat za jednu datoteku iz "
                      "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">cdyforever/how-to-live-better</a> "
                      "(bez zadržavanja prava); generisao build.py.",
        "foot_translated": "Prevod na srpski pripremili održavaoci ovog repozitorijuma, dostupan pod licencom CC BY 4.0.",
    },
}


# ------------------------------------------------------------------- flags
# Simplified national flags, one per language, embedded as inline SVG so the
# pages stay single-file and offline (no emoji flags — they degrade to letter
# pairs on Windows — and no external images). Each is a few hundred bytes on
# a 30x20 viewBox; a CSS border in --divider keeps white areas visible in
# dark mode. The flag is decorative: the accessible name comes from the
# link's aria-label (switcher) or the text label beside the flag (landing
# language cards).

_STAR = ("M0-1 .224-.309 .951-.309 .363.118 .588.809 0 .382 -.588.809"
         " -.363.118 -.951-.309 -.224-.309Z")  # unit 5-point star, point up

FLAGS = {
    "zh": '<path fill="#DE2910" d="M0 0h30v20H0z"/><g fill="#FFDE00">'
          '<path d="%(s)s" transform="translate(5 5) scale(3)"/>'
          '<path d="%(s)s" transform="translate(10 2)"/>'
          '<path d="%(s)s" transform="translate(12 4)"/>'
          '<path d="%(s)s" transform="translate(12 7)"/>'
          '<path d="%(s)s" transform="translate(10 9)"/></g>' % {"s": _STAR},
    "en": '<path fill="#012169" d="M0 0h30v20H0z"/>'
          '<path stroke="#fff" stroke-width="3.4" d="M0 0l30 20M30 0L0 20"/>'
          '<path stroke="#C8102E" stroke-width="2" d="M0 0l30 20M30 0L0 20"/>'
          '<path stroke="#fff" stroke-width="6.7" d="M15 0v20M0 10h30"/>'
          '<path stroke="#C8102E" stroke-width="4" d="M15 0v20M0 10h30"/>',
    "de": '<path fill="#000" d="M0 0h30v20H0z"/>'
          '<path fill="#D00" d="M0 6.7h30v6.6H0z"/>'
          '<path fill="#FFCE00" d="M0 13.3h30v6.7H0z"/>',
    "ru": '<path fill="#fff" d="M0 0h30v6.7H0z"/>'
          '<path fill="#0039A6" d="M0 6.7h30v6.6H0z"/>'
          '<path fill="#D52B1E" d="M0 13.3h30v6.7H0z"/>',
    "sr": '<path fill="#C6363C" d="M0 0h30v6.7H0z"/>'
          '<path fill="#0C4076" d="M0 6.7h30v6.6H0z"/>'
          '<path fill="#fff" d="M0 13.3h30v6.7H0z"/>'
          '<path fill="#C6363C" stroke="#FFCE00" stroke-width=".9" '
          'd="M11.8 8.3L15 7.4l3.2 .9v3.5c0 2.7-1.9 4.3-3.2 5'
          '-1.3-.7-3.2-2.3-3.2-5z"/>',
}


def flag_svg(code):
    """Decorative inline flag for a language link. The accessible name comes
    from the link's aria-label (switcher) or the text label rendered beside
    the flag (landing language cards)."""
    return ('<svg class="fl" viewBox="0 0 30 20" aria-hidden="true" '
            'focusable="false">%s</svg>' % FLAGS[code])


# ------------------------------------------------------------------ parsing


def avail_sections(lang):
    d = CONTENT / lang
    if not d.is_dir():
        return []
    return sorted(int(p.name[:2]) for p in d.glob("[0-9][0-9]-*.md"))


def find_file(lang, n):
    hits = sorted((CONTENT / lang).glob("%02d-*.md" % n))
    if not hits:
        raise SystemExit("language %r: no file for section %d" % (lang, n))
    return hits[0]


def compile_parsers(spec):
    """Build the per-language regexes: field lines and the cost-tag comment."""
    kw2canon = dict(spec["fields_kw"])
    field_re = re.compile(r"^-\s*(%s)\s*[:：]\s*(.*)$" %
                          "|".join(re.escape(k) for k in kw2canon))
    tagkey2canon = dict(spec["tag_keys"])
    tag_key_re = re.compile(r"(%s)=(\S+)" %
                            "|".join(re.escape(k) for k in tagkey2canon))
    tag_vals = spec["tag_vals"]

    def parse_tags(raw):
        if not raw:
            return {}
        out = {}
        for k, v in tag_key_re.findall(raw):
            canon = tagkey2canon[k]
            out[canon] = tag_vals[canon].get(v, v)
        return out

    return field_re, kw2canon, parse_tags


def parse(path, field_re, kw2canon):
    """Parse one content/<lang>/NN-*.md into (title, intro, entries).

    Same grammar as the upstream book: '# ' section title, '### N. ' entries,
    a '<!-- ... -->' cost-tag comment, '- Field: ...' bullet fields with
    continuation lines.
    """
    lines = path.read_text(encoding="utf-8").split("\n")
    title, intro, entries, cur = "", [], [], None
    for ln in lines:
        m = re.match(r"^#\s+(.*)$", ln)
        if m and not title:
            title = m.group(1).strip()
            continue
        m = re.match(r"^###\s+(\d+)\.\s*(.*)$", ln)
        if m:
            cur = {"no": int(m.group(1)), "title": m.group(2).strip(),
                   "tags_raw": None, "fields": {}, "last": None}
            entries.append(cur)
            continue
        if cur is None:
            if ln.strip() and not ln.startswith("["):
                intro.append(ln.strip())
            continue
        mt = re.match(r"^<!--\s*(.*?)\s*-->", ln)
        if mt:
            cur["tags_raw"] = mt.group(1)
            continue
        mf = field_re.match(ln)
        if mf:
            cur["last"] = kw2canon[mf.group(1)]
            cur["fields"][cur["last"]] = mf.group(2).strip()
            continue
        if not ln.strip():
            cur["last"] = None
            continue
        if cur["last"]:
            cur["fields"][cur["last"]] += ln.strip()
    return title, intro, entries


def inline(s):
    """把一小段 markdown 行内语法转成 HTML。先整体转义，再用占位符放链接。"""
    stash = []

    def mk(url, text=None):
        shown = text or url
        if len(shown) > 62:
            shown = shown[:59] + "…"
        stash.append('<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, shown))
        return "\u0001%d\u0001" % (len(stash) - 1)

    s = html.escape(s, quote=False)
    s = re.sub(r"&lt;(https?://[^\s]+?)&gt;", lambda m: mk(m.group(1)), s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", lambda m: mk(m.group(2), m.group(1)), s)
    s = re.sub(r"(?<![\w\"=])(https?://[^\s，。；）)]+)", lambda m: mk(m.group(1)), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = s.replace("\\*", "*").replace("\\_", "_")
    s = re.sub("\u0001(\\d+)\u0001", lambda m: stash[int(m.group(1))], s)
    return s


def link_count(s):
    return len(re.findall(r"https?://", s or ""))


# ---------------------------------------------------------------- rendering

# Inline SVG favicon (sprout + sun) so every page stays a single, offline-readable file.
FAVICON = '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 64 64\'%3E%3Cdefs%3E%3ClinearGradient id=\'g\' x1=\'0\' y1=\'0\' x2=\'1\' y2=\'1\'%3E%3Cstop offset=\'0\' stop-color=\'%234a6be0\'/%3E%3Cstop offset=\'1\' stop-color=\'%232c3f96\'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width=\'64\' height=\'64\' rx=\'15\' fill=\'url(%23g)\'/%3E%3Ccircle cx=\'47\' cy=\'17\' r=\'6\' fill=\'%23f9b44e\'/%3E%3Cpath d=\'M32 54V31\' stroke=\'%23fff\' stroke-width=\'5\' stroke-linecap=\'round\' fill=\'none\'/%3E%3Cpath d=\'M32 34C32 23 25 17 13 17c0 11 7 17 19 17z\' fill=\'%23fff\'/%3E%3Cpath d=\'M32 40c0-9 6-14 16-14 0 9-6 14-16 14z\' fill=\'%23c3d0ff\'/%3E%3C/svg%3E">'


CSS = r"""
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#ffffff;--bg-alt:#f6f6f7;--bg-elv:#ffffff;--bg-mute:#f1f1f2;
  --divider:#e2e2e3;
  --t1:rgba(60,60,67,1);--t2:rgba(60,60,67,.78);--t3:rgba(60,60,67,.56);
  --brand-1:#3451b2;--brand-2:#3a5ccc;--brand-soft:rgba(100,108,255,.12);
  --green-1:#18794e;--green-soft:rgba(16,185,129,.13);
  --yellow-1:#915930;--yellow-soft:rgba(234,179,8,.15);
  --red-1:#b8272c;--red-soft:rgba(244,63,94,.12);
  --gray-1:#565a5f;--gray-soft:rgba(142,150,170,.15);
  --mark:rgba(234,179,8,.34);
  --font:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --bar:56px;--side:296px;
}
[data-theme=dark]{
  --bg:#1b1b1f;--bg-alt:#161618;--bg-elv:#202127;--bg-mute:#2b2b2f;
  --divider:#2e2e32;
  --t1:rgba(255,255,245,.88);--t2:rgba(235,235,245,.62);--t3:rgba(235,235,245,.4);
  --brand-1:#a8b1ff;--brand-2:#c3c9ff;--brand-soft:rgba(100,108,255,.18);
  --green-1:#3dd68c;--green-soft:rgba(16,185,129,.16);
  --yellow-1:#f9b44e;--yellow-soft:rgba(234,179,8,.16);
  --red-1:#f66f81;--red-soft:rgba(244,63,94,.16);
  --gray-1:#a4a8ae;--gray-soft:rgba(142,150,170,.16);
  --mark:rgba(234,179,8,.3);
}
html{scroll-behavior:smooth;scroll-padding-top:calc(var(--bar) + 14px)}
body{margin:0;background:var(--bg);color:var(--t1);font:15px/1.75 var(--font);
  -webkit-font-smoothing:antialiased;-webkit-text-size-adjust:100%}
a{color:var(--brand-1);text-decoration:none}
a:hover{color:var(--brand-2);text-decoration:underline;text-underline-offset:2px}
mark{background:var(--mark);color:inherit;border-radius:2px;padding:0 1px}
strong{font-weight:600;color:var(--t1)}

/* min-height 用常量、不用 --bar：--bar 是 JS 实测回写的值，
   若拿它当 min-height，顶栏收起后会因为 min-height 还停在旧高度而缩不下去。 */
.bar{position:sticky;top:0;z-index:30;display:flex;flex-wrap:wrap;align-items:center;gap:10px;
  padding:0 18px;min-height:56px;background:var(--bg);border-bottom:1px solid var(--divider)}
.bar h1{font-size:15px;font-weight:600;margin:0;white-space:nowrap;min-width:0}
.bar h1 small{font-weight:400;font-size:12px;color:var(--t3);margin-left:8px}
.spacer{flex:1}
.search{position:relative;width:300px;max-width:42vw}
.search input{width:100%;height:34px;padding:0 30px 0 32px;border-radius:8px;border:1px solid var(--divider);
  background:var(--bg-alt);color:var(--t1);font:inherit;font-size:13px}
.search input:focus{outline:0;border-color:var(--brand-1);background:var(--bg-elv)}
.search svg{position:absolute;left:9px;top:50%;transform:translateY(-50%);width:15px;height:15px;
  fill:none;stroke:var(--t3);stroke-width:2;pointer-events:none}
.search kbd{position:absolute;right:8px;top:50%;transform:translateY(-50%);font:500 10px/1 var(--font);
  color:var(--t3);border:1px solid var(--divider);border-radius:4px;padding:2px 4px;background:var(--bg-elv)}
.btn{height:30px;padding:0 11px;border-radius:999px;border:1px solid var(--divider);background:var(--bg-elv);
  color:var(--t2);font:500 12px/1 var(--font);cursor:pointer;transition:all .18s;white-space:nowrap}
.btn:hover{border-color:var(--brand-2);color:var(--t1)}
.btn[aria-pressed=true]{background:var(--brand-soft);border-color:var(--brand-1);color:var(--brand-1)}
.count{font-size:12px;color:var(--t3);white-space:nowrap;font-variant-numeric:tabular-nums}
.langs{display:flex;align-items:center;gap:0;font-size:12.5px;white-space:nowrap}
.langs a{display:inline-flex;align-items:center;color:var(--t3);padding:4px 6px;border-radius:6px}
.fl{width:16px;height:11px;flex:none;border-radius:2px;border:1px solid var(--divider)}
.langs a:hover,.langs a:focus{color:var(--t1);background:var(--bg-mute);text-decoration:none;box-shadow:inset 0 -2px 0 var(--t1)}
.langs a[aria-current=true]{background:var(--brand-soft);box-shadow:inset 0 0 0 2px var(--brand-1)}
.langs i{font-style:normal;color:var(--divider);margin:0 -1px}
.jump{display:none;height:30px;max-width:38vw;padding:0 6px;border-radius:8px;border:1px solid var(--divider);
  background:var(--bg-elv);color:var(--t2);font:500 12px/1 var(--font)}

.shell{display:flex;align-items:flex-start}
.toc{position:sticky;top:var(--bar);flex:none;width:var(--side);height:calc(100vh - var(--bar));
  overflow-y:auto;padding:18px 14px 80px 18px;background:var(--bg-alt);border-right:1px solid var(--divider)}
.toc .gt{width:100%;padding:2px 6px;margin:0 -6px 6px;border:0;background:none;border-radius:6px;
  font:600 13px/1.6 var(--font);color:var(--t1);text-align:left;cursor:pointer;
  display:flex;justify-content:space-between;align-items:baseline;gap:6px}
.toc .gt:hover{color:var(--brand-1)}
.toc .gt:focus-visible{outline:2px solid var(--brand-1);outline-offset:1px}
.toc .gt::before{content:"▸";flex:none;font-size:10px;color:var(--t3);transition:transform .2s ease}
@supports (content:"x"/""){.toc .gt::before{content:"▸"/""}}
.toc .grp:not(.closed) .gt::before{transform:rotate(90deg)}
.toc .gt .ttl{flex:1;min-width:0}
.toc .gt small{font-weight:400;font-size:11px;color:var(--t3)}
.toc .grp{padding-bottom:14px;margin-bottom:14px;border-bottom:1px solid var(--divider)}
.toc .grp:last-of-type{border-bottom:0;margin-bottom:0}
.toc .gl{display:grid;grid-template-rows:1fr;transition:grid-template-rows .25s ease}
.toc .gl>.gli{min-height:0;overflow:hidden}
.toc .grp.closed .gl{grid-template-rows:0fr}
.toc .grp.closed .gl>.gli{visibility:hidden;transition:visibility 0s .25s}
.toc .gall{display:block;width:100%;padding:5px 6px;border:0;border-radius:6px;background:none;
  font:500 12px/1.6 var(--font);color:var(--t3);text-align:center;cursor:pointer}
.toc .gall[hidden]{display:none}
.toc .gall:hover{color:var(--brand-1)}
.toc .gall:focus-visible{outline:2px solid var(--brand-1);outline-offset:1px}
@media (prefers-reduced-motion:reduce){
  .toc .gl,.toc .grp.closed .gl>.gli,.toc .gt::before{transition:none}
}
.toc a{display:flex;gap:6px;align-items:baseline;padding:3px 6px;border-radius:6px;font-size:12.5px;
  line-height:1.5;color:var(--t2)}
.toc a:hover{background:var(--bg-elv);color:var(--t1);text-decoration:none}
.toc a.active{background:var(--brand-soft);color:var(--brand-1)}
.toc a i{font-style:normal;color:var(--t3);font-variant-numeric:tabular-nums;flex:none;min-width:16px;text-align:right}
.dot{width:6px;height:6px;border-radius:50%;flex:none;margin-top:6px}
.d0{background:var(--brand-1)}.d1{background:var(--green-1)}.d2{background:var(--t3)}

main{flex:1;min-width:0;padding:26px 40px 140px;max-width:940px}
section{margin-bottom:44px}
.sec-h{display:flex;align-items:baseline;gap:12px;padding-bottom:10px;border-bottom:2px solid var(--divider);margin-bottom:6px}
.sec-h h2{font-size:22px;font-weight:600;margin:0;letter-spacing:-.2px}
.sec-h .meta{font-size:12px;color:var(--t3);font-variant-numeric:tabular-nums}
.intro{color:var(--t2);font-size:14px;margin:12px 0 22px;padding-left:12px;border-left:2px solid var(--divider)}

.card{background:var(--bg-elv);border:1px solid var(--divider);border-radius:12px;padding:16px 18px 14px;margin-bottom:12px}
.chead{display:flex;gap:10px;align-items:flex-start}
.num{flex:none;min-width:24px;height:24px;padding:0 6px;border-radius:7px;background:var(--bg-mute);color:var(--t3);
  font:600 12px/24px var(--font);text-align:center;font-variant-numeric:tabular-nums}
.chead h3{margin:0;font-size:16px;font-weight:600;line-height:1.5;letter-spacing:-.1px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 12px 34px}
.badge{font:500 11px/1 var(--font);padding:4px 9px;border-radius:999px;border:1px solid transparent}
.gA{background:var(--green-soft);color:var(--green-1);border-color:var(--green-soft)}
.gB{background:var(--yellow-soft);color:var(--yellow-1);border-color:var(--yellow-soft)}
.gC{background:var(--gray-soft);color:var(--gray-1);border-color:var(--gray-soft)}
.r0{background:var(--brand-soft);color:var(--brand-1);border-color:var(--brand-soft)}
.r1{background:var(--green-soft);color:var(--green-1);border-color:var(--green-soft)}
.r2{background:var(--gray-soft);color:var(--gray-1);border-color:var(--gray-soft)}
.tag{font:400 11px/1 var(--font);padding:4px 9px;border-radius:999px;background:var(--bg-mute);color:var(--t3)}

.plain{margin:0 0 12px 34px;padding:10px 14px;background:var(--brand-soft);
  border-left:3px solid var(--brand-1);border-radius:0 8px 8px 0;font-size:15px;line-height:1.8;color:var(--t1)}
.fields{margin-left:34px}
.f{display:grid;grid-template-columns:52px 1fr;gap:10px;padding:7px 0;border-top:1px solid var(--divider);
  font-size:13.5px;line-height:1.75;color:var(--t2)}
.f b{font-weight:500;color:var(--t3);font-size:12.5px;padding-top:2px}
.f.note b{color:var(--yellow-1)}
.f>div{min-width:0;overflow-wrap:anywhere}
.src{margin:10px 0 0 34px;border-top:1px solid var(--divider);padding-top:8px}
.src summary{cursor:pointer;font-size:12.5px;color:var(--t3);list-style:none;user-select:none}
.src summary::-webkit-details-marker{display:none}
.src summary::before{content:"▸ ";color:var(--t3)}
.src[open] summary::before{content:"▾ "}
.src summary:hover{color:var(--brand-1)}
.src .sbody{font-size:12.5px;line-height:1.8;color:var(--t2);padding:8px 0 2px;word-break:break-word;overflow-wrap:anywhere}

body.plain-only .fields,body.plain-only .src{display:none}
.hidden{display:none!important}

.empty{color:var(--t3);font-size:14px;padding:40px 0;text-align:center}
footer{color:var(--t3);font-size:12px;border-top:1px solid var(--divider);padding-top:14px;line-height:1.9}
footer a{color:var(--t2)}

#top{position:fixed;right:16px;bottom:16px;z-index:40;width:42px;height:42px;border-radius:50%;
  border:1px solid var(--divider);background:var(--bg-elv);color:var(--t2);cursor:pointer;
  font:400 17px/1 var(--font);box-shadow:0 2px 12px rgba(0,0,0,.14);
  opacity:0;pointer-events:none;transition:opacity .2s,color .18s}
#top.show{opacity:1;pointer-events:auto}
#top:hover{color:var(--brand-1);border-color:var(--brand-1)}

@media (max-width:1080px){
  .toc{display:none}
  .jump{display:block}
  main{padding:22px 22px 130px;max-width:none}
}
@media (max-width:820px){
  .bar{padding:8px 12px;gap:8px;min-height:0}
  /* 顶栏三行：① 标题+节号+明暗 ② 筛选按钮+计数 ③ 搜索（独占整行，手机上才好打字） */
  .bar h1{order:1;flex:1 1 120px;font-size:14px;overflow:hidden;text-overflow:ellipsis}
  .spacer{display:none}
  .jump{order:2}
  #theme{order:3}
  .langs{order:4}
  #f-all{order:5}#f-a{order:6}#f-plain{order:7}
  .count{order:8;margin-left:auto}
  .search{order:9;width:auto;max-width:none;flex:1 1 100%;margin-top:2px}
  .search input{height:34px}
  .search kbd{display:none}
  /* 向下滚动后收成一行（标题+搜索+明暗），把竖向空间还给正文；滚回顶部再展开 */
  body.compact .jump,body.compact #f-all,body.compact #f-a,
  body.compact #f-plain,body.compact .count,body.compact .langs{display:none}
  body.compact .search{order:2;flex:1 1 120px;margin-top:0}
  body.compact #theme{order:3}
  main{padding:16px 13px 110px}
  .sec-h h2{font-size:19px}
  .card{padding:14px 14px 12px;border-radius:10px;margin-bottom:10px}
  .chead h3{font-size:15px}
  .plain{font-size:14.5px;padding:9px 12px}
  .f{font-size:13px;grid-template-columns:44px 1fr;gap:8px}
  .intro{font-size:13.5px;margin:10px 0 18px}
}
@media (max-width:520px){
  .bar h1 small{display:none}
  .chips,.plain,.fields,.src{margin-left:0}
  .num{min-width:22px;height:22px;font-size:11px;line-height:22px}
}
/* 320-380px 的窄屏：按钮和节号下拉都收紧，否则顶栏会被挤到多占一到两行 */
@media (max-width:380px){
  .btn{padding:0 8px;font-size:11px}
  .bar h1{flex:1 1 90px;font-size:13px}
  .jump{max-width:32vw}
}
@media print{
  .bar,.toc,#top{display:none}
  main{max-width:none;padding:0}
  .card{break-inside:avoid;border-color:#ccc}
  .src .sbody{display:block}
  body{font-size:11pt}
}
"""

JS_CORE = r"""
const cards=[...document.querySelectorAll('.card')];
const secs=[...document.querySelectorAll('section')];
const bar=document.querySelector('.bar');
const q=document.getElementById('q');
const cnt=document.getElementById('cnt');
const jump=document.getElementById('jump');
const fAll=document.getElementById('f-all');
const fA=document.getElementById('f-a');
const fP=document.getElementById('f-plain');
const themeBtn=document.getElementById('theme');
const topBtn=document.getElementById('top');
let grade=null, plainOnly=false;

/* 顶栏高度会随换行变化，交给 JS 实测，锚点跳转才不会被顶栏盖住 */
function syncBar(){
  const h=Math.round(bar.getBoundingClientRect().height);
  document.documentElement.style.setProperty('--bar', h+'px');
}

function clearMarks(root){
  const ms=[...root.querySelectorAll('mark')];
  ms.forEach(m=>m.replaceWith(document.createTextNode(m.textContent)));
  if(ms.length) root.normalize();
}
function markAll(root,term){
  if(!term) return;
  const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode(n){
    if(!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
    const p=n.parentElement;
    if(!p) return NodeFilter.FILTER_REJECT;
    if(p.closest('script,style,mark,a')) return NodeFilter.FILTER_REJECT;
    return NodeFilter.FILTER_ACCEPT;
  }});
  const nodes=[]; while(w.nextNode()) nodes.push(w.currentNode);
  const t=term.toLowerCase();
  nodes.forEach(n=>{
    const raw=n.nodeValue.toLowerCase();
    if(raw.indexOf(t)<0) return;
    const frag=document.createDocumentFragment();
    let i=raw.indexOf(t), last=0;
    while(i>=0){
      frag.appendChild(document.createTextNode(n.nodeValue.slice(last,i)));
      const m=document.createElement('mark');
      m.textContent=n.nodeValue.slice(i,i+t.length);
      frag.appendChild(m);
      last=i+t.length; i=raw.indexOf(t,last);
    }
    frag.appendChild(document.createTextNode(n.nodeValue.slice(last)));
    n.replaceWith(frag);
  });
}
function apply(){
  const term=q.value.trim().toLowerCase();
  /* 搜索时把目录分组全部展开，否则折叠组里的过滤结果看不见；清空后恢复搜索前的状态 */
  if(term&&!tocPre&&grps.length){
    tocPre=grps.map(g=>!g.classList.contains('closed'));
    grps.forEach(g=>setOpen(g,true));
  }else if(!term&&tocPre){
    grps.forEach((g,i)=>setOpen(g,tocPre[i]));
    tocPre=null;
  }
  clearMarks(document.querySelector('main'));
  let shown=0;
  cards.forEach(c=>{
    let ok=true;
    if(grade && c.dataset.grade!==grade) ok=false;
    if(ok && term && !c.textContent.toLowerCase().includes(term)) ok=false;
    c.classList.toggle('hidden',!ok);
    if(ok) shown++;
  });
  secs.forEach(s=>{
    const n=s.querySelectorAll('.card:not(.hidden)').length;
    s.classList.toggle('hidden',n===0);
    if(jump){
      const o=jump.querySelector('option[value="'+s.id+'"]');
      if(o) o.disabled=(n===0);
    }
  });
  document.getElementById('empty').classList.toggle('hidden',shown>0);
  cnt.textContent=cstr(shown).replace('%1',shown).replace('%2',cards.length);
  if(term) markAll(document.querySelector('main'),term);
  document.querySelectorAll('.toc a').forEach(a=>{
    const el=document.getElementById(a.getAttribute('href').slice(1));
    a.classList.toggle('hidden',!el||el.classList.contains('hidden'));
  });
}
let timer=null;
q.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(apply,90);});
function setMode(mode){
  grade=(mode==='A')?'A':null;
  plainOnly=(mode==='plain');
  document.body.classList.toggle('plain-only',plainOnly);
  const map={'all':fAll,'A':fA,'plain':fP};
  Object.keys(map).forEach(k=>map[k].setAttribute('aria-pressed',String(k===mode)));
  apply();
}
fAll.onclick=()=>setMode('all');
fA.onclick=()=>setMode('A');
fP.onclick=()=>setMode('plain');
fAll.setAttribute('aria-pressed','true');

if(jump){
  jump.addEventListener('change',()=>{
    const el=document.getElementById(jump.value);
    if(el) el.scrollIntoView({block:'start'});
  });
}
themeBtn.onclick=()=>{
  const cur=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';
  document.documentElement.setAttribute('data-theme',cur);
  try{localStorage.setItem('hltb-theme',cur);}catch(e){}
};
try{
  const t=localStorage.getItem('hltb-theme');
  if(t) document.documentElement.setAttribute('data-theme',t);
  else if(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)
    document.documentElement.setAttribute('data-theme','dark');
}catch(e){}
document.addEventListener('keydown',e=>{
  if(e.key==='/'&&document.activeElement!==q&&!/^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement.tagName)){
    e.preventDefault();q.focus();
  }
  if(e.key==='Escape'&&document.activeElement===q){q.value='';apply();q.blur();}
});
topBtn.onclick=()=>window.scrollTo({top:0,behavior:'smooth'});
/* 滚动状态：① 顶栏收起（手机）② 回到顶部按钮出现。
   用 rAF 节流，避免滚动时每帧都跑；阈值留迟滞区间，防止在临界点来回抖动。 */
let compact=false, ticking=false;
function onScroll(){
  const y=window.scrollY;
  const want = compact ? (y>200) : (y>420);
  if(want!==compact){compact=want;document.body.classList.toggle('compact',compact);syncBar();}
  topBtn.classList.toggle('show',y>900);
}
addEventListener('scroll',()=>{
  if(ticking) return;
  ticking=true;
  requestAnimationFrame(()=>{ticking=false;onScroll();});
},{passive:true});
addEventListener('resize',syncBar);
if(document.fonts&&document.fonts.ready) document.fonts.ready.then(syncBar);
syncBar();

const links=[...document.querySelectorAll('.toc a')];
/* ---- 目录手风琴：按分组折叠/展开 ----
   默认只展开当前阅读位置所在的组；滚动进入新分组时自动换组（autoFollow）。
   用户手动点过分组标题或“全部”按钮后，本次访问内不再自动换组；
   锚点跳转（目录链接、前进/后退）始终展开目标所在的组。 */
const grps=[...document.querySelectorAll('.toc .grp')];
const gall=document.getElementById('gall');
let autoFollow=true, tocPre=null;
function allOpen(){ return grps.every(g=>!g.classList.contains('closed')); }
function syncGall(){ if(gall) gall.textContent=allOpen()?L10N.collapseAll:L10N.showAll; }
function setOpen(g,open){
  g.classList.toggle('closed',!open);
  const b=g.querySelector('.gt');
  if(b) b.setAttribute('aria-expanded',String(open));
  syncGall();
}
function openOnly(g){ grps.forEach(x=>setOpen(x,x===g)); }
function groupFor(el){
  const s=el.closest('section');
  return s?document.querySelector('.toc .grp[data-sec="'+s.id.slice(3)+'"]'):null;
}
function openHashGroup(){
  const h=location.hash;
  if(!h||h.length<2) return false;
  const el=document.getElementById(h.slice(1));
  const g=el&&groupFor(el);
  if(!g) return false;
  setOpen(g,true);
  return true;
}
grps.forEach(g=>{
  const b=g.querySelector('.gt');
  if(b) b.addEventListener('click',()=>{
    autoFollow=false;
    setOpen(g,g.classList.contains('closed'));
  });
});
if(gall) gall.addEventListener('click',()=>{
  autoFollow=false;
  const open=!allOpen();
  grps.forEach(g=>setOpen(g,open));
});
if(grps.length){
  grps.forEach(g=>setOpen(g,false));
  if(!openHashGroup()) setOpen(grps[0],true);
  if(gall) gall.hidden=false;
}
addEventListener('hashchange',openHashGroup);
const io=new IntersectionObserver(es=>{
  es.forEach(e=>{ if(e.isIntersecting){
    if(e.target.classList.contains('card')){
      links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+e.target.id));
      if(autoFollow&&!q.value.trim()){
        const act=links.find(a=>a.getAttribute('href')==='#'+e.target.id);
        const g=act&&act.closest('.grp');
        if(g) openOnly(g);
      }
    }else if(jump && e.target.tagName==='SECTION')
      jump.value=e.target.id;
  }});
},{rootMargin:'-70px 0px -75% 0px'});
cards.forEach(c=>io.observe(c));
if(jump) secs.forEach(s=>io.observe(s));
"""

LANGS_JS = r"""
/* 语言切换：记住手动选择，回落地页时直接进该语言 */
document.querySelectorAll('.langs a').forEach(a=>{
  a.addEventListener('click',()=>{try{localStorage.setItem('hltb-lang',a.dataset.lang);}catch(e){}});
});
"""


def count_line(spec, shown, total):
    """Render the localized count line. count_js is either a single format
    string (zh/en), a 2-form [one, other] list selected by n == 1 (de), or a
    3-form [one, few, many] list with the Slavic 11-14 exception (ru/sr);
    the form is selected by the shown count."""
    c = spec["count_js"]
    if isinstance(c, str):
        return c.replace("%1", str(shown)).replace("%2", str(total))
    if len(c) == 2:
        i = 0 if shown == 1 else 1
    else:
        m, u = shown % 10, shown % 100
        i = 0 if (m == 1 and u != 11) else (1 if (2 <= m <= 4 and not 12 <= u <= 14) else 2)
    return c[i].replace("%1", str(shown)).replace("%2", str(total))


def page_js(count_fmt, filter_init="all", toc_toggle=None):
    """Identical page logic for every language; only the count-line format
    string (or its plural forms) is localized (injected as the L10N
    constant), plus the TOC show-all/collapse-all labels when toc_toggle is
    given as a (show_all, collapse_all) pair. A non-default filter_init
    appends one setMode() call so the page opens with that filter active
    (EN ships with Grade A preselected); the default leaves the emitted JS
    byte-identical to before. The cstr rules mirror count_line() — keep them
    in sync."""
    forms = json.dumps(count_fmt, ensure_ascii=False)
    if isinstance(count_fmt, str):
        l10n = "const L10N={count:%s};\nconst cstr=n=>L10N.count;\n" % forms
    elif len(count_fmt) == 2:
        l10n = "const L10N={count:%s};\nconst cstr=n=>L10N.count[n===1?0:1];\n" % forms
    else:
        l10n = ("const L10N={count:%s};\n"
                "const cstr=n=>{const m=n%%10,u=n%%100;"
                "return L10N.count[(m===1&&u!==11)?0:(m>=2&&m<=4&&(u<12||u>14))?1:2];};\n" % forms)
    if toc_toggle:
        l10n += ("L10N.showAll=%s;L10N.collapseAll=%s;\n"
                 % (json.dumps(toc_toggle[0], ensure_ascii=False),
                    json.dumps(toc_toggle[1], ensure_ascii=False)))
    init = ("" if filter_init == "all"
            else "setMode(%s);\n" % json.dumps(filter_init, ensure_ascii=False))
    return l10n + JS_CORE + LANGS_JS + init


def render_entry(e, sec_no, spec, parse_tags):
    t = parse_tags(e["tags_raw"])
    f = e["fields"]
    grade = (f.get("evidence") or "?").strip()[:1]
    ratio = ratio_of(t)
    disp, tk, sep = spec["disp"], spec["tag_disp"], spec["chip_sep"]
    chips = []
    gcls = {"A": "gA", "B": "gB", "C": "gC"}.get(grade, "gC")
    chips.append('<span class="badge %s">%s</span>' % (gcls, spec["grade_fmt"] % grade))
    if ratio:
        chips.append('<span class="badge r%d">%s</span>'
                     % (TIER_ORDER[ratio], spec["tier_fmt"] % disp["tier"][ratio]))
    if t.get("metric"):
        chips.append('<span class="tag">%s</span>' % (tk["metric"] + sep + disp["metric"][t["metric"]]))
    for k in ("money", "time", "will"):
        if t.get(k):
            chips.append('<span class="tag">%s</span>' % (tk[k] + sep + disp[k][t[k]]))
    if t.get("benefit"):
        chips.append('<span class="tag">%s</span>' % (tk["benefit"] + sep + disp["benefit"][t["benefit"]]))

    field_disp = {canon: kw for kw, canon in spec["fields_kw"].items()}
    rows = []
    for k in ("cost", "benefit"):
        if f.get(k):
            rows.append('<div class="f"><b>%s</b><div>%s</div></div>' % (field_disp[k], inline(f[k])))
    if f.get("note"):
        rows.append('<div class="f note"><b>%s</b><div>%s</div></div>' % (field_disp["note"], inline(f["note"])))

    src = f.get("source", "")
    n = link_count(src)
    src_html = ""
    if src:
        src_html = ('<details class="src"><summary>%s</summary>'
                    '<div class="sbody">%s</div></details>'
                    % ((spec["src_many"] % n) if n else spec["src_one"], inline(src)))

    return ('<article class="card" id="s%d-%d" data-grade="%s" data-ratio="%s">'
            '<div class="chead"><span class="num">%d</span><h3>%s</h3></div>'
            '<div class="chips">%s</div>'
            '<p class="plain">%s</p>'
            '<div class="fields">%s</div>%s</article>') % (
        sec_no, e["no"], grade, ratio or "-", e["no"], inline(e["title"]),
        "".join(chips), inline(f.get("plain", "")), "".join(rows), src_html)


def lang_switcher(current, built):
    """Compact switcher: flag-only links, no visible text; the language's
    own name lives in each link's aria-label and title tooltip."""
    parts = []
    for code in built:
        spec = LANGS[code]
        cur = ' aria-current="true"' if code == current else ""
        label = html.escape(spec["label"])
        parts.append('<a href="../%s/index.html" hreflang="%s" data-lang="%s" lang="%s" '
                     'aria-label="%s" title="%s"%s>%s</a>'
                     % (code, spec["html_lang"], code, spec["html_lang"],
                        label, label, cur, flag_svg(code)))
    return '<nav class="langs" aria-label="%s">%s</nav>' % (
        html.escape(LANGS[current]["langs_aria"]), "<i> · </i>".join(parts))


# ------------------------------------------------------------------ builds


def build_lang(lang, sections, out=None, built=None):
    spec = LANGS[lang]
    field_re, kw2canon, parse_tags = compile_parsers(spec)
    built = built or [lang]

    sec_toc, sec_html, jump_opts = [], [], []
    total = 0
    grade_cnt = {"A": 0, "B": 0, "C": 0}
    link_total = 0

    for n in sections:
        title, intro, entries = parse(find_file(lang, n), field_re, kw2canon)
        cards, links = [], []
        for e in entries:
            g = (e["fields"].get("evidence") or "?").strip()[:1]
            if g in grade_cnt:
                grade_cnt[g] += 1
            total += 1
            link_total += link_count(e["fields"].get("source", "")) + link_count(e["fields"].get("note", ""))
            cards.append(render_entry(e, n, spec, parse_tags))
            r = ratio_of(parse_tags(e["tags_raw"]))
            clip = spec["toc_clip"]
            short = e["title"] if len(e["title"]) <= clip else e["title"][:clip - 1] + "…"
            links.append('<a href="#s%d-%d" title="%s"><span class="dot d%d"></span>'
                         '<i>%d</i><span>%s</span></a>'
                         % (n, e["no"], html.escape(e["title"], quote=True),
                            TIER_ORDER.get(r, 2), e["no"], html.escape(short)))
        sec_toc.append('<div class="grp" data-sec="%d">'
                       '<button class="gt" type="button" aria-expanded="true" aria-controls="tocg%d">'
                       '<span class="ttl">%s</span><small>%s</small></button>'
                       '<div class="gl" id="tocg%d"><div class="gli">%s</div></div></div>'
                       % (n, n, inline(title), spec["toc_count"] % len(entries), n, "".join(links)))
        sec_html.append(
            '<section id="sec%d"><div class="sec-h"><h2>%s</h2>'
            '<span class="meta">%s</span></div>%s%s</section>'
            % (n, inline(title), spec["toc_count"] % len(entries),
               ('<p class="intro">%s</p>' % inline(" ".join(intro))) if intro else "",
               "".join(cards)))
        jump_opts.append('<option value="sec%d">%s</option>' % (n, html.escape(title)))

    rev, rev_date = load_vendor()
    all_secs = avail_sections(lang)
    scope = ((spec["scope_all"] % len(all_secs)) if sections == all_secs
             else spec["scope_sel"] % ", ".join(str(n) for n in sections))

    head = ('<!DOCTYPE html><html lang="%s" data-theme="light"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="color-scheme" content="light dark">'
            '<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff">'
            '<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#1b1b1f">'
            '<meta name="description" content="%s">%s'
            '<title>%s · %s</title><style>%s</style></head><body>'
            % (spec["html_lang"], html.escape(spec["meta_desc"] % (scope, total), quote=True), FAVICON,
               html.escape(spec["book_title"]), html.escape(scope), CSS))

    bar = ('<header class="bar"><h1>%s<small>%s</small></h1>'
           '<select class="jump" id="jump" aria-label="%s">%s</select>'
           '<div class="spacer"></div>'
           '<button class="btn" id="f-all">%s</button>'
           '<button class="btn" id="f-a">%s</button>'
           '<button class="btn" id="f-plain">%s</button>'
           '<div class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/>'
           '<path d="M20 20l-3.5-3.5"/></svg>'
           '<input id="q" type="search" placeholder="%s" autocomplete="off">'
           '<kbd>/</kbd></div>'
           '<span class="count" id="cnt">%s</span>%s'
           '<button class="btn" id="theme" aria-label="%s" title="%s">%s</button></header>' % (
               html.escape(spec["book_title"]), html.escape(scope),
               html.escape(spec["jump_aria"]), "".join(jump_opts),
               html.escape(spec["btn_all"]), html.escape(spec["btn_a"]), html.escape(spec["btn_plain"]),
               html.escape(spec["search_ph"], quote=True),
               html.escape(count_line(spec, total, total)),
               lang_switcher(lang, built),
               html.escape(spec["theme_aria"]), html.escape(spec["theme_aria"]),
               html.escape(spec["btn_theme"])))

    foot = spec["foot_source"] % (UPSTREAM, CC_BY)
    if rev:
        foot += spec["foot_snapshot"] % (rev, (spec["snap_date"] % rev_date) if rev_date else "")
    foot += ".<br>" + (spec["foot_excerpt"] % (total, grade_cnt["A"], grade_cnt["B"], grade_cnt["C"], link_total))
    foot += "<br>" + (spec["foot_self"] % RENDERER)
    if spec["foot_translated"]:
        foot += "<br>" + spec["foot_translated"]
    footer = "<footer>%s</footer>" % foot

    shell = ('<div class="shell"><aside class="toc">%s'
             '<button class="gall" id="gall" type="button" hidden>%s</button></aside><main>%s'
             '<div class="empty hidden" id="empty">%s</div>%s'
             '</main></div>'
             '<button id="top" title="%s" aria-label="%s">↑</button>'
             % ("".join(sec_toc), html.escape(spec["toc_show_all"]), "".join(sec_html), html.escape(spec["empty"]), footer,
                html.escape(spec["top_title"]), html.escape(spec["top_title"])))

    out_html = head + bar + shell + "<script>" + page_js(spec["count_js"], spec.get("filter_init", "all"),
                                                        (spec["toc_show_all"], spec["toc_hide_all"])) + "</script></body></html>"

    if out:
        name = Path(out)
        if not name.is_absolute():
            name = HERE / name
    else:
        name = HERE / lang / "index.html"
    name.parent.mkdir(parents=True, exist_ok=True)
    name.write_text(out_html, encoding="utf-8")

    print("[%s] sections %d | entries %d | A %d B %d C %d | links %d | %s (%d bytes)"
          % (lang, len(sections), total, grade_cnt["A"], grade_cnt["B"], grade_cnt["C"],
             link_total, name, len(out_html.encode("utf-8"))))
    return total


LANDING_CSS = r"""
*,*::before,*::after{box-sizing:border-box}
:root{--bg:#ffffff;--divider:#e2e2e3;--t1:rgba(60,60,67,1);--t2:rgba(60,60,67,.78);--t3:rgba(60,60,67,.56);
  --brand-1:#3451b2;--brand-2:#3a5ccc;--brand-soft:rgba(100,108,255,.12);
  --font:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif}
[data-theme=dark]{--bg:#1b1b1f;--divider:#2e2e32;--t1:rgba(255,255,245,.88);--t2:rgba(235,235,245,.62);
  --t3:rgba(235,235,245,.4);--brand-1:#a8b1ff;--brand-2:#c3c9ff;--brand-soft:rgba(100,108,255,.18)}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--t1);font:16px/1.8 var(--font);
  -webkit-font-smoothing:antialiased;min-height:100vh;display:flex;flex-direction:column}
main{flex:1;max-width:640px;margin:0 auto;padding:11vh 24px 40px}
h1{font-size:30px;font-weight:700;letter-spacing:-.5px;margin:0 0 6px}
h1 span{font-size:17px;font-weight:500;color:var(--t2);margin-left:10px;white-space:nowrap}
p{color:var(--t2);margin:0 0 34px}
ul{list-style:none;margin:0 0 40px;padding:0}
li{border:1px solid var(--divider);border-radius:12px;margin-bottom:10px;overflow:hidden}
li a{display:flex;align-items:center;gap:9px;padding:14px 18px;color:var(--t1);
  font-size:17px}
li a .fl{width:21px;height:14px;flex:none;border-radius:3px;border:1px solid var(--divider)}
li a:hover{background:var(--brand-soft);text-decoration:none;color:var(--brand-1)}
li a small{color:var(--t3);font-size:13px}
li a[lang]{font-weight:600}
footer{color:var(--t3);font-size:12.5px;border-top:1px solid var(--divider);
  max-width:640px;width:100%;margin:0 auto;padding:16px 24px 28px;line-height:1.9}
footer a{color:var(--t2)}
a{color:var(--brand-1);text-decoration:none}
a:hover{color:var(--brand-2);text-decoration:underline;text-underline-offset:2px}
"""


def build_landing(built, entry_total, section_total):
    codes = json.dumps(built)
    items = []
    for code in built:
        spec = LANGS[code]
        note = "原文" if code == "zh" else "translation"
        items.append('<li><a href="%s/" lang="%s">%s%s</a><small>%s</small></li>'
                     % (code, spec["html_lang"], flag_svg(code), spec["label"], note))
    foot = ('Content: <em>How to Live Better</em> (《高性价比人生指南》) by '
            '<a href="%s" target="_blank" rel="noopener">eternity4719/HowToLiveBetter</a>, '
            'licensed <a href="%s" target="_blank" rel="noopener">CC BY 4.0</a>. '
            'Page rendered with the builder from <a href="%s" target="_blank" rel="noopener">'
            'cdyforever/how-to-live-better</a> (no rights reserved). '
            'Translations into other languages are made by this repository.'
            % (UPSTREAM, CC_BY, RENDERER))
    rev, rev_date = load_vendor()
    if rev:
        foot += ' Snapshot <span style="font-family:ui-monospace,monospace">%s</span>%s.' % (
            rev, (" (%s)" % rev_date) if rev_date else "")
    page = ('<!DOCTYPE html><html lang="en" data-theme="light"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="color-scheme" content="light dark">'
            '<meta name="description" content="How to Live Better (《高性价比人生指南》) — '
            'a cost-effectiveness guide to life. %d sections, %d recommendations, each with costs, '
            'benefits, an evidence grade (A/B/C) and links to the research. Multiple languages, '
            'single-file pages, readable offline.">%s'
            '<title>How to Live Better · 高性价比人生指南</title>'
            '<style>%s</style></head><body><main>'
            '<h1>How to Live Better<span lang="zh">高性价比人生指南</span></h1>'
            '<p>A cost-effectiveness guide to life: %d sections, %d recommendations, each spelling '
            'out what it costs you, what it gets you, and how solid the evidence is. Pick a language:</p>'
            '<ul>%s</ul></main><footer>%s</footer>'
            '<script>var LANGS=%s;(function(){var d=document.documentElement;'
            'try{var t=localStorage.getItem(\'hltb-theme\');if(t)d.setAttribute(\'data-theme\',t);'
            'else if(window.matchMedia&&window.matchMedia(\'(prefers-color-scheme: dark)\').matches)'
            'd.setAttribute(\'data-theme\',\'dark\');}catch(e){}'
            'function go(c){location.replace(c+\'/\');}'
            'try{var s=localStorage.getItem(\'hltb-lang\');if(s&&LANGS.indexOf(s)>=0)return go(s);'
            'var p=navigator.languages||[navigator.language||\'en\'];'
            'for(var i=0;i<p.length;i++){var q=(p[i]||\'\').toLowerCase().split(\'-\')[0];'
            'if(LANGS.indexOf(q)>=0)return go(q);}}catch(e){}go(\'en\');})();</script>'
            '</body></html>'
            % (section_total, entry_total, FAVICON, LANDING_CSS, section_total, entry_total,
               "".join(items), foot, codes))
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("[landing] %d languages -> index.html (%d bytes)"
          % (len(built), len(page.encode("utf-8"))))


def main():
    ap = argparse.ArgumentParser(description="Build the multilingual single-file reading pages")
    ap.add_argument("sections", nargs="*", help="section numbers (dev; default: all sections)")
    ap.add_argument("--lang", default="all",
                    help="language code (%s) or 'all' (default)" % "/".join(LANGS))
    ap.add_argument("-o", "--out", default=None, help="output file (dev; default <lang>/index.html)")
    args = ap.parse_args()

    present = [c for c in LANGS if avail_sections(c)]
    if not present:
        raise SystemExit("no content/<lang>/NN-*.md found under %s" % CONTENT)

    if args.lang == "all":
        if args.sections:
            raise SystemExit("--lang all ignores section selection; use --lang <code> for a subset")
        for c in present:
            build_lang(c, avail_sections(c), built=present)
        zh = LANGS and "zh" in present
        # entry/section totals for the landing come from the original (zh)
        src_lang = "zh" if zh else present[0]
        field_re, kw2canon, _ = compile_parsers(LANGS[src_lang])
        total = 0
        for n in avail_sections(src_lang):
            _, _, entries = parse(find_file(src_lang, n), field_re, kw2canon)
            total += len(entries)
        build_landing(present, total, len(avail_sections(src_lang)))
        return

    if args.lang not in LANGS:
        raise SystemExit("unknown language %r; known: %s (dirs present: %s)"
                         % (args.lang, "/".join(LANGS), "/".join(present)))
    if args.lang not in present:
        raise SystemExit("language %r has no content directory" % args.lang)

    avail = avail_sections(args.lang)
    sections = [int(a) for a in args.sections] if args.sections else avail
    missing = [n for n in sections if n not in avail]
    if missing:
        raise SystemExit("language %r: no sections %s" % (args.lang, missing))
    build_lang(args.lang, sections, out=args.out, built=present)


if __name__ == "__main__":
    main()
