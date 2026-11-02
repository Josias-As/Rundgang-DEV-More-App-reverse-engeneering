"""Rundgang-App ab dem Export 02.11.2026 15:41: Nachhol-Paket N (Abgleich Export ↔ Soll nach Paket 1–7) und Paket 8+9 (App-Teil).
Aufruf: python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/doc_app89.py
Ergebnis: pakete/PAKET_N_Nachholen.md, pakete/PAKET_8_9_10_APP.md, arbeit/2026-11-02_App89/abgleich.txt"""
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baukasten  # noqa: E402
import rg  # noqa: E402

EXPORT = "2026-11-02_1541"
AUS = os.path.join(rg.REPO, "pakete")
ARB = os.path.join(rg.REPO, "arbeit", "2026-11-02_App89")
BLOECKE = os.path.join(rg.REPO, "arbeit", "2026-10-27_Baukasten", "bloecke.json")


def norm(f):
    return re.sub(r"\s+", " ", rg.ohne_kommentare(f or "")).strip()


def de(f):
    return rg.to_de(rg.ohne_kommentare(f))


def diff(alt, neu):
    z = [x for x in difflib.unified_diff(de(alt).split("\n"), de(neu).split("\n"), lineterm="", n=0) if not x.startswith(("---", "+++", "@@"))]
    return "\n".join(x if len(x) < 240 else x[:237] + " …" for x in z) or "(nur Zeilenumbrüche)"


def ende(f):
    z = [x.strip() for x in de(f).split("\n") if x.strip()]
    return z[-1][-90:] if z else ""


def yaml_wert(v):
    v = "=" + v
    if "\n" in v or ": " in v or " #" in v or "{" in v:
        return "|-\n" + "\n".join("  " + z for z in v.split("\n"))
    return v


def yaml_block(name, alle, tiefe=0):
    info = alle[name]
    e = "    " * tiefe
    z = [e + "- " + name + ":", e + "    Control: " + info["typ"]]
    if info["typ"].startswith("GroupContainer"):
        z.append(e + "    Variant: ManualLayout")
    if info["typ"].startswith("Gallery"):
        z.append(e + "    Variant: Vertical")
    z.append(e + "    Properties:")
    for k in sorted(info["props"]):
        w = yaml_wert(info["props"][k])
        if w.startswith("|-"):
            zeilen = w.split("\n")
            z.append(e + "      " + k + ": " + zeilen[0])
            z += [e + "      " + x for x in zeilen[1:]]
        else:
            z.append(e + "      " + k + ": " + w)
    kinder = [n for n, i in alle.items() if i["eltern"] == name]
    if kinder:
        z.append(e + "    Children:")
        for k in kinder:
            z += yaml_block(k, alle, tiefe + 1)
    return z


def pfad(name, eltern):
    t = [name]
    while t[-1] in eltern and eltern[t[-1]]:
        t.append(eltern[t[-1]])
    return " › ".join(reversed(t))


def prop_abschnitt(nr, key, alt, neu, erkl, eltern, standard=False):
    ctl, prop = key.split(".", 1)
    z = ["### %s · `%s`" % (nr, key), "", "**Pfad:** `%s` → %s" % (pfad(ctl, eltern) if ctl != "App" else "App", prop), "",
         "```", de(neu), "```", ""]
    z += ["**Das ändert sich:**", "", "```diff", ("- (Standardwert)\n+ " + de(neu)[:200]) if standard else diff(alt, neu), "```", ""]
    z += ["**Kurz erklärt:** " + erkl, "", "**Nachprüfen:** Ende der Formel: `%s`" % ende(neu), ""]
    return z


# ---------------------------------------------------------------- Abgleich Export ↔ Soll (Paket 1–7)

def soll_nach_7():
    app0 = rg.App("2026-10-27_0909")
    st = baukasten.Stand(app0)
    for f in baukasten.PAKETE[:7]:
        f(st)
    return st


ERKL_N = {
    "lblKaHinweis.Text": "**Reparatur:** Hier stand der Text von `lblKaFotoHinweis` (beim Einfügen von Paket 1 ins falsche Steuerelement geraten). Die Karte zeigt wieder den Hinweis des Prüfpunkts.",
    "lblKaAbstand.Text": "**Reparatur:** Hier stand der Text von `lblKaStand` (beim Einfügen von Paket 4 ins falsche Steuerelement geraten). `lblKaAbstand` ist nur ein Abstandhalter, Text wie im Original.",
    "lblKaFotoHinweis.Text": "Fehlte (Paket 1 Schritt 1.9 + Paket 7): Hinweis im Foto-Fenster je nach Foto-Regel.",
    "lblKaStand.Text": "Fehlte (Paket 4 Schritt 4.5): Fortschrittszeile zählt nur sichtbare Fragen.",
    "txtKaZahl.BorderColor": "Fehlte (Paket 3 Schritt 3.5): Rahmen orange bei Warnen, rot bei Sperren/Mangel.",
    "btnKaFoto.Text": "Fehlte (Paket 7): Stern bei „Foto Pflicht bei Mangel“.",
    "btnKaFoto.Visible": "Fehlte (Paket 7): Foto-Knopf bei „Bei Mangel Pflicht“ erst nach n.i.O.",
    "App.Formulas": "Fehlte: Paket 5 (Typen MEHRFACH/DATUM/DATUMZEIT in `fnFehltGrund`, neue `fnDatumText`) und Paket 7 (`fnFotoModus`, Foto bei Mangel).",
}


def nachhol(export, soll, d):
    neu_p5 = ["dpKaDatum", "ddKaStunde", "ddKaMinute", "btnKaDatumLeeren", "cboKaMehrfach"]
    keys = sorted(k for k in soll.props if k.split(".")[0] not in neu_p5 and k in export.props and norm(soll.props[k]) != norm(export.props[k]))
    nur_export = [k for k in export.props if k not in soll.props]
    assert nur_export == ["lblKaZahlInfo.BorderColor"], nur_export
    fehlen = [k for k in soll.props if k not in export.props and k.split(".")[0] in export.typ and k.split(".")[0] not in neu_p5]
    reihen = ["lblKaHinweis.Text", "lblKaAbstand.Text", "lblKaFotoHinweis.Text", "lblKaStand.Text", "txtKaZahl.BorderColor", "btnKaFoto.Text",
              "btnKaFoto.Visible", "App.Formulas"]
    assert sorted(reihen) == keys, keys
    eltern = dict(export.eltern)
    p5 = open(os.path.join(AUS, "PAKET_5_Typen.md"), encoding="utf-8").read()
    teil = p5[p5.index("### Schritt 5.4"):p5.index("### Schritt 5.6")]
    teil = teil.replace("### Schritt 5.4", "### Schritt N.5a").replace("### Schritt 5.5", "### Schritt N.5b")
    z = ["# Paket N – Nachholen in der Rundgang-App (Stand 02.11.2026)", "",
         "Erzeugt mit `werkzeuge/doc_app89.py`: Abgleich des Exports **02.11.2026 15:41** gegen den Soll-Stand nach Paket 1–7 "
         "(Export 27.10. 09:09 + Pakete 1–7 aus `baukasten.py`).", "",
         "## Kurzfassung", "",
         "- Pakete 1, 2, 4 und 6 sind fast vollständig drin, Paket 3 bis auf einen Rahmen.",
         "- **Drei Formeln sind im falschen Steuerelement gelandet:** `lblKaHinweis.Text` enthält den Foto-Hinweis, `lblKaAbstand.Text` die Fortschrittszeile, "
         "`lblKaZahlInfo.BorderColor` den Rahmen des Zahlenfelds. Dafür fehlen sie in `lblKaFotoHinweis`, `lblKaStand` und `txtKaZahl`.",
         "- **Paket 5 (Mehrfach, Datum, Datum + Uhrzeit) fehlt ganz:** die fünf Steuerelemente und die Änderung an `App.Formulas`.",
         "- **Paket 7 (Foto „Bei Mangel Pflicht“) fehlt.**",
         "- Alles andere stimmt zeichengleich mit dem Soll überein (%d Properties geprüft, %d fehlen nur, weil Studio Standardwerte weglässt: %s)." % (
             len(soll.props), len(fehlen), ", ".join(fehlen)),
         "- Wichtig: Der Builder bietet die Typen Mehrfach/Datum und „Foto Pflicht bei Mangel“ schon an. Ohne dieses Paket versteht die Rundgang-App sie nicht.",
         "- Umfang: 9 Properties, 5 Steuerelemente (4 per YAML, 1 per Menü), 2 Auswahlwerte in SharePoint. Danach folgt Paket 8–10.", "",
         "## Schritt N.1 – SharePoint (zuerst)", "",
         "- `RG_Pruefpunkte` → Spalte **Eingabetyp** → Auswahlmöglichkeiten **ergänzen**: **MEHRFACH**, **DATUM**, **DATUMZEIT** (nichts umbenennen).",
         "- `RG_Pruefpunkte` → Spalte **Foto** → Auswahl **ergänzen**: **Bei Mangel Pflicht** (genau so).",
         "- Danach in der Rundgang-App: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**.", "",
         "## Schritt N.2 – zwei Formeln zurück ins richtige Steuerelement", ""]
    for i, k in enumerate(reihen[:2], 1):
        z += prop_abschnitt("N.2.%d" % i, k, export.props[k], soll.props[k], ERKL_N[k], eltern)
    z += ["### N.2.3 · `lblKaZahlInfo.BorderColor`", "", "**Pfad:** `%s` → BorderColor" % pfad("lblKaZahlInfo", eltern), "",
          "```", "RGBA(0; 0; 0; 0)", "```", "",
          "**Das ändert sich:** Hier stand die Formel für `txtKaZahl.BorderColor` (Paket 3, Schritt 3.5). Vorher war es der Standardwert. "
          "Sichtbar war es nicht, weil der Rahmen 0 ist. `RGBA(0; 0; 0; 0)` ist durchsichtig.", "",
          "**Kurz erklärt:** **Reparatur.** Die richtige Formel kommt in Schritt N.3 nach `txtKaZahl.BorderColor`.", ""]
    z += ["## Schritt N.3 – fehlende Formeln", ""]
    for i, k in enumerate(reihen[2:7], 1):
        z += prop_abschnitt("N.3.%d" % i, k, export.props[k], soll.props[k], ERKL_N[k], eltern)
    z += ["## Schritt N.4 – App.Formulas", "",
          "Rot ist danach nichts zu erwarten (die neuen Teile werden nur von Paket 5/7 benutzt).", ""]
    z += prop_abschnitt("N.4", "App.Formulas", export.props["App.Formulas"], soll.props["App.Formulas"], ERKL_N["App.Formulas"], eltern)
    z += ["## Schritt N.5 – Paket 5 nachholen (Steuerelemente)", "",
          "Unverändert aus `pakete/PAKET_5_Typen.md` (Schritt 5.4 und 5.5):", "", teil]
    z += ["## Schritt N.6 – App-Prüfung", "", "App-Prüfung → Formeln = **0**. Speichern. Dann Paket 8–10 (`pakete/PAKET_8_9_10_APP.md`).", "",
          "## Test (wenn du testest)", "", "Paket 5: Tests T5.x in `pakete/PAKET_5_Typen.md`. Paket 7: T7.1–T7.7 in `pakete/PAKET_7_FotoBeiMangel.md`. "
          "Reparatur: eine Karte mit Hinweis zeigt wieder den Hinweis (nicht den Foto-Text).", "",
          "## Anhang – Vorher-Fassungen (aus dem Export)", ""]
    for k in reihen:
        z += ["**`%s` vorher**" % k, "", "```", de(export.props[k]), "```", ""]
    return "\n".join(z), reihen


# ---------------------------------------------------------------- Paket 8+9 (Endfassungen, je Property einmal)

ERKL_89 = {
    "App.Formulas": "`fnFehltGrund`/`fnFehlt` bekommen ein 13. Argument: kritischer Mangel noch nicht bestätigt → „fehlt“ (Grund „Kritisch“).",
    "scrKategorie.OnVisible": "Lädt die Ansprechpartner, setzt die beiden Fenster zurück, neue Felder in allen drei Zweigen (Abschnitt, Kopf-Kennzeichen, kritisch, Rückfrage, Bestätigung). "
                              "Danach wird je Abschnitt die erste Frage als Überschrift-Träger markiert (bevorzugt eine ohne Bedingung).",
    "btnKaSpeichern.OnSelect": "Speichert Abschnitt und Bestätigung im JSON. Gesperrt, solange ein Fenster offen ist. Öffnet bei fehlender Bestätigung das rote Fenster. "
                               "**Paket 10:** Der Zweig „Bitte zuerst die vorherigen Kategorien abschließen“ ist weg.",
    "lblRuSymbol.Text": "Paket 10: Statt 🔒 steht bei offenen Kategorien ○.",
    "lblRuSymbol.Color": "Paket 10: offen = grau statt „gesperrt“-grau.",
    "lblRuKatZustand.Text": "Paket 10: „Offen“ statt „Gesperrt – erst die vorherige Kategorie abschließen“.",
    "btnRuOeffnen.Text": "Paket 10: Knopf heißt bei offenen Kategorien „Öffnen“.",
    "conKaKarte.Y": "Platz für die Abschnitt-Überschrift über der Karte.",
    "lblKaFehlend.Text": "„Noch offen“ nennt den Abschnitt vor der Frage (bei gleichen Fragen in mehreren Abschnitten wichtig) und „(kritisch: Bescheid bestätigen)“.",
    "lblKaFehlendAnzahl.Text": "Zählt einen unbestätigten kritischen Mangel als offen.",
    "conKaKarte.BorderColor": "Rahmen „fehlt“ auch bei unbestätigtem kritischem Mangel.",
    "conKaKarte.BorderThickness": "Wie BorderColor.",
    "htmProtokoll.HtmlText": "Protokoll: Abschnitt-Überschriften, Bereichsname nur wenn nicht ausgeblendet, Zeile „KRITISCH – Bescheid gegeben, bestätigt von … um …“.",
    "btnRuAbschluss.OnSelect": "Mängel: Frage mit Abschnitt („Kompressor 1 › Betriebsdruck“), Kommentar beginnt bei kritisch mit „KRITISCH – Bescheid gegeben hh:mm.“",
    "btnRgAktion.OnSelect": "Beim Start: ausgeblendete Bereiche bekommen einen leeren Namen.",
    "galRuKategorien.Items": "Bereichs-Überschrift nur, wenn der Bereich einen Namen hat. **Paket 10:** Zustand „offen“ statt „gesperrt“ – alle Kategorien sind antippbar.",
    "lblKaUnter.Text": "Kopfzeile ohne Bereichsnamen, wenn er ausgeblendet ist.",
    "btnKaNIO.OnSelect": "Bei neuem n.i.O.: erst Rückfrage (wenn eingestellt), sonst gleich die kritische Meldung (wenn eingestellt). Zurücknehmen löscht die Bestätigung.",
    "txtKaZahl.OnChange": "Wie bei n.i.O.: Zahl außerhalb (Mangel) löst Rückfrage bzw. kritische Meldung aus. Eine schon gegebene Bestätigung bleibt, solange es n.i.O. bleibt.",
}

GRUPPEN_89 = [
    ("SharePoint und Datenquelle", None),
    ("Laden und Formeln", ["scrKategorie.OnVisible", "App.Formulas"]),
    ("Auslöser und „Noch offen“", ["btnKaNIO.OnSelect", "txtKaZahl.OnChange", "lblKaFehlendAnzahl.Text", "lblKaFehlend.Text",
                                   "conKaKarte.BorderColor", "conKaKarte.BorderThickness"]),
    ("Speichern", ["btnKaSpeichern.OnSelect"]),
    ("Abschnitt-Überschrift in der Karte", ["conKaKarte.Y", "#lblKaAbschnitt"]),
    ("Bereich ausblenden", ["btnRgAktion.OnSelect", "galRuKategorien.Items", "lblKaUnter.Text"]),
    ("Protokoll und Mängel", ["htmProtokoll.HtmlText", "btnRuAbschluss.OnSelect"]),
    ("Fenster „Ist das wirklich so?“", ["#conKaRueck"]),
    ("Fenster „Kritischer Mangel“", ["#conKaKrit"]),
    ("Kategorien in beliebiger Reihenfolge (Paket 10)", ["lblRuSymbol.Text", "lblRuSymbol.Color", "lblRuKatZustand.Text", "btnRuOeffnen.Text"]),
]


def paket89(d, soll):
    end, vorher = {}, {}
    for p in d["pakete"][7:10]:
        for c in p["props"]:
            vorher.setdefault(c["key"], c["vorher"])
            end[c["key"]] = c["nachher"]
    alle_keys = [k for _, ks in GRUPPEN_89 if ks for k in ks if not k.startswith("#")]
    assert sorted(alle_keys) == sorted(end), set(alle_keys) ^ set(end)
    for k in end:
        assert norm(vorher[k]) == norm(soll.props[k]), k
    eltern = {k: v for k, v in rg.App(EXPORT).eltern.items()}
    for n, i in d["neue_controls"].items():
        eltern[n] = i["eltern"]
    neu = d["neue_controls"]
    z = ["# Paket 8–10 – Rundgang-App: Abschnitte, Bereich ausblenden, Rückfrage, kritischer Mangel, Kategorien ohne Reihenfolge-Sperre", "",
         "Stand 02.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (Paket 8 und 9 als Zustandskette mit exakten Ankern) und `werkzeuge/doc_app89.py`. "
         "Voraussetzung: **Paket N** (`pakete/PAKET_N_Nachholen.md`) ist eingefügt. Dann ist dein Stand zeichengleich mit dem Stand, auf dem dieses Paket aufbaut (maschinell geprüft).", "",
         "## Kurzfassung", "",
         "- **Abschnitte:** Über der ersten Frage eines Abschnitts steht eine Überschrift (z. B. „Kompressor 1“). Protokoll und Mängel nennen den Abschnitt.",
         "- **Bereich ausblenden:** Im Builder ausgeblendete Bereiche erscheinen nicht mehr als Überschrift (gilt für Rundgänge, die danach gestartet werden).",
         "- **Rückfrage:** Bei n.i.O. (oder Zahl außerhalb, Modus Mangel) fragt die App „Ist das wirklich so?“ mit dem normalen Wert. „Nein“ nimmt die Antwort zurück.",
         "- **Kritischer Mangel:** rotes Fenster über den ganzen Bildschirm mit den Ansprechpartnern (Name, Telefon, Hinweis). Nur „Ich habe Bescheid gegeben“ "
         "oder „war ein Versehen“. Ohne Bestätigung lässt sich die Kategorie nicht speichern. Protokoll und Mangel nennen die Bestätigung. **Es wird nichts verschickt.**",
         "- **Kategorien ohne Reihenfolge-Sperre (Paket 10):** Alle Kategorien lassen sich in beliebiger Reihenfolge öffnen und speichern. Die erste offene bleibt als „▶ Als Nächstes“ markiert, "
         "die übrigen heißen „○ Offen“. „Speichern“ springt wie bisher zur ersten noch offenen Kategorie. Abschließen geht weiterhin erst, wenn alle gespeichert sind.",
         "- Eingestellt wird alles im Builder (Paket 9 Builder-Teil folgt). Bis dahin: Spalten direkt in SharePoint setzen.",
         "- Umfang: %d Properties (jede einmal in der Endfassung), %d neue Steuerelemente in 3 Blöcken, 1 neue Liste, 5 neue Spalten." % (len(end), len(d["pakete"][7]["neu"]) + len(d["pakete"][8]["neu"])),
         "- Geprüft: Generator 0 Fehler (Namen, Klammern, Rückübersetzung, gleiche Felder in allen drei Zweigen von colAntworten, 13 Argumente in jedem fnFehlt-Aufruf). "
         "Unabhängig geprüft (14 Befunde eingearbeitet, `arbeit/2026-11-02_App89/pruefung_unabhaengig.md`). **Nicht in Studio getestet.**", ""]
    for gi, (titel, ks) in enumerate(GRUPPEN_89, 1):
        z += ["## Schritt %d – %s" % (gi, titel), ""]
        if ks is None:
            z += ["1. **Neue Liste `RG_Ansprechpartner`** (SharePoint, IMS+). Spalten: `Title` (vorhanden, = Gewerk/Rolle, z. B. „Elektriker“), "
                  "`Kontakt` (Eine Textzeile, Name oder Firma; **nicht** „Name“ nennen, den Namen hat SharePoint schon intern vergeben), `Telefon` (Eine Textzeile), `Hinweis` (Mehrere Textzeilen, nur Text), `Allgemein` (Ja/Nein, Standard Nein), `Aktiv` (Ja/Nein, Standard Ja).",
                  "   Testzeilen: „Allgemein“ (Allgemein = Ja), „Elektriker“, „IT-Dienstleister“. Berechtigung: wie die anderen RG-Listen (Prüfer lesen, Pflegegruppe bearbeiten).",
                  "2. **`RG_Pruefpunkte`** neue Spalten: `Kritisch` (Ja/Nein, Standard Nein), `KritischText` (Eine Textzeile), `Ansprechpartner` (Eine Textzeile, IDs aus `RG_Ansprechpartner` mit `;` getrennt), "
                  "`Rueckfrage` (Ja/Nein, Standard Nein), `RueckfrageText` (Eine Textzeile). `Abschnitt` gibt es schon.",
                  "3. Rundgang-App: **Daten** → `RG_Pruefpunkte` und `RG_Bereiche` → ⋯ → **Aktualisieren**, dann **Daten hinzufügen** → SharePoint → IMS+ → `RG_Ansprechpartner`.",
                  "4. Zum Testen an einem ZZ-Test-Prüfpunkt in SharePoint: `Kritisch` = Ja, `KritischText` = „Anlage nicht weiter betreiben.“, `Ansprechpartner` = ID von „Elektriker“, "
                  "`Rueckfrage` = Ja, `RueckfrageText` = „Normalerweise steht hier i.O.“.", "",
                  "**Rot ab hier bis Schritt 4:** Nach Schritt 2 sind die Aufrufe von `fnFehlt` rot (13 statt 12 Argumente), bis Schritt 3/4 sie ersetzen. Das ist erwartet.", ""]
            continue
        for i, k in enumerate(ks, 1):
            nr = "%d.%d" % (gi, i)
            if k.startswith("#"):
                name = k[1:]
                e = neu[name]["eltern"]
                wo = ("**`%s`** in der Strukturansicht markieren → Strg+V (landet als Geschwister in der Galerievorlage)." % "lblKaAbstand") if e == "galKaPruefpunkte" else (
                    "**`scrKategorie`** (den Bildschirm) markieren → Strg+V. Der Block landet ganz oben und liegt damit über allem.")
                z += ["### %s · neues Steuerelement `%s`" % (nr, name), "", "**Wo hin:** " + wo, "", "```yaml"] + yaml_block(name, neu) + ["```", ""]
                if e == "galKaPruefpunkte":
                    z += ["**Nachprüfen (E-05):** `lblKaAbschnitt.Height` muss die Formel `If(ThisItem.AbsKopf; 44; 0)` sein, keine Zahl. Sonst von Hand einsetzen.", ""]
                else:
                    z += ["**Nachprüfen:** liegt direkt unter `scrKategorie`, ganz oben in der Liste, kein `_1`.", ""]
                continue
            z += prop_abschnitt(nr, k, vorher[k], end[k], ERKL_89[k], eltern)
    z += ["## Test (Zeitachse, nur ZZ-Test-Rundgang)", "",
          "| # | Schritt | erwartet |", "|---|---|---|",
          "| T1 | (braucht Paket 8 im Builder; sonst `Abschnitt` direkt in SharePoint setzen) Zwei Prüfpunkten derselben Kategorie Abschnitt „Kompressor 1“ geben. Rundgang heute starten, Kategorie öffnen | Überschrift „Kompressor 1“ über der ersten der beiden Fragen |",
          "| T2 | (sonst `Ausblenden` = Ja direkt in `RG_Bereiche`) Bereich ausblenden, Rundgang **neu starten** (am Testtag zurücksetzen) | Rundgangsübersicht ohne Bereichs-Überschrift, Kopfzeile ohne Bereich. Ergebnisse und Mängel haben dann keinen Bereichsnamen (gewollt) |",
          "| T3 | Prüfpunkt mit Rückfrage: n.i.O. | Fenster „Ist das wirklich so?“ mit Text. „Nein, korrigieren“ → Antwort leer |",
          "| T4 | n.i.O., „Ja, stimmt“ (Punkt auch kritisch) | rotes Fenster mit „Elektriker“ und „Allgemein“ |",
          "| T5 | Vorher: einen Punkt mit n.i.O. + Kommentar speichern, **danach** in SharePoint `Kritisch` = Ja setzen. Kategorie neu öffnen, Speichern | „Noch offen … (kritisch: Bescheid bestätigen)“, das rote Fenster öffnet sich |",
          "| T5b | Im roten Fenster „n.i.O. war ein Versehen“ | Fenster zu, Antwort leer. Nochmal n.i.O. → Fenster kommt wieder |",
          "| T5c | n.i.O. zweimal schnell tippen | kein Fenster bleibt stehen (Antwort leer → Fenster zu) |",
          "| T6 | „Ich habe Bescheid gegeben“, Kommentar, Speichern | gespeichert. Protokoll: „KRITISCH – Bescheid gegeben, bestätigt von … um …“ |",
          "| T7 | Rundgang abschließen | Mangel: Frage mit Abschnitt, Kommentar beginnt mit „KRITISCH – Bescheid gegeben“ |",
          "| T8 | Zahl mit Grenzen und Rückfrage: Wert außerhalb | Rückfrage „Normalerweise: ab … bis …“ |",
          "| T9 | Neuen Rundgang starten → direkt die 3. Kategorie öffnen, ausfüllen, speichern | gespeichert, danach öffnet sich die 1. Kategorie (erste offene) |",
          "| T10 | Rundgangsübersicht | 3. Kategorie ✓, 1. „▶ Als Nächstes“, übrige „○ Offen“, „Rundgang abschließen“ grau mit „(noch … offen)“ |", "",
          "## Bekannte Grenzen (bewusst nicht gebaut)", "",
          "- Ein sehr schneller zweiter Tipp auf einen Fensterknopf kann in der Karte darunter landen (Befund B10, niedrig).",
          "- Entfernte (deaktivierte) Prüfpunkte erscheinen im Protokoll am Ende, optisch unter dem letzten Abschnitt (B12).",
          "- Ein ausgeblendeter Bereich hat auch in Ergebnissen und Mängeln keinen Namen (B13, gewollt).", "",
          "## Rückweg", "", "Vorher-Fassungen im Anhang einsetzen, die zwei Fenster und `lblKaAbschnitt` löschen. Spalten und Liste dürfen bleiben.", "",
          "## Anhang – Vorher-Fassungen (= Stand nach Paket N)", ""]
    for k in alle_keys:
        z += ["**`%s` vorher**" % k, "", "```", de(vorher[k]), "```", ""]
    return "\n".join(z), alle_keys


def main():
    os.makedirs(ARB, exist_ok=True)
    export = rg.App(EXPORT)
    soll = soll_nach_7()
    d = json.load(open(BLOECKE, encoding="utf-8"))
    t1, reihen = nachhol(export, soll, d)
    open(os.path.join(AUS, "PAKET_N_Nachholen.md"), "w", encoding="utf-8").write(t1 + "\n")
    t2, keys = paket89(d, soll)
    open(os.path.join(AUS, "PAKET_8_9_10_APP.md"), "w", encoding="utf-8").write(t2 + "\n")
    open(os.path.join(ARB, "abgleich.txt"), "w", encoding="utf-8").write(
        "Paket N: " + ", ".join(reihen) + "\nPaket 8-10: " + ", ".join(keys) + "\n")
    print("geschrieben: PAKET_N_Nachholen.md (%d Properties), PAKET_8_9_10_APP.md (%d Properties)" % (len(reihen), len(keys)))


if __name__ == "__main__":
    main()
