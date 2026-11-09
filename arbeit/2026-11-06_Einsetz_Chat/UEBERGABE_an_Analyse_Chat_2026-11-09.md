# Übergabe Einsetz-Chat → Analyse-Chat (09.11.2026)

Ab jetzt wird wieder mit dem Analyse-Chat gebaut. Dieses Dokument enthält alles, was sich beim Einsetzen geändert hat, vor allem die Formeln, die der Einsetz-Chat **selbst** geschrieben hat (nicht aus einem Paket). Details und Chronik stehen in `STAND_EINSETZ_CHAT.md` (Abschnitt 5).

## 1. Stand der Pakete

| Paket | Rundgang DEV | Builder | Test |
|---|---|---|---|
| N, 8–10, 12+16, 13, 14+15, 17, 19–22 | drin | drin | getestet (19–21 bestätigt) |
| 23 Banner/Test/Kontakte | drin | drin | kurz getestet |
| 18 Zugangscodes | drin | drin | 🔑-Anzeige in Lauf 25 noch nicht bestätigt |
| 11 Prüfer/Unterschrift/Kopfdaten | drin, mit Abweichungen (Abschnitt 3) | drin, mit Abweichungen | V1 ok; T1–T13, V2–V4 offen |
| **24 Info-Knopf ⓘ** | **fehlt** | **fehlt** | – |

Weitere offene Arbeit (Fehlerliste, Flows, Ideen) siehe Abschnitt 6.

Fehlerzahl zuletzt: Builder 0, Rundgang DEV 0 (vor den Korrekturen A18/A20, deren Einbau ist unbestätigt).

## 2. Neue Entscheidung von Josias (09.11.): kein Gerätekonto, keine Prüferauswahl

> „die anmeldung in der app muss nicht mehr passieren. wir sparen uns den geteilten zugriff und sagen dass jeder sich mit seiner echten mail anmelden soll. also das alles wieder zurückbauen.“

Bitte als Rückbau-Paket für Paket 11 (Teil „Prüfer wählen“) bauen:
- Prüfer = wieder `User()` (FullName/Email) an allen Stellen, die Paket 11 auf `varPruefer` umgestellt hat: `btnRgAktion` (PrueferEmail/PrueferName, `Geraetekonto` kann weg oder bleiben), `btnKaSpeichern`, `btnKaKritOk` (KritischVon), `btnRuAbschluss` (FestgestelltVon, UnterschriftName, Reset von varPruefer/varPrWahl), `lblStartNutzer.Text/OnSelect`, `lblRuUText`/`lblRuUName`, `App.OnStart`, `scrStart.OnVisible` (colPrueferAlle).
- Entfernen: `conPwWahl` (DEV), Builder `scrPruefer` + `btnKoPruefer`, Datenquellen `RG_Pruefer` und Office 365-Benutzer (in beiden Apps, wenn sonst nicht gebraucht). SharePoint-Liste `RG_Pruefer` darf bleiben (2 Einträge: Josias, Julia Manthey).
- **Unklar, bitte mit Josias klären:** Bleiben **Unterschrift** (conRuUnterschrift, penRuUnterschrift, RG_Unterschriften, Spalten an RG_Durchfuehrungen) und **Kopfdaten** (Standort/Adresse/Auftraggeber im Builder-Plan, Protokollkopf)? Annahme des Einsetz-Chats: ja, nur die Prüferauswahl fällt weg.

## 3. Abweichungen beim Einsetzen von Paket 11 (vom Einsetz-Chat selbst geschrieben oder geändert)

Alle Formeln in deutscher Formelleiste (`;` / `;;`).

**A15 – Stifteingabe:** „Einfügen → Eingabe → Stifteingabe“ liefert die **moderne** Stifteingabe (kein OnSelect/Fill/Image). Eingesetzt wurde die **klassische** (Einfügen → Suche „Stift“ → Klassisch), Properties wie im Paket. V1 (`varUnterschriftDa` wird true) ok. → Paket-Text anpassen.

**A16 – Connector-Name (Builder):** In der deutschen Formelleiste des Builders heißt der Connector **`'Office365-Benutzer'`**. `Office365Users.*` war komplett rot (auch `MyProfileV2`). Geändert:
- Builder `galPfSuche.Items`:
  `If(Len(Trim(txtPfSuche.Text)) >= 3; Filter('Office365-Benutzer'.SearchUserV2({searchTerm: Trim(txtPfSuche.Text); top: 15; isSearchTermRequired: true}).value; !IsBlank(Mail) && AccountEnabled))`
- In **Rundgang DEV** funktioniert `Office365Users.SearchUserV2` dagegen (Monitor 09.11.: Status 200). Fällt mit dem Rückbau ohnehin weg.

**A17 – `btnRuAbschluss.OnSelect` (DEV):** `IfError(Patch(RG_Unterschriften; …); Set(varPatchFehler; true))` innerhalb eines `If(…)` gab Typfehler (Record vs. Boolean, 2 Fehler). Ersetzt durch (gleiche Wirkung):
  `If(IsError(Patch(RG_Unterschriften; Defaults(RG_Unterschriften); {Title: "D" & varDurchID; DurchfuehrungID: varDurchID; Bild: varUnterschriftBild})); Set(varPatchFehler; true))`
→ Generator: `IfError(Patch…; Set…)` nicht als Zweig in `If` verwenden.

**A18 – Builder `txtPfSuche.DisplayMode`:** hing an `varSchreibbar` (nur im Editor wahr) → Suchfeld gesperrt. Gegeben: `If(varIsLoading; DisplayMode.View; DisplayMode.Edit)` (Einbau unbestätigt; fällt mit Rückbau weg).

**A19 – nicht übernommene Formeln (DEV):** `App.OnStart`, `lblStartNutzer.Text/OnSelect`, vermutlich `scrStart.OnVisible` standen nach dem Einsetzen noch auf der alten Fassung und wurden erneut gegeben. → Nach dem Rückbau **Export beider Apps abgleichen**.

**A20 – Prüfer ohne Namen (DEV):** In der veröffentlichten App war `varPruefer.Email` gefüllt, `Name` leer → Fenster ließ sich ohne Namen schließen, Kopf „· wechseln ›“ ohne Namen. Vermutete Ursache: `ClearCollect(colPrueferAlle; RG_Pruefer)` lädt `Title` nicht (Spaltenauswahl). Gegeben (Einbau unbestätigt, fällt mit Rückbau weg):
- `scrStart.OnVisible`: `ClearCollect(colPrueferAlle; ShowColumns(RG_Pruefer; ID; Title; Email; Aktiv))`
- `btnPwZu.Visible`: `Coalesce(varPruefer.Email; "") <> "" && Coalesce(varPruefer.Name; "") <> ""`
- `btnPwZu.DisplayMode`: `If(Coalesce(varPruefer.Email; "") <> "" && Coalesce(varPruefer.Name; "") <> ""; DisplayMode.Edit; DisplayMode.Disabled)`
- `conPwWahl.Visible`: `varPrWahl || Coalesce(varPruefer.Email; "") = "" || Coalesce(varPruefer.Name; "") = ""`
- Josias hatte testweise `Set(varPrWahlGetroffen; true);;` in `btnPwTreffer.OnSelect` ergänzt; Rücknahme wurde gegeben (unbestätigt).

## 4. Sonstige Korrekturen beim Einsetzen (P18/P23, Fehlplatzierungen)
- `scrKategorie.Width` hatte die lblKaFrage-Formel → zurück auf `Max(App.Width; App.MinScreenWidth)`, Formel in `lblKaFrage.Width`.
- `btnStartOffen.Width` hatte die lblStartOffen-Formel → zurück auf `196`, `X = Parent.Width - 220`; Formel in `lblStartOffen.Width`.
- Builder 262 Fehler nach P18: `RG_Zugangscodes` fehlte als Datenquelle, `RG_Pruefpunkte` nicht aktualisiert → behoben.

## 5. Daten (SharePoint IMS+)
- Neu (P11-Skript `skripte/paket11_sharepoint.js`): Listen `RG_Pruefer`, `RG_Unterschriften`; Spalten `RG_Rundgaenge.Standort/Adresse/Auftraggeber`, `RG_Durchfuehrungen.UnterschriftUrl/UnterschriftName/UnterschriftZeit/Geraetekonto`.
- Lauf 23 per Skript abgeschlossen (Test). In den **Papierkorb** verschoben (auf Wunsch): Testläufe 26, 28, 29 (09.11.) und Haustechnik-Läufe 19, 27 (keine Ergebnisse dran).
- Funktionsrundgang: Fassung 3 aktiv (🔑 Code ID 1 bei „Öltemperatur Kompressor“, Prüfpunkt 403), Entwurf Fassung 4 offen. Lauf 25 (05.11.) hat Fassung 3.
- Haustechnik Rundgang ist **nicht** als Testrundgang markiert.

## 6. Was noch nicht gebaut ist (alles, nicht nur Paket 24)

Die Anforderungen A–L aus `arbeit/2026-11-02_Neue_Anforderungen/ANALYSE_Neue_Anforderungen.md` sind alle als Pakete gebaut und eingesetzt. Offen ist:

| # | Was | Quelle | wartet seit | Vorschlag |
|---|---|---|---|---|
| 1 | **Rückbau Prüferauswahl** (P11 Teil A) | Entscheidung 09.11. | neu | zuerst |
| 2 | **Paket 24** Info-Knopf ⓘ | freigegeben 06.11., nicht eingesetzt | 06.11. | gegen Stand nach Rückbau prüfen, dann einsetzen |
| 3 | **Fehler „Beheben vor Echtbetrieb“** A3, A5, A9, A12, A13 (dazu A10, A14) | `TESTLAUF_2026-11-06.md` | 06.11. | **ein Fix-Paket**, vor den echten Rundgängen. A3 ist kritisch (Kategorie ohne aktive Prüfpunkte ⇒ Lauf nie abschließbar) |
| 4 | **Entscheidungen B1–B5** mit Josias | `TESTLAUF_2026-11-06.md` | 06.11. | B1: Hinweistext-Skript gegeben, Lauf unbestätigt. B4 will Josias genauer durchgehen. B5 („Wirklich abschließen?“ verfällt nie) ist durch die Unterschrift überholt, falls die bleibt |
| 5 | **D1** Komma/Punkt bei Zahlen | TESTLAUF | 06.11. | am Tablet testen (7,5 / 7.5), sonst Fix |
| 6 | **C1–C27** Aufräumen | TESTLAUF | 06.11. | Aufräum-Paket, niedrig |
| 7 | **Flows rückmelden** (Foto-Upload, Archiv-PDF, Mängel-Mail, Unterschrift-Upload) | `pakete/BAUKASTEN_UEBERSICHT.md` (Vorschlag, nicht gebaut) | 27.10. | eigenes Paket; Flow-Änderung im Konto von Josias |
| 8 | Archiv: Schalter „Testläufe“ doppelt bei „alle Rundgänge“ | Josias 06.11. | 06.11. | vor Go-live |
| 9 | Knopf „Rundgang zurücksetzen“ mit Code (Code im Builder änderbar; Zurücksetzen auch im Builder nur mit Code) | Josias 06.11. | 06.11. | nach den Fehlern |
| 10 | Eigene Bilder in Anleitungen (heute nur Text + Beispielbild des Prüfpunkts) | Wunsch, nicht bestellt | 06.11. | mit Josias klären; ggf. mit Paket 24 zusammen denken |
| 11 | Builder-Übersicht: „· Testrundgang“ bei langen Plan-Texten abgeschnitten | Beobachtung 06.11. | 06.11. | klein, ins Aufräum-Paket |
| 12 | Echte Rundgänge anlegen (Haustechnik, Infrastruktur, Legionellen, Gefahrstoffschränke) | `arbeit/2026-11-03_MoreApp_Vergleich/` | 03.11. | Infos fehlen: Herkunft Bilder 10–16, Grenzwerte, Formularbilder der anderen drei |
| 13 | Export-Abgleich beider Apps gegen die Paketkette | Einsetz-Chat | – | nach dem Rückbau, vor Paket 24 |

Verworfen/erledigt: feste Reihenfolge (Josias: nein), Prüfpunkte verschieben (gibt es schon: ↑↓, Kategorie-/Bereichsfeld).

## 7. Arbeitsweise, die sich bewährt hat
- Antwortformat beim Einsetzen: App oben, je Block „Farbmarker + Steuerelement · Property“, reine Kopierblöcke, **darunter ein diff-Block** mit vollen Zeilen (🟦 Formel, 🟩 YAML, 🟧 SP-Skript, 🟨 Daten, 🟥 Prüfen).
- Deutsche Namen in der Formelleiste beachten: `Thumbnail` → `Miniaturansicht`, `Office365Users` → `'Office365-Benutzer'` (Builder).
- „Daten hinzufügen“ nur ohne ausgewähltes Steuerelement (sonst landet der Listenname in der Property, z. B. `tmrArbeit.Duration`).
