# Prüfung Paket 5 (Typen) und Paket 6 (Beispielbild)

Prüfer: unabhängiger Prüf-Agent, 27.10.2026. Ich habe nur gelesen. Grundlage: `export/*.pa.yaml`, `export/SPALTEN.md` und die Pakete 1–6.
Den Stand vor Paket 5 habe ich maschinell aufgebaut: Export plus jeweils der letzte „neu“-Block aus Paket 1–4 je Property. Für Paket 6 kommt Paket 5 dazu.

## Kurzfassung

- **Kein hoher Befund.** Die Formeln sind syntaktisch sauber, die Vorher-Fassungen stimmen zeichengleich und die Logik trägt.
- **1 mittlerer Befund:** In Paket 6, Schritt 6.6, fehlt die E-05-Prüfung für die Height-/Y-Formeln von `conKaBild` und seinen Kindern.
- **6 niedrige Befunde:** Rückweg und Einfügetexte nennen falsche Anzahlen, Testdaten und Aufräumen fehlen, Teilauswahlen Stunde/Minute werden nicht gespeichert, der Testbogen hat Lücken, ein Titel wird abgeschnitten.

## Was maschinell geprüft ist (ohne Befund)

| Punkt | Ergebnis |
|---|---|
| Vorher `App.Formulas` (P5) | zeichengleich mit P4-neu ✔ |
| Vorher `scrKategorie.OnVisible` (P6) | zeichengleich mit P4-neu ✔ (P5 ändert OnVisible nicht) |
| Vorher `lblKaFrage.Width` (P6) | zeichengleich mit dem Export (`Parent.Width - 40`) ✔ |
| Nur Beschriebenes geändert, P5 `App.Formulas` | Diff: `fnFehltGrund` Zeile „Wert“ um MEHRFACH/DATUM/DATUMZEIT erweitert, neue Zeile „Uhrzeit“, neu `fnDatumText`. Sonst nichts ✔ |
| Nur Beschriebenes geändert, P6 `OnVisible` | Diff: `Set(varBildID; 0)` und `BildID` in allen **drei** Zweigen (Nur-Ansicht `pp.HinweisBildID`, Bearbeiten `p.HinweisBildID`, Inaktiv `0`) → das Schema von `colAntworten` bleibt einheitlich ✔. `varSprungRec` wird nur aus `colAntworten` gesetzt, es gibt keinen zweiten Record-Typ ✔ |
| Klammern | alle Blöcke ausgeglichen ✔ |
| YAML | alle 6 Blöcke mit PyYAML gültig. Blockstil bei „: “ und „{“ eingehalten (`AccessibleLabel`, `Items`, `OnChange`, `OnSelect`). Englische Trennzeichen (`,`, Kette `;`) ✔. Classic/Button ohne `AccessibleLabel` ✔ |
| Control-Versionen | DatePicker@2.6.0, DropDown@2.3.1, Button@2.2.0, GroupContainer@1.5.0 ManualLayout, Label@2.5.1, Image@2.2.3 ✔ |
| Properties | DatePicker: `IconBackground`, `IconFill`, `InputTextPlaceholder`, `StartOfWeek`, `DefaultDate` vorhanden. Dropdown: dieselben Properties wie das bestehende `ddKaAuswahl`. Klassisches Kombinationsfeld: `Items`, `DisplayFields`, `SearchFields`, `SelectMultiple`, `IsSearchable`, `DefaultSelectedItems`, `InputTextPlaceholder`, `Chevron*`, `Selection*` vorhanden ✔ |
| Kommentare in Verhaltensformeln | keine ✔ |
| `Reset()` derselben Galeriezeile | `btnKaDatumLeeren` setzt `dpKaDatum`, `ddKaStunde` und `ddKaMinute` aus derselben Vorlage zurück. Das ist zulässig (nur von außerhalb der Galerie nicht). Reihenfolge: zuerst Patch, dann Datum, dann die Listen. Feuert dabei `OnChange`, schreibt es nur `""` ✔ |
| Positionen im Text | „27.10.2026 07:05“: `Left(…;10)`, `Mid(…;12;2)`, `Mid(…;15;2)` treffen ✔. `Sequence(24;0)`/`Sequence(60;0)` = 00–23/00–59 ✔ |
| Datum/Gebietsschema | Schreiben: `Text(d; "dd.mm.yyyy")`. Lesen: `DateValue(…; "de-DE")` in `IfError`. Unabhängig von der Gerätesprache ✔ |
| MEHRFACH | gespeichert in der Reihenfolge der Auswahlwerte (`Filter` über `Split(Auswahl)`), Trennzeichen „; “. Rücklesen über `DefaultSelectedItems` mit demselben Schema `{Value}`. Nur-Ansicht: `Auswahl` = `WertText` (P1–P4) → `Items` = gespeicherte Werte ✔ |
| Bedingung auf MEHRFACH | `fnBedGueltig` kennt MEHRFACH schon (P4). `fnBedPasst` teilt `wt` an „;“, `fnBedNorm` trimmt → „ Leck“ passt auf „Leck“ ✔ |
| Pflicht/Uhrzeit | `lblKaFehlend` (P4) kennt „Uhrzeit“ → „(Uhrzeit)“. `BorderColor`, Sprung und Zähler laufen über `fnFehlt` ✔ |
| Protokoll/Mängel | Mängel entstehen nur aus `Bewertung = "NIO"` (`scrRundgang`, Export). Das Protokoll zeigt `WertText`. Die neuen Typen erzeugen keine Mängel ✔ |
| Layout Karte (720) | DATUMZEIT: Datum 20–260, Stunde 272–376, Minute 388–492, ✕ 504–560. DATUM: ✕ 272–328. Kombinationsfeld 20–480. Alles in der Eingabezeile (Y 54/78, Höhe 56). Die Zeile darunter (+68) ist für Kommentar/Foto → keine Überlappung. Die Kartenhöhe aus P1 passt ✔ |
| Layout Knopf „Bild“ | X 636–700, Y 10–44. Die Frage endet bei 620 (16 px Abstand). `lblKaHinweis` beginnt bei Y 46 ✔ |
| Abfrage Bild | `Image` = `If(varBildID > 0; LookUp(…))` → keine Abfrage bei geschlossenem Fenster, auch nicht bei unsichtbarem Container. `ID =` ist delegierbar ✔ |
| Reihenfolge P6 | OnVisible (`BildID`, `varBildID`) → `lblKaFrage.Width` → `btnKaBild` (setzt `varBildFrage`) → `conKaBild` liest beide ✔ |
| Szenarien P6 | Nur-Ansicht: Bild aus den heutigen Stammdaten (dokumentiert). Inaktiver/gelöschter Punkt: 0, kein Knopf. Bild-ID gibt es nicht: leere Fläche (T6.6). Speichern/zwei Prüfer/Netzfehler: unberührt ✔ |

## Befunde

### B1 – Paket 6 · mittel · Schritt 6.6 „Prüfen nach dem Schritt“ (`conKaBild`)
**Stelle:** Der YAML-Block `conKaBild` enthält sechs Height-/Y-Formeln:
- `conKaBild.Height = Parent.Height`
- `btnKaBildSperre.Height = Parent.Height`
- `conKaBildKarte.Height = Min(Parent.Height - 32; 900)`
- `conKaBildKarte.Y = (Parent.Height - Self.Height) / 2`
- `imgKaBild.Height = Parent.Height - 76 - 96`
- `btnKaBildSchliessen.Y = Parent.Height - 76`

Die Prüfliste fragt nur, ob die Kinder im Container geblieben sind. Paket 5 (Schritt 5.4) und Paket 1 prüfen nach E-05 ausdrücklich, ob Y/Height Formeln bleiben. Hier fehlt das.

**Szenario:** Studio friert beim YAML-Einfügen die Höhen auf die Studio-Bildschirmgröße ein (E-05). Danach gibt es zwei mögliche Fehlbilder:
- Auf dem Tablet ist der Bildschirm höher als in Studio, oder er wird gedreht. Dann deckt `btnKaBildSperre` nicht mehr alles ab. Bei offenem Fenster lassen sich darunter andere Karten antippen, zum Beispiel „Bild“ eines anderen Punkts oder Eingaben. T6.2 („Rest nicht tippbar“) prüft das nur in Studio.
- Der Bildschirm ist kleiner. Dann liegen „Schließen“ oder der untere Bildrand außerhalb.

Folgenlos ist das Einfrieren nur, wenn „An Bildschirm anpassen“ eine feste Höhe erzwingt. Das ist aus dem Export nicht belegt.

**Vorschlag:** Die sechs Formeln in die Prüfliste von 6.6 aufnehmen, Muster: „steht als Formel da, nicht als Zahl (E-05) – sonst per Formelleiste setzen“. Dazu ein Test T6.8: am Tablet hochkant und quer öffnen, unten links tippen → nichts passiert.
**Belegt:** Prüfliste und Formeln stehen im Paket. **Geschlussfolgert:** die Auswirkung (E-05 laut Auftrag).

### B2 – Paket 5 · niedrig · Rückweg
**Stelle:** „die **vier** neuen Steuerelemente löschen“. Es sind **fünf**: `dpKaDatum`, `ddKaStunde`, `ddKaMinute`, `btnKaDatumLeeren`, `cboKaMehrfach`.
**Szenario:** Josias löscht die vier YAML-Steuerelemente aus 5.4. `cboKaMehrfach` bleibt in jeder Karte stehen. Ein Fehler entsteht nicht, weil es `fnDatumText` nicht nutzt. Der Rückweg ist aber nicht vollständig, und ein MEHRFACH-Punkt bleibt bearbeitbar, obwohl die alte `fnFehltGrund` ihn nicht kennt.
**Vorschlag:** Alle fünf mit Namen nennen und zuerst löschen, dann `App.Formulas` einfügen.
**Belegt.**

### B3 – Paket 5 · niedrig · Schritt 5.4, Einfügetext
**Stelle:** „**Drei** Blöcke nacheinander oder zusammen“. Es folgen **vier** YAML-Blöcke.
**Szenario:** Josias fügt nur drei ein. Der vierte fehlt, in der Regel der ✕-Knopf, weil er zuletzt steht. Die Prüfliste darunter („Alle vier liegen in `conKaKarte`“) fängt das auf, der Text widerspricht sich aber.
Beim Einfügen „nacheinander“ verweisen `dpKaDatum.OnChange` und `ddKaStunde.OnChange` auf noch nicht vorhandene Steuerelemente (`ddKaStunde`, `ddKaMinute`). Bis alle da sind, stehen rote Fehler, ohne Hinweis.
**Vorschlag:** „Vier Blöcke, am besten zusammen (alle vier Blöcke hintereinander kopieren, ein Strg+V). Bis alle vier drin sind, können rote Fehler stehen.“
**Belegt.**

### B4 – Paket 5 · niedrig · Schritt 5.2 Testdaten / Testbogen ohne Aufräumen
**Stelle:** Die Testpunkte M, D, DZ und F werden nur mit „Pflicht = Ja“ beschrieben. Es fehlen:
- **Aktiv = Ja**: `colPP` filtert `Aktiv = true`. Paket 3 und 4 nennen das ausdrücklich.
- **Foto = Aus**: Paket 1 kennt Foto „Pflicht“.
- **RgReihenfolge** hinter den vorhandenen Punkten.

Außerdem fehlt ein Aufräumschritt. Paket 3 hatte „Z1–Z3 auf Aktiv = Nein setzen (sonst bleiben sie Pflichtpunkte in K1)“.
**Szenario:**
- Bei Aktiv = Nein (falls das der Standardwert der Spalte ist) erscheint in T5.1 nichts.
- Ohne Aufräumen bleiben M, D und DZ Pflichtpunkte in K1. Jede spätere DEV-Durchführung (Paket 6 und weitere) muss sie ausfüllen, sonst lässt sich K1 nicht speichern.

**Vorschlag:** In 5.2 „Aktiv = Ja, Foto = Aus, RgReihenfolge hinter den vorhandenen, F direkt hinter M“ ergänzen. Unter den Test schreiben: „Aufräumen: M, D, DZ, F auf Aktiv = Nein, Testdaten in den Papierkorb.“
**Belegt:** Text. **Geschlussfolgert:** die Folgen.

### B5 – Paket 5 · niedrig · `ddKaStunde`/`ddKaMinute`: Teilauswahl wird nicht gespeichert, Restwerte möglich
**Stelle:** `fnDatumText` schreibt die Uhrzeit nur, wenn **beide** Werte gewählt sind. Eine einzeln gewählte Stunde oder Minute steht nur im Steuerelement, nicht in `colAntworten`. `Default` liest nur aus `WertText`.
**Szenarien:**
1. DZ mit „… 07:05“. Wer die Stunde leert (AllowEmptySelection), bekommt `WertText` = nur Datum. Damit springt `ddKaMinute.Default` von „05“ auf „“, und das klassische Dropdown setzt die Minute zurück. Die Minute muss neu gewählt werden. Datenverlust gibt es nicht, weil „(Uhrzeit)“ offen bleibt.
2. **UNSICHER**, abhängig davon, ob die Galerie den Zustand der Steuerelemente je Zeile behält. `galKaPruefpunkte` ist dieselbe Galerie für **alle** Kategorien.
   - Ablauf: In K1 hat DZ ein Datum und Stunde 07, aber keine Minute. Dann „Zurück → Verwerfen“, danach eine Kategorie, deren Punkt an derselben Zeilenposition ebenfalls DATUMZEIT ohne Wert ist.
   - `Default` bleibt „“ → „“ und löst daher kein Zurücksetzen aus. „07“ kann stehen bleiben (vorerst gesperrt).
   - Wählt der Prüfer dann Datum und nur die Minute, speichert `OnChange` „… 07:mm“, eine Stunde, die er hier nie gewählt hat.
   - Dasselbe kann passieren, wenn eine bedingte Frage (P4) über DZ ein- oder ausgeblendet wird und die Zeilen verrutschen.

**Vorschlag:**
- Mindestens ein Test: „DZ: Datum + nur Stunde, Zurück (Verwerfen), K1 erneut öffnen → Stunde leer“, dasselbe mit einer bedingten Frage über DZ. Fällt er durch:
- `Std`/`Min` als eigene Felder in `colAntworten` führen, nicht ins JSON. `OnChange` der Listen schreibt sie, `Default` liest sie.
- Einfacher, aber gröber: Ist das Datum leer, setzt `dpKaDatum.OnChange` die Listen per `Reset` zurück.

**Geschlussfolgert.** Der Mechanismus ist aus den Formeln belegt, das Galerieverhalten ist UNSICHER.

### B6 – Paket 5 · niedrig · Testbogen: Lücken bei neuen Wegen
**Stelle:** Testtabelle T5.1–T5.12. Ungetestet bleiben:
- „✕“ bei **DZ**: andere X-Position (504). Nach dem Zurücksetzen müssen beide Listen leer **und wieder gesperrt** sein.
- MEHRFACH: alle Werte wieder abwählen → M wieder offen, F verschwindet (Bedingung fällt weg).
- DZ: eine Uhrzeit-Komponente leeren → „(Uhrzeit)“ (siehe B5).
- Nur-Ansicht von DZ: die Listen zeigen „07“/„05“ in der Ansicht. T5.12 prüft nur das Protokoll und allgemein „Nur-Ansicht zeigt die Werte“.

**Szenario:** Gerade die Wege, die Paket 4 (Bedingung) und Paket 5 verbinden, bleiben ungeprüft. Ein Fehler in `btnKaDatumLeeren.X` oder beim Zurücksetzen der Listen fällt erst im Betrieb auf.
**Vorschlag:** Nach T5.8 drei Zeilen einfügen:
- T5.8a: „DZ ✕ → Datum, Stunde, Minute leer, Listen gesperrt, DZ offen; dann wieder 07:05“.
- T5.8b: „M alle abwählen → M offen, F weg; dann Riss, Leck, Korrosion wieder wählen“.
- T5.8c: „DZ Stunde leeren → (Uhrzeit); wieder 07“.

Die Zeitachse bleibt dabei erhalten.
**Belegt:** Test fehlt.

### B7 – Paket 6 · niedrig · `lblKaBildTitel` abgeschnitten
**Stelle:** `Height 56`, `Size 18`, Breite 680 (Karte 720 − 40), Text „Beispiel – “ & Frage.
**Schätzung:** 18 pt ≈ 24 px Schrift, ≈ 29 px Zeilenhöhe. Bei Label-Innenabstand 5 + 5 bleiben 46 px, also eine Zeile. Bei ≈ 12 px je Zeichen passen ≈ 55 Zeichen in eine Zeile. Fragen mit mehr als ≈ 45 Zeichen umbrechen, die zweite Zeile wird abgeschnitten.
**Szenario:** Bei einer langen Frage ist im Bildfenster genau der Teil abgeschnitten, der sagt, wozu das Bild gehört. Das ist der Zweck des Titels. In der Karte ist die Frage wegen des Knopfs jetzt ohnehin 80 px kürzer.
**Vorschlag:** `Size 16` und `Height 64`. Bild auf `Y 84` und `Height Parent.Height - 84 - 96` setzen. Oder den Titel zweizeilig auslegen (`Height 72`) und das Bild entsprechend verschieben.
**Geschlussfolgert:** Schätzung der Textbreite je Zeichen.

## Hinweise (kein Befund: dokumentiert, Entscheidung oder sehr gering)

- H1 (P5, T5.10, als UNSICHER dokumentiert): Feuert `OnChange` beim Laden oder beim Wechsel der Kategorie, liest `dpKaDatum.OnChange` die Listen. Sind deren `Default`-Werte noch nicht nachgezogen, könnte „… 07:05“ als nur Datum zurückgeschrieben werden. T5.10 erkennt das, weil dort „TT.MM.JJJJ 07:05“ erwartet wird. Empfehlung: Bei einem Fund in T5.10 zusätzlich den gespeicherten Text in SharePoint (`Antworten`) ansehen.
- H2 (P5, Entscheidung): Bei DATUMZEIT ohne Pflicht blockiert „nur Datum“ das Speichern (dokumentiert: „immer offen“). Leeren geht über ✕.
- H3 (P5): Ein MEHRFACH-Wert, der nicht mehr in den Auswahlwerten steht (umbenannt), wird beim nächsten Antippen des Feldes still entfernt (`Filter` über `Auswahl`). Das passt zur Pflegeregel und verhält sich wie AUSWAHL.
- H4 (P5): Das Einfrieren nach E-05 betrifft laut Auftrag Y/Height. `btnKaDatumLeeren.X` ist ebenfalls eine Formel (504/272). Vorsichtshalber in der Prüfliste 5.4 mitprüfen.
- H5 (P5/P6, wie E-07): `btnKaDatumLeeren` („✕“) und `btnKaBild` („Bild“) haben keine sprechende Beschriftung für Screenreader (Classic/Button ohne `AccessibleLabel` nach Regel). Das meldet die Barrierefreiheitsprüfung, nicht „Formeln“.
- H6 (P6): `btnKaBild` ist 34 px hoch. Für Tablet-Bedienung, etwa mit Handschuhen, sind ≥ 44 px üblich. Mehr Höhe ginge nur auf Kosten von `lblKaHinweis` (Y 46), deshalb nur ein Hinweis.
- H7 (P6, Entscheidung): Fenster statt Aufklappen ist als „Bitte bestätigen“ markiert. Das Vorschaubild `Thumbnail.Large` ist durch den Vorab-Test 6.3 und T6.7 abgedeckt.
- H8 (P5, Leistung): Jede Karte rechnet jetzt `ForAll(Sequence(24/60))` für die Listen, auch wenn sie unsichtbar sind. Das kostet keine Abfragen und ist bei üblichen Kategoriegrößen unkritisch.

## Anzahl je Schwere

- hoch: 0
- mittel: 1 (B1)
- niedrig: 6 (B2–B7)
- Hinweise: 8
