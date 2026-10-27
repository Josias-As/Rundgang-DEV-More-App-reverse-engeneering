# Prüfung Paket 1 (Foto) und Paket 2 (Kommentar) – unabhängige Durchsicht

Stand 27.10.2026. Grundlage: `export/*.pa.yaml` (Export 09:09), `export/SPALTEN.md`, `HINWEIS.md`. Es wurde nur gelesen. Die Prüfskripte liegen außerhalb des Prüfordners.

## Kurzfassung

- **Kein Code-Fehler mit Schwere hoch.** Syntax, Klammern, Argumentanzahl und Schema stimmen. Die Vorher-Fassungen sind zeichengleich, und die Blöcke ändern nur das, was beschrieben ist (geprüft per Skript, siehe Abschnitt „Maschinell geprüft“).
- Die Befunde betreffen vor allem die **Testbögen**: Ein Bogen setzt Testdaten voraus, sagt aber nicht, wie man sie bekommt. Einige Schritte lassen sich so nicht ausführen oder nicht beobachten.
- Dazu kommt ein schon vorhandener Weg, auf dem ein Foto still verloren geht und den Paket 1 als behoben darstellt. Außerdem zeigt „Noch offen“ immer nur den ersten Grund an.

## Maschinell geprüft (belegt)

| Prüfung | Ergebnis |
|---|---|
| P1: alle 24 Vorher-Blöcke gegen den Export (englisch → deutsch, ohne Kommentare) | 24/24 zeichengleich, `imgKaFotoNeu.Y` richtig als Standard 0 |
| P2: 5 Vorher-Blöcke gegen Export + P1 (`App.Formulas`, `OnVisible` = P1-Endfassung; 3 weitere = Export) | 5/5 zeichengleich |
| Diff Neu ↔ Vorher je Property | Nur die beschriebenen Änderungen. Kleine Abweichungen, die nicht beschrieben sind, stehen unter H2/H3 |
| Klammern/Anführungszeichen in allen 30 Blöcken | ok |
| Argumentanzahl jeder `fn…`-Aufruf in allen Screens (Stand nach P1 und nach P1+P2) | ok. `fnZahlBewertung` (4) und `fnFehlt` (12) haben alle Aufrufer ersetzt (`OnVisible`, `txtKaZahl`, `conKaKarte` ×2, `lblKaFehlend*` ×2, `btnKaSpeichern`). Auf anderen Screens gibt es keine Aufrufer |
| Schema `colAntworten` in allen 3 Zweigen | gleiche 19 Felder mit gleichen Typen (`FotoModus` Text, `KommentarPflicht` Boolean, `Grenzmodus` Text). Kein Verweis mehr auf `colAntworten.FotoMoeglich` und kein `LookUp(colPP…).FotoMoeglich` |
| Andere Stellen (scrRundgang Abschluss/Mängel, scrProtokoll, scrStart) | lesen nur das JSON (`Bewertung`, `Kommentar`, `Fotos`), JSON-Spalten unverändert. `lblKaUnter`, `lblKaStand`, `conKaBalkenWert` und `btnKaSpeichern.Text/Fill/Color` hängen an `lblKaFehlendAnzahl` und bleiben stimmig |
| Studio-Fallen | keine Kommentare in Verhaltensformeln, kein Navigate in OnVisible. `Concat(Filter(… As a; …) As z; z.…)` ist richtig benannt. Der Flow-Aufruf `aRG_Foto_hochladen.Run(…)` ist unverändert. Layout ohne Zirkelbezug (die Kinder von `conKaKarte` hängen nicht an `Parent.Height`) |

## Befunde

| Nr | Paket | Schwere | Stelle | Fehlerszenario | Vorschlag | Beleg |
|---|---|---|---|---|---|---|
| 1 | P1, P2 | **mittel** | Testbögen (P1 Teil A/B, B5, B7, Aufräumen; P2 T2.1, T2.10, Aufräumen) | `TestDatensatz` ist nur Ja, wenn der Rundgang-Titel mit „ZZ Test“ beginnt (`scrStart`: `TestDatensatz: StartsWith(ThisItem.Title; "ZZ Test")`). Die Bögen nennen nur K1 = „Kategorie mit Id 10“, aber nicht, dass K1 in einem „ZZ Test“-Rundgang liegen muss. Liegt Id 10 in einem echten Rundgang, dann: B5 erwartet den Ordner `TEST/2026/10/…`, das Foto liegt aber unter `2026/10/…`. „Aufräumen (nur TestDatensatz = Ja)“ erfasst nichts. B7 legt echte Mängel in RG_Maengel und ein echtes PDF an. Der Tagesschlüssel `R<id>-<Datum>` ist für den echten Rundgang des Tages belegt: Ein echter Prüfer setzt die Testdurchführung fort, oder der Test setzt seine fort. | Im Kopf beider Bögen festlegen: „K1 muss in einem Rundgang liegen, dessen Titel mit ‚ZZ Test‘ beginnt. Sonst einen Testrundgang anlegen bzw. Id 10 nicht verwenden.“ Die Prüfpunkte P10/PO/PX/PK/PN/PM in diesem Testrundgang wählen. | Mechanismus belegt. Ob Id 10 in einem echten Rundgang liegt: geschlussfolgert/unbekannt |
| 2 | P1 | niedrig | Test B6 → B6a | B6 erwartet „Speichern ohne neues Foto möglich“. Wer das durch Tippen prüft, speichert. Die App meldet „Gespeichert.“, setzt `varWeiter` und `tmrWeiter` öffnet die nächste offene Kategorie (K2). B6a („PX auf n.i.O. tippen“) setzt aber voraus, dass K1 noch offen ist. | B6: „Fuß zeigt ‚✓ Alles ausgefüllt‘, Knopf heißt ‚Speichern…‘ statt ‚Offene Punkte ↓‘ – **nicht** tippen.“ Oder B6a beginnt mit „Zurück, K1 erneut ‚Bearbeiten‘“. | belegt (`btnKaSpeichern`, `tmrWeiter.OnTimerEnd`) |
| 3 | P2 | niedrig | Test T2.5/T2.6 | Erwartet ist, dass der Hinweis zu „Kommentar zum Mangel (Pflicht)“ bzw. „Kommentar (Pflicht)“ wechselt und „sauber“ stehen bleibt. `HintText` erscheint aber nur in einem **leeren** Feld. Mit „sauber“ im Feld ist der Wechsel nicht zu sehen, der Schritt ist nicht prüfbar. | Den Wechsel in T2.2 (leeres Feld) prüfen, z. B. erst n.i.O. → Hinweis „…zum Mangel…“, dann i.O. → „Kommentar (Pflicht)“, danach „sauber“ eintragen. In T2.5/T2.6 nur noch „‚sauber‘ bleibt stehen, Feld sichtbar“ erwarten. | belegt (Verhalten von `HintText` bei TextInput) |
| 4 | P2 | niedrig | Test T2.1 | Pro Rundgang und Tag gibt es nur eine Durchführung (`varSchluessel = "R" & ID & "-" & varTagText`). Wer P1 am selben Tag mit B7 abgeschlossen und nicht aufgeräumt hat, kann weder neu starten (nur noch „Ansehen“) noch K1/K2 bearbeiten (Nur-Lesen). Der Test ist dann blockiert. Wer B7 ausgelassen hat, setzt die alte Durchführung fort, in der K1 schon gespeichert ist. Das geht, entspricht aber nicht „neu starten“. | Vorbedingung ergänzen: „Die P1-Testdurchführung vorher in den Papierkorb legen (Durchführung + KategorieErgebnisse) oder einen anderen ZZ-Test-Rundgang bzw. Nachholtag nehmen.“ | belegt (`scrStart` Start-Knopf) |
| 5 | P1 | niedrig | Test A10 | „K1 öffnen, Zurück (‚Verwerfen? Erneut tippen‘)“: Ohne Änderung ist `varGeaendert` false. `btnKaZurueck` navigiert dann sofort, ohne nachzufragen. Die Erwartung in Klammern tritt nicht ein und verunsichert den Tester. | Die Klammer streichen oder „(ohne Änderung kommt keine Rückfrage)“ schreiben. | belegt (`btnKaZurueck.OnSelect`) |
| 6 | P1 | niedrig | Schritt 1.6 „Prüfen nach dem Schritt“ | In Studio enthält `colAntworten` noch die Zeilen vom letzten Vorschau-Lauf. `FotoModus` ist dort leer, bis `OnVisible` erneut läuft. `btnKaFoto.Visible` (`FotoModus <> "Aus"` → leer ≠ „Aus“ = wahr) zeigt dann an **allen** Karten den Foto-Knopf, und alle Karten sind höher. Ist die Sammlung leer, ist die Galerie leer. In beiden Fällen lässt sich die Prüfung „Karte von Id 10 ist höher …“ so nicht vornehmen. | Diese Prüfung nach Schritt 1.9 bzw. in Test A1 verschieben (Vorschau, K1 neu öffnen). Bei 1.6 nur prüfen, dass `btnKaFoto.Y` eine Formel ist. | geschlussfolgert (Studio behält Sammlungen) |
| 7 | P1 | niedrig | `btnKaFoto.Visible`, Upload in `btnKaSpeichern` (vorhandener Weg) | Punkt mit Foto „Aus“: auf n.i.O. setzen, Foto aufnehmen, dann zurück auf i.O. Danach ist der Foto-Knopf unsichtbar (keine gespeicherten Links, nicht n.i.O., Modus Aus). Beim Speichern wird das Foto nicht hochgeladen (`fnFotoNeuErlaubt` = falsch), nach Erfolg folgt `Clear(colFotos)`. Das Foto ist still weg. Schritt 1.9 begründet `addKaFoto.Visible` gerade mit „sonst gingen sie still verloren“. Dieser Weg bleibt aber offen (war vorher genauso). | Entweder `btnKaFoto.Visible` um `CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) > 0` erweitern (Knopf bleibt sichtbar, Hinweis im Fenster „wird nicht gespeichert“), oder in der Übergabe als bekannte Grenze dokumentieren. | belegt (Codepfad) |
| 8 | P1 | niedrig | `lblKaFehlend.Text` / `fnFehltGrund` | `fnFehltGrund` liefert nur den **ersten** Grund (Wert → Kommentar → Foto). Ein n.i.O.-Punkt mit Foto „Pflicht“, ohne Kommentar und ohne Foto, erscheint als „… (Kommentar)“. Erst nach dem Kommentar erscheint „(Foto)“. Der Prüfer erfährt also erst beim zweiten Versuch, dass auch ein Foto fehlt. Bei der Wert-Lücke fehlt der Zusatz ganz. | Ist das gewollt, im Text erwähnen. Sonst den Zusatz zusammensetzen, z. B. `If(Kommentar fehlt; " (Kommentar)"; "") & If(Foto fehlt; " (Foto)"; "")`, und die Zählung über `fnFehlt` lassen. | belegt |

## Hinweise (keine Mängel, bitte bewusst entscheiden)

- **H1 – Uneinheitliche Pflicht-Regeln (P1 ↔ P2).** Foto „Pflicht“ greift immer, auch bei einem **unbeantworteten Nicht-Pflicht-Punkt** (`foto = "Pflicht" && fanz < 1` ohne `fnBeantwortet`). Ein solcher Punkt lässt sich also nicht überspringen. KommentarPflicht (P2) greift nur, wenn der Punkt beantwortet ist (T2.3). Wenn das so gewollt ist, gehört es in die Kurzfassung. Sonst: `foto = "Pflicht" && fanz < 1 && (pflicht || fnBeantwortet(bew; wt; wz))`.
- **H2 – Nicht beschriebene Verhaltensänderung in `btnKaSpeichern`.** „Kommentar leeren“ gilt jetzt nur noch für `!Inaktiv`. Bisher wurden auch die i.O.-Kommentare inaktiver Punkte geleert. Das passt zu „inaktive unverändert mitführen“ und ist eher eine Verbesserung. Die Aussage „heute gleiches Ergebnis“ stimmt aber nicht ganz.
- **H3 – Weitere nicht beschriebene Änderungen (unkritisch).** `btnKaFoto.Text` zählt nur noch `!Uebernommen`. Damit ist eine Doppelzählung nach einem gescheiterten Speichern behoben. `txtKaKommentar.Visible` zeigt in der Nur-Ansicht jetzt auch Kommentare bei i.O. (Grundlage für P2). In P1 steht dort bis P2 noch der Text „Kommentar zum Mangel: …“ (`AccessibleLabel`).
- **H4 – Flow.** `aRG_Foto_hochladen` bekommt jetzt auch Fotos von i.O.-Punkten (Optional/Pflicht). Aus dem Export lässt sich nicht prüfen, ob der Flow n.i.O. voraussetzt (z. B. Metadaten oder eine Zuordnung zum Mangel). Kurz in den Flow schauen.
- **H5 – Nachträglich gesetzte Foto-Pflicht.** Wird Foto = Pflicht erst nach dem Speichern einer Kategorie gesetzt, verlangt jedes spätere „Bearbeiten“ (auch nach „Zurück auf In Arbeit“) ein Foto, bevor gespeichert werden kann. Das ist wohl gewollt, sollte aber im Betriebshinweis stehen.
- **H6 – Standardwert „Aus“ der Spalte Foto.** Er ist als UNSICHER dokumentiert. Einfacher und ohne Risiko wäre **kein** Standardwert: Leer bedeutet ohnehin „wie bisher“, und neue Punkte werden ausdrücklich gesetzt. Dann entfällt die Prüfung, ob SharePoint vorhandene Zeilen füllt.

## Szenarien ohne Befund (geprüft)

- Neuer Punkt ohne Daten (`alt` leer): Felder richtig vorbelegt, `FotoModus`/`KommentarPflicht` kommen aus der Liste.
- Alter gespeicherter Punkt im Bearbeiten-Zweig: Fotos werden über `fnLinkAnzahl` gezählt und erfüllen die Pflicht (B6). Ein alter i.O.-Kommentar wird wie bisher geleert (ohne KommentarPflicht).
- Inaktiver Punkt: `FotoModus "Aus"`, `KommentarPflicht false`, ausgeblendet, zählt nicht, Kommentar bleibt erhalten.
- Nur-Lesen: Kein `*`, `addKaFoto` aus, Foto-Knopf nur bei gespeicherten Links, „Noch offen“ unsichtbar (`lblKaStand`/`lblKaUnter`/Balken zeigen „Nur Ansicht“).
- Wechsel n.i.O. → i.O. → n.i.O.: Kommentar und Fotos bleiben in der Sammlung, Anzeige und Pflicht folgen der Bewertung. Bei Optional/Pflicht werden die Fotos hochgeladen. Ausnahme siehe Befund 7.
- Zweimal speichern bzw. Netzfehler: Bei einem Teilfehler im Upload wird nichts übernommen und erneut versucht. Nach einem Patch-Fehler zählt die Pflicht über die angehängten Links (`Uebernommen` = wahr, ohne Doppelzählung). Nachlese unverändert.
- Abbruch im Speichern und zwei Prüfer gleichzeitig: Verhalten wie bisher (`GespeichertAm`-Abgleich vor dem Upload).
- Mängel beim Abschluss: weiterhin nur n.i.O. `AnzahlNIO` und `colMaengelSoll` bleiben stimmig, Fotos von i.O.-Punkten erscheinen nur im Protokoll.
- Layout: Kommentarfeld (X 20, Breite W − 196) und Foto-Knopf (X W − 164) liegen in einer Zeile, keine Überlappung mit `lblKaZahlInfo`. `lblKaAbstand.Y` = Kartenende (behebt die zu niedrige Zeile bei FotoMoeglich). ✕ (Y 8–48) liegt über dem Bild (Y 52).
- Rückweg P1/P2: Reihenfolge „Steuerelemente, dann App.Formulas“ erzeugt nur vorübergehend Fehler. Die JSON-Spalten sind unverändert. Die P2-Warnung zum Löschen der i.O.-Kommentare steht im Dokument.

## Anzahl je Schwere

- hoch: **0**
- mittel: **1** (Nr. 1)
- niedrig: **7** (Nr. 2–8)
- Hinweise: 6 (H1–H6)
