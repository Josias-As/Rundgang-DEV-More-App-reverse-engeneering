"""Paket 14+15 (Abweichung zum letzten Rundgang, zwei Werte vergleichen): Einbau-Dokumente für Rundgang-App und Builder.
Aufruf: python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket14_15.py
Vorher Rundgang-App = Stand nach Paket 12+16, Vorher Builder = arbeit/2026-11-02_Paket8/builder_nach_p12_16.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import doc_app89  # noqa: E402
import rg  # noqa: E402
from doc_paket12_16 import block, pfad  # noqa: E402

BL = json.load(open(doc_app89.BLOECKE, encoding="utf-8"))
BV = json.load(open(os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8", "builder_nach_p12_16.json"), encoding="utf-8"))
BN = json.load(open(os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8", "builder_nach_p14_15.json"), encoding="utf-8"))  # eingefroren nach 14+15

KURZ = [
    "- **Paket 14 – Abweichung zum letzten Rundgang:** Bei einer Zahl lässt sich im Builder einstellen, wie stark sie vom letzten abgeschlossenen Rundgang abweichen darf "
    "(absolut oder in %), und/oder „Zählerstand: darf nicht kleiner werden“. Die Karte zeigt „zuletzt 7,6 (26.10.)“. Weicht der Wert stärker ab, wird die Zeile orange "
    "und eine **Begründung ist Pflicht**. Kein Mangel. Der erste Rundgang hat keinen Vergleich. Testläufe vergleichen nur mit Testläufen.",
    "- **Paket 15 – zwei Werte vergleichen:** Eine Zahl kann mit einer anderen Zahl derselben Kategorie verglichen werden (z. B. zwei gleiche Geräte) mit erlaubtem Unterschied "
    "(0 = gleich). Weichen sie stärker ab, ist ebenfalls eine Begründung Pflicht.",
    "- Protokoll: „(starke Abweichung zum letzten Mal, zuletzt 7,6, begründet)“ bzw. „(weicht von „…“ ab (7,2), begründet)“.",
    "- Nach einer neuen Fassung findet die App den alten Wert über `QuelleID` (eine Fassung zurück). Lagen zwei Aktivierungen zwischen zwei Rundgängen, fehlt der Vergleich einmal.",
]
ERKL_APP = {
    "App.Formulas": "Zwei neue Funktionen: `fnAbweichung` (zum letzten Mal, absolut/%, Zähler) und `fnVergleich` (zwei Werte, Toleranz).",
    "scrKategorie.OnVisible": "Lädt einmal je Rundgang die Zahlen des letzten abgeschlossenen Laufs **vor diesem Tag** (frisch gelesen, nach Tag sortiert, also auch bei Nachhol-Läufen richtig; nur wenn ein Prüfpunkt der Kategorie es braucht). "
                              "Neue Felder in allen drei Zweigen. Danach wird für alle Zahlen bestimmt, ob eine Begründung nötig ist.",
    "btnKaSpeichern.OnSelect": "Speichert „zuletzt“ und den Abweichungs-Text mit (Protokoll, Nur-Ansicht).",
    "txtKaZahl.OnChange": "Nach jeder Eingabe werden Abweichung und Vergleich neu bestimmt (auch beim Partner-Punkt).",
    "btnKaNM.OnSelect": "Wie txtKaZahl: „nicht messbar“ hebt eine Abweichung auf.",
    "btnKaRueckNein.OnSelect": "„Nein, korrigieren“ leert den Wert – danach Abweichung/Vergleich neu bestimmen (auch beim Partner).",
    "btnKaKritVersehen.OnSelect": "Wie btnKaRueckNein.",
    "lblKaZahlInfo.Height": "Etwas höher, wenn zusätzlicher Text da ist (sonst wird „bitte begründen“ abgeschnitten).",
    "lblKaZahlInfo.Text": "Zeigt „zuletzt …“ und den Abweichungs-Text mit „bitte begründen“.",
    "lblKaZahlInfo.Color": "Orange bei Abweichung.",
    "lblKaZahlInfo.Size": "Kleiner, wenn zusätzlicher Text da ist.",
    "htmProtokoll.HtmlText": "Protokoll nennt die Abweichung.",
}
ERKL_BUILDER = {
    "App.OnStart": "Neuer Startwert `varZaOffen` (Fenster „Verlauf und Vergleich“).",
    "scrEditor.OnVisible": "Schließt das neue Fenster beim Öffnen des Editors.",
    "lblPGrenz.Width": "Macht Platz für den neuen Knopf „Verlauf/Vergleich“.",
    "lblVsRegeln.Text": "Vorschau nennt Abweichung, Zähler und Vergleich.",
    "galAkt.Items": "Änderungen an den neuen Feldern zählen als „geändert“ (Vergleichspunkt über QuelleID).",
    "galPr.Items": "Fehler, wenn der Vergleich auf keine Zahl derselben Kategorie zeigt oder die Abweichung negativ ist. Hinweis bei anderem Typ.",
    "tmrArbeit.OnTimerEnd": "Kopie/neue Fassung übernehmen die fünf Felder. Der Vergleichs-Verweis wird wie die Bedingung auf die neue Frage umgeschrieben.",
    "btnEdEntf.OnSelect": "Wird ein Prüfpunkt entfernt, verlieren Prüfpunkte, die mit ihm verglichen werden, den Verweis.",
    "ddPKategorie.OnChange": "Beim Verschieben in eine andere Kategorie entfällt der Vergleich (er gilt nur innerhalb einer Kategorie).",
    "btnGlNeuP.OnSelect": "Neuer Prüfpunkt mit leeren Vergleichsfeldern.",
    "btnMehrAnlegen.OnSelect": "Wie btnGlNeuP.",
}


def app_doc():
    p = [q for q in BL["pakete"] if q["nr"] == 14][0]
    assert p["nr"] == 14
    end = {c["key"]: c["nachher"] for c in p["props"]}
    vorher = {}
    for c in p["props"]:
        vorher.setdefault(c["key"], c["vorher"])
    eltern = dict(rg.App(doc_app89.EXPORT).eltern)
    for n, i in BL["neue_controls"].items():
        eltern[n] = i["eltern"]
    gruppen = [("Formeln und Laden", ["App.Formulas", "scrKategorie.OnVisible"]),
               ("Eingabe und Speichern", ["txtKaZahl.OnChange", "btnKaNM.OnSelect", "btnKaRueckNein.OnSelect", "btnKaKritVersehen.OnSelect", "btnKaSpeichern.OnSelect"]),
               ("Anzeige in der Karte", ["lblKaZahlInfo.Text", "lblKaZahlInfo.Color", "lblKaZahlInfo.Size", "lblKaZahlInfo.Height"]),
               ("Protokoll", ["htmProtokoll.HtmlText"])]
    keys = [k for _, ks in gruppen for k in ks]
    assert sorted(keys) == sorted(end), set(keys) ^ set(end)
    z = ["# Paket 14+15 – Rundgang-App: Abweichung zum letzten Rundgang, zwei Werte vergleichen", "",
         "Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket14) und `werkzeuge/doc_paket14_15.py`. "
         "**Voraussetzung: Paket N, 8–10 und 12+16 eingefügt.** Danach folgen Paket 17 und 13 (die bauen auf diesem Stand auf).", "", "## Kurzfassung", ""] + KURZ + [
         "- Umfang: 5 Spalten, %d Properties (jede einmal), kein neues Steuerelement. Generator 0 Fehler, Mutation, Logik 103 Szenarien. "
         "Unabhängig geprüft (Befunde eingearbeitet, `arbeit/2026-11-03_Paket14_15/pruefung_unabhaengig.md`). **Nicht in Studio getestet.**" % len(end), "",
         "## Schritt 1 – SharePoint", "",
         "`RG_Pruefpunkte`: `AbwMax` (Zahl, leer), `AbwProzent` (Ja/Nein, Nein), `NurSteigend` (Ja/Nein, Nein), `VergleichPunkt` (Zahl, 0), `VergleichTol` (Zahl, 0). "
         "Danach in der Rundgang-App: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**. (`QuelleID` gibt es schon, vom Builder.)", ""]
    for gi, (titel, ks) in enumerate(gruppen, 2):
        z += ["## Schritt %d – %s" % (gi, titel), ""]
        for i, k in enumerate(ks, 1):
            z += block("%d.%d" % (gi, i), k, doc_app89.de(vorher[k]), doc_app89.de(end[k]), ERKL_APP[k], eltern)
    z += ["## Test (ZZ-Test-Rundgang, Zeitachse)", "",
          "| # | Schritt | erwartet |", "|---|---|---|",
          "| T0 | **Vorher alles in einer Fassung einstellen** (sonst liegen zwei Fassungen zwischen den Läufen und der Vorwert fehlt): Zahl A `AbwMax` = 0,5; Zähler Z `NurSteigend` = Ja; "
          "Zahl B `VergleichPunkt` = ID von A, `VergleichTol` = 0,2 | – |",
          "| T1 | **Tag N** (oder als Nachholtag): Rundgang starten, A = 7,6, Z = 5000, B = 7,6, alles speichern, **abschließen** | erster Lauf: kein „zuletzt“ |",
          "| T2 | **Tag N+1:** Rundgang starten, Kategorie öffnen | Karte zeigt „zuletzt 7,6 (TT.MM.)“ |",
          "| T3 | 7,9 eingeben | nichts Besonderes |",
          "| T4 | 8,4 eingeben | orange „starke Abweichung zum letzten Mal, bitte begründen“, Kommentar Pflicht. Begründen, speichern, Protokoll nennt es |",
          "| T5 | Z = 4999 | „kleiner als beim letzten Mal“, Begründung Pflicht |",
          "| T6 | A = 7,6, B = 8,0 | B: „weicht von „A“ ab (7,6)“. A auf 7,9 ändern → Hinweis bei B verschwindet |",
          "| T6b | Bei A (mit Rückfrage) n.i.O.-Wert, dann „Nein, korrigieren“ | Hinweis bei B verschwindet (A leer) |",
          "| T7 | B „nicht messbar“ | Vergleich entfällt, nur Begründung für „nicht messbar“ |", "",
          "## Rückweg", "", "Vorher-Fassungen im Anhang einsetzen. Spalten dürfen bleiben.", "",
          "## Anhang – Vorher-Fassungen (Stand nach Paket 12+16)", ""]
    for k in keys:
        z += ["**`%s` vorher**" % k, "", "```", doc_app89.de(vorher[k]), "```", ""]
    open(os.path.join(doc_app89.AUS, "PAKET_14_15_APP.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    return len(end)


def builder_doc():
    v, n = BV["de"], BN["de"]
    geaendert = sorted(k for k in n if k in v and v[k] != n[k])
    eltern = BN["eltern"]
    gruppen = [("Start und kleine Werte", ["App.OnStart", "scrEditor.OnVisible", "lblPGrenz.Width", "lblVsRegeln.Text"]),
               ("Neue Prüfpunkte und Verschieben", ["btnGlNeuP.OnSelect", "btnMehrAnlegen.OnSelect", "ddPKategorie.OnChange"]),
               ("Listen", ["galAkt.Items"]),
               ("Lange Formeln", ["btnEdEntf.OnSelect", "galPr.Items", "tmrArbeit.OnTimerEnd"])]
    keys = [k for _, ks in gruppen for k in ks]
    assert sorted(keys) == geaendert, set(keys) ^ set(geaendert)

    def yaml_von(name):
        for s in builder.SCREENS:
            for c, _ in builder.alle(s):
                if c.name == name:
                    return "\n".join(builder.yaml_control(c, ""))
        raise KeyError(name)

    z = ["# Paket 14+15 – Builder: Verlauf und Vergleich bei Zahlen", "",
         "Stand 03.11.2026. Erzeugt mit `werkzeuge/builder.py` und `werkzeuge/doc_paket14_15.py`. **Voraussetzung: Builder-Pakete 8, 9, 12+16 eingefügt. "
         "Unbedingt vor Paket 13 einfügen** (Paket 13 ersetzt einige dieser Formeln noch einmal mit seinen Ergänzungen).", "",
         "## Kurzfassung", ""] + KURZ + [
         "- Im Prüfpunkt-Editor bei Zahlen ein Knopf **„Verlauf/Vergleich ›“** neben „Wert außerhalb der Grenzen ergibt“. Er öffnet ein Fenster: höchste Abweichung (absolut/%), "
         "„Zählerstand: darf nicht kleiner werden“, Vergleichs-Prüfpunkt (nur Zahlen derselben Kategorie) und erlaubter Unterschied.",
         "- Kopie und neue Fassung schreiben den Vergleichs-Verweis auf die neue Frage um (wie bei Bedingungen). Entfernen/Verschieben löst ihn.",
         "- Umfang: 5 Spalten (dieselben wie in der Rundgang-App), 2 neue Blöcke, %d geänderte Properties. Generator 0 Fehler, Mutation 13/13. "
         "Unabhängig geprüft. **Nicht in Studio getestet.**" % len(geaendert), "",
         "## Schritt 0 – SharePoint", "", "Die fünf Spalten aus `PAKET_14_15_APP.md`, Schritt 1 (nur einmal anlegen). Im Builder: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**.", "",
         "## Schritt 1 – neue Steuerelemente", "",
         "### 1a · Knopf „Verlauf/Vergleich“", "", "**Wo hin:** **`conPZahl`** (`%s`) markieren → Strg+V." % pfad("conPZahl", eltern), "",
         "```yaml", yaml_von("btnPZahlMehr"), "```", "",
         "**Rot bis 1b:** `txtZaAbwMax`, `txtZaTol`, `ddZaVgl`, `varZaOffen` (bis Schritt 2).", "",
         "### 1b · Fenster „Verlauf und Vergleich“", "", "**Wo hin:** **`scrEditor`** markieren → Strg+V (liegt dann über allem; `conEdLaden` danach wieder ganz nach oben schieben: "
         "`conEdLaden` markieren → ⋯ → Neu anordnen → Ganz nach vorne).", "",
         "```yaml", yaml_von("conZa"), "```", ""]
    for gi, (titel, ks) in enumerate(gruppen, 2):
        z += ["## Schritt %d – %s" % (gi, titel), ""]
        for i, k in enumerate(ks, 1):
            z += block("%d.%d" % (gi, i), k, v[k], n[k], ERKL_BUILDER[k], eltern)
    z += ["## Test", "",
          "1. Zahl-Prüfpunkt → „Verlauf/Vergleich ›“ → höchstens 0,5, absolut → Vorschau „höchstens 0,5 Abweichung …“, Knopf „Verlauf/Vergleich: an“.",
          "2. Zweiten Zahl-Prüfpunkt derselben Kategorie als Vergleich wählen, Unterschied 0,2 → Vorschau nennt ihn.",
          "3. Neue Fassung anlegen → im Entwurf zeigt der Vergleich auf die **neue** Frage (Vorschau-Titel gleich, Prüfung ohne Fehler).",
          "4. Den Vergleichs-Partner entfernen → Vergleich ist weg, keine Fehlermeldung.",
          "5. Bekannt: Nach einem Typwechsel weg von „Zahl“ ist das Fenster nicht mehr erreichbar; die Prüfung meldet den Rest. Typ kurz zurück auf Zahl, Vergleich entfernen.", "",
          "## Rückweg", "", "Vorher-Fassungen im Anhang einsetzen, dann `btnPZahlMehr` und `conZa` löschen.", "",
          "## Anhang – Vorher-Fassungen (Stand nach Paket 12+16)", ""]
    for k in keys:
        z += ["**`%s` vorher**" % k, "", "```", v[k], "```", ""]
    open(os.path.join(builder.AUS_PAKET, "PAKET_14_15_BUILDER.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    return len(geaendert)


if __name__ == "__main__":
    a = app_doc()
    b = builder_doc()
    print("geschrieben: pakete/PAKET_14_15_APP.md (%d Properties), pakete/builder/PAKET_14_15_BUILDER.md (%d Properties)" % (a, b))
