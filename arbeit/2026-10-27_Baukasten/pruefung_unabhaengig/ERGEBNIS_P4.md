# Prüfergebnis Paket 4 – Bedingte Fragen

Prüfer: unabhängiger Prüf-Agent, 27.10.2026. Grundlage: `export/*.pa.yaml` (Stand 08:24 + Zeile 08:44 laut HINWEIS.md), Blöcke aus Paket 1–3, `PAKET_4_Bedingung.md`.

## Kurzfassung

- **0 hoch, 3 mittel, 9 niedrig.** Ich habe keinen Syntax- oder Typfehler gefunden, der das Einfügen in Studio verhindert. Ich habe auch keinen Fehler gefunden, der Mängel oder die Plausibilitätsprüfung beim Abschluss verfälscht.
- Maschinell geprüft (belegt): Alle 10 Blöcke haben ausgeglichene Klammern (Zeichenketten ausgenommen). Alle 10 Vorher-Fassungen sind zeichengleich mit dem Stand Export + P1–P3: App.Formulas, OnVisible, lblKaFehlendAnzahl, lblKaFehlend, btnKaSpeichern und htmProtokoll gleichen den P1–P3-Blöcken, die übrigen 4 dem Export. Der Diff gegenüber dem Vorher-Stand enthält nur die angekündigten Änderungen.
- Hauptpunkte: (1) Beim Ausblenden bleiben die **Fotos** von B erhalten. Unter Umständen werden sogar neue Links an den ausgeblendeten Punkt gehängt. (2) Ein **BedingungWert, der nie passt**, blendet einen Pflichtpunkt dauerhaft und ohne Hinweis aus. Das widerspricht dem Versprechen „sicherer Ausfall“. (3) Der **Testbogen** ist in der angegebenen Reihenfolge nicht vollständig ausführbar.

## Befunde

### B1 – mittel – `btnKaSpeichern.OnSelect`: Fotos ausgeblendeter Punkte werden nicht geleert und können sogar nachträglich angehängt werden (belegt)

- `UpdateIf(colAntworten; PruefpunktID in colVersteckt.PruefpunktID; {Bewertung: ""; WertText: ""; WertZahl: Blank(); Kommentar: ""; Ausgeblendet: true}; …)` leert `Fotos` nicht. Gespeicherte Links von B bleiben im JSON, nur mit `Ausgeblendet: true`.
- Der Anhänge-Schritt `ForAll(Distinct(Filter(colFotos; !Uebernommen && !IsBlank(Url)); PruefpunktID) As d; Patch(colAntworten; …{Fotos: …}))` prüft nicht auf ausgeblendet.
- Szenario a: Versuch 1 lädt ein Foto für das sichtbare B hoch (Url gesetzt). Ein anderes Foto scheitert, die App meldet den Fehler und bricht ab. Der Prüfer setzt A auf i.O., B wird ausgeblendet. In Versuch 2 schließt `colFotoNeu` B zwar aus, der Anhänge-Schritt hängt den Link aus Versuch 1 aber an das geleerte B. Gespeichert wird ein ausgeblendeter Punkt mit Foto, die Datei liegt verwaist in RG_Fotos.
- Szenario b: Bei einer späteren Bearbeitung derselben Durchführung wird A wieder n.i.O. und B erscheint mit „📷 Foto (1)“. `fnLinkAnzahl(a.Fotos)` erfüllt dabei eine **Foto-Pflicht** mit einem alten Foto aus einem anderen Zustand. Das widerspricht T4.5 („Folgefrage leer“) und der Kurzfassung („leert die App ausgeblendete Punkte“).
- Vorschlag:
  - Im UpdateIf zusätzlich `Fotos: ""` setzen, wenn Josias das will. Sonst bewusst dokumentieren, dass Fotos stehen bleiben.
  - Den Anhänge-Filter auf `Filter(colFotos; !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID))` ändern.
  - Den Test um „Foto an B, A auf i.O., Speichern, wieder öffnen, A n.i.O.“ ergänzen.

### B2 – mittel – `App.Formulas` `fnBedPasst`/`fnSichtbar`: Ein falscher BedingungWert blendet einen Pflichtpunkt für immer und ohne Hinweis aus (belegt durch die Formel, Szenario geschlussfolgert)

- Der sichere Ausfall greift nur, wenn A fehlt, bei einer Kette oder bei leerem Wert.
- Werte, die nie passen, führen dagegen zu „nie sichtbar“: Tippfehler „NOI“, die Anzeigeform „n.i.O.“ oder „i.O.“, eine Liste „Rot;Gelb“, ein Wert, den es in A’s Auswahl nicht gibt, oder „NIO“ an einem Text-Punkt.
- B zählt dann nicht als offen, wird nie verlangt und taucht im Protokoll nicht auf. Für eine Pflicht-Folgefrage in einem Kontrollrundgang ist das der unsichere Ausfall.
- Vorschlag:
  - Gültigkeit beim Laden prüfen. Bei IONIO nur `IO`, `NIO` oder `*` zulassen. Bei AUSWAHL muss der Wert in `Split(A.Auswahl; ";")` (getrimmt, ohne Groß-/Kleinschreibung) vorkommen oder `*` sein. Bei TEXT/ZAHL nur `*`.
  - Passt der Wert nicht: wie bei einer Fehlkonfiguration B immer zeigen. Dazu z. B. ein zusätzlicher Parameter `bTyp`/`bAuswahl` an `fnSichtbar`.
  - Zusätzlich Aliase annehmen: „i.O.“ → IO, „n.i.O.“ → NIO.
  - Test „BedingungWert = n.i.O.“ ergänzen.

### B3 – mittel – Testbogen: Reihenfolge nicht ausführbar, Vorbedingungen fehlen (belegt durch App-Ablauf)

- **T4.7 → T4.8:** Für T4.7 muss der Rundgang abgeschlossen werden (`btnRuAbschluss`). Danach ist alles Nur-Ansicht (`varNurLesen`). Dort zählt nur das gespeicherte Flag, nicht BedingungWert. T4.8 („BedingungWert leeren → immer sichtbar“) prüft danach also nichts mehr. Zurücksetzen gibt es nur im Status „Abschluss“, nicht aus „Abgeschlossen“.
- **T4.7, zweiter Teil:** „bei ausgeblendeter Folgefrage fehlt die Zeile“ braucht eine zweite Durchführung, weil T4.6 B sichtbar gespeichert hat.
- **T4.1:** Ist Kategorie 1 schon mit A = n.i.O. gespeichert (frühere Tests), ist B beim Öffnen sichtbar und T4.1 schlägt fehl. Vorbedingung „A ist i.O. oder leer gespeichert“ fehlt.
- **T4.5:** Nach dem Speichern öffnet `tmrWeiter` automatisch die nächste offene Kategorie. Der Rückweg zu Kategorie 1 („‹ Kategorien“ → „Bearbeiten“) sollte im Test stehen.
- **T4.6:** Es fehlt, wo das JSON zu sehen ist (SharePoint `RG_KategorieErgebnisse` → Spalte `Antworten`).
- **Testdaten:** Der Prüfpunkt B braucht `Aktiv = Ja` und eine `RgReihenfolge` direkt nach A. Bei leerer oder kleinerer Reihenfolge erscheint B oberhalb von A, und die erwartete Lage „unter ihrer Reihenfolge“ ist unbestimmt. Für BedingungPunkt muss die ID-Spalte in der Listenansicht eingeblendet sein.
- **Fehlende Fälle:** Nur-Ansicht mit ausgeblendetem B. RG_Maengel ohne Eintrag für ausgeblendetes B, Plausibilität ohne Fehlermeldung. Foto an B, dann B ausgeblendet → kein Upload. A in anderer Kategorie oder Kette → B sichtbar. Fall B2.
- Vorschlag: Testbogen als Zeitachse mit zwei Durchführungen schreiben (D-a: T4.1–T4.6 und T4.8, alles „in Arbeit“; D-b: einmal B sichtbar, einmal ausgeblendet speichern, dann Abschluss und T4.7). Vorbedingungen ausdrücklich nennen.

### B4 – niedrig – `btnKaSpeichern.OnSelect`: Geleert wird vor dem Upload, bei Abbruch ist B’s Eingabe in der Sitzung verloren (belegt)

- Das Leeren läuft vor dem Foto-Upload und vor der Prüfung „Foto(s) konnten nicht hochgeladen werden“, ebenso vor Patch und Nachlese.
- Schlägt etwas davon fehl, bleibt der Prüfer auf der Seite und B ist im Speicher schon geleert. Wechselt er A zurück auf n.i.O., erscheint B leer. Das Verhalten aus T4.4 („kommt mit der Antwort zurück“) gilt nach einem fehlgeschlagenen Speicherversuch nicht mehr.
- Vorher (P1–P3) lag das Leeren des Kommentars erst im Erfolgszweig nach dem Upload.
- Vorschlag: Nur `colVersteckt` vor dem Upload bilden. Die Upload- und Zählfilter mit `!(f0.PruefpunktID in colVersteckt.PruefpunktID)` statt `!a.Ausgeblendet` schreiben. Das `UpdateIf(colAntworten; … Ausgeblendet …)` in den Erfolgszweig direkt vor das Kommentar-UpdateIf legen. Nachteil: Ein fehlgeschlagener Patch lässt die Flags ungesetzt, das ist harmlos, weil sie beim nächsten Versuch neu berechnet werden.

### B5 – niedrig – `btnKaSpeichern.OnSelect`: Neue Fotos eines ausgeblendeten Punkts werden ohne Hinweis verworfen (belegt)

- Fotos in `colFotos` für B werden nicht hochgeladen. Nach dem Erfolg löscht `Clear(colFotos)` sie, ohne Meldung.
- Wer erst fotografiert und dann A ändert, verliert die Aufnahme unbemerkt.
- Vorschlag: In der Erfolgsmeldung die Zahl nennen, z. B. `CountRows(Filter(colFotos; IsBlank(Url) && PruefpunktID in colVersteckt.PruefpunktID))` → „x Foto(s) ausgeblendeter Punkte nicht gespeichert“. Alternativ die Zahl vor dem Speichern im Fuß zeigen.

### B6 – niedrig – `fnSichtbar`: Die Kettenerkennung ist zu grob (belegt)

- `bBid <> 0` wertet A schon als „bedingt“, wenn bei A nur BedingungPunkt gesetzt ist. Das gilt auch bei leerem BedingungWert oder wenn A’s eigener Bezugspunkt fehlt, obwohl A dann immer sichtbar ist.
- B wird dann immer gezeigt, obwohl seine Bedingung auswertbar wäre. Das ist kein Sicherheitsproblem, aber eine überraschende Konfiguration.
- Vorschlag: Kette nur bei `b.BedID <> 0 && Trim(b.BedWert) <> ""` annehmen. Oder in der Doku sagen: „Bei A BedingungPunkt = 0 lassen.“

### B7 – niedrig – Bedeutung von IO/NIO bei Zahl-Punkten mit Grenzmodus (belegt, Doku)

- Bei Grenzmodus **Warnen** ergibt ein Wert außerhalb `Bewertung = "IO"`. BedingungWert „NIO“ greift also nicht, „IO“ greift innerhalb **und** außerhalb des Bereichs.
- Bei **Sperren** außerhalb ist `Bewertung = ""`. Nur „*“ greift.
- Vorschlag: In der Doku festhalten. Wenn gewünscht, eigene Werte wie „AUSSERHALB“ über `fnAusserhalb` in `fnBedPasst` unterstützen. Dazu bräuchte es Min/Max von A als Parameter.

### B8 – niedrig – Stammdaten-Änderungen mitten im Rundgang (geschlussfolgert)

- Wird A deaktiviert (Aktiv = Nein), ist B (oft Pflicht) ab dann in jedem Rundgang immer sichtbar und Pflicht. Das ist so gewollt („sicherer Ausfall“), muss aber im Betriebshandbuch stehen.
- Wird ein Punkt nachträglich bedingt, während der Rundgang in Arbeit ist, leert das nächste Speichern der Kategorie B’s gespeicherte Antwort. Bei einem gespeicherten **n.i.O.** verschwindet damit der künftige Mangel, ohne Hinweis.
- Vorschlag: Regel für Admins „Bedingungen nur ändern, wenn kein Rundgang in Arbeit ist“. Wenn gewünscht, im Speichern einen Hinweis, wenn `colVersteckt` einen Punkt mit gespeichertem `Bewertung = "NIO"` enthält.

### B9 – niedrig – Leistung und Wartung: Die Sichtbarkeitsregel steht zehnmal da (belegt)

- Derselbe Filter mit `LookUp` je Zeile (n²) steht in galKaPruefpunkte.Items, lblKaFehlendAnzahl, lblKaFehlend, lblKaUnter (2×), conKaBalkenWert, lblKaStand, OnVisible und btnKaSpeichern (2×). Alle werden bei jedem Antippen neu berechnet.
- Bei 20–40 Punkten ist das unkritisch (geschlussfolgert). Jede künftige Regeländerung (z. B. B2) muss aber an zehn Stellen gleich nachgezogen werden.
- Vorschlag: Ein unsichtbares Label `lblKaSichtbarAnzahl` mit der Anzahl, das lblKaUnter, conKaBalkenWert und lblKaStand nutzen. Oder eine benannte Formel `SichtbareAntworten = Filter(colAntworten As a; …)` in App.Formulas (UNSICHER: benannte Formel auf eine Sammlung vorher in Studio testen). Im Generator prüfen, dass alle Stellen zeichengleich sind (das ist heute der Fall).

### B10 – niedrig – UNSICHER – Galeriezeilen verschieben sich, wenn B ein- oder ausgeblendet wird (geschlussfolgert)

- Bisher änderte sich die Zeilenmenge von `galKaPruefpunkte` beim Bearbeiten nie. Jetzt rutschen alle Zeilen unter B um eine Position.
- Classic-TextInput und Classic-Dropdown übernehmen `Default` nur, wenn sich der Wert ändert.
- Risiko: Nicht übernommener Text bleibt in der falschen Zeile stehen, oder ein Dropdown-OnChange schreibt beim Neubinden.
- Vorschlag (Test ergänzen): In einem TEXT- oder AUSWAHL-Punkt **unterhalb** von B etwas eingeben, ohne das Feld zu verlassen. Dann direkt A auf n.i.O. tippen. Danach prüfen, dass B leer ist, der untere Punkt seinen Wert behält und `colAntworten` stimmt (z. B. über „Noch offen“).

### B11 – niedrig – UNSICHER – Andere Leser des JSON (geschlussfolgert)

- Ausgeblendete Zeilen stehen weiter im JSON (`RG_KategorieErgebnisse.Antworten`), nur mit Flag.
- Die App filtert sie in Protokoll und Nur-Ansicht. Flows oder Auswertungen, die das JSON selbst lesen (Mail-Versand → `MailGesendetAm`, Auswertungen), zeigen sie als leere Zeilen.
- Vorschlag: Prüfen, welche Flows `Antworten` lesen, und dort `Ausgeblendet` ebenso filtern. Wenn keiner das JSON liest, ist nichts zu tun.

### B12 – niedrig – Doku der Einfügeschritte (belegt)

- Schritt 4.5 nennt keine Pfade: `lblKaUnter` liegt in `conKaKopf`, `conKaBalkenWert` in `conKaBalken`, `lblKaStand` in `conKaFuss`, die beiden Zähl-Labels direkt auf `scrKategorie` (unsichtbar). Paket 1 hat diese Pfade genannt.
- Schritt 4.2: Der Standardwert 0 gilt nur für neue Zeilen. Bestehende Zeilen bleiben leer. Das ist durch `Coalesce(p.BedingungPunkt; 0)` abgedeckt, sollte aber erwähnt werden, damit niemand alle Zeilen nachpflegt.

## Ohne Befund geprüft

**Syntax und Studio**
- Deutsche Schreibweise (`;`, `;;`, `";"` in Zeichenketten unverändert), Klammern maschinell geprüft.
- UDFs mit `With`, `Filter … As s` und Aufruf anderer UDFs (wie das bewährte `fnPlanPasst`/`fnLinkAnzahl`). Leere Werte an Boolean- und Number-Parameter sind abgefangen, weil `!gef` zuerst kurzschließt.
- `With` im Filter-Prädikat und `LookUp` auf dieselbe Sammlung im Filter: nur lesend, auch in den Verhaltensformeln. Im `UpdateIf`-Prädikat wird bewusst `colVersteckt` statt `colAntworten` gelesen.
- `UpdateIf` mit zwei Bedingungs-/Änderungspaaren (schließen sich gegenseitig aus) und `in` gegen `colVersteckt.PruefpunktID`, auch wenn die Sammlung leer ist.
- `Boolean()` auf untypisierten Werten mit `IfError`/`Coalesce`: fehlendes Feld ergibt false.
- `Filter(Table(ParseJSON(e.Antworten)); … ThisRecord.Value.Ausgeblendet)` innerhalb von `Concat(… As e)`: ThisRecord ist die Filterzeile.
- Keine Kommentare in Verhaltensformeln, `Concat … As` wie in P1 bewährt, kein Navigate in OnVisible.

**Daten**
- Schema von `colAntworten` in allen drei Zweigen gleich: BedID Zahl, BedWert Text, Ausgeblendet Boolean, Reihenfolge der Felder bis Inaktiv identisch.
- `galKaPruefpunkte.Default = varSprungRec` passt zum Typ.
- `ShowColumns` mit Bezeichner (`supportcolumnnamesasidentifiers`).

**Logik**
- Sichtbarkeit live beim Bearbeiten, in der Nur-Ansicht über das gespeicherte Flag. Altes JSON ohne Feld gilt als sichtbar (T4.9).
- Ausgeblendete werden nicht als offen gezählt, nicht angesprungen, nicht in „x von y“ und nicht in der n.i.O.-Zahl geführt.
- AnzahlNIO wird nach dem Leeren berechnet und ist konsistent mit `colMaengelSoll` (Filter `Bewertung = "NIO"`), die Plausibilität in `btnRuAbschluss` bleibt erfüllt. Inaktive Punkte werden wie bisher in beiden mitgezählt.
- Kette, Selbstbezug, A in anderer Kategorie, A inaktiv mitgeführt: B ist sichtbar.
- Leeren ist stabil: Ein geleertes B kann keine andere Sichtbarkeit ändern, weil Ketten ausgeschlossen sind.
- Inaktive mitgeführte Antworten behalten ihr Flag.
- Konfliktprüfung bei zwei Prüfern, Nachlese und die 2-s-Sperre sind unverändert.
- Zweites Speichern derselben Kategorie: Flags werden neu berechnet, keine doppelten Foto-Links (außer B1).

**Rückweg**
- Die Vorher-Blöcke sind zeichengleich. Die Reihenfolge „App.Formulas zuletzt“ passt, weil die Vorher-Fassungen `fnSichtbar` nicht nutzen.
- Die alte App ignoriert das Feld `Ausgeblendet`.
