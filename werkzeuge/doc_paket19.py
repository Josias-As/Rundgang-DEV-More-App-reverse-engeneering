"""Paket 19 (Fix: Datum springt zurück): Einbau-Dokument.
Aufruf: python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/doc_paket19.py  ->  pakete/PAKET_19_FIX_EINGABEN.md"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_app89  # noqa: E402
import rg  # noqa: E402
from doc_paket12_16 import block  # noqa: E402

BL = json.load(open(doc_app89.BLOECKE, encoding="utf-8"))
ERKL = {
    "cboKaMehrfach.OnChange": "**Hauptursache.** Das unsichtbare Kombinationsfeld hängt mit `DefaultSelectedItems` an `WertText`. Ändert das Datum `WertText`, wählt es neu aus, `OnChange` feuert und schrieb \"\" zurück. Jetzt schreibt es nur bei Mehrfachauswahl und nur, wenn sich wirklich etwas ändert.",
    "ddKaAuswahl.OnChange": "Gleiches Muster (`Default = ThisItem.WertText`): schreibt nur bei Auswahl-Punkten und nur bei echter Änderung.",
    "dpKaDatum.OnChange": "Schreibt nur bei Datum/Datum+Uhrzeit. Sonst unverändert.",
    "ddKaStunde.OnChange": "Wie `dpKaDatum`.",
    "ddKaMinute.OnChange": "Wie `dpKaDatum`.",
    "txtKaText.OnChange": "Vorsorglich gleich gebaut: schreibt nur bei Text-Punkten und nur bei echter Änderung.",
}


def main():
    p = [q for q in BL["pakete"] if q["nr"] == 19][0]
    eltern = dict(rg.App(doc_app89.EXPORT).eltern)
    for n, i in BL["neue_controls"].items():
        eltern[n] = i["eltern"]
    z = ["# Paket 19 – Fix: Datum (und andere Eingaben) werden überschrieben", "",
         "Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket19) und `werkzeuge/doc_paket19.py`. "
         "Setzt auf den Stand **nach Paket N + 8–10** auf. Die 6 Properties ändert kein anderes Paket → passt auch, wenn später 12–17/13 eingefügt werden (Reihenfolge egal).", "",
         "## Kurzfassung", "",
         "- **Fehler (Studio-Test 03.11.):** Datum wählen → Feld springt auf „Datum wählen“ zurück, `WertText` bleibt leer, Punkt bleibt offen.",
         "- **Ursache (geschlussfolgert, passt zum Befund):** In jeder Karte liegen alle Eingabe-Steuerelemente, nur das passende ist sichtbar. "
         "Die unsichtbaren hängen mit `Default`/`DefaultSelectedItems` an `ThisItem.WertText`. Schreibt das Datum `WertText`, setzen "
         "`cboKaMehrfach` und `ddKaAuswahl` ihre Auswahl neu, ihr `OnChange` feuert und schreibt \"\" zurück. Derselbe Fehler hätte auch Mehrfachauswahl und Auswahl getroffen.",
         "- **Abhilfe:** Jede Schreibstelle schreibt nur beim eigenen Typ (und Mehrfach/Auswahl/Text nur bei echter Änderung). 6 Properties, keine neuen Steuerelemente, keine Spalten.",
         "- Generator 0 Fehler, Mutation 12/12, Logik-Probe 104/0. **Nicht in Studio getestet.** Nicht unabhängig geprüft (kleiner Fix).", "",
         "## Schritte", ""]
    for i, c in enumerate(p["props"], 1):
        z += block("19.%d" % i, c["key"], doc_app89.de(c["vorher"]), doc_app89.de(c["nachher"]), ERKL[c["key"]], eltern)
    z += ["## Test", "",
          "| # | Schritt | erwartet |", "|---|---|---|",
          "| T1 | „ZZ Test Datum letzte Wartung“: Datum wählen | Datum bleibt stehen, Punkt verschwindet aus „Noch offen“ |",
          "| T2 | Kategorie speichern, wieder öffnen | Datum steht noch da |",
          "| T3 | „Leeren“ | Feld leer, Punkt wieder offen |",
          "| T4 | Datum + Uhrzeit: Datum, Stunde, Minute wählen | alles bleibt stehen, Text „TT.MM.JJJJ HH:MM“ im Protokoll |",
          "| T5 | Mehrfachauswahl: zwei Werte wählen, einen abwählen | Auswahl bleibt, Protokoll zeigt die Werte mit „; “ |",
          "| T6 | Auswahl (Dropdown) und Text | bleiben gespeichert (Gegenprobe) |", "",
          "## Rückweg", "", "Vorher-Fassungen aus dem Anhang einsetzen.", "", "## Anhang – Vorher-Fassungen", ""]
    for c in p["props"]:
        z += ["**`%s` vorher**" % c["key"], "", "```", doc_app89.de(c["vorher"]), "```", ""]
    open(os.path.join(doc_app89.AUS, "PAKET_19_FIX_EINGABEN.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_19_FIX_EINGABEN.md (%d Properties)" % len(p["props"]))


if __name__ == "__main__":
    main()
