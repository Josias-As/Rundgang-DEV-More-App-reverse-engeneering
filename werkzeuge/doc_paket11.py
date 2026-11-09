"""Paket 11 (Prüfer, Unterschrift, Kopfdaten): python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket11.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doc_app89  # noqa: E402
import doc_generisch as g  # noqa: E402
import rg  # noqa: E402

BL = g.BL
PEN = [n for n in BL["neue_controls"] if n == "penRuUnterschrift"][0]
PEN_P = BL["neue_controls"][PEN]["props"]
ERKL_APP = {
    "App.OnStart": "Startwerte für den gewählten Prüfer (`varPruefer`) und die Unterschrift. Beim Start ist niemand gewählt → die Prüferauswahl erscheint.",
    "scrStart.OnVisible": "Liest die Prüferliste (`colPrueferAlle`).",
    "lblStartNutzer.Text": "Oben rechts steht der gewählte Prüfer statt des Gerätekontos.",
    "lblStartNutzer.OnSelect": "Antippen öffnet die Prüferauswahl (Prüfer wechseln).",
    "btnRgAktion.OnSelect": "Ohne gewählten Prüfer öffnet sich die Auswahl. Sonst wie bisher, aber Prüfer = gewählte Person; das Gerätekonto wird in `Geraetekonto` mitgeschrieben.",
    "btnKaSpeichern.OnSelect": "Prüfer der Kategorie = gewählte Person (statt `User()`).",
    "btnKaKritOk.OnSelect": "„Bescheid gegeben“ mit dem Namen der gewählten Person.",
    "btnRuAbschluss.OnSelect": "Erstes Tippen öffnet die Unterschrift (statt „Wirklich abschließen?“). Nach der Unterschrift läuft der bisherige Abschluss; zusätzlich: Unterschrift als PNG in `RG_Fotos` (Testablage wie Fotos), Bild in `RG_Unterschriften`, Link/Name/Zeit an der Durchführung, `FestgestelltVon` = gewählte Person. Danach ist kein Prüfer mehr gewählt. Ohne Prüfer: Meldung statt Unterschrift. Nach einem Fehler schließt das Fenster (neu unterschreiben).",
    "htmProtokoll.HtmlText": "Kopf: Standort · Adresse, Auftraggeber (wenn gepflegt), dann wie bisher Datum mit KW und Prüfer. Unten: Unterschrift mit Name, Datum, Uhrzeit (auch im Archiv-PDF).",
}
ERKL_B = {
    "galPl.Height": "Platz für die Kopfdaten unten.",
}
SP = ["- Neue Liste **`RG_Pruefer`**: `Title` (vorhanden, = Name), `Email` (Eine Textzeile), `Aktiv` (Ja/Nein, Standard Ja).",
      "- `RG_Rundgaenge`: neue Spalten **`Standort`**, **`Adresse`**, **`Auftraggeber`** (je Eine Textzeile).",
      "- Neue Liste **`RG_Unterschriften`**: `Title` (vorhanden), `DurchfuehrungID` (Zahl), `Bild` (Mehrere Textzeilen, **nur Text**). Eigene Liste, damit das große Bild nicht bei jeder Abfrage der Durchführungen mitgeladen wird.",
      "- `RG_Durchfuehrungen`: neue Spalten **`UnterschriftUrl`** (Mehrere Textzeilen, nur Text), "
      "**`UnterschriftName`** (Eine Textzeile), **`UnterschriftZeit`** (Datum und Uhrzeit), **`Geraetekonto`** (Eine Textzeile).",
      "- Rundgang DEV: Daten → `RG_Rundgaenge` und `RG_Durchfuehrungen` → ⋯ → Aktualisieren; Daten hinzufügen → SharePoint → IMS+ → `RG_Pruefer` und `RG_Unterschriften`; "
      "Daten hinzufügen → **„Office 365-Benutzer“** (Connector `Office365Users`).",
      "- **Für IT/Michael (vor dem Test):** Das gemeinsame Gerätekonto braucht eine Power-Apps-Lizenz, Zugriff auf beide Apps, Schreibrechte auf IMS+ "
      "(alle RG-Listen und `RG_Fotos`) und muss den Connector **Office 365-Benutzer** verwenden dürfen (DLP-Richtlinie der Umgebung: Office 365 Users in derselben Gruppe wie SharePoint). "
      "Beim ersten Start fragt die App einmal nach der Zustimmung für den Connector – mit dem Gerätekonto bestätigen.",
      "- **Wichtig:** `varIstAdmin` (Admin-Funktionen) hängt weiter am angemeldeten Konto (`User()`), also am Gerätekonto. Soll das Gerätekonto keine Admin-Rechte haben, nicht in `cfgAdmins` eintragen."]
PEN_SCHRITT = [
    "**Stifteingabe (über das Menü, ohne YAML):** In der Strukturansicht `conRuUKarte` markieren → **Einfügen → im Suchfeld „Stift“ → die Stifteingabe unter „Klassisch“** (nicht die moderne unter „Eingabe“: sie hat kein `OnSelect`/`Image`, A15). Es muss **in** `conRuUKarte` landen. "
    "Umbenennen in **`penRuUnterschrift`**. Dann diese Properties setzen (Formelleiste, ganze Property):", ""]
for k in ("X", "Y", "Width", "Height", "OnSelect", "Fill", "Color", "BorderColor", "BorderThickness"):
    if k in PEN_P:
        PEN_SCHRITT += ["- `%s`: `%s`" % (k, rg.to_de(PEN_P[k]))]
PEN_SCHRITT += ["", "**Vorab-Test (Pflicht, U1):** In der Vorschau auf der Stifteingabe zeichnen → `varUnterschriftDa` muss `true` werden (Variablen-Ansicht). "
                "Bleibt es `false`, löst das Zeichnen kein `OnSelect` aus – dann melden; der Knopf „Unterschreiben und abschließen“ bliebe gesperrt.", ""]


def main():
    ROT = ["**Kurzzeitig rot (erwartet):** Nach A2.1/A2.2 sind `colPrueferAlle`, `varPruefer` und `penRuUnterschrift` noch unbekannt. "
           "Das verschwindet mit der Stifteingabe (Ende A2.2), A3.1 (`App.OnStart`) und A3.2 (`scrStart.OnVisible`). Erst danach die App-Prüfung ansehen.", ""]
    za, na, neu_a, anh_a = g.app_teil(11, ERKL_APP, SP, zusatz_vor=ROT, ohne=[PEN], nach={"conRuUnterschrift": PEN_SCHRITT})
    zb, keys_b, neu_b, anh_b = g.builder_teil("builder_nach_p18.json", None, ERKL_B,
                                               ["Spalten und Liste aus A1 (nur einmal anlegen). Builder: `RG_Rundgaenge` aktualisieren, `RG_Pruefer` und **Office 365-Benutzer** hinzufügen."])
    z = ["# Paket 11 – Prüfer wählen, Unterschrift, Kopfdaten", "",
         "Stand 06.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket11), `werkzeuge/builder.py`, `werkzeuge/doc_paket11.py`. Voraussetzung: Paket 23 und 18 in beiden Apps.", "",
         "## Kurzfassung", "",
         "- **Gerätekonto:** Das iPad bleibt mit einem gemeinsamen Konto angemeldet. Wer prüft, wählt beim Start seinen Namen: oben die Liste `RG_Pruefer` (ein Tipp), darunter **„Andere Person suchen“** im Firmenverzeichnis (Vertretung). "
         "Über die Suche gewählte Personen kommen automatisch in `RG_Pruefer`. Keine PIN.",
         "- Überall, wo bisher `User()` den Prüfer lieferte (Durchführung, Kategorie, Mängel, „Bescheid gegeben“), steht jetzt die gewählte Person. Das Gerätekonto wird in `Geraetekonto` mitgeschrieben.",
         "- **Unterschrift Pflicht:** „Rundgang abschließen“ öffnet ein Unterschriftsfeld, darunter Name, Datum, Uhrzeit. Erst „Unterschreiben und abschließen“ schließt ab. "
         "Die Unterschrift wird als PNG in `RG_Fotos` abgelegt (Testablage wie Fotos), Bild und Link stehen an der Durchführung, im Protokoll und im Archiv-PDF.",
         "- **Danach ist kein Prüfer mehr gewählt:** Zurück auf der Startseite erscheint wieder die Auswahl.",
         "- **Kopfdaten:** Je Rundgang im Builder unter **Plan** unten Standort, Adresse, Auftraggeber (optional). Protokollkopf: Rundgang, Standort · Adresse, Auftraggeber, Datum mit KW, Prüfer.",
         "- **Builder:** Prüferliste unter Übersicht › Ansprechpartner › **👤 Prüfer** (Liste, aktiv/inaktiv, Personensuche aus dem Firmenverzeichnis).",
         "- Umfang: App %d Properties + %d neue Steuerelemente (davon die Stifteingabe über das Menü); Builder %d Properties + %s. Generatoren 0 Fehler, Mutation 12/12 und 13/13, Textbreiten geprüft. **Nicht in Studio getestet.**"
         % (na, len(BL["neue_controls"]) and len([q for q in BL["pakete"] if q["nr"] == 11][0]["neu"]), len(keys_b), ", ".join("`%s`" % x for x in neu_b)),
         "- **UNSICHER (Vorab-Tests):** U1 `OnSelect` der Stifteingabe beim Zeichnen; U2 Flow `aRG_Foto_hochladen` nimmt `penRuUnterschrift.Image` wie ein Foto an; "
         "U3 das Bild (Daten-URL) erscheint im Archiv-PDF; U4 das Bild passt in `RG_Unterschriften.Bild` (mehrzeiliger Text) – bei Fehler „Schreibfehler“ beim Abschluss. Alle vier stehen in der Testtabelle (V1–V4).", ""] + za + zb + [
         "## Test", "",
         "| # | Schritt | erwartet |", "|---|---|---|",
         "| V1 | Vorab: auf der Stifteingabe zeichnen (Vorschau) | `varUnterschriftDa` = true |",
         "| V2 | Vorab: T6 durchführen | PNG liegt im Ordner des Laufs; im Flow-Verlauf kein Fehler, keine Foto-Zeile mit Prüfpunkt 0, die stört |",
         "| V3 | Vorab: Archiv-PDF des Laufs aus T6 öffnen | Unterschrift sichtbar |",
         "| V4 | Vorab: lange Unterschrift über das ganze Feld | Abschluss ohne Schreibfehler, Zeile in `RG_Unterschriften` |",
         "| T1 | App neu starten | Vollbild „Wer prüft?“; ohne Auswahl geht nichts |",
         "| T2 | „Andere Person suchen“: 3 Buchstaben eines Kollegen | Treffer mit Abteilung; antippen → Startseite, oben „Name · wechseln ›“; Kollege steht jetzt in `RG_Pruefer` |",
         "| T3 | Name oben antippen → anderen wählen | Wechsel ohne Neustart |",
         "| T4 | Rundgang starten, Kategorie speichern | `PrueferName`/`PrueferEmail` = gewählte Person, `Geraetekonto` = Gerätekonto |",
         "| T5 | „Rundgang abschließen“ | Unterschriftsfeld; Knopf gesperrt bis gezeichnet; „Löschen“ leert; „Abbrechen“ schließt ohne Abschluss |",
         "| T6 | Unterschreiben und abschließen | Protokoll unten mit Unterschrift, Name, Datum, Uhrzeit; PNG im Ordner des Laufs (`TEST/…` bei Testrundgang); `UnterschriftUrl` gefüllt |",
         "| T7 | Zurück zur Startseite | „Wer prüft?“ erscheint wieder |",
         "| T8 | Builder › Plan: Standort/Adresse/Auftraggeber eintragen | Protokollkopf zeigt sie (neu geöffnetes Protokoll) |",
         "| T9 | Builder › Ansprechpartner › 👤 Prüfer: Person suchen, „+“; Eintrag inaktiv | erscheint/verschwindet in der App-Auswahl (nach Neustart der Startseite) |",
         "| T10 | Fehlerfall: Flow ausschalten, abschließen | Abschluss klappt, Meldung „Unterschrift-Datei nicht hochgeladen“, Unterschrift im Protokoll |",
         "| T11 | „Unterschreiben und abschließen“ zweimal schnell tippen | nur ein Abschluss |",
         "| T12 | Mitten im Lauf Prüfer wechseln, Kategorie speichern | neue Kategorie mit neuem Prüfer, ältere behalten ihren |",
         "| T13 | Nach Abschluss: Startseite, „Weiter ›“ im roten Hinweis | erst „Wer prüft?“, der Hinweis liegt darunter |", "",
         "## Rückweg", "", "Vorher-Fassungen einsetzen; neue Steuerelemente und Bildschirm löschen. Listen/Spalten dürfen bleiben.", "",
         "## Anhang – Vorher-Fassungen", ""] + anh_a + anh_b
    open(os.path.join(doc_app89.AUS, "PAKET_11_PRUEFER_UNTERSCHRIFT.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_11_PRUEFER_UNTERSCHRIFT.md (App %d, Builder %d, neu App %s, neu Builder %s)" % (na, len(keys_b), neu_a, neu_b))


if __name__ == "__main__":
    main()
