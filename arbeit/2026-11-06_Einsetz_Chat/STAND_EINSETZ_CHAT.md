# Stand Einsetz-Chat – Protokoll aller Einbau-Schritte (02.–06.11.2026)

Geschrieben vom Einsetz-Chat (Claude, Josias' Hauptkonto) als Übergabe, weil Josias auf einen anderen Account wechselt.
Ein neuer Einsetz-Chat soll **diese Datei zuerst lesen**, dann `CLAUDE.md`, dann das nächste Paket.

Kennzeichnung: **belegt** = durch Export-Abgleich oder SharePoint-Abfrage geprüft · **laut Josias** = von Josias gemeldet, nicht per Export geprüft.


## 0. NACHTRAG 06.11. später (zuerst lesen)

- **Paket 23 komplett eingefügt** (laut Josias): Teil A (DEV) geprüft – btnStartOffenWeiter da, btnRgAktion nutzt Testrundgang, conStartOffen filtert Testläufe; Banner zeigt nur noch Lauf 19 (Haustechnik). Teil B (Builder) ausgegeben, Josias hat „next“ geschrieben (App-Prüfung Builder nicht ausdrücklich gemeldet).
- Spalten-Skript Paket 23: FERTIG – Testrundgang = Ja für 1, 3, 4; Haustechnik (2) nicht.
- **Haustechnik Rundgang (ID 2): echt, aber noch nicht final** → im Builder unter Plan auf „✓ Testrundgang“ setzen bis Inbetriebnahme. Offener Lauf 19 zählt als echt (bleibt im Banner) – Josias wurde angeboten, ihn per Skript auf TestDatensatz = Ja + Abgeschlossen zu setzen (Antwort offen).
- Testläufe 18, 20, 21, 22: Josias will abschließen/löschen → Skript (setzt Status Abgeschlossen + EndeZeit, nur wenn TestDatensatz = true) ausgegeben; FERTIG-Meldung offen.
- **Paket 18 begonnen:** SharePoint-Skript skripte/paket18_sharepoint.js (Liste RG_Zugangscodes + Testcode „ZZ Test Bedienfeld Kältemaschine“ 1234, Spalte ZugangscodeID) + A2.1/A2.2 (btnKaCode, conKaCode) ausgegeben. Weiter mit A3.1 (scrKategorie.OnVisible), A3.2, dann Teil B.
- **Paket 18 eingefügt (beide Apps):** Teil A + Teil B komplett. Builder hatte danach 262 Fehler (RG_Zugangscodes fehlte als Datenquelle, RG_Pruefpunkte nicht aktualisiert) → Daten hinzugefügt/aktualisiert → Fehler 0. Offen: speichern/veröffentlichen + Kurztest (🔑 im Builder setzen, in der App „1234“ sehen). Weiter mit Paket 11, dann 24.
- **Neu im Repo: Paket 24** (ein Info-Knopf ⓘ für Anleitung und Bild, Wunsch Josias). Kette: 23 → 18 → 11 → **24**.
- Entscheidungen Josias: B2–B5 aus TESTLAUF später einzeln durchgehen. Feste Reihenfolge/Sperre: nicht bauen. Flow-Rückmeldungen (Foto-Upload, Archiv-PDF, Mängel-Mail, Unterschrift) nur später und nur wenn nicht aufwendig. Prüfpunkte verschieben gibt es schon (↑↓, Feld Kategorie, Feld Bereich) – Josias ggf. fragen, ob „an bestimmte Stelle verschieben“ gewünscht ist.

---

## 1. Wo wir stehen (06.11.2026, Nachmittag)

| App | eingefügt | offen (in dieser Reihenfolge) |
|---|---|---|
| **Rundgang DEV** | N, 8–10, 19, 20, 21, 22, 12+16 (**belegt**, Export 03.11. 15:11) · 14+15, 17, 13, A1-Fix (**laut Josias**, App-Prüfung 0) · **Paket 23 Teil A: Formeln ausgegeben**, Rückmeldung (FERTIG des Spalten-Skripts, App-Prüfung) steht aus | **23 Teil A abschließen** → 18 → 11 |
| **Rundgang Builder** | 8, 9, 12+16 (**belegt**, Export 15:11, bis auf 4 Nachkorrekturen, die danach eingefügt wurden) · 14+15, 13, A2-Knopf (**laut Josias**) | **23 Teil B** → 18 → 11 |

Kette (Engineering): … 13 → **23 → 18 → 11**. Alle drei sind unabhängig geprüft und freigegeben, nicht in Studio getestet.

**Nächster konkreter Schritt:** Josias fragen, ob `skripte/paket23_sharepoint.js` FERTIG gemeldet hat (Spalte `RG_Rundgaenge.Testrundgang` + Testrundgang = Ja für alle „ZZ Test …“) und ob die App-Prüfung nach Teil A bei 0 ist. Dann `PAKET_23_BANNER_TEST_KONTAKTE.md` Teil B (Builder) ausgeben.

**Noch kein Export-Abgleich** nach 14+15, 17, 13, 23. Nach Paket 23 (oder spätestens nach 11) beide Apps veröffentlichen, exportieren und gegen die Kette abgleichen (Werkzeug `werkzeuge/abgleich_app.py` bzw. das Node-Skript des Einsetz-Chats, siehe Abschnitt 6).

---

## 2. Chronik

### 02.11.
- Analyse der 4 MoreApp-PDFs (Haustechnik, Infrastruktur, Legionellen, Gefahrstoffschränke) → Übergaben an Analyse-Chat (`C:\rundgang_work\UEBERGABE_NEUE_ANFORDERUNGEN_2026-11-02.md`, `UEBERGABE_SPERRE_UND_STANDFRAGE_2026-11-02.md`).
- Empfehlung Benutzerwechsel am iPad: gemeinsames Gerätekonto + Prüferauswahl + Unterschrift → später Paket 11.
- **Probe-Rundgang** „ZZ Test Infrastrukturrundgang“ per Konsole (`skripte/probe_infrastruktur_anlegen.js`): Rundgang 3, Plan 10, Bereiche 6–10, Kategorien 9–19, Prüfpunkte 39–115 (**belegt**).
- Paket N (Nachholen) ausgegeben.

### 03.11.
- Export 09:59 zeigte: Paket N zu 85 % – fehlten N.2.1 (`lblKaHinweis.Text` hatte die Foto-Formel), N.3.1 (`lblKaFotoHinweis.Text`), N.2.2, N.2.3, Kombinationsfeld hieß `ComboBox1` → nachgeholt, umbenannt in `cboKaMehrfach`.
- **Builder Paket 8 Schritt 2–5** ausgegeben (waren nicht eingefügt, nicht nur unveröffentlicht).
- **Paket 8–10 App**: SharePoint per `skripte/paket8_10_sharepoint.js` – FERTIG: RG_Ansprechpartner angelegt (+ 3 Testzeilen, Elektriker = ID 2), 5 Spalten an RG_Pruefpunkte, Prüfpunkt 39 kritisch + Rückfrage, Abschnitt bei 27 Punkten (**belegt**). Danach alle Formeln/YAML eingefügt.
- **Fehler in Studio gefunden → Pakete 19, 20, 21** (Engineering):
  - Datum speicherte nicht (unsichtbare Combobox/Dropdown überschrieben `WertText`) → Paket 19, bestätigt.
  - Stunde/Minute sprangen zurück → Paket 20 (Platzhalter `08:--`) → reichte nicht → Paket 21 (jedes Feld ändert nur seinen Teil). **In Studio bestätigt.**
  - Wunsch Josias „(mehrere möglich)“ hinter Mehrfach-Fragen → Paket 22.
- **Builder Paket 9** eingefügt. Dabei:
  - 267 Fehler → Ursache: `RG_Ansprechpartner` fehlte als Datenquelle.
  - danach 1 Fehler: lange Formel in `tmrArbeit.Duration` statt `OnTimerEnd` gelandet → Duration = 100.
  - **Eigener Fehler des Einsetz-Chats:** In der ausgegebenen P8-Fassung von `tmrArbeit.OnTimerEnd` stand im Zweig „zurueck“ `Set(varJob; "");` statt `;;`. Mit P9 (ganze Formel ersetzt) behoben.
- **Paket 12+16** in beiden Apps (Spalten per `skripte/paket12_16_sharepoint.js`).
- Export 15:11 abgeglichen (**belegt**): DEV sauber. Builder: 4 Nachkorrekturen nötig – `App.OnStart` (P9 Schritt 1 fehlte), `btnVsIO.Text`, `ddPKategorie.Width` 340, `lblGlHilfe.Y` war versehentlich 140 → 32. Josias hat sie eingefügt (laut Josias).
- **„ZZ Test Funktionsrundgang“** gebaut (`skripte/funktionsrundgang_anlegen.js`): zeigt jede Funktion, sinnvoll gruppiert.

### 06.11.
- Funktionsrundgang existierte schon (vor der Pause ausgeführt): Rundgang 4, Bereiche 21–23 (C ausgeblendet), Kategorien 42–48, Prüfpunkte 270–300 (31, kein Beispielbild, weil RG_Hinweisbilder damals leer), Pläne 11–17 (jeder Wochentag) (**belegt**).
- **Paket 14+15** in beiden Apps (Spalten per `skripte/paket14_15_sharepoint.js`).
- **Paket 17** (Archiv) in DEV.
- **Paket 13** in beiden Apps (Liste/Spalte + Testanleitung per `skripte/paket13_sharepoint.js`).
  - „Daten hinzufügen“ bei ausgewähltem `tmrArbeit` → `RG_Anleitungen` in `tmrArbeit.Duration` → wieder 100.
  - `imgKaInfo.Image` Fehler „Thumbnail wird nicht erkannt“ → **A1:** in der deutschen Formelleiste heißt das Feld `Miniaturansicht` → behoben (Engineering übersetzt das jetzt im Generator).
- **Code-Prüfung** durch Test-Chat: `TESTLAUF_2026-11-06.md` (liegt hier). A2 (Knopf `btnLiAnleitungen` fehlte) war Einfügefehler → nachgeholt.
- SharePoint-Abfrage (**belegt**): RG_Hinweisbilder hat Bild 1 und 2; Funktionsrundgang hat **Fassung 2** aktiv (neu angelegt von Josias): „Prüfplakette Feuerlöscher lesbar“ = Prüfpunkt **315** in Kategorie **49**, `HinweisBildID` 2, `AnleitungID` 1. Alte Fassung 1 (Prüfpunkt 272, Kategorie 42) inaktiv.
- Offene Durchführungen (**belegt**, Konsole): ID 18, 20, 21, 22 = ZZ-Test-Läufe (InArbeit, TestDatensatz true); **ID 19 „Haustechnik Rundgang“ vom 02.11., TestDatensatz false** – Josias klärt, ob Test.
- Entscheidungen Josias zu **Paket 11 und 18** an Engineering gegeben (Gerätekonto, alle Mitarbeiter dürfen prüfen: Liste + Firmenverzeichnis-Suche, Unterschrift Pflicht, Kopfdaten je Rundgang; Kältemaschinen-Code ist nur Bedien-Code). Engineering hat 11, 18, 23 gebaut, geprüft, freigegeben.
- **Paket 23 Teil A** (DEV) ausgegeben inkl. `skripte/paket23_sharepoint.js`.

---

## 3. Testdaten (alle TestDatensatz = Ja bzw. „ZZ Test“)

| Was | IDs |
|---|---|
| ZZ Test Objektrundgang TCC | Rundgang 1 (ursprünglicher Testrundgang) |
| ZZ Test Infrastrukturrundgang | Rundgang 3, Plan 10, Bereiche 6–10, Kategorien 9–19, Prüfpunkte 39–115 |
| ZZ Test Funktionsrundgang | Rundgang 4; Fassung 1: Bereiche 21–23, Kategorien 42–48, Prüfpunkte 270–300; **Fassung 2 (aktiv)**: Bereiche ab 24, Kategorien ab 49, Prüfpunkte ab 301; Pläne 11–17 |
| RG_Ansprechpartner | 3 Testzeilen (Allgemein, Elektriker = 2, IT-Dienstleister) |
| RG_Anleitungen | 1 „ZZ Test Feuerlöscher prüfen“ |
| RG_Hinweisbilder | 1, 2 |
| Offene Läufe | 18, 20, 21, 22 (Test), 19 (Haustechnik, unklar) |

Aufräumen später (nur mit Josias' Ja): obige Rundgänge inaktiv, Testläufe/Ergebnisse/Mängel über TestDatensatz = Ja, Testordner in RG_Fotos.

---

## 4. Arbeitsregeln (aus der Praxis, wichtig)

- **Antwortformat (neu, 06.11.):** Ganz oben einmal „App: Rundgang DEV“ bzw. „App: Rundgang Builder“. Je Block nur eine Zeile mit Farbmarker + **Steuerelement** · Property bzw. Einfügeziel, kein Erklärtext. Legende: 🟦 Formel ersetzen · 🟩 neu einfügen (YAML, Ziel markieren → Strg+V) · 🟧 SharePoint-Konsolen-Skript · 🟨 Daten in Studio (aktualisieren/hinzufügen, nichts ausgewählt) · 🟥 danach prüfen. Kopierblöcke nur mit dem einzufügenden Inhalt.
- **Antwortformat für Josias:** `**Steuerelement** · Property`, darunter ein Codeblock **nur** mit dem einzufügenden Code. Wenig Text. Eine Gruppe je Nachricht, Josias antwortet „next“.
- Formelleiste **deutsch** (`;` und `;;`), YAML **englisch** (`,` und `;`). Ganze Property ersetzen, nie Teile.
- **YAML einfügen:** Container/Bildschirm selbst markieren → Strg+V (bei Galerievorlage ein Kind der Vorlage, z. B. `txtKaZahl`). Danach prüfen, dass X/Y/Height noch **Formeln** sind (Studio friert sie manchmal als Zahl ein).
- **„Daten hinzufügen“ nur ohne ausgewähltes Steuerelement** – sonst schreibt Studio den Listennamen in die gerade gewählte Property (passiert: `htmProtokoll`, `tmrArbeit.Duration` zweimal; Duration muss 100 sein).
- **Bei vielen Fehlern auf einmal:** meist fehlende/nicht aktualisierte Datenquelle. Zuerst Daten prüfen, dann die ersten 3–5 Meldungen ansehen.
- **Lange Formeln** zusätzlich als Datei bereitstellen (Josias kopiert mit Strg+A/Strg+C), `OnTimerEnd` ausdrücklich nennen („nicht Duration“).
- Export enthält nur die **veröffentlichte** Fassung → vor Export veröffentlichen.
- **Keine Formeln selbst bauen** – Fehler mit genauer Stelle an Engineering; jedes Paket wird vor Freigabe unabhängig geprüft.
- **SharePoint per Konsolen-Skript** (IMS+ → F12 → Konsole; ggf. `allow pasting`): nur anlegen, was fehlt; nichts löschen; Ausgabe FERTIG/FEHLER. Skripte liegen in `skripte/` und bei Josias unter `C:\rundgang_work\bau\probe\`.
- Nur Testdaten; keine Passwörter/MFA; Zustimmungsdialoge nur mit Josias' Ja; Obsidian-Vault nicht schreiben.

---

## 5. Offen / Fragen

- Paket 23 Teil A Rückmeldung, dann Teil B; danach 18, dann 11 (Paket 11: Vorab-Test V1 direkt nach Einfügen der Stifteingabe, V2–V4 nach komplettem Paket mit einem Testlauf).
- Für echten Einsatz von Paket 11: IT/Michael – Gerätekonto, Lizenz, Rechte IMS+, Connector „Office 365-Benutzer“ (DLP). Testen geht mit Josias' eigenem Konto.
- Fehlerliste `TESTLAUF_2026-11-06.md`: nach 23 noch offen A3, A5, A9, A12, A13; später A10, A14; C als Aufräum-Paket; **D1** (Komma/Punkt bei Zahlen) am Tablet testen; B2–B5 entscheidet Josias.
- ID 19 „Haustechnik Rundgang“: Test oder echt? Wenn Test: sauber aus echten Daten entfernen (Engineering fragen).
- Vier ZZ-Testläufe (18, 20, 21, 22): in der App abschließen oder per Skript auf „Abgeschlossen“ setzen – Frage an Engineering/Josias offen.
- Echte Rundgänge anlegen: Infos fehlen (Bilder 10–16, Grenzwerte, Aufteilung Infrastrukturraum, Formularbilder der anderen drei).
- Wunsch (nicht bestellt): eigene Bilder in Anleitungen (heute nur Text + Beispielbild des Prüfpunkts).

---

## 6. Abgleich-Methode des Einsetz-Chats (ohne Python)

Auf Josias' Rechner gibt es kein Python. Der Einsetz-Chat hat Exporte mit einem Node-Skript abgeglichen: `pa.yaml` aus dem `.msapp` entpacken, Properties je `Steuerelement.Property` einlesen, gegen die Nachher-Blöcke der eingefügten Pakete (deutsch → englisch übersetzt) und gegen die Vorher-Blöcke der offenen Pakete (Anhang „Vorher-Fassungen“) vergleichen. Ergebnis 03.11. 15:11 siehe Abschnitt 2. Für den nächsten Abgleich besser `werkzeuge/abgleich_app.py` hier im Repo laufen lassen (Engineering).

## 7. Startprompt für einen neuen Einsetz-Chat

```
Du bist der Einsetz-Chat für meine zwei Power-Apps (Rundgang DEV, Rundgang Builder). Repo: Josias-As/Rundgang-DEV-More-App-reverse-engeneering, Branch claude/upbeat-tesla-emx06l. Lies zuerst arbeit/2026-11-06_Einsetz_Chat/STAND_EINSETZ_CHAT.md, dann CLAUDE.md. Du baust nichts neu und änderst keine Formel – du führst mich durch das Einfügen der freigegebenen Pakete (als Nächstes Paket 23 Teil B, dann 18, dann 11). Pro Nachricht eine Gruppe, ich antworte „next“. Format: **Steuerelement** · Property, darunter ein Codeblock nur mit dem Code. SharePoint-Änderungen als Konsolen-Skript. Am Ende sag mir, was ich dem Engineering-Chat schicken soll.
```
