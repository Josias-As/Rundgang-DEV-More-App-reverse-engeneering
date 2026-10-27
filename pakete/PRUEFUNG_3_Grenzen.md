# Prüfung Baukasten-Paket 3 – Zahlengrenzen pro Prüfpunkt: Mangel, Warnen oder Sperren

Export: `2026-10-27_0724` – **Simulation der Änderung von 08:44, vor dem Einfügen mit dem frischen Export wiederholen**. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## a) Namenscheck (maschinell, belegt)

Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.

```
== Paket 3: 5 Properties, neue Steuerelemente: -
  App.Formulas                     ok
  scrKategorie.OnVisible           ok
  lblKaZahlInfo.Text               ok
  lblKaZahlInfo.Color              ok
  txtKaZahl.BorderColor            ok
  Paket 3: colAntworten hat in allen drei Zweigen dieselben 19 Felder
```

## b) Typcheck

- `Grenzmodus` Auswahlspalte: nur `p.Grenzmodus.Value` / `pp.Grenzmodus.Value` über `fnGrenzmodus` (leer/unbekannt → "Mangel", maschinell + Logik-Probe).
- `fnAusserhalb(z; mi; ma)`: Blank-Grenzen zählen nicht, Blank-Wert ist nie außerhalb (wie die alte Formel).
- `fnZahlBewertung` liefert "" bei Sperren außerhalb; alle Stellen, die Bewertung lesen, vertragen "" (unbewertet).

## c) Reihenfolge

1. Spalte + aktualisieren vor OnVisible.
2. App.Formulas vor/mit OnVisible (fnGrenzmodus neu). Paket 1 (4. Parameter, Feld Grenzmodus) und Paket 2 (Hinweistext „Kommentar (Pflicht)“) müssen drin sein.

## d) Auswirkungsliste

| Stelle | betroffen | wie |
|---|---|---|
| scrKategorie.OnVisible | ja | Grenzmodus aus Spalte (Bearbeiten, Nur-Ansicht über pp); Neubewertung gespeicherter Zahlen mit Grenzmodus |
| fnFehlt / fnFehltGrund | ja | „Bereich“ bei Sperren außerhalb |
| btnKaSpeichern: Prüfung und Sprung | ja (indirekt) | Sperren blockiert, Sprung zum Punkt |
| Kommentar leeren (08:44) | ja (indirekt) | Warnen außerhalb behält den Kommentar |
| JSON-Aufbau (varAntwortJSON) | nein | Bewertung IO/NIO/"" wie bisher; Sperren außerhalb wird nie gespeichert |
| Mängel bei Abschluss (btnRuAbschluss) | nein | nur NIO; Warnen speichert IO → kein Mangel (gewollt) |
| htmProtokoll | nein | Warnen: i.O. + grauer Kommentar (Paket 2) |
| Foto-Upload | nein | Bedingung NIO/FotoModus; Warnen ohne NIO lädt nur bei FotoModus ≠ Aus |
| Lesemodus nach Abschluss | ja | Hinweistext nach Grenzmodus der heutigen Stammdaten; bei gespeichertem NIO immer „außerhalb des Sollbereichs“ |
| Nachlese-Vergleich | nein |  |
| Zahlenfeld-Anzeige | ja | Text/Farbe Label, Rahmenfarbe |

## e) Szenarien

| Szenario | erwartetes Ergebnis | Beleg |
|---|---|---|
| neuer Punkt ohne Daten | kein Hinweis, Wert fehlt wie bisher | Logik-Probe |
| alter gespeicherter Punkt (JSON ohne neues Feld) | beim Öffnen neu bewertet mit dem Grenzmodus von heute (wie bisher mit Min/Max) | OnVisible |
| inaktiver Punkt | Grenzmodus "Mangel", keine Wirkung | Code |
| Rundgang abgeschlossen (Nur-Lesen) | Bewertung so wie gespeichert, keine Neubewertung | OnVisible Nur-Ansicht |
| Wechsel n.i.O. → i.O. → n.i.O. | bei ZAHL über den Wert: 18,5 → 12 → 18,5 ergibt je Modus NIO/IO, IO/IO (+Warnung), ""/IO (gesperrt) | Logik-Probe P3 |
| Kategorie zweimal speichern | Warnen: Kommentar bleibt; Sperren: nur Werte im Bereich gespeichert | Code |
| Abbruch mitten im Speichern | wie Paket 2 | Code |
| Netzfehler | unverändert | Code |
| zwei Prüfer gleichzeitig | unverändert | Code |
| Grenze genau auf Min/Max | im Bereich | Logik-Probe |

Logik-Gegenprobe der Funktionen (`werkzeuge/logik_probe.py`, Python-Nachbildung der Formeln, keine Ausführung von Power Fx):

```
P3  ok    Mangel: 18,5 bei Soll 6–16 -> n.i.O.                                   erwartet 'NIO'        ist 'NIO'
P3  ok    Warnen: 18,5 bei Soll 6–16 -> i.O. (kein Mangel)                       erwartet 'IO'         ist 'IO'
P3  ok    Sperren: 18,5 bei Soll 6–16 -> unbewertet                              erwartet ''           ist ''
P3  ok    Warnen: Wert im Bereich -> i.O.                                        erwartet 'IO'         ist 'IO'
P3  ok    Warnen außerhalb: Kommentar Pflicht                                    erwartet 'Kommentar'  ist 'Kommentar'
P3  ok    Warnen außerhalb mit Kommentar: vollständig                            erwartet ''           ist ''
P3  ok    Sperren außerhalb: unzulässig, Speichern gesperrt                      erwartet 'Bereich'    ist 'Bereich'
P3  ok    Sperren außerhalb mit Kommentar: trotzdem gesperrt                     erwartet 'Bereich'    ist 'Bereich'
P3  ok    Sperren im Bereich: vollständig                                        erwartet ''           ist ''
P3  ok    Grenze genau auf Min (6) ist im Bereich                                erwartet 'IO'         ist 'IO'
P3  ok    fnGrenzmodus: leere Spalte -> Mangel                                   erwartet 'Mangel'     ist 'Mangel'
P3  ok    fnGrenzmodus: unbekannter Wert -> Mangel                               erwartet 'Mangel'     ist 'Mangel'
```

## f) Studio-Fallen

- Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).
- `Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.
- Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.
- Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).

## g) Lauffähigkeit

- T3.1–T3.8 in der Vorschau.

## Offene Befunde

- Fachliche Annahme „Warnen verlangt Begründung“ ist von Josias zu bestätigen (kein technischer Befund).

