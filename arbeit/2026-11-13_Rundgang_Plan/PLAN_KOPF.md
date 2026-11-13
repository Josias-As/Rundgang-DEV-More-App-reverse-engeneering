# Bauplan der echten Rundgänge (Stand 13.11.2026, Fassung „am Original“)

Erstellt vom Einsetz-Chat als **Denkschritt vor dem Bauen**. Grundlage: Bildanalyse `arbeit/2026-11-10_Bildanalyse/` (133 Screenshots Mo/Di/Mi + 4 PDFs). Noch **nichts** davon ist in SharePoint angelegt.

- **Josias' Vorgaben (13.11.):** „alles so gut es geht am Original“ · Ansprechpartner und Schlüssel (Zugangscode) erstmal überall **Platzhalter** · aktuelles Konzept (5 Rundgänge nach Intervall), späterer Umbau auf Wochentags-Rundgänge möglich · alles dokumentieren · Liste der Punkte, die mit den Verantwortlichen zu besprechen sind → `BESPRECHUNG.md`.
- **Maschinenlesbar:** `PLAN_RUNDGAENGE.csv` (eine Zeile je Prüfpunkt, alle Einstellungen, Begründung, Quelle), erzeugt mit `plan_erzeugen.js` (`ORIGINAL = true`). Die zuerst geplante Variante „mit Zusätzen“ (Rückfragen, Plausibilitätsgrenzen, „nur steigend“, „nicht messbar“, Seiten-Aufteilung, „durchgeführt“-Knöpfe …) steckt im Skript (`ORIGINAL = false`) und steht als Vorschlagsliste in `BESPRECHUNG.md` Teil C.
- **Kennzeichnung:** Spalte „Änderung ggü. MoreApp“ – leer = genau wie MoreApp.

## 1. Überblick

| Rundgang | Plan | Prüfpunkte | Seiten (= MoreApp-Unterformulare) |
|---|---|---|---|
| Infrastrukturrundgang TGI MMS | Mo, Mi, Fr | 76 + Bemerkungen | 4: Batterieraum (1) · Infrastrukturraum (44) · Produktionshalle (30) · Büro 1. OG (1 + Bemerkungen) |
| Brandschutzrundgang TGI MMS | Mo–Fr | 45 + Bemerkungen | 4: Brandmeldezentrale (BMZ) (1) · Infrastrukturraum/ Produktionshalle (3) · Produktionshalle (29) · Brandschutz (12 + Bemerkungen) |
| Haustechnikrundgang TGI MMS | Mo | 75 + Bemerkungen | 8: Grünflächen, Parkplätze (7) · Eingangsbereich/ Treppenhaus (6) · Infrastrukturraum (6) · Büro EG (9) · Büro 1. OG (17) · Sozialräume (15) · Allgemein (11) · Sammelstation (4 + Bemerkungen) |
| Legionellen Prävention TGI MMS | Mo (MoreApp: Mi) | 2 + Bemerkungen | 1 |
| Sichtprüfung Gefahrstoffschränke TGI MMS | Mo (MoreApp: Mi) | 6 + Bemerkungen | 1 |

Alle Rundgänge: ein Bereich, **Überschrift ausgeblendet** (MoreApp hat keine Ebene über den Unterformularen) · **Testrundgang = Ja** bis zur Inbetriebnahme · Kopfdaten Standort „TGI MMS“, Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“, Auftraggeber „Technoform Glass Insulation GmbH“ (aus dem PDF-Kopf).

## 2. Einstellungen je Prüfpunkt (wenn in der Tabelle nichts anderes steht)

| Einstellung | Wert | Herkunft |
|---|---|---|
| Typ | i.O./n.i.O. bzw. Zahl/Text wie MoreApp | belegt |
| Antwort | Pflicht | Stern in MoreApp (belegt) |
| Kommentar | Pflicht bei Mangel | = MoreApp-Feld „Mangelbeschreibung*“ je Unterformular |
| Foto | kein Foto (bei n.i.O. möglich) | in MoreApp kein Foto-Feld zu sehen |
| Grenzen | nur wo MoreApp sie nennt (Heizung 1,5–2,0 bar, Heizungspumpe min. 2,0 bar, Klima Haftungskabine 21–25 °C, Messraum 19–24 °C, Serverraum 18–21 °C, cos φ > 0,90), außerhalb = Mangel | belegt im Fragetext / rote Meldung |
| Knopf-Wörter | i.O./n.i.O.; Legionellen „durchgeführt / nicht durchgeführt“ | belegt |
| Abschnitte | wie die grauen Balken in MoreApp (Kompressor 1–3, Kältemaschine 1–3, Herren/Damen WC …) | belegt |
| Fragetext | wörtlich, nur der Doppelpunkt am Ende entfällt und eindeutige Tippfehler sind korrigiert („Kältemschine“, „Kühlamellen“, „::“) | Formatierung |

## 3. Die einzigen Abweichungen vom Original

| # | Abweichung | Warum |
|---|---|---|
| A1 | Gaszähler S1–S8 und „Füllung Stickstoffflasche“ (Infrastruktur) **freiwillig** + Hinweis „Nur montags ablesen“ | MoreApp blendet sie außer montags aus; unsere App kann nicht nach Wochentag ausblenden. So bleiben sie drin. |
| A2 | 🔑 Zugangscode **„PLATZHALTER Bedienteil Kältemaschine 1“** an Wassertemperatur, Betriebsstunden C1/C2 | MoreApp zeigt den Code offen (belegt); bei uns hinter 🔑. Code-Wert fehlt noch. |
| A3 | Brandmeldezentrale: **kritisch** mit Ansprechpartner **„PLATZHALTER Ansprechpartner BMZ“** | Josias: Ansprechpartner als Platzhalter. In MoreApp nicht vorhanden → Besprechungspunkt B1. Ohne Freigabe einfach „kritisch“ wieder aus. |
| A4 | „Bemerkungen“ (Text, freiwillig) als letzte Frage jedes Rundgangs | MoreApp hat „Bemerkungen:“ am Formularende (belegt) |
| A5 | Zuordnung der Unterformulare zu den 5 Rundgängen; BMZ und Produktionshalle zum Brandschutz | MoreApp ist **ein** Formular nach Wochentag (belegt); Zuordnung BMZ/Produktionshalle geschlussfolgert → B2 |
| A6 | Legionellen und Gefahrstoffschränke laufen **montags** | Josias' Intervall-Liste; MoreApp: Mittwoch → B3 |

## 4. Vor dem Bauen anzulegen (mit Platzhaltern)

1. RG_Zugangscodes: Eintrag „PLATZHALTER Bedienteil Kältemaschine 1“, Code „0000“, Hinweis „Platzhalter – echten Code eintragen“.
2. RG_Ansprechpartner: Eintrag Rolle „PLATZHALTER Ansprechpartner BMZ“, Kontakt „noch offen“, Telefon leer, Hinweis „Platzhalter – mit Verantwortlichen klären“.

## 5. Bauweg

1. SharePoint-Skript legt Platzhalter, Rundgänge, Bereich, Kategorien, Prüfpunkte, Plan, Kopfdaten, „Testrundgang = Ja“ an – genau nach `PLAN_RUNDGAENGE.csv`.
2. Builder: je Rundgang Prüfung „keine Fehler“ (Hinweis „über 30 Prüfpunkte“ bei Infrastrukturraum ist erwartet).
3. Rundgang DEV: je Rundgang ein Testlauf.

## 6. Tabellen je Rundgang

Spalten wie im Builder. **Nr** = Nummer aus der Bildanalyse (Bilder/Quelle dort). Foto immer „kein Foto (bei n.i.O. möglich)“, Kommentar immer „Pflicht bei Mangel“.

