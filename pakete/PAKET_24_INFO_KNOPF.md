# Paket 24 – Ein Info-Knopf ⓘ für Anleitung und Beispielbild

Stand 06.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket24), `werkzeuge/builder.py`, `werkzeuge/doc_paket24.py`. Voraussetzung: Paket 23, 18, 11 und **25 (Rückbau Prüferauswahl)** in beiden Apps. Nach Paket 25 neu geprüft: keine gemeinsame Property, Vorher-Fassungen unverändert gültig.

## Kurzfassung

- **Rundgang DEV:** Pro Prüfpunkt nur noch **ein** runder Knopf **ⓘ** oben rechts, sichtbar bei Anleitung, Beispielbild oder beidem. Der Bild-Knopf („Bild“) und sein Fenster entfallen.
- Das Fenster passt sich an: **nur Text** → Text auf voller Höhe; **nur Bild** → großes Bild, Überschrift „ⓘ Beispielbild“, darunter die Frage; **beides** → Text oben, Bild unten (wie bisher).
- **Builder:** Im Prüfpunkt steht in der Zeile „Info ⓘ“ links die **Anleitung**, rechts das **Beispielbild** – unabhängig, beide optional. Der Hinweis für den Prüfer rückt dafür nach oben rechts neben „Foto“ (mit 🔑). Ein Bild pro Prüfpunkt.
- Umfang: App 10 Properties (+ 2 Steuerelemente löschen); Builder 20 Properties (nur Lage/Text). Keine Daten. Generatoren 0 Fehler, Mutation 12/12 und 13/13. **Nicht in Studio getestet.** Leicht unabhängig geprüft, Befunde eingearbeitet (`arbeit/2026-11-06_Paket24/pruefung_unabhaengig.md`).

## Teil A – Rundgang DEV

### A1 – SharePoint und Daten (zuerst)

Keine neuen Spalten oder Listen.

### A3 – geänderte Properties

### A3.1 · `btnKaInfo.Visible`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaInfo` → Visible

```
(ThisItem.AnlID > 0 || ThisItem.BildID > 0)
```

```diff
-ThisItem.AnlID > 0
+(ThisItem.AnlID > 0 || ThisItem.BildID > 0)
```

**Kurz erklärt:** ⓘ erscheint, wenn eine (aktive) Anleitung **oder** ein Beispielbild hinterlegt ist.

**Nachprüfen:** endet auf `(ThisItem.AnlID > 0 || ThisItem.BildID > 0)`

### A3.2 · `btnKaInfo.X`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaInfo` → X

```
Parent.Width - 60
```

```diff
-Parent.Width - 60 - If(ThisItem.BildID > 0; 80; 0)
+Parent.Width - 60
```

**Kurz erklärt:** ⓘ steht ganz rechts (der Bild-Knopf entfällt).

**Nachprüfen:** endet auf `Parent.Width - 60`

### A3.3 · `btnKaInfo.OnSelect`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaInfo` → OnSelect

```
Set(varInfoFrage; ThisItem.Frage);;
Set(varInfoBild; ThisItem.BildID);;
Set(varInfo; If(ThisItem.AnlID > 0; LookUp(RG_Anleitungen; ID = ThisItem.AnlID)));;
If(IsBlank(varInfo.ID) && ThisItem.BildID = 0;
    Notify("Die Anleitung wurde nicht gefunden."; NotificationType.Warning);
    Set(varInfoID; 1)
)
```

```diff
-Set(varInfo; LookUp(RG_Anleitungen; ID = ThisItem.AnlID));;
-If(IsBlank(varInfo.ID); Notify("Die Anleitung wurde nicht gefunden."; NotificationType.Warning); Set(varInfoID; ThisItem.AnlID))
+Set(varInfo; If(ThisItem.AnlID > 0; LookUp(RG_Anleitungen; ID = ThisItem.AnlID)));;
+If(IsBlank(varInfo.ID) && ThisItem.BildID = 0;
+    Notify("Die Anleitung wurde nicht gefunden."; NotificationType.Warning);
+    Set(varInfoID; 1)
+)
```

**Kurz erklärt:** Öffnet das Fenster auch ohne Anleitung (nur Bild). `varInfoID` ist jetzt nur noch „Fenster offen“ (1). Anleitung gelöscht und kein Bild → Meldung.

**Nachprüfen:** endet auf `)`

### A3.4 · `btnKaBild.Visible`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaBild` → Visible

```
false
```

```diff
-ThisItem.BildID > 0
+false
```

**Kurz erklärt:** Der alte Bild-Knopf wird ausgeblendet. **Besser:** `btnKaBild` und das alte Bild-Fenster `conKaBild` ganz löschen – keine andere Formel verweist darauf (maschinell geprüft). Dann diesen Schritt überspringen.

**Nachprüfen:** endet auf `false`

### A3.5 · `btnKaCode.X`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaCode` → X

```
Parent.Width - 60 - If((ThisItem.AnlID > 0 || ThisItem.BildID > 0); 48; 0)
```

```diff
-Parent.Width - 60 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 48; 0)
+Parent.Width - 60 - If((ThisItem.AnlID > 0 || ThisItem.BildID > 0); 48; 0)
```

**Kurz erklärt:** 🔑 rückt neben ⓘ.

**Nachprüfen:** endet auf `Parent.Width - 60 - If((ThisItem.AnlID > 0 || ThisItem.BildID > 0); 48; 0)`

### A3.6 · `lblKaFrage.Width`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaFrage` → Width

```
Parent.Width - 40 - If((ThisItem.AnlID > 0 || ThisItem.BildID > 0); 64; 0) - If(ThisItem.CodeID > 0; 48; 0)
```

```diff
-Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0) - If(ThisItem.CodeID > 0; 48; 0)
+Parent.Width - 40 - If((ThisItem.AnlID > 0 || ThisItem.BildID > 0); 64; 0) - If(ThisItem.CodeID > 0; 48; 0)
```

**Kurz erklärt:** Platz nur noch für ⓘ und 🔑.

**Nachprüfen:** endet auf `sItem.AnlID > 0 || ThisItem.BildID > 0); 64; 0) - If(ThisItem.CodeID > 0; 48; 0)`

### A3.7 · `lblKaInfoTitel.Text`

**Pfad:** `scrKategorie › conKaInfo › conKaInfoKarte › lblKaInfoTitel` → Text

```
If(IsBlank(varInfo.ID); "ⓘ Beispielbild"; "ⓘ " & varInfo.Title)
```

```diff
-"ⓘ " & varInfo.Title
+If(IsBlank(varInfo.ID); "ⓘ Beispielbild"; "ⓘ " & varInfo.Title)
```

**Kurz erklärt:** Nur Bild: „ⓘ Beispielbild“, darunter wie bisher „zu: <Frage>“. Mit Anleitung: ⓘ + Titel der Anleitung.

**Nachprüfen:** endet auf `If(IsBlank(varInfo.ID); "ⓘ Beispielbild"; "ⓘ " & varInfo.Title)`

### A3.8 · `lblKaInfoText.Height`

**Pfad:** `scrKategorie › conKaInfo › conKaInfoKarte › lblKaInfoText` → Height

```
If(IsBlank(varInfo.ID); 0; varInfoBild > 0; (Parent.Height - 180) * 0,55; Parent.Height - 180)
```

```diff
-If(varInfoBild > 0; (Parent.Height - 180) * 0,55; Parent.Height - 180)
+If(IsBlank(varInfo.ID); 0; varInfoBild > 0; (Parent.Height - 180) * 0,55; Parent.Height - 180)
```

**Kurz erklärt:** Ohne Anleitung Höhe 0 → das Bild bekommt den ganzen Platz.

**Nachprüfen:** endet auf `Info.ID); 0; varInfoBild > 0; (Parent.Height - 180) * 0,55; Parent.Height - 180)`

### A3.9 · `imgKaInfo.Y`

**Pfad:** `scrKategorie › conKaInfo › conKaInfoKarte › imgKaInfo` → Y

```
lblKaInfoText.Y + lblKaInfoText.Height + If(lblKaInfoText.Height > 0; 8; 0)
```

```diff
-96 + (Parent.Height - 180) * 0,55
+lblKaInfoText.Y + lblKaInfoText.Height + If(lblKaInfoText.Height > 0; 8; 0)
```

**Kurz erklärt:** Bild direkt unter dem Text (bzw. oben, wenn es keinen Text gibt).

**Nachprüfen:** endet auf `lblKaInfoText.Y + lblKaInfoText.Height + If(lblKaInfoText.Height > 0; 8; 0)`

### A3.10 · `imgKaInfo.Height`

**Pfad:** `scrKategorie › conKaInfo › conKaInfoKarte › imgKaInfo` → Height

```
Max(Parent.Height - 92 - Self.Y; 0)
```

```diff
-(Parent.Height - 180) * 0,45 - 8
+Max(Parent.Height - 92 - Self.Y; 0)
```

**Kurz erklärt:** Bild füllt den Rest bis über „Schließen“.

**Nachprüfen:** endet auf `Max(Parent.Height - 92 - Self.Y; 0)`

## Teil B – Builder

### B0 – Daten

Keine neuen Daten.

### B2.1 · `btnPBild.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › btnPBild` → Width

```
204
```

```diff
-124
+204
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `204`

### B2.2 · `btnPBild.X`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › btnPBild` → X

```
272
```

```diff
-352
+272
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `272`

### B2.3 · `btnPCode.Height`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › btnPCode` → Height

```
36
```

```diff
-44
+36
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `36`

### B2.4 · `btnPCode.X`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › btnPCode` → X

```
480
```

```diff
-298
+480
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `480`

### B2.5 · `btnPCode.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › btnPCode` → Y

```
20
```

```diff
-144
+20
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `20`

### B2.6 · `ddPAnl.X`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPAnl` → X

```
0
```

```diff
-272
+0
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `0`

### B2.7 · `ddPAnl.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPAnl` → Y

```
148
```

```diff
-20
+148
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `148`

### B2.8 · `lblPAnl.Text`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPAnl` → Text

```
"Info ⓘ: Anleitung (optional)"
```

```diff
-"Anleitung (ⓘ beim Prüfer)"
+"Info ⓘ: Anleitung (optional)"
```

**Kurz erklärt:** „Info ⓘ: Anleitung“.

**Nachprüfen:** endet auf `"Info ⓘ: Anleitung (optional)"`

### B2.9 · `lblPAnl.X`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPAnl` → X

```
0
```

```diff
-272
+0
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `0`

### B2.10 · `lblPAnl.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPAnl` → Y

```
124
```

```diff
-0
+124
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `124`

### B2.11 · `lblPBild.Text`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPBild` → Text

```
"Info ⓘ: Beispielbild (optional)"
```

```diff
-"Beispielbild"
+"Info ⓘ: Beispielbild (optional)"
```

**Kurz erklärt:** „Info ⓘ: Beispielbild“.

**Nachprüfen:** endet auf `"Info ⓘ: Beispielbild (optional)"`

### B2.12 · `lblPBild.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPBild` → Width

```
256
```

```diff
-176
+256
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `256`

### B2.13 · `lblPBild.X`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPBild` → X

```
272
```

```diff
-352
+272
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `272`

### B2.14 · `lblPHinweis.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPHinweis` → Width

```
256
```

```diff
-340
+256
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `256`

### B2.15 · `lblPHinweis.X`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPHinweis` → X

```
272
```

```diff
-0
+272
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `272`

### B2.16 · `lblPHinweis.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPHinweis` → Y

```
0
```

```diff
-124
+0
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `0`

### B2.17 · `txtPHinweis.Height`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › txtPHinweis` → Height

```
36
```

```diff
-44
+36
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `36`

### B2.18 · `txtPHinweis.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › txtPHinweis` → Width

```
202
```

```diff
-292
+202
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `202`

### B2.19 · `txtPHinweis.X`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › txtPHinweis` → X

```
272
```

```diff
-0
+272
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `272`

### B2.20 · `txtPHinweis.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › txtPHinweis` → Y

```
20
```

```diff
-144
+20
```

**Kurz erklärt:** Nur Lage/Größe: Anleitung und Bild nebeneinander in der Zeile „Info ⓘ“, Hinweis oben rechts.

**Nachprüfen:** endet auf `20`

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | Prüfpunkt nur mit Anleitung | ⓘ → Text auf voller Höhe, kein Bildbereich |
| T2 | Prüfpunkt nur mit Beispielbild (lange Frage) | ⓘ → „ⓘ Beispielbild“, darunter „zu: …“, großes Bild |
| T3 | Prüfpunkt mit beidem | Text oben, Bild unten |
| T4 | Prüfpunkt mit ⓘ + 🔑 | zwei runde Knöpfe rechts, Frage gekürzt, nichts überlappt |
| T5 | Anleitung inaktiv, Bild vorhanden | ⓘ zeigt nur das Bild (inaktive Anleitungen kommen seit Paket 13 als `AnlID` 0 an) |
| T5b | Anleitung in SharePoint gelöscht, kein Bild | ⓘ → Meldung „Die Anleitung wurde nicht gefunden.“ |
| T5c | `btnKaBild`/`conKaBild` gelöscht | App-Prüfung ohne neue Fehler |
| T6 | Builder: Prüfpunkt öffnen | Zeile „Info ⓘ: Anleitung“ links, „Info ⓘ: Beispielbild“ rechts; Hinweis oben rechts mit 🔑 |

## Rückweg

Vorher-Fassungen einsetzen. Falls `btnKaBild`/`conKaBild` gelöscht wurden: aus Paket 6 (YAML) wieder einfügen.

## Anhang – Vorher-Fassungen

**Rundgang DEV `btnKaInfo.Visible` vorher**

```
ThisItem.AnlID > 0
```

**Rundgang DEV `btnKaInfo.X` vorher**

```
Parent.Width - 60 - If(ThisItem.BildID > 0; 80; 0)
```

**Rundgang DEV `btnKaInfo.OnSelect` vorher**

```
Set(varInfoFrage; ThisItem.Frage);;
Set(varInfoBild; ThisItem.BildID);;
Set(varInfo; LookUp(RG_Anleitungen; ID = ThisItem.AnlID));;
If(IsBlank(varInfo.ID); Notify("Die Anleitung wurde nicht gefunden."; NotificationType.Warning); Set(varInfoID; ThisItem.AnlID))
```

**Rundgang DEV `btnKaBild.Visible` vorher**

```
ThisItem.BildID > 0
```

**Rundgang DEV `btnKaCode.X` vorher**

```
Parent.Width - 60 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 48; 0)
```

**Rundgang DEV `lblKaFrage.Width` vorher**

```
Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0) - If(ThisItem.CodeID > 0; 48; 0)
```

**Rundgang DEV `lblKaInfoTitel.Text` vorher**

```
"ⓘ " & varInfo.Title
```

**Rundgang DEV `lblKaInfoText.Height` vorher**

```
If(varInfoBild > 0; (Parent.Height - 180) * 0,55; Parent.Height - 180)
```

**Rundgang DEV `imgKaInfo.Y` vorher**

```
96 + (Parent.Height - 180) * 0,55
```

**Rundgang DEV `imgKaInfo.Height` vorher**

```
(Parent.Height - 180) * 0,45 - 8
```

**Builder `btnPBild.Width` vorher**

```
124
```

**Builder `btnPBild.X` vorher**

```
352
```

**Builder `btnPCode.Height` vorher**

```
44
```

**Builder `btnPCode.X` vorher**

```
298
```

**Builder `btnPCode.Y` vorher**

```
144
```

**Builder `ddPAnl.X` vorher**

```
272
```

**Builder `ddPAnl.Y` vorher**

```
20
```

**Builder `lblPAnl.Text` vorher**

```
"Anleitung (ⓘ beim Prüfer)"
```

**Builder `lblPAnl.X` vorher**

```
272
```

**Builder `lblPAnl.Y` vorher**

```
0
```

**Builder `lblPBild.Text` vorher**

```
"Beispielbild"
```

**Builder `lblPBild.Width` vorher**

```
176
```

**Builder `lblPBild.X` vorher**

```
352
```

**Builder `lblPHinweis.Width` vorher**

```
340
```

**Builder `lblPHinweis.X` vorher**

```
0
```

**Builder `lblPHinweis.Y` vorher**

```
124
```

**Builder `txtPHinweis.Height` vorher**

```
44
```

**Builder `txtPHinweis.Width` vorher**

```
292
```

**Builder `txtPHinweis.X` vorher**

```
0
```

**Builder `txtPHinweis.Y` vorher**

```
144
```

