# HINWEIS: nach Paket 9 nicht mehr neu erzeugen (Vorher/Nachher-Stand Paket 8 eingefroren, siehe arbeit/2026-11-02_Paket8/gruppen.json)
"""Paket 8 (Abschnitte + Bereich ausblendbar), Teil Builder: Einbau-Dokument aus dem Generator-Stand vorher/nachher.
Aufruf: python3 -I werkzeuge/doc_paket8_builder.py  ->  pakete/builder/PAKET_8_BUILDER.md, arbeit/2026-11-02_Paket8/gruppen.json"""
import difflib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import rg  # noqa: E402

ARB = os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8")
VORHER = json.load(open(os.path.join(ARB, "builder_vorher.json"), encoding="utf-8"))
NACHHER = json.load(open(os.path.join(builder.AUS_ARB, "bloecke.json"), encoding="utf-8"))

NEU = [("conPRest", ["lblPAbschnitt", "txtPAbschnitt"]), ("conEdB", ["lblBZeigen", "galBZeigen"]),
       ("conMehrKarte", ["lblMehrAbschnitt", "txtMehrAbschnitt"])]
GRUPPEN = [
    ("Optik und kleine Werte", ["lblGlHilfe.Height", "lblBInfo.Y", "lblBInfo.Height", "lblBInfo.Text", "lblPKat.Width", "ddPKategorie.Width",
                                "lblHolenLeer.Height", "lblMehrHilfe.Text", "lblPlKopf3.Width", "lblGlInfo.Text", "lblHoInfo.Text"]),
    ("Anzeige des Abschnitts", ["galGl.Items", "galHolen.Items", "lblVsListe.Text", "galAkt.Items", "btnMehrAnlegen.OnSelect"]),
    ("Auswahl wechseln (setzt das Abschnittsfeld zurück)", ["btnGlZeile.OnSelect", "btnGlNeuB.OnSelect", "btnGlNeuK.OnSelect", "btnGlNeuP.OnSelect",
                                                          "btnPrZeile.OnSelect", "ddKBereich.OnChange", "ddPKategorie.OnChange"]),
    ("Lange Formeln", ["btnEdEntf.OnSelect", "galPr.Items", "tmrArbeit.OnTimerEnd"]),
]
ERKL = {
    "galGl.Items": "Die Gliederung zeigt bei Prüfpunkten mit Abschnitt „Abschnitt › Frage“, bei ausgeblendeten Bereichen „ausgeblendet“.",
    "galHolen.Items": "Wie die Gliederung, im Fenster „Holen“.",
    "lblGlInfo.Text": "Die Info-Spalte zeigt jetzt auch beim Bereich etwas an („ausgeblendet“).",
    "lblHoInfo.Text": "Wie lblGlInfo, im Fenster „Holen“.",
    "lblVsListe.Text": "Die Vorschau einer Kategorie zeigt den Abschnitt vor der Frage.",
    "galAkt.Items": "Eine Änderung am Abschnitt zählt beim Aktivieren als „geändert“.",
    "btnMehrAnlegen.OnSelect": "„Mehrere Fragen“ setzt den Abschnitt aus dem neuen Feld für alle neuen Fragen.",
    "btnGlNeuP.OnSelect": "Ein neuer Prüfpunkt übernimmt den Abschnitt des gerade gewählten Prüfpunkts (gleiche Kategorie).",
    "galPr.Items": "Neuer Hinweis, wenn die Fragen eines Abschnitts nicht zusammenstehen (sonst stünde die Überschrift zweimal da).",
    "tmrArbeit.OnTimerEnd": "Kopie, neue Fassung und „Holen“ übernehmen Abschnitt und „Bereich ausblenden“. Dazu das Zurücksetzen des Abschnittsfelds.",
    "btnEdEntf.OnSelect": "Nur das Zurücksetzen des Abschnittsfelds nach dem Entfernen.",
    "lblBInfo.Text": "Erklärt „ausblenden“. Rückt nach unten, weil darüber der neue Schalter steht.",
    "lblMehrHilfe.Text": "Kürzer, damit der Text in eine Zeile passt (Höhe 22).",
}
STANDARD = "Neu ist `Reset(txtPAbschnitt)`. So zeigt das Abschnittsfeld nach jedem Wechsel den richtigen Wert."


def pfad(name):
    teile = [name]
    while teile[-1] in NACHHER["eltern"] and NACHHER["eltern"][teile[-1]]:
        teile.append(NACHHER["eltern"][teile[-1]])
    return " › ".join(reversed(teile))


def diff(alt, neu):
    z = [x for x in difflib.unified_diff(alt.split("\n"), neu.split("\n"), lineterm="", n=0) if not x.startswith(("---", "+++", "@@"))]
    return "\n".join(x if len(x) < 260 else x[:257] + " …" for x in z)


def ende(f):
    z = [x for x in f.strip().split("\n") if x.strip()]
    return z[-1].strip() if z else f


def neue_yaml(eltern, namen):
    s = [c for s in builder.SCREENS for c, _ in builder.alle(s) if c.name == eltern][0]
    out = []
    for k in s.kinder:
        if k.name in namen:
            out += builder.yaml_control(k, "")
    return "\n".join(out)


def main():
    v, n = VORHER["de"], NACHHER["de"]
    alle_geaendert = sorted(k for k in n if k in v and v[k] != n[k])
    in_gruppen = [k for _, ks in GRUPPEN for k in ks]
    assert sorted(in_gruppen) == alle_geaendert, (set(alle_geaendert) ^ set(in_gruppen))
    z = ["# Paket 8 – Abschnitte und Bereich ausblendbar (Teil Builder)", "",
         "Stand 02.11.2026. Erzeugt mit `werkzeuge/builder.py` + `werkzeuge/doc_paket8_builder.py` gegen den Builder-Stand nach F1–F4 "
         "(Export 02.11. + F1–F4 + deine Optik-Änderungen `lblPlAb/lblPlBis.Size` 10, `conPlTermine` X 980/Y 90).", "",
         "## Kurzfassung", "",
         "- **Abschnitt** (neue Textspalte `RG_Pruefpunkte.Abschnitt`): Prüfpunkte einer Kategorie lassen sich gruppieren (z. B. „Kompressor 1“). "
         "Im Builder: Feld „Abschnitt“ beim Prüfpunkt, Anzeige „Abschnitt › Frage“ in Gliederung und Vorschau, „Mehrere Fragen“ mit Abschnitt für alle, "
         "neuer Prüfpunkt übernimmt den Abschnitt, Kopie und Fassungen übernehmen ihn, Prüfhinweis bei unterbrochenem Abschnitt.",
         "- **Bereich ausblenden** (neue Ja/Nein-Spalte `RG_Bereiche.Ausblenden`): Schalter beim Bereich. Die Rundgang-App zeigt den Namen dann nicht "
         "(dieser Teil kommt mit dem Export der Rundgang-App).",
         "- Dazu Optik: 4 Texte, die knapp waren (Prüfung jetzt mit Innenabstand 5 + 5 px).",
         "- Umfang: 2 SharePoint-Spalten, %d neue Steuerelemente (3 Blöcke), %d geänderte Properties in %d Gruppen." % (
             sum(len(x) for _, x in NEU) + 1, len(alle_geaendert), len(GRUPPEN)),
         "- Geprüft: Generator 0 Fehler (neu: Datenvertrag Kopie/Änderungsliste, Textbreiten mit Innenabstand), Mutation 13/13, Logik 27 Szenarien. "
         "**Nicht in Studio getestet.**", "",
         "## Schritt 0 – SharePoint-Spalten (zuerst)", "",
         "| Liste | Spalte | Typ | Standard |", "|---|---|---|---|",
         "| `RG_Pruefpunkte` | `Abschnitt` | Eine Textzeile | leer |", "| `RG_Bereiche` | `Ausblenden` | Ja/Nein | Nein |", "",
         "Danach im Builder: Daten → `RG_Pruefpunkte` und `RG_Bereiche` → ⋯ → **Aktualisieren**. Die Rundgang-App liest die Spalten erst mit ihrem Teil von Paket 8.", "",
         "## Schritt 1 – neue Steuerelemente", ""]
    for eltern, namen in NEU:
        z += ["### In `%s` (`%s`)" % (eltern, pfad(eltern)), "",
              "**Wo hin:** `%s` selbst markieren → Strg+V." % eltern, "", "```yaml", neue_yaml(eltern, namen), "```", ""]
    nr = 2
    anhang = ["## Anhang – Vorher-Fassungen", ""]
    gruppen_json = []
    for titel, keys in GRUPPEN:
        z += ["## Schritt %d – %s" % (nr, titel), ""]
        g = []
        for i, k in enumerate(keys, 1):
            ctl, prop = k.split(".", 1)
            z += ["### %d.%d · `%s`" % (nr, i, k), "", "**Pfad:** `%s` → %s" % (pfad(ctl), prop), "", "```", n[k], "```", "",
                  "```diff", diff(v[k], n[k]), "```", "",
                  "**Kurz erklärt:** " + ERKL.get(k, STANDARD if "Reset(txtPAbschnitt)" in n[k] and "Reset(txtPAbschnitt)" not in v[k] else "Optik/Wert."), "",
                  "**Nachprüfen:** endet auf `%s`" % ende(n[k])[-80:], ""]
            anhang += ["### `%s` (vorher)" % k, "", "```", v[k], "```", ""]
            g.append({"key": k, "pfad": pfad(ctl), "de": n[k], "diff": diff(v[k], n[k]), "erkl": ERKL.get(k, "")})
        gruppen_json.append({"titel": titel, "props": g})
        nr += 1
    z += ["## Test (wenn du testest)", "",
          "1. Prüfpunkt wählen, Abschnitt „Kompressor 1“ eintragen, Tab → Gliederung zeigt „Kompressor 1 › Frage“.",
          "2. „+ Prüfpunkt“ → neuer Punkt hat denselben Abschnitt.",
          "3. Zwei Punkte mit Abschnitt A, dazwischen einer mit B → Prüfung: Hinweis „Abschnitt … ist unterbrochen“.",
          "4. Bereich wählen → „ausblenden“ → Gliederung zeigt beim Bereich „ausgeblendet“.",
          "5. „Mehrere Fragen“ mit Abschnitt „Kältemaschine 1“ → alle neuen Fragen haben ihn.",
          "6. Neue Fassung anlegen → Abschnitte und „ausgeblendet“ sind in der neuen Fassung noch da.", "",
          "## Rückweg", "",
          "Die Vorher-Fassungen stehen im Anhang. Die neuen Steuerelemente können gelöscht werden, die Spalten können bleiben. "
          "Achtung: Wenn `txtPAbschnitt` gelöscht wird, werden alle Formeln mit `Reset(txtPAbschnitt)` rot. Dann erst die Vorher-Fassungen einsetzen.", ""]
    os.makedirs(ARB, exist_ok=True)
    open(os.path.join(builder.AUS_PAKET, "PAKET_8_BUILDER.md"), "w", encoding="utf-8").write("\n".join(z + anhang) + "\n")
    json.dump({"neu": [{"eltern": e, "pfad": pfad(e), "yaml": neue_yaml(e, ns)} for e, ns in NEU], "gruppen": gruppen_json},
              open(os.path.join(ARB, "gruppen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben: pakete/builder/PAKET_8_BUILDER.md, %d Properties" % len(alle_geaendert))


if __name__ == "__main__":
    main()
