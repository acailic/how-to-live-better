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

## Translation glossary (RU)

Canonical Russian terminology, mirroring the English table above. Адресация читателя — неформальное «ты» во всей книге. Числа, единицы, доверительные интервалы, P-значения и величины эффекта никогда не меняются, не конвертируются и не округляются (запятая тысяч остаётся: 248,099). Уровни доказательности (A/B/C), стоимости и ценность не пересчитываются заново — их пересобирает build.py из тегов.

| Chinese | English | Русский |
|---|---|---|
| 《高性价比人生指南》 | *How to Live Better* | «Как жить лучше» |
| 说人话 | In plain terms | «Простыми словами» (метка поля); сама колонка читается как разговорная речь |
| 证据等级 | Evidence grade | Уровень доказательности |
| A 级 / B 级 / C 级 | Grade A / B / C | уровень A / B / C |
| 性价比 | value ("Value: …") | Ценность («Ценность: …»); в прозе — «соотношение затрат и пользы» |
| 极高 / 高 / 一般 (tier) | very high / high / average | очень высокая / высокая / средняя |
| 成本 / 收益 / 备注 / 来源 | Cost / Benefit / Note / Sources | Затраты / Польза / Примечание / Источники |
| 口径 | Metric | Метрика (тег); «Метрика:» в начале раздела |
| 打折看 | discount this figure | смотри на эту цифру со скидкой |
| 反面清单 | the don't-do list | список «не делай» |
| 荟萃分析 | meta-analysis | метаанализ |
| 随机对照试验 | randomized controlled trial | рандомизированное контролируемое испытание |
| 队列研究 | cohort study | когортное исследование |
| 病例对照研究 | case–control study | исследование «случай—контроль» |
| 观察性研究 | observational study | наблюдательное исследование |
| 风险比 / 比值比 / 相对风险 | hazard ratio / odds ratio / relative risk | HR / OR / RR (латиницей, как в оригинале) |
| 95% CI | 95% CI | 95% ДИ (доверительный интервал) |
| P 值 | P value | P-значение |
| 全因死亡率 | all-cause mortality | общая смертность |
| 发病率 / 患病率 | incidence / prevalence | заболеваемость / распространённость |
| 医保 | basic medical insurance | государственная базовая медицинская страховка |
| 国家医保局 | NHSA | Государственное управление медицинского страхования (NHSA) |
| 报销 / 报销比例 | reimbursement / rate | возмещение страховкой / доля возмещения |
| 统筹地区 | pooling area | зона страхового пула |
| 异地就医备案 | cross-region filing | межрегиональная регистрация лечения |
| 社区卫生服务中心 | community health center | центр здоровья общины/района |
| 三级医院 | tertiary hospital | больница третичного уровня |
| 元 / 万元 / 亿元 | yuan / 10,000 yuan / 100 million yuan | юань / 10,000 юаней / 100 миллионов юаней (никогда не конвертировать) |
| 个百分点 | percentage point | процентный пункт |
| 学区房 | school-district housing | жильё в школьном районе (学区房) |
| 户口 | hukou | хукоу (домохозяйственная регистрация) |

## Cross-references and style (RU)

- 见第 X 节第 Y 条 → «см. раздел X, совет Y» (простой текст, без гиперссылки — как в оригинале).
- Адресация читателя — неформальное «ты» во всей книге, императивы в заголовках советов.
- Кавычки «……」 → «ёлочки» « ». Сохранять `**жирный**` и экранированные `\*` ровно.
- Никогда не выдумывать, смягчать или ужесточать медицинское, финансовое или правовое утверждение; переводить смысл точно, включая оговорки (约 → около, 可能 → может, 或许 → возможно).
- Где оригинал помечает неопределённость («这个数要打折看»), пометка остаётся равно заметной.
- Названия исследований, имена авторов, обозначения (OR/RR/HR/CI) и ссылки остаются латиницей дословно.
