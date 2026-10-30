# Ergebnis Prüfung Paket 3 (Warnung) und Paket 4 (Speichern, Schritt 4.6)

Gegenstand: Paket 3 Schritte 3.4 bis 3.7, Paket 4 Schritte 4.4, 4.6, 4.7. Gegengelesen: Export `scrRundgang.pa.yaml` (Abschluss), App.Formulas aus Paket 4.

## Ergebnis: kein hoher, kein mittlerer Befund. Ein niedriger Hinweis.

### N1 – Paket 4 – niedrig – Stelle: Foto-Upload vor Abbruch (geschlussfolgert)
Szenario: B sichtbar, neues Foto. Speichern: Upload klappt, `Patch(RG_KategorieErgebnisse)` scheitert (Meldung „nicht bestätigt“). Der Prüfer setzt A auf i.O., B wird ausgeblendet, er speichert erneut. Das JSON hat dann `Fotos: ""` für B. Die schon hochgeladene Datei liegt in `RG_Fotos`, ohne Verweis aus dem JSON.
Folgen: Datei verwaist, harmlos. Setzt der Prüfer A zurück auf n.i.O. und speichert nicht zwischendurch, bleiben die Links in `colAntworten.Fotos` erhalten. Das ist richtig, weil `colSpeichern` nur eine Kopie ist.
Vorschlag: nichts ändern. Im Betriebshandbuch erwähnen, dass einzelne Dateien in `RG_Fotos` ohne Verweis bleiben können. Kein Fehler des Pakets.

## Geprüft ohne Befund

### A) Paket 3, Feld `Warnung`
- **Drei Zweige von `scrKategorie.OnVisible`** (Nur-Ansicht-Zweig, Bearbeiten-Zweig, Zweig der Altlasten): Das Feld steht in allen drei, immer als Boolean.
  - Nur-Ansicht: `Coalesce(IfError(Boolean(a.Warnung); false); false)`.
  - Bearbeiten: `false`.
  - Altlasten: `Coalesce(IfError(Boolean(o.Value.Warnung); false); false)`.
  - Die Typen sind gleich. Auch in Paket 4 mit `BedID`, `BedWert`, `Ausgeblendet` stehen alle Felder in allen drei Zweigen (belegt, Zeilen 194, 213 und 222 in `PAKET_4_Bedingung.md`).
- **`btnKaSpeichern.OnSelect`**:
  - `UpdateIf(colAntworten; !Inaktiv; {Warnung: Typ = "ZAHL" && Grenzmodus = "Warnen" && fnAusserhalb(...)})` steht nach „Kommentar leeren“ und vor dem JSON.
  - `Warnung` ist in der `ShowColumns`-Liste des JSON.
  - Die Feldverweise im Änderungsdatensatz sind dasselbe Muster wie die bestehende Zeile für „Kommentar leeren“. Geschlussfolgert: gültig.
  - Warnung ist nur dann wahr, wenn der Kommentar Pflicht ist (`fnKommentarNoetig` enthält die Warnen-Bedingung). Der Kommentar wird beim „Kommentar leeren“ nicht gelöscht, weil `fnKommentarNoetig` wahr ist.
- **Nur-Ansicht**: `lblKaZahlInfo.Text`, `lblKaZahlInfo.Color` und `txtKaZahl.BorderColor` lesen bei `varNurLesen` nur `ThisItem.Warnung` und nicht `fnAusserhalb` oder den Kommentar.
  - Die Argumentzahl der Text-`If` ist ungerade (11), also gibt es ein Sonst.
  - Die Reihenfolge Bewertung = NIO vor Nur-Lesen vor Bearbeiten ist sinnvoll. Im Bearbeiten-Modus liefern Mangel und Sperren über die erste Bedingung rot.
  - Altes JSON ohne `Warnung` ergibt `false`, also keine Hinweiszeile. Das ist plausibel, weil es vor Paket 3 keinen Warnen-Modus gab.
- **Protokoll** (`htmProtokoll.HtmlText`, 3.7 und 4.7): `w: Coalesce(IfError(Boolean(a.Value.Warnung); false); false)` ist auch bei fehlendem Feld im alten JSON `false`. Das `If(b = "NIO"; rot; w; orange; grün)` ist gültig mit ungeradem Argumentzähler. Der orange Zusatz erscheint nur bei `w`.
- **Studio mit `powerfxv1 = false`**: Kein Syntax- oder Typfehler gefunden. Klammern und `;`/`;;` stimmen. Das `As` an `Concat(Filter(...) As a; ...)` in 4.7 ist die zulässige Form (nicht `Concat(Filter(... As x ...); x.Feld)`).

### B) Paket 4, Speichern (4.6)
- **Reihenfolge** (belegt, im Block):
  1. `colVersteckt` direkt im Sonst-Zweig, vor `colFotoNeu` und dem Upload.
  2. Upload, Prüfung „Fotos fehlgeschlagen“, Links anhängen und `Uebernommen` nur für sichtbare Punkte (`!(PruefpunktID in colVersteckt.PruefpunktID)` an allen fünf Stellen).
  3. Kommentar leeren.
  4. Warnung setzen.
  5. `ClearCollect(colSpeichern; …)`.
  6. JSON aus `colSpeichern`.
  7. `Patch`, mit `AnzahlNIO` aus `colSpeichern`.
  8. Refresh und Nachlese.
  Keine dieser Anweisungen ändert die Eingaben für `colVersteckt` (`Bewertung`, `WertText`, `WertZahl` bleiben), und `colVersteckt` bleibt gültig.
- **`ClearCollect(colSpeichern; ForAll(colAntworten As r; If(…)))`**:
  - Drei Zweige: versteckt → `Patch(r; {…})`, Inaktiv → `r`, sonst → `Patch(r; {Ausgeblendet: false})`.
  - Alle liefern denselben Datensatztyp wie `colAntworten`.
  - Patch auf einen Datensatz mit zwei Datensätzen (Record, Record) ist gültig.
  - `WertZahl: Blank()` ändert den Typ nicht. Selbst wenn ein Blank im Zusammenführen den Altwert nicht überschriebe, blieben die Werte im JSON, aber Bewertung ist `""`, Protokoll und Nur-Ansicht blenden aus, und Mängel und `AnzahlNIO` zählen nur `Bewertung = "NIO"`. Folgenlos.
  - `x in colVersteckt.PruefpunktID` ist gültig. Bei leerer Sammlung ist das Ergebnis `false`.
  - `colVersteckt` fehlt auch bei „keine versteckten“ nicht. Das `ClearCollect` legt die Spalte `PruefpunktID` an.
  - Inaktive Altlasten (Zweig 3) sind aus `colVersteckt` ausgeschlossen und behalten Bewertung und `Ausgeblendet` aus dem JSON.
- **`ShowColumns(colSpeichern; …Warnung; Ausgeblendet)`**: Alle Spalten existieren in `colSpeichern`. Bezeichner statt Text (`supportcolumnnamesasidentifiers`) ist eingehalten.
- **Nachlese**: `varNachlese.Antworten = varAntwortJSON` vergleicht dasselbe `varAntwortJSON`, das geschrieben wurde. Keine Änderung zur Vorversion.
- **Plausibilität im Abschluss** (`btnRuAbschluss`, Export `scrRundgang` Zeilen 372 bis 391):
  - Mängel kommen aus dem JSON mit `Text(a.Value.Bewertung) = "NIO"`. Ausgeblendete haben `""`.
  - `AnzahlNIO` wird aus `colSpeichern` mit `Bewertung = "NIO"` gezählt. Beide Zähler arbeiten auf denselben Zeilen, einschließlich der Altlasten. Die Summe stimmt.
  - Die neuen JSON-Felder `Warnung` und `Ausgeblendet` werden dort nicht gelesen oder gebraucht, also keine Auswirkung.
  - Warnung-Zeilen haben Bewertung IO und zählen nicht als Mangel.
- **Fotos und Links ausgeblendeter Punkte**: Neue Fotos werden nicht hochgeladen und nicht als `Uebernommen` markiert. Bestehende Links werden im JSON geleert (dokumentiert). `Clear(colFotos)` folgt nur nach bestätigter Nachlese.
- **Abbruch mitten im Speichern**:
  - `colAntworten` wird nie durch das Ausblenden verändert, nur `Fotos` (sichtbare, angehängt) und `Kommentar`/`Warnung`.
  - Setzt der Prüfer A zurück, kommt B mit seinen Eingaben und seinen Links zurück.
  - Ein erneutes Speichern lädt nichts doppelt hoch, weil `Uebernommen` und `Url` gesetzt sind.
  - Siehe nur N1 (verwaiste Datei).
- **Altes JSON ohne `Ausgeblendet`/`Warnung`**: `Coalesce(IfError(Boolean(...)); false)` in `OnVisible`, Protokoll und Filter in 4.7 ergibt sichtbar und keine Warnung. Der Filter `!Coalesce(IfError(Boolean(ThisRecord.Value.Ausgeblendet); false); false)` ist in `Filter(Table(ParseJSON(...)); ...)` auf nicht typisierten Werten gültig.

## Anzahl
hoch 0, mittel 0, niedrig 1 (N1, kein Eingriff nötig).

Nicht in Studio ausgeführt. Alles belegt am Text der Pakete und am Export. Die Gültigkeit von `UpdateIf` mit Feldverweisen im Änderungsdatensatz und `Patch(Record; Record)` ist geschlussfolgert aus bekannten Mustern (die erste Form steht ähnlich schon in Paket 1).
