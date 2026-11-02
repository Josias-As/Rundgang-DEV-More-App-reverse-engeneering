# Stand für den Planer-Chat (Engineering-Chat, 02.11.2026 abends)

Antwort auf `UEBERGABE_SPERRE_UND_STANDFRAGE_2026-11-02.md`. Repo `Josias-As/Rundgang-DEV-More-App-reverse-engeneering`, Branch `claude/upbeat-tesla-emx06l`.

## 1. Builder-App
- **Name „Rundgang Builder“**, App-ID `6310209112270376249` (aus dem Export), Tablet quer 1366 × 768. Bildschirme: `scrListe` (Übersicht), `scrEditor` (Gliederung | Editor | Vorschau + Prüfung), `scrPlan` (Termine), mit Paket 9 neu `scrKontakte` (Ansprechpartner).
- **Was sie kann:** Rundgänge anlegen (leer oder als Kopie), Bereiche/Kategorien/Prüfpunkte bearbeiten, verschieben, duplizieren, entfernen (zweites Tippen), „Mehrere Fragen“ auf einmal, Bausteine aus „Vorlagen (Builder)“ oder aus anderen Rundgängen holen, Beispielbild wählen, laufende Prüfung (Fehler und Hinweise), Plan pflegen, archivieren und reaktivieren.
- **Fassungen:** Eine Änderung an einem aktiven Rundgang ist ein **Entwurf (neue Fassung)**. Die aktive Fassung bleibt, bis „Aktivieren“. Laufende Rundgänge enden mit der alten Fassung. Die Fassung hängt an den **Bereichen** (`Aktiv` je Bereich).
- **Schreibt in:** `RG_Rundgaenge` (neu `Status`, `Fassung`, `EntwurfFassung`, `EntwurfVon`), `RG_Bereiche` (neu `Fassung`, `QuelleID`, `Ausblenden`), `RG_Kategorien` (neu `RundgangID`, `Fassung`, `QuelleID`), `RG_Pruefpunkte` (neu `RundgangID`, `Fassung`, `QuelleID`, `Abschnitt`, mit Paket 9 `Kritisch`, `KritischText`, `Ansprechpartner`, `Rueckfrage`, `RueckfrageText`), `RG_Plan`, mit Paket 9 die neue Liste `RG_Ansprechpartner` (`Title`, `Kontakt`, `Telefon`, `Hinweis`, `Allgemein`, `Aktiv`).
- **Stand:** eingefügt, Fehler der App-Prüfung behoben (IfError-Typfehler). Paket 8 (Abschnitte, Bereich ausblenden) teilweise eingefügt, der Rest läuft über einen Einsetz-Chat. Paket 9 Builder gebaut, nicht eingefügt. **Nicht getestet, nicht veröffentlicht.**

## 2. Änderungen an „Rundgang DEV“ seit Paket 6
- **Abgleich Export 02.11. 15:41:** Paket 5 fehlt ganz, Paket 7 fehlt, 3 Formeln stehen im falschen Steuerelement, 3 fehlen. Dafür gibt es **Paket N (Nachholen)**.
- **Paket 7:** Foto „Bei Mangel Pflicht“ (Auswahlwert in `Foto`).
- **Paket 8–10 (ein Dokument, jede Property einmal):**
  - Abschnitte: Überschrift in der Karte, Protokoll, Mangel. Spalte `RG_Pruefpunkte.Abschnitt`.
  - Bereich ausblenden: `RG_Bereiche.Ausblenden`.
  - Rückfrage und kritischer Mangel mit Ansprechpartnern (neue Fenster `conKaRueck`, `conKaKrit`). `fnFehlt`/`fnFehltGrund` haben jetzt **13 Argumente** (kritisch, nicht bestätigt). Neue JSON-Felder in den Antworten: `Abschnitt`, `AbsKopf`, `Kritisch`, `KritischOk`, `KritischZeit`, `KritischVon`.
  - **Paket 10 = euer Umbaupunkt „Sperre entfernen“**, siehe 5.
- Nichts umbenannt. Keine Spalte gelöscht. **Achtung:** `Fassungf` ist der interne Name von „Fassung“. Nicht löschen.

## 3. Veröffentlicht, Tests
Nichts veröffentlicht. In Studio getestet ist nur, was Josias selbst bestätigt hat (Test-Gruppe 1 von Paket 1). Unsere Prüfungen sind maschinell: Generator, Mutationstests, Logik-Proben und je eine unabhängige Prüfung.

## 4. Punkte aus `UEBERGABE_NEUE_ANFORDERUNGEN_2026-11-02.md`

| Punkt | Stand |
|---|---|
| L3 eigene Antwortwörter | geklärt: AUSWAHL erzeugt nie einen Mangel (belegt). Vorschlag `TextIO`/`TextNIO` an i.O./n.i.O., **nicht gebaut** |
| KW falsch | nur in MoreApp. Die App rechnet mit `ISOWeekNum`. |
| 3.5 Anleitungen / ⓘ | offen |
| 4 Struktur: Abschnitt, Bereich optional | **gebaut** als Abschnitt + „Bereich ausblenden“ (Paket 8). Der Bereich bleibt in den Daten Pflicht, weil die Fassung daran hängt. |
| 3.1 Abweichung zum letzten Lauf | offen. Muss über `QuelleID` laufen, weil die Prüfpunkt-IDs je Fassung wechseln. |
| 3.3 zwei Werte vergleichen | offen. Der Verweis muss beim Kopieren umgeschrieben werden. |
| 3.2 Zugangsdaten | offen (Frage an Josias: Bedien-PIN oder sensibel?) |
| 3.4 Archiv | offen |
| 2 Prüferauswahl, Unterschrift, Kopfdaten | offen. 5 `User()`-Stellen sind bekannt. |
| **neu (Josias): kritischer Mangel + Rückfrage + Ansprechpartner** | **gebaut** (Paket 9, App + Builder). Keine automatische Benachrichtigung, nur „bei wem melden“. |
| L5 viele gleiche Blöcke | durch den Builder gelöst (Holen, Vorlagen, Mehrere Fragen) |
| Paketnummern | Unsere 7 = Foto bei Mangel. 8 = Abschnitte, 9 = kritisch, 10 = Sperre weg. Eure Liste bitte ab 11 zählen. |

## 5. Umbaupunkt „Kategorie-Sperre entfernen“ (Paket 10)
Euer Vorschlag passt. Gegen den aktuellen Stand geprüft:
- `galRuKategorien.Items`: „gesperrt“ → „offen“. `lblRuSymbol.Text` 🔒 → ○, `lblRuSymbol.Color` grau. `lblRuKatZustand.Text` → „Offen“. `btnRuOeffnen.Text` → „Öffnen“. Die übrigen Prüfungen auf „gesperrt“ (Fill, DropShadow, DisplayMode, OnSelect) greifen nie mehr und bleiben, damit weniger einzufügen ist.
- `btnKaSpeichern.OnSelect`: Der Zweig „Bitte zuerst die vorherigen Kategorien abschließen“ ist entfernt. Die ganze Property liefern wir zusammen mit Paket 8/9, weil sie dort ohnehin ersetzt wird.
- **Weiter-Sprung:** `tmrWeiter` nimmt schon die **erste offene** Kategorie (nicht Position + 1). Keine Änderung nötig.
- **Abschluss:** `btnRuAbschluss` prüft schon „alle Kategorien gespeichert“ (DisplayMode, Text „(noch … offen)“, OnSelect). Unverändert.
- Weitere Stellen mit „nacheinander“/„vorherige“: keine. Der Builder hat keine Einstellung dazu, nur einen Erklärtext („Die Kategorien werden der Reihe nach freigeschaltet“). Den ändern wir beim nächsten Builder-Paket.
- **Vorschlag, nicht gebaut:** `RG_Rundgaenge.FesteReihenfolge` (Ja/Nein), im Builder pflegbar. Wäre 1 Spalte + 3 Properties in der App. Nur wenn Josias es will.

## 6. Probe-Rundgang „ZZ Test Infrastrukturrundgang“ (Rundgang 3)
- Der Builder **bereitet Altbestand beim ersten Öffnen selbst vor**: Er setzt `Fassung` = 1 und `RundgangID` an Kategorien und Prüfpunkten, `Status` am Rundgang. Die per Skript angelegten Einträge brauchen also nichts weiter, solange die Bereiche `RundgangID` = 3 haben und die Kategorien die richtige `BereichID`.
- Ohne `Status` gilt: `Aktiv` = Ja → „Aktiv“, sonst „Archiviert“. Ein noch nicht freigegebener Probe-Rundgang erscheint im Builder also als „Archiviert“, bis man ihn reaktiviert oder bearbeitet.
- Abschnitte (Kompressor 1/2/3, Kältemaschine 1/2/3) gibt es erst nach Paket 8. Danach im Builder je Prüfpunkt eintragen oder per „Mehrere Fragen“ mit Abschnitt neu anlegen.
- Haustechnik und Infrastruktur, ein Rundgang oder zwei: Das entscheidet Josias. Der Builder kann beides, Zusammenführen geht über „Holen“.
