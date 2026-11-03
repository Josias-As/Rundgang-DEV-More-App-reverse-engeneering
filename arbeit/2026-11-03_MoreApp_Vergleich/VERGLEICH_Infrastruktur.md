# MoreApp-Formular und MoreApp-Protokoll im Vergleich – Infrastrukturrundgang

Stand 03.11.2026. Quellen: 16 Bilder in `quellen/2026-11-03_MoreApp_Bilder/infrastruktur/` (vom 02.11.), 4 PDFs in `quellen/2026-11-03_MoreApp_Bilder/pdf/` (26.10./28.10.). Abgleich mit `werkzeuge/moreapp_vergleich.py` → `abgleich.txt` (die Fragen aus den Bildern sind von Hand abgeschrieben).

## Kurzfassung

1. **Infrastrukturraum: Das PDF ist vollständig.** Alle 44 Fragen aus den Bildern 01–09 stehen im PDF, in derselben Reihenfolge und mit den Antworten (belegt, Abgleich 44/44). Das Formular ist also nicht „genauer“ als das Protokoll. Das PDF lässt nur die Hilfen weg: Platzhalter („Druck in bar“), Pflicht-Sternchen, die rote Warnung bei Grenzverletzung und den Zugangscode-Hinweis.
2. **Die Bilder 10–16 („Produktionshalle“) passen zu keinem der vier PDFs.** 22 der 29 Fragen (Abfallcontainer, Selbstpresscontainer, Regal-Liftsystem, Hochregale, Staplerstation, Erste-Hilfe, Gehörschutz, Tore 2–6 Aschenbecher/Beleuchtung, Staubsauger Messstation …) stehen in keinem PDF (belegt). Die „Produktionshalle“ im Infrastruktur-PDF fragt etwas ganz anderes ab (Gaszähler S1–S8, Hauptverteilung 1–4, Kompensationsanlage, Klima Haftungskabine/Messraum …). Der Fragestil (Ordnung, Seifenspender, Durchlauferhitzer) gleicht dem Haustechnik-PDF, aber dort gibt es keine Produktionshalle. **UNSICHER, Frage an Josias:** Aus welchem Formular stammen die Bilder 10–16? Gibt es einen weiteren Rundgang (z. B. eine Hallenbegehung an einem anderen Tag), oder fehlen Teile im Haustechnik-PDF?
3. **Länge:** Laut PDF hat der Infrastrukturrundgang 76 Antworten (Batterieraum 1, Infrastrukturraum 44, Produktionshalle 30, Büro 1. OG 1) und der Haustechnikrundgang 75. Legionellen hat 2 Antworten, Gefahrstoffschränke 6 (von Hand gezählt).
4. **Passt zum App-Konzept: ja.** Jede Frage lässt sich mit den vorhandenen Eingabetypen und Paketen abbilden. Es fehlt kein Grundbaustein. Offen sind Kopf/Unterschrift (Paket 11), der Zugangscode (Paket 18) und wie groß eine Kategorie sein soll.

## Abbildung MoreApp → Rundgang-App

| MoreApp | Rundgang-App | Stand |
|---|---|---|
| Formular „Infrastrukturrundgang“ | Rundgang (`RG_Rundgaenge`), Tag über `RG_Plan` (Mo) | vorhanden |
| Unterformular „Infrastrukturraum (IS)“ mit eigenem „Speichern“ | **Kategorie** (eine Seite, eigenes Speichern = `RG_KategorieErgebnisse`) | vorhanden |
| graue Überschrift „Kompressor 3“, „ONI Kühlanlage“ | **Abschnitt** am Prüfpunkt | Paket 8 |
| „in Ordnung / nicht in Ordnung“ | IONIO, eigene Wörter möglich | Paket 12 (Standard i.O./n.i.O.) |
| Zahl mit Einheit (bar, m³, °C, Stunde(n), kWh, cos φ) | ZAHL + `Einheit` | vorhanden |
| „1,5 bis 2,0 bar“, „min. 2,0 bar“, „Soll 21–25 °C“, „cos φ > 0,90“, „Serverraum 18–21 °C“ | `MinWert`/`MaxWert`/`Grenzmodus` | vorhanden |
| rote Warnung „Sollzustand … nicht erreicht!“ | Hinweis unter dem Zahlenfeld (`lblKaZahlInfo`) | vorhanden |
| Zählerstände, Betriebsstunden | Abweichung zum letzten Lauf, „nur steigend“ | Paket 14 |
| „Mangelbeschreibung“ (ein Textfeld je Unterformular, Pflicht) | Kommentar je Frage, Pflicht bei n.i.O./Grenze, Mangel-Eintrag je Frage | vorhanden (genauer) |
| roter Hinweis „Zugangscode für Bedienteil …“ | Hinweis am Prüfpunkt / Anleitung (ⓘ) – **Code selbst: Paket 18 offen** | Paket 13 / 18 |
| Legionellen „durchgeführt“ | IONIO mit Wort „durchgeführt“ / „nicht durchgeführt“ | Paket 12 |
| Gefahrstoffschrank „Nr. 01 Service Nr./ Barcode 106304“ | Abschnitt-Text | Paket 8 |
| Kopf (Kunde, Adresse, Ausführender, KW, Wochentag), Unterschrift | Kopf teilweise (`PrueferName`, `KW`, `Wochentag`), Unterschrift fehlt | Paket 11 offen |
| Reihenfolge nach Laufweg (Kompressor 3 → 2 → 1) | `RgReihenfolge` | vorhanden |
| gleiche Blöcke (Kompressor 1–3, Kältemaschine 1–3, Tore, Gaszähler S1–S8, Schränke 01–03) | Builder „Duplizieren“ (Bereich/Kategorie/Prüfpunkt), „Mehrere Fragen …“ | vorhanden (kein „Abschnitt duplizieren“) |

## Befunde aus dem Protokoll (wichtig für den Nachbau)

- **„0“ statt „nicht messbar“:** Haftungskabine Klima **0 °C** (Soll 21–25 °C), Wareneingangsbüro 0 °C, Warenausgangsbüro 0 °C, Gaszähler S2 und S8 0 m³ (belegt). Eine Raumtemperatur von 0 °C ist nicht echt: Das Gerät war vermutlich aus, nicht ablesbar oder es gibt keins (geschlussfolgert). In der App: „nicht messbar“ mit Begründung (Paket 16). Zähler, die immer 0 sind, gar nicht erst anlegen (Frage an Josias).
- **Grenzverletzung ohne Folge:** 0 °C bei Soll 21–25 °C ist im PDF trotzdem kein Mangel. Bei der Produktionshalle steht als Mangelbeschreibung nur ein Komma (belegt). Vermutlich hat die Grenzverletzung das Pflichtfeld geöffnet und der Prüfer hat es mit „,“ übergangen (geschlussfolgert). Die App verlangt die Begründung an der Frage selbst und legt einen Mangel an.
- **Kalenderwoche falsch:** Das PDF zeigt KW 38 für Montag, 26.10.2026. Richtig ist **KW 44** (ISO). Die App rechnet mit `ISOWeekNum` (belegt).
- **Auffällige Werte:** Kompressor 1 hat 92 °C, Kompressor 2 31 °C, Kompressor 3 19 °C. Das ist echt oder ein Tippfehler; MoreApp hat keine Grenze. In der App eine Obergrenze setzen (Wert von der Haustechnik erfragen). Hauptverteilung 3 steht ohne Leerzeichen da („1390991kWh“), Dezimalpunkt statt Komma (1.8 bar).
- **Tippfehler im Formular:** „Kältemschine“, „Kühlamellen“, „nachfüllen)::“. Im Formular vom 02.11. sind „Kältemaschine 2/3“ schon korrigiert, im PDF vom 26.10. nicht → **MoreApp wird laufend geändert.** Vor dem Anlegen den aktuellen Formularstand nehmen.

## Was das für den Bau heißt

1. **Kategorien schneiden.** Der Infrastrukturraum hat in MoreApp 44 Fragen auf einer Seite. In der App wäre das eine sehr lange Kategorie (scrollen, beim Speichern geht alles zusammen). Vorschlag: nach Anlagen schneiden, z. B. „Heizung und Kompressoren“ (15), „Trockner und Wasser“ (6), „ONI Kühlanlage“ (8), „Kältemaschinen“ (15), dazu Abschnitte wie in MoreApp. Ob 44 Karten auf einer Seite flüssig laufen, ist nicht gemessen (UNSICHER) – mit dem echten Rundgang im Testmodus prüfen.
2. **Bereiche:** Batterieraum, Infrastrukturraum, Produktionshalle, Büro 1. OG (wie im PDF).
3. **Vor dem Anlegen klären:** Herkunft der Bilder 10–16 (siehe Kurzfassung 2), Zugangscode (Paket 18), Kopf/Unterschrift (Paket 11), Grenzwerte für Kompressor-Temperatur, Klima ohne Soll (Analysebüro, Wareneingangs-/Warenausgangsbüro) und Wassertemperatur Kältemaschinen.
4. Für die anderen drei Rundgänge fehlen noch die Formular-Bilder. Das PDF reicht als Fragenliste (beim Infrastrukturraum vollständig, belegt), zeigt aber keine Grenzen, Hinweise oder Bedingungen.
