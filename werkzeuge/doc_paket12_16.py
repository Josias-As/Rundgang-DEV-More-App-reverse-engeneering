"""Paket 12 (eigene Antwortwörter) + Paket 16 („nicht messbar“): Einbau-Dokumente für Rundgang-App und Builder.
Aufruf: python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket12_16.py
Vorher Rundgang-App = Stand nach Paket 8–10, Vorher Builder = Stand nach Paket 9 (arbeit/2026-11-02_Paket8/builder_nach_p9.json)."""
import difflib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import doc_app89  # noqa: E402
import rg  # noqa: E402

BL = json.load(open(doc_app89.BLOECKE, encoding="utf-8"))
BV = json.load(open(os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8", "builder_nach_p9.json"), encoding="utf-8"))
BN = json.load(open(os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8", "builder_nach_p12_16.json"), encoding="utf-8"))  # eingefroren nach 12+16

KURZ = [
    "- **Paket 12 – eigene Antwortwörter:** Bei i.O./n.i.O.-Fragen lassen sich die Knöpfe umbenennen, z. B. „durchgeführt“ / „nicht durchgeführt“ (Legionellen). "
    "Intern bleibt es i.O./n.i.O.: „nicht durchgeführt“ ergibt weiter einen Mangel. Leer = „i.O.“/„n.i.O.“ wie bisher. Protokoll zeigt die eigenen Wörter. Höchstens 18 Zeichen.",
    "- **Paket 16 – „nicht messbar“:** Bei Zahlen, für die es im Builder erlaubt ist, gibt es den Knopf „nicht messbar“ (z. B. Anlage aus). Dann ist das Feld leer, "
    "die Frage gilt als beantwortet, aber eine **Begründung (Kommentar) ist Pflicht**. Im Protokoll steht „nicht messbar“ statt „0“. Kein Mangel.",
]
ERKL_APP = {
    "scrKategorie.OnVisible": "Neue Felder `TextIO`, `TextNIO`, `NMErlaubt` in allen drei Zweigen.",
    "btnKaSpeichern.OnSelect": "Speichert die Knopf-Wörter mit (für Protokoll und Nur-Ansicht).",
    "btnKaIO.Text": "Eigenes Wort oder „i.O.“.",
    "btnKaNIO.Text": "Eigenes Wort oder „n.i.O.“.",
    "btnKaIO.Width": "Breiter (250), wenn ein Wort länger als 8 Zeichen ist.",
    "btnKaNIO.Width": "Wie btnKaIO.Width.",
    "btnKaNIO.X": "Steht immer 16 px rechts vom i.O.-Knopf.",
    "htmProtokoll.HtmlText": "Protokoll zeigt die eigenen Wörter, Spalte etwas breiter (110 px).",
    "App.Formulas": "„nicht messbar“ zählt als beantwortet (`fnFehltGrund`) und braucht einen Kommentar (`fnKommentarNoetig`).",
    "txtKaZahl.OnChange": "Eine eingetippte Zahl hebt „nicht messbar“ wieder auf.",
    "lblKaZahlInfo.Width": "Macht Platz für den neuen Knopf.",
    "lblKaZahlInfo.Size": "Etwas kleiner, solange der Knopf „nicht messbar“ da ist (sonst wird „… bitte begründen“ abgeschnitten).",
    "btnKaIO.Size": "Schrift 14 statt 17 bei Wörtern über 12 Zeichen.",
    "btnKaNIO.Size": "Wie btnKaIO.Size.",
    "lblKaRueckFrage.Text": "Rückfrage zeigt das eigene Wort statt „n.i.O.“.",
    "btnKaKritVersehen.Text": "„… war ein Versehen“ mit dem eigenen Wort.",
}
ERKL_BUILDER = {
    "lblKInfo.Text": "Erklärtext: Kategorien in beliebiger Reihenfolge (seit Paket 10).",
    "conPRest.Y": "Bei i.O./n.i.O. rückt der untere Teil unter die neuen Felder.",
    "btnPNio.Y": "Wie conPRest.Y.",
    "btnVsIO.Text": "Vorschau zeigt das eigene Wort.",
    "btnVsNIO.Text": "Vorschau zeigt das eigene Wort.",
    "btnVsIO.Width": "Vorschau-Knöpfe breiter bei langen Wörtern.",
    "btnVsNIO.Width": "Wie btnVsIO.Width.",
    "btnVsNIO.X": "Steht immer neben dem i.O.-Knopf.",
    "lblVsRegeln.Text": "Vorschau nennt „nicht messbar erlaubt“.",
    "galAkt.Items": "Änderungen an Wörtern und „nicht messbar“ zählen als „geändert“.",
    "galPr.Items": "Hinweis, wenn eigene Wörter bei einem anderen Typ eingetragen sind.",
    "tmrArbeit.OnTimerEnd": "Kopie/neue Fassung übernehmen die drei neuen Felder. Dazu das Zurücksetzen der neuen Eingabefelder.",
    "btnMehrAnlegen.OnSelect": "„Mehrere Fragen“ legt die neuen Felder leer an.",
    "btnGlNeuP.OnSelect": "Neuer Prüfpunkt mit leeren Wörtern. Dazu das Zurücksetzen der neuen Eingabefelder.",
}
STD = "Neu ist `Reset(txtPTextIO)` und `Reset(txtPTextNIO)`: Die neuen Felder zeigen nach jedem Wechsel den richtigen Wert."


def _fenster(x, i):
    """Lange Zeile: Ausschnitt um die erste unterschiedliche Stelle i (Vorzeichen bleibt vorn)."""
    if len(x) < 240:
        return x
    von = max(1, i - 60)
    return x[0] + " " + ("… " if von > 1 else "") + x[von:von + 180].strip() + " …"


def diff(a, b):
    z = [x for x in difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm="", n=0) if not x.startswith(("---", "+++", "@@"))]
    minus = [x for x in z if x.startswith("-")]
    plus = [x for x in z if x.startswith("+")]
    aus = []
    for x in z:
        partner = plus if x.startswith("-") else minus
        eigen = minus if x.startswith("-") else plus
        k = eigen.index(x)
        g = partner[k] if k < len(partner) else ""
        i = next((j for j in range(1, min(len(x), len(g))) if x[j] != g[j]), min(len(x), len(g)))
        aus.append(_fenster(x, i))
    return "\n".join(aus)


def pfad(name, eltern):
    t = [name]
    while t[-1] in eltern and eltern[t[-1]]:
        t.append(eltern[t[-1]])
    return " › ".join(reversed(t))


def block(nr, key, alt_de, neu_de, erkl, eltern, standard=False):
    ctl, prop = key.split(".", 1)
    ende = [x for x in neu_de.strip().split("\n") if x.strip()][-1].strip()[-80:]
    return ["### %s · `%s`" % (nr, key), "", "**Pfad:** `%s` → %s" % (pfad(ctl, eltern) if ctl != "App" else "App", prop), "",
            "```", neu_de, "```", "", "```diff", ("- " + alt_de + " (Standard)\n+ " + neu_de) if standard else diff(alt_de, neu_de), "```", "",
            "**Kurz erklärt:** " + erkl, "", "**Nachprüfen:** endet auf `%s`" % ende, ""]


def app_doc():
    end, vorher, std = {}, {}, set()
    for p in BL["pakete"][10:12]:
        assert p["nr"] in (12, 16)
        for c in p["props"]:
            vorher.setdefault(c["key"], c["vorher"])
            if c.get("standard"):
                std.add(c["key"])
            end[c["key"]] = c["nachher"]
    eltern = dict(rg.App(doc_app89.EXPORT).eltern)
    for n, i in BL["neue_controls"].items():
        eltern[n] = i["eltern"]
    gruppen = [("Laden, Formeln, Speichern", ["App.Formulas", "scrKategorie.OnVisible", "btnKaSpeichern.OnSelect"]),
               ("Knöpfe i.O./n.i.O.", ["btnKaIO.Text", "btnKaNIO.Text", "btnKaIO.Width", "btnKaNIO.Width", "btnKaNIO.X", "btnKaIO.Size", "btnKaNIO.Size"]),
               ("Fenster mit dem eigenen Wort", ["lblKaRueckFrage.Text", "btnKaKritVersehen.Text"]),
               ("„nicht messbar“", ["txtKaZahl.OnChange", "lblKaZahlInfo.Width", "lblKaZahlInfo.Size", "#btnKaNM"]),
               ("Protokoll", ["htmProtokoll.HtmlText"])]
    keys = [k for _, ks in gruppen for k in ks if not k.startswith("#")]
    assert sorted(keys) == sorted(end), set(keys) ^ set(end)
    z = ["# Paket 12+16 – Rundgang-App: eigene Antwortwörter, „nicht messbar“", "",
         "Stand 02.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket12, paket16) und `werkzeuge/doc_paket12_16.py`. "
         "**Voraussetzung: Paket N und Paket 8–10 eingefügt** (`PAKET_N_Nachholen.md`, `PAKET_8_9_10_APP.md`).", "",
         "## Kurzfassung", ""] + KURZ + [
         "- Umfang: 3 Spalten, %d Properties (jede einmal), 1 neuer Knopf. Generator 0 Fehler, Mutation 12/12, Logik 91 Szenarien, unabhängig geprüft (9 Befunde eingearbeitet, `arbeit/2026-11-02_Paket12_16/pruefung_unabhaengig.md`). **Nicht in Studio getestet.**" % len(end), "",
         "## Schritt 1 – SharePoint", "",
         "`RG_Pruefpunkte`: `TextIO` (Eine Textzeile), `TextNIO` (Eine Textzeile), `NichtMessbar` (Ja/Nein, Standard Nein). "
         "Danach in der Rundgang-App: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**.", ""]
    for gi, (titel, ks) in enumerate(gruppen, 2):
        z += ["## Schritt %d – %s" % (gi, titel), ""]
        for i, k in enumerate(ks, 1):
            if k.startswith("#"):
                z += ["### %d.%d · neuer Knopf `%s`" % (gi, i, k[1:]), "",
                      "**Wo hin:** in der Strukturansicht `txtKaZahl` (in `conKaKarte`) markieren → Strg+V (landet in derselben Karte).", "",
                      "```yaml"] + doc_app89.yaml_block(k[1:], doc_app89.neue_bis(BL, 16)) + ["```", "",
                      "**Nachprüfen (E-05):** `btnKaNM.Y` muss die Formel `54 + If(ThisItem.Hinweis <> \"\"; 24; 0)` sein, keine Zahl.", ""]
                continue
            z += block("%d.%d" % (gi, i), k, doc_app89.de(vorher[k]), doc_app89.de(end[k]), ERKL_APP[k], eltern, k in std)
    z += ["## Test (ZZ-Test-Rundgang)", "",
          "| # | Schritt | erwartet |", "|---|---|---|",
          "| T1 | In SharePoint an einer i.O./n.i.O.-Frage `TextIO` = „durchgeführt“, `TextNIO` = „nicht durchgeführt“. Kategorie öffnen | Knöpfe heißen so, breiter |",
          "| T2 | „nicht durchgeführt“ tippen | wie n.i.O.: Kommentar Pflicht, Mangel beim Abschluss |",
          "| T3 | Speichern, Protokoll ansehen | Protokoll zeigt „nicht durchgeführt“ |",
          "| T4 | Zahl-Frage mit `NichtMessbar` = Ja: „nicht messbar“ tippen | Feld leer, Knopf grau gefüllt „✓ nicht messbar“, „Noch offen … (Kommentar)“ |",
          "| T5 | Begründung eintragen, speichern | gespeichert, Protokoll „nicht messbar“ + Begründung, kein Mangel |",
          "| T6 | Kategorie neu öffnen, eine Zahl eintippen | „nicht messbar“ ist aufgehoben, Zahl gilt |",
          "| T7 | Zahl-Frage ohne `NichtMessbar` | kein Knopf, alles wie bisher |",
          "| T8 | Zahl-Frage mit Rückfrage: Wert außerhalb tippen und **ohne** das Feld zu verlassen „nicht messbar“ tippen | kein Fenster, Speichern verlangt nur die Begründung |",
          "| T9 | Rückfrage bei „nicht durchgeführt“ | Fenster sagt „Ihre Antwort: nicht durchgeführt“ |", "",
          "## Bekannt / Frage an den Planer", "",
          "- „nicht messbar“ umgeht Grenzmodus „Sperren“ und „kritisch“ (es gibt keinen Wert). Gewollt? Sonst: „nicht messbar“ bei kritischen Punkten im Builder sperren.",
          "- Wird „nicht messbar“ im Builder später abgeschaltet, bleibt ein schon gespeichertes „nicht messbar“ gültig. Der Knopf bleibt dann sichtbar, damit man es aufheben kann.", "",
          "## Rückweg", "", "Vorher-Fassungen im Anhang einsetzen, `btnKaNM` löschen. Spalten dürfen bleiben.", "",
          "## Anhang – Vorher-Fassungen (Stand nach Paket 8–10)", ""]
    for k in keys:
        z += ["**`%s` vorher**" % k, "", "```", doc_app89.de(vorher[k]) if k not in std else vorher[k] + " (Standard)", "```", ""]
    open(os.path.join(doc_app89.AUS, "PAKET_12_16_APP.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    return len(end)


def builder_doc():
    v, n = BV["de"], BN["de"]
    geaendert = sorted(k for k in n if k in v and v[k] != n[k])
    eltern = BN["eltern"]
    gruppen = [("Kleine Werte und Vorschau", ["lblKInfo.Text", "conPRest.Y", "btnPNio.Y", "btnVsIO.Text", "btnVsNIO.Text", "btnVsIO.Width", "btnVsNIO.Width",
                                              "btnVsNIO.X", "lblVsRegeln.Text"]),
               ("Auswahl wechseln (setzt die neuen Felder zurück)", ["btnGlZeile.OnSelect", "btnGlNeuB.OnSelect", "btnGlNeuK.OnSelect", "btnGlNeuP.OnSelect",
                                                                    "btnPrZeile.OnSelect", "ddKBereich.OnChange", "ddPKategorie.OnChange"]),
               ("Listen und Mehrere Fragen", ["galAkt.Items", "btnMehrAnlegen.OnSelect"]),
               ("Lange Formeln", ["btnEdEntf.OnSelect", "galPr.Items", "tmrArbeit.OnTimerEnd"])]
    keys = [k for _, ks in gruppen for k in ks]
    assert sorted(keys) == geaendert, set(keys) ^ set(geaendert)

    def yaml_von(name):
        for s in builder.SCREENS:
            for c, _ in builder.alle(s):
                if c.name == name:
                    return "\n".join(builder.yaml_control(c, ""))
        raise KeyError(name)

    def yaml_kinder(eltern_name, namen):
        for s in builder.SCREENS:
            for c, _ in builder.alle(s):
                if c.name == eltern_name:
                    return "\n".join(x for k in c.kinder if k.name in namen for x in builder.yaml_control(k, ""))
        raise KeyError(eltern_name)

    z = ["# Paket 12+16 – Builder: eigene Antwortwörter, „nicht messbar“", "",
         "Stand 02.11.2026. Erzeugt mit `werkzeuge/builder.py` und `werkzeuge/doc_paket12_16.py`. **Voraussetzung: Paket 8 und Paket 9 (Builder) eingefügt.**", "",
         "## Kurzfassung", ""] + KURZ + [
         "- Im Prüfpunkt-Editor: bei i.O./n.i.O. zwei Felder „Knopf heißt …“, bei Zahl der Knopf „nicht messbar: erlaubt“. Kopie, Fassungen, Änderungsliste, Vorschau und Prüfung kennen die Felder.",
         "- Dazu: Der Erklärtext bei Kategorien sagt jetzt „beliebige Reihenfolge“ (Paket 10).",
         "- Umfang: 3 Spalten (dieselben wie in der Rundgang-App), 2 neue Blöcke, %d geänderte Properties. Generator 0 Fehler, Mutation 13/13, Logik 27, unabhängig geprüft. "
         "**Nicht in Studio getestet.**" % len(geaendert), "",
         "## Schritt 0 – SharePoint", "", "Die drei Spalten aus `PAKET_12_16_APP.md`, Schritt 1 (nur einmal anlegen). Im Builder: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**.", "",
         "## Schritt 1 – neue Steuerelemente", "",
         "### 1a · Felder für die Knopf-Wörter", "", "**Wo hin:** **`conEdP`** (`%s`) markieren → Strg+V." % pfad("conEdP", eltern), "",
         "```yaml", yaml_von("conPIonio"), "```", "",
         "### 1b · „nicht messbar“ bei Zahlen", "", "**Wo hin:** **`conPZahl`** (`%s`) markieren → Strg+V." % pfad("conPZahl", eltern), "",
         "```yaml", yaml_kinder("conPZahl", ["lblPNM", "btnPNM"]), "```", "",
         "**Nachprüfen:** `conPIonio` liegt in `conEdP`, `lblPNM`/`btnPNM` in `conPZahl`. Kein `_1`.", ""]
    for gi, (titel, ks) in enumerate(gruppen, 2):
        z += ["## Schritt %d – %s" % (gi, titel), ""]
        for i, k in enumerate(ks, 1):
            z += block("%d.%d" % (gi, i), k, v[k], n[k], ERKL_BUILDER.get(k, STD), eltern)
    z += ["## Test", "",
          "1. Prüfpunkt i.O./n.i.O. wählen → „durchgeführt“ / „nicht durchgeführt“ eintragen → Vorschau-Knöpfe heißen so.",
          "2. Zahl-Prüfpunkt → „nicht messbar: nicht erlaubt“ antippen → „✓ erlaubt“, Vorschau nennt es. Schnell zweimal tippen → schaltet nur einmal um.",
          "2b. „durchgeführt“/„nicht durchgeführt“ eintragen → Vorschau-Knöpfe werden breiter, nichts abgeschnitten. Mehr als 18 Zeichen lassen sich nicht eintippen.",
          "3. Anderen Prüfpunkt wählen und zurück → Felder zeigen die richtigen Werte.",
          "4. Aktivieren → Änderungsliste „geändert“. Neue Fassung → Werte noch da.", "",
          "## Rückweg", "", "Vorher-Fassungen im Anhang. `conPIonio`, `lblPNM`, `btnPNM` erst löschen, **nachdem** die Vorher-Fassungen drin sind "
          "(sonst werden die Formeln mit `Reset(txtPTextIO)` rot).", "",
          "## Anhang – Vorher-Fassungen (Stand nach Paket 9)", ""]
    for k in keys:
        z += ["**`%s` vorher**" % k, "", "```", v[k], "```", ""]
    open(os.path.join(builder.AUS_PAKET, "PAKET_12_16_BUILDER.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    return len(geaendert)


if __name__ == "__main__":
    a = app_doc()
    b = builder_doc()
    print("geschrieben: pakete/PAKET_12_16_APP.md (%d Properties), pakete/builder/PAKET_12_16_BUILDER.md (%d Properties)" % (a, b))
