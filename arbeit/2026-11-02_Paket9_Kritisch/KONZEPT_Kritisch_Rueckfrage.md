# Paket 9 – Kritischer Mangel und Rückfrage (Konzept, 02.11.2026)

Wunsch von Josias (02.11.): Ist ein n.i.O. sehr ernst, soll eine Meldung erscheinen, die man nicht übersehen kann („sofort Bescheid geben“). Dazu eine Rückfrage „Ist es wirklich so? Normalerweise ist es …“.

**Entscheidungen von Josias (02.11.):**
- **Keine automatische Benachrichtigung.** Die App sagt nur, bei wem man sich melden soll.
- Ansprechpartner sind pflegbar: Namen oder Gewerke (z. B. „Allgemein“, „Elektriker“, „IT-Dienstleister“). Bei n.i.O. zeigt die App die Personen an, die für diesen Prüfpunkt ausgewählt sind.
- Rückfrage und kritische Meldung sind **getrennt einstellbar** (je Prüfpunkt: nur Rückfrage, nur kritisch, beides).
- Die Bestätigung kommt ins Protokoll/PDF.
- Reihenfolge: nach Paket 8 (Abschnitte), als Paket 9.

## Daten

| Liste | Spalte | Typ | Zweck |
|---|---|---|---|
| **`RG_Ansprechpartner`** (neu) | `Title` | Text | Gewerk/Rolle, z. B. „Elektriker“ |
| | `Name` | Text | Person oder Firma |
| | `Telefon` | Text | |
| | `Hinweis` | mehrzeilig | z. B. „außerhalb 7–16 Uhr: Bereitschaft …“ |
| | `Allgemein` | Ja/Nein | wird bei **jedem** kritischen Mangel mit angezeigt |
| | `Aktiv` | Ja/Nein | |
| `RG_Pruefpunkte` | `Kritisch` | Ja/Nein | n.i.O. löst die kritische Meldung aus |
| | `KritischText` | Text | z. B. „Anlage nicht weiter betreiben.“ |
| | `Ansprechpartner` | Text | IDs aus `RG_Ansprechpartner`, mit `;` getrennt |
| | `Rueckfrage` | Ja/Nein | n.i.O. löst zuerst die Rückfrage aus |
| | `RueckfrageText` | Text | z. B. „Normalerweise 6–8 bar.“ Leer bei Zahl: Text aus den Grenzen |

Text-IDs statt Lookup: Das ist einfacher zu kopieren (Builder) und kommt ohne Mehrfach-Lookup aus. Die Ansprechpartner-Liste ist nicht an Fassungen gebunden. Änderungen an Telefonnummern gelten sofort.

## Ablauf in der Rundgang-App (Prüfer)

1. Der Prüfer setzt n.i.O. (Knopf, oder Zahl außerhalb der Grenzen mit Modus „Mangel“).
2. **Rückfrage** (wenn eingestellt): Fenster mit der Frage, „Ist das wirklich so?“, dem Text oder den Grenzen und dem eingegebenen Wert. Knöpfe:
   - „Ja, stimmt“: weiter mit Schritt 3
   - „Nein, korrigieren“: die Antwort wird zurückgenommen (bei i.O./n.i.O. leer, bei einer Zahl wird das Feld geleert)
3. **Kritische Meldung** (wenn eingestellt): rotes Vollbild-Fenster, das man nicht wegklicken kann. Inhalt: „Kritischer Mangel – sofort melden“, die Frage, `KritischText` und die Ansprechpartner (zuerst die zugeordneten, dann die allgemeinen) mit Name, Telefon und Hinweis. Ein einziger Knopf: „Ich habe Bescheid gegeben“. Er speichert in der Antwort `KritischOk` = true und `KritischZeit`.
4. Speichern der Kategorie: Ein kritischer Mangel ohne Bestätigung zählt als **fehlend**. Das fängt den Fall ab, dass die App zwischendurch geschlossen wurde. Ein Tipp auf „fehlt“ öffnet das Fenster erneut.
5. Protokoll/PDF: Beim Mangel steht „KRITISCH – Bescheid gegeben, bestätigt von <Prüfer> um hh:mm“. In `RG_Maengel` kommt ein Präfix „KRITISCH:“ in den Kommentar (keine neue Spalte nötig, UNSICHER, ob ihr eine eigene Spalte wollt).

## Builder

- Prüfpunkt: neuer Bereich „Bei n.i.O.“ mit Schalter „Rückfrage“ + Text, Schalter „kritisch“ + Text + Mehrfachauswahl der Ansprechpartner. Platz: In `conEdP` ist kein Platz mehr frei. Deshalb kommt **eine zweite Seite** im Prüfpunkt-Editor mit zwei Reitern: „Grunddaten“ und „Bei n.i.O.“.
- Neuer Bildschirm **„Ansprechpartner“** (aus der Übersicht): Liste anlegen, ändern, deaktivieren. Ansprechpartner werden nie gelöscht, nur deaktiviert, weil alte Rundgänge auf sie zeigen.
- Kopie, Fassungen, Änderungsliste und Datenvertrag: die 5 neuen Spalten. `Ansprechpartner` wird **nicht** umgeschrieben (zeigt auf eine Liste ohne Fassungen).
- Prüfregeln: kritisch ohne Ansprechpartner und ohne allgemeinen Ansprechpartner → Fehler. Rückfrage bei Typ Text/Datum → Hinweis (wirkt nur bei i.O./n.i.O. und Zahl).

## Rundgang-App (Stellen, belegt im Endstand 1–7)

- `btnKaNIO.OnSelect`, `txtKaZahl.OnChange`: Auslöser (setzen `Bewertung = "NIO"`)
- `scrKategorie.OnVisible`: 3 Zweige, die `colAntworten` füllen → neue Felder `Kritisch`, `KritischOk`, `KritischZeit`, `Rueckfrage`, `RueckfrageText`, `KritischText`, `Ansprechpartner` in **allen** Zweigen (Datensatz-Regel)
- `fnFehlt` (App.Formulas) + alle Aufrufe: Argument für „kritisch, nicht bestätigt“
- `btnKaSpeichern.OnSelect`: JSON um `KritischOk`/`KritischZeit` erweitern
- `btnRuAbschluss.OnSelect` (Mängel), `htmProtokoll.HtmlText` (Protokoll)
- 2 neue Fenster auf `scrKategorie` (Rückfrage, kritisch), Datenquelle `RG_Ansprechpartner`

## Voraussetzung

Ein frischer Export der Rundgang-App (vorher veröffentlichen). Ohne ihn baue ich die Rundgang-App-Seite nicht, weil die Anker exakt passen müssen.
