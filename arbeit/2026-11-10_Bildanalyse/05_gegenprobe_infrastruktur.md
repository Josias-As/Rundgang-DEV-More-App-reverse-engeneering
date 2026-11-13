# Durchgang 5 – Gegenprobe: Infrastrukturrundgang

Abgleich der Bilder (Mo/Di/Mi 10.11., REPO 02.11.) mit dem PDF „Infrastrukturrundgang“ vom 26.10.2026 (Montag, Text: `arbeit/2026-11-03_MoreApp_Vergleich/2026-10-26_Infrastrukturrundgang_TGI_MMS.txt`) und untereinander.

## 1. Zahlen: Fragen je Kategorie

| Kategorie | Bild Mo | Bild Di | Bild Mi | Bild 02.11. | PDF 26.10. (Mo) | Ergebnis |
|---|---|---|---|---|---|---|
| Batterieraum | 1 | 1 | 1 | – | 1 | gleich |
| Infrastrukturraum | 44 | 44 | 44 | 44 | 44 | gleich |
| Produktionshalle | 30 | 21 | 21 | – | 30 | Mo = PDF (das PDF ist ein Montag). Di/Mi ohne die 9 Montagsfragen |
| Büro 1. OG | 1 | 1 | 1 | – | 1 | gleich |
| **Summe** | **76** | **67** | **67** | | **76** | |

Die Reihenfolge der 76 Montagsfragen ist mit dem PDF identisch (von Hand Zeile für Zeile verglichen; der automatische Abgleich scheiterte nur an Zeilenumbrüchen im PDF-Text).

## 2. Unterschiede im Wortlaut

| Stelle | Bilder 10.11. sagen | Bild 02.11. sagt | PDF 26.10. sagt | Bewertung |
|---|---|---|---|---|
| Abschnitt Kältemaschine 2 | „Kältemaschine 2 (Außenbereich)“ | „Kältemaschine 2 (Außenbereich)“ | „Kältemschine 2 (Außenbereich)“ | zwischen 26.10. und 02.11. korrigiert (belegt) |
| Abschnitt Kältemaschine 3 | „Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum)“ | gleich | „Kältemschine 3 (…)“ | korrigiert (belegt) |
| Abschnitt Kältemaschine 1 | „Kältemschine 1 (…)“ | gleich | gleich | **noch falsch** (Vorschlag: „Kältemaschine 1“) |
| Kältemaschine 1, Frage | „Kontrolle Kühlamellen:“ | gleich | gleich | **noch falsch** (Vorschlag: „Kühllamellen“) |
| Überschriften | „Infrastrukturraum (IS)“, „Produktionshalle (IS):“, „Büro 1. OG (IS)“ | – | „Infrastrukturraum:“, „Produktionshalle:“, „Büro 1. OG:“ | Das PDF lässt „(IS)“ weg → der Kategoriename ohne Kürzel ist belegt |
| rote Meldung Heizungspumpe | „Sollzustand von mindesten 2,0 bar nicht erreicht!“ | gleich | – (das PDF zeigt keine Meldungen) | Tippfehler „mindesten“; in der App nicht nötig |
| Zugangscode KM 1 | rote Zeile mit Code | geschwärzt | – | nur im Formular sichtbar |

Was das PDF nicht zeigt: Platzhalter, Sterne, rote Meldungen, Zugangscode (wie schon im Vergleich vom 03.11. festgestellt).

## 3. Werte im PDF, die für die Einstellungen wichtig sind

| Frage | PDF-Wert | Folgerung (in `04_…` eingetragen) |
|---|---|---|
| Betriebsstunden (alle) | „… Stunde(n)“ | Einheit „h“ (geschlussfolgert) |
| Druckmanometer Heizung | „1.8 bar“ | Punkt statt Komma: Die App sollte Komma erzwingen bzw. beides annehmen (Info für den Einsetz-Chat) |
| Temperatur Kompressor 1 / 2 / 3 | 92 / 31 / 19 °C | Grenze unbekannt → Q-IS-4 |
| Temperatur Klimaanlage Haftungskabine | 0 °C (Soll 21–25) | NichtMessbar = Ja (Vorschlag) |
| Temperatur Klimaanlage Wareneingangs-/Warenausgangsbüro | 0 °C | NichtMessbar = Ja (Vorschlag) |
| Gaszähler S2, S8 | 0 m³ | NichtMessbar = Ja (Vorschlag) oder gar nicht anlegen → Q-IS-6 |
| Zählerstand Hauptverteilung 3 | „1390991kWh“ | fehlendes Leerzeichen, nur Druckbild |
| Mangelbeschreibung Produktionshalle | „,“ | Pflichtfeld wurde übergangen; die App verlangt den Kommentar je Frage |
| Kalenderwoche | 38 (am 26.10.) | auch am 10.11. noch „38“ vorbelegt → KW in MoreApp fest; nicht übernehmen |

## 4. Lücken
- Kein Bild mit gewählter Antwort oder eingetragener Zahl. Ob MoreApp bei „nicht in Ordnung“ oder bei einer Grenzverletzung zusätzliche Felder einblendet (z. B. Foto, eigene Beschreibung), ist **nicht belegt** → Q-ALL-3.
- Kein Bild vom Donnerstag/Freitag → Q-ALL-2.

## 5. Nicht abbildbar
1. Wochentag-abhängige Fragen (9 Montagsfragen) → Q-IS-1.
2. Sonst ist alles mit den vorhandenen App-Typen abbildbar: IONIO, ZAHL mit Einheit/Min/Max, Abschnitte, Zugangscode.
