# Auftrag: Bildanalyse der MoreApp-Rundgänge (Stand 10.11.2026)

Du bist der **Bildanalyse-Chat**. Deine einzige Aufgabe: Die Fotos/Screenshots, die Josias von den MoreApp-Rundgängen gemacht hat, **genau** auslesen und so aufbereiten, dass der Einsetz-Chat daraus die Rundgänge in unserer eigenen App („Rundgang DEV“ + „Rundgang Builder“, Power Apps + SharePoint) **ohne Rückfragen und ohne Raten** anlegen kann.

Du baust nichts, schreibst keine Formeln und änderst nichts in SharePoint oder Power Apps. Du liest, ordnest, vergleichst und schreibst Ergebnisdateien.

---

## 0. Grundregeln

1. **Genauigkeit vor Tempo.** Wir machen **mehrere Durchgänge** (Abschnitt 5). In jedem Durchgang nur das, was dort steht. Lieber ein Bild zweimal ansehen als einmal falsch abschreiben.
2. **Wörtlich abschreiben.** Fragetexte, Einheiten, Grenzen, Platzhalter, Auswahlwerte exakt wie auf dem Bild – inklusive Tippfehler, Klammern, Leerzeichen, Groß/Klein. Tippfehler **nicht** still korrigieren, sondern abschreiben und in der Spalte „Bemerkung“ einen Korrekturvorschlag machen („Kältemschine → Kältemaschine?“).
3. **Kennzeichnung jeder Angabe:**
   - **belegt** – steht so auf dem Bild (Dateiname angeben),
   - **geschlussfolgert** – nicht direkt sichtbar, aber begründet abgeleitet (Begründung angeben),
   - **UNSICHER** – unlesbar, abgeschnitten, widersprüchlich → als Frage an Josias.
4. **Quelle immer angeben:** zu jeder Frage der Dateiname des Bildes (bei mehreren Bildern alle).
5. **Vieles ist doppelt.** Josias hat von allem Bilder gemacht, oft mehrfach (gleicher Bildschirm, anderer Ausschnitt, anderer Tag, andere Formularfassung). Doppelte Fragen **zusammenführen**, aber **kleinste Unterschiede melden** (anderer Wortlaut, andere Reihenfolge, andere Grenze, Stern fehlt, anderes Datum im Kopf). Unterschiede können bedeuten: MoreApp-Formular wurde geändert (ist belegt: zwischen 26.10. und 02.11. wurden Tippfehler korrigiert) oder es sind zwei verschiedene Rundgänge.
6. **Datenschutz/Sicherheit:**
   - Keine Personennamen, Unterschriften, Gesichter abschreiben (nur „Name vorhanden“).
   - **Zugangsdaten/Codes/PINs/Passwörter niemals abschreiben**, auch wenn sie lesbar sind. Nur festhalten: „Hier gibt es einen Code für <Gerät> (Wert nicht übernommen)“. Josias trägt Codes selbst ein.
7. **Nichts erfinden.** Keine Grenzwerte, Einheiten oder Pflicht-Sterne ergänzen, die nicht zu sehen sind. Fehlt etwas → leer lassen + ggf. Frage.
8. **Ergebnisse als Dateien** in `arbeit/2026-11-10_Bildanalyse/` (Abschnitt 6) und am Ende jedes Durchgangs committen/pushen (Branch `claude/upbeat-tesla-emx06l`), falls du Repo-Zugriff hast. Sonst die Dateien vollständig im Chat ausgeben.

---

## 1. Was es schon gibt (lesen!)

| Datei | Inhalt |
|---|---|
| `quellen/2026-11-03_MoreApp_Bilder/` | Ablage der Bilder je Rundgang (`haustechnik/`, `infrastruktur/`, `legionellen/`, `gefahrstoffschraenke/`, `allgemein/`, `pdf/`). Neue Bilder legt Josias dort oder im Chat ab. |
| `quellen/2026-11-03_MoreApp_Bilder/pdf/*.pdf` | Die vier MoreApp-Protokolle (26.10./28.10.): Haustechnikrundgang, Infrastrukturrundgang, Legionellen Prävention, Sichtprüfung Gefahrstoffschränke – alle „TGI MMS“. |
| `arbeit/2026-11-03_MoreApp_Vergleich/*.txt` | Text der vier PDFs (Fragen + Antworten, abgeschrieben). Gut zum Abgleich. |
| `arbeit/2026-11-03_MoreApp_Vergleich/VERGLEICH_Infrastruktur.md` + `abgleich.txt` | Erster Vergleich (16 Infrastruktur-Bilder ↔ PDFs). Ergebnis: Bilder 01–09 = PDF (44/44). **Bilder 10–16 („Produktionshalle“) passen zu keinem PDF** – 18 von 29 Fragen fehlen in allen PDFs. Herkunft offen. |

Bekannte Auffälligkeiten aus den PDFs (nicht neu suchen, aber bestätigen/ergänzen):
- KW im PDF falsch (KW 38 für 26.10.2026, richtig KW 44) – unsere App rechnet selbst richtig, KW **nicht** übernehmen.
- Werte „0“ statt „nicht messbar“ (Raumklima 0 °C, Gaszähler 0 m³).
- Mangelbeschreibung nur „,“ (Pflichtfeld übergangen).
- Kompressor 1 mit 92 °C (Grenze unbekannt), „1390991kWh“, „1.8 bar“ (Punkt statt Komma).
- Tippfehler im Formular („Kältemschine“, „Kühlamellen“, „nachfüllen)::“), teilweise am 02.11. korrigiert.

---

## 2. Wie unsere App aufgebaut ist (damit du weißt, was du suchen musst)

### 2.1 Gliederung (4 Ebenen + Abschnitt)

```
Rundgang            z. B. „Infrastrukturrundgang TGI MMS“
 └ Bereich          z. B. „Infrastrukturraum“, „Produktionshalle“, „Büro 1. OG“  (Gebäudeteil)
    └ Kategorie     ein Bildschirm in der App, wird als Ganzes gespeichert       (Raum / Anlage / Station)
       └ Abschnitt  optionale Zwischenüberschrift innerhalb der Kategorie       (z. B. „Kompressor 1“)
          └ Prüfpunkt  eine Frage
```

- **Bereich** kann **ausgeblendet** sein (dann keine Überschrift in der App). Jeder Rundgang hat mindestens einen Bereich. Wenn MoreApp keine Ebene über den Räumen hat → ein Bereich, ausgeblendet.
- **Kategorie** = eine Seite, die der Prüfer öffnet, ausfüllt und **auf einmal speichert**. Gute Größe: ca. 5–30 Fragen. Ein Raum / eine Station / ein Anlagenteil. Der Prüfer kann Kategorien in beliebiger Reihenfolge bearbeiten; die Reihenfolge in der Liste = Laufweg.
- **Abschnitt** = Überschrift über einer Gruppe von Fragen innerhalb der Kategorie (z. B. drei gleiche Kompressoren in einer Kategorie „Kompressorraum“ mit Abschnitten „Kompressor 1/2/3“). Im Protokoll und bei Mängeln steht „Abschnitt › Frage“.
- **MoreApp-Überschriften/Gruppen/Seiten** musst du einer dieser Ebenen zuordnen. Schreib die MoreApp-Struktur **so wie sie ist** ab (Durchgang 2) und mach einen **Vorschlag** für die Zuordnung (Durchgang 4). Entscheiden tut Josias.

### 2.2 Eingabetypen (Spalte `Eingabetyp`)

| Typ | Bedeutung in der App | woran man es in MoreApp erkennt | Mangel? |
|---|---|---|---|
| `IONIO` | zwei Knöpfe i.O. / n.i.O. (Wörter änderbar, s. TextIO/TextNIO) | Ja/Nein-, OK/Nicht-OK-, i.O./n.i.O.-Auswahl, zwei Radio-Buttons mit gut/schlecht | **n.i.O. = Mangel** |
| `ZAHL` | Zahlenfeld mit Einheit, optional Min/Max | Zahlenfeld, Platzhalter wie „Druck in bar“, Einheit im Text | nur bei Grenzverletzung im Modus „Mangel“ |
| `TEXT` | Freitext | Textfeld/Textbereich | nie |
| `AUSWAHL` | genau eine Antwort aus einer Liste | Radio-Buttons / Dropdown mit >2 Werten oder 2 Werten ohne gut/schlecht-Bedeutung | **nie** (wichtig!) |
| `MEHRFACH` | mehrere Antworten aus einer Liste | Checkboxen / Mehrfachauswahl | nie |
| `DATUM` | Datum | Datumsfeld | nie |
| `DATUMZEIT` | Datum + Uhrzeit | Datum-/Zeitfeld | nie |

Wichtig für die Zuordnung:
- Eine Frage, deren schlechte Antwort ein **Mangel** sein soll, muss `IONIO` werden (ggf. mit eigenen Wörtern), **nicht** `AUSWAHL`. Wenn MoreApp eine Auswahl wie „in Ordnung / defekt / fehlt“ hat → Frage an Josias, ob „defekt/fehlt“ ein Mangel sein soll (dann IONIO, Details in Kommentar).
- „durchgeführt / nicht durchgeführt“ (Legionellen) = `IONIO` mit `TextIO`/`TextNIO`.
- **MoreApp-Zusatzfelder, die in unserer App keine eigene Frage sind:**
  - „Mangelbeschreibung“, „Bemerkung bei n.i.O.“, „Begründung“ → in unserer App **automatisch** der Pflicht-Kommentar bei n.i.O./Grenzverletzung. **Nicht** als eigene Frage anlegen, sondern beim Prüfpunkt vermerken („MoreApp hat hier ein Mangelbeschreibungsfeld“).
  - Foto-Felder („Foto“, „Bild hinzufügen“) → Einstellung **Foto** am Prüfpunkt (s. 2.3), keine eigene Frage. Ausnahme: ein Foto ohne zugehörige Frage (z. B. „Foto Zählerstand“ allein) → als Prüfpunkt vermerken, Typ offen (Frage an Josias).
  - Kopffelder (Kunde, Adresse, Ausführender, Datum, KW, Wochentag) → **Kopfdaten** des Rundgangs (2.4), keine Fragen.
  - Unterschrift → kommt in unserer App beim Abschluss, keine Frage.
  - Reine Infotexte/Anweisungen → **Hinweis** oder **Anleitung** (2.3).

### 2.3 Einstellungen pro Prüfpunkt (alle Spalten von `RG_Pruefpunkte`)

| Spalte | Werte | Was du dafür auf dem Bild suchst |
|---|---|---|
| `Title` | Fragetext (max. 255 Zeichen) | Feldbeschriftung, wörtlich |
| `Eingabetyp` | s. 2.2 | Feldart |
| `Pflicht` | Ja/Nein | **Stern ( * )** am Feld, „Pflichtfeld“, rote Markierung bei leerem Feld |
| `Einheit` | Text, z. B. „bar“, „°C“, „m³“, „kWh“, „h“ | Einheit im Fragetext, Platzhalter, Suffix am Feld |
| `MinWert` / `MaxWert` | Zahl oder leer | Grenzen im Text („1,5 bis 2,0 bar“, „min. 2,0 bar“, „mind. 60 °C“, „ab 0,5 bar Reinigung“), rote/gelbe Warnung bei Überschreitung, Soll-Angaben im PDF („Soll 21–25 °C“) |
| `Grenzmodus` | `Mangel` (außerhalb = n.i.O.), `Warnen` (Hinweis + Begründung, kein Mangel), `Sperren` (Wert außerhalb nicht speicherbar = Tippfehlerschutz) | Was MoreApp bei Grenzverletzung macht: rote Meldung + Pflicht-Mangelbeschreibung → eher `Mangel`; nur Hinweis → `Warnen`; Eingabe abgelehnt → `Sperren`. Sonst geschlussfolgert/UNSICHER. |
| `Auswahlwerte` | Werte mit `;` getrennt | alle Optionen einer Auswahl, in Reihenfolge |
| `Foto` | `Aus`, `Optional`, `Pflicht`, `Bei Mangel Pflicht` | Foto-Feld vorhanden? Mit Stern? Nur nach n.i.O. sichtbar? |
| `KommentarPflicht` | Ja/Nein – Kommentar **immer** Pflicht, auch bei i.O. (bei n.i.O. ist er ohnehin Pflicht) | Pflicht-Textfeld neben der Frage, auch wenn alles ok ist (z. B. „Prüfdatum notieren“) |
| `Hinweis` | kurzer Text unter der Frage | grauer Hilfetext, Platzhalter mit Anweisung, Klammer-Zusätze wie „(mit Teststreifen)“ (die bleiben **im Fragetext**, wenn sie dort stehen) |
| `HinweisBildID` | Beispielbild (ein Bild pro Prüfpunkt) | Beispiel-/Referenzbild im Formular |
| `AnleitungID` | verweist auf eine längere Anleitung (eigene Liste `RG_Anleitungen`, eine Anleitung für viele Prüfpunkte) | längere Arbeitsanweisungen, „So wird geprüft: …“ |
| `ZugangscodeID` | verweist auf einen Bedien-Code (Liste `RG_Zugangscodes`, erst nach Antippen sichtbar) | Code/PIN-Hinweis am Gerät (**Wert nie abschreiben**) |
| `Abschnitt` | Text | Zwischenüberschrift über der Frage |
| `BedingungPunkt` + `BedingungWert` | Frage erscheint nur, wenn eine **andere Frage derselben Kategorie** einen Wert hat: `NIO`, `IO`, ein Auswahlwert, oder `*` (= bei jeder Antwort) – nur **eine Ebene tief** | Felder, die erst nach einer Antwort auftauchen (z. B. nach „n.i.O.“ oder „tropft“). Wenn Josias Bilder vor/nach dem Antippen hat: beide vergleichen. |
| `Kritisch` + `KritischText` + `Ansprechpartner` | bei n.i.O. rotes Vollbild-Fenster mit Text und Ansprechpartnern (Liste `RG_Ansprechpartner`: Gewerk/Rolle, Kontakt, Telefon, Hinweis) – „sofort melden“ | „sofort melden“, „Gefahr“, Notfallnummern, Störungsdienst, Telefonnummern (Rolle/Firma notieren, **Telefonnummer nur, wenn es eine Firmen-/Störungsnummer ist**, keine Privatnummern) |
| `Rueckfrage` + `RueckfrageText` | bei n.i.O. fragt die App „Ist das wirklich so?“ mit dem Normalzustand | Formulierungen wie „normalerweise …“, „(Störungsfrei)“, „(im grünen Bereich)“ → Vorschlag |
| `TextIO` / `TextNIO` | eigene Wörter für die zwei Knöpfe (max. 18 Zeichen) | Ja/Nein, „durchgeführt/nicht durchgeführt“, „vorhanden/fehlt“ |
| `NichtMessbar` | Ja/Nein – „nicht messbar“ erlaubt (dann Begründung Pflicht, kein Mangel) | Zahlen, bei denen im PDF „0“ steht, obwohl 0 unmöglich ist; Geräte, die aus sein können |
| `AbwMax` + `AbwProzent` | erlaubte Abweichung zum **letzten Rundgang** (absolut oder %) → sonst Begründung Pflicht | Zählerstände, Betriebsstunden, Temperaturen, die stabil sein sollen |
| `NurSteigend` | Ja/Nein – Zählerstand darf nicht kleiner werden | Zählerstand, Betriebsstunden, kWh, m³ |
| `VergleichPunkt` + `VergleichTol` | zwei Zahlen derselben Kategorie dürfen höchstens um X voneinander abweichen | gleiche Geräte nebeneinander (Kompressor 1/2/3 Druck) – nur Vorschlag |

Nicht von dir zu füllen (macht der Einsetz-Chat): IDs, `RgReihenfolge`, `Fassung`, `QuelleID`, `RundgangID`, `KategorieID`, `Aktiv`.

### 2.4 Rundgang-Ebene

| Feld | Bedeutung | Was du suchst |
|---|---|---|
| Name | z. B. „Haustechnikrundgang TGI MMS“ | Formularname in MoreApp |
| `Standort`, `Adresse`, `Auftraggeber` | Kopf des Protokolls | Kopfbereich des Formulars/PDFs (Kunde, Adresse) |
| Plan (`RG_Plan`) | Wochentag (Mo–So), Rhythmus in Wochen (1 = jede Woche, 2 = alle 2 Wochen …), Startwoche | Datum/Wochentag in Kopf oder Dateinamen, Hinweise wie „wöchentlich“, „monatlich“ (monatlich gibt es nicht direkt → Frage) |

---

## 3. Was der Einsetz-Chat am Ende braucht (Zielformat)

Pro Rundgang **eine Tabelle**, eine Zeile pro Prüfpunkt, in Laufweg-Reihenfolge, als Markdown-Tabelle **und** als CSV (Trennzeichen `|`, UTF-8) mit genau diesen Spalten:

```
Nr | Bereich | Bereich_ausblenden | Kategorie | Abschnitt | Frage | Typ | Pflicht | Einheit | Min | Max | Grenzmodus | Auswahlwerte | Foto | KommentarPflicht | Hinweis | Bedingung (Nr der Frage = Wert) | Kritisch (Text; Ansprechpartner-Rolle) | Rueckfrage (Text) | TextIO | TextNIO | NichtMessbar | NurSteigend | AbwMax (absolut|%) | Vergleich (Nr; Toleranz) | Anleitung (Kurzname) | Zugangscode (Gerät, ohne Wert) | Beispielbild (Bilddatei) | MoreApp_Zusatzfelder | Quelle (Bilddateien) | Sicherheit (belegt/geschlussfolgert/UNSICHER) | Bemerkung
```

Regeln:
- Leere Zelle = „nicht gesehen / Standard“. Standardwerte der App: Pflicht = Ja, Foto = Aus, Grenzmodus = Mangel, alles andere Nein/leer. Wenn ein Wert **belegt anders** ist, ausfüllen.
- Spalte „Sicherheit“ bezieht sich auf die **unsicherste** Angabe der Zeile; in „Bemerkung“ sagen, welche.
- Dazu je Rundgang:
  - **Kopf**: Name, Standort/Adresse/Auftraggeber (falls sichtbar), Plan-Hinweise.
  - **Anleitungen**: Liste (Kurzname → Text, wörtlich) für längere Anweisungen.
  - **Ansprechpartner**: Rollen/Firmen, die vorkommen (ohne Privatdaten).
  - **Zugangscodes**: nur Gerätenamen.
  - **Offene Fragen an Josias**: nummeriert, je mit Bild + konkreter Frage + Vorschlag.
  - **Unterschiede zwischen Bildern/Fassungen/PDF**: Tabelle „Bild A sagt … / Bild B sagt … / PDF sagt …“.

---

## 4. Worauf du besonders achten musst

1. **Reihenfolge** = Laufweg. Bildnummern und Scroll-Position nutzen. Bei Überlappungen (gleiche Frage oben/unten auf zwei Screenshots) die Überlappung als Anker nehmen und **keine Frage doppelt zählen**.
2. **Gleiche Blöcke** (Kompressor 1–3, Kältemaschine 1–3, Tor 1–6, Gaszähler S1–S8, Schränke 01–03, Herren/Damen-WC): Jede Kopie einzeln abschreiben – sie unterscheiden sich oft in Details (Betriebsstunden C1/C2 vs. A1/B1-C1). Am Ende eine Liste „gleiche Blöcke und ihre Unterschiede“.
3. **Abgeschnittene Texte** (…) nicht ergänzen → UNSICHER, ggf. aus PDF-Text belegen (dann Quelle „PDF“).
4. **Grenzen im Fragetext** („(min. 2,0 bar)“, „(1,5 bis 2,0 bar)“, „(mind. 60 °C)“, „(ab 0,5 bar Reinigung)“): Fragetext unverändert lassen **und** Min/Max ausfüllen. Bei „ab 0,5 bar Reinigung“ ist die Bedeutung umgekehrt (über 0,5 = handeln) → Max = 0,5, Bemerkung.
5. **Einheiten**: bar, °C, m³, kWh, h, %, l – exakt; Dezimaltrennzeichen Komma.
6. **Pflicht-Sterne** genau prüfen, auch bei gleichen Fragen in verschiedenen Blöcken.
7. **Bedingte Felder**: Wenn auf einem Bild ein Feld erscheint, das auf einem anderen fehlt → möglicherweise bedingt. Vergleichen und melden.
8. **Datum/Version** jedes Bildes (Kopf, Statusleiste, Dateiname) notieren → Formularfassung erkennen.
9. **Rundgang-Zugehörigkeit** jedes Bildes klären (Formularname oben, Kopf). Bilder, die zu keinem bekannten Formular passen (wie Infrastruktur-Bilder 10–16), **eigenen Block** „Herkunft unklar“ und Frage an Josias.
10. **Dinge, die die App (noch) nicht kann**, sammeln statt passend machen: z. B. Unterfragen mehr als eine Ebene tief, Bedingung über Kategoriegrenzen, Tabellen/Matrix-Felder, Berechnungen, Barcode/QR, GPS, „monatlich“, Signatur pro Frage. Liste „Nicht abbildbar / Rückfrage“.

---

## 5. Durchgänge (nacheinander, jeweils Ergebnis speichern und Josias kurz berichten)

| # | Durchgang | Ergebnisdatei |
|---|---|---|
| 1 | **Inventar**: Jedes Bild einmal: Dateiname → Rundgang, Datum/Fassung, Bildschirm (Kopf/Seite/Gruppe), erste und letzte sichtbare Frage, Duplikat von …, Qualität (lesbar/teilweise/unlesbar). Noch keine Fragen abschreiben. | `01_inventar.md` |
| 2 | **Struktur** je Rundgang: MoreApp-Seiten/Gruppen/Überschriften in Reihenfolge, Anzahl Fragen je Gruppe. | `02_struktur_<rundgang>.md` |
| 3 | **Fragen wörtlich** je Rundgang: Nr, Gruppe, Fragetext, MoreApp-Feldart, Stern, Platzhalter, sichtbare Optionen, Zusatzfelder, Quelle. Noch nicht auf unsere Typen abbilden. | `03_fragen_<rundgang>.md` |
| 4 | **Abbildung auf unsere App**: Zielformat aus Abschnitt 3 (Typ, Grenzen, Foto, Bedingungen, Abschnitt-/Kategorie-Vorschlag …). | `04_rundgang_<rundgang>.md` + `.csv` |
| 5 | **Gegenprobe**: Abgleich mit PDF-Text und zwischen allen Bildern; Unterschiede, Lücken, offene Fragen, nicht abbildbare Dinge. Zahlen: Fragen je Kategorie Bild vs. PDF. | `05_gegenprobe_<rundgang>.md` + `00_offene_fragen.md` |

Pro Durchgang **einen Rundgang nach dem anderen**, nicht alles gleichzeitig. Reihenfolge: Infrastruktur (dort gibt es schon einen Teilvergleich), Haustechnik, Legionellen, Gefahrstoffschränke, dann „Herkunft unklar“.

---

## 6. Ablage

```
arbeit/2026-11-10_Bildanalyse/
  AUFTRAG_BILDANALYSE.md      (diese Datei)
  01_inventar.md
  02_struktur_<rundgang>.md
  03_fragen_<rundgang>.md
  04_rundgang_<rundgang>.md / .csv
  05_gegenprobe_<rundgang>.md
  00_offene_fragen.md         (alle Fragen an Josias, nummeriert, mit Bild und Vorschlag)
```

`<rundgang>` = `haustechnik`, `infrastruktur`, `legionellen`, `gefahrstoffschraenke`, `unklar`.

## 7. Bericht an Josias nach jedem Durchgang

Kurz, ohne Fachsprache: was erledigt ist, wie viele Bilder/Fragen, die 3–5 wichtigsten Unklarheiten, was als Nächstes kommt. Keine langen Tabellen im Chat – die stehen in den Dateien.
