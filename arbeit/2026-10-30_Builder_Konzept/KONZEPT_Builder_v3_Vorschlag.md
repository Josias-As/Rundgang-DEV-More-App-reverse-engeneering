# Konzept Rundgang-Builder v3 (Vorschlag, 30.10.2026)

Kritische Durchsicht von `KONZEPT_Builder_v2.md`, Recherche zu Baukasten- und Checklisten-Editoren, neue Wege, Abwägung. **Noch kein Bau.** v2 bleibt unverändert. Kennzeichnung: **belegt** (Export/Quelle), **geschlussfolgert**, **UNSICHER**.

## Kurzfassung

1. **Versionen ohne neue Rundgang-Nummer (größte Änderung):** v2 kopiert für jede Änderung den ganzen Rundgang samt Plan. Neu bleibt die Rundgang-Nummer gleich. Nur die **Bereiche einer Fassung** werden beim Aktivieren umgeschaltet: neue Fassung an, alte aus. Das trägt, weil die Rundgang-App Bereiche und Kategorien nur beim **Start** liest. Beim Öffnen einer Kategorie liest sie die Prüfpunkte nur über `KategorieID` und `Aktiv` (**belegt**, `btnRgAktion.OnSelect`, `scrKategorie.OnVisible`). Folgen:
   - Laufende Rundgänge laufen mit der alten Fassung zu Ende.
   - Plan, Durchführungsnummer `R<id>-Tag` und Auswertung bleiben durchgehend.
   - **Zwei aktive Fassungen desselben Rundgangs kann es nicht mehr geben.** Die Warnung aus v2 wird überflüssig, weil es den Fehler nicht mehr gibt.
2. **Ein Bildschirm statt Durchklicken über vier Ebenen:**
   - Links die Gliederung (Bereich ▸ Kategorie ▸ Prüfpunkt), in der Mitte der Editor für das gewählte Teil, rechts eine Vorschau der Karte wie am Tablet.
   - Ein Assistent (Schritt für Schritt) kommt nur beim Anlegen vor, nicht beim Ändern.
3. **Fehler gar nicht erst entstehen lassen, statt sie am Ende zu melden:**
   - Auswahl statt Tippen, z. B. Bedingung nur aus früheren Fragen derselben Kategorie und Grenzen als Satz.
   - Ein Warnzeichen direkt an der Zeile.
   - „Aktivieren“ ist gesperrt, solange es Fehler gibt, und sagt warum.
4. **Vorlagen ohne eigene Liste:**
   - Statt `RG_Vorlagen` gibt es einen Rundgang „Vorlagen“ (Status Vorlage, nie aktiv). Seine Kategorien sind die Gruppen, seine Prüfpunkte die Vorlagen.
   - Gleiche Spalten, gleicher Editor, gleiche Kopierfunktion. Jede künftige Baukasten-Spalte gilt sofort auch für Vorlagen.
   - Auch ganze Kategorien und Bereiche lassen sich als Vorlage ablegen.
5. **Schneller bauen:**
   - „Mehrere Prüfpunkte einfügen“: eine Frage pro Zeile, daraus entstehen n Punkte.
   - **Aus Excel einfügen**: Spalten kopieren und in ein Textfeld einfügen, die App zerlegt sie. Dafür ist weder Premium noch ein Flow nötig.
   - Duplizieren auf jeder Ebene.
6. **Rückgängig statt Rückfragen:**
   - Im Entwurf ist Entfernen gefahrlos, weil die Zeilen nie live waren. „Entfernt – Rückgängig“ ersetzt das Bestätigungsfenster.
   - Eine Bestätigung gibt es nur beim Aktivieren und Archivieren, dann mit **Änderungsübersicht** („3 neu, 1 geändert, 2 entfernt“).
7. **Rundgang-App:** außer Paket 7 (Foto „Bei Mangel Pflicht“) **keine Änderung** (belegt aus den Formeln, Abschnitt 6).
8. **Fragen an dich (Abschnitt 8):**
   - Wo wird gebaut, am PC oder am Tablet?
   - Kommen die Rundgänge als Excel?
   - Ist „Versionen ohne neue Nummer“ ok?
   - Sind Vorlagen als „Vorlagen-Rundgang“ ok?

## 1. Was die Recherche zeigt

Viele Fachseiten (nngroup.com, help.safetyculture.com) sind aus der Cloud nicht abrufbar. Was hier steht, stammt aus Suchergebnissen und Herstellerhilfen. Es sind Muster, keine Studien.

| Befund | Quelle | Was es für den Builder heißt |
|---|---|---|
| **Logik ist der schwerste Teil.** SafetyCulture-Nutzer loben den Editor, nennen das Einrichten von Logik aber „ein bisschen wie ein Puzzle“. Bei großen, stark verzweigten Vorlagen wird es mühsam. | Fluix-Test, Capterra-, SaaSworthy-Bewertungen | Bedingungen klein halten (eine Ebene, wie Paket 4). Direkt an der Frage als Satz einstellen („Nur zeigen, wenn …“), nicht in einem eigenen Regel-Reiter. |
| **MoreApp** (das Vorbild) trennt Felder und Regeln. Regeln stehen in einem eigenen Reiter „Rules“ mit Bedingung und Aktion. Gilt dasselbe Feld in zwei Regeln, greift nur die letzte. | MoreApp-Hilfe | Genau diese Falle vermeiden: Eine Bedingung gehört zur Frage. Mehr als eine Bedingung pro Frage lässt der Builder gar nicht zu. |
| **Änderungen an veröffentlichten Vorlagen** sind ein häufiger Ärger. Ein Nutzer berichtet, er habe für einen Schritt mehr alles neu bauen müssen. | Software-Advice-Bewertung (Einzelstimme) | „Neue Fassung“ muss ein Klick sein, kein Neubau. |
| **Vorlagen gegen das leere Blatt**, aber immer mit Option „Leer“. Lieber wenige geprüfte Vorlagen als viele ähnliche, sonst wählen Nutzer die falsche. | ApostropheCMS, Agiled, Jira-Feature-Wunsch | Wenige Startvorlagen, sauber gruppiert. „Leer anfangen“ immer daneben. |
| **Assistent oder eine Seite:** Assistenten passen zum Anlegen. Zum Ansehen und Ändern ist eine einzelne Seite besser, weil das Durchklicken eines Assistenten beim Bearbeiten mühsam ist. Assistenten gelten als schwere Form der Oberfläche: kurz halten und mit Voreinstellungen füllen. | Mirakl-Designsystem, Microsoft-Richtlinien | Assistent nur für „Neuer Rundgang“ (Name, Wann, Start leer, aus Kopie oder aus Excel). Danach ein Editor. |
| **Liste und Detail nebeneinander** eignen sich für breite Bildschirme. Den rechten Bereich nie leer lassen, immer etwas vorauswählen. | Microsoft (Dual-Screen-Muster), saasui.design | Gliederung links, Editor rechts, beim Öffnen ist das erste Teil gewählt. |
| **Rückgängig statt Bestätigen:** Bestätigungsfenster werden aus Gewohnheit weggeklickt. Wo es geht, Rückgängig anbieten. Bestätigen nur, wo Rückgängig nicht geht. | GNOME-Richtlinien, mehrere UX-Quellen (keine kontrollierte Studie) | Entfernen im Entwurf mit „Rückgängig“. Bestätigung nur beim Aktivieren und Archivieren, mit konkretem Text (was sich ändert). |
| **Prüfung vor dem Veröffentlichen:** gängig sind ein ausgegrauter Knopf, bis alles behoben ist (MoJ Forms), Markierung am fehlerhaften Teil sowie eine Trennung von Fehlern (sperren) und Warnungen (dürfen bleiben). | MoJ Forms, Oracle Field Service, OpenCMS | Zwei Stufen: **Fehler** sperren das Aktivieren, **Hinweise** nicht. Jede Meldung springt zum Teil. |
| **Tabelle oder Klick-Editor:** In KoboToolbox entsteht aus Excel (XLSForm) und aus dem Klick-Editor dasselbe Formular. Excel ist stärker für Großes und Komplexes, der Klick-Editor leichter für Einsteiger. Viele starten im Klick-Editor und machen in Excel weiter. | KoboToolbox-Hilfe, CartONG | Beide Wege anbieten. Der Klick-Editor ist der Hauptweg, „Aus Excel einfügen“ der schnelle Weg für Listen vom Fachbereich. |
| **Excel einfügen in Power Apps:** In ein Textfeld eingefügte Excel-Zellen lassen sich mit `Split(…; Char(10))` in Zeilen und mit `Char(9)` in Spalten zerlegen, mit Vorschau vor dem Übernehmen. Falle: Zellen mit Zeilenumbruch stehen in Anführungszeichen. | Power-Users-Community (Blog und Forum) | Machbar ohne Premium. Zellen mit Umbruch erkennen und als Fehler zeigen, nicht still falsch zerlegen. |
| **Sortieren in Power Apps:** Ziehen und Ablegen ist nicht eingebaut. Dafür bräuchte es eine PCF-Komponente, die in der Umgebung freigeschaltet sein muss. Üblich sind ↑/↓-Knöpfe, die die Sortiernummer tauschen. | Matthew Devaney, Power-Users-Community | ↑/↓ und „Verschieben nach …“ (andere Kategorie). Kein Ziehen. |
| **Baum in Power Apps:** Ein Steuerelement dafür gibt es nicht. Eine Galerie mit flacher Sammlung (Ebene, Pfad, sichtbar) erlaubt Einrücken und Auf-/Zuklappen über beliebig viele Ebenen. Verschachtelte Galerien gehen nur 2 Ebenen tief. | Canviz-Blog | Gliederung als **eine** Galerie aus einer flachen Sammlung (Bereich, Kategorie, Prüfpunkt mit Ebene 0/1/2). |

## 2. Kritik an v2

| Nr | Punkt in v2 | Problem | Schwere |
|---|---|---|---|
| K1 | Änderung = **Kopie des ganzen Rundgangs** mit neuer Nummer, Plan wird mitkopiert | Die Durchführungsnummer `R<id>-Tag` wechselt, Auswertungen über Zeit brechen. Der Plan muss umgehängt werden, alte Planzeilen bleiben stehen. Erst diese Kopie macht „zwei aktive Fassungen“ möglich und damit die Warnung nötig. Die Kopie samt Plan ist der aufwendigste Schreibweg im ganzen Builder. | hoch |
| K2 | Neue Liste `RG_Vorlagen` mit denselben Feldern wie Prüfpunkte | Jede neue Baukasten-Spalte (Paket 7 und alle künftigen) muss in **zwei** Listen und zwei Editoren nachgezogen werden. Vergisst man das, gehen Felder beim Übernehmen still verloren (dieselbe Fehlerart wie `FotoMoeglich` am 27.10.). | mittel |
| K3 | Bauen über Ebenen hinweg (Rundgang → Bereich → Kategorie → Prüfpunkt als einzelne Schritte) | Man verliert den Überblick und springt viel hin und her. Für das Ändern ist ein Assistent schlecht (Recherche). | mittel |
| K4 | Prüfbericht erst am Ende („aktivierbar ja/nein, weil …“) | Fehler fallen spät auf. Besser verhindern (Auswahl statt Eingabe) und direkt an der Zeile zeigen. | mittel |
| K5 | Stabile Schlüssel (Planer-Chat: Spalte `Schluessel`) fehlen in v2 | Ohne Schlüssel gibt es keine Änderungsübersicht zwischen Fassungen, keine Auswertung „dieselbe Frage über mehrere Fassungen“ und kein sauberes Abbilden alt → neu beim Kopieren. | mittel |
| K6 | Spaltenname `Version` | SharePoint hat ein eingebautes Feld mit dem Anzeigenamen „Version“. Eine eigene Spalte gleichen Namens verwechselt man leicht (geschlussfolgert). → `Fassung`. | niedrig |
| K7 | `Filter(RG_Kategorien; Aktiv = true)` beim Start lädt **alle** aktiven Kategorien aller Rundgänge, danach wird lokal gefiltert (**belegt**, `btnRgAktion.OnSelect`, lokaler Filter mit `As`) | Bleiben die Kategorien alter Fassungen aktiv, wächst diese Menge mit jeder Fassung. Ab der Zeilengrenze 2000 fehlen Kategorien beim Start. v2 sagt nicht, was mit alten Kategorien passiert. → Beim Aktivieren alte Kategorien auf `Aktiv = Nein` setzen (gefahrlos, siehe 6). | mittel |
| K8 | Rechte, gleichzeitiges Bearbeiten | Zwei Personen am selben Entwurf überschreiben sich. → Je Rundgang nur ein Entwurf, mit Anzeige „Entwurf von <Name> seit <Datum>“. | niedrig |
| K9 | Der Plan ist in v2 Teil der Kopie | Der Plan ist kein Inhalt, sondern „wann“. Wer nur den Wochentag ändern will, braucht keine neue Fassung. → Plan direkt änderbar, mit Hinweis „wirkt ab sofort“. | niedrig |

Was an v2 richtig bleibt: Der Builder ändert nie die **aktive** Fassung. Es wird nichts gelöscht, was je live war. Es gibt zwei Apps, keine Konfiguration im Builder und einen Status je Rundgang. Kopieren statt Teilen gilt, ebenso Vorlagen in v1 und Paket 7.

## 3. Neue Wege (gesammelt und bewertet)

Bewertet nach Einfachheit für die Bauenden (E), Fehlersicherheit (F), Bauaufwand für dich (A, + = wenig), Risiko für die Rundgang-App (R, + = keins).

| Nr | Idee | E | F | A | R | Urteil |
|---|---|---|---|---|---|---|
| W1 | **Fassung an den Bereichen**, Umschalten beim Aktivieren (statt Rundgang-Kopie) | + | + | + | + | **nehmen** (Abschnitt 4A) |
| W2 | Entwurf als **ein JSON-Dokument** (lokal bearbeiten, beim Aktivieren in die Listen schreiben) | + | o | − | o | verwerfen. Schnell beim Klicken, aber: Grenze der Mehrzeilenspalte (UNSICHER), Umwandlung beim Aktivieren mit Abbildung aller Nummern, keine Vorschau in der Rundgang-App möglich. |
| W3 | **Gliederung + Editor + Vorschau auf einem Bildschirm** | + | + | o | + | **nehmen** (4B) |
| W4 | Durchklicken über 4 Bildschirme (v1/v2) | o | o | + | + | nur, falls am Tablet gebaut wird (Frage 1) |
| W5 | **Typ als Kachel „Was tut der Prüfer?“** (Abhaken, Zahl ablesen, Aus Liste wählen, Mehrere wählen, Text, Datum) mit Mini-Vorschau. Nur die zum Typ passenden Felder werden gezeigt. | + | + | + | + | **nehmen** |
| W6 | **Regeln als Sätze:** „Mangel, wenn unter [100] oder über [1000] [Stück]“, „Was passiert außerhalb? ○ Mangel ○ Hinweis mit Begründung ○ nicht speicherbar (Tippfehler)“, „Nur zeigen, wenn [Frage ▼] [n.i.O. ▼] ist“ | + | + | o | + | **nehmen** |
| W7 | **Nachweis-Block** pro Prüfpunkt: Foto ○ nie ○ freiwillig ○ Pflicht bei Mangel ○ immer Pflicht · Kommentar ○ nur bei Mangel ○ immer | + | + | + | Paket 7 | **nehmen** |
| W8 | **Vorlagen-Rundgang** statt Liste `RG_Vorlagen` | + | + | + | + | **nehmen** (4C) |
| W9 | **Mehrere Prüfpunkte einfügen** (eine Frage pro Zeile, Typ für alle wählbar) | + | o | + | + | **nehmen** |
| W10 | **Aus Excel einfügen** (Spalten Bereich, Kategorie, Frage, Typ, Pflicht, Foto, Min, Max, Einheit, Werte) mit Vorschau und Fehlerliste | + | o | − | + | **nehmen, aber in Stufe 3**. Zuerst wichtig, falls der Fachbereich Excel schickt (Frage 2). |
| W11 | **Duplizieren** auf jeder Ebene + **„Aus anderem Rundgang holen“** (Bereich/Kategorie kopieren) | + | + | o | + | **nehmen** |
| W12 | ↑/↓ + „Verschieben nach …“ | + | + | + | + | **nehmen** (Ziehen geht nicht ohne PCF) |
| W13 | **Warnzeichen an der Zeile + Fehlerleiste oben**, „Aktivieren“ gesperrt mit Grund, Fehler und Hinweise getrennt | + | + | o | + | **nehmen** (statt Bericht am Ende) |
| W14 | **Rückgängig statt Bestätigen** beim Entfernen im Entwurf | + | + | o | + | **nehmen** (letzte Entfernung merken) |
| W15 | **Änderungsübersicht** vor dem Aktivieren (neu/geändert/entfernt über `Schluessel`) | + | + | − | + | **nehmen, Stufe 3** |
| W16 | **Probelauf in der echten Rundgang-App** (Entwurf nur für Admins als Test startbar) | + | + | − | − | **später**. Braucht einen Umbau der Startseite und der Testdaten-Regel. Bis dahin: Vorschau im Builder + Kopie „ZZ Test …“ (bestehende Testregel, belegt). |
| W17 | **Rundgang per KI aus Beschreibung erzeugen** (AI-Builder-Prompt) | + | − | − | + | verwerfen für jetzt. KI-Credits/Premium unklar (UNSICHER), Ergebnisse müsste man ohnehin prüfen. |
| W18 | **Plan als Satz** „Jeden [Mo ▼], alle [1 ▼] Woche(n), ab [Montag]“ + „Nächste Termine: …“ mit derselben Logik wie `fnPlanPasst` | + | + | o | + | **nehmen** |
| W19 | **Speichern bei jeder Änderung** mit Anzeige „gespeichert ✓“ (wie Google Forms), kein Speichern-Knopf | + | o | o | + | **nehmen**. Pro Änderung ein Patch, Doppelklick-Sperre wie gewohnt. |
| W20 | **Nullvariante:** nur SharePoint-Ansichten und Excel, kein Builder | − | − | + | + | verwerfen (IDs von Hand, deine Vorgabe „so einfach wie möglich“) |
| W21 | Leere Zustände mit nächster Aktion („Noch keine Kategorie – + Kategorie“), kurze Hilfe unter jeder Option statt Anleitung | + | o | + | + | **nehmen** |

## 4. Abwägung der großen Entscheidungen

### 4A. Wie entsteht eine neue Fassung?
| | v2: Kopie des Rundgangs | **v3: Fassung an den Bereichen** |
|---|---|---|
| Rundgang-Nummer, Plan, `R<id>-Tag` | ändern sich, Plan umhängen | **bleiben** |
| Zwei aktive Fassungen möglich | ja → Warnung nötig | **nein** (eine aktive Fassung je Rundgang) |
| Laufende Durchführung beim Aktivieren | läuft weiter (alte IDs bleiben) | **läuft weiter**: Die Kategorienliste ist beim Start eingefroren, Prüfpunkte werden nur über `KategorieID` + `Aktiv` gelesen, alte Prüfpunkte bleiben aktiv (belegt) |
| Schreiben beim Aktivieren | Rundgang, Plan umhängen, alten archivieren | 3 Sammel-Patches: alte Bereiche aus, alte Kategorien aus, neue Bereiche an. Danach die Nachlese, Fassung am Rundgang +1. Wiederholbar, falls abgebrochen. |
| Zwei Fassungen bewusst parallel (z. B. Erprobung) | geht | geht nur als **Kopie unter neuem Namen** (W11) |
| Neue Spalten | `Status`, `Version`, `VorgaengerID` am Rundgang | `Status`, `Fassung` am Rundgang, `Fassung` am Bereich, `Schluessel` an Bereich/Kategorie/Prüfpunkt |

So funktioniert es:
- **Entwurf:** Der Builder kopiert die aktiven Bereiche, Kategorien und Prüfpunkte des Rundgangs. Die Kopien bekommen dieselbe `RundgangID`, `Fassung = aktiv + 1`, Bereiche `Aktiv = Nein`, gleiche `Schluessel`. Bedingungen werden über den Schlüssel auf die neuen Nummern umgestellt.
- Unsichtbar ist der Entwurf, weil der Start nur Bereiche mit `Aktiv = true` nimmt (belegt).
- **Aktivieren:** zuerst alte Bereiche und Kategorien aus, dann neue Bereiche an. Absichtlich in dieser Reihenfolge: Startet jemand genau in dieser Sekunde, sieht er „keine aktiven Kategorien“ und versucht es noch einmal. Er bekommt nie doppelte Kategorien.
- Danach die Nachlese: Es gibt genau eine aktive Fassung.
- **Alte Fassung ansehen:** Bereiche mit `Fassung = k`, schreibgeschützt.
- **Neuer Rundgang:** Zeile mit `Aktiv = Nein`, `Status = Entwurf`, Bereiche `Fassung = 1`. Aktivieren setzt Rundgang und Bereiche aktiv.

Empfehlung: **v3**. Deine Wünsche aus v2 bleiben erfüllt:
- Änderungen laufen nur als Entwurf.
- Der Schalter „Alle zeigen“ bleibt (Entwürfe, Archivierte, Vorlagen).
- Die Warnung „alte Version noch aktiv“ wird zu einem Hinweis: „Heute läuft noch eine Durchführung mit Fassung 2. Sie wird mit Fassung 2 beendet.“ Den Fehlerfall, vor dem sie warnen sollte, gibt es nicht mehr.

### 4B. Wie sieht der Editor aus?
Vorschlag für den PC (Querformat, 1366 × 768):

```
┌ Objektrundgang TCC · Entwurf Fassung 3 von Josias · gespeichert ✓      ⚠ 2 Fehler  [Änderungen] [Aktivieren] ┐
│ GLIEDERUNG                  │ PRÜFPUNKT                                │ VORSCHAU (Tablet)       │
│ ▾ Lagerhalle          ↑ ↓ ⋯ │ Frage  [Anzahl Teile am Produkt im Regal]│ ┌─────────────────────┐ │
│   ▾ Teilelager        ↑ ↓ ⋯ │ Was tut der Prüfer?                      │ │ Anzahl Teile am …   │ │
│     ✓ Lager sauber?   ↑ ↓ ⋯ │ [✓ Abhaken] [123 Zahl] [≡ Liste] [☰ Mehr-│ │ [      ] Stück      │ │
│     ⚠ Anzahl Teile …  ↑ ↓ ⋯ │  fach] [Aa Text] [📅 Datum]              │ │ i.O. 100 bis 1000   │ │
│     + Prüfpunkt             │ i.O. zwischen [100] und [1000] [Stück]   │ └─────────────────────┘ │
│   + Kategorie               │ Außerhalb: (•) Mangel ( ) Hinweis + Grund │ Zum Ausprobieren: Wert  │
│ + Bereich                   │            ( ) nicht speicherbar          │ eingeben, n.i.O. tippen │
│ [Mehrere einfügen] [Vorlage]│ Pflicht (•) ja · Foto ( ) nie ( ) freiw.  │                         │
│ [Aus Excel] [Aus Rundgang]  │  (•) bei Mangel ( ) immer · Kommentar …   │                         │
│                             │ Nur zeigen, wenn [— immer —        ▼]     │                         │
│                             │ Hinweis für Prüfer [               ]      │                         │
└─────────────────────────────┴──────────────────────────────────────────┴─────────────────────────┘
```

- Ist links ein Bereich oder eine Kategorie gewählt, zeigt die Mitte nur Name und Hinweis. Für eine Kategorie gibt es dazu „Prüfpunkte dieser Kategorie“ als kurze Liste.
- Das Menü „⋯“ je Zeile enthält Duplizieren, Verschieben nach …, Als Vorlage speichern und Entfernen (mit Rückgängig).
- „Alle Rundgänge“ ist der Startbildschirm: eine Liste mit Status, Fassung, Plan als Satz, darunter „Neuer Rundgang“.

Wird am **Tablet** gebaut: dieselben drei Teile als Abfolge (Gliederung → Editor, Vorschau als Knopf). Das ist schlechter, aber machbar.

### 4C. Vorlagen
| | v2: Liste `RG_Vorlagen` | **v3: Rundgang „Vorlagen“** |
|---|---|---|
| neue Baukasten-Spalten | in 2 Listen + 2 Editoren pflegen | **automatisch dabei** |
| Editor | eigener | **derselbe** (Status Vorlage) |
| ganze Kategorie/Bereich als Vorlage | nein | **ja** |
| Risiko | Felder gehen still verloren | Vorlagen-Rundgang darf nie aktiv werden (Status-Regel im Builder, keine Planzeile). Name ohne „ZZ Test“. |

## 5. Empfohlenes Konzept v3 (zusammengefasst)

**Bildschirme:** (1) Alle Rundgänge, (2) Neuer Rundgang (kurzer Assistent: Name → Wann → Leer / Kopie / Vorlage / Excel), (3) Editor (Gliederung · Editor · Vorschau), (4) Aktivieren (Prüfliste + Änderungsübersicht + Bestätigen).

**Datenmodell (nur Spalten hinzufügen):**
| Liste | neu | Zweck |
|---|---|---|
| `RG_Rundgaenge` | `Status` (Auswahl Entwurf / Aktiv / Archiviert / Vorlage), `Fassung` (Zahl, aktive Fassung), `EntwurfVon` (Text), `EntwurfSeit` (Datum/Zeit) | Status, Anzeige, ein Entwurf je Rundgang. `Aktiv` wird mitgesetzt (Rundgang-App unverändert). |
| `RG_Bereiche` | `Fassung` (Zahl), `Schluessel` (Text) | Fassungen umschalten, Abgleich |
| `RG_Kategorien` | `Schluessel` (Text) | Abgleich, Bedingungen beim Kopieren |
| `RG_Pruefpunkte` | `Schluessel` (Text) | Abgleich, Änderungsübersicht, Auswertung über Fassungen |
| `RG_Plan` | – | wie heute, direkt änderbar |
| ~~`RG_Vorlagen`~~ | entfällt | Vorlagen-Rundgang |

Bestand: Vorhandene Zeilen bekommen einmalig `Fassung = 1` und einen Schlüssel. Das übernimmt der Builder beim ersten Öffnen eines Rundgangs: Er zeigt „Rundgang für den Builder vorbereiten“ und setzt die Werte per Sammel-Patch. SharePoint füllt Standardwerte bei alten Zeilen nicht nach (belegt 27.10.).

**Prüfregeln** (Fehler sperren das Aktivieren, Hinweise nicht):
- **Fehler:**
  - Kategorie ohne Prüfpunkt, Bereich ohne Kategorie, Rundgang ohne Bereich.
  - Auswahl/Mehrfach ohne Werte oder mit doppelten Werten.
  - Zahl mit Min > Max, Grenzmodus ohne Grenze.
  - Bedingung zeigt auf eine spätere oder fehlende Frage, oder der Wert passt nicht zum Typ.
  - Frage leer.
  - Kein aktiver Plan beim ersten Aktivieren.
  - `StartMontag` liegt nicht auf einem Montag.
- **Hinweise:**
  - Doppelte Fragetexte in einer Kategorie.
  - Mehr als 30 Prüfpunkte in einer Kategorie (Prüfer scrollt lange).
  - Foto „immer Pflicht“ bei vielen Punkten.
  - Rundgang heute schon gestartet (läuft mit alter Fassung zu Ende).

**Bewusst nicht drin:** Konfiguration (Admins, Empfänger), Ziehen und Ablegen, KI, Bedingungen über mehrere Ebenen, Probelauf in der Rundgang-App.

## 6. Was die Rundgang-App dazu sagt (belegt, Export 27.10. 09:09)
- `scrStart.OnVisible`: `Filter(RG_Rundgaenge, Aktiv = true)`, `Filter(RG_Plan, Aktiv = true)`. Entwürfe und Vorlagen bleiben unsichtbar, solange `Aktiv = Nein`.
- `btnRgAktion.OnSelect` (Start): `Filter(RG_Bereiche, RundgangID = varRgID && Aktiv = true)` und `Filter(RG_Kategorien, Aktiv = true)`, verknüpft über `BereichID`, eingefroren in `KategorieListe`. Bereiche eines Entwurfs (`Aktiv = Nein`) kommen nicht in einen Start.
- `scrKategorie.OnVisible`: `Filter(RG_Pruefpunkte, KategorieID = varKatID && Aktiv = true)`. Weder Bereich noch Kategorie werden hier geprüft. Deshalb darf der Builder alte Bereiche und Kategorien beim Aktivieren ausschalten, solange er die alten **Prüfpunkte aktiv lässt**. Laufende Durchführungen und die Nur-Ansicht alter Durchführungen bleiben dann vollständig.
- Testregel: `TestDatensatz = StartsWith(Title, "ZZ Test")`. Der Vorlagen-Rundgang darf so nicht heißen.
- Folge: **Für Fassungen keine Änderung an der Rundgang-App.** Nur Paket 7 (Foto „Bei Mangel Pflicht“) ist nötig.

## 7. Schnitt in Pakete (Vorschlag, Reihenfolge)
| Stufe | Paket | Inhalt |
|---|---|---|
| 0 | Paket 7 (Rundgang-App) | Foto „Bei Mangel Pflicht“ |
| 0 | Datenpaket | Spalten aus Abschnitt 5, Vorlagen-Rundgang anlegen |
| 1 | B1 Gerüst | neue App, Datenquellen, Farben wie Rundgang-App, „Alle Rundgänge“ mit Schalter |
| 1 | B2 Editor | Gliederung (flache Sammlung, ↑/↓, ⋯), Bereich/Kategorie bearbeiten, automatisches Speichern |
| 1 | B3 Prüfpunkt | Typ-Kacheln, Satz-Regeln, Nachweis-Block, Bedingung, Vorschau-Karte |
| 1 | B4 Plan | Plan als Satz + nächste Termine |
| 1 | B5 Prüfen und Aktivieren | Warnzeichen, Fehlerleiste, Entwurf anlegen (Kopie mit Schlüssel), Aktivieren/Archivieren mit Nachlese |
| 2 | B6 Schneller bauen | Vorlagen, Mehrere einfügen, Duplizieren, Aus anderem Rundgang, Rückgängig |
| 3 | B7 Excel und Übersicht | Aus Excel einfügen, Änderungsübersicht |

Stufe 1 ist ein vollständiger, benutzbarer Builder. Deine Vorgabe „Vorlagen in v1“ lässt sich erfüllen, indem B6 in die erste Auslieferung kommt. B6 braucht nichts außer B2/B3.

UNSICHER (vor dem Bau klären oder als Vorab-Test einbauen):
- Ob Studio ganze **Bildschirme** als YAML einfügen lässt oder nur Steuerelemente. Davon hängt ab, wie die Pakete für eine neue App aussehen.
- Ob `Patch` mit einer Tabelle (Sammel-Patch) die neuen IDs zuverlässig zurückgibt. Abbildung alt → neu deshalb über `Schluessel`, nicht über die Reihenfolge.
- Ob eine Komponentenbibliothek in der Umgebung erlaubt ist (Vorschau-Karte teilen statt nachbauen).
- Ob `Aktiv = true` auf SharePoint delegierbar ist. Die Zahl aktiver Kategorien bleibt durch das Ausschalten alter Fassungen ohnehin klein.

## 8. Fragen an Josias
1. **Wo wird gebaut?** Am PC (Querformat, drei Spalten nebeneinander, empfohlen) oder am Tablet (Abfolge)?
2. **Woher kommen die Rundgänge?** Schickt der Fachbereich Excel-Listen? Dann rückt „Aus Excel einfügen“ nach vorne.
3. **Fassungen ohne neue Nummer (4A)** statt Kopie des Rundgangs? Dann entfällt die Warnung „alte Version aktiv“, weil es den Fall nicht mehr gibt. Der Schalter „Alle zeigen“ bleibt.
4. **Vorlagen als Rundgang „Vorlagen“ (4C)** statt eigener Liste?

## Quellen (Suchergebnisse 30.10.2026)
- MoreApp-Regeln: https://helpcenter.moreapp.com/en/how-to-add-rules-to-your-form-moreapp, https://help.moreapp.com/en/support/solutions/articles/13000080274-how-to-show-one-or-multiple-widgets-with-rules-moreapp
- SafetyCulture-Logik und Bewertungen: https://help.safetyculture.com/002285, https://fluix.io/blog/safetyculture-review, https://www.capterra.com/p/141080/iAuditor/reviews/, https://www.saasworthy.com/product/safetyculture-iauditor/reviews, https://softwareadvice.com/cmms/iauditor-profile/reviews/
- Lumiform-Logik und Abschnitte: https://help.lumiformapp.com/en/knowledge/add-logics-to-your-checklists, https://help.lumiformapp.com/en/knowledge/how-to-create-and-delete-sections-and-pages
- Microsoft Forms vs. Google Forms (Logik je Frage vs. je Abschnitt): https://www.jotform.com/blog/microsoft-forms-vs-google-forms
- Assistent vs. eine Seite: https://design.mirakl.com/design/patterns/progressive-disclosure, https://learn.microsoft.com/en-us/windows/win32/uxguide/win-wizards
- Liste und Detail: https://learn.microsoft.com/dual-screen/design/list-detail, https://www.saasui.design/blog/saas-list-detail-master-detail-ux-patterns
- Rückgängig statt Bestätigen: https://developer.gnome.org/hig/patterns/feedback/dialogs.html, https://www.nngroup.com/articles/confirmation-dialog/
- Prüfung vor dem Veröffentlichen: https://moj-forms.service.justice.gov.uk/testing-and-publishing, https://docs.oracle.com/en/cloud/saas/field-service/faadu/t-validate-template-in-form-configuration.html, https://www.opencms.org/en/article/notes/Improved-content-validation-in-the-form-editor
- Vorlagen und leeres Blatt: https://apostrophecms.com/extensions/template-library, https://docs.agiled.app/docs/templates/form-template-library
- XLSForm vs. Klick-Editor: https://support.kobotoolbox.org/getting_started_xlsform.html, https://cartong.pages.gitlab.cartong.org/learning-corner/en/5_survey_design_mdc/5_6_form/5_6_1_tools
- Excel einfügen in Power Apps: https://powerusers.microsoft.com/t5/Power-Apps-Community-Blog/Pasting-Excel-data-displaying-and-patching-to-data-source/ba-p/1313138
- Sortieren und Ziehen in Power Apps: https://matthewdevaney.com/power-apps-drag-drop-kanban-tutorial, https://powerusers.microsoft.com/t5/Webinars-and-Video-Gallery/Power-Apps-Reorder-Collection-Items-in-a-Gallery/td-p/657480
- Baum in Power Apps: https://www.canviz.com/power-apps-tree-control/amp/
