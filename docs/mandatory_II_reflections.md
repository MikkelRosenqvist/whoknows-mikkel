
# Mandatory II – DevOps Reflections

**Project:** WhoKnows

**Work type:** Individual

## 1. Version Control & Branching

Jeg valgte GitHub Flow, fordi jeg synes, det er en super smart og samtidig simpel måde at arbejde på.

I mit tilfælde arbejdede jeg alene, så i princippet kunne jeg godt bare have arbejdet direkte på main i stedet for at oprette separate branches til nye implementeringer. Men hvis jeg havde siddet i en gruppe, som jeg med stor sandsynlighed også kommer til, når jeg skal ud og arbejde, synes jeg, GitHub Flow giver rigtig god mening.

Det gør det muligt at arbejde på forskellige funktioner isoleret uden at påvirke main, før ændringerne er blevet testet og gennemgået.

Et konkret eksempel var min feature/request-monitoring-branch, hvor jeg implementerede monitoring og forbedrede søgefunktionen. Før jeg mergede ændringerne til main, blev de automatisk kontrolleret med GitHub Actions og SonarQube.

Jeg har ikke oplevet mange ulemper ved GitHub Flow endnu. Jeg har bevidst forsøgt at holde ændringerne på hver branch relativt små for at undgå unødvendig kompleksitet og merge-konflikter.

En ulempe er selvfølgelig, at det tager lidt ekstra tid at oprette branches og Pull Requests. Da jeg arbejdede alene, havde jeg heller ikke mulighed for at få en rigtig code review fra en anden udvikler. De automatiske kontroller kan finde mange problemer, men de kan ikke erstatte en menneskelig gennemgang.

Jeg valgte også GitHub Flow frem for eksempelvis Git Flow, fordi jeg synes, Git Flow ville være unødvendigt kompliceret til et projekt af denne størrelse, hvor jeg arbejder alene. Ekstra branches som develop og release ville ikke give mig nogen særlig fordel på nuværende tidspunkt.

## 2. How Are You DevOps?

Et godt eksempel på, hvor jeg har arbejdet efter DevOps-principper i WhoKnows, var mit arbejde med monitoring.

Et centralt princip i DevOps er den løbende proces: Develop → Test → Deploy → Monitor → Improve.

Da jeg implementerede monitoring i WhoKnows, opdagede jeg, at søgefunktionen returnerede HTTP-statuskode 200, selvom der ikke kom nogen søgeresultater frem.

En statuskode på 200 betyder normalt, at serveren har behandlet requesten korrekt, men det betyder ikke nødvendigvis, at brugeren har fået et brugbart resultat.

Jeg undersøgte derfor problemet nærmere og fandt ud af, at databasen faktisk indeholdt 0 indekserede sider.

På baggrund af den observation forbedrede jeg applikationen, så brugeren nu får en besked om, at der endnu ikke er indekseret nogen sider. Samtidig forbedrede jeg min logging, så jeg fremover kan se, hvor mange søgeresultater der bliver returneret, og om søgeindekset er tomt.

Det synes jeg er et godt eksempel på DevOps, fordi jeg ikke bare udviklede en funktion og antog, at alt virkede. Jeg observerede, hvordan systemet opførte sig, fandt en begrænsning og brugte den viden til at forbedre det.

Jeg har også arbejdet med automatiserede tests, GitHub Actions og SonarQube, som hjælper mig med at opdage fejl og kontrollere kvaliteten af min kode, inden jeg merger ændringer til main.

Jeg har dog endnu ikke implementeret en egentlig deployment til et produktionsmiljø. Derfor har jeg ikke gennemført hele DevOps-processen i praksis. Jeg mangler også blandt andet automatiske alerts og erfaring med at samarbejde om udvikling og drift i et team.

## 3. Software Quality

I arbejdet med Software Quality brugte jeg blandt andet SonarQube, Ruff og Radon til at undersøge kvaliteten af min kode i WhoKnows.

Jeg synes generelt, at SonarQube kom med nogle relevante fund. Især manglen på CSRF-beskyttelse synes jeg var vigtig at få rettet, da det kunne gøre det muligt for andre hjemmesider at forsøge at udføre uønskede handlinger gennem en brugers browser.

Jeg implementerede derfor CSRF-beskyttelse med Flask-WTF og tilføjede automatiske tests, som kontrollerede, at requests uden et gyldigt CSRF-token blev afvist.

En anden forbedring, som jeg synes var mindst lige så interessant, var en fejl i databaseinitialiseringen. Her opdagede jeg, at programmet kunne slette alle eksisterende brugere, hvis databasen blev initialiseret igen. Jeg skrev derfor en test, som først fejlede, og derefter rettede jeg problemet, så testen bestod.

Det interessante ved den fejl var, at SonarQube ikke havde opdaget den. Det viste mig, at selvom automatiske analyseværktøjer er rigtig gode, kan man ikke bare stole blindt på dem. Man skal stadig selv forstå sin kode og teste, hvordan den fungerer.

Jeg valgte også at rette de resterende problemer med HTML-formularernes tilgængelighed og opdatere de biblioteker, som SonarQube havde fundet sikkerhedsrisici i. Til sidst havde projektet A i Security, Reliability og Maintainability samt 0 rapporterede dependency-risici.

Jeg valgte ikke at prioritere yderligere forbedringer på nuværende tidspunkt, blandt andet at få sat måling af test coverage op. Selvom mine automatiske tests består, kan jeg derfor endnu ikke dokumentere, hvor stor en del af koden de dækker. Det er noget, jeg gerne vil arbejde videre med frem mod eksamen.

## 4. Monitoring Realization

Da jeg begyndte at teste søgefunktionen i WhoKnows, lagde jeg mærke til, at der ikke kom nogen søgeresultater frem, når jeg søgte på eksempelvis Python eller football.

Jeg gik derfor tilbage for at undersøge mine logs og se, om der var en fejl i applikationen. Her opdagede jeg dog, at serveren faktisk returnerede HTTP-statuskode 200, hvilket undrede mig lidt, da søgningen jo ikke viste nogen resultater.

Det fik mig til at indse, at selvom en request bliver behandlet korrekt af serveren, betyder det ikke nødvendigvis, at brugeren får det forventede resultat.

Jeg undersøgte derfor problemet nærmere ved at kontrollere API'ets respons og derefter databasen. Her fandt jeg ud af, at der faktisk var 0 indekserede sider i databasen. Søgefunktionen havde altså ikke nogen data at søge i.

På baggrund af den observation valgte jeg at forbedre WhoKnows på to måder.

For det første tilføjede jeg yderligere logging, så jeg nu kan se, hvor mange søgeresultater en søgning returnerer, og om søgeindekset er tomt.

For det andet forbedrede jeg brugeroplevelsen, så der nu kommer en besked om, at der endnu ikke er indekseret nogen sider, i stedet for bare at vise en tom resultatliste.

Jeg verificerede efterfølgende forbedringen ved at teste søgefunktionen i browseren, undersøge de nye logs og køre mine automatiske tests, hvor alle 9 bestod.

Jeg synes, det er et rigtig godt eksempel på, hvorfor monitoring er vigtigt i DevOps. Det handler ikke kun om at kontrollere, om en applikation kører, men også om at forstå, hvordan den faktisk fungerer, og bruge den information til at forbedre den.

Jeg har ikke løst problemet med de manglende sider i databasen endnu, men jeg har gjort det lettere både for mig selv at opdage problemet og for brugeren at forstå, hvorfor søgningen ikke giver noget resultat.

## Documentation

- [WhoKnows Repository](https://github.com/MikkelRosenqvist/whoknows-mikkel)
- [CI Implementation – PR #1](https://github.com/MikkelRosenqvist/whoknows-mikkel/pull/1)
- [Security and Software Quality – PR #2](https://github.com/MikkelRosenqvist/whoknows-mikkel/pull/2)
- [Monitoring Realization – PR #6](https://github.com/MikkelRosenqvist/whoknows-mikkel/pull/6)
