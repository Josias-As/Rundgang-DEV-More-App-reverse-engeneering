# Unabhängige Prüfung – Paket N und Paket 8+9 (Rundgang-App)

Stand 02.11.2026. Geprüft: `pakete/PAKET_N_Nachholen.md`, `pakete/PAKET_8_9_APP.md`, Generator `werkzeuge/baukasten.py` (`paket8`, `paket9`, `fnfehlt_erweitern`, `ABS_KOPF`), `werkzeuge/doc_app89.py`, Ausgangsstand Export `2026-11-02_1541` (`arbeit/_entpackt/2026-11-02_1541/msapp/Src`, `References/DataSources.json`).

Eigene maschinelle Gegenproben (nicht aus dem Generator übernommen):
- Soll nach Paket 1–7 (aus Export 27.10. 09:09) gegen Export 02.11. 15:41 neu abgeglichen, auch in Gegenrichtung (Properties, die nur im Export stehen).
- Alle deutschen Blöcke beider Dokumente mit `rg.from_de` zurückübersetzt und gegen den Soll-Stand verglichen: 23/23 gleich, Klammern in Ordnung.
- Alle YAML-Blöcke (7) mit PyYAML gelesen: gültig.
- Feldlisten der drei `colAntworten`-Zweige: je 33 Felder, gleiche Menge.
- Jeder Aufruf von `fnFehlt`/`fnFehltGrund` (5 Stellen + App.Formulas): 13 Argumente.
- Spalten-Metadaten der Listen aus `DataSources.json` (interne Namen, Anzeigenamen, Längen).

Nicht in Studio getestet. Alles Folgende ist aus Export und Formeln **geschlussfolgert**, außer wo **belegt** steht.

---

## Befunde

### B1 · hoch · Paket N, Schritt N.1 (Spalte „Fassungf“) – Empfehlung würde die Fassungs-Spalte löschen

**Belegt** (`DataSources.json`, beide Exporte 1541 und Builder): In `RG_Pruefpunkte` gibt es **nur eine** Fassungs-Spalte. Ihr interner Name ist `Fassungf`, ihr Anzeigename `Fassung` (`"Fassungf": {"title": "Fassung", "type": "number"}`). Eine Spalte mit internem Namen `Fassung` existiert nicht. `rg.App.spalten` trägt jede Spalte unter internem **und** Anzeigenamen ein; dadurch sah es nach zwei Spalten aus.

**Ablauf:** Josias liest „Spalte `Fassungf` … kann gelöscht werden“, findet in den Listeneinstellungen über die Feld-URL (`Field=Fassungf`) die Spalte „Fassung“ und löscht sie. Danach sind alle Fassungen der Prüfpunkte weg; der Builder (Fassungen an den Bereichen, Kopie über `Fassung`) liest/schreibt eine nicht mehr vorhandene Spalte.

**Korrektur:** Den ganzen Spiegelstrich „Aufgefallen: … `Fassungf` …“ aus N.1 streichen (Generator `doc_app89.py`). Ebenso den Satz „Spalte `Fassungf` (Tippfehler) in `RG_Pruefpunkte`“ in CLAUDE.md Abschnitt 5 berichtigen (interner Name, kein zweites Feld). Nichts löschen.

### B2 · hoch (UNSICHER, vor Schritt 1 klären) · `RG_Ansprechpartner.Name` – Namenskonflikt mit der eingebauten Spalte „Name“

**Belegt:** Jede SharePoint-Liste bringt in Power Apps die schreibgeschützte Spalte `{Name}` mit dem **Anzeigenamen „Name“** mit (z. B. `RG_Konfiguration`: `{Name}` title „Name“, read-only). Paket 8+9 Schritt 1 lässt eine eigene Spalte `Name` anlegen und liest sie mit `ThisItem.Name` (`lblKaKritName.Text`); Paket 9 Builder schreibt sie mit `Patch(…; {Name: …})` und liest `ThisItem.Name`.

**Ablauf (UNSICHER, welcher der beiden Fälle eintritt):** Entweder lehnt SharePoint den Spaltennamen „Name“ ab („bereits verwendet oder reserviert“), oder es gibt danach zwei Spalten mit Anzeigename „Name“; Power Apps löst `ThisItem.Name` dann nicht eindeutig auf (im ungünstigen Fall auf den Dateinamen wie „3_.000“), und der Builder-Patch trifft das schreibgeschützte Feld.

**Korrektur:** Spalte anders nennen, z. B. `Kontakt` (oder `Person`), in beiden Paketen ersetzen: `lblKaKritName.Text` → `Coalesce(ThisItem.Kontakt; "") & …`, Schritt-1-Text, Builder-Paket 9 (`{Kontakt: …}`, `ThisItem.Kontakt`), `paket9()`-Spaltenliste. Kostet nichts und schließt den Fall aus.

### B3 · mittel · `btnKaNIO.OnSelect` + `conKaRueck`/`conKaKrit` – Doppeltippen meldet einen kritischen Mangel, der nicht gespeichert wird

**Ablauf:** Prüfpunkt IONIO, Rückfrage = Ja, Kritisch = Ja, **nicht Pflicht**. Prüfer tippt n.i.O. zweimal schnell (Handschuh). 1. Tipp: `Bewertung = "NIO"`, `varRueckPP` gesetzt. 2. Tipp trifft den Knopf, bevor das Fenster gezeichnet ist: `neu = ""` → Bewertung leer, `varRueckPP` bleibt gesetzt. Das Fenster zeigt fest „Ihre Antwort: n.i.O.“ (Text hängt nicht an der Bewertung). „Ja, stimmt“ → rotes Fenster (`r.Kritisch && !r.KritischOk` ist wahr) → „Ich habe Bescheid gegeben“ setzt `KritischOk` auf eine **leere** Antwort. Da nicht Pflicht, fehlt nichts → Speichern geht → kein n.i.O., kein Mangel, im Protokoll nichts. Der Prüfer glaubt, den Mangel erfasst zu haben.

**Korrektur (beides):**
1. Fenster nur bei echtem n.i.O.: `conKaRueck.Visible` = `varRueckPP > 0 && LookUp(colAntworten; PruefpunktID = varRueckPP).Bewertung = "NIO"`, `conKaKrit.Visible` entsprechend mit `varKritPP`; in `btnKaRueckJa` die Bedingung zu `If(r.Bewertung = "NIO" && r.Kritisch && !r.KritischOk; …)`.
2. In `btnKaNIO.OnSelect` beim Zurücknehmen die Fenster schließen: `If(neu = "NIO"; …; Set(varRueckPP; 0);; Set(varKritPP; 0))`. Optional eine eigene 1-s-Sperre (`varNioSperreBis`), nicht `varSperreBis` (die blockiert sonst still den Speichern-Zweig).

### B4 · mittel · Testbogen T5 – so nicht ausführbar

**Ablauf:** „Im roten Fenster nichts tun, App neu laden, Kategorie öffnen, Speichern“. Das n.i.O. steht nur in `colAntworten`; ohne Speichern ist es nach dem Neuladen weg. Beim Öffnen kommt die Antwort leer aus SharePoint, „Noch offen … (kritisch …)“ erscheint nicht, das rote Fenster auch nicht. Der Fall „App zwischendurch geschlossen“ aus dem Konzept kann gar nicht eintreten (es wird ohne Bestätigung nie gespeichert).

**Korrektur:** T5 ersetzen durch einen realen Weg zu „n.i.O. ohne Bestätigung“: (a) Prüfpunkt ohne Kritisch auf n.i.O. + Kommentar speichern; dann in SharePoint `Kritisch` = Ja setzen; Kategorie neu öffnen → „Noch offen … (kritisch: Bescheid bestätigen)“, Speichern öffnet das rote Fenster. (b) Rotes Fenster „n.i.O. war ein Versehen“ testen (fehlt im Bogen). Zeitachse: nach (a) Kritisch wieder auf Nein.

### B5 · mittel · `htmProtokoll.HtmlText` („bestätigt von …“) und `btnKaKritOk.OnSelect` – falsche Person, Uhrzeit ohne Tag

**Ablauf:** Prüfer A bestätigt den kritischen Mangel um 07:10 und speichert. Prüfer B öffnet die Kategorie (Rundgang noch in Arbeit), ändert eine andere Frage und speichert. `KritischOk`/`KritischZeit` kommen aus dem JSON mit (`alt.Value.KritischOk`), `PrueferName` des Ergebnisses ist jetzt B. Protokoll: „Bescheid gegeben, bestätigt von **B** um 07:10“. Bei Nachhol-Tagen (`cfgNachholTage`) steht nur die Uhrzeit, nicht der Tag.

**Korrektur:** Bei der Bestätigung die Person festhalten: Feld `KritischVon` (Text) in allen drei Zweigen (`""` bzw. aus JSON wie `KritischZeit`), in `btnKaKritOk`: `{KritischOk: true; KritischZeit: Text(Now(); "dd.mm. hh:mm"); KritischVon: User().FullName}`, in `ShowColumns(colSpeichern; …)` aufnehmen, Protokoll `fnHtml(Coalesce(Text(a.Value.KritischVon); e.PrueferName))`. In `btnKaNIO`, `txtKaZahl.OnChange`, `btnKaRueckNein`, `btnKaKritVersehen` beim Zurücksetzen `KritischVon: ""` ergänzen.

### B6 · mittel · `scrKategorie.OnVisible` (Block `colAbsTmp`) und Protokoll – Abschnitt-Überschrift verschwindet

**Ablauf 1 (Nur-Ansicht):** Abschnitt „Kompressor 1“ beginnt mit einer bedingten Frage, die beim Speichern ausgeblendet war (`Ausgeblendet = true`). Im Nur-Lesen-Zweig ist `BedID` immer 0, also bekommt die Frage mit der kleinsten `Reihenfolge` den Kopf – die ausgeblendete. `galKaPruefpunkte.Items` filtert sie weg (`!a.Ausgeblendet`) → keine Überschrift, obwohl Fragen des Abschnitts sichtbar sind. (Im Bearbeiten-Zweig verhindert die Regel „bevorzugt ohne Bedingung“ das, nur hier nicht.)

**Ablauf 2 (Protokoll):** Abschnitt nur aus bedingten Fragen; die erste ist beim Speichern ausgeblendet. `colSpeichern` behält `AbsKopf = true` auf der ausgeblendeten Zeile, `htmProtokoll` filtert ausgeblendete Zeilen weg → Überschrift fehlt im Protokoll/PDF.

**Korrektur:** (1) Im Filter `ClearCollect(colAbsTmp; ShowColumns(Filter(colAntworten; !Inaktiv && !Ausgeblendet && Abschnitt <> ""); …))` – im Bearbeiten-Zweig ist `Ausgeblendet` immer false, ändert dort nichts. (2) In `btnKaSpeichern.OnSelect` nach `ClearCollect(colSpeichern; …)` die Köpfe für das JSON neu bestimmen: derselbe `ForAll`-Block über die Zeilen mit `!Inaktiv && !Ausgeblendet && Abschnitt <> ""` von `colSpeichern` (vorher `UpdateIf(colSpeichern; true; {AbsKopf: false})`).

### B7 · niedrig · Paket N – dritte Fehleinfügung nicht erfasst: `lblKaZahlInfo.BorderColor`

**Belegt:** Der Export enthält `lblKaZahlInfo.BorderColor` = die Formel aus Paket 3 Schritt 3.5 (gehört zu `txtKaZahl.BorderColor`); im Soll gibt es diese Property nicht. Der Abgleich in `doc_app89.nachhol()` prüft nur Soll → Export, nicht Properties, die nur im Export stehen. Wirkung heute keine (Label hat `BorderThickness` 0), aber die Aussage „Alles andere stimmt zeichengleich“ stimmt nicht, und die Formel wird je Karte berechnet.

**Korrektur:** In Paket N einen Schritt „`lblKaZahlInfo.BorderColor` auf Standard zurück“ (Property in Studio zurücksetzen bzw. `RGBA(0; 18; 107; 1)`), Kurzfassung anpassen; im Generator auch Export-Properties ohne Soll melden.

Nebenbei (belegt, kein Paketthema): `addKaFoto.OnChange` und `scrProtokoll.OnVisible` enthalten im Export noch `//`-Kommentare (Regel 27.10.: keine Kommentare). Beim nächsten Ersetzen dieser Properties fallen sie weg.

### B8 · niedrig · `txtKaZahl.OnChange` + `btnKaSpeichern.OnSelect` – Rückfrage wird übersprungen

**Ablauf:** Zahl mit Rückfrage, bereits n.i.O. mit Kommentar gespeichert (z. B. 150, Grenze 100). Prüfer ändert auf 160 und tippt direkt „Speichern“. `OnChange` (Fokusverlust) setzt `varRueckPP`, danach läuft `OnSelect` von Speichern: nichts fehlt (Kommentar da, `KritischOk` bleibt nach `war`) → gespeichert, Bildschirm wechselt, die Rückfrage war nie zu sehen. Ist zusätzlich ein Kommentar leer und der Punkt kritisch, stehen beide Fenster gleichzeitig offen (rotes vorne) – Ergebnis bleibt stimmig.

**Korrektur (optional):** Am Anfang von `btnKaSpeichern.OnSelect` `If(varRueckPP > 0 || varKritPP > 0; false; …)` bzw. als erste Bedingung des mehrarmigen `If`: `varRueckPP > 0 || varKritPP > 0; Notify("Bitte zuerst die Rückfrage beantworten."; NotificationType.Warning);`.

### B9 · niedrig · `btnKaSpeichern.OnSelect` – rotes Fenster nur, wenn der kritische Punkt der erste offene ist

**Ablauf:** Frage 2 fehlt (Kommentar), Frage 7 ist kritisch unbestätigt. Speichern springt zu Frage 2, kein rotes Fenster. Erst nach dem Beheben von Frage 2 kommt es. Funktioniert, aber die Kurzerklärung „Fehlt nur noch die Bestätigung …“ beschreibt es ungenau; im Konzept stand „Tipp auf ‚fehlt‘ öffnet das Fenster“.

**Korrektur (optional):** Den kritischen Punkt vorziehen: `With({k: First(Filter(Sort(colAntworten; Reihenfolge) As a; !a.Inaktiv && <sichtbar> && a.Kritisch && a.Bewertung = "NIO" && !a.KritischOk))}; If(!IsBlank(k); Set(varKritPP; k.PruefpunktID);; Set(varSprungRec; k); Set(varSprungRec; <wie bisher>)))`.

### B10 · niedrig · Fenster-Knöpfe – zweiter Tipp landet in der Karte darunter

**Ablauf:** „Nein, korrigieren“, „Ich habe Bescheid gegeben“ oder „Versehen“ doppelt getippt: Der erste Tipp blendet das Fenster aus, der zweite trifft die Galerie darunter (z. B. `btnKaIO` einer anderen Karte) und setzt dort still i.O. bzw. nimmt es zurück. (Gleiches Muster wie das Foto-Fenster.)

**Korrektur (optional):** Beim Schließen `Set(varFensterZuBis; DateAdd(Now(); 1; TimeUnit.Seconds))` und `btnKaIO/btnKaNIO.OnSelect` mit `If(Now() >= varFensterZuBis; …)` umschließen (eigene Variable, nicht `varSperreBis`).

### B11 · niedrig · Layout der Fenster (Breite 768, Karte 720) – Texte können abgeschnitten werden

Geschätzt mit Segoe UI, Pt → px ×1,333, mittlere Zeichenbreite ~0,5 em, Zeilenhöhe ~1,3:
- `lblKaKritFrage` Höhe 64, Größe 18 → 2 Zeilen à ~56 Zeichen; `Frage` bis 255 Zeichen → ab ~110 Zeichen abgeschnitten.
- `lblKaKritText` Höhe 84, Größe 17 → knapp 3 Zeilen à ~59 Zeichen (~170); `KritischText` bis 255.
- `lblKaRueckFrage` Höhe 96 → 3 Zeilen inkl. „Ihre Antwort“: Frage nur ~2 Zeilen. `lblKaRueckNormal` 120 → 4 Zeilen, `RueckfrageText` bis 255 → knapp.
- `lblKaKritHinweis` `Wrap` false, 1 Zeile, `Hinweis` ist mehrzeilig gedacht („außerhalb 7–16 Uhr: Bereitschaft …“).
- Überlappungen: keine (Rückfrage: 20–68, 76–172, 180–300, Knöpfe 352–416 von 440; Kritisch bei 820: Galerie 280–648, Knöpfe 660–728 und 740–796).

**Korrektur:** In `conKaKritKarte` Frage 64→72 und Text 84→112 (Galerie-Y 280→316, Galeriehöhe `Parent.Height - 316 - 172`, `lblKaKritMelden.Y` 244→280, `lblKaKritLeer.Y` 320); `lblKaKritHinweis` Wrap true, Höhe 44, `TemplateSize` 110. Rückfrage-Karte 440→480, `lblKaRueckNormal.Y` 180→196.

### B12 · niedrig · Abschnitt-Kopf – Sonderfälle

- Zwei Prüfpunkte desselben Abschnitts mit gleicher `RgReihenfolge` → beide `AbsKopf` → zwei Überschriften. Korrektur: Gleichstand über die ID brechen, z. B. `t.PruefpunktID = First(SortByColumns(Filter(g …); "Reihenfolge"; SortOrder.Ascending; "PruefpunktID"; SortOrder.Ascending)).PruefpunktID`.
- Derselbe Abschnittsname an zwei getrennten Stellen → nur eine Überschrift (beim ersten Vorkommen). Im Builder als Pflegeregel nennen.
- Zeilen aus dem dritten Zweig (Prüfpunkt nicht mehr in der Kategorie) hängen hinten im JSON und stehen im Protokoll damit unter der letzten Abschnitt-Überschrift, obwohl sie zu einem anderen Abschnitt gehören. Korrektur: im Protokoll die Zeile mit `Abschnitt › Frage` beschriften, wenn `Abschnitt` ≠ Abschnitt des letzten Kopfes – oder einfacher: in der Zeile immer den Abschnitt klein vor die Frage setzen, wenn `AbsKopf` der Gruppe fehlt.

### B13 · niedrig · Bereich ausblenden – Name geht auch in Ergebnissen und Mängeln verloren

**Ablauf:** `btnRgAktion` schreibt für ausgeblendete Bereiche `BereichName = ""` in `KategorieListe`. Dieser Wert landet über `varBereichName` in `RG_KategorieErgebnisse.BereichName` und über `e3.BereichName` in `RG_Maengel.BereichName`. Für den gedachten Fall (ein ausgeblendeter Standard-Bereich je Rundgang) richtig. Blendet jemand einen echten Bereich aus, fehlt der Bereich in der Mängelliste dauerhaft.

Alte, bereits gestartete Rundgänge: `KategorieListe` ist beim Start eingefroren → sie zeigen den Bereich weiter (im Dokument so beschrieben, stimmt). `scrRundgang.OnVisible`, `btnRuAbschluss` und `tmrWeiter` lesen `""` problemlos; `galRuKategorien.ErsteImBereich` ist für `""` false. Kein Fehler.

**Korrektur (optional):** Im Builder beim Schalter „Ausblenden“ den Hinweis „Name erscheint dann auch nicht in Mängeln/Protokoll“.

### B14 · niedrig · Dokumentation

- Kurzfassung Paket 8+9: „30 neue Steuerelemente“ – es sind **23** (1 + 8 + 14). `doc_app89.py` rechnet `len(neue_controls) - 5`; die 7 Steuerelemente aus Paket 6 (`conKaBild` …) werden mitgezählt.
- „Dann ist dein Stand zeichengleich“ – nicht ganz (B7, Kommentare in `btnRuAbschluss` des Solls statt Export; Wirkung gleich).
- T1/T2 setzen den Builder-Teil von Paket 8 voraus, der laut CLAUDE.md noch nicht eingefügt ist. Ersatz nennen: `Abschnitt` bzw. `Ausblenden` direkt in SharePoint setzen.
- Schritt 1: Berechtigung der neuen Liste `RG_Ansprechpartner` (mindestens Lesen für alle Prüfer, wie die übrigen RG-Listen) erwähnen; sonst schlägt `ClearCollect(colKontakte …)` in `OnVisible` fehl und das rote Fenster zeigt „Keine Ansprechpartner“.
- Rückfrage und kritische Meldung greifen nur bei n.i.O. aus IONIO oder bei ZAHL im Grenzmodus „Mangel“ (bei „Warnen“ und „Sperren“ nie). So im Konzept gewollt; im Test T8 den Grenzmodus „Mangel“ ausdrücklich nennen.

---

## Geprüft, ohne Befund

- **Paket N, Reparaturen:** `lblKaHinweis.Text` = `ThisItem.Hinweis` und `lblKaAbstand.Text` = `ThisItem.Auswahl` entsprechen genau dem Export 27.10. 09:09 (belegt). Die Formel aus `lblKaHinweis` gehört in `lblKaFotoHinweis` (N.3.1), die aus `lblKaAbstand` in `lblKaStand` (N.3.2) – passt.
- **Paket N, Vollständigkeit:** Eigener Abgleich Soll 1–7 ↔ Export ergibt genau die 8 Properties aus N + die 5 Paket-5-Steuerelemente; die 2 fehlenden (`btnKaFoto.PressedColor` = `Self.Color`, `imgKaBild.ImagePosition` = `ImagePosition.Fit`) sind Standardwerte. Aus Paket 5 fehlt sonst nichts (Paket 5 ändert nur App.Formulas + 5 Steuerelemente; `conKaKarte.Height` braucht keine Änderung, die neuen Felder liegen in derselben Zeile). Aus Paket 7 fehlt nichts (App.Formulas, `btnKaFoto.Text/Visible`, `lblKaFotoHinweis`).
- **Paket N, Reihenfolge:** N.4 (App.Formulas mit `fnDatumText`) vor N.5 (Steuerelemente, die `fnDatumText` aufrufen); Signatur von `fnFehlt` bleibt 12 → „kein Rot“ stimmt. YAML-Einfügeort (`txtKaText` in `conKaKarte` markieren) und E-05-Hinweise stimmen.
- **Rückübersetzung:** alle 23 deutschen Blöcke = Soll (englisch), Klammern in Ordnung, keine Kommentare.
- **colAntworten:** alle drei Zweige dieselben 33 Felder. Typen stimmig: `Abschnitt`, `KritischText`, `Ansprechpartner`, `RueckfrageText`, `KritischZeit` Text; `AbsKopf`, `Kritisch`, `Rueckfrage`, `KritischOk` Boolean (JSON über `Coalesce(IfError(Boolean(…); false); false)`); `MinWert/MaxWert` Number bzw. `Blank()` im `Collect`.
- **Block `colAbsTmp` + `ForAll(… Patch(colAntworten …))`:** gültig. `ForAll` läuft über `colAbsTmp` und ändert nur `colAntworten`; das Lesen von `colAbsTmp` im Schleifenrumpf ist erlaubt. `Min(g; Reihenfolge)` auf einer `With`-Tabelle gültig. `ShowColumns` mit Bezeichnern (passt zu `supportcolumnnamesasidentifiers`). Logik: je Abschnitt (Groß/Klein egal) genau die erste Frage ohne Bedingung, sonst die erste überhaupt (Ausnahmen B6/B12).
- **fnFehlt/fnFehltGrund:** 13 Parameter in beiden Definitionen, alle 5 Aufrufer (`lblKaFehlendAnzahl`, `lblKaFehlend` ×2, `conKaKarte.BorderColor/BorderThickness`, `btnKaSpeichern`) mit 13 Argumenten und passendem Präfix (`a.`, `z.`, `ThisItem.`). Keine weiteren Aufrufer in anderen Bildschirmen (belegt). Grund „Kritisch“ hat die niedrigste Rangfolge, „Noch offen“ zeigt zuerst Kommentar/Foto, dann „(kritisch: Bescheid bestätigen)“ – stimmig.
- **Ablauf n.i.O. → Rückfrage → Ja/Nein → kritisch → Bestätigung → Speichern:** Reihenfolge Rückfrage vor kritisch, „Nein“ leert Bewertung und Zahl (das Zahlfeld folgt, weil sich `Default` ändert), „Ja“ öffnet bei Kritisch das rote Fenster, Speichern ist ohne Bestätigung gesperrt (`fnFehlt`), „Versehen“ nimmt zurück. Zurücknehmen per n.i.O.-Knopf löscht die Bestätigung.
- **txtKaZahl.OnChange / fnZahlBewertung:** Mangel → NIO → Auslöser; Warnen → IO (kein Auslöser, Rahmen orange); Sperren → `""` (Grund „Bereich“); Sperren mit min > max → Mangel. Bestätigung bleibt, solange es n.i.O. bleibt (`war`); Wechsel in den Sollbereich löscht sie.
- **Erneutes Öffnen:** `KritischOk`/`KritischZeit` kommen im Bearbeiten-Zweig aus dem JSON (`alt.Value…`), bei fehlendem Feld (alte Ergebnisse) false/leer; ein neu als kritisch markierter Punkt mit altem n.i.O. muss bestätigt werden – gewollt.
- **Nur-Ansicht:** `btnKaNIO`/`txtKaZahl` im `DisplayMode.View`, `btnKaSpeichern.Visible = !varNurLesen` → keine Fenster, keine Änderungen. `varRueckPP`/`varKritPP` werden in `OnVisible` auf 0 gesetzt.
- **Deaktivierte Punkte (`Inaktiv`) und ausgeblendete Fragen:** zählen nicht als offen, lösen nichts aus; beim Speichern werden ausgeblendete geleert (alte `KritischOk`-Reste dort sind wirkungslos, Protokoll filtert, Mängel nur NIO).
- **Galerie `galKaPruefpunkte` (VariableHeight):** `lblKaAbschnitt` Y 8 + Höhe 44 endet bei 52 = `conKaKarte.Y`; `lblKaAbstand.Y = conKaKarte.Y + conKaKarte.Height` folgt automatisch. Keine Überlappung.
- **YAML:** Property-Namen gültig für Label@2.5.1 (Align, Fill, VerticalAlign, Wrap …), Classic/Button@2.2.0 (kein AccessibleLabel verwendet), GroupContainer@1.5.0 ManualLayout, Gallery@2.15.0 Vertical. Reihenfolge der Kinder (Sperr-Knopf zuerst = hinten, Karte danach = vorne) wie bei `conKaFoto` im Export (belegt). `conKaKrit` liegt nach dem Einfügen vor `conKaRueck`; beide gleichzeitig nur im Fall B8, dann ist das rote vorne – richtig.
- **galKaKritKontakte.Items:** `Sort(…; If(Coalesce(Allgemein; false); 1; 0))` gültig (Satzbereich der gefilterten Tabelle), zugeordnete vor allgemeinen; `Filter(colKontakte; false)` liefert eine leere Tabelle gleichen Typs; ID-Vergleich über `Trim(s.Value) = Text(k.ID)` verträgt Leerzeichen nach `;`. `Filter(RG_Ansprechpartner; Aktiv = true)` delegierbar.
- **Textbreiten der Knöpfe/Titel:** „Ist das wirklich so?“, „Nein, korrigieren“/„Ja, stimmt“ (328 px), „⚠ Kritischer Mangel – sofort melden“, „Ich habe Bescheid gegeben“, „n.i.O. war ein Versehen – Antwort zurücknehmen“ passen in eine Zeile.
- **Speichern/JSON/Mängel:** `ShowColumns(colSpeichern; …; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit)` vollständig; `RG_Maengel.Kommentar` ist mehrzeilig (keine 255-Grenze, belegt), `Frage` mit `Left(…; 255)` begrenzt.
- **Bereich ausblenden:** `btnRgAktion` (`Coalesce(…Ausblenden; false)`, Spalte vorhanden, belegt), `galRuKategorien.Items` (keine Überschrift bei leerem Namen), `lblKaUnter.Text`, Protokollkopf – stimmig; alte Rundgänge unverändert.


## Einarbeitung (Engineering-Chat, 02.11.)
- B1 übernommen: Absatz zu `Fassungf` gestrichen, CLAUDE.md berichtigt (Fehlurteil).
- B2: Spalte heißt `Kontakt` (App und Builder).
- B3: Fenster nur sichtbar bei `Bewertung = "NIO"`, Zurücknehmen schließt beide Fenster, „Bescheid gegeben“ speichert nur bei n.i.O.
- B4: Test T5 neu (gespeichertes n.i.O., danach Kritisch), T5b „Versehen“, T5c Doppeltipp.
- B5: neues Feld `KritischVon` (User().FullName), Zeit mit Datum; Protokoll nennt es.
- B6/B12: Kopf nur aus sichtbaren Fragen, Ordnung Reihenfolge*1000000+ID, beim Speichern auf colSpeichern neu bestimmt.
- B7: Reparatur N.2.3 `lblKaZahlInfo.BorderColor`.
- B8: Speichern gesperrt, solange ein Fenster offen ist. B9: Speichern öffnet das erste unbestätigte kritische n.i.O. (sichtbar), nicht nur den ersten offenen Punkt.
- B10, B12 (entfernte Punkte), B13: als bekannte Grenzen dokumentiert.
- B11: Höhen der Fenstertexte erhöht, Hinweis zweizeilig.
- B14: Anzahl korrigiert, T1/T2 mit Ersatzweg über SharePoint, Berechtigung genannt.
Danach: Generator 0 Fehler, Mutation 12/12, Logik 81 Szenarien 0 Fehler.
