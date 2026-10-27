# Prüfung Paket 3 (Grenzen) und Paket 4 (Bedingte Fragen)

Prüfer: unabhängiger Prüf-Agent, 27.10.2026. Grundlage: `export/*.pa.yaml` (27.10. 09:09), `export/SPALTEN.md`, Pakete 1–4.
Kennzeichnung: **belegt** = aus Export/Blöcken maschinell oder durch Lesen nachgewiesen, **geschlussfolgert** = abgeleitet, nicht in Studio getestet.

## Kurzfassung

- **Kein hoher Befund.** Syntax, Klammern, Argumentanzahl und Vorher-Fassungen sind in beiden Paketen in Ordnung (maschinell geprüft).
- **Paket 3:** Die Nur-Ansicht zeigt „außerhalb, begründet“ nach den **heutigen** Stammdaten, nicht nach dem gespeicherten Kennzeichen `Warnung` (mittel). Dazu kleinere Punkte: Kennzeichen geht bei deaktivierten Punkten verloren, Text nennt `clrWarnungHell`, das es nicht gibt, Lücken im Testbogen.
- **Paket 4:** T4.10 prüft den sicheren Ausfall nicht, weil A dort schon n.i.O. ist (mittel). Ausgeblendete Punkte werden **vor** Upload und Nachlese in `colAntworten` geleert. Scheitert das Speichern, sind die Eingaben trotzdem weg und Foto-Links können verloren gehen (mittel). Dazu kleinere Punkte zu Rückweg, Pflegehinweisen und Testbogen.

---

## Befunde

### Paket 3

**B3-1 · Paket 3 · mittel · `lblKaZahlInfo.Text`, `lblKaZahlInfo.Color`, `scrKategorie.OnVisible` (Zweig Nur-Ansicht) · belegt**
- Befund: Die Kurzfassung sagt: „Gespeichert mit Kennzeichen `Warnung`: … die Nur-Ansicht ‚außerhalb, begründet‘“. Der Zweig Nur-Ansicht in `OnVisible` liest `a.Warnung` aber nicht. `MinWert`/`MaxWert` kommen dort aus `pp` (den **aktuellen** Stammdaten). `lblKaZahlInfo` entscheidet in der Nur-Ansicht nur über `!fnAusserhalb(WertZahl; MinWert; MaxWert)`.
- Szenario a: Ein Punkt im Modus **Mangel** wurde mit 15 gespeichert (Soll 6–16, also i.O.). Später wird Max in SharePoint auf 14 gesenkt. „Ansehen“ zeigt dann orange „außerhalb, begründet“, obwohl nie etwas begründet wurde. Das Protokoll (liest `Warnung`) zeigt richtig grün. Gleiches gilt für einen Punkt im Modus **Sperren**.
- Szenario b: Ein Punkt im Modus **Warnen** wurde mit 18,5 begründet gespeichert. Später wird Max auf 20 erhöht. Die Nur-Ansicht zeigt keinen Hinweis mehr, das Protokoll zeigt weiter „(außerhalb Soll, begründet)“. Die beiden Anzeigen widersprechen sich.
- Vorschlag: Ein Feld `Warnung` in alle drei Zweige von `colAntworten` aufnehmen (gleiches Schema): Nur-Ansicht `Coalesce(IfError(Boolean(a.Warnung); false); false)`, Bearbeiten `false`, inaktiv aus `o.Value.Warnung`. In `lblKaZahlInfo.Text`/`.Color` für `varNurLesen` nur `ThisItem.Warnung` verwenden (`varNurLesen && ThisItem.Warnung` → „außerhalb, begründet“/orange, sonst nichts). Alternativ die Kurzfassung korrigieren („Nur-Ansicht nach aktuellen Grenzen“).

**B3-2 · Paket 3 · niedrig · `btnKaSpeichern.OnSelect` (JSON-Zeile) und Zweig „inaktiv“ in `OnVisible` · belegt**
- Szenario: Z2 (Warnen) wird außerhalb und begründet gespeichert, das JSON enthält `Warnung: true`. Danach wird Z2 deaktiviert, und die Kategorie wird in derselben Durchführung erneut gespeichert. Die inaktive Zeile hat `Grenzmodus: "Mangel"` und `MinWert/MaxWert: Blank()`. `AddColumns(…; Warnung; Typ = "ZAHL" && Grenzmodus = "Warnen" && …)` ergibt deshalb `false`, und das Kennzeichen geht verloren. Im Protokoll steht der Wert dann grün als „i.O.“ mit grauem Kommentar, ohne „(außerhalb Soll, begründet)“. Der Kommentar selbst bleibt erhalten (`UpdateIf` nur `!Inaktiv`).
- Vorschlag: Zusammen mit B3-1 das gespeicherte `Warnung` in der inaktiven Zeile mitführen und in `AddColumns` `If(Inaktiv; Warnung; Typ = "ZAHL" && …)` nehmen. Dafür braucht die Spalte einen anderen Namen, etwa `WarnungAlt`, sonst kollidiert `AddColumns` mit einem vorhandenen Feld.

**B3-3 · Paket 3 · niedrig · Text Schritt 3.3 · belegt**
- „Neu: Farben clrWarnung/clrWarnungHell“, im Block steht aber nur `clrWarnung`. Es gibt keinen Aufrufer, also keinen Fehler in Studio. Josias könnte jedoch nach der fehlenden Farbe suchen oder sie selbst ergänzen.
- Vorschlag: Text auf „clrWarnung“ korrigieren.

**B3-4 · Paket 3 · niedrig · `lblKaZahlInfo.Text`, Regel Min > Max · belegt**
- Szenario: Sperren mit Min 16, Max 6 (T3.11). Die Beschriftung lautet „zulässig ab 16 bis 6 · außerhalb des Sollbereichs“, obwohl der Punkt als Mangel wirkt. Der Schutz gilt außerdem nur für Sperren: Bei **Warnen** mit Min > Max liegt jeder Wert „außerhalb“ und verlangt immer eine Begründung. Bei **Mangel** wird jeder Wert n.i.O. (das war schon vorher so).
- Vorschlag: „zulässig“ nur bei `ThisItem.Grenzmodus = "Sperren" && fnSperreGilt(ThisItem.MinWert; ThisItem.MaxWert)`, sonst „Soll“. In der Pflegeregel (Schritt 3.2) ergänzen: Min ≤ Max in allen Modi.

**B3-5 · Paket 3 · niedrig · `lblKaZahlInfo.Text` · belegt**
- Szenario: Bei Warnen steht „außerhalb, bitte begründen“ auch noch da, nachdem die Begründung eingetragen ist (T3.10 erwartet das sogar). Das ist nur eine Frage der Darstellung.
- Vorschlag: Bei `Trim(ThisItem.Kommentar) <> ""` „außerhalb, begründet“ anzeigen.

**B3-6 · Paket 3 · niedrig · Testbogen / Schritt 3.2 · belegt**
- Für Z1–Z3 fehlen „Aktiv = Ja“ und ausdrücklich „Eingabetyp ZAHL, Kategorie = K1“. `colPP` filtert `Aktiv = true`, ohne diese Angaben erscheinen die Punkte nicht. Paket 4 nennt „Aktiv = Ja“, Paket 3 nicht.
- Es fehlt ein Aufräumschritt. Z1–Z3 bleiben als Pflichtpunkte aktiv in K1 und müssen in jedem weiteren Rundgang ausgefüllt werden, auch in T4.6 (dort nicht erwähnt).
- T3.11 sagt nicht, dass die Änderung (Z3 = 12) **nicht gespeichert** werden darf, also „Zurück → Verwerfen“ oder Vorschau neu starten.
- Vorschlag: Die drei Punkte ergänzen. Aufräumen: Z1–Z3 nach Paket 4 auf „Aktiv = Nein“ setzen.

**B3-7 · Paket 3 · niedrig · Rückweg · geschlussfolgert**
- Nach dem Rückweg rechnet die alte App einen mit Warnen gespeicherten Wert beim „Bearbeiten“ als n.i.O. (alte `fnZahlBewertung`). Ein erneutes Speichern erzeugt dann beim Abschluss einen Mangel. Ohne erneutes Speichern bleibt der Wert i.O. und das Protokoll zeigt ihn grün ohne Hinweis. Der Rückweg-Text sagt dazu nichts.
- Vorschlag: Einen Satz im Rückweg ergänzen.

**B3-8 · Paket 3 · niedrig · Pflegehinweis Sperren · geschlussfolgert**
- Szenario: In einer laufenden Durchführung wird ein Punkt von Mangel auf Sperren umgestellt, nachdem schon ein Wert außerhalb gespeichert war. Beim „Bearbeiten“ ergibt sich `Bewertung ""` und „unzulässiger Wert“, sodass die Kategorie erst nach Änderung des echten Messwerts gespeichert werden kann. Die Kurzfassung warnt nur allgemein.
- Vorschlag: Im Pflegehinweis ergänzen: Grenzmodus nicht umstellen, solange Rundgänge in Arbeit sind.

**B3-9 · Paket 3 · niedrig · `lblKaZahlInfo` (Layout) · geschlussfolgert**
- Der längste Text, etwa „°C  ·  zulässig ab −50 bis 150  ·  unzulässig, bitte prüfen“ (rund 55 Zeichen, Größe 14), braucht bei `Width = Parent.Width - 256` und Tablet-Breite 2 Zeilen. Das passt in `Height 56`. Bei Breite unter etwa 650 px werden 3 Zeilen daraus und die dritte wird abgeschnitten.
- Vorschlag: Im Test auf dem kleinsten Zielgerät prüfen.

### Paket 4

**B4-1 · Paket 4 · mittel · Testbogen T4.10 · belegt**
- Szenario: Nach T4.8 ist A als **n.i.O.** gespeichert. T4.9 und T4.10 starten die Vorschau neu, dabei werden nicht gespeicherte Änderungen verworfen. In T4.10 („BedingungWert = Rot … K1 Bearbeiten → B immer sichtbar“) ist A also n.i.O. B wäre damit auch bei **gültiger** Bedingung sichtbar. Der Test kann den sicheren Ausfall weder belegen noch widerlegen.
- Vorschlag: In T4.10 ergänzen: „A auf i.O. → B bleibt sichtbar (ungültiger Wert → sicherer Ausfall); Zurück, Verwerfen“.

**B4-2 · Paket 4 · mittel · `btnKaSpeichern.OnSelect` (Reihenfolge `UpdateIf` vor Upload/Nachlese) · belegt (Ablauf), geschlussfolgert (Folgen)**
- Befund: `ClearCollect(colVersteckt …)` und `UpdateIf(colAntworten; … in colVersteckt …; {Bewertung: ""; WertText: ""; …; Fotos: ""; Ausgeblendet: true} …)` laufen **vor** dem Foto-Upload, der Fehlerverzweigung „Foto(s) konnten nicht hochgeladen werden“, dem Patch und der Nachlese.
- Szenario a: A wird auf i.O. gestellt, B (mit „Leck“) ist ausgeblendet. Speichern scheitert, weil ein Foto eines anderen Punkts nicht hochlädt oder die Nachlese nicht stimmt. Der Prüfer merkt den Fehler und stellt A wieder auf n.i.O. B erscheint **leer**, obwohl nichts gespeichert wurde. Das widerspricht der Zusage aus T4.5 („noch nicht gespeichert, also nicht verloren“).
- Szenario b: B hatte in einem früheren, gescheiterten Versuch derselben Sitzung schon ein hochgeladenes Foto (`Url` gesetzt, `Uebernommen` false). Danach wird B ausgeblendet. Die Link-Anhängung schließt B aus, aber `UpdateIf(colFotos; !Uebernommen && !IsBlank(Url); {Uebernommen: true})` markiert das Foto trotzdem als übernommen. Der Link ist weg, die Datei liegt ohne Verweis in RG_Fotos. Wird B danach wieder eingeblendet, zählt das Foto nicht mehr, bei Foto = Pflicht muss neu fotografiert werden.
- Vorschlag: `colAntworten` nicht verändern. Das JSON und `AnzahlNIO` aus einer Projektion bilden, etwa `ForAll(colAntworten As r; If(r.PruefpunktID in colVersteckt.PruefpunktID; Patch(r; {Bewertung: ""; WertText: ""; WertZahl: Blank(); Kommentar: ""; Fotos: ""; Ausgeblendet: true}); Patch(r; {Ausgeblendet: false})))`. `Patch(Record; Record)` ist erlaubt. Den Uebernommen-Schritt auf sichtbare Punkte beschränken: `UpdateIf(colFotos; !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID); {Uebernommen: true})`. Mindestens aber das `UpdateIf` der Ausgeblendeten erst nach erfolgreichem Upload ausführen und den Uebernommen-Filter ergänzen.

**B4-3 · Paket 4 · niedrig · `btnKaSpeichern.OnSelect` · belegt**
- Szenario: B ist ausgefüllt und hat neue Fotos. A wird versehentlich auf i.O. gestellt, dann wird gespeichert. Werte, Kommentar und Fotos von B werden **ohne jeden Hinweis** verworfen: nicht hochgeladen, nach Erfolg `Clear(colFotos)`. Das ist so gewollt (Kurzfassung), der Prüfer bemerkt den Verlust aber nicht.
- Vorschlag: Nach dem Speichern bei `CountRows(Filter(colFotos; PruefpunktID in colVersteckt.PruefpunktID)) > 0` oder bei geleerten Werten eine Information anzeigen („n ausgeblendete Punkte wurden geleert“).

**B4-4 · Paket 4 · niedrig · Ausblenden bereits gespeicherter Fotos · belegt**
- Szenario: B wurde mit Foto gespeichert. Beim späteren „Bearbeiten“ wird A auf i.O. gestellt und gespeichert. `Fotos: ""` entfernt den Link aus dem JSON, die Datei bleibt in RG_Fotos ohne Verweis. Sie erscheint weder im Protokoll noch im Mangel und wird nicht aufgeräumt (Datenschutz und Aufbewahrung).
- Vorschlag: In Kurzfassung und Betriebshinweis aufnehmen. Bei Bedarf später ein Aufräum-Flow (nicht in diesem Paket).

**B4-5 · Paket 4 · niedrig · Schritt 4.2 (Pflegehinweis), `fnBedGueltig` · belegt**
- Bei A = ZAHL mit Grenzmodus **Sperren** liefert ein Wert außerhalb `Bewertung ""` (Paket 3), ein Wert innerhalb liefert „IO“. „NIO“ kommt nur bei Min > Max vor. Eine Bedingung „NIO“ an einem Sperren-Punkt ist damit nie erfüllt. B bleibt dauerhaft ausgeblendet und wird beim Speichern immer geleert, ohne dass der sichere Ausfall greift. Der Hinweis nennt nur Warnen.
- Nebenbei: `fnBedNorm` entfernt „.“ und Leerzeichen auch in Auswahlwerten von A. „1.5 bar“ und „15 bar“ gelten dann als gleich (theoretisch).
- Vorschlag: Im Hinweis „Warnen **und Sperren**: keine Bedingung auf NIO“ schreiben. Oder in `fnSichtbar`/`fnBedGueltig` bei `bTyp = "ZAHL"` nur „IO“/„*“ als gültig zulassen. Das wäre eine Signaturänderung, wenn der Grenzmodus von A gebraucht wird.

**B4-6 · Paket 4 · niedrig · `fnSichtbar` (Erkennung „Kette“) · belegt**
- `bBid <> 0` wertet A als bedingt, auch wenn A selbst `BedingungWert` leer hat. A ist dann tatsächlich unbedingt, B wird trotzdem immer gezeigt. Das ist ein sicherer Ausfall, passt aber nicht zur Kurzfassung („A ist selbst bedingt“).
- Vorschlag: Im Pflegehinweis „BedingungPunkt nur zusammen mit BedingungWert setzen (sonst 0)“ ergänzen. Die Formel kann bleiben.

**B4-7 · Paket 4 · niedrig · Rückweg · belegt**
- „Vor dem Rückweg BedingungPunkt der Testpunkte auf 0 setzen“ wirkt in der alten App nicht, weil sie die Spalte gar nicht liest. Dort ist B (Pflicht = Ja) **immer** sichtbar und Pflicht. Jede K1-Kategorie lässt sich dann nur mit ausgefülltem B speichern.
- Vorschlag: Vor dem Rückweg B auf **Aktiv = Nein** setzen, oder Pflicht = Nein für alle bedingten Punkte.

**B4-8 · Paket 4 · niedrig · Testbogen Vorbedingungen und Ablauf · belegt**
- „Neue Durchführung (K1 noch nicht gespeichert)“: Pro Rundgang und Tag gibt es genau eine Durchführung (Schlüssel `R<id>-<Tag>`, `btnRgAktion`). Nach den Tests aus Paket 1–3 ist K1 am selben Tag schon gespeichert. Eine neue Durchführung geht nur an einem Nachholtag (`cfgNachholTage` ≥ 1) oder mit einem anderen Rundgang. Für T4.1–T4.8 ist das aber nicht nötig, weil A dort als i.O. gespeichert ist und B anfangs ausgeblendet bleibt. Die Vorbedingung lässt sich also lockern.
- T4.12 braucht ebenfalls einen anderen Tag. Das ist nur machbar, wenn NachholTage ≥ 1 ist oder an einem späteren Tag.
- T4.6 „übrige Punkte ausfüllen“ schließt Z1–Z3 aus Paket 3 ein (Z1 außerhalb → Kommentar, Z3 nur im Bereich). Das sollte erwähnt werden.
- T4.3 „B nicht mehr offen“ tritt erst ein, wenn das Textfeld verlassen wird (`OnChange` bei Fokusverlust). Gleiches gilt für A vom Typ TEXT/ZAHL mit Bedingung „*“: B erscheint erst nach Verlassen des Felds.
- Vorschlag: Vorbedingung „Durchführung, in der K1 bearbeitet werden kann“. Für T4.12 „Nachholtag, falls NachholTage ≥ 1, sonst am Folgetag“. Hinweise zu Z1–Z3 und „Feld verlassen“ ergänzen.

**B4-9 · Paket 4 · niedrig · Schritt 4.2 / Kurzfassung · belegt**
- „bei A = Auswahl/**Mehrfachauswahl**“ und `typ = "MEHRFACH"` in `fnBedGueltig` beziehen sich auf den Eingabetyp aus Paket 5, den es in diesem Stand noch nicht gibt. Das ist harmlos, kann Josias bei der Pflege aber verwirren.
- Vorschlag: „(ab Paket 5)“ ergänzen.

---

## Geprüft ohne Befund

**Mechanisch (belegt, Skripte in `/tmp/claude-0/-home-user/669e7a2c-198a-5710-8334-2ed3dd37c3ff/scratchpad/pruefskripte/`):**
- Vorher-Fassungen: Alle 7 Vorher-Blöcke aus Paket 3 und alle 10 aus Paket 4 sind zeichengleich mit dem Stand Export + Paket 1 + 2 bzw. + 3 (nach Rückübersetzung des Exports ins Deutsche und ohne Kommentare). Paket 1 und 2 stimmen ebenfalls mit dem Export überein.
- Diff Neu gegen Vorher: Nur die beschriebenen Änderungen, keine weiteren. Paket 3: Formulas (Farbe, `fnGrenzmodus`, `fnSperreGilt`, `fnZahlBewertung`, `fnKommentarNoetig`, `fnFehltGrund`), 3 Stellen `fnGrenzmodus` in `OnVisible` (inaktive Zeile bleibt „Mangel“), Zahlenanzeige, JSON-Zeile, Protokoll. Paket 4: Formulas (`fnBedNorm`, `fnBedGueltig`, `fnBedPasst`, `fnSichtbar`), Felder `BedID`/`BedWert`/`Ausgeblendet` in allen 3 Zweigen, Sichtbarkeitsfilter an 10 Stellen in 8 Properties, `colVersteckt` + `UpdateIf` + 3 × `!a.Ausgeblendet` + Link-Filter + `Ausgeblendet` im JSON, Protokoll-Filter. Die Kurzfassung von Paket 3 nennt `clrWarnungHell`, das fehlt (B3-3).
- Klammern und Zeichenketten in allen 17 Blöcken ausgeglichen. Keine Kommentare, keine Dezimalzahlen außerhalb von Zeichenketten, also ist die Rückübersetzung unkritisch.
- Argumentanzahl: Jeder Aufruf jeder benannten Funktion passt zur Signatur, auch im ganzen App-Stand nach Paket 4. `fnSichtbar` hat 10 Parameter, alle 10 Aufrufe (in 8 Properties) übergeben 10. `fnFehlt`/`fnFehltGrund` 12, `fnKommentarNoetig` 8, `fnZahlBewertung` 4, `fnBedPasst` 4, `fnBedGueltig` 3. `UpdateIf` hat 5 Argumente (2 Paare), `With` hat überall 2, `LookUp` 2.
- Namen: `Grenzmodus`, `BedingungPunkt`, `BedingungWert` werden in Schritt 3.2/4.2 angelegt, Studio-Aktualisieren ist beschrieben. `clrWarnung`, `colVersteckt`, `Warnung`, `Ausgeblendet`, `BedID`, `BedWert` werden vor ihrer Verwendung definiert. Steuerelemente und Pfade (`lblKaUnter` in `conKaKopf`, `conKaBalkenWert` in `conKaBalken`, `lblKaStand` in `conKaFuss`) existieren im Export.

**Studio-Gültigkeit (geschlussfolgert, Einstellungen laut HINWEIS):**
- `AddColumns(colAntworten; Warnung; …)` und `ShowColumns(…; Warnung; Ausgeblendet)` mit Bezeichnern passen zu `supportcolumnnamesasidentifiers = true`. `JSON(…)` auf eine Tabelle mit Wahrheitswerten ist erlaubt.
- `Boolean(untyped)` mit `IfError` und `Coalesce` ergibt bei fehlendem Feld (altes JSON) `false`. Im Zweig Nur-Ansicht ist `a` schon `Index(t; i).Value`, also ist `a.Ausgeblendet` richtig. Im inaktiven Zweig ist `o.Value.Ausgeblendet` richtig.
- `Filter(Table(ParseJSON(…)); … ThisRecord.Value.Ausgeblendet …) As a` in `Concat` ist gültig. Dieselbe Form läuft schon im Abschluss.
- `With` in `Filter` und `LookUp(colAntworten As b0; …)` innerhalb `Filter(colAntworten As a; …)` sind nur lesende Zugriffe, ohne Schreiben in dieselbe Sammlung. Das Schreiben läuft über `colVersteckt`, damit ist die Falle vermieden.
- `UpdateIf` mit zwei Bedingungs-Paaren und `PruefpunktID in colVersteckt.PruefpunktID` ist gültig, die Paare schließen sich gegenseitig aus.
- UDFs rufen UDFs auf, `With`/`Filter(Split … As s)` stehen in UDFs, die Reihenfolge der Definitionen spielt keine Rolle. `Boolean`-Parameter bekommen bei fehlendem Datensatz Blank, `||` bricht vorher ab (`!gef`).
- Kein `Navigate` in `OnVisible`. `Concat … As z` war schon in Paket 1 so.
- Reihenfolge beim Einfügen: Formulas zuerst, dann `OnVisible` (neue Felder), dann die Verbraucher. Kein ungültiger Zwischenstand außer den angekündigten roten Fehlern.

**Logik ohne Befund:**
- Paket 3: Mangel unverändert. Warnen ergibt „IO“, Kommentarpflicht, keinen Mangel, `Kommentar leeren` lässt die Begründung stehen. Sperren ergibt `""`, „Bereich“ blockiert auch Nicht-Pflichtpunkte, leeren hebt die Sperre auf. Ein Wert genau auf der Grenze (6/16) liegt im Bereich, 16,01 liegt außerhalb. Leere Min/Max ergeben nie „außerhalb“, mit nur einer Grenze wird einseitig geprüft. `fnSperreGilt` bei Min > Max ergibt n.i.O. (T3.11 stimmt, auch schon beim Öffnen). `AnzahlNIO` und die Abschlussprüfung `Sum(AnzahlNIO) = Mängel` bleiben gleich. Protokoll: altes JSON ohne `Warnung` ergibt `false`.
- Paket 4: Die Sichtbarkeit wird im Bearbeiten-Modus live berechnet, in der Nur-Ansicht aus dem gespeicherten Feld. Sicherer Ausfall bei A fehlt / A in anderer Kategorie / A inaktiv / A bedingt / Selbstbezug / Zyklus A↔B / Wert leer / ungültig. Schreibweisen „n.i.O.“, „NIO“ und „ nio “ sind gleich. „*“ gilt erst, wenn A beantwortet ist. Ausgeblendete Punkte zählen nicht für Zähler, Balken, n.i.O.-Zahl, „Noch offen“, Sprung (beim Öffnen und bei „Offene Punkte ↓“), Upload und Fehlermeldung zum Upload. Beim Speichern werden sie geleert und markiert. Der zweite Teil von `UpdateIf` setzt `Ausgeblendet` nach einem gescheiterten Versuch zurück. Inaktive Zeilen behalten ihr Kennzeichen. Protokoll und Nur-Ansicht lassen ausgeblendete Zeilen weg. Abschluss: Geleerte Zeilen haben `Bewertung ""`, `AnzahlNIO` wird nach dem Leeren gezählt, die Prüfung bleibt also stimmig. Altes JSON ohne `Ausgeblendet` gilt als sichtbar (T4.13). Bei zwei gleichzeitigen Prüfern greift die `GespeichertAm`-Prüfung unverändert. Netzfehler und Nachlese sind unverändert (bis auf B4-2). Eine Kategorie zweimal speichern ist unkritisch, weil `colAntworten` beim Öffnen neu aufgebaut wird.
- Nicht angepasste Stellen: Abschluss (`scrRundgang.btnRuAbschluss`) ignoriert die neuen JSON-Felder. `btnKaSpeichern.Text`, die Kartenhöhe, der Foto-Dialog (modal, A kann sich bei offenem Dialog nicht ändern) und das Archiv-PDF (übernimmt `htmProtokoll`) wirken richtig. `CountRows(Filter(colAntworten; !Inaktiv)) = 0` zählt Ausgeblendete mit, das ist unkritisch.

## Anzahl je Schwere

| Schwere | Paket 3 | Paket 4 | Summe |
|---|---|---|---|
| hoch | 0 | 0 | **0** |
| mittel | 1 (B3-1) | 2 (B4-1, B4-2) | **3** |
| niedrig | 8 | 7 | **15** |
