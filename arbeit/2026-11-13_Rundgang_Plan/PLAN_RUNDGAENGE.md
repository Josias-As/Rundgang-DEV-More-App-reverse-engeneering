# Bauplan der echten Rundgänge (Stand 13.11.2026)

Erstellt vom Einsetz-Chat als **Denkschritt vor dem Bauen**. Grundlage: Bildanalyse `arbeit/2026-11-10_Bildanalyse/` (133 Screenshots Mo/Di/Mi + 4 PDFs), Vorgaben von Josias. Noch **nichts** davon ist in SharePoint angelegt.

- **Josias' Vorgaben (13.11.):** „lieber mehr drin als weniger“ · aktuelles Konzept (5 Rundgänge nach Intervall), ein späterer Umbau auf Wochentags-Rundgänge bleibt möglich · zu jedem Prüfpunkt alles festlegen · Änderungen erlaubt, wenn sie gut passen · alles dokumentieren.
- **Maschinenlesbar:** `PLAN_RUNDGAENGE.csv` (eine Zeile je Prüfpunkt, alle Einstellungen, Begründung, Quelle). Erzeugt mit `plan_erzeugen.js` aus den Analyse-CSVs – Änderungen an den Regeln dort, dann neu erzeugen.
- **Kennzeichnung:** In der Spalte „Änderung ggü. MoreApp“ steht alles, was **nicht** 1:1 aus MoreApp kommt. Leer = genau wie in MoreApp.

## 1. Überblick

| Rundgang | Plan | Prüfpunkte | Kategorien (Seiten) |
|---|---|---|---|
| Infrastrukturrundgang TGI MMS | Mo, Mi, Fr | 76 + Bemerkungen | 8 |
| Brandschutzrundgang TGI MMS | Mo–Fr | 45 + Bemerkungen | 5 |
| Haustechnikrundgang TGI MMS | Mo | 75 + Bemerkungen | 9 |
| Legionellen Prävention TGI MMS | Mo | 2 + Bemerkungen | 1 |
| Sichtprüfung Gefahrstoffschränke TGI MMS | Mo | 6 + Bemerkungen | 1 |

Alle: **Testrundgang = Ja** bis zur Inbetriebnahme (Läufe landen in der Test-Ablage, nicht im Banner). Kopfdaten: Standort „TGI MMS“, Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“, Auftraggeber „Technoform Glass Insulation GmbH“ (aus dem PDF-Kopf; „TGI MMS“ als Standort geschlussfolgert).

## 2. Grundregeln für jeden Prüfpunkt (wenn in der Tabelle nichts anderes steht)

| Einstellung | Wert | Warum |
|---|---|---|
| Typ | i.O./n.i.O. | MoreApp nutzt fast überall „in Ordnung / nicht in Ordnung“ (belegt) |
| Antwort | **Pflicht** | in MoreApp mit Stern (belegt) |
| Kommentar | **Pflicht bei Mangel** | entspricht dem MoreApp-Feld „Mangelbeschreibung*“ je Unterformular – bei uns direkt an der Frage |
| Foto | **kein Foto (bei n.i.O. möglich)** | in MoreApp kein Foto-Feld zu sehen (Q-ALL-3); bei n.i.O. kann der Prüfer trotzdem fotografieren |
| Zahl außerhalb Grenzen | **Mangel** (bei echten Soll-Werten) | MoreApp zeigt rote Meldung (belegt bei 2,0 bar) |
| Fragetext | wörtlich aus MoreApp, **ohne** den Doppelpunkt am Ende, eindeutige Tippfehler korrigiert | Doppelpunkt ist MoreApp-Formularstil; Tippfehler haben keine Bedeutung |
| Nur zeigen, wenn … | immer zeigen | MoreApp-Bilder zeigen keine bedingten Felder (nichts angetippt, Q-ALL-3) |
| Info ⓘ (Anleitung/Bild) | keine | Objekthandouts noch unbekannt (Q-ALL-4) |

## 3. Entscheidungen (mit Begründung und Sicherheit)

| # | Entscheidung | Begründung | Sicherheit |
|---|---|---|---|
| E1 | **Gaszähler S1–S8 und „Füllung Stickstoffflasche“** bleiben im Infrastrukturrundgang (Mo/Mi/Fr), aber **freiwillig** mit Hinweis „Nur montags ablesen“ | „lieber mehr drin“; kein Extra-Rundgang nötig; an Mi/Fr darf leer bleiben. Bei Umbau auf Wochentags-Rundgänge einfach im Montags-Rundgang Pflicht setzen | gut begründet |
| E2 | **Brandmeldezentrale** und **Produktionshalle** (ohne Kürzel) → **Brandschutzrundgang** | täglich in MoreApp wie Brandschutz, Inhalte Sicherheit/Ordnung | geschlussfolgert (kein PDF) |
| E3 | **Legionellen** und **Gefahrstoffschränke**: Plan **Montag** (Josias' Liste) | MoreApp zeigt sie am Mittwoch – Plan ist im Builder mit 2 Klicks änderbar | Vorgabe Josias, Widerspruch dokumentiert |
| E4 | **Infrastrukturraum (44 Fragen)** in 4 Seiten: Heizung und Kompressoren · Kältetrockner und Wasseraufbereitung · ONI Kühlanlage · Kältemaschinen | kürzere Seiten, Zwischenspeichern, weniger Verlust bei Abbruch; Reihenfolge wie MoreApp | gut begründet |
| E5 | **Produktionshalle (IS)** in 2 Seiten (Räume und Klima / Zähler, Tore, Technik); **Produktionshalle (Brandschutz)** in 2 Seiten; **Büro 1. OG (Haustechnik)** in 2 Seiten | gleiche Gründe wie E4, Reihenfolge bleibt | gut begründet |
| E6 | **Bereichs-Überschriften** nur im Infrastrukturrundgang sichtbar (Batterieraum, Infrastrukturraum, Produktionshalle, Büro 1. OG); sonst ein ausgeblendeter Bereich | dort helfen sie bei 8 Seiten; bei den anderen entsprechen die Seiten direkt den MoreApp-Unterformularen | Geschmack |
| E7 | **„nur steigend“** bei allen Zählerständen und Betriebsstunden | fängt Tippfehler ab (Josias: Prüfer nicht verlässlich → Kontrollen) | sicher sinnvoll |
| E8 | **„nicht messbar“ erlaubt** bei Raumklima ohne Gerät/Anzeige (Haftungskabine, Waren-Ein-/Ausgangsbüro) und Gaszähler S2/S8 | im PDF stand dort „0“ – ehrliche Antwort mit Begründung statt falscher 0 | belegt (PDF) |
| E9 | **Plausibilitätsgrenzen „Hinweis + Grund“** für Zahlen ohne Soll: Kompressor-Betriebsdruck 4–13 bar, Kompressor-Temperatur 0–110 °C, Wassertemperatur Kältemaschine 0–30 °C, Raumtemperatur 10–35 °C, Stickstoffflasche 0–300 bar | fängt Vertipper (z. B. 920 statt 92), **sperrt nie, kein Mangel** – nur Begründung | **Grenzen geraten** – Haustechnik bitte bestätigen oder Werte nennen |
| E10 | **Rückfrage** bei „Störungsfrei“, „Störungsanzeige“, „im grünen Bereich“ | verhindert versehentliches n.i.O. bei Anlagen, die praktisch immer laufen | sinnvoll, abschaltbar |
| E11 | **Brandmeldezentrale „kritisch“** (rotes Fenster, sofort melden) | ÜE aus = Brand wird nicht an Feuerwehr gemeldet. Braucht Ansprechpartner-Einträge (Brandschutzbeauftragter, Haustechnik-Leitung) – **Namen/Telefon von Josias** | Vorschlag, in MoreApp nicht vorhanden |
| E12 | **🔑 Zugangscode „Bedienteil Kältemaschine 1“** an Wassertemperatur + Betriebsstunden C1/C2 | MoreApp zeigt den Code rot offen (belegt) – bei uns erst nach Antippen | belegt; **Codewert trägt Josias ein** |
| E13 | **Trinkwasser spülen** (10 Entnahmestellen): Knöpfe „durchgeführt / nicht durchgeführt“, Zeitangabe als Hinweis | es wird eine Tätigkeit bestätigt (wie Legionellen) | Änderung ggü. MoreApp |
| E14 | **„Rücksprache mit Kunde …“** eigener Abschnitt „Reinigung“, Knöpfe „zufriedenstellend / nicht zufrieden“, Hinweis „im Kommentar dokumentieren“ | gehört nicht zum Spülen; „Mängelprotokoll“ = bei uns Kommentar + Mangel | Änderung ggü. MoreApp |
| E15 | Klammer-Anweisungen werden **Hinweise**: Legionellen „10 Minuten … 60 °C“, Sammelstation „Verschmutzungen sofort entfernen lassen!“, Brandschutz „Aufgrund der baulichen Gegebenheiten …“ | Frage bleibt kurz, Anweisung steht trotzdem unter der Frage | Änderung ggü. MoreApp |
| E16 | Am Ende jedes Rundgangs **„Bemerkungen“** (Text, freiwillig) | MoreApp hat „Bemerkungen:“ am Formularende (belegt) | belegt |
| E17 | Grenzen, die nur im Text stehen, aber in MoreApp i.O./n.i.O. sind (Durchlauferhitzer „mind. 60 °C“, „min. 1 Karton“, Siebkorbfilter „ab 0,5 bar“) → **bleiben i.O./n.i.O.** | 1:1, kein Zahlenfeld in MoreApp | belegt |
| E18 | **Gefahrstoffschränke**: Service-Nr. im Abschnitt („Gefahrstoffschrank Nr. 01 · Service-Nr. 106304“), kein Barcode | App kann nicht scannen; Inhalt nur aus PDF (Unterformular nicht fotografiert) | UNSICHER bis Fotos da |
| E19 | „Kühlamellen“ → „Kühllamellen“, „Kältemschine“ → „Kältemaschine“, „::“ → „:“ | eindeutige Tippfehler | sicher |

## 4. Vor dem Bauen nötig (von Josias)

1. **Ansprechpartner** für E11: Rolle, Name/Firma, Telefon (Brandschutzbeauftragter, Haustechnik-Leitung o. ä.). Ohne Einträge zeigt das rote Fenster nur die allgemeinen Kontakte.
2. **Zugangscode-Wert** Kältemaschine 1 (trägst du selbst im Builder unter 🔑 Zugangscodes ein – ich lege nur den Eintrag mit Platzhalter an oder du legst ihn an).
3. Optional: **Grenzwerte** aus E9 bestätigen/ändern (sonst bleiben die geratenen Plausibilitätsbereiche, die nie sperren).
4. Optional: Fotos vom Unterformular **Gefahrstoffschränke** (Q-ALL-6), um E18 zu belegen.

## 5. Bauweg (danach)

1. SharePoint-Skript (Konsole) legt je Rundgang Rundgang → Bereich(e) → Kategorien → Prüfpunkte, Plan, Kopfdaten, „Testrundgang = Ja“ an – genau nach `PLAN_RUNDGAENGE.csv` (wie beim Funktionsrundgang). Vorher: Zugangscode-Eintrag und Ansprechpartner.
2. Im Builder je Rundgang öffnen → Prüfung „keine Fehler“ → ansehen.
3. In Rundgang DEV je Rundgang einen Testlauf.

## 6. Tabellen je Rundgang

Spalten: **Nr** = Nummer aus der Bildanalyse (Quelle/Bilder dort nachschlagen) · **Typ/Pflicht/Einheit/ab/bis/außerhalb** wie im Builder · **Hinweis** = „Hinweis für den Prüfer“ · **Extras** = Rückfrage, kritisch, nicht messbar, nur steigend, 🔑 · Foto immer „kein Foto (bei n.i.O. möglich)“, Kommentar immer „Pflicht bei Mangel“ (siehe §2).

## Infrastrukturrundgang TGI MMS

- **Plan:** Mo, Mi, Fr – jede Woche
- **Bereich-Überschrift:** sichtbar (Batterieraum, Infrastrukturraum, Produktionshalle, Büro 1. OG)
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Batterieraum › Batterieraum (1) · Infrastrukturraum › Heizung und Kompressoren (15) · Infrastrukturraum › Kältetrockner und Wasseraufbereitung (6) · Infrastrukturraum › ONI Kühlanlage (8) · Infrastrukturraum › Kältemaschinen (15) · Produktionshalle › Produktionshalle – Räume und Klima (9) · Produktionshalle › Produktionshalle – Zähler, Tore, Technik (21) · Büro 1. OG › Serverraum (2)


### Batterieraum › Batterieraum

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | Kontrolle ob Störungsfrei | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise ist die Anlage störungsfrei.“ | neu: Rückfrage |

### Infrastrukturraum › Heizung und Kompressoren

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 |  | Sichtprüfung Heizungsanlage | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 3 |  | Zählerstand Wasseruhr | Zahl | Ja | m³ |  |  |  |  | nur steigend | neu: nur steigend |
| 4 |  | Druckmanometer Heizung (schwarz, 1,5 bis 2,0 bar) | Zahl | Ja | bar | 1,5 | 2,0 | Mangel |  |  |  |
| 5 | Kompressor 3 | Betriebsdruck | Zahl | Ja | bar | 4 | 13 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 6 | Kompressor 3 | Betriebsstunden | Zahl | Ja | h |  |  |  |  | nur steigend | neu: nur steigend |
| 7 | Kompressor 3 | Temperatur | Zahl | Ja | °C | 0 | 110 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 8 | Kompressor 3 | Kontrolle Druckluftfilter (Störungsfrei) | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise ist die Anlage störungsfrei.“ | neu: Rückfrage |
| 9 | Kompressor 2 | Betriebsdruck | Zahl | Ja | bar | 4 | 13 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 10 | Kompressor 2 | Betriebsstunden | Zahl | Ja | h |  |  |  |  | nur steigend | neu: nur steigend |
| 11 | Kompressor 2 | Temperatur | Zahl | Ja | °C | 0 | 110 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 12 | Kompressor 2 | Kontrolle Druckluftfilter (Störungsfrei) | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise ist die Anlage störungsfrei.“ | neu: Rückfrage |
| 13 | Kompressor 1 | Betriebsdruck | Zahl | Ja | bar | 4 | 13 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 14 | Kompressor 1 | Betriebsstunden | Zahl | Ja | h |  |  |  |  | nur steigend | neu: nur steigend |
| 15 | Kompressor 1 | Temperatur | Zahl | Ja | °C | 0 | 110 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 16 | Kompressor 1 | Kontrolle Druckluftfilter (Störungsfrei) | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise ist die Anlage störungsfrei.“ | neu: Rückfrage |

### Infrastrukturraum › Kältetrockner und Wasseraufbereitung

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 17 | Kältetrockner 1 | Sichtprüfung Betriebszustand (im Grünen Bereich) | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise steht die Anzeige im grünen Bereich.“ | neu: Rückfrage |
| 18 | Kältetrockner 2 | Sichtprüfung Betriebszustand (im Grünen Bereich) | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise steht die Anzeige im grünen Bereich.“ | neu: Rückfrage |
| 19 | Wasseraufbereitung (Jansen) | Kontrolle Vorrat Biozid | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 20 | Wasseraufbereitung (Jansen) | Kontrolle Vorrat Korrosionsschutz | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 21 | Wasseraufbereitung (Jansen) | Kontrolle Wasseraufbereitung (Störungsfrei) | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise ist die Anlage störungsfrei.“ | neu: Rückfrage |
| 22 | Öwamat | Kontrolle Wasserqualität Öwamat (mit Teststreifen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Infrastrukturraum › ONI Kühlanlage

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 23 | ONI Kühlanlage | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 24 | ONI Kühlanlage | Druck Heizungspumpe (WR6) PCC71 (min. 2,0 bar) | Zahl | Ja | bar | 2,0 |  | Mangel |  |  |  |
| 25 | ONI Kühlanlage | Kontrolle Siebkorbfilter 1 (ab 0,5 bar Reinigung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 26 | ONI Kühlanlage | Kontrolle Siebkorbfilter 2 (ab 0,5 bar Reinigung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 27 | ONI Kühlanlage | Kontrolle Verschmutzung Pumpen (Lüfterräder) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 28 | ONI Kühlanlage | Kontrolle Schrägsitzfilter | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 29 | ONI Kühlanlage | Kontrolle Luftfilter Schaltschrank | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 30 | ONI Kühlanlage | Zählerstand Wasseruhr über Tank | Zahl | Ja | m³ |  |  |  |  | nur steigend | neu: nur steigend |

### Infrastrukturraum › Kältemaschinen

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Kontrolle Kühllamellen | i.O./n.i.O. | Ja |  |  |  |  |  |  | Tippfehler „Kühlamellen“ → „Kühllamellen“; Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“ |
| 32 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Wassertemperatur (Ausgang) | Zahl | Ja | °C | 0 | 30 | Hinweis + Grund |  | 🔑 Zugangscode „Bedienteil Kältemaschine 1“ (Wert trägt Josias ein) | Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“; neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 33 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Betriebsstunden C1 | Zahl | Ja | h |  |  |  |  | nur steigend<br>🔑 Zugangscode „Bedienteil Kältemaschine 1“ (Wert trägt Josias ein) | Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“; neu: nur steigend |
| 34 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Betriebsstunden C2 | Zahl | Ja | h |  |  |  |  | nur steigend<br>🔑 Zugangscode „Bedienteil Kältemaschine 1“ (Wert trägt Josias ein) | Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“; neu: nur steigend |
| 35 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Kontrolle Störungsanzeige | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise ist die Anlage störungsfrei.“ | Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“; neu: Rückfrage |
| 36 | Kältemaschine 2 (Außenbereich) | Kontrolle Kühllamellen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 37 | Kältemaschine 2 (Außenbereich) | Wassertemperatur (Ausgang) | Zahl | Ja | °C | 0 | 30 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 38 | Kältemaschine 2 (Außenbereich) | Betriebsstunden A1 | Zahl | Ja | h |  |  |  |  | nur steigend | neu: nur steigend |
| 39 | Kältemaschine 2 (Außenbereich) | Betriebsstunden B1/ C1 | Zahl | Ja | h |  |  |  |  | nur steigend | neu: nur steigend |
| 40 | Kältemaschine 2 (Außenbereich) | Kontrolle Störungsanzeige | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise ist die Anlage störungsfrei.“ | neu: Rückfrage |
| 41 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Kontrolle Kühllamellen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 42 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Wassertemperatur (Ausgang) | Zahl | Ja | °C | 0 | 30 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 43 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Betriebsstunden A1 | Zahl | Ja | h |  |  |  |  | nur steigend | neu: nur steigend |
| 44 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Betriebsstunden B1/ C1 | Zahl | Ja | h |  |  |  |  | nur steigend | neu: nur steigend |
| 45 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Kontrolle Störungsanzeige | i.O./n.i.O. | Ja |  |  |  |  |  | Rückfrage: „Normalerweise ist die Anlage störungsfrei.“ | neu: Rückfrage |

### Produktionshalle › Produktionshalle – Räume und Klima

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 46 |  | Sichtprüfung Tor 1 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 47 | WZB | Sichtprüfung Aktivkohlefilter / Gefahrstoffschränke | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 48 | Regalanlagen | Sichtprüfung Regalanlagen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 49 | Haftungskabine | Temperatur Klimaanlage (Sollzustand 21,0 °C - 25,0 °C) | Zahl | Ja | °C | 21,0 | 25,0 | Mangel |  | nicht messbar erlaubt | neu: nicht messbar erlaubt |
| 50 | Analysebüro | Sichtprüfung Stickstoffflasche | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 51 | Analysebüro | Füllung Stickstoffflasche | Zahl | Nein | bar | 0 | 300 | Hinweis + Grund | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | neu: Plausibilitätsgrenze (Hinweis + Grund); freiwillig statt Pflicht (nur Mo nötig) |
| 52 | Analysebüro | Temperatur Klimaanlage | Zahl | Ja | °C | 10 | 35 | Hinweis + Grund |  |  | neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 53 | Messraum | Temperatur Klimaanlage (Sollzustand 19,0 °C - 24,0 °C) | Zahl | Ja | °C | 19,0 | 24,0 | Mangel |  |  |  |
| 54 | Wareneingangsbüro | Temperatur Klimaanlage | Zahl | Ja | °C | 10 | 35 | Hinweis + Grund |  | nicht messbar erlaubt | neu: nicht messbar erlaubt; neu: Plausibilitätsgrenze (Hinweis + Grund) |

### Produktionshalle › Produktionshalle – Zähler, Tore, Technik

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 55 | Allgemein | Zählerstand Gaszähler S1 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. | nur steigend | neu: nur steigend; freiwillig statt Pflicht (nur Mo nötig) |
| 56 | Allgemein | Zählerstand Gaszähler S2 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. | nur steigend<br>nicht messbar erlaubt | neu: nur steigend; neu: nicht messbar erlaubt; freiwillig statt Pflicht (nur Mo nötig) |
| 57 | Allgemein | Zählerstand Gaszähler S3 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. | nur steigend | neu: nur steigend; freiwillig statt Pflicht (nur Mo nötig) |
| 58 | Allgemein | Zählerstand Gaszähler S4 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. | nur steigend | neu: nur steigend; freiwillig statt Pflicht (nur Mo nötig) |
| 59 | Allgemein | Zählerstand Gaszähler S5 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. | nur steigend | neu: nur steigend; freiwillig statt Pflicht (nur Mo nötig) |
| 60 | Allgemein | Zählerstand Gaszähler S6 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. | nur steigend | neu: nur steigend; freiwillig statt Pflicht (nur Mo nötig) |
| 61 | Allgemein | Zählerstand Gaszähler S7 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. | nur steigend | neu: nur steigend; freiwillig statt Pflicht (nur Mo nötig) |
| 62 | Allgemein | Zählerstand Gaszähler S8 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. | nur steigend<br>nicht messbar erlaubt | neu: nur steigend; neu: nicht messbar erlaubt; freiwillig statt Pflicht (nur Mo nötig) |
| 63 | Allgemein | Sichtprüfung Tor 2 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 64 | Allgemein | Sichtprüfung Tor 3 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 65 | Allgemein | Sichtprüfung Tor 4 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 66 | Allgemein | Sichtprüfung Tor 5 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 67 | Warenausgangsbüro | Temperatur Klimaanlage | Zahl | Ja | °C | 10 | 35 | Hinweis + Grund |  | nicht messbar erlaubt | neu: nicht messbar erlaubt; neu: Plausibilitätsgrenze (Hinweis + Grund) |
| 68 | Allgemein | Sichtprüfung Tor 6 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 69 | Allgemein | cos φ Wert Kompensationsanlage (Normalbereich cos φ > 0,90) | Zahl | Ja | cos φ | 0,90 |  | Mangel |  |  |  |
| 70 | Allgemein | Sichtprüfung Filtervlies Kompensationsanlage (Reinigung nur durch eingewiesenes Fachpersonal) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 71 | Allgemein | Zählerstand Hauptverteilung 1 | Zahl | Ja | kWh |  |  |  |  | nur steigend | neu: nur steigend |
| 72 | Allgemein | Zählerstand Hauptverteilung 2 | Zahl | Ja | kWh |  |  |  |  | nur steigend | neu: nur steigend |
| 73 | Allgemein | Zählerstand Hauptverteilung 3 | Zahl | Ja | kWh |  |  |  |  | nur steigend | neu: nur steigend |
| 74 | Allgemein | Zählerstand Hauptverteilung 4 | Zahl | Ja | kWh |  |  |  |  | nur steigend | neu: nur steigend |
| 75 | Allgemein | Sichtprüfung Elektronische Dachfenstersteuerung/ Lichtschalter | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Büro 1. OG › Serverraum

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 76 |  | Temperatur Serverraum (Sollzustand 18,0 °C - 21,0 °C) | Zahl | Ja | °C | 18,0 | 21,0 | Mangel |  |  |  |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |

## Brandschutzrundgang TGI MMS

- **Plan:** Mo–Fr – jede Woche
- **Bereich-Überschrift:** ausgeblendet
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Brandschutz › Brandmeldezentrale (BMZ) (1) · Brandschutz › Infrastrukturraum / Produktionshalle (3) · Brandschutz › Produktionshalle – Sanitär, Außenbereich, Büros (13) · Brandschutz › Produktionshalle – Hallenbereich und Tore (16) · Brandschutz › Brandschutz allgemein (13)


### Brandschutz › Brandmeldezentrale (BMZ)

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | Sichtprüfung ob frei zugänglich, ÜE eingeschaltet | i.O./n.i.O. | Ja |  |  |  |  |  | KRITISCH: „Brandmeldezentrale nicht zugänglich oder Übertragung zur Feuerwehr aus – sofort melden.“ Ansprechpartner: Brandschutzbeauftragter, Haustechnik-Leitung (Einträge noch anlegen) | neu: kritisch |

### Brandschutz › Infrastrukturraum / Produktionshalle

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 |  | Sichtprüfung Feuerlöscher | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 3 |  | Druckgasflaschen und Behälter für brennbare Flüssigkeiten an den vorgeschriebenen Orten | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 4 |  | Brennbare Abfälle und selbstentzündliche Stoffe (Späne, Verpackung, Lappen, etc.) vorschriftsmäßig aufbewahrt | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Brandschutz › Produktionshalle – Sanitär, Außenbereich, Büros

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | Sanitärräume (Herren WC) | Kontrolle Ordnung und Sauberkeit Herren WC | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 6 | Sanitärräume (Herren WC) | Kontrolle Füllstand Seifenspender Herren WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 7 | Sanitärräume (Herren WC) | Kontrolle Füllstand Handtuchpapierspender Herren WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 8 | Sanitärräume (Damen WC) | Kontrolle Ordnung und Sauberkeit Damen WC | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 9 | Sanitärräume (Damen WC) | Kontrolle Füllstand Seifenspender Damen WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  | Tippfehler „::“ → „:“ |
| 10 | Sanitärräume (Damen WC) | Kontrolle Füllstand Handtuchpapierspender Damen WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 11 | Sanitärräume (Damen WC) | Kontrolle Temperatur aller Durchlauferhitzer (mind. 60 °C) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 12 | Außenbereich | Kontrolle Ordnung und Sauberkeit (Wareneingang) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 13 | Außenbereich | Kontrolle Aschenbecher/ Beleuchtung (Wareneingang) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 14 | Außenbereich | Kontrolle der Wartungsaufkleber an allen Abfallcontainern immer bei Austausch: Presscontainer nach UVV freigeprüft, Container/Mulden nach BGR186 freigeprüft | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 15 | Außenbereich | Kontrolle der Sicherung gegen Einschalten der Selbstpresscontainer (Schlüssel (w.v.) abgezogen, Not-Aus-Schalter gedrückt) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 16 | WZB | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 17 | Analysebüro | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Brandschutz › Produktionshalle – Hallenbereich und Tore

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 18 | Allgemein | Sichtprüfung Regal-Liftsystem | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 19 | Allgemein | Sichtprüfung Hochregale | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 20 | Allgemein | Kontrolle destilliertes Wasser (Staplerstation) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 21 | Allgemein | Kontrolle allgemeine Deckenbeleuchtung | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 22 | Allgemein | Kontrolle Erste-Hilfe-Kästen / Pflasterboxen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 23 | Allgemein | Kontrolle Gehörschutzboxen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 24 | Außenbereich | Kontrolle Aschenbecher/ Beleuchtung (Tor 2) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 25 | Außenbereich | Kontrolle Ordnung und Sauberkeit (Containerbereich) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 26 | Außenbereich | Kontrolle Beleuchtung (Tor 3) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 27 | Außenbereich | Kontrolle Beleuchtung (Tor 4) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 28 | Außenbereich | Kontrolle Aschenbecher/ Beleuchtung (Tor 5) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 29 | Außenbereich | Kontrolle Beleuchtung (Tor 6) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 30 | Außenbereich | Kontrolle Ordnung und Sauberkeit (Warenausgang) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 31 | Konfektion | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 32 | Messstation | Kontrolle Funktion Staubsauger | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 33 | Küchenbereich | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Brandschutz › Brandschutz allgemein

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 34 |  | Feuerschutzabschlüsse (BS-Türen, BS-Tore) geschlossen, bzw. ordnungsgemäß aufgestellt, nicht blockiert, nicht beschädigt und leichtgängig | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 35 |  | Feuerlöscheinrichtungen zugänglich | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 36 |  | Lagergut und Abfall im Abstand von den Außenwänden abgestellt (5 m) | i.O./n.i.O. | Ja |  |  |  |  | Aufgrund der baulichen Gegebenheiten kann die 5 Meter Vorgabe nicht eingehalten werden. |  | Satz 2 als Hinweis statt im Fragetext |
| 37 |  | Druckgasflaschen und Behälter für brennbare Flüssigkeiten an den vorgeschriebenen Orten | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 38 |  | Brennbare Abfälle und selbstentzündliche Stoffe (Späne, Verpackungen, Lappen, etc.) vorschriftsmäßig aufbewahrt | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 39 |  | Fluchtwege frei begehbar, Sicherheitsflächen frei | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 40 |  | Zufahrt, Aufstell- und Begehungsflächen für die Feuerwehr frei | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 41 |  | Ausreichende Sicherheitsabstände zwischen brennbaren Stoffen und Zündquellen, wie Öfen, Feuerungen, Wärmestrahlern, Gabelstaplerladestationen, Trockenanlagen und sonstigen aufgeheizten Einrichtungen vorhanden | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 42 |  | Kontrolle ob das Rauchverbot entsprechend eingehalten wird | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 43 |  | Keine brennenden Kerzen, brennbare Dekorationen, Heiz-, oder Elektrogeräte vorhanden - ggf. entfernen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 44 |  | Keine Verschmutzungen hinter und unter Brandschutztüren/ -toren | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 45 |  | Serverraum (keine Brandlasten vorhanden, ggf. entfernen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |

## Haustechnikrundgang TGI MMS

- **Plan:** Mo – jede Woche
- **Bereich-Überschrift:** ausgeblendet
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Haustechnik › Grünflächen, Parkplätze (vor Bürogebäude) (7) · Haustechnik › Eingangsbereich/ Treppenhaus (6) · Haustechnik › Infrastrukturraum (6) · Haustechnik › Büro EG (9) · Haustechnik › Büro 1. OG (9) · Haustechnik › Büro 1. OG – Küche und Besucher-WCs (8) · Haustechnik › Sozialräume (15) · Haustechnik › Trinkwasser und Reinigung (11) · Haustechnik › Sammelstation für Altöl und Gefahrstoffe (5)


### Haustechnik › Grünflächen, Parkplätze (vor Bürogebäude)

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 2 |  | Kontrolle Toreinfahrt | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 3 |  | Sichtprüfung Feuerwehrtresor | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 4 |  | Sichtprüfung Gegensprechanlage | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 5 |  | Kontrolle Torausfahrt | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 6 |  | Reinigung Straßeneinläufe | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 7 |  | Reinigung Straßeneinlaufrinnen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnik › Eingangsbereich/ Treppenhaus

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 |  | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 9 |  | Sichtprüfung Beleuchtung, elektrische Bauteile (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 10 |  | Sichtprüfung Türen, Fenster (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 11 |  | Sichtprüfung Wände, Decken, Böden (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 12 |  | Sichtprüfung Inventar, Büromöbel, etc. (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 13 |  | Sichtprüfung Heizung, Lüftung, Klima (Beschädigung, Verschmutzung, Wartung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnik › Infrastrukturraum

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 |  | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 15 |  | Sichtprüfung Beleuchtung, elektrische Bauteile (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 16 |  | Sichtprüfung Türen, Fenster (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 17 |  | Sichtprüfung Wände, Decken, Böden (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 18 |  | Sichtprüfung Inventar, Büromöbel, etc. (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 19 |  | Sichtprüfung Heizung, Lüftung, Klima (Beschädigung, Verschmutzung, Wartung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnik › Büro EG

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 |  | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 21 |  | Sichtprüfung Beleuchtung, elektrische Bauteile (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 22 |  | Sichtprüfung Türen, Fenster, Sonnenschutz (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 23 |  | Sichtprüfung Wände, Decken, Böden (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 24 |  | Sichtprüfung Inventar, Büromöbel, etc. (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 25 |  | Sichtprüfung Heizung, Lüftung, Klima (Beschädigung, Verschmutzung, Wartung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 26 |  | Kontrolle Kopierpapier (min. 1 Karton) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 27 |  | Kontrolle Reinigungsstand | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 28 |  | Sichtprüfung Leerung der Mülleimer | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnik › Büro 1. OG

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 29 | Allgemein | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 30 | Allgemein | Sichtprüfung Beleuchtung, elektrische Bauteile (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 31 | Allgemein | Sichtprüfung Türen, Fenster, Sonnenschutz (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 32 | Allgemein | Sichtprüfung Wände, Decken, Böden (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 33 | Allgemein | Sichtprüfung Inventar, Büromöbel, etc. (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 34 | Allgemein | Sichtprüfung Heizung, Lüftung, Klima (Beschädigung, Verschmutzung, Wartung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 35 | Allgemein | Kontrolle Kopierpapier (min. 1 Karton) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 36 | Allgemein | Kontrolle Reinigungsstand | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 37 | Allgemein | Sichtprüfung Leerung der Mülleimer | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnik › Büro 1. OG – Küche und Besucher-WCs

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 38 | Küchenbereich | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 39 | Besuchertoiletten (Herren WC) | Kontrolle Ordnung und Sauberkeit Herren WC | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 40 | Besuchertoiletten (Herren WC) | Kontrolle Füllstand Seifenspender Herren WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 41 | Besuchertoiletten (Herren WC) | Kontrolle Füllstand Handtuchpapierspender Herren WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 42 | Besuchertoiletten (Herren WC) | Kontrolle Temperatur aller Durchlauferhitzer (mind. 60 °C) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 43 | Besuchertoiletten (Damen WC) | Kontrolle Ordnung und Sauberkeit Damen WC | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 44 | Besuchertoiletten (Damen WC) | Kontrolle Füllstand Seifenspender Damen WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  | Tippfehler „::“ → „:“ |
| 45 | Besuchertoiletten (Damen WC) | Kontrolle Füllstand Handtuchpapierspender Damen WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnik › Sozialräume

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 46 | Allgemein | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 47 | Allgemein | Sichtprüfung Beleuchtung, elektrische Bauteile (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 48 | Allgemein | Sichtprüfung Türen, Fenster (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 49 | Allgemein | Sichtprüfung Wände, Decken, Böden (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 50 | Allgemein | Sichtprüfung Inventar, Büromöbel, etc. (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 51 | Allgemein | Sichtprüfung Heizung, Lüftung, Klima (Beschädigung, Verschmutzung, Wartung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 52 | Herren WC | Kontrolle Ordnung und Sauberkeit Herren WC | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 53 | Herren WC | Kontrolle Füllstand Seifenspender Herren WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  | Tippfehler „::“ → „:“ |
| 54 | Herren WC | Kontrolle Füllstand Handtuchpapierspender Herren WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 55 | Herren WC | Kontrolle Temperatur aller Durchlauferhitzer (mind. 60 °C) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 56 | Damen WC | Kontrolle Ordnung und Sauberkeit Damen WC | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 57 | Damen WC | Kontrolle Füllstand Seifenspender Damen WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 58 | Damen WC | Kontrolle Füllstand Handtuchpapierspender Damen WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 59 | Damen WC | Kontrolle Temperatur aller Durchlauferhitzer (mind. 60 °C) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 60 | Damen WC | Kontrolle Abluftanlage | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnik › Trinkwasser und Reinigung

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 61 | Spülen der Trinkwasserleitungen | EG Behinderten WC HWB | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 62 | Spülen der Trinkwasserleitungen | EG Halle Damen WC HWB | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 63 | Spülen der Trinkwasserleitungen | EG Halle Herren WC HWB | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 64 | Spülen der Trinkwasserleitungen | EG Küche Spüle | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 65 | Spülen der Trinkwasserleitungen | 1. OG Damen WC HWB rechts | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 66 | Spülen der Trinkwasserleitungen | 1. OG Besucher WC HWB | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 67 | Spülen der Trinkwasserleitungen | 1. OG Herren Dusche links Mischarmatur (Einfluss des Duschschlauchs) | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 68 | Spülen der Trinkwasserleitungen | 1. OG Herren Dusche 4. HWB von links | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 69 | Spülen der Trinkwasserleitungen | 1. OG Herren WC HWB rechts | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 70 | Spülen der Trinkwasserleitungen | 1. OG Küche Spüle | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | ca. 1–2 Minuten pro Entnahmestelle spülen. |  | Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.; Zeitangabe aus Abschnitt als Hinweis |
| 71 | Reinigung | Rücksprache mit Kunde, ob Reinigungszustand zufriedenstellend | i.O./n.i.O. („zufriedenstellend“ / „nicht zufrieden“) | Ja |  |  |  |  | Wenn nicht: im Kommentar näher dokumentieren (wird als Mangel erfasst). |  | eigener Abschnitt „Reinigung“; Knöpfe „zufriedenstellend / nicht zufrieden“; Klammertext als Hinweis |

### Haustechnik › Sammelstation für Altöl und Gefahrstoffe

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 72 |  | Sichtkontrolle der Auffangwannen/ Auffangtassen nach AwSV | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 73 |  | Kontrolle der Beschaffenheit auf Dichtheit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 74 |  | Kontrolle der Beschaffenheit auf Standfestigkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 75 |  | Kontrolle der Beschaffenheit auf Verschmutzung | i.O./n.i.O. | Ja |  |  |  |  | Verschmutzungen sofort entfernen lassen! |  | Klammer-Anweisung als Hinweis |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |

## Legionellen Prävention TGI MMS

- **Plan:** Mo – jede Woche (MoreApp: Mittwoch, s. E3)
- **Bereich-Überschrift:** ausgeblendet
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Legionellen › Legionellen Prävention (3)


### Legionellen › Legionellen Prävention

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | 1. OG Damenumkleide Dusche | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | 10 Minuten Wasser mit mind. 60 °C durchlaufen lassen. |  | Klammer-Anweisung als Hinweis |
| 2 |  | 1. OG Damenumkleide HWB links | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  | 10 Minuten Wasser mit mind. 60 °C durchlaufen lassen. |  | Klammer-Anweisung als Hinweis |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |

## Sichtprüfung Gefahrstoffschränke TGI MMS

- **Plan:** Mo – jede Woche (MoreApp: Mittwoch, s. E3)
- **Bereich-Überschrift:** ausgeblendet
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Gefahrstoffschränke › Gefahrstoffschränke (7)


### Gefahrstoffschränke › Gefahrstoffschränke

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Gefahrstoffschrank Nr. 01 · Service-Nr. 106304 | Sichtprüfung Außen (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 2 | Gefahrstoffschrank Nr. 01 · Service-Nr. 106304 | Sichtprüfung Innen (beschädigte Gefäße, Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 3 | Gefahrstoffschrank Nr. 02 · Service-Nr. 106303 | Sichtprüfung Außen (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 4 | Gefahrstoffschrank Nr. 02 · Service-Nr. 106303 | Sichtprüfung Innen (beschädigte Gefäße, Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 5 | Gefahrstoffschrank Nr. 03 · Service-Nr. 106305 | Sichtprüfung Außen (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 6 | Gefahrstoffschrank Nr. 03 · Service-Nr. 106305 | Sichtprüfung Innen (beschädigte Gefäße, Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |
