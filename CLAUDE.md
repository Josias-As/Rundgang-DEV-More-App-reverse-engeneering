# CLAUDE.md – Rundgang-App (Power Apps Canvas, SharePoint IMS+)

Stand: 27.10.2026. Kennzeichnung: **belegt** (Export/Dokument), **gemessen**, **geschlussfolgert**, **UNSICHER**.

## 1. Rahmen
- **Josias** (Technoform) baut die App „Rundgang DEV“ (Nachbau der MoreApp-Form „Objektrundgang TCC“, Tablet hochkant). Er fügt jede Formel selbst in Studio ein. Claude liest Exporte und liefert Pakete, ändert nie App, Listen oder Flows.
- Rollen: **Planer-Chat** plant, **Engineering-Chat** (dieses Repo) baut die Pakete. Bei Widerspruch zählt die Aussage des Planer-Chats mehr.
- Stil der Pakete: Kurzfassung zuerst, je Schritt `Steuerelement.Property` mit ganzem Block (deutsch), Test, Rückweg, Vorher-Fassungen im Anhang. Alles maschinell aus dem Export erzeugt und geprüft.
- **Keine Kommentare in Formeln** (Josias, 27.10.), auch nicht in App.Formulas. Alte `//`-Zeilen fallen beim Ersetzen weg.
- Vault: darf beschrieben werden, ist aus der Cloud aber nicht erreichbar → alles ins Repo.

## 2. Ordner
| Ordner | Inhalt |
|---|---|
| `quellen/<datum>_…/` | Exporte und Übergaben, nur lesen |
| `arbeit/<datum>_<thema>/` | Analysen, Zwischenstände (`bloecke.json`, `pruefung_auto.txt`) |
| `arbeit/_entpackt/` | entpackte Exporte (nicht eingecheckt) |
| `pakete/` | Pakete zum Einfügen und Prüfberichte |
| `werkzeuge/` | Python, immer `python3 -I` |

## 3. Werkzeuge
- `werkzeuge/rg.py`: Export-ZIP → `.msapp` → Src/*.pa.yaml → `App`-Klasse (`"Steuerelement.Property"` → Formel englisch), Spalten aus DataSources.json, `to_de`/`from_de`, `ohne_kommentare`, `klammern_ok`, `bezeichner`. Neuer Export: Pfad in `EXPORTE` eintragen.
- `werkzeuge/baukasten.py <Schlüssel>`: erzeugt Pakete 1–6 als Zustandskette (exakte Anker, Abbruch bei Abweichung) und prüft Namen, Klammern, Kommentare, Rückübersetzung, `.Value`/Coalesce, Schema der drei colAntworten-Zweige, Felder, Argumentanzahl fnFehlt, Textbreiten. `--simulation-0844` nur für Entwürfe ohne frischen Export.
- `werkzeuge/logik_probe.py`: Python-Nachbildung der UDFs, Rückwärtsgleichheit und Szenarien.
- `werkzeuge/mutation_baukasten.py`: Mutationstest der Prüfungen (9/9).
- `werkzeuge/doc_baukasten.py` + `baukasten_text.py`: Paket- und Prüfdokumente in `pakete/`.
- `werkzeuge/builder.py`: erzeugt die Builder-App (3 Bildschirme als YAML, App.Formulas/OnStart deutsch) nach `pakete/builder/` und prüft (Namen, Klammern, Rückübersetzung, Startwerte aller Variablen, Sammlungen, Steuerelemente, Patch-Felder gegen Spalten, Auswahlspalten `{Value:}`, Argumentanzahl, YAML zurücklesen, Textbreiten). `werkzeuge/doc_builder.py` → `pakete/builder/EINBAU_BUILDER.md`. `werkzeuge/mutation_builder.py` (10/10), `werkzeuge/logik_builder.py` (Abläufe gegen die Leselogik der Rundgang-App, 27 Szenarien).
- `werkzeuge/einbau_seite.py <Schlüssel>`: erzeugt `pakete/EINBAU_ASSISTENT.html` (Einbau-Seite mit Kopierfeldern, farbig markierten Änderungen, Häkchen). Nach jedem neuen Export `baukasten.py`, `doc_baukasten.py`, dann `einbau_seite.py` laufen lassen und die Seite neu veröffentlichen.

## 4. Formelregeln (Rundgang)
- YAML-Quelltext englisch (`,` / `;`), Formelleiste deutsch (`;` / `;;`, Dezimalkomma). Immer die ganze Property.
- `Navigate` nicht in OnVisible (Timer `tmrWeiter`). YAML in Galerien: Y/Height prüfen (frieren ein, E-05). YAML in eine Galerievorlage mit einem Kind der Vorlage markiert einfügen. Classic/Button kennt kein AccessibleLabel. Werte mit `{n: ` im Blockstil `|-`.
- `Concat(Filter(… As x; …); x.Feld)` ist ungültig. `As` am ersten Argument von Concat selbst ist gültig.
- Flow-Name in Studio: `aRG_Foto_hochladen`. Flows ohne Antwort (Premium) → App baut Links mit `fnSpUrl`.
- `Refresh` vor jedem Frisch-Lesen (Sitzungs-Cache, E-01). Schreibstellen: Sperre `varSperreBis` + Nachlese.
- Datensatz-Literale, die eine Sammlung füllen, müssen in **allen** Zweigen dieselben Felder haben (Fehler 27.10.: `FotoMoeglich` fehlte im Bearbeiten-Zweig → Feld leer). Der Generator prüft das.
- Spaltennamen in Add/Drop/Rename/ShowColumns als Bezeichner (`supportcolumnnamesasidentifiers`).
- Unsichtbare Steuerelemente rechnen trotzdem: Abfragen hinter `If(<offen>; …)`.
- SharePoint-Spaltennamen: `rg.App.spalten` enthält interne **und** Anzeigenamen (z. B. `Fassungf` = „Fassung“). Neue Spalten nie `Name` nennen (eingebaute Spalte `{Name}`), z. B. `Kontakt`.
- **`IfError(Patch/Remove(…); Set(…))` nur als Glied einer Kette** (danach `;;`). Als Wert (Zweig eines `If`, Argument) meldet Studio einen Typfehler Record/Table ↔ Boolean und führt die ganze Formel nicht aus (belegt 02.11., Builder: 8 Stellen, Ladeanzeige hing). Dort `If(IsError(…); Set(…))`. Der Generator baut das um und prüft es.
- Ein Export-Paket enthält die **zuletzt veröffentlichte** Fassung, nicht den Studio-Stand (belegt 02.11.). Vor dem Export veröffentlichen.

## 5. Stand
- Export 27.10. 08:24 in `quellen/2026-10-27_Export/` (vor der Änderung 08:44 „Kommentar leeren“). Übergabe Planer + Paket (FORTSCHRITT, ENTSCHEIDUNGEN, pakete) in `quellen/2026-10-27_Uebergabe*/`.
- Analysen: `arbeit/2026-10-27_Analyse/`, Builder: `arbeit/2026-10-27_Builder/` (Entscheidungen: Baukasten 1–6 zuerst, dann Schlüssel/Status/Einfrieren, dann Builder; zwei Apps, Komponentenbibliothek falls erlaubt; keine Konfiguration im Builder).
- **Baukasten 1–6 (27.10.–30.10.), nicht eingefügt:** `pakete/BAUKASTEN_UEBERSICHT.md`, `PAKET_n_*.md`, `PRUEFUNG_n_*.md`, erzeugt aus dem Export 27.10. 09:09 (`quellen/2026-10-27_Export0909/`). Unabhängig geprüft in 3 Runden + gezielte Runde 4 (Paket 3+4). Vorschlag „Flows rückmelden“ (nicht gebaut) in der Übersicht. Nach jedem neuen Export `baukasten.py` mit neuem Schlüssel laufen lassen.
- **Builder-Konzept (30.10.):** v1/v2 in `arbeit/2026-10-30_Builder_Konzept/`. **v3-Vorschlag** (`KONZEPT_Builder_v3_Vorschlag.md`, Recherche + Kritik + Abwägung, noch nicht von Josias bestätigt): Fassung an den Bereichen statt Rundgang-Kopie (belegt: Kategorie liest Prüfpunkte nur über KategorieID+Aktiv), Editor mit Gliederung/Editor/Vorschau, Vorlagen-Rundgang statt `RG_Vorlagen`, Spalten `Status`/`Fassung`/`Schluessel`, Excel einfügen, Rückgängig statt Rückfragen. 4 Fragen offen (PC/Tablet, Excel, Fassungen, Vorlagen).
- **Paket 7 (30.10.), nicht eingefügt:** Foto „Bei Mangel Pflicht“ (`pakete/PAKET_7_FotoBeiMangel.md`), im Generator `baukasten.py` als Paket 7, Logik-Gegenprobe 81 Szenarien. Muss vor dem Builder eingefügt sein.
- **Rundgang-Builder (30.10.), nicht eingefügt, nicht in Studio getestet:** `pakete/builder/EINBAU_BUILDER.md` (+ `scrListe/scrEditor/scrPlan.yaml`, `App.Formulas.txt`, `App.OnStart.txt`). Neue App, Tablet quer. Entscheidungen **von Josias bestätigt (02.11.)**: PC, Fassungen an den Bereichen (Spalten `Fassung`, `QuelleID`, `RundgangID` an Kategorien/Prüfpunkten, `Status`/`Fassung`/`EntwurfFassung`/`EntwurfVon` am Rundgang), Vorlagen-Rundgang, kein Excel-Import (nur „Mehrere Fragen“), Entfernen per zweitem Tippen. Alle längeren Abläufe im Zeitgeber `tmrArbeit` (Stufen über `varJob`). Altbestand wird beim ersten Öffnen vorbereitet (Fassung 1).
- **Builder eingefügt (02.11.), Export `quellen/2026-11-02_Builder/` (Schlüssel `2026-11-02_Builder`):** Abgleich `werkzeuge/abgleich_builder.py` → alle Steuerelemente da, App.Formulas/OnStart gleich. App-Prüfung: 16 Fehler (Studio zählt 39) = 8× IfError als Wert in `btnLiAktion`, `btnLiVerwerfen`, `tmrArbeit.OnTimerEnd` (deshalb hing die Ladeanzeige). Behoben im Generator, Mutation 11/11. Abweichungen: `btnLiVorlagen.OnSelect` fehlt (leer), `conEdP.X` 32, `conPlTermine` X/Y verschoben, `lblPlAb/lblPlBis.Size` 10, `ddPKategorie.OnChange` letzte zwei Resets vertauscht (gleiche Wirkung). Testbogen noch offen.

- **Neue Anforderungen (Planer, 02.11.):** `quellen/2026-11-02_Uebergabe_Planer/`, Analyse `arbeit/2026-11-02_Neue_Anforderungen/ANALYSE_Neue_Anforderungen.md`. Belegt: AUSWAHL erzeugt nie einen Mangel (nur `Bewertung = "NIO"`), KW in der App richtig (`ISOWeekNum`), 5 `User()`-Stellen. Planer-Pakete ab **8** (7 = Foto bei Mangel). Jede neue Prüfpunkt-Spalte auch im Builder (6 Stellen, §3), Verweise auf Prüfpunkte beim Kopieren umschreiben, Abweichung zum letzten Lauf über `QuelleID`. Bereich bleibt Pflicht (Fassung), nur ausblendbar. Wartet auf: Export Rundgang-App nach 1–6, die 4 PDFs, Entscheidung Reihenfolge.

- **Paket 8 Teil Builder (02.11.), nicht eingefügt:** `pakete/builder/PAKET_8_BUILDER.md` (`werkzeuge/doc_paket8_builder.py`, Vorher = `arbeit/2026-11-02_Paket8/builder_vorher.json` = Studio-Stand nach F1–F4 + Josias' Optik `lblPlAb/Bis.Size` 10, `conPlTermine` 980/90). Spalten `RG_Pruefpunkte.Abschnitt` (Text), `RG_Bereiche.Ausblenden` (Ja/Nein). 7 neue Steuerelemente, 26 Properties. Generator prüft neu: Datenvertrag (Spalten in Kopie + galAkt), Label-Textbreite mit Innenabstand 5+5 px (Josias' Befund „ab“). Mutation 13/13. Teil Rundgang-App wartet auf deren Export.

- **Export Rundgang-App 02.11. 15:41** (`quellen/2026-11-02_RundgangApp/`, Schlüssel `2026-11-02_1541`). Abgleich gegen Soll 1–7 (`doc_app89.py`): Paket 5 fehlt ganz (5 Steuerelemente + App.Formulas), Paket 7 fehlt, 3.5/4.5/1.9 fehlen, **zwei Fehleinfügungen** (`lblKaHinweis.Text` = Foto-Hinweis, `lblKaAbstand.Text` = Fortschrittszeile). Dritte Fehleinfügung `lblKaZahlInfo.BorderColor`. Rest zeichengleich. (`Fassungf` ist der **interne Name** der Spalte „Fassung“, kein Tippfehler – nie löschen; Fehlurteil von mir, vom Prüfer gefunden.)
- **Paket N (Nachholen), Paket 8+9 App (02.11.), nicht eingefügt:** `pakete/PAKET_N_Nachholen.md`, `pakete/PAKET_8_9_10_APP.md` (baukasten.py `paket8`, `paket9`, `fnfehlt_erweitern`; fnFehlt jetzt 13 Argumente). Mutation 12/12. Unabhängige Prüfung: `arbeit/2026-11-02_App89/pruefung_unabhaengig.md`.
- **Paket 9 Builder (02.11.), nicht eingefügt:** `pakete/builder/PAKET_9_BUILDER.md` (Vorher = `arbeit/2026-11-02_Paket8/builder_nach_p8.json`): Bildschirm `scrKontakte`, Knopf `btnPNio` + Fenster `conNio`, Kopie/galAkt/galPr. Konzept `arbeit/2026-11-02_Paket9_Kritisch/`. Rest von Paket 8 Builder läuft über den Einsetz-Chat (`arbeit/2026-11-02_Paket8/UEBERGABE_Paket8_Rest_an_Einsetz_Chat.md`).

- **Paket 10 (02.11.):** Kategorie-Sperre entfernt (Wunsch Josias über Planer, `quellen/2026-11-02_Uebergabe_Planer/UEBERGABE_SPERRE_UND_STANDFRAGE_2026-11-02.md`), im Dokument `pakete/PAKET_8_9_10_APP.md` zusammen mit 8/9 (jede Property einmal). Übergabe Paket N + 8–10 an Einsetz-Chat: `arbeit/2026-11-02_App89/UEBERGABE_PaketN_und_8-10_an_Einsetz_Chat.md` + Startprompt. Stand für den Planer: `arbeit/2026-11-02_App89/STAND_FUER_PLANER_2026-11-02.md`. Planer-Pakete ab 11.

- **Paket 12+16 (02.11.), nicht eingefügt:** eigene Antwortwörter (`TextIO`/`TextNIO`, max. 18 Zeichen, intern weiter IO/NIO) und „nicht messbar“ bei Zahlen (`NichtMessbar` Ja/Nein, WertText „nicht messbar“, Kommentar Pflicht). `pakete/PAKET_12_16_APP.md` (Vorher = nach 8–10), `pakete/builder/PAKET_12_16_BUILDER.md` (Vorher = `arbeit/2026-11-02_Paket8/builder_nach_p9.json`), Generator `werkzeuge/doc_paket12_16.py`. Builder-Erklärtext Kategorien angepasst. Logik-Probe 91 Szenarien (kritisch + nicht messbar ergänzt). doc_paket8/9_builder sind eingefroren.

- **Paket 14+15 (03.11.), nicht eingefügt:** Abweichung zum letzten abgeschlossenen Lauf (`AbwMax`, `AbwProzent`, `NurSteigend`; Vorwert über `ID` oder `QuelleID`, nur gleiche Test-Art) und Vergleich zweier Zahlen (`VergleichPunkt`, `VergleichTol`). Wirkung: Begründung Pflicht über `KommentarPflicht` (Original in `KPflOrig`), kein Mangel, Text `AbwText` in JSON/Protokoll. `pakete/PAKET_14_15_APP.md`, `pakete/builder/PAKET_14_15_BUILDER.md` (Fenster `conZa`, Knopf `btnPZahlMehr`, Verweis wird beim Kopieren umgeschrieben wie Bedingung). `werkzeuge/doc_paket14_15.py`. Logik 103 Szenarien. Vorher Builder = `builder_nach_p12_16.json`. **Regel:** YAML neuer Steuerelemente mit `doc_app89.neue_bis(d, nr)` im Stand des Pakets ausgeben (Kettenreihenfolge, nicht Nummer).

- **Paket 17 Archiv (03.11.), nicht eingefügt:** `pakete/PAKET_17_ARCHIV.md` (`werkzeuge/doc_paket17.py`, baukasten `paket17`): Bildschirm `scrArchiv` (Zeitraum/Rundgang delegierbar, Rest lokal, max. 500), Knopf `btnStartArchiv`, `varAusArchiv` für „Zurück“. Nur lesen, offene Läufe nicht öffnen.

## 6. Lieferstil für Einbau-Anweisungen (Josias findet ihn gut, beibehalten)
Eine Gruppe (höchstens etwa 8 Properties) je Nachricht, Josias antwortet „next“/„ok“. Je Property: Überschrift mit Schritt, **Steuerelement** und **Pfad** (`scrKategorie › galKaPruefpunkte › conKaKarte › txtKaZahl`), **Text zum Kopieren** (ganze Property, deutsch, ohne `=`, ohne Kommentare, nur der Block), **„Das ändert sich“** als ```diff mit nur den geänderten Stellen, **Kurz erklärt** (1–3 Sätze), **Nachprüfen** (Formel statt Zahl, Ende der Formel). SharePoint-Spalte immer zuerst, danach „Daten aktualisieren“. Rote Fehler vorher ankündigen, bei Rot Ursache und Behebung der Reihe nach. Fortschritt ehrlich in Prozent, nichts als getestet ausgeben, was nicht getestet ist. Übergabe an den Einsetz-Chat: `arbeit/2026-10-30_Uebergabe_Einsetz_Chat/UEBERGABE_an_Einsetz_Chat_v2.md`.
