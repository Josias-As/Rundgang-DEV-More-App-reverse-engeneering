"""Einbau-Anleitung für den Rundgang-Builder aus arbeit/2026-10-30_Builder/bloecke.json erzeugen.
Aufruf: python3 -I werkzeuge/doc_builder.py  ->  pakete/builder/EINBAU_BUILDER.md"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rg  # noqa: E402
import builder  # noqa: E402

ARB = os.path.join(rg.REPO, "arbeit", "2026-10-30_Builder")
AUS = os.path.join(rg.REPO, "pakete", "builder")


def block(t, sprache=""):
    return ["```" + sprache, t, "```", ""]


def main():
    d = json.load(open(os.path.join(ARB, "bloecke.json"), encoding="utf-8"))
    pruef = open(os.path.join(ARB, "pruefung.txt"), encoding="utf-8").read()
    st = d["stat"]
    fehler = pruef.strip().split("\n")[-1]
    z = ["# Rundgang-Builder – Einbau (neue App)", "",
         "Stand: 30.10.2026 · erzeugt mit `werkzeuge/builder.py` (Formeln und Bildschirme) und `werkzeuge/doc_builder.py`. "
         "Grundlage: Konzept v3 (`arbeit/2026-10-30_Builder_Konzept/KONZEPT_Builder_v3_Vorschlag.md`) und die Spalten aus dem Export 27.10. 09:09 + Pakete 1–7.", "",
         "## Kurzfassung", "",
         "- **Neue Canvas-App „Rundgang Builder“** (Tablet-Format quer, 1366 × 768, für den PC gedacht) mit drei Bildschirmen: "
         "**Übersicht** (alle Rundgänge), **Editor** (Gliederung · Bearbeiten · Vorschau und Prüfung) und **Plan**.",
         "- Einfügen in 6 Schritten: SharePoint-Spalten → App anlegen → App.Formulas → App.OnStart → drei Bildschirme als YAML → App-Prüfung. "
         "%d Steuerelemente, %d Properties, alles maschinell erzeugt und geprüft (%s)." % (st["steuerelemente"], st["properties"], fehler),
         "- **Die Rundgang-App wird nicht geändert** (außer Paket 7, das vorher eingefügt sein muss). Der Builder schreibt nur Daten, die die Rundgang-App schon richtig liest.",
         "- **Fassungen:** Ein aktiver Rundgang wird nie direkt geändert. „Bearbeiten“ legt einen Entwurf (neue Fassung) an. „Aktivieren“ schaltet die Bereiche der alten Fassung aus und die der neuen an. "
         "Rundgang-Nummer, Plan und Auswertung bleiben gleich. Laufende Rundgänge von heute werden mit der alten Fassung beendet.",
         "- **Vorlagen** sind ein eigener Rundgang „Vorlagen (Builder)“ mit 10 Startvorlagen; „Aus Vorlage holen“ kopiert Prüfpunkte, Kategorien oder ganze Bereiche – auch aus anderen Rundgängen.",
         "- Nicht getestet (UNSICHER, Abschnitt 9): Einfügen ganzer Bildschirme als YAML in einer **neuen** App, Leeren von Zahlspalten mit `Blank()`, Vorschaubilder. Für jeden Punkt steht ein Test im Testbogen.", "",
         "## 1. Was die App kann", "",
         "| Bildschirm | Inhalt |", "|---|---|",
         "| Übersicht | Liste der Rundgänge (Entwürfe und aktive; Schalter „Archivierte zeigen“). Je Zeile: Status, aktive Fassung, Plan, offener Entwurf. Knöpfe **Bearbeiten**, **Ansehen**, **Plan**, **Archivieren/Reaktivieren/Löschen**, **Entwurf verwerfen**. Oben **+ Neuer Rundgang** (leer oder als Kopie) und **Vorlagen bearbeiten**. |",
         "| Editor | Links die **Gliederung** (Bereich ▸ Kategorie ▸ Prüfpunkte der gewählten Kategorie, ⚠ bei Fehlern), unten **+ Bereich / + Kategorie / + Prüfpunkt**, **Mehrere Fragen** (eine pro Zeile, auch aus Excel kopiert) und **Aus Vorlage holen**. "
         "In der Mitte das gewählte Teil bearbeiten (↑ ↓, Duplizieren, Entfernen mit zweitem Tippen, Verschieben über „Gehört zu …“). Prüfpunkt: Frage, Art als Kacheln, Pflicht, Kommentar, Grenzen als „ab/bis“ und „außerhalb ergibt“, Antwortmöglichkeiten eine pro Zeile, Foto-Regel, Bedingung als „Nur zeigen, wenn [Frage] [Wert]“, Hinweis, Beispielbild. "
         "Rechts die **Vorschau** (so sieht es der Prüfer, plus die Regeln in Worten) und die **Prüfung** (Fehler rot, Hinweise gelb, antippen springt zur Stelle). Oben **Aktivieren …** mit Änderungsübersicht. Jede Änderung wird sofort gespeichert („Gespeichert hh:mm:ss“). |",
         "| Plan | Planzeilen als Wochentag · Rhythmus · Startwoche · gültig bis · aktiv/pausiert, rechts die nächsten Termine (gleiche Regel wie die Rundgang-App). Änderungen gelten sofort. |", "",
         "## 2. Entscheidungen (von mir getroffen, bitte bestätigen)", "",
         "- **Gebaut wird am PC** (Querformat, drei Spalten nebeneinander). Am Tablet quer ist die App bedienbar, hochkant nicht.",
         "- **Fassungen an den Bereichen** statt Kopie des ganzen Rundgangs (Konzept v3, 4A). Deshalb gibt es die Warnung „alte Version noch aktiv“ nicht: Zwei aktive Fassungen desselben Rundgangs kann es nicht geben. Der Schalter in der Übersicht zeigt Archivierte; Entwürfe und aktive sieht man immer.",
         "- **Vorlagen als Rundgang „Vorlagen (Builder)“** statt eigener Liste (Konzept v3, 4C). Er wird beim ersten Tippen auf „Vorlagen bearbeiten“ angelegt und nie aktiviert.",
         "- **Excel:** kein eigener Import. Eine Spalte mit Fragen lässt sich in „Mehrere Fragen“ einfügen (eine Zeile = ein Prüfpunkt). Ein Import mehrerer Spalten folgt, wenn der Fachbereich wirklich Excel schickt.",
         "- **Entfernen mit zweitem Tippen** (1-s-Sperre gegen Doppelklick) statt „Rückgängig“: einfacher und sicher, weil im Entwurf nichts Live ist.",
         "- **Plan und Name** gelten sofort (sie sind keine Inhalte der Fassung). Der Plan wird beim Kopieren nicht mitkopiert.",
         "- **Bereichs- und Kategorie-Hinweise** bietet der Builder nicht an: Die Rundgang-App zeigt sie nicht (belegt). Beim Kopieren werden sie mitgenommen.", "",
         "## 3. Voraussetzungen", "",
         "- Rundgang-App: **Pakete 1–7** eingefügt (Paket 6 = Bibliothek `RG_Hinweisbilder` und Spalte `HinweisBildID`, Paket 7 = Foto-Wert „Bei Mangel Pflicht“). Ohne Paket 7 nie „Foto Pflicht bei Mangel“ wählen.",
         "- In `RG_Hinweisbilder` mindestens ein Bild (für den Test).",
         "- Nur die Pflegegruppe bekommt den Builder. Rechte auf den Stammdaten-Listen: Pflegegruppe bearbeiten, Prüfer lesen (sonst kann jeder über SharePoint ändern).", "",
         "## 4. Schritt B0 – SharePoint-Spalten (zuerst)", "",
         "Nur Spalten hinzufügen, nichts umbenennen. Name **genau so** (intern = Anzeigename), keine Pflichtspalten, keine Standardwerte nötig (der Builder schreibt immer alle Werte). "
         "Bestehende Zeilen bleiben leer – der Builder füllt sie beim ersten Öffnen eines Rundgangs („wird für den Builder vorbereitet“).", "",
         "| Liste | Spalte | Typ |", "|---|---|---|"]
    for liste, cols in builder.NEU_SPALTEN.items():
        for name, typ in cols.items():
            if liste == "RG_Pruefpunkte" and name in ("Foto", "KommentarPflicht", "Grenzmodus", "BedingungPunkt", "BedingungWert", "HinweisBildID"):
                continue
            z.append("| %s | %s | %s |" % (liste, name, {"Text": "Eine Textzeile", "Zahl": "Zahl, 0 Dezimalstellen"}[typ]))
    z += ["", "Empfohlen (für später, mehr als 5000 Zeilen): in `RG_Kategorien` und `RG_Pruefpunkte` die Spalte **RundgangID** indizieren (Listeneinstellungen → Indizierte Spalten).", "",
          "## 5. Schritt B1 – App anlegen", "",
          "1. make.powerapps.com → gleiche Umgebung wie „Rundgang DEV“ → **Erstellen → Leere App → Leere Canvas-App** → Name **Rundgang Builder**, Format **Tablet** → Erstellen.",
          "2. **Einstellungen → Allgemein:** Datenzeilen-Grenzwert **2000**. **Einstellungen → Updates → Neu:** **Benutzerdefinierte Funktionen** an (wie in der Rundgang-App). **Anzeige:** Querformat, „An Bildschirm anpassen“ an (Standard).",
          "3. **Daten → Daten hinzufügen → SharePoint** → IMS+ (`https://technoformgroup.sharepoint.com/sites/IMSKonzept`) → diese 7 Listen/Bibliotheken: " + ", ".join("`%s`" % q for q in builder.QUELLEN) + ".",
          "4. Speichern.", "",
          "## 6. Schritt B2/B3 – App.Formulas und App.OnStart", "",
          "**Steuerelement:** App · **Property:** `Formulas` – ganzen Text ersetzen (Datei `pakete/builder/App.Formulas.txt`):", ""]
    z += block(rg.to_de(builder.FORMULAS))
    z += ["**Steuerelement:** App · **Property:** `OnStart` – ganzen Text ersetzen (Datei `pakete/builder/App.OnStart.txt`). Danach oben bei App „OnStart ausführen“:", ""]
    z += block(rg.to_de(builder.ONSTART))
    z += ["Rot erwartet: Nichts. Die Listen müssen schon als Daten hinzugefügt sein (sonst sind `RG_…` rot).", "",
          "## 7. Schritt B4 – Bildschirme einfügen", "",
          "Reihenfolge: **scrListe**, dann **scrEditor**, dann **scrPlan**. So geht es je Datei:",
          "1. Datei öffnen (`pakete/builder/scrListe.yaml` usw.), **alles** markieren und kopieren.",
          "2. In Studio in der **Strukturansicht** einen Bildschirm markieren (z. B. `Screen1`) und **Strg+V**. Studio legt den Bildschirm mit allen Steuerelementen an.",
          "3. Prüfen: Der Bildschirm heißt genau `scrListe` (bzw. `scrEditor`, `scrPlan`). Heißt er `scrListe_1`, umbenennen.",
          "", "Rot erwartet, bis alle drei eingefügt sind: `Navigate(scrEditor…)` und `Navigate(scrPlan…)` in scrListe. Nach dem dritten Bildschirm muss alles weg sein.",
          "", "Danach: `Screen1` löschen. **App → StartScreen** = `scrListe`. Speichern.",
          "", "Falls Strg+V keinen Bildschirm anlegt (UNSICHER, U1): Bildschirm von Hand anlegen (Neuer Bildschirm → Leer), umbenennen, `Fill` und `OnVisible` aus der YAML-Datei (Abschnitt `Properties` oben) in die Formelleiste kopieren, "
          "dann die Steuerelemente unter `Children:` als Block kopieren und auf dem markierten Bildschirm einfügen. Mir Bescheid geben, dann erzeuge ich Dateien je Container.", "",
          "| Datei | Bildschirm | Steuerelemente (Container oben) |", "|---|---|---|"]
    for s in builder.SCREENS:
        z.append("| `pakete/builder/%s.yaml` | %s | %s |" % (s.name, s.name, ", ".join(k.name for k in s.kinder)))
    z += ["", "Wichtig: In der Strukturansicht müssen die Fenster (`conNeu`, `conAkt`, `conHolen`, `conMehr`, `conBild`) und die Lade-Fläche (`conLiLaden`, `conEdLaden`, `conPlLaden`) **ganz oben** stehen (sie liegen in der Datei am Ende = vorne). Falls nicht: Rechtsklick → Nach vorne bringen.", "",
          "## 8. Schritt B5 – App-Prüfung, Speichern, Teilen", "",
          "- **App-Prüfung → Formeln = 0.** Barrierefreiheit-Hinweise sind bekannt (Knöpfe ohne Beschriftung für Bildschirmleser).",
          "- Speichern, dann den **Testbogen** (Abschnitt 10) in der Vorschau. Erst danach veröffentlichen und nur mit der Pflegegruppe teilen.", "",
          "## 9. UNSICHER – vor dem Einsatz testen", "",
          "| Nr | Punkt | Test | Wenn es nicht geht |", "|---|---|---|---|",
          "| U1 | Ganze Bildschirme als YAML in eine neue App einfügen (in der Rundgang-App belegt: scrStart/scrRundgang/scrKategorie so eingefügt) | B4 | Weg aus Abschnitt 7 |",
          "| U2 | Zahl leeren: `Patch(…; {MinWert: Blank()})` leert die SharePoint-Spalte | T5 (ab-Wert löschen) | Ich baue das Leeren um (Formelebene-Fehlerverwaltung prüfen) |",
          "| U3 | Vorschaubilder `Thumbnail.Small` der Bibliothek | T9 | wie Paket 6, Vorab-Test 6.3 |",
          "| U4 | Auswahl-Steuerelemente (Classic Dropdown) lösen `OnChange` auch beim Wechsel der Auswahl aus | T5–T8 | unkritisch: Jede `OnChange`-Formel schreibt nur, wenn sich der Wert wirklich ändert |",
          "| U5 | Reihenfolge der Ereignisse: Text ändern und sofort links einen anderen Punkt antippen speichert beim **alten** Punkt | T5 (letzte Zeile) | Ich baue ein Speichern beim Verlassen der Auswahl |",
          "| U6 | `fnMontag` (Startwoche) und Datumsspalten: Speichern als Datum ohne Zeitverschiebung | T13 | Datum in SharePoint ansehen |",
          "| U7 | Der Arbeits-Zeitgeber `tmrArbeit` startet nach dem Öffnen des Editors (Wechsel von `varArbeitStart` false → true) | T2, T3 | Bleibt „Bitte warten …“ stehen: Vorschau neu starten, mir Bescheid geben (dann Knopf „Abbrechen“) |",
          "| U8 | Ein zweites Fenster mit demselben Entwurf: nach dem Aktivieren im ersten schreibt das zweite nichts mehr | T11b | – |", "",
          "## 10. Testbogen (Zeitachse)", "",
          "Mit dem bestehenden Testrundgang „ZZ Test Objektrundgang TCC“ und neuen Rundgängen, die mit **ZZ Test** beginnen (die Rundgang-App legt dafür Testdatensätze an). Reihenfolge einhalten.", "",
          "| # | Schritt | erwartet |", "|---|---|---|",
          "| T1 | Builder in der Vorschau starten | Übersicht: „ZZ Test Objektrundgang TCC“, Status Aktiv, Plan-Text |",
          "| T2 | „Ansehen“ | Meldung „wird für den Builder vorbereitet“, dann Editor nur lesen: Gliederung mit den aktiven Bereichen/Kategorien, deaktivierte (Id 9, inaktive Kategorie) fehlen. In SharePoint haben die Zeilen jetzt Fassung 1 und RundgangID. |",
          "| T3 | Zurück, „Bearbeiten“ → Text „Neue Fassung?“ und Hinweiszeile → nochmal tippen | Editor „Entwurf Fassung 2“, gleiche Inhalte. Übersicht zeigt danach „Entwurf Fassung 2 in Arbeit (Name)“. Die Rundgang-App zeigt den Rundgang unverändert. |",
          "| T4 | Rundgang-App: den Testrundgang heute **starten** und die erste Kategorie öffnen (nicht abschließen) | läuft wie bisher |",
          "| T5 | Builder: Prüfpunkt antippen, Frage ändern, Tab | „Gespeichert hh:mm:ss“; Vorschau zeigt neuen Text. Art „Zahl“, ab 100, bis 1000, „Hinweis + Grund“: Vorschau-Regeln passen. ab-Wert löschen (U2): Feld bleibt leer nach erneutem Öffnen. Zuletzt: Frage ändern und **ohne Tab** sofort einen anderen Prüfpunkt antippen (U5): Änderung beim richtigen Punkt. |",
          "| T6 | ab 1000, bis 100 | Prüfung rot „ab ist größer als bis“, ⚠ in der Gliederung, „Aktivieren …“ grau und meldet die Fehler. Wieder richtig stellen. |",
          "| T7 | + Prüfpunkt, „Mehrere Fragen“ mit 3 Zeilen, Duplizieren, ↑ ↓, Entfernen (zweimal tippen), „Gehört zur Kategorie“ ändern | jeweils sofort sichtbar; doppelt schnell tippen auf „+ Bereich“ legt nur einen Bereich an |",
          "| T8 | Bedingung: an einem späteren Punkt „Nur zeigen, wenn“ eine frühere i.O./n.i.O.-Frage und „n.i.O. (Mangel)“ | Auswahl zeigt nur frühere Fragen ohne eigene Bedingung; an der Frage A ist die Bedingung danach gesperrt; Vorschau „nur sichtbar, wenn …“ |",
          "| T9 | „Bild wählen“ → Bild antippen | Vorschaubild neben dem Knopf, Vorschau „mit Beispielbild“ (U3) |",
          "| T10 | Übersicht → „Vorlagen bearbeiten“ | Rundgang „Vorlagen (Builder)“ mit Bereich „Vorlagen“, 3 Kategorien, 10 Prüfpunkten. Zurück, Testrundgang bearbeiten, „Aus Vorlage holen“ → Prüfpunkt „Temperatur“ → übernehmen | erscheint am Ende der gewählten Kategorie |",
          "| T11 | „Aktivieren …“ | Fenster: neu/geändert/entfernt mit Liste, Hinweis „Heute läuft noch ein Rundgang …“ (wegen T4). „Jetzt aktivieren“ → Übersicht „aktive Fassung 2“ |",
          "| T11b | Vor T11 den Builder in einem zweiten Browser-Fenster mit demselben Entwurf offen lassen; nach T11 dort eine Frage ändern | Meldung „Dieser Entwurf ist nicht mehr offen …“, nichts geändert, Editor nur lesen |",
          "| T12 | Rundgang-App: den Rundgang aus T4 weiter bearbeiten | Kategorien und Fragen der **alten** Fassung, Speichern geht |",
          "| T13 | Neuer Rundgang „ZZ Test Builder“ (leer): Bereich, Kategorie, 2 Prüfpunkte; Plan: heutiger Wochentag, jede Woche, Startwoche diese Woche; aktivieren | Plan zeigt heute unter „Nächste Termine“; Rundgang-App zeigt ihn heute; Durchführung und Protokoll gehen; in SharePoint ist `StartMontag` ein Montag (U6) |",
          "| T14 | Neuer Rundgang als „Kopie eines Rundgangs“ von ZZ Test Objektrundgang TCC | gleiche Gliederung, Bedingungen zeigen auf die neuen Fragen, Plan leer |",
          "| T15 | „ZZ Test Builder“ archivieren (zweimal tippen), Rundgang-App neu laden; dann „Archivierte zeigen“ → Reaktivieren | verschwindet und erscheint wieder |",
          "| T16 | Am Testrundgang „Bearbeiten“ (Entwurf 3) → Übersicht → „Entwurf verwerfen“; Kopie aus T14 (nie aktiviert) „Löschen“ | Entwurf weg, aktive Fassung 2 bleibt; die Kopie ist samt Zeilen weg (SharePoint-Papierkorb) |",
          "",
          "Nach dem Test: Testrundgänge archivieren oder löschen. Ihre Durchführungen sind Testdatensätze.", "",
          "## 11. Rückweg", "",
          "- Builder-App löschen oder nicht teilen. Die Rundgang-App ist davon nicht betroffen.",
          "- Die neuen Spalten dürfen bleiben (die Rundgang-App liest sie nicht).",
          "- Eine aktivierte Fassung zurückholen: Die alte Fassung ist noch da (Bereiche mit `Fassung = alt`, `Aktiv = Nein`). Rückschalten ist im Builder nicht eingebaut; in SharePoint: Bereiche der alten Fassung auf Aktiv = Ja, die der neuen auf Nein, Kategorien der alten Fassung auf Aktiv = Ja, `RG_Rundgaenge.Fassung` auf alt.", "",
          "## 12. Regeln, die der Builder einhält (Datenvertrag)", "",
          "- Aktive Bereiche, Kategorien und Prüfpunkte werden nie geändert oder gelöscht. Geschrieben wird nur in Zeilen des Entwurfs (`RundgangID` und `Fassung` des Entwurfs, Bereiche des Entwurfs `Aktiv = Nein`).",
          "- Beim Aktivieren: zuerst alte Bereiche und Kategorien aus, dann neue Bereiche an, dann Nachlese, erst dann `RG_Rundgaenge` (Fassung, Status, Aktiv). Abbruch → „nochmal Aktivieren“ ist gefahrlos.",
          "- Die Prüfpunkte alter Fassungen bleiben aktiv: Laufende und alte Durchführungen öffnen ihre Kategorien weiter (die Rundgang-App liest Prüfpunkte nur über `KategorieID` und `Aktiv`, belegt).",
          "- Jede Schreibstelle hat die Doppelklick-Sperre oder blockiert die App während des Schreibens; Kopieren und Aktivieren prüfen das Ergebnis und melden Fehlendes.",
          "- Fehler sperren das Aktivieren: Rundgang ohne Bereich, Bereich ohne Kategorie, Kategorie ohne Prüfpunkt, leere Namen, Auswahl mit weniger als zwei oder doppelten Werten, „ab“ > „bis“, Bedingung auf eine Frage außerhalb der Kategorie, auf eine spätere Frage, auf eine bedingte Frage oder mit unpassendem Wert. Hinweise sperren nicht.",
          "", "## 13. Prüfstand", "",
          "- Maschinell (`arbeit/2026-10-30_Builder/pruefung.txt`): Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, jeder Name bekannt, jede Variable mit Startwert in App.OnStart, jede Sammlung gefüllt, jedes Steuerelement vorhanden, "
          "jedes Patch-Feld ist eine Spalte der Liste (Auswahlspalten als `{Value: …}`), Argumentanzahl der Funktionen, YAML zeichengleich zurückgelesen, Textbreiten geschätzt. " + fehler + ".",
          "- Mutationstest `werkzeuge/mutation_builder.py`: 10/10.",
          "- Unabhängige Prüfung: 8 Befunde (1 hoch, 5 mittel), alle behoben oder als UNSICHER im Testbogen – siehe `pakete/builder/PRUEFUNG_BUILDER.md`.",
          "- In Studio getestet: **nein** (Testbogen).", ""]
    open(os.path.join(AUS, "EINBAU_BUILDER.md"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("geschrieben: pakete/builder/EINBAU_BUILDER.md")


if __name__ == "__main__":
    main()
