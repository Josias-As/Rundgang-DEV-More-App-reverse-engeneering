# Prüfung Baukasten-Paket 1 – Foto-Modus pro Prüfpunkt (Aus / Optional / Pflicht)

Export: `2026-10-27_0724` – **Simulation der Änderung von 08:44, vor dem Einfügen mit dem frischen Export wiederholen**. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## a) Namenscheck (maschinell, belegt)

Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.

```
== Paket 1: 24 Properties, neue Steuerelemente: -
  App.Formulas                     ok
  scrKategorie.OnVisible           ok
  txtKaZahl.OnChange               ok
  conKaKarte.BorderColor           ok
  conKaKarte.BorderThickness       ok
  conKaKarte.Height                ok
  lblKaAbstand.Y                   ok
  txtKaKommentar.Visible           ok
  btnKaFoto.Visible                ok
  btnKaFoto.Y                      ok
  btnKaFoto.Text                   ok
  btnKaFoto.BorderColor            ok
  btnKaFoto.Color                  ok
  btnKaFoto.HoverColor             ok
  btnKaFoto.PressedColor           ok
  btnKaFoto.HoverFill              ok
  btnKaFoto.PressedFill            ok
  lblKaFehlendAnzahl.Text          ok
  lblKaFehlend.Text                ok
  btnKaSpeichern.OnSelect          ok
  lblKaFotoHinweis.Text            ok
  addKaFoto.Size                   ok
  imgKaFotoNeu.Y                   ok
  imgKaFotoNeu.Height              ok
  Paket 1: colAntworten hat in allen drei Zweigen dieselben 19 Felder
```

## b) Typcheck

- `Foto` ist eine Auswahlspalte: gelesen nur als `p.Foto.Value` / `pp.Foto.Value` (maschinell geprüft: kein Zugriff ohne `.Value`).
- `FotoMoeglich` (Ja/Nein) nur mit `Coalesce(…; false)` (maschinell geprüft).
- Leere Auswahl liefert Blank: `fnFotoModus` vergleicht nur mit den drei Werten, alles andere fällt auf FotoMoeglich zurück (belegt durch Logik-Probe).
- `fnFehlt`/`fnFehltGrund` haben 12 Parameter; jeder Aufruf im Endstand hat 12 Argumente (maschinell gezählt, 5 Aufrufer).
- Typen der Argumente: Typ/Bewertung/WertText/Kommentar/FotoModus/Grenzmodus Text, Pflicht/KommentarPflicht Boolean, WertZahl/MinWert/MaxWert/Fotoanzahl Number – so in allen drei Zweigen von colAntworten angelegt.
- **Schema von colAntworten:** alle drei Datensatz-Literale (Nur-Ansicht, Bearbeiten, deaktivierte) haben dieselben 19 Felder (maschinell). Im Export hatte der Bearbeiten-Zweig 16 statt 17 Felder – genau `FotoMoeglich` fehlte (maschinell belegt). Das war die Ursache des Fehlers vom 27.10.
- `fnZahlBewertung` hat einen 4. Parameter, der in Paket 1 nicht benutzt wird. UNSICHER, ob Studio einen unbenutzten Parameter anmahnt (kein Fehler erwartet, App-Prüfung Schritt 1.10 zeigt es).

## c) Reihenfolge

1. Spalte `Foto` anlegen und Datenquelle aktualisieren **vor** OnVisible (liest `p.Foto.Value`).
2. App.Formulas vor oder nach den Aufrufern: dazwischen stehen rote Fehler, weil sich die Anzahl der Parameter ändert. Das Paket ist nur als Ganzes gültig (atomar), App-Prüfung erst am Ende.
3. colAntworten wird in OnVisible mit allen Feldern angelegt, bevor ein Aufrufer sie liest (Karte, Labels, Speichern laufen erst nach OnVisible).
4. Kein Schritt hängt von Paket 2–6 ab. `KommentarPflicht`/`Grenzmodus` sind feste Werte (false/"Mangel"), ihre Spalten kommen erst in Paket 2/3.

## d) Auswirkungsliste

| Stelle | betroffen | wie |
|---|---|---|
| scrKategorie.OnVisible | ja | FotoModus, KommentarPflicht, Grenzmodus in allen drei Zweigen; FotoMoeglich nur noch als Rückfall in fnFotoModus |
| fnFehlt / fnFehltGrund | ja | neue Regel „Foto“ (nur bei FotoModus Pflicht und 0 Fotos); alte Regeln zeichengleich übernommen, Rückwärtsgleichheit für alle 1.296 alten Kombinationen belegt |
| btnKaSpeichern: Prüfung und Sprung | ja | Prüfung über lblKaFehlendAnzahl (enthält jetzt Foto-Pflicht), Sprung mit derselben Regel |
| JSON-Aufbau (varAntwortJSON) | nein | ShowColumns unverändert, kein neues Feld im JSON |
| Mängel bei Abschluss (btnRuAbschluss) | nein | liest nur NIO-Zeilen aus dem JSON, unverändert |
| htmProtokoll | nein |  |
| Foto-Upload (btnKaSpeichern F1/F2) | ja | Bedingung `a.Bewertung = "NIO" || a.FotoModus <> "Aus"` statt LookUp(colPP).FotoMoeglich, an allen 3 Stellen (Upload, Fehlerzählung, Meldung) |
| Lesemodus nach Abschluss | ja | Foto-Knopf nur bei gespeicherten Fotos; Kommentar sichtbar, wenn gespeichert oder n.i.O. |
| Nachlese-Vergleich | nein | unverändert, JSON gleich aufgebaut |
| Kommentar leeren (08:44) | ja | Bedingung über fnKommentarNoetig, in Paket 1 gleiches Ergebnis wie `Bewertung <> "NIO"` (Logik-Probe) |
| Kartenhöhe, lblKaAbstand | ja | Zeile unter der Eingabe erscheint, wenn Kommentar oder Foto-Knopf sichtbar ist; Abstand folgt der Kartenhöhe (vorher fehlte er bei Foto ohne n.i.O.) |
| Foto-Zähler btnKaFoto.Text | ja | zählt neue Fotos ohne `Uebernommen` + gespeicherte Links; vorher doppelt gezählt nach fehlgeschlagenem Speichern |

## e) Szenarien

| Szenario | erwartetes Ergebnis | Beleg |
|---|---|---|
| neuer Punkt ohne Daten | FotoModus aus der Spalte; bei Pflicht „(Foto)“ offen, sonst wie bisher | Logik-Probe P1, T1.1–T1.3 |
| alter gespeicherter Punkt (JSON ohne neues Feld) | JSON hat kein Foto-Feld, FotoModus kommt aus den Stammdaten; gespeicherte Links zählen als Fotos (Pflicht erfüllt) | OnVisible Bearbeiten-Zweig, fnLinkAnzahl, T1.9 |
| inaktiver Punkt | FotoModus "Aus", ausgeblendet, zählt nicht (Filter `!Inaktiv`), Foto-Pflicht greift nicht | Code |
| Rundgang abgeschlossen (Nur-Lesen) | keine Pflicht-Prüfung, Foto-Knopf nur mit gespeicherten Fotos, keine Uploads | Code, T1.11 |
| Wechsel n.i.O. → i.O. → n.i.O. | Foto-Knopf rot → (bei Aus) verschwindet / (bei Optional/Pflicht) blau → rot; schon gewählte Fotos bleiben in colFotos; Upload nur, wenn beim Speichern n.i.O. oder Modus ≠ Aus | Code, T1.6 |
| Kategorie zweimal speichern | zweites Mal: gespeicherte Links zählen, kein erneuter Upload (Uebernommen/Url), keine Doppelungen | Code F1/F2 unverändert, T1.9 |
| Abbruch mitten im Speichern | Upload fertig, Patch nicht: Links stehen schon in colAntworten, Fotos `Uebernommen` → erneutes Speichern lädt nicht doppelt hoch; Pflicht bleibt erfüllt | Code |
| Netzfehler | Upload-Fehler → Meldung „x Foto(s) konnten nicht hochgeladen werden“, Kategorie nicht gespeichert; Pflicht zählt das nicht hochgeladene Foto, erneutes Tippen lädt nach. Grenze: Flow ohne Rückmeldung (siehe Offene Befunde) | Code |
| zwei Prüfer gleichzeitig | unverändert: GespeichertAm-Vergleich lehnt das zweite Speichern ab; Fotos des zweiten bleiben unhochgeladen | Code |
| Foto Pflicht + Punkt nicht Pflicht und unbeantwortet | Foto trotzdem verlangt (Pflicht = Nachweis) | Logik-Probe |
| FotoMoeglich Ja, Foto leer | Optional | Logik-Probe, T1.10 |

Logik-Gegenprobe der Funktionen (`werkzeuge/logik_probe.py`, Python-Nachbildung der Formeln, keine Ausführung von Power Fx):

```
P1  ok    Foto Pflicht, kein Foto, sonst alles ausgefüllt                        erwartet 'Foto'       ist 'Foto'
P1  ok    Foto Pflicht, 1 neues Foto (colFotos)                                  erwartet ''           ist ''
P1  ok    Foto Pflicht, Foto schon gespeichert (Link)                            erwartet ''           ist ''
P1  ok    Foto Pflicht, Punkt nicht Pflicht und unbeantwortet                    erwartet 'Foto'       ist 'Foto'
P1  ok    Foto Optional, kein Foto                                               erwartet ''           ist ''
P1  ok    n.i.O. ohne Kommentar und Foto Pflicht ohne Foto: Kommentar zuerst     erwartet 'Kommentar'  ist 'Kommentar'
P1  ok    Pflicht-Wert fehlt vor allem anderen                                   erwartet 'Wert'       ist 'Wert'
P1  ok    fnFotoModus: Spalte leer, FotoMoeglich Ja -> Optional                  erwartet 'Optional'   ist 'Optional'
P1  ok    fnFotoModus: Spalte leer, FotoMoeglich Nein -> Aus                     erwartet 'Aus'        ist 'Aus'
P1  ok    fnFotoModus: Spalte Aus schlägt FotoMoeglich Ja                        erwartet 'Aus'        ist 'Aus'
P1  ok    fnLinkAnzahl leer                                                      erwartet 0            ist 0
P1  ok    fnLinkAnzahl zwei Links                                                erwartet 2            ist 2
```

## f) Studio-Fallen

- Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).
- `Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.
- Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.
- Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).
- Y in Galerien friert beim YAML-Einfügen ein: Paket 1 fügt kein YAML ein, alle Werte per Formelleiste. Nach Schritt 1.6 trotzdem `btnKaFoto.Y` prüfen.
- Zwischenablage: Länge des kopierten Blocks prüfen (Lehre 27.10.: alter Inhalt eingefügt → 35 Fehler).
- Ebenenreihenfolge ✕/Bild: nicht über „Nach vorne“ gelöst, sondern über Lage (Bild beginnt bei Y 52), damit es unabhängig von der Reihenfolge stimmt.

## g) Lauffähigkeit

- Nicht automatisch ausführbar: Formeln in Studio, Foto-Auswahl, Upload. Testfolge T1.1–T1.12 im Paket, Foto-Teil (T1.5, T1.8) am Tablet durch Josias.
- Maschinell: Namen, Klammern, Rückübersetzung, Schema der drei Zweige, Anzahl Argumente, Textbreiten, Logik-Gegenprobe.

## Offene Befunde

- **Nicht Teil dieses Pakets, aber für Foto-Pflicht wichtig:** Der Flow `RG_Foto_hochladen` antwortet nicht. Scheitert er nach dem Start, steht der Link trotzdem im JSON und die Pflicht gilt als erfüllt. Vorschlag „Flows rückmelden“ in BAUKASTEN_UEBERSICHT.md (eigenes Paket, nicht gebaut).

