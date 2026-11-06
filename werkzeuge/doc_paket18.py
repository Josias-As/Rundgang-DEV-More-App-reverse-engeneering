"""Paket 18 (Zugangscodes): python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket18.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_app89  # noqa: E402
import doc_generisch as g  # noqa: E402

ERKL_APP = {
    "scrKategorie.OnVisible": "Neues Feld `CodeID` in allen drei Zweigen von `colAntworten` (nicht im JSON – `btnKaSpeichern` speichert nur ausgewählte Spalten). Das Code-Fenster ist beim Öffnen zu.",
    "lblKaFrage.Width": "Platz für den 🔑-Knopf.",
}
ERKL_B = {
    "App.OnStart": "Startwerte `varCodeOffen`, `varZcID`.",
    "txtPHinweis.Width": "Etwas schmaler für den 🔑-Knopf daneben.",
    "lblVsRegeln.Text": "Vorschau nennt den Zugangscode.",
    "galAkt.Items": "Änderung des Codes zählt als „geändert“.",
    "tmrArbeit.OnTimerEnd": "Kopie/neue Fassung übernehmen den Code.",
    "btnGlNeuP.OnSelect": "Neuer Prüfpunkt ohne Code.",
    "btnMehrAnlegen.OnSelect": "Wie btnGlNeuP.",
}
SP = ["- Neue Liste **`RG_Zugangscodes`**: `Title` (vorhanden, = Bezeichnung), `Code` (Eine Textzeile), `Hinweis` (Mehrere Textzeilen, nur Text), `Aktiv` (Ja/Nein, Standard Ja).",
      "- **Berechtigung:** Lesen für alle Prüfer (wie die anderen RG-Listen). Bedien-Codes sind damit für jeden mit Listenzugriff in SharePoint lesbar – deshalb nie echte Passwörter.",
      "- `RG_Pruefpunkte`: neue Spalte **`ZugangscodeID`** (Zahl, Standard 0).",
      "- Rundgang DEV: Daten → `RG_Pruefpunkte` → ⋯ → Aktualisieren, dann Daten hinzufügen → SharePoint → IMS+ → `RG_Zugangscodes`."]


def main():
    za, na, neu_a, anh_a = g.app_teil(18, ERKL_APP, SP, zusatz_vor=["**Kurzzeitig rot (erwartet):** `btnKaCode` nennt `ThisItem.CodeID`, das erst A3.1 (`scrKategorie.OnVisible`) anlegt.", ""])
    zb, keys_b, neu_b, anh_b = g.builder_teil("builder_nach_p23.json", "builder_nach_p18.json", ERKL_B,
                                               ["Liste und Spalte aus A1 (nur einmal anlegen). Builder: `RG_Pruefpunkte` aktualisieren, `RG_Zugangscodes` hinzufügen."])
    z = ["# Paket 18 – Zugangscodes (Bedien-Codes, erst nach Antippen sichtbar)", "",
         "Stand 06.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket18), `werkzeuge/builder.py`, `werkzeuge/doc_paket18.py`. Voraussetzung: Paket 23 in beiden Apps.", "",
         "## Kurzfassung", "",
         "- Eigene Liste `RG_Zugangscodes`. Im Builder am Prüfpunkt über den Knopf **🔑** neben dem Hinweis zuordnen; Codes pflegen unter Übersicht › Anleitungen › **Zugangscodes**.",
         "- In der Rundgang-App: runder Knopf **🔑** oben rechts in der Karte. Erst nach Antippen öffnet sich ein Fenster mit dem Code (groß) und dem Hinweis. Der Code wird erst dann gelesen.",
         "- **Nie** im Protokoll, PDF, in Mängeln oder im JSON: Der Code liegt nur in der Liste und in einer Variablen, solange das Fenster offen ist.",
         "- Echte Passwörter kommen nicht in die App: Code leer lassen und im Hinweis z. B. „Code bei der IT (Herr …)“ eintragen.",
         "- Umfang: App %d Properties + Knopf + Fenster; Builder %d Properties + %s. Generatoren 0 Fehler, Mutation 12/12 und 13/13. **Nicht in Studio getestet.**"
         % (na, len(keys_b), ", ".join("`%s`" % x for x in neu_b)), ""] + za + zb + [
         "## Test", "",
         "| # | Schritt | erwartet |", "|---|---|---|",
         "| T1 | Builder: Anleitungen › Zugangscodes › „+ Zugangscode“: „Bedienteil Kältemaschine 1“, Code 1234 | Eintrag in der Liste |",
         "| T2 | Prüfpunkt öffnen › 🔑 › Code wählen › Fertig | 🔑 hellblau, Vorschau „• 🔑 Zugangscode …“ |",
         "| T3 | Rundgang DEV: Kategorie öffnen | 🔑 rechts oben in der Karte; Code nirgends sichtbar |",
         "| T4 | 🔑 antippen | Fenster mit „1234“ und Hinweis, Schließen |",
         "| T5 | Kategorie speichern, Protokoll ansehen | Code steht nirgends (auch nicht im JSON `Antworten` der Liste) |",
         "| T6 | Code im Builder inaktiv stellen → App 🔑 | „kein Code hinterlegt“ |",
         "| T7 | Code ohne Wert, nur Hinweis „Code bei der IT“ | Fenster zeigt „—“ und den Hinweis |",
         "| T8 | Code in SharePoint löschen → App 🔑 | „kein Code hinterlegt“; Builder-Auswahl zeigt „… (inaktiv oder gelöscht)“ |",
         "| T9 | Prüfpunkt mit Bild + ⓘ + 🔑 | drei Knöpfe nebeneinander, Frage gekürzt, nichts überlappt |", "",
         "## Rückweg", "", "Vorher-Fassungen einsetzen; neue Steuerelemente löschen. Liste/Spalte dürfen bleiben.", "",
         "## Anhang – Vorher-Fassungen", ""] + anh_a + anh_b
    open(os.path.join(doc_app89.AUS, "PAKET_18_ZUGANGSCODES.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_18_ZUGANGSCODES.md (App %d, Builder %d, neu App %s, neu Builder %s)" % (na, len(keys_b), neu_a, neu_b))


if __name__ == "__main__":
    main()
