# Paket 24 – leichte unabhängige Prüfung (06.11.2026)

Prüf-Agent (Paketdokument bis „Anhang“, dazu `pakete/builder/scrEditor.yaml`). 5 Befunde (1 mittel, 4 niedrig). Ohne Befund: Syntax/Klammern, kein Zirkelbezug (`imgKaInfo.Y` ← `lblKaInfoText`), Bild endet 16 px über „Schließen“ in allen Fällen, Meldung bei gelöschter Anleitung ohne Bild, `varInfoID` als Flag konsistent, Builder-Layout in `conPRest` ohne Überlappung.

| Befund | Umgang |
|---|---|
| 1 `Set(varInfo; Blank())` (Typ) | ein einziges `Set(varInfo; If(ThisItem.AnlID > 0; LookUp(…)))`. |
| 2 lange Frage im Titel abgeschnitten | Titel bei „nur Bild“ = „ⓘ Beispielbild“; die Zeile „zu: <Frage>“ bleibt sichtbar (keine Änderung an `lblKaInfoFrage.Visible`). |
| 3 negative Bildhöhe bei „nur Text“ | `Max(…; 0)`. |
| 4 Tests/Doku | T2 mit langer Frage, T5b (gelöscht, kein Bild), T5c (Löschen `btnKaBild`/`conKaBild`), „Kurz erklärt“ für alle Builder-Schritte. T5: inaktive Anleitung → `AnlID` 0 ist belegt (Paket 13, `colAnlAktivApp`). |
| 5 Altlast nach Löschen | Rest-Variable `varBildID` in `scrKategorie.OnVisible` ist unschädlich; Aufräum-Paket C. |

Nach der Einarbeitung: baukasten 0 Fehler, Mutation 12/12; builder unverändert 0 Fehler, 13/13.
