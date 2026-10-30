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
- `werkzeuge/builder.py`: erzeugt die Builder-App (3 Bildschirme als YAML, App.Formulas/OnStart deutsch) nach `pakete/builder/` und prüft (Namen, Klammern, Rückübersetzung, Startwerte aller Variablen, Sammlungen, Steuerelemente, Patch-Felder gegen Spalten, Auswahlspalten `{Value:}`, Argumentanzahl, YAML zurücklesen, Textbreiten). `werkzeuge/doc_builder.py` → `pakete/builder/EINBAU_BUILDER.md`.
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

## 5. Stand
- Export 27.10. 08:24 in `quellen/2026-10-27_Export/` (vor der Änderung 08:44 „Kommentar leeren“). Übergabe Planer + Paket (FORTSCHRITT, ENTSCHEIDUNGEN, pakete) in `quellen/2026-10-27_Uebergabe*/`.
- Analysen: `arbeit/2026-10-27_Analyse/`, Builder: `arbeit/2026-10-27_Builder/` (Entscheidungen: Baukasten 1–6 zuerst, dann Schlüssel/Status/Einfrieren, dann Builder; zwei Apps, Komponentenbibliothek falls erlaubt; keine Konfiguration im Builder).
- **Baukasten 1–6 (27.10.–30.10.), nicht eingefügt:** `pakete/BAUKASTEN_UEBERSICHT.md`, `PAKET_n_*.md`, `PRUEFUNG_n_*.md`, erzeugt aus dem Export 27.10. 09:09 (`quellen/2026-10-27_Export0909/`). Unabhängig geprüft in 3 Runden + gezielte Runde 4 (Paket 3+4). Vorschlag „Flows rückmelden“ (nicht gebaut) in der Übersicht. Nach jedem neuen Export `baukasten.py` mit neuem Schlüssel laufen lassen.
- **Builder-Konzept (30.10.):** v1/v2 in `arbeit/2026-10-30_Builder_Konzept/`. **v3-Vorschlag** (`KONZEPT_Builder_v3_Vorschlag.md`, Recherche + Kritik + Abwägung, noch nicht von Josias bestätigt): Fassung an den Bereichen statt Rundgang-Kopie (belegt: Kategorie liest Prüfpunkte nur über KategorieID+Aktiv), Editor mit Gliederung/Editor/Vorschau, Vorlagen-Rundgang statt `RG_Vorlagen`, Spalten `Status`/`Fassung`/`Schluessel`, Excel einfügen, Rückgängig statt Rückfragen. 4 Fragen offen (PC/Tablet, Excel, Fassungen, Vorlagen).
- **Paket 7 (30.10.), nicht eingefügt:** Foto „Bei Mangel Pflicht“ (`pakete/PAKET_7_FotoBeiMangel.md`), im Generator `baukasten.py` als Paket 7, Logik-Gegenprobe 81 Szenarien. Muss vor dem Builder eingefügt sein.
- **Rundgang-Builder (30.10.), nicht eingefügt, nicht in Studio getestet:** `pakete/builder/EINBAU_BUILDER.md` (+ `scrListe/scrEditor/scrPlan.yaml`, `App.Formulas.txt`, `App.OnStart.txt`). Neue App, Tablet quer. Entscheidungen von Claude (zu bestätigen): PC, Fassungen an den Bereichen (Spalten `Fassung`, `QuelleID`, `RundgangID` an Kategorien/Prüfpunkten, `Status`/`Fassung`/`EntwurfFassung`/`EntwurfVon` am Rundgang), Vorlagen-Rundgang, kein Excel-Import (nur „Mehrere Fragen“), Entfernen per zweitem Tippen. Alle längeren Abläufe im Zeitgeber `tmrArbeit` (Stufen über `varJob`). Altbestand wird beim ersten Öffnen vorbereitet (Fassung 1).

## 6. Lieferstil für Einbau-Anweisungen (Josias findet ihn gut, beibehalten)
Eine Gruppe (höchstens etwa 8 Properties) je Nachricht, Josias antwortet „next“/„ok“. Je Property: Überschrift mit Schritt, **Steuerelement** und **Pfad** (`scrKategorie › galKaPruefpunkte › conKaKarte › txtKaZahl`), **Text zum Kopieren** (ganze Property, deutsch, ohne `=`, ohne Kommentare, nur der Block), **„Das ändert sich“** als ```diff mit nur den geänderten Stellen, **Kurz erklärt** (1–3 Sätze), **Nachprüfen** (Formel statt Zahl, Ende der Formel). SharePoint-Spalte immer zuerst, danach „Daten aktualisieren“. Rote Fehler vorher ankündigen, bei Rot Ursache und Behebung der Reihe nach. Fortschritt ehrlich in Prozent, nichts als getestet ausgeben, was nicht getestet ist. Übergabe an den Einsetz-Chat: `arbeit/2026-10-30_Uebergabe_Einsetz_Chat/UEBERGABE_an_Einsetz_Chat_v2.md`.
