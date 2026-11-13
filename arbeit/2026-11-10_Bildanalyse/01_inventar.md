# Durchgang 1 – Inventar der MoreApp-Bilder

Stand 10.11.2026, Bildanalyse-Chat. Hier werden noch keine Fragen abgeschrieben, sondern nur die Bilder geordnet.
Kennzeichnung: **belegt** (steht so auf dem Bild), **geschlussfolgert** (abgeleitet, mit Begründung), **UNSICHER** (Frage an Josias).

## 1. Welche Bilder es gibt

| Quelle | Ort | Dateien | ausgewertet | Bemerkung |
|---|---|---|---|---|
| ZIP „RG Montag + Dienstag“ (10.11.) | `C:\rundgang_work\moreapp_bilder\montag_dienstag\` (nicht im Repo) | 84 | 84 | Montag und Dienstag liegen in einem Ordner. Die Grenze liegt zwischen `…_124814` und `…_125017` (s. 2.2). |
| ZIP „RG Mittwoch“ (10.11.) | `C:\rundgang_work\moreapp_bilder\mittwoch\` (nicht im Repo) | 66 | 33 | Jede Datei gibt es zweimal, einmal mit „(1)“ im Namen. Die Paare sind **byte-gleich** (per Vergleich geprüft). Ausgewertet sind nur die 33 Dateien ohne „(1)“. |
| Repo `quellen/2026-11-03_MoreApp_Bilder/infrastruktur/` (02.11.) | im Repo | 16 | 16 | Das sind die alten Bilder 01–16. |
| PDFs 26.10./28.10. | `quellen/…/pdf/` + Text in `arbeit/2026-11-03_MoreApp_Vergleich/` | 4 | – | werden in Durchgang 5 zum Abgleich genutzt |

**Zusammen 133 verschiedene Bilder.** Alle sind lesbar, nur an den Rändern ist manches abgeschnitten.
Je Bild gibt es eine wörtliche Abschrift unter `C:\rundgang_work\bildtexte\` (außerhalb des Repos, ohne Codes und Namen). Die Durchgänge 2–5 bauen darauf auf.

Dateinamen-Kürzel in dieser Datei:
- `MD 124141` = `Screenshot_20261110_124141.jpg` aus Montag+Dienstag
- `MI 130117` = `Screenshot_20261110_130117.jpg` aus Mittwoch
- `REPO 01` = `01_infrastrukturraum_heizung_kompressor3.jpg` usw.

## 2. Wichtigste Erkenntnis: Es ist **ein** Formular, das sich nach dem Wochentag richtet

### 2.1 Ein Formular „Objektrundgang TGI MMS“ (belegt)
- Alle Bilder vom 10.11. und vom 02.11. stammen aus **einem** MoreApp-Formular mit dem Namen **„Objektrundgang TGI MMS“**. Belege: Titel in `MD 124141` und `MI 130432`, dazu die Unterformulare mit den Knöpfen „‹ Zurück | Optionen“.
- Im Formular steht wörtlich (`MD 124141`, `MI 130432`): „Dies ist ein dynamisches Formular. Die Inhalte des Formulars ändern sich anhand getätigter Eingaben (z.B. Wochentag). Somit werden nicht immer alle Felder angezeigt - Positionen die nur an bestimmten Wochentagen fällig sind, werden an den anderen Wochentagen automatisch ausgeblendet.“
- Im Kopf stehen folgende Felder (belegt `MD 124141`, `MI 130432`):
  - „Datum:“*
  - „Kalenderwoche:“*
  - „Wochentag:“*
  - „Ausführender Haustechniker:“* (Auswahl)
  - Dazu zwei Links „Objekthandout Haustechnik“ und „Objekthandout Brandschutz“.
- Danach folgt eine Liste von **Unterformularen**: Jedes hat einen Knopf „+ Kontrollieren“ und einen eigenen „Speichern“-Knopf. Darin stehen die Fragen.
- Am Ende kommen „Bemerkungen:“ (freiwillig), „Unterschrift des ausführenden Haustechnikers:“* und „Formular senden“ (belegt `MD 124814`, `MD 125340`, `MI 130442`).
- Das Handy zeigt auf allen Bildern vom 10.11. „Di., 10. Nov.“. Josias hat also an einem Tag den Wochentag im Formular umgestellt (Montag / Dienstag / Mittwoch) und jeweils fotografiert (geschlussfolgert).
- Auch die Repo-Bilder vom 02.11. (Handy: „Mo., 2. Nov.“) zeigen dieselben Unterformulare „Infrastrukturraum (IS):“ und „Produktionshalle:“ (belegt).

### 2.2 Die Tage
| Tag | Bilder | Wochentag im Formular | Beleg |
|---|---|---|---|
| **Montag** | `MD 124141` … `MD 124814` (54 Bilder) | „Montag“ | belegt `MD 124141`. Das Ende mit „Formular senden“ ist `MD 124814`. |
| **Dienstag** | `MD 125017` … `MD 125340` (30 Bilder) | nicht fotografiert | **geschlussfolgert**: Josias sagt, der Dienstag fängt wieder mit Brandmeldezentrale/Batterieraum an. Zwischen 12:48:14 und 12:50:17 ist eine Pause von 2 Minuten, und davor endet das Formular mit „Formular senden“. Der Kopf mit „Wochentag: Dienstag“ ist auf keinem Bild zu sehen. |
| **Mittwoch** | `MI 130117` … `MI 130442` (33 Bilder) | „Mittwoch“ | belegt `MI 130432` |
| 02.11. (alt) | `REPO 01` … `REPO 16` | nicht sichtbar | Handy-Statusleiste „Mo., 2. Nov.“, 17:17–17:21 Uhr |

Bei allen Tagen ist die Kalenderwoche fest mit **38** vorbelegt (belegt `MD 124141`, `MI 130432`), obwohl der 10.11.2026 in **KW 46** liegt. Das passt zum bekannten KW-Fehler im PDF: Das Feld ist ein fester Vorgabewert, keine Rechnung (geschlussfolgert). KW deshalb **nicht** übernehmen.

### 2.3 Unterformulare je Tag (Laufweg-Reihenfolge)
✔ = Unterformular fotografiert, ◻ = in der Liste des Hauptformulars sichtbar, aber Inhalt nicht fotografiert, – = an diesem Tag nicht vorhanden bzw. nicht gesehen.

| Unterformular (wörtlich) | Mo | Di | Mi | 02.11. | in welchem PDF? |
|---|---|---|---|---|---|
| „Grünflächen, Parkplätze (vor Bürogebäude):“ | ✔ | – | – | – | Haustechnik (belegt, PDF-Überschrift) |
| „Eingangsbereich/ Treppenhaus:“ | ✔ | – | – | – | Haustechnik (belegt) |
| „Brandmeldezentrale (BMZ):“ | ✔ | ✔ | ✔ | – | **in keinem PDF** |
| „Batterieraum:“ | ✔ | ✔ | ✔ | – | Infrastruktur (belegt) |
| „Infrastrukturraum:“ | ✔ | – | – | – | Haustechnik (belegt) |
| „Infrastrukturraum (IS):“ | ✔ | ✔ | ✔ | ✔ | Infrastruktur (belegt) |
| „Infrastrukturraum/ Produktionshalle (BS):“ | ✔ | ✔ | ✔ | – | **in keinem PDF** |
| „Gefahrstoffschränke:“ | ? | ? | ◻ | – | Gefahrstoffschränke (PDF 28.10. = Mittwoch) |
| „Produktionshalle:“ | ✔ | ✔ | ✔ | ✔ | **in keinem PDF** (= die alten „Herkunft unklar“-Bilder 10–16) |
| „Produktionshalle (IS):“ | ✔ | ✔ | ✔ | – | Infrastruktur (belegt) |
| „Büro EG:“ | ✔ | – | – | – | Haustechnik (belegt) |
| „Büro 1. OG:“ | ✔ | – | – | – | Haustechnik (belegt) |
| „Büro 1. OG (IS):“ | ✔ | ✔ | ✔ | – | Infrastruktur (belegt) |
| „Sozialräume:“ | ✔ | – | – | – | Haustechnik (geschlussfolgert: PDF hat die Abschnitte „Allgemein / Herren WC / Damen WC“) |
| „Allgemein:“ | ✔ | – | – | – | Haustechnik (geschlussfolgert, Trinkwasser-Spülen) |
| „Sammelstation für Altöl und Gefahrstoffe:“ | ✔ | – | – | – | Haustechnik (belegt, PDF-Überschrift) |
| „Legionellen Prävention:“ | – | – | ✔ | – | Legionellen (PDF 28.10. = Mittwoch) |
| „Brandschutz:“ | ✔ | ✔ | ✔ | – | **in keinem PDF** |

Hinweise zur Tabelle:
- **Mittwoch** ist vollständig belegt. Das Hauptformular ist ganz fotografiert (`MI 130432`, `130437`, `130442`) und zeigt in dieser Reihenfolge: BMZ, Batterieraum, Infrastrukturraum (IS), Infrastrukturraum/ Produktionshalle (BS), **Gefahrstoffschränke**, Produktionshalle, Produktionshalle (IS), Büro 1. OG (IS), Legionellen Prävention, Brandschutz.
- **Montag**: Vom Hauptformular sind nur der Anfang (`MD 124141`, bis „Grünflächen …“) und das Ende (`MD 124814`, ab „Allgemein:“) fotografiert. Die Reihenfolge dazwischen ist aus der Reihenfolge der Screenshots **geschlussfolgert**. Ob es montags auch „Gefahrstoffschränke:“ gibt, ist nicht zu sehen (UNSICHER).
- **Dienstag**: Vom Hauptformular ist nur das Ende fotografiert (`MD 125340`: Produktionshalle (IS), Büro 1. OG (IS), Brandschutz). Das Feld darüber ist abgeschnitten. Ob es dienstags auch „Gefahrstoffschränke:“ gibt, ist nicht zu sehen (UNSICHER).
- **Kürzel im Namen**:
  - „(IS)“ = genau die Unterformulare im PDF „Infrastrukturrundgang“ (dazu kommt der Batterieraum).
  - Ohne Kürzel = PDF „Haustechnikrundgang“.
  - „(BS)“ und „Brandschutz:“ stehen in keinem PDF. Vermutlich gibt es ein fünftes Protokoll „Brandschutz“, das nicht vorliegt (geschlussfolgert, wegen des Links „Objekthandout Brandschutz“) – UNSICHER.
- **Unterschied innerhalb eines Unterformulars je Tag (belegt):** In „Produktionshalle (IS):“ gibt es „Füllung Stickstoffflasche:“ (Abschnitt „Analysebüro“) und „Zählerstand Gaszähler S1:“ … „S8:“ (Abschnitt „Allgemein“ nach „Wareneingangsbüro“) **nur am Montag** (`MD 124529`, `MD 124535`, `MD 124543`, `MD 124550`). Am Dienstag (`MD 125232`/`125237`) und Mittwoch (`MI 130332`/`130336`) fehlen diese 9 Felder. (Korrigiert am 13.11. in Durchgang 2.) Innerhalb eines Unterformulars werden also einzelne Fragen je Tag aus- oder eingeblendet. Das wird in Durchgang 2/3 für jedes Unterformular genau verglichen.

### 2.4 Was das für „Herkunft unklar“ heißt
Die alten Repo-Bilder 10–16 („Produktionshalle“), die zu keinem PDF passten, gehören zum Unterformular **„Produktionshalle:“** (ohne „(IS)“) desselben Formulars. Das ist belegt, denn es ist an allen drei Tagen vorhanden. In keinem der vier PDFs steht es. Offen ist nur noch, **zu welchem unserer Rundgänge** es gehören soll (Frage F1).

## 3. Inventar je Bild

Spalten:
- **Tag**: Mo / Di / Mi / 02.11.
- **PDF-Rundgang**: HT = Haustechnik, IS = Infrastruktur, LEG = Legionellen, GEF = Gefahrstoffschränke, **ohne** = in keinem PDF. Die Zuordnung ist geschlussfolgert über den Unterformular-Namen, s. 2.3.
- **Bildschirm**: HF = Hauptformular, UF = Unterformular.
- **erste / letzte sichtbare Frage**: wörtlich, lange Texte mit … gekürzt. Graue Balken (Zwischenüberschriften) stehen in [eckigen Klammern].
- **Überlappung / Duplikat**: „↔“ = überlappt beim Scrollen mit dem Nachbarbild. „gleich wie“ = dieselbe Stelle an einem anderen Tag.
- **Qualität**: Alle Bilder sind lesbar. Abgeschnittene Ränder stehen in der Spalte „Bemerkung“.

### 3.1 Montag (`montag_dienstag`, 12:41–12:48)

| # | Datei | PDF | Bildschirm | erste sichtbare Frage | letzte sichtbare Frage | Überlappung / Duplikat | Bemerkung |
|---|---|---|---|---|---|---|---|
| 1 | MD 124141 | – | HF Kopf | „Datum:“ | „Grünflächen, Parkplätze (vor Bürogebäude):“ (+ Kontrollieren) | gleich wie MI 130432 (Kopf) | Datum 10.11.2026, KW 38, Wochentag Montag, Haustechniker leer |
| 2 | MD 124149 | HT | UF „Grünflächen, Parkplätze (vor Bürogebäude):“ | „Kontrolle Ordnung und Sauberkeit:“ | „Reinigung Straßeneinläufe:“ | ↔ 124203 | unten abgeschnitten |
| 3 | MD 124203 | HT | UF Grünflächen … | „Sichtprüfung Feuerwehrtresor:“ | „Mangelbeschreibung:“ | ↔ 124149 | Ende des UF |
| 4 | MD 124214 | HT | UF „Eingangsbereich/ Treppenhaus:“ | „Kontrolle Ordnung und Sauberkeit:“ | „Sichtprüfung Inventar, Büromöbel, etc. …“ | ↔ 124219 | |
| 5 | MD 124219 | HT | UF Eingangsbereich/ Treppenhaus | „Sichtprüfung Türen, Fenster …“ | „Mangelbeschreibung:“ | ↔ 124214 | oben ein Knopfpaar abgeschnitten |
| 6 | MD 124226 | ohne | UF „Brandmeldezentrale (BMZ):“ | „Sichtprüfung ob frei zugänglich, ÜE eingeschaltet:“ | „Mangelbeschreibung:“ | gleich wie MD 125017, MI 130117 | UF vollständig auf einem Bild |
| 7 | MD 124232 | IS | UF „Batterieraum:“ | „Kontrolle ob Störungsfrei:“ | „Mangelbeschreibung:“ | gleich wie MD 125026, MI 130123 | UF vollständig |
| 8 | MD 124239 | HT | UF „Infrastrukturraum:“ | „Kontrolle Ordnung und Sauberkeit:“ | „Sichtprüfung Inventar, Büromöbel, etc. …“ | ↔ 124246 | gleiche Fragen wie Eingangsbereich (wird in D3 geprüft) |
| 9 | MD 124246 | HT | UF Infrastrukturraum | „Sichtprüfung Türen, Fenster …“ | „Mangelbeschreibung:“ | ↔ 124239 | |
| 10 | MD 124255 | IS | UF „Infrastrukturraum (IS):“ | „Sichtprüfung Heizungsanlage:“ | „Temperatur:“ [Kompressor 3] | ↔ 124303; gleich wie MD 125037, MI 130130, REPO 01 | |
| 11 | MD 124303 | IS | UF Infrastrukturraum (IS) | „Temperatur:“ [Kompressor 3] | „Kontrolle Druckluftfilter (Störungsfrei):“ [Kompressor 2] | ↔ 124255/124310; ≈ MD 125043, MI 130134, REPO 02 | |
| 12 | MD 124310 | IS | UF Infrastrukturraum (IS) | „Kontrolle Druckluftfilter (Störungsfrei):“ | [Kältetrockner 1] | ↔; ≈ MD 125048, MI 130139, REPO 03 | |
| 13 | MD 124319 | IS | UF Infrastrukturraum (IS) | [Kältetrockner 1] | „Kontrolle Wasseraufbereitung (Störungsfrei):“ | ↔; ≈ MD 125054, MI 130144, REPO 03/04 | Balken „Wasseraufbereitung (Jansen)“ |
| 14 | MD 124327 | IS | UF Infrastrukturraum (IS) | „Kontrolle Wasseraufbereitung (Störungsfrei):“ | „Kontrolle Siebkorbfilter 1 (ab 0,5 bar Reinigung):“ | ↔; ≈ MD 125100, MI 130147, REPO 04/05 | rote Meldung „Sollzustand von mindesten 2,0 bar nicht erreicht!“ bei leerem Feld |
| 15 | MD 124334 | IS | UF Infrastrukturraum (IS) | „Sollzustand von mindesten 2,0 bar …“ (Meldung) | „Zählerstand Wasseruhr über Tank:“ | ↔; ≈ MD 125105, MI 130153, REPO 05/06 | |
| 16 | MD 124341 | IS | UF Infrastrukturraum (IS) | „Kontrolle Luftfilter Schaltschrank:“ | „Betriebsstunden C1:“ [Kältemschine 1] | ↔; ≈ MD 125113, MI 130158, REPO 06 | **Zugangscode Kältemaschine 1 sichtbar – Wert nicht übernommen** |
| 17 | MD 124351 | IS | UF Infrastrukturraum (IS) | „Betriebsstunden C1:“ | „Betriebsstunden A1:“ [Kältemaschine 2] | ↔; ≈ MD 125118, REPO 07 | |
| 18 | MD 124359 | IS | UF Infrastrukturraum (IS) | „Betriebsstunden A1:“ | „Betriebsstunden A1:“ [Kältemaschine 3] | ↔; ≈ MD 125125, MI 130204, REPO 08 | |
| 19 | MD 124405 | IS | UF Infrastrukturraum (IS) | „Kontrolle Kühllamellen:“ | „Mangelbeschreibung:“ | ↔; ≈ MD 125129, MI 130211, REPO 09 | Ende des UF |
| 20 | MD 124413 | ohne | UF „Infrastrukturraum/ Produktionshalle (BS):“ | „Sichtprüfung Feuerlöscher:“ | „Mangelbeschreibung:“ | gleich wie MD 125138, MI 130234 | UF vollständig |
| 21 | MD 124420 | ohne | UF „Produktionshalle:“ | [Sanitärräume (Herren WC)] | „Kontrolle Ordnung und Sauberkeit Damen WC:“ | ↔ 124426; ≈ MD 125145, MI 130240, REPO 10 | |
| 22 | MD 124426 | ohne | UF Produktionshalle | [Sanitärräume (Damen WC)] | „Kontrolle Ordnung und Sauberkeit (Wareneingang):“ | ↔; ≈ MD 125150, MI 130245, REPO 11 | „(ggf. nachfüllen)::“ (doppelter Doppelpunkt) |
| 23 | MD 124432 | ohne | UF Produktionshalle | [Außenbereich] | „Kontrolle Ordnung und Sauberkeit:“ [WZB] | ↔; ≈ MI 130249, REPO 11/12 | |
| 24 | MD 124441 | ohne | UF Produktionshalle | [WZB] | „Kontrolle destilliertes Wasser (Staplerstation):“ | ↔; ≈ MD 125200, MI 130253, REPO 12 | |
| 25 | MD 124457 | ohne | UF Produktionshalle | „Kontrolle destilliertes Wasser (Staplerstation):“ | „Kontrolle Ordnung und Sauberkeit (Containerbereich):“ | ↔; ≈ MD 125204, REPO 12/13 | |
| 26 | MD 124504 | ohne | UF Produktionshalle | [Außenbereich] (2. Mal) | „Kontrolle Beleuchtung (Tor 6):“ | ↔; ≈ MI 130307, REPO 14 | |
| 27 | MD 124511 | ohne | UF Produktionshalle | „Kontrolle Beleuchtung (Tor 6):“ | „Kontrolle Ordnung und Sauberkeit:“ [Küchenbereich] | ↔; ≈ MD 125209, MI 130311, REPO 15 | |
| 28 | MD 124516 | ohne | UF Produktionshalle | (Knopfpaar oben abgeschnitten) [Konfektion] | „Mangelbeschreibung:“ | ↔; ≈ MD 125215, MI 130317, REPO 16 | Ende des UF |
| 29 | MD 124524 | IS | UF „Produktionshalle (IS):“ | „Sichtprüfung Tor 1 (Funktion, Piktogramm):“ | „Temperatur Klimaanlage (Sollzustand 21,0 °C - 25,0 °C):“ [Haftungskabine] | ↔ 124529; gleich wie MD 125227, MI 130328 | |
| 30 | MD 124529 | IS | UF Produktionshalle (IS) | [Haftungskabine] | „Temperatur Klimaanlage (Sollzustand 19,0 °C - 24,0 °C):“ [Messraum] | ↔ | |
| 31 | MD 124535 | IS | UF Produktionshalle (IS) | [Messraum] | „Zählerstand Gaszähler S3:“ | ↔ | **nur Montag**: Stickstoffflasche, Gaszähler |
| 32 | MD 124543 | IS | UF Produktionshalle (IS) | „Zählerstand Gaszähler S2:“ | „Zählerstand Gaszähler S8:“ | ↔ | **nur Montag** |
| 33 | MD 124550 | IS | UF Produktionshalle (IS) | „Zählerstand Gaszähler S8:“ | „Temperatur Klimaanlage:“ [Warenausgangsbüro] | ↔ | |
| 34 | MD 124556 | IS | UF Produktionshalle (IS) | [Warenausgangsbüro] | „Zählerstand Hauptverteilung 1:“ | ↔; ≈ MD 125244, MI 130347 | |
| 35 | MD 124602 | IS | UF Produktionshalle (IS) | „Zählerstand Hauptverteilung 1:“ | „Mangelbeschreibung:“ | ↔; ≈ MD 125301, MI 130351 | Ende des UF; „cos φ“ |
| 36 | MD 124612 | HT | UF „Büro EG:“ | „Kontrolle Ordnung und Sauberkeit:“ | „Sichtprüfung Inventar, Büromöbel, etc. …“ | ↔ 124617 | |
| 37 | MD 124617 | HT | UF Büro EG | „Sichtprüfung Inventar, Büromöbel, etc. …“ | „Mangelbeschreibung:“ | ↔ | unten abgeschnitten |
| 38 | MD 124628 | HT | UF „Büro 1. OG:“ | [Allgemein] | „Sichtprüfung Inventar, Büromöbel, etc. …“ | ↔ 124634 | |
| 39 | MD 124634 | HT | UF Büro 1. OG | „Sichtprüfung Inventar, Büromöbel, etc. …“ | „Kontrolle Ordnung und Sauberkeit:“ [Küchenbereich] | ↔ | |
| 40 | MD 124639 | HT | UF Büro 1. OG | [Küchenbereich] | „Kontrolle Temperatur aller Durchlauferhitzer (mind. 60 °C):“ | ↔ | Besuchertoiletten Herren/Damen |
| 41 | MD 124644 | HT | UF Büro 1. OG | „Kontrolle Temperatur aller Durchlauferhitzer (mind. 60 °C):“ | „Mangelbeschreibung:“ | ↔ | „(ggf. nachfüllen)::“ |
| 42 | MD 124653 | IS | UF „Büro 1. OG (IS):“ | „Temperatur Serverraum (Sollzustand 18,0 °C - 21,0 °C):“ | „Mangelbeschreibung:“ | gleich wie MD 125317, MI 130401 | UF vollständig |
| 43 | MD 124702 | HT | UF „Sozialräume:“ | [Allgemein] | „Sichtprüfung Inventar, Büromöbel, etc. …“ | ↔ 124708 | |
| 44 | MD 124708 | HT | UF Sozialräume | (Knopfpaar oben abgeschnitten) [Herren WC] | „Kontrolle Füllstand Handtuchpapierspender Herren WC (ggf. …“ | ↔ | „(ggf. nachfüllen)::“ bei Seifenspender Herren |
| 45 | MD 124714 | HT | UF Sozialräume | „Kontrolle Füllstand Handtuchpapierspender Herren WC …“ | „Kontrolle Füllstand Handtuchpapierspender Damen WC …“ | ↔ | |
| 46 | MD 124720 | HT | UF Sozialräume | „Kontrolle Füllstand Seifenspender Damen WC …“ | „Mangelbeschreibung:“ | ↔ | oben ein Knopfpaar ohne Beschriftung |
| 47 | MD 124729 | HT | UF „Allgemein:“ | [Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle)] | „1. OG Damen WC HWB rechts:“ | ↔ 124737 | |
| 48 | MD 124737 | HT | UF Allgemein | „1. OG Damen WC HWB rechts:“ | „Rücksprache mit Kunde, ob Reinigungszustand …“ | ↔ | |
| 49 | MD 124743 | HT | UF Allgemein | „1. OG Herren Dusche 4. HWB von links:“ | „Mangelbeschreibung:“ | ↔ | |
| 50 | MD 124750 | HT | UF „Sammelstation für Altöl und Gefahrstoffe:“ | „Sichtkontrolle der Auffangwannen/ Auffangtassen nach AwSV:“ | „Mangelbeschreibung:“ | – | UF vollständig |
| 51 | MD 124756 | ohne | UF „Brandschutz:“ | „Feuerschutzabschlüsse (BS-Türen, BS-Tore) geschlossen, bzw. …“ | „Brennbare Abfälle und selbstentzündliche Stoffe …“ | ↔ 124801; gleich wie MD 125324, MI 130410 | |
| 52 | MD 124801 | ohne | UF Brandschutz | „Brennbare Abfälle …“ | „Kontrolle ob das Rauchverbot entsprechend eingehalten wird:“ | ↔; ≈ MD 125330, MI 130415 | |
| 53 | MD 124807 | ohne | UF Brandschutz | „Kontrolle ob das Rauchverbot …“ | „Mangelbeschreibung:“ | ↔; ≈ MD 125334, MI 130420 | |
| 54 | MD 124814 | – | HF Ende | „Allgemein:“ (+ Kontrollieren) | „Unterschrift des ausführenden Haustechnikers:“ | ≈ MD 125340, MI 130442 | danach „Bemerkungen:“, „Formular senden“ |

### 3.2 Dienstag (`montag_dienstag`, 12:50–12:53)

| # | Datei | PDF | Bildschirm | erste sichtbare Frage | letzte sichtbare Frage | Überlappung / Duplikat | Bemerkung |
|---|---|---|---|---|---|---|---|
| 55 | MD 125017 | ohne | UF „Brandmeldezentrale (BMZ):“ | „Sichtprüfung ob frei zugänglich, ÜE eingeschaltet:“ | „Mangelbeschreibung:“ | gleich wie MD 124226, MI 130117 | erstes Bild Dienstag |
| 56 | MD 125026 | IS | UF „Batterieraum:“ | „Kontrolle ob Störungsfrei:“ | „Mangelbeschreibung:“ | gleich wie MD 124232, MI 130123 | |
| 57 | MD 125037 | IS | UF „Infrastrukturraum (IS):“ | „Sichtprüfung Heizungsanlage:“ | „Temperatur:“ | ↔; gleich wie MD 124255 | |
| 58 | MD 125043 | IS | UF Infrastrukturraum (IS) | „Temperatur:“ | „Kontrolle Druckluftfilter (Störungsfrei):“ | ↔ | |
| 59 | MD 125048 | IS | UF Infrastrukturraum (IS) | „Kontrolle Druckluftfilter (Störungsfrei):“ | „Sichtprüfung Betriebszustand (im Grünen Bereich):“ | ↔ | |
| 60 | MD 125054 | IS | UF Infrastrukturraum (IS) | [Kältetrockner 1] | „Kontrolle Wasseraufbereitung (Störungsfrei):“ | ↔ | |
| 61 | MD 125100 | IS | UF Infrastrukturraum (IS) | „Kontrolle Wasseraufbereitung (Störungsfrei):“ | „Kontrolle Siebkorbfilter 1 (ab 0,5 bar Reinigung):“ | ↔ | rote Meldung „mindesten 2,0 bar“ |
| 62 | MD 125105 | IS | UF Infrastrukturraum (IS) | „Sollzustand von mindesten 2,0 bar …“ (Meldung) | „Zählerstand Wasseruhr über Tank:“ | ↔ | |
| 63 | MD 125113 | IS | UF Infrastrukturraum (IS) | „Zählerstand Wasseruhr über Tank:“ | „Betriebsstunden C2:“ | ↔ | **Zugangscode Kältemaschine 1 sichtbar – nicht übernommen** |
| 64 | MD 125118 | IS | UF Infrastrukturraum (IS) | „Betriebsstunden C2:“ | „Betriebsstunden B1/ C1:“ [Kältemaschine 2] | ↔ | |
| 65 | MD 125125 | IS | UF Infrastrukturraum (IS) | „Betriebsstunden B1/ C1:“ | „Betriebsstunden B1/ C1:“ [Kältemaschine 3] | ↔ | |
| 66 | MD 125129 | IS | UF Infrastrukturraum (IS) | „Kontrolle Kühllamellen:“ | „Mangelbeschreibung:“ | ↔ | Ende des UF |
| 67 | MD 125138 | ohne | UF „Infrastrukturraum/ Produktionshalle (BS):“ | „Sichtprüfung Feuerlöscher:“ | „Mangelbeschreibung:“ | gleich wie MD 124413, MI 130234 | |
| 68 | MD 125145 | ohne | UF „Produktionshalle:“ | [Sanitärräume (Herren WC)] | „Kontrolle Füllstand Seifenspender Damen WC (ggf.“ | ↔ | unten abgeschnitten |
| 69 | MD 125150 | ohne | UF Produktionshalle | [Sanitärräume (Damen WC)] | „Kontrolle Ordnung und Sauberkeit (Wareneingang):“ | ↔ | |
| 70 | MD 125155 | ohne | UF Produktionshalle | (Knopfpaar oben abgeschnitten) | [WZB] | ↔ | |
| 71 | MD 125200 | ohne | UF Produktionshalle | [WZB] | „Kontrolle destilliertes Wasser (Staplerstation):“ | ↔ | |
| 72 | MD 125204 | ohne | UF Produktionshalle | „Kontrolle destilliertes Wasser (Staplerstation):“ | „Kontrolle Ordnung und Sauberkeit (Containerbereich):“ | ↔ | |
| 73 | MD 125209 | ohne | UF Produktionshalle | „Kontrolle Ordnung und Sauberkeit (Containerbereich):“ | [Konfektion] | ↔ | **UNSICHER**: Ob zwischen 125204 und 125209 Bereiche fehlen (Mo hat dort Allgemein / 2. Außenbereich / Tore), wird in D2 geprüft. |
| 74 | MD 125215 | ohne | UF Produktionshalle | (Knopfpaar oben abgeschnitten) [Konfektion] | „Mangelbeschreibung:“ | ↔ | Ende des UF |
| 75 | MD 125227 | IS | UF „Produktionshalle (IS):“ | „Sichtprüfung Tor 1 (Funktion, Piktogramm):“ | „Temperatur Klimaanlage (Sollzustand 21,0 °C - 25,0 °C):“ | gleich wie MD 124524 | |
| 76 | MD 125232 | IS | UF Produktionshalle (IS) | „Temperatur Klimaanlage (Sollzustand 21,0 °C - 25,0 °C):“ | „Temperatur Klimaanlage:“ [Wareneingangsbüro] | ↔ | **keine Gaszähler** (anders als Mo) |
| 77 | MD 125237 | IS | UF Produktionshalle (IS) | [Wareneingangsbüro] | [Warenausgangsbüro] | ↔ | |
| 78 | MD 125244 | IS | UF Produktionshalle (IS) | [Warenausgangsbüro] | „Zählerstand Hauptverteilung 1:“ | ↔ | |
| 79 | MD 125301 | IS | UF Produktionshalle (IS) | „Zählerstand Hauptverteilung 1:“ | „Mangelbeschreibung:“ | ↔ | |
| 80 | MD 125317 | IS | UF „Büro 1. OG (IS):“ | „Temperatur Serverraum (Sollzustand 18,0 °C - 21,0 °C):“ | „Mangelbeschreibung:“ | gleich wie MD 124653, MI 130401 | |
| 81 | MD 125324 | ohne | UF „Brandschutz:“ | „Feuerschutzabschlüsse …“ | „Brennbare Abfälle …“ | ↔; gleich wie MD 124756 | |
| 82 | MD 125330 | ohne | UF Brandschutz | „Brennbare Abfälle …“ | „Keine brennenden Kerzen, …“ (halb abgeschnitten) | ↔ | Text vollständig in 125334 |
| 83 | MD 125334 | ohne | UF Brandschutz | „Kontrolle ob das Rauchverbot …“ | „Mangelbeschreibung:“ | ↔ | |
| 84 | MD 125340 | – | HF Ende | „Produktionshalle (IS):“ (+ Kontrollieren) | „Unterschrift des ausführenden Haustechnikers:“ | ≈ MD 124814 | das Feld darüber ist abgeschnitten |

### 3.3 Mittwoch (`mittwoch`, 13:01–13:04)

| # | Datei | PDF | Bildschirm | erste sichtbare Frage | letzte sichtbare Frage | Überlappung / Duplikat | Bemerkung |
|---|---|---|---|---|---|---|---|
| 85 | MI 130117 | ohne | UF „Brandmeldezentrale (BMZ):“ | „Sichtprüfung ob frei zugänglich, ÜE eingeschaltet:“ | „Mangelbeschreibung:“ | gleich wie MD 124226/125017 | Kopie „(1)“ byte-gleich |
| 86 | MI 130123 | IS | UF „Batterieraum:“ | „Kontrolle ob Störungsfrei:“ | „Mangelbeschreibung:“ | gleich wie MD 124232/125026 | |
| 87 | MI 130130 | IS | UF „Infrastrukturraum (IS):“ | „Sichtprüfung Heizungsanlage:“ | „Temperatur:“ | ↔ | |
| 88 | MI 130134 | IS | UF Infrastrukturraum (IS) | „Temperatur:“ | „Kontrolle Druckluftfilter (Störungsfrei):“ | ↔ | |
| 89 | MI 130139 | IS | UF Infrastrukturraum (IS) | „Kontrolle Druckluftfilter (Störungsfrei):“ | „Sichtprüfung Betriebszustand (im Grünen Bereich):“ | ↔ | |
| 90 | MI 130144 | IS | UF Infrastrukturraum (IS) | [Kältetrockner 1] | „Kontrolle Wasseraufbereitung (Störungsfrei):“ | ↔ | |
| 91 | MI 130147 | IS | UF Infrastrukturraum (IS) | „Kontrolle Wasseraufbereitung (Störungsfrei):“ | „Kontrolle Siebkorbfilter 1 (ab 0,5 bar Reinigung):“ | ↔ | rote Meldung „mindesten 2,0 bar“ |
| 92 | MI 130153 | IS | UF Infrastrukturraum (IS) | „Kontrolle Siebkorbfilter 1 …“ | [Kältemschine 1 (Außenbereich/ Display im …] | ↔ | |
| 93 | MI 130158 | IS | UF Infrastrukturraum (IS) | [Kältemschine 1 (Außenbereich/ Display im Infrastrukturraum)] | „Kontrolle Störungsanzeige:“ | ↔ | **Zugangscode Kältemaschine 1 sichtbar – nicht übernommen** |
| 94 | MI 130204 | IS | UF Infrastrukturraum (IS) | [Kältemaschine 2 (Außenbereich)] | [Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum)] | – | **UNSICHER**: Zwischen 130158 und 130204 fehlt evtl. das Ende von Kältemaschine 1 (Mo: Betriebsstunden C1/C2). Prüfung in D2. |
| 95 | MI 130211 | IS | UF Infrastrukturraum (IS) | [Kältemaschine 3 …] | „Mangelbeschreibung:“ | ↔ | |
| 96 | MI 130234 | ohne | UF „Infrastrukturraum/ Produktionshalle (BS):“ | „Sichtprüfung Feuerlöscher:“ | „Mangelbeschreibung:“ | gleich wie MD 124413/125138 | |
| 97 | MI 130240 | ohne | UF „Produktionshalle:“ | [Sanitärräume (Herren WC)] | „Kontrolle Ordnung und Sauberkeit Damen WC:“ | ↔ | |
| 98 | MI 130245 | ohne | UF Produktionshalle | [Sanitärräume (Damen WC)] | „Kontrolle Ordnung und Sauberkeit (Wareneingang):“ | ↔ | „(ggf. nachfüllen)::“ |
| 99 | MI 130249 | ohne | UF Produktionshalle | [Außenbereich] | „Kontrolle Ordnung und Sauberkeit:“ [WZB] | ↔ | |
| 100 | MI 130253 | ohne | UF Produktionshalle | [WZB] | „Kontrolle destilliertes Wasser (Staplerstation):“ | ↔ | |
| 101 | MI 130301 | ohne | UF Produktionshalle | [Allgemein] | „Kontrolle Gehörschutzboxen:“ | ↔ (Lücke?) | Kopfzeile hier „‹ Speichern & Schließen“ statt „‹ Zurück“ |
| 102 | MI 130307 | ohne | UF Produktionshalle | „Kontrolle Gehörschutzboxen:“ | „Kontrolle Aschenbecher/ Beleuchtung (Tor 5):“ | ↔ | |
| 103 | MI 130311 | ohne | UF Produktionshalle | „Kontrolle Aschenbecher/ Beleuchtung (Tor 5):“ | (Balken halb sichtbar, vermutlich [Küchenbereich]) | ↔ | |
| 104 | MI 130317 | ohne | UF Produktionshalle | (Knopfzeile oben abgeschnitten) | „Mangelbeschreibung:“ | ↔ | Ende des UF |
| 105 | MI 130328 | IS | UF „Produktionshalle (IS):“ | „Sichtprüfung Tor 1 (Funktion, Piktogramm):“ | (Balken halb sichtbar) | gleich wie MD 124524/125227 | |
| 106 | MI 130332 | IS | UF Produktionshalle (IS) | [Analysebüro] | [Allgemein] | ↔ | keine Gaszähler (wie Di) |
| 107 | MI 130336 | IS | UF Produktionshalle (IS) | [Allgemein] | „Temperatur Klimaanlage:“ + Balken abgeschnitten | ↔ | |
| 108 | MI 130347 | IS | UF Produktionshalle (IS) | [Warenausgangsbüro] | „Zählerstand Hauptverteilung 1:“ | ↔ | „cos φ“, „Normalbereich cos φ > 0,90“ |
| 109 | MI 130351 | IS | UF Produktionshalle (IS) | „Zählerstand Hauptverteilung 1:“ | „Mangelbeschreibung:“ | ↔ | |
| 110 | MI 130401 | IS | UF „Büro 1. OG (IS):“ | „Temperatur Serverraum (Sollzustand 18,0 °C - 21,0 °C):“ | „Mangelbeschreibung:“ | gleich wie MD 124653/125317 | |
| 111 | MI 130405 | LEG | UF „Legionellen Prävention:“ | „1. OG Damenumkleide Dusche (10 Minuten Wasser mit mind. 60 °…“ | „Mangelbeschreibung:“ | – | **einziges Bild Legionellen**, UF vollständig |
| 112 | MI 130410 | ohne | UF „Brandschutz:“ | „Feuerschutzabschlüsse …“ | „Brennbare Abfälle …“ | ↔; gleich wie MD 124756/125324 | |
| 113 | MI 130415 | ohne | UF Brandschutz | „Brennbare Abfälle …“ | „Kontrolle ob das Rauchverbot …“ | ↔ | |
| 114 | MI 130420 | ohne | UF Brandschutz | (Knopfpaar oben abgeschnitten) | „Mangelbeschreibung:“ | ↔ | |
| 115 | MI 130432 | – | HF Kopf | „Datum:“ | „Brandmeldezentrale (BMZ):“ | gleich wie MD 124141 | Datum 10.11.2026, KW 38, Wochentag **Mittwoch** |
| 116 | MI 130437 | – | HF Liste | „Brandmeldezentrale (BMZ):“ | „Produktionshalle (IS):“ | – | enthält **„Gefahrstoffschränke:“** ohne rote Meldung; „Produktionshalle:“ hat einen angefangenen Eintrag „1. Eingaben bearbeiten“ + „Ein Artikel ist ungültig“ |
| 117 | MI 130442 | – | HF Ende | „Produktionshalle (IS):“ | „Unterschrift des ausführenden Haustechnikers:“ | ≈ MD 124814/125340 | |

### 3.4 Alte Repo-Bilder vom 02.11. (`quellen/…/infrastruktur/`)

| # | Datei | PDF | Bildschirm | erste sichtbare Frage | letzte sichtbare Frage | Duplikat | Bemerkung |
|---|---|---|---|---|---|---|---|
| 118 | REPO 01 | IS | UF „Infrastrukturraum (IS):“ | „Sichtprüfung Heizungsanlage:“ | „Temperatur:“ [Kompressor 3] | ≈ MD 124255 | |
| 119 | REPO 02 | IS | UF Infrastrukturraum (IS) | (Zahlenfeld oben abgeschnitten) | „Kontrolle Druckluftfilter (Störungsfrei):“ [Kompressor 2] | ≈ MD 124303 | |
| 120 | REPO 03 | IS | UF Infrastrukturraum (IS) | [Kompressor 1] | [Kältetrockner 2] | ≈ MD 124310 | |
| 121 | REPO 04 | IS | UF Infrastrukturraum (IS) | [Kältetrockner 2] | „Kontrolle Wasserqualität Öwamat (mit Teststreifen):“ | ≈ MD 124319 | |
| 122 | REPO 05 | IS | UF Infrastrukturraum (IS) | [Öwamat] | „Kontrolle Siebkorbfilter 2 (ab 0,5 bar Reinigung):“ | ≈ MD 124327/124334 | rote Meldung „mindesten 2,0 bar“ |
| 123 | REPO 06 | IS | UF Infrastrukturraum (IS) | „Kontrolle Verschmutzung Pumpen (Lüfterräder):“ | „Wassertemperatur (Ausgang):“ [Kältemschine 1] | ≈ MD 124334/124341 | Zugangscode im Bild **schon geschwärzt** |
| 124 | REPO 07 | IS | UF Infrastrukturraum (IS) | (Zahlenfeld oben abgeschnitten) | „Betriebsstunden A1:“ [Kältemaschine 2] | ≈ MD 124351 | |
| 125 | REPO 08 | IS | UF Infrastrukturraum (IS) | „Betriebsstunden B1/ C1:“ | „Betriebsstunden B1/ C1:“ [Kältemaschine 3] | ≈ MD 124359 | |
| 126 | REPO 09 | IS | UF Infrastrukturraum (IS) | [Kältemaschine 3 …] | „Mangelbeschreibung:“ | ≈ MD 124405 | |
| 127 | REPO 10 | ohne | UF „Produktionshalle:“ | [Sanitärräume (Herren WC)] | „Kontrolle Füllstand Seifenspender Damen WC (ggf. nachfüllen)::“ | ≈ MD 124420 | |
| 128 | REPO 11 | ohne | UF Produktionshalle | „Kontrolle Füllstand Seifenspender Damen WC …::“ | „Kontrolle der Wartungsaufkleber an allen Abfallcontainern …“ | ≈ MD 124426/124432 | |
| 129 | REPO 12 | ohne | UF Produktionshalle | „Kontrolle der Wartungsaufkleber …“ | [Allgemein] | ≈ MD 124441/124457 | |
| 130 | REPO 13 | ohne | UF Produktionshalle | [Allgemein] | [Außenbereich] | ≈ MD 124457/124504 | |
| 131 | REPO 14 | ohne | UF Produktionshalle | [Außenbereich] | „Kontrolle Ordnung und Sauberkeit (Warenausgang):“ | ≈ MD 124504 | |
| 132 | REPO 15 | ohne | UF Produktionshalle | „Kontrolle Aschenbecher/ Beleuchtung (Tor 5):“ | [Küchenbereich] | ≈ MD 124511 | |
| 133 | REPO 16 | ohne | UF Produktionshalle | (Knöpfe oben abgeschnitten) [Konfektion] | „Mangelbeschreibung:“ | ≈ MD 124516 | |

## 4. Erste Auffälligkeiten (werden in den Durchgängen 2–5 genau geprüft)

1. **Zugangscode Kältemaschine 1** ist auf `MD 124341`, `MD 125113` und `MI 130158` **ungeschwärzt lesbar**. Diese Bilder liegen nur lokal und kommen nicht ins Repo. Der Wert wurde nirgends abgeschrieben. Im Repo-Bild `REPO 06` ist er geschwärzt.
2. **Tippfehler stehen noch am 10.11. im Formular** (belegt):
   - „Kältemschine 1“ im Balken
   - „Kontrolle Kühlamellen:“ bei Kältemaschine 1 (bei 2/3 „Kühllamellen“)
   - „(ggf. nachfüllen)::“ in Produktionshalle, Büro 1. OG und Sozialräume
   - „mindesten“ in der roten Meldung
   „Kältemaschine 2/3“ sind schon richtig geschrieben.
3. **Rote Meldung bei leerem Feld:** „Sollzustand von mindesten 2,0 bar nicht erreicht!“ steht schon da, bevor etwas eingetragen ist (alle Tage). Das ist ein Hinweis darauf, wie MoreApp die Grenze prüft (s. Durchgang 4).
4. **„Wasseraufbereitung (Jansen)“**: Das ist vermutlich ein Firmenname (Hersteller/Wartungsfirma), kein Personenname. Deshalb wurde er übernommen (geschlussfolgert, Frage F6).
5. **Ausgefüllt ist nichts:** Auf den Bildern vom 10.11. ist kein Knopf gewählt und kein Wert eingetragen. Deshalb sieht man **keine** Felder, die erst nach „nicht in Ordnung“ erscheinen. Ob es solche bedingten Felder gibt, lässt sich mit diesen Bildern nicht prüfen (Frage F5).

## 5. Lücken – was auf keinem Bild zu sehen ist

| # | Lücke | Folge |
|---|---|---|
| L1 | Unterformular **„Gefahrstoffschränke:“** (Mittwoch): nur in der Liste, **Inhalt nicht fotografiert** | Fragen nur aus dem PDF vom 28.10. (3 Schränke × 2 Fragen); Stern, Hinweise und Mangelfeld unbekannt |
| L2 | Hauptformular **Montag** zwischen „Grünflächen …“ und „Allgemein:“ | Reihenfolge der Unterformulare ist nur aus der Reihenfolge der Screenshots erschlossen. Ob es montags „Gefahrstoffschränke“ gibt, ist offen. |
| L3 | Hauptformular **Dienstag** oben (Wochentag-Feld, Liste bis „Produktionshalle (IS)“) | Dass die Bilder ab 125017 Dienstag sind, sagt nur Josias. Die Liste der Unterformulare ist aus den Screenshots erschlossen. |
| L4 | **Donnerstag, Freitag** (und Sa/So) | Keine Bilder. Gibt es an diesen Tagen einen Rundgang? |
| L5 | Bilder **nach „nicht in Ordnung“** bzw. mit Grenzverletzung | Bedingte Felder und Foto-Felder sind nicht prüfbar. |
| L6 | Auswahlliste „Wochentag“ aufgeklappt, „Ausführender Haustechniker“ aufgeklappt | Welche Wochentage es gibt, ist unbekannt. Namen sollen sowieso nicht übernommen werden. |
| L7 | mögliche Scroll-Lücken: Mi Infrastrukturraum (IS) zwischen 130158 und 130204, Di Produktionshalle zwischen 125204 und 125209, Mi Produktionshalle zwischen 130253 und 130301 | wird in Durchgang 2 gegen die anderen Tage geprüft |

## 6. Fragen an Josias aus Durchgang 1

- **F1 (wichtig, Zuordnung):** In MoreApp gibt es **einen** Rundgang „Objektrundgang TGI MMS“. Er zeigt je nach Wochentag andere Unterformulare. Die vier PDFs sind Auszüge daraus. Wie soll das in unserer App aussehen?
  - **Vorschlag A:** je Wochentag ein Rundgang, z. B. „Objektrundgang Montag / Dienstag / Mittwoch“, mit Plan = dieser Wochentag. Das bildet MoreApp am genauesten nach.
  - **Vorschlag B:** je PDF ein Rundgang (Haustechnik, Infrastruktur, Legionellen, Gefahrstoffschränke, dazu neu „Brandschutz“?). Dann müssten Unterformulare wie „Infrastrukturraum (IS)“ in mehreren Plänen (Mo + Di + Mi) laufen.
  - Dazu: Wohin gehören die Unterformulare ohne PDF („Brandmeldezentrale (BMZ)“, „Infrastrukturraum/ Produktionshalle (BS)“, „Produktionshalle“, „Brandschutz“)?
- **F2:** Gibt es Donnerstag/Freitag-Rundgänge? Wenn ja, bitte dieselben Bilder auch für diese Tage machen.
- **F3:** Bitte das Unterformular **„Gefahrstoffschränke:“** (Mittwoch) fotografieren. Außerdem bitte das Hauptformular **Montag** und **Dienstag** einmal ganz durchscrollen und fotografieren (nur die Liste der Unterformulare).
- **F4:** Gibt es Gefahrstoffschränke auch am Montag oder Dienstag? Das klärt sich mit den Bildern aus F3.
- **F5 (für später):** Wenn möglich, bei zwei oder drei Fragen „nicht in Ordnung“ antippen und fotografieren, z. B. Batterieraum und eine Zahl außerhalb der Grenze. So sehen wir, ob Zusatzfelder (Foto, Text) erscheinen. Danach **nicht senden**.
- **F6:** Ist „Jansen“ in „Wasseraufbereitung (Jansen)“ eine Firma? (Vorschlag: ja, so übernehmen.)

## 7. Nächster Schritt
Durchgang 2 (Struktur) beginnt mit **Infrastruktur**: Batterieraum, Infrastrukturraum (IS), Produktionshalle (IS), Büro 1. OG (IS). Dabei werden die Abschnitte und die Zahl der Fragen je Abschnitt für jeden Tag einzeln aufgeschrieben und die Tage miteinander verglichen. Wegen F1 ordne ich zunächst so zu wie im PDF und kennzeichne die Wochentage.
