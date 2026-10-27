# Prüfung Baukasten-Paket 4 – Bedingte Fragen

Export: `2026-10-27_0909`. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar).

## a) Namenscheck (maschinell, belegt)

Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.

```
== Paket 4: 10 Properties, neue Steuerelemente: -
  App.Formulas                     ok
  scrKategorie.OnVisible           ok
  galKaPruefpunkte.Items           ok
  lblKaFehlendAnzahl.Text          ok
  lblKaFehlend.Text                ok
  lblKaUnter.Text                  ok
  conKaBalkenWert.Width            ok
  lblKaStand.Text                  ok
  btnKaSpeichern.OnSelect          ok
  htmProtokoll.HtmlText            ok
  Paket 4: colAntworten hat in allen drei Zweigen dieselben 23 Felder
```

## b) Typcheck

- `BedingungPunkt` Zahl: `Coalesce(p.BedingungPunkt; 0)`; `BedingungWert` Text: `Coalesce(…; "")`.
- `Ausgeblendet` aus dem JSON: `Coalesce(IfError(Boolean(…); false); false)` – fehlt das Feld (altes JSON), ist es false. UNSICHER: `Boolean()` auf einem fehlenden untypisierten Feld (deshalb IfError + Coalesce; Test T4.9).
- `fnSichtbar` bekommt die Felder von A einzeln (Funktionen nehmen keine Datensätze). Argumente werden vor dem Aufruf ausgewertet; Felder eines leeren Datensatzes (A nicht gefunden) liefern Blank, keinen Fehler. In `fnSichtbar` steht `!gef` vor allen Feldern von A, entscheidet also zuerst.
- `PruefpunktID in colVersteckt.PruefpunktID`: Zahl in einer Zahlenspalte.

## c) Reihenfolge

1. Spalten + aktualisieren vor OnVisible.
2. App.Formulas (fnSichtbar) vor den Aufrufern; zwischendurch rote Fehler möglich, App-Prüfung am Ende.
3. Im Speichern: `colVersteckt` **vor** dem Foto-Upload (Upload, Links, „übernommen“ lesen sie), `colSpeichern` direkt **vor** dem JSON (nach „Kommentar leeren“ und „Warnung setzen“), AnzahlNIO danach aus colSpeichern.

## d) Auswirkungsliste

| Stelle | betroffen | wie |
|---|---|---|
| scrKategorie.OnVisible | ja | BedID, BedWert, Ausgeblendet in allen Zweigen; Start-Sprung auf ersten sichtbaren Punkt |
| fnFehlt / fnFehltGrund | nein | unverändert; Aufrufer filtern vorher auf sichtbar |
| btnKaSpeichern: Prüfung und Sprung | ja | Prüfung über lblKaFehlendAnzahl (nur sichtbare), Sprung nur auf sichtbare |
| JSON-Aufbau (varAntwortJSON) | ja | aus der Kopie colSpeichern: neues Feld Ausgeblendet, ausgeblendete Punkte leer (auch Warnung = false); AnzahlNIO ebenfalls aus der Kopie |
| Mängel bei Abschluss (btnRuAbschluss) | nein (Formel) | ausgeblendete haben Bewertung "" → keine Mängel; AnzahlNIO zählt nach dem Leeren → Plausibilität Sum(AnzahlNIO) = Mängel stimmt |
| htmProtokoll | ja | ausgeblendete Zeilen weggelassen |
| Foto-Upload (btnKaSpeichern F1/F2) | ja | nur sichtbare (`!a.Ausgeblendet`) an allen 3 Stellen; Links werden nur an sichtbare Punkte gehängt; ausgeblendete verlieren ihre Foto-Links (Dateien bleiben in RG_Fotos) |
| Lesemodus nach Abschluss | ja | Galerie zeigt nur nicht ausgeblendete (gespeichertes Flag) |
| Nachlese-Vergleich | nein | vergleicht weiterhin den gesendeten Text |
| Zähler/Balken/Kopf/Fuß | ja | zählen nur sichtbare |
| Foto-Pflicht/Kommentar-Pflicht ausgeblendeter Punkte | ja | gelten nicht (Filter vor fnFehlt) |

## e) Szenarien

| Szenario | erwartetes Ergebnis | Beleg |
|---|---|---|
| neuer Punkt ohne Daten | B ohne Bedingung: wie bisher; B mit Bedingung: unsichtbar, bis A passt | Logik-Probe P4, T4.1–T4.2 |
| alter gespeicherter Punkt (JSON ohne neues Feld) | Ausgeblendet = false; im Bearbeiten wird live neu berechnet | OnVisible, T4.9 |
| inaktiver Punkt | A deaktiviert → B sichtbar (sicher); deaktivierte B bleiben wie bisher unsichtbar mitgeführt, ihr gespeichertes Flag bleibt erhalten | Logik-Probe, UpdateIf `!Inaktiv` |
| Rundgang abgeschlossen (Nur-Lesen) | Sichtbarkeit aus dem gespeicherten Flag, keine Neuberechnung | Code |
| Wechsel n.i.O. → i.O. → n.i.O. (an A) | B erscheint/verschwindet/erscheint; Eingaben in B bleiben bis zum Speichern erhalten | T4.2–T4.4 |
| Kategorie zweimal speichern | B einmal ausgeblendet gespeichert → leer; beim zweiten Mal wieder live berechnet | T4.5 |
| Abbruch mitten im Speichern | colAntworten bleibt unverändert (JSON aus der Kopie colSpeichern); stellt der Prüfer A zurück, erscheint B mit seinen Eingaben; Fotos von B bleiben unübernommen in colFotos | Code, T4.5 |
| Netzfehler | unverändert (Nachlese) | Code |
| zwei Prüfer gleichzeitig | unverändert (GespeichertAm) | Code |
| Fehlkonfiguration (A fehlt, Kette, leerer Wert, Wert passt nicht zu A, Liste) | B sichtbar und verlangt | Logik-Probe, T4.10 |
| Schreibweise i.O./n.i.O., Groß-/Kleinschreibung | wie IO/NIO | Logik-Probe, T4.9 |
| Foto an B, dann B ausgeblendet, Speichern | Foto wird nicht hochgeladen und nicht verlinkt; im JSON sind die Links von B leer; schon früher hochgeladene Dateien von B bleiben ohne Verweis in RG_Fotos (bekannt, harmlos) | Code |

Logik-Gegenprobe der Funktionen (`werkzeuge/logik_probe.py`, Python-Nachbildung der Formeln, keine Ausführung von Power Fx):

```
P4  ok    Bedingung NIO, A ist n.i.O. -> B sichtbar                              erwartet True         ist True
P4  ok    Bedingung NIO, A ist i.O. -> B ausgeblendet                            erwartet False        ist False
P4  ok    Bedingung NIO, A unbeantwortet -> B ausgeblendet                       erwartet False        ist False
P4  ok    Bedingung klein geschrieben (nio)                                      erwartet True         ist True
P4  ok    Bedingung * und A hat Text                                             erwartet True         ist True
P4  ok    Bedingung * und A leer                                                 erwartet False        ist False
P4  ok    Bedingung Auswahlwert                                                  erwartet True         ist True
P4  ok    Bedingung Wert in Mehrfachauswahl                                      erwartet True         ist True
P4  ok    Fehlkonfiguration: Punkt A nicht in der Kategorie -> B sichtbar        erwartet True         ist True
P4  ok    Fehlkonfiguration: A selbst bedingt (Kette) -> B sichtbar              erwartet True         ist True
P4  ok    Fehlkonfiguration: Bedingungswert leer -> B sichtbar                   erwartet True         ist True
P4  ok    A deaktiviert (mitgeführt) -> B sichtbar                               erwartet True         ist True
P4  ok    keine Bedingung (0) -> sichtbar                                        erwartet True         ist True
P4  ok    Schreibweise n.i.O. wie NIO                                            erwartet True         ist True
P4  ok    Schreibweise i.O. bei A n.i.O. -> ausgeblendet                         erwartet False        ist False
P4  ok    Tippfehler im Bedingungswert (Rot bei i.O./n.i.O.) -> B sichtbar       erwartet True         ist True
P4  ok    Liste als Bedingungswert (Rot;Gelb) -> B sichtbar                      erwartet True         ist True
P4  ok    Auswahlwert, den es in A nicht gibt -> B sichtbar                      erwartet True         ist True
P4  ok    Auswahlwert passt nicht (A = ok) -> ausgeblendet                       erwartet False        ist False
P4  ok    Bedingung NIO bei Text-Punkt A (ungültig) -> B sichtbar                erwartet True         ist True
```

## f) Studio-Fallen

- Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).
- `Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.
- Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.
- Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).
- `Filter(colAntworten As a; … LookUp(colAntworten As b0; …))` liest dieselbe Sammlung zweimal – nur lesend, erlaubt. Geschrieben wird mit UpdateIf auf colAntworten mit einer **anderen** Sammlung (colVersteckt) in der Bedingung (kein „ForAllWithMutation“).

## g) Lauffähigkeit

- T4.1–T4.9 in der Vorschau.

## Unabhängige Prüfung – Runde 1 und Umgang

| Befund | Umgang |
|---|---|
| B1 mittel: Fotos ausgeblendeter Punkte bleiben | behoben: Fotos leeren, Links nicht an ausgeblendete hängen |
| B2 mittel: falscher Bedingungswert blendet für immer aus | behoben: fnBedGueltig prüft gegen Typ/Auswahl von A, sonst B sichtbar; i.O./n.i.O. und Schreibweisen normalisiert (fnBedNorm) |
| B3 mittel: Testbogen nicht ausführbar | neu: Vorbedingungen, zweite Durchführung für den ausgeblendeten Fall, Abschluss getrennt |
| B4/B5: Eingaben/neue Fotos ausgeblendeter Punkte verworfen | gewollt, dokumentiert |
| B6: Kettenerkennung grob | gewollt (sicherer Ausfall) |
| B7: Zahl mit Warnen und Bedingung NIO | Hinweis in Schritt 4.2 |
| B8: Stammdaten während laufender Rundgänge | bekannte Regel F4 (nach Feierabend pflegen) |
| B9: Sichtbarkeitsregel an zehn Stellen | vom Generator aus einer Vorlage erzeugt, maschinell gleich |
| B10 UNSICHER: Galerie verschiebt sich | Test T4.4 |
| B11 UNSICHER: Flows lesen JSON | kein Flow liest das JSON (Export belegt) |
| B12: Pfade in 4.5 | ergänzt |

## Unabhängige Prüfung – Runde 2 und Umgang

| Befund | Umgang |
|---|---|
| B4-1 mittel: T4.10 prüft den sicheren Ausfall nicht | T4.10: A auf i.O. → B bleibt sichtbar |
| B4-2 mittel: Leeren vor Upload/Nachlese verliert Eingaben, Fotos falsch übernommen | behoben: JSON und AnzahlNIO aus Kopie colSpeichern, colAntworten bleibt; Upload/Links/„übernommen“ über colVersteckt |
| Bedingung NIO an Sperren-Punkt | Pflegehinweis: NIO nur bei Grenzmodus Mangel |
| Rückweg „BedingungPunkt auf 0“ wirkungslos | korrigiert: B auf Aktiv = Nein |
| Testbogen (neue Durchführung, Nachholtage, Z1–Z3, Textfeld verlassen) | ergänzt |
| MEHRFACH erst ab Paket 5 | im Hinweis vermerkt |
| Kette, verworfene Werte/Fotos, Dateien ohne Verweis | gewollt bzw. bekannt, dokumentiert |

## Offene Befunde

Keine.

