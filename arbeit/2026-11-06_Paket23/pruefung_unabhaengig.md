# Paket 23 – leichte unabhängige Prüfung (06.11.2026)

Prüf-Agent (nur das Paketdokument gelesen, auf Josias' Wunsch „leicht“). 14 Befunde, davon 1 hoch, 7 mittel, 6 niedrig. Ohne Befund: Klammern/Trennzeichen aller Blöcke, With/If-Struktur, Index() bei leerer Liste abgesichert, Coalesce auf nie gesetztem `varOffenNr`, Delegation, Präzedenz von `in`, ShowColumns mit Bezeichnern, Vorher/Nachher-Diffs.

## Einarbeitung

| Befund | Umgang |
|---|---|
| 1 T1 hängt an `TestDatensatz` der Läufe 18, 20–22 | Laut Josias' Konsolenabfrage `TestDatensatz` = true. T1 präzisiert. |
| 2 `varOffenNr` nie zurückgesetzt | `Set(varOffenNr, 1)` am Ende von `btnStartTagLaden.OnSelect`. Text und „Öffnen“ lesen dieselbe Formel (konsistent). |
| 3 Sortierung nicht stabil / Text-Sort | `TagText` ist ISO `yyyy-mm-dd` (belegt: `Text(varTag, "yyyy-mm-dd")`), Text-Sort ist zeitlich richtig. Zweiter Schlüssel `ID` ergänzt (`SortByColumns(…, "TagText", …, "ID", …)`). |
| 4, 5, 11, 13 | ohne Handlungsbedarf (bestätigt). |
| 6 Spalte in den Sammlungen | belegt: App `colRundgaenge = Filter(RG_Rundgaenge, Aktiv = true)` (alle Spalten), Builder `colRg = RG_Rundgaenge` (alle Spalten). Kein Schritt nötig. |
| 7 (hoch) Lesen ohne Refresh in `btnPlTest` | `Refresh(RG_Rundgaenge)` vor dem `LookUp` ergänzt. `Patch(colRg, …, varPlanRg)`: gleiche Quelle, gleiches Schema. |
| 8 Überlappung im Plan-Kopf | belegt: `lblPlTitel` 172–1072, `btnPlTest` ab 1130 (bei 1366). Plan wird nur mit gewähltem Rundgang geöffnet. |
| 9 Format von `Ansprechpartner` | belegt: `NIO_TOGGLE` schreibt IDs mit `;` ohne Leerzeichen. Kein Schritt nötig. |
| 10 Inaktive versehentlich hinzufügen | belegt: Inaktive erscheinen nur, wenn eingetragen; `NIO_TOGGLE` entfernt eingetragene → nur Entfernen möglich. |
| 12 weitere Leser von `colKontakte` | belegt (builder.py): nur `galNioKontakte`, `btnNioKontakt`, `lblNioLeer`. |
| 14 Doku | `lblKoNutzung` „kurzzeitig rot bis B2.8“ angekündigt; T2 mit Hinweis, wie zwei offene Läufe entstehen; T4 als bestehendes Verhalten markiert. |

Nach der Einarbeitung: baukasten 0 Fehler, builder 0 Fehler, Dokument neu erzeugt.
