# Übergabe: Paket N und Paket 8–10 für die Rundgang-App an den Einsetz-Chat – 02.11.2026

Von: Engineering-Chat. Repo `Josias-As/Rundgang-DEV-More-App-reverse-engeneering`, Branch `claude/upbeat-tesla-emx06l`.
Aufgabe: Josias zwei Pakete für die App **„Rundgang DEV“** (Tablet hochkant) zum Einfügen ausgeben, Gruppe für Gruppe, **mit kurzer Erklärung je Änderung**. Du baust nichts neu und änderst keine Formel.

## 1. Was Josias wissen muss, bevor es losgeht (bitte als Erstes ausgeben, kurz)

**Warum Paket N?** Ich habe seinen Export vom 02.11. 15:41 Zeichen für Zeichen mit dem Stand verglichen, den Paket 1–7 ergeben sollten. Ergebnis:
- Paket 1, 2, 4, 6 sind fast vollständig drin, Paket 3 bis auf einen Rahmen.
- **Drei Formeln sind im falschen Steuerelement gelandet:**
  - `lblKaHinweis.Text` enthält den Foto-Hinweis. Folge: Eine Karte mit Hinweis zeigt den falschen Text.
  - `lblKaAbstand.Text` enthält die Fortschrittszeile (unsichtbar, aber falsch).
  - `lblKaZahlInfo.BorderColor` enthält den Rahmen des Zahlenfelds (unsichtbar, aber falsch).
  Dafür fehlen diese Formeln in `lblKaFotoHinweis`, `lblKaStand` und `txtKaZahl`.
- **Paket 5 fehlt ganz** (Typen Mehrfach, Datum, Datum + Uhrzeit: 5 Steuerelemente + `App.Formulas`).
- **Paket 7 fehlt** (Foto „Bei Mangel Pflicht“).
- Alles andere stimmt überein.
- Wichtig: Der Builder bietet Mehrfach/Datum und „Foto Pflicht bei Mangel“ schon an. Ohne Paket N versteht die Rundgang-App das nicht.

**Was bringt Paket 8–10?**
- **Abschnitte:** Über der ersten Frage eines Abschnitts steht eine Überschrift (z. B. „Kompressor 1“). Protokoll und Mängel nennen den Abschnitt („Kompressor 1 › Betriebsdruck“).
- **Bereich ausblenden:** Im Builder ausgeblendete Bereiche erscheinen nicht mehr als Überschrift (bei danach gestarteten Rundgängen).
- **Rückfrage:** Bei n.i.O. (oder Zahl außerhalb, Modus Mangel) fragt die App „Ist das wirklich so?“ und zeigt den normalen Wert. „Nein“ nimmt die Antwort zurück.
- **Kritischer Mangel:** rotes Vollbild-Fenster mit den Ansprechpartnern (Gewerk, Kontakt, Telefon, Hinweis). Nur „Ich habe Bescheid gegeben“ oder „war ein Versehen“. Ohne Bestätigung lässt sich die Kategorie nicht speichern. Protokoll und Mangel nennen, wer wann bestätigt hat. **Es wird nichts verschickt.**
- **Neuer Fix, Paket 10 – keine Reihenfolge-Sperre mehr:** Alle Kategorien lassen sich in beliebiger Reihenfolge öffnen und speichern. Die erste offene bleibt „▶ Als Nächstes“, die anderen heißen „○ Offen“ statt „🔒 Gesperrt“. „Speichern“ springt wie bisher zur ersten noch offenen Kategorie. „Rundgang abschließen“ geht weiterhin erst, wenn alle gespeichert sind (das prüfte der Abschluss schon, unverändert).

Geprüft: Generator 0 Fehler, Mutation 12/12, Logik 81 Szenarien, unabhängige Prüfung (14 Befunde eingearbeitet). **Nicht in Studio getestet.**

## 2. Reihenfolge und Quellen
1. **`pakete/PAKET_N_Nachholen.md`**: Schritt N.1 (SharePoint) → N.2 (3 Reparaturen) → N.3 (5 fehlende Formeln) → N.4 (`App.Formulas`) → N.5 (Paket-5-Steuerelemente, YAML + ein Kombinationsfeld über das Menü) → N.6 (App-Prüfung = 0).
2. **`pakete/PAKET_8_9_10_APP.md`**: Schritt 1 (SharePoint: neue Liste `RG_Ansprechpartner`, 5 Spalten, Datenquelle) → 2 bis 10. Jede Property kommt dort **einmal in ihrer Endfassung** vor (Paket 8, 9 und 10 zusammengefasst).
Die Blöcke **zeichengenau** übernehmen. Die Erklärung „Kurz erklärt“ steht im Dokument bei jeder Property, bitte mit ausgeben.

## 3. Lieferstil (wie bisher, Josias mag ihn)
Josias antwortet „next“. Je Nachricht eine Gruppe (höchstens etwa 8 Properties, lange Formeln einzeln). Je Property:
1. Überschrift mit Schritt und `Steuerelement.Property`
2. **Pfad** (steht im Dokument) und wie man hinkommt: in der Strukturansicht markieren, Property oben links wählen, Formelleiste: alles ersetzen
3. **Text zum Kopieren:** ganze Property, deutsch, ohne `=`, ohne Kommentare
4. **Das ändert sich:** der ```diff-Block aus dem Dokument
5. **Kurz erklärt** (aus dem Dokument)
6. **Nachprüfen:** Ende der Formel
7. Am Schluss „Schreib ‚next‘ für …“ und der Fortschritt in Prozent

YAML: **Wo hin** steht im Dokument. Regel: In einen Container fügt man ein, indem man **den Container selbst** markiert. Markiert man ein Kind, landet der Block daneben. In eine Galerievorlage fügt man ein, indem man ein Kind der Vorlage markiert (bei `lblKaAbschnitt`: `lblKaAbstand`). Danach Y/Height prüfen: Es müssen Formeln sein, keine Zahlen (Studio friert sie beim Einfügen manchmal ein).

## 4. Was rot werden darf
- Paket N: Rot ist nicht zu erwarten. Bei Paket 5 können zwischen den YAML-Blöcken kurz rote Fehler stehen, bis alle vier drin sind (steht im Dokument).
- Paket 8–10: Ab dem Schritt mit `App.Formulas` sind die Aufrufe von `fnFehlt` rot (jetzt 13 statt 12 Argumente), bis die nächsten Schritte sie ersetzen. Das steht im Dokument.
- `Kritisch`, `Abschnitt`, `Kontakt` usw. rot → Spalte fehlt oder Datenquelle nicht aktualisiert.
- Syntaxfehler (z. B. „Eof“) → beim Kopieren abgeschnitten. Mit dem Kopier-Knopf neu kopieren, nichts von Hand reparieren.
- Nie eine Formel selbst abändern. Bei Problemen genaue Meldung und Stelle notieren, das geht an den Engineering-Chat.

## 5. Achtung
- **Die Spalte `Fassung` in `RG_Pruefpunkte` heißt intern `Fassungf`. Nicht löschen, nicht umbenennen.**
- Die neue Spalte für Person/Firma in `RG_Ansprechpartner` heißt **`Kontakt`**, nicht „Name“ (den Namen benutzt SharePoint intern).
- Liste und Spalten nur **einmal** anlegen. Der Builder (Paket 9 Builder) benutzt dieselben.
- Testen in der **Vorschau (F5)**, nicht mit Alt+Klick.

## 6. Wenn du fertig bist
Gib Josias mit:
1. App-Prüfung → Formeln = 0? (Sonst Screenshot.)
2. Testbogen: Tests in `PAKET_N_Nachholen.md` und `PAKET_8_9_10_APP.md` (T1–T10, T5b/T5c). Nur mit ZZ-Test-Rundgängen.
3. **Veröffentlichen und exportieren** (ein Export enthält nur die veröffentlichte Fassung) und den Export an den Engineering-Chat schicken, damit er den Stand maschinell abgleicht.
4. Eine kurze Notiz für den Engineering-Chat: was eingefügt ist, was rot war, was Josias selbst geändert hat.
