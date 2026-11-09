"""Paket 24 (ein Info-Knopf ⓘ): python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket24.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_app89  # noqa: E402
import doc_generisch as g  # noqa: E402

ERKL_APP = {
    "btnKaInfo.Visible": "ⓘ erscheint, wenn eine (aktive) Anleitung **oder** ein Beispielbild hinterlegt ist.",
    "btnKaInfo.X": "ⓘ steht ganz rechts (der Bild-Knopf entfällt).",
    "btnKaInfo.OnSelect": "Öffnet das Fenster auch ohne Anleitung (nur Bild). `varInfoID` ist jetzt nur noch „Fenster offen“ (1). Anleitung gelöscht und kein Bild → Meldung.",
    "btnKaBild.Visible": "Der alte Bild-Knopf wird ausgeblendet. **Besser:** `btnKaBild` und das alte Bild-Fenster `conKaBild` ganz löschen – keine andere Formel verweist darauf (maschinell geprüft). Dann diesen Schritt überspringen.",
    "btnKaCode.X": "🔑 rückt neben ⓘ.",
    "lblKaFrage.Width": "Platz nur noch für ⓘ und 🔑.",
    "lblKaInfoTitel.Text": "Nur Bild: „ⓘ Beispielbild“, darunter wie bisher „zu: <Frage>“. Mit Anleitung: ⓘ + Titel der Anleitung.",
    "lblKaInfoText.Height": "Ohne Anleitung Höhe 0 → das Bild bekommt den ganzen Platz.",
    "imgKaInfo.Y": "Bild direkt unter dem Text (bzw. oben, wenn es keinen Text gibt).",
    "imgKaInfo.Height": "Bild füllt den Rest bis über „Schließen“.",
}


def main():
    za, na, _, anh_a = g.app_teil(24, ERKL_APP, ["Keine neuen Spalten oder Listen."])
    zb, keys_b, neu_b, anh_b = g.builder_teil("builder_nach_p11.json", None, {
        "lblPAnl.Text": "„Info ⓘ: Anleitung“.", "lblPBild.Text": "„Info ⓘ: Beispielbild“.",
        **{k: "Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts." for k in (
            "btnPBild.Width", "btnPBild.X", "btnPCode.Height", "btnPCode.X", "btnPCode.Y", "ddPAnl.X", "ddPAnl.Y", "lblPAnl.X", "lblPAnl.Y",
            "lblPBild.Width", "lblPBild.X", "lblPHinweis.Width", "lblPHinweis.X", "lblPHinweis.Y", "txtPHinweis.Height", "txtPHinweis.Width",
            "txtPHinweis.X", "txtPHinweis.Y")},
    }, ["Keine neuen Daten."])
    z = ["# Paket 24 – Ein Info-Knopf ⓘ für Anleitung und Beispielbild", "",
         "Stand 06.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket24), `werkzeuge/builder.py`, `werkzeuge/doc_paket24.py`. Voraussetzung: Paket 23, 18, 11 und **25 (Rückbau Prüferauswahl)** in beiden Apps. Nach Paket 25 neu geprüft: keine gemeinsame Property, Vorher-Fassungen unverändert gültig.", "",
         "## Kurzfassung", "",
         "- **Rundgang DEV:** Pro Prüfpunkt nur noch **ein** runder Knopf **ⓘ** oben rechts, sichtbar bei Anleitung, Beispielbild oder beidem. Der Bild-Knopf („Bild“) und sein Fenster entfallen.",
         "- Das Fenster passt sich an: **nur Text** → Text auf voller Höhe; **nur Bild** → großes Bild, Überschrift „ⓘ Beispielbild“, darunter die Frage; **beides** → Text oben, Bild unten (wie bisher).",
         "- **Builder:** Im Prüfpunkt steht in der Zeile „Info ⓘ“ links die **Anleitung**, rechts das **Beispielbild** – unabhängig, beide optional. Der Hinweis für den Prüfer rückt dafür nach oben rechts neben „Foto“ (mit 🔑). Ein Bild pro Prüfpunkt.",
         "- Umfang: App %d Properties (+ 2 Steuerelemente löschen); Builder %d Properties (nur Lage/Text). Keine Daten. Generatoren 0 Fehler, Mutation 12/12 und 13/13. **Nicht in Studio getestet.** Leicht unabhängig geprüft, Befunde eingearbeitet (`arbeit/2026-11-06_Paket24/pruefung_unabhaengig.md`)." % (na, len(keys_b)), ""] + za + zb + [
         "## Test", "",
         "| # | Schritt | erwartet |", "|---|---|---|",
         "| T1 | Prüfpunkt nur mit Anleitung | ⓘ → Text auf voller Höhe, kein Bildbereich |",
         "| T2 | Prüfpunkt nur mit Beispielbild (lange Frage) | ⓘ → „ⓘ Beispielbild“, darunter „zu: …“, großes Bild |",
         "| T3 | Prüfpunkt mit beidem | Text oben, Bild unten |",
         "| T4 | Prüfpunkt mit ⓘ + 🔑 | zwei runde Knöpfe rechts, Frage gekürzt, nichts überlappt |",
         "| T5 | Anleitung inaktiv, Bild vorhanden | ⓘ zeigt nur das Bild (inaktive Anleitungen kommen seit Paket 13 als `AnlID` 0 an) |",
         "| T5b | Anleitung in SharePoint gelöscht, kein Bild | ⓘ → Meldung „Die Anleitung wurde nicht gefunden.“ |",
         "| T5c | `btnKaBild`/`conKaBild` gelöscht | App-Prüfung ohne neue Fehler |",
         "| T6 | Builder: Prüfpunkt öffnen | Zeile „Info ⓘ: Anleitung“ links, „Info ⓘ: Beispielbild“ rechts; Hinweis oben rechts mit 🔑 |", "",
         "## Rückweg", "", "Vorher-Fassungen einsetzen. Falls `btnKaBild`/`conKaBild` gelöscht wurden: aus Paket 6 (YAML) wieder einfügen.", "",
         "## Anhang – Vorher-Fassungen", ""] + anh_a + anh_b
    open(os.path.join(doc_app89.AUS, "PAKET_24_INFO_KNOPF.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_24_INFO_KNOPF.md (App %d, Builder %d: %s)" % (na, len(keys_b), keys_b))


if __name__ == "__main__":
    main()
