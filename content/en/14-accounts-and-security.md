# 14. Accounts and information security

Metrics: money and personal information. When someone logs into your account, money goes first; they'll also use your account to defraud your contacts — and your identity effectively walks away with them.

### 1. Turn on two-factor authentication for email, payment, and social accounts — app-popup approval first, SMS codes second
<!-- costs: money=none time=low will=no benefit=large metric=money -->
- Cost: Free. One setup per account, 2–3 minutes.
- In plain terms: Two-factor means a second confirmation beyond the password at login. A popup on your phone that you tap blocks over 90% of phishing takeovers. Answering "where did you last log in" and "what's your backup email" blocks only about 10%.
- Benefit: Google analyzed 350,000 real account-takeover attempts. Device-based verification — phone popups you confirm, or plugged-in security keys — blocked "over 94% of phishing-based takeover attempts and 100% of automated ones" (phishing meaning fake-site password harvesting; automated meaning bulk tries with leaked passwords). Knowledge-based verification — last-login locations, backup emails — "blocked as little as 10% of phishing takeovers and 73% of automated"
- Evidence grade: A
- Sources: Doerfler P, Thomas K, Marincenko M, et al. (2019). Evaluating Login Challenges as a Defense Against Account Takeover. The World Wide Web Conference (WWW '19). <https://doi.org/10.1145/3308558.3313481>
- Note: The same study found such challenges sometimes lock out the true owner — 52% of legitimate users failed the first try, though 97% eventually got in. Enable it on email first: most other accounts recover through email. Verification codes are yours alone — the cost of reading codes or face-scanning for others: Section 8, item 45.

### 2. Your email password stands alone — never reused anywhere
<!-- costs: money=none time=low will=some benefit=large metric=money -->
- Cost: Free. A password manager remembers it for you. The hard part: breaking the one-password habit.
- In plain terms: Passwords stolen from other sites get replayed straight against your email. Once your email falls, every account recoverable through it falls too. So the email password is used nowhere else.
- Benefit: Replaying leaked credentials site by site — credential stuffing — is the cheapest attack, and your email gets tried. One email breach cascades into every email-recoverable account. The US CISA's advice: a different strong password per account, at least 16 characters, stored in a password manager
- Evidence grade: C
- Sources: US CISA. Use Strong Passwords. <https://www.cisa.gov/secure-our-world/use-strong-passwords>
- Note: Use your browser's built-in password manager if nothing else — far better than one password everywhere. Don't store passwords in WeChat favorites or notes apps.

### 3. Set a lock-screen password on the phone and a PIN on the SIM
<!-- costs: money=none time=low will=no benefit=large metric=money -->
- Cost: Free. One setup each.
- In plain terms: The SIM is the little card inside — SMS verification codes arrive through it. Lose the phone, and whoever finds it pops the card into their own phone, harvests your codes, and resets account after account. A SIM PIN requires the code at every power-up in a new phone — closing the road.
- Benefit: After a lost phone, the finder's fastest route is your SIM in their phone collecting SMS codes — with codes, accounts reset one by one. A SIM PIN demands the code on boot in any new device, cutting the finder off
- Evidence grade: C
- Sources: 作者经验，无直接文献
- Note: The PIN lives under "SIM card lock" in settings; factory defaults are usually 1234 or 0000; three wrong entries demand the carrier's PUK — write both down on paper first.

### 4. Phone lost — this order: suspend the SIM, remote-lock, change passwords, report, freeze cards
<!-- costs: money=none time=low will=no benefit=large metric=money -->
- Cost: Free. The whole sequence takes a dozen-odd minutes.
- In plain terms: Order beats speed. Suspend the SIM first — the code lifeline dies. Remote-lock the phone next, change email and payment passwords from a computer, report to police for the receipt, then freeze bank cards as needed. Borrow any phone to call the carrier.
- Benefit: Order beats speed. Step one, suspend the SIM — codes stop arriving for anyone. Step two, remote-lock and wipe. Step three, change email and payment passwords from a computer. Step four, police report with receipt. Finally, freeze cards as needed. The US FCC concurs: remote-lock even if you think it's merely lost; when stolen, report immediately with model and IMEI (the phone's identity number) and notify the carrier at once
- Evidence grade: C
- Sources: US FCC. Protect Your Smart Device. <https://www.fcc.gov/consumers/guides/protect-your-mobile-device>；步骤顺序是作者经验；补办身份证见第 7 节，冒名贷款见第 8 节关于征信的一条
- Note: Save the three carriers' numbers now: China Mobile 10086, Unicom 10010, Telecom 10000. Note which city your number was registered in — the hotline will ask. Any borrowed phone works for suspension.

### 5. Card fraud: suspend and freeze first, report second, then demand the bank pay — proving "you did it yourself" is the bank's burden
<!-- costs: money=none time=low will=some benefit=large metric=money -->
- Cost: Free. On suspicious activity: freeze immediately. Keep the report, suspension, and transaction notifications. With the card still in hand, make one small transaction nearby to prove possession at the time. The hard part: suspending before arguing with customer service.
- In plain terms: You don't have to prove "that wasn't me" — the bank must prove the transaction was yours or authorized, or pay. The precondition: you suspended on discovery. Delaying, you eat the added losses.
- Benefit: The Supreme Court's provisions split the burden. You claim card-counterfeit or online fraud — you produce initial evidence: effective legal documents, the true card's location and the transaction's location, statements, notifications, police and suspension records. **Conversely, when the issuing bank or payment institution asserts the cardholder did or authorized the transaction, the evidence is theirs to produce.** Where the bank failed to verify promptly after your notice, or failed to preserve slips and footage, the evidentiary failure is theirs. Established: debit-card holders may reclaim the stolen principal and interest plus damages; credit-card holders may reclaim charged overdraft principal, interest, and penalties plus damages — banks demanding repayment of that overdraft get no court support — and may demand prompt removal of the adverse credit record (national; effective 2021-05-25)
- Evidence grade: A
- Sources: 最高人民法院 (2021). 关于审理银行卡民事纠纷案件若干问题的规定（第四、五、七、十四、十五条）. <https://www.court.gov.cn/fabu/xiangqing/304771.html>
- Note: Two situations leave you liable: your own fault in safeguarding card, password, or codes ("failure of proper custody with fault") — proportionate to the fault, so never share passwords or forward codes (item 1's popup first); and failure to suspend promptly, eating the expansion. So step one is always suspension, never argument. Third-party payment institutions follow the same rules — concrete, explicit "advance compensation" promises in their materials bind them. Money you were tricked into transferring yourself takes another route: Section 8, item 2.

### 6. Periodically review logged-in devices and authorized apps — clear what's unused
<!-- costs: money=none time=low will=some benefit=medium metric=money -->
- Cost: Free. Minutes per review. The hard part: remembering without reminders.
- In plain terms: "Logged-in devices" are the phones and computers that can still use your account. Takers usually lurk before acting. An unfamiliar device or long-dead app still linked: log out everywhere, change the password.
- Benefit: Takeovers rarely act immediately — the intruder lurks. The device list records which phones and computers currently reach the account; the authorized-apps list records which third-party software you permitted. Unfamiliar devices and dead third-party apps are the most visible traces
- Evidence grade: C
- Sources: 作者经验，无直接文献
- Note: WeChat, Alipay, email, and Apple/Android accounts all carry these entries. On anything unfamiliar: log out everywhere, then change the password.

### 7. Don't tap "agree to all" for an app: non-essential information may not be leveraged against service
<!-- costs: money=none time=low will=some benefit=medium metric=freedom -->
- Cost: Free. The hard part: resisting "agree to all."
- In plain terms: If the information isn't necessary for the service, refusing it can't be held against you — and collection is limited to what's genuinely needed. Maps need location; a flashlight doesn't need your contacts.
- Benefit: The law states two things: refusal or withdrawal of consent may not justify denying product or service, save where processing is necessary to provide it; and collection is limited to the minimum scope implementing the purpose — only what's needed
- Evidence grade: A
- Sources: 全国人大常委会 (2021). 个人信息保护法. 中国人大网. <http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html>：第六条「收集个人信息，应当限于实现处理目的的最小范围，不得过度收集个人信息」；第十六条「个人信息处理者不得以个人不同意处理其个人信息或者撤回同意为由，拒绝提供产品或者服务；处理个人信息属于提供产品或者服务所必需的除外」；第十五条「基于个人同意处理个人信息的，个人有权撤回其同意。个人信息处理者应当提供便捷的撤回同意的方式」
- Note: The test is necessity for the service — maps and location yes, flashlights and contacts no. After installing, switch off non-essential permissions in the app-permissions page, granting "just once" when genuinely needed.

### 8. You may view, copy, correct, and delete your personal information — refusal can be sued
<!-- costs: money=none time=low will=some benefit=medium metric=freedom -->
- Cost: Free. Complaints and suits come only on stonewalling — litigation runs months with your own attorney fees, so complain first. The hard part: repeated pushing when they stall.
- In plain terms: You may demand viewing, copying, correction, and deletion of your information. Service ended, retention expired, consent withdrawn — they should delete on their own. Refusal requires stated reasons; continued refusal, sue directly. Account cancellation and information deletion are two things — file deletion separately after canceling.
- Benefit: Several situations oblige active deletion: service ended, retention expired, consent withdrawn, purpose achieved. Undeleted, you may demand deletion; refused, reasons must be stated; you may sue directly
- Evidence grade: A
- Sources: 全国人大常委会 (2021). 个人信息保护法. 中国人大网. <http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html>：第四十五条「个人有权向个人信息处理者查阅、复制其个人信息……个人请求查阅、复制其个人信息的，个人信息处理者应当及时提供」；第四十六条更正、补充权；第四十七条列了五种应当主动删除的情形，含「（一）处理目的已实现、无法实现或者为实现处理目的不再必要」「（二）个人信息处理者停止提供产品或者服务，或者保存期限已届满」「（三）个人撤回同意」，「个人信息处理者未删除的，个人有权请求删除」；第五十条「个人信息处理者应当建立便捷的个人行使权利的申请受理和处理机制。拒绝个人行使权利的请求的，应当说明理由」「个人可以依法向人民法院提起诉讼」
- Note: Cancellation and deletion are separate — after canceling, file deletion separately. Before switching or selling phones: log out and unbind everything, then factory reset. The law grants after-the-fact deletion; it can't recall what already leaked.

### 9. Face-scanning is never mandatory: alternatives exist means face-only is barred — disagreement must earn you another way
<!-- costs: money=none time=low will=some benefit=medium metric=money -->
- Cost: Free. When asked to scan, ask "is there another verification?" On "no," demand one. The hard part: asking aloud.
- In plain terms: Where another method achieves the same purpose, face-only verification is barred. Refusing the face must earn you card, password, or ID alternatives — no "then no service" coercion. Hotel rooms, public baths, changing rooms, and toilets admit no facial-recognition devices for anyone.
- Benefit: The facial-recognition security measures state: "where other non-facial-recognition means achieve the same purpose or equivalent business requirements, facial recognition may not be the sole verification method; where an individual disagrees with facial-identity verification, other reasonable and convenient means shall be provided," and "no organization or individual may mislead, defraud, or coerce individuals into accepting facial-identity verification on grounds of business handling or service quality." Processing facial data on consent requires "separate consent, voluntarily and explicitly given with full knowledge" — asked about this one thing, agreed to this one thing. Consent is withdrawable, with convenient withdrawal. Minors under 14 need parental or guardian consent. Public installations "must be necessary for public safety" with conspicuous signage; hotel rooms, public baths, changing rooms, and toilets — private spaces within public venues — admit no installations, full stop. Facial data must be stored on-device, never transmitted over the internet, save statutory provisions or separate consent (national; effective 2025-06-01)
- Evidence grade: A
- Sources: 国家互联网信息办公室、公安部 (2025). 人脸识别技术应用安全管理办法（第 19 号令，第十条、十二条、十三条，2025 年 6 月 1 日起施行）. <https://www.cac.gov.cn/2025-03/21/c_1744174262156096.htm>
- Note: The commonest encounters: compound gates, rental platforms, gyms, hotels. On "the system only supports faces," recite the measures: "where other non-facial-recognition means achieve the same purpose or equivalent business requirements, facial recognition may not be the sole verification method" — then demand card, password, or ID. Still refused: report to the local cyberspace administration. Sectors with separate state rules — some finance and government services — follow those. The deepest difference between faces and passwords: leaked faces can't be changed — treat them more carefully than passwords. Operators holding 100,000-plus facial records must file with provincial-plus cyberspace authorities within 30 working days — itself a question worth asking. View-correct-delete rights: item 8. Lending your face to someone else's loan is another matter entirely: Section 8, item 45.

### 10. Never hand code, keys, or private material to an unknown "AI relay" — especially with AI auto-executing commands
<!-- costs: money=low time=low will=some benefit=medium metric=freedom -->
- Cost: Official direct connections usually cost more and top up less conveniently. The hard part: relays are cheap and fan out to several models from one entrance.
- In plain terms: The relay sits between you and the model vendor, seeing and able to alter both your prompts and the replies. A study measured 400-plus relays: 9 injected malicious code into replies, and 17 touched honey-trap cloud keys. With AI auto-executing commands, one altered command can own the machine.
- Benefit: The state security ministry's June 2026 notice: some relays retain user data, secretly intercepting and reselling it to other model vendors for training; some hide backdoors planting malware to steal account keys and cloud credentials, even remote-control programs. The advice: official direct connections and properly licensed platforms only; sanitize private and project material before submission; manage and rotate keys; on abnormal billing, unexplained bans, or data anomalies — stop, rotate keys, scan for malware, preserve evidence. UCSB-led researchers' 2026 measurement: buying 28 paid relays from Taobao, Xianyu, and offshore shops plus 400 free relays from public communities — 1 paid and 8 free injected malicious code into returned tool calls (tool calls being commands the AI runs on your machine, like package installs); 2 timed their strikes, one example targeting only fully automated sessions; 17 touched deliberately planted AWS keys; 1 drained a researcher's Ethereum wallet — lightly funded, losses under 50 US dollars. The demonstrated alteration was subtle: swapping "requests" for the near-identical "reqeusts" in an install command, invisible at a glance (national)
- Evidence grade: B
- Sources: 国家安全部 (2026). 「AI中转站」，风险要防范. <https://www.szzg.gov.cn/2026/xwzx/szkx/202606/t20260608_5331487.htm>（数字中国建设峰会官网转载国家安全部微信公众号）；Liu H, Shou C, Wen H, Chen Y, Fang RJ, Feng Y. (2026). Your Agent Is Mine: Measuring Malicious Intermediary Attacks on the LLM Supply Chain. arXiv:2604.08407. <https://arxiv.org/abs/2604.08407>
- Note: Grade B: one study, preprint (the pre-publication version). Mostly free relays — only 28 paid — so "what share of relays are dirty" is uncomputable. Some media inflated the theft to $500,000; the paper says under 50 dollars. Benefit "medium" is sized by consequence: key and code thefts range wildly, with no amounts to apply. Having used an unknown relay: revoke and regenerate every key that passed through it, cloud services and code repositories included. Through relays, never let the AI auto-execute — review commands before release. Running a relay carries criminal risk: Section 11, item 19. Beneficiary: you.
