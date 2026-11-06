"""Paket 23 (A8 Banner, A11 Testkennung, A7 Ansprechpartner, A6 Entfernen): Einbau-Dokument App + Builder.
Aufruf: python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket23.py
Vorher Builder = arbeit/2026-11-02_Paket8/builder_nach_p13.json (Stand nach 13)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import doc_app89  # noqa: E402
import rg  # noqa: E402
from doc_paket12_16 import block  # noqa: E402

BL = json.load(open(doc_app89.BLOECKE, encoding="utf-8"))
BV = json.load(open(os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8", "builder_nach_p13.json"), encoding="utf-8"))
BN = json.load(open(os.path.join(builder.AUS_ARB, "bloecke.json"), encoding="utf-8"))

ERKL_APP = {
    "btnStartTagLaden.OnSelect": "Liest zu den offenen Läufen auch `TestDatensatz` mit (nur eine Spalte mehr in `ShowColumns`).",
    "conStartOffen.Visible": "Der Hinweis erscheint nur für echte offene Läufe vor heute. Testläufe zählen nicht mehr.",
    "lblStartOffen.Text": "Zeigt den gewählten offenen Lauf. Bei mehreren steht „(2/5)“ dahinter.",
    "lblStartOffen.Width": "Platz für den neuen Knopf „Weiter ›“, wenn es mehrere gibt.",
    "btnStartOffen.OnSelect": "„Öffnen“ öffnet den gerade angezeigten Lauf (nicht mehr immer den ältesten).",
    "btnRgAktion.OnSelect": "**A11:** Ein Lauf ist Test, wenn der Rundgang die neue Spalte `Testrundgang` = Ja hat. Der Name („ZZ Test“) spielt keine Rolle mehr. Sonst unverändert.",
}
ERKL_B = {
    "btnEdEntf.OnSelect": "Unverändert in der Wirkung – nur weil sich der Warntext geändert hat (falls Studio ihn hier zeigt).",
    "lblEdArt.Text": "**A6:** Beim Entfernen eines Prüfpunkts steht dabei, wie viele Fragen davon abhängen (Bedingung oder Vergleich). Die fallen beim Entfernen weg – das war schon so, jetzt sieht man es vorher.",
    "lblLiInfo.Text": "**A11:** Zeigt „· Testrundgang“ in der Übersicht.",
    "lblPlHinweis.Text": "**A11:** Hinweis, was „Testrundgang“ bewirkt.",
    "galNioKontakte.Items": "**A7:** Zeigt auch inaktive Ansprechpartner, **wenn** sie an diesem Prüfpunkt eingetragen sind (unten, zum Entfernen).",
    "btnNioKontakt.Text": "**A7:** Kennzeichnet inaktive mit „(inaktiv – entfernen)“. Antippen nimmt sie heraus.",
    "btnPNio.OnSelect": "**A7:** Das Fenster liest die Ansprechpartner frisch und vollständig (auch inaktive).",
    "lblNioLeer.Visible": "**A7:** „Noch keine Ansprechpartner“ zählt nur aktive.",
    "scrKontakte.OnVisible": "**A7:** Liest zusätzlich, an welchen kritischen Prüfpunkten wer eingetragen ist (`colKoNutz`).",
}


def app_teil():
    p = [q for q in BL["pakete"] if q["nr"] == 23][0]
    eltern = dict(rg.App(doc_app89.EXPORT).eltern)
    for n, i in BL["neue_controls"].items():
        eltern[n] = i["eltern"]
    alle = doc_app89.neue_bis(BL, 23)
    z = ["## Teil A – Rundgang DEV", "",
         "### A1 – SharePoint (zuerst)", "",
         "- `RG_Rundgaenge`: neue Spalte **`Testrundgang`** (Ja/Nein, Standard **Nein**).",
         "- Danach bei den Test-Rundgängen auf **Ja** setzen: „ZZ Test Infrastrukturrundgang“ (ID 3), „ZZ Test Funktionsrundgang“ (ID 4) und alle weiteren ZZ-Test-Rundgänge "
         "(im Builder unter „Plan“ → „○ Testrundgang“, oder in der Liste). **Ohne diesen Schritt zählen neue Läufe dieser Rundgänge als echt.**",
         "- Rundgang DEV: Daten → `RG_Rundgaenge` → ⋯ → Aktualisieren.", "",
         "### A2 – Properties", ""]
    for i, c in enumerate(p["props"], 1):
        z += block("A2.%d" % i, c["key"], doc_app89.de(c["vorher"]), doc_app89.de(c["nachher"]), ERKL_APP[c["key"]], eltern)
    z += ["### A3 – neuer Knopf „Weiter ›“", "", "**Wo hin:** in der Strukturansicht **`conStartOffen`** markieren → Strg+V.", "",
          "```yaml"] + doc_app89.yaml_block("btnStartOffenWeiter", alle) + ["```", ""]
    return z, len(p["props"])


def builder_teil():
    v, n = BV["de"], BN["de"]
    geaendert = sorted(k for k in n if k in v and v[k] != n[k])
    neu = sorted(k for k in n if k not in v)
    eltern = BN["eltern"]

    def finde(name):
        for s in builder.SCREENS:
            for c, _ in builder.alle(s):
                if c.name == name:
                    return c
        raise KeyError(name)
    neue_ctl = sorted({k.split(".")[0] for k in neu})
    z = ["## Teil B – Builder", "", "### B0 – Daten", "", "Spalte aus A1. Builder: Daten → `RG_Rundgaenge` → ⋯ → Aktualisieren.", ""]
    for name in neue_ctl:
        c = finde(name)
        z += ["### B1 – neues Steuerelement `%s`" % name, "", "**Wo hin:** **`%s`** markieren → Strg+V." % eltern.get(name, "?"), "",
              "```yaml"] + builder.yaml_control(c, "") + ["```", ""] + (
            ["**Kurzzeitig rot:** `colKoNutz` gibt es erst nach B2.8 (`scrKontakte.OnVisible`). Erwartet.", ""] if name == "lblKoNutzung" else [])
    for i, k in enumerate(geaendert, 1):
        z += block("B2.%d" % i, k, v[k], n[k], ERKL_B.get(k, "Siehe Kurzfassung."), eltern)
    return z, geaendert, neue_ctl


def main():
    za, na = app_teil()
    zb, keys_b, neue_b = builder_teil()
    z = ["# Paket 23 – Banner „Nicht abgeschlossen“, Testkennung, Ansprechpartner, Entfernen-Warnung", "",
         "Stand 06.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket23), `werkzeuge/builder.py` und `werkzeuge/doc_paket23.py`. "
         "Voraussetzung: alle Pakete bis 13 in beiden Apps (Stand Einsetz-Chat 06.11.).", "",
         "## Kurzfassung", "",
         "- **A8 (App):** Der rote Hinweis „Nicht abgeschlossen“ auf der Startseite zeigt keine Testläufe mehr. Gibt es mehrere offene Läufe, blättert **„Weiter ›“** durch alle, „Öffnen“ öffnet den angezeigten.",
         "- **A11 (App + Builder):** Test ist ein Rundgang jetzt über die neue Spalte **`Testrundgang`**, nicht mehr über den Namen „ZZ Test“. Pflegen im Builder unter **Plan → „○ Testrundgang“**; die Übersicht zeigt „· Testrundgang“. "
         "Gilt für **neue** Läufe; bestehende Läufe behalten ihr `TestDatensatz`.",
         "- **A7 (Builder):** Im Fenster „Bei n.i.O.“ erscheinen eingetragene, aber inaktive Ansprechpartner („inaktiv – entfernen“) und lassen sich herausnehmen. "
         "Unter „Ansprechpartner“ steht je Eintrag, bei wie vielen kritischen Prüfpunkten in wie vielen Rundgängen er eingetragen ist; inaktiv + verwendet ist rot.",
         "- **A6 (Builder):** Beim Entfernen eines Prüfpunkts warnt der Text, wenn andere Fragen über Bedingung oder Vergleich davon abhängen.",
         "- **A1:** Der Generator schreibt in der deutschen Formelleiste jetzt `.Miniaturansicht.` statt `.Thumbnail.` (Paket 13 und alle späteren). In YAML-Blöcken bleibt der interne Name `Thumbnail` (wie im Export).",
         "- Umfang: App %d Properties + 1 Knopf + 1 Spalte; Builder %d Properties%s. Generatoren 0 Fehler, Mutation 12/12 und 13/13, Textbreiten geprüft. **Nicht in Studio getestet.** Leicht unabhängig geprüft, Befunde eingearbeitet (`arbeit/2026-11-06_Paket23/pruefung_unabhaengig.md`)."
         % (na, len(keys_b), (" + " + ", ".join(neue_b)) if neue_b else ""), ""] + za + zb + [
         "## Test", "",
         "| # | Schritt | erwartet |", "|---|---|---|",
         "| T1 | Startseite öffnen. Die ZZ-Test-Läufe 18, 20–22 (02./03.11., `TestDatensatz` = Ja) sind noch offen | kein roter Hinweis für diese |",
         "| T2 | zwei echte offene Läufe an früheren Tagen (z. B. ID 19 + einen echten Lauf an einem anderen Tag anfangen und nicht abschließen) | Hinweis „… (1/2)“, „Weiter ›“ → „(2/2)“, „Öffnen“ öffnet den angezeigten |",
         "| T3 | Builder: Plan → „○ Testrundgang“ | „✓ Testrundgang“, Übersicht „· Testrundgang“ |",
         "| T4 | App: Lauf dieses Rundgangs starten | `TestDatensatz` = Ja (Konsole/Liste), Protokoll „TESTDATEN“, Fotos unter `TEST/` (bestehendes Verhalten, hängt an `TestDatensatz`) |",
         "| T5 | Rundgang mit Namen „ZZ Test …“, Testrundgang = Nein | Lauf zählt als echt (Absicht) |",
         "| T6 | Builder: Ansprechpartner inaktiv stellen, der an einem kritischen Prüfpunkt hängt | rote Zeile „Eingetragen bei 1 …“; im Prüfpunkt „Bei n.i.O.“: „(inaktiv – entfernen)“, antippen → weg |",
         "| T7 | Builder: Prüfpunkt entfernen, an dem eine Bedingung hängt | Warntext „Achtung: 1 Frage hängt davon ab …“ |", "",
         "## Rückweg", "", "Vorher-Fassungen einsetzen, `btnStartOffenWeiter`%s löschen. Spalte darf bleiben." % ("".join(", `%s`" % x for x in neue_b)), "",
         "## Anhang – Vorher-Fassungen", ""]
    p = [q for q in BL["pakete"] if q["nr"] == 23][0]
    for c in p["props"]:
        z += ["**Rundgang DEV `%s` vorher**" % c["key"], "", "```", doc_app89.de(c["vorher"]), "```", ""]
    for k in keys_b:
        z += ["**Builder `%s` vorher**" % k, "", "```", BV["de"][k], "```", ""]
    open(os.path.join(doc_app89.AUS, "PAKET_23_BANNER_TEST_KONTAKTE.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_23_BANNER_TEST_KONTAKTE.md (App %d, Builder %d Properties, neu: %s)" % (na, len(keys_b), neue_b))


if __name__ == "__main__":
    main()
