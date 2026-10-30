# Übergabe v2: Einbau der Baukasten-Pakete 1–6 in „Rundgang DEV“ (30.10.2026 abends)

Ersetzt `UEBERGABE_an_Einsetz_Chat.md`. Von: Engineering-Chat (Repo `Rundgang-DEV-More-App-reverse-engeneering`, Branch `claude/upbeat-tesla-emx06l`).

## 1. Was neu gebaut wurde (sechs Pakete, nur der Reihe nach einsetzen)
| Paket | Inhalt |
|---|---|
| 1 | Foto-Modus pro Prüfpunkt (Aus / Optional / Pflicht). Behebt den Fehler „FotoMoeglich kam aus colAntworten nicht an“: Der Bearbeiten-Zweig von `scrKategorie.OnVisible` legte das Feld nie an. Jetzt haben alle drei Zweige dieselben Felder. |
| 2 | Pflicht-Kommentar auch bei i.O. (pro Prüfpunkt, Spalte `KommentarPflicht`) |
| 3 | Zahlengrenzen pro Prüfpunkt: Mangel / Warnen (i.O., aber Begründung Pflicht, kein Mangel) / Sperren (Wert außerhalb lässt sich nicht speichern). Spalte `Grenzmodus`. |
| 4 | Bedingte Fragen: Frage B nur, wenn Frage A einen Wert hat (Spalten `BedingungPunkt`, `BedingungWert`). Speichern aus einer Kopie (`colSpeichern`), ausgeblendete Fragen im JSON mit `Ausgeblendet`. |
| 5 | Neue Typen MEHRFACH, DATUM, DATUMZEIT: vier YAML-Steuerelemente (`dpKaDatum`, `ddKaStunde`, `ddKaMinute`, `btnKaDatumLeeren`) plus `cboKaMehrfach` per Menü (Einfügen → Klassisch → Kombinationsfeld). |
| 6 | Beispielbild am Prüfpunkt: neue Bibliothek `RG_Hinweisbilder`, Spalte `HinweisBildID`, Knopf „Bild“ und Fenster `conKaBild`. |

Alle Blöcke sind aus dem Export vom **27.10.2026 09:09** erzeugt (`quellen/2026-10-27_Export0909/`) und unabhängig geprüft (drei Runden, dazu eine gezielte Runde für Paket 3+4). **Nicht in Studio getestet (UNSICHER):** `UpdateIf` mit Feldverweisen (Paket 3), `Patch(Datensatz; Datensatz)` in `ForAll` (Paket 4), Vorschaubilder der Bibliothek (Paket 6), Kamera und Upload.

## 2. Wo wir stehen
| Paket | Stand |
|---|---|
| 1 | eingefügt. Test: **A1 und A2 ok**, A3 bis A10 und Teil B (Tablet, Foto) **nicht gemacht**. App-Prüfung (Formeln = 0) nicht ausdrücklich bestätigt. |
| 2 | eingefügt (Josias schrieb „next“). Nicht getestet. |
| 3 | eingefügt. Josias hatte die Spalte `Grenzmodus` erst vergessen (Rot bei `Grenzmodus.Value`), danach nachgeholt. Nicht getestet. |
| 4 | geliefert, Josias schrieb „next“. Einfügen nicht ausdrücklich bestätigt. Nicht getestet. |
| 5 | **geliefert, Bestätigung steht aus.** |
| 6 | **noch nicht geliefert.** Blöcke fertig in `pakete/PAKET_6_Beispielbild.md`. |

Fortschritt zuletzt gezählt: 97 Einbau-Schritte insgesamt, rund 8 % bei Gruppe A von Paket 1. Seitdem sind Paket 1 bis 4 durchgegangen. **Nichts ist veröffentlicht, nur gespeichert.**

**SharePoint-Änderungen von Josias (seit 27.10.):**
- `RG_Pruefpunkte`: Spalten `Foto` (Auswahl Aus/Optional/Pflicht, Standard Aus), `KommentarPflicht` (Ja/Nein, Standard Nein), `Grenzmodus` (Auswahl Mangel/Warnen/Sperren, Standard Mangel). `FotoMoeglich` hat er nur in der Ansicht eingeblendet. Alle bestehenden Zeilen stehen bei `Foto` auf „Aus“ (SharePoint füllt Standardwerte nicht nachträglich), nur **„ZZ Test Thermometer Serverraum“ (Id 10) steht auf „Optional“**.
- Noch zu prüfen: `BedingungPunkt` (Zahl, 0), `BedingungWert` (Text) und die Auswahlwerte MEHRFACH/DATUM/DATUMZEIT bei `Eingabetyp`. Josias wurde dazu aufgefordert, bestätigt hat er es nicht ausdrücklich.
- `RG_Plan`: Testzeilen für Mo (jede Woche), Mi, Do, Fr, Sa auf den Test-Rundgang, damit er jeden Tag erscheint. **Vor dem echten Betrieb auf Aktiv = Nein setzen.**

## 3. So hat der Engineering-Chat geliefert (Josias fand das besser, bitte beibehalten)
Josias antwortet nur „next“ oder „ok“ bzw. „A1 ok“. Pro Nachricht eine Gruppe (höchstens etwa 8 Properties), immer in dieser Reihenfolge:

1. **Überschrift** mit Schritt und Gruppe, z. B. „Schritt 1.8: `btnKaSpeichern` → `OnSelect`“.
2. **Steuerelement** und **Pfad** in der Strukturansicht: `scrKategorie › conKaFuss › btnKaSpeichern`. Dazu ein Satz, wie man es findet (Suchfeld oben, Property oben links im Auswahlfeld wählen, Formelleiste anklicken, Strg+A, Strg+V).
3. **Text zum Kopieren:** ein Codeblock mit der **ganzen Property**, deutsche Formelleiste (`;` als Trenner, `;;` zum Verketten, Dezimalkomma), **ohne `=` am Anfang, ohne Kommentare**, sonst nichts im Block.
4. **„Das ändert sich“:** ein ```diff-Block mit nur den geänderten Zeilen (rot/grün), lange gleiche Teile mit „…“ gekürzt. Bei neuen Properties: „Vorher: Standardwert“.
5. **Kurz erklärt:** ein bis drei einfache Sätze.
6. **Nachprüfen:** zum Beispiel „Hier muss eine Formel stehen, keine Zahl (Studio friert Höhen in Galerien ein)“ oder „Das Ende muss lauten …“.
7. Am Ende ein Satz, wie es weitergeht („Schreib ‚next‘ für Schritt …“).

Außerdem:
- **SharePoint-Spalte immer zuerst** (Name, Typ, Auswahlwerte, Standardwert), danach „Daten aktualisieren“ in Studio. Fehlt das, werden Formeln rot (`Foto.Value`, `Grenzmodus.Value`).
- Ankündigen, **wann rote Fehler normal sind** (bis alle Aufrufer einer geänderten Funktion ersetzt sind) und wann die App-Prüfung gemacht wird.
- Bei Rot erst die **Ursache nennen** und die Behebung **der Reihe nach** (aktualisieren, speichern, F5, dann Fehlermeldung schicken).
- **Fortschritt ehrlich in Prozent** nennen, auch wenn er klein ist. Nie behaupten, etwas sei getestet, wenn es nicht getestet ist; unsichere Stellen als **UNSICHER** kennzeichnen.
- Ton: Deutsch, kurz, einfache Sätze, „du“.
- Dieselben Texte gibt es fertig auf der Einbau-Seite https://claude.ai/artifact/Ff3qCtpZYf4EuMXinh94bd (Datei `pakete/EINBAU_ASSISTENT.html`, Kopierfelder und farbig markierte Änderungen) und in `pakete/PAKET_n_*.md`. Aus dem Repo erzeugt: `python3 -I werkzeuge/baukasten.py 2026-10-27_0909`, dann `doc_baukasten.py`, `einbau_seite.py`.

## 4. Als Nächstes
1. Josias fragen: Paket 5 drin? App-Prüfung → Formeln = 0 nach Paket 4 und 5? Spalten und Auswahlwerte aus 4.2 und 5.2 angelegt?
2. **Paket 6 liefern:** 6.2 SharePoint (Bibliothek `RG_Hinweisbilder`, Spalte `HinweisBildID`, Testbild hochladen, ID notieren), 6.3 Datenquelle in Studio hinzufügen und **Vorab-Test** (Bild-Steuerelement mit `LookUp(RG_Hinweisbilder; ID = …).Thumbnail.Large`; zeigt es nichts, abbrechen), 6.4 `scrKategorie.OnVisible`, 6.5 `lblKaFrage.Width` und YAML `btnKaBild`, 6.6 YAML `conKaBild` (Bildschirm markieren, ganz nach vorne), 6.7 App-Prüfung.
3. **Tests nachholen**, am besten pro Paket gebündelt: Paket 1 ab A3, danach die Testbögen in `PAKET_2` bis `PAKET_6`. Teil B (Foto-Auswahl) nur am Tablet.
4. Erst nach bestandenen Tests **veröffentlichen**.

## 5. Offen bei Josias
Annahmen in `pakete/BAUKASTEN_UEBERSICHT.md` bestätigen (Foto-Pflicht auch bei unbeantworteten Punkten, „Warnen“ verlangt Begründung, „Sperren“ nur für Tippfehler-Grenzen, Bedingungen nur eine Ebene tief, Datum als Text, Beispielbild als Fenster), Pflegegruppe benennen, ob der Fachbereich Excel oder Papier liefert.

## 6. Danach (Planung, Engineering-Chat)
Schlüssel/Status/Einfrieren der Fragen, dann die Builder-App (zwei Fenster: „Alle Rundgänge“ und „Rundgang bauen“, Status Entwurf/Aktiv/Archiviert, keine Konfiguration im Builder). Siehe `arbeit/2026-10-27_Builder/`. Josias sagt dem Engineering-Chat, was in die App soll.
