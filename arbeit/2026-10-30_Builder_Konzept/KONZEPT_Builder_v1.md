# Konzept Rundgang-Builder v1 (30.10.2026, Entwurf)

Auftrag von Josias: Eine zweite App, mit der man Rundgänge **so einfach wie möglich** baut. Hauptgrund für die Extra-App ist die Einfachheit. Die App muss nicht aufwendig sein.

## Vorgaben von Josias
- Ein Bereich mit **bestehenden Rundgängen** und ein Bereich für **neue Rundgänge**.
- Alles in einzelne Kategorien unterteilt. Neue Bereiche, Kategorien und Prüfpunkte lassen sich aus den vorhandenen Bausteinen **auswählen und durchklicken**.
- Beispiel: Bereich „Lagerhalle“, Kategorie „Teilelager“; Prüfpunkt 1: i.O./n.i.O., Bild oder Kommentar nur bei Mangel; Prüfpunkt 2: „Anzahl Teile am Produkt im Regal“, Zahl, i.O. zwischen 100 und 1000.

## Reihenfolge der Listen (heute, belegt aus dem Export)
Rundgang (`RG_Rundgaenge`) → Bereich (`RG_Bereiche`, Überschrift) → Kategorie (`RG_Kategorien`, eine Seite, wird als Ganzes gespeichert, wird der Reihe nach freigeschaltet) → Prüfpunkt (`RG_Pruefpunkte`, die einzelne Frage, das Kleinste).
Dazu `RG_Plan` (wann ist der Rundgang dran). Verknüpft über Zahlen-IDs. Reihenfolge in der App: Bereichs-Reihenfolge, darin Kategorien-Reihenfolge. Jeder Bereich gehört genau einem Rundgang, jede Kategorie genau einem Bereich.

## Fest im Bauplan (der Builder ändert das nicht)
- Die Listenstruktur und die Hierarchie.
- Der Ablauf der Rundgang-App: Starten, Kategorien nacheinander, Speichern mit Prüfung, Abschluss mit Mängeln, Protokoll als PDF.
- Die Schutzmechanismen (Doppelklick-Sperre, Nachlese, Zwischenstatus beim Abschluss).
- Die Eingabetypen als Bausteine der Rundgang-App (i.O./n.i.O., Zahl, Auswahl, Text, Mehrfachauswahl, Datum, Datum + Uhrzeit).
- Die Prüflogik (was „noch offen“ ist) und die Planlogik (Wochentag, Zyklus, Start).
- Rechte, Archiv, Fotoablage.

## Aus dem Katalog wählbar (der Builder setzt nur Schalter, keine Formeln)
Pro Prüfpunkt: Frage, Typ, Pflicht ja/nein, Foto (Aus/Optional/Pflicht), Kommentar auch bei i.O., bei Zahl: von/bis + Grenzmodus (Mangel/Warnen/Sperren) + Einheit, bei Auswahl: Werte, Hinweistext, Beispielbild, Bedingung („nur wenn Frage A = Wert“), Reihenfolge.
Pro Rundgang: Name, Plan (Wochentag, Zyklus, ab wann, bis wann), Status.

## Lücken gegenüber dem Beispiel
- „Foto Pflicht nur bei Mangel“ gibt es noch nicht (heute: Foto-Pflicht gilt immer, bei n.i.O. ist ein Foto immer erlaubt). Vorschlag: neuer Foto-Wert „Bei Mangel Pflicht“.
- „Kommentar nur bei Mangel“ ist heute Standard (bei n.i.O. immer Pflicht).

## Einfachster Bauablauf (Vorschlag)
1. Neuer Rundgang: Name und Wann (Wochentag/Zyklus).
2. Bereich anlegen, darin Kategorien anlegen (nur Namen).
3. Prüfpunkte: „+ Prüfpunkt“, Frage tippen, Typ als große Kachel wählen, nur die passenden Schalter sehen, Vorschau der Karte wie im Rundgang.
4. Prüfen und aktivieren: Liste „aktivierbar ja/nein, weil …“.
Später: kleine Vorlagen für typische Prüfpunkte (zum Antippen und Anpassen), Rundgang/Bereich/Kategorie kopieren.

## Offene Fragen an Josias
1. Dieselben Bereiche/Kategorien in mehreren Rundgängen nutzen (teilen) oder immer kopieren? Empfehlung: kopieren.
2. Kleine Vorlagen für typische Prüfpunkte gewünscht? Empfehlung: ja, aber erst nach der ersten Version.
3. Neuer Foto-Wert „Bei Mangel Pflicht“ ok?
4. Änderung an einem aktiven Rundgang: als Kopie (Entwurf) und dann aktivieren (Entscheidung des Planer-Chats)?
