# Prüfergebnis Paket 5 (Typen) und Paket 6 (Beispielbild)

Prüfer: unabhängiger Prüf-Agent, 27.10.2026. Ich habe nur gelesen und keine Datei geändert außer dieser.
Grundlage: `export/*.pa.yaml` (Export 27.10. 09:09), `SPALTEN.md`, Pakete 1–6. Den Stand nach Paket 4 bzw. 5 habe ich maschinell aus Export + Blöcken 1..n−1 aufgebaut (Skript im Scratchpad `rv2tools/`).
Kennzeichnung: **belegt** = aus Export/Paket nachgewiesen, **geschlussfolgert** = aus bekanntem Verhalten der Steuerelemente abgeleitet, **UNSICHER** = nur in Studio/Gerät zu klären.

## Kurzfassung

- **Kein hoher Befund.** Syntax, Klammern, YAML, Versionen, Namen, Spalten und Vorher-Fassungen sind in Ordnung (siehe „Geprüft ohne Befund“).
- **Mittel (2):** P5-1: Die klassische Datumsauswahl lässt sich nicht leeren. Wer bei einem freiwilligen DATUMZEIT-Punkt aus Versehen ein Datum wählt, muss danach eine Uhrzeit eintragen und kann sonst nicht speichern. P6-1: Bei Punkten mit Bild ist der Fragetext 160 px schmaler, bei fester Höhe von 32 px. Längere Fragen werden dann abgeschnitten.
- Dazu 14 niedrige Befunde, vor allem zu Testbogen, Standardwerten der Steuerelemente und Randfällen.

---

## Befunde

### P5-1 · Paket 5 · mittel · `dpKaDatum` (dazu `fnFehltGrund`, Zweig „Uhrzeit“)
**Szenario (geschlussfolgert):** Die klassische Datumsauswahl (Classic/DatePicker@2.6.0) hat keine Funktion zum Leeren. `IsEditable` steht auf dem Standardwert `false`, löschen per Tastatur geht also auch nicht. Ist ein Datum einmal gewählt, bleibt es bis zum Speichern stehen.
- Freiwilliger DATUM-Punkt, Datum aus Versehen gewählt: Es wird ein falscher Wert gespeichert und steht im Protokoll.
- Freiwilliger DATUMZEIT-Punkt, Datum aus Versehen gewählt: `fnFehltGrund` meldet „Uhrzeit“, auch ohne Pflicht (`typ = "DATUMZEIT" && wt <> "" && Len(wt) < 16`). Der Prüfer muss eine erfundene Uhrzeit eintragen, sonst lässt sich die Kategorie nicht speichern.

**Vorschlag:** Einen kleinen Knopf „✕“ (`btnKaDatumLeeren`, Classic/Button) rechts neben den Feldern ergänzen:
- `Visible = !varNurLesen && (ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && ThisItem.WertText <> ""`
- `OnSelect = Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: ""});; Reset(dpKaDatum);; Reset(ddKaStunde);; Reset(ddKaMinute);; Set(varGeaendert; true)`

`Reset` auf Geschwister in derselben Galeriezeile ist erlaubt. Bei DATUM ist bis X = 272 Platz, bei DATUMZEIT ab X = 504. Alternativ den Zweig „Uhrzeit“ an `pflicht` koppeln. Dann wird bei freiwilligen Punkten aber ein Datum ohne Uhrzeit gespeichert.

### P5-2 · Paket 5 · niedrig · Testbogen T5.5–T5.8
**Szenario (belegt aus der Testfolge + P5-1):** T5.7 („erst Stunde/Minute, dann Datum“) soll nach T5.5/T5.6 laufen. Die Ablesezeit hat dann aber schon ein Datum, und das lässt sich nicht entfernen (P5-1). Der Test ist so nicht ausführbar.
- Das Ergebnis „ergibt TT.MM.JJJJ 07:05“ ist in der Karte nicht zu sehen, erst im Protokoll (T5.9).
- T5.8 „Speichern, Kategorie wieder öffnen“: Speichern geht nur, wenn alle übrigen Pflichtpunkte von K1 ausgefüllt sind. Danach öffnet die Übersicht über `varWeiter` von selbst die nächste Kategorie. Beides fehlt im Testtext (in Paket 4, T4.6 steht es).

**Vorschlag:** T5.7 mit einem vierten Testpunkt „ZZ Test Ablesezeit 2“ (DATUMZEIT) oder in einer neuen Durchführung machen. Prüfung: „Fuß zählt den Punkt nicht mehr“, Text dann in T5.9. T5.8: „übrige Punkte ausfüllen, Speichern, in der Übersicht K1 → Bearbeiten“.

### P5-3 · Paket 5 · niedrig · `ddKaStunde.OnChange`/`ddKaMinute.OnChange`/`.Default`
**Szenario (geschlussfolgert):** Wählt man Stunde/Minute vor dem Datum, speichert die App nichts (`fnDatumText` gibt bei leerem Datum "" zurück). Die Auswahl steckt nur im Zustand der Liste. Die Galerie (VariableHeight) baut Zeilen beim Scrollen neu auf, oder sie rücken nach, wenn sich eine Bedingung ändert (Paket 4). Dann springen die Listen auf `Default` = "" zurück. Der Prüfer wählt später das Datum, und der Fuß meldet „(Uhrzeit)“, obwohl er die Zeit eingetragen hatte.
Gleiches Muster: Ist der Wert vollständig und setzt man die Minute auf leer, wird `WertText` zu „TT.MM.JJJJ“. Damit springt auch `ddKaStunde.Default` auf "" und die Stunde ist weg.

**Vorschlag:** Stunde/Minute erst freigeben, wenn ein Datum gewählt ist: `DisplayMode = If(varNurLesen; DisplayMode.View; IsBlank(dpKaDatum.SelectedDate); DisplayMode.Disabled; DisplayMode.Edit)`. Dazu `DisabledFill`/`DisabledColor` setzen. Dann T5.7 umschreiben („Stunde/Minute vor dem Datum gesperrt“). Die Kurzfassung nennt T5.7 als Ziel, das wäre dann eine Änderung des Verhaltens → kurz mit dem Auftraggeber abstimmen.

### P5-4 · Paket 5 · niedrig · `dpKaDatum` (fehlende Properties `InputTextPlaceholder`, `Format`, `Language`)
**Szenario (geschlussfolgert):** Der Block lässt diese Properties weg, sie bekommen ihre Standardwerte.
- `InputTextPlaceholder` zeigt beim klassischen DatePicker standardmäßig ein Beispieldatum (31.12.2001) in grauer Schrift. Ein leeres Datum sieht dann wie ausgefüllt aus, gerade in der Nur-Ansicht bei freiwilligen Punkten.
- `Format` ist ShortDate in der Gerätesprache. Auf einem englisch eingestellten Tablet steht „10/27/2026“ im Feld, im Protokoll aber „27.10.2026“. Gespeichert wird richtig.

**Vorschlag:** Im YAML ergänzen: `InputTextPlaceholder: ="Datum wählen"`, `Language: ="de-DE"`, eventuell `Format: =DateTimeFormat.ShortDate`. UNSICHER: Den Standardtext des Platzhalters in Studio prüfen.

### P5-5 · Paket 5 · niedrig · UNSICHER · `cboKaMehrfach.OnChange`, `ddKaStunde/ddKaMinute.OnChange`, `dpKaDatum.OnChange`
**Szenario (geschlussfolgert, UNSICHER):** Bei klassischen Listen und Kombinationsfeldern kann `OnChange` auch dann auslösen, wenn sich `Default`/`DefaultSelectedItems` ändert (zum Beispiel wenn die Galerie nach `ClearCollect` neue Datensätze bekommt). Dann steht direkt nach dem Öffnen `varGeaendert = true`, und „‹ Kategorien“ fragt „Verwerfen?“, ohne dass etwas geändert wurde. Beim Kombinationsfeld kommt hinzu: Jeder Patch ändert `DefaultSelectedItems` → das Feld wird zurückgesetzt, die Liste klappt eventuell nach jedem Tippen zu. `ddKaAuswahl` nutzt im Export dasselbe Muster (belegt), dort ist nichts gemeldet.

**Vorschlag:** Test ergänzen: eine gespeicherte Kategorie mit allen drei neuen Typen öffnen und sofort „‹ Kategorien“ tippen → Erwartung: keine Rückfrage. Dazu im Kombinationsfeld drei Werte nacheinander wählen → die Liste bleibt offen, alle drei sind gewählt. Tritt es auf: `Set(varGeaendert; true)` nur, wenn sich der Wert ändert (`If(neu <> ThisItem.WertText; …)`).

### P5-6 · Paket 5 · niedrig · UNSICHER · `dpKaDatum.DefaultDate`, `ddKaStunde/ddKaMinute.Default` (Fehlerklasse F-L11)
**Szenario (geschlussfolgert):** Ein Datum wählen, ohne zu speichern „‹ Kategorien“ → „Verwerfen“, dieselbe Kategorie wieder öffnen. `WertText` ist wieder "", `DefaultDate` bleibt Blank, hat sich also **nicht geändert**. Wenn die Galeriezeile ihren Steuerelementzustand behält, zeigt die Datumsauswahl das alte Datum, obwohl nichts gespeichert ist. Der Fuß zählt den Punkt als offen, die Karte zeigt ein Datum, und leeren lässt es sich nicht (P5-1). `Reset(galKaPruefpunkte)` setzt nach meinem Verständnis nur die Auswahl der Galerie zurück, nicht die Steuerelemente in den Zeilen. Gleiches Muster wie `txtKaText` im Export.

**Vorschlag:** Den Fall als Test aufnehmen. Hält sich der alte Wert: `DefaultDate`/`Default` über eine Variable bei jedem Öffnen umschalten (zum Beispiel `varKaOeffnung` in `OnVisible` hochzählen und in `If(varKaOeffnung > 0; …)` einbauen) oder die Galerie mit neuen Datensätzen erzwingen.

### P5-7 · Paket 5 · niedrig · `fnFehltGrund` (Pflicht DATUM/DATUMZEIT/MEHRFACH)
**Szenario (geschlussfolgert):** Der Eingabetyp eines Punkts wird in SharePoint von TEXT auf DATUM/DATUMZEIT umgestellt, während eine Durchführung mit gespeichertem Wert noch in Arbeit ist. `WertText` (zum Beispiel „erledigt“) bleibt stehen. Die Datumsauswahl zeigt leer (`IfError` → Blank), aber `wt <> ""` zählt als ausgefüllt. Bei DATUMZEIT passiert das mit Texten ab 16 Zeichen. Gespeichert und im Protokoll angezeigt wird der unsichtbare alte Text. Beim Wechsel AUSWAHL → MEHRFACH ist das unkritisch.

**Vorschlag:** In der Pflichtprüfung `IsError(DateValue(Left(wt; 10); "de-DE"))` als „Wert fehlt“ werten, oder in der SharePoint-Anleitung festhalten: Eingabetyp nur ändern, wenn keine Durchführung in Arbeit ist.

### P5-8 · Paket 5 · niedrig · `cboKaMehrfach.OnChange` / `.Height`
**Szenario (geschlussfolgert):** `Concat(Self.SelectedItems; …)` speichert in der Reihenfolge der Klicks. Wer erst Leck, dann Riss wählt, bekommt „Leck; Riss“. Die Erwartung in T5.9 („Riss; Leck“) stimmt dann nur zufällig, und dieselbe Antwort steht in verschiedenen Protokollen verschieden da. Zweitens UNSICHER: Bei vielen oder langen Werten passen die gewählten Einträge nicht in 460 × 56. Ein klassisches Kombinationsfeld wächst nicht mit, besonders in der Nur-Ansicht sind dann Werte verdeckt.

**Vorschlag:** In der Reihenfolge der Auswahlwerte speichern:
`Concat(Filter(ForAll(Split(ThisItem.Auswahl; ";") As s; {Value: Trim(s.Value)}) As w; w.Value <> "" && w.Value in Self.SelectedItems.Value); w.Value; "; ")`
(lokal, `in` unproblematisch). Dazu einen Test mit allen Werten einer langen Liste in Bearbeiten und in der Nur-Ansicht.

### P5-9 · Paket 5 · niedrig · Schritt 5.5 (Einfügen des Kombinationsfelds) und fehlende Stil-Properties
**Szenario (geschlussfolgert):** Ist die Funktion „moderne Steuerelemente“ an, steht unter „Eingabe“ auch das **moderne** Kombinationsfeld, unter einem fast gleichen Namen. Dort gibt es `DisplayFields`, `SearchFields`, `ChevronBackground`, `SelectionFill` nicht. Josias bekäme rote Fehler oder fehlende Properties, ohne zu wissen warum. Außerdem fehlen gegenüber `ddKaAuswahl` die Properties `Fill`, `Color`, `HoverFill`, `ChevronHoverBackground`/`ChevronHoverFill`, `PaddingLeft`, `SelectionTagFill`/`SelectionTagColor`. Die Einträge erscheinen dann in der Standardfarbe des Designs statt in `clrPrimaer`, und das Feld sieht anders aus als die Auswahlliste daneben.

**Vorschlag:** Den Weg genau nennen („Einfügen → Klassisch → Kombinationsfeld“) mit einer Kontrolle: Im Property-Auswahlfeld muss `DisplayFields` stehen. Die Stil-Properties wie bei `ddKaAuswahl` ergänzen (`Fill = clrKarte`, `Color = clrText`, `HoverFill = clrPrimaerHell`, `PaddingLeft = 12`, `SelectionTagFill = clrPrimaer`, `SelectionTagColor = Color.White`).

### P5-10 · Paket 5 · niedrig · Schritt 5.2 (Doku)
**Szenario (belegt):** Der Satz „sonst kennt die App die neue Spalte nicht“ ist aus Paket 1–4 übernommen. Paket 5 legt keine Spalte an, nur Auswahlwerte (`Eingabetyp.Value` ist Text). Das schadet nicht, kann aber verwirren. Es fehlt außerdem ein Hinweis: Ein Pflichtpunkt MEHRFACH mit leeren `Auswahlwerte` lässt sich nie ausfüllen, die Kategorie bleibt dann gesperrt (wie bei AUSWAHL im Bestand).

**Vorschlag:** Den Satz kürzen und in 5.2 ergänzen: „MEHRFACH nur mit mindestens einem Auswahlwert“.

### P5-11 · Paket 5 · niedrig · Testbogen (Lücken)
**Szenario (belegt, die Tests fehlen):** Die Kurzfassung verspricht „Bedingungen (Paket 4) können auf einen Wert der Mehrfachauswahl zeigen“, getestet wird das nicht. Ebenfalls ohne Test sind: freiwilliger DATUMZEIT-Punkt nur mit Datum (soll „(Uhrzeit)“ melden und das Speichern sperren), Zurück ohne Änderung (P5-5), Verwerfen und wieder öffnen (P5-6), der Ablauf in der Nur-Ansicht bei mehreren gewählten Werten (P5-8).

**Vorschlag:** Testbogen als Zeitachse ergänzen. Zum Beispiel Punkt B mit BedingungPunkt = Mängelarten, BedingungWert = „leck“ (Schreibweise egal): erscheint bei Riss + Leck, verschwindet, wenn nur Riss gewählt ist.

### P6-1 · Paket 6 · mittel · `lblKaFrage.Width`
**Szenario (geschlussfolgert, Maße belegt):** `lblKaFrage` hat eine feste Höhe von 32 bei Size 17 (Export). Mehrzeilige Fragen werden also schon heute abgeschnitten, nicht vergrößert. Paket 6 nimmt bei Punkten mit Bild 160 px Breite weg (Karte 720 → Label 520 statt 680 px). Bei Segoe UI Semibold 17 pt (≈ 22,7 px, ≈ 11–12 px je Zeichen) passen etwa 44 statt 57 Zeichen, mit „  *“ für Pflicht noch weniger. Typische Fragen („Thermometer im Kühlraum zeigt korrekte Temperatur an?“) verlieren das Ende, und das bei genau den Punkten, die eine Erklärung brauchen. T6.1 prüft nur „läuft nicht darunter“.

**Vorschlag:** Knopf schmaler machen (Symbol „🖼“, 48 × 34, `X = Parent.Width - 68`, Label-Abzug 64 statt 160) oder „Beispielbild“ in die Zeile von `lblKaHinweis` setzen. Dort müsste dann die Breite des Hinweises verringert werden, die Kartenhöhe bleibt gleich. In T6.1 den längsten echten Fragetext mit Bild prüfen. Kleinigkeit im selben Zug: `lblKaBildTitel` (Height 56, Size 18) zeigt höchstens 2 Zeilen, längere Titel werden abgeschnitten.

### P6-2 · Paket 6 · niedrig · Test T6.4
**Szenario (belegt aus dem Paket):** Ist das Fenster offen, liegt `btnKaBildSperre` über dem ganzen Bildschirm, auch über `btnKaZurueck`. „Fenster offen lassen, Bildschirm wechseln (Zurück)“ ist also nicht ausführbar. Der Test misst nichts oder verwirrt den Tester.

**Vorschlag:** T6.4 streichen oder anders formulieren („Fenster offen, Vorschau mit Esc schließen, Vorschau neu starten, Kategorie öffnen → Fenster zu“). `Set(varBildID; 0)` in `OnVisible` bleibt trotzdem sinnvoll.

### P6-3 · Paket 6 · niedrig · Schritt 6.3 / `imgKaBild.Image`
**Szenario (geschlussfolgert, UNSICHER):** Der Vorab-Test und alle T6-Tests laufen in Studio im Browser. Auf dem Tablet läuft die App in der Power-Apps-App. Ob die SharePoint-Vorschaubilder (`Thumbnail.Large`, angemeldete URL) dort genauso ankommen, prüft niemand. Dazu erzeugt SharePoint Vorschaubilder erst mit Verzögerung: Wer direkt nach dem Hochladen testet, sieht eventuell nichts und bricht unnötig ab.

**Vorschlag:** In 6.3: „Nach dem Hochladen 2–3 Minuten warten.“ Nach dem Veröffentlichen T6.2 einmal auf dem Tablet wiederholen.

### P6-4 · Paket 6 · niedrig · `imgKaBild.Image` (Rückmeldung)
**Szenario (belegt T6.7, geschlussfolgert bei Netzfehler):** Bei einer falschen Id, einer gelöschten Datei oder einem Netzfehler öffnet sich das Fenster mit leerer Fläche, ohne Hinweis. Der Prüfer weiß nicht, ob noch geladen wird.

**Vorschlag:** Die Abfrage in `btnKaBild.OnSelect` verlegen: `Set(varBildUrl; LookUp(RG_Hinweisbilder; ID = ThisItem.BildID).Thumbnail.Large)`, weiter nur beim Öffnen. Dann `imgKaBild.Image = varBildUrl` und ein Label „Bild nicht gefunden“ mit `Visible = IsBlank(varBildUrl)`. Optional, keine Pflicht.

### P6-5 · Paket 6 · niedrig · `scrKategorie.OnVisible`, Zweig Nur-Ansicht (`BildID: Coalesce(pp.HinweisBildID; 0)`)
**Szenario (belegt):** Die Nur-Ansicht zeigt sonst genau das Gespeicherte (Kommentar im Export: „unabhängig von späteren Stammdaten-Änderungen“). Das Bild kommt dagegen aus den **heutigen** Stammdaten: Ein später geändertes Bild erscheint bei alten Rundgängen, und bei inzwischen deaktivierten Punkten fehlt der Knopf (`pp` leer → 0). Fachlich vertretbar, weil es eine Hilfe ist und kein Prüfergebnis.

**Vorschlag:** Im Paket als bewusste Ausnahme dokumentieren und T6.6 entsprechend formulieren.

---

## Geprüft ohne Befund

1. **Vorher-Fassungen (maschinell, belegt):** Die Vorher-Fassung von `App.Formulas` in P5 ist zeichengleich mit `App.Formulas` nach P4. Die Vorher-Fassung von `scrKategorie.OnVisible` in P6 ist zeichengleich mit dem Stand nach P4 (P5 ändert `OnVisible` nicht). `lblKaFrage.Width` vorher = Export (`Parent.Width - 40`), keines der Pakete 1–5 ändert sie. Auch die ganze Kette P1→P4 passt.
2. **Rückübersetzung / nur beschriebene Änderungen (Diff, belegt):** P5 `App.Formulas`: nur die Pflichtzeile um MEHRFACH/DATUM/DATUMZEIT erweitert, der Zweig „Uhrzeit“ und `fnDatumText` neu. P6 `OnVisible`: nur `Set(varBildID; 0)` und das Feld `BildID` in allen drei Zweigen (gleicher Typ Zahl, Schema der Sammlung einheitlich). P6 `lblKaFrage.Width`: nur der Abzug.
3. **Syntax:** Klammern in allen neuen deutschen Blöcken und allen YAML-Formeln ausgeglichen. Deutsche Blöcke ohne Komma-Trenner, YAML-Blöcke englisch (`;` nur als Verkettung in `OnChange`/`OnSelect`). Keine Kommentare in Verhaltensformeln.
4. **YAML:** Alle 5 Blöcke parsen. Alle Werte sind Formeln mit `=`. Werte mit „: “ oder „{“ stehen im Blockstil (`AccessibleLabel`, `Items`, `OnChange`, `OnSelect`). Classic/Button ohne `AccessibleLabel`. Versionen wie vorgegeben (DatePicker@2.6.0, DropDown@2.3.1, Button@2.2.0, GroupContainer@1.5.0 mit `Variant: ManualLayout`, Label@2.5.1, Image@2.2.3). Alle verwendeten Properties gibt es bei diesen Steuerelementen. Die Properties des Kombinationsfelds (Items, DisplayFields, SearchFields, SelectMultiple, IsSearchable, DefaultSelectedItems, OnChange, InputTextPlaceholder, AccessibleLabel, Chevron*, Selection*) gibt es beim klassischen Kombinationsfeld.
5. **Namen/Felder/Typen:** `colAntworten`-Felder (Typ, WertText, Auswahl, Hinweis, Frage, PruefpunktID, BildID) existieren nach P4/P6. `varNurLesen`, `varGeaendert`, Farbkonstanten vorhanden. `fnDatumText(Date; Text; Text; Boolean)`: 4 Argumente bei allen drei Aufrufen, `SelectedDate` ist Date, Blank wird über `IsBlank(d)` abgefangen. `fnFehltGrund` mit unveränderter Signatur (12 Argumente), alle Aufrufer aus P1–P4 passen weiter. `Eingabetyp`, `Auswahlwerte` in `RG_Pruefpunkte` (SPALTEN.md). `HinweisBildID` wird in 6.2 angelegt und in 6.3 vor 6.4 aktualisiert.
6. **Speicherform und Rücklesen:** „TT.MM.JJJJ hh:mm“ hat 16 Zeichen. `Mid(…; 12; 2)` = Stunde, `Mid(…; 15; 2)` = Minute, `Left(…; 10)` + `DateValue(…; "de-DE")` = Datum. `Text(s.Value; "00")` passt zu `Default`. `Sequence(24; 0)`/`Sequence(60; 0)` = 0–23/0–59. „erst Uhrzeit, dann Datum“ ergibt den vollständigen Text (der Zustand der Listen bleibt erhalten, solange die Zeile nicht neu aufgebaut wird, siehe P5-3). Mehrfach: Trennzeichen „; “ beim Speichern, `Split(…; ";")` + `Trim` beim Lesen.
7. **Nur-Ansicht:** `Auswahl = WertText` (Export) → Items des Kombinationsfelds = gespeicherte Werte, DefaultSelectedItems passt. `DisplayMode.View` bei allen vier neuen Steuerelementen. Der Zweig „Uhrzeit“ ohne Pflicht hat in der Nur-Ansicht keine Wirkung (`lblKaStand` zeigt „Nur Ansicht“).
8. **Protokoll/Mängel:** `htmProtokoll` gibt `WertText` mit `fnHtml` aus, Mängel entstehen nur bei `Bewertung = "NIO"` (scrRundgang, belegt) → neue Typen erzeugen keine Mängel, wie beschrieben. Das JSON enthält `WertText` (P4-ShowColumns).
9. **Bedingungen (P4):** `fnBedGueltig` kennt MEHRFACH schon. `fnBedPasst` teilt `wt` an „;“ und normalisiert (Leerzeichen/Groß-Klein) → „Riss; Leck“ erfüllt „leck“. DATUM/DATUMZEIT nur mit „*“ gültig, sonst sicherer Ausfall (immer sichtbar). Ausgeblendete Punkte werden beim Speichern geleert → `Default` der neuen Steuerelemente wird wieder leer. Der Grund „(Uhrzeit)“ ist in `lblKaFehlend.Text` (P4) schon vorhanden.
10. **Zeitzone:** Gespeichert wird Text in Ortszeit ohne UTC-Umrechnung. DatePicker (`DateTimeZone` Standard Local) und `DateValue` lokal → keine Verschiebung, auch nicht am 25.10. (Zeitumstellung).
11. **Layout P5 (Karte 720 breit):** Datum 20–260, Stunde 272–376, Minute 388–492. Kombinationsfeld 20–480 (`Min(460; …)`). Alles in Zeile 1 (Y 54/78, Höhe 56), passt in `conKaKarte.Height` (P1). `btnKaFoto`/`txtKaKommentar` liegen in Zeile 2, keine Überlappung. Die Sichtbarkeit schließt sich je Typ gegenseitig aus.
12. **Layout P6:** `btnKaBild` Y 10–44 endet vor `lblKaHinweis` (Y 46). Waagerecht beginnt er bei Parent.Width − 164, das Label endet bei Parent.Width − 180 (16 px Abstand). Fenster: Titel 12–68, Bild 76 bis H − 96, Knopf H − 76 bis H − 20. Keine Überlappung, Kartenhöhe unverändert.
13. **P6-Logik:** Bild nur bei offenem Fenster (`If(varBildID > 0; …)` + `Visible`), eine Abfrage mit `ID =` (delegierbar). `varBildFrage` wird vor `varBildID` gesetzt. Vollflächige Sperre `btnKaBildSperre` wie bei `conKaFoto`. Zurücksetzen in `OnVisible`. Ebenen: `conKaBild` vor `conKaFoto`/`conKaLaden` (die Fenster schließen sich gegenseitig aus, das Laden setzt `varBildID` zuerst auf 0). `varBildID` ist nicht in OnStart: Blank > 0 = false, unkritisch.
14. **Einfügen:** Y/Height der YAML-Steuerelemente: Die Prüfung von Y ist in 5.4 verlangt (E-05). Die Höhen sind feste Zahlen, `btnKaBild` hat nur feste Y/Height. Das Kombinationsfeld kommt ohne YAML (keine Falle durch Einfrieren). Rückwege: Reihenfolge Steuerelemente → Formeln ist genannt. Das JSON mit neuen Typen stört die alte Fassung nicht (Werte bleiben beim Speichern erhalten).
15. **Szenarien ohne neuen Mangel:** neuer Punkt ohne Daten (leer, als offen gezählt), alter gespeicherter Punkt (Rücklesen, siehe 6), inaktiver Punkt (wird mitgeführt, ausgeblendet), Netzfehler/Abbruch im Speichern/zwei Prüfer gleichzeitig: P5/P6 ändern die Speicherlogik nicht, Werte bleiben in `colAntworten`, `GespeichertAm`-Prüfung unverändert. Doppelklick auf „Beispielbild“: setzt nur Variablen, harmlos.

## Anzahl je Schwere

| Schwere | Paket 5 | Paket 6 | Summe |
|---|---|---|---|
| hoch | 0 | 0 | **0** |
| mittel | 1 (P5-1) | 1 (P6-1) | **2** |
| niedrig | 10 (P5-2 … P5-11) | 4 (P6-2 … P6-5) | **14** |
