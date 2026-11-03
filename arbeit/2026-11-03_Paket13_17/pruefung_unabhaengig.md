# Unabhängige Prüfung Paket 17 (Archiv) und Paket 13 (Anleitungen)

Stand 03.11.2026, Prüfer-Agent. Nur gelesen, nichts geändert außer dieser Datei.

**Geprüfter Stand:** `pakete/PAKET_17_ARCHIV.md` und `pakete/PAKET_13_ANLEITUNGEN.md` vom 03.11. 08:16:43. `werkzeuge/baukasten.py` wurde **während** der Prüfung geändert (08:15:36, Paket 14 Vorwert über `TagText`/`colLetzteKand`), die Dokumente wurden danach neu erzeugt. Alle Abgleiche unten beziehen sich auf diesen Endstand.

Grundlagen: Generator-Kette im Speicher (`baukasten.Stand(rg.App('2026-10-27_0909'))`, alle `PAKETE`, `pruefe` + `pruefe_texte` → 0 Fehler, ohne Dateien zu schreiben), echter Studio-Stand `arbeit/_entpackt/2026-11-02_1541/msapp/Src` (Export 02.11.), `Properties.json` der Rundgang-App (768 × 1366 hochkant, `DefaultConnectedDataSourceMaxGetRowsCount` = **2000**, `supportcolumnnamesasidentifiers`, `powerfxv1 = false`), Builder `arbeit/2026-11-02_Paket8/builder_nach_p14_15.json` → `arbeit/2026-10-30_Builder/bloecke.json`, Builder-Export (1366 × 768).

Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

---

## Paket 17 – Archiv

### A17-1 · mittel · „Ansehen → Protokoll“ schreibt bei alten Läufen ohne PDF
- **Stelle:** Ablauf `btnArOeffnen` → `scrRundgang` → `btnRuProtokoll` → `scrProtokoll.OnVisible` (`Set(varArchivStart, varDurch.Status = stAbgeschlossen && IsBlank(varDurch.ProtokollUrl))`) → `tmrPrArchiv` → `Select(btnPrArchivieren)` (belegt).
- **Ablauf:** Prüfer öffnet im Archiv einen abgeschlossenen Lauf, der (noch) kein PDF hat (z. B. Läufe aus der Zeit vor dem Archiv-Flow, oder Flow damals fehlgeschlagen), tippt „Protokoll“. Die App startet automatisch den Flow `RG_Protokoll_archivieren` und patcht `ProtokollUrl`/`ProtokollErstelltAm` in `RG_Durchfuehrungen` – mit dem heutigen Protokoll-Layout und dem Konto des Betrachters.
- **Folge:** Die Kurzfassung „Daten: nur lesen“ stimmt nicht. Je nach Bestand entstehen beim Stöbern viele PDFs nachträglich; ohne Schreibrecht kommt eine Fehlermeldung. Kein Datenverlust.
- **Vorschlag:** Entscheidung festhalten. Entweder (a) gewollt: in Kurzfassung und Test aufnehmen („Ansehen eines Laufs ohne PDF erzeugt das PDF“), oder (b) im Archiv nicht automatisch: `scrProtokoll.OnVisible` letzte Zeile `Set(varArchivStart, !varAusArchiv && varDurch.Status = stAbgeschlossen && IsBlank(varDurch.ProtokollUrl))` (manuell über „Archivieren“ bleibt möglich). (b) wäre eine vierte Property.

### A17-2 · niedrig · Grenze 500 passt nicht zur App-Einstellung 2000
- **Stelle:** `btnArSuchen.OnSelect` (`If(CountRows(colArchiv) >= 500, Notify("… höchstens 500 angezeigt …"))`), Kurzfassung „Höchstens 500 je Suche“.
- **Belegt:** `Properties.json` → `DefaultConnectedDataSourceMaxGetRowsCount: 2000`. Ein delegierter `ClearCollect` holt bis 2000 Zeilen.
- **Ablauf:** 3 Monate × mehrere Rundgänge täglich → 500–1999 Läufe: Warnung erscheint, obwohl alle angezeigt werden; ab 2000 wird ohne passende Warnung abgeschnitten (sortiert auf dem Server, also die ältesten fehlen).
- **Vorschlag:** `>= 2000` und Text „höchstens 2000“, oder bewusst `FirstN(Sort(Filter(…)), 500)` – dann stimmt 500. Kurzfassung angleichen.

### A17-3 · niedrig · Zeitraum filtert `StartZeit`, angezeigt wird `TagText`
- **Belegt:** `StartZeit: Now()` beim Anlegen (`btnRgAktion`), `TagText` = gewählter Tag (Nachholen bis `cfgNachholTage`).
- **Ablauf:** Lauf für den 31.10. am 02.11. nachgeholt, Zeitraum „bis 31.10.“ → Lauf fehlt; Zeitraum „ab 01.11.“ → Lauf erscheint mit Datum 31.10.
- **Vorschlag:** So lassen (Text-Vergleich `>=` auf `TagText` ist nicht delegierbar), aber in Kurzfassung/`lblArVon` sagen „begonnen von/bis“ oder Hinweis im Dokument. Kein Code nötig.

### A17-4 · niedrig · Liste wird beim erneuten Öffnen nicht neu geladen
- **Stelle:** `scrArchiv.OnVisible` `If(IsEmpty(colArchiv), Select(btnArSuchen))`.
- **Ablauf:** Archiv öffnen → Start → heute einen Lauf abschließen → wieder Archiv: der neue Lauf fehlt bis „Suchen“.
- **Vorschlag:** `If(IsEmpty(colArchiv) || !varAusArchiv, Select(btnArSuchen))` – von der Startseite (`varAusArchiv` = false) wird neu gesucht, beim „Zurück“ aus `scrRundgang` (true) bleibt die Liste samt Scrollstand.

### A17-5 · niedrig · `lblArInfo` zweite Zeile knapp
- **Stelle:** `lblArInfo` Size 13, zwei Zeilen (`Char(10)`), Height 44, Y 42, Karte 92 hoch.
- **Geschlussfolgert:** 13 pt ≈ 17,3 px, Zeilenhöhe ≈ 20,8 px → 41,6 px + Innenabstand oben 5 = 46,6 px > 44 → Unterlängen der zweiten Zeile werden abgeschnitten.
- **Vorschlag:** `Y: =40`, `Height: =50` (endet bei 90 ≤ 92).

### A17-6 · kosmetisch
- `btnRuZurueck.Text` bleibt „‹  Übersicht“, führt aus dem Archiv aber ins Archiv. Optional `If(varAusArchiv, "‹  Archiv", "‹  Übersicht")`.
- Test T4 „rote Zeile“: rot ist nur die Info-Schrift (`lblArInfo.Color`), nicht die Zeile.
- `btnStartArchiv` liegt nach dem Einfügen über `conStartLaden`/`btnStartLadenSperre` (Einfügen = oberste Ebene). Während des Ladens gesperrt (`DisplayMode`, `If(!varIsLoading…)`), also nur optisch.

### A17-7 · Hinweis · ältere Fassungen im Archiv
Nur-Lesen-Zweig in `scrKategorie.OnVisible` holt Grenzen, Fotomodus, `BildID` und (Paket 13) `AnlID` aus dem **heutigen** Prüfpunkt (`LookUp(colPP, …)`, `colPP` = nur aktive Prüfpunkte der Kategorie). Läufe einer älteren Fassung zeigen daher ohne „Bild“/ⓘ, Werte und Fotos bleiben sichtbar (belegt aus der Formel). Das war schon so, wird durch das Archiv aber häufiger. Nur im Dokument erwähnen.

### Paket 17 – geprüft, ohne Befund
- **Gültigkeit:** `StartZeit >= varArVon` (DateTime-Spalte gegen Date-Variable) ist zulässig und delegierbar (wie `Created >= Today()`), Zeitzone über lokale Mitternacht korrekt. `Sort(…, StartZeit, SortOrder.Descending)` delegierbar. `RundgangID = varArRg` (Zahl) delegierbar. Status/Test/n.i.O. lokal auf `colArchiv` – richtig getrennt.
- `Refresh(RG_Durchfuehrungen)` vor dem Lesen (E-01) vorhanden. `varIsLoading` an Anfang und Ende, Knöpfe gesperrt.
- `colArRg` aus `ShowColumns(RG_Rundgaenge, ID, Title)` (Bezeichner), `Ungroup(Table({T: Table({ID: 0, Title: …})}, {T: colArRg}), T)` – gleiches Muster läuft im Builder (belegt). `ddArRg.Default` „Alle Rundgänge“ ist immer in Items. `Coalesce(ddArRg.Selected.ID, 0)` richtig.
- `Set(varArTest, Coalesce(varArTest, false))` usw.: liefert bei leer `false`, bei `false` bleibt `false` – korrekt.
- `fnTagAnzeige(DateValue(ThisItem.TagText))` passt zur UDF (Date). Spalten `PrueferName`, `AnzahlNIO`, `TestDatensatz`, `ProtokollUrl`, `StartZeit`, `RundgangID`, `TagText`, `Status` existieren (belegt `DataSources`).
- **Ablauf Start → Archiv → Ansehen → Kategorie → zurück → Archiv → Start:** `btnArOeffnen` setzt `varDurchID`, `varWeiter = false` (sonst würde `scrRundgang.OnVisible` nicht laden und `tmrWeiter` liefe), `varAusArchiv = true`. `scrRundgang.OnVisible` lädt `varDurch` frisch. `btnKaZurueck`/`btnPrZurueck` → `scrRundgang` (lädt neu), `btnRuZurueck` → Archiv. `btnArZurueck` und `scrStart.OnVisible` setzen `varAusArchiv` zurück; jeder Weg zur Startseite läuft über `scrStart.OnVisible`. `varTag`, `varTagText`, `varSchluessel` werden in `scrRundgang`/`scrKategorie`/`scrProtokoll` nicht gelesen (belegt) → kein Rest vom Archiv. `varRgID` wird nur in `btnRgAktion` gelesen, das ihn selbst setzt → harmlos.
- **Abschluss/Zurücksetzen bei abgeschlossenen Läufen:** `conRuFuss.Visible` nur bei InArbeit/Abschluss, `btnRuZuruecksetzen.Visible` nur bei Abschluss, `btnRuAbschluss.OnSelect` prüft zusätzlich den Status → aus dem Archiv nicht erreichbar. Offene Läufe öffnet das Archiv nicht (Hinweis). `varNurLesen` in `scrKategorie` greift.
- **Layout 768:** Kopf, Datumsfelder 24–244/260–480, „Suchen“ 496–744, Schalter 3 × 234,7, Karte 720 breit, PDF 524–604, Ansehen 612–712, Name 484 – keine Überlappung. `galArListe` 344 bis Bildschirmende. `btnStartArchiv` 216–256 zwischen `ddStartTag` (bis 204) und Galerie (ab 256), `lblStartListeTitel` auf 536 verkürzt. Textbreiten-Prüfung des Generators ok.
- **YAML:** Beide Blöcke mit PyYAML gelesen, jede Property beginnt mit `=`. `Screens:`-Format wie die eingefügten Builder-Bildschirme, Kinderlisten im selben Stil wie Paket 6 (`conKaBild`, eingefügt, belegt). Steuerelement-Versionen wie im Export. `Variant` bei Containern/Galerie gesetzt. Kein `AccessibleLabel` an Classic/Button. Hinweis E-05 im Dokument.
- **Vollständigkeit:** genau 3 geänderte Properties, Vorher = Export 02.11. (zeichengleich), Nachher = Generator; alle 24 neuen Steuerelemente im Dokument. Reihenfolge Schritt 1 → 2 → 3 erzeugt keinen roten Zwischenstand (`scrArchiv` existiert vor den Verweisen).

---

## Paket 13 – Anleitungen

### A13-1 · mittel · `ddPAnl`: aktueller Wert fehlt in Items (inaktiv, gelöscht, doppelter Titel)
- **Stelle:** Builder `ddPAnl.Items` = nur **aktive** Anleitungen; `ddPAnl.Default` = Titel der zugeordneten Anleitung (auch inaktiv) bzw. „(fehlt)“; `OnChange` mit Wächter `Self.Selected.ID <> AnleitungID`.
- **Ablauf 1:** Anleitung inaktiv stellen (oder in SharePoint löschen) → Prüfpunkt mit dieser Anleitung antippen. Default-Text steht nicht in Items → Classic-Dropdown zeigt das erste Element „— keine —“ (geschlussfolgert), „(fehlt)“ erscheint nie. Die Prüfregel meldet zwar „inaktiv“, das Feld behauptet aber „keine“. Falls das Dropdown bei geändertem Default `OnChange` auslöst (UNSICHER, genau dagegen ist der Wächter in allen Builder-Dropdowns gebaut), greift der Wächter hier nicht (0 ≠ alte ID) → stilles `Patch(… {AnleitungID: 0})` im offenen Entwurf.
- **Ablauf 2:** Zweimal „+ Anleitung“ → zwei „Neue Anleitung“. Die zweite einem Prüfpunkt zuordnen, Prüfpunkt erneut antippen → Default trifft per Titel die erste → falsche Anzeige, gleiches OnChange-Risiko mit der falschen ID.
- **Vorschlag:** wie `ddPBedA`: in Items ein drittes Element für den aktuellen, nicht wählbaren Wert, Titel bei Dubletten eindeutig machen, Default identisch bilden. Skizze (englisch):
  - Items: `Ungroup(Table({T: Table({ID: 0, Title: "— keine —"})}, {T: ForAll(Sort(Filter(RG_Anleitungen, Aktiv = true), Title) As a, {ID: a.ID, Title: a.Title & " (#" & a.ID & ")"})}, {T: Filter(Table({ID: Coalesce(LookUp(colP, ID = varAuswahlID).AnleitungID, 0), Title: Coalesce(LookUp(RG_Anleitungen, ID = LookUp(colP, ID = varAuswahlID).AnleitungID).Title, "(fehlt)") & " (inaktiv) (#" & LookUp(colP, ID = varAuswahlID).AnleitungID & ")"}), Coalesce(LookUp(colP, ID = varAuswahlID).AnleitungID, 0) <> 0 && IsBlank(LookUp(RG_Anleitungen, ID = LookUp(colP, ID = varAuswahlID).AnleitungID && Aktiv = true)))}), T)`
  - Default entsprechend (gleiche Textbildung). „(#ID)“ immer anhängen ist einfacher als nur bei Dubletten; oder nur bei Dubletten wie `ddPBedA`.

### A13-2 · mittel (Entscheidung) · Inaktive Anleitung bleibt beim Prüfer sichtbar
- **Stelle:** App `btnKaInfo.Visible = ThisItem.AnlID > 0`, `OnSelect` `LookUp(RG_Anleitungen, ID = ThisItem.AnlID)` ohne `Aktiv`. Builder `lblAnHilfe`: „Nicht mehr gebraucht: inaktiv stellen.“, Prüfregel „gibt es nicht mehr oder sie ist inaktiv“.
- **Ablauf:** Josias stellt eine veraltete Anleitung inaktiv, erwartet, dass sie verschwindet. In der aktiven Fassung hängt sie weiter an Prüfpunkten → Prüfer sieht ⓘ und den alten Text, bis eine neue Fassung die Zuordnung entfernt.
- **Vorschlag:** festlegen, was „inaktiv“ heißt. (a) Nur „nicht mehr wählbar“: `lblAnHilfe` und Kurzfassung so formulieren („bereits zugeordnete bleiben sichtbar, bis du sie im Prüfpunkt entfernst“). (b) Beim Prüfer ausblenden: in `scrKategorie.OnVisible` einmal `ClearCollect(colAnlAktivApp, ShowColumns(Filter(RG_Anleitungen, Aktiv = true), ID))` und `AnlID: If(IsBlank(LookUp(colAnlAktivApp, ID = …)), 0, …)` in den Zweigen (dann alle drei Zweige gleich halten). (a) ist ohne Code.

### A13-3 · niedrig · Kein `Refresh` vor dem Lesen der Anleitung (E-01)
- **Stelle:** App `btnKaInfo.OnSelect` (`LookUp(RG_Anleitungen, …)`), Builder `tmrArbeit` Stufe „laden“ (`ClearCollect(colAnlAktiv, …)`; die `Refresh`-Liste davor enthält `RG_Anleitungen` nicht).
- **Ablauf:** Tablet läuft den ganzen Tag, Josias korrigiert den Text im Builder → Prüfer sieht im Sitzungs-Cache womöglich den alten Text (UNSICHER, Regel E-01 belegt den Cache). Im Builder sieht man fremde Änderungen an „aktiv“ erst nach Neustart.
- **Vorschlag:** `Refresh(RG_Anleitungen);` als erste Anweisung in `btnKaInfo.OnSelect` und in der `Concurrent(Refresh(…))`-Liste der Stufe „laden“.

### A13-4 · niedrig · Roter Zwischenstand B6.1 vor B6.2 nicht angekündigt
- `galPr.Items` (B6.1) verweist auf `colAnlAktiv`, das erst `tmrArbeit.OnTimerEnd` (B6.2) anlegt → zwischen den Schritten Fehler „Name ungültig“. CLAUDE.md §6 verlangt Ankündigung. **Vorschlag:** B6.2 vor B6.1 oder Satz „rot bis B6.2“.

### A13-5 · niedrig · Diff-Blöcke zeigen die Änderung nicht
- A2.1 (drei Zeilen), B5.1–B5.4, B6.1, B6.2: Die Zeilen werden nach ~200 Zeichen mit „…“ gekürzt, die Änderung steht weiter hinten → „-“ und „+“ sehen gleich aus. **Vorschlag:** im Generator den Ausschnitt um die erste abweichende Stelle zeigen („… FotoModus … AnlID: Coalesce(pp.AnleitungID; 0); Inaktiv: false}“).

### A13-6 · niedrig · Testbogen unvollständig / Test 4 so nicht ausführbar
- Test 4 („inaktiv stellen → Prüfung zeigt Hinweis“): `colAnlAktiv` wird nur in Stufe „laden“ gelesen → erst nach „← Übersicht“ und erneutem Öffnen des Rundgangs. Schritt ausdrücklich nennen.
- Fehlen: (a) App mit inaktiver und mit gelöschter Anleitung (Erwartung je nach A13-2; gelöscht → Meldung „nicht gefunden“), (b) ⓘ im Nur-Lesen (abgeschlossener Lauf, Archiv), (c) ⓘ + „Bild“ in derselben Karte (Lage, Frage gekürzt), (d) Builder: bestehende Prüfpunkte zeigen nach B4.4/B4.5 den richtigen Foto-Wert, (e) „Bearbeiten“ (neue Fassung) und „Holen“ übernehmen die Anleitung, Aktivieren-Liste zeigt „geändert“ bei geänderter Anleitung.

### A13-7 · niedrig · Kleinigkeiten `scrAnleitungen`
- `OnVisible` wählt `First(Sort(colAnAlle, Title))`, die Liste sortiert aber aktive zuerst → markiert ist ggf. eine inaktive weiter unten. Gleiche Sortierung nehmen (`If(Coalesce(Aktiv, false), "0", "1") & Lower(Title)`).
- `btnAnNeu`: `SetFocus(txtAnTitel)` direkt nach `Set(varAnID, …)`; beim allerersten Eintrag ist `conAnForm` in diesem Moment noch unsichtbar → Fokus greift evtl. nicht (UNSICHER, harmlos).
- `btnKaInfo` ist mit 48 × 34 und Radius 17 eine „Pille“, nicht rund (Kurzfassung sagt „rund“). Kosmetisch.

### Paket 13 – geprüft, ohne Befund
- **ⓘ-Lage:** `btnKaBild` X = W−84 (64 breit). `btnKaInfo` X = W−68−80 → W−148…W−100, 16 px Abstand zu „Bild“; ohne Bild W−68…W−20. `lblKaFrage.Width` endet mit Bild+ⓘ bei W−164, mit ⓘ allein bei W−84 → jeweils 16 px Luft. Keine anderen Steuerelemente oben rechts in `conKaKarte` (belegt). Y 10/Höhe 34 wie „Bild“. `AbsKopf` verschiebt die ganze Karte (`conKaKarte.Y`), nicht die Kinder → passt.
- **Fenster:** Karte `Min(H−32, 1000)` → bei 1366 hoch 1000: Text 88–539, Bild 547–908, „Schließen“ 924–980; ohne Bild Text 88–908. Im Querformat (Ausrichtung nicht gesperrt) 736 hoch, passt ebenfalls. `Overflow.Scroll` am Label, `btnKaInfoSperre` deckt den Bildschirm, `conKaInfo` liegt nach dem Einfügen oben. `varInfoID` wird in `scrKategorie.OnVisible` auf 0 gesetzt; leer (nie gesetzt) = unsichtbar.
- **`varInfo` leer/gelöscht:** `If(IsBlank(varInfo.ID), Notify(…), Set(varInfoID, …))` – Fenster bleibt zu. Bild nur mit `varInfoID > 0 && varInfoBild > 0` (keine Abfrage bei geschlossenem Fenster). Gleiche Bildquelle wie `imgKaBild`.
- **`AnlID` in colAntworten:** in allen drei Zweigen (Nur-Lesen aus `pp`, Bearbeiten aus `p`, inaktive Altpunkte 0), Typ Zahl; Generator-Schemaprüfung 0 Fehler; `btnKaSpeichern` speichert per `ShowColumns` → `AnlID` gelangt nicht ins JSON (belegt).
- **Builder `conPRest` Zeile 1:** `lblPFoto`/`ddPFoto` 0–256, `lblPAnl`/`ddPAnl` 272–528, Zeile 2 (`lblPBed`) ab Y 62 unverändert; `conPRest` bleibt 528 × 250, `btnPNio` bei +256 unberührt. Kurzzeitige Überlappung bis B4 angekündigt. Foto-Texte nur Anzeige (`N`), Werte `W` gleich; `fnFotoText` (Vorschau) bewusst lang – kein Abgleich auf die alten Texte (belegt).
- **`ddPAnl.OnChange`:** gleiches Muster wie `ddPFoto` (Entwurf-Prüfung, frischer `LookUp` mit `RundgangID`/`Fassung`, `IfError` als Kettenglied, Nachlese in `colP`).
- **Prüfregel `colAnlAktiv`:** gefüllt in Stufe „laden“; alle Wege in den Editor (Ansehen, Bearbeiten → neue Fassung, Vorlagen, Neu) laufen über „laden“, „auswahl“ nach Holen/Duplizieren behält die Sammlung (belegt aus `varJob`/`varNach`/`varKopieNach`). Nur Art „Hinweis“ → blockiert das Aktivieren nicht.
- **Kopie/galAkt/neue Prüfpunkte:** `AnleitungID: Coalesce(q.AnleitungID, 0)` in der Kopie, `AnleitungID: 0` in `btnGlNeuP` und `btnMehrAnlegen`, Vergleich in `galAkt.Items` – vollständig.
- **`scrAnleitungen`:** `Refresh` vor `ClearCollect`, `Patch` mit frischem `LookUp`, `IfError` nur als Kettenglied, Nachlese `Patch(colAnAlle, …, LookUp(RG_Anleitungen, …))`, `Reset` der Eingaben bei Zeilenwechsel und beim Öffnen, Sperre `varSperreBis` bei „+ Anleitung“, Ladeschicht mit Sperrknopf. Layout 1366 × 768: Liste 24–444, Formular 468–1342, Text bis Y 560, Aktiv-Schalter 572–612. `btnLiAnleitungen` 862–1042 neben `btnLiKontakte` (650–850) und `btnLiAlle` (ab 1102).
- **Vollständigkeit:** App 2 Properties (Vorher/Nachher = Generator-Endstand nach der Änderung 08:15, zeichengleich), 9 neue Steuerelemente; Builder 11 Properties = genau die Differenz `builder_nach_p14_15.json` → `bloecke.json`, Vorher und Nachher je im Dokument, alle 24 neuen Builder-Steuerelemente im Dokument. Alle YAML-Blöcke mit PyYAML lesbar, jede Property mit `=`. Spalte/Liste zuerst (A1/B0), dann „Daten aktualisieren“.

---

## Zusammenfassung

Kein kritischer Befund, beide Pakete sind formal sauber (Generator 0 Fehler, Vorher/Nachher vollständig und zeichengleich, YAML lesbar, Delegation des Archivs korrekt, Ablauf Start → Archiv → Ansehen → Kategorie → zurück → Archiv → Start trägt). Zu beheben bzw. zu entscheiden:
1. **A13-1 (mittel):** `ddPAnl` ohne aktuellen Wert in Items (inaktiv/gelöscht/doppelter Titel) → falsche Anzeige, ggf. stilles Zurücksetzen auf 0. Wie `ddPBedA` bauen, Titel mit „(#ID)“.
2. **A13-2 (mittel, Entscheidung):** Inaktive Anleitung bleibt beim Prüfer sichtbar, Builder-Text verspricht anderes.
3. **A17-1 (mittel, Entscheidung):** „Ansehen → Protokoll“ erzeugt bei alten Läufen ohne PDF automatisch ein PDF und patcht – „nur lesen“ stimmt nicht.
4. Niedrig: Grenze 500 vs. 2000 (A17-2), Liste bei Wiederkehr nicht neu geladen (A17-4), `lblArInfo` 2. Zeile knapp (A17-5), Refresh fehlt (A13-3), roter Zwischenstand B6.1 (A13-4), Diffs ohne sichtbare Änderung (A13-5), Testbogen (A13-6).
Hinweis: `baukasten.py` wurde während der Prüfung geändert; geprüft ist der Stand der Dokumente von 08:16:43.
