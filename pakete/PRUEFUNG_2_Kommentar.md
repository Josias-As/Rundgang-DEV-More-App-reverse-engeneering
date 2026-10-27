# Prüfung Baukasten-Paket 2 – Pflicht-Kommentar auch bei i.O. (pro Prüfpunkt)

Export: `2026-10-27_0724` – **Simulation der Änderung von 08:44, vor dem Einfügen mit dem frischen Export wiederholen**. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## a) Namenscheck (maschinell, belegt)

Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.

```
== Paket 2: 5 Properties, neue Steuerelemente: -
  App.Formulas                     ok
  scrKategorie.OnVisible           ok
  txtKaKommentar.HintText          ok
  txtKaKommentar.AccessibleLabel   ok
  htmProtokoll.HtmlText            ok
  Paket 2: colAntworten hat in allen drei Zweigen dieselben 19 Felder
```

## b) Typcheck

- `KommentarPflicht` Ja/Nein: nur `Coalesce(p.KommentarPflicht; false)` (maschinell).
- `fnBeantwortet(bew; wt; wz)`: Text, Text, Number – Blank wird wie leer behandelt (`bew <> ""`, `Trim(wt) <> ""`, `!IsBlank(wz)`).
- Protokoll: `b` ist dort `Text(a.Value.Bewertung)` (unverändert), Vergleich mit "NIO" ist Text.

## c) Reihenfolge

1. Spalte anlegen + aktualisieren vor OnVisible.
2. App.Formulas, OnVisible, Kommentarfeld, Protokoll – kein Block hängt von einem späteren ab. Paket 1 muss drin sein (Felder und fnKommentarNoetig).

## d) Auswirkungsliste

| Stelle | betroffen | wie |
|---|---|---|
| scrKategorie.OnVisible | ja | Bearbeiten-Zweig liest KommentarPflicht; Nur-Ansicht und deaktivierte bleiben false (dort keine Prüfung) |
| fnFehlt / fnFehltGrund | ja (indirekt) | über fnKommentarNoetig |
| btnKaSpeichern: Prüfung und Sprung | ja (indirekt) | Prüfung/Sprung zählen fehlende Pflicht-Kommentare bei i.O. |
| Kommentar leeren (08:44) | ja (indirekt) | Kommentar bleibt bei KommentarPflicht und beantwortetem Punkt; ohne Pflicht wie bisher geleert |
| JSON-Aufbau (varAntwortJSON) | nein | Kommentar war schon im JSON |
| Mängel bei Abschluss (btnRuAbschluss) | nein | nur NIO; i.O.-Kommentare werden keine Mängel |
| htmProtokoll | ja | Farbe des Kommentars nach Bewertung |
| Foto-Upload | nein |  |
| Lesemodus nach Abschluss | ja | Kommentar bei i.O. wird angezeigt (Paket 1: sichtbar, wenn nicht leer) |
| Nachlese-Vergleich | nein |  |
| Kommentarfeld (Sichtbarkeit, Kartenhöhe) | ja (indirekt) | über fnKommentarNoetig aus Paket 1, keine Formel neu |

## e) Szenarien

| Szenario | erwartetes Ergebnis | Beleg |
|---|---|---|
| neuer Punkt ohne Daten | kein Kommentar verlangt, bis der Punkt beantwortet ist | Logik-Probe P2 |
| alter gespeicherter Punkt (JSON ohne neues Feld) | Kommentarpflicht kommt aus den Stammdaten; alter i.O. ohne Kommentar zählt beim Wiederöffnen als offen (gewollt: Kontrolle) | Code |
| inaktiver Punkt | KommentarPflicht false, zählt nicht | Code |
| Rundgang abgeschlossen (Nur-Lesen) | keine Prüfung, Kommentar sichtbar wenn gespeichert | Code |
| Wechsel n.i.O. → i.O. → n.i.O. | Kommentar bleibt im Feld; Hinweistext wechselt; beim Speichern bleibt er (Pflicht) bzw. wird bei i.O. ohne Pflicht geleert | Logik-Probe, T2.3–T2.6 |
| Kategorie zweimal speichern | Kommentar bleibt erhalten (wird beim Öffnen aus dem JSON gelesen) | T2.5 |
| Abbruch mitten im Speichern | UpdateIf lief schon: Kommentare ohne Pflicht sind in colAntworten geleert (wie 08:44); bei Pflicht bleiben sie | Code |
| Netzfehler | Patch scheitert → Nachlese ungleich → Meldung, nichts verloren (Formular bleibt offen) | Code unverändert |
| zwei Prüfer gleichzeitig | unverändert (GespeichertAm) | Code |

Logik-Gegenprobe der Funktionen (`werkzeuge/logik_probe.py`, Python-Nachbildung der Formeln, keine Ausführung von Power Fx):

```
P2  ok    Kommentarpflicht, i.O., kein Kommentar                                 erwartet 'Kommentar'  ist 'Kommentar'
P2  ok    Kommentarpflicht, i.O., mit Kommentar                                  erwartet ''           ist ''
P2  ok    Kommentarpflicht, optionaler Punkt unbeantwortet                       erwartet ''           ist ''
P2  ok    Kommentarpflicht, Text-Punkt mit Eingabe ohne Kommentar                erwartet 'Kommentar'  ist 'Kommentar'
P2  ok    ohne Kommentarpflicht, i.O. ohne Kommentar                             erwartet ''           ist ''
P2  ok    Kommentar leeren beim Speichern: i.O. ohne Pflicht -> leeren           erwartet False        ist False
P2  ok    Kommentar leeren beim Speichern: i.O. mit Pflicht -> behalten          erwartet True         ist True
```

## f) Studio-Fallen

- Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).
- `Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.
- Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.
- Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).
- HtmlText: der Block ist die ganze Property; einfache Anführungszeichen im HTML stehen innerhalb der Texte, Rückübersetzung zeichengleich (maschinell).

## g) Lauffähigkeit

- Testfolge T2.1–T2.8 in der Vorschau, alles ohne Tablet möglich.

## Offene Befunde

Keine.

