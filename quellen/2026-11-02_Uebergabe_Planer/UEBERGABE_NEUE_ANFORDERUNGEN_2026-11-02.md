# Übergabe an den Analyse-/Engineering-Chat: neue Anforderungen (02.11.2026)

Von: Planer-Chat (Josias' Hauptkonto). Für: Analyse-/Engineering-Chat (Repo `Rundgang-DEV-More-App-reverse-engeneering`).
Inhalt: alles, was Josias seit dem Einbau der Baukasten-Pakete 1–6 neu gesagt hat, plus Analyse und Vorschläge des Planer-Chats.
Kennzeichnung: **[Josias]** = Wunsch/Aussage von Josias · **[Vorschlag]** = Empfehlung Planer-Chat, noch nicht entschieden · **UNSICHER** = nicht geprüft.

---

## 0. Stand der App (Kurz)
- Pakete 1–6 (Foto-Modus, Kommentarpflicht, Zahlengrenzen, Bedingungen, Typen MEHRFACH/DATUM/DATUMZEIT, Beispielbild) sind **eingebaut, gespeichert, nicht veröffentlicht**. Formeln = 0.
- Tests: Test-Gruppe 1 (Anzeige) ok. Test-Gruppe 2 (Eingaben/Pflichtprüfung) **steht noch aus**. Danach Speichern/Wiederöffnen/Abschluss/Protokoll/PDF/Foto am Tablet.
- Test-Stammdaten (Stand Anlage-Datei `bau/schema/rg_schema.json`, live ggf. erweitert):
  - Bereich „ZZ Test Serverräume“ → Kategorien „ZZ Test Serverraum EG (BS)“, „ZZ Test Serverraum EG (IS)“
  - Bereich „ZZ Test Infrastruktur“ → „ZZ Test Infrastrukturraum (IS)“, „ZZ Test Kategorie inaktiv“ (aus)
  - Test-Prüfpunkte 11–19 aus den Paket-Tests (nach Tests aufräumen).

---

## 1. Die echten Rundgänge (Vorlage: 4 MoreApp-PDFs)
**[Josias]** „Das hier sind die zu erstellenden Rundgänge.“ Josias hängt die vier PDFs an:
- `2026-10-26 - Haustechnikrundgang TGI MMS.pdf` (Montag)
- `2026-10-26 - Infrastrukturrundgang TGI MMS.pdf` (Montag)
- `2026-10-28 - Legionellen Prävention TGI MMS.pdf` (Mittwoch)
- `2026-10-28 - Sichtprüfung Gefahrstoffschränke TGI MMS.pdf` (Mittwoch)

Standort: Technoform Glass Insulation GmbH, Matthäus-Merian-Straße 6, 34253 Lohfelden. Ausführender: Haustechniker (Beispiel Peter Götl).

### Inhalt (aus den PDFs ausgelesen; einzelne Zeilen beim Auslesen abgeschnitten → am Original prüfen)
**Haustechnikrundgang** (~70 Punkte, fast alle „in Ordnung“-Typ):
- ohne Überschrift (→ Außenbereich): Ordnung/Sauberkeit, Toreinfahrt, Feuerwehrtresor, Gegensprechanlage, Torausfahrt, Straßeneinläufe, Straßeneinlaufrinnen
- Eingangsbereich/Treppenhaus, Infrastrukturraum, Büro EG: je Ordnung/Sauberkeit, Beleuchtung/elektrische Bauteile, (abgeschnitten), Wände/Decken/Böden, Inventar/Büromöbel, (abgeschnitten); Büro EG zusätzlich Kopierpapier (min. 1 Karton), Reinigungsstand, Leerung Mülleimer
- Büro 1. OG mit Unterüberschriften: Allgemein, Küchenbereich, Besuchertoiletten (Herren WC), Besuchertoiletten (Damen WC), Allgemein, Herren WC, Damen WC (Sauberkeit, Seifenspender, Handtuchpapierspender …), Kontrolle Abluftanlage
- (Überschrift verloren, wohl Wasserentnahmestellen): EG Behinderten-WC HWB, EG Halle Damen/Herren WC HWB, EG Küche Spüle, 1. OG Damen WC HWB rechts, 1. OG Besucher WC HWB, 1. OG Herren Dusche links Mischarmatur, 1. OG Herren Dusche 4. HWB von links, 1. OG Herren WC HWB rechts, 1. OG Küche Spüle, „…Mängelprotokoll)“
- Sammelstation für Altöl und Gefahrstoffe: Auffangwannen nach AwSV, Dichtheit, Standfestigkeit
- Unterschrift des ausführenden Haustechnikers

**Infrastrukturrundgang** (~70 Punkte, viele Messwerte):
- Batterieraum: Störungsfrei
- Infrastrukturraum: Zählerstand Wasseruhr (m³), Druck (bar); **Kompressor 1/2/3** je Betriebsdruck (bar), Betriebsstunden (h), Temperatur (°C), Druckluftfilter; Kältetrockner 1/2; Wasseraufbereitung (Jansen); Wamat inkl. Wasserqualität mit Teststreifen; ONI Kühlanlage (Ordnung, Druck bar, Siebkorbfilter 1/2 „ab 0,5 bar Reinigung“, Luftfilter Schaltschrank, Zählerstand Wasseruhr über Tank m³); **Kältemaschine 1/2/3** je Kühllamellen, Wassertemperatur Ausgang (°C), Betriebsstunden C1/C2 bzw. A1 und B1/C1 (h)
- Produktionshalle: Tore 1–6 (Funktion, Piktogramm), WZB Aktivkohlefilter/Gefahrstoffschränke, Regalanlagen, Haftungskabine (°C), Analysebüro (Stickstoffflasche Sichtprüfung + Füllung bar, Temperatur Klima °C), Messraum (°C), Wareneingangsbüro (°C), Warenausgangsbüro (°C), ca. 8 Zählerstände m³ (Bezeichnungen beim Auslesen verloren), cos φ Kompensationsanlage (Normalbereich > 0,90), Filtervlies Kompensationsanlage, Zählerstand Hauptverteilung 1–4 (kWh), Dachfenstersteuerung/Lichtschalter, Mangelbeschreibung (Text), Büro 1. OG (°C)
- Unterschrift
- Auffällig: mehrere Werte „0 °C“ / „0 m³“ → vermutlich „nicht messbar/aus“, wird aber als 0 erfasst.

**Legionellen Prävention**: 1. OG Damenumkleide Dusche und HWB links (je „10 Minuten Wasser mit mind. 60 °C durchlaufen lassen“) → Antwort „durchgeführt“. Unterschrift.

**Sichtprüfung Gefahrstoffschränke**: Schrank Nr. 01/02/03 mit Service-Nr./Barcode (106304, 106303, 106305), je Außen-Sichtprüfung + Innen (beschädigte Gefäße, Beschädigung …). Unterschrift.

**Kopfdaten in allen vier PDFs:** Kunde, Adresse, Ausführender Haustechniker, Datum, Kalenderwoche, Wochentag. (MoreApp schreibt für 26.10.2026 „KW 38“ – falsch, richtig KW 44.)

### Lücken für diese Rundgänge
| # | Lücke | Vorschlag |
|---|---|---|
| L1 | **Unterschrift** (alle 4 PDFs) | Stifteingabe beim Abschluss, Bild ins Protokoll/PDF, Spalte in `RG_Durchfuehrungen` |
| L2 | **Kopfdaten** Kunde/Adresse/KW/Wochentag | Spalten Standort/Kunde/Adresse in `RG_Rundgaenge`; KW/Wochentag im Protokollkopf berechnen |
| L3 | **Eigene Antwortwörter** („durchgeführt“ statt „in Ordnung“) | Beschriftung pro Prüfpunkt für Zweiwert-Fragen, negativer Wert erzeugt trotzdem Mangel. **UNSICHER:** ob AUSWAHL heute beim Abschluss Mängel anlegt – im Code prüfen |
| L4 | „nicht messbar / außer Betrieb“ bei Zahlen | Haken am Zahlenfeld statt 0 |
| L5 | Viele gleiche Blöcke pro Raum | Kopieren/Vorlagen oder Excel-Import vor der Builder-App |
| Frage | Rhythmus Legionellen/Gefahrstoff | `RG_Plan` kann Wochentag + „jede n. Woche“, **nicht** „1. Mittwoch im Monat“ – beim Fachbereich klären |

---

## 2. Benutzerwechsel am geteilten iPad
**[Josias]**
- Verschiedene Personen benutzen **dasselbe iPad**, häufiger Benutzerwechsel.
- **Alle haben ein eigenes Microsoft-Konto, alle arbeiten im Unternehmen.** Wichtig ist nur, wie man schnell zwischen ihnen wechselt.
- **Ein geteiltes Konto ist kein Problem** (eine Schwesterfirma hat einen virtuellen Nutzer).
- Josias' eigene Ideen waren: eigenes Konto pro Person, Name + Personensuche, Name + gespeichertes Passwort.

**[Vorschlag, mit Josias besprochen, noch nicht final bestätigt]**
- iPad dauerhaft mit einem **virtuellen/geteilten Konto** angemeldet (Kontowechsel in Power Apps = Abmelden + MFA, zu langsam).
- Startbildschirm: „Wer macht den Rundgang?“ → Auswahl aus neuer Liste **`RG_Pruefer`** (Spalten: Person [Personenspalte → Name/E-Mail aus dem Verzeichnis], Aktiv, optional PIN 4-stellig als Verklick-Schutz, **kein** echtes Passwort).
- Gewählter Prüfer in Variable; überall statt `User()` verwenden (Durchführung, KategorieErgebnisse `PrueferName/PrueferEmail`, Mängel `FestgestelltVon`, Protokoll, Konfliktmeldung).
- **Unterschrift** beim Abschluss (= Nachweis, wie heute Papier/MoreApp).
- Nach Abschluss oder ~10 min Inaktivität zurück zur Namensauswahl.
- Admin-Funktionen (Zurücksetzen) weiter an echte Admin-Konten binden – beim geteilten Konto neu durchdenken (z. B. Admin = Prüfer mit Admin-Kennzeichen + PIN, oder nur in der Builder-App).
- Gelöste Altlast: Flows (`RG_Foto_hochladen`, `RG_Protokoll_archivieren`) und App sollten dem virtuellen Konto gehören statt Josias.
- Klären (IT/Josias): Lizenz des virtuellen Kontos (Power Apps über M365 reicht), Zugriff IMS+, Umzug/Teilen von App und Flows. **Keine Konten/Berechtigungen selbst anfassen.**

---

## 3. Neue Baukasten-Funktionen
**[Josias]** „eher sehr spezielle Fälle“:

### 3.1 Abweichung zum letzten Rundgang
**[Josias]** Prüfen, ob ein heutiger Wert stark vom Wert des letzten Rundgangs abweicht („2 Tage vergleichen, ob es stimmen kann“).
**[Vorschlag]** Spalten in `RG_Pruefpunkte`: `AbweichungMax` (Zahl), `AbweichungArt` (absolut/Prozent), `AbweichungModus` (Warnen/Mangel/Sperren wie Grenzmodus), `NurSteigend` (Ja/Nein, für Zähler). Vergleichswert = letzte **abgeschlossene, nicht-Test**-Durchführung desselben Rundgangs (JSON aus `RG_KategorieErgebnisse`). Anzeige „Letztes Mal: 7,6 bar (26.10.)“. Kein Vergleich beim ersten Lauf.

### 3.2 Passwörter für Maschinen
**[Josias]** Bei manchen Maschinen muss man mit einem Passwort arbeiten; „irgendwo einbauen, wo es Sinn macht, vielleicht eine extra Passwort-Spalte“.
**[Vorschlag]** Eigene Liste `RG_Zugangsdaten` (Titel/Maschine, Zugang), Prüfpunkt verweist mit `ZugangID`; 🔑-Knopf bzw. Anzeige im ⓘ-Fenster, erst auf Antippen sichtbar, **nie ins Protokoll**.
**Offen (Josias):** Sind das einfache Bedien-PINs (dann ok in SharePoint) oder sensible IT-Zugänge (dann Passwort-Tresor, nicht SharePoint)? Jeder mit iPad-Zugang kann die Liste lesen.

### 3.3 Zwei Werte vergleichen
**[Josias]** Es gibt z. B. zweimal dasselbe Gerät, und es muss geprüft werden, ob beide denselben Wert haben; **leichte Abweichung soll einstellbar sein**.
**[Vorschlag]** Spalten `VergleichPunkt` (ID), `VergleichToleranz` (0 = exakt gleich), `VergleichModus` (Warnen/Mangel/Sperren). Start: nur innerhalb derselben Kategorie (kategorieübergreifend = Nachladen, mehr Aufwand, UNSICHER).

### 3.4 Archiv / vergangene Läufe
**[Josias]** Alte Läufe ansehen können, als **extra Bereich/Bildschirm**, mit einer **Auflistung aller Rundgänge**, „vielleicht gefiltert, mal gucken, wie es Sinn macht“.
**[Vorschlag]** Neuer Bildschirm `scrArchiv` (Knopf auf Start). Filter: Rundgang, Zeitraum (Standard 3 Monate, wegen Delegation immer zuerst nach Datum), Status, Prüfer, „nur mit Mängeln“. Zeile: Datum, Rundgang, Prüfer, Anzahl Mängel, Status. Antippen → bestehende Nur-Ansicht; Knopf „PDF öffnen“ (Link aus `RG_Protokolle`).

### 3.5 Anleitungen im ⓘ-Knopf
**[Josias]** „Ganz viele“ Anleitungen, **sehr unterschiedliche Längen** → Textbereich muss mit der Textlänge wachsen bzw. genug Platz haben. In einem **ⓘ-Info-Knopf**. „Da würde ich alles reinmachen, was nicht zwingend gesehen werden muss … vielleicht auch die Foto-Funktion.“
**[Vorschlag]**
- Eigene Liste `RG_Anleitungen` (Titel, Text mehrzeilig, optional Bild), Prüfpunkt verweist mit `AnleitungID` → eine Anleitung für viele gleiche Prüfpunkte.
- ⓘ öffnet ein fast bildschirmfüllendes Fenster, Höhe wächst mit dem Text, scrollbar. Inhalt: Anleitung, Beispielbild (Paket 6), Hinweistext, ggf. Zugang (3.2), **Foto nur bei Modus „Optional“**.
- **Foto bei „Pflicht“ und bei n.i.O. bleibt in der Karte** – Josias' Regel „Prüfer sind nicht verlässlich“ (versteckte Pflichtfunktionen werden vergessen). Mit Josias abstimmen.

---

## 4. Struktur: Kategorien / Bereiche / neue Abschnitte
**[Josias]**
- Dachte, Bereiche wären Kategorien; fragte, wo Kategorien angezeigt werden.
- Fragte, ob man „keine Kategorie“ gültig machen kann.
- Im PDF sind kaum Kategorien erkennbar → „können wir welche erfinden, wenn wir sie immer brauchen?“
- **„Wäre es nicht besser, man macht sie nicht mehr verpflichtend?“**
- Man braucht manchmal **Gruppierung innerhalb** einer Kategorie: im Technikraum Abschnitte pro Maschine („Maschine 1: Punkt 1, 2, 3 – Maschine 2 …“, alles im Technikraum).
- „Die anderen Kategorien braucht man doch nicht mal, oder?“

**Erklärt (Ist-Zustand):** Rundgang (Start) → Bereich (nur Beschriftung) → Kategorie (Zeile auf `scrRundgang`, **= Speicherschritt**) → Prüfpunkt (Karte). Prüfpunkte hängen per `KategorieID` an der Kategorie; ohne Kategorie erscheint nichts. Kategorie optional zu machen wäre ein großer Umbau (Speichern, Nachlese, Freischalten, Ergebnisse, Protokoll laufen über die Kategorie).

**[Vorschlag]**
| Ebene | Pflicht | Beispiel |
|---|---|---|
| Bereich (Stockwerk/Gebäude) | **optional** | – |
| Raum/Station (= heutige Kategorie, Speicherschritt) | Pflicht | Infrastrukturraum |
| **Abschnitt (neu)** | optional | Kompressor 1, Kompressor 2, Kältemaschine 3 |
| Prüfpunkt | Pflicht | Betriebsdruck |

- **Jetzt:** neue Textspalte `Abschnitt` in `RG_Pruefpunkte`; Karte/Galerie zeigt eine Überschrift, wenn sich der Abschnitt zum vorigen Punkt ändert; Protokoll ebenso. Klein, nichts bricht. Hilft auch bei 3.3.
- **Übergang Bereich:** pro Rundgang ein Bereich; App blendet Bereichsnamen aus, wenn er leer/gleich dem Kategorienamen ist (oder ein Kennzeichen „ausblenden“).
- **Später (mit Builder):** `RundgangID` in `RG_Kategorien`, Bereich nur noch Anzeige; in der Oberfläche „Kategorie“ → „Raum/Station“ umbenennen (SharePoint-Spaltennamen bleiben).
- Faustregel für Räume/Stationen: das, was der Prüfer an einem Ort am Stück erledigt; ca. 3–15 Punkte; Reihenfolge = Laufweg (mit Haustechniker abstimmen).
- Beispielzuordnung Haustechnik: Außenbereich · Eingangsbereich/Treppenhaus · Infrastrukturraum · Büro EG · Büro 1. OG (Allgemein, Küche, Besucher-WC H/D, WC H/D – als Räume oder als Abschnitte, Josias entscheidet) · Wasserentnahmestellen · Sammelstation.

---

## 5. Vorgeschlagene Paketreihenfolge (Planer-Chat, nicht entschieden)
| Paket | Inhalt | Aufwand |
|---|---|---|
| 7 | Prüferauswahl (`RG_Pruefer`), Unterschrift, Kopfdaten (Standort/KW/Wochentag), eigene Antwortwörter | M |
| 8 | **Abschnitte** in Prüfpunkten + Bereich ausblendbar | S |
| 9 | ⓘ-Fenster mit Anleitungen (`RG_Anleitungen`), Bild, Hinweis, optionales Foto | M |
| 10 | Abweichung zum letzten Rundgang + Zähler-Prüfung | M |
| 11 | Vergleich zweier Punkte (in einer Kategorie) | S |
| 12 | Zugangsdaten/Passwörter (nach Josias' Antwort) | S |
| 13 | Archiv-Bildschirm | M |
| danach | „nicht messbar“, Excel-Import/Kopieren, vier echte Rundgänge anlegen, Builder-App | – |

Vorher: Tests der Pakete 1–6 abschließen und veröffentlichen.

## 6. Offene Fragen an Josias / Fachbereich
1. Passwörter: Bedien-PINs oder sensible Zugänge?
2. Prüferauswahl mit PIN ja/nein? Wer pflegt `RG_Pruefer`?
3. Virtuelles Konto: wer richtet es ein (IT), Lizenz, Übernahme von App und Flows.
4. Büro 1. OG: Unterbereiche als eigene Räume (eigene Speicherschritte) oder als Abschnitte in einem Raum?
5. Rhythmus Legionellen/Gefahrstoffschränke (monatlich?), echter Laufweg/Reihenfolge.
6. Gefahrstoffschränke per Barcode/QR scannen oder Nummer im Text?

## 7. Regeln (unverändert)
Lieferformat nach `ARBEITSWEISE_AENDERUNGEN.md` (Steuerelement → Property, ganze Property, deutsch in der Formelleiste, YAML englisch, Test + Rückweg). Nur Testdaten (`ZZ Test`, `TestDatensatz = Ja`). Keine fremden Flows/Apps. Kein Schreiben in den Obsidian-Vault. Berechtigungsdialoge nur mit Josias' Ja. Mails nur im Testmodus.
