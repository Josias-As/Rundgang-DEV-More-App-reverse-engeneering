# Konzept Rundgang-Builder v2 (30.10.2026, Entwurf)

Baut auf `KONZEPT_Builder_v1.md` auf. Entscheidungen von Josias am 30.10.:
1. Bereiche und Kategorien werden **kopiert**, nicht geteilt.
2. **Vorlagen für Prüfpunkte schon in der ersten Version.**
3. Neuer Foto-Wert **„Bei Mangel Pflicht“** (kommt als Paket 7 in die Rundgang-App).
4. Änderungen an einem aktiven Rundgang nur **als Kopie (Entwurf)**. In der Ansicht „Alle Rundgänge“ gibt es einen **Schalter „alle zeigen“**. Aktiviert man eine Version, während die **alte Version noch aktiv** ist, zeigt der Builder eine **Warnung**.

## Datenmodell-Ergänzungen (nur Spalten hinzufügen, nichts umbenennen)
`RG_Rundgaenge`: `Status` (Auswahl Entwurf / Aktiv / Archiviert), `Version` (Zahl), `VorgaengerID` (Zahl, 0 = erste Version). `Aktiv` bleibt und wird vom Builder passend mitgesetzt (Aktiv = Status „Aktiv“), die Rundgang-App ändert sich dadurch nicht.
Neue Liste `RG_Vorlagen`: dieselben Felder wie ein Prüfpunkt (Frage, Typ, Pflicht, Foto, KommentarPflicht, Grenzen, Grenzmodus, Einheit, Auswahlwerte, Hinweis), ohne `KategorieID`, dazu `Gruppe` (z. B. Sauberkeit, Messwert) und `Titel` der Vorlage.

## Prinzip „Kopie statt Bearbeiten“
- Der Builder ändert **nur Entwürfe**. Aktive und archivierte Rundgänge sind schreibgeschützt.
- „Ändern“ eines aktiven Rundgangs = **Kopie als Entwurf** (Version + 1, VorgaengerID gesetzt): der Builder kopiert Rundgang, Bereiche, Kategorien, Prüfpunkte und Planzeilen (Planzeilen der Kopie inaktiv). Die Zuordnung alt → neu für die Nummern merkt sich der Builder während des Kopierens.
- Folge (geschlussfolgert): Weil aktive Fassungen nie verändert werden, ist ein Einfrieren der Prüfpunkte beim Start in der Rundgang-App für den Builder nicht nötig. Voraussetzung: Prüfer haben auf die Stammdaten nur Leserechte.

## Ansicht „Alle Rundgänge“
- Standard: nur **aktive** Rundgänge. Schalter „Alle zeigen“ blendet **Entwürfe und Archivierte** ein.
- Pro Zeile: Name, Version, Status, Plan, Knöpfe „Ansehen“, „Als Kopie ändern“, „Aktivieren“, „Archivieren“.
- **Warnung beim Aktivieren:** Ist von diesem Rundgang (Vorgänger oder gleicher Name) eine **andere Version noch aktiv**, steht dort „Die alte Version ‚<Name> v<n>‘ ist noch aktiv.“ Der Builder bietet „Alte Version archivieren“ oder „Beide aktiv lassen“ an; ohne Wahl wird nicht aktiviert.
- Beim **Archivieren** prüft der Builder, ob **heute eine Durchführung dieses Rundgangs läuft**, und warnt, weil die Startseite der Rundgang-App nur aktive Rundgänge zeigt (eine laufende Durchführung eines archivierten Rundgangs würde dort nicht mehr erscheinen).

## Vorlagen (erste Version)
- Beim „+ Prüfpunkt“: „Aus Vorlage“ (Liste, nach Gruppen) oder „Leer anfangen“. Die Vorlage füllt alle Schalter, danach ist alles änderbar.
- „Als Vorlage speichern“ an jedem Prüfpunkt.
- Startvorlagen (Vorschlag): Sauberkeit (i.O./n.i.O., Foto bei Mangel), Sichtprüfung mit Foto Pflicht, Temperatur °C (Zahl, Grenzen, Warnen), Zählerstand (Zahl), Anzahl im Bereich (Zahl, Grenzen, Mangel), Zustand (Auswahl gut/mäßig/schlecht), Bemerkung (Text), Datum der letzten Wartung (Datum).

## Pakete davor (Rundgang-App)
- **Paket 7:** Foto-Wert „Bei Mangel Pflicht“ (Auswahlwert in `Foto`, `fnFotoModus`, `fnFehltGrund`, `fnFotoNeuErlaubt`, Foto-Fenster).
- **Datenpaket:** neue Spalten an `RG_Rundgaenge`, neue Liste `RG_Vorlagen` (nur SharePoint, keine Änderung an der Rundgang-App nötig).

## Offen
- Wie sehen die Bildschirme aus? Vorschlag: zuerst ein anklickbares Muster, bevor Code gebaut wird.
- Wer darf bauen (Pflegegruppe), Excel oder Papier für den Fachbereich, Konfiguration bleibt draußen.
