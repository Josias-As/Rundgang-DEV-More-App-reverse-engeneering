"""Paket 9 (Rückfrage, kritischer Mangel, Ansprechpartner), Teil Builder: Einbau-Dokument.
Vorher = Builder nach Paket 8 (arbeit/2026-11-02_Paket8/builder_nach_p8.json).
Aufruf: python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket9_builder.py  ->  pakete/builder/PAKET_9_BUILDER.md"""
import difflib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import rg  # noqa: E402

VORHER = json.load(open(os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8", "builder_nach_p8.json"), encoding="utf-8"))
NACHHER = json.load(open(os.path.join(builder.AUS_ARB, "bloecke.json"), encoding="utf-8"))

ERKL = {
    "App.OnStart": "Zwei neue Startwerte: `varNioOffen` (Fenster „Bei n.i.O.“) und `varKoID` (gewählter Ansprechpartner).",
    "lblVsRegeln.Text": "Die Vorschau nennt „Rückfrage“ und „KRITISCH“.",
    "galAkt.Items": "Änderungen an Rückfrage/kritisch/Ansprechpartnern zählen beim Aktivieren als „geändert“.",
    "galPr.Items": "Zwei neue Hinweise: Rückfrage/kritisch bei einem Typ, wo es nicht wirkt, und kritisch ohne eigenen Ansprechpartner.",
    "tmrArbeit.OnTimerEnd": "Kopie, neue Fassung und „Holen“ übernehmen die fünf neuen Felder.",
}


def pfad(name):
    t = [name]
    while t[-1] in NACHHER["eltern"] and NACHHER["eltern"][t[-1]]:
        t.append(NACHHER["eltern"][t[-1]])
    return " › ".join(reversed(t))


def diff(a, b):
    z = [x for x in difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm="", n=0) if not x.startswith(("---", "+++", "@@"))]
    return "\n".join(x if len(x) < 240 else x[:237] + " …" for x in z)


def finde(name):
    for s in builder.SCREENS:
        for c, _ in builder.alle(s):
            if c.name == name:
                return c, s
    raise KeyError(name)


def yaml_von(name):
    c, s = finde(name)
    if c is s:
        return builder.yaml_screen(c).rstrip("\n")
    return "\n".join(builder.yaml_control(c, ""))


def main():
    v, n = VORHER["de"], NACHHER["de"]
    geaendert = sorted(k for k in n if k in v and v[k] != n[k])
    assert geaendert == sorted(ERKL), geaendert
    neu_top = ["scrKontakte", "btnLiKontakte", "btnPNio", "conNio"]
    z = ["# Paket 9 – Kritischer Mangel, Rückfrage, Ansprechpartner (Teil Builder)", "",
         "Stand 02.11.2026. Erzeugt mit `werkzeuge/builder.py` + `werkzeuge/doc_paket9_builder.py`. **Voraussetzung: Paket 8 (Builder) vollständig eingefügt** "
         "(`PAKET_8_BUILDER.md`, Schritt 0–5). Die Formeln hier enthalten die Änderungen von Paket 8 schon.", "",
         "## Kurzfassung", "",
         "- Neuer Bildschirm **„Ansprechpartner“** (aus der Übersicht): Gewerk/Rolle, Name, Telefon, Hinweis, „bei jedem kritischen Mangel“, aktiv/inaktiv.",
         "- Im Prüfpunkt-Editor unten ein Knopf **„Bei n.i.O.: …“**. Er öffnet ein Fenster: Rückfrage an/aus mit Text, kritisch ja/nein mit Text, Ansprechpartner antippen.",
         "- Kopie, neue Fassung, Änderungsliste und Prüfung kennen die fünf neuen Felder.",
         "- Umfang: neue Liste + 5 Spalten (gemeinsam mit der Rundgang-App), 1 neuer Bildschirm, 3 neue Blöcke im Editor/Übersicht, %d geänderte Properties." % len(geaendert),
         "- Geprüft: Generator 0 Fehler (Datenvertrag, Textbreiten mit Innenabstand), Mutation 13/13, Logik 27 Szenarien. **Nicht in Studio getestet. Nicht unabhängig geprüft.**", "",
         "## Schritt 0 – SharePoint und Datenquellen", "",
         "Die Liste `RG_Ansprechpartner` und die 5 Spalten an `RG_Pruefpunkte` sind dieselben wie im App-Teil (`pakete/PAKET_8_9_APP.md`, Schritt 1). Nur einmal anlegen.", "",
         "Im Builder: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**, dann **Daten hinzufügen** → SharePoint → IMS+ → `RG_Ansprechpartner`.", "",
         "## Schritt 1 – App.OnStart", "",
         "**Pfad:** App → OnStart. Ganze Formel ersetzen.", "", "```", n["App.OnStart"], "```", "",
         "```diff", diff(v["App.OnStart"], n["App.OnStart"]), "```", "", "**Kurz erklärt:** " + ERKL["App.OnStart"], "",
         "## Schritt 2 – neuer Bildschirm „Ansprechpartner“", "",
         "**Wo hin:** In der Strukturansicht einen Bildschirm markieren (z. B. `scrPlan`) → Strg+V. Studio legt `scrKontakte` mit allen Steuerelementen an.", "",
         "```yaml", yaml_von("scrKontakte"), "```", "",
         "**Nachprüfen:** `scrKontakte` ist da, kein `_1`. Rot ist nur `RG_Ansprechpartner`, falls die Datenquelle noch fehlt.", "",
         "## Schritt 3 – Knopf in der Übersicht", "",
         "**Wo hin:** **`scrListe`** markieren → Strg+V.", "", "```yaml", yaml_von("btnLiKontakte"), "```", "",
         "## Schritt 4 – Knopf „Bei n.i.O.“ im Prüfpunkt-Editor", "",
         "**Wo hin:** **`conEdP`** (`%s`) markieren → Strg+V." % pfad("conEdP"), "", "```yaml", yaml_von("btnPNio"), "```", "",
         "**Rot bis Schritt 5:** `txtNioRueckText`, `txtNioKritText` (kommen mit dem Fenster).", "",
         "## Schritt 5 – Fenster „Bei n.i.O.“", "",
         "**Wo hin:** **`scrEditor`** markieren → Strg+V. Danach ist nichts mehr rot.", "", "```yaml", yaml_von("conNio"), "```", "",
         "## Schritt 6 – geänderte Formeln", ""]
    for i, k in enumerate(["lblVsRegeln.Text", "galAkt.Items", "galPr.Items", "tmrArbeit.OnTimerEnd"], 1):
        ctl, prop = k.split(".", 1)
        z += ["### 6.%d · `%s`" % (i, k), "", "**Pfad:** `%s` → %s" % (pfad(ctl), prop), "", "```", n[k], "```", "",
              "```diff", diff(v[k], n[k]), "```", "", "**Kurz erklärt:** " + ERKL[k], "",
              "**Nachprüfen:** endet auf `%s`" % [x for x in n[k].strip().split("\n") if x.strip()][-1].strip()[-80:], ""]
    z += ["## Test (wenn du testest)", "",
          "1. Übersicht → „Ansprechpartner“ → „+ Ansprechpartner“: „Elektriker“, Name, Telefon. Zweiter: „Allgemein“, „bei jedem“ = ja.",
          "2. Testrundgang bearbeiten → Prüfpunkt → „Bei n.i.O.: nichts Besonderes ›“ → Rückfrage an + Text, kritisch ja + Text, „Elektriker“ antippen (✓).",
          "3. Knopf zeigt „⚠ Bei n.i.O.: Rückfrage + kritisch ›“ in Rot, Vorschau nennt beides.",
          "4. Aktivieren → Änderungsliste zeigt den Punkt als „geändert“. Neue Fassung → Einstellungen sind noch da.",
          "5. In der Rundgang-App (nach Paket 8+9 App): Ablauf aus `PAKET_8_9_APP.md`, Test T3–T7.", "",
          "## Rückweg", "", "Vorher-Fassungen im Anhang. `scrKontakte`, `btnLiKontakte`, `btnPNio`, `conNio` löschen. Liste und Spalten dürfen bleiben.", "",
          "## Anhang – Vorher-Fassungen (Stand nach Paket 8)", ""]
    for k in geaendert:
        z += ["**`%s` vorher**" % k, "", "```", v[k], "```", ""]
    open(os.path.join(builder.AUS_PAKET, "PAKET_9_BUILDER.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/builder/PAKET_9_BUILDER.md, %d Properties, neu: %s" % (len(geaendert), ", ".join(neu_top)))


if __name__ == "__main__":
    main()
