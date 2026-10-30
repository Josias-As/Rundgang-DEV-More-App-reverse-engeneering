# Prüfung Rundgang-Builder

Stand 30.10.2026. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## Maschinell (belegt)
- `werkzeuge/builder.py` → `arbeit/2026-10-30_Builder/pruefung.txt`: **0 Fehler**. Geprüft werden:
  - Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich.
  - Jeder Name ist bekannt, jede Variable hat einen Startwert in App.OnStart, jede Sammlung wird gefüllt, jedes Steuerelement und jeder Bildschirm ist vorhanden.
  - Jedes Patch-Feld ist eine Spalte der Liste, Auswahlspalten werden als `{Value: …}` geschrieben.
  - Die Argumentanzahl der Funktionen stimmt, Felder nach einem Punkt sind bekannt.
  - Die YAML-Dateien lesen sich zeichengleich zurück, die Textbreiten sind geschätzt.
- Mutationstest `werkzeuge/mutation_builder.py`: **10/10** absichtlich eingebaute Fehler werden gefunden (`arbeit/2026-10-30_Builder/mutation.txt`).
- Logik-Gegenprobe `werkzeuge/logik_builder.py`: **27 Szenarien ohne Fehler** – Python-Nachbildung der Abläufe (Vorbereiten, neue Fassung, Kopie mit Bedingungen, Aktivieren, halbes Aktivieren, veraltetes Fenster, Verwerfen, Kopierfehler, Reaktivieren, Kopie als neuer Rundgang, Vorlagen) gegen die Leselogik der Rundgang-App (`btnRgAktion`, `scrKategorie.OnVisible`). Belegt damit die Datenlogik, nicht die Power-Fx-Schreibweise.
- Sichtprüfung `werkzeuge/vorschau_builder.py`: Die Bildschirme werden mit den echten Positionen nachgezeichnet (`arbeit/2026-10-30_Builder/vorschau_*.png`, Zustand „Prüfpunkt Zahl gewählt, beschreibbar“). **0 Überlappungen** gleichzeitig sichtbarer Steuerelemente, alle Knöpfe frei, das Prüfpunkt-Formular passt in die Höhe. Formeltexte sind dort Platzhalter, Farben nur angedeutet.
- Paket 7: Generator ohne Fehler, Mutationstest Baukasten 9/9, Logik-Gegenprobe 81 Szenarien ohne Fehler.

## Unabhängige Prüfung (ein Prüfer, 30.10.) und Umgang
Der Prüfer fand keine Formel, die in Studio sicher rot wird. Er hat Schemas, ForAll, Funktionen und Property-Namen durchgesehen. Die Rundgang-App bleibt im Normalfall korrekt: Eine laufende Durchführung arbeitet nach dem Aktivieren mit der alten Fassung weiter (belegt über `btnRgAktion` und `scrKategorie.OnVisible`).

| Nr | Befund | Schwere | Umgang |
|---|---|---|---|
| 1 | Ein veralteter Entwurf (zweites Fenster/Gerät) schreibt nach dem Aktivieren in die jetzt aktive Fassung | hoch | **Behoben.** Vor jedem Schreiben wird frisch geprüft, ob `EntwurfFassung` noch der offenen Fassung entspricht (`CHECK`, Variable `varEntwurfOk`). Das gilt für Feldänderungen, Neu, Entfernen, ↑↓, Duplizieren, Verschieben, Holen und Mehrere. Sonst wird nichts geschrieben, der Editor wechselt auf Lesen, und es kommt eine Meldung. Beim Laden zeigt der Editor einen nicht mehr offenen Entwurf nur zum Lesen. Jede Schreibstelle prüft zusätzlich `RundgangID` und `Fassung` der Zeile. |
| 2 | Halb fertiges Aktivieren, danach löscht „Entwurf verwerfen“ die live laufende Fassung | mittel | **Behoben.** „Entwurf verwerfen“ löscht nur, wenn kein Bereich dieser Fassung aktiv ist (frisch gelesen), sonst kommt eine Meldung. Erkennt das Aktivieren oder das Laden einen Zwischenstand, wechselt der Editor auf Lesen. Er zeigt „Aktivieren unvollständig“, und nur „Aktivieren …“ bleibt bedienbar (`varAktivRest`). |
| 3 | „Reaktivieren“ setzt bei Altbestand die Fassung auf 1, dadurch wird nie vorbereitet | mittel | **Behoben.** Reaktivieren setzt nur noch Status und Aktiv. |
| 4 | Auswahllisten finden ihren Standardwert über den Anzeigetext: gleiche Namen → falscher Standardwert → stilles Verschieben (UNSICHER, falls `OnChange` beim Standardwert auslöst) | mittel | **Behoben.** Bei gleichen Namen wird „(#ID)“ angehängt (Bereich, Kategorie, Bedingungsfrage). Eine ungültige Bedingungsfrage und ein unpassender Bedingungswert erscheinen als eigener Eintrag „(ungültig)“ bzw. „(passt nicht)“ und werden nicht still überschrieben. |
| 5 | Neue Fassung mit Kopierfehlern wird trotzdem als Entwurf geöffnet | mittel | **Behoben.** Gibt es beim Anlegen einer neuen Fassung oder eines kopierten Rundgangs Fehler, werden die Zeilen der neuen Fassung gelöscht. Bei einer neuen Fassung wird `EntwurfFassung` auf 0 zurückgesetzt, dann geht es zurück zur Übersicht. Abgesichert ist, dass nie die aktive Fassung gelöscht wird. |
| 6 | `patch_feld` schreibt per `varAuswahlID` ohne Prüfung von Ebene und Fassung | niedrig–mittel | **Behoben.** Es wird nur geschrieben, wenn die Ebene passt. Der Datensatz wird über `ID && RundgangID && Fassung` gelesen. Ein Treffer außerhalb des Entwurfs ist damit ausgeschlossen. Die Reihenfolge der Ereignisse bleibt UNSICHER U5 (Test T5). |
| 7 | Die Fassungsnummer wird nur aus den Bereichen bestimmt | niedrig | **Behoben.** Höchster Wert aus Bereichen, Kategorien und Prüfpunkten (sortiert gelesen, eine Zeile je Liste). |
| 8a | Namensänderung im Entwurf ist sofort live | niedrig | Meldung „Der Name gilt sofort, auch für die aktive Fassung“. In der Anleitung beschrieben. |
| 8b | Das Lade-Fenster hat keinen Ausweg, wenn der Zeitgeber nicht startet (UNSICHER) | niedrig | **Behoben:** Im Editor steht unter „Bitte warten …“ der Knopf „Zur Übersicht“ (setzt den Ablauf zurück). Ein abgebrochener Ablauf ist gefahrlos, weil Schreibprüfung und Zurücknehmen wirksam bleiben. |
| 8c | Kurz „keine aktiven Kategorien“ beim Start während des Umschaltens | – | So gewollt (Reihenfolge erst aus, dann an). |

## Offen
- Nicht in Studio getestet, siehe UNSICHER U1–U7 und den Testbogen in `EINBAU_BUILDER.md`.
- Nach den Korrekturen keine zweite unabhängige Prüfung. Auf Wunsch eine gezielte Runde auf die geänderten Stellen (`CHECK`, `STUFE_LADEN`, `STUFE_KOPIE`, `LI_VERWERFEN`).
