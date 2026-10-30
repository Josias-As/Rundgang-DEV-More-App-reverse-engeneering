# Prüfung Baukasten-Paket 7 – Foto „Bei Mangel Pflicht“

Export: `2026-10-27_0909`. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## a) Namenscheck (maschinell, belegt)

Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.

```
== Paket 7: 4 Properties, neue Steuerelemente: -
  App.Formulas                     ok
  btnKaFoto.Visible                ok
  btnKaFoto.Text                   ok
  lblKaFotoHinweis.Text            ok
  Paket 1: colAntworten hat in allen drei Zweigen dieselben 19 Felder
  Paket 2: colAntworten hat in allen drei Zweigen dieselben 19 Felder
  Paket 3: colAntworten hat in allen drei Zweigen dieselben 20 Felder
  Paket 4: colAntworten hat in allen drei Zweigen dieselben 23 Felder
  Paket 5: colAntworten hat in allen drei Zweigen dieselben 23 Felder
  Paket 6: colAntworten hat in allen drei Zweigen dieselben 24 Felder
  Paket 7: colAntworten hat in allen drei Zweigen dieselben 24 Felder
Aufrufe fnFehlt im Endstand: btnKaSpeichern.OnSelect, conKaKarte.BorderColor, conKaKarte.BorderThickness, lblKaFehlend.Text, lblKaFehlendAnzahl.Text
Textbreiten (Segoe UI, Schätzung je Zeichenart, Punkt -> Pixel x 1,333):
  btnKaFoto                     122 px (+10 %) / 124 px, 1 Zeile(n) nötig, erlaubt 1  ok  '📷 Foto (10)'
  btnKaFoto                      93 px (+10 %) / 124 px, 1 Zeile(n) nötig, erlaubt 1  ok  '📷 Foto *'
  lblKaFotoHinweis              536 px (+10 %) / 670 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren.'
  lblKaFotoHinweis              632 px (+10 %) / 670 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Keine Personen fotografieren. Fotos werden beim „Speichern“ hochgeladen.'
  addKaFoto                     343 px (+10 %) / 660 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Foto aufnehmen / auswählen'
  txtKaKommentar (Hinweis)      341 px (+10 %) / 500 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Kommentar zum Mangel (Pflicht)'
  txtKaKommentar (Hinweis)      207 px (+10 %) / 500 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Kommentar (Pflicht)'
  lblKaZahlInfo                 653 px (+10 %) / 454 px, 2 Zeile(n) nötig, erlaubt 2  ok  'Betriebsstunden  ·  Soll ab 1000 bis 99999  ·  außerhalb des Sollbereichs'
  lblKaZahlInfo                 649 px (+10 %) / 454 px, 2 Zeile(n) nötig, erlaubt 2  ok  'Betriebsstunden  ·  Soll ab 1000 bis 99999  ·  außerhalb, bitte begründen'
  lblKaZahlInfo                 620 px (+10 %) / 454 px, 2 Zeile(n) nötig, erlaubt 2  ok  'Betriebsstunden  ·  Soll ab 1000 bis 99999  ·  unzulässig, bitte prüfen'
  cboKaMehrfach (Platzhalter)   307 px (+10 %) / 400 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Auswählen (mehrere möglich)'
  btnKaBild                      33 px (+10 %) / 44 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Bild'
  btnKaDatumLeeren               29 px (+10 %) / 36 px, 1 Zeile(n) nötig, erlaubt 1  ok  '✕'
  btnKaBildSchliessen           107 px (+10 %) / 180 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Schließen'
  lblKaFotoHinweis              559 px (+10 %) / 670 px, 1 Zeile(n) nötig, erlaubt 1  ok  'Mangel: mindestens ein Foto Pflicht. Keine Personen fotografieren.'
  lblKaBildTitel                734 px (+10 %) / 670 px, 2 Zeile(n) nötig, erlaubt 2  ok  'Beispiel – ZZ Test Thermometer Serverraum (Foto der Anzeige) prüfen'

Fehler gesamt: 0

  Paket 7: colAntworten hat in allen drei Zweigen dieselben 24 Felder
```

## b) Typcheck

- `Foto` bleibt eine Auswahlspalte, gelesen nur über `fnFotoModus(p.Foto.Value; …)`. Der neue Text „Bei Mangel Pflicht“ wird dort auf den internen Wert `BeiMangel` abgebildet; alle anderen Stellen vergleichen nur `FotoModus`.
- Kein neues Feld in colAntworten (Schema in allen drei Zweigen unverändert, maschinell geprüft).

## c) Reihenfolge

1. Auswahlwert in SharePoint und Daten aktualisieren.
2. App.Formulas.
3. Knopf und Hinweis.

## d) Auswirkungsliste

| Stelle | betroffen | wie |
|---|---|---|
| App.Formulas (fnFotoModus, fnFehltGrund) | ja | neuer Wert, Foto-Pflicht nur bei NIO |
| btnKaSpeichern: Prüfung und Sprung | ja (über fnFehlt) | Foto fehlt bei n.i.O. |
| btnKaFoto.Visible/Text, lblKaFotoHinweis | ja | Knopf erst bei n.i.O., Stern, Hinweis |
| Foto-Upload (fnFotoNeuErlaubt) | nein | BeiMangel lädt nur bei n.i.O. hoch (wie Aus) |
| JSON, Mängel, Protokoll | nein |  |

## e) Szenarien

| Szenario | erwartetes Ergebnis | Beleg |
|---|---|---|
| neuer Punkt ohne Daten | kein Knopf, nichts offen | T7.1 |
| alter gespeicherter Punkt (JSON ohne neues Feld) | unverändert | – |
| inaktiver Punkt | FotoModus Aus (dritter Zweig) | Code |
| Rundgang abgeschlossen (Nur-Lesen) | Knopf nur bei gespeicherten Fotos | Code |
| Wechsel n.i.O. → i.O. → n.i.O. | Pflicht folgt der Bewertung | T7.3, T7.6 |
| Kategorie zweimal speichern | nicht betroffen | – |
| Abbruch mitten im Speichern | nicht betroffen | – |
| Netzfehler | nicht betroffen | – |
| zwei Prüfer gleichzeitig | nicht betroffen | – |

Logik-Gegenprobe der Funktionen (`werkzeuge/logik_probe.py`, Python-Nachbildung der Formeln, keine Ausführung von Power Fx):

```
P7  ok    fnFotoModus: Bei Mangel Pflicht -> BeiMangel                           erwartet 'BeiMangel'  ist 'BeiMangel'
P7  ok    Bei Mangel Pflicht, i.O., kein Foto -> vollständig                     erwartet ''           ist ''
P7  ok    Bei Mangel Pflicht, n.i.O. mit Kommentar, kein Foto -> Foto            erwartet 'Foto'       ist 'Foto'
P7  ok    Bei Mangel Pflicht, n.i.O. mit Kommentar und Foto -> vollständig       erwartet ''           ist ''
P7  ok    Bei Mangel Pflicht, n.i.O. ohne Kommentar -> Kommentar zuerst          erwartet 'Kommentar'  ist 'Kommentar'
P7  ok    Bei Mangel Pflicht, Zahl außerhalb (Mangel) mit Kommentar ohne Foto -> Foto erwartet 'Foto'       ist 'Foto'
P7  ok    Bei Mangel Pflicht, Zahl außerhalb bei Warnen (i.O.) -> kein Foto nötig erwartet ''           ist ''
P7  ok    Bei Mangel Pflicht, unbeantwortet optional -> nichts fehlt             erwartet ''           ist ''
P7  ok    fnFotoNeuErlaubt: i.O. und BeiMangel -> nein                           erwartet False        ist False
P7  ok    fnFotoNeuErlaubt: n.i.O. und BeiMangel -> ja                           erwartet True         ist True
```

## f) Studio-Fallen

- Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).
- `Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.
- Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.
- Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).
- Den Auswahlwert in SharePoint genau als „Bei Mangel Pflicht“ anlegen (sonst gilt er als leer → FotoMoeglich).

## g) Lauffähigkeit

- T7.1–T7.7 in der Vorschau. Logik-Gegenprobe: 10 neue Szenarien (P7), frühere Szenarien unverändert.

## Offene Befunde

Keine.

