# Rundgang-App: Analyse des Exports vom 27.10.2026

Quelle: `quellen/2026-10-27_Export/RundgangApp_20261027072413.zip` (App „Rundgang DEV“, gespeichert 27.10. 07:04 UTC, Umgebung „Personal Productivity“). YAML-Quellen liegen in `quellen/2026-10-27_Export/Src/`.
Auftrag: **nur analysieren und verstehen**, keine Formeln.
Kennzeichnung: **belegt** (Export), **geschlussfolgert**, **UNSICHER** (in Studio oder per Test prüfen).

## Kurzfassung
- Die App ersetzt MoreApp für wiederkehrende Rundgänge: Rundgang wählen → Kategorien der Reihe nach abarbeiten (i.O./n.i.O., Auswahl, Zahl, Text, Fotos) → abschließen → Mängelliste → PDF-Protokoll im SharePoint-Archiv.
- Die Bauweise ist solide und folgt den Lehren aus der Tischbuchung: feste Schlüssel statt neuer IDs, Nachlese nach jedem Schreiben, Doppelklick-Sperre, Bestätigung durch zweites Tippen, Momentaufnahme der Kategorien beim Start und Erkennung gleichzeitiger Bearbeitung. Die App-Prüfung meldet **0 Fehler** (belegt).
- Größte Risiken (geschlussfolgert):
  1. Beide Flows antworten nicht an die App. Die App wertet den Aufruf wahrscheinlich schon als Erfolg, sobald der Flow startet. Foto- und PDF-Links würden dann auch gespeichert, wenn die Datei nie entsteht.
  2. In SharePoint sind keine eindeutigen Schlüssel erzwungen. Wenn zwei Geräte gleichzeitig dasselbe tun, entstehen doppelte Durchführungen, Ergebnisse oder Mängel.
  3. Das PDF entsteht nur, solange die Protokoll-Seite offen bleibt.
  4. Noch nicht gebaut: der Mailversand und die Bearbeitung der Mängel.
  5. Rechte und Betrieb: Wer `RG_Konfiguration` bearbeiten darf, kann sich selbst zum Admin machen. Flows und Verbindungen laufen unter Josias' Konto.

## 1. Aufbau
**App** (belegt): 4 Bildschirme, Hochformat 768 × 1366 ohne „An Bildschirm anpassen“ (passt sich an). Farben und Funktionen stehen als benannte Formeln in `App.Formulas`. Einstellungen: `powerfxv1 = false`, `supportcolumnnamesasidentifiers = true`, `usenonblockingonstartrule = true`, Datenzeilen-Limit 2000.

| Bildschirm | Aufgabe |
|---|---|
| `scrStart` | Tag wählen (heute + `NachholTage`), geplante Rundgänge des Tages mit Fortschritt, Starten/Fortsetzen/Ansehen, Warnbalken „nicht abgeschlossen“ für alte offene Rundgänge |
| `scrRundgang` | Kategorienliste (gesperrt bis die vorige gespeichert ist), Abschluss, Admin: „Zurück auf In Arbeit“, Weg zum Protokoll |
| `scrKategorie` | Prüfpunkte ausfüllen, Fotos (`addKaFoto`), Pflichtprüfung mit Sprung zum ersten offenen Punkt, „Speichern & weiter“ |
| `scrProtokoll` | HTML-Protokoll, automatisches Archivieren als PDF (Timer 800 ms), Link zum Archiv-PDF |

**Listen** (SharePoint `IMSKonzept`, belegt):
- Stammdaten: `RG_Rundgaenge` → `RG_Bereiche` (`RundgangID`) → `RG_Kategorien` (`BereichID`) → `RG_Pruefpunkte` (`KategorieID`, `Eingabetyp` IONIO/AUSWAHL/ZAHL/TEXT, `Pflicht`, `Min/MaxWert`, `Auswahlwerte` mit `;`, `FotoMoeglich`). Plan: `RG_Plan` (`Wochentag` 1 = Mo, `ZyklusWochen`, `StartMontag`, `GueltigBis`). `RG_Konfiguration` (Schlüssel/Wert: `NachholTage`, `Testmodus`, `Testadresse`, `Empfaenger`, `Admins`).
- Bewegungsdaten:
  - `RG_Durchfuehrungen`: Schlüssel `Title = "R{RundgangID}-{yyyy-mm-dd}"`, `Status` InArbeit → Abschluss → Abgeschlossen, `KategorieListe` als JSON-Momentaufnahme.
  - `RG_KategorieErgebnisse`: `Title = "D{DurchID}-K{KatID}"`, `Antworten` als JSON, `GespeichertAm` für die Erkennung gleichzeitiger Bearbeitung.
  - `RG_Maengel`: `Title = "D{DurchID}-P{PPID}"`, Status-Auswahl „Offen“, die Felder `Verantwortlich`/`Frist`/`Massnahme`/`ErledigtAm` sind noch ungenutzt.
- Bibliotheken: `RG_Fotos`, `RG_Protokolle` (Ordner `[TEST/]JJJJ/MM`), dazu OneDrive `/RG_Temp` (Josias).

**Flows** (belegt, beide mit PowerApps-V2-Auslöser, **ohne „Antwort an PowerApp“**):
- `RG_Foto_hochladen` (in der App `aRG_Foto_hochladen`): legt eine Datei in `RG_Fotos/{Ordner}` an und setzt `DurchfuehrungID`, `PruefpunktID` und `TestDatensatz`.
- `RG_Protokoll_archivieren`: legt die HTML-Datei in OneDrive `/RG_Temp` an, wandelt sie in PDF um, speichert sie in `RG_Protokolle/{Ordner}` und setzt die Eigenschaften.

## 2. Ablauf und Zustände
1. **Start** (`btnRgAktion`): Die App liest die Durchführung frisch über ihren Schlüssel. Gibt es keine, baut sie aus den aktiven Bereichen und Kategorien die sortierte `colKatBau` und legt die Durchführung an (Patch, dann Nachlese über den Schlüssel). Gestartet werden darf nur ein Tag zwischen heute und `heute − NachholTage`.
2. **Kategorie** (`scrKategorie.OnVisible`): In Arbeit kommen die aktiven Prüfpunkte aus den Stammdaten und werden mit dem gespeicherten JSON vorbelegt. Antworten zu inzwischen deaktivierten Punkten laufen unsichtbar mit. In der Nur-Ansicht zeigt die App genau das gespeicherte JSON.
3. **Speichern** (`btnKaSpeichern`):
   - Prüfungen: Pflicht, Status = InArbeit, `GespeichertAm` unverändert seit dem Öffnen, Reihenfolge.
   - Danach lädt die App neue Fotos hoch (Dateiname steht schon beim Aufnehmen fest), hängt die Links an und patcht.
   - Nachlese: Das JSON muss zeichengleich zurückkommen. Dann `varWeiter`, und `tmrWeiter` öffnet die nächste offene Kategorie.
4. **Abschluss** (`btnRuAbschluss`, zweites Tippen):
   - Status → Abschluss, ab dann lehnt Speichern Änderungen ab.
   - Die App erzeugt aus den n.i.O.-Antworten `colMaengelSoll`. Die Anzahl muss `Sum(AnzahlNIO)` entsprechen.
   - Fehlende Mängel legt sie per `Collect` an, das lässt sich gefahrlos wiederholen.
   - Nachlese: Mängel vollständig, Ergebnisse unverändert, Status noch Abschluss. Dann Status → Abgeschlossen und weiter zum Protokoll.
5. **Zurücksetzen** (nur Admin, nur im Status Abschluss, frühestens 5 Min nach der letzten Änderung): Die App löscht die offenen Mängel und setzt den Status zurück auf InArbeit.
6. **Protokoll**: Ist der Rundgang abgeschlossen und noch kein PDF da, archiviert die App nach 800 ms automatisch. Danach zeigt der Knopf „Archiv-PDF öffnen“.

## 3. Was gut gelöst ist (belegt)
- Jede Schreibstelle hat die Sperre `!varIsLoading && Now() >= varSperreBis`, `IfError` und eine Nachlese.
- Feste Schlüssel machen Wiederholungen gefahrlos (Mängel, Fotodateinamen).
- Die Kategorienliste wird beim Start eingefroren. Spätere Änderungen an den Stammdaten verändern laufende Rundgänge nicht.
- Gleichzeitige Bearbeitung erkennt die App über `GespeichertAm`. Die Meldung nennt den Namen, wer zuerst gespeichert hat.
- Nicht blockierender OnStart ist abgesichert (`IsBlank(varHeute)` in `scrStart.OnVisible`).
- Tageswechsel bei offener App über `tmrStartTag`.
- Zahlen bewertet die App automatisch gegen Min/Max. Für jedes n.i.O. ist ein Kommentar Pflicht (`fnFehlt`).
- Text, der ins HTML-Protokoll geht, wird maskiert (`fnHtml`). Dateinamen werden bereinigt (`fnDateiname`).
- Testdaten sind getrennt (`TestDatensatz` bei „ZZ Test…“, Ordner `TEST/`).

## 4. Befunde
| Nr | Befund | Kennzeichnung | Folge | Prüfen / Richtung |
|---|---|---|---|---|
| R1 | Beide Flows haben keine Aktion „Auf PowerApp oder Flow antworten“. Ohne Antwort wartet die App nicht auf das Ende des Flows. `IsError(….Run(…))` erkennt dann nur Fehler beim Start. | Flow belegt, Verhalten geschlussfolgert | Ein Foto-Link landet im JSON, ein `ProtokollUrl` in der Durchführung, obwohl die Datei fehlen kann. Danach zeigt die App „✓ Archiv-PDF öffnen“ und archiviert nicht noch einmal. | Test: Ordnerpfad im Flow absichtlich falsch → zeigt die App Erfolg? Richtung: Antwort-Aktion mit der echten Datei-URL, die App speichert diese URL statt `fnSpUrl` |
| R2 | Kein eindeutiger `Title` erzwungen (aus dem Export nicht sichtbar) | UNSICHER | Zwei Geräte starten gleichzeitig denselben Rundgang oder speichern dieselbe Kategorie zum ersten Mal → doppelte Datensätze. Beim Abschluss kann ein doppeltes Ergebnis Mängel doppelt anlegen. | In SharePoint: Spalte `Title` in Durchführungen, Ergebnissen und Mängeln indiziert + „Eindeutige Werte erzwingen“. Das zweite Patch scheitert dann, die Nachlese findet den ersten Datensatz (keine App-Änderung) |
| R3 | Das PDF entsteht nur über `scrProtokoll` (Timer). Wer nach dem Abschluss sofort zurückgeht oder die App schließt, hat kein PDF. | belegt | Rundgang ist abgeschlossen ohne Archiv, nur „Protokoll ⚠“ in der Übersicht | Bewusst so? Sonst später: Archivierung über einen Flow auslösen, wenn der Status wechselt |
| R4 | Mailversand fehlt: `MailGesendetAm` wird nur angezeigt, `cfgEmpfaenger`/`cfgTestadresse` sind definiert und ungenutzt, `cfgTestmodus` steht nur im Kopf | belegt | Teil von „nicht fertig“ | Klären: Wer bekommt was, wann? Testmodus → Testadresse |
| R5 | Mängel-Nacharbeit fehlt in der App (`Verantwortlich`, `Frist`, `Massnahme`, `ErledigtAm`) | belegt | Nacharbeit nur direkt in der SharePoint-Liste | Klären, ob in der App oder über die Liste |
| R6 | Rechte stehen nicht im Export. Kann jeder Prüfer `RG_Konfiguration` und die Stammdaten bearbeiten, kann er sich in `Admins` eintragen oder Prüfpunkte ändern. | geschlussfolgert | Rechteausweitung, verändertes Prüfschema | Stammdaten und Konfiguration für Prüfer nur lesbar (Thema für Michael) |
| R7 | Betrieb hängt an Josias: Flows und Verbindungen unter seinem Konto, HTML-Zwischendateien in seinem OneDrive `/RG_Temp` (werden nie gelöscht), Support-Mail fest im Banner | belegt | Wie bei der Tischbuchung: eine Person | Flow-Mitbesitzer, Löschschritt für die Zwischendatei, Support-Adresse in die Konfiguration |
| R8 | Zurücksetzen löscht nur „Offen“-Mängel. Hat jemand einen Mangel schon weiterbearbeitet und der Punkt ist nach der Korrektur i.O., bleibt der alte Mangel stehen. | belegt | Veralteter Mangel in der Liste | Klären, ob Zurücksetzen nach Beginn der Nacharbeit überhaupt erlaubt sein soll |
| R9 | `AnzahlNIO` und die Mängel zählen auch n.i.O.-Antworten deaktivierter Prüfpunkte, die in der Kategorie unsichtbar sind | belegt | Mangel, den der Prüfer nicht sieht und nicht korrigieren kann (Sonderfall) | Bewusst? |
| R10 | Fotos aus `AddMedia` gehen unkomprimiert über den Flow, eines nach dem anderen | geschlussfolgert | Speichern dauert bei mehreren Handyfotos und schwachem WLAN lange | Messen (Monitor) |
| R11 | Ein Foto, das schon hochgeladen ist, bleibt am Punkt, auch wenn er wieder auf i.O. gestellt wird. Nach „Verwerfen“ bleiben hochgeladene Dateien als Waisen. | belegt | Fotos an i.O.-Punkten im Protokoll | Bewusst? |
| R12 | Start-Abfrage: `Filter(k, CountRows(Filter(b, …)))` mit `b`/`k` als Abfragen in `With` | UNSICHER | Möglicherweise viele Einzelabfragen beim Starten | Monitor beim ersten Start |
| R13 | `Properties.json`: `ParserErrorCount = 1`, die App-Prüfung zeigt aber keinen Fehler | belegt / Ursache UNSICHER | evtl. eine rot markierte Formel in Studio | In Studio prüfen |
| R14 | `tmrWeiter.Start = varWeiter`: varWeiter wird gesetzt, bevor `scrRundgang` sichtbar ist | UNSICHER | Falls der Timer den Wechsel nicht sieht, bleibt „Nächste Kategorie wird geöffnet …“ stehen | Test: zwei Kategorien hintereinander speichern |
| R15 | Rundgänge, die an vergangenen Tagen geplant waren und nie gestartet wurden, sieht niemand (nur begonnene erscheinen im Warnbalken) | belegt | Versäumte Rundgänge bleiben unbemerkt | Fachlich klären (Auswertung oder Hinweis) |

Kleinigkeiten (belegt):
- `varAlleIOFrage` ist ungenutzt, „Alle i.O.“ ist offenbar geplant.
- 9 × `CollectingReadOnlyTable` und 1 × `ForAllWithMutation` sind Hinweise, keine Fehler.
- `lblKaAbstand.Text = ThisItem.Auswahl` ist vermutlich ein Platzhalter.

## 5. Offene Fragen an Josias
1. Was fehlt laut dir noch („nicht fertig“)? Mail, Mängel-Nacharbeit, „Alle i.O.“, Auswertung?
2. Wer prüft (Handy, Tablet)? Läuft die App auch am Handy (Breite ~390)?
3. Sind die `Title`-Spalten in SharePoint schon eindeutig?
4. Soll das PDF auch ohne geöffnete Protokoll-Seite entstehen?
5. Welche Rechte haben Prüfer auf Stammdaten und Konfiguration?
6. Welche MoreApp-Funktionen werden heute genutzt (Unterschrift, GPS, Zeitstempel je Punkt, Wiederholungsgruppen, Auswertung)?
