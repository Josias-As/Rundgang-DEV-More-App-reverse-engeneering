# Paket 11 + 18 – leichte unabhängige Prüfung (06.11.2026)

Prüf-Agent (nur Paketdokumente bis „Anhang“). 13 Befunde: 3 mittel, 10 niedrig. Ohne Befund: IfError nur als Kettenglied, Sperren an Prüferwahl/Start, Builder-Teil 11, Record-Literale (`CodeID` in allen drei Zweigen), Code nie in JSON/Protokoll/PDF/Mängeln, Position 🔑/ⓘ/Bild, Data-URI `Mid(j; 2; Len(j) - 2)`, Suche nur bei offenem Fenster, Protokoll-HTML mit `fnHtml`, IT-Schritte.

## Einarbeitung

| Befund | Umgang |
|---|---|
| 1 Select durch `varSperreBis` verschluckt | `btnRuUOk` setzt `varSperreBis` auf `Now()` vor `Select(btnRuAbschluss)`. |
| 2 großes Bild in `RG_Durchfuehrungen` | Eigene Liste **`RG_Unterschriften`** (Title, DurchfuehrungID, Bild); das Protokoll liest das Bild per `LookUp`. Spalte `UnterschriftBild` entfällt. |
| 3, 11 rote Zwischenzustände | in beiden Dokumenten angekündigt. |
| 4 kein Guard ohne Prüfer | `btnRuAbschluss`: ohne Prüfer Meldung statt Unterschrift. Speichern: nicht nötig (Startseite verdeckt alles ohne Prüfer). |
| 5 `Now()` in Anzeige | Anzeige nur Datum (`Today()`), Uhrzeit kommt beim Speichern. |
| 6 Fenster bleibt nach Fehler offen | `btnRuAbschluss` schließt das Fenster am Ende immer. |
| 7 Dubletten über Geräte | `Refresh(RG_Pruefer)` und `LookUp(RG_Pruefer; Email = Lower(…))` vor dem Anlegen. |
| 8 Prüfer ohne E-Mail | Liste zeigt nur Einträge mit E-Mail. |
| 9, 10 Tests | Vorab-Tests V1–V4 in die Tabelle; T10–T13 (Flow aus, Doppeltippen, Wechsel im Lauf, „Weiter ›“ ohne Prüfer) ergänzt. |
| 12 Refresh vor Code-Lesen | `Refresh(RG_Zugangscodes)` in `btnKaCode`. |
| 13 Patch auf gelöschten Code / Kürzung Hinweis | Patch nur bei vorhandener Zeile; Hinweis (mehrzeilig) ohne `Left(…; 255)`. |

Nach der Einarbeitung: baukasten 0 Fehler, builder 0 Fehler, Mutation 12/12 und 13/13. Dokumente neu erzeugt.
