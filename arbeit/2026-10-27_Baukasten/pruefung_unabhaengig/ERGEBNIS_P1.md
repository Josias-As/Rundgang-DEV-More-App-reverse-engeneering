# Prüfung Paket 1 – Foto-Modus (unabhängige Prüfung, 27.10.2026)

Grundlage: `export/*.pa.yaml` (Stand 08:24) + die Zeile von 08:44 laut `HINWEIS.md`, `export/SPALTEN.md`, `pakete/PAKET_1_Foto.md`.
Kennzeichnung: **belegt** = aus Export/Paket nachgewiesen, **geschlussfolgert** = abgeleitet, **UNSICHER** = nicht prüfbar.

## Ergebnis in Kürze

- **0 hoch, 2 mittel, 7 niedrig.** Ich habe keinen Formel- oder Namensfehler gefunden, der in Studio rot würde oder falsch speichert. Die beiden mittleren Befunde betreffen die SharePoint-Spalte (Standardwert) und den Testbogen, der so nicht ausführbar ist.
- Maschinell geprüft (eigene Skripte, nur lesend):
  - Klammern in allen 24 Blöcken stimmen.
  - Rückübersetzung DE→EN jedes Blocks gegen den Export: Die Unterschiede sind **genau** die angekündigten Änderungen. Bei `App.Formulas`, `scrKategorie.OnVisible` und `btnKaSpeichern.OnSelect` per Zeilen-Diff, sonst Text gegen Text. Unveränderte Teile sind zeichengleich.
  - Die Vorher-Fassungen sind zeichengleich mit dem Export. Einzige Ausnahme: `btnKaSpeichern.OnSelect` enthält zusätzlich die Zeile von 08:44 an der in HINWEIS.md genannten Stelle.
  - Alle Aufrufe der UDFs haben die richtige Zahl an Argumenten: `fnFehlt` 12× (5 Stellen), `fnFehltGrund` 12, `fnKommentarNoetig` 8, `fnZahlBewertung` 4, `fnFotoModus` 2, `fnLinkAnzahl` 1.
  - Der Export enthält 5 Aufrufe von `fnFehlt` und 2 von `fnZahlBewertung`. Alle stehen im Paket. Keine Stelle bleibt mit der alten Signatur zurück.

## Befunde

### B1 – mittel – SharePoint-Spalte `Foto`: Standardwert „Aus“ hebelt die Rückfallregel für neue Prüfpunkte aus (Schritt 1.2)
- **Belegt:** Laut Schritt 1.2 ist der Standardwert „Aus“. `fnFotoModus` gibt jeden gültigen Wert zurück und fällt nur bei leerem Wert auf `FotoMoeglich` zurück. In der App gibt es kein `Patch(RG_Pruefpunkte…)`, die Pflege läuft also über SharePoint-Formulare.
- **Szenario (geschlussfolgert):** Ein Admin legt nach dem Einführen einen neuen Prüfpunkt an und setzt wie gewohnt `FotoMoeglich = Ja`. SharePoint füllt `Foto = Aus` → `fnFotoModus("Aus"; true)` = „Aus“ → kein Foto-Knopf. Das widerspricht der Kurzfassung („Leere Spalte = wie bisher“), und niemand merkt es.
- **Vorschlag:** In Schritt 1.2 **keinen Standardwert** setzen (leer). Alternativ ausdrücklich dokumentieren, dass ab jetzt nur noch `Foto` zählt und `FotoMoeglich` bei neuen Punkten wirkungslos ist. Dann `FotoMoeglich` im Formular ausblenden.
- Dazu gehört: T1.10 verlangt „Foto leer lassen“ bei Id 10, das in 1.2 auf Pflicht gesetzt wurde. Wie man eine Auswahl wieder leert, steht nicht im Bogen. Sicher geht es in der Rasteransicht, Zelle leeren. Ob das Formular „leer“ anbietet, ist UNSICHER.

### B2 – mittel – Testbogen in der angegebenen Umgebung nicht ausführbar (Schritt 1.10, Test)
- **Belegt:** Schritt 1.10 sagt „Speichern (noch nicht veröffentlichen) und den Test in der Vorschau machen“. Laut Kopf des Testbogens wählt Josias das Foto am Tablet aus (T1.5, T1.8). Ab T1.2 ist Id 10 Pflicht. `btnKaSpeichern` speichert erst, wenn `lblKaFehlendAnzahl = 0`.
- **Szenario:**
  - Das Tablet läuft mit der veröffentlichten (alten) Fassung. Ohne Veröffentlichen, oder ohne Studio im Tablet-Browser, gibt es am Tablet weder „📷 Foto *“ noch die Pflichtprüfung (geschlussfolgert).
  - Die Sitzung wechselt zwischen Vorschau und Tablet. `colFotos` lebt nur in einer Sitzung, also ist das Foto aus T1.5 in der Vorschau nicht da.
  - T1.7 („Gespeichert.“) ist in der Vorschau dann blockiert: „Noch offen (1): … (Foto)“. T1.8–T1.12 bauen darauf auf.
- **Vorschlag:** Den Bogen in zwei Durchläufe teilen.
  - (a) Vorschau T1.1–T1.4 und T1.6. Vor T1.7 Id 10 auf „Optional“ stellen, dann Kategorie neu öffnen und T1.7 ausführen.
  - (b) Tablet T1.4–T1.9 komplett in **einer** Sitzung. Dafür entweder bewusst veröffentlichen (DEV-App) oder Studio im Tablet-Browser öffnen. Das Testmodus-Ende ausdrücklich nennen.

### B3 – niedrig (Rückfrage) – Foto-Pflicht gilt auch für unbeantwortete Nicht-Pflicht-Punkte (`App.Formulas` → `fnFehltGrund`)
- **Belegt:** Der Arm `foto = "Pflicht" && fanz < 1; "Foto"` prüft nicht, ob der Punkt beantwortet ist. `fnBeantwortet` ist definiert, wird aber nicht benutzt.
- **Szenario:** Ein Punkt mit `Pflicht = Nein` und `Foto = Pflicht` bleibt leer, weil er heute nicht zutrifft. Die Kategorie lässt sich trotzdem nur mit Foto speichern („(Foto)“).
- **Vorschlag:** Mit Josias klären. Falls „Foto nur, wenn beantwortet“ gemeint ist: `foto = "Pflicht" && fanz < 1 && (pflicht || fnBeantwortet(bew; wt; wz))`. Andernfalls in die Kurzfassung schreiben: „Foto Pflicht gilt immer, auch ohne Antwort“.

### B4 – niedrig – Kopf und Voraussetzungen widersprechen sich, Anhang „zeichengleich mit dem Export“ stimmt nicht ganz
- **Belegt:**
  - Der Kopf nennt den Export „2026-10-27_0724“ und „ENTWURF: Simulation der Änderung von 08:44“. HINWEIS.md nennt den Export 08:24.
  - Die Voraussetzungen behaupten „Frischer Export nach dem Stand von 08:44 eingelesen (dieses Dokument wurde daraus erzeugt)“.
  - Das Vorher von `btnKaSpeichern.OnSelect` enthält die 08:44-Zeile, die nicht im Export steht. Das ist sachlich richtig, aber nicht „zeichengleich mit dem Export“.
- **Szenario:** Josias fügt den Entwurf ohne Neuerzeugung ein. Weicht die echte 08:44-Zeile in Studio ab (andere Stelle, Tippfehler, weitere Änderung), dann überschreibt der Ganz-Ersatz von `btnKaSpeichern.OnSelect` sie unbemerkt.
- **Vorschlag:** Kopf und Voraussetzungen vereinheitlichen. Vor Schritt 1.8 einen Abgleich einbauen: Inhalt in Studio = Vorher-Block, sonst abbrechen. Oder wie angekündigt mit dem frischen Export neu erzeugen.

### B5 – niedrig – Foto-Fenster in der Nur-Ansicht zeigt einen irreführenden Hinweis (`lblKaFotoHinweis.Text`)
- **Belegt:**
  - In der Nur-Ansicht öffnet `btnKaFoto` das Fenster. Es ist nur sichtbar, wenn Links da sind.
  - `addKaFoto` ist dort unsichtbar.
  - Der Text lautet „Fotos werden beim „Speichern“ hochgeladen.“ oder „Foto Pflicht: mindestens ein Foto.“. `FotoModus` kommt in der Nur-Ansicht aus den **heutigen** Stammdaten (`pp.Foto`), nicht aus dem gespeicherten Stand.
- **Szenario:** Ein Rundgang ist abgeschlossen. Ein Punkt ist heute Pflicht → „📷 Foto (1)“ antippen → Hinweis „Foto Pflicht: mindestens ein Foto“, obwohl nichts mehr geändert werden kann.
- **Vorschlag:** `If(varNurLesen; "Gespeicherte Fotos (nur Ansicht)."; <bisheriger Block>)`. Rein kosmetisch: Vorher stand dort auch der Speichern-Hinweis.

### B6 – niedrig – Prüfung „Formel statt Zahl“ (E-05) nur für `btnKaFoto.Y`
- **Belegt:** „Prüfen nach dem Schritt“ nennt nur `btnKaFoto.Y`. Ebenfalls Formeln in der Galerie mit variabler Höhe bzw. im Foto-Fenster sind: `conKaKarte.Height`, `lblKaAbstand.Y` (bestimmt die Zeilenhöhe), `imgKaFotoNeu.Height`.
- **Szenario (geschlussfolgert):** Studio friert `lblKaAbstand.Y` oder `conKaKarte.Height` als Zahl ein. Dann schneiden Karten mit Kommentar/Foto unten ab oder überlappen die nächste Karte.
- **Vorschlag:** Alle vier Properties in die Nachprüfung aufnehmen.

### B7 – niedrig – Testbogen: unklare oder nicht garantierte Erwartungen (Test T1.1, T1.6, T1.8, T1.11)
- **T1.1** „Übrige Punkte: kein Foto-Knopf“ gilt nur, wenn kein anderer Punkt der Kategorie `FotoMoeglich = Ja` hat. Solche Punkte zeigen jetzt „📷 Foto“ (Optional). Ob Id 10 in „Kategorie 1“ liegt, ist UNSICHER.
- **T1.6** „zurück auf i.O. → beides weg“ stimmt nur für einen Punkt mit Foto = Aus. Wählt man den Optional-Punkt aus 1.2, bleibt der Foto-Knopf stehen. Den Punkt im Bogen benennen.
- **T1.8** Der Ordner lautet `TEST/2026/10/<durch.Title>`. „R…“ ist eine Annahme über den Titel.
- **T1.11** verlangt „n.i.O.-Punkt ohne Foto“. Nach T1.7 ist der n.i.O.-Punkt wieder i.O., in Kategorie 1 gibt es dann keinen mehr. Außerdem schließt T1.11 D13 ab. Das ist mehr als „darf fortgesetzt werden“: Es legt Mängel an und startet die Protokoll-Archivierung bzw. Mail an die Testadresse. Wer aufräumt, muss davon wissen.
- **Vorschlag:** Bogen als Zeitachse mit eindeutig benannten Punkten. Für T1.11 einen eigenen n.i.O.-Punkt ohne Foto anlegen. Den Abschluss von D13 und die Folgen (RG_Maengel, PDF) ausdrücklich nennen.

### B8 – niedrig (Hinweis, nicht durch Paket 1 verursacht) – Kommentar inaktiver Antworten wird beim Speichern geleert (`btnKaSpeichern.OnSelect`)
- **Belegt:** `UpdateIf(colAntworten; !fnKommentarNoetig(…); {Kommentar: ""})` läuft auch über die Zeilen mit `Inaktiv = true`. Diese sollen laut Export-Kommentar (3b) „unverändert mitgeführt“ werden. Die Zeile von 08:44 tat dasselbe, Paket 1 ändert daran nichts („heute gleiches Ergebnis“ stimmt).
- **Szenario:** Ein Prüfpunkt war i.O. mit Kommentar (vor 08:44 gespeichert) und ist inzwischen deaktiviert. Die Kategorie wird erneut gespeichert → Kommentar weg, unsichtbar für den Prüfer.
- **Vorschlag:** Falls ungewollt: `UpdateIf(colAntworten; !Inaktiv && !fnKommentarNoetig(…); {Kommentar: ""})`. Josias entscheidet.

### B9 – niedrig (Hinweis, unverändert) – Alte Foto-Links an i.O.-Punkten mit Foto = Aus sind beim Bearbeiten unsichtbar
- **Belegt:** `btnKaFoto.Visible` (Bearbeiten) = `Bewertung = "NIO" || FotoModus <> "Aus"`. `Fotos` bleibt aber im JSON und erscheint im Protokoll als „Foto ›“.
- **Szenario:** Ein Punkt war n.i.O. mit Foto, gespeichert, und wird jetzt auf i.O. umgestellt. Das Foto bleibt gespeichert, der Prüfer sieht es nicht mehr. In der Nur-Ansicht erscheint es jetzt wieder (neu: Knopf, sobald Links da sind). Vorher war das genauso, also kein Rückschritt.
- **Vorschlag:** Optional `btnKaFoto.Visible` im Bearbeiten-Zweig um `|| fnLinkAnzahl(ThisItem.Fotos) > 0` erweitern (Kartenhöhe folgt automatisch). Josias entscheidet.

## Geprüft ohne Befund

1. **Syntax:**
   - `;` / `;;` / Dezimal korrekt.
   - Keine Kommentare in Verhaltensformeln.
   - UDF-Köpfe mit Typen.
   - Mehrarmiges `If` in UDF (`fnFehltGrund`, `fnFotoModus`).
   - UDF ruft UDF ohne Rekursion.
   - `fnKommentarNoetig(...): Boolean = bew = "NIO"` ist gültig: Das erste `=` definiert.
   - `As` in Filter/Concat/LookUp wird schon im Export benutzt.
2. **Namen:**
   - Alle Steuerelemente und Properties gibt es im Export: `conKaKarte`, `lblKaAbstand`, `txtKaKommentar`, `btnKaFoto` (Hover/Pressed\*), `lblKaFehlend(Anzahl)`, `btnKaSpeichern`, `lblKaFotoHinweis`, `addKaFoto.Size`, `imgKaFotoNeu.Y/Height`.
   - Variablen, Sammlungen (`colFotos.Uebernommen/Nr/Url`, `colFotoNeu`, `colKatListe`, `colErledigt`) und der Flow `aRG_Foto_hochladen` mit 6 Argumenten sind unverändert übernommen.
   - Die Spalte `Foto` wird in 1.2 angelegt, die Daten werden vor 1.3/1.4 aktualisiert.
3. **Typen:**
   - `p.Foto.Value` / `pp.Foto.Value` (Auswahl) → Text.
   - Leer bzw. `pp` leer → Rückfall `FotoMoeglich` → „Aus“.
   - `KommentarPflicht` Boolean, `Grenzmodus`/`FotoModus` Text in allen Zweigen.
   - Blank an Number-Parametern unkritisch.
4. **Schema von `colAntworten`:** Alle drei Zweige legen dieselben 19 Felder an (maschinell geprüft). Weder Export noch Paket lesen `FotoMoeglich` aus `colAntworten`. Alle drei `LookUp(colPP; …).FotoMoeglich`-Stellen des Exports sind ersetzt. Außerhalb von `scrKategorie` liest niemand `colAntworten`.
5. **Logik:**
   - `fnFehlt` ohne Foto-Pflicht ist gleichwertig zum alten Ausdruck.
   - Die Meldungstexte in `lblKaFehlend` sind gleich wie vorher, „(Foto)“ ist neu.
   - Upload-Bedingung und `btnKaFoto.Visible` (Bearbeiten) haben dieselbe Regel.
   - Die Fotozählung (`!Uebernommen` + Links) bleibt über Upload, Übernahme und fehlgeschlagene Nachlese hinweg konstant: keine Doppelzählung, kein Rückfall auf 0, kein doppelter Link beim Wiederholen.
   - JSON-Felder, Nachlese, Protokoll und `btnRuAbschluss` (Mängel aus JSON) sind unverändert.
6. **Auswirkungen:** `scrRundgang`, `scrProtokoll`, `scrStart` und `App.OnStart` nutzen keine der geänderten Funktionen oder Felder.
7. **Szenarien:**
   - Neuer Punkt ohne Daten → „Aus“ (aber B1).
   - Altes JSON ohne neues Feld.
   - Inaktiver Punkt (FotoModus „Aus“, ausgeblendet).
   - Nur-Ansicht (Pflicht false, Zähler unsichtbar, `varZeigeFehlend` bleibt false).
   - n.i.O.→i.O.→n.i.O. (Kommentar bleibt bis zum Speichern in der Sammlung).
   - Zweimal speichern (Links zählen).
   - Netzfehler/Abbruch.
   - Zwei Prüfer (`GespeichertAm`-Vergleich unverändert).
8. **Layout:**
   - Zeile 2 bei Y = 54(+24)+68.
   - Kommentar 20 … B−176, Foto-Knopf B−164 … B−20: 12 px Abstand.
   - 20 px Rand unten.
   - `lblKaAbstand.Y` = Kartenende: behebt nebenbei die alte Abweichung bei FotoMoeglich-Karten.
   - Das ✕ (Y 8–48) liegt nicht mehr unter dem Bild (ab 52).
   - Die Hinweis- und Knopftexte sind kürzer bzw. kleiner als vorher.
9. **Reihenfolge und Rückweg:** Spalte → Daten aktualisieren → Formulas → Aufrufer. Rote Zwischenfehler sind angekündigt. Rückweg: Formulas zuletzt, Version wiederherstellen.
10. **Studio-Fallen:**
    - Kein `Navigate` in `OnVisible`.
    - `Concat(Filter(…) As z; z.Frage …)` korrekt aliasiert.
    - Innere `Filter(colFotos; PruefpunktID = a.PruefpunktID …)` greifen auf das richtige Feld zu.
    - Flow-Name unverändert.
