# Translation glossary (EN)

Canonical terminology for translating the book into English. Other languages
(DE/RU/SR) should maintain an equivalent table — copy this file's structure.

Numbers, units, confidence intervals, P values, and effect sizes are never
altered, converted, or rounded. Evidence grades (A/B/C), cost tiers, and value
tiers are never re-derived — the build recomputes them from the tags.

## Book-level terms

| Chinese | English |
|---|---|
| 《高性价比人生指南》 | *How to Live Better* (short: the book). Subtitle sense: "a cost-effectiveness guide to life" |
| 说人话 | In plain terms (field label); the plain-language column |
| 证据等级 | Evidence grade |
| A 级 / B 级 / C 级 | Grade A / Grade B / Grade C |
| 性价比 | value, in badges ("Value: …"); cost-effectiveness in prose |
| 极高 / 高 / 一般 (tier) | very high / high / average |
| 成本 | Cost |
| 收益 | Benefit |
| 备注 | Note |
| 来源 | Sources |
| 口径 | Metric (tag); "Metric:" at section start |
| 打折看 | discount this figure / take it with a discount |
| 反面清单 | the don't-do list |
| 荟萃分析 | meta-analysis |
| 随机对照试验 | randomized controlled trial |
| 队列研究 | cohort study |
| 病例对照研究 | case–control study |
| 观察性研究 | observational study |
| 风险比 | hazard ratio (HR) |
| 比值比 | odds ratio (OR) |
| 相对风险 | relative risk (RR) |
| 95% CI（可信范围） | 95% CI (confidence interval) |
| P 值 | P value |
| 质量调整生命年 | quality-adjusted life-year (QALY) |
| 四分位距 | interquartile range |
| 健康依从者效应 | healthy-adherer effect |
| 依从性 | adherence |
| 黑框警告 | boxed warning (FDA) |
| 强推荐 | strong recommendation |
| 有条件地推荐 | conditionally recommends |
| 证据确定性 | certainty of evidence |
| 全因死亡率 / 总死亡率 | all-cause mortality / overall mortality |
| 发病率 | incidence |
| 患病率 | prevalence |

## Tags (file tokens)

`<!-- costs: money=none time=low will=yes benefit=large metric=mortality -->`

| Chinese token | English token |
|---|---|
| 钱=0 / 少 / 多 | money=none / low / high |
| 时间=少 / 中 / 多 | time=low / medium / high |
| 毅力=否 / 些 / 是 | will=no / some / yes |
| 收益=大 / 中 / 小 | benefit=large / medium / small |
| 口径=死亡率 / 金钱 / 时间 / 自由 | metric=mortality / money / time / freedom |

## China-specific terms

| Chinese | English |
|---|---|
| 医保 | basic medical insurance (the public system); "bill insurance directly" for 刷医保 |
| 国家医保局 | National Healthcare Security Administration (NHSA) |
| 报销 / 报销比例 | reimbursement / reimbursement rate |
| 统筹地区 | insurance pooling area |
| 异地就医备案 | cross-region treatment registration (file it before traveling for care) |
| 门诊慢特病认定 | outpatient chronic/special-disease certification |
| 社区卫生服务中心 | community health center |
| 家庭医生（签约） | (contracted) family doctor |
| 三级医院 | tertiary hospital |
| 挂号（费） | hospital registration (fee) |
| 城乡居民 / 职工医保 | resident / employee medical insurance |
| 公积金 | housing provident fund |
| 元 / 万元 / 亿元 | yuan / 10,000 yuan / 100 million yuan (never convert) |
| 个百分点 | percentage point |
| 学区房 | school-district housing |
| 户口 | hukou (household registration) |

## Cross-references and style

- 见第 X 节第 Y 条 → "see Section X, item Y" (plain text, no hyperlink — match the original).
- Address the reader as "you"; imperatives for entry titles, matching the original's direct tone.
- 「……」 quotes → curly quotes “ ”. Keep `**bold**` and escaped `\*` exactly.
- Never invent, soften, or harden a medical, financial, or legal claim; translate the meaning exactly, including its hedges (约 → about, 可能 → may, 或许 → might).
- Where the original flags uncertainty ("这个数要打折看"), keep the flag equally visible.

---

# Translation glossary (SR)

Srpski — latinično pismo, ekavica (standard Srbije), pristojni oblik „vi", navodnici „…". Terminologija za prevod knjige na srpski; struktura odgovara engleskoj tabeli gore.

## Book-level terms (sr)

| Chinese | Serbian |
|---|---|
| 《高性价比人生指南》 | *Kako živeti bolje* (kratko: knjiga). Podnaslov: vodič kroz isplativost života |
| 说人话 | Prostim jezikom (naziv polja) |
| 证据等级 | Nivo dokaza |
| A 级 / B 级 / C 级 | ocena A / ocena B / ocena C (u tekstu: „Nivo dokaza: A") |
| 性价比 | isplativost (u prozi); vrednost (u bedževima) |
| 极高 / 高 / 一般 (tier) | vrlo visoka / visoka / prosezna |
| 成本 | Trošak |
| 收益 | Korist |
| 条 / 节 | stavka / odeljak („Odeljak 7, stavka 8" za 第 7 节第 8 条) |
| 元 | juan (nikad ne pretvarati u druge valute) |
| 相对风险 / 风险比 | RR — relativni rizik; OR — odnos šansi; HR — odnos opasnosti |
| 置信区间 | CI — raspon poverenja (95% CI … do …) |
| meta 分析 / 系统综述 | meta-analiza / sistematski pregled |
| 随机对照试验 | randomizovano kontrolisano iskušavanje |
| 队列研究 | kohortna studija |
| 作者经验，无直接文献 | Iskustvo autora, nema direktne literature |

## Tags (file tokens) — sr

`<!-- costs: novac=nema vreme=malo volja=delimično korist=velika mera=smrtnost -->`

| English token | Serbian token |
|---|---|
| money=none / low / high | novac=nema / malo / puno |
| time=low / medium / high | vreme=malo / srednje / puno |
| will=no / some / yes | volja=ne / delimično / da |
| benefit=large / medium / small | korist=velika / srednja / mala |
| metric=mortality / money / time / freedom | mera=smrtnost / novac / vreme / sloboda |

Napomena: dijakritike su obavezne u tokenima (`volja=delimično`, nikad `delimicno` — ASCII varijanta pada na proveri).

## Field labels (sr)

- Cost → `Trošak:` / In plain terms → `Prostim jezikom:` / Benefit → `Korist:` / Evidence grade → `Nivo dokaza:` / Sources → `Izvori:` / Note → `Napomena:`

## Style rules (sr)

- Latinica + ekavica; „…" navodnici; pristojni oblik „vi" u drugom licu.
- Brojevi: zapeta za hiljade, tačka za decimale — identično engleskom (100,000; 95% CI 1.03–1.31; P=0.02). Nikad tačka za hiljade („100.000" je greška).
- Izvori se kopiraju doslovno iz engleske verzije, uključujući kineski tekst i URL-ove; URL-ovi moraju odgovarati zh originalu po stavci (ne globalna zamena puteva).
- Finansijski/medicinski/pravni iskazi: nikad ne izmišljati, ublažavati ni pooštravati; hedge-ove preneti jednako vidljivo (约 → „oko", 可能 → „može", 或许 → „možda").
- Unakrsne reference: „Odeljak X, stavka Y" običан tekst, bez linka — kao u originalu.
- Srpske skovanice koje se ponavljaju: odeljak, stavka, ocena, isplativost, raspon poverenja, randomizovano kontrolisano iskušavanje, kohortna studija, sistematski pregled, zatajenje jetre/bubrega, prevencija, skrining, dozvola (licence), uverenje o rođenju.
