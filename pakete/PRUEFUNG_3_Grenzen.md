# Prüfung Baukasten-Paket 3 – Zahlengrenzen pro Prüfpunkt: Mangel, Warnen oder Sperren

Export: `2026-10-27_0909`. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## a) Namenscheck (maschinell, belegt)

Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.

```
== Paket 3: 7 Properties, neue Steuerelemente: -
  App.Formulas                     ok
  scrKategorie.OnVisible           ok
  lblKaZahlInfo.Text               ok
  lblKaZahlInfo.Color              ok
  txtKaZahl.BorderColor            ok
  btnKaSpeichern.OnSelect          ok
  htmProtokoll.HtmlText            ok
  Paket 3: colAntworten hat in allen drei Zweigen dieselben 20 Felder
```

## b) Typcheck

- `Grenzmodus` Auswahlspalte: nur `p.Grenzmodus.Value` / `pp.Grenzmodus.Value` über `fnGrenzmodus` (leer/unbekannt → "Mangel", maschinell + Logik-Probe).
- `fnAusserhalb(z; mi; ma)`: Blank-Grenzen zählen nicht, Blank-Wert ist nie außerhalb (wie die alte Formel).
- `fnZahlBewertung` liefert "" bei Sperren außerhalb; alle Stellen, die Bewertung lesen, vertragen "" (unbewertet).

## c) Reihenfolge

1. Spalte + aktualisieren vor OnVisible.
2. App.Formulas vor/mit OnVisible (fnGrenzmodus, fnSperreGilt neu). Paket 1 (4. Parameter, Feld Grenzmodus) und Paket 2 (Hinweistext „Kommentar (Pflicht)“) müssen drin sein.
3. Speichern (JSON mit Warnung) und Protokoll (liest Warnung) sind unabhängig voneinander; altes JSON ohne Warnung wird als false gelesen.

## d) Auswirkungsliste

| Stelle | betroffen | wie |
|---|---|---|
| scrKategorie.OnVisible | ja | Grenzmodus aus Spalte (Bearbeiten, Nur-Ansicht über pp); Neubewertung gespeicherter Zahlen mit Grenzmodus |
| fnFehlt / fnFehltGrund | ja | „Bereich“ bei Sperren außerhalb |
| btnKaSpeichern: Prüfung und Sprung | ja (indirekt) | Sperren blockiert, Sprung zum Punkt |
| Kommentar leeren (08:44) | ja (indirekt) | Warnen außerhalb behält den Kommentar |
| JSON-Aufbau (varAntwortJSON) | ja | neues Feld `Warnung` (per AddColumns, nur im JSON, nicht in colAntworten); Sperren außerhalb wird nie gespeichert |
| Mängel bei Abschluss (btnRuAbschluss) | nein | nur NIO; Warnen speichert IO → kein Mangel (gewollt) |
| htmProtokoll | ja | Warnung: i.O. orange + „(außerhalb Soll, begründet)“; Kommentar grau (Paket 2); altes JSON ohne Warnung → false |
| Foto-Upload | nein | Bedingung NIO/FotoModus; Warnen ohne NIO lädt nur bei FotoModus ≠ Aus |
| Lesemodus nach Abschluss | ja | kein Aufforderungstext mehr: NIO „außerhalb des Sollbereichs“, i.O. außerhalb „außerhalb, begründet“ (orange), unabhängig vom heutigen Grenzmodus; Min/Max aus den heutigen Stammdaten |
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
| Sperren mit Min > Max (Fehleinstellung) | wie Mangel (n.i.O., Kommentar), Rundgang bleibt abschließbar | Logik-Probe, T3.11 |
| Sperren und echter Wert außerhalb | Speichern unmöglich – deshalb Pflegeregel „Sperren nur für Tippfehler-Grenzen“ (Schritt 3.2) | Regel |
| Grenzmodus nach dem Speichern umgestellt | beim Öffnen neu bewertet (wie bisher bei Min/Max); die Karte kann dann vom gespeicherten Stand abweichen, ohne als Änderung zu zählen (vorhandenes Verhalten) | Code |

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
P3  ok    Sperren mit Min > Max: wie Mangel (n.i.O.), nicht gesperrt             erwartet 'NIO'        ist 'NIO'
P3  ok    Sperren mit Min > Max: kein Bereich-Fehler, Kommentar verlangt         erwartet 'Kommentar'  ist 'Kommentar'
P3  ok    Sperren nur Max gesetzt, Wert darüber                                  erwartet 'Bereich'    ist 'Bereich'
P3  ok    Dezimalzahl 16,01 bei Max 16 -> außerhalb                              erwartet 'NIO'        ist 'NIO'
P3  ok    Warnen ohne Min/Max: nie außerhalb                                     erwartet ''           ist ''
```

## f) Studio-Fallen

- Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).
- `Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.
- Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.
- Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).

## g) Lauffähigkeit

- T3.1–T3.8 in der Vorschau.

## Unabhängige Prüfung – Runde 1 und Umgang

| Befund | Umgang |
|---|---|
| B2 mittel: Warnen nicht von normalem i.O. zu unterscheiden | behoben: JSON-Feld Warnung, Protokoll orange mit Hinweis, Nur-Ansicht „außerhalb, begründet“ |
| B3 mittel: Sperren ohne Ausweg / Min > Max | Pflegeregel „nur Tippfehler-Grenzen“ in Schritt 3.2 und Kurzfassung; Min > Max → wie Mangel (fnSperreGilt) |
| B7 mittel: Testbogen nicht der Reihe nach ausführbar | neu: Z1/Z2/Z3 gleichzeitig, Kommentare in der Folge, Abschluss getrennt |
| B4: „Soll“ bei Sperren | behoben: „zulässig ab … bis …“ |
| B5: Neubewertung beim Öffnen zählt nicht als Änderung | vorhandenes Verhalten, als Szenario dokumentiert |
| B6: Nur-Ansicht zeigt Aufforderungen | behoben |
| B11: clrWarnungHell unbenutzt | entfernt |

## Unabhängige Prüfung – Runde 2 und Umgang

| Befund | Umgang |
|---|---|
| B3-1 mittel: Nur-Ansicht liest heutige Min/Max statt des Kennzeichens | behoben: Feld `Warnung` in allen drei Zweigen, Nur-Ansicht liest nur das Feld; deaktivierte Punkte behalten es |
| „zulässig“ bei Min > Max | behoben: „zulässig“ nur, wenn die Sperre gilt |
| „bitte begründen“ bleibt nach der Begründung | behoben: dann „außerhalb, begründet“ |
| Testbogen (Aktiv, Aufräumen, T3.11 nicht speichern) | ergänzt |
| Rückweg: Warnen-Werte in der alten App; Umstellen während laufender Rundgänge | im Rückweg bzw. als Pflegeregel ergänzt |
| Warnen/Mangel bei Min > Max | vorhandenes Verhalten (alles außerhalb), Pflegeregel „Min nie größer als Max“ |
| lblKaZahlInfo auf schmalen Geräten | App ist für Tablet hochkant (768) gebaut; dort 2 Zeilen geprüft |

## Unabhängige Prüfung – Runde 3 und Umgang

| Befund | Umgang |
|---|---|
| Gezielte Prüfung (30.10.) von Feld Warnung, Nur-Ansicht und Protokoll: kein Befund | alle drei Zweige von OnVisible haben das Feld, Speichern setzt es vor dem JSON, Nur-Ansicht liest nur das Feld, altes JSON → false. Zwei Punkte geschlussfolgert, nicht in Studio getestet: UpdateIf mit Feldverweisen im Änderungsdatensatz (Schritt 3.8 und T3.10 zeigen es) |

## Offene Befunde

- Fachliche Annahme „Warnen verlangt Begründung“ ist von Josias zu bestätigen (kein technischer Befund).

