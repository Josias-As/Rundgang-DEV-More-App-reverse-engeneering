# Rundgang-Builder: Analyse vor dem Bau

Stand 27.10.2026. Grundlage: `quellen/2026-10-27_Uebergabe/UEBERGABE_ENGINEERING.md` (Planer-Chat) und der Export `quellen/2026-10-27_Export/` (siehe `arbeit/2026-10-27_Analyse/`).
Auftrag: verstehen, noch nichts bauen. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Ziel:** Eine zweite App, der „Builder“, legt Rundgänge per Klick an: Bereiche, Kategorien, Prüfpunkte und Plan. Niemand muss dafür SharePoint-IDs kennen. Builder und Rundgang-App arbeiten auf denselben `RG_`-Listen. **Die Daten sind die Schnittstelle.**
- **Was der Builder sicherstellen muss:** Er darf nur Daten schreiben, die die Rundgang-App heute schon richtig liest (Abschnitt 2). Dazu gehören lückenlose IDs, `Aktiv`, Reihenfolge, ein gültiger Plan und mindestens 1 aktiver Prüfpunkt je Kategorie.
- **Größtes fachliches Risiko** (belegt): Die Rundgang-App liest die Prüfpunkte **live** beim Öffnen einer Kategorie. Nur die Kategorienliste ist eingefroren. Ändert jemand im Builder einen aktiven Rundgang, verändert er laufende Rundgänge mitten am Tag. Deshalb braucht der Builder einen Entwurf, bevor er an echte Rundgänge darf.
- **Empfehlung zur Reihenfolge** (geschlussfolgert, Entscheidung bei Josias/Planer): Den Umbau auf Nachschlagespalten (Plan, Schritt 2) **nicht vor** den Builder stellen. Er zwingt alle Formeln der Rundgang-App zum Umbau und braucht eine Datenübernahme. Im Builder bringt er kaum etwas, denn dort sieht ohnehin niemand die Zahlen. Kopieren geht mit Zahlen-IDs genauso (Zuordnung alt → neu).
- **Vorher klären:** 7 Fragen (Abschnitt 6) und die fehlenden Projektdateien (`FORTSCHRITT.md`, `ENTSCHEIDUNGEN.md`, `FEATURES.json`, `pakete\`) liegen nur lokal unter `C:\rundgang_work\`, nicht in diesem Repo.

## 1. Abgleich Übergabe ↔ Export
| Punkt in der Übergabe | Export | Kennzeichnung |
|---|---|---|
| Variable `varIsAdmin` | heißt `varIstAdmin` | belegt |
| Zurücksetzen „frühestens 5 Minuten nach dem Start“ | 5 Minuten nach der **letzten Änderung** (`Geändert`), nur im Status `Abschluss` | belegt |
| Textwert von `stAbschluss` „nicht erneut geprüft“ | `stAbschluss = "Abschluss"` in `App.Formulas` | belegt |
| `ThisItem.FotoMoeglich` kam aus `colAntworten` nicht an, „Ursache ungeklärt“ | **Ursache gefunden:** Im Zweig „Bearbeiten“ von `scrKategorie.OnVisible` fehlt das Feld `FotoMoeglich` im Datensatz. Nur der Zweig „Nur-Ansicht“ und die Zeilen deaktivierter Punkte setzen es. Der Notbehelf `LookUp(colPP; …)` ist richtig. Bei Auftrag 1 (Foto-Modus) das Feld gleich in alle drei Zweige aufnehmen. | belegt |
| Antwort-Aktion im Flow „wäre Premium“ | Die Aktion **„Auf eine PowerApp oder einen Flow antworten“** gehört nach meinem Wissen zum Standard. Premium ist nur „Antwort“ aus dem HTTP-Anforderungs-Connector. Wenn das stimmt, ist der stille Fehlschlag bei Foto/PDF (Befund R1) ohne Premium lösbar: Der Flow gibt den echten Dateilink zurück. | geschlussfolgert, im Flow-Editor prüfen (Premium-Raute) |
| Veröffentlicht 27.10. 08:06 | Export gespeichert 07:04 UTC = 08:04 Ortszeit, passt zur veröffentlichten Fassung | geschlussfolgert |
| Plan-Datum „als Vortag 22:00 UTC gespeichert“ | Die App liest `StartMontag` als reines Datum (Schema `format: date`). Eine Verschiebung durch die Zeitumstellung (25.10.) ist deshalb unwahrscheinlich. | UNSICHER: einen Sonntags-Plan mit Zyklus 2 nach dem 25.10. testen |

## 2. Was die Rundgang-App von den Stammdaten erwartet (Datenvertrag, belegt aus dem Export)
Diese Regeln muss der Builder einhalten. Sonst zeigt die Rundgang-App falsche oder leere Rundgänge.

| Liste | Die App liest | Folge, wenn falsch |
|---|---|---|
| `RG_Rundgaenge` | `Aktiv = true`, `Title`, `RgReihenfolge` (Sortierung Startseite) | Rundgang fehlt auf der Startseite |
| `RG_Plan` | `Aktiv = true`, `RundgangID`, `Wochentag` 1–7, `ZyklusWochen` (≥ 1, sonst als 1 behandelt), `StartMontag` (Pflicht, sonst nie fällig), `GueltigBis` (leer = unbegrenzt) | Ein leerer `StartMontag` heißt: nie geplant. Liegt `StartMontag` nicht auf einem Montag, verschiebt sich die Zykluszählung. |
| `RG_Bereiche` | `RundgangID`, `Aktiv`, `RgReihenfolge`, `Title` | Inaktiver Bereich → seine Kategorien fehlen beim Start |
| `RG_Kategorien` | `BereichID`, `Aktiv`, `RgReihenfolge`, `Title`. Sortierung beim Start = `BereichReihenfolge × 10000 + KategorieReihenfolge` | Ab `RgReihenfolge` ≥ 10000 stimmt die Sortierung nicht mehr. Ohne aktive Kategorie: „keine aktiven Kategorien“, kein Start. |
| `RG_Pruefpunkte` | `KategorieID`, `Aktiv`, `RgReihenfolge`, `Eingabetyp` (IONIO/AUSWAHL/ZAHL/TEXT), `Pflicht`, `Auswahlwerte` (getrennt durch `;`), `Einheit`, `MinWert`/`MaxWert`, `Hinweis`, `FotoMoeglich` | Hat eine Kategorie 0 aktive Prüfpunkte, kann der Prüfer sie nicht speichern → der Rundgang hängt. Ist AUSWAHL ohne Werte und Pflicht, ist der Punkt nie erfüllbar. Ist Min > Max, ist jede Zahl n.i.O. |
| `RG_Konfiguration` | `NachholTage`, `Testmodus`, `Testadresse`, `Empfaenger`, `Admins` | Konfiguration ist Teil des Builders oder bleibt eine Liste (Frage 5) |

Weitere belegte Eigenschaften:
- Wann wird was gelesen? Die Kategorienliste wird beim **Start** eingefroren (`KategorieListe`). Die Prüfpunkte werden beim **Öffnen** einer Kategorie live gelesen. Antworten zu deaktivierten Punkten laufen unsichtbar mit.
- Ein Rundgang mit Titel „ZZ Test…“ erzeugt Testdatensätze (`TestDatensatz`). Der Builder kann das als Schalter „Testrundgang“ anbieten, solange die Regel am Titel hängt.
- Die App verlangt keine lückenlose Reihenfolge. Sie sortiert nur nach `RgReihenfolge`, gleiche Werte stehen in zufälliger Folge.

## 3. Was der Builder können muss (aus Übergabe Abschnitt 7–9, gegliedert)
| Stufe | Funktion | Liste(n) | Schwierigkeit |
|---|---|---|---|
| B1 | Rundgänge auflisten, anlegen, umbenennen, aktiv/inaktiv | Rundgaenge | leicht |
| B2 | Bereiche und Kategorien anlegen, sortieren (Auf/Ab), deaktivieren | Bereiche, Kategorien | leicht–mittel (Sortieren = zwei Patches, Reihenfolge in Zehnerschritten) |
| B3 | Prüfpunkte mit Formular je Typ (Pflicht, Einheit, Grenzen, Auswahlwerte, Hinweis, Foto) + **Vorschau der Karte** wie in der Rundgang-App | Pruefpunkte | mittel (Vorschau = Karte `conKaKarte` aus der Rundgang-App übernehmen) |
| B4 | Plan: Wochentag, Zyklus, Startwoche (nur Montage wählbar), gültig bis + Vorschau „nächste 8 Termine“ mit derselben Formel `fnPlanPasst` | Plan | mittel |
| B5 | **Prüfbericht** „aktivierbar ja/nein, weil …“ (Regeln aus Abschnitt 2) | alle | mittel |
| B6 | Entwurf ↔ Aktiv, damit laufende Rundgänge sich nicht ändern | Rundgaenge (+ ggf. Kopie) | **schwer, Entscheidung nötig** (Abschnitt 4) |
| B7 | Rundgang kopieren (Vorlage), IDs neu verknüpfen | alle Stammdaten | mittel: in der App möglich, `Patch` liefert die neue ID, Zuordnung alt → neu je Stufe |
| B8 | Baukasten-Felder aus Auftrag 1–6 (Foto-Modus, Kommentar bei i.O., Bild-Hinweis, warnen/sperren, Bedingung, neue Typen) | Pruefpunkte | wächst mit jedem Auftrag |

## 4. Entscheidungen, die vor dem Bau fallen müssen
**E1 Entwurf und Aktivieren.** Heute gibt es nur `Aktiv`. Drei Wege:
- (a) **Entwurf als Kopie** (geschlussfolgert, empfohlen):
  - Der Builder bearbeitet einen aktiven Rundgang nie direkt. „Bearbeiten“ kopiert ihn als Entwurf (`Aktiv = Nein`, Status Entwurf).
  - „Aktivieren“ setzt den alten Rundgang auf inaktiv, den neuen auf aktiv und hängt den Plan um (`RundgangID`).
  - Vorteil: Laufende Durchführungen behalten ihre alten Prüfpunkte, weil deren IDs unverändert und aktiv bleiben, bis der Tageslauf vorbei ist. Die Rundgang-App muss dafür nicht geändert werden.
  - Nachteil: Die Rundgang-ID ändert sich. Die Durchführung heißt danach `R<neu>-Tag`, das kann für Auswertungen wichtig sein.
- (b) Statusspalte und Bearbeiten direkt, gesperrt solange heute eine Durchführung läuft. Das ist einfach, aber Änderungen wirken sofort.
- (c) Schnappschuss der Prüfpunkte beim Start (Designprinzip 7). Das ist der sauberste Weg, braucht aber einen Umbau der Rundgang-App (`KategorieListe` → auch Prüfpunkte).

**E2 Nachschlagespalten jetzt oder später** (Plan Schritt 2):
- Heute verknüpfen Zahlen-IDs. Ein Umstieg betrifft alle Filter der Rundgang-App (`RundgangID = …` → `Rundgang.Id = …`) und braucht neue Spalten mit Datenübernahme.
- Für den Builder sind Zahlen gleichwertig. Empfehlung: zuerst der Builder auf Zahlen, die Nachschlagespalten danach oder gar nicht.

**E3 Wer darf pflegen?**
- SharePoint-Rechte gelten je Liste, nicht je App. Nur-Lesen für Prüfer auf den Stammdaten heißt: Die Pflegegruppe braucht eigene Bearbeitungsrechte auf diesen 6 Listen.
- Das löst auch Befund R6 (Admin über die Konfiguration).

**E4 Eine App oder zwei?**
- Die Übergabe sagt zwei Apps. Das spricht dafür: getrennte Rechte und ein kleinerer Code der Prüfer-App.
- Das spricht dagegen: Die Vorschau der Karte muss in zwei Apps gleich bleiben (Kopie). Ich empfehle zwei Apps und die Karte als Komponente aus einer Komponentenbibliothek (UNSICHER, ob in der Umgebung erlaubt).

**E5 Löschen.** Die Übergabe sagt „nie löschen, deaktivieren“. Aber: Ein Entwurf, der nie aktiv war, kann gefahrlos weg. Der Builder darf deshalb nur Entwürfe ohne Durchführung in den Papierkorb legen.

## 5. Risiken
- Umgebung: Beide Apps laufen in der **Default-Umgebung**, ohne Test-Umgebung. Die Flows hängen an Josias' Konto. Das ist dasselbe Betriebsrisiko wie bei der Tischbuchung (eine Person).
- Teilweises Kopieren: Power Apps kennt keine Transaktion. Bricht das Kopieren ab, bleibt ein halber Entwurf. Deshalb kopiert der Builder immer in einen Entwurf, prüft danach mit dem Prüfbericht und bietet „unvollständigen Entwurf löschen“ an.
- Gleichzeitiges Pflegen durch zwei Personen: selten. Wie in der Rundgang-App über `Geändert` vor dem Speichern erkennen.
- Baukasten und Builder hängen zusammen: Jede neue Prüfpunkt-Spalte (Auftrag 1–6) braucht ein Feld im Builder. Wird der Builder vor den Baukasten-Aufträgen gebaut, muss er mitwachsen. Danach gebaut, ist das Schema stabiler (Reihenfolge laut Übergabe).

## 6. Fragen an Josias
1. Reihenfolge: zuerst Baukasten 1–6 in der Rundgang-App (laut Übergabe) oder zuerst der Builder? Und Nachschlagespalten vorher, nachher oder nie (E2)?
2. Entwurf: Weg (a) Kopie, (b) gesperrt oder (c) Schnappschuss (E1)?
3. Wer pflegt Rundgänge (Namen oder Gruppe)? Sollen Prüfer die Stammdaten nur lesen dürfen (E3)?
4. Ein oder zwei Apps? Ist eine Komponentenbibliothek erlaubt (E4)?
5. Soll der Builder auch die Konfiguration pflegen (NachholTage, Admins, Empfänger)?
6. Kommen die echten Rundgänge vom Fachbereich als Liste (Excel?) oder tippt jemand sie in den Builder? Bei einer Excel-Liste ist ein Import-Weg wertvoller als die Klick-Oberfläche.
7. Kannst du `C:\rundgang_work\` in dieses Repo schieben (mindestens `FORTSCHRITT.md`, `ENTSCHEIDUNGEN.md`, `FEATURES.json`, `pakete\IDEEN_PAKETE.md`)? Die Übergabe verweist darauf.
