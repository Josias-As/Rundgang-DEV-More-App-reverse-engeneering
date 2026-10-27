# Prüfung Baukasten-Paket 5 – Neue Typen: Mehrfachauswahl, Datum, Datum + Uhrzeit

Export: `2026-10-27_0909`. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## a) Namenscheck (maschinell, belegt)

Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.

```
== Paket 5: 1 Properties, neue Steuerelemente: cboKaMehrfach, dpKaDatum, ddKaStunde, ddKaMinute
  App.Formulas                     ok
  cboKaMehrfach.Items              ok
  cboKaMehrfach.DisplayFields      ok
  cboKaMehrfach.SearchFields       ok
  cboKaMehrfach.SelectMultiple     ok
  cboKaMehrfach.IsSearchable       ok
  cboKaMehrfach.DefaultSelectedItems ok
  cboKaMehrfach.OnChange           ok
  cboKaMehrfach.InputTextPlaceholder ok
  cboKaMehrfach.AccessibleLabel    ok
  cboKaMehrfach.DisplayMode        ok
  cboKaMehrfach.Visible            ok
  cboKaMehrfach.BorderColor        ok
  cboKaMehrfach.ChevronBackground  ok
  cboKaMehrfach.ChevronFill        ok
  cboKaMehrfach.SelectionFill      ok
  cboKaMehrfach.SelectionColor     ok
  cboKaMehrfach.Font               ok
  cboKaMehrfach.Size               ok
  cboKaMehrfach.X                  ok
  cboKaMehrfach.Y                  ok
  cboKaMehrfach.Width              ok
  cboKaMehrfach.Height             ok
  dpKaDatum.AccessibleLabel        ok
  dpKaDatum.BorderColor            ok
  dpKaDatum.Color                  ok
  dpKaDatum.DefaultDate            ok
  dpKaDatum.DisplayMode            ok
  dpKaDatum.Font                   ok
  dpKaDatum.Height                 ok
  dpKaDatum.IconBackground         ok
  dpKaDatum.IconFill               ok
  dpKaDatum.OnChange               ok
  dpKaDatum.Size                   ok
  dpKaDatum.StartOfWeek            ok
  dpKaDatum.Visible                ok
  dpKaDatum.Width                  ok
  dpKaDatum.X                      ok
  dpKaDatum.Y                      ok
  ddKaStunde.AccessibleLabel       ok
  ddKaStunde.AllowEmptySelection   ok
  ddKaStunde.BorderColor           ok
  ddKaStunde.ChevronBackground     ok
  ddKaStunde.ChevronFill           ok
  ddKaStunde.ChevronHoverBackground ok
  ddKaStunde.ChevronHoverFill      ok
  ddKaStunde.Color                 ok
  ddKaStunde.Default               ok
  ddKaStunde.DisplayMode           ok
  ddKaStunde.Fill                  ok
  ddKaStunde.Font                  ok
  ddKaStunde.Height                ok
  ddKaStunde.HoverFill             ok
  ddKaStunde.Items                 ok
  ddKaStunde.Items.Value           ok
  ddKaStunde.OnChange              ok
  ddKaStunde.PaddingLeft           ok
  ddKaStunde.PressedColor          ok
  ddKaStunde.PressedFill           ok
  ddKaStunde.SelectionColor        ok
  ddKaStunde.SelectionFill         ok
  ddKaStunde.Size                  ok
  ddKaStunde.Visible               ok
  ddKaStunde.Width                 ok
  ddKaStunde.X                     ok
  ddKaStunde.Y                     ok
  ddKaMinute.AccessibleLabel       ok
  ddKaMinute.AllowEmptySelection   ok
  ddKaMinute.BorderColor           ok
  ddKaMinute.ChevronBackground     ok
  ddKaMinute.ChevronFill           ok
  ddKaMinute.ChevronHoverBackground ok
  ddKaMinute.ChevronHoverFill      ok
  ddKaMinute.Color                 ok
  ddKaMinute.Default               ok
  ddKaMinute.DisplayMode           ok
  ddKaMinute.Fill                  ok
  ddKaMinute.Font                  ok
  ddKaMinute.Height                ok
  ddKaMinute.HoverFill             ok
  ddKaMinute.Items                 ok
  ddKaMinute.Items.Value           ok
  ddKaMinute.OnChange              ok
  ddKaMinute.PaddingLeft           ok
  ddKaMinute.PressedColor          ok
  ddKaMinute.PressedFill           ok
  ddKaMinute.SelectionColor        ok
  ddKaMinute.SelectionFill         ok
  ddKaMinute.Size                  ok
  ddKaMinute.Visible               ok
  ddKaMinute.Width                 ok
  ddKaMinute.X                     ok
  ddKaMinute.Y                     ok
  Paket 5: colAntworten hat in allen drei Zweigen dieselben 22 Felder
```

## b) Typcheck

- `Eingabetyp` bleibt Auswahlspalte, `.Value` wie bisher; neue Werte sind Texte.
- `dpKaDatum.SelectedDate` ist ein Datum → `fnDatumText(d: Date; …)`. `ddKaStunde.Selected.Value` Text, leer → `Coalesce(…; "")`.
- Gespeicherte Form „TT.MM.JJJJ“ wird mit `DateValue(Left(…; 10); "de-DE")` zurückgelesen, `IfError` fängt kaputte Texte ab.
- Kombinationsfeld: Items/DefaultSelectedItems sind Tabellen mit Spalte `Value` (Text), DisplayFields `["Value"]`.

## c) Reihenfolge

1. Auswahlwerte ergänzen + aktualisieren.
2. App.Formulas vor den neuen Steuerelementen (fnDatumText).
3. Steuerelemente: Datum vor Stunde/Minute ist egal (sie lesen sich gegenseitig, beide sind vor der App-Prüfung da).

## d) Auswirkungsliste

| Stelle | betroffen | wie |
|---|---|---|
| scrKategorie.OnVisible | nein | Typ kommt schon aus Eingabetyp.Value bzw. dem JSON |
| fnFehlt / fnFehltGrund | ja | Wert fehlt für MEHRFACH/DATUM/DATUMZEIT, „Uhrzeit“ bei Datum ohne Zeit |
| btnKaSpeichern: Prüfung und Sprung | ja (indirekt) |  |
| JSON-Aufbau (varAntwortJSON) | nein | Werte in WertText |
| Mängel bei Abschluss (btnRuAbschluss) | nein | keine Bewertung → keine Mängel; Wert-Spalte würde WertText zeigen |
| htmProtokoll | nein | zeigt WertText |
| Foto-Upload | nein |  |
| Lesemodus nach Abschluss | ja | neue Felder DisplayMode.View; Mehrfachauswahl: Auswahl = gespeicherter Text (Nur-Ansicht-Zweig) → zeigt genau die gewählten Werte |
| Nachlese-Vergleich | nein |  |
| Bedingungen (Paket 4) | ja (indirekt) | fnBedPasst prüft Werte der Mehrfachauswahl einzeln |

## e) Szenarien

| Szenario | erwartetes Ergebnis | Beleg |
|---|---|---|
| neuer Punkt ohne Daten | leer, bei Pflicht offen | Logik-Probe P5 |
| alter gespeicherter Punkt (JSON ohne neues Feld) | kein neues Feld; neue Typen gab es vorher nicht | – |
| inaktiver Punkt | unsichtbar, zählt nicht | Code |
| Rundgang abgeschlossen (Nur-Lesen) | Werte sichtbar, nicht änderbar | T5.10 |
| Wechsel n.i.O. → i.O. → n.i.O. | nicht anwendbar (keine Bewertung); Wechsel der Auswahl schreibt WertText neu | Code |
| Kategorie zweimal speichern | Werte werden beim Öffnen aus WertText wieder eingestellt | T5.8 |
| Abbruch mitten im Speichern | unverändert | Code |
| Netzfehler | unverändert | Code |
| zwei Prüfer gleichzeitig | unverändert | Code |
| Uhrzeit vor Datum gewählt | Text entsteht beim Datum mit der gewählten Zeit | Logik-Probe fnDatumText, T5.7 |

Logik-Gegenprobe der Funktionen (`werkzeuge/logik_probe.py`, Python-Nachbildung der Formeln, keine Ausführung von Power Fx):

```
P5  ok    Mehrfach Pflicht leer                                                  erwartet 'Wert'       ist 'Wert'
P5  ok    Mehrfach Pflicht zwei Werte                                            erwartet ''           ist ''
P5  ok    Datum Pflicht leer                                                     erwartet 'Wert'       ist 'Wert'
P5  ok    Datum gesetzt                                                          erwartet ''           ist ''
P5  ok    Datum+Uhrzeit nur Datum                                                erwartet 'Uhrzeit'    ist 'Uhrzeit'
P5  ok    Datum+Uhrzeit optional, nur Datum -> trotzdem unvollständig            erwartet 'Uhrzeit'    ist 'Uhrzeit'
P5  ok    Datum+Uhrzeit vollständig                                              erwartet ''           ist ''
P5  ok    Datum+Uhrzeit optional leer                                            erwartet ''           ist ''
P5  ok    fnDatumText nur Datum (DATUM)                                          erwartet '27.10.2026' ist '27.10.2026'
P5  ok    fnDatumText Datum + Zeit                                               erwartet '27.10.2026 07:05' ist '27.10.2026 07:05'
P5  ok    fnDatumText Zeit ohne Minute                                           erwartet '27.10.2026' ist '27.10.2026'
P5  ok    fnDatumText ohne Datum                                                 erwartet ''           ist ''
```

## f) Studio-Fallen

- Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).
- `Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.
- Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.
- Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).
- YAML in eine Galerievorlage: mit einem Kind von conKaKarte markiert einfügen (Übergabe 5); danach Y prüfen (E-05).
- Kombinationsfeld ohne YAML (Version unbekannt), Properties per Formelleiste.
- Classic/DatePicker@2.6.0 und Classic/DropDown@2.3.1 sind in den Exporten belegt (Tischbuchung bzw. diese App).

## g) Lauffähigkeit

- T5.1–T5.10 in der Vorschau. UNSICHER: Darstellung einer leeren Datumsauswahl (DefaultDate leer) – T5.1 zeigt es.

## Offene Befunde

Keine.

