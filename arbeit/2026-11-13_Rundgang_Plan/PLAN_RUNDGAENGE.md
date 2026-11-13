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

## Infrastrukturrundgang TGI MMS

- **Plan:** Mo, Mi, Fr – jede Woche
- **Bereich-Überschrift:** ausgeblendet
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Infrastrukturrundgang TGI MMS › Batterieraum (1) · Infrastrukturrundgang TGI MMS › Infrastrukturraum (44) · Infrastrukturrundgang TGI MMS › Produktionshalle (30) · Infrastrukturrundgang TGI MMS › Büro 1. OG (2)


### Infrastrukturrundgang TGI MMS › Batterieraum

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | Kontrolle ob Störungsfrei | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Infrastrukturrundgang TGI MMS › Infrastrukturraum

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 |  | Sichtprüfung Heizungsanlage | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 3 |  | Zählerstand Wasseruhr | Zahl | Ja | m³ |  |  |  |  |  |  |
| 4 |  | Druckmanometer Heizung (schwarz, 1,5 bis 2,0 bar) | Zahl | Ja | bar | 1,5 | 2,0 | Mangel |  |  |  |
| 5 | Kompressor 3 | Betriebsdruck | Zahl | Ja | bar |  |  |  |  |  |  |
| 6 | Kompressor 3 | Betriebsstunden | Zahl | Ja | h |  |  |  |  |  |  |
| 7 | Kompressor 3 | Temperatur | Zahl | Ja | °C |  |  |  |  |  |  |
| 8 | Kompressor 3 | Kontrolle Druckluftfilter (Störungsfrei) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 9 | Kompressor 2 | Betriebsdruck | Zahl | Ja | bar |  |  |  |  |  |  |
| 10 | Kompressor 2 | Betriebsstunden | Zahl | Ja | h |  |  |  |  |  |  |
| 11 | Kompressor 2 | Temperatur | Zahl | Ja | °C |  |  |  |  |  |  |
| 12 | Kompressor 2 | Kontrolle Druckluftfilter (Störungsfrei) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 13 | Kompressor 1 | Betriebsdruck | Zahl | Ja | bar |  |  |  |  |  |  |
| 14 | Kompressor 1 | Betriebsstunden | Zahl | Ja | h |  |  |  |  |  |  |
| 15 | Kompressor 1 | Temperatur | Zahl | Ja | °C |  |  |  |  |  |  |
| 16 | Kompressor 1 | Kontrolle Druckluftfilter (Störungsfrei) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 17 | Kältetrockner 1 | Sichtprüfung Betriebszustand (im Grünen Bereich) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 18 | Kältetrockner 2 | Sichtprüfung Betriebszustand (im Grünen Bereich) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 19 | Wasseraufbereitung (Jansen) | Kontrolle Vorrat Biozid | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 20 | Wasseraufbereitung (Jansen) | Kontrolle Vorrat Korrosionsschutz | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 21 | Wasseraufbereitung (Jansen) | Kontrolle Wasseraufbereitung (Störungsfrei) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 22 | Öwamat | Kontrolle Wasserqualität Öwamat (mit Teststreifen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 23 | ONI Kühlanlage | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 24 | ONI Kühlanlage | Druck Heizungspumpe (WR6) PCC71 (min. 2,0 bar) | Zahl | Ja | bar | 2,0 |  | Mangel |  |  |  |
| 25 | ONI Kühlanlage | Kontrolle Siebkorbfilter 1 (ab 0,5 bar Reinigung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 26 | ONI Kühlanlage | Kontrolle Siebkorbfilter 2 (ab 0,5 bar Reinigung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 27 | ONI Kühlanlage | Kontrolle Verschmutzung Pumpen (Lüfterräder) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 28 | ONI Kühlanlage | Kontrolle Schrägsitzfilter | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 29 | ONI Kühlanlage | Kontrolle Luftfilter Schaltschrank | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 30 | ONI Kühlanlage | Zählerstand Wasseruhr über Tank | Zahl | Ja | m³ |  |  |  |  |  |  |
| 31 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Kontrolle Kühllamellen | i.O./n.i.O. | Ja |  |  |  |  |  |  | Tippfehler „Kühlamellen“ → „Kühllamellen“; Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“ |
| 32 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Wassertemperatur (Ausgang) | Zahl | Ja | °C |  |  |  |  | 🔑 Zugangscode „PLATZHALTER Bedienteil Kältemaschine 1“ (Code fehlt noch) | Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“ |
| 33 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Betriebsstunden C1 | Zahl | Ja | h |  |  |  |  | 🔑 Zugangscode „PLATZHALTER Bedienteil Kältemaschine 1“ (Code fehlt noch) | Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“ |
| 34 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Betriebsstunden C2 | Zahl | Ja | h |  |  |  |  | 🔑 Zugangscode „PLATZHALTER Bedienteil Kältemaschine 1“ (Code fehlt noch) | Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“ |
| 35 | Kältemaschine 1 (Außenbereich/ Display im Infrastrukturraum) | Kontrolle Störungsanzeige | i.O./n.i.O. | Ja |  |  |  |  |  |  | Abschnitt: Tippfehler „Kältemschine“ → „Kältemaschine“ |
| 36 | Kältemaschine 2 (Außenbereich) | Kontrolle Kühllamellen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 37 | Kältemaschine 2 (Außenbereich) | Wassertemperatur (Ausgang) | Zahl | Ja | °C |  |  |  |  |  |  |
| 38 | Kältemaschine 2 (Außenbereich) | Betriebsstunden A1 | Zahl | Ja | h |  |  |  |  |  |  |
| 39 | Kältemaschine 2 (Außenbereich) | Betriebsstunden B1/ C1 | Zahl | Ja | h |  |  |  |  |  |  |
| 40 | Kältemaschine 2 (Außenbereich) | Kontrolle Störungsanzeige | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 41 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Kontrolle Kühllamellen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 42 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Wassertemperatur (Ausgang) | Zahl | Ja | °C |  |  |  |  |  |  |
| 43 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Betriebsstunden A1 | Zahl | Ja | h |  |  |  |  |  |  |
| 44 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Betriebsstunden B1/ C1 | Zahl | Ja | h |  |  |  |  |  |  |
| 45 | Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum) | Kontrolle Störungsanzeige | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Infrastrukturrundgang TGI MMS › Produktionshalle

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 46 |  | Sichtprüfung Tor 1 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 47 | WZB | Sichtprüfung Aktivkohlefilter / Gefahrstoffschränke | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 48 | Regalanlagen | Sichtprüfung Regalanlagen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 49 | Haftungskabine | Temperatur Klimaanlage (Sollzustand 21,0 °C - 25,0 °C) | Zahl | Ja | °C | 21,0 | 25,0 | Mangel |  |  |  |
| 50 | Analysebüro | Sichtprüfung Stickstoffflasche | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 51 | Analysebüro | Füllung Stickstoffflasche | Zahl | Nein | bar |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 52 | Analysebüro | Temperatur Klimaanlage | Zahl | Ja | °C |  |  |  |  |  |  |
| 53 | Messraum | Temperatur Klimaanlage (Sollzustand 19,0 °C - 24,0 °C) | Zahl | Ja | °C | 19,0 | 24,0 | Mangel |  |  |  |
| 54 | Wareneingangsbüro | Temperatur Klimaanlage | Zahl | Ja | °C |  |  |  |  |  |  |
| 55 | Allgemein | Zählerstand Gaszähler S1 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 56 | Allgemein | Zählerstand Gaszähler S2 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 57 | Allgemein | Zählerstand Gaszähler S3 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 58 | Allgemein | Zählerstand Gaszähler S4 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 59 | Allgemein | Zählerstand Gaszähler S5 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 60 | Allgemein | Zählerstand Gaszähler S6 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 61 | Allgemein | Zählerstand Gaszähler S7 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 62 | Allgemein | Zählerstand Gaszähler S8 | Zahl | Nein | m³ |  |  |  | Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen. |  | freiwillig statt Pflicht (MoreApp blendet die Frage außer montags aus) |
| 63 | Allgemein | Sichtprüfung Tor 2 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 64 | Allgemein | Sichtprüfung Tor 3 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 65 | Allgemein | Sichtprüfung Tor 4 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 66 | Allgemein | Sichtprüfung Tor 5 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 67 | Warenausgangsbüro | Temperatur Klimaanlage | Zahl | Ja | °C |  |  |  |  |  |  |
| 68 | Allgemein | Sichtprüfung Tor 6 (Funktion, Piktogramm) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 69 | Allgemein | cos φ Wert Kompensationsanlage (Normalbereich cos φ > 0,90) | Zahl | Ja | cos φ | 0,90 |  | Mangel |  |  |  |
| 70 | Allgemein | Sichtprüfung Filtervlies Kompensationsanlage (Reinigung nur durch eingewiesenes Fachpersonal) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 71 | Allgemein | Zählerstand Hauptverteilung 1 | Zahl | Ja | kWh |  |  |  |  |  |  |
| 72 | Allgemein | Zählerstand Hauptverteilung 2 | Zahl | Ja | kWh |  |  |  |  |  |  |
| 73 | Allgemein | Zählerstand Hauptverteilung 3 | Zahl | Ja | kWh |  |  |  |  |  |  |
| 74 | Allgemein | Zählerstand Hauptverteilung 4 | Zahl | Ja | kWh |  |  |  |  |  |  |
| 75 | Allgemein | Sichtprüfung Elektronische Dachfenstersteuerung/ Lichtschalter | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Infrastrukturrundgang TGI MMS › Büro 1. OG

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 76 |  | Temperatur Serverraum (Sollzustand 18,0 °C - 21,0 °C) | Zahl | Ja | °C | 18,0 | 21,0 | Mangel |  |  |  |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |

## Brandschutzrundgang TGI MMS

- **Plan:** Mo–Fr – jede Woche
- **Bereich-Überschrift:** ausgeblendet
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Brandschutzrundgang TGI MMS › Brandmeldezentrale (BMZ) (1) · Brandschutzrundgang TGI MMS › Infrastrukturraum/ Produktionshalle (3) · Brandschutzrundgang TGI MMS › Produktionshalle (29) · Brandschutzrundgang TGI MMS › Brandschutz (13)


### Brandschutzrundgang TGI MMS › Brandmeldezentrale (BMZ)

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | Sichtprüfung ob frei zugänglich, ÜE eingeschaltet | i.O./n.i.O. | Ja |  |  |  |  |  | KRITISCH (Platzhalter): Text „Bitte sofort melden.“ · Ansprechpartner „PLATZHALTER Ansprechpartner BMZ“ | neu: kritisch mit Platzhalter (zur Besprechung) |

### Brandschutzrundgang TGI MMS › Infrastrukturraum/ Produktionshalle

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 |  | Sichtprüfung Feuerlöscher | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 3 |  | Druckgasflaschen und Behälter für brennbare Flüssigkeiten an den vorgeschriebenen Orten | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 4 |  | Brennbare Abfälle und selbstentzündliche Stoffe (Späne, Verpackung, Lappen, etc.) vorschriftsmäßig aufbewahrt | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Brandschutzrundgang TGI MMS › Produktionshalle

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

### Brandschutzrundgang TGI MMS › Brandschutz

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 34 |  | Feuerschutzabschlüsse (BS-Türen, BS-Tore) geschlossen, bzw. ordnungsgemäß aufgestellt, nicht blockiert, nicht beschädigt und leichtgängig | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 35 |  | Feuerlöscheinrichtungen zugänglich | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 36 |  | Lagergut und Abfall im Abstand von den Außenwänden abgestellt (5 m), Aufgrund der baulichen Gegebenheiten kann die 5 Meter Vorgabe nicht eingehalten werden | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
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
- **Gliederung:** Haustechnikrundgang TGI MMS › Grünflächen, Parkplätze (vor Bürogebäude) (7) · Haustechnikrundgang TGI MMS › Eingangsbereich/ Treppenhaus (6) · Haustechnikrundgang TGI MMS › Infrastrukturraum (6) · Haustechnikrundgang TGI MMS › Büro EG (9) · Haustechnikrundgang TGI MMS › Büro 1. OG (17) · Haustechnikrundgang TGI MMS › Sozialräume (15) · Haustechnikrundgang TGI MMS › Allgemein (11) · Haustechnikrundgang TGI MMS › Sammelstation für Altöl und Gefahrstoffe (5)


### Haustechnikrundgang TGI MMS › Grünflächen, Parkplätze (vor Bürogebäude)

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 2 |  | Kontrolle Toreinfahrt | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 3 |  | Sichtprüfung Feuerwehrtresor | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 4 |  | Sichtprüfung Gegensprechanlage | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 5 |  | Kontrolle Torausfahrt | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 6 |  | Reinigung Straßeneinläufe | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 7 |  | Reinigung Straßeneinlaufrinnen | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnikrundgang TGI MMS › Eingangsbereich/ Treppenhaus

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 |  | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 9 |  | Sichtprüfung Beleuchtung, elektrische Bauteile (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 10 |  | Sichtprüfung Türen, Fenster (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 11 |  | Sichtprüfung Wände, Decken, Böden (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 12 |  | Sichtprüfung Inventar, Büromöbel, etc. (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 13 |  | Sichtprüfung Heizung, Lüftung, Klima (Beschädigung, Verschmutzung, Wartung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnikrundgang TGI MMS › Infrastrukturraum

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 |  | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 15 |  | Sichtprüfung Beleuchtung, elektrische Bauteile (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 16 |  | Sichtprüfung Türen, Fenster (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 17 |  | Sichtprüfung Wände, Decken, Böden (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 18 |  | Sichtprüfung Inventar, Büromöbel, etc. (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 19 |  | Sichtprüfung Heizung, Lüftung, Klima (Beschädigung, Verschmutzung, Wartung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnikrundgang TGI MMS › Büro EG

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

### Haustechnikrundgang TGI MMS › Büro 1. OG

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
| 38 | Küchenbereich | Kontrolle Ordnung und Sauberkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 39 | Besuchertoiletten (Herren WC) | Kontrolle Ordnung und Sauberkeit Herren WC | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 40 | Besuchertoiletten (Herren WC) | Kontrolle Füllstand Seifenspender Herren WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 41 | Besuchertoiletten (Herren WC) | Kontrolle Füllstand Handtuchpapierspender Herren WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 42 | Besuchertoiletten (Herren WC) | Kontrolle Temperatur aller Durchlauferhitzer (mind. 60 °C) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 43 | Besuchertoiletten (Damen WC) | Kontrolle Ordnung und Sauberkeit Damen WC | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 44 | Besuchertoiletten (Damen WC) | Kontrolle Füllstand Seifenspender Damen WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  | Tippfehler „::“ → „:“ |
| 45 | Besuchertoiletten (Damen WC) | Kontrolle Füllstand Handtuchpapierspender Damen WC (ggf. nachfüllen) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnikrundgang TGI MMS › Sozialräume

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

### Haustechnikrundgang TGI MMS › Allgemein

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 61 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | EG Behinderten WC HWB | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 62 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | EG Halle Damen WC HWB | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 63 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | EG Halle Herren WC HWB | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 64 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | EG Küche Spüle | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 65 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | 1. OG Damen WC HWB rechts | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 66 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | 1. OG Besucher WC HWB | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 67 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | 1. OG Herren Dusche links Mischarmatur (Einfluss des Duschschlauchs) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 68 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | 1. OG Herren Dusche 4. HWB von links | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 69 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | 1. OG Herren WC HWB rechts | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 70 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | 1. OG Küche Spüle | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 71 | Spülen der Trinkwasserleitungen (ca. 1-2 Minuten pro Entnahmestelle) | Rücksprache mit Kunde, ob Reinigungszustand zufriedenstellend! (Wenn nicht, nähere Dokumentation auf Mängelprotokoll) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |

### Haustechnikrundgang TGI MMS › Sammelstation für Altöl und Gefahrstoffe

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 72 |  | Sichtkontrolle der Auffangwannen/ Auffangtassen nach AwSV | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 73 |  | Kontrolle der Beschaffenheit auf Dichtheit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 74 |  | Kontrolle der Beschaffenheit auf Standfestigkeit | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 75 |  | Kontrolle der Beschaffenheit auf Verschmutzung (Verschmutzungen sofort entfernen lassen!) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |

## Legionellen Prävention TGI MMS

- **Plan:** Mo – jede Woche (in MoreApp: Mittwoch – Besprechungspunkt)
- **Bereich-Überschrift:** ausgeblendet
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Legionellen Prävention TGI MMS › Legionellen Prävention (3)


### Legionellen Prävention TGI MMS › Legionellen Prävention

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | 1. OG Damenumkleide Dusche (10 Minuten Wasser mit mind. 60 °C durchlaufen lassen) | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  |  |  |  |
| 2 |  | 1. OG Damenumkleide HWB links (10 Minuten Wasser mit mind. 60 °C durchlaufen lassen) | i.O./n.i.O. („durchgeführt“ / „nicht durchgeführt“) | Ja |  |  |  |  |  |  |  |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |

## Sichtprüfung Gefahrstoffschränke TGI MMS

- **Plan:** Mo – jede Woche (in MoreApp: Mittwoch – Besprechungspunkt)
- **Bereich-Überschrift:** ausgeblendet
- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“
- **Testrundgang:** Ja (bis Inbetriebnahme)
- **Gliederung:** Sichtprüfung Gefahrstoffschränke TGI MMS › Gefahrstoffschränke (7)


### Sichtprüfung Gefahrstoffschränke TGI MMS › Gefahrstoffschränke

| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Gefahrstoffschrank Nr. 01 Service Nr./ Barcode: 106304 | Sichtprüfung Außen (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 2 | Gefahrstoffschrank Nr. 01 Service Nr./ Barcode: 106304 | Sichtprüfung Innen (beschädigte Gefäße, Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 3 | Gefahrstoffschrank Nr. 02 Service Nr./ Barcode: 106303 | Sichtprüfung Außen (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 4 | Gefahrstoffschrank Nr. 02 Service Nr./ Barcode: 106303 | Sichtprüfung Innen (beschädigte Gefäße, Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 5 | Gefahrstoffschrank Nr. 03 Service Nr./ Barcode: 106305 | Sichtprüfung Außen (Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| 6 | Gefahrstoffschrank Nr. 03 Service Nr./ Barcode: 106305 | Sichtprüfung Innen (beschädigte Gefäße, Beschädigung, Verschmutzung) | i.O./n.i.O. | Ja |  |  |  |  |  |  |  |
| +1 | Abschluss | Bemerkungen | Text | Nein |  |  |  |  | Freiwillig: alles, was sonst nirgends hinpasst. |  | neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars |
