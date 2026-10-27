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
            "Frischer Export nach dem Stand von 27.10. 08:44 eingelesen (dieses Dokument wurde daraus erzeugt, siehe Kopfzeile).",
            "Die App ist gespeichert, nichts halb eingefügt.",
        ],
        "schritte": [
            dict(SICHERUNG, nr="1.1"),
            {"nr": "1.2", "titel": "SharePoint-Spalte anlegen", "text": [
                "IMS+ → Liste **RG_Pruefpunkte** → **+ Spalte hinzufügen → Auswahl**:",
                "- Name: **Foto** (genau so)",
                "- Auswahlmöglichkeiten (je eine Zeile): **Aus**, **Optional**, **Pflicht**",
                "- Standardwert: **Aus** · Mehrfachauswahl: **Nein** · Werte erforderlich: **Nein**",
                "- **FotoMoeglich nicht löschen und nicht umbenennen.** Vorhandene Zeilen bleiben leer, die App liest leer wie bisher.",
                "Für den Test: Prüfpunkt **Id 10** (Thermometer) → Foto = **Pflicht**. Einen zweiten i.O./n.i.O.-Punkt derselben Kategorie → Foto = **Optional**.",
                DATEN_AKT,
            ]},
            {"nr": "1.3", "titel": "App.Formulas", "text": [EINFUEGEN,
                                                           "`App` markieren, Property **Formulas**. Ganzer Inhalt wird ersetzt (neu: fnLinkAnzahl, fnFotoModus, fnBeantwortet, fnAusserhalb, fnKommentarNoetig, fnFehltGrund; fnFehlt mit 12 Werten; fnZahlBewertung mit 4. Wert)."]},
            {"nr": "1.4", "titel": "Kategorie öffnen: Felder der Antworten", "text": ["`scrKategorie` markieren, Property **OnVisible**."]},
            {"nr": "1.5", "titel": "Zahlenfeld", "text": []},
            {"nr": "1.6", "titel": "Karte, Kommentar und Foto-Knopf", "text": [
                "Alle Steuerelemente liegen in `galKaPruefpunkte` → `conKaKarte` (Karte) bzw. direkt in der Galerievorlage (`lblKaAbstand`)."],
             "pruefen": ["Karte eines Punkts mit Foto = Pflicht ist höher und zeigt rechts unten „📷 Foto *“ (blau).",
                         "Y von `btnKaFoto` steht als Formel da, nicht als Zahl (E-05)."]},
            {"nr": "1.7", "titel": "Zähler „Noch offen“ (unsichtbare Labels)", "text": [
                "`lblKaFehlendAnzahl` und `lblKaFehlend` liegen direkt auf `scrKategorie` (unsichtbar)."]},
            {"nr": "1.8", "titel": "Speichern", "text": [
                "`conKaFuss` → `btnKaSpeichern`, Property **OnSelect**. Gegenüber vorher: Sprung zum ersten offenen Punkt mit der neuen Prüfregel, "
                "Upload-Bedingung liest `FotoModus` (statt `LookUp(colPP; …).FotoMoeglich`), „Kommentar leeren“ (08:44) über `fnKommentarNoetig` "
                "(heute gleiches Ergebnis: nur bei n.i.O. bleibt der Kommentar). Kommentare im alten Code entfallen."]},
            {"nr": "1.9", "titel": "Foto-Fenster", "text": [
                "`conKaFoto` → `conKaFotoKarte` → `lblKaFotoHinweis`, `addKaFoto`, und in `galKaFotoNeu` das Bild `imgKaFotoNeu` "
                "(Bild beginnt unter dem ✕-Knopf, damit das ✕ immer tippbar ist, egal wie die Ebenen liegen)."]},
            pruefung_schritt("1.10"),
        ],
        "test": [
            "Zeitachse in der Studio-Vorschau mit dem Test-Rundgang „ZZ Test Objektrundgang TCC“ (Tag mit Plan oder Nachholtag; laufende Durchführung D13 darf fortgesetzt werden). "
            "Foto-Auswahl selbst testet Josias am Tablet (die Datei-Auswahl der Vorschau ist für die Automation nicht bedienbar).",
            "",
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T1.1 | Kategorie 1 öffnen | Thermometer-Karte: „📷 Foto *“ blau umrandet, Karte höher. Optional-Punkt: „📷 Foto“. Übrige Punkte: kein Foto-Knopf. |",
            "| T1.2 | Alle Punkte ausfüllen, kein Foto | Fuß: „Noch offen (1): ZZ Test Thermometer … (Foto)“, Knopf „Offene Punkte ↓“ |",
            "| T1.3 | „Offene Punkte ↓“ tippen | Liste springt zur Thermometer-Karte, Karte rot umrandet |",
            "| T1.4 | Foto-Knopf tippen | Fenster: Hinweis „Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren.“ einzeilig, Knopf „Foto aufnehmen / auswählen“ normal groß |",
            "| T1.5 | (Tablet) Foto wählen, ✕ antippen, erneut wählen, „Fertig“ | ✕ entfernt das Foto; danach Knopf „📷 Foto (1)“, Fuß „✓ Alles ausgefüllt“ |",
            "| T1.6 | Einen anderen Punkt auf n.i.O. | Kommentarfeld links, roter „📷 Foto“ rechts in einer Zeile; zurück auf i.O. → beides weg, Karte wieder niedrig |",
            "| T1.7 | n.i.O. + Kommentar „test“ → wieder i.O. → Speichern | „Gespeichert.“; nächste Kategorie öffnet sich. (08:44-Verhalten: Kommentar wird nicht gespeichert) |",
            "| T1.8 | (Tablet) Bibliothek RG_Fotos → TEST/2026/10/R…/ | Datei `D…-K…-P10-xxxxxxxx.jpg` vorhanden |",
            "| T1.9 | Kategorie 1 wieder öffnen (Bearbeiten) | Thermometer „📷 Foto (1)“ ohne „*“; Speichern ohne neues Foto möglich |",
            "| T1.10 | Prüfpunkt Id 10: Foto leer lassen, FotoMoeglich = Ja; Kategorie neu öffnen | verhält sich wie Optional (Knopf da, nicht Pflicht) |",
            "| T1.11 | Rundgang abschließen → Ansehen → Kategorie 1 | Nur-Ansicht: Thermometer zeigt „📷 Foto (1)“ (öffnet die gespeicherten Fotos); n.i.O.-Punkt ohne Foto zeigt keinen Foto-Knopf; Kommentar sichtbar, wo einer gespeichert ist |",
            "| T1.12 | Protokoll | wie bisher; T1.7-Punkt ohne Kommentar |",
            "",
            "Danach: Foto bei Id 10 wieder auf den gewünschten Wert setzen. Testdaten wie gewohnt aufräumen (Papierkorb, nur TestDatensatz = Ja).",
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
        "voraus": ["Paket 1 ist eingefügt, getestet und gespeichert."],
        "schritte": [
            dict(SICHERUNG, nr="2.1"),
            {"nr": "2.2", "titel": "SharePoint-Spalte anlegen", "text": [
                "RG_Pruefpunkte → **+ Spalte hinzufügen → Ja/Nein**: Name **KommentarPflicht**, Standardwert **Nein**.",
                "Für den Test: einen i.O./n.i.O.-Punkt in Kategorie 2 → KommentarPflicht = **Ja**.", DATEN_AKT]},
            {"nr": "2.3", "titel": "App.Formulas", "text": [EINFUEGEN, "Nur `fnKommentarNoetig` ändert sich; der Block ist trotzdem die ganze Property."]},
            {"nr": "2.4", "titel": "Kategorie öffnen", "text": ["`scrKategorie.OnVisible`: `KommentarPflicht` kommt jetzt aus der Spalte."]},
            {"nr": "2.5", "titel": "Kommentarfeld", "text": ["`conKaKarte` → `txtKaKommentar`."]},
            {"nr": "2.6", "titel": "Protokoll", "text": ["`scrProtokoll` → `conPrInhalt` → `htmProtokoll`, Property **HtmlText**."]},
            pruefung_schritt("2.7"),
        ],
        "test": [
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T2.1 | Kategorie 2 öffnen, KommentarPflicht-Punkt auf i.O. | Kommentarfeld erscheint mit „Kommentar (Pflicht)“, rot umrandet; Fuß „Noch offen (1): … (Kommentar)“ |",
            "| T2.2 | Kommentar „sauber“ eintragen | Fuß „✓ Alles ausgefüllt“ |",
            "| T2.3 | Auf n.i.O. wechseln | Hinweis „Kommentar zum Mangel (Pflicht)“, Kommentar bleibt stehen |",
            "| T2.4 | Zurück auf i.O., Speichern | „Gespeichert.“ |",
            "| T2.5 | Kategorie 2 wieder öffnen | i.O. + Kommentar „sauber“ ist da |",
            "| T2.6 | Anderer Punkt ohne KommentarPflicht: n.i.O. + Kommentar → i.O. → Speichern → wieder öffnen | Kommentar ist weg (Verhalten 08:44 bleibt) |",
            "| T2.7 | Abschluss → Protokoll | „sauber“ grau kursiv beim i.O.-Punkt; Mängel nur für n.i.O. |",
            "| T2.8 | Optionaler Punkt mit KommentarPflicht unbeantwortet lassen | kein Kommentar verlangt |",
        ],
        "rueck": [
            "- Version wiederherstellen oder die Vorher-Blöcke einfügen (App.Formulas zuletzt).",
            "- Die Spalte darf bleiben. Gespeicherte i.O.-Kommentare bleiben im JSON und erscheinen nach dem Rückweg im Protokoll rot (alte Darstellung).",
        ],
    },
    3: {
        "titel": "Zahlengrenzen pro Prüfpunkt: Mangel, Warnen oder Sperren",
        "datei": "Grenzen",
        "kurz": [
            "Neue Auswahlspalte **Grenzmodus** am Prüfpunkt: Mangel (Standard = wie heute), Warnen, Sperren.",
            "**Mangel:** Wert außerhalb Min/Max → n.i.O., Kommentar Pflicht, Mangel beim Abschluss (unverändert).",
            "**Warnen:** Wert außerhalb → orange Hinweis „außerhalb, bitte begründen“, Kommentar Pflicht, Bewertung i.O., **kein** Mangel.",
            "**Sperren:** Wert außerhalb → rot „unzulässig, bitte prüfen“, Speichern geht erst mit einem Wert im Bereich (für Tippfehler-Grenzen).",
            "Annahme (bitte bestätigen): „Warnen“ verlangt eine Begründung, weil Josias Kontrollen statt Abkürzungen will.",
        ],
        "voraus": ["Paket 1 und 2 sind eingefügt und getestet."],
        "schritte": [
            dict(SICHERUNG, nr="3.1"),
            {"nr": "3.2", "titel": "SharePoint-Spalte anlegen", "text": [
                "RG_Pruefpunkte → **+ Spalte hinzufügen → Auswahl**: Name **Grenzmodus**, Auswahlmöglichkeiten **Mangel**, **Warnen**, **Sperren**, Standardwert **Mangel**, keine Mehrfachauswahl.",
                "Für den Test: drei Zahl-Prüfpunkte mit Min/Max (oder einen nacheinander umstellen): Grenzmodus Mangel / Warnen / Sperren.", DATEN_AKT]},
            {"nr": "3.3", "titel": "App.Formulas", "text": [EINFUEGEN, "Neu: Farben clrWarnung/clrWarnungHell, fnGrenzmodus; geändert: fnZahlBewertung, fnKommentarNoetig, fnFehltGrund."]},
            {"nr": "3.4", "titel": "Kategorie öffnen", "text": ["`scrKategorie.OnVisible`: Grenzmodus aus der Spalte, Bewertung gespeicherter Zahlen mit dem Grenzmodus."]},
            {"nr": "3.5", "titel": "Anzeige am Zahlenfeld", "text": ["`conKaKarte` → `lblKaZahlInfo`, `txtKaZahl`."]},
            pruefung_schritt("3.6"),
        ],
        "test": [
            "Prüfpunkt mit Soll 6–16 °C (wie T11 im Testprotokoll).",
            "",
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T3.1 | Grenzmodus Mangel: 18,5 eingeben | wie heute: rot „außerhalb des Sollbereichs“, Kommentar Pflicht, Karte rot |",
            "| T3.2 | Grenzmodus Warnen: 18,5 | orange „außerhalb, bitte begründen“, Rahmen orange, Kommentarfeld „Kommentar (Pflicht)“, Karte **nicht** rot umrandet |",
            "| T3.3 | Kommentar „Fühler defekt“, Speichern | „Gespeichert.“ |",
            "| T3.4 | Grenzmodus Sperren: 18,5 | rot „unzulässig, bitte prüfen“, Fuß „Noch offen (1): … (unzulässiger Wert)“, Speichern springt zum Punkt |",
            "| T3.5 | 12 eingeben | Hinweis weg, Speichern möglich |",
            "| T3.6 | Grenzwert genau 6 | im Bereich (i.O.) |",
            "| T3.7 | Abschluss → Protokoll und RG_Maengel | Mangel nur für T3.1; T3.3 als i.O. mit grauem Kommentar |",
            "| T3.8 | Grenzmodus leer lassen (alter Punkt) | wie Mangel |",
        ],
        "rueck": ["- Version wiederherstellen oder Vorher-Blöcke einfügen (App.Formulas zuletzt). Spalte darf bleiben."],
    },
    4: {
        "titel": "Bedingte Fragen",
        "datei": "Bedingung",
        "kurz": [
            "Zwei neue Spalten am Prüfpunkt B: **BedingungPunkt** (Id von Punkt A, gleiche Kategorie) und **BedingungWert** (z. B. NIO, IO, ein Auswahlwert, oder * = irgendeine Antwort).",
            "B erscheint und wird verlangt nur, wenn A den Wert hat. Sonst ist B unsichtbar, zählt nicht als offen und bekommt keine Fotos hochgeladen.",
            "Beim Speichern leert die App ausgeblendete Punkte und merkt sie im JSON als `Ausgeblendet` – keine Mängel, im Protokoll und in der Nur-Ansicht nicht sichtbar.",
            "Fehlkonfiguration fällt sicher aus: A fehlt, A ist selbst bedingt (Kette) oder BedingungWert ist leer → B wird immer gezeigt.",
            "Zähler (x von y ausgefüllt, Balken, n.i.O.-Zahl, Noch offen, Sprung) zählen nur sichtbare Punkte.",
        ],
        "voraus": ["Pakete 1–3 eingefügt und getestet."],
        "schritte": [
            dict(SICHERUNG, nr="4.1"),
            {"nr": "4.2", "titel": "SharePoint-Spalten anlegen", "text": [
                "RG_Pruefpunkte:",
                "- **BedingungPunkt** – Zahl, 0 Dezimalstellen, Standardwert **0** (0 = keine Bedingung)",
                "- **BedingungWert** – Einzelne Textzeile, Standardwert leer",
                "Für den Test in Kategorie 1: neuer Prüfpunkt „ZZ Test Folgefrage Ursache“ (IONIO oder TEXT, Pflicht = Ja), BedingungPunkt = Id eines i.O./n.i.O.-Punkts derselben Kategorie (Punkt A), BedingungWert = **NIO**.",
                DATEN_AKT]},
            {"nr": "4.3", "titel": "App.Formulas", "text": [EINFUEGEN, "Neu: fnBedPasst, fnSichtbar."]},
            {"nr": "4.4", "titel": "Kategorie öffnen", "text": ["`scrKategorie.OnVisible`: Felder BedID, BedWert, Ausgeblendet; Start-Sprung auf den ersten sichtbaren Punkt."]},
            {"nr": "4.5", "titel": "Galerie und Zähler", "text": []},
            {"nr": "4.6", "titel": "Speichern", "text": ["`btnKaSpeichern.OnSelect`: Ausgeblendete leeren und markieren (vor dem Foto-Upload), Upload nur sichtbare, JSON mit `Ausgeblendet`."]},
            {"nr": "4.7", "titel": "Protokoll", "text": ["`htmProtokoll.HtmlText`: ausgeblendete Zeilen weglassen."]},
            pruefung_schritt("4.8"),
        ],
        "test": [
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T4.1 | Kategorie 1 öffnen | Folgefrage ist **nicht** zu sehen; Kopf „… von N ausgefüllt“ zählt sie nicht |",
            "| T4.2 | Punkt A auf n.i.O. | Folgefrage erscheint (unter ihrer Reihenfolge), Fuß zählt sie als offen |",
            "| T4.3 | Folgefrage beantworten, A zurück auf i.O. | Folgefrage verschwindet, Fuß „✓ Alles ausgefüllt“ (wenn sonst alles da) |",
            "| T4.4 | A wieder n.i.O. | Folgefrage kommt mit der eingegebenen Antwort zurück (noch nicht gespeichert, also nicht verloren) |",
            "| T4.5 | A auf i.O., Speichern, Kategorie wieder öffnen, A auf n.i.O. | Folgefrage leer (beim Speichern geleert) |",
            "| T4.6 | A n.i.O. + Kommentar, Folgefrage beantworten, Speichern | gespeichert, Folgefrage im JSON mit `Ausgeblendet:false` |",
            "| T4.7 | Abschluss → Protokoll | Folgefrage steht bei T4.6-Stand drin; bei ausgeblendeter Folgefrage fehlt die Zeile |",
            "| T4.8 | BedingungWert leeren | Folgefrage immer sichtbar (sicherer Ausfall) |",
            "| T4.9 | Alte gespeicherte Kategorie (vor Paket 4) ansehen | unverändert (JSON ohne `Ausgeblendet` gilt als sichtbar) |",
        ],
        "rueck": [
            "- Version wiederherstellen oder Vorher-Blöcke einfügen (App.Formulas zuletzt).",
            "- JSON mit `Ausgeblendet` stört die alte App nicht (Feld wird ignoriert); ausgeblendete Punkte stehen dann als leere Zeilen im Protokoll.",
            "- Spalten dürfen bleiben; vor dem Rückweg BedingungPunkt der Testpunkte auf 0 setzen.",
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
        "voraus": ["Pakete 1–4 eingefügt und getestet."],
        "schritte": [
            dict(SICHERUNG, nr="5.1"),
            {"nr": "5.2", "titel": "SharePoint: Auswahlwerte ergänzen", "text": [
                "RG_Pruefpunkte → Spalte **Eingabetyp** → Spalteneinstellungen → Bearbeiten → Auswahlmöglichkeiten **ergänzen** (nichts umbenennen oder löschen): **MEHRFACH**, **DATUM**, **DATUMZEIT**. Standardwert unverändert lassen.",
                "Für den Test in Kategorie 1: drei neue Prüfpunkte (Pflicht = Ja): „ZZ Test Mängelarten“ MEHRFACH mit Auswahlwerte `Riss;Leck;Korrosion`, „ZZ Test Datum letzte Wartung“ DATUM, „ZZ Test Ablesezeit“ DATUMZEIT.",
                DATEN_AKT]},
            {"nr": "5.3", "titel": "App.Formulas", "text": [EINFUEGEN, "fnFehltGrund kennt die neuen Typen, neu: fnDatumText."]},
            {"nr": "5.4", "titel": "Datum und Uhrzeit (YAML)", "text": [
                "In der Strukturansicht in `conKaKarte` das Steuerelement `txtKaText` markieren, dann den YAML-Block mit **Strg+V** einfügen "
                "(landet in derselben Karte). Drei Blöcke nacheinander oder zusammen."],
             "yaml": ["dpKaDatum", "ddKaStunde", "ddKaMinute"],
             "pruefen": ["Alle drei liegen in `conKaKarte` (Strukturansicht).",
                         "Y steht als Formel `54 + If(ThisItem.Hinweis <> \"\"; 24; 0)` da, nicht als Zahl (E-05) – sonst per Formelleiste setzen.",
                         "Die Namen sind genau `dpKaDatum`, `ddKaStunde`, `ddKaMinute` (Studio hängt bei Doppelungen „_1“ an)."]},
            {"nr": "5.5", "titel": "Mehrfachauswahl (Kombinationsfeld über das Menü)", "text": [
                "Für das klassische Kombinationsfeld kenne ich die Steuerelement-Version in dieser Umgebung nicht sicher, deshalb ohne YAML:",
                "1. Strukturansicht: `conKaKarte` markieren.",
                "2. **Einfügen → Eingabe → Kombinationsfeld** (klassisch). Es muss **in** `conKaKarte` landen.",
                "3. Umbenennen in **cboKaMehrfach**.",
                "4. Die folgenden Properties setzen (je ganze Property ersetzen):"],
             "einzeln": ["cboKaMehrfach"],
             "pruefen": ["`cboKaMehrfach` liegt in `conKaKarte`.", "Y ist eine Formel (E-05)."]},
            pruefung_schritt("5.6"),
        ],
        "test": [
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T5.1 | Kategorie 1 öffnen | Mängelarten: Kombinationsfeld „Auswählen (mehrere möglich)“; Datum: Datumsauswahl; Ablesezeit: Datum + zwei Listen (Stunde, Minute). Andere Typen unverändert |",
            "| T5.2 | Nichts davon ausfüllen | Fuß zählt alle drei als offen |",
            "| T5.3 | Riss und Leck wählen | Fuß zählt Mängelarten nicht mehr |",
            "| T5.4 | Datum letzte Wartung wählen | erledigt |",
            "| T5.5 | Ablesezeit: nur Datum | „… (Uhrzeit)“ im Fuß |",
            "| T5.6 | Stunde 07, Minute 05 | erledigt |",
            "| T5.7 | Ablesezeit: erst Stunde/Minute, dann Datum | ergibt „TT.MM.JJJJ 07:05“, erledigt |",
            "| T5.8 | Speichern, Kategorie wieder öffnen | alle drei Werte stehen wieder da (Kombinationsfeld mit Riss, Leck) |",
            "| T5.9 | Abschluss → Protokoll | „Riss; Leck“, „27.10.2026“, „27.10.2026 07:05“ in der Wertspalte; keine Mängel durch diese Punkte |",
            "| T5.10 | Ansehen nach Abschluss | Werte sichtbar, nicht änderbar |",
        ],
        "rueck": [
            "- Version wiederherstellen, oder: die vier neuen Steuerelemente löschen und App.Formulas aus dem Anhang einfügen.",
            "- Prüfpunkte mit den neuen Typen vorher deaktivieren (die alte App kennt die Typen nicht und würde sie nicht anzeigen, aber Pflicht-Prüfung würde sie nicht verlangen).",
        ],
    },
    6: {
        "titel": "Hinweis mit Beispielbild",
        "datei": "Beispielbild",
        "kurz": [
            "Neue Bildbibliothek **RG_Hinweisbilder** und neue Zahlspalte **HinweisBildID** am Prüfpunkt (Id des Bilds in der Bibliothek, 0 = keins).",
            "Hat ein Punkt ein Bild, steht rechts oben in der Karte „Beispielbild“. Tippen öffnet ein Fenster mit dem Bild in voller Breite.",
            "Statt „in der Karte aufklappen“ (Übergabe) ein Fenster: größeres Bild auf dem Tablet, keine wechselnde Kartenhöhe (Falle E-05). Bitte bestätigen.",
            "Das Bild wird erst beim Öffnen geladen (eine Abfrage), nicht für jede Karte.",
            "Vorab-Test (Schritt 6.3) klärt, ob die Vorschaubilder der Bibliothek in der App ankommen; sonst Abbruch ohne Änderung.",
        ],
        "voraus": ["Pakete 1–5 eingefügt und getestet."],
        "schritte": [
            dict(SICHERUNG, nr="6.1"),
            {"nr": "6.2", "titel": "SharePoint: Bibliothek und Spalte", "text": [
                "IMS+ → Neu → **Dokumentbibliothek** „**RG_Hinweisbilder**“. Rechte wie die anderen RG-Bibliotheken (alle lesen). Ein Testbild hochladen (JPG/PNG), dessen **ID** notieren (Ansicht → Spalte ID einblenden).",
                "RG_Pruefpunkte → **+ Spalte → Zahl**: **HinweisBildID**, 0 Dezimalstellen, Standardwert **0**.",
                "Für den Test: Prüfpunkt Id 10 → HinweisBildID = ID des Testbilds."]},
            {"nr": "6.3", "titel": "Datenquelle und Vorab-Test", "text": [
                "Studio → **Daten → Daten hinzufügen → SharePoint → IMS+ → RG_Hinweisbilder** (die bestehende SharePoint-Verbindung wird benutzt, kein neuer Berechtigungsdialog erwartet; falls doch einer kommt: abbrechen und mir Bescheid geben). Danach `RG_Pruefpunkte` aktualisieren.",
                "Vorab-Test: auf `scrKategorie` vorübergehend ein Bild-Steuerelement einfügen, Image = `LookUp(RG_Hinweisbilder; ID = <Test-ID>).Thumbnail.Large`. Zeigt es das Bild → weiter. Zeigt es nichts → **Abbruch**, Bild-Steuerelement löschen, mir Bescheid geben (Ausweg: Bildspalte in RG_Pruefpunkte). Teststeuerelement danach löschen."]},
            {"nr": "6.4", "titel": "Kategorie öffnen", "text": ["`scrKategorie.OnVisible`: Feld BildID, Fenster beim Öffnen zu."]},
            {"nr": "6.5", "titel": "Knopf in der Karte", "text": [
                "`lblKaFrage.Width` ersetzen. Dann in `conKaKarte` `txtKaText` markieren und den YAML-Block einfügen."],
             "yaml": ["btnKaBild"],
             "pruefen": ["`btnKaBild` liegt in `conKaKarte`, Y = 10, Höhe 34 (endet über `lblKaHinweis` bei Y 46)."]},
            {"nr": "6.6", "titel": "Bildfenster", "text": [
                "Den Bildschirm `scrKategorie` in der Strukturansicht markieren und den YAML-Block einfügen. `conKaBild` muss in der Strukturansicht **ganz oben** stehen (vor `conKaFoto` und `conKaLaden`), sonst per Rechtsklick → **Nach vorne bringen**."],
             "yaml": ["conKaBild"],
             "pruefen": ["Beim Einfügen eines Containers bleiben die Kinder in ihm (Strukturansicht prüfen)."]},
            pruefung_schritt("6.7"),
        ],
        "test": [
            "| # | Klickfolge | erwartet |",
            "|---|---|---|",
            "| T6.1 | Kategorie 1 öffnen | Thermometer-Karte: rechts oben „Beispielbild“, Fragetext läuft nicht darunter |",
            "| T6.2 | „Beispielbild“ tippen | Fenster mit Titel „Beispiel – …“ und Bild; Rest der App nicht tippbar |",
            "| T6.3 | „Schließen“ | Fenster zu |",
            "| T6.4 | Fenster offen lassen, Bildschirm wechseln (Zurück) und Kategorie wieder öffnen | Fenster ist zu |",
            "| T6.5 | Punkt ohne Bild | kein Knopf |",
            "| T6.6 | Nur-Ansicht nach Abschluss | Knopf vorhanden, Bild lässt sich ansehen |",
            "| T6.7 | HinweisBildID auf eine nicht vorhandene Id | Fenster öffnet, Bildfläche leer (kein Absturz) |",
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
            ("fnFehlt / fnFehltGrund", "ja", "neue Regel „Foto“ (nur bei FotoModus Pflicht und 0 Fotos); alte Regeln zeichengleich übernommen, Rückwärtsgleichheit für alle 1.296 alten Kombinationen belegt"),
            ("btnKaSpeichern: Prüfung und Sprung", "ja", "Prüfung über lblKaFehlendAnzahl (enthält jetzt Foto-Pflicht), Sprung mit derselben Regel"),
            ("JSON-Aufbau (varAntwortJSON)", "nein", "ShowColumns unverändert, kein neues Feld im JSON"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein", "liest nur NIO-Zeilen aus dem JSON, unverändert"),
            ("htmProtokoll", "nein", ""),
            ("Foto-Upload (btnKaSpeichern F1/F2)", "ja", "Bedingung `a.Bewertung = \"NIO\" || a.FotoModus <> \"Aus\"` statt LookUp(colPP).FotoMoeglich, an allen 3 Stellen (Upload, Fehlerzählung, Meldung)"),
            ("Lesemodus nach Abschluss", "ja", "Foto-Knopf nur bei gespeicherten Fotos; Kommentar sichtbar, wenn gespeichert oder n.i.O."),
            ("Nachlese-Vergleich", "nein", "unverändert, JSON gleich aufgebaut"),
            ("Kommentar leeren (08:44)", "ja", "Bedingung über fnKommentarNoetig, in Paket 1 gleiches Ergebnis wie `Bewertung <> \"NIO\"` (Logik-Probe)"),
            ("Kartenhöhe, lblKaAbstand", "ja", "Zeile unter der Eingabe erscheint, wenn Kommentar oder Foto-Knopf sichtbar ist; Abstand folgt der Kartenhöhe (vorher fehlte er bei Foto ohne n.i.O.)"),
            ("Foto-Zähler btnKaFoto.Text", "ja", "zählt neue Fotos ohne `Uebernommen` + gespeicherte Links; vorher doppelt gezählt nach fehlgeschlagenem Speichern"),
        ],
        "e": [
            ("neuer Punkt ohne Daten", "FotoModus aus der Spalte; bei Pflicht „(Foto)“ offen, sonst wie bisher", "Logik-Probe P1, T1.1–T1.3"),
            ("alter gespeicherter Punkt (JSON ohne neues Feld)", "JSON hat kein Foto-Feld, FotoModus kommt aus den Stammdaten; gespeicherte Links zählen als Fotos (Pflicht erfüllt)", "OnVisible Bearbeiten-Zweig, fnLinkAnzahl, T1.9"),
            ("inaktiver Punkt", "FotoModus \"Aus\", ausgeblendet, zählt nicht (Filter `!Inaktiv`), Foto-Pflicht greift nicht", "Code"),
            ("Rundgang abgeschlossen (Nur-Lesen)", "keine Pflicht-Prüfung, Foto-Knopf nur mit gespeicherten Fotos, keine Uploads", "Code, T1.11"),
            ("Wechsel n.i.O. → i.O. → n.i.O.", "Foto-Knopf rot → (bei Aus) verschwindet / (bei Optional/Pflicht) blau → rot; schon gewählte Fotos bleiben in colFotos; Upload nur, wenn beim Speichern n.i.O. oder Modus ≠ Aus", "Code, T1.6"),
            ("Kategorie zweimal speichern", "zweites Mal: gespeicherte Links zählen, kein erneuter Upload (Uebernommen/Url), keine Doppelungen", "Code F1/F2 unverändert, T1.9"),
            ("Abbruch mitten im Speichern", "Upload fertig, Patch nicht: Links stehen schon in colAntworten, Fotos `Uebernommen` → erneutes Speichern lädt nicht doppelt hoch; Pflicht bleibt erfüllt", "Code"),
            ("Netzfehler", "Upload-Fehler → Meldung „x Foto(s) konnten nicht hochgeladen werden“, Kategorie nicht gespeichert; Pflicht zählt das nicht hochgeladene Foto, erneutes Tippen lädt nach. Grenze: Flow ohne Rückmeldung (siehe Offene Befunde)", "Code"),
            ("zwei Prüfer gleichzeitig", "unverändert: GespeichertAm-Vergleich lehnt das zweite Speichern ab; Fotos des zweiten bleiben unhochgeladen", "Code"),
            ("Foto Pflicht + Punkt nicht Pflicht und unbeantwortet", "Foto trotzdem verlangt (Pflicht = Nachweis)", "Logik-Probe"),
            ("FotoMoeglich Ja, Foto leer", "Optional", "Logik-Probe, T1.10"),
        ],
        "f": FALLEN_ALLG + [
            "Y in Galerien friert beim YAML-Einfügen ein: Paket 1 fügt kein YAML ein, alle Werte per Formelleiste. Nach Schritt 1.6 trotzdem `btnKaFoto.Y` prüfen.",
            "Zwischenablage: Länge des kopierten Blocks prüfen (Lehre 27.10.: alter Inhalt eingefügt → 35 Fehler).",
            "Ebenenreihenfolge ✕/Bild: nicht über „Nach vorne“ gelöst, sondern über Lage (Bild beginnt bei Y 52), damit es unabhängig von der Reihenfolge stimmt.",
        ],
        "g": [
            "- Nicht automatisch ausführbar: Formeln in Studio, Foto-Auswahl, Upload. Testfolge T1.1–T1.12 im Paket, Foto-Teil (T1.5, T1.8) am Tablet durch Josias.",
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
            ("inaktiver Punkt", "KommentarPflicht false, zählt nicht", "Code"),
            ("Rundgang abgeschlossen (Nur-Lesen)", "keine Prüfung, Kommentar sichtbar wenn gespeichert", "Code"),
            ("Wechsel n.i.O. → i.O. → n.i.O.", "Kommentar bleibt im Feld; Hinweistext wechselt; beim Speichern bleibt er (Pflicht) bzw. wird bei i.O. ohne Pflicht geleert", "Logik-Probe, T2.3–T2.6"),
            ("Kategorie zweimal speichern", "Kommentar bleibt erhalten (wird beim Öffnen aus dem JSON gelesen)", "T2.5"),
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
        "c": ["1. Spalte + aktualisieren vor OnVisible.", "2. App.Formulas vor/mit OnVisible (fnGrenzmodus neu). Paket 1 (4. Parameter, Feld Grenzmodus) und Paket 2 (Hinweistext „Kommentar (Pflicht)“) müssen drin sein."],
        "d": [
            ("scrKategorie.OnVisible", "ja", "Grenzmodus aus Spalte (Bearbeiten, Nur-Ansicht über pp); Neubewertung gespeicherter Zahlen mit Grenzmodus"),
            ("fnFehlt / fnFehltGrund", "ja", "„Bereich“ bei Sperren außerhalb"),
            ("btnKaSpeichern: Prüfung und Sprung", "ja (indirekt)", "Sperren blockiert, Sprung zum Punkt"),
            ("Kommentar leeren (08:44)", "ja (indirekt)", "Warnen außerhalb behält den Kommentar"),
            ("JSON-Aufbau (varAntwortJSON)", "nein", "Bewertung IO/NIO/\"\" wie bisher; Sperren außerhalb wird nie gespeichert"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein", "nur NIO; Warnen speichert IO → kein Mangel (gewollt)"),
            ("htmProtokoll", "nein", "Warnen: i.O. + grauer Kommentar (Paket 2)"),
            ("Foto-Upload", "nein", "Bedingung NIO/FotoModus; Warnen ohne NIO lädt nur bei FotoModus ≠ Aus"),
            ("Lesemodus nach Abschluss", "ja", "Hinweistext nach Grenzmodus der heutigen Stammdaten; bei gespeichertem NIO immer „außerhalb des Sollbereichs“"),
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
            "3. Im Speichern: Ausblenden/Leeren **vor** dem Foto-Upload und **vor** dem JSON (sonst würden Fotos ausgeblendeter Punkte hochgeladen bzw. alte Werte gespeichert).",
            "4. `colVersteckt` wird im selben Klick angelegt, bevor UpdateIf sie liest.",
        ],
        "d": [
            ("scrKategorie.OnVisible", "ja", "BedID, BedWert, Ausgeblendet in allen Zweigen; Start-Sprung auf ersten sichtbaren Punkt"),
            ("fnFehlt / fnFehltGrund", "nein", "unverändert; Aufrufer filtern vorher auf sichtbar"),
            ("btnKaSpeichern: Prüfung und Sprung", "ja", "Prüfung über lblKaFehlendAnzahl (nur sichtbare), Sprung nur auf sichtbare"),
            ("JSON-Aufbau (varAntwortJSON)", "ja", "neues Feld Ausgeblendet; ausgeblendete Punkte mit leeren Werten"),
            ("Mängel bei Abschluss (btnRuAbschluss)", "nein (Formel)", "ausgeblendete haben Bewertung \"\" → keine Mängel; AnzahlNIO zählt nach dem Leeren → Plausibilität Sum(AnzahlNIO) = Mängel stimmt"),
            ("htmProtokoll", "ja", "ausgeblendete Zeilen weggelassen"),
            ("Foto-Upload (btnKaSpeichern F1/F2)", "ja", "nur sichtbare (`!a.Ausgeblendet`) an allen 3 Stellen"),
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
            ("Abbruch mitten im Speichern", "Leeren ausgeblendeter Punkte ist schon passiert (nur unsichtbare Werte); erneutes Speichern konsistent", "Code"),
            ("Netzfehler", "unverändert (Nachlese)", "Code"),
            ("zwei Prüfer gleichzeitig", "unverändert (GespeichertAm)", "Code"),
            ("Fehlkonfiguration (A fehlt, Kette, leerer Wert)", "B sichtbar und verlangt", "Logik-Probe"),
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
            ("Bedingungen (Paket 4)", "ja (indirekt)", "fnBedPasst prüft Werte der Mehrfachauswahl einzeln"),
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
