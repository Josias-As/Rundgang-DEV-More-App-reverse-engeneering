# Übergabe an einen neuen Chat: App durchtesten (06.11.2026)

Von: Einsetz-Chat. Josias will beide Apps jetzt gründlich testen.

## Die zwei Apps
- **Rundgang DEV** (Prüfer-App, App-ID 1b9800f7-8289-4ee8-b720-cef0bbf1eae1): Bildschirme scrStart, scrRundgang, scrKategorie, scrProtokoll, scrArchiv.
- **Rundgang Builder** (Pflege-App): scrListe, scrEditor, scrPlan, scrKontakte (Ansprechpartner), scrAnleitungen.
- Daten: SharePoint-Site IMS+ https://technoformgroup.sharepoint.com/sites/IMSKonzept, Listen RG_Rundgaenge, RG_Bereiche, RG_Kategorien, RG_Pruefpunkte, RG_Plan, RG_Durchfuehrungen, RG_KategorieErgebnisse, RG_Maengel, RG_Konfiguration, RG_Ansprechpartner, RG_Anleitungen, Bibliotheken RG_Hinweisbilder, RG_Fotos.
- Repo des Engineering-Chats (Pakete, Werkzeuge): Josias-As/Rundgang-DEV-More-App-reverse-engeneering, Branch claude/upbeat-tesla-emx06l.

## Stand
Alle gebauten Pakete sind in beiden Apps eingefügt (nicht in Studio getestet, nur App-Prüfung):
- Rundgang DEV: N, 8–10, 19, 20, 21, 22, 12+16, 14+15, 17, 13.
- Builder: 8, 9, 12+16, 14+15, 13 (+ Korrekturen OnStart, btnVsIO.Text, ddPKategorie.Width 340, lblGlHilfe.Y 32).
- Letzter geprüfter Export: 03.11. 15:11 (danach eingefügt: 14+15, 17, 13 – noch kein Export-Abgleich).

**Einziger offener Fehler:** Rundgang DEV, `imgKaInfo.Image` (ⓘ-Fenster): „Thumbnail wird nicht erkannt“. Gleiche Formel wie im funktionierenden `imgKaBild.Image`. Vorübergehend `Blank()`. Prüfidee: Ist imgKaBild.Image grün? Schlägt Studio nach `First(RG_Hinweisbilder).` das Feld Thumbnail vor? Sonst Datenquelle neu hinzufügen bzw. Formel von Hand neu tippen.

## Funktionen (was getestet werden soll)
- Antworttypen: i.O./n.i.O., Auswahl, Mehrfach („(mehrere möglich)“), Text, Zahl, Datum, Datum+Uhrzeit (Stunde/Minute einzeln, „08:--“ als Zwischenstand).
- Zahl: Grenzmodus Mangel / Warnen (Begründung) / Sperren (nicht speicherbar), „nicht messbar“ (Begründung Pflicht, kein Mangel).
- Eigene Knopfwörter (TextIO/TextNIO, z. B. „durchgeführt / nicht durchgeführt“, zählt wie n.i.O.).
- Foto: Aus / Optional / Pflicht / Bei Mangel Pflicht. Beispielbild (HinweisBildID).
- Bedingte Folgefragen (bei NIO, bei Auswahlwert, bei „*“ = jede Antwort).
- Abschnitte (Überschrift über der ersten Frage), Bereich ausblenden.
- Rückfrage „Ist das wirklich so?“, kritischer Mangel (rotes Fenster mit Ansprechpartnern, Bestätigung Pflicht).
- Kategorien in beliebiger Reihenfolge (▶ Als Nächstes, ○ Offen), Abschluss erst wenn alle gespeichert.
- Abweichung zum letzten Lauf (AbwMax absolut/%, NurSteigend) und Vergleich zweier Zahlen (VergleichPunkt/Tol) – braucht zwei abgeschlossene Läufe an zwei Tagen.
- Archiv (Startseite „🗂 Archiv“, Testläufe nur mit Häkchen), Anleitungen über ⓘ.
- Protokoll: Abschnitte, eigene Wörter, „nicht messbar“, Abweichung, „KRITISCH – Bescheid gegeben …“.
- Builder: Ansprechpartner, Anleitungen, „Bei n.i.O.“-Fenster, „Verlauf/Vergleich“-Fenster, Knopf-Wörter, „nicht messbar erlaubt“, Abschnitt-Feld, Fassungen (neue Fassung → aktivieren), Kopie.

## Testdaten (alles „ZZ Test“ → TestDatensatz = Ja)
- **ZZ Test Funktionsrundgang** (Skript bau/probe/funktionsrundgang_anlegen.js): Rundgang 4, Bereiche 21–23 (C ausgeblendet), Kategorien 42–48, Prüfpunkte 270–300, Pläne 11–17 (jeden Tag). Jede Funktion mit erklärendem Hinweistext. Testanleitung „ZZ Test Feuerlöscher prüfen“ an „Prüfplakette Feuerlöscher lesbar“.
- **ZZ Test Infrastrukturrundgang**: Rundgang 3, Kategorien 9–19, Prüfpunkte 39–115, Plan 10. Prüfpunkt 39 kritisch + Rückfrage (Elektriker), Abschnitte bei Kompressoren/Kältemaschinen.
- **ZZ Test Objektrundgang TCC**: ursprünglicher Testrundgang (Datum, Mehrfach, Folgefragen).
- RG_Ansprechpartner: Allgemein (bei jedem), Elektriker (ID 2), IT-Dienstleister – alle „ZZ Test“.
- Je Rundgang und Tag nur eine Durchführung.

## Arbeitsregeln (wichtig)
- Formelleiste ist deutsch (`;` und `;;`), YAML-Blöcke englisch (`,` und `;`).
- Antwortformat, das Josias will: **Steuerelement** · Property, darunter ein Codeblock nur mit dem einzufügenden Code. Wenig Text.
- YAML einfügen: Container selbst markieren → Strg+V (bei Galerievorlage ein Kind der Vorlage markieren). Danach prüfen, dass Y/Height/X noch Formeln sind.
- „Daten hinzufügen“ nur, wenn **kein** Steuerelement ausgewählt ist – sonst landet der Listenname in einer Property (ist zweimal passiert: htmProtokoll, tmrArbeit.Duration – dort muss 100 stehen).
- Export enthält nur die veröffentlichte Fassung → vor Export veröffentlichen.
- Keine Formeln selbst ändern; Fehler mit genauer Stelle an den Engineering-Chat. Nur Testdaten, nichts an anderen Flows/Apps, keine Passwörter, Mails nur im Testmodus.
- SharePoint-Änderungen per Konsolen-Skript (IMS+ → F12 → Konsole), immer „nur anlegen, was fehlt“, Ausgabe FERTIG/FEHLER.

## Offen (keine Pakete, warten auf Josias)
- Paket 11: Prüferauswahl (gemeinsames Konto? wer pflegt Prüferliste?), Unterschrift, Kopfdaten (Kunde/Adresse).
- Paket 18: Zugangsdaten (Bedien-PIN oder sensibel?).
- Echte Rundgänge anlegen (Infrastruktur, Haustechnik, Legionellen, Gefahrstoffschränke) – Infos fehlen (Bilder 10–16, Grenzwerte, Aufteilung).
- Aufräumen später: Testrundgänge 3 und 4, Testpläne, Testergebnisse (TestDatensatz = Ja).
