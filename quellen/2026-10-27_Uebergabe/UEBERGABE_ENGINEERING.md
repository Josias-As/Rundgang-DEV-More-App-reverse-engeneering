# Übergabe an den Engineering-Chat: Rundgang-App (RG)

Stand: 27.10.2026. Verfasser: Planer-Chat (bisher Planer, Ingenieur und Bauer in einem). Ab jetzt: **dieser Chat plant, der Engineering-Chat baut.**
Alles, was hier steht, wurde am 27.10.2026 gegen die echten Listen und die App geprüft. Was nicht geprüft ist, steht unter „Ungeprüft / offen“.

## 0. Rahmen und Regeln (zuerst lesen)
- **Auftraggeber:** Josias Assefaw (josias.assefaw@technoform.com). Spricht Deutsch. Mag kurze, einfache Erklärungen. Mag keine langen Anleitungen. Will, dass Kontrollen statt Abkürzungen gebaut werden (die Prüfer sind nicht verlässlich, siehe 8).
- **Projekt:** Die MoreApp-Form „Objektrundgang TCC“ (FM-Rundgangsformular) als Power-Apps-Canvas-App nachbauen und zu einem **Baukasten** ausbauen: Rundgänge sind Daten in SharePoint, die App baut sie zusammen.
- **Umgebung:** Power Platform „Personal Productivity“ (Default), Umgebung `Default-84e2e900-49ec-4416-85fb-299b258a5227`.
- **App:** „Rundgang DEV“, App-ID `1b9800f7-8289-4ee8-b720-cef0bbf1eae1`.
  - Studio: `https://make.powerapps.com/e/Default-84e2e900-49ec-4416-85fb-299b258a5227/canvas/?action=edit&app-id=%2Fproviders%2FMicrosoft.PowerApps%2Fapps%2F1b9800f7-8289-4ee8-b720-cef0bbf1eae1`
  - Abspielen (zeigt die **veröffentlichte** Version, nicht den Entwurf): `https://apps.powerapps.com/play/e/Default-84e2e900-49ec-4416-85fb-299b258a5227/a/1b9800f7-8289-4ee8-b720-cef0bbf1eae1?tenantId=84e2e900-49ec-4416-85fb-299b258a5227`
  - Zuletzt veröffentlicht: 27.10.2026 08:06.
- **SharePoint-Site:** `https://technoformgroup.sharepoint.com/sites/IMSKonzept` (IMS+). Alle Listen mit Präfix `RG_`.
- **Flows (Power Automate, Konto von Josias):**
  - `RG_Foto_hochladen`, ID `3c8c1241-13eb-4769-9e72-98a8e06c588c`. In Studio heißt er **`aRG_Foto_hochladen`** (alter Name beim Hinzufügen). Formeln benutzen diesen Namen.
  - `RG_Protokoll_archivieren`, ID `c6ac2276-0b3e-465e-9239-42c84883bba4`.
- **Dateien des Projekts:** `C:\rundgang_work\` (Git-Repo). Wichtig: `FORTSCHRITT.md` (Protokoll), `ENTSCHEIDUNGEN.md`, `FEATURES.json`, `TESTPROTOKOLL.md`, `pakete\` (Formel- und YAML-Pakete), `app\ablage\` (zuletzt eingefügte Formeln/YAML), `app\yaml\stand_2026-10-26_vor_Chrome\` (Exporte vor der Chrome-Phase).

### Harte Schranken
1. **Nicht in den Obsidian-Vault „Technoform Jornals“ schreiben**, bis Josias es ausdrücklich freigibt. (Vorfall am 26.10.: `search_and_replace` mit leerem Regex-Treffer hat viele Dateien beschädigt.)
2. Nur eigene Testdaten anfassen (`TestDatensatz = Ja`, Titel `ZZ Test …`, `D<n>-…`, `R<n>-…`). **Keine bestehenden Flows, Apps oder Listen von Josias** ändern.
3. Keine Passwörter, kein MFA. Berechtigungsdialoge (Verbindungen zulassen) nur mit ausdrücklichem Ja von Josias.
4. Mails nur im Testmodus an Josias, Betreff mit Präfix „TEST –“.
5. Vor jedem Löschen ansehen, was gelöscht wird. SharePoint-Zeilen mit `/recycle()` in den Papierkorb, nicht hart löschen.
6. Nach Änderungen: App-Check „Formeln“ = 0 Fehler, speichern, dokumentieren (`FORTSCHRITT.md`), committen.

## 1. Was die App tut (Fachlogik)
- Prüfer öffnen die App am Tablet (Hochformat). Die Startseite zeigt für einen Tag (heute, gestern bis `NachholTage`) die **geplanten Rundgänge** (laut `RG_Plan`).
- „Starten“ legt eine **Durchführung** an (`RG_Durchfuehrungen`). Der Rundgang besteht aus **Kategorien in fester Reihenfolge**, jede wird erst nach der vorherigen freigeschaltet.
- In einer Kategorie beantwortet der Prüfer **Prüfpunkte**: i.O./n.i.O., Zahl (mit Min/Max), Auswahl, Text. Pflichtfelder müssen ausgefüllt sein, bevor man speichern kann. Bei n.i.O. ist ein Kommentar Pflicht.
- „Speichern & weiter“ speichert die Antworten **als JSON** pro Kategorie (`RG_KategorieErgebnisse`) und öffnet automatisch die nächste Kategorie.
- „Rundgang abschließen“ (erst wenn alle Kategorien gespeichert sind) legt für jeden n.i.O.-Punkt einen **Mangel** an (`RG_Maengel`), setzt den Status auf „Abgeschlossen“ und springt zum **Protokoll**. Das Protokoll wird als PDF in `RG_Protokolle` archiviert.
- Fotos: pro Prüfpunkt, hochgeladen beim Speichern der Kategorie nach `RG_Fotos`. Links stehen in den Antworten, bei Mängeln und im Protokoll.
- Admins (Konfiguration `Admins`) können einen Rundgang zurücksetzen (frühestens 5 Minuten nach dem Start; entfernt nur Mängel mit Status „Offen“).

## 2. SharePoint-Datenmodell (geprüft 27.10.2026)
Pfad für Listen: `…/sites/IMSKonzept/Lists/<Name>`; Bibliotheken: `…/sites/IMSKonzept/<Name>`.

### 2.1 Stammdaten (die „Baustein“-Listen)
Verknüpfung heute **über Zahlen-IDs** (SharePoint-`Id`), nicht über Nachschlagespalten.

**RG_Rundgaenge** – der Rundgang. `Title`* Text, `Beschreibung` Note, `RgReihenfolge`* Zahl, `Aktiv` Ja/Nein.
**RG_Bereiche** – Gruppierung innerhalb eines Rundgangs. `Title`*, `RundgangID`* Zahl → RG_Rundgaenge.Id, `RgReihenfolge`*, `Hinweis` Note, `Aktiv`.
**RG_Kategorien** – das, was der Prüfer als ein Schritt speichert. `Title`*, `BereichID`* Zahl → RG_Bereiche.Id, `RgReihenfolge`*, `Hinweis` Note, `Aktiv`.
  Achtung: Eine Kategorie hat **keine** RundgangID. Der Rundgang ergibt sich über den Bereich.
**RG_Pruefpunkte** – die Fragen. `Title`* (Fragetext), `KategorieID`* Zahl → RG_Kategorien.Id, `RgReihenfolge`*, `Eingabetyp`* Auswahl `IONIO | AUSWAHL | ZAHL | TEXT`, `Pflicht` Ja/Nein, `Auswahlwerte` Text (Werte durch Trennzeichen), `Einheit` Text, `MinWert`/`MaxWert` Zahl, `Hinweis` Note, `Aktiv`, **`FotoMoeglich` Ja/Nein** (neu 26.10., Standard Nein).
**RG_Plan** – wann ein Rundgang dran ist. `Title`*, `RundgangID`*, `Wochentag`* Zahl (1 = Montag … 7 = Sonntag), `ZyklusWochen`* Zahl (1 = jede Woche, 2 = jede zweite …), `StartMontag`* Datum (Montag der Startwoche, Zeitzone beachten: gespeichert als Vortag 22:00 UTC), `GueltigBis` Datum, `Aktiv`.
**RG_Konfiguration** – Schlüssel/Wert: `Testmodus=Ja`, `Testadresse`, `Empfaenger`, `NachholTage=1`, `Admins` (E-Mail, Liste).

### 2.2 Ergebnisse (schreibt nur die App)
**RG_Durchfuehrungen** – eine Zeile je Rundgang je Tag. `Title` = `R<RundgangID>-<yyyy-mm-dd>`, `RundgangID`, `RundgangName`, `TagText` (yyyy-mm-dd), `KW`, `Wochentag`, `Status` Text (geprüft sind `InArbeit` und `Abgeschlossen`; der Zwischenstatus „Abschluss“ steht als `stAbschluss`, sein Textwert wurde nicht erneut geprüft; die Werte stehen als Konstanten `stInArbeit`, `stAbschluss`, `stAbgeschlossen` in der App), `AnzahlKategorien`, `KategorieListe` Note (JSON-Schnappschuss der Kategorien beim Start: KategorieID, Position, BereichName, KategorieName), `PrueferEmail`, `PrueferName`, `StartZeit`, `EndeZeit`, `AnzahlNIO`, `MailGesendetAm`, `TestDatensatz`, `ProtokollUrl`, `ProtokollErstelltAm`.
**RG_KategorieErgebnisse** – eine Zeile je Kategorie je Durchführung. `Title` = `D<DurchfuehrungID>-K<KategorieID>`, `DurchfuehrungID`, `TagText`, `KategorieID`, `Position`, `BereichName`, `KategorieName`, **`Antworten` Note = JSON** (Liste mit je PruefpunktID, Frage, Typ, Bewertung `IO|NIO`, WertText, WertZahl, Einheit, Kommentar, Fotos), `AnzahlNIO`, `PrueferEmail`, `PrueferName`, `GespeichertAm`, `TestDatensatz`.
**RG_Maengel** – je n.i.O.-Punkt beim Abschluss. `Title` = `D<id>-P<PruefpunktID>`, `DurchfuehrungID`, `PruefpunktID`, `RundgangName`, `BereichName`, `KategorieName`, `Frage`, `Wert`, `Kommentar`, `FestgestelltAm`, `FestgestelltVon`, `Status` Auswahl `Offen | InArbeit | Erledigt`, `Verantwortlich`, `Frist`, `ErledigtAm`, `Massnahme`, `TestDatensatz`, `FotoUrls` Note (Links durch ` | ` getrennt).

### 2.3 Bibliotheken
**RG_Protokolle** – PDF-Archiv. Spalten: `DurchfuehrungID`, `TestDatensatz`. Ordner: `[TEST/]<Jahr>/<Monat>/` (z. B. `TEST/2026/10/`). Dateiname: `<Durchführung-Title> <Rundgangname> <yyyymmdd-hhmmss>.pdf`.
**RG_Fotos** – Fotos. Spalten: `DurchfuehrungID`, `PruefpunktID`, `TestDatensatz`. Ordner: `[TEST/]<Jahr>/<Monat>/<Durchführung-Title>/`. Dateiname: `D<id>-K<katid>-P<ppid>-<8 Zeichen>.jpg`.
Beide hängen **nicht** im DMS. Rechte: erben von IMS+; Josias wollte „alle dürfen lesen“, Admin „nur ich“ (noch nicht eigens eingestellt, offen).

### 2.4 Konventionen
- `RgReihenfolge` ist die Sortierung (kleiner = früher). `Aktiv = Nein` blendet aus, löscht nicht (alte Ergebnisse bleiben lesbar).
- Test-Stammdaten tragen Titel `ZZ Test …` (ZZ = sortiert ans Ende). Test-Ergebnisse tragen `TestDatensatz = Ja`.
- Vorhandene Test-Stammdaten: 1 Rundgang („ZZ Test Objektrundgang TCC“), 2 Bereiche, 4 Kategorien (eine inaktiv), 10 Prüfpunkte (Id 9 inaktiv, Id 10 = Thermometer mit FotoMoeglich = Ja), 3 Planzeilen (Sonntag jede Woche, Montag 2-wöchig, **Dienstag jede Woche = nur für den Foto-Test, löschen**).
- Echte Rundgangs-Stammdaten gibt es noch nicht. Sie kommen vom Fachbereich.

## 3. App-Struktur (Power Apps Canvas, Tablet-Hochformat)
**Bildschirme:** `scrStart` (Tag wählen, geplante Rundgänge, Banner für ältere offene Rundgänge), `scrRundgang` (Kategorienliste, Abschluss-Knopf, Zurücksetzen), `scrKategorie` (Prüfpunkte als Galerie `galKaPruefpunkte` mit Karten `conKaKarte`, Speichern-Knopf `btnKaSpeichern`, Foto-Fenster `conKaFoto`), `scrProtokoll` (HTML-Protokoll `htmProtokoll`, Archiv-Knopf `btnPrArchivieren`, Timer `tmrPrArchiv`).
**Wichtige Steuerelemente:** `ddStartTag`, `galStartRundgaenge`, `conStartOffen` (rotes Banner für offene frühere Rundgänge), `tmrWeiter` (öffnet nach Speichern die nächste Kategorie, nötig, weil `Navigate` in `OnVisible` verboten ist), `conKaBalken` (Fortschritt), `addKaFoto` (Bild hinzufügen), `btnKaFoto`, `galKaFotoNeu`/`galKaFotoAlt`, `btnRuAbschluss`, `btnRuZuruecksetzen`, `btnRuProtokoll`.
**Datenquellen:** alle `RG_*`-Listen (SharePoint-Connector, Konto des Prüfers) plus die zwei Flows.
**App.Formulas (benannte Formeln/Funktionen):** `fnFehlt(typ; pflicht; bew; wt; wz; kom)` (ist ein Punkt noch offen?), `fnZahlBewertung`, `fnPlanPasst` (Plan-Logik: Wochentag/Zyklus/Start), `fnTagLabel`, `fnTagAnzeige`, `fnHtml` (HTML-Escaping), `fnDateiname`, `fnArchivOrdner(tag; test)`, `fnSpUrl(bib; pfad)`, `cfgAdmins`, `cfgNachholTage`, Konstanten `stInArbeit` usw., Farben `clrPrimaer`, `clrKarte`, `clrFehler`, `clrText`, `clrTextGrau`, `clrRahmen`, `clrHintergrund`.
**App.OnStart:** lädt Konfiguration und setzt Variablen (`varIsAdmin`, `varHeute`, `varTag`, `varSperreBis` u. a.).
**Zentrale Sammlungen/Variablen:** `colRundgaenge`, `colPlan`, `colDurchTag`, `colErgTag`, `colKatListe`, `colPP` (aktive Prüfpunkte der Kategorie), `colAntworten` (Antworten im Bearbeiten), `colFotos`, `colErledigt`, `colErgAlle`, `colMaengelSoll/Ist`, `varDurch`, `varDurchID`, `varKatID`, `varSchluesselK`, `varNurLesen`, `varSprungRec`, `varWeiter`, `varFotoPP`, `varZeigeFehlend`.
**Schutzmechanismen (nicht entfernen):** Doppelklick-Sperre (`varSperreBis`), Nachlese nach jedem Schreiben (gespeicherter JSON wird mit dem gesendeten verglichen), „Abschluss“ als Zwischenstatus gegen gleichzeitiges Speichern, Prüfung, dass der Rundgang nicht schon abgeschlossen ist, Kategorienreihenfolge, Warnungen bei Fehlern statt stiller Fehlschläge.

## 4. Die zwei Flows
Beide: Trigger „Power Apps (V2)“, laufen mit Josias’ Konto (SharePoint, OneDrive for Business), **ohne** „Antwort“-Aktion (die wäre Premium). Die App berechnet den Dateilink selbst mit `fnSpUrl`. Folge: Der Aufruf kehrt sofort zurück, scheitert der Flow später, merkt die App das nicht.
- **RG_Foto_hochladen:** Eingaben in dieser Reihenfolge: Foto (Datei), Dateiname, Ordner, DurchfuehrungID, PruefpunktID, Test. Aktionen: SharePoint „Datei erstellen“ in `/RG_Fotos/<Ordner>`, „Dateieigenschaften aktualisieren“.
- **RG_Protokoll_archivieren:** Eingaben: HTML, Dateiname, Ordner, DurchfuehrungID, Test. OneDrive „Datei erstellen“ in `/RG_Temp` (`<Dateiname>.html` mit `<meta charset="utf-8">`), „Datei konvertieren“ (PDF), SharePoint „Datei erstellen“ in `/RG_Protokolle/<Ordner>`, Eigenschaften setzen. **Offen:** Löschen der Zwischendatei in `/RG_Temp`.
- Beim Aufruf aus Power Fx müssen die Argumente in derselben Reihenfolge stehen wie die Trigger-Eingaben.
- Beim Tippen von „/“ in einem Flow-Feld öffnet sich das Menü „dynamischer Inhalt“ und das Zeichen wird verschluckt: für einen Schrägstrich vor einem Token „//“ tippen. (Im Code-View prüfen.)

## 5. Verhalten und Fallen (aus dem Bau gelernt)
**Power Apps / Studio**
- Ein Speichern in Studio ≠ Veröffentlichen. Der Abspiel-Link zeigt nur die veröffentlichte Version. Zum Testen des Entwurfs die Studio-Vorschau (Play) benutzen.
- `Navigate` ist in `OnVisible` nicht erlaubt: Timer (`tmrWeiter`) benutzen.
- Beim Einfügen von YAML friert Studio in Galerien mit flexibler Höhe gelegentlich Y/Height als feste Zahl ein: nach dem Einfügen prüfen und die Formel neu setzen.
- Kopieren und Einfügen: YAML wird auf einem markierten Container/Bildschirm eingefügt (Strg+V). Ein Bildsteuerelement in eine Galerie-Vorlage: YAML mit einem Kind der Vorlage markiert einfügen.
- Ein neu hinzugefügter Flow behält manchmal seinen alten Namen (`aRG_Foto_hochladen`).
- `Concat(Filter(coll As x; …); x.Feld; …)` ist ungültig (`x` gilt nur im Filter). Stattdessen ohne `As`.
- `ThisItem.FotoMoeglich` kam aus `colAntworten` nicht an (leer). Lösung: direkt `LookUp(colPP; ID = ThisItem.PruefpunktID).FotoMoeglich` benutzen. Ursache ungeklärt (Hinweis für den Umbau: Feldübernahme in `colAntworten` im `OnVisible` prüfen).
- Formelleiste ist deutsch: Argumente mit `;`, Dezimalkomma, Ketten mit `;;`. YAML ist englisch: Argumente mit `,`, Ketten mit `;`.
- Property-Dropdown in Studio hat keine Texteingabe. Immer scrollen und klicken.
- App-Check: „Barrierefreiheit“ (~80) und „Leistung“ (~12) sind bekannte, dokumentierte Hinweise (E-07/E-08 in ENTSCHEIDUNGEN.md), „Formeln“ muss 0 sein.
**SharePoint**
- Der Abruf `…/items?$top=500` genügt für die Testgröße. Für große Datenmengen auf Delegation achten (Filter/LookUp auf SharePoint sind begrenzt delegierbar).
- `Refresh(<Liste>)` vor Lesen, um den Sitzungs-Cache zu umgehen.
- Zeitzonen: Datumswerte als UTC-Vortag-22:00 gespeichert.
- Per Chrome-Konsole lassen sich Listen über REST lesen/ändern (digest über `/_api/contextinfo`), Papierkorb über `/items(id)/recycle()`. Das Tab muss auf `…sharepoint.com` stehen.
**Chrome-Werkzeug**
- Studio lässt sich über Claude in Chrome bedienen (Koordinaten aus Screenshots). Die Datei-Auswahl (Foto hochladen) ist **nicht** bedienbar: die Vorschau liegt in einem fremden Frame. Foto-Tests muss Josias machen.
- Lokaler Hilfsserver `C:\rundgang_work\bau\werkzeuge\ablage_server.js` (Port 8765): `/<datei>` zeigt eine Datei mit „KOPIEREN“-Knopf (Zwischenablage), `/empfang` speichert eingefügten Text. Praktisch, um lange Formeln in die Formelleiste zu bringen (Seite öffnen, Knopf klicken, in Studio Strg+A, Strg+V).

## 6. Stand der Funktionen
Fertig und in der veröffentlichten App (Stand 27.10. 08:06): Plan nach KW/Wochentag/Zyklus, Kategorien nacheinander, Typen IO/NIO, Zahl, Auswahl, Text, Pflichtprüfung und „Offene Punkte“-Sprung, Speichern mit Nachlese, automatisches Weiterspringen, Mängel beim Abschluss, Protokoll als HTML, PDF-Archiv (Studio-Test erfolgreich), Banner für offene frühere Rundgänge, Zurücksetzen für Admins, Foto-Knopf bei n.i.O. oder `FotoMoeglich = Ja`.
**Ungeprüft / offen:**
- **Foto-Upload** (Datei wählen → `RG_Fotos`) ist noch **nicht** getestet. Josias testet.
- Optik: Knopftext „Foto aufnehmen / auswählen“ im Foto-Fenster ist sehr groß; die Reihenfolge ✕-Knopf/Bild in `galKaFotoNeu` ist nicht verifiziert.
- Flow `RG_Protokoll_archivieren`: Zwischendatei in `/RG_Temp` wird nicht gelöscht.
- Outlook-Protokollmail (Paket CP2) nicht gebaut (braucht Josias’ Ok für die Verbindung).
- Tablet-Test auf den echten Geräten (J1) fehlt.
- Rechte der Bibliotheken, Aufbewahrung der PDFs (QM/IMS fragen).
- Der Dienstags-Testplan in `RG_Plan` und der Testlauf D13 müssen aufgeräumt werden.

## 7. Die Aufträge für den Engineering-Chat (Reihenfolge)
Josias hat diese Baukasten-Funktionen freigegeben („gut“):
1. **Foto-Auswahl pro Prüfpunkt:** `FotoMoeglich` (Ja/Nein) wird zu einer Auswahlspalte `Foto` mit `Aus | Optional | Pflicht`. Bei `Pflicht` ist Speichern erst mit mindestens einem Foto möglich (Eintrag in „Noch offen“ und in `fnFehlt`).
2. **Pflicht-Kommentar auch bei i.O.** (pro Prüfpunkt wählbar).
3. **Hinweistext mit Bild/Beispielfoto** (Bild aus einer Bibliothek, in der Karte aufklappbar).
4. **Zahlengrenzen mit Warnung statt Sperre** (pro Prüfpunkt: sperren oder warnen).
5. **Bedingte Fragen:** Prüfpunkt B nur zeigen/verlangen, wenn Prüfpunkt A einen Wert (z. B. n.i.O.) hat.
6. **Mehrfachauswahl** und **Datum-/Uhrzeitfeld** als neue Typen.
7. **Rundgang kopieren** (als Vorlage), mit richtiger Neuverknüpfung der IDs (Bereiche → Kategorien → Prüfpunkte, Plan).
8. Dann: Listen mit **Nachschlagespalten** statt Zahlen und danach die **Pflege-App** (siehe 9).
Bei jedem Schritt: Listen ändern → App-Formeln → Pflichtprüfung (`fnFehlt`) → Speichern/JSON → Mängel → Protokoll (HTML/PDF) → Testrundgang → Josias testet → veröffentlichen.

## 8. Wichtige Nutzer-Entscheidungen
- Prüfer sind nicht verlässlich (viele tippen „gzgz“). **Keine** „alles i.O.“-Abkürzung, keine Knöpfe, die Pflichtfelder umgehen (CP3 wurde verworfen, E-09). Immer Kontrollen statt Abkürzungen.
- Protokolle müssen **archiviert** werden (PDF in SharePoint, nicht nur Mail).
- Fotos beim Prüfpunkt, hochgeladen beim Speichern.
- Eine **Test-/Entwicklungsumgebung** soll bleiben (Testmodus, `TestDatensatz`).
- Josias will eine Oberfläche, mit der man Rundgänge „durchklickend“ erstellt (siehe 9) und möglichst viele Baukasten-Funktionen.

## 9. Ideen für die Zukunft und die Pflege-App („Rundgang-Builder“)
**Ziel:** Rundgang erstellen, ohne SharePoint-Zahlen zu kennen. Die Builder-App und die Rundgang-App sind **zwei Apps über denselben Daten**; die Daten sind die Schnittstelle.

**Designprinzipien, damit beide Apps zusammenpassen und leicht änderbar bleiben**
1. **Daten sind der Vertrag.** Ein einziges, versioniertes Schema (z. B. `RG_Konfiguration`: `SchemaVersion=n`). Die Rundgang-App prüft die Version und warnt, wenn sie zu alt ist. Die Builder-App schreibt nur Daten, die zu dieser Version passen.
2. **Eigenschaften als Daten, nicht als Code.** Jede neue Funktion (Foto-Modus, Pflicht-Kommentar, Grenzen warnen/sperren, Bedingung) ist eine **Spalte am Prüfpunkt**, die die Rundgang-App liest. Neue Funktion = neue Spalte + eine Zeile in der App, nicht ein neuer Rundgang-Typ im Code.
3. **Typen als Register.** Eine Liste `RG_Typen` (oder ein JSON in der Konfiguration) beschreibt jeden Eingabetyp: Name, Felder, die Eingabemaske, Pflichtregel. Die Rundgang-App rendert nach dem Register. Neue Typen werden zuerst im Register ergänzt.
4. **Verknüpfen mit Nachschlagespalten** (oder stabilen GUID-Schlüsseln) statt freier Zahlen, damit nichts falsch verknüpft wird und Kopieren leicht ist. Beim Kopieren IDs neu vergeben (Zuordnungstabelle alt→neu).
5. **Entwurf und Veröffentlichung trennen.** Ein Rundgang hat einen Status `Entwurf | Aktiv | Archiviert`. Die Rundgang-App zeigt nur `Aktiv`. Der Builder erlaubt Änderungen nur am Entwurf und prüft vor dem Aktivieren (jede Kategorie hat ≥ 1 aktiven Prüfpunkt, Reihenfolge lückenlos, gültiger Plan, Bedingungen verweisen auf vorhandene Punkte).
6. **Nie löschen, sondern deaktivieren.** Alte Ergebnisse bleiben lesbar, weil die Antworten den Fragetext mitspeichern.
7. **Schnappschuss im Ergebnis.** Beim Start einer Durchführung steht die Kategorienliste schon im Datensatz (`KategorieListe`). Der Weg lässt sich auf Prüfpunkte ausdehnen (Schnappschuss der Frage-Definition), damit spätere Änderungen laufende Rundgänge nicht verändern.
8. **Vorlagen:** Ein Rundgang kann als Vorlage markiert und kopiert werden. Das Kopieren läuft als Flow (Konto-gebunden, mit Zuordnungstabelle) oder in der Builder-App.
9. **Prüfungen in einem Bericht:** Die Builder-App zeigt eine Prüfliste („Rundgang ist aktivierbar: ja/nein, weil …“) statt stiller Fehler.
10. **Berechtigungen:** Builder nur für eine Pflegegruppe, Rundgang-App für alle Prüfer. Daten der Stammdaten für Prüfer nur lesend.

**Builder-App, Bildschirme (Vorschlag):** Rundgangsliste → Rundgang (Name, Beschreibung, Plan) → Bereiche und Kategorien (Sortieren per Auf/Ab) → Prüfpunkte (Typ, Pflicht, Foto-Modus, Grenzen, Auswahlwerte, Hinweis/Bild, Bedingung, Vorschau der Karte) → Plan → Prüfen & Aktivieren → Kopieren.
**Reihenfolge der Entwicklung:** (1) Baukasten-Funktionen in der Rundgang-App (siehe 7), (2) Listenumbau auf Nachschlagespalten und Statusfeld, (3) Kopier-Flow, (4) Builder-App.

**Weitere Ideen (aus `pakete\IDEEN_PAKETE.md`, Auswahl):** Foto-Pflicht und Foto-Kennzeichnung, Offline-Fähigkeit (Power Apps Offline für Tablet, Funkloch im Keller), Mängelverfolgung mit Fristen/Verantwortlichen und Erinnerungsmail, Wochenbericht, Kennzahlen (n.i.O.-Quote pro Bereich), Sprachnotiz als Kommentar, QR-Code zum direkten Starten eines Rundgangs, Unterschrift beim Abschluss, Outlook-Protokollmail (CP2, noch Josias’ Ok nötig).

## 10. Erste Schritte für den Engineering-Chat
1. `FORTSCHRITT.md`, `ENTSCHEIDUNGEN.md`, `FEATURES.json` lesen. Dann diese Datei mit dem Zustand der App in Studio abgleichen.
2. In Studio die Bildschirme öffnen, App-Check (Formeln) ausführen, in der Vorschau einen Testlauf machen (Test-Rundgang am Dienstag/Sonntag).
3. Josias nach dem Ergebnis seines Foto-Tests fragen.
4. Mit Auftrag 1 (Foto-Auswahl Aus/Optional/Pflicht) beginnen, in dieser Reihenfolge: SharePoint-Spalte → `colAntworten`/`OnVisible` → `fnFehlt` → Karte → Speichern → Test → veröffentlichen.
5. Nach jedem Schritt dokumentieren (`FORTSCHRITT.md`) und committen.
