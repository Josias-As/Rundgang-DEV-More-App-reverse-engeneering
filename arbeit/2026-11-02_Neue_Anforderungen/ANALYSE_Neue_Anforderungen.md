# Analyse: Neue Anforderungen (Übergabe Planer-Chat 02.11.2026)

Quelle: `quellen/2026-11-02_Uebergabe_Planer/UEBERGABE_NEUE_ANFORDERUNGEN_2026-11-02.md`.
Grundlage Code: Export 27.10. 09:09 + Baukasten 1–7, wie sie der Generator erzeugt (`baukasten.py`, Endstand). Einen Export **nach** dem Einbau von 1–6 gibt es im Repo noch nicht.
Kennzeichnung: **belegt** (Code) · **geschlussfolgert** · **UNSICHER**.

## Kurzfassung

1. **L3 ist geklärt (belegt):** AUSWAHL/MEHRFACH/TEXT/DATUM schreiben nur `WertText` und nie eine `Bewertung`. Mängel entstehen beim Abschluss ausschließlich aus `Bewertung = "NIO"`, also aus i.O./n.i.O. und aus Zahlen außerhalb der Grenzen. Eine Auswahl wie „schlecht“ erzeugt **keinen** Mangel. Eigene Antwortwörter („durchgeführt“) gehen deshalb am besten über **Beschriftungen für den Zweiwert-Typ**, nicht über AUSWAHL.
2. **KW ist in unserer App schon richtig (belegt):** `fnTagAnzeige` und der Durchführungs-Datensatz rechnen mit `ISOWeekNum`. Der KW-Fehler steckt nur in MoreApp.
3. **Nummern kollidieren:** Unser **Paket 7 ist schon belegt** (Foto „Bei Mangel Pflicht“, gebaut 30.10., Einbau offen). Vorschlag: Die Pakete des Planer-Chats laufen ab **8** (Liste unten).
4. **Der Builder ist betroffen:** Jede neue Spalte an `RG_Pruefpunkte` muss auch im Builder bearbeitbar sein und beim Kopieren und bei neuen Fassungen mitkommen. Verweise auf andere Prüfpunkte (`VergleichPunkt`) müssen beim Kopieren **umgeschrieben** werden, so wie heute schon `BedingungPunkt`. Sonst zeigt eine neue Fassung auf Fragen der alten Fassung.
5. **„Bereich optional“ passt nur als Anzeige:** Der Builder hängt die Fassung an die Bereiche (`Fassung` + `Aktiv` je Bereich, von Josias am 02.11. bestätigt). Zu jedem Rundgang muss also mindestens ein Bereich bestehen bleiben. Er darf aber **ausgeblendet** werden. Das entspricht dem Vorschlag „Bereich ausblendbar“ des Planer-Chats. Bereiche in den Daten ganz wegzulassen ist nicht möglich.
6. **L5 (viele gleiche Blöcke) deckt der Builder schon weitgehend ab:** Er kann Bereiche, Kategorien und Prüfpunkte aus einem anderen Rundgang oder aus „Vorlagen (Builder)“ holen und mehrere Fragen auf einmal anlegen (eine pro Zeile, auch aus Excel kopiert). Ein Excel-Import vor dem Builder ist nicht nötig.

## 1. Belege zu den UNSICHER-Punkten der Übergabe

| Punkt | Ergebnis | Beleg |
|---|---|---|
| L3: legt AUSWAHL Mängel an? | **Nein.** | `ddKaAuswahl.OnChange`, `cboKaMehrfach.OnChange`, `txtKaText.OnChange` und `dpKaDatum.OnChange` schreiben nur `WertText`. `Bewertung` setzen nur `btnKaIO`, `btnKaNIO` und `txtKaZahl` (über `fnZahlBewertung`). `btnRuAbschluss.OnSelect` baut `colMaengelSoll` aus `Bewertung = "NIO"`. |
| KW falsch? | Nur in MoreApp. | `ISOWeekNum(d)` in `fnTagAnzeige` (App.Formulas) und `KW: ISOWeekNum(varTag)` in `btnRgAktion.OnSelect` |
| Wo steht `User()`? (für die Prüferauswahl) | **5 Stellen** | `App.OnStart` (Admin-Prüfung über `cfgAdmins`), `btnRgAktion.OnSelect` (Durchführung: PrueferEmail/Name), `btnKaSpeichern.OnSelect` (KategorieErgebnis: PrueferEmail/Name), `btnRuAbschluss.OnSelect` (Mängel: `FestgestelltVon`), `lblStartNutzer.Text`. Den Prüfernamen lesen außerdem `htmProtokoll`, `scrRundgang.OnVisible` und `tmrWeiter` (Konfliktmeldung). |
| Admin bei geteiltem Konto | Mit einem geteilten Konto sind entweder alle Admin oder keiner. | `varIstAdmin` aus `cfgAdmins` gegen `User().Email`. Steuert `btnRuZuruecksetzen`. |

## 2. Auswirkungen je Anforderung

| # | Anforderung | Rundgang-App | Builder | Risiko / Hinweis |
|---|---|---|---|---|
| A | Prüferauswahl `RG_Pruefer` | 5 `User()`-Stellen durch `varPruefer` ersetzen, Startbildschirm mit Auswahl, Rückkehr nach Abschluss oder Inaktivität (Zeitgeber) | – | Die Admin-Frage gehört zu Michael/IT (geteiltes Konto). **Keine Konten selbst anfassen.** |
| B | Unterschrift | Stifteingabe beim Abschluss. Speichern als Bild-Text (`JSON(Pen.Image; JSONFormat.IncludeBinaryData)`) in einer neuen Spalte von `RG_Durchfuehrungen`, im Protokoll als `<img src="data:…">` | – | **UNSICHER:** die Größe des Bild-Texts in einer mehrzeiligen Textspalte. Ein Vorab-Test mit einer echten Unterschrift ist nötig. Ein Flow ist dafür nicht nötig. |
| C | Kopfdaten Kunde/Adresse | 2–3 Textspalten in `RG_Rundgaenge`, Protokollkopf. KW/Wochentag sind schon vorhanden (belegt). | Felder im Kopf des Editors (Rundgang-Ebene) | klein |
| D | Eigene Antwortwörter | Spalten `TextIO`/`TextNIO` an `RG_Pruefpunkte`. `btnKaIO.Text`/`btnKaNIO.Text` und das Protokoll zeigen sie an. „n.i.O.“ bleibt intern `NIO` und ergibt einen Mangel. | 2 Felder bei Typ i.O./n.i.O., Kopie und Fassungen | klein. Einfacher als eine AUSWAHL mit Mangelwert (siehe Kurzfassung 1). |
| E | **Abschnitt** | Textspalte `Abschnitt`. Überschrift in der Kartengalerie, wenn sich der Abschnitt ändert (Höhe der Galerievorlage über eine Zeile mit Höhe 0, wenn keine Überschrift). Protokoll ebenso. | Feld „Abschnitt“ beim Prüfpunkt, Gliederung zeigt den Abschnitt. Kopie, Fassungen und Änderungsliste. „Mehrere Fragen“ mit Abschnitt für alle. | **UNSICHER:** variable Höhe der Galerievorlage. Heute frieren Y/Height ein (E-05). Ein Vorab-Test ist nötig, oder alternativ eine eigene Überschrift-Karte als Pseudo-Prüfpunkt. |
| F | Bereich ausblendbar | `lblRuBereich` u. a. blenden aus, wenn `BereichAusblenden` gesetzt ist oder der Name leer ist | Schalter am Bereich. Ein neuer Rundgang legt einen ausgeblendeten Standard-Bereich an. | Passt zur Fassung an den Bereichen (Kurzfassung 5) |
| G | ⓘ-Fenster + `RG_Anleitungen` | neues Fenster auf `scrKategorie` (fast ganzer Bildschirm, scrollbares HTML/Label mit AutoHeight), Inhalt: Anleitung, Beispielbild (Paket 6), Hinweis, optionales Foto | Auswahl der Anleitung beim Prüfpunkt. Die Pflege der Anleitungen geht über SharePoint oder später einen eigenen Bildschirm. | Josias' Regel: Pflichtfoto und Foto bei n.i.O. bleiben in der Karte. |
| H | Abweichung zum letzten Lauf | `scrKategorie.OnVisible`: letzte abgeschlossene Nicht-Test-Durchführung desselben Rundgangs (`Filter` nach RundgangID + Status, `Sort` nach Datum, delegierbar) und deren `RG_KategorieErgebnisse` dieser Kategorie (JSON). Neue Bewertungsfunktion wie `fnZahlBewertung`. Anzeige „Letztes Mal …“. | 4 Felder bei Typ Zahl, Kopie und Fassungen | **Abgleich über die Prüfpunkt-ID:** Nach einer neuen Fassung haben die Prüfpunkte **neue IDs**. Der Vergleich muss deshalb über `QuelleID` (Builder) zurückgehen, sonst fehlt der Vergleich nach jeder Änderung. Das gilt auch für B/E nicht, nur hier. |
| I | Zwei Werte vergleichen | Feld `VergleichPunkt` in derselben Kategorie, Bewertung beim Eingeben | Auswahl wie bei der Bedingung (nur Zahlen derselben Kategorie). **Beim Kopieren umschreiben** wie `BedingungPunkt`. Prüfregel im Builder: Ziel existiert, ist eine Zahl, liegt in derselben Kategorie. | Mittel. Muss zusammen mit dem Builder gebaut werden. |
| J | Zugangsdaten | eigene Liste, 🔑 erst auf Antippen, nie ins Protokoll | Auswahl beim Prüfpunkt | **Offen bei Josias:** Bedien-PIN oder sensibler Zugang? Für sensible Zugänge nicht SharePoint. |
| K | Archiv-Bildschirm | neuer Bildschirm, Filter zuerst nach Datum (Delegation), Nur-Ansicht vorhanden | – | mittel |
| L | „nicht messbar“ | Haken an der Zahl → `WertText "n. m."`, `WertZahl` leer, keine Bewertung. Ob das als beantwortet zählt, entscheidet `fnFehlt`. | Schalter „darf nicht messbar sein“ | klein bis mittel |

## 3. Regeln für jede neue Prüfpunkt-Spalte (aus dem Builder-Datenvertrag)

Jede neue Spalte an `RG_Pruefpunkte` braucht diese 6 Stellen, sonst geht sie mit der nächsten Fassung verloren:
1. SharePoint-Spalte, Daten aktualisieren (in **beiden** Apps)
2. Rundgang-App: lesen (Karte/Protokoll)
3. Builder: Feld im Editor (`conEdP`) + Vorschau
4. Builder: `tmrArbeit` Stufe `kopie`: Feld im Patch (Kopie, neue Fassung, Vorlage holen)
5. Builder: `btnMehrAnlegen` / `neu_eintrag` mit Standardwert (die Datensatz-Literale müssen in allen Zweigen gleich sein)
6. Builder: `galAkt` (Änderungsliste) + `galPr` (Prüfregeln)

Bei Verweisen auf Prüfpunkte kommt noch die Umschreibung in `colBedErg` dazu (beim Vergleich ein zweiter Durchlauf).

## 4. Vorgeschlagene Reihenfolge (Engineering-Sicht)

Der Planer-Chat entscheidet. Mein Vorschlag mit neuer Nummerierung:

| Paket | Inhalt | Builder-Anteil | Aufwand |
|---|---|---|---|
| 7 | Foto „Bei Mangel Pflicht“ (schon gebaut) | im Builder schon drin | – |
| 8 | Abschnitt + Bereich ausblendbar | ja | S–M (Vorab-Test Galeriehöhe) |
| 9 | Prüferauswahl, Unterschrift, Kopfdaten, Antwortwörter | Kopfdaten, Antwortwörter | M |
| 10 | ⓘ-Fenster + Anleitungen | Anleitung wählen | M |
| 11 | Abweichung zum letzten Lauf (über `QuelleID`) | 4 Felder | M |
| 12 | Vergleich zweier Punkte | Auswahl + Umschreibung | S–M |
| 13 | Zugangsdaten (nach Josias' Antwort) | Auswahl | S |
| 14 | Archiv-Bildschirm | – | M |

Begründung für **Abschnitt zuerst**: Die vier echten Rundgänge brauchen Abschnitte. Würde man sie ohne Abschnitte im Builder anlegen, müsste man sie danach umbauen. Die Prüferauswahl hängt dagegen an der Frage zum Konto bei IT/Michael.

## 5. Was ich vor dem Bauen brauche

1. **Frischer Export der Rundgang-App** nach dem Einbau von 1–6 (und 7, falls drin). Dafür vorher **veröffentlichen**, weil ein Export nur den veröffentlichten Stand enthält (belegt 02.11.). Neue Pakete setzen exakt auf diesem Stand auf.
2. Die **vier MoreApp-PDFs** ins Repo. Damit kann ich die abgeschnittenen Zeilen nachlesen und die Rundgänge als Liste vorbereiten (Raum → Abschnitt → Frage → Typ/Einheit/Grenze), die man im Builder per „Mehrere Fragen“ einfügt.
3. Antworten auf die offenen Fragen in §6 der Übergabe. Für das Bauen zählen vor allem: 4 (Büro 1. OG: Räume oder Abschnitte), 1 (Passwörter), 2 (PIN).

## 6. Antwort an den Planer-Chat (zum Weitergeben)

- L3 geklärt: AUSWAHL erzeugt nie einen Mangel (belegt). Für „durchgeführt“ Beschriftungen am i.O./n.i.O.-Typ (`TextIO`/`TextNIO`) nehmen.
- KW: In unserer App ist sie richtig (`ISOWeekNum`).
- Nummern: Paket 7 ist schon „Foto bei Mangel Pflicht“. Eure Pakete bitte ab 8 zählen (Tabelle §4).
- Bereich: Er bleibt in den Daten Pflicht (die Builder-Fassungen hängen daran) und wird nur ausblendbar. „Kategorie optional“ ist nicht nötig, wenn Abschnitte kommen.
- Abweichung zum letzten Lauf muss über `QuelleID` gehen, sonst bricht der Vergleich nach jeder neuen Fassung.
- Jede neue Prüfpunkt-Spalte gibt auch eine Änderung am Builder (§3). Ich baue beides zusammen.
- Vor dem nächsten Paket: Rundgang-App veröffentlichen und exportieren, PDFs hochladen.
