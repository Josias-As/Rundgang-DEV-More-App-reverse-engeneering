"""Paket 26 (Fehler A3–A14 + Builder-Optik): python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket26.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_app89  # noqa: E402
import doc_generisch as g  # noqa: E402

ERKL_APP = {
    "btnRgAktion.OnSelect": "**Reparatur + A3 + A10.** Im Export 13.11. steht hier die Formel von `btnKaSpeichern` (Fehleinfügung bei Paket 25). Deshalb die **ganze** Property ersetzen, auch wenn sie anders aussieht als die Vorher-Fassung. "
                            "Neu: Kategorien werden nur aus **diesem** Rundgang gelesen (`RundgangID = varRgID`, A10). Beim Start werden nur Kategorien aufgenommen, die mindestens einen aktiven Prüfpunkt haben (A3). "
                            "Für Altbestand ohne `RundgangID` an Kategorien/Prüfpunkten gilt die alte Regel weiter (dann alle aktiven Kategorien bzw. ohne Prüfpunkt-Filter). **Wichtig:** Fehlt `RundgangID` nur an einzelnen Prüfpunkten, fällt deren Kategorie weg. Vor dem Anlegen der echten Rundgänge prüfen, dass alle Kategorien und Prüfpunkte eine `RundgangID` haben (der Builder setzt sie immer). Gilt nur für **neu gestartete** Läufe.",
    "btnKaSpeichern.OnSelect": "**A9.** Antworten zu inzwischen inaktiven Prüfpunkten (`Inaktiv`) kommen nicht mehr in `colSpeichern`: Sie werden nicht mehr mitgeschrieben, nicht gezählt (AnzahlNIO) und nicht als Mangel angelegt. Achtung: Beim nächsten Speichern der Kategorie wird die Antwortliste ganz neu geschrieben, die alte Antwort des inaktiven Punkts fällt dabei heraus (gewollt). Sonst wie bisher.",
    "App.Formulas": "**A5:** `fnFehltGrund` verlangt bei „Foto Pflicht“ ein Foto nur noch, wenn die Frage Pflicht ist oder beantwortet wurde (freiwillige, unbeantwortete Frage sperrt nicht mehr). „Foto bei Mangel“ unverändert. "
                    "**A14:** `fnPlanPasst` zählt die Wochen ab dem **Montag der Startwoche**, fällig erst ab dem Startdatum selbst.",
}
ERKL_B = {
    "App.Formulas": "**A14:** `fnPlanPasst` wie in Rundgang DEV (Wochen ab Montag der Startwoche, fällig erst ab Startdatum). Der Plan-Bildschirm setzt bei neuen Terminen schon einen Montag; Altdaten können aber einen anderen Tag haben.",
    "btnPTyp.OnSelect": "**A12.** Beim Wechsel des Eingabetyps weg von „Zahl“ wird der Vergleich (`VergleichPunkt`) auf 0 gesetzt. Damit sperrt kein unsichtbarer Vergleich mehr das Aktivieren.",
    "galPr.Items": "**Leere orange Punkte:** `Ungroup` liefert für Regeln ohne Treffer vermutlich eine **leere Zeile** (Art leer → Farbe Orange, Text leer; Indiz: „Alles in Ordnung ✓“ erschien nie). Jetzt werden nur Zeilen mit Art „Fehler“/„Hinweis“ und Text gezeigt. "
                   "**A12:** Der Vergleich wird nur bei Zahl-Fragen geprüft; steht er an einer anderen Frage, kommt nur ein Hinweis. "
                   "**A13:** Neuer Fehler, wenn eine Bedingung „n.i.O.“ auf eine Zahl-Frage zeigt, die nie n.i.O. werden kann (keine Grenzen ab/bis oder „Außerhalb“ = Hinweis/nicht speicherbar).",
    "ddPKategorie.Items": "Nur noch der **Kategoriename**. Der Bereich steht nur dabei, wenn es den Namen mehrmals gibt („Name · Bereich“), bei Doppelten im selben Bereich zusätzlich „#ID“.",
    "ddPKategorie.Default": "Gleiche Anzeige wie die Liste (muss zur Liste passen).",
    "ddPKategorie.Size": "Schrift 13 statt 14, damit längere Namen passen.",
    "btnEdAktivieren.Fill": "Grün, wenn aktivierbar.",
    "btnEdAktivieren.Color": "Weiße Schrift.",
    "btnEdAktivieren.HoverFill": "Dunkleres Grün beim Darüberfahren.",
    "btnEdAktivieren.PressedFill": "Noch dunkler beim Drücken.",
    "btnEdAktivieren.HoverColor": "Weiß.",
    "btnEdAktivieren.PressedColor": "Weiß.",
    "btnEdAktivieren.BorderThickness": "Kein Rahmen.",
    "btnEdAktivieren.DisplayMode": "Bei Fehlern **gesperrt** (grau, Farben aus `DisabledFill`/`DisabledColor`). Der Hinweis „Erst die Fehler beheben“ entfällt dadurch; die Fehlerzahl steht links daneben.",
}


def main():
    za, na, _, anh_a = g.app_teil(26, ERKL_APP, ["Keine neuen Spalten oder Listen."], zusatz_vor=[
        "**Vorab prüfen (Strukturansicht `scrKategorie`):** Im Export 13.11. sind `btnKaBild` und `conKaBild` (mit `btnKaBildSperre`, `conKaBildKarte`) noch da. "
        "Falls sie in Studio schon gelöscht sind: nichts tun (der Export zeigt nur die veröffentlichte Fassung). Sonst jetzt löschen (Paket 24) – sie würden das ⓘ überdecken.", ""])
    zb, keys_b, _, anh_b = g.builder_teil("builder_nach_p24.json", None, ERKL_B, [
        "Keine neuen Daten.",
        "**Voraussetzung:** Die Lage-Werte aus Paket 24 (B2.1–B2.19, `conPRest`) sind eingesetzt. Im Export 13.11. fehlen sie noch (Texte drin, Positionen nicht). "
        "Erst danach prüfen, ob in `conPRest` noch etwas abgeschnitten ist: Laut Generator passen alle Beschriftungen (Textbreiten-Prüfung mit Innenabstand)."])
    z = ["# Paket 26 – Fehler aus dem Testlauf (A3, A5, A9, A10, A12, A13, A14) und Builder-Optik", "",
         "Stand 13.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket26), `werkzeuge/builder.py`, `werkzeuge/doc_paket26.py`. "
         "Vorher = Export 13.11. 12:58 (DEV) bzw. 12:59 (Builder), Kette bis Paket 25 + 24. Alle Vorher-Fassungen sind zeichengleich mit dem Export, **außer** `btnRgAktion.OnSelect` (Fehleinfügung, siehe A3.1).", "",
         "## Kurzfassung", "",
         "- **A3 (hoch):** Beim Start eines Laufs kommen nur Kategorien mit mindestens einem aktiven Prüfpunkt hinein. Vorher blieb so ein Lauf für immer offen.",
         "- **A5 (hoch):** „Foto Pflicht“ sperrt eine freiwillige, unbeantwortete Frage nicht mehr.",
         "- **A9 (hoch):** Antworten zu inaktiven Prüfpunkten zählen nicht mehr als n.i.O./Mangel.",
         "- **A10:** Kategorien werden nur aus dem eigenen Rundgang gelesen (Zeilenlimit).",
         "- **A12 (Builder):** Typwechsel weg von „Zahl“ löscht den Vergleich; die Prüfung meldet ihn nur noch bei Zahlen.",
         "- **A13 (Builder):** Neuer Fehler für eine Bedingung „n.i.O.“ an einer Zahl, die nie n.i.O. wird.",
         "- **A14 (beide):** Plan-Wochen zählen ab dem Montag der Startwoche.",
         "- **Builder-Optik:** keine leeren orangen Punkte mehr in der Prüfliste, „Aktivieren …“ grün (bei Fehlern grau und gesperrt), „Gehört zur Kategorie“ zeigt nur den Kategorienamen.",
         "- **Reparatur DEV:** In `btnRgAktion.OnSelect` steht im Export die Formel von `btnKaSpeichern`. A3.1 ersetzt sie ganz.",
         "- **Bewusst nicht drin:** C25 (alle typfremden Felder beim Typwechsel leeren). Ein versehentlicher Typwechsel würde sonst Grenzen/Einheit löschen. Nur der Vergleich wird geleert, weil nur er das Aktivieren sperrt.",
         "- Umfang: DEV %d Properties, Builder %d Properties, keine neuen Steuerelemente, keine Daten. Generatoren 0 Fehler, Mutation 13/13 und 13/13, Logik-Probe 124 Szenarien (A5, A14), Builder-Logik 27. **Nicht in Studio getestet.**" % (na, len(keys_b)), ""] + za + zb + [
         "## Test", "",
         "| # | Schritt | erwartet |", "|---|---|---|",
         "| T1 | Testdaten: im Testrundgang bei einer Kategorie alle Prüfpunkte in SharePoint auf Aktiv = Nein; DEV: **neuen** Lauf starten. Danach Prüfpunkte wieder auf Aktiv = Ja | diese Kategorie fehlt in der Liste, der Lauf lässt sich abschließen (A3; schon gestartete Läufe behalten ihre Liste) |",
         "| T2 | DEV: Startseite → Rundgang starten | Zahl der Kategorien = Zahl der aktiven Kategorien (mit aktivem Prüfpunkt) dieses Rundgangs im Builder (A10) |",
         "| T3 | DEV: freiwillige Frage mit „Foto Pflicht“ leer lassen, Kategorie speichern | speichert ohne Foto (A5) |",
         "| T4 | DEV: dieselbe Frage beantworten, kein Foto | „Foto“ fehlt, Speichern gesperrt (A5) |",
         "| T5 | DEV: im Testlauf eine Frage n.i.O. beantworten, Kategorie speichern. In SharePoint diesen Prüfpunkt auf Aktiv = Nein. DEV: Kategorie neu öffnen, speichern. Danach Aktiv = Ja zurück | `AnzahlNIO` der Kategorie zählt ihn nicht mehr, kein neuer Mangel, Antwort nicht mehr im JSON (A9) |",
         "| T6 | Builder: Zahl-Frage mit Vergleich → Typ auf i.O./n.i.O. | Vergleich leer, Prüfliste ohne Fehler, Aktivieren grün (A12) |",
         "| T7 | Builder: Bedingung „n.i.O.“ auf eine Zahl ohne Grenzen | roter Fehler „… wird nie n.i.O. …“, Aktivieren grau; Grenze „bis“ eintragen → Fehler weg (A13) |",
         "| T8 | Der Builder setzt den Start immer auf einen Montag; der Fehler betrifft nur Altdaten. Test: in `RG_Plan` (Testrundgang) `StartMontag` = Mi 04.11., Zyklus 2, Wochentag Mo direkt in SharePoint setzen; Builder-Plan ansehen | fällig Mo 16.11. und 30.11. (vorher falsch: 09.11. und 23.11.) (A14) |",
         "| T9 | Builder: Rundgang ohne Fehler und Hinweise | „Prüfung: keine Fehler“, darunter „Alles in Ordnung ✓“, **keine** orangen Punkte |",
         "| T10 | Builder: „Aktivieren …“ mit/ohne Fehler, Maus darüber, drücken | ohne Fehler grün/weiß, dunkler bei Maus/Druck; mit Fehler grau, nicht klickbar |",
         "| T11 | Builder: Prüfpunkt → „Gehört zur Kategorie“ | nur Kategoriename; bei gleichem Namen in zwei Bereichen „Name · Bereich“ |", "",
         "## Rückweg", "", "Vorher-Fassungen aus dem Anhang einsetzen. Für `btnRgAktion.OnSelect` die Vorher-Fassung aus dem Anhang nehmen (nicht den Export-Stand, der ist falsch).", "",
         "## Anhang – Vorher-Fassungen", ""] + anh_a + anh_b
    open(os.path.join(doc_app89.AUS, "PAKET_26_FEHLER_UND_OPTIK.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_26_FEHLER_UND_OPTIK.md (App %d, Builder %d: %s)" % (na, len(keys_b), keys_b))


if __name__ == "__main__":
    main()
