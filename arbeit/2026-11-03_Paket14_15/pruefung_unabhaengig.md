# Unabhängige Prüfung Paket 14+15 (Rundgang-App + Builder)

Stand 03.11.2026. Geprüft: `pakete/PAKET_14_15_APP.md`, `pakete/builder/PAKET_14_15_BUILDER.md`, Generator `werkzeuge/baukasten.py` (`paket14`), Vorher-/Nachher-Stände. Nur gelesen, nichts geändert. Nicht in Studio getestet.

## 0. Maschinelle Gegenproben (eigene Skripte)

| Prüfung | Ergebnis |
|---|---|
| 9 App-Blöcke im Dokument = Kette `paket1…paket16, paket14` (`to_de`/`from_de`) | 9/9 gleich |
| 9 App-Vorher-Fassungen = Stand nach Paket 16 | 9/9 gleich |
| 11 Builder-Vorher-Fassungen = `builder_nach_p12_16.json` | 11/11 gleich |
| Builder-Nachher: `bloecke.json` enthält schon Paket 13 (Anleitungen). Abweichungen zu den 14+15-Blöcken nur durch `AnleitungID`/`varAnID`/`colAnlAktiv` | erklärt, siehe B-H1 |
| Felder in den drei `colAntworten`-Zweigen | 46/46/46, gleiche Namen |
| Logik-Probe `logik_probe.py` | 103 Szenarien, 0 Fehler |
| Textbreiten (Schätzfunktion `textbreite`) Fenster `conZa`, `btnPZahlMehr`, `lblPGrenz` | passen (179/202, 241/290 px) |
| Layout `conPZahl`: Knopf 316/56/212×26 endet bei X 528 = Containerbreite, Y 82 = Beginn `galPGrenz`; `txtPMin/Max/btnPNM` enden bei Y 56 | keine Überlappung |

## 1. Befunde Rundgang-App

### A-1 · Mittel · `btnKaRueckNein.OnSelect`, `btnKaKritVersehen.OnSelect` (nicht im Paket)
**Ablauf:** Zahl A (Rückfrage oder kritisch, `AbwMax` 0,5, zuletzt 7,6). Prüfer tippt 12 → n.i.O. → `txtKaZahl.OnChange` rechnet neu: A „starke Abweichung“, B (vergleicht mit A) „weicht von „A“ ab (12)“, beide `KommentarPflicht = true`. Prüfer tippt „Nein, Versehen“ → beide Knöpfe setzen `WertZahl: Blank()`, rechnen aber **nicht** neu.
**Folge:** A zeigt weiter orange „starke Abweichung …, bitte begründen“ bei leerem Feld (nur Anzeige). B verlangt weiter eine Begründung, und wenn A nicht Pflicht ist und leer bleibt, wird B mit `AbwText` „weicht von „A“ ab (12)“ gespeichert, obwohl A leer ist (Protokoll falsch).
**Korrektur:** In beiden Knöpfen vor `Set(varGeaendert; true)` dieselben zwei Zeilen wie in `txtKaZahl.OnChange` einfügen (`ClearCollect(colVglTmp; …);; ForAll(colVglTmp As v; Patch(…))`). +2 Properties im Paket, Vorher-Fassungen in den Anhang. Generator: Prüfung „jede Stelle, die `WertZahl` in `colAntworten` schreibt, endet mit REKALK“.

### A-2 · Mittel · `lblKaZahlInfo` (Height 56 fest, Text 4.1)
**Ablauf:** Zahl mit Grenzen, „nicht messbar“ erlaubt (`btnKaNM` sichtbar) und Abweichung. Breite bei 768 px: 720 − 256 − 136 = 328 px (Inhalt ~318). Text z. B. „bar · Soll ab 1,5 bis 2,5 · zuletzt 7,6 (26.10.) · starke Abweichung zum letzten Mal, bitte begründen“ ≈ 714 px bei Größe 12 → 3 Zeilen; Platz hat die Höhe 56 nur für 2 (Zeile ≈ 19 px + 2×5 Innenabstand). Ohne NM-Knopf (454 px Inhalt) reicht es knapp; mit Vergleich und langem Partnertitel („…; weicht von „Druck Kessel links“ ab (7,2), bitte begründen“ ≈ 810–850 px) oder schmalerem Gerät ebenfalls 3 Zeilen.
**Folge:** Ausgerechnet das Ende „bitte begründen“ wird abgeschnitten (Classic Label, Overflow verborgen).
**Korrektur (eine davon):** (a) Abweichungs-Text an den Anfang stellen (`AbwText` vor Einheit/Soll), (b) eigene Zeile `lblKaAbw` unter der Zahl mit eigener Höhe und `conKaKarte.Height` + 22 bei `AbwText <> ""`, (c) Höhe 56 → `If(ThisItem.AbwText <> "" || !IsBlank(ThisItem.Letzter); 76; 56)` mit Anpassung von `conKaKarte.Height`/`txtKaKommentar.Y`. Die Textbreitenprüfung des Generators auf dynamische Texte dieses Labels ausdehnen (Beispieltexte wie oben).

### A-3 · Mittel · `scrKategorie.OnVisible` (Auswahl „letzter Lauf“)
**Ablauf:** `First(Sort(Filter(…); ID; SortOrder.Descending))` nimmt die **zuletzt angelegte** Durchführung, nicht die mit dem spätesten Tag. Mit `cfgNachholTage ≥ 1`: Lauf heute (ID 50) abgeschlossen, danach gestern nachgeholt (ID 51). Morgen vergleicht die App mit **gestern** (ID 51) statt mit heute. Beim Nachholen von gestern ist der „letzte“ Lauf der von heute (späterer Tag) → bei `NurSteigend` meldet ein korrekter Zählerstand „kleiner als beim letzten Mal“.
**Korrektur:**
```
Set(varLetzteDurch; First(Filter(Sort(Filter(RG_Durchfuehrungen; RundgangID = varLetzteRg && Status = stAbgeschlossen && TestDatensatz = varLetzteTest); TagText; SortOrder.Descending); DateValue(TagText) < DateValue(varDurch.TagText))))
```
Innerer Teil delegierbar (Text-Sortierung SharePoint), äußerer Filter lokal auf den neuesten 500 (Delegationswarnung, hier unkritisch). Wenn Nachholen in Betrieb nie vorkommt (`NachholTage` = 0): als bekannte Grenze dokumentieren.

### A-4 · Mittel · `scrKategorie.OnVisible` (kein `Refresh(RG_Durchfuehrungen)`)
**Ablauf:** Tablet bleibt über Nacht offen. Tag 1: Abfrage „letzter abgeschlossener Lauf von Rundgang A“ liefert D0. Tag 2 (neue `varDurchID`, gleiche Filterwerte, gleiche Abfrage-URL): Ohne `Refresh` kann der Sitzungs-Cache (Regel E-01, CLAUDE.md §4) wieder D0 liefern statt D1.
**Korrektur:** Im Ladezweig vor `Set(varLetzteDurch; …)` `Refresh(RG_Durchfuehrungen);;` einfügen (läuft nur einmal je Durchführung).

### A-5 · Niedrig–Mittel · Partner mit Bedingung (ausgeblendet)
**Ablauf:** B vergleicht mit A, A hat eine Bedingung. Prüfer trägt A = 9 ein, ändert danach die Bedingungsfrage → A wird ausgeblendet (Wert bleibt bis zum Speichern in `colAntworten`). REKALK läuft bei Bedingungsänderungen nicht, und auch beim nächsten Lauf zählt `w.WertZahl` eines ausgeblendeten A. B verlangt eine Begründung und speichert „weicht von „A“ ab (9)“, A selbst wird leer/ausgeblendet gespeichert.
**Korrektur:** Einfachste Lösung im Builder: `galPr` Fehler „Vergleich mit einer Frage, die eine Bedingung hat, ist nicht möglich“ (oder nur, wenn Bedingungen von p und Partner verschieden sind). Alternative in der App: Sichtbarkeit von `w` per `fnSichtbar` in REKALK prüfen und REKALK zusätzlich in alle Knöpfe legen, die eine Bedingung umschalten (viele Stellen). Zusätzlich in `btnKaSpeichern` beim Ausblenden `AbwText: ""` mitsetzen (sauberes JSON).

### A-6 · Niedrig · Nur-Ansicht ohne gespeicherte Antworten nutzt alten `colLetzte`
**Ablauf:** `varNurLesen` und `t` leer → Zweig 2 rechnet `Letzter` aus `colLetzte`, der im Nur-Lesen-Fall nicht geladen wird und von einer anderen Durchführung stammen kann. Die Karte zeigt dann „zuletzt …“ eines fremden Laufs.
**Korrektur:** In `Letzter:` die Bedingung um `!varNurLesen && varLetzteFuer = varDurchID &&` ergänzen. Kosmetisch dazu: `LetzterTag` steht in jedem Eintrag des JSON (auch ohne `Letzter`, ggf. Datum eines fremden Laufs, wenn die Kategorie keinen Abw-Punkt hat). Angezeigt wird es nie ohne `Letzter`, daher nur Datenrauschen.

### A-7 · Niedrig · Grenzwert und Rundung (`fnAbweichung`, `fnVergleich`)
`Abs(1,1 − 0,8) > 0,3` ist bei Gleitkomma wahr (0,30000000000000004). Ein Wert genau an der Grenze verlangt dann eine Begründung. **Korrektur:** `Round(Abs(z − l); 6) > …` bzw. `Round(Abs(z − w); 6) > …`. Logik-Probe um einen Grenzfall mit solchen Zahlen ergänzen. Hinweis: `AbwProzent` bei Vorwert 0 → jede Änderung ist eine Abweichung (in Ordnung, aber im Builder-Hinweistext nennen).

### A-8 · Niedrig · Lücke beim Vorwert
Hatte der letzte Lauf „nicht messbar“ oder war der Punkt ausgeblendet, fehlt `Z` (gefiltert) → kein Vergleich, auch nicht mit dem vorletzten Lauf. Bei Zählerständen fällt die Prüfung dann einmal aus. In der Kurzfassung als Grenze nennen (wie „zwei Aktivierungen“).

### A-9 · Niedrig · `QuelleID` aus dem eigenen aktiven Stand
Holt der Builder einen Prüfpunkt aus der **aktiven** Fassung desselben Rundgangs in den Entwurf (Holen/Duplizieren), hat die Kopie `QuelleID` = ID aus dem letzten Lauf. Nach dem Aktivieren bekommt die Kopie den Vorwert des Originals („Zähler 2“ vergleicht mit „Zähler 1“). Selten; dokumentieren oder beim Holen aus dem eigenen Rundgang `QuelleID: 0` setzen.

### A-10 · Mittel (Testbogen) · Tests T1–T7 so nicht ausführbar
- T2 „Rundgang zurücksetzen und neu starten“: `btnRuZuruecksetzen` wirkt nur im Status „Abschluss“ (setzt auf „InArbeit“, belegt), ein abgeschlossener Lauf lässt sich nicht zurücksetzen. Es gibt je Rundgang und Tag nur **eine** Durchführung (Schlüssel `R<ID>-<TagText>`, belegt in `btnRgAktion`). T2 braucht also einen zweiten Tag oder Nachholen.
- T5/T6 setzen `NurSteigend`/`VergleichPunkt` nach T1. Jede Builder-Änderung braucht einen Entwurf + Aktivieren. Werden die Einstellungen in zwei Schritten aktiviert, liegen zwischen T1-Lauf und Test-Lauf zwei Fassungen → kein Vorwert (bekannte Grenze) → T5 schlägt fehl.
**Korrektur (Zeitachse):** Vorher im Builder in **einer** Fassung einstellen: P1 `AbwMax` 0,5, P2 `NurSteigend`, P3/P4 Vergleich 0,2; aktivieren. Tag N (oder Nachholtag „gestern“ mit `NachholTage ≥ 1`): Lauf 1 komplett abschließen (P1 7,6, P2 1000). Tag N+1: T2–T7. Ausdrücklich: Test-Rundgang „ZZ Test …“ (beide Läufe Testdaten).

## 2. Befunde Builder

### B-1 · Niedrig–Mittel · `ddZaVgl` zeigt ungültigen Verweis nicht
`ddPBedA.Items` hat einen dritten Teil mit dem aktuellen (ungültigen) Wert, `ddZaVgl.Items` nicht. **Ablauf:** P vergleicht mit Q, Q wird auf i.O./n.i.O. umgestellt → `galPr` Fehler „Der Vergleich zeigt auf keine Zahl-Frage …“. Im Fenster steht der Dropdown dann auf dem ersten Eintrag „— kein Vergleich —“; diesen nochmals zu wählen löst kein `OnChange` aus → Fehler lässt sich nur über einen Umweg (anderen Punkt wählen, dann „kein Vergleich“) beheben. UNSICHER: Löst die Default-Änderung beim Auswählen von P ein `OnChange` aus, wird `VergleichPunkt` still auf 0 gesetzt.
**Korrektur:** Dritten Teil wie bei `ddPBedA` ergänzen (`{T: Filter(Table({ID: VergleichPunkt; N: "⚠ " & …}); <ungültig>)}`) und `Default` darauf abstimmen.

### B-2 · Niedrig · Typwechsel weg von „Zahl“
**Ablauf:** P (Zahl, `VergleichPunkt` ≠ 0) wird auf Auswahl umgestellt → `conPZahl` (mit `btnPZahlMehr`) ist unsichtbar, `galPr` meldet Fehler, Aktivieren gesperrt. Beheben nur durch Zurückstellen auf Zahl, Fenster, „kein Vergleich“, wieder umstellen.
**Korrektur:** `btnPTyp.OnSelect` beim Verlassen von „ZAHL“ eigenen `VergleichPunkt` und Verweise anderer Punkte auf P (`Filter(colP; VergleichPunkt = varAuswahlID)`) auf 0 setzen (wie beim Verschieben). Alternativ Fehlertext „… (Typ wieder auf Zahl stellen und Vergleich entfernen)“.

### B-3 · Niedrig · `galPr` prüft `VergleichTol` nicht
Negativer Unterschied → jede Eingabe verlangt eine Begründung. **Korrektur:** Fehlerzeile analog `AbwMax < 0` für `VergleichTol < 0`. Optional Hinweis bei gegenseitigem Vergleich (P→Q und Q→P: doppelte Begründung).

### B-4 · Niedrig · `galAkt` bei Vergleich mit neuer Frage
P vergleicht neu mit einer im Entwurf neu angelegten Frage (QuelleID 0), vorher kein Vergleich (0) → `0 <> 0` falsch → P erscheint nicht als „geändert“. Gleiches Verhalten wie bei Bedingungen; nur Übersicht. Hinnehmbar, ggf. `p.VergleichPunkt <> 0 && Coalesce(a.VergleichPunkt; 0) = 0` zusätzlich prüfen.

### B-5 · Kosmetisch · `ddPKategorie.OnChange`
Meldung nennt nur entfernte Bedingungen, gelöste Vergleiche werden still entfernt. Text um „… Vergleich(e)“ ergänzen.

### B-H1 · Hinweis · Reihenfolge zu Paket 13
`bloecke.json` (Nachher) enthält bereits Paket 13; `PAKET_13_ANLEITUNGEN.md` setzt „Builder bis Paket 14+15“ voraus. Die 14+15-Blöcke sind ganze Properties ohne Paket-13-Anteile. **14+15 muss vor 13 eingefügt werden**, sonst überschreibt 14+15 `btnGlNeuP`, `btnMehrAnlegen`, `galAkt`, `galPr`, `tmrArbeit`, `lblVsRegeln`, `App.OnStart` von Paket 13. In beide Kurzfassungen aufnehmen.

## 3. Geprüft, ohne Befund

- **Power Fx gültig:** UDFs `fnAbweichung`/`fnVergleich` (reine Funktionen, `Abs`, `If`, `Coalesce`; Blank-Werte über Number-Parameter zulässig). REKALK: `ForAll(Filter(colAntworten As a0; …) As a; …)` liest `colAntworten` nur (kein Ändern der durchlaufenen Sammlung), schreibt in `colVglTmp`; zweiter `ForAll` über `colVglTmp` patcht `colAntworten` – zulässig. Feld `Text` in `colVglTmp` kollidiert nicht (überall `As`). `Ungroup(…; T)` als Bezeichner wie in `btnRuAbschluss`/`ddArRg`. `Table(ParseJSON(…))`, `Value(j.Value.WertZahl)` (JSON-Zahl, null → leer), `DateValue(TagText)` (ISO, wie im Protokoll). Klammern und Ketten (`;;` im Dann-Zweig) stimmen.
- **Delegation:** `RundgangID =`, `Status = stAbgeschlossen` (Text, benannte Konstante), `TestDatensatz = varLetzteTest` (Ja/Nein `=` auf SharePoint delegierbar), `Sort(…; ID; Descending)` delegierbar. `TestDatensatz` wird bei jedem Start gesetzt (`StartsWith(Title; "ZZ Test")`), also nie leer; „Test nur mit Test“ wirkt praktisch nur nach Umbenennen – korrekt.
- **KommentarPflicht zurücksetzen:** Jeder Punkt in `colVglTmp` bekommt `KPflOrig || Abw || Vgl`; fällt die Abweichung weg, gilt wieder das Original. Punkte außerhalb von `colVglTmp` (VglID 0 und `Letzter` leer) werden nie angehoben; die Menge ist pro Öffnen fest (`Letzter`/`VglID` ändern sich nicht), also nichts zurückzusetzen. `UpdateIf` „Kommentar leeren“ lässt Begründungen angehobener Punkte stehen und leert sie, wenn die Abweichung entfallen ist (gleich wie „Warnen“).
- **Abläufe:** erster Lauf (kein Vorwert, `colLetzte` leer, kein „zuletzt“), zweiter Lauf, neue Fassung (ID oder `QuelleID`), Bearbeiten einer gespeicherten Kategorie (Vorwert neu berechnet, Pflicht neu angehoben), Wechsel der Durchführung (`varLetzteFuer`, Neuladen bei Rückkehr), Nur-Ansicht mit JSON (`Letzter`, `AbwText`, orange, „begründet“), gelöschter Prüfpunkt (Zweig 3, aus REKALK ausgeschlossen), Partner leer/„nicht messbar“ (kein Vergleich), „nicht messbar“ am Punkt selbst (keine Abweichung, nur NM-Begründung), kein Mangel (`Bewertung` unverändert), Protokoll mit `fnHtml`.
- **colAntworten-Schema:** 46 Felder in allen drei Zweigen, Typen passend (`Letzter` Number, `AbwMax` Blank/Number wie bisher `MinWert`).
- **Builder:** Fenster `conZa` (620×560, alle Elemente innerhalb, Hinweistext 3 Zeilen in 88 px), Sperrfläche, Reihenfolge `conZa` vor `conEdLaden` (Anleitung zum Nach-vorne-Holen vorhanden). Schreibstellen mit Entwurfsprüfung wie die übrigen Felder, `btnZaSteigend` mit 1-s-Sperre. Kopie: `VglAlt` wird wie `BedAlt` umgeschrieben (ganze Kopie → neue ID; einzelner Punkt in dieselbe Kategorie → alter Partner; andere Kategorie/anderer Rundgang/inaktiver Partner → 0); Fehler zählen in `varKopieFehler` (Rücknahme). Entfernen (Ebene 3) und Verschieben lösen Verweise. Neue Prüfpunkte mit leeren Feldern. `galPr` Fehler für ungültigen Verweis und negative Abweichung. `btnLiVorlagen` legt Punkte ohne die neuen Felder an (Spaltenstandard greift).
- **Dokumente:** jede Property genau einmal (App 9, Builder 11 + 2 Blöcke), Vorher-Fassungen vollständig und zeichengleich, „Nachprüfen“-Enden passen, Builder-Tests 1–4 ausführbar.

## 4. Zusammenfassung

- Kein Syntax- oder Schemafehler gefunden. Blöcke und Vorher-Fassungen entsprechen dem Generator (9 + 11), drei colAntworten-Zweige gleich (46 Felder).
- Mittel: A-1 „Nein, Versehen“/„war ein Versehen“ rechnen nicht neu → veralteter Abweichungstext und Begründungspflicht (auch beim Partner), ggf. falsch gespeichert.
- Mittel: A-2 `lblKaZahlInfo` (Höhe 56) schneidet „bitte begründen“ ab, sicher mit NM-Knopf.
- Mittel: A-3 „letzter Lauf“ nach höchster ID statt spätestem Tag (Nachholen); A-4 kein `Refresh(RG_Durchfuehrungen)` (App über Nacht offen).
- Mittel: A-10 Testbogen: T2 so nicht ausführbar (eine Durchführung je Tag, Zurücksetzen nur aus „Abschluss“), Einstellungen in einer Fassung vorab.
- Niedrig: ausgeblendeter Partner (A-5), Nur-Ansicht mit fremdem Vorwert (A-6), Gleitkomma an der Grenze (A-7), Builder-Dropdown ohne ungültigen Wert (B-1), Typwechsel (B-2), `VergleichTol < 0` (B-3).
- KommentarPflicht wird korrekt zurückgesetzt. Punkte außerhalb von `colVglTmp` brauchen kein Zurücksetzen.
- Reihenfolge: Builder 14+15 vor Paket 13 einfügen (B-H1).
- Empfehlung: A-1 bis A-4 und den Testbogen vor dem Einfügen beheben, Rest nach Wahl.

## Einarbeitung (Engineering-Chat, 03.11.)
- A-1: `btnKaRueckNein.OnSelect` und `btnKaKritVersehen.OnSelect` rechnen Abweichung/Vergleich neu (2 Properties mehr im App-Paket, jetzt 12).
- A-2: `lblKaZahlInfo.Height` 64 statt 56, wenn Zusatztext da ist (Lücke zur Kommentarzeile 68).
- A-3/A-4: `Refresh(RG_Durchfuehrungen)`, Kandidaten nach `TagText` absteigend (FirstN 20), lokal `DateValue(TagText) < DateValue(varLetzteTag)` – richtig auch bei Nachhol-Läufen.
- A-10: Testbogen neu (T0 alles in einer Fassung, Tag N / N+1, T6b).
- Niedrig: `Round(…; 6)` in `fnAbweichung`/`fnVergleich` (Szenario 1,1/0,8/0,3 ergänzt, Logik 104); Prüfregel „erlaubter Unterschied negativ“ (kommt mit Builder-Paket 13, das galPr ohnehin ganz ersetzt); Typwechsel als bekannt im Builder-Test; übrige niedrige Befunde (ausgeblendeter Partner, Nur-Ansicht ohne Speicherung, „nicht messbar“ im Vorlauf, ddZaVgl-Anzeige, galAkt neu-zu-neu, Meldung beim Verschieben) bewusst nicht geändert.
- Reihenfolge Builder 14+15 vor 13: in beiden Dokumenten vermerkt.
Danach: Generatoren 0 Fehler, Mutation 12/12 und 13/13, Logik 104.
