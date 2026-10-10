# 14. Nalozi i bezbednost informacija

Mere: novac i lični podaci. Kad se neko prijavi na vaš nalog, novac ide prvo; koristiće vaš nalog i da prevare vaše kontakte — a vaš identitet efektivno ode s njima.

### 1. Uključite dvofaktorsku potvrdu za imejl, plaćanja i društvene naloge — prvo odobrenje iskačućom u aplikaciji, drugo SMS kodovi
<!-- costs: novac=nema vreme=malo volja=ne korist=velika mera=novac -->
- Trošak: Besplatno. Jedno podešavanje po nalogu, 2–3 minute.
- Prostim jezikom: Dvofaktorska znači drugu potvrdu preko lozinke pri prijavi. Iskok na telefonu koji tapnete blokira preko 90% preuzimanja fišingom. Odgovaranje „gde ste se poslednji put prijavili" i „koji je vaš rezervni imejl" blokira samo oko 10%.
- Korist: Google je analizirao 350,000 stvarnih pokušaja preuzimanja naloga. Potvrda zasnovana na uređaju — iskoci na telefonu koje potvrđujete, ili utaknuti sigurnosni ključevi — blokirala je „preko 94% pokušaja preuzimanja fišingom i 100% automatizovanih" (fišing znači žetvu lozinki s lažnih sajtova; automatizovano znači masovne pokušaje procurlim lozinkama). Potvrda zasnovana na znanju — lokacije poslednjih prijava, rezervni imejlovi — „blokirala je svega 10% preuzimanja fišingom i 73% automatizovanih"
- Nivo dokaza: A
- Izvori: Doerfler P, Thomas K, Marincenko M, et al. (2019). Evaluating Login Challenges as a Defense Against Account Takeover. The World Wide Web Conference (WWW '19). <https://doi.org/10.1145/3308558.3313481>
- Napomena: Ista studija našla je da takve provere katkad zaključaju pravog vlasnika — 52% legitimnih korisnika palo na prvom pokušaju, mada je 97% na kraju ušlo. Uključite prvo na imejlu: većina ostalih naloga oporavlja se kroz imejl. Verifikacioni kodovi vaši su sami — cena čitanja kodova ili skeniranja lica za druge: odeljak 8, stavka 45.

### 2. Lozinka vašeg imejla stoji sama — nikad ponovljena bilo gde
<!-- costs: novac=nema vreme=malo volja=delimično korist=velika mera=novac -->
- Trošak: Besplatno. Menadžer lozinki pamti za vas. Teško je: slomiti naviku jedne lozinke.
- Prostim jezikom: Lozinke ukradene s drugih sajtova pušu pravo na vaš imejl. Jednom kad imejl padne, svaki nalog oporavljiv kroz njega pada isto. Zato se lozinka imejla ne koristi nigde drugde.
- Korist: Reprodukovanje procurlih kredencijala sajt po sajt — credential stuffing — najjeftiniji je napad, i vaš imejl biva isproban. Jedan prolom imejla kaskira u svaki imejlom-oporavljiv nalog. Savet američkog CISA: drugačija jaka lozinka po nalogu, najmanje 16 znakova, u menadžeru lozinki
- Nivo dokaza: C
- Izvori: US CISA. Use Strong Passwords. <https://www.cisa.gov/secure-our-world/use-strong-passwords>
- Napomena: Koristite ugrađen menadžer pregledača ako ništa drugo — daleko bolje od jedne lozinke svuda. Ne čuvajte lozinke u WeChat omiljenim ili aplikacijama beleški.

### 3. Postavite lozinku zaključanog ekrana na telefonu i PIN na SIM
<!-- costs: novac=nema vreme=malo volja=ne korist=velika mera=novac -->
- Trošak: Besplatno. Jedno podešavanje svako.
- Prostim jezikom: SIM je mala kartica unutra — SMS verifikacioni kodovi stižu kroz nju. Izgubite telefon, i ko ga nađe prebaci karticu u svoj telefon, žanje vaše kodove i resetuje nalog za nalogom. PIN na SIM traži kod pri svakom paljenju u novom telefonu — zatvara put.
- Korist: Posle izgubljenog telefona, najbrža ruta nalazača jeste vaš SIM u njihovom telefonu koji skuplja SMS kodove — s kodovima, nalozi se resetuju jedan po jedan. PIN na SIM traži kod pri paljenju u svakom novom uređaju, odsecajući nalazača
- Nivo dokaza: C
- Izvori: Iskustvo autora, nema direktne literature
- Napomena: PIN živi pod „zaključavanje SIM kartice" u podešavanjima; fabrički obično 1234 ili 0000; tri pogrešna unosa traže operaterov PUK — zapišite oba na papir prvo.

### 4. Telefon izgubljen — ovaj redosled: suspendujte SIM, daljinski zaključajte, promenite lozinke, prijavite, zamrznite kartice
<!-- costs: novac=nema vreme=malo volja=ne korist=velika mera=novac -->
- Trošak: Besplatno. Cela sekvenca traje desetak minuta.
- Prostim jezikom: Redosled bije brzinu. Prvo suspendujte SIM — životna linija kodova umire. Zatim daljinski zaključajte telefon, promenite lozinke imejla i plaćanja s računara, prijavite policiji radi potvrde, pa zamrznite bankovne kartice po potrebi. Pozajmite bilo koji telefon da zovete operatera.
- Korist: Redosled bije brzinu. Korak jedan, suspendujte SIM — kodovi prestaju stizati ikome. Korak dva, daljinski zaključajte i obrišite. Korak tri, promenite lozinke imejla i plaćanja s računara. Korak četiri, policijska prijava s potvrdom. Na kraju, zamrznite kartice po potrebi. Američki FCC se slaže: daljinski zaključajte čak i ako mislite da je samo izgubljen; kad je ukraden, prijavite odmah s modelom i IMEI (matični broj telefona) i odmah obavestite operatera
- Nivo dokaza: C
- Izvori: US FCC. Protect Your Smart Device. <https://www.fcc.gov/consumers/guides/protect-your-mobile-device>；步骤顺序是作者经验；补办身份证见第 7 节，冒名贷款见第 8 节关于征信的一条
- Napomena: Sačuvajte sada brojeve tri operatera: China Mobile 10086, Unicom 10010, Telecom 10000. Zapišite u kom gradu je broj registrovan — linija će pitati. Svaki pozajmljeni telefon radi za suspenziju.

### 5. Prevara karticom: prvo suspendujte i zamrznite, drugo prijavite, pa tražite da banka plati — dokazivanje „sami ste to uradili" teret je banke
<!-- costs: novac=nema vreme=malo volja=delimično korist=velika mera=novac -->
- Trošak: Besplatno. Na sumnjivu aktivnost: odmah zamrznite. Čuvajte izveštaj, suspenziju i obaveštenja o transakcijama. S karticom još u ruci, izvedite jednu malu transakciju u blizini da dokažete posed u trenutku. Teško je: suspendovati pre svađe s korisničkom podrškom.
- Prostim jezikom: Ne morate dokazati „to nisam bio ja" — banka mora dokazati da je transakcija vaša ili ovlašćena, ili plaća. Preduslov: suspendovali ste pri otkriću. Oklevali, jedete proširene gubitke.
- Korist: Odredbe Vrhovnog suda dele teret. Vi tvrdite falsifikat kartice ili prevaru na mreži — dajete početne dokaze: važeće pravne dokumente, lokaciju prave kartice i lokaciju transakcije, izvode, obaveštenja, policijske zapise i suspenzije. **Obrnuto, kad izdavalna banka ili platna institucija tvrdi da je korisnik izvršio ili ovlastio transakciju, dokaze daju one.** Gde banka nije blagovremeno proverila posle vaše prijave, ili nije sačuvala slipove i snimke, dokazni promašaj njihov je. Uspostavljeno: nosioci debitnih kartica mogu tražiti ukradenu glavnicu i kamatu plus štetu; nosioci kreditnih mogu tražiti naplaćenu glavnicu prekoračenja, kamatu i penale plus štetu — banci koja traži povraćaj tog prekoračenja sud ne pomaže — i mogu tražiti hitno uklanjanje negativnog zapisa kredita (nacionalno; na snazi od 2021-05-25)
- Nivo dokaza: A
- Izvori: 最高人民法院 (2021). 关于审理银行卡民事纠纷案件若干问题的规定（第四、五、七、十四、十五条）. <https://www.court.gov.cn/fabu/xiangqing/304771.html>
- Napomena: Dve situacije ostavljaju vas odgovornim: sopstvena krivica u čuvanju kartice, lozinke ili kodova („nepravilno čuvanje s krivicom") — srazmerno krivici, zato nikad ne delite lozinke niti prosleđujte kodove (iskok stavke 1 prvo); i propust suspenzije na vreme, jedući širenje. Zato korak jedan uvek suspenzija, nikad rasprava. Platne institucije trećih strana prate ista pravila — konkretna, izričita obećanja „naknadne kompenzacije" u njihovim materijalima vezuju ih. Novac koji ste prevareni da sami prebacite ide drugim putem: odeljak 8, stavka 2.

### 6. Periodično pregledajte prijavljene uređaje i odobrene aplikacije — očistite nekorišćene
<!-- costs: novac=nema vreme=malo volja=delimično korist=srednja mera=novac -->
- Trošak: Besplatno. Minute po pregledu. Teško je: pamtiti bez podsetnika.
- Prostim jezikom: „Prijavljeni uređaji" jesu telefoni i računari koji i dalje mogu koristiti vaš nalog. Preuzimači obično čuče pre delanja. Nepoznat uređaj ili davno mrtva aplikacija i dalje vezana: odjavite svuda, promenite lozinku.
- Korist: Preuzimanja retko deluju odmah — uljez čuči. Lista uređaja beleži koji telefoni i računari trenutno dosežu nalog; lista odobrenih aplikacija beleži koji softver trećih strana ste odobrili. Nepoznati uređaji i mrtve aplikacije trećih najvidljiviji su tragovi
- Nivo dokaza: C
- Izvori: Iskustvo autora, nema direktne literature
- Napomena: WeChat, Alipay, imejl i Apple/Android nalozi svi nose te stavke. Na bilo šta nepoznato: odjavite svuda, pa promenite lozinku.

### 7. Ne tapćite „slažem se sa svime" za aplikaciju: nebitne informacije ne smeju se isticati uslugom
<!-- costs: novac=nema vreme=malo volja=delimično korist=srednja mera=sloboda -->
- Trošak: Besplatno. Teško je: odupreti se „slažem se sa svima".
- Prostim jezikom: Ako informacija nije nužna za uslugu, odbijanje ne sme ići na račun usluge — i prikupljanje je ograničeno na stvarno potrebno. Mape trebaju lokaciju; baterijska lampa ne treba vaše kontakte.
- Korist: Zakon kaže dve stvari: odbijanje ili povlačenje saglasnosti ne sme opravdavati uskraćivanje proizvoda ili usluge, osim kad je obrada nužna za pružanje; i prikupljanje je ograničeno na minimalan obim ostvarivanja svrhe — samo ono što treba
- Nivo dokaza: A
- Izvori: 全国人大常委会 (2021). 个人信息保护法. 中国人大网. <http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html>：第六条「收集个人信息，应当限于实现处理目的的最小范围，不得过度收集个人信息」；第十六条「个人信息处理者不得以个人不同意处理其个人信息或者撤回同意为由，拒绝提供产品或者服务；处理个人信息属于提供产品或者服务所必需的除外」；第十五条「基于个人同意处理个人信息的，个人有权撤回其同意。个人信息处理者应当提供便捷的撤回同意的方式」
- Napomena: Test je nužnost za uslugu — mape i lokacija da, lampe i kontakti ne. Posle instalacije, isključite nebitne dozvole na stranici dozvola aplikacije, dajući „samo jednom" kad stvarno treba.

### 8. Možete pregledati, kopirati, ispraviti i izbrisati svoje lične podatke — odbijanje se može tužiti
<!-- costs: novac=nema vreme=malo volja=delimično korist=srednja mera=sloboda -->
- Trošak: Besplatno. Pritužbe i tužbe dolaze tek na zid — litigacija traje mesece s vašim advokatskim troškovima, pa prvo pritužba. Teško je: gurati iznova kad odugovlače.
- Prostim jezikom: Možete tražiti pregled, kopiranje, ispravku i brisanje svojih podataka. Usluga završena, rok čuvanja istekao, saglasnost povučena — trebali bi sami obrisati. Odbijanje traži navedene razloge; dalje odbijanje, tužite direktno. Otkaz naloga i brisanje podataka dve su stvari — zahtev za brisanje podnesite odvojeno posle otkaza.
- Korist: Nekoliko situacija obavezuje aktivno brisanje: usluga završena, rok istekao, saglasnost povučena, svrha ostvarena. Neobrisano, možete tražiti brisanje; odbijeno, razlozi moraju biti navedeni; možete tužiti direktno
- Nivo dokaza: A
- Izvori: 全国人大常委会 (2021). 个人信息保护法. 中国人大网. <http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html>：第四十五条「个人有权向个人信息处理者查阅、复制其个人信息……个人请求查阅、复制其个人信息的，个人信息处理者应当及时提供」；第四十六条更正、补充权；第四十七条列了五种应当主动删除的情形，含「（一）处理目的已实现、无法实现或者为实现处理目的不再必要」「（二）个人信息处理者停止提供产品或者服务，或者保存期限已届满」「（三）个人撤回同意」，「个人信息处理者未删除的，个人有权请求删除」；第五十条「个人信息处理者应当建立便捷的个人行使权利的申请受理和处理机制。拒绝个人行使权利的请求的，应当说明理由」「个人可以依法向人民法院提起诉讼」
- Napomena: Otkaz i brisanje odvojeni su — posle otkaza, podnesite brisanje odvojeno. Pre zamene ili prodaje telefona: odjavite i odvežite sve, pa fabrički reset. Zakon daje naknadno brisanje; ne može opozvati ono što je već procurilo.

### 9. Skeniranje lica nikad nije obavezno: postoje alternative znači samo-lice je zabranjeno — neslaganje mora vam zaraditi drugi put
<!-- costs: novac=nema vreme=malo volja=delimično korist=srednja mera=novac -->
- Trošak: Besplatno. Kad traže skeniranje, pitajte „ima li druga verifikacija?" Na „nema", zahtevajte jednu. Teško je: pitati naglas.
- Prostim jezikom: Gde druga metoda postiže istu svrhu, verifikacija samo licem zabranjena je. Odbijanje lica mora vam zaraditi kartične, lozinkom ili dokumentovane alternative — bez prinude „onda nema usluge". Sobe hotela, javna kupatila, svlačionice i toaleti ne primaju uređaje prepoznavanja lica ni za koga.
- Korist: Mere bezbednosti prepoznavanja lica kažu: „gde druga, ne-lica-prepoznajuća sredstva postižu istu svrhu ili ekvivalentne poslovne zahteve, prepoznavanje lica ne sme biti jedina metoda verifikacije; kad se pojedinac ne slaže s verifikacijom identiteta licem, obezbediće se druga razumna i pogodna sredstva", i „nijedna organizacija ni pojedinac ne sme zavoditi, prevarom ili prinudom navesti pojedince da prihvate verifikaciju identiteta licem uz razloge poslovanja ili kvaliteta usluge." Obrada podataka lica po saglasnosti traži „posebnu saglasnost, dobrovoljno i izričito datu uz punu svest" — pitano o ovoj jednoj stvari, složeno s ovom jednom stvari. Saglasnost se može povući, s pogodnim povlačenjem. Maloletnici ispod 14 trebaju saglasnost roditelja ili staratelja. Javne instalacije „moraju biti nužne za javnu bezbednost" s upadljivom signalizacijom; sobe hotela, javna kupatila, svlačionice i toaleti — privatni prostori u javnim objektima — ne primaju instalacije, tačka. Podaci lica moraju biti skladišteni na uređaju, nikad preneti internetom, osim zakonskih odredbi ili posebne saglasnosti (nacionalno; na snazi od 2025-06-01)
- Nivo dokaza: A
- Izvori: 国家互联网信息办公室、公安部 (2025). 人脸识别技术应用安全管理办法（第 19 号令，第十条、十二条、十三条，2025 年 6 月 1 日起施行）. <https://www.cac.gov.cn/2025-03/21/c_1744174262156096.htm>
- Napomena: Najčešći susreti: kapije naselja, platforme najma, teretane, hoteli. Na „sistem podržava samo lica", izrecite mere: „gde druga, ne-lica-prepoznajuća sredstva postižu istu svrhu ili ekvivalentne poslovne zahteve, prepoznavanje lica ne sme biti jedina metoda verifikacije" — pa zahtevajte karticu, lozinku ili dokument. Još odbijaju: prijavite lokalnoj sajber upravi. Sektori s posebnim državnim pravilima — deo finansija i vladinih usluga — prate njih. Najdublja razlika lica i lozinki: procurela lica ne mogu se promeniti — čuvajte ih pažljivije od lozinki. Operateri s 100,000-plus zapisa lica moraju prijaviti pokrajinskim-naviše sajber vlastima u roku od 30 radnih dana — samo po sebi pitanje vredno postavljanja. Prava pregled-ispravka-brisanje: stavka 8. Pozamljivanje lica tuđem kreditu sasvim je druga stvar: odeljak 8, stavka 45.

### 10. Nikad ne predajte kod, ključeve ni privatni materijal nepoznatom „AI releju" — posebno uz AI koji automatski izvršava komande
<!-- costs: novac=malo vreme=malo volja=delimično korist=srednja mera=sloboda -->
- Trošak: Zvanične direktne veze obično koštaju više i dopunjuju se manje zgodno. Teško je: releji su jeftini i šire se na više modela s jednog ulaza.
- Prostim jezikom: Relej sedi između vas i prodavca modela, videći i moguće menjajući i vaše upite i odgovore. Studija merila 400-plus releja: 9 ubacivalo zlonameran kod u odgovore, a 17 diralo mamčene oblačne ključeve. S AI-jem koji automatski izvršava komande, jedna izmenjena komanda može preuzeti mašinu.
- Korist: Obaveštenje ministarstva državne bezbednosti iz juna 2026: neki releji zadržavaju korisničke podatke, tajno ih presrećući i preprodajući drugim prodavcima modela za trening; neki kriju zadnja vrata sadržeći malware za krađu ključeva naloga i oblačnih kredencijala, čak programe daljinskog upravljanja. Savet: samo zvanične direktne veze i propisno licencirane platforme; sanitizujte privatni i projektni materijal pre slanja; upravljajte i rotirajte ključeve; na abnormalno naplaćivanje, neobjašnjene zabrane ili anomalije podataka — stanite, rotirajte ključeve, skenirajte na malware, sačuvajte dokaze. Merenje istraživača predvođenih UCSB-om iz 2026: kupivši 28 plaćenih releja s Taobao, Xianyu i ofšor radnji plus 400 besplatnih releja iz javnih zajednica — 1 plaćeni i 8 besplatnih ubacilo zlonameran kod u vraćene pozive alata (pozivi alata komande su koje AI pokreće na vašoj mašini, poput instalacija paketa); 2 tempirala udare, jedan primer gađajući samo potpuno automatizovane sesije; 17 diralo namerno posađene AWS ključeve; 1 ispraznio novčanik istraživača u Ethereumu — slabo finansiran, gubici ispod 50 američkih dolara. Pokazana izmena bila je suptilna: zamena „requests" gotovo identičnim „reqeusts" u instalacionoj komandi, nevidljiva prvim pogledom (nacionalno)
- Nivo dokaza: B
- Izvori: 国家安全部 (2026). 「AI中转站」，风险要防范. <https://www.szzg.gov.cn/2026/xwzx/szkx/202606/t20260608_5331487.htm>（数字中国建设峰会官网转载国家安全部微信公众号）；Liu H, Shou C, Wen H, Chen Y, Fang RJ, Feng Y. (2026). Your Agent Is Mine: Measuring Malicious Intermediary Attacks on the LLM Supply Chain. arXiv:2604.08407. <https://arxiv.org/abs/2604.08407>
- Napomena: Ocena B: jedna studija, preprint (verzija pre objave). Uglavnom besplatni releji — samo 28 plaćenih — pa „koji udeo releja je prljav" nije izračunljiv. Neki mediji naduli krađu na 500,000 dolara; rad kaže ispod 50 dolara. Korist „srednja" veličinom po posledici: krađe ključeva i koda sežu svuda, bez iznosa za primenu. Koristili nepoznati relej: opozovite i regenerišite svaki ključ koji je prošao kroz njega, oblačne usluge i repozitorijume koda uključeno. Kroz releje, nikad ne puštajte AI da izvršava automatski — pregledajte komande pre puštanja. Vođenje releja nosi krivični rizik: odeljak 11, stavka 19. Korisnik: vi.
