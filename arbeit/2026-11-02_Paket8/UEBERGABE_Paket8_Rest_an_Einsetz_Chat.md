# Übergabe: Rest von Paket 8 (Builder) an den Einsetz-Chat – 02.11.2026

Von: Engineering-Chat. Repo `Josias-As/Rundgang-DEV-More-App-reverse-engeneering`, Branch `claude/upbeat-tesla-emx06l`.
Aufgabe: Josias die noch offenen Schritte von **Paket 8 (Teil Builder)** zum Einfügen ausgeben, Gruppe für Gruppe. Du baust nichts neu und änderst keine Formeln.

## 1. Worum es geht
App: **„Rundgang Builder“** (zweite Canvas-App, Tablet quer 1366 × 768, Bildschirme `scrListe`, `scrEditor`, `scrPlan`). Damit pflegt Josias die Rundgänge der App „Rundgang DEV“.
Paket 8 bringt **Abschnitte** (Prüfpunkte einer Kategorie gruppieren, z. B. „Kompressor 1“, Spalte `RG_Pruefpunkte.Abschnitt`) und **Bereich ausblenden** (Spalte `RG_Bereiche.Ausblenden`).

## 2. Was schon drin ist (laut Josias, 02.11.)
- Schritt 0: SharePoint-Spalten `Abschnitt` (Eine Textzeile) und `Ausblenden` (Ja/Nein, Standard Nein), Datenquellen aktualisiert
- Schritt 1: neue Steuerelemente `lblPAbschnitt`, `txtPAbschnitt` (in `conPRest`), `lblBZeigen`, `galBZeigen` (in `conEdB`), `lblMehrAbschnitt`, `txtMehrAbschnitt` (in `conMehrKarte`)

Nicht ausdrücklich bestätigt: ob `conEdP.X` auf **16** steht (nach einem Ausschneiden/Einfügen stand es auf 32). Bitte als Erstes kurz mitgeben: `scrEditor › conEdMitte › conEdP` → X = `16`.

## 3. Was du ausgeben sollst
Quelle: **`pakete/builder/PAKET_8_BUILDER.md`**, Abschnitte „Schritt 2“ bis „Schritt 5“. Gleicher Inhalt maschinenlesbar in `arbeit/2026-11-02_Paket8/gruppen.json` (Felder `pfad`, `de` = Text zum Kopieren, `diff`, `erkl`). **Blöcke zeichengenau übernehmen, nichts umformulieren, nichts kürzen.**

| Nachricht | Schritt | Properties |
|---|---|---|
| 1 | 2 – Optik und kleine Werte | 11 (meist Zahlen, dazu 4 kurze Texte) |
| 2 | 3 – Anzeige des Abschnitts | `galGl.Items`, `galHolen.Items`, `lblVsListe.Text`, `galAkt.Items`, `btnMehrAnlegen.OnSelect` |
| 3 | 4 – Auswahl wechseln | `btnGlZeile`, `btnGlNeuB`, `btnGlNeuK`, `btnGlNeuP`, `btnPrZeile` (je OnSelect), `ddKBereich.OnChange`, `ddPKategorie.OnChange` |
| 4 | 5a – `btnEdEntf.OnSelect` | 1 lange Formel |
| 5 | 5b – `galPr.Items` | 1 lange Formel (ersetzt die ganze Prüfliste) |
| 6 | 5c – `tmrArbeit.OnTimerEnd` | 1 sehr lange Formel (~17.500 Zeichen) |
| 7 | Abschluss | App-Prüfung → Formeln = 0, speichern, veröffentlichen, Export hochladen (siehe 6) |

Lange Formeln je einzeln, damit nichts abgeschnitten wird.

## 4. Lieferstil (Josias mag ihn, genau so)
Josias antwortet nur „next“ oder „ok“. Je Property:
1. Überschrift mit Schritt, z. B. „Schritt 3.1 · `galGl.Items`“
2. **Pfad** aus dem Dokument (`scrEditor › conEdGl › galGl`) und wie man hinkommt: in der Strukturansicht markieren, oben links die Property wählen, in der Formelleiste alles ersetzen
3. **Text zum Kopieren:** ein Codeblock mit der ganzen Property (deutsch, `;`/`;;`), ohne `=`, ohne Kommentare
4. **Das ändert sich:** der ```diff-Block aus dem Dokument
5. **Kurz erklärt:** 1–2 Sätze (im Dokument „Kurz erklärt“)
6. **Nachprüfen:** das Ende der Formel (steht im Dokument)
7. Am Schluss: „Schreib ‚next‘ für Schritt …“ und der Fortschritt ehrlich in Prozent (Schritt 2 ≈ 35 %, 3 ≈ 50 %, 4 ≈ 70 %, 5a ≈ 80 %, 5b ≈ 90 %, 5c ≈ 100 %)

Kurz und auf Deutsch, keine langen Erklärungen.

## 5. Was rot werden darf und was nicht
- Seit Schritt 0+1 gibt es alle Namen. **Rot wird nichts erwartet.**
- Wird `Abschnitt` oder `Ausblenden` rot: Die Spalte fehlt oder die Datenquelle ist nicht aktualisiert (Daten → Liste → ⋯ → Aktualisieren).
- Wird `txtPAbschnitt` rot: Schritt 1a fehlt.
- **Syntaxfehler** wie „Eof“ oder „unerwartetes Zeichen“ am Ende: Beim Kopieren wurde abgeschnitten. Lass Josias den Block mit dem Kopier-Knopf neu kopieren. Nicht von Hand reparieren lassen.
- **Nie** eine Formel selbst abändern. Passt etwas nicht, schreib die genaue Meldung, die Stelle und einen Screenshot-Hinweis in eine Notiz für den Engineering-Chat (Abschnitt 7).

## 6. Wichtige Regeln aus der Arbeit am Builder
- Zeitgeber laufen in Studio nur in der **Vorschau (F5)**, nicht bei Alt+Klick.
- In einen Container fügt man ein, indem man **den Container selbst** markiert und Strg+V drückt. (Markiert man ein Kind, landet es daneben, und markiert man einen anderen Container, landet es darin.)
- Ein Export enthält die **zuletzt veröffentlichte** Fassung. Vor dem Export veröffentlichen. Der Builder ist mit niemandem geteilt, Veröffentlichen ist gefahrlos.
- Josias darf Optik selbst ändern (er hat z. B. `lblPlAb/lblPlBis.Size` auf 10 gesetzt). Lass ihn sagen, was er geändert hat, und notiere es.

## 7. Wenn du fertig bist
Gib Josias diese Bitte mit:
1. App-Prüfung → **Formeln = 0**? (Bei Fehlern: Screenshot)
2. Builder **veröffentlichen** und **exportieren**, außerdem die **Rundgang-App „Rundgang DEV“ veröffentlichen und exportieren**. Beide ZIPs gehen an den Engineering-Chat. Der baut damit den Teil von Paket 8 für die Rundgang-App und Paket 9 (kritischer Mangel, Rückfrage, Ansprechpartner).
3. Eine kurze Notiz an den Engineering-Chat (Josias kopiert sie dorthin): was eingefügt ist, was rot war, was Josias selbst geändert hat.
