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

