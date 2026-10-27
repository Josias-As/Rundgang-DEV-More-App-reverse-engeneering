# Abgleich: Builder-Analyse ↔ Planer-Chat ↔ Josias (27.10.2026)

Bezug: `ANALYSE_Builder.md` (gleicher Ordner, bleibt unverändert). Regel von Josias: **Bei Widerspruch wiegt der Planer-Chat schwerer.**

## Ergebnis je Frage
| Nr | Meine Analyse | Planer | Josias | Gilt jetzt |
|---|---|---|---|---|
| 1 Reihenfolge | Baukasten wie geplant zuerst. Nachschlagespalten nicht vor dem Builder, eher nie. | Baukasten 1–6 zuerst. Danach ein stabiler Schlüssel je Zeile vor dem Builder. Vorschlag: Textspalte `Schluessel` (GUID), Zahlen-ID bleibt. | – | **Planer.** Baukasten 1–6 → Spalte `Schluessel` + Status + Momentaufnahme → Builder. Die Zahlen-IDs bleiben, die Rundgang-App muss nicht auf Nachschlagespalten umgebaut werden. Damit fällt mein Haupteinwand weg. |
| 2 Entwurf | (a) Kopie als Entwurf empfohlen, (c) Momentaufnahme „am saubersten, aber Umbau“ | Status `Entwurf / Aktiv / Archiviert` + Momentaufnahme der Prüfpunkte beim Start + Kopie als neue Version zum Ändern aktiver Rundgänge. Kein gesperrtes Bearbeiten. | – | **Planer** (= meine (a) + (c) zusammen). Folge: Die Rundgang-App wird einmal mehr umgebaut. Das passt in die Baukasten-Arbeit, weil 1–6 ohnehin `scrKategorie.OnVisible`/`colAntworten` anfassen. |
| 3 Pflege | Pflegegruppe mit eigenen Rechten | Pflegegruppe schreibt, Prüfer lesen | „ich und ein paar andere“ | Pflegegruppe = Josias + wenige. **Offen:** Namen (für eine SharePoint-Gruppe) |
| 4 Apps | zwei Apps, Karte als Komponente | gleich, falls die Umgebung es zulässt, sonst Karte nachbauen | fragt nach Bedeutung | gleich. Beim Anlegen prüfen, ob eine Komponentenbibliothek erlaubt ist |
| 5 Konfiguration | Frage | nicht in Version 1 | Builder = nur Rundgänge: Fenster „alle Rundgänge“ + Fenster „neuen Rundgang bauen“ | **übereinstimmend:** keine Konfiguration im Builder |
| 6 Excel | Frage | Frage, bei Excel Import zuerst | – | **offen** bei Josias |
| 7 Dateien | Frage | Paket `C:\rundgang_work\UEBERGABE_PAKET.zip` (138 Dateien) | – | Josias lädt die ZIP hier hoch |

## Neue Punkte zum Mitnehmen (geschlussfolgert)
- **Status statt `Aktiv`:** Die Rundgang-App filtert heute `RG_Rundgaenge` auf `Aktiv = true` (`scrStart.OnVisible`). Entweder wird `Aktiv` beim Statuswechsel mitgesetzt (keine Änderung an der Rundgang-App) oder der Filter wechselt auf `Status = "Aktiv"`. Ich empfehle das Mitsetzen in Version 1.
- **Größe der Momentaufnahme:** Hängt die Momentaufnahme aller Prüfpunkte an der Durchführung (wie `KategorieListe`), kann der JSON-Text bei großen Rundgängen lang werden. Die Grenze der SharePoint-Mehrzeilenspalte ist UNSICHER. Vor dem Bau messen. Ausweichweg: Momentaufnahme je Kategorie.
- **Aktivieren einer neuen Version:** Der alte Rundgang wird „Archiviert“, der neue „Aktiv“, die Planzeilen werden umgehängt (`RundgangID`). Laufende Durchführungen des Tages sind durch die Momentaufnahme geschützt.
- **Josias' Bild vom Builder** (zwei Fenster) passt zum Plan: „Alle Rundgänge“ (Liste, Status, Kopieren/Neue Version, Aktivieren, Archivieren) und „Rundgang bauen“ (Bereiche → Kategorien → Prüfpunkte → Plan → Prüfbericht). Bearbeitet wird nur, was im Status Entwurf ist.
