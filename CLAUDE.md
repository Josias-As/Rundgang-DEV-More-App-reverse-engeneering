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
