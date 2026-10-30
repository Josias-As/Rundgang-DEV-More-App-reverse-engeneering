# Prüfung Baukasten-Paket 6 – Hinweis mit Beispielbild

Export: `2026-10-27_0909`. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## a) Namenscheck (maschinell, belegt)

Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.

```
== Paket 6: 2 Properties, neue Steuerelemente: btnKaBild, conKaBild, btnKaBildSperre, conKaBildKarte, lblKaBildTitel, imgKaBild, btnKaBildSchliessen
  scrKategorie.OnVisible           ok
  lblKaFrage.Width                 ok
  btnKaBild.BorderColor            ok
  btnKaBild.BorderThickness        ok
  btnKaBild.Color                  ok
  btnKaBild.Fill                   ok
  btnKaBild.Font                   ok
  btnKaBild.Height                 ok
  btnKaBild.HoverColor             ok
  btnKaBild.HoverFill              ok
  btnKaBild.OnSelect               ok
  btnKaBild.PressedColor           ok
  btnKaBild.PressedFill            ok
  btnKaBild.RadiusBottomLeft       ok
  btnKaBild.RadiusBottomRight      ok
  btnKaBild.RadiusTopLeft          ok
  btnKaBild.RadiusTopRight         ok
  btnKaBild.Size                   ok
  btnKaBild.Text                   ok
  btnKaBild.Visible                ok
  btnKaBild.Width                  ok
  btnKaBild.X                      ok
  btnKaBild.Y                      ok
  conKaBild.Fill                   ok
  conKaBild.Height                 ok
  conKaBild.Visible                ok
  conKaBild.Width                  ok
  btnKaBildSperre.BorderThickness  ok
  btnKaBildSperre.Fill             ok
  btnKaBildSperre.Height           ok
  btnKaBildSperre.HoverFill        ok
  btnKaBildSperre.PressedFill      ok
  btnKaBildSperre.Text             ok
  btnKaBildSperre.Width            ok
  conKaBildKarte.Fill              ok
  conKaBildKarte.Height            ok
  conKaBildKarte.RadiusBottomLeft  ok
  conKaBildKarte.RadiusBottomRight ok
  conKaBildKarte.RadiusTopLeft     ok
  conKaBildKarte.RadiusTopRight    ok
  conKaBildKarte.Width             ok
  conKaBildKarte.X                 ok
  conKaBildKarte.Y                 ok
  lblKaBildTitel.Color             ok
  lblKaBildTitel.Font              ok
  lblKaBildTitel.FontWeight        ok
  lblKaBildTitel.Height            ok
  lblKaBildTitel.Size              ok
  lblKaBildTitel.Text              ok
  lblKaBildTitel.Width             ok
  lblKaBildTitel.X                 ok
  lblKaBildTitel.Y                 ok
  imgKaBild.AccessibleLabel        ok
  imgKaBild.Height                 ok
  imgKaBild.Image                  ok
  imgKaBild.ImagePosition          ok
  imgKaBild.Width                  ok
  imgKaBild.X                      ok
  imgKaBild.Y                      ok
  btnKaBildSchliessen.BorderThickness ok
  btnKaBildSchliessen.Color        ok
  btnKaBildSchliessen.Fill         ok
  btnKaBildSchliessen.Font         ok
  btnKaBildSchliessen.Height       ok
  btnKaBildSchliessen.HoverFill    ok
  btnKaBildSchliessen.OnSelect     ok
  btnKaBildSchliessen.PressedFill  ok
  btnKaBildSchliessen.Size         ok
  btnKaBildSchliessen.Text         ok
  btnKaBildSchliessen.Width        ok
  btnKaBildSchliessen.X            ok
  btnKaBildSchliessen.Y            ok
  Paket 6: colAntworten hat in allen drei Zweigen dieselben 24 Felder
```

## b) Typcheck

- `HinweisBildID` Zahl: `Coalesce(…; 0)`.
- Bild: `LookUp(RG_Hinweisbilder; ID = varBildID).Thumbnail.Large` – UNSICHER bis zum Vorab-Test 6.3 (Feldname Thumbnail in dieser Umgebung).
- Abfrage nur bei geöffnetem Fenster (`If(varBildID > 0; …)`), da versteckte Steuerelemente trotzdem rechnen.

## c) Reihenfolge

1. Bibliothek, Spalte, Datenquelle und Vorab-Test vor allen Formeln.
2. OnVisible vor dem Knopf (Feld BildID).
3. Fenster zuletzt; muss vor conKaFoto/conKaLaden liegen.

## d) Auswirkungsliste

| Stelle | betroffen | wie |
|---|---|---|
| scrKategorie.OnVisible | ja | BildID in allen Zweigen, varBildID = 0 |
| fnFehlt / fnFehltGrund | nein |  |
| btnKaSpeichern: Prüfung und Sprung | nein |  |
| JSON-Aufbau (varAntwortJSON) | nein | BildID wird nicht gespeichert |
| Mängel bei Abschluss (btnRuAbschluss) | nein |  |
| htmProtokoll | nein |  |
| Foto-Upload | nein |  |
| Lesemodus nach Abschluss | ja | Knopf auch in der Nur-Ansicht (Bild aus heutigen Stammdaten) |
| Nachlese-Vergleich | nein |  |

## e) Szenarien

| Szenario | erwartetes Ergebnis | Beleg |
|---|---|---|
| neuer Punkt ohne Daten | Knopf nur bei HinweisBildID > 0 | T6.1, T6.5 |
| alter gespeicherter Punkt (JSON ohne neues Feld) | nicht betroffen | – |
| inaktiver Punkt | unsichtbar | Code |
| Rundgang abgeschlossen (Nur-Lesen) | Bild ansehbar | T6.6 |
| Wechsel n.i.O. → i.O. → n.i.O. | nicht betroffen | – |
| Kategorie zweimal speichern | nicht betroffen | – |
| Abbruch mitten im Speichern | nicht betroffen | – |
| Netzfehler | Bild lädt nicht, Fenster bleibt bedienbar (Schließen) | geschlussfolgert |
| zwei Prüfer gleichzeitig | nicht betroffen | – |

## f) Studio-Fallen

- Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).
- `Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.
- Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.
- Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).
- Container-YAML auf dem Bildschirm einfügen; danach Ebene prüfen (ganz oben).

## g) Lauffähigkeit

- Vorab-Test 6.3 und T6.1–T6.7 in der Vorschau.

## Unabhängige Prüfung – Runde 2 und Umgang

| Befund | Umgang |
|---|---|
| P6-1 mittel: Frage wird 160 px schmaler, abgeschnitten | Knopf „Bild“ 64 px, Frage nur 80 px schmaler |
| T6.4 nicht ausführbar | entfernt, Absicherung erklärt |
| P6-3: Vorschaubilder am Tablet / Verzögerung | Hinweis in 6.2, Test T6.7 |
| P6-4: leere Bildfläche ohne Hinweis | bewusst so (Schließen geht), Test T6.6 |
| P6-5: Nur-Ansicht zeigt heutiges Bild | bewusst; Einfrieren kommt mit dem späteren Paket „Schlüssel/Status/Einfrieren“ |

## Unabhängige Prüfung – Runde 3 und Umgang

| Befund | Umgang |
|---|---|
| B1 mittel: E-05-Prüfung für das Bildfenster fehlt | Prüfliste mit den sechs Formeln in 6.6, Test T6.7 hochkant/quer |
| B7: Titel im Bildfenster abgeschnitten | Größe 16, Höhe 64, Bild ab Y 84 (Textbreite maschinell geprüft: 2 Zeilen) |

## Offene Befunde

Keine.

