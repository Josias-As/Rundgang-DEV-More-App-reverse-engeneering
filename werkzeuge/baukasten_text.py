"""Texte für doc_baukasten.py (Pakete 1–6 und Prüfberichte)."""

SICHERUNG = {"titel": "Sicherung", "text": [
    "Studio: oben **Speichern**. Dann make.powerapps.com → Apps → „Rundgang DEV“ → … → **Details → Versionen**: die oberste Versionsnummer notieren. "
    "Das ist der Rückweg auf Knopfdruck (Version wiederherstellen).",
]}


def pruefung_schritt(nr):
    return {"nr": nr, "titel": "App-Prüfung und Speichern", "text": [
        "Studio → **App-Prüfung → Formeln**: muss **0** sein (Barrierefreiheit/Leistung wie bisher, siehe E-07/E-08). "
        "Dann **Speichern** (noch nicht veröffentlichen) und den Test unten in der **Vorschau** machen.",
        "Bei einem Formelfehler: Fehlermeldung und Steuerelement notieren, nicht selbst umbauen, mir schicken.",
    ]}


DATEN_AKT = ("Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren** (sonst kennt die App die neue Spalte nicht "
             "und die Formeln in den nächsten Schritten zeigen Fehler).")

EINFUEGEN = ("Je Block: Steuerelement in der Strukturansicht markieren, Property oben links im Auswahlfeld wählen, in der Formelleiste "
             "**Strg+A**, dann den ganzen Block einfügen. Bis alle Blöcke dieses Pakets drin sind, können rote Fehler stehen "
             "(neue Funktionsköpfe passen erst zusammen, wenn alle Aufrufer ersetzt sind).")

PAKET_TEXT = {
    1: {
        "titel": "Foto-Modus pro Prüfpunkt (Aus / Optional / Pflicht)",
        "datei": "Foto",
        "kurz": [
            "Neue Auswahlspalte **Foto** am Prüfpunkt: Aus, Optional, Pflicht. Leere Spalte = wie bisher (FotoMoeglich Ja → Optional, sonst Aus).",
            "Bei **Pflicht** lässt sich die Kategorie erst mit mindestens einem Foto speichern („Noch offen: … (Foto)“, Sprung, rote Karte).",
            "Der Fehler „FotoMoeglich kam aus colAntworten nicht an“ ist an der Ursache behoben: Der Bearbeiten-Zweig in `scrKategorie.OnVisible` legte das Feld nicht an. Jetzt haben alle drei Zweige dieselben Felder (maschinell geprüft). Kein `LookUp(colPP; …)` mehr nötig.",
            "Grundlage für Paket 2 und 3: die Prüfregel steckt in einer Funktion (`fnFehltGrund`), die Antworten tragen schon die Felder `KommentarPflicht` und `Grenzmodus` (vorerst fest: aus / Mangel). Am Verhalten ändert das nichts.",
            "Nebenbei: Foto-Knopf blau statt rot, wenn der Punkt nicht n.i.O. ist; ✕ im Foto-Fenster liegt nicht mehr unter dem Bild; Knopftext „Foto aufnehmen / auswählen“ normal groß; in der Nur-Ansicht erscheint der Foto-Knopf nur, wenn wirklich Fotos gespeichert sind.",
        ],
        "voraus": [
            "Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt.",
            "Die App ist gespeichert, nichts halb eingefügt.",
        ],
        "schritte": [
            dict(SICHERUNG, nr="1.1"),
            {"nr": "1.2", "titel": "SharePoint-Spalte anlegen", "text": [
                "IMS+ → Liste **RG_Pruefpunkte** → **+ Spalte hinzufügen → Auswahl**:",
                "- Name: **Foto** (genau so)",
                "- Auswahlmöglichkeiten (je eine Zeile): **Aus**, **Optional**, **Pflicht**",
                "- Standardwert: **Aus** · Mehrfachauswahl: **Nein** · Werte erforderlich: **Nein**",
                "- **FotoMoeglich nicht löschen und nicht umbenennen.** Die App liest eine leere Foto-Spalte wie bisher (FotoMoeglich Ja → Optional). Neue Prüfpunkte ab jetzt nur noch über **Foto** steuern; der Standardwert „Aus“ gilt für neu angelegte Zeilen, FotoMoeglich wirkt dort nicht mehr. Empfehlung: FotoMoeglich im Listenformular ausblenden (Formular bearbeiten → Spalten), damit niemand sie noch benutzt.",
                "- **Danach prüfen (UNSICHER, wie SharePoint vorhandene Zeilen füllt):** Rasteransicht von RG_Pruefpunkte, Spalte Foto. Stehen die vorhandenen Zeilen leer → gut. Steht überall „Aus“, bei allen Zeilen mit FotoMoeglich = Ja Foto = **Optional** setzen (heute nur Id 10).",
                "- Für den Test noch **nichts** umstellen; Test-Teil A beginnt mit dem Ist-Zustand.",
                DATEN_AKT,
            ]},
            {"nr": "1.3", "titel": "App.Formulas", "text": [EINFUEGEN,
                                                           "`App` markieren, Property **Formulas**. Ganzer Inhalt wird ersetzt (neu: fnLinkAnzahl, fnFotoModus, fnFotoNeuErlaubt, fnBeantwortet, fnAusserhalb, fnKommentarNoetig, fnFehltGrund; fnFehlt mit 12 Werten; fnZahlBewertung mit 4. Wert)."]},
            {"nr": "1.4", "titel": "Kategorie öffnen: Felder der Antworten", "text": ["`scrKategorie` markieren, Property **OnVisible**."]},
            {"nr": "1.5", "titel": "Zahlenfeld", "text": []},
            {"nr": "1.6", "titel": "Karte, Kommentar und Foto-Knopf", "text": [
                "Alle Steuerelemente liegen in `galKaPruefpunkte` → `conKaKarte` (Karte) bzw. direkt in der Galerievorlage (`lblKaAbstand`)."],
             "pruefen": ["Y von `btnKaFoto` steht als Formel da, nicht als Zahl (E-05). Das Aussehen der Karten erst im Test (Vorschau) prüfen – in Studio ist colAntworten noch vom alten Stand."]},
            {"nr": "1.7", "titel": "Zähler „Noch offen“ (unsichtbare Labels)", "text": [
                "`lblKaFehlendAnzahl` und `lblKaFehlend` liegen direkt auf `scrKategorie` (unsichtbar)."]},
            {"nr": "1.8", "titel": "Speichern", "text": [
                "`conKaFuss` → `btnKaSpeichern`, Property **OnSelect**. Gegenüber vorher: Sprung zum ersten offenen Punkt mit der neuen Prüfregel, "
                "Upload-Bedingung liest `FotoModus` (statt `LookUp(colPP; …).FotoMoeglich`), „Kommentar leeren“ (08:44) über `fnKommentarNoetig` "
                "(heute gleiches Ergebnis: nur bei n.i.O. bleibt der Kommentar). Kommentare im alten Code entfallen."]},
            {"nr": "1.9", "titel": "Foto-Fenster", "text": [
                "`conKaFoto` → `conKaFotoKarte` → `lblKaFotoHinweis`, `addKaFoto`, und in `galKaFotoNeu` das Bild `imgKaFotoNeu` "
                "(Bild beginnt unter dem ✕-Knopf, damit das ✕ immer tippbar ist, egal wie die Ebenen liegen). "
                "`addKaFoto` ist nur sichtbar, wenn für den Punkt neue Fotos auch hochgeladen werden (n.i.O. oder Foto Optional/Pflicht). Ein bei n.i.O. gewähltes Foto geht weiterhin verloren, wenn der Punkt (Foto = Aus) vor dem Speichern auf i.O. zurückgestellt wird (wie bisher, gewollt)."],
             "pruefen": ["`conKaKarte.Height`, `lblKaAbstand.Y`, `imgKaFotoNeu.Height` und `btnKaFoto.Y` zeigen Formeln, keine festen Zahlen (E-05)."]},
            pruefung_schritt("1.10"),
        ],
        "test": [
            "**Nur im Test-Rundgang „ZZ Test Objektrundgang TCC“ testen** (nur dort entstehen Testdaten, Ordner TEST/, TestDatensatz = Ja). Je Rundgang und Tag gibt es eine Durchführung; ist die heutige schon abgeschlossen, einen Tag mit Testplan oder den Nachholtag nehmen.",
            "Namen im Bogen: **K1** = Kategorie, in der Prüfpunkt Id 10 (Thermometer) liegt. **P10** = Id 10. **PO** = ein anderer i.O./n.i.O.-Punkt in K1. **PX** = ein dritter i.O./n.i.O.-Punkt in K1 mit FotoMoeglich = Nein.",
            "Stammdaten werden pro Sitzung zwischengespeichert: nach jeder Änderung in RG_Pruefpunkte in Studio **Daten → RG_Pruefpunkte → Aktualisieren** und die Vorschau neu starten.",
            "Kategorien werden der Reihe nach freigeschaltet: Liegt K1 nicht als erste Kategorie, vorher die davor liegenden Kategorien speichern (oder eine neue Durchführung, in der K1 die nächste offene ist).",
            "",
            "**Teil A – Studio-Vorschau (ohne Foto-Auswahl)**",
            "",
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| A1 | Ist-Zustand (Foto-Spalte leer, P10 FotoMoeglich = Ja): Rundgang starten oder fortsetzen, K1 öffnen | P10 zeigt „📷 Foto“ (blau, ohne *), Karte höher; PX ohne Foto-Knopf |",
            "| A2 | SharePoint: P10 Foto = **Pflicht**, PO Foto = **Optional**. Vorschau neu starten, K1 öffnen | P10 „📷 Foto *“ blau; PO „📷 Foto“; PX kein Foto-Knopf |",
            "| A3 | Alle Punkte in K1 beantworten (i.O.), kein Foto | Fuß: „Noch offen (1): <Frage P10> (Foto)“, Knopf „Offene Punkte ↓“ |",
            "| A4 | „Offene Punkte ↓“ tippen | Liste springt zu P10, Karte rot umrandet |",
            "| A5 | Foto-Knopf an P10 tippen | Fenster: „Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren.“ in einer Zeile, Knopf „Foto aufnehmen / auswählen“ in normaler Größe; „Fertig“ |",
            "| A6 | PX auf n.i.O. | Kommentarfeld links, roter „📷 Foto“ rechts in einer Zeile |",
            "| A7 | PX zurück auf i.O. | Kommentarfeld und Foto-Knopf weg, Karte wieder niedrig |",
            "| A8 | PO auf n.i.O., dann i.O. | Foto-Knopf rot, dann wieder blau (Optional bleibt) |",
            "| A9 | SharePoint: P10 Foto = **Aus** (FotoMoeglich bleibt Ja), aktualisieren, Vorschau neu, K1 öffnen | P10 ohne Foto-Knopf (Foto-Spalte schlägt FotoMoeglich) |",
            "| A10 | SharePoint: P10 Foto = **Pflicht**, aktualisieren, Vorschau neu. K1 öffnen, nichts ändern, Zurück | Übersicht direkt (ohne Nachfrage); nichts gespeichert |",
            "",
            "**Teil B – Tablet (Foto-Auswahl).** Entweder Studio im Browser des Tablets öffnen und dort die Vorschau nehmen, oder die App veröffentlichen (Josias entscheidet; die veröffentlichte DEV-App sehen alle mit Zugriff).",
            "",
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| B1 | K1 öffnen, alle Punkte i.O., an P10 „📷 Foto *“ → Foto wählen | Bild erscheint im Fenster, ✕ oben rechts über dem Bild |",
            "| B2 | ✕ antippen, danach erneut ein Foto wählen, „Fertig“ | ✕ entfernt das Foto; Knopf jetzt „📷 Foto (1)“, Fuß „✓ Alles ausgefüllt“ |",
            "| B3 | PX: n.i.O. + Kommentar „test“, dann zurück auf i.O. | Kommentarfeld verschwindet |",
            "| B4 | Speichern | Meldung „Gespeichert.“, nächste Kategorie öffnet sich |",
            "| B5 | Bibliothek RG_Fotos → TEST/2026/10/<Title der Durchführung>/ | Datei `D<id>-K<kat>-P10-xxxxxxxx.jpg` |",
            "| B6 | Zurück zur Übersicht, K1 „Bearbeiten“ | P10 „📷 Foto (1)“ ohne *; Speicher-Knopf zeigt „Speichern“ bzw. „Speichern & weiter“, nicht „Offene Punkte ↓“ (nicht tippen) |",
            "| B6a | PX auf n.i.O. tippen | Kommentarfeld ist **leer** (beim Speichern geleert, Verhalten 08:44); dann PX zurück auf i.O. und Zurück („Verwerfen? Erneut tippen“) |",
            "| B7 | Nur wenn der Testrundgang ohnehin abgeschlossen werden soll: vorher in einer Kategorie einen Punkt **n.i.O. + Kommentar, ohne Foto** speichern, dann alle Kategorien speichern und abschließen (legt Mängel in RG_Maengel und ein PDF in RG_Protokolle an) | Nach dem Abschluss „Ansehen“: P10 „📷 Foto (1)“, Fenster zeigt „Gespeicherte Fotos (nur Ansicht).“; der n.i.O.-Punkt ohne Foto hat keinen Foto-Knopf, Kommentar sichtbar |",
            "",
            "Aufräumen: Testdaten wie gewohnt in den Papierkorb (nur TestDatensatz = Ja). P10 Foto auf den gewünschten Wert lassen.",
        ],
        "rueck": [
            "- **Am schnellsten:** make.powerapps.com → Details → Versionen → notierte Version **Wiederherstellen**.",
            "- **Einzeln:** die Vorher-Blöcke aus dem Anhang einfügen, zuerst alle Steuerelemente, **App.Formulas zuletzt**. Danach App-Prüfung = 0.",
            "- Die Spalte **Foto** kann stehen bleiben (die alte App liest sie nicht). Gespeicherte Ergebnisse sind nicht betroffen (das JSON hat kein neues Feld).",
        ],
    },
    2: {
        "titel": "Pflicht-Kommentar auch bei i.O. (pro Prüfpunkt)",
        "datei": "Kommentar",
        "kurz": [
            "Neue Ja/Nein-Spalte **KommentarPflicht** am Prüfpunkt (Standard Nein).",
            "Bei Ja verlangt die App einen Kommentar, sobald der Punkt beantwortet ist – auch bei i.O. (bei n.i.O. wie bisher immer).",
            "„Kommentar leeren beim Speichern“ (08:44) berücksichtigt das automatisch: bei KommentarPflicht bleibt der Kommentar auch bei i.O. erhalten.",
            "Hinweistext im Feld: „Kommentar (Pflicht)“ bei i.O., „Kommentar zum Mangel (Pflicht)“ bei n.i.O.",
            "Protokoll: Kommentar bei i.O. grau, bei n.i.O. rot wie bisher. Mängel unverändert (nur n.i.O.).",
        ],
        "voraus": ["Paket 1 ist eingefügt, getestet und gespeichert.", "Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt."],
        "schritte": [
            dict(SICHERUNG, nr="2.1"),
            {"nr": "2.2", "titel": "SharePoint-Spalte anlegen", "text": [
                "RG_Pruefpunkte → **+ Spalte hinzufügen → Ja/Nein**: Name **KommentarPflicht**, Standardwert **Nein**.",
                "Für den Test: siehe Vorbereitung im Testbogen (zwei Punkte PK und PN).", DATEN_AKT]},
            {"nr": "2.3", "titel": "App.Formulas", "text": [EINFUEGEN, "Nur `fnKommentarNoetig` ändert sich; der Block ist trotzdem die ganze Property."]},
            {"nr": "2.4", "titel": "Kategorie öffnen", "text": ["`scrKategorie.OnVisible`: `KommentarPflicht` kommt jetzt aus der Spalte."]},
            {"nr": "2.5", "titel": "Kommentarfeld", "text": ["`conKaKarte` → `txtKaKommentar`."]},
            {"nr": "2.6", "titel": "Protokoll", "text": ["`scrProtokoll` → `conPrInhalt` → `htmProtokoll`, Property **HtmlText**."]},
            pruefung_schritt("2.7"),
        ],
        "test": [
            "Vorbereitung in RG_Pruefpunkte, danach Daten aktualisieren und Vorschau neu starten: P10 Foto = **Optional** (sonst blockiert die Foto-Pflicht das Speichern in der Vorschau). **K2** = die Kategorie nach K1. Dort: **PK** (i.O./n.i.O., Pflicht = Ja) KommentarPflicht = **Ja**; **PN** (i.O./n.i.O., Pflicht auf **Nein** stellen) KommentarPflicht = **Ja**; **PM** = ein anderer i.O./n.i.O.-Punkt ohne KommentarPflicht.",
            "",
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T2.1 | Test-Rundgang öffnen (Durchführung des Tages; ist sie abgeschlossen: Tag mit Testplan oder Nachholtag). K1 speichern bzw. „Bearbeiten“ und speichern | K2 öffnet sich automatisch (oder über die Übersicht öffnen) |",
            "| T2.2 | PK auf i.O. | Kommentarfeld „Kommentar (Pflicht)“, rot umrandet; Fuß nennt „<PK> (Kommentar)“ |",
            "| T2.3 | PN unbeantwortet lassen | PN steht nicht in „Noch offen“ |",
            "| T2.4 | PK Kommentar „sauber“ | PK nicht mehr offen |",
            "| T2.5 | PK auf n.i.O., Kommentar kurz leeren | leeres Feld zeigt „Kommentar zum Mangel (Pflicht)“; dann „sauber“ wieder eintragen |",
            "| T2.6 | PK zurück auf i.O. | „sauber“ steht noch, PK nicht offen |",
            "| T2.7 | PM: n.i.O. + Kommentar „weg“, dann i.O. | Kommentarfeld von PM verschwindet |",
            "| T2.8 | Übrige Punkte ausfüllen, Speichern | „Gespeichert.“, die nächste offene Kategorie öffnet sich (falls es eine gibt) |",
            "| T2.9 | Zurück zur Übersicht, K2 „Bearbeiten“ | PK i.O., Kommentarfeld mit „sauber“ sichtbar |",
            "| T2.9a | PM auf n.i.O. tippen | Kommentarfeld von PM ist **leer** (beim Speichern geleert); PM zurück auf i.O., Zurück („Verwerfen? Erneut tippen“) |",
            "| T2.10 | Nur mit Abschluss (siehe Paket 1, B7): Protokoll | „sauber“ grau kursiv beim i.O.-Punkt; kein Mangel für PK |",
            "",
            "Aufräumen: PN wieder Pflicht = Ja (falls vorher so), Testdaten in den Papierkorb (nur TestDatensatz = Ja).",
        ],
        "rueck": [
            "- Version wiederherstellen oder die Vorher-Blöcke einfügen (App.Formulas zuletzt).",
            "- Die Spalte darf bleiben. Gespeicherte i.O.-Kommentare bleiben im JSON und erscheinen nach dem Rückweg im Protokoll rot (alte Darstellung). **Achtung:** Wird eine solche Kategorie nach dem Rückweg erneut gespeichert, löscht „Kommentar leeren“ die i.O.-Kommentare (die Kommentarpflicht ist dann ja weg).",
        ],
    },
    3: {
        "titel": "Zahlengrenzen pro Prüfpunkt: Mangel, Warnen oder Sperren",
        "datei": "Grenzen",
        "kurz": [
            "Neue Auswahlspalte **Grenzmodus** am Prüfpunkt: Mangel (Standard = wie heute), Warnen, Sperren.",
            "**Mangel:** Wert außerhalb Min/Max → n.i.O., Kommentar Pflicht, Mangel beim Abschluss (unverändert).",
            "**Warnen:** Wert außerhalb → orange „außerhalb, bitte begründen“, Kommentar Pflicht, Bewertung i.O., **kein** Mangel. Gespeichert mit Kennzeichen `Warnung`: Protokoll zeigt i.O. orange mit „(außerhalb Soll, begründet)“, die Nur-Ansicht „außerhalb, begründet“.",
            "**Sperren:** harte Plausibilitätsgrenze (Beschriftung „zulässig ab … bis …“). Wert außerhalb → rot „unzulässig, bitte prüfen“, Speichern erst mit einem Wert im Bereich. **Nur für Grenzen, die ein echter Messwert nie überschreitet** (Tippfehler-Schutz), sonst lässt sich der Rundgang nicht abschließen. Ist Min > Max eingestellt, gilt der Punkt als „Mangel“ statt zu sperren.",
        ],
        "voraus": ["Paket 1 und 2 sind eingefügt und getestet.", "Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt."],
        "schritte": [
            dict(SICHERUNG, nr="3.1"),
            {"nr": "3.2", "titel": "SharePoint-Spalte anlegen", "text": [
                "RG_Pruefpunkte → **+ Spalte hinzufügen → Auswahl**: Name **Grenzmodus**, Auswahlmöglichkeiten **Mangel**, **Warnen**, **Sperren**, Standardwert **Mangel**, keine Mehrfachauswahl.",
                "Regeln für die Pflege: **Sperren** nur mit Grenzen, die ein echter Wert nie überschreitet (z. B. Temperatur −50 bis 150); Sollwerte immer mit Mangel oder Warnen. Min nie größer als Max. Grenzmodus und Min/Max nicht umstellen, solange Rundgänge des Tages laufen (beim Öffnen wird neu bewertet).",
                "Für den Test in K1 drei neue Prüfpunkte (ZAHL, Pflicht = Ja, Aktiv = Ja, Einheit °C, Min 6, Max 16, Reihenfolge hinter den vorhandenen): **Z1** „ZZ Test Temp Mangel“ (Grenzmodus Mangel), **Z2** „ZZ Test Temp Warnen“ (Warnen), **Z3** „ZZ Test Temp Sperren“ (Sperren).", DATEN_AKT]},
            {"nr": "3.3", "titel": "App.Formulas", "text": [EINFUEGEN, "Neu: Farben clrWarnung/clrWarnungHell, fnGrenzmodus; geändert: fnZahlBewertung, fnKommentarNoetig, fnFehltGrund."]},
            {"nr": "3.4", "titel": "Kategorie öffnen", "text": ["`scrKategorie.OnVisible`: Grenzmodus aus der Spalte, Bewertung gespeicherter Zahlen mit dem Grenzmodus, neues Feld `Warnung` (in der Nur-Ansicht aus dem gespeicherten JSON)."]},
            {"nr": "3.5", "titel": "Anzeige am Zahlenfeld", "text": ["`conKaKarte` → `lblKaZahlInfo`, `txtKaZahl`."]},
            {"nr": "3.6", "titel": "Speichern: Kennzeichen Warnung im JSON", "text": ["`btnKaSpeichern.OnSelect`: vor dem JSON wird `Warnung` für aktive Punkte gesetzt, das JSON nimmt das Feld mit."]},
            {"nr": "3.7", "titel": "Protokoll", "text": ["`htmProtokoll.HtmlText`: i.O. mit Warnung orange und „(außerhalb Soll, begründet)“."]},
            pruefung_schritt("3.8"),
        ],
        "test": [
            "Vorschau neu starten (Stammdaten). P10 Foto = Optional (siehe Paket 2). Neue Durchführung oder eine, in der K1 offen ist.",
            "",
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T3.1 | K1 öffnen, Z1 = 18,5 | wie heute: rot „Soll ab 6 bis 16 · außerhalb des Sollbereichs“, Karte rot, Kommentarfeld |",
            "| T3.2 | Z1 Kommentar „zu warm“ | Z1 nicht mehr offen |",
            "| T3.3 | Z2 = 18,5 | orange „außerhalb, bitte begründen“, Rahmen orange, Kommentarfeld „Kommentar (Pflicht)“, Karte **nicht** rot |",
            "| T3.4 | Z2 Kommentar „Fühler defekt“ | Z2 nicht mehr offen |",
            "| T3.5 | Z3 = 18,5 | rot „zulässig ab 6 bis 16 · unzulässig, bitte prüfen“; Fuß „<Z3> (unzulässiger Wert)“ |",
            "| T3.6 | Übrige Punkte ausfüllen, „Offene Punkte ↓“ | Liste springt zu Z3 |",
            "| T3.7 | Z3 = 16,01 | weiter unzulässig (Dezimalzahl über Max) |",
            "| T3.8 | Z3 = 6 | im Bereich, Hinweis weg |",
            "| T3.9 | Speichern | „Gespeichert.“ |",
            "| T3.10 | Zurück, K1 „Bearbeiten“ | Z1 n.i.O. + „zu warm“; Z2 orange „außerhalb, bitte begründen“ + „Fühler defekt“; Z3 = 6 |",
            "| T3.11 | Zurück (Verwerfen). SharePoint: Z3 Min = 16, Max = 6, Daten aktualisieren, Vorschau neu, K1 „Bearbeiten“, Z3 = 12 | Z3 wird n.i.O. mit Kommentarpflicht statt gesperrt (Schutz bei Min > Max), Beschriftung „Soll“. **Nicht speichern:** Zurück („Verwerfen? Erneut tippen“). Danach Z3 wieder Min 6, Max 16 |",
            "| T3.12 | Nur mit Abschluss (siehe Paket 1, B7): RG_Maengel und Protokoll | Mangel für Z1, keiner für Z2; im Protokoll Z2 „i.O.“ orange mit „(außerhalb Soll, begründet)“ und grauem Kommentar; „Ansehen“: Z2 „außerhalb, begründet“ (aus dem gespeicherten Kennzeichen) |",
            "",
            "Aufräumen: Z1–Z3 auf Aktiv = Nein setzen (sonst bleiben sie Pflichtpunkte in K1), Testdaten in den Papierkorb.",
        ],
        "rueck": ["- Version wiederherstellen oder Vorher-Blöcke einfügen (App.Formulas zuletzt). Spalte darf bleiben.",
                  "- Gespeicherte Warnen-Werte (i.O. außerhalb) bleiben im JSON. Öffnet die alte App eine solche Kategorie zum Bearbeiten, bewertet sie den Wert neu als n.i.O. (Kommentar ist da). Abgeschlossene Rundgänge sind nicht betroffen."],
    },
    4: {
        "titel": "Bedingte Fragen",
        "datei": "Bedingung",
        "kurz": [
            "Zwei neue Spalten am Prüfpunkt B: **BedingungPunkt** (Id von Punkt A, gleiche Kategorie) und **BedingungWert** (z. B. NIO, IO, ein Auswahlwert, oder * = irgendeine Antwort).",
            "B erscheint und wird verlangt nur, wenn A den Wert hat. Sonst ist B unsichtbar, zählt nicht als offen und bekommt keine Fotos hochgeladen.",
            "Beim Speichern schreibt die App ausgeblendete Punkte leer (Werte, Kommentar, Foto-Links) und mit `Ausgeblendet` ins JSON – keine Mängel, im Protokoll und in der Nur-Ansicht nicht sichtbar. Die Eingaben auf dem Bildschirm bleiben unangetastet, bis das Speichern geklappt hat (das JSON entsteht aus einer Kopie). Neue Fotos eines ausgeblendeten Punkts werden nicht hochgeladen.",
            "Fehlkonfiguration fällt sicher aus: A fehlt, A ist selbst bedingt (Kette), BedingungWert ist leer oder passt nicht zu A (z. B. Tippfehler, Wert, den es in A nicht gibt) → B wird immer gezeigt. Schreibweisen „i.O.“/„n.i.O.“, Groß-/Kleinschreibung und Leerzeichen sind egal.",
            "Zähler (x von y ausgefüllt, Balken, n.i.O.-Zahl, Noch offen, Sprung) zählen nur sichtbare Punkte.",
        ],
        "voraus": ["Pakete 1–3 eingefügt und getestet.", "Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt."],
        "schritte": [
            dict(SICHERUNG, nr="4.1"),
            {"nr": "4.2", "titel": "SharePoint-Spalten anlegen", "text": [
                "RG_Pruefpunkte:",
                "- **BedingungPunkt** – Zahl, 0 Dezimalstellen, Standardwert **0** (0 = keine Bedingung)",
                "- **BedingungWert** – Einzelne Textzeile, Standardwert leer",
                "Gültige Bedingungswerte: bei A = i.O./n.i.O. oder Zahl: **IO** oder **NIO**; bei A = Auswahl (ab Paket 5 auch Mehrfachauswahl): einer der Auswahlwerte von A; bei jedem Typ: `*` (irgendeine Antwort). Bei Zahl-Punkten mit Grenzmodus Warnen ist ein Wert außerhalb „IO“, mit Sperren nie „NIO“ – Bedingungen auf NIO nur bei Grenzmodus Mangel.",
                "Für den Test in K1: **A** = PX (i.O./n.i.O., Pflicht = Ja). Neuer Prüfpunkt **B** „ZZ Test Folgefrage Ursache“: TEXT, Pflicht = Ja, Aktiv = Ja, Foto = Optional, RgReihenfolge direkt hinter A, BedingungPunkt = Id von A, BedingungWert = **NIO**.",
                DATEN_AKT]},
            {"nr": "4.3", "titel": "App.Formulas", "text": [EINFUEGEN, "Neu: fnBedPasst, fnSichtbar."]},
            {"nr": "4.4", "titel": "Kategorie öffnen", "text": ["`scrKategorie.OnVisible`: Felder BedID, BedWert, Ausgeblendet; Start-Sprung auf den ersten sichtbaren Punkt."]},
            {"nr": "4.5", "titel": "Galerie und Zähler", "text": ["Pfade: `galKaPruefpunkte` (Items) und die unsichtbaren `lblKaFehlendAnzahl`, `lblKaFehlend` liegen direkt auf `scrKategorie`; `lblKaUnter` in `conKaKopf`; `conKaBalkenWert` in `conKaBalken`; `lblKaStand` in `conKaFuss`."]},
            {"nr": "4.6", "titel": "Speichern", "text": ["`btnKaSpeichern.OnSelect`: ausgeblendete Punkte vor dem Foto-Upload bestimmen (`colVersteckt`); Upload, Anhängen von Links und „übernommen“ nur für sichtbare; JSON und AnzahlNIO aus einer Kopie (`colSpeichern`), in der ausgeblendete leer und markiert sind."]},
            {"nr": "4.7", "titel": "Protokoll", "text": ["`htmProtokoll.HtmlText`: ausgeblendete Zeilen weglassen."]},
            pruefung_schritt("4.8"),
        ],
        "test": [
            "Daten aktualisieren, Vorschau neu starten. K1 öffnen (neu oder „Bearbeiten“); A muss dabei i.O. oder leer sein. Textfelder übernehmen die Eingabe erst beim Verlassen des Felds (woanders hintippen). „Übrige Punkte ausfüllen“ heißt: alle Pflichtpunkte von K1, auch Z1–Z3 aus Paket 3, falls noch aktiv.",
            "",
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T4.1 | K1 öffnen | B ist nicht zu sehen; Kopf „… von N ausgefüllt“ zählt B nicht |",
            "| T4.2 | A auf n.i.O. | B erscheint direkt unter A; Fuß nennt A (Kommentar) und B |",
            "| T4.3 | B Text „Leck“, an B ein Foto-Knopf (Optional) sichtbar | B nicht mehr offen |",
            "| T4.4 | A zurück auf i.O. | B verschwindet, Liste rückt nach; Fuß ohne B |",
            "| T4.5 | A wieder n.i.O. | B kommt mit „Leck“ zurück (noch nicht gespeichert, also nicht verloren) |",
            "| T4.6 | A auf i.O., übrige Punkte ausfüllen, Speichern | „Gespeichert.“ (B war ausgeblendet) |",
            "| T4.7 | Zurück, K1 „Bearbeiten“, A auf n.i.O. | B erscheint **leer** (beim Speichern geleert) |",
            "| T4.8 | A Kommentar „tropft“, B „Leck“, Speichern | „Gespeichert.“ |",
            "| T4.9 | SharePoint: BedingungWert von B = **n.i.O.**; Vorschau neu starten, K1 „Bearbeiten“, A auf i.O. | B verschwindet (Schreibweise egal) |",
            "| T4.10 | BedingungWert = **Rot**; aktualisieren, Vorschau neu, K1 „Bearbeiten“, A auf i.O. | B bleibt sichtbar (ungültiger Wert → sicherer Ausfall). Zurück („Verwerfen?“). Danach BedingungWert wieder **NIO** |",
            "| T4.11 | Nur mit Abschluss (siehe Paket 1, B7), Stand T4.8: RG_Maengel, Protokoll, „Ansehen“ | Mangel nur für A; Protokoll und Nur-Ansicht zeigen B mit „Leck“ |",
            "| T4.12 | Zweite Durchführung (anderer Tag mit Testplan oder Nachholtag ≥ 1; am selben Tag gibt es je Rundgang nur eine): K1 mit A = i.O. speichern, abschließen | Protokoll und Nur-Ansicht ohne B; kein Mangel |",
            "| T4.13 | Eine vor Paket 4 gespeicherte Kategorie „Ansehen“ | unverändert (JSON ohne `Ausgeblendet` gilt als sichtbar) |",
        ],
        "rueck": [
            "- Version wiederherstellen oder Vorher-Blöcke einfügen (App.Formulas zuletzt).",
            "- JSON mit `Ausgeblendet` stört die alte App nicht (Feld wird ignoriert); ausgeblendete Punkte stehen dann als leere Zeilen im Protokoll.",
            "- Spalten dürfen bleiben. Vor dem Rückweg alle bedingten Punkte (B) auf **Aktiv = Nein** setzen – die alte App kennt keine Bedingung und würde sie immer als Pflicht zeigen.",
        ],
    },
    5: {
        "titel": "Neue Typen: Mehrfachauswahl, Datum, Datum + Uhrzeit",
        "datei": "Typen",
        "kurz": [
            "Eingabetyp bekommt drei neue Werte: **MEHRFACH**, **DATUM**, **DATUMZEIT**.",
            "MEHRFACH: Kombinationsfeld mit den Auswahlwerten (wie AUSWAHL, Trennzeichen „;“), mehrere wählbar, gespeichert als „Wert1; Wert2“.",
            "DATUM: Datumsauswahl, gespeichert als „TT.MM.JJJJ“. DATUMZEIT: dazu Stunde und Minute, gespeichert als „TT.MM.JJJJ hh:mm“.",
            "Pflicht wie bei anderen Typen; „nur Datum ohne Uhrzeit“ zählt bei DATUMZEIT immer als offen („(Uhrzeit)“).",
            "Protokoll und Mängel zeigen den Text so, wie er gespeichert ist – dort ändert sich nichts. Bedingungen (Paket 4) können auf einen Wert der Mehrfachauswahl zeigen.",
        ],
        "voraus": ["Pakete 1–4 eingefügt und getestet.", "Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt."],
        "schritte": [
            dict(SICHERUNG, nr="5.1"),
            {"nr": "5.2", "titel": "SharePoint: Auswahlwerte ergänzen", "text": [
                "RG_Pruefpunkte → Spalte **Eingabetyp** → Spalteneinstellungen → Bearbeiten → Auswahlmöglichkeiten **ergänzen** (nichts umbenennen oder löschen): **MEHRFACH**, **DATUM**, **DATUMZEIT**. Standardwert unverändert lassen.",
                "Pflegeregel: den Typ eines schon benutzten Prüfpunkts nicht ändern (alte Antworten passen nicht zum neuen Typ), sondern einen neuen Punkt anlegen und den alten deaktivieren.",
                "Für den Test in K1 neue Prüfpunkte, alle Pflicht = Ja, Aktiv = Ja, Foto = Aus, RgReihenfolge hinter den vorhandenen in dieser Folge: **M** „ZZ Test Mängelarten“ MEHRFACH mit Auswahlwerte `Riss;Leck;Korrosion`, **F** „ZZ Test Folge Leck“ (TEXT) mit BedingungPunkt = Id von M, BedingungWert = **Leck**, **D** „ZZ Test Datum letzte Wartung“ DATUM, **DZ** „ZZ Test Ablesezeit“ DATUMZEIT.",
                "Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren** (damit die App die neuen Auswahlwerte kennt)."]},
            {"nr": "5.3", "titel": "App.Formulas", "text": [EINFUEGEN, "fnFehltGrund kennt die neuen Typen, neu: fnDatumText."]},
            {"nr": "5.4", "titel": "Datum, Uhrzeit und Leeren-Knopf (YAML)", "text": [
                "In der Strukturansicht in `conKaKarte` das Steuerelement `txtKaText` markieren, dann den YAML-Block mit **Strg+V** einfügen "
                "(landet in derselben Karte). **Alle vier Blöcke zusammen** kopieren und einfügen (sie verweisen aufeinander; einzeln eingefügt stehen kurz rote Fehler)."],
             "yaml": ["dpKaDatum", "ddKaStunde", "ddKaMinute", "btnKaDatumLeeren"],
             "pruefen": ["Alle vier liegen in `conKaKarte` (Strukturansicht).",
                         "Y steht als Formel `54 + If(ThisItem.Hinweis <> \"\"; 24; 0)` da, nicht als Zahl (E-05) – sonst per Formelleiste setzen.",
                         "Die Namen sind genau `dpKaDatum`, `ddKaStunde`, `ddKaMinute`, `btnKaDatumLeeren` (Studio hängt bei Doppelungen „_1“ an)."]},
            {"nr": "5.5", "titel": "Mehrfachauswahl (Kombinationsfeld über das Menü)", "text": [
                "Für das klassische Kombinationsfeld kenne ich die Steuerelement-Version in dieser Umgebung nicht sicher, deshalb ohne YAML:",
                "1. Strukturansicht: `conKaKarte` markieren.",
                "2. **Einfügen → Klassisch → Kombinationsfeld** (nicht das moderne Kombinationsfeld unter „Eingabe“). Es muss **in** `conKaKarte` landen.",
                "3. Umbenennen in **cboKaMehrfach**.",
                "4. Die folgenden Properties setzen (je ganze Property ersetzen):"],
             "einzeln": ["cboKaMehrfach"],
             "pruefen": ["`cboKaMehrfach` liegt in `conKaKarte`.", "Y ist eine Formel (E-05)."]},
            pruefung_schritt("5.6"),
        ],
        "test": [
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T5.1 | K1 öffnen | M: Kombinationsfeld „Auswählen (mehrere möglich)“; D: Datumsauswahl „Datum wählen“; DZ: Datum + zwei Listen (Stunde, Minute, noch gesperrt); F nicht sichtbar. Andere Typen unverändert |",
            "| T5.2 | Nichts davon ausfüllen | Fuß zählt M, D, DZ als offen |",
            "| T5.3 | M: Korrosion, dann Riss wählen | M erledigt (gespeichert wird „Riss; Korrosion“ in der Reihenfolge der Auswahlwerte) |",
            "| T5.4 | M zusätzlich Leck | F erscheint (Bedingung auf einen Wert der Mehrfachauswahl) |",
            "| T5.5 | F „x“, D Datum wählen | erledigt; rechts neben D ein „✕“ |",
            "| T5.6 | D „✕“ | Datum wieder leer, D offen; dann Datum erneut wählen |",
            "| T5.7 | DZ: nur Datum | Stunde/Minute werden wählbar; Fuß „… (Uhrzeit)“ |",
            "| T5.8 | DZ Stunde 07, Minute 05 | erledigt |",
            "| T5.8a | DZ „✕“ | Datum, Stunde und Minute leer, Stunde/Minute wieder gesperrt; dann Datum, 07, 05 erneut wählen |",
            "| T5.8b | M: alle Werte abwählen | M offen, F verschwindet; dann Riss, Leck, Korrosion wieder wählen, F erscheint mit „x“ |",
            "| T5.8c | DZ: Stunde leeren (leerer Eintrag), Kategorie nicht speichern, Zurück („Verwerfen?“), andere Kategorie öffnen, dann K1 erneut | in keiner Karte steht eine Stunde/Minute, die nicht gespeichert ist (UNSICHER, Restwerte in Galerie-Zeilen; falls doch: Befund melden, dann Stunde/Minute als eigene Felder führen) |",
            "| T5.9 | Übrige Pflichtpunkte von K1 ausfüllen, Speichern | „Gespeichert.“, die nächste offene Kategorie öffnet sich |",
            "| T5.10 | Zurück, K1 „Bearbeiten“ | M zeigt Riss, Leck, Korrosion; D und DZ („TT.MM.JJJJ 07:05“) stehen da; F mit „x“. „Zurück“ fragt **nicht** „Verwerfen?“ (UNSICHER: falls doch, Befund melden – Auswahlfelder lösen dann OnChange beim Laden aus) |",
            "| T5.11 | DZ Datum ändern, ohne zu speichern Zurück („Verwerfen? Erneut tippen“), K1 erneut öffnen | alter gespeicherter Wert steht wieder da (keine Restwerte) |",
            "| T5.12 | Nur mit Abschluss (siehe Paket 1, B7): Protokoll, „Ansehen“ | „Riss; Leck; Korrosion“, „TT.MM.JJJJ“, „TT.MM.JJJJ 07:05“ in der Wertspalte; keine Mängel durch diese Punkte; Nur-Ansicht zeigt die Werte inkl. Stunde/Minute, nicht änderbar, kein „✕“ |",
            "",
            "Aufräumen: M, F, D, DZ auf Aktiv = Nein (sonst bleiben sie Pflichtpunkte in K1), Testdaten in den Papierkorb.",
        ],
        "rueck": [
            "- Version wiederherstellen, oder: die fünf neuen Steuerelemente (`cboKaMehrfach`, `dpKaDatum`, `ddKaStunde`, `ddKaMinute`, `btnKaDatumLeeren`) löschen und App.Formulas aus dem Anhang einfügen.",
            "- Prüfpunkte mit den neuen Typen vorher deaktivieren (die alte App kennt die Typen nicht und würde sie nicht anzeigen, aber Pflicht-Prüfung würde sie nicht verlangen).",
        ],
    },
    6: {
        "titel": "Hinweis mit Beispielbild",
        "datei": "Beispielbild",
        "kurz": [
            "Neue Bildbibliothek **RG_Hinweisbilder** und neue Zahlspalte **HinweisBildID** am Prüfpunkt (Id des Bilds in der Bibliothek, 0 = keins).",
            "Hat ein Punkt ein Bild, steht rechts oben in der Karte ein kleiner Knopf „Bild“ (64 px, die Frage wird nur 80 px schmaler). Tippen öffnet ein Fenster mit dem Bild in voller Breite.",
            "Statt „in der Karte aufklappen“ (Übergabe) ein Fenster: größeres Bild auf dem Tablet, keine wechselnde Kartenhöhe (Falle E-05). Bitte bestätigen.",
            "Das Bild wird erst beim Öffnen geladen (eine Abfrage), nicht für jede Karte.",
            "Vorab-Test (Schritt 6.3) klärt, ob die Vorschaubilder der Bibliothek in der App ankommen; sonst Abbruch ohne Änderung.",
        ],
        "voraus": ["Pakete 1–5 eingefügt und getestet.", "Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt."],
        "schritte": [
            dict(SICHERUNG, nr="6.1"),
            {"nr": "6.2", "titel": "SharePoint: Bibliothek und Spalte", "text": [
                "IMS+ → Neu → **Dokumentbibliothek** „**RG_Hinweisbilder**“. Rechte wie die anderen RG-Bibliotheken (alle lesen). Ein Testbild hochladen (JPG/PNG), dessen **ID** notieren (Ansicht → Spalte ID einblenden).",
                "RG_Pruefpunkte → **+ Spalte → Zahl**: **HinweisBildID**, 0 Dezimalstellen, Standardwert **0**.",
                "Für den Test: Prüfpunkt Id 10 → HinweisBildID = ID des Testbilds. Nach dem Hochladen ein paar Minuten warten (SharePoint erzeugt die Vorschaubilder verzögert).",
                "Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren**."]},
            {"nr": "6.3", "titel": "Datenquelle und Vorab-Test", "text": [
                "Studio → **Daten → Daten hinzufügen → SharePoint → IMS+ → RG_Hinweisbilder** (die bestehende SharePoint-Verbindung wird benutzt, kein neuer Berechtigungsdialog erwartet; falls doch einer kommt: abbrechen und mir Bescheid geben). Danach `RG_Pruefpunkte` aktualisieren.",
                "Vorab-Test: auf `scrKategorie` vorübergehend ein Bild-Steuerelement einfügen, Image = `LookUp(RG_Hinweisbilder; ID = <Test-ID>).Thumbnail.Large`. Zeigt es das Bild → weiter. Zeigt es nichts → **Abbruch**, Bild-Steuerelement löschen, mir Bescheid geben (Ausweg: Bildspalte in RG_Pruefpunkte). Teststeuerelement danach löschen."]},
            {"nr": "6.4", "titel": "Kategorie öffnen", "text": ["`scrKategorie.OnVisible`: Feld BildID, Fenster beim Öffnen zu."]},
            {"nr": "6.5", "titel": "Knopf in der Karte", "text": [
                "`lblKaFrage.Width` ersetzen. Dann in `conKaKarte` `txtKaText` markieren und den YAML-Block einfügen."],
             "yaml": ["btnKaBild"],
             "pruefen": ["`btnKaBild` liegt in `conKaKarte`, X = Parent.Width - 84, Y = 10, Höhe 34 (endet über `lblKaHinweis` bei Y 46)."]},
            {"nr": "6.6", "titel": "Bildfenster", "text": [
                "Den Bildschirm `scrKategorie` in der Strukturansicht markieren und den YAML-Block einfügen. `conKaBild` muss in der Strukturansicht **ganz oben** stehen (vor `conKaFoto` und `conKaLaden`), sonst per Rechtsklick → **Nach vorne bringen**."],
             "yaml": ["conKaBild"],
             "pruefen": ["Beim Einfügen eines Containers bleiben die Kinder in ihm (Strukturansicht prüfen).",
                         "Formeln statt Zahlen (E-05): `conKaBild.Height` = Parent.Height, `btnKaBildSperre.Height` = Parent.Height, `conKaBildKarte.Height` = Min(Parent.Height - 32; 900), `conKaBildKarte.Y` = (Parent.Height - Self.Height) / 2, `imgKaBild.Height` = Parent.Height - 84 - 96, `btnKaBildSchliessen.Y` = Parent.Height - 76 – sonst per Formelleiste setzen."]},
            pruefung_schritt("6.7"),
        ],
        "test": [
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T6.1 | K1 öffnen | Karte von P10: rechts oben „Bild“, Fragetext endet davor (lange Frage: ggf. abgeschnitten wie bisher, nur 80 px früher) |",
            "| T6.2 | „Bild“ tippen | Fenster mit Titel „Beispiel – …“ und Bild; Rest der App nicht tippbar |",
            "| T6.3 | „Schließen“ | Fenster zu |",
            "| T6.4 | Punkt ohne Bild | kein Knopf |",
            "| T6.5 | Nur-Ansicht nach Abschluss | Knopf vorhanden, Bild lässt sich ansehen (Bild aus den heutigen Stammdaten) |",
            "| T6.6 | HinweisBildID auf eine nicht vorhandene Id, aktualisieren, Vorschau neu | Fenster öffnet, Bildfläche leer, „Schließen“ geht |",
            "| T6.7 | Am Tablet (veröffentlicht oder Studio im Tablet-Browser), hochkant und quer | Bild erscheint; das Fenster deckt den ganzen Bildschirm ab (Karten darunter nicht tippbar), „Schließen“ ist sichtbar |",
            "",
            "Hinweis: Das Zurücksetzen des Fensters in OnVisible ist eine Absicherung; über die Oberfläche lässt sich die Kategorie bei offenem Fenster nicht verlassen (Hintergrund gesperrt).",
        ],
        "rueck": ["- Version wiederherstellen, oder `conKaBild` und `btnKaBild` löschen und die Vorher-Blöcke einfügen. Spalte und Bibliothek dürfen bleiben."],
    },
}


# --------------------------------------------------------------------------- Prüfberichte

ORTE = ["scrKategorie.OnVisible", "fnFehlt / fnFehltGrund", "btnKaSpeichern: Prüfung und Sprung", "JSON-Aufbau (varAntwortJSON)",
        "Mängel bei Abschluss (btnRuAbschluss)", "htmProtokoll", "Foto-Upload (btnKaSpeichern F1/F2)", "Lesemodus nach Abschluss",
        "Nachlese-Vergleich (varNachlese.Antworten = varAntwortJSON)"]

PFLICHT_SZENARIEN = ["neuer Punkt ohne Daten", "alter gespeicherter Punkt (JSON ohne neues Feld)", "inaktiver Punkt",
                     "Rundgang abgeschlossen (Nur-Lesen)", "Wechsel n.i.O. → i.O. → n.i.O.", "Kategorie zweimal speichern",
                     "Abbruch mitten im Speichern", "Netzfehler", "zwei Prüfer gleichzeitig"]

FALLEN_ALLG = [
    "Navigate in OnVisible: nicht verwendet (Weiterspringen bleibt bei `tmrWeiter`).",
    "`Concat(Filter(… As x; …); x.Feld)`: nicht verwendet. Wo ein Alias in Concat nötig ist, steht `As` am ersten Argument von Concat selbst (`Concat(Filter(…) As z; z.Frage …)`), das ist gültig.",
    "Flow-Name in Studio `aRG_Foto_hochladen`: unverändert übernommen, nicht umbenannt.",
    "Keine Kommentare in den Blöcken (auch die alten `//`-Zeilen in ersetzten Properties entfallen).",
]

PRUEF_TEXT = {
    1: {
        "b": [
            "- `Foto` ist eine Auswahlspalte: gelesen nur als `p.Foto.Value` / `pp.Foto.Value` (maschinell geprüft: kein Zugriff ohne `.Value`).",
            "- `FotoMoeglich` (Ja/Nein) nur mit `Coalesce(…; false)` (maschinell geprüft).",
            "- Leere Auswahl liefert Blank: `fnFotoModus` vergleicht nur mit den drei Werten, alles andere fällt auf FotoMoeglich zurück (belegt durch Logik-Probe).",
            "- `fnFehlt`/`fnFehltGrund` haben 12 Parameter; jeder Aufruf im Endstand hat 12 Argumente (maschinell gezählt, 5 Aufrufer).",
            "- Typen der Argumente: Typ/Bewertung/WertText/Kommentar/FotoModus/Grenzmodus Text, Pflicht/KommentarPflicht Boolean, WertZahl/MinWert/MaxWert/Fotoanzahl Number – so in allen drei Zweigen von colAntworten angelegt.",
            "- **Schema von colAntworten:** alle drei Datensatz-Literale (Nur-Ansicht, Bearbeiten, deaktivierte) haben dieselben 19 Felder (maschinell). Im Export hatte der Bearbeiten-Zweig 16 statt 17 Felder – genau `FotoMoeglich` fehlte (maschinell belegt). Das war die Ursache des Fehlers vom 27.10.",
            "- `fnZahlBewertung` hat einen 4. Parameter, der in Paket 1 nicht benutzt wird. UNSICHER, ob Studio einen unbenutzten Parameter anmahnt (kein Fehler erwartet, App-Prüfung Schritt 1.10 zeigt es).",
        ],
        "c": [
            "1. Spalte `Foto` anlegen und Datenquelle aktualisieren **vor** OnVisible (liest `p.Foto.Value`).",
            "2. App.Formulas vor oder nach den Aufrufern: dazwischen stehen rote Fehler, weil sich die Anzahl der Parameter ändert. Das Paket ist nur als Ganzes gültig (atomar), App-Prüfung erst am Ende.",
            "3. colAntworten wird in OnVisible mit allen Feldern angelegt, bevor ein Aufrufer sie liest (Karte, Labels, Speichern laufen erst nach OnVisible).",
            "4. Kein Schritt hängt von Paket 2–6 ab. `KommentarPflicht`/`Grenzmodus` sind feste Werte (false/\"Mangel\"), ihre Spalten kommen erst in Paket 2/3.",
        ],
        "d": [
            ("scrKategorie.OnVisible", "ja", "FotoModus, KommentarPflicht, Grenzmodus in allen drei Zweigen; FotoMoeglich nur noch als Rückfall in fnFotoModus"),
            ("fnFehlt / fnFehltGrund", "ja", "neue Regel „Foto“ (nur bei FotoModus Pflicht und 0 Fotos); alte Regeln zeichengleich übernommen, Rückwärtsgleichheit für alle 648 alten Kombinationen je Paketstand belegt (Logik-Probe)"),
            ("btnKaSpeichern: Prüfung und Sprung", "ja", "Prüfung über lblKaFehlendAnzahl (enthält jetzt Foto-Pflicht), Sprung mit derselben Regel"),
            ("JSON-Aufbau (varAntwortJSON)", "nein", "ShowColumns unverändert, kein neues Feld im JSON"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein", "liest nur NIO-Zeilen aus dem JSON, unverändert"),
            ("htmProtokoll", "nein", ""),
            ("Foto-Upload (btnKaSpeichern F1/F2)", "ja", "Bedingung `fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)` statt LookUp(colPP).FotoMoeglich, an allen 3 Stellen (Upload, Fehlerzählung, Meldung); dieselbe Funktion steuert `addKaFoto.Visible`, damit nie ein Foto gewählt werden kann, das nicht hochgeladen würde"),
            ("Lesemodus nach Abschluss", "ja", "Foto-Knopf nur bei gespeicherten Fotos, Fenster-Hinweis „Gespeicherte Fotos (nur Ansicht).“; Kommentar sichtbar, wenn gespeichert oder n.i.O."),
            ("Foto-Knopf beim Bearbeiten", "ja", "zusätzlich sichtbar, wenn alte Links da sind (vorher unsichtbar bei i.O. + Aus)"),
            ("Nachlese-Vergleich", "nein", "unverändert, JSON gleich aufgebaut"),
            ("Kommentar leeren (08:44)", "ja", "Bedingung über fnKommentarNoetig, für aktive Punkte gleiches Ergebnis wie `Bewertung <> \"NIO\"` (Logik-Probe); deaktivierte, mitgeführte Punkte (`Inaktiv`) bleiben jetzt unverändert (vorher wurde auch ihr Kommentar geleert)"),
            ("Kartenhöhe, lblKaAbstand", "ja", "Zeile unter der Eingabe erscheint, wenn Kommentar oder Foto-Knopf sichtbar ist; Abstand folgt der Kartenhöhe (vorher fehlte er bei Foto ohne n.i.O.)"),
            ("Foto-Zähler btnKaFoto.Text", "ja", "zählt neue Fotos ohne `Uebernommen` + gespeicherte Links; vorher doppelt gezählt nach fehlgeschlagenem Speichern"),
        ],
        "e": [
            ("neuer Punkt ohne Daten", "FotoModus aus der Spalte; bei Pflicht „(Foto)“ offen, sonst wie bisher", "Logik-Probe P1, A2–A4"),
            ("alter gespeicherter Punkt (JSON ohne neues Feld)", "JSON hat kein Foto-Feld, FotoModus kommt aus den Stammdaten; gespeicherte Links zählen als Fotos (Pflicht erfüllt)", "OnVisible Bearbeiten-Zweig, fnLinkAnzahl, T1.9"),
            ("inaktiver Punkt", "FotoModus \"Aus\", ausgeblendet, zählt nicht (Filter `!Inaktiv`), Foto-Pflicht greift nicht; Kommentar bleibt beim Speichern unverändert", "Code"),
            ("Rundgang abgeschlossen (Nur-Lesen)", "keine Pflicht-Prüfung, Foto-Knopf nur mit gespeicherten Fotos, keine Uploads", "Code, B7"),
            ("Wechsel n.i.O. → i.O. → n.i.O.", "Foto-Knopf rot → (bei Aus) verschwindet / (bei Optional/Pflicht) blau → rot; schon gewählte Fotos bleiben in colFotos; Upload nur, wenn beim Speichern n.i.O. oder Modus ≠ Aus", "Code, A6–A8"),
            ("Kategorie zweimal speichern", "zweites Mal: gespeicherte Links zählen, kein erneuter Upload (Uebernommen/Url), keine Doppelungen", "Code F1/F2 unverändert, B6"),
            ("Abbruch mitten im Speichern", "Upload fertig, Patch nicht: Links stehen schon in colAntworten, Fotos `Uebernommen` → erneutes Speichern lädt nicht doppelt hoch; Pflicht bleibt erfüllt", "Code"),
            ("Netzfehler", "Upload-Fehler → Meldung „x Foto(s) konnten nicht hochgeladen werden“, Kategorie nicht gespeichert; Pflicht zählt das nicht hochgeladene Foto, erneutes Tippen lädt nach. Grenze: Flow ohne Rückmeldung (siehe Offene Befunde)", "Code"),
            ("zwei Prüfer gleichzeitig", "unverändert: GespeichertAm-Vergleich lehnt das zweite Speichern ab; Fotos des zweiten bleiben unhochgeladen", "Code"),
            ("Foto Pflicht + Punkt nicht Pflicht und unbeantwortet", "Foto trotzdem verlangt (Pflicht = Nachweis)", "Logik-Probe"),
            ("FotoMoeglich Ja, Foto leer", "Optional", "Logik-Probe, A1"),
        ],
        "f": FALLEN_ALLG + [
            "Y in Galerien friert beim YAML-Einfügen ein: Paket 1 fügt kein YAML ein, alle Werte per Formelleiste. Nach Schritt 1.6 trotzdem `btnKaFoto.Y` prüfen.",
            "Zwischenablage: Länge des kopierten Blocks prüfen (Lehre 27.10.: alter Inhalt eingefügt → 35 Fehler).",
            "Ebenenreihenfolge ✕/Bild: nicht über „Nach vorne“ gelöst, sondern über Lage (Bild beginnt bei Y 52), damit es unabhängig von der Reihenfolge stimmt.",
        ],
        "g": [
            "- Nicht automatisch ausführbar: Formeln in Studio, Foto-Auswahl, Upload. Testbogen Teil A (Vorschau) und Teil B (Tablet, Foto) im Paket.",
            "- Maschinell: Namen, Klammern, Rückübersetzung, Schema der drei Zweige, Anzahl Argumente, Textbreiten, Logik-Gegenprobe.",
        ],
        "offen": [
            "- **Nicht Teil dieses Pakets, aber für Foto-Pflicht wichtig:** Der Flow `RG_Foto_hochladen` antwortet nicht. Scheitert er nach dem Start, steht der Link trotzdem im JSON und die Pflicht gilt als erfüllt. Vorschlag „Flows rückmelden“ in BAUKASTEN_UEBERSICHT.md (eigenes Paket, nicht gebaut).",
        ],
    },
    2: {
        "b": [
            "- `KommentarPflicht` Ja/Nein: nur `Coalesce(p.KommentarPflicht; false)` (maschinell).",
            "- `fnBeantwortet(bew; wt; wz)`: Text, Text, Number – Blank wird wie leer behandelt (`bew <> \"\"`, `Trim(wt) <> \"\"`, `!IsBlank(wz)`).",
            "- Protokoll: `b` ist dort `Text(a.Value.Bewertung)` (unverändert), Vergleich mit \"NIO\" ist Text.",
        ],
        "c": ["1. Spalte anlegen + aktualisieren vor OnVisible.", "2. App.Formulas, OnVisible, Kommentarfeld, Protokoll – kein Block hängt von einem späteren ab. Paket 1 muss drin sein (Felder und fnKommentarNoetig)."],
        "d": [
            ("scrKategorie.OnVisible", "ja", "Bearbeiten-Zweig liest KommentarPflicht; Nur-Ansicht und deaktivierte bleiben false (dort keine Prüfung)"),
            ("fnFehlt / fnFehltGrund", "ja (indirekt)", "über fnKommentarNoetig"),
            ("btnKaSpeichern: Prüfung und Sprung", "ja (indirekt)", "Prüfung/Sprung zählen fehlende Pflicht-Kommentare bei i.O."),
            ("Kommentar leeren (08:44)", "ja (indirekt)", "Kommentar bleibt bei KommentarPflicht und beantwortetem Punkt; ohne Pflicht wie bisher geleert"),
            ("JSON-Aufbau (varAntwortJSON)", "nein", "Kommentar war schon im JSON"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein", "nur NIO; i.O.-Kommentare werden keine Mängel"),
            ("htmProtokoll", "ja", "Farbe des Kommentars nach Bewertung"),
            ("Foto-Upload", "nein", ""),
            ("Lesemodus nach Abschluss", "ja", "Kommentar bei i.O. wird angezeigt (Paket 1: sichtbar, wenn nicht leer)"),
            ("Nachlese-Vergleich", "nein", ""),
            ("Kommentarfeld (Sichtbarkeit, Kartenhöhe)", "ja (indirekt)", "über fnKommentarNoetig aus Paket 1, keine Formel neu"),
        ],
        "e": [
            ("neuer Punkt ohne Daten", "kein Kommentar verlangt, bis der Punkt beantwortet ist", "Logik-Probe P2"),
            ("alter gespeicherter Punkt (JSON ohne neues Feld)", "Kommentarpflicht kommt aus den Stammdaten; alter i.O. ohne Kommentar zählt beim Wiederöffnen als offen (gewollt: Kontrolle)", "Code"),
            ("inaktiver Punkt", "KommentarPflicht false, zählt nicht; gespeicherter Kommentar bleibt beim erneuten Speichern erhalten (`!Inaktiv` in „Kommentar leeren“)", "Code"),
            ("Kommentarpflicht wird später abgeschaltet", "gespeicherte i.O.-Kommentare werden beim nächsten Speichern der Kategorie geleert (gewollt: Regel gilt dann nicht mehr)", "Code"),
            ("Rundgang abgeschlossen (Nur-Lesen)", "keine Prüfung, Kommentar sichtbar wenn gespeichert", "Code"),
            ("Wechsel n.i.O. → i.O. → n.i.O.", "Kommentar bleibt im Feld; Hinweistext wechselt; beim Speichern bleibt er (Pflicht) bzw. wird bei i.O. ohne Pflicht geleert", "Logik-Probe, T2.5–T2.7"),
            ("Kategorie zweimal speichern", "Kommentar bleibt erhalten (wird beim Öffnen aus dem JSON gelesen)", "T2.9"),
            ("Abbruch mitten im Speichern", "UpdateIf lief schon: Kommentare ohne Pflicht sind in colAntworten geleert (wie 08:44); bei Pflicht bleiben sie", "Code"),
            ("Netzfehler", "Patch scheitert → Nachlese ungleich → Meldung, nichts verloren (Formular bleibt offen)", "Code unverändert"),
            ("zwei Prüfer gleichzeitig", "unverändert (GespeichertAm)", "Code"),
        ],
        "f": FALLEN_ALLG + ["HtmlText: der Block ist die ganze Property; einfache Anführungszeichen im HTML stehen innerhalb der Texte, Rückübersetzung zeichengleich (maschinell)."],
        "g": ["- Testfolge T2.1–T2.8 in der Vorschau, alles ohne Tablet möglich."],
    },
    3: {
        "b": [
            "- `Grenzmodus` Auswahlspalte: nur `p.Grenzmodus.Value` / `pp.Grenzmodus.Value` über `fnGrenzmodus` (leer/unbekannt → \"Mangel\", maschinell + Logik-Probe).",
            "- `fnAusserhalb(z; mi; ma)`: Blank-Grenzen zählen nicht, Blank-Wert ist nie außerhalb (wie die alte Formel).",
            "- `fnZahlBewertung` liefert \"\" bei Sperren außerhalb; alle Stellen, die Bewertung lesen, vertragen \"\" (unbewertet).",
        ],
        "c": ["1. Spalte + aktualisieren vor OnVisible.", "2. App.Formulas vor/mit OnVisible (fnGrenzmodus, fnSperreGilt neu). Paket 1 (4. Parameter, Feld Grenzmodus) und Paket 2 (Hinweistext „Kommentar (Pflicht)“) müssen drin sein.", "3. Speichern (JSON mit Warnung) und Protokoll (liest Warnung) sind unabhängig voneinander; altes JSON ohne Warnung wird als false gelesen."],
        "d": [
            ("scrKategorie.OnVisible", "ja", "Grenzmodus aus Spalte (Bearbeiten, Nur-Ansicht über pp); Neubewertung gespeicherter Zahlen mit Grenzmodus"),
            ("fnFehlt / fnFehltGrund", "ja", "„Bereich“ bei Sperren außerhalb"),
            ("btnKaSpeichern: Prüfung und Sprung", "ja (indirekt)", "Sperren blockiert, Sprung zum Punkt"),
            ("Kommentar leeren (08:44)", "ja (indirekt)", "Warnen außerhalb behält den Kommentar"),
            ("JSON-Aufbau (varAntwortJSON)", "ja", "neues Feld `Warnung` (per AddColumns, nur im JSON, nicht in colAntworten); Sperren außerhalb wird nie gespeichert"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein", "nur NIO; Warnen speichert IO → kein Mangel (gewollt)"),
            ("htmProtokoll", "ja", "Warnung: i.O. orange + „(außerhalb Soll, begründet)“; Kommentar grau (Paket 2); altes JSON ohne Warnung → false"),
            ("Foto-Upload", "nein", "Bedingung NIO/FotoModus; Warnen ohne NIO lädt nur bei FotoModus ≠ Aus"),
            ("Lesemodus nach Abschluss", "ja", "kein Aufforderungstext mehr: NIO „außerhalb des Sollbereichs“, i.O. außerhalb „außerhalb, begründet“ (orange), unabhängig vom heutigen Grenzmodus; Min/Max aus den heutigen Stammdaten"),
            ("Nachlese-Vergleich", "nein", ""),
            ("Zahlenfeld-Anzeige", "ja", "Text/Farbe Label, Rahmenfarbe"),
        ],
        "e": [
            ("neuer Punkt ohne Daten", "kein Hinweis, Wert fehlt wie bisher", "Logik-Probe"),
            ("alter gespeicherter Punkt (JSON ohne neues Feld)", "beim Öffnen neu bewertet mit dem Grenzmodus von heute (wie bisher mit Min/Max)", "OnVisible"),
            ("inaktiver Punkt", "Grenzmodus \"Mangel\", keine Wirkung", "Code"),
            ("Rundgang abgeschlossen (Nur-Lesen)", "Bewertung so wie gespeichert, keine Neubewertung", "OnVisible Nur-Ansicht"),
            ("Wechsel n.i.O. → i.O. → n.i.O.", "bei ZAHL über den Wert: 18,5 → 12 → 18,5 ergibt je Modus NIO/IO, IO/IO (+Warnung), \"\"/IO (gesperrt)", "Logik-Probe P3"),
            ("Kategorie zweimal speichern", "Warnen: Kommentar bleibt; Sperren: nur Werte im Bereich gespeichert", "Code"),
            ("Abbruch mitten im Speichern", "wie Paket 2", "Code"),
            ("Netzfehler", "unverändert", "Code"),
            ("zwei Prüfer gleichzeitig", "unverändert", "Code"),
            ("Grenze genau auf Min/Max", "im Bereich", "Logik-Probe"),
            ("Sperren mit Min > Max (Fehleinstellung)", "wie Mangel (n.i.O., Kommentar), Rundgang bleibt abschließbar", "Logik-Probe, T3.11"),
            ("Sperren und echter Wert außerhalb", "Speichern unmöglich – deshalb Pflegeregel „Sperren nur für Tippfehler-Grenzen“ (Schritt 3.2)", "Regel"),
            ("Grenzmodus nach dem Speichern umgestellt", "beim Öffnen neu bewertet (wie bisher bei Min/Max); die Karte kann dann vom gespeicherten Stand abweichen, ohne als Änderung zu zählen (vorhandenes Verhalten)", "Code"),
        ],
        "f": FALLEN_ALLG,
        "g": ["- T3.1–T3.8 in der Vorschau."],
        "offen": ["- Fachliche Annahme „Warnen verlangt Begründung“ ist von Josias zu bestätigen (kein technischer Befund)."],
    },
    4: {
        "b": [
            "- `BedingungPunkt` Zahl: `Coalesce(p.BedingungPunkt; 0)`; `BedingungWert` Text: `Coalesce(…; \"\")`.",
            "- `Ausgeblendet` aus dem JSON: `Coalesce(IfError(Boolean(…); false); false)` – fehlt das Feld (altes JSON), ist es false. UNSICHER: `Boolean()` auf einem fehlenden untypisierten Feld (deshalb IfError + Coalesce; Test T4.9).",
            "- `fnSichtbar` bekommt die Felder von A einzeln (Funktionen nehmen keine Datensätze). Argumente werden vor dem Aufruf ausgewertet; Felder eines leeren Datensatzes (A nicht gefunden) liefern Blank, keinen Fehler. In `fnSichtbar` steht `!gef` vor allen Feldern von A, entscheidet also zuerst.",
            "- `PruefpunktID in colVersteckt.PruefpunktID`: Zahl in einer Zahlenspalte.",
        ],
        "c": [
            "1. Spalten + aktualisieren vor OnVisible.",
            "2. App.Formulas (fnSichtbar) vor den Aufrufern; zwischendurch rote Fehler möglich, App-Prüfung am Ende.",
            "3. Im Speichern: `colVersteckt` **vor** dem Foto-Upload (Upload, Links, „übernommen“ lesen sie), `colSpeichern` direkt **vor** dem JSON (nach „Kommentar leeren“ und „Warnung setzen“), AnzahlNIO danach aus colSpeichern.",
        ],
        "d": [
            ("scrKategorie.OnVisible", "ja", "BedID, BedWert, Ausgeblendet in allen Zweigen; Start-Sprung auf ersten sichtbaren Punkt"),
            ("fnFehlt / fnFehltGrund", "nein", "unverändert; Aufrufer filtern vorher auf sichtbar"),
            ("btnKaSpeichern: Prüfung und Sprung", "ja", "Prüfung über lblKaFehlendAnzahl (nur sichtbare), Sprung nur auf sichtbare"),
            ("JSON-Aufbau (varAntwortJSON)", "ja", "aus der Kopie colSpeichern: neues Feld Ausgeblendet, ausgeblendete Punkte leer (auch Warnung = false); AnzahlNIO ebenfalls aus der Kopie"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein (Formel)", "ausgeblendete haben Bewertung \"\" → keine Mängel; AnzahlNIO zählt nach dem Leeren → Plausibilität Sum(AnzahlNIO) = Mängel stimmt"),
            ("htmProtokoll", "ja", "ausgeblendete Zeilen weggelassen"),
            ("Foto-Upload (btnKaSpeichern F1/F2)", "ja", "nur sichtbare (`!a.Ausgeblendet`) an allen 3 Stellen; Links werden nur an sichtbare Punkte gehängt; ausgeblendete verlieren ihre Foto-Links (Dateien bleiben in RG_Fotos)"),
            ("Lesemodus nach Abschluss", "ja", "Galerie zeigt nur nicht ausgeblendete (gespeichertes Flag)"),
            ("Nachlese-Vergleich", "nein", "vergleicht weiterhin den gesendeten Text"),
            ("Zähler/Balken/Kopf/Fuß", "ja", "zählen nur sichtbare"),
            ("Foto-Pflicht/Kommentar-Pflicht ausgeblendeter Punkte", "ja", "gelten nicht (Filter vor fnFehlt)"),
        ],
        "e": [
            ("neuer Punkt ohne Daten", "B ohne Bedingung: wie bisher; B mit Bedingung: unsichtbar, bis A passt", "Logik-Probe P4, T4.1–T4.2"),
            ("alter gespeicherter Punkt (JSON ohne neues Feld)", "Ausgeblendet = false; im Bearbeiten wird live neu berechnet", "OnVisible, T4.9"),
            ("inaktiver Punkt", "A deaktiviert → B sichtbar (sicher); deaktivierte B bleiben wie bisher unsichtbar mitgeführt, ihr gespeichertes Flag bleibt erhalten", "Logik-Probe, UpdateIf `!Inaktiv`"),
            ("Rundgang abgeschlossen (Nur-Lesen)", "Sichtbarkeit aus dem gespeicherten Flag, keine Neuberechnung", "Code"),
            ("Wechsel n.i.O. → i.O. → n.i.O. (an A)", "B erscheint/verschwindet/erscheint; Eingaben in B bleiben bis zum Speichern erhalten", "T4.2–T4.4"),
            ("Kategorie zweimal speichern", "B einmal ausgeblendet gespeichert → leer; beim zweiten Mal wieder live berechnet", "T4.5"),
            ("Abbruch mitten im Speichern", "colAntworten bleibt unverändert (JSON aus der Kopie colSpeichern); stellt der Prüfer A zurück, erscheint B mit seinen Eingaben; Fotos von B bleiben unübernommen in colFotos", "Code, T4.5"),
            ("Netzfehler", "unverändert (Nachlese)", "Code"),
            ("zwei Prüfer gleichzeitig", "unverändert (GespeichertAm)", "Code"),
            ("Fehlkonfiguration (A fehlt, Kette, leerer Wert, Wert passt nicht zu A, Liste)", "B sichtbar und verlangt", "Logik-Probe, T4.10"),
            ("Schreibweise i.O./n.i.O., Groß-/Kleinschreibung", "wie IO/NIO", "Logik-Probe, T4.9"),
            ("Foto an B, dann B ausgeblendet, Speichern", "Foto wird nicht hochgeladen und nicht verlinkt; im JSON sind die Links von B leer; schon früher hochgeladene Dateien von B bleiben ohne Verweis in RG_Fotos (bekannt, harmlos)", "Code"),
        ],
        "f": FALLEN_ALLG + ["`Filter(colAntworten As a; … LookUp(colAntworten As b0; …))` liest dieselbe Sammlung zweimal – nur lesend, erlaubt. Geschrieben wird mit UpdateIf auf colAntworten mit einer **anderen** Sammlung (colVersteckt) in der Bedingung (kein „ForAllWithMutation“)."],
        "g": ["- T4.1–T4.9 in der Vorschau."],
    },
    5: {
        "b": [
            "- `Eingabetyp` bleibt Auswahlspalte, `.Value` wie bisher; neue Werte sind Texte.",
            "- `dpKaDatum.SelectedDate` ist ein Datum → `fnDatumText(d: Date; …)`. `ddKaStunde.Selected.Value` Text, leer → `Coalesce(…; \"\")`.",
            "- Gespeicherte Form „TT.MM.JJJJ“ wird mit `DateValue(Left(…; 10); \"de-DE\")` zurückgelesen, `IfError` fängt kaputte Texte ab.",
            "- Kombinationsfeld: Items/DefaultSelectedItems sind Tabellen mit Spalte `Value` (Text), DisplayFields `[\"Value\"]`.",
        ],
        "c": ["1. Auswahlwerte ergänzen + aktualisieren.", "2. App.Formulas vor den neuen Steuerelementen (fnDatumText).", "3. Steuerelemente: Datum vor Stunde/Minute ist egal (sie lesen sich gegenseitig, beide sind vor der App-Prüfung da)."],
        "d": [
            ("scrKategorie.OnVisible", "nein", "Typ kommt schon aus Eingabetyp.Value bzw. dem JSON"),
            ("fnFehlt / fnFehltGrund", "ja", "Wert fehlt für MEHRFACH/DATUM/DATUMZEIT, „Uhrzeit“ bei Datum ohne Zeit"),
            ("btnKaSpeichern: Prüfung und Sprung", "ja (indirekt)", ""),
            ("JSON-Aufbau (varAntwortJSON)", "nein", "Werte in WertText"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein", "keine Bewertung → keine Mängel; Wert-Spalte würde WertText zeigen"),
            ("htmProtokoll", "nein", "zeigt WertText"),
            ("Foto-Upload", "nein", ""),
            ("Lesemodus nach Abschluss", "ja", "neue Felder DisplayMode.View; Mehrfachauswahl: Auswahl = gespeicherter Text (Nur-Ansicht-Zweig) → zeigt genau die gewählten Werte"),
            ("Nachlese-Vergleich", "nein", ""),
            ("Bedingungen (Paket 4)", "ja (indirekt)", "fnBedPasst prüft Werte der Mehrfachauswahl einzeln, fnBedGueltig kennt MEHRFACH"),
            ("Leeren eines Datums", "ja", "btnKaDatumLeeren setzt WertText = \"\" und die drei Felder zurück; Stunde/Minute erst nach dem Datum wählbar"),
        ],
        "e": [
            ("neuer Punkt ohne Daten", "leer, bei Pflicht offen", "Logik-Probe P5"),
            ("alter gespeicherter Punkt (JSON ohne neues Feld)", "kein neues Feld; neue Typen gab es vorher nicht", "–"),
            ("inaktiver Punkt", "unsichtbar, zählt nicht", "Code"),
            ("Rundgang abgeschlossen (Nur-Lesen)", "Werte sichtbar, nicht änderbar", "T5.10"),
            ("Wechsel n.i.O. → i.O. → n.i.O.", "nicht anwendbar (keine Bewertung); Wechsel der Auswahl schreibt WertText neu", "Code"),
            ("Kategorie zweimal speichern", "Werte werden beim Öffnen aus WertText wieder eingestellt", "T5.8"),
            ("Abbruch mitten im Speichern", "unverändert", "Code"),
            ("Netzfehler", "unverändert", "Code"),
            ("zwei Prüfer gleichzeitig", "unverändert", "Code"),
            ("Uhrzeit vor Datum gewählt", "Text entsteht beim Datum mit der gewählten Zeit", "Logik-Probe fnDatumText, T5.7"),
        ],
        "f": FALLEN_ALLG + [
            "YAML in eine Galerievorlage: mit einem Kind von conKaKarte markiert einfügen (Übergabe 5); danach Y prüfen (E-05).",
            "Kombinationsfeld ohne YAML (Version unbekannt), Properties per Formelleiste.",
            "Classic/DatePicker@2.6.0 und Classic/DropDown@2.3.1 sind in den Exporten belegt (Tischbuchung bzw. diese App).",
        ],
        "g": ["- T5.1–T5.10 in der Vorschau. UNSICHER: Darstellung einer leeren Datumsauswahl (DefaultDate leer) – T5.1 zeigt es."],
    },
    6: {
        "b": [
            "- `HinweisBildID` Zahl: `Coalesce(…; 0)`.",
            "- Bild: `LookUp(RG_Hinweisbilder; ID = varBildID).Thumbnail.Large` – UNSICHER bis zum Vorab-Test 6.3 (Feldname Thumbnail in dieser Umgebung).",
            "- Abfrage nur bei geöffnetem Fenster (`If(varBildID > 0; …)`), da versteckte Steuerelemente trotzdem rechnen.",
        ],
        "c": ["1. Bibliothek, Spalte, Datenquelle und Vorab-Test vor allen Formeln.", "2. OnVisible vor dem Knopf (Feld BildID).", "3. Fenster zuletzt; muss vor conKaFoto/conKaLaden liegen."],
        "d": [
            ("scrKategorie.OnVisible", "ja", "BildID in allen Zweigen, varBildID = 0"),
            ("fnFehlt / fnFehltGrund", "nein", ""),
            ("btnKaSpeichern: Prüfung und Sprung", "nein", ""),
            ("JSON-Aufbau (varAntwortJSON)", "nein", "BildID wird nicht gespeichert"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein", ""),
            ("htmProtokoll", "nein", ""),
            ("Foto-Upload", "nein", ""),
            ("Lesemodus nach Abschluss", "ja", "Knopf auch in der Nur-Ansicht (Bild aus heutigen Stammdaten)"),
            ("Nachlese-Vergleich", "nein", ""),
        ],
        "e": [
            ("neuer Punkt ohne Daten", "Knopf nur bei HinweisBildID > 0", "T6.1, T6.5"),
            ("alter gespeicherter Punkt (JSON ohne neues Feld)", "nicht betroffen", "–"),
            ("inaktiver Punkt", "unsichtbar", "Code"),
            ("Rundgang abgeschlossen (Nur-Lesen)", "Bild ansehbar", "T6.6"),
            ("Wechsel n.i.O. → i.O. → n.i.O.", "nicht betroffen", "–"),
            ("Kategorie zweimal speichern", "nicht betroffen", "–"),
            ("Abbruch mitten im Speichern", "nicht betroffen", "–"),
            ("Netzfehler", "Bild lädt nicht, Fenster bleibt bedienbar (Schließen)", "geschlussfolgert"),
            ("zwei Prüfer gleichzeitig", "nicht betroffen", "–"),
        ],
        "f": FALLEN_ALLG + ["Container-YAML auf dem Bildschirm einfügen; danach Ebene prüfen (ganz oben)."],
        "g": ["- Vorab-Test 6.3 und T6.1–T6.7 in der Vorschau."],
    },
}


RUNDE1 = {
    1: [("B1 mittel: Standardwert „Aus“ widerspricht „leere Spalte = wie bisher“", "Standardwert bleibt „Aus“ (Vorgabe: neue Spalten immer mit Standardwert); FotoMoeglich gilt nur noch für alte Zeilen, neue Punkte über Foto. Prüfschritt, ob SharePoint vorhandene Zeilen füllt (UNSICHER) mit Abhilfe"),
        ("B2 mittel: Testbogen nicht ausführbar (Vorschau ohne Foto, Tablet zeigt veröffentlichte Fassung)", "Testbogen in Teil A (Vorschau) und Teil B (Tablet: Studio im Browser oder veröffentlichen) geteilt"),
        ("B3: Foto-Pflicht auch bei unbeantworteten optionalen Punkten", "bewusst (Nachweis), als Annahme in der Übersicht"),
        ("B4: Kopf/Voraussetzungen widersprüchlich", "jetzt aus dem frischen Export 09:09 erzeugt, ohne Simulation; Voraussetzung nennt den Export"),
        ("B5: Hinweis im Foto-Fenster in der Nur-Ansicht irreführend", "behoben: „Gespeicherte Fotos (nur Ansicht).“"),
        ("B6: E-05-Prüfung nur bei btnKaFoto.Y", "Prüfhinweis für alle Positions-/Höhenformeln ergänzt"),
        ("B7: Testerwartungen unklar", "Testbogen mit benannten Punkten (K1, P10, PO, PX), Folgen des Abschlusses genannt"),
        ("B8: Kommentar inaktiver Antworten wird geleert", "behoben: `!Inaktiv` in „Kommentar leeren“"),
        ("B9: alte Foto-Links bei i.O. + Aus unsichtbar", "behoben: Foto-Knopf auch bei vorhandenen Links; neue Fotos dort nicht wählbar (addKaFoto.Visible)")],
    2: [("B1 mittel: „Kommentar leeren“ läuft über deaktivierte Punkte", "behoben in Paket 1 (`!Inaktiv`)"),
        ("B8: Testlücken (Pflicht = Nein, T2.1)", "Testbogen neu mit PK/PN/PM und Weg über K1"),
        ("B9: Rückweg verschweigt Löschen der i.O.-Kommentare", "im Rückweg ergänzt"),
        ("B10: Kommentar vor dem Patch geleert", "vorhandenes Verhalten (08:44), bleibt; als Szenario dokumentiert"),
        ("B12: ENTWURF nicht in den Voraussetzungen", "erledigt (frischer Export)")],
    3: [("B2 mittel: Warnen nicht von normalem i.O. zu unterscheiden", "behoben: JSON-Feld Warnung, Protokoll orange mit Hinweis, Nur-Ansicht „außerhalb, begründet“"),
        ("B3 mittel: Sperren ohne Ausweg / Min > Max", "Pflegeregel „nur Tippfehler-Grenzen“ in Schritt 3.2 und Kurzfassung; Min > Max → wie Mangel (fnSperreGilt)"),
        ("B7 mittel: Testbogen nicht der Reihe nach ausführbar", "neu: Z1/Z2/Z3 gleichzeitig, Kommentare in der Folge, Abschluss getrennt"),
        ("B4: „Soll“ bei Sperren", "behoben: „zulässig ab … bis …“"),
        ("B5: Neubewertung beim Öffnen zählt nicht als Änderung", "vorhandenes Verhalten, als Szenario dokumentiert"),
        ("B6: Nur-Ansicht zeigt Aufforderungen", "behoben"),
        ("B11: clrWarnungHell unbenutzt", "entfernt")],
    4: [("B1 mittel: Fotos ausgeblendeter Punkte bleiben", "behoben: Fotos leeren, Links nicht an ausgeblendete hängen"),
        ("B2 mittel: falscher Bedingungswert blendet für immer aus", "behoben: fnBedGueltig prüft gegen Typ/Auswahl von A, sonst B sichtbar; i.O./n.i.O. und Schreibweisen normalisiert (fnBedNorm)"),
        ("B3 mittel: Testbogen nicht ausführbar", "neu: Vorbedingungen, zweite Durchführung für den ausgeblendeten Fall, Abschluss getrennt"),
        ("B4/B5: Eingaben/neue Fotos ausgeblendeter Punkte verworfen", "gewollt, dokumentiert"),
        ("B6: Kettenerkennung grob", "gewollt (sicherer Ausfall)"),
        ("B7: Zahl mit Warnen und Bedingung NIO", "Hinweis in Schritt 4.2"),
        ("B8: Stammdaten während laufender Rundgänge", "bekannte Regel F4 (nach Feierabend pflegen)"),
        ("B9: Sichtbarkeitsregel an zehn Stellen", "vom Generator aus einer Vorlage erzeugt, maschinell gleich"),
        ("B10 UNSICHER: Galerie verschiebt sich", "Test T4.4"),
        ("B11 UNSICHER: Flows lesen JSON", "kein Flow liest das JSON (Export belegt)"),
        ("B12: Pfade in 4.5", "ergänzt")],
}


RUNDE2_34 = {
    3: [("B3-1 mittel: Nur-Ansicht liest heutige Min/Max statt des Kennzeichens", "behoben: Feld `Warnung` in allen drei Zweigen, Nur-Ansicht liest nur das Feld; deaktivierte Punkte behalten es"),
        ("„zulässig“ bei Min > Max", "behoben: „zulässig“ nur, wenn die Sperre gilt"),
        ("„bitte begründen“ bleibt nach der Begründung", "behoben: dann „außerhalb, begründet“"),
        ("Testbogen (Aktiv, Aufräumen, T3.11 nicht speichern)", "ergänzt"),
        ("Rückweg: Warnen-Werte in der alten App; Umstellen während laufender Rundgänge", "im Rückweg bzw. als Pflegeregel ergänzt"),
        ("Warnen/Mangel bei Min > Max", "vorhandenes Verhalten (alles außerhalb), Pflegeregel „Min nie größer als Max“"),
        ("lblKaZahlInfo auf schmalen Geräten", "App ist für Tablet hochkant (768) gebaut; dort 2 Zeilen geprüft")],
    4: [("B4-1 mittel: T4.10 prüft den sicheren Ausfall nicht", "T4.10: A auf i.O. → B bleibt sichtbar"),
        ("B4-2 mittel: Leeren vor Upload/Nachlese verliert Eingaben, Fotos falsch übernommen", "behoben: JSON und AnzahlNIO aus Kopie colSpeichern, colAntworten bleibt; Upload/Links/„übernommen“ über colVersteckt"),
        ("Bedingung NIO an Sperren-Punkt", "Pflegehinweis: NIO nur bei Grenzmodus Mangel"),
        ("Rückweg „BedingungPunkt auf 0“ wirkungslos", "korrigiert: B auf Aktiv = Nein"),
        ("Testbogen (neue Durchführung, Nachholtage, Z1–Z3, Textfeld verlassen)", "ergänzt"),
        ("MEHRFACH erst ab Paket 5", "im Hinweis vermerkt"),
        ("Kette, verworfene Werte/Fotos, Dateien ohne Verweis", "gewollt bzw. bekannt, dokumentiert")],
}

RUNDE3 = {
    5: [("B2: Rückweg nennt vier statt fünf Steuerelemente", "korrigiert"),
        ("B3: „Drei Blöcke“, einzeln eingefügt kurz rote Fehler", "„alle vier zusammen einfügen“"),
        ("B4: Testdaten ohne Aktiv/Foto/Reihenfolge, kein Aufräumen", "ergänzt"),
        ("B5: nur Stunde oder nur Minute wird nicht gespeichert; Restwerte UNSICHER", "Teilangabe ist gewollt unvollständig („(Uhrzeit)“ im Fuß); Restwerte: Test T5.8c mit Ausweichplan"),
        ("B6: Testlücken (✕ bei Datum+Uhrzeit, alle Werte abwählen, Nur-Ansicht der Uhrzeit)", "T5.8a–c, T5.12 ergänzt")],
    6: [("B1 mittel: E-05-Prüfung für das Bildfenster fehlt", "Prüfliste mit den sechs Formeln in 6.6, Test T6.7 hochkant/quer"),
        ("B7: Titel im Bildfenster abgeschnitten", "Größe 16, Höhe 64, Bild ab Y 84 (Textbreite maschinell geprüft: 2 Zeilen)")],
}

RUNDE3_12 = {
    1: [("Nr. 1 mittel: Tests nicht auf den ZZ-Test-Rundgang beschränkt", "Hinweis am Anfang des Bogens; Id 10 liegt laut Fortschritt im ZZ-Test-Rundgang, echte Stammdaten gibt es noch nicht"),
        ("Nr. 2/5/6: B6 speichert beim Prüfen, A10 erwartet Nachfrage, Prüfung nach 1.6 in Studio nicht möglich", "Bogen und Prüfhinweis korrigiert"),
        ("Nr. 7: Schritt 1.9 stellt Fotoverlust als behoben dar", "Text korrigiert (vorhandenes, gewolltes Verhalten)"),
        ("Nr. 8: Fuß nennt nur den ersten Grund", "bekannt, bleibt so")],
    2: [("Nr. 1 mittel: ZZ-Test-Rundgang", "wie Paket 1"),
        ("Nr. 3/4: Hinweistext bei gefülltem Feld nicht sichtbar; eine Durchführung je Tag", "T2.1, T2.5, T2.6 angepasst")],
}

RUNDE3_34 = {
    3: [("Gezielte Prüfung (30.10.) von Feld Warnung, Nur-Ansicht und Protokoll: kein Befund", "alle drei Zweige von OnVisible haben das Feld, Speichern setzt es vor dem JSON, Nur-Ansicht liest nur das Feld, altes JSON → false. Zwei Punkte geschlussfolgert, nicht in Studio getestet: UpdateIf mit Feldverweisen im Änderungsdatensatz (Schritt 3.8 und T3.10 zeigen es)")],
    4: [("Gezielte Prüfung (30.10.) des Speicherns aus der Kopie: kein mittlerer oder hoher Befund", "Reihenfolge colVersteckt → Upload → Kommentar leeren → Warnung → colSpeichern → JSON → Patch stimmt, alle If-Zweige liefern denselben Datensatztyp, Abschluss-Plausibilität stimmt, Abbruch lässt colAntworten unverändert. Geschlussfolgert, nicht in Studio getestet: Patch(Datensatz; Datensatz) in ForAll (Schritt 4.8 und T4.5–T4.8 zeigen es)"),
        ("N1 niedrig: hochgeladene Datei ohne Verweis nach Abbruch", "harmlos, dokumentiert")],
}

RUNDE2 = {
    1: [("Nr. 1 mittel: Erwartung „ohne Kommentar“ bei i.O. nicht sichtbar", "Test B6a: Punkt auf n.i.O. tippen, Kommentarfeld muss leer sein"),
        ("Nr. 2/3/4/6/13: Testbogen (Reihenfolge der Kategorien, Namen, Prüfhinweis 1.6, Daten aktualisieren, Foto = Aus bei FotoMoeglich Ja)", "ergänzt (A9, Hinweise im Bogen, Prüfhinweis 1.6)"),
        ("Nr. 5: addKaFoto.Visible nicht in der E-05-Liste", "kein YAML-Einfügen, per Formelleiste – E-05 betrifft es nicht"),
        ("Nr. 7: Foto-Pflicht bei unbeantwortetem optionalem Punkt", "Annahme, von Josias zu bestätigen"),
        ("Nr. 8: FotoMoeglich bei neuen Punkten wirkungslos", "Empfehlung in 1.2: Spalte im Formular ausblenden"),
        ("Nr. 9/10: Doku", "Auswirkungsliste und Schritt 1.3 ergänzt"),
        ("Nr. 11/12: Foto bei Wechsel n.i.O.→i.O. (Aus) verworfen; Fuß nennt nur den ersten Grund", "vorhandenes bzw. gewolltes Verhalten"),
        ("Nr. 17: ProtokollErstelltAm fehlt", "Fehlalarm: Spalte existiert (DataSources), sie fehlte nur in der Prüfer-Übersicht")],
    2: [("Nr. 1 mittel: T2.9 nicht sichtbar prüfbar", "T2.9/T2.9a neu"),
        ("Nr. 14: KommentarPflicht abschalten löscht Kommentare", "im Rückweg und in den Szenarien genannt"),
        ("Nr. 15: Schritt 2.2 nennt einen Testpunkt", "verweist auf PK/PN"),
        ("Nr. 16 UNSICHER: Mail-Flow", "es gibt keinen Mail-Flow (Export)")],
    5: [("P5-1 mittel: Datum lässt sich nicht leeren", "neuer Knopf `btnKaDatumLeeren` (✕) leert den Wert und setzt die drei Felder zurück"),
        ("P5-3: Uhrzeit vor Datum geht verloren", "Stunde/Minute gesperrt, bis ein Datum gewählt ist"),
        ("P5-4: Platzhalter der Datumsauswahl", "InputTextPlaceholder „Datum wählen“"),
        ("P5-5/P5-6 UNSICHER: OnChange beim Laden / Restwerte nach Verwerfen", "Tests T5.10/T5.11"),
        ("P5-7: Typwechsel eines benutzten Punkts", "Pflegeregel in 5.2"),
        ("P5-8: Reihenfolge der Mehrfachauswahl", "gespeichert in der Reihenfolge der Auswahlwerte"),
        ("P5-9: modernes statt klassisches Kombinationsfeld", "Menüpfad „Einfügen → Klassisch“ genannt"),
        ("P5-10/11: Doku, Testlücke Bedingung auf MEHRFACH", "5.2 angepasst, Test T5.4"),
        ("Tests T5.7/T5.8 nicht ausführbar", "Testbogen neu")],
    6: [("P6-1 mittel: Frage wird 160 px schmaler, abgeschnitten", "Knopf „Bild“ 64 px, Frage nur 80 px schmaler"),
        ("T6.4 nicht ausführbar", "entfernt, Absicherung erklärt"),
        ("P6-3: Vorschaubilder am Tablet / Verzögerung", "Hinweis in 6.2, Test T6.7"),
        ("P6-4: leere Bildfläche ohne Hinweis", "bewusst so (Schließen geht), Test T6.6"),
        ("P6-5: Nur-Ansicht zeigt heutiges Bild", "bewusst; Einfrieren kommt mit dem späteren Paket „Schlüssel/Status/Einfrieren“")],
}


for _k, _v in RUNDE2_34.items():
    RUNDE2[_k] = _v



for _k, _v in RUNDE3_12.items():
    RUNDE3[_k] = _v
for _k, _v in RUNDE3_34.items():
    RUNDE3[_k] = _v


def UEBERSICHT(d):
    z = ["# Baukasten-Pakete 1–6 – Übersicht", ""]
    if d["simulation"]:
        z += ["> **ENTWURF.** Erzeugt aus dem Export 27.10. 08:24 mit einer Simulation der Änderung von 08:44 (`UpdateIf(colAntworten; Bewertung <> \"NIO\"; {Kommentar: \"\"})`). "
              "Vor dem Einfügen: frischen Export hochladen, `python3 -I werkzeuge/baukasten.py <Schlüssel>` ohne Simulation laufen lassen. "
              "Bricht er nicht ab, gelten die Blöcke für den echten Stand.", ""]
    z += ["## Reihenfolge", "",
          "Pakete **nur in dieser Reihenfolge**, jedes ganz (atomar), nach jedem Paket App-Prüfung = 0, Test, speichern. Erst nach Paket 1 und erfolgreichem Test weitermachen.", "",
          "| Paket | Inhalt | SharePoint | Properties | neue Steuerelemente |", "|---|---|---|---|---|"]
    sp_je = {1: "Foto (Auswahl)", 2: "KommentarPflicht (Ja/Nein)", 3: "Grenzmodus (Auswahl)", 4: "BedingungPunkt (Zahl), BedingungWert (Text)",
             5: "Eingabetyp + 3 Werte", 6: "Bibliothek RG_Hinweisbilder, HinweisBildID (Zahl)"}
    for p in d["pakete"]:
        z.append("| %d | %s | %s | %d | %s |" % (p["nr"], PAKET_TEXT[p["nr"]]["titel"], sp_je[p["nr"]], len(p["props"]), ", ".join(p["neu"]) or "–"))
    z += ["", "## Prüfstand", "",
          "- Erzeugt aus dem frischen Export 27.10.2026 09:09 (ohne Simulation). Maschinelle Prüfung 0 Fehler, Mutationstest 9/9, Logik-Gegenprobe 71 Szenarien ohne Fehler.",
          "- Unabhängige Prüfung: Runde 1 (Pakete 1–4), Runde 2 (alle sechs) und Runde 3 (Pakete 1, 2, 5, 6) eingearbeitet, siehe PRUEFUNG_n. In Runde 3 fand kein Prüfer einen Code-Fehler, nur Testbogen- und Doku-Befunde (eingearbeitet).",
          "- Die Änderungen aus Runde 2 an Paket 3 (Feld Warnung) und Paket 4 (Speichern aus der Kopie colSpeichern) hat am 30.10. ein gezielter unabhängiger Prüfer durchgesehen: kein mittlerer oder hoher Befund, ein niedriger Hinweis (N1, harmlos). Nicht für jedes Paket liegt eine Gesamtprüfung der letzten Fassung vor (3 und 4 nur gezielt auf die geänderten Stellen); die letzten Befunde waren Testbogen/Doku.",
          ]
    z += ["", "## Entscheidungen und Annahmen (bitte bestätigen)", "",
          "- **Foto-Pflicht gilt immer**, auch wenn der Punkt selbst nicht Pflicht ist (Nachweis, z. B. Thermometer).",
          "- **n.i.O. erlaubt immer Fotos** (wie bisher), auch bei Foto = Aus.",
          "- **Kommentarpflicht greift, sobald der Punkt beantwortet ist** (bei optionalen, unbeantworteten Punkten nicht).",
          "- **Grenzmodus Warnen** = i.O. mit Pflicht-Begründung, kein Mangel. **Sperren** = Wert außerhalb lässt sich nicht speichern.",
          "- **Bedingte Fragen nur eine Ebene tief**, A in derselben Kategorie. Falsch eingerichtete Bedingungen zeigen B immer (sicherer Ausfall). Der Builder soll das später beim Anlegen verhindern.",
          "- **Datum/Uhrzeit als Text** „TT.MM.JJJJ [hh:mm]“ in WertText (keine Zeitzonen-Fallen, Protokoll und Mängel unverändert).",
          "- **Beispielbild als Fenster** statt aufklappbar in der Karte.",
          "",
          "## Vorschlag (nicht gebaut): Paket „Flows rückmelden“", "",
          "Die Flows antworten nicht (Antwort-Aktion wäre Premium). Folge: Scheitert ein Upload oder das PDF nach dem Start, merkt die App es nicht; bei Foto-Pflicht gilt das Foto als vorhanden. "
          "Vorschlag ohne Premium: (1) RG_Foto_hochladen schreibt nach „Datei erstellen“ mit der Standard-Aktion **Element aktualisieren** nichts zurück, sondern die App prüft beim **Abschluss** gegen die Bibliothek RG_Fotos (Datenquelle, Filter `DurchfuehrungID`), ob jede verlinkte Datei existiert, und meldet fehlende; "
          "(2) RG_Protokoll_archivieren schreibt am Ende per **Element aktualisieren** `ProtokollUrl` und `ProtokollErstelltAm` in RG_Durchfuehrungen, die App setzt die URL nicht mehr selbst und zeigt „Archivieren läuft …“, bis die Nachlese die URL findet. "
          "Das ist ein eigenes Paket mit Flow-Änderung (Josias' Konto) und gehört nicht zu 1–6.",
          "",
          "## Dateien", "",
          "- `PAKET_n_*.md` – zum Einfügen (Kurzfassung, Schritte, Blöcke deutsch, YAML, Test, Rückweg, Vorher-Fassungen)",
          "- `PRUEFUNG_n_*.md` – Prüfung a–g, Szenarien, offene Befunde",
          "- `stand_baukasten.json` – maschineller Stand (alle Blöcke englisch, vorher/nachher)",
          "- Erzeugt mit `werkzeuge/baukasten.py`, `werkzeuge/doc_baukasten.py`, `werkzeuge/baukasten_text.py`; Gegenprobe `werkzeuge/logik_probe.py`.",
          ]
    hinw = d.get("hinweise") or []
    if hinw:
        z += ["", "## Hinweise des Generators", ""] + ["- " + h for h in hinw]
    return z
