"""Paket 13 (Anleitung im ⓘ-Fenster): Einbau-Dokumente für Rundgang-App und Builder.
Aufruf: python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket13.py
Vorher Rundgang-App = Stand nach Paket 17, Vorher Builder = arbeit/2026-11-02_Paket8/builder_nach_p14_15.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import doc_app89  # noqa: E402
import rg  # noqa: E402
from doc_paket12_16 import block, pfad  # noqa: E402

BL = json.load(open(doc_app89.BLOECKE, encoding="utf-8"))
BV = json.load(open(os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8", "builder_nach_p14_15.json"), encoding="utf-8"))
BN = json.load(open(os.path.join(builder.AUS_ARB, "bloecke.json"), encoding="utf-8"))

KURZ = [
    "- **Anleitungen:** Eine neue Liste `RG_Anleitungen` (Titel, Text beliebig lang, aktiv). Eine Anleitung kann an vielen Prüfpunkten hängen.",
    "- **Prüfer:** An Prüfpunkten mit Anleitung steht ein runder Knopf **ⓘ**. Er öffnet ein großes Fenster mit dem Text (scrollbar) und, falls vorhanden, dem Beispielbild.",
    "- **Builder:** neuer Bildschirm „Anleitungen“ (anlegen, ändern, inaktiv stellen) und im Prüfpunkt das Feld „Anleitung“ neben „Foto“. "
    "Die Foto-Auswahl hat dafür kürzere Texte (gleiche Werte).",
    "- Bewusst nicht gebaut: Foto-Aufnahme im ⓘ-Fenster (Pflicht-Fotos bleiben sichtbar in der Karte – „Prüfer sind nicht verlässlich“).",
]
ERKL_APP = {
    "scrKategorie.OnVisible": "Liest die aktiven Anleitungen frisch. Neues Feld `AnlID` in allen drei Zweigen – nur wenn die Anleitung aktiv ist (inaktive sieht der Prüfer nicht). Das ⓘ-Fenster ist beim Öffnen zu.",
    "lblKaFrage.Width": "Platz für den ⓘ-Knopf.",
}
ERKL_B = {
    "App.OnStart": "Neuer Startwert `varAnID` (gewählte Anleitung).",
    "lblPFoto.Width": "Halbe Breite, daneben „Anleitung“.",
    "ddPFoto.Width": "Halbe Breite.",
    "ddPFoto.Items": "Kürzere Texte (gleiche Werte): „kein Foto“, „Foto freiwillig“, „Foto immer Pflicht“, „Foto bei Mangel“.",
    "ddPFoto.Default": "Wie Items.",
    "lblVsRegeln.Text": "Vorschau nennt die Anleitung.",
    "galAkt.Items": "Änderung der Anleitung zählt als „geändert“.",
    "galPr.Items": "**Bis zum nächsten Schritt (tmrArbeit) ist `colAnlAktiv` rot – erwartet.** Hinweis, wenn die Anleitung fehlt oder inaktiv ist. Dazu (Nachtrag aus der Prüfung von 14+15): Fehler bei negativem „erlaubter Unterschied“.",
    "tmrArbeit.OnTimerEnd": "Kopie/neue Fassung übernehmen die Anleitung. Beim Laden werden die aktiven Anleitungen frisch für die Prüfung gelesen (danach ist galPr nicht mehr rot).",
    "btnGlNeuP.OnSelect": "Neuer Prüfpunkt ohne Anleitung.",
    "btnMehrAnlegen.OnSelect": "Wie btnGlNeuP.",
}


def app_teil():
    p = [q for q in BL["pakete"] if q["nr"] == 13][0]
    alle = doc_app89.neue_bis(BL, 13)
    eltern = dict(rg.App(doc_app89.EXPORT).eltern)
    for n, i in BL["neue_controls"].items():
        eltern[n] = i["eltern"]
    z = ["## Teil A – Rundgang-App", "",
         "### A1 – SharePoint", "",
         "- Neue Liste **`RG_Anleitungen`**: `Title` (vorhanden), `Anleitung` (Mehrere Textzeilen, **nur Text**), `Aktiv` (Ja/Nein, Standard Ja). Berechtigung wie die anderen RG-Listen.",
         "- `RG_Pruefpunkte`: neue Spalte `AnleitungID` (Zahl, Standard 0).",
         "- Rundgang-App: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**, dann **Daten hinzufügen** → SharePoint → IMS+ → `RG_Anleitungen`.", "",
         "### A2 – zwei Properties", ""]
    for i, c in enumerate(p["props"], 1):
        z += block("A2.%d" % i, c["key"], doc_app89.de(c["vorher"]), doc_app89.de(c["nachher"]), ERKL_APP[c["key"]], eltern)
    z += ["### A3 – Knopf ⓘ in der Karte", "", "**Wo hin:** in der Strukturansicht `btnKaBild` (in `conKaKarte`) markieren → Strg+V.", "",
          "```yaml"] + doc_app89.yaml_block("btnKaInfo", alle) + ["```", "", "**Nachprüfen (E-05):** `btnKaInfo.X` ist eine Formel.", "",
          "### A4 – Fenster", "", "**Wo hin:** **`scrKategorie`** markieren → Strg+V (liegt dann über allem).", "",
          "```yaml"] + doc_app89.yaml_block("conKaInfo", alle) + ["```", ""]
    return z, len(p["props"])


def builder_teil():
    v, n = BV["de"], BN["de"]
    geaendert = sorted(k for k in n if k in v and v[k] != n[k])
    eltern = BN["eltern"]
    gruppen = [("Start und Foto/Anleitung", ["App.OnStart", "lblPFoto.Width", "ddPFoto.Width", "ddPFoto.Items", "ddPFoto.Default"]),
               ("Vorschau, neue Prüfpunkte, Liste", ["lblVsRegeln.Text", "btnGlNeuP.OnSelect", "btnMehrAnlegen.OnSelect", "galAkt.Items"]),
               ("Lange Formeln", ["galPr.Items", "tmrArbeit.OnTimerEnd"])]
    keys = [k for _, ks in gruppen for k in ks]
    assert sorted(keys) == geaendert, set(keys) ^ set(geaendert)

    def finde(name):
        for s in builder.SCREENS:
            for c, _ in builder.alle(s):
                if c.name == name:
                    return c, s
        raise KeyError(name)

    def yaml_von(name):
        c, s = finde(name)
        return builder.yaml_screen(c).rstrip("\n") if c is s else "\n".join(builder.yaml_control(c, ""))

    conprest, _ = finde("conPRest")
    z = ["## Teil B – Builder", "",
         "### B0 – Daten", "", "Liste und Spalte aus A1 (nur einmal anlegen). Builder: `RG_Pruefpunkte` aktualisieren, `RG_Anleitungen` hinzufügen.", "",
         "### B1 – Bildschirm „Anleitungen“", "", "**Wo hin:** einen Bildschirm markieren (z. B. `scrKontakte`) → Strg+V.", "",
         "```yaml", yaml_von("scrAnleitungen"), "```", "",
         "### B2 – Knopf in der Übersicht", "", "**Wo hin:** **`scrListe`** markieren → Strg+V.", "", "```yaml", yaml_von("btnLiAnleitungen"), "```", "",
         "### B3 – Feld „Anleitung“ im Prüfpunkt", "", "**Wo hin:** **`conPRest`** (`%s`) markieren → Strg+V." % pfad("conPRest", eltern), "",
         "```yaml", "\n".join(x for k in conprest.kinder if k.name in ("lblPAnl", "ddPAnl") for x in builder.yaml_control(k, "")), "```", "",
         "**Kurzzeitig normal:** `ddPAnl` liegt über der Foto-Auswahl, bis B4 sie schmaler macht.", ""]
    for gi, (titel, ks) in enumerate(gruppen, 4):
        z += ["### B%d – %s" % (gi, titel), ""]
        for i, k in enumerate(ks, 1):
            z += block("B%d.%d" % (gi, i), k, v[k], n[k], ERKL_B[k], eltern)
    return z, keys, len(geaendert)


def main():
    za, na = app_teil()
    zb, keys_b, nb = builder_teil()
    z = ["# Paket 13 – Anleitungen im ⓘ-Fenster (Rundgang-App + Builder)", "",
         "Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket13), `werkzeuge/builder.py` und `werkzeuge/doc_paket13.py`. "
         "**Voraussetzung:** Rundgang-App bis Paket 17 eingefügt, Builder bis Paket 14+15 (**Builder 14+15 vorher**, sonst überschreibt es Teile von Paket 13).", "",
         "## Kurzfassung", ""] + KURZ + [
         "- Umfang: 1 Liste, 1 Spalte. Rundgang-App %d Properties + 2 Blöcke. Builder 1 Bildschirm, 2 Blöcke, %d Properties. "
         "Generatoren 0 Fehler. Unabhängig geprüft (Befunde eingearbeitet, `arbeit/2026-11-03_Paket13_17/pruefung_unabhaengig.md`). **Nicht in Studio getestet.**" % (na, nb), ""] + za + zb + [
         "## Test", "",
         "1. Builder → „Anleitungen“ → „+ Anleitung“: Titel „Kompressor ablesen“, Text mit mehreren Absätzen.",
         "2. Prüfpunkt → „Anleitung“ wählen → Vorschau „ⓘ Anleitung …“. Aktivieren (oder in der Vorlage/im Entwurf).",
         "3. Rundgang-App: Kategorie öffnen → ⓘ neben der Frage → Fenster mit Text (bei langem Text scrollen), Beispielbild darunter, „Schließen“.",
         "4. Anleitung im Builder inaktiv stellen → Rundgang im Editor neu öffnen → Prüfung zeigt den Hinweis, das Feld zeigt „… (inaktiv oder gelöscht)“.",
         "5. Rundgang-App: Kategorie neu öffnen → bei dieser Frage ist kein ⓘ mehr da.",
         "6. Zwei Anleitungen gleichen Titels → Auswahl zeigt „Titel (#ID)“.",
         "7. Nur-Ansicht (abgeschlossener Lauf): ⓘ öffnet die Anleitung, wenn sie aktiv ist.",
         "8. Neue Fassung → die Anleitung hängt weiter am Prüfpunkt. Foto-Auswahl: gespeicherte Werte unverändert („Foto bei Mangel“ = „Bei Mangel Pflicht“).", "",
         "## Rückweg", "", "Vorher-Fassungen im Anhang einsetzen, dann die neuen Steuerelemente und den Bildschirm löschen. Liste/Spalte dürfen bleiben.", "",
         "## Anhang – Vorher-Fassungen", ""]
    p = [q for q in BL["pakete"] if q["nr"] == 13][0]
    for c in p["props"]:
        z += ["**Rundgang-App `%s` vorher**" % c["key"], "", "```", doc_app89.de(c["vorher"]), "```", ""]
    for k in keys_b:
        z += ["**Builder `%s` vorher**" % k, "", "```", BV["de"][k], "```", ""]
    open(os.path.join(doc_app89.AUS, "PAKET_13_ANLEITUNGEN.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_13_ANLEITUNGEN.md (App %d, Builder %d Properties)" % (na, nb))


if __name__ == "__main__":
    main()
