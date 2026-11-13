# Auftrag an den Analyse-Chat: Paket 26 (Fehler + Builder-Optik) – 13.11.2026

Vom Einsetz-Chat, mit Josias abgestimmt. Ziel: Die Apps vor dem Anlegen der echten Rundgänge stabil machen. Danach werden die 5 Rundgänge angelegt und das Projekt vorerst abgeschlossen.

## 0. Stand (wichtig für die Vorher-Fassungen)

- In beiden Apps eingesetzt: alles bis **Paket 25** (Rückbau Prüferauswahl) und **Paket 24** (Info-Knopf), 13.11.
  - P25 DEV: `btnKaSpeichern` musste zweimal eingefügt werden, jetzt 0 Fehler.
  - P24 DEV: `btnKaBild` und `conKaBild` wurden **gelöscht** (statt Visible = false).
  - P24 Builder: die 20 Lage-/Text-Werte in `conPRest` – Einbau gerade im Gange (Texte waren drin, Positionen noch nicht, Stand Screenshot 13.11.).
- **Vor dem Bauen bitte einen frischen Export beider Apps von Josias anfordern** (vorher veröffentlichen, Export enthält nur den veröffentlichten Stand). Paket 26 muss exakt auf diesem Stand aufsetzen. Beim Abgleich auf die bekannten Abweichungen aus `arbeit/2026-11-06_Einsetz_Chat/UEBERGABE_an_Analyse_Chat_2026-11-09.md` achten (A15–A20).

## 1. Fehler aus dem Testlauf beheben (`arbeit/2026-11-06_Einsetz_Chat/TESTLAUF_2026-11-06.md`, Abschnitt A)

| Nr | App | Kurz | Priorität |
|---|---|---|---|
| **A3** | DEV | Kategorie ohne aktiven Prüfpunkt wird beim Start aufgenommen, ist nie speicherbar ⇒ Lauf **nie abschließbar** | **hoch** – beim Start nur Kategorien mit ≥ 1 aktivem Prüfpunkt aufnehmen (und/oder Builder-Prüfliste warnt) |
| **A5** | DEV | `fnFehltGrund`: Foto Pflicht sperrt auch freiwillige, unbeantwortete Frage | hoch |
| **A9** | DEV | Antworten zu inzwischen inaktiven Prüfpunkten zählen in AnzahlNIO/Mängel, sind aber unsichtbar | hoch |
| **A10** | DEV | `Filter(RG_Kategorien; Aktiv = true)` ohne Rundgang-Filter (Delegations-/Zeilenlimit) | mittel |
| **A12** | Builder | Typwechsel weg von ZAHL lässt `VergleichPunkt` stehen ⇒ Aktivieren gesperrt ohne sichtbaren Ausweg | mittel |
| **A13** | Builder | Bedingung „NIO“ an ZAHL ohne Grenzen / Modus Warnen/Sperren gilt als gültig ⇒ Folgefrage erscheint nie | mittel |
| **A14** | DEV/Builder | `fnPlanPasst` zählt Wochen ab StartMontag statt ab Montag der Startwoche; prüfen, ob scrPlan einen Montag erzwingt | mittel |

Details, Zeilen und Szenarien stehen in der TESTLAUF-Datei. Die C-Punkte (Aufräumen) **nicht** in dieses Paket, außer sie hängen direkt an einer der Stellen oben (z. B. C25 bei A12).

## 2. Builder-Optik (Josias, Screenshot 13.11.)

1. **Gequetschte Stellen im Prüfpunkt-Bereich (`scrEditor › conEdMitte › conEdP`)**: Nach dem Einbau der P24-Positionen kommt ein neuer Screenshot von Josias. Alles, was danach noch abgeschnitten, umgebrochen oder überlappend ist, mit in dieses Paket. Schon jetzt sichtbar:
   - Beschriftung „Info ⓘ: Beispielbild (optional)“ bricht um und wird abgeschnitten (sollte mit P24 B2.12/B2.13 weg sein – prüfen).
   - „Gehört zur Kategorie“-Auswahl schneidet „Bereich › Kategorie“ ab (Breite/Text kürzen, z. B. nur Kategoriename + Tooltip).
   - Generell: Beschriftungen in `conPRest`/`conEdP` auf Textbreite prüfen (Generator-Prüfung „Textbreiten“ wie bei P11).
2. **Prüfliste zeigt leere Punkte**: Rechts unter „Prüfung: keine Fehler“ stehen mehrere **leere orange Punkte** (Galerie mit leeren Einträgen). Erwartet: bei 0 Fehlern keine Einträge. Vermutlich `galPr.Items` liefert Zeilen mit leerem Text (Filter auf `Text <> ""` fehlt) – bitte belegen.
3. **„Aktivieren …“ farblich hervorheben** (Josias: grün):
   - Prüfung ohne Fehler und Entwurf offen ⇒ **grün gefüllt, weiße Schrift** (eigene Farbe `clrOk`/vorhandenes Grün aus App.Formulas verwenden, falls vorhanden).
   - Fehler vorhanden ⇒ **grau/gesperrt** (DisplayMode.Disabled, wie bisher gesperrt).
   - Hover/Pressed passend abdunkeln.

## 3. Nicht in dieses Paket (zur Info)

- **Entscheidung offen:** Fragen/Kategorien nur an bestimmten Wochentagen (MoreApp blendet z. B. Gaszähler S1–S8 nur montags ein, siehe `arbeit/2026-11-10_Bildanalyse/00_offene_fragen.md` Q-IS-1). Ob dafür eine Funktion gebaut wird, entscheidet Josias beim Anlegen der Rundgänge.
- Flows rückmelden, B1–B5, C1–C27, Archiv-Schalter, Zurücksetzen mit Code: später.
- D1 (Komma/Punkt) testet Josias am Tablet.

## 4. Lieferung

Wie bisher: `pakete/PAKET_26_….md` mit Kurzfassung, SharePoint (falls nötig), A/B-Teilen, Vorher-Fassungen, Test, Rückweg; Generator 0 Fehler, Mutation, **unabhängige Prüfung** vor Freigabe. Danach meldet sich Josias beim Einsetz-Chat.
