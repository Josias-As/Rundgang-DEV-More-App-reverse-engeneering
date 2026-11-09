"""Paket 25 (Rückbau Prüferauswahl): python3 -I werkzeuge/baukasten.py 2026-10-27_0909 && python3 -I werkzeuge/builder.py && python3 -I werkzeuge/doc_paket25.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import doc_app89  # noqa: E402
import doc_generisch as g  # noqa: E402
from doc_paket12_16 import block, pfad  # noqa: E402

ERKL = {
    "App.OnStart": "Startwerte `varPruefer`/`varPrWahl` entfallen. Die Startwerte der Unterschrift bleiben.",
    "scrStart.OnVisible": "Die Prüferliste wird nicht mehr geladen.",
    "lblStartNutzer.Text": "Oben rechts wieder der angemeldete Name (wie vor Paket 11).",
    "lblStartNutzer.OnSelect": "Antippen tut nichts mehr (Standardwert `false`).",
    "btnRgAktion.OnSelect": "Wieder genau wie vor Paket 11: Prüfer = angemeldete Person (`User()`), keine Prüfer-Abfrage, `Geraetekonto` wird nicht mehr geschrieben.",
    "btnKaSpeichern.OnSelect": "Prüfer der Kategorie wieder `User()`.",
    "btnKaKritOk.OnSelect": "„Bescheid gegeben“ wieder mit `User().FullName`.",
    "btnRuAbschluss.OnSelect": "Unterschrift bleibt. Entfernt: die Meldung „Kein Prüfer gewählt“ und das Zurücksetzen des Prüfers nach dem Abschluss. `FestgestelltVon` und `UnterschriftName` wieder aus `User()`. Die Korrektur A17 (`If(IsError(Patch(RG_Unterschriften …)))`) ist enthalten.",
    "lblRuUText.Text": "Name aus `User()`.",
    "lblRuUName.Text": "Name aus `User()`.",
}


def main():
    za, na, _, anh_a = g.app_teil(25, ERKL, [
        "Keine neuen Spalten. Die Liste `RG_Pruefer` und die Spalte `Geraetekonto` dürfen in SharePoint bleiben (werden nicht mehr benutzt).",
        "**Reihenfolge:** erst A3 (Formeln), dann A4 (Löschen), dann A5 (Datenquellen). Sonst wird es rot."])
    bn = json.load(open(os.path.join(builder.AUS_ARB, "bloecke.json"), encoding="utf-8"))
    eltern = bn["eltern"]
    z = ["# Paket 25 – Rückbau Prüferauswahl (echte Anmeldung statt Gerätekonto)", "",
         "Stand 09.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket25), `werkzeuge/builder.py`, `werkzeuge/doc_paket25.py`. "
         "Vorher = Export 09.11. 14:09 (DEV) bzw. 14:09 (Builder) – die vom Einsetz-Chat geänderte Fassung (A17) ist berücksichtigt; alle Vorher-Fassungen sind zeichengleich mit dem Export.", "",
         "## Kurzfassung", "",
         "- Entscheidung 09.11.: Jeder meldet sich mit seiner echten Mail an. Die **Prüferauswahl aus Paket 11 fällt weg**, Prüfer ist wieder überall `User()` (wie vor Paket 11).",
         "- **Bleibt:** Unterschrift (Pflicht beim Abschließen, `RG_Unterschriften`, Link/Name/Zeit an der Durchführung) und Kopfdaten (Standort/Adresse/Auftraggeber). Unter der Unterschrift steht jetzt der angemeldete Name.",
         "- **Weg:** `conPwWahl` (Rundgang DEV), `scrPruefer` + `btnKoPruefer` (Builder), Datenquellen `RG_Pruefer` und Office 365-Benutzer (beide Apps).",
         "- **Dazu Reparatur Builder:** Beim Einsetzen von Paket 23 ist die neue Formel für `btnPNio.OnSelect` in `btnNioKontakt.OnSelect` gelandet (Export 09.11.). Folge: Antippen eines Ansprechpartners im Fenster „Bei n.i.O.“ öffnet das Fenster neu, statt ihn an-/abzuwählen.",
         "- Der Generator prüft, dass danach **keine** Formel mehr auf `varPruefer`, `varPrWahl`, `colPrueferAlle`, `RG_Pruefer`, `Office365Users`, `conPwWahl` oder dessen Kinder verweist. Neu: Prüfung gegen `IfError(…; Set(…))` als `If`-Zweig auch für Rundgang DEV (A17), Mutation 13/13.",
         "- Umfang: DEV %d Properties + 1 Container löschen + 2 Datenquellen; Builder 1 Bildschirm + 1 Knopf löschen, 2 Properties reparieren, 2 Datenquellen. **Nicht in Studio getestet.**" % na, ""] + za + [
         "### A4 – löschen", "", "In der Strukturansicht von `scrStart` **`conPwWahl`** löschen (mit allen Kindern: `lblPwTitel`, `lblPwHinweis`, `galPwListe`, `btnPwName`, `lblPwLeer`, `lblPwSuchT`, `txtPwSuche`, `galPwSuche`, `btnPwTreffer`, `btnPwZu`).", "",
         "### A5 – Datenquellen entfernen", "", "Daten → `RG_Pruefer` → ⋯ → **Entfernen**; Daten → **Office 365-Benutzer** (`Office365Users`) → ⋯ → **Entfernen**. Danach App-Prüfung: 0 Fehler erwartet.", "",
         "## Teil B – Builder", "",
         "### B1 – Reparatur (Fehleinfügung aus Paket 23)", ""]
    for i, k in enumerate(("btnNioKontakt.OnSelect", "btnPNio.OnSelect"), 1):
        ende = [x for x in bn["de"][k].strip().split("\n") if x.strip()][-1].strip()[-60:]
        z += ["### B1.%d · `%s`" % (i, k), "", "**Pfad:** `%s` → OnSelect" % pfad(k.split(".")[0], eltern), "",
              "```", bn["de"][k], "```", "", "**Nachprüfen:** endet auf `%s`" % ende, "",
              "**Kurz erklärt:** " + ("Wieder: Antippen nimmt den Ansprechpartner auf bzw. heraus (Formel aus Paket 9). Hier stand die Öffnen-Formel von `btnPNio`."
                                      if i == 1 else "Öffnet „Bei n.i.O.“ und liest alle Ansprechpartner frisch (auch inaktive, zum Entfernen) – das war der eigentliche Schritt aus Paket 23."), ""]
    z += ["### B2 – löschen", "",
          "- Bildschirm **`scrPruefer`** löschen (falls schon eingefügt).",
          "- In `scrKontakte › conKoKopf` den Knopf **`btnKoPruefer`** löschen (falls schon eingefügt).",
          "- Daten → `RG_Pruefer` und **Office365-Benutzer** (deutsch `'Office365-Benutzer'`) → ⋯ → Entfernen.", "",
          "### B3 – Kopfdaten im Plan (bleiben)", "",
          "Im Export 09.11. fehlen die Kopfdaten-Felder (Paket 11 B1.2–B1.9: `lblPlKopfT`, `lblPlStandortT`, `txtPlStandort`, `lblPlAdresseT`, `txtPlAdresse`, `lblPlAuftragT`, `txtPlAuftrag`; B2.1 `galPl.Height`). "
          "Wenn sie in Studio noch nicht da sind (oder nicht veröffentlicht): aus `pakete/PAKET_11_PRUEFER_UNTERSCHRIFT.md` B1.2–B1.9 und B2.1 einfügen – unverändert gültig.", "",
          "## Test", "",
          "| # | Schritt | erwartet |", "|---|---|---|",
          "| T1 | App starten | kein „Wer prüft?“; oben rechts der eigene Name |",
          "| T2 | Rundgang starten, Kategorie speichern | `PrueferName`/`PrueferEmail` = angemeldete Person; `Geraetekonto` leer |",
          "| T3 | Kritischer Mangel → Bescheid gegeben | im JSON `KritischVon` = eigener Name; Protokoll „KRITISCH – Bescheid gegeben, bestätigt von <Name>“ |",
          "| T4 | Abschließen | Unterschriftsfeld mit eigenem Namen; Protokoll unten Unterschrift + Name; Mängel `FestgestelltVon` = eigene Mail |",
          "| T4b | „Rundgang abschließen“ → Unterschrift → Abbrechen → erneut „Rundgang abschließen“ | Feld wieder leer, Abschluss erst nach neuer Unterschrift |",
          "| T4c | „Unterschreiben und abschließen“ zweimal schnell | nur ein Abschluss, Mängel nicht doppelt |",
          "| T5 | Nach dem Abschluss zur Startseite | keine Prüferauswahl |",
          "| T6 | App-Prüfung beider Apps | 0 Fehler |",
          "| T7 | Builder: Prüfpunkt › Bei n.i.O. › Ansprechpartner antippen | ✓/○ wechselt, Fenster bleibt offen |",
          "| T8 | Builder: Plan eines Rundgangs | unten Kopfdaten-Felder |", "",
          "## Rückweg", "", "Erst die Datenquellen `RG_Pruefer` und Office 365-Benutzer wieder hinzufügen, dann `conPwWahl` aus Paket 11 (A2.1) einfügen, dann die Vorher-Fassungen. Builder: `scrPruefer`/`btnKoPruefer` aus Paket 11.", "",
          "## Anhang – Vorher-Fassungen", ""] + anh_a
    open(os.path.join(doc_app89.AUS, "PAKET_25_RUECKBAU_PRUEFER.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/PAKET_25_RUECKBAU_PRUEFER.md (DEV %d Properties)" % na)


if __name__ == "__main__":
    main()
