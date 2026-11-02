# Unabhängige Prüfung – Paket 12+16 (Rundgang-App und Builder)

Stand 02.11.2026. Geprüft: `pakete/PAKET_12_16_APP.md`, `pakete/builder/PAKET_12_16_BUILDER.md`. Endstand App aus `baukasten.PAKETE` (Export `2026-10-27_0909`, Kette 1–10, 12, 16), Builder Vorher `arbeit/2026-11-02_Paket8/builder_nach_p9.json`, Nachher `arbeit/2026-10-30_Builder/bloecke.json`. Kennzeichnung: **belegt** (aus Formeln/Generator), **geschlussfolgert**, **UNSICHER** (Laufzeitverhalten von Studio, nicht getestet).

## Kurzurteil

Kein hoher Befund. 1 mittlerer Befund (Ablauf „Zahl tippen → direkt ‚nicht messbar‘“ kann eine unsichtbare Rückfrage/Kritisch-Sperre hinterlassen), 7 niedrige (Anzeige/Textbreiten, Nur-Ansicht-Fallback, Texte mit festem „n.i.O.“, MaxLength, fachliche Hinweise, Tests). Logik von „nicht messbar“ in `fnFehltGrund`/`fnKommentarNoetig`/Speichern/Abschluss/Protokoll ist schlüssig. Dokumente sind vollständig und zeichengleich mit dem Generator.

## Befunde

### M1 (mittel, UNSICHER zur Ereignisreihenfolge) – Rückfrage-/Kritisch-Variable bleibt nach „nicht messbar“ stehen, Speichern blockiert ohne sichtbares Fenster

**Stelle:** `btnKaNM.OnSelect` (neu), Zusammenspiel mit `txtKaZahl.OnChange`, `conKaRueck.Visible`/`conKaKrit.Visible`, `btnKaSpeichern.OnSelect` (Paket 9).

**Ablauf:** Zahl-Prüfpunkt mit `NichtMessbar` = Ja und Rückfrage (oder Kritisch), Grenzmodus Mangel. Prüfer tippt einen Wert außerhalb des Sollbereichs ins Feld und tippt **ohne das Feld zu verlassen** direkt auf „nicht messbar“ (das liegt nahe: der Wert ist offensichtlich unsinnig, die Anlage ist aus).
1. Beim Verlassen des Felds feuert `txtKaZahl.OnChange`: `Bewertung = "NIO"` → `Set(varRueckPP, …)` bzw. `Set(varKritPP, …)`.
2. Danach `btnKaNM.OnSelect`: `Bewertung: ""`. `varRueckPP`/`varKritPP` werden **nicht** zurückgesetzt (belegt).
3. `conKaRueck.Visible`/`conKaKrit.Visible` verlangen `Bewertung = "NIO"` → Fenster verschwindet.
4. `btnKaSpeichern` prüft zuerst `varRueckPP > 0 || varKritPP > 0` → „Bitte zuerst die offene Frage im Fenster beantworten.“ – es ist aber kein Fenster da. Lösen lässt sich das nur, wenn man zufällig einen Wert im Sollbereich eintippt (der `OnChange`-Zweig setzt beide auf 0) oder die Kategorie neu öffnet (Eingaben weg, wenn nicht gespeichert).

UNSICHER: Ob der Tipp auf `btnKaNM` nach dem Erscheinen des Fensters (mit `btnKaRueckSperre`) noch beim Knopf ankommt, hängt von Studio ab. Kommt er an, tritt der Fehler auf. Die umgekehrte Reihenfolge (OnSelect vor OnChange) würde „nicht messbar“ sofort wieder mit der Zahl überschreiben – ebenfalls ungetestet.

**Korrektur:** im Setzen-Zweig von `btnKaNM.OnSelect` beide Variablen leeren (die Fenster sind modal, ein Tipp auf `btnKaNM` bei offenem Fenster einer anderen Frage ist nicht möglich, das Leeren ist also gefahrlos):
```
Patch(colAntworten, LookUp(…), {WertText: "nicht messbar", WertZahl: Blank(), Bewertung: "", KritischOk: false, KritischZeit: "", KritischVon: ""});
Set(varRueckPP, 0);
Set(varKritPP, 0);
Reset(txtKaZahl)
```
Zusätzlich (robuster, optional) in `btnKaSpeichern.OnSelect` die erste Bedingung an die Sichtbarkeit binden: `conKaRueck.Visible || conKaKrit.Visible` statt `varRueckPP > 0 || varKritPP > 0`. Test ergänzen (T8 unten).

### N1 (niedrig) – Textbreiten in der Karte: `lblKaZahlInfo` wird bei sichtbarem „nicht messbar“ zu schmal, „✓ nicht messbar“ knapp

**Stelle:** `lblKaZahlInfo.Width` (4.2), `btnKaNM.Width/Size` (4.3); Generator `baukasten.TEXTE` prüft `lblKaZahlInfo` nur mit 464 px.

**Ablauf:** Karte 720 px. Ist `NMErlaubt`, ist der Knopf **immer** sichtbar (auch wenn eine Zahl eingetragen ist) → `lblKaZahlInfo` 284 px (−10 Innenabstand = 274). Mit dem eigenen Prüftext des Generators „Betriebsstunden · Soll ab 1000 bis 99999 · außerhalb, bitte begründen“ (Size 14): ≈ 649 px (+10 %) → 3 Zeilen, Höhe 56 fasst 2 → genau der Handlungshinweis („bitte begründen“ / „unzulässig, bitte prüfen“) wird abgeschnitten. „✓ nicht messbar“ Size 14 in 164 px: Schätzung 160 px (+10 %) gegen 144 px nutzbar → nach der Generator-Regel ein Fehler (Umbruch in 2 Zeilen, passt in 56 px gerade noch).

**Korrektur:** `TEXTE` um beide Fälle ergänzen (274 px bzw. 164−20). Lösungsvorschlag: `btnKaNM.Size` 13 und `Width` 172 (`X: Parent.Width - 192`, `lblKaZahlInfo.Width: Parent.Width - 256 - If(btnKaNM.Visible, 188, 0)`), und für `lblKaZahlInfo` bei schmaler Breite `Size: If(btnKaNM.Visible, 12, 14)` oder die Einheit/Soll-Angabe kürzen. Alternativ den Knopf nur bei leerem Feld zeigen (`IsBlank(ThisItem.WertZahl)`), dann ist die Info mit „außerhalb …“ immer breit.

### N2 (niedrig) – Eigene Wörter bei langen/großen Texten und in der Builder-Vorschau abgeschnitten

**Stelle:** `btnKaIO/btnKaNIO.Width` (3.3/3.4), Builder `btnVsIO/btnVsNIO` (Width 120, unverändert), `txtPTextNIO.HintText`.

**Ablauf:** 18 Zeichen sind erlaubt. „nicht durchgeführt“ (Size 17) ≈ 199 px → passt in 250. In Großbuchstaben „NICHT DURCHGEFÜHRT“ ≈ 269 px > 230 px nutzbar → zweizeilig in 56 px, untere Zeile beschnitten. Builder-Vorschau: 120 px bei Size 14 → schon „nicht durchgeführt“ (≈ 164 px) bricht um und wird in 44 px Höhe beschnitten. Hinweistext „n.i.O. (z. B. nicht durchgeführt)“ Size 14 ≈ 272 px in 256 − 24 px → abgeschnitten.

**Korrektur:** App: `If(Max(Len(…)) > 12, 300, Max(…) > 8, 250, 160)` (Platz: 36 + 300 + 300 = 636 < 700, kein Konflikt mit `btnKaFoto`, der in der zweiten Zeile liegt – belegt). Builder-Vorschau: `btnVsIO.Width` wie in der App skaliert (z. B. `If(Max(Len(TextIO), Len(TextNIO)) > 8, 200, 120)`, `btnVsNIO.X = 24 + btnVsIO.Width`, vorher `conVsKarte`-Breite prüfen). HintText kürzen: „z. B. nicht durchgeführt“. Alle drei in die Textbreitenprüfung aufnehmen.

### N3 (niedrig) – Nur-Ansicht fällt bei alten Ergebnissen auf die **heutigen** Wörter des Prüfpunkts zurück, Protokoll nicht

**Stelle:** `scrKategorie.OnVisible`, Nur-Ansicht-Zweig: `TextIO: Coalesce(Text(a.TextIO), pp.TextIO, "")`.

**Ablauf:** Rundgang abgeschlossen vor Paket 12 (JSON ohne `TextIO`) oder gespeichert, als die Wörter leer waren (`"TextIO":""` – `Coalesce` überspringt auch `""`). Später trägt jemand im Builder „durchgeführt“ ein. Nur-Ansicht zeigt jetzt „durchgeführt“, `htmProtokoll` (liest nur das JSON) zeigt „i.O.“. Historische Ansicht und Protokoll widersprechen sich. Typen sind in Ordnung (Text/Text/Text, belegt).

**Korrektur:** `TextIO: Coalesce(Text(a.TextIO), "")`, `TextNIO: Coalesce(Text(a.TextNIO), "")` – wie im Waisen-Zweig und wie im Protokoll.

### N4 (niedrig) – Feste „n.i.O.“-Texte in Rückfrage, Kritisch-Fenster, Foto-Hinweis

**Stelle:** `lblKaRueckFrage.Text` („Ihre Antwort: n.i.O.“), `btnKaKritVersehen.Text` („n.i.O. war ein Versehen – Antwort zurücknehmen“), `lblKaFotoHinweis.Text` („Neue Fotos nur bei n.i.O. …“); `RG_Maengel.Wert` bleibt bei i.O./n.i.O.-Mängeln leer.

**Ablauf:** Legionellen-Prüfpunkt mit Rückfrage/Kritisch: Prüfer tippt „nicht durchgeführt“ → Fenster sagt „Ihre Antwort: n.i.O.“. Die Kurzfassung verspricht „Protokoll zeigt die eigenen Wörter“; in den Fenstern stimmt es nicht. Kein Logikfehler.

**Korrektur:** `lblKaRueckFrage`: `… If(r.Typ = "ZAHL", Text(r.WertZahl) & " " & r.Einheit, If(Trim(r.TextNIO) = "", "n.i.O.", r.TextNIO))`. `btnKaKritVersehen.Text`: `With({r: LookUp(colAntworten, PruefpunktID = varKritPP)}, If(r.Typ = "IONIO" && Trim(r.TextNIO) <> "", "„" & r.TextNIO & "“", "n.i.O.") & " war ein Versehen – Antwort zurücknehmen")`. Optional `Wert` im Mangel: `If(Text(n.Value.Typ) = "IONIO", Coalesce(Text(n.Value.TextNIO), ""), …)`.

### N5 (niedrig) – Builder: `txtPTextIO`/`txtPTextNIO` ohne `MaxLength`

**Stelle:** Builder 1a, `OnChange` speichert `Left(Trim(Self.Text), 18)`.

**Ablauf:** Eingabe mit 25 Zeichen, deren erste 18 dem gespeicherten Wert gleichen → Patch schreibt denselben Wert, `colP` unverändert → `Default` ändert sich nicht → Feld zeigt weiter 25 Zeichen, gespeichert sind 18. Auch sonst sieht der Bearbeiter erst nach dem Speichern, dass gekürzt wurde.

**Korrektur:** `MaxLength: =18` an beiden Feldern (Classic/TextInput kennt die Eigenschaft).

### N6 (niedrig, fachlich – an den Planer) – „nicht messbar“ umgeht Sperren und Kritisch

**Ablauf (belegt):** Prüfpunkt mit Grenzmodus „Sperren“ und `NichtMessbar` = Ja: unzulässiger Wert → nicht speicherbar → Prüfer tippt „nicht messbar“ + beliebige Begründung → speicherbar, kein Mangel. Kritischer Zahl-Prüfpunkt: statt Bescheid-Bestätigung „nicht messbar“ → kein rotes Fenster, kein Mangel. Das ist mit der Beschreibung („Kein Mangel“) vereinbar, aber nicht ausdrücklich entschieden.

**Vorschlag:** Entscheidung beim Planer/Josias einholen. Mindestens eine Builder-Prüfregel `Art: "Hinweis"` bei `NichtMessbar && (Grenzmodus = "Sperren" || Kritisch)` („‚nicht messbar‘ hebt Sperre/Kritisch auf“).

### N7 (niedrig) – Abschalten von „nicht messbar“ im Builder

**Frage aus dem Auftrag:** Bleibt WertText „nicht messbar“ hängen? **Nein, nicht blockierend** (belegt): Bearbeiten-Zweig lädt `WertText` aus dem JSON, `NMErlaubt` = false, `btnKaNM.Visible` bleibt wegen `WertText = "nicht messbar"` sichtbar („✓ nicht messbar“) und lässt sich aufheben; danach verschwindet der Knopf. Bis dahin gilt die Frage als beantwortet (Kommentar Pflicht) und wird so gespeichert – der Prüfer wird nicht darauf hingewiesen, dass „nicht messbar“ nicht mehr erlaubt ist. Bei einer neuen Fassung entstehen neue Prüfpunkt-IDs, die alte Antwort wird ohnehin Waise (`Inaktiv`), dort spielt es keine Rolle.
**Optional:** im Bearbeiten-Zweig `WertText: If(IsBlank(alt), "", p.Eingabetyp.Value = "ZAHL" && !Coalesce(p.NichtMessbar, false) && Text(alt.Value.WertText) = "nicht messbar", "", Coalesce(Text(alt.Value.WertText), ""))`.

### N8 (niedrig) – Tests decken nicht alle neuen Wege ab; `btnPNM` ist ein Umschalter

**App-Test fehlt:** (T8) Wert außerhalb mit Rückfrage tippen, ohne Feld zu verlassen „nicht messbar“ tippen → kein Fenster, Speichern möglich (siehe M1); (T9) „✓ nicht messbar“ erneut tippen → aufgehoben, „Noch offen … (Wert)“ bei Pflicht; (T10) abgeschlossenen Rundgang öffnen (Nur-Ansicht) → eigene Wörter und „✓ nicht messbar“ grau, nicht tippbar; (T11) Folgefrage mit Bedingung „*“ an einer Zahl → erscheint bei „nicht messbar“; Bedingung „n.i.O.“ an einer i.O./n.i.O.-Frage mit eigenen Wörtern → erscheint bei „nicht durchgeführt“.
**Builder-Test fehlt:** „Mehrere Fragen“ anlegen, Kopie einer Kategorie in neue Fassung (Wörter/„erlaubt“ übernommen), Prüfung zeigt Hinweis bei Zahl-Prüfpunkt mit Wörtern.
**`btnPNM.OnSelect`:** schreibt `!aktueller Wert` (Umschalter, nicht Zielwert wie `btnPKomm`); ein Doppeltippen schaltet zweimal und landet wieder beim Ausgangswert (sichtbar, kein Datenschaden). Das äußere `If(varSchreibbar && varAuswahlEbene = 3, …)` ist doppelt verschachtelt (wirkungslos).

## Geprüft, ohne Befund

- **App.Formulas:** `fnFehltGrund` (`ZAHL && IsBlank(wz) && wt = ""`) und `fnKommentarNoetig` (`ZAHL && wt = "nicht messbar"`) schlüssig; Kommentar-Pflicht unabhängig von `Pflicht`; Foto „Bei Mangel“ und „Kritisch“ greifen nicht (Bewertung leer). Keine Kommentare in Formeln.
- **`txtKaZahl`:** `OnChange` setzt `WertText: ""` → Zahl hebt „nicht messbar“ auf; `Default` leer nach `Reset` (WertZahl leer); `Reset` liegt im selben Galerie-Element.
- **Bedingungen:** `fnBedPasst`/`fnSichtbar` – Werte „io“/„nio“ vergleichen weiter `Bewertung` (intern IO/NIO), eigene Wörter wirken nicht auf Bedingungen; „*“ zählt „nicht messbar“ als beantwortet (plausibel).
- **Grenzmodus:** Warnen → `Warnung` false (WertZahl leer), „Bereich“ greift nicht. `UpdateIf … Kommentar leeren` behält die Begründung (fnKommentarNoetig true); nach Aufheben wird sie korrekt geleert.
- **Abschluss/Mängel:** nur `Bewertung = "NIO"` → „nicht messbar“ erzeugt keinen Mangel, `AnzahlNIO` und `colMaengelSoll` bleiben deckungsgleich.
- **Protokoll:** Wort-Spalte mit `Coalesce(If(…= ""; Blank(); …); "i.O.")` richtig für alte JSON ohne `TextIO`; „nicht messbar“ erscheint über `WertText`, Begründung darunter.
- **colAntworten:** alle drei Zweige von `scrKategorie.OnVisible` haben dieselben 37 Felder (maschinell abgeglichen), Typen passend (`TextIO`/`TextNIO` Text, `NMErlaubt` Boolean). `ShowColumns` im Speichern enthält `TextIO`, `TextNIO`.
- **Kartenlayout (720 px):** i.O./n.i.O.-Zeile 20–270 / 286–536, keine Überschneidung mit `btnKaFoto` (zweite Zeile) und `btnKaBild` (Y 10). Zahl-Zeile 20–220 / 236–520 / 536–700. `btnKaNM.Y` als Formel (E-05-Hinweis vorhanden).
- **Builder-Layout `conEdP` (648):** IONIO 232–292 → Rest 296–546, `btnPNio` 552–584; ZAHL Rest 360–610, `btnPNio` 616–648 (genau bündig); AUSWAHL/MEHRFACH 638; übrige 520. `lblPNM`/`btnPNM` (416–528) überlappen `txtPMax` (284–404) und `lblPGrenz` (Y 62) nicht.
- **Reset-Vollständigkeit:** alle 9 Stellen, die `varAuswahlID` setzen (außer App.OnStart), setzen `txtPTextIO`/`txtPTextNIO` zurück (maschinell). `btnPNM` braucht keinen Reset.
- **Datenvertrag Builder:** Kopie in `tmrArbeit` (`TextIO`, `TextNIO`, `NichtMessbar`), `btnGlNeuP`, `btnMehrAnlegen`, Änderungsliste `galAkt` (alle drei Felder). `btnLiVorlagen` nutzt Spalten-Standard (leer/Nein, über `Coalesce` abgefangen). Prüfregel in `galPr` ist `Art: "Hinweis"` (blockiert Aktivieren nicht).
- **Dokumente:** App 11 Properties + 1 Steuerelement, Builder 18 Properties + 7 Steuerelemente (89 Properties), jede genau einmal. Alle deutschen Blöcke und Vorher-Fassungen rückübersetzt zeichengleich (ohne Leerraum) mit Generator-Stand bzw. `builder_nach_p9.json`; YAML-Blöcke (25 bzw. 89 Properties) identisch. „Wo hin“ bei YAML vorhanden (Galerie: Kind der Vorlage markieren; Builder: `conEdP`/`conPZahl`). Rückweg mit Reihenfolge (erst Vorher-Fassungen, dann löschen) korrekt.

## Einarbeitung (Engineering-Chat, 02.11.)
- M1: `btnKaNM.OnSelect` setzt `varRueckPP`/`varKritPP` auf 0 (Test T8).
- N1: `btnKaNM` 120 px (Text bricht zweizeilig um), `lblKaZahlInfo.Width` −136, `lblKaZahlInfo.Size` 12 solange der Knopf da ist.
- N2: App-Knöpfe 260 px und Größe 14 ab 13 Zeichen; Builder-Vorschau 200 px bei langen Wörtern; HintTexte gekürzt.
- N3: Nur-Ansicht ohne Rückgriff auf die heutigen Wörter.
- N4: Rückfrage-Fenster und „… war ein Versehen“ mit eigenem Wort (Foto-Hinweis unverändert, sagt „Mangel“).
- N5: `MaxLength` 18.
- N6: als Frage an den Planer im Dokument. N7: dokumentiert.
- N8: Tests T8/T9 und Builder-Test 2/2b; `btnPNM` mit 1-s-Sperre.
Danach: Generatoren 0 Fehler, Mutation 12/12 und 13/13, Logik 91.
