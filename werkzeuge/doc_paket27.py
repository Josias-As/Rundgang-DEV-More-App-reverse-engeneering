"""Paket 27 (Builder-Optik Prüfpunkt-Bereich): python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket27.py
Vorher = arbeit/2026-11-02_Paket8/builder_nach_p26.json (Export 13.11. + Paket 24 Lage-Werte + Paket 26)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import doc_app89  # noqa: E402
import doc_generisch as g  # noqa: E402
from doc_paket12_16 import block, pfad  # noqa: E402

LAGE = "Nur Lage/Größe (enger gesetzt, damit unten alles sichtbar bleibt)."
ERKL = {
    "conPZahl.Height": "Der Zahl-Bereich endet jetzt unter „Mangel / Hinweis + Grund / nicht speicherbar“ (der Knopf „Verlauf/Vergleich“ ist nicht mehr darin).",
    "conPRest.Y": "Steht bei Zahl 4 px höher (356 statt 360), weil der Zahl-Bereich kürzer ist.",
    "conPRest.Height": "242 statt 250 (Zeile „Info ⓘ“ ist 8 px flacher).",
    "ddPAnl.Y": "Anleitung-Auswahl auf gleicher Höhe wie „Bild wählen“.",
    "btnPBild.Height": "36 wie alle Felder.", "btnPBild.Width": "Bis 8 px vor das Vorschaubild.",
    "imgPBild.X": "Vorschaubild 36 × 36 rechts bündig.", "imgPBild.Width": "36 × 36.", "imgPBild.Height": "36 × 36.",
    "lblPKat.Y": LAGE, "ddPKategorie.Y": LAGE, "lblPAbschnitt.Y": LAGE, "txtPAbschnitt.Y": LAGE,
    "btnPNio.Y": "Unterste Zeile: 248 unter dem Beginn des Rest-Bereichs. Bei Zahl endet sie 12 px über dem Rand (vorher genau am Rand → abgeschnitten).",
    "btnPNio.Width": "Bei Zahl 316 breit (rechts daneben „Verlauf/Vergleich ›“), sonst ganze Breite.",
    "btnPNio.Size": "12 statt 13, damit auch „⚠ Bei n.i.O.: Rückfrage + kritisch ›“ in 316 px passt.",
}


def main():
    bv = json.load(open(os.path.join(g.SNAP, "builder_nach_p26.json"), encoding="utf-8"))
    bn = json.load(open(os.path.join(builder.AUS_ARB, "bloecke.json"), encoding="utf-8"))
    v, n, eltern = bv["props"], bn["props"], bn["eltern"]
    geaendert = sorted(k for k in n if v.get(k) != n[k])
    assert not [k for k in v if k not in n]
    verschoben = "btnPZahlMehr"
    assert bv["eltern"][verschoben] == "conPZahl" and eltern[verschoben] == "conEdP"
    rest = [k for k in geaendert if not k.startswith(verschoben + ".")]
    assert set(rest) == set(ERKL), set(rest) ^ set(ERKL)
    c_neu = [c for c, _ in builder.alle([s for s in builder.SCREENS if s.name == "scrEditor"][0]) if c.name == verschoben][0]
    pruef = open(os.path.join(builder.AUS_ARB, "pruefung.txt"), encoding="utf-8").read()
    rechtecke = pruef.split("Rechtecke in conEdP je Eingabetyp (Bildschirm 768 px hoch):\n")[1].split("\n\n")[0]
    reihen = ["- " + x.strip() for x in rechtecke.splitlines() if x.strip()]
    z = ["# Paket 27 – Builder: Prüfpunkt-Bereich ohne Überlappung, unten nichts abgeschnitten", "",
         "Stand 13.11.2026. Erzeugt mit `werkzeuge/builder.py` und `werkzeuge/doc_paket27.py`. "
         "**Voraussetzung:** im Builder Paket 24 (alle Lage-Werte B2.x in `conPRest`) und Paket 26. Vorher-Fassungen = dieser Stand (Export 13.11. + P24-Lage + P26). Rundgang DEV ändert sich nicht.", "",
         "## Kurzfassung", "",
         "- **„Verlauf/Vergleich ›“** lag im Zahl-Bereich direkt unter „i.O. bis“/„nicht erlaubt“ und deckte sie zum Teil ab. Er steht jetzt **unten rechts neben „Bei n.i.O. ›“** (nur bei Zahl). "
         "Ob Verlauf/Vergleich eingestellt ist, zeigt die Füllung (hellblau wie beim 🔑); der Text ist immer „Verlauf/Vergleich ›“ (der alte Text „…: an ›“ passte nicht).",
         "- **„Bei n.i.O. ›“** wurde unten abgeschnitten: Bei Zahl endete er genau am Rand des Bereichs (648 px). Durch den kürzeren Zahl-Bereich (ohne den Knopf) und eine 8 px flachere Zeile „Info ⓘ“ endet er jetzt 12 px über dem Rand.",
         "- **Neue Generator-Prüfung:** Alle Steuerelemente in `conEdP` werden für **jeden Eingabetyp** als Rechtecke gezeichnet (sichtbare je Typ, Bildschirm 768 px). Geprüft: keine Überlappung, nichts ragt aus seinem Container, unten 6 px Rand. Mutation 15/15 (zwei neue Fälle: Überlappung, abgeschnitten). Ergebnis:", ""] + reihen + [
         "", "- Kein Scrollen nötig: Ein klassischer Container kann nicht scrollen. Ein Umbau auf einen automatischen vertikalen Container würde alle Lage-Werte ändern.",
         "- Umfang: 1 Knopf verschieben (löschen + YAML einfügen), %d Properties. Keine Daten, keine Formel-Logik. **Nicht in Studio getestet.**" % len(rest), "",
         "## B1 – „Verlauf/Vergleich ›“ verschieben", "",
         "1. Strukturansicht: `scrEditor › conEdMitte › conEdP › conPZahl › btnPZahlMehr` → **Löschen**. Keine andere Formel verweist auf den Knopf.",
         "2. **`conEdP`** markieren → Strg+V mit diesem YAML. Der Knopf landet direkt in `conEdP` (nicht in einem Unter-Container) und behält den Namen `btnPZahlMehr`.", "",
         "```yaml"] + builder.yaml_control(c_neu, "") + ["```", "",
         "**Nachprüfen:** `btnPZahlMehr.Visible` endet auf `= \"ZAHL\")`, `X` = 324, `Width` = 204. Bei einem Prüfpunkt vom Typ Zahl steht der Knopf unten rechts neben „Bei n.i.O. ›“.", "",
         "## B2 – geänderte Properties", ""]
    for i, k in enumerate(rest, 1):
        z += block("B2.%d" % i, k, bv["de"][k], bn["de"][k], ERKL[k], eltern)
    z += ["## Test", "", "| # | Schritt | erwartet |", "|---|---|---|",
          "| T1 | Prüfpunkt Typ **Zahl** öffnen (Fenster 1366 × 768) | „i.O. bis“, „nicht erlaubt“ frei; unten links „Bei n.i.O.: … ›“, rechts „Verlauf/Vergleich ›“, beide ganz sichtbar |",
          "| T2 | „Verlauf/Vergleich ›“ antippen, Vergleich einstellen, Fertig | Fenster öffnet wie bisher; danach Knopf hellblau gefüllt |",
          "| T3 | Typ **i.O./n.i.O.**, **Auswahl**, **Text** | „Bei n.i.O. ›“ über die ganze Breite, unten nichts abgeschnitten, kein „Verlauf/Vergleich“ |",
          "| T4 | Zeile „Info ⓘ“ | Anleitung und „Bild wählen“ auf einer Höhe, Vorschaubild rechts 36 × 36 |",
          "| T5 | Prüfpunkt kritisch + Rückfrage, Typ Zahl | Text „⚠ Bei n.i.O.: Rückfrage + kritisch ›“ passt in den Knopf |", "",
          "## Rückweg", "", "Vorher-Fassungen einsetzen; `btnPZahlMehr` in `conEdP` löschen und das YAML aus dem Anhang in `conPZahl` einfügen.", "",
          "## Anhang – Vorher-Fassungen", ""]
    for k in rest:
        z += ["**Builder `%s` vorher**" % k, "", "```", bv["de"][k], "```", ""]
    z += ["**`btnPZahlMehr` vorher (in `conPZahl`), Properties:**", "", "```"]
    z += ["%s: %s" % (k.split(".", 1)[1], bv["de"][k]) for k in sorted(bv["props"]) if k.startswith(verschoben + ".")] + ["```", ""]
    open(os.path.join(doc_app89.AUS, "builder", "PAKET_27_BUILDER_OPTIK.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/builder/PAKET_27_BUILDER_OPTIK.md (%d Properties + btnPZahlMehr verschoben)" % len(rest))


if __name__ == "__main__":
    main()
