# 14. Konten und Informationssicherheit

Kennzahlen: Geld und personenbezogene Information. Loggt sich jemand in dein Konto, geht zuerst Geld; sie nutzen dein Konto auch, deine Kontakte zu betrügen — und deine Identität läuft praktisch mit ihnen fort.

### 1. Zwei-Faktor für E-Mail-, Zahlungs- und Social-Konten einschalten — App-Popup-Freigabe zuerst, SMS-Codes danach
<!-- costs: Geld=0 Zeit=wenig Wille=nein Nutzen=gross Kennzahl=Geld -->
- Kosten: Gratis. Ein Setup pro Konto, 2–3 Minuten.
- Klartext: Zwei-Faktor heißt eine zweite Bestätigung jenseits des Passworts beim Login. Ein Popup auf deinem Handy, das du tippst, blockt über 90 % der Phishing-Übernahmen. „Wo hast du zuletzt eingeloggt“ und „was ist deine Backup-Mail“ zu beantworten blockt nur rund 10 %.
- Nutzen: Google analysierte 350000 echte Kontoübernahme-Versuche. Gerätebasierte Verifizierung — Handy-Popups, die du bestätigst, oder eingesteckte Sicherheitsschlüssel — blockte „über 94 % der phishing-basierten und 100 % der automatisierten Übernahmeversuche“ (Phishing heißt Passwort-Ernte über Fake-Seiten; automatisiert heißt Massenversuche mit geleakten Passwörtern). Wissensbasierte Verifizierung — letzte Login-Orte, Backup-Mails — „blockte so wenig wie 10 % der Phishing-Übernahmen und 73 % der automatisierten“
- Evidenzgrad: A
- Quellen: Doerfler P, Thomas K, Marincenko M, et al. (2019). Evaluating Login Challenges as a Defense Against Account Takeover. The World Wide Web Conference (WWW '19). <https://doi.org/10.1145/3308558.3313481>
- Hinweis: Dieselbe Studie fand, solche Herausforderungen sperren manchmal den echten Eigentümer aus — 52 % der legitimen Nutzer scheiterten am ersten Versuch, 97 % kamen schließlich rein. Erst auf E-Mail aktivieren: Die meisten anderen Konten erholen sich über E-Mail. Bestätigungscodes sind allein deine — der Preis, Codes vorzulesen oder für andere zu scannen: Abschnitt 8, Eintrag 45.

### 2. Dein E-Mail-Passwort steht allein — nirgendwo wiederverwendet
<!-- costs: Geld=0 Zeit=wenig Wille=etwas Nutzen=gross Kennzahl=Geld -->
- Kosten: Gratis. Ein Passwortmanager merkt es dir. Schwer: die Ein-Passwort-Gewohnheit brechen.
- Klartext: Von anderen Seiten gestohlene Passwörter werden direkt gegen deine E-Mail durchprobiert. Fällt die E-Mail, fällt jedes darüber wiederherstellbare Konto. Also: das E-Mail-Passwort nirgendwo sonst nutzen.
- Nutzen: Geleakte Zugangsdaten Seite für Seite abzuspielen — Credential Stuffing — ist der billigste Angriff, und deine E-Mail wird durchprobiert. Ein E-Mail-Einbruch kaskadiert in jedes E-Mail-wiederherstellbare Konto. Der Rat der US-CISA: pro Konto ein anderes starkes Passwort, mindestens 16 Zeichen, im Passwortmanager verwahrt
- Evidenzgrad: C
- Quellen: US CISA. Use Strong Passwords. <https://www.cisa.gov/secure-our-world/use-strong-passwords>
- Hinweis: Nutze den eingebauten Passwortmanager des Browsers, wenn sonst nichts — weit besser als ein Passwort überall. Keine Passwörter in WeChat-Favoriten oder Notiz-Apps lagern.

### 3. Sperrbildschirm-Passwort aufs Handy und eine PIN auf die SIM
<!-- costs: Geld=0 Zeit=wenig Wille=nein Nutzen=gross Kennzahl=Geld -->
- Kosten: Gratis. Je ein Setup.
- Klartext: Die SIM ist die kleine Karte innen — SMS-Bestätigungscodes kommen über sie. Verlierst du das Handy, steckt der Finder die Karte in sein eigenes Gerät, erntet deine Codes und setzt Konto um Konto zurück. Eine SIM-PIN verlangt den Code bei jedem Hochfahren in einem neuen Gerät — und schließt die Straße.
- Nutzen: Nach einem verlorenen Handy ist der schnellste Weg des Finders deine SIM in seinem Gerät, SMS-Codes sammelnd — mit Codes werden Konten eins nach dem anderen zurückgesetzt. Eine SIM-PIN verlangt den Code beim Start in jedem neuen Gerät und schneidet den Finder ab
- Evidenzgrad: C
- Quellen: 作者经验，无直接文献
- Hinweis: Die PIN wohnt unter „SIM-Kartensperre“ in den Einstellungen; Werksstandards sind meist 1234 oder 0000; drei Fehlversuche verlangen die PUK des Anbieters — schreib beide vorher auf Papier.

### 4. Handy verloren — diese Reihenfolge: SIM sperren, fernsperren, Passwörter ändern, Anzeige, Karten einfrieren
<!-- costs: Geld=0 Zeit=wenig Wille=nein Nutzen=gross Kennzahl=Geld -->
- Kosten: Gratis. Die ganze Sequenz kostet ein Dutzend-und-etwas Minuten.
- Klartext: Reihenfolge schlägt Tempo. Zuerst die SIM sperren — die Code-Lebensader stirbt. Als Nächstes das Handy fernsperren, E-Mail- und Zahlungspasswörter vom Computer ändern, zur Polizei für den Beleg, dann Bankkarten nach Bedarf einfrieren. Jedes geliehene Handy reicht zum Anruf beim Anbieter.
- Nutzen: Reihenfolge schlägt Tempo. Schritt eins, SIM sperren — Codes treffen bei niemandem mehr ein. Schritt zwei, fernsperren und -löschen. Schritt drei, E-Mail- und Zahlungspasswörter vom Computer ändern. Schritt vier, Polizeianzeige mit Beleg. Schließlich Karten nach Bedarf einfrieren. Die US-FCC stimmt zu: fernsperren, selbst wenn du es für bloß verloren hältst; bei Diebstahl sofort anzeigen mit Modell und IMEI (der Identitätsnummer des Handys) und den Anbieter sofort benachrichtigen
- Evidenzgrad: C
- Quellen: US FCC. Protect Your Smart Device. <https://www.fcc.gov/consumers/guides/protect-your-mobile-device>；步骤顺序是作者经验；补办身份证见第 7 节，冒名贷款见第 8 节关于征信的一条
- Hinweis: Speichere jetzt die drei Anbieternummern: China Mobile 10086, Unicom 10010, Telecom 10000. Notiere, in welcher Stadt deine Nummer registriert wurde — die Hotline fragt. Jedes geliehene Handy tuts zum Sperren.

### 5. Kartenbetrug: zuerst sperren und einfrieren, dann anzeigen, dann die Bank zahlen lassen — „du hast es selbst getan“ zu beweisen ist der Bank ihre Last
<!-- costs: Geld=0 Zeit=wenig Wille=etwas Nutzen=gross Kennzahl=Geld -->
- Kosten: Gratis. Bei verdächtiger Aktivität: sofort einfrieren. Behalte den Bericht, die Sperrung und die Transaktionsmitteilungen. Karte noch in der Hand: mach eine kleine Transaktion in der Nähe, um den Besitz zum Zeitpunkt zu beweisen. Schwer: sperren, bevor mit dem Kundendienst gestritten wird.
- Klartext: Du musst nicht beweisen, „das war ich nicht“ — die Bank muss beweisen, dass die Transaktion deine oder autorisiert war, oder zahlen. Voraussetzung: du hast bei Entdecken gesperrt. Verzögerst du, isst du die erweiterten Verluste.
- Nutzen: Die Bestimmungen des Obersten Gerichts teilen die Beweislast. Du behauptest Kartenfälschung oder Online-Betrug — du lieferst Erstbeweise: wirksame Rechtsdokumente, Ort der echten Karte und Ort der Transaktion, Abrechnungen, Mitteilungen, Polizei- und Sperraufzeichnungen. **Umgekehrt, wenn die kartenausgebende Bank oder das Zahlungsinstitut behauptet, der Karteninhaber habe die Transaktion getan oder autorisiert, liegt der Beweis bei ihnen.** Wo die Bank nach deiner Mitteilung nicht zeitnah prüfte oder Belege und Aufnahmen nicht bewahrte, ist der Beweisfehler ihrer. Festgestellt: Debitkarteninhaber dürfen abgebuchtes Kapital und Zinsen plus Schadensersatz zurückfordern; Kreditkarteninhaber dürfen belastetes Dispo-Kapital, Zinsen und Strafen plus Schadensersatz zurückfordern — Banken, die diese Dispo-Rückzahlung verlangen, bekommen keine Gerichtsunterstützung — und dürfen umgehende Entfernung des negativen Krediteintrags verlangen (national; wirksam 2021-05-25)
- Evidenzgrad: A
- Quellen: 最高人民法院 (2021). 关于审理银行卡民事纠纷案件若干问题的规定（第四、五、七、十四、十五条）. <https://www.court.gov.cn/fabu/xiangqing/304771.html>
- Hinweis: Zwei Lagen lassen dich haften: eigenes Verschulden beim Bewachen von Karte, Passwort oder Codes („Obhutsfehler mit Verschulden“) — dem Verschulden proportional, also niemals Passwörter teilen oder Codes weiterleiten (Eintrag 1s Popup zuerst); und versäumtes zeitnahes Sperren, das die Ausweitung isst. Also ist Schritt eins immer Sperren, nie Argument. Drittanbieter-Zahlungsinstitute folgen denselben Regeln — konkrete, ausdrückliche „Vorabentschädigung“-Versprechen in ihren Unterlagen binden sie. Selbst überwiesenes, erschwindeltes Geld nimmt einen anderen Weg: Abschnitt 8, Eintrag 2.

### 6. Periodisch angemeldete Geräte und autorisierte Apps durchsehen — Unbenutztes löschen
<!-- costs: Geld=0 Zeit=wenig Wille=etwas Nutzen=mittel Kennzahl=Geld -->
- Kosten: Gratis. Minuten je Durchgang. Schwer: ohne Erinnerungen dranbleiben.
- Klartext: „Angemeldete Geräte“ sind die Handys und Computer, die dein Konto noch nutzen können. Übernehmer lauern meist vor dem Handeln. Ein unbekanntes Gerät oder eine langtote App noch verknüpft: überall abmelden, Passwort ändern.
- Nutzen: Übernahmen handeln selten sofort — der Eindringling lauert. Die Geräteliste verzeichnet, welche Handys und Computer das Konto derzeit erreichen; die autorisierte-Apps-Liste, welche Drittpoftware du erlaubt hast. Unbekannte Geräte und tote Drittanbieter-Apps sind die sichtbarsten Spuren
- Evidenzgrad: C
- Quellen: 作者经验，无直接文献
- Hinweis: WeChat, Alipay, E-Mail und Apple-/Android-Konten tragen alle diese Einträge. Bei irgendetwas Unbekanntem: überall abmelden, dann Passwort ändern.

### 7. Bei einer App nicht „allen zustimmen“ tippen: nicht-notwendige Information darf nicht gegen Dienstleistung verwertet werden
<!-- costs: Geld=0 Zeit=wenig Wille=etwas Nutzen=mittel Kennzahl=Freiheit -->
- Kosten: Gratis. Schwer: „allen zustimmen“ widerstehen.
- Klartext: Ist die Information für den Dienst unnötig, darf die Verweigerung nicht gegen dich verwendet werden — und das Sammeln ist auf das wirklich Nötige begrenzt. Karten brauchen Ort; eine Taschenlampe braucht deine Kontakte nicht.
- Nutzen: Das Gesetz besagt zwei Dinge: Verweigerung oder Widerruf der Zustimmung darf die Versagung von Produkt oder Dienst nicht begründen, außer wo die Verarbeitung zu deren Bereitstellung nötig ist; und das Sammeln ist begrenzt auf den Mindestumfang, der den Zweck umsetzt — nur das Nötige
- Evidenzgrad: A
- Quellen: 全国人大常委会 (2021). 个人信息保护法. 中国人大网. <http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html>：第六条「收集个人信息，应当限于实现处理目的的最小范围，不得过度收集个人信息」；第十六条「个人信息处理者不得以个人不同意处理其个人信息或者撤回同意为由，拒绝提供产品或者服务；处理个人信息属于提供产品或者服务所必需的除外」；第十五条「基于个人同意处理个人信息的，个人有权撤回其同意。个人信息处理者应当提供便捷的撤回同意的方式」
- Hinweis: Der Test ist Dienstnotwendigkeit — Karten und Ort ja, Taschenlampen und Kontakte nein. Nach der Installation unnötige Berechtigungen auf der App-Berechtigungsseite ausschalten und im echten Bedarf „nur diesmal“ gewähren.

### 8. Du darfst deine personenbezogene Information einsehen, kopieren, berichtigen und löschen — Verweigerung ist verklagbar
<!-- costs: Geld=0 Zeit=wenig Wille=etwas Nutzen=mittel Kennzahl=Freiheit -->
- Kosten: Gratis. Beschwerden und Klagen kommen erst aufs Mauern — Prozesse laufen Monate mit eigenen Anwaltskosten, also erst beschweren. Schwer: wiederholt nachschieben, wenn sie blocken.
- Klartext: Du darfst Einsehen, Kopieren, Berichtigen und Löschen deiner Information verlangen. Dienst beendet, Aufbewahrung abgelaufen, Zustimmung widerrufen — sie sollen von selbst löschen. Verweigerung verlangt benannte Gründe; fortgesetzte Verweigerung: direkt klagen. Kontolöschung und Informationslöschung sind zwei Dinge — nach der Löschung separat die Dateien löschen beantragen.
- Nutzen: Mehrere Lagen verpflichten aktives Löschen: Dienst beendet, Aufbewahrung abgelaufen, Zustimmung widerrufen, Zweck erreicht. Ungelöscht darfst du Löschung verlangen; verweigert, müssen Gründe benannt werden; du darfst direkt klagen
- Evidenzgrad: A
- Quellen: 全国人大常委会 (2021). 个人信息保护法. 中国人大网. <http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html>：第四十五条「个人有权向个人信息处理者查阅、复制其个人信息……个人请求查阅、复制其个人信息的，个人信息处理者应当及时提供」；第四十六条更正、补充权；第四十七条列了五种应当主动删除的情形，含「（一）处理目的已实现、无法实现或者为实现处理目的不再必要」「（二）个人信息处理者停止提供产品或者服务，或者保存期限已届满」「（三）个人撤回同意」，「个人信息处理者未删除的，个人有权请求删除」；第五十条「个人信息处理者应当建立便捷的个人行使权利的申请受理和处理机制。拒绝个人行使权利的请求的，应当说明理由」「个人可以依法向人民法院提起诉讼」
- Hinweis: Löschung und Kündigung sind getrennt — nach der Kündigung separat Dateilöschung beantragen. Vor Handywechsel oder -verkauf: überall abmelden und entkoppeln, dann auf Werkszustand zurücksetzen. Das Gesetz gewährt nachträgliche Löschung; es kann nicht zurückrufen, was schon leakte.

### 9. Gesichtsscan ist nie Pflicht: Alternativen existieren heißt Nur-Gesicht verboten — Widerspruch muss dir einen anderen Weg einbringen
<!-- costs: Geld=0 Zeit=wenig Wille=etwas Nutzen=mittel Kennzahl=Geld -->
- Kosten: Gratis. Beim Scan-Wunsch fragen: „gibt es eine andere Verifizierung?“ Bei „nein“: eine verlangen. Schwer: laut fragen.
- Klartext: Wo eine andere Methode denselben Zweck erreicht, ist Nur-Gesichts-Verifizierung verboten. Die Verweigerung des Gesichts muss dir Karten-, Passwort- oder Ausweis-Alternativen einbringen — kein „dann kein Service“-Zwang. Hotelzimmer, öffentliche Bäder, Umkleiden und Toiletten dulden für niemanden Gesichtserkennungsanlagen.
- Nutzen: Die Gesichtserkennungs-Sicherheitsmaßnahmen schreiben vor: „wo andere nicht-gesichtserkennende Mittel denselben Zweck oder gleichwertige Geschäftsanforderungen erreichen, darf Gesichtserkennung nicht die alleinige Verifizierungsmethode sein; widerspricht eine Einzelperson der Gesichtsidentitätsverifizierung, sind andere vernünftige und bequeme Mittel bereitzustellen“, und „keine Organisation und keine Einzelperson darf Einzelpersonen durch Irreführung, Täuschung oder Zwang zur Annahme der Gesichtsidentitätsverifizierung bewegen mit dem Hinweis auf Geschäftsabwicklung oder Dienstqualität.“ Gesichtdaten auf Zustimmung zu verarbeiten verlangt „separate Zustimmung, freiwillig und ausdrücklich in voller Kenntnis gegeben“ — über dieses Eine gefragt, diesem Einen zugestimmt. Zustimmung ist widerrufbar, mit bequemem Widerruf. Minderjährige unter 14 brauchen Eltern- oder Vormundszustimmung. Öffentliche Installationen „müssen für die öffentliche Sicherheit notwendig sein“ mit auffälliger Beschilderung; Hotelzimmer, öffentliche Bäder, Umkleiden und Toiletten — Privaträume in öffentlichen Räumen — dulden keinerlei Installationen, Punkt. Gesichtdaten sind auf dem Gerät zu speichern, nie über das Internet zu übertragen, außer gesetzliche Regelungen oder separate Zustimmung (national; wirksam 2025-06-01)
- Evidenzgrad: A
- Quellen: 国家互联网信息办公室、公安部 (2025). 人脸识别技术应用安全管理办法（第 19 号令，第十条、十二条、十三条，2025 年 6 月 1 日起施行）. <https://www.cac.gov.cn/2025-03/21/c_1744174262156096.htm>
- Hinweis: Die häufigsten Begegnungen: Wohnanlage-Tore, Mietplattformen, Fitnessstudios, Hotels. Bei „das System unterstützt nur Gesichter“ sprich die Maßnahmen: „wo andere nicht-gesichtserkennende Mittel denselben Zweck oder gleichwertige Geschäftsanforderungen erreichen, darf Gesichtserkennung nicht die alleinige Verifizierungsmethode sein“ — dann Karte, Passwort oder Ausweis verlangen. Weiter verweigert: bei der örtlichen Netzverwaltung melden. Sektoren mit eigenen staatlichen Regeln — manche Finanz- und Regierungsdienste — folgen jenen. Der tiefste Unterschied zwischen Gesichtern und Passwörtern: geleakte Gesichter lassen sich nicht wechseln — behandle sie vorsichtiger als Passwörter. Betreiber mit über 100000 Gesichtsdatensätzen müssen binnen 30 Arbeitstagen bei Provinz-plus-Netzbehörden registrieren — selbst eine Frage, die sich zu stellen lohnt. Einsehen-berichtigen-löschen-Rechte: Eintrag 8. Dein Gesicht für fremde Kredite herzugeben ist ein ganz anderes Thema: Abschnitt 8, Eintrag 45.

### 10. Nie Code, Schlüssel oder privates Material einem unbekannten „KI-Relais“ übergeben — besonders bei KI-automer Befehlsausführung
<!-- costs: Geld=wenig Zeit=wenig Wille=etwas Nutzen=mittel Kennzahl=Freiheit -->
- Kosten: Offizielle Direktverbindungen kosten meist mehr und laden unbequemer auf. Schwer: Relais sind billig und fächern von einem Eingang zu mehreren Modellen.
- Klartext: Das Relais sitzt zwischen dir und dem Modellanbieter und sieht und verändert deine Prompts und die Antworten. Eine Studie maß über 400 Relais: 9 injizierten Schadcode in Antworten, und 17 fassen honigtopf-Cloud-Schlüssel an. Mit KI-automer Befehlsausführung kann ein veränderter Befehl die Maschine übernehmen.
- Nutzen: Die Mitteilung des Staatssicherheitsministeriums Juni 2026: Manche Relais behalten Nutzerdaten, fangen sie heimlich ab und verkaufen sie an andere Modellanbieter zum Training weiter; manche verstecken Hintertüren, Malware pflanzend, um Kontoschlüssel und Cloud-Zugangsdaten zu stehlen, gar Fernsteuerprogramme. Der Rat: nur offizielle Direktverbindungen und ordnungsgemäß lizenzierte Plattformen; privates und Projektmaterial vor der Einreichung säubern; Schlüssel verwalten und rotieren; bei abnormaler Abrechnung, unerklärten Sperren oder Datenanomalien — stoppen, Schlüssel rotieren, auf Malware scannen, Beweise sichern. Die Messung UCSB-geführter Forscher 2026: 28 bezahlte Relais von Taobao, Xianyu und Offshore-Läden plus 400 Gratis-Relais aus öffentlichen Communities gekauft — 1 bezahltes und 8 Gratis injizierten Schadcode in zurückgegebene Werkzeugaufrufe (Werkzeugaufrufe sind Befehle, die die KI auf deiner Maschine ausführt, etwa Paketinstallationen); 2 timten ihre Schläge, ein Beispiel zielte nur auf vollautomatische Sitzungen; 17 fassen absichtlich gepflanzte AWS-Schlüssel an; 1 leerte die Ethereum-Wallet eines Forschers — gering finanziert, Verluste unter 50 US-Dollar. Die demonstrierte Veränderung war subtil: „requests“ gegen das fast identische „reqeusts“ in einem Installationsbefehl zu tauschen, auf den ersten Blick unsichtbar (national)
- Evidenzgrad: B
- Quellen: 国家安全部 (2026). 「AI中转站」，风险要防范. <https://www.szzg.gov.cn/2026/xwzx/szkx/202606/t20260608_5331487.htm>（数字中国建设峰会官网转载国家安全部微信公众号）；Liu H, Shou C, Wen H, Chen Y, Fang RJ, Feng Y. (2026). Your Agent Is Mine: Measuring Malicious Intermediary Attacks on the LLM Supply Chain. arXiv:2604.08407. <https://arxiv.org/abs/2604.08407>
- Hinweis: Stufe B: eine Studie, Preprint (die Vor-Publikations-Version). Überwiegend Gratis-Relais — nur 28 bezahlte — also ist „welcher Anteil der Relais dreckig ist“ nicht berechenbar. Manche Medien blähten den Diebstahl auf 500000 $; die Arbeit sagt unter 50 Dollar. Nutzen „mittel“ ist nach Folgen bemessen: Schlüssel- und Code-Diebstähle streuen weit, ohne anwendbare Beträge. Ein unbekanntes Relais genutzt: jeden Schlüssel, der durchlief, widerrufen und neu erzeugen, Cloud-Dienste und Code-Repos eingeschlossen. Über Relais nie die KI automatisch ausführen lassen — Befehle vor der Freigabe prüfen. Ein Relais zu betreiben trägt Strafrisiko: Abschnitt 11, Eintrag 19. Nutznießer: du.
