# Prüfergebnis Paket 1 (Foto) und Paket 2 (Kommentar)

Prüfer: unabhängige Prüfung, nur lesend. Grundlage: `export/*.pa.yaml` (27.10.2026 09:09), `export/SPALTEN.md`, `pakete/PAKET_1_Foto.md`, `pakete/PAKET_2_Kommentar.md`. Die Pakete 3 bis 6 habe ich nur als Kontext gelesen.
Kennzeichnung: **belegt** (aus Export oder Paket nachgewiesen), **geschlussfolgert**, **UNSICHER**.

## Kurzfassung

- In beiden Paketen habe ich **keinen Syntax-, Namens-, Typ- oder Schemafehler** gefunden. Rückübersetzung, Klammern, Funktionsköpfe und Schema habe ich maschinell geprüft. Kein hoher Befund.
- Alle Vorher-Fassungen sind **zeichengleich**: in Paket 1 mit dem Export (ohne Kommentare), in Paket 2 mit dem Stand nach Paket 1 bzw. mit dem Export. Die Kette bis Paket 3 passt ebenfalls.
- Die Mängel liegen vor allem im **Testbogen** (zwei Erwartungen sind in der App nicht sichtbar, Vorbedingungen fehlen) und in **Kleinigkeiten der Dokumentation**. Dazu kommt eine fachliche Frage zur Foto-Pflicht.

## Maschinell geprüft (ohne Befund)

1. **Rückübersetzung DE→EN** (`;;`→`;`, `;`→`,` außerhalb von Texten) gegen den Export, Leerraum und Kommentare entfernt:
   - Paket 1: alle 24 Vorher-Blöcke sind zeichengleich. `imgKaFotoNeu.Y` fehlt im Export, ist also wirklich „(Standard) 0“.
   - Paket 2: `txtKaKommentar.HintText`, `.AccessibleLabel` und `htmProtokoll.HtmlText` sind vorher zeichengleich mit dem Export. `App.Formulas` und `scrKategorie.OnVisible` vorher sind identisch mit den Neu-Blöcken aus Paket 1.
   - Die Vorher-Fassungen von Paket 3 passen auf den Stand nach Paket 2 (Kette geschlossen).
2. **Abweichung neu ↔ vorher** zeilenweise: Es ändert sich nur, was beschrieben ist. Einzige Ausnahmen sind die undokumentierte Änderung in Befund 9 und der Zusatz `!Uebernommen` in `btnKaFoto.Text`. Letzterer behebt eine Doppelzählung nach einem Speichern, das nach dem Upload scheiterte (die Kurzfassung erwähnt ihn nicht, siehe Befund 10).
3. **Klammern** `()[]{}` (Texte ausgeblendet): Alle 30 Neu-Blöcke und alle Vorher-Blöcke sind ausgeglichen.
4. **Anzahl der Werte jedes UDF-Aufrufs** gegen die Köpfe: fnZahlBewertung 4, fnFehlt und fnFehltGrund 12, fnKommentarNoetig 8, fnFotoNeuErlaubt 2, fnFotoModus 2, fnLinkAnzahl 1, fnBeantwortet 3. **Keine Abweichung.** Außerhalb von Paket 1 ruft im ganzen Export niemand `fnFehlt` oder `fnZahlBewertung` auf (nur fnTagAnzeige, fnHtml, fnDateiname, fnArchivOrdner, fnSpUrl, fnTagLabel, fnPlanPasst, alle unverändert). Die geänderten Köpfe brechen also nichts.
5. **Schema von `colAntworten`**: In allen drei Zweigen von `scrKategorie.OnVisible` (Nur-Ansicht, Bearbeiten, inaktive Punkte) stehen dieselben 19 Felder in derselben Reihenfolge, in Paket 1 und in Paket 2: PruefpunktID, Frage, Typ, Pflicht, Einheit, MinWert, MaxWert, Auswahl, Hinweis, Reihenfolge, Bewertung, WertText, WertZahl, Kommentar, Fotos, FotoModus, KommentarPflicht, Grenzmodus, Inaktiv. Die Typen sind gleich (Text bzw. Boolean bzw. Number). `MinWert: Blank()` im Inaktiv-Zweig war schon vorher so. **belegt**
6. **Namen und Spalten**: Alle Steuerelemente stehen im Export. Die Felder `colFotos.Uebernommen/Url/Nr` und `colAntworten.*` gibt es. Die Spalten `Foto` (Auswahl → `.Value`) und `KommentarPflicht` (Ja/Nein → `Coalesce(…; false)`) werden in den Schritten 1.2 bzw. 2.2 angelegt, danach ist „Daten aktualisieren“ vorgeschrieben. `FotoMoeglich` wird nur noch in `OnVisible` gelesen (über `p.`/`pp.`), sonst nirgends im Export. `LookUp(colPP; …).FotoMoeglich` ist an allen 5 Stellen ersetzt. **belegt**
7. **Studio-Fallen**:
   - In keinem Block steht ein Kommentar.
   - Kein `Navigate` in OnVisible.
   - `Concat(… As z; z.Frage …)` in `lblKaFehlend` hat `As` richtig am äußeren Concat, nicht nur im inneren Filter.
   - Innere `Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)` lösen ohne Qualifizierung korrekt auf colFotos auf.
   - Der Flow-Aufruf `aRG_Foto_hochladen.Run({contentBytes: f.Bild; name: f.Datei}; f.Datei; ordner; varDurchID; f.PruefpunktID; durch.TestDatensatz)` ist zeichengleich mit dem Export.
   - Mehrarmige `If` mit Ketten (`;;`) sind in powerfxv1 = false zulässig.
   - Die UDF-Parameter sind deutsch mit `;` getrennt.
   - Keine Dezimalzahlen.
8. **Mängel beim Abschluss** (`btnRuAbschluss.OnSelect`): Mängel entstehen nur aus `Text(a.Value.Bewertung) = "NIO"`. Der Abgleich `Sum(AnzahlNIO)` gegen `colMaengelSoll` zählt in beiden Fällen inaktive n.i.O.-Zeilen mit. i.O.-Kommentare aus Paket 2 erzeugen also **keine** Mängel, und die Zählung bleibt stimmig. **belegt**
9. **Nachlese**: `ShowColumns(colAntworten; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos)` ist unverändert. Die neuen Felder landen nicht im JSON, der Vergleich `varNachlese.Antworten = varAntwortJSON` gilt weiter. Alte JSONs (ohne neue Felder) lesen sich unverändert, weil FotoModus und KommentarPflicht aus den Stammdaten kommen. **belegt**
10. **Layout** im Foto-Fenster und auf der Karte:
    - ✕ (Y 8, Standardhöhe 40) endet über dem Bild (Y 52).
    - Bild 52 + (200 − 60) = 192 < 200.
    - addKaFoto 96–160, Hinweis 56–84, Galerie ab 176: keine Überlappung.
    - Kommentarfeld endet bei Breite − 176, der Foto-Knopf beginnt bei Breite − 164.
    - Kartenhöhe und `btnKaFoto.Y` passen zusammen (Knopfende 54 + h + 124, Karte 54 + h + 144).
    - `conKaKarte.Height` liest `txtKaKommentar.Visible`/`btnKaFoto.Visible` der eigenen Kinder. Das ist kein Kreisbezug, weil deren Visible nur von ThisItem abhängt.
    - `lblKaAbstand.Y` stimmt jetzt auch im Fall „nur Foto“. Vorher fehlten dort 64 px, das war ein bestehender Fehler.

## Befunde

| Nr | Paket | Schwere | Property / Stelle | Fehlerszenario | Vorschlag | Beleg |
|---|---|---|---|---|---|---|
| 1 | P1 + P2 | mittel | Testbogen B6 („PX ohne Kommentar“), T2.9 („PM ohne Kommentar“) | Nach dem erneuten Öffnen ist PX bzw. PM i.O. `txtKaKommentar.Visible` ist dann im Bearbeiten-Modus `fnKommentarNoetig(…)` = falsch, das Feld ist also **immer** ausgeblendet, ob ein Kommentar drinsteht oder nicht. Die Erwartung lässt sich in der App nicht beobachten. Der Prüfer hakt sie blind ab oder schaltet auf n.i.O. um und verändert damit Daten. | Erwartung ändern: „Kommentar in `RG_KategorieErgebnisse.Antworten` (Zeile `D<id>-K<kat>`) für PX/PM leer“ oder im Protokoll nach dem Abschluss (B7/T2.10) „kein Kommentar bei PX/PM“. Alternativ ein Testschritt: n.i.O. tippen → Feld leer → wieder i.O. → Zurück, verwerfen. | belegt (`txtKaKommentar.Visible` P1) |
| 2 | P1 | niedrig | Testbogen A1 (Vorbedingung) | `galRuKategorien` sperrt jede ungespeicherte Kategorie außer der ersten offenen („gesperrt“, `btnRuOeffnen.DisplayMode`). Liegt P10 nicht in der ersten Kategorie, lässt sich K1 in A1 nicht öffnen. Der Prüfer muss erst die Kategorien davor speichern, und davon steht nichts im Bogen. | Vorbedingung ergänzen: „K1 muss ‚Als Nächstes‘ oder schon erledigt sein. Sonst die Kategorien davor speichern.“ | belegt (`galRuKategorien.Items`, Zustand) |
| 3 | P2 | niedrig | Testbogen (Benennung K1/K2), T2.1, T2.8 | In Paket 1 ist **K1** die Kategorie mit P10, in Paket 2 offenbar die erste Kategorie („K2 = zweite Kategorie“, „K1 speichern → K2 öffnet sich“). Ist P10 nicht in der ersten Kategorie, ist der Bogen doppeldeutig. T2.8 „K3 öffnet sich“ gilt nur, wenn es eine ungespeicherte K3 gibt, sonst erscheint die Übersicht. | In Paket 2 eigene Namen verwenden (KA = erste offene Kategorie, KB = Kategorie mit PK/PN). Bei T2.8 „nächste offene Kategorie oder Übersicht“ schreiben. | belegt |
| 4 | P1 | niedrig | Schritt 1.6, „Prüfen nach dem Schritt“ | Verlangt wird „Karte eines Punkts mit Foto = Pflicht ist höher …“. Schritt 1.2 sagt aber ausdrücklich „Für den Test noch **nichts** umstellen“, also gibt es zu diesem Zeitpunkt keinen Pflicht-Punkt. Der Prüfschritt ist nicht ausführbar. | Ändern in „Karte von P10 (FotoMoeglich = Ja) zeigt rechts unten ‚📷 Foto‘ (blau)“. Den Pflicht-Fall in A2 belassen. | belegt |
| 5 | P1 | niedrig | Schritt 1.6/1.9 Prüfliste E-05 | Die Prüfung „steht als Formel da, nicht als Zahl“ erfasst `btnKaFoto.Y`, `conKaKarte.Height`, `lblKaAbstand.Y` und `imgKaFotoNeu.Height`. `addKaFoto.Visible` steht im Export ebenfalls als per YAML eingefügter Block (`\|+`, wie `btnKaFoto.Y`) und bekommt eine neue Formel, fehlt aber in der Liste. | `addKaFoto.Visible` (und vorsorglich `addKaFoto.Text/Height/Y`) in die Liste aufnehmen. | belegt (Export), Wirkung geschlussfolgert |
| 6 | P1 | niedrig | Testbogen, Hinweis „Vorschau schließen und neu starten“ | Die Stammdaten werden laut Paket „pro Sitzung zwischengespeichert“. In Studio bleibt die Sitzung beim Schließen der Vorschau bestehen, und `OnVisible` macht kein `Refresh(RG_Pruefpunkte)`. A2 kann deshalb noch den alten Foto-Wert zeigen und fälschlich als Fehler gelten. | Nach jeder Stammdaten-Änderung zusätzlich in Studio **Daten → RG_Pruefpunkte → … → Aktualisieren**. Oder die Vorschau in einem neuen Browser-Tab öffnen. | UNSICHER |
| 7 | P1 | niedrig | `App.Formulas` (`fnFehltGrund`), fachlich | Foto = Pflicht verlangt das Foto **auch dann, wenn der Punkt unbeantwortet ist und Pflicht = Nein**. Der Prüfer kann die Kategorie nicht speichern, obwohl er den (freiwilligen) Punkt nicht bewertet. Paket 2 wählt für die Kommentarpflicht dagegen „erst sobald beantwortet“. Die Regeln sind uneinheitlich. | Josias fragen. Variante „wie Kommentar“: `foto = "Pflicht" && fanz < 1 && (pflicht \|\| fnBeantwortet(bew; wt; wz))`. | geschlussfolgert (Fachfrage) |
| 8 | P1 | niedrig | Schritt 1.2 (Standardwert „Aus“) | Neue Prüfpunkte bekommen in SharePoint Foto = „Aus“. Wer im Listenformular weiter „FotoMoeglich“ ankreuzt (die Spalte bleibt sichtbar), merkt nicht, dass das keine Wirkung mehr hat. Die Rückfalllogik in `fnFotoModus` greift nur bei leerer Foto-Spalte. | Keinen Standardwert setzen, dann gilt bei neuen Zeilen weiter FotoMoeglich. Oder FotoMoeglich in der Listenansicht und im Formular ausblenden und in der Kurzanleitung vermerken. | geschlussfolgert |
| 9 | P1 | niedrig | `btnKaSpeichern.OnSelect` (UpdateIf) | Neu ist `UpdateIf(colAntworten; !Inaktiv && !fnKommentarNoetig(…); …)`, vorher `Bewertung <> "NIO"` für **alle** Zeilen. Kommentare inaktiver i.O.-Zeilen werden nicht mehr geleert. Das ist fachlich richtig und für Paket 2 nötig, im Text aber als „heute gleiches Ergebnis“ beschrieben. Der Unterschied betrifft nur Alt-JSON mit i.O.-Kommentar. | In Schritt 1.8 einen Satz ergänzen: „Antworten inaktiver Punkte bleiben unverändert (auch der Kommentar).“ | belegt |
| 10 | P1 | niedrig | Doku Schritt 1.3 / Kurzfassung | Die Liste der neuen Funktionen in 1.3 nennt `fnFotoNeuErlaubt` nicht (sie ist im Block enthalten). Dass `btnKaFoto.Text` jetzt nur noch nicht übernommene Fotos zählt (`!Uebernommen`), steht nirgends. Das behebt die bisherige Doppelzählung nach einem gescheiterten Speichern. | Beide Punkte in der Kurzfassung bzw. in Schritt 1.3/1.6 nennen. | belegt |
| 11 | P1 | niedrig | `btnKaFoto.Visible` / `btnKaSpeichern` (bestehend) | Ein Punkt mit Foto = Aus wird n.i.O., der Prüfer nimmt ein Foto auf und stellt den Punkt dann auf i.O. Der Foto-Knopf verschwindet. Beim Speichern wird das Foto nicht hochgeladen und mit `Clear(colFotos)` **still verworfen**. Paket 1 begründet das Ausblenden von `addKaFoto` gerade mit „sonst gingen sie still verloren“, dieser Weg bleibt aber offen. Das Verhalten war schon vorher so. | Optional: vor dem Upload `CountRows(Filter(colFotos; IsBlank(Url) && !fnFotoNeuErlaubt(…)))` > 0 → Hinweis „x Foto(s) werden verworfen (Punkt nicht mehr n.i.O.)“. Oder den Foto-Knopf zeigen, solange ungespeicherte Fotos da sind. | geschlussfolgert |
| 12 | P1 | niedrig | `lblKaFehlend.Text` | `fnFehltGrund` liefert nur den ersten Grund (Wert → Kommentar → Foto). Fehlen Kommentar und Foto, zeigt der Fuß nur „(Kommentar)“, nach dem Eintragen dann „(Foto)“. Zwei Anläufe statt einem. | Hinnehmbar. Wer es ändern will: Text aus beiden Prüfungen zusammensetzen („(Kommentar, Foto)“). | belegt |
| 13 | P1 + P2 | niedrig | Testbogen (Lücken) | Es fehlt ein Test für: (a) einen ZAHL-Punkt (`txtKaZahl.OnChange` und die Bewertung in `OnVisible` sind geändert, Rückfall bei Fehler wäre falsche n.i.O.-Bewertung), (b) Foto = **Aus** bei FotoMoeglich = Ja (ausdrücklicher Wert schlägt Altspalte), (c) die Nur-Ansicht eines Pflicht-Punkts ohne gespeichertes Foto (kein Knopf, kein Stern). In Paket 2 fehlt das **Aufräumen**: PK/PN zurück auf KommentarPflicht = Nein, PN zurück auf Pflicht = Ja, P10 Foto auf den Zielwert. | Drei kurze Zeilen in Teil A ergänzen, dazu eine Aufräumzeile in Paket 2. | belegt |
| 14 | P2 | niedrig | Betrieb `fnKommentarNoetig` / UpdateIf | Wird KommentarPflicht eines Punkts später wieder auf Nein gestellt, ist ein gespeicherter i.O.-Kommentar im Bearbeiten-Modus unsichtbar. Beim nächsten Speichern der Kategorie wird er **ohne Hinweis gelöscht**. Der Rückweg-Abschnitt erwähnt das nur für den Rückbau der App, nicht für das Umstellen der Spalte. | Im Betriebshandbuch vermerken: „KommentarPflicht nur bei neuen Rundgängen ausschalten. Gespeicherte i.O.-Kommentare gehen sonst beim erneuten Speichern verloren.“ | geschlussfolgert |
| 15 | P2 | niedrig | Schritt 2.2 vs. Test-Vorbereitung | Schritt 2.2 sagt „einen Punkt in Kategorie 2 → KommentarPflicht = Ja“. Der Test braucht aber zwei (PK und PN), und PN muss Pflicht = Nein haben. Dafür muss eventuell Pflicht an einem Stammdatenpunkt umgestellt werden, ohne dass ein Rückstellen beschrieben ist (siehe 13). | Schritt 2.2 an die Test-Vorbereitung angleichen. | belegt |
| 16 | P2 | niedrig | außerhalb der App (Mail) | Die Mail stellt nicht die App her (`MailGesendetAm` wird extern gesetzt). Baut der Mail-Flow seinen Text selbst aus `Antworten` (statt aus dem PDF), zeigt er i.O.-Kommentare womöglich rot bzw. als Mangel an. | Den Mail-Flow einmal ansehen. Hängt er nur das PDF an, ist alles in Ordnung. | UNSICHER |
| 17 | – | niedrig | Nebenbefund, außerhalb P1/P2: `btnPrArchivieren.OnSelect` | Die Formel patcht `ProtokollErstelltAm` in `RG_Durchfuehrungen`, diese Spalte fehlt aber in `SPALTEN.md`. Entweder ist SPALTEN.md unvollständig, oder die App hat schon jetzt einen Formelfehler. Dann ist „App-Prüfung → Formeln = 0“ (Schritte 1.10/2.7) aus einem fremden Grund nicht erreichbar. | Vor Paket 1 die App-Prüfung einmal ansehen und den Ausgangswert notieren. Die Spalte in SharePoint prüfen. | belegt (Export vs. SPALTEN.md) |

## Szenarien (gedanklich gegen die Blöcke durchgespielt, ohne weiteren Befund)

- **Neuer Punkt ohne Daten:** Bearbeiten-Zweig mit `alt` leer. FotoModus und KommentarPflicht kommen aus den Stammdaten. Bei Pflicht-Foto stehen der Stern und „(Foto)“ da.
- **Alter gespeicherter Punkt (JSON ohne neue Felder):** Es wird nichts aus dem JSON gelesen, was neu ist, also kein Fehler. Gespeicherte Links zählen über `fnLinkAnzahl` (leerer Text = 0).
- **Inaktiver Punkt:** FotoModus „Aus“, KommentarPflicht falsch. Er ist überall durch `!Inaktiv` ausgenommen (Zähler, Sprung, UpdateIf). Seine Antwort bleibt im JSON.
- **Rundgang abgeschlossen (Nur-Ansicht):**
  - Der Foto-Knopf erscheint nur bei gespeicherten Links.
  - `addKaFoto` ist aus, der Hinweis lautet „Gespeicherte Fotos (nur Ansicht).“
  - Das Kommentarfeld erscheint bei vorhandenem Kommentar oder n.i.O.
  - Eine Foto-Pflicht kann `lblKaFehlendAnzahl` zwar > 0 machen. Sichtbar wird das nicht: Fuß, Balken, Speichern-Knopf und die rote Karte (wegen `varZeigeFehlend` = falsch) sind in der Nur-Ansicht aus bzw. anders beschriftet.
- **Wechsel n.i.O. → i.O. → n.i.O.:** Kommentar und Fotos bleiben in der Sammlung erhalten. Geleert wird erst beim Speichern. Die Farben wechseln rot/blau (Ausnahme Foto = Aus, siehe Befund 11).
- **Kategorie zweimal speichern:** Beim zweiten Öffnen zählt der Link. Es gibt keinen erneuten Upload, weil `colFotoNeu` nur Fotos mit leerer `Url` nimmt. Die Prüfung von GespeichertAm ist unverändert.
- **Netzfehler beim Upload (Pflicht-Foto):** Es wird nicht gespeichert, die Meldung erscheint. Beim nächsten Tippen wird nur nachgeladen, was noch keine Url hat. Scheitert erst der Patch, steht der Link schon in `colAntworten.Fotos`. Die Pflicht ist dann erfüllt, und der Zähler zählt nicht doppelt (`!Uebernommen`).
- **Abbruch mitten im Speichern / zwei Prüfer:** Das Verhalten ist unverändert gegenüber dem Export (verwaiste Datei in RG_Fotos möglich, wie bisher). Die Konfliktprüfung über GespeichertAm ist unverändert.
- **Reihenfolge der Schritte:** Spalte anlegen → Daten aktualisieren → App.Formulas → Aufrufer. Zwischenfehler sind angekündigt. Den Rückweg (Steuerelemente zuerst, App.Formulas zuletzt) habe ich nachgeprüft, er führt in den Ausgangsstand.

## Anzahl je Schwere

- hoch: **0**
- mittel: **1** (Nr. 1)
- niedrig: **16** (Nr. 2–17, davon Nr. 17 ein Nebenbefund außerhalb von P1/P2)
