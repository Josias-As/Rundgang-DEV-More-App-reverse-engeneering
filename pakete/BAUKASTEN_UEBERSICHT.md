# Baukasten-Pakete 1–6 – Übersicht

> **ENTWURF.** Erzeugt aus dem Export 27.10. 08:24 mit einer Simulation der Änderung von 08:44 (`UpdateIf(colAntworten; Bewertung <> "NIO"; {Kommentar: ""})`). Vor dem Einfügen: frischen Export hochladen, `python3 -I werkzeuge/baukasten.py <Schlüssel>` ohne Simulation laufen lassen. Bricht er nicht ab, gelten die Blöcke für den echten Stand.

## Reihenfolge

Pakete **nur in dieser Reihenfolge**, jedes ganz (atomar), nach jedem Paket App-Prüfung = 0, Test, speichern. Erst nach Paket 1 und erfolgreichem Test weitermachen.

| Paket | Inhalt | SharePoint | Properties | neue Steuerelemente |
|---|---|---|---|---|
| 1 | Foto-Modus pro Prüfpunkt (Aus / Optional / Pflicht) | Foto (Auswahl) | 24 | – |
| 2 | Pflicht-Kommentar auch bei i.O. (pro Prüfpunkt) | KommentarPflicht (Ja/Nein) | 5 | – |
| 3 | Zahlengrenzen pro Prüfpunkt: Mangel, Warnen oder Sperren | Grenzmodus (Auswahl) | 5 | – |
| 4 | Bedingte Fragen | BedingungPunkt (Zahl), BedingungWert (Text) | 10 | – |
| 5 | Neue Typen: Mehrfachauswahl, Datum, Datum + Uhrzeit | Eingabetyp + 3 Werte | 1 | cboKaMehrfach, dpKaDatum, ddKaStunde, ddKaMinute |
| 6 | Hinweis mit Beispielbild | Bibliothek RG_Hinweisbilder, HinweisBildID (Zahl) | 2 | btnKaBild, conKaBild, btnKaBildSperre, conKaBildKarte, lblKaBildTitel, imgKaBild, btnKaBildSchliessen |

## Entscheidungen und Annahmen (bitte bestätigen)

- **Foto-Pflicht gilt immer**, auch wenn der Punkt selbst nicht Pflicht ist (Nachweis, z. B. Thermometer).
- **n.i.O. erlaubt immer Fotos** (wie bisher), auch bei Foto = Aus.
- **Kommentarpflicht greift, sobald der Punkt beantwortet ist** (bei optionalen, unbeantworteten Punkten nicht).
- **Grenzmodus Warnen** = i.O. mit Pflicht-Begründung, kein Mangel. **Sperren** = Wert außerhalb lässt sich nicht speichern.
- **Bedingte Fragen nur eine Ebene tief**, A in derselben Kategorie. Falsch eingerichtete Bedingungen zeigen B immer (sicherer Ausfall). Der Builder soll das später beim Anlegen verhindern.
- **Datum/Uhrzeit als Text** „TT.MM.JJJJ [hh:mm]“ in WertText (keine Zeitzonen-Fallen, Protokoll und Mängel unverändert).
- **Beispielbild als Fenster** statt aufklappbar in der Karte.

## Vorschlag (nicht gebaut): Paket „Flows rückmelden“

Die Flows antworten nicht (Antwort-Aktion wäre Premium). Folge: Scheitert ein Upload oder das PDF nach dem Start, merkt die App es nicht; bei Foto-Pflicht gilt das Foto als vorhanden. Vorschlag ohne Premium: (1) RG_Foto_hochladen schreibt nach „Datei erstellen“ mit der Standard-Aktion **Element aktualisieren** nichts zurück, sondern die App prüft beim **Abschluss** gegen die Bibliothek RG_Fotos (Datenquelle, Filter `DurchfuehrungID`), ob jede verlinkte Datei existiert, und meldet fehlende; (2) RG_Protokoll_archivieren schreibt am Ende per **Element aktualisieren** `ProtokollUrl` und `ProtokollErstelltAm` in RG_Durchfuehrungen, die App setzt die URL nicht mehr selbst und zeigt „Archivieren läuft …“, bis die Nachlese die URL findet. Das ist ein eigenes Paket mit Flow-Änderung (Josias' Konto) und gehört nicht zu 1–6.

## Dateien

- `PAKET_n_*.md` – zum Einfügen (Kurzfassung, Schritte, Blöcke deutsch, YAML, Test, Rückweg, Vorher-Fassungen)
- `PRUEFUNG_n_*.md` – Prüfung a–g, Szenarien, offene Befunde
- `stand_baukasten.json` – maschineller Stand (alle Blöcke englisch, vorher/nachher)
- Erzeugt mit `werkzeuge/baukasten.py`, `werkzeuge/doc_baukasten.py`, `werkzeuge/baukasten_text.py`; Gegenprobe `werkzeuge/logik_probe.py`.

## Hinweise des Generators

- SIMULATION: UpdateIf von 08:44 vor Set(varAntwortJSON eingefügt (nur Entwurf).

## Stand bei Arbeitsende 27.10.2026 (auf Josias' Wunsch angehalten)

**Nicht einsetzbereit.** Offen:
1. Frischer Export nach 08:44 fehlt (Blöcke beruhen auf Simulation).
2. Unabhängige Prüfung: Paket 1 (2 mittel, 7 niedrig), Paket 2+3 (4 mittel, 8 niedrig) und Paket 4 (3 mittel, 9 niedrig) liegen vor, sind aber **noch nicht eingearbeitet**. Die Prüfung für Paket 5+6 wurde abgebrochen. Berichte: `arbeit/2026-10-27_Baukasten/pruefung_unabhaengig/`.
3. Geplante Korrekturen (noch nicht umgesetzt):
   - „Kommentar leeren“ nur für aktive Punkte (`!Inaktiv`).
   - Foto-Knopf auch, wenn alte Links vorhanden sind.
   - Hinweis im Foto-Fenster in der Nur-Ansicht.
   - Prüfen, ob SharePoint den Standardwert „Aus“ auch in vorhandene Zeilen schreibt.
   - Sperren: Regel „nur Tippfehler-Grenzen“, Schutz bei Min > Max, Beschriftung „zulässig“.
   - Warnen: JSON-Feld `Warnung`, orange im Protokoll und in der Nur-Ansicht.
   - `clrWarnungHell` entfernen.
   - Bedingte Fragen: Fotos ausgeblendeter Punkte leeren und nicht anhängen; Bedingungswert gegen die möglichen Werte von A prüfen (sonst B zeigen); i.O./n.i.O. als Schreibweise annehmen.
   - Testbögen 1–4 als ausführbare Zeitachse (Vorschau ohne Foto / Tablet mit Foto).
