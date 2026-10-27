# Prüfergebnis Paket 2 (Pflicht-Kommentar) und Paket 3 (Grenzmodus)

Prüfer: unabhängiger Prüf-Agent, 27.10.2026. Grundlage: `export/*.pa.yaml` (+ Zeile 08:44 laut HINWEIS.md), `SPALTEN.md`, Paket 1 als Vorstand, Paket 2 und 3.
Kennzeichnung: **belegt** = aus Export/Paketblöcken direkt ablesbar, **geschlussfolgert** = aus dem Verhalten von Power Apps abgeleitet, nicht in Studio getestet.

## Kurzfassung

- **Keine Syntax- oder Namensfehler gefunden.** Klammern, Trennzeichen, Vorher-Fassungen und Funktionsköpfe passen (maschinell geprüft, siehe unten).
- **0 hoch, 4 mittel, 8 niedrig.**
- Wichtigste Punkte: (B1) „Kommentar leeren“ löscht Kommentare deaktivierter Prüfpunkte, das trifft durch Paket 2/3 jetzt echte Daten. (B2) „Warnen“ hinterlässt im Protokoll, in der Übersicht und im JSON keine Spur: ein Wert außerhalb steht als grünes „i.O.“ da. (B3) „Sperren“ hat keinen Ausweg: ist der echte Messwert außerhalb, lässt sich die Kategorie nicht speichern und der Rundgang nicht abschließen. (B7) Der Testbogen von Paket 3 lässt sich so nicht der Reihe nach ausführen.

## Maschinell geprüft (ohne Befund)

- Alle 10 Blöcke (P2: 5, P3: 5): Klammern und Anführungszeichen sind ausgeglichen (eigenes Skript, Zeichenketten berücksichtigt).
- „Vorher“-Fassungen: P2 `App.Formulas`/`scrKategorie.OnVisible` stimmen zeichengleich mit den Paket-1-Blöcken überein, P3 mit den Paket-2-Blöcken. `txtKaKommentar.HintText`/`AccessibleLabel`, `htmProtokoll.HtmlText` (EN→DE umgesetzt, Leerraum normalisiert), `lblKaZahlInfo.Text/.Color`, `txtKaZahl.BorderColor` stimmen mit dem Export überein (**belegt**).
- Diff neu gegen vorher: P2 ändert genau `fnKommentarNoetig`, eine Zeile in OnVisible (`KommentarPflicht`), HintText, AccessibleLabel und die Kommentarfarbe im Protokoll. P3 ändert die Farben (neu), `fnZahlBewertung`, `fnGrenzmodus` (neu), `fnKommentarNoetig`, `fnFehltGrund` („Bereich“), 3 Stellen in OnVisible und 3 Anzeige-Properties. Es gibt keine versteckten Nebenänderungen (**belegt**).
- Deutsche Schreibweise: `;` trennt Argumente, `;;` trennt Ketten und Benannte Formeln. Dezimalzahlen kommen nicht vor. In P2/P3 stehen keine Kommentare in Formeln. Es gibt kein `Navigate` in OnVisible. `Concat … As` kommt nur im unveränderten Protokoll vor (läuft im Export).
- Funktionsköpfe: Die Signaturen von `fnZahlBewertung`, `fnKommentarNoetig`, `fnFehltGrund` und `fnFehlt` bleiben gleich (seit Paket 1). Damit entstehen beim Einfügen in der Reihenfolge Formulas → OnVisible → Steuerelemente keine Zwischenfehler, ebenso nicht beim Rückweg (Formulas zuletzt). Nicht benutzte Parameter in UDFs sind zulässig.
- Namen: `KommentarPflicht`, `Grenzmodus`, `FotoModus`, `MinWert`, `MaxWert` und `Inaktiv` stehen in allen drei Zweigen von `colAntworten` mit gleichem Typ (Boolean/Text). `fnAusserhalb`, `fnBeantwortet` und `fnLinkAnzahl` gibt es seit Paket 1. Die Steuerelemente `txtKaKommentar`, `lblKaZahlInfo`, `txtKaZahl` und `htmProtokoll` gibt es im Export. Die Spalten `KommentarPflicht` (Ja/Nein) und `Grenzmodus` (Auswahl, `.Value`) legen die Schritte 2.2/3.2 an, beide werden mit `Coalesce` bzw. `fnGrenzmodus` gegen leere Werte abgesichert (leere Zeile → Nein bzw. Mangel).
- `txtKaZahl.OnChange` (Paket 1) gibt `ThisItem.Grenzmodus` schon weiter, also wirkt P3 auch beim Tippen. Die Galerie-Items enthalten das Feld (**belegt**).
- Grenzwerte: Ein Wert genau auf Min/Max zählt als im Bereich (`<`/`>`). Bei leerem Min und/oder Max greift die jeweilige Grenze nicht. Leeres `z` gilt als nicht außerhalb (`fnAusserhalb`), die Aufrufer prüfen `IsBlank` vorher. Dezimalwerte funktionieren (`Value` mit de-DE).
- Mängel beim Abschluss (`btnRuAbschluss`) zählen nur `Bewertung = "NIO"` aus dem JSON. `AnzahlNIO` beim Speichern zählt dasselbe → „Warnen“ (IO) und „Sperren“ (nie gespeichert) bleiben in sich stimmig (**belegt**).
- Textlängen: Die neuen Hinweise („außerhalb, bitte begründen“ 26 Zeichen, „unzulässig, bitte prüfen“ 24) sind kürzer als der bisherige („außerhalb des Sollbereichs“ 26/28). „Kommentar (Pflicht)“ ist kürzer als „Kommentar zum Mangel (Pflicht)“ → nichts wird neu abgeschnitten (**geschlussfolgert**).

## Befunde

### B1 – Paket 2 (wirkt auch in 3) – mittel – `btnKaSpeichern.OnSelect` (Zeile „Kommentar leeren“ aus Paket 1)
**Belegt.** `UpdateIf(colAntworten; !fnKommentarNoetig(Typ; Bewertung; …; KommentarPflicht; Grenzmodus; MinWert; MaxWert); {Kommentar: ""})` läuft über **alle** Zeilen, auch über `Inaktiv = true`. Inaktive Zeilen bekommen in OnVisible fest `KommentarPflicht: false`, `Grenzmodus: "Mangel"` und `MinWert/MaxWert: Blank()`.
**Szenario:** Ein Punkt mit KommentarPflicht wird mit i.O. + Kommentar gespeichert (P2), oder ein Warnen-Punkt mit Begründung (P3). Danach wird er in den Stammdaten deaktiviert. Ein Prüfer öffnet die Kategorie erneut und speichert → der i.O.-Kommentar bzw. die Begründung wird aus dem JSON gelöscht, obwohl OnVisible (3b) verspricht, dass deaktivierte Antworten „unverändert mitgeführt“ werden. Das Gleiche passiert, wenn der Admin KommentarPflicht auf Nein stellt: Beim nächsten Speichern verschwinden alle i.O.-Kommentare dieses Punkts, und das Kommentarfeld war vorher nicht sichtbar. Vor Paket 2 gab es i.O.-Kommentare fast nicht, jetzt sind es gewollte Daten.
**Vorschlag:** In P2 einen eigenen Block für `btnKaSpeichern.OnSelect` mitliefern: `UpdateIf(colAntworten; !Inaktiv && !fnKommentarNoetig(…); {Kommentar: ""})`. Das Abschalten von KommentarPflicht in der Kurzfassung als „löscht vorhandene i.O.-Kommentare beim nächsten Speichern“ benennen (oder nur löschen, wenn `varGeaendert` für diesen Punkt gilt).

### B2 – Paket 3 – mittel (fachliche Rückfrage) – `fnZahlBewertung`, `htmProtokoll.HtmlText`, JSON in `btnKaSpeichern`
**Belegt.** Bei „Warnen“ wird der Wert außerhalb als `Bewertung = "IO"` gespeichert. Im JSON stehen nur `PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos`, also weder Grenzmodus noch Min/Max.
**Szenario:** Kühlschrank 18,5 °C bei Soll 6–16, Grenzmodus Warnen. Im Protokoll und im Archiv-PDF steht „i.O.“ in Grün mit einem grauen Kommentar (P2-Farbe). Die Rundgang-Übersicht zeigt „Erledigt · alles i.O.“, der Startbildschirm „0 n.i.O.“. Wer das Protokoll später liest, kann „i.O. im Bereich“ nicht von „i.O. außerhalb, begründet“ unterscheiden. Ändert sich später Min/Max, ist auch in der Nur-Ansicht nicht mehr erkennbar, dass der Wert außerhalb lag. Bei Warnen gibt es außerdem keinen Foto-Knopf (FotoModus Aus und nicht NIO), bei Mangel schon.
**Vorschlag:** Josias fragen, ob „Warnen“ im Protokoll sichtbar sein muss (Annahme: ja, er will Kontrollen). Dann ein JSON-Feld ergänzen, z. B. `Hinweis: "außerhalb"` oder `Grenze: Grenzmodus & " " & MinWert & "–" & MaxWert`, in `ShowColumns` und in den drei OnVisible-Zweigen. Im Protokoll die Bewertung orange als „i.O. (außerhalb)“ darstellen. Das Kommentarfeld bei Warnen mit „Begründung (Pflicht)“ beschriften statt „Kommentar (Pflicht)“.

### B3 – Paket 3 – mittel – `fnFehltGrund` („Bereich“), fachliche Bedeutung von „Sperren“
**Geschlussfolgert aus belegter Logik.** Bei Sperren blockiert ein Wert außerhalb das Speichern, und es gibt keinen Ausweg (keine Bestätigung, kein Ausweichen auf n.i.O.).
**Szenarien:**
- Der echte Messwert liegt außerhalb (Gerät tatsächlich defekt) und der Punkt ist **Pflicht**: Ein leeres Feld ergibt „Wert“ fehlt, ein Wert außerhalb ergibt „Bereich“. Die Kategorie lässt sich nicht speichern, alle folgenden Kategorien bleiben gesperrt, der Rundgang lässt sich nicht abschließen. Der Prüfer kann nur einen falschen Wert eintragen.
- Nicht Pflicht: Der Prüfer muss das Feld leeren, damit verschwindet der echte (auffällige) Wert spurlos.
- Fehlkonfiguration Min > Max oder enge Grenzen mit Pflicht → dauerhaft unspeicherbar.
**Vorschlag:** In der Kurzfassung als Regel festhalten: „Sperren nur mit physikalisch unmöglichen Grenzen (Tippfehler-Schutz)“. Besser einen Ausweg einbauen, z. B. bei „Bereich“ ein zweites Tippen „Wert bestätigen“, das den Punkt als n.i.O. mit Kommentarpflicht übernimmt. Mindestens Min ≤ Max in den Stammdaten prüfen lassen (Hinweis an den Admin).

### B4 – Paket 3 – niedrig – `lblKaZahlInfo.Text`
**Belegt.** Bei Sperren zeigt die Karte die Grenzen als „Soll ab … bis …“. Bei Sperren sind das aber Plausibilitätsgrenzen, und ein Wert darin ist immer „i.O.“. Ein Prüfpunkt kann nicht gleichzeitig einen Soll-Bereich (Mangel) und Tippfehler-Grenzen (Sperren) haben, weil es nur ein Min/Max-Paar gibt. Wer auf „Sperren“ umstellt, verliert die Mangel-Erkennung für diesen Punkt.
**Vorschlag:** Bei Sperren „zulässig …“ statt „Soll …“ anzeigen. In der Kurzfassung deutlich machen, dass Sperren die Mangel-Prüfung ersetzt. Wird beides gebraucht, wären zwei weitere Spalten nötig (Plausi-Min/-Max).

### B5 – Paket 3 – niedrig – `scrKategorie.OnVisible` (Bewertung beim Öffnen) / `btnKaZurueck`
**Geschlussfolgert.** Die Bewertung von ZAHL-Punkten wird beim Öffnen mit dem **aktuellen** Grenzmodus neu berechnet, `varGeaendert` bleibt dabei `false`.
**Szenario:** Ein Punkt wurde als Mangel (NIO) gespeichert, dann stellt der Admin auf Warnen um. Der Prüfer öffnet die Kategorie: Er sieht „i.O., außerhalb, bitte begründen“ und geht ohne Speichern zurück, ohne Rückfrage. Beim Abschluss entsteht trotzdem ein Mangel aus dem alten JSON. Umgekehrt (Warnen → Mangel) zeigt die Karte n.i.O., es entsteht aber kein Mangel. Bei einer Umstellung auf Sperren zeigt eine erledigte Kategorie „Noch offen (unzulässiger Wert)“, zählt aber weiter als erledigt. Das Muster gab es schon bei Min/Max-Änderungen, P3 fügt einen weiteren Auslöser hinzu.
**Vorschlag:** In OnVisible `varGeaendert` auf `true` setzen, wenn eine neu berechnete Bewertung von der gespeicherten abweicht. Dann fragt „Zurück“ nach. Alternativ in der Kurzfassung: „Grenzmodus nur zwischen Rundgängen ändern.“

### B6 – Paket 3 – niedrig – `lblKaZahlInfo.Text/.Color`, `txtKaZahl.BorderColor` in der Nur-Ansicht
**Belegt.** Im Nur-Ansicht-Zweig kommen `Grenzmodus` und `MinWert/MaxWert` aus den **aktuellen** Stammdaten (`pp`), nicht aus dem Gespeicherten.
**Szenario:** In einem abgeschlossenen Rundgang steht bei einem Warnen-Wert „außerhalb, bitte begründen“ in Orange, obwohl nichts mehr zu tun ist. Wurde der Grenzmodus später auf Mangel gestellt, erscheint bei einem gespeicherten i.O.-Wert außerhalb gar kein Hinweis. Bei Sperren kann „unzulässig, bitte prüfen“ an einem gespeicherten Wert stehen.
**Vorschlag:** In der Nur-Ansicht neutrale Texte verwenden („außerhalb, begründet“ bzw. keinen Sperren-Text): `If(varNurLesen; …)` in den drei Properties. Langfristig mit B2 lösen (Grenzen im JSON).

### B7 – Paket 3 – mittel – Testbogen T3.1–T3.8
**Belegt.**
- T3.1 (Mangel, 18,5) trägt keinen Kommentar ein, T3.3 tippt danach „Speichern“. Liegen beide Punkte in derselben Kategorie, scheitert das Speichern mit „Noch offen: … (Kommentar)“.
- Nach erfolgreichem Speichern (T3.3) öffnet die App automatisch die **nächste** Kategorie (`varWeiter`). Für T3.4 muss man zurück und die Kategorie neu öffnen, das steht nicht da.
- Schritt 3.2 erlaubt „einen nacheinander umstellen“. Dann überschreibt T3.3 das Ergebnis von T3.1, und T3.7 („Mangel nur für T3.1“) ist nicht mehr prüfbar. Außerdem wirkt eine Umstellung erst nach erneutem Öffnen der Kategorie.
- T3.7 verlangt einen Abschluss, also alle Kategorien gespeichert. Sperren-Punkte, die bei T3.4 noch außerhalb stehen, blockieren das.
**Vorschlag:** Den Test als Zeitachse schreiben: drei getrennte Punkte (Mangel/Warnen/Sperren) in **einer** Kategorie, alle in einem Durchgang ausfüllen (Mangel mit Kommentar), Sperren erst 18,5 (Prüfung Fuß/Sprung), dann 12, dann einmal speichern. Danach Kategorie neu öffnen (Bearbeiten), Anzeige prüfen, Abschluss, RG_Maengel. Ausdrücklich „nicht nacheinander umstellen“.

### B8 – Paket 2 – niedrig – Testbogen T2.1/T2.8, Schritt 2.2
**Belegt.** Schritt 2.2 setzt KommentarPflicht nur für **einen** Punkt. T2.8 („optionaler Punkt mit KommentarPflicht unbeantwortet“) braucht aber einen Punkt mit KommentarPflicht = Ja **und** Pflicht = Nein, bei T2.1 ist das nicht festgelegt. T2.1 erwartet „Noch offen (1)“, das gilt nur, wenn alle anderen Pflichtpunkte der Kategorie schon ausgefüllt sind. T2.5 setzt voraus, dass man nach dem Speichern (Sprung in die nächste Kategorie) zurückgeht.
**Vorschlag:** In 2.2 einen Punkt mit Pflicht = Nein festlegen, T2.1 mit „übrige Punkte vorher ausfüllen“ beginnen, in T2.5 „zurück → Kategorie 2 Bearbeiten“ ergänzen.

### B9 – Paket 2 – niedrig – Rückweg
**Belegt.** Der Rückweg nennt nur die rote Darstellung. Nach dem Rückweg gilt `fnKommentarNoetig = (bew = "NIO")`. Das nächste Speichern einer Kategorie löscht dann alle gespeicherten i.O.-Kommentare (UpdateIf), es gehen also Daten verloren.
**Vorschlag:** Im Rückweg-Abschnitt ergänzen: „Nach dem Rückweg verschwinden i.O.-Kommentare beim nächsten Speichern der jeweiligen Kategorie.“

### B10 – Paket 2/3 – niedrig – `btnKaSpeichern.OnSelect` (Netzfehler)
**Geschlussfolgert.** Das `UpdateIf … {Kommentar: ""}` läuft vor dem `Patch`.
**Szenario:** Ein Punkt war n.i.O. mit Kommentar und wurde auf i.O. gestellt. Das Speichern scheitert (Netz), der Prüfer stellt wieder auf n.i.O.: Der Kommentar ist weg und muss neu getippt werden. Bei einem Warnen-Wert, der wieder außerhalb gestellt wird, passiert dasselbe. Das gab es seit 08:44, durch P2/P3 gibt es mehr Fälle.
**Vorschlag:** Erst in der JSON-Erzeugung leeren (`JSON(ShowColumns(AddColumns(…)))` mit einer berechneten Kommentarspalte), `colAntworten` selbst nicht ändern. Alternativ als bekanntes Verhalten hinnehmen.

### B11 – Paket 3 – niedrig – `App.Formulas`
**Belegt.** `clrWarnungHell` wird definiert, aber nirgends verwendet.
**Vorschlag:** Weglassen oder z. B. als `HoverFill`/Hintergrund des Warn-Hinweises verwenden. Das ist nur kosmetisch.

### B12 – Paket 2/3 – niedrig – Kopfzeile/Voraussetzungen
**Belegt.** Beide Pakete tragen „ENTWURF: Simulation der Änderung von 08:44, vor dem Einfügen mit dem frischen Export neu erzeugen“. Die Voraussetzungen verlangen aber nur „Paket 1 eingefügt“. Wer nach den Voraussetzungen vorgeht, fügt womöglich den Entwurf ein.
**Vorschlag:** Den Satz „Paket aus dem Export nach dem Einfügen von Paket 1 neu erzeugt (Kopfzeile ohne ENTWURF)“ als Voraussetzung aufnehmen. Nach jedem Paket neu exportieren und gegen den Soll-Stand abgleichen.

## Szenarien (Zusammenfassung)

| Szenario | Paket 2 | Paket 3 |
|---|---|---|
| neuer Punkt ohne Daten | ok (`Coalesce` → Nein) | ok (`fnGrenzmodus` → Mangel) |
| alter gespeicherter Punkt (JSON ohne neues Feld) | ok, kein neues JSON-Feld | ok, Bewertung wird neu berechnet (siehe B5) |
| inaktiver Punkt | **B1** (Kommentar wird gelöscht) | **B1** (Begründung wird gelöscht) |
| Nur-Ansicht | ok, i.O.-Kommentar sichtbar und grau im Protokoll | B6 |
| n.i.O. → i.O. → n.i.O. | ok (Kommentar bleibt bis zum Speichern) | ok, nach Speicherfehler B10 |
| Kategorie zweimal speichern | ok | ok |
| Abbruch/Netzfehler | B10 | B10 |
| zwei Prüfer gleichzeitig | ok (bestehende Prüfung `GespeichertAm`) | ok |
| Grenzwert genau, leeres Min/Max, Dezimalzahl | – | ok |
| echter Wert außerhalb bei Sperren | – | **B3** |
