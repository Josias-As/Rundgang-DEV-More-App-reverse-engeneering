"""Paket 17 (Archiv): Einbau-Dokument für die Rundgang-App.
Aufruf: python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/doc_paket17.py  ->  pakete/PAKET_17_ARCHIV.md"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_app89  # noqa: E402
import rg  # noqa: E402
from doc_paket12_16 import block  # noqa: E402

BL = json.load(open(doc_app89.BLOECKE, encoding="utf-8"))
ERKL = {
    "btnRuZurueck.OnSelect": "Wer aus dem Archiv kommt, landet mit „Zurück“ wieder im Archiv.",
    "scrStart.OnVisible": "Auf der Startseite gilt man nicht mehr als „aus dem Archiv“.",
    "lblStartListeTitel.Width": "Macht Platz für den Knopf „Archiv“.",
}


def screen_yaml(name, alle):
    info = alle[name]
    z = ["Screens:", "  %s:" % name, "    Properties:"]
    for k in sorted(info["props"]):
        w = doc_app89.yaml_wert(info["props"][k])
        if w.startswith("|-"):
            zeilen = w.split("\n")
            z.append("      " + k + ": " + zeilen[0])
            z += ["      " + x for x in zeilen[1:]]
        else:
            z.append("      " + k + ": " + w)
    z.append("    Children:")
    for k in [n for n, i in alle.items() if i["eltern"] == name]:
        z += ["      " + x for x in doc_app89.yaml_block(k, alle)]
    return "\n".join(z)


def main():
    p = [q for q in BL["pakete"] if q["nr"] == 17][0]
    alle = doc_app89.neue_bis(BL, 17)
    eltern = dict(rg.App(doc_app89.EXPORT).eltern)
    for n, i in BL["neue_controls"].items():
        eltern[n] = i["eltern"]
    keys = [c["key"] for c in p["props"]]
    z = ["# Paket 17 – Rundgang-App: Archiv vergangener Rundgänge", "",
         "Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket17) und `werkzeuge/doc_paket17.py`. "
         "**Voraussetzung: Paket N, 8–10, 12+16, 14+15 eingefügt** (es baut auf deren Stand auf; inhaltlich hängt es nur an `btnRuZurueck`, `scrStart`).", "",
         "## Kurzfassung", "",
         "- Neuer Bildschirm **„Archiv“** (Knopf „🗂 Archiv“ auf der Startseite). Zeitraum (Standard: letzte 3 Monate), Rundgang (alle oder einer), "
         "Schalter „nur mit Mängeln“, „auch offene“, „Testläufe“.",
         "- Liste: Rundgang, Tag mit KW, Prüfer, Anzahl n.i.O. **„Ansehen“** öffnet den Rundgang wie gewohnt nur zum Lesen (Kategorien, Protokoll). "
         "**„PDF“** öffnet das archivierte Protokoll, wenn es eins gibt. „Zurück“ führt wieder ins Archiv.",
         "- Offene (nicht abgeschlossene) Rundgänge werden nur angezeigt. Fortsetzen geht wie bisher über die Startseite am jeweiligen Tag.",
         "- Daten: nur lesen. SharePoint filtert nach Zeitraum und Rundgang (delegierbar), der Rest in der App. Höchstens 500 je Suche.",
         "- Umfang: 1 neuer Bildschirm, 1 neuer Knopf, %d Properties. Keine neuen Spalten. Generator 0 Fehler. **Nicht in Studio getestet. Nicht unabhängig geprüft.**" % len(keys), "",
         "## Schritt 1 – Bildschirm „Archiv“", "",
         "**Wo hin:** In der Strukturansicht einen Bildschirm markieren (z. B. `scrProtokoll`) → Strg+V. Studio legt `scrArchiv` an.", "",
         "```yaml", screen_yaml("scrArchiv", alle), "```", "",
         "**Nachprüfen (E-05):** In `galArListe › conArKarte` müssen `Height` (`Parent.TemplateHeight - 12`) und bei den Knöpfen `Y` Formeln sein, keine Zahlen.", "",
         "## Schritt 2 – Knopf auf der Startseite", "",
         "**Wo hin:** **`scrStart`** markieren → Strg+V.", "", "```yaml"] + doc_app89.yaml_block("btnStartArchiv", alle) + ["```", "",
         "## Schritt 3 – drei Properties", ""]
    vorher = {c["key"]: c["vorher"] for c in p["props"]}
    for i, k in enumerate(keys, 1):
        z += block("3.%d" % i, k, doc_app89.de(vorher[k]), doc_app89.de([c["nachher"] for c in p["props"] if c["key"] == k][0]), ERKL[k], eltern)
    z += ["## Test", "",
          "| # | Schritt | erwartet |", "|---|---|---|",
          "| T1 | Startseite → „🗂 Archiv“ | Liste der abgeschlossenen Rundgänge der letzten 3 Monate, neueste zuerst. Testläufe nicht dabei |",
          "| T2 | „Testläufe“ antippen | ZZ-Test-Läufe erscheinen mit „· Test“ |",
          "| T3 | Rundgang wählen, Zeitraum ändern, „Suchen“ | nur dieser Rundgang im Zeitraum |",
          "| T4 | „nur mit Mängeln“ | nur Läufe mit n.i.O. (rote Zeile) |",
          "| T5 | „Ansehen“ | Rundgangsübersicht, Kategorien nur zum Lesen, „Protokoll“ geht. „Zurück“ → wieder im Archiv |",
          "| T6 | „PDF“ (wenn vorhanden) | archiviertes PDF öffnet sich |",
          "| T7 | „auch offene“ → offenen Lauf „Ansehen“ | Hinweis „… auf der Startseite fortsetzen“ |", "",
          "## Rückweg", "", "`scrArchiv` und `btnStartArchiv` löschen, die drei Vorher-Fassungen einsetzen.", "",
          "## Anhang – Vorher-Fassungen", ""]
    for k in keys:
        z += ["**`%s` vorher**" % k, "", "```", doc_app89.de(vorher[k]), "```", ""]
    open(os.path.join(doc_app89.AUS, "PAKET_17_ARCHIV.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_17_ARCHIV.md (%d Properties, %d neue Steuerelemente)" % (len(keys), len(p["neu"])))


if __name__ == "__main__":
    main()
