# Übergabe an den Einsetz-Chat: Stand Baukasten-Pakete (30.10.2026)

Von: Engineering-Chat (Repo `Rundgang-DEV-More-App-reverse-engeneering`, Branch `claude/upbeat-tesla-emx06l`).
Für: den Chat, der Josias beim Einsetzen in Studio begleitet. Josias macht Schritt für Schritt weiter.

## Was es gibt
- Sechs Baukasten-Pakete (Foto-Modus, Pflicht-Kommentar auch bei i.O., Zahlengrenzen, bedingte Fragen, neue Typen, Beispielbild), nur der Reihe nach einsetzen.
- Dateien im Repo: `pakete/PAKET_1_Foto.md` … `PAKET_6_Beispielbild.md`, `PRUEFUNG_n_*.md`, `BAUKASTEN_UEBERSICHT.md`.
- Einbau-Seite mit Kopierfeldern und farbig markierten Änderungen: https://claude.ai/artifact/Ff3qCtpZYf4EuMXinh94bd (Datei `pakete/EINBAU_ASSISTENT.html`).
- Alle Blöcke sind aus dem Export vom **27.10.2026 09:09** erzeugt (`quellen/2026-10-27_Export0909/`). Hat sich die App seitdem verändert, muss „Vorher“ nicht mehr passen: dann nicht einfügen, sondern frischen Export an den Engineering-Chat geben (Blöcke werden neu erzeugt, der Generator bricht bei Abweichung ab).

## Wie Josias es haben will
Je Schritt: Name des Steuerelements, Name der Property, der Text einmal zum Kopieren (deutsche Formelleiste, kein `=`, keine Kommentare), dann die Änderungen farbig (diff: rot = vorher, grün = nachher). Er antwortet „next“. Eure Arbeitsweise (ARBEITSWEISE_AENDERUNGEN.md) ist eingehalten.

## Stand Paket 1 (Foto)
| Schritt | Stand |
|---|---|
| 1.1 Sicherung (speichern, Version notieren) | von Josias nicht ausdrücklich bestätigt, bitte nachfragen |
| 1.2 SharePoint: Spalte `Foto` (Auswahl Aus/Optional/Pflicht, Standard Aus) | erledigt. Vorhandene Zeilen waren leer (SharePoint füllt den Standard nicht nach); Josias hat alle auf „Aus“ gestellt. `FotoMoeglich` hat er nur in der Ansicht eingeblendet (nicht neu angelegt). **Offen:** Zeile „ZZ Test Thermometer Serverraum“ (Id 10) steht auf „Aus“, soll auf **Optional** (sonst überstimmt „Aus“ das FotoMoeglich = Ja). Bitte nachfragen. |
| Studio: Daten `RG_Pruefpunkte` aktualisieren | erledigt (war nötig, sonst war `Foto.Value` rot) |
| 1.3 `App` → `Formulas` | eingefügt |
| 1.4 `scrKategorie` → `OnVisible` | eingefügt, rote Linie unter `Foto.Value` ist nach dem Aktualisieren weg |
| 1.5 `txtKaZahl` → `OnChange` | eingefügt |
| 1.6 Gruppe A: `conKaKarte` → `BorderColor`, `BorderThickness`, `Height` | **zuletzt geliefert, Bestätigung steht aus.** Bei `Height` prüfen, dass eine Formel (keine Zahl) steht. |

Rote Fehler bis Schritt 1.9 sind normal (Funktionsköpfe `fnFehlt` und `fnZahlBewertung` haben neue Parameter, die Aufrufer folgen erst nach und nach).

## Als Nächstes (Paket 1)
1. Josias fragen: Gruppe A drin? Sicherung gemacht? Id 10 auf Optional?
2. 1.6 Gruppe B: `lblKaAbstand.Y`, `txtKaKommentar.Visible`, `btnKaFoto.Visible`.
3. 1.6 Gruppe C: `btnKaFoto` → `Y`, `Text`, `BorderColor`, `Color`, `HoverColor`, `PressedColor`, `HoverFill`, `PressedFill`.
4. 1.7 `lblKaFehlendAnzahl.Text` und `lblKaFehlend.Text` (unsichtbare Labels direkt auf `scrKategorie`).
5. 1.8 `btnKaSpeichern` → `OnSelect` (in `conKaFuss`).
6. 1.9 Foto-Fenster: `lblKaFotoHinweis.Text`, `addKaFoto.Size`, `addKaFoto.Visible`, `imgKaFotoNeu.Y`, `imgKaFotoNeu.Height`.
7. 1.10 App-Prüfung: Formeln = 0, speichern, Test Teil A (Vorschau) und Teil B (Tablet, Foto), erst dann Paket 2.
Alle Blöcke stehen fertig in `pakete/PAKET_1_Foto.md` und auf der Einbau-Seite.

## Prüfstand
- Unabhängig geprüft in drei Runden plus eine gezielte Runde für Paket 3+4. Paket 1, 2, 5, 6 ohne Code-Befund in der letzten Runde; Paket 3+4 nur gezielt (Feld `Warnung`, Speichern aus der Kopie).
- Nicht in Studio getestet (UNSICHER): `UpdateIf` mit Feldverweisen (Paket 3), `Patch(Datensatz; Datensatz)` in `ForAll` (Paket 4), Vorschaubilder in Paket 6, Kamera/Foto-Auswahl/Upload. Tests dafür stehen in den Paketen.
- Foto-Auswahl und Upload kann nur Josias am Tablet testen. Nur im Test-Rundgang „ZZ Test Objektrundgang TCC“ testen.

## Bei Fehlern in Studio
Josias nennt Steuerelement, Property und Fehlermeldung. Bitte nicht selbst umbauen: Meldung an den Engineering-Chat (Repo oben), der erzeugt die Blöcke neu und prüft sie.

## Offen bei Josias
Annahmen in `BAUKASTEN_UEBERSICHT.md` bestätigen (Foto-Pflicht auch bei unbeantworteten Punkten, „Warnen“ verlangt Begründung, „Sperren“ nur für Tippfehler-Grenzen), Pflegegruppe benennen, Excel oder Papier für die Rundgänge.
