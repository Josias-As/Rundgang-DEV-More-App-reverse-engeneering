# Paket 27 – Builder: Prüfpunkt-Bereich ohne Überlappung, unten nichts abgeschnitten

Stand 13.11.2026. Erzeugt mit `werkzeuge/builder.py` und `werkzeuge/doc_paket27.py`. **Voraussetzung:** im Builder Paket 24 (alle Lage-Werte B2.x in `conPRest`) und Paket 26. Vorher-Fassungen = dieser Stand (Export 13.11. + P24-Lage + P26). Rundgang DEV ändert sich nicht.

## Kurzfassung

- **„Verlauf/Vergleich ›“** lag im Zahl-Bereich direkt unter „i.O. bis“/„nicht erlaubt“ und deckte sie zum Teil ab. Er steht jetzt **unten rechts neben „Bei n.i.O. ›“** (nur bei Zahl). Ob Verlauf/Vergleich eingestellt ist, zeigt die Füllung (hellblau wie beim 🔑); der Text ist immer „Verlauf/Vergleich ›“ (der alte Text „…: an ›“ passte nicht).
- **„Bei n.i.O. ›“** wurde unten abgeschnitten: Bei Zahl endete er genau am Rand des Bereichs (648 px). Durch den kürzeren Zahl-Bereich (ohne den Knopf) und eine 8 px flachere Zeile „Info ⓘ“ endet er jetzt 12 px über dem Rand.
- **Neue Generator-Prüfung:** Alle Steuerelemente in `conEdP` werden für **jeden Eingabetyp** als Rechtecke gezeichnet (sichtbare je Typ, Bildschirm 768 px). Geprüft: keine Überlappung, nichts ragt aus seinem Container, unten 6 px Rand. Mutation 15/15 (zwei neue Fälle: Überlappung, abgeschnitten). Ergebnis:

- IONIO     32 Steuerelemente, unterster Rand 576 von 648 px
- ZAHL      39 Steuerelemente, unterster Rand 636 von 648 px
- AUSWAHL   30 Steuerelemente, unterster Rand 630 von 648 px
- MEHRFACH  30 Steuerelemente, unterster Rand 630 von 648 px
- TEXT      27 Steuerelemente, unterster Rand 512 von 648 px
- DATUM     27 Steuerelemente, unterster Rand 512 von 648 px
- DATUMZEIT 27 Steuerelemente, unterster Rand 512 von 648 px

- Kein Scrollen nötig: Ein klassischer Container kann nicht scrollen. Ein Umbau auf einen automatischen vertikalen Container würde alle Lage-Werte ändern.
- Umfang: 1 Knopf verschieben (löschen + YAML einfügen), 16 Properties. Keine Daten, keine Formel-Logik. **Nicht in Studio getestet.**

## B1 – „Verlauf/Vergleich ›“ verschieben

1. Strukturansicht: `scrEditor › conEdMitte › conEdP › conPZahl › btnPZahlMehr` → **Löschen**. Keine andere Formel verweist auf den Knopf.
2. **`conEdP`** markieren → Strg+V mit diesem YAML. Der Knopf landet direkt in `conEdP` (nicht in einem Unter-Container) und behält den Namen `btnPZahlMehr`.

```yaml
- btnPZahlMehr:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrPrimaer
      BorderThickness: =1
      Color: =clrPrimaer
      DisabledBorderColor: =clrGesperrtHell
      DisabledColor: =clrGesperrt
      DisabledFill: =clrGesperrtHell
      DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
      Fill: =If(!IsBlank(LookUp(colP, ID = varAuswahlID).AbwMax) || Coalesce(LookUp(colP, ID = varAuswahlID).NurSteigend, false) || Coalesce(LookUp(colP, ID = varAuswahlID).VergleichPunkt, 0) <> 0, clrPrimaerHell, clrKarte)
      Font: =Font.'Segoe UI'
      Height: =32
      HoverColor: =clrPrimaer
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =If(!varIsLoading,
            Reset(txtZaAbwMax);
            Reset(txtZaTol);
            Reset(ddZaVgl);
            Set(varZaOffen, true)
        )
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =12
      Text: ="Verlauf/Vergleich  ›"
      Visible: =(LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "ZAHL")
      Width: =204
      X: =324
      Y: =If((LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "ZAHL"), 356, (LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"), 350, (LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "IONIO"), 296, 232) + 248
```

**Nachprüfen:** `btnPZahlMehr.Visible` endet auf `= "ZAHL")`, `X` = 324, `Width` = 204. Bei einem Prüfpunkt vom Typ Zahl steht der Knopf unten rechts neben „Bei n.i.O. ›“.

## B2 – geänderte Properties

### B2.1 · `btnPBild.Height`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › btnPBild` → Height

```
36
```

```diff
-44
+36
```

**Kurz erklärt:** 36 wie alle Felder.

**Nachprüfen:** endet auf `36`

### B2.2 · `btnPBild.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › btnPBild` → Width

```
212
```

```diff
-204
+212
```

**Kurz erklärt:** Bis 8 px vor das Vorschaubild.

**Nachprüfen:** endet auf `212`

### B2.3 · `btnPNio.Size`

**Pfad:** `scrEditor › conEdMitte › conEdP › btnPNio` → Size

```
12
```

```diff
-13
+12
```

**Kurz erklärt:** 12 statt 13, damit auch „⚠ Bei n.i.O.: Rückfrage + kritisch ›“ in 316 px passt.

**Nachprüfen:** endet auf `12`

### B2.4 · `btnPNio.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › btnPNio` → Width

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 316; 528)
```

```diff
-528
+If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 316; 528)
```

**Kurz erklärt:** Bei Zahl 316 breit (rechts daneben „Verlauf/Vergleich ›“), sonst ganze Breite.

**Nachprüfen:** endet auf `If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 316; 528)`

### B2.5 · `btnPNio.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › btnPNio` → Y

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 356; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232) + 248
```

```diff
- … ookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = …
+ … ookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 356; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = …
```

**Kurz erklärt:** Unterste Zeile: 248 unter dem Beginn des Rest-Bereichs. Bei Zahl endet sie 12 px über dem Rand (vorher genau am Rand → abgeschnitten).

**Nachprüfen:** endet auf `0; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232) + 248`

### B2.6 · `conPRest.Height`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest` → Height

```
242
```

```diff
-250
+242
```

**Kurz erklärt:** 242 statt 250 (Zeile „Info ⓘ“ ist 8 px flacher).

**Nachprüfen:** endet auf `242`

### B2.7 · `conPRest.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest` → Y

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 356; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232)
```

```diff
- … ookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = …
+ … ookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 356; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = …
```

**Kurz erklärt:** Steht bei Zahl 4 px höher (356 statt 360), weil der Zahl-Bereich kürzer ist.

**Nachprüfen:** endet auf `"); 350; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232)`

### B2.8 · `conPZahl.Height`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPZahl` → Height

```
118
```

```diff
-120
+118
```

**Kurz erklärt:** Der Zahl-Bereich endet jetzt unter „Mangel / Hinweis + Grund / nicht speicherbar“ (der Knopf „Verlauf/Vergleich“ ist nicht mehr darin).

**Nachprüfen:** endet auf `118`

### B2.9 · `ddPAnl.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPAnl` → Y

```
144
```

```diff
-148
+144
```

**Kurz erklärt:** Anleitung-Auswahl auf gleicher Höhe wie „Bild wählen“.

**Nachprüfen:** endet auf `144`

### B2.10 · `ddPKategorie.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPKategorie` → Y

```
206
```

```diff
-214
+206
```

**Kurz erklärt:** Nur Lage/Größe (enger gesetzt, damit unten alles sichtbar bleibt).

**Nachprüfen:** endet auf `206`

### B2.11 · `imgPBild.Height`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › imgPBild` → Height

```
36
```

```diff
-44
+36
```

**Kurz erklärt:** 36 × 36.

**Nachprüfen:** endet auf `36`

### B2.12 · `imgPBild.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › imgPBild` → Width

```
36
```

```diff
-44
+36
```

**Kurz erklärt:** 36 × 36.

**Nachprüfen:** endet auf `36`

### B2.13 · `imgPBild.X`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › imgPBild` → X

```
492
```

```diff
-484
+492
```

**Kurz erklärt:** Vorschaubild 36 × 36 rechts bündig.

**Nachprüfen:** endet auf `492`

### B2.14 · `lblPAbschnitt.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPAbschnitt` → Y

```
186
```

```diff
-194
+186
```

**Kurz erklärt:** Nur Lage/Größe (enger gesetzt, damit unten alles sichtbar bleibt).

**Nachprüfen:** endet auf `186`

### B2.15 · `lblPKat.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPKat` → Y

```
186
```

```diff
-194
+186
```

**Kurz erklärt:** Nur Lage/Größe (enger gesetzt, damit unten alles sichtbar bleibt).

**Nachprüfen:** endet auf `186`

### B2.16 · `txtPAbschnitt.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › txtPAbschnitt` → Y

```
206
```

```diff
-214
+206
```

**Kurz erklärt:** Nur Lage/Größe (enger gesetzt, damit unten alles sichtbar bleibt).

**Nachprüfen:** endet auf `206`

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | Prüfpunkt Typ **Zahl** öffnen (Fenster 1366 × 768) | „i.O. bis“, „nicht erlaubt“ frei; unten links „Bei n.i.O.: … ›“, rechts „Verlauf/Vergleich ›“, beide ganz sichtbar |
| T2 | „Verlauf/Vergleich ›“ antippen, Vergleich einstellen, Fertig | Fenster öffnet wie bisher; danach Knopf hellblau gefüllt |
| T3 | Typ **i.O./n.i.O.**, **Auswahl**, **Text** | „Bei n.i.O. ›“ über die ganze Breite, unten nichts abgeschnitten, kein „Verlauf/Vergleich“ |
| T4 | Zeile „Info ⓘ“ | Anleitung und „Bild wählen“ auf einer Höhe, Vorschaubild rechts 36 × 36 |
| T5 | Prüfpunkt kritisch + Rückfrage, Typ Zahl | Text „⚠ Bei n.i.O.: Rückfrage + kritisch ›“ passt in den Knopf |

## Rückweg

Vorher-Fassungen einsetzen; `btnPZahlMehr` in `conEdP` löschen und das YAML aus dem Anhang in `conPZahl` einfügen.

## Anhang – Vorher-Fassungen

**Builder `btnPBild.Height` vorher**

```
44
```

**Builder `btnPBild.Width` vorher**

```
204
```

**Builder `btnPNio.Size` vorher**

```
13
```

**Builder `btnPNio.Width` vorher**

```
528
```

**Builder `btnPNio.Y` vorher**

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232) + 256
```

**Builder `conPRest.Height` vorher**

```
250
```

**Builder `conPRest.Y` vorher**

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232)
```

**Builder `conPZahl.Height` vorher**

```
120
```

**Builder `ddPAnl.Y` vorher**

```
148
```

**Builder `ddPKategorie.Y` vorher**

```
214
```

**Builder `imgPBild.Height` vorher**

```
44
```

**Builder `imgPBild.Width` vorher**

```
44
```

**Builder `imgPBild.X` vorher**

```
484
```

**Builder `lblPAbschnitt.Y` vorher**

```
194
```

**Builder `lblPKat.Y` vorher**

```
194
```

**Builder `txtPAbschnitt.Y` vorher**

```
214
```

**`btnPZahlMehr` vorher (in `conPZahl`), Properties:**

```
BorderColor: clrPrimaer
BorderThickness: 1
Color: clrPrimaer
DisabledBorderColor: clrGesperrtHell
DisabledColor: clrGesperrt
DisabledFill: clrGesperrtHell
DisplayMode: If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
Fill: clrKarte
Font: Font.'Segoe UI'
Height: 26
HoverColor: clrPrimaer
HoverFill: clrPrimaerHell
OnSelect: If(!varIsLoading;
    Reset(txtZaAbwMax);;
    Reset(txtZaTol);;
    Reset(ddZaVgl);;
    Set(varZaOffen; true)
)
PressedColor: clrPrimaer
PressedFill: clrPrimaerHell
RadiusBottomLeft: 6
RadiusBottomRight: 6
RadiusTopLeft: 6
RadiusTopRight: 6
Size: 12
Text: If(!IsBlank(LookUp(colP; ID = varAuswahlID).AbwMax) || Coalesce(LookUp(colP; ID = varAuswahlID).NurSteigend; false) || Coalesce(LookUp(colP; ID = varAuswahlID).VergleichPunkt; 0) <> 0; "Verlauf/Vergleich: an  ›"; "Verlauf/Vergleich  ›")
Width: 212
X: 316
Y: 56
```

