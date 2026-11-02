# Paket 12+16 – Builder: eigene Antwortwörter, „nicht messbar“

Stand 02.11.2026. Erzeugt mit `werkzeuge/builder.py` und `werkzeuge/doc_paket12_16.py`. **Voraussetzung: Paket 8 und Paket 9 (Builder) eingefügt.**

## Kurzfassung

- **Paket 12 – eigene Antwortwörter:** Bei i.O./n.i.O.-Fragen lassen sich die Knöpfe umbenennen, z. B. „durchgeführt“ / „nicht durchgeführt“ (Legionellen). Intern bleibt es i.O./n.i.O.: „nicht durchgeführt“ ergibt weiter einen Mangel. Leer = „i.O.“/„n.i.O.“ wie bisher. Protokoll zeigt die eigenen Wörter. Höchstens 18 Zeichen.
- **Paket 16 – „nicht messbar“:** Bei Zahlen, für die es im Builder erlaubt ist, gibt es den Knopf „nicht messbar“ (z. B. Anlage aus). Dann ist das Feld leer, die Frage gilt als beantwortet, aber eine **Begründung (Kommentar) ist Pflicht**. Im Protokoll steht „nicht messbar“ statt „0“. Kein Mangel.
- Im Prüfpunkt-Editor: bei i.O./n.i.O. zwei Felder „Knopf heißt …“, bei Zahl der Knopf „nicht messbar: erlaubt“. Kopie, Fassungen, Änderungsliste, Vorschau und Prüfung kennen die Felder.
- Dazu: Der Erklärtext bei Kategorien sagt jetzt „beliebige Reihenfolge“ (Paket 10).
- Umfang: 3 Spalten (dieselben wie in der Rundgang-App), 2 neue Blöcke, 21 geänderte Properties. Generator 0 Fehler, Mutation 13/13, Logik 27, unabhängig geprüft. **Nicht in Studio getestet.**

## Schritt 0 – SharePoint

Die drei Spalten aus `PAKET_12_16_APP.md`, Schritt 1 (nur einmal anlegen). Im Builder: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**.

## Schritt 1 – neue Steuerelemente

### 1a · Felder für die Knopf-Wörter

**Wo hin:** **`conEdP`** (`scrEditor › conEdMitte › conEdP`) markieren → Strg+V.

```yaml
- conPIonio:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      BorderThickness: =0
      Fill: =clrHintergrund
      Height: =60
      Visible: =(LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "IONIO")
      Width: =528
      X: =0
      Y: =232
    Children:
      - lblPTextIO:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =20
            Size: =12
            Text: ="Knopf „i.O.“ heißt"
            Width: =256
            X: =0
            Y: =0
      - lblPTextNIO:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =20
            Size: =12
            Text: ="Knopf „n.i.O.“ heißt (Mangel)"
            Width: =256
            X: =272
            Y: =0
      - txtPTextIO:
          Control: Classic/TextInput@2.3.2
          Properties:
            AccessibleLabel: ="Beschriftung des i.O.-Knopfs"
            BorderColor: =clrRahmen
            Color: =clrText
            Default: =Coalesce(LookUp(colP, ID = varAuswahlID).TextIO, "")
            DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
            Fill: =clrKarte
            FocusedBorderColor: =clrPrimaer
            Font: =Font.'Segoe UI'
            Height: =36
            HintText: ="z. B. durchgeführt"
            HoverBorderColor: =clrPrimaer
            MaxLength: =18
            OnChange: |-
              =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colP, ID = varAuswahlID).TextIO, "")),
                  If(varSchreibbar && varAuswahlEbene = 3,
                      Refresh(RG_Rundgaenge);
                      Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                      If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                      If(varEntwurfOk,
                          Set(varPatchFehler, false);
                          IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {TextIO: Left(Trim(Self.Text), 18)}), Set(varPatchFehler, true));
                          If(varPatchFehler,
                              Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                              Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                              Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                          )
                      )
                  )
              )
            Size: =14
            Width: =256
            X: =0
            Y: =20
      - txtPTextNIO:
          Control: Classic/TextInput@2.3.2
          Properties:
            AccessibleLabel: ="Beschriftung des n.i.O.-Knopfs"
            BorderColor: =clrRahmen
            Color: =clrText
            Default: =Coalesce(LookUp(colP, ID = varAuswahlID).TextNIO, "")
            DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
            Fill: =clrKarte
            FocusedBorderColor: =clrPrimaer
            Font: =Font.'Segoe UI'
            Height: =36
            HintText: ="z. B. nicht durchgeführt"
            HoverBorderColor: =clrPrimaer
            MaxLength: =18
            OnChange: |-
              =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colP, ID = varAuswahlID).TextNIO, "")),
                  If(varSchreibbar && varAuswahlEbene = 3,
                      Refresh(RG_Rundgaenge);
                      Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                      If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                      If(varEntwurfOk,
                          Set(varPatchFehler, false);
                          IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {TextNIO: Left(Trim(Self.Text), 18)}), Set(varPatchFehler, true));
                          If(varPatchFehler,
                              Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                              Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                              Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                          )
                      )
                  )
              )
            Size: =14
            Width: =256
            X: =272
            Y: =20
```

### 1b · „nicht messbar“ bei Zahlen

**Wo hin:** **`conPZahl`** (`scrEditor › conEdMitte › conEdP › conPZahl`) markieren → Strg+V.

```yaml
- lblPNM:
    Control: Label@2.5.1
    Properties:
      Color: =clrTextGrau
      Font: =Font.'Segoe UI'
      Height: =20
      PaddingLeft: =0
      PaddingRight: =0
      Size: =12
      Text: ="nicht messbar"
      Width: =112
      X: =416
      Y: =0
- btnPNM:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrPrimaer
      BorderThickness: =1
      Color: =If(Coalesce(LookUp(colP, ID = varAuswahlID).NichtMessbar, false), Color.White, clrPrimaer)
      DisabledBorderColor: =clrGesperrtHell
      DisabledColor: =clrGesperrt
      DisabledFill: =clrGesperrtHell
      DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.Disabled)
      Fill: =If(Coalesce(LookUp(colP, ID = varAuswahlID).NichtMessbar, false), clrPrimaer, clrKarte)
      Font: =Font.'Segoe UI'
      Height: =36
      HoverColor: =If(Coalesce(LookUp(colP, ID = varAuswahlID).NichtMessbar, false), Color.White, clrPrimaer)
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =If(varSchreibbar && varAuswahlEbene = 3 && !varIsLoading && Now() >= varSperreBis,
            Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));
            If(varSchreibbar && varAuswahlEbene = 3,
                Refresh(RG_Rundgaenge);
                Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                If(varEntwurfOk,
                    Set(varPatchFehler, false);
                    IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {NichtMessbar: !Coalesce(LookUp(colP, ID = varAuswahlID).NichtMessbar, false)}), Set(varPatchFehler, true));
                    If(varPatchFehler,
                        Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                        Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                        Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                    )
                )
            )
        )
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =12
      Text: =If(Coalesce(LookUp(colP, ID = varAuswahlID).NichtMessbar, false), "✓ erlaubt", "nicht erlaubt")
      Width: =112
      X: =416
      Y: =20
```

**Nachprüfen:** `conPIonio` liegt in `conEdP`, `lblPNM`/`btnPNM` in `conPZahl`. Kein `_1`.

## Schritt 2 – Kleine Werte und Vorschau

### 2.1 · `lblKInfo.Text`

**Pfad:** `scrEditor › conEdMitte › conEdK › lblKInfo` → Text

```
CountRows(Filter(colP; KategorieID = varAuswahlID)) & " Prüfpunkte." & Char(10) & Char(10) & "Eine Kategorie ist eine Seite im Rundgang: Der Prüfer füllt sie aus und speichert sie als Ganzes. Der Prüfer kann die Kategorien in beliebiger Reihenfolge ausfüllen. Neuer Prüfpunkt: links „+ Prüfpunkt“."
```

```diff
-CountRows(Filter(colP; KategorieID = varAuswahlID)) & " Prüfpunkte." & Char(10) & Char(10) & "Eine Kategorie ist eine Seite im Rundgang: Der Prüfer füllt sie aus und speichert sie als Ganzes. Die Kategorien werden der Reihe nach freiges …
+CountRows(Filter(colP; KategorieID = varAuswahlID)) & " Prüfpunkte." & Char(10) & Char(10) & "Eine Kategorie ist eine Seite im Rundgang: Der Prüfer füllt sie aus und speichert sie als Ganzes. Der Prüfer kann die Kategorien in beliebiger …
```

**Kurz erklärt:** Erklärtext: Kategorien in beliebiger Reihenfolge (seit Paket 10).

**Nachprüfen:** endet auf `rien in beliebiger Reihenfolge ausfüllen. Neuer Prüfpunkt: links „+ Prüfpunkt“."`

### 2.2 · `conPRest.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest` → Y

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232)
```

```diff
-If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; 232)
+If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; (LookUp(colP; ID = varAuswahlID). …
```

**Kurz erklärt:** Bei i.O./n.i.O. rückt der untere Teil unter die neuen Felder.

**Nachprüfen:** endet auf `"); 350; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232)`

### 2.3 · `btnPNio.Y`

**Pfad:** `scrEditor › conEdMitte › conEdP › btnPNio` → Y

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232) + 256
```

```diff
-If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; 232) + 256
+If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; (LookUp(colP; ID = varAuswahlID). …
```

**Kurz erklärt:** Wie conPRest.Y.

**Nachprüfen:** endet auf `0; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "IONIO"); 296; 232) + 256`

### 2.4 · `btnVsIO.Text`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › btnVsIO` → Text

```
If(Trim(Coalesce(LookUp(colP; ID = varAuswahlID).TextIO; "")) = ""; "i.O."; LookUp(colP; ID = varAuswahlID).TextIO)
```

```diff
-"i.O."
+If(Trim(Coalesce(LookUp(colP; ID = varAuswahlID).TextIO; "")) = ""; "i.O."; LookUp(colP; ID = varAuswahlID).TextIO)
```

**Kurz erklärt:** Vorschau zeigt das eigene Wort.

**Nachprüfen:** endet auf `varAuswahlID).TextIO; "")) = ""; "i.O."; LookUp(colP; ID = varAuswahlID).TextIO)`

### 2.5 · `btnVsNIO.Text`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › btnVsNIO` → Text

```
If(Trim(Coalesce(LookUp(colP; ID = varAuswahlID).TextNIO; "")) = ""; "n.i.O."; LookUp(colP; ID = varAuswahlID).TextNIO)
```

```diff
-"n.i.O."
+If(Trim(Coalesce(LookUp(colP; ID = varAuswahlID).TextNIO; "")) = ""; "n.i.O."; LookUp(colP; ID = varAuswahlID).TextNIO)
```

**Kurz erklärt:** Vorschau zeigt das eigene Wort.

**Nachprüfen:** endet auf `uswahlID).TextNIO; "")) = ""; "n.i.O."; LookUp(colP; ID = varAuswahlID).TextNIO)`

### 2.6 · `btnVsIO.Width`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › btnVsIO` → Width

```
If(Max(Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextIO; "")); Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextNIO; ""))) > 8; 200; 120)
```

```diff
-120
+If(Max(Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextIO; "")); Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextNIO; ""))) > 8; 200; 120)
```

**Kurz erklärt:** Vorschau-Knöpfe breiter bei langen Wörtern.

**Nachprüfen:** endet auf `"")); Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextNIO; ""))) > 8; 200; 120)`

### 2.7 · `btnVsNIO.Width`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › btnVsNIO` → Width

```
If(Max(Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextIO; "")); Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextNIO; ""))) > 8; 200; 120)
```

```diff
-120
+If(Max(Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextIO; "")); Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextNIO; ""))) > 8; 200; 120)
```

**Kurz erklärt:** Wie btnVsIO.Width.

**Nachprüfen:** endet auf `"")); Len(Coalesce(LookUp(colP; ID = varAuswahlID).TextNIO; ""))) > 8; 200; 120)`

### 2.8 · `btnVsNIO.X`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › btnVsNIO` → X

```
24 + btnVsIO.Width
```

```diff
-144
+24 + btnVsIO.Width
```

**Kurz erklärt:** Steht immer neben dem i.O.-Knopf.

**Nachprüfen:** endet auf `24 + btnVsIO.Width`

### 2.9 · `lblVsRegeln.Text`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › lblVsRegeln` → Text

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NichtMessbar; false); Char(10) & "• „nicht messbar“ erlaubt (dann Begründung Pflicht)"; "")
```

```diff
-"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglic …
+"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglic …
```

**Kurz erklärt:** Vorschau nennt „nicht messbar erlaubt“.

**Nachprüfen:** endet auf `r; false); Char(10) & "• „nicht messbar“ erlaubt (dann Begründung Pflicht)"; "")`

## Schritt 3 – Auswahl wechseln (setzt die neuen Felder zurück)

### 3.1 · `btnGlZeile.OnSelect`

**Pfad:** `scrEditor › conEdGl › galGl › btnGlZeile` → OnSelect

```
If(!varIsLoading;
    If(ThisItem.Ebene = 3;
        Set(varAuswahlEbene; 3);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.BerID);;
        Set(varCtxK; ThisItem.KatID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO);
    ThisItem.Ebene = 2;
        Set(varAuswahlEbene; 2);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.BerID);;
        Set(varCtxK; ThisItem.ID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO);
    ThisItem.Ebene = 1;
        Set(varAuswahlEbene; 1);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.ID);;
        Set(varCtxK; 0);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO)
    )
)
```

```diff
-        Reset(txtPAbschnitt);
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO);
-        Reset(txtPAbschnitt);
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO);
-        Reset(txtPAbschnitt)
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO)
```

**Kurz erklärt:** Neu ist `Reset(txtPTextIO)` und `Reset(txtPTextNIO)`: Die neuen Felder zeigen nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 3.2 · `btnGlNeuB.OnSelect`

**Pfad:** `scrEditor › conEdGl › conGlFuss › btnGlNeuB` → OnSelect

```
If(varSchreibbar && !varIsLoading && Now() >= varSperreBis;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(!varEntwurfOk;
        false;
        false;
        Notify(""; NotificationType.Warning);
        Set(varNeuID; IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: "Neuer Bereich"; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(colB; RgReihenfolge); 0) + 10; Hinweis: ""; Aktiv: false; QuelleID: 0; Ausblenden: false}).ID; 0));;
        If(varNeuID = 0;
            Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
            Collect(colB; LookUp(RG_Bereiche; ID = varNeuID));;
            Set(varAuswahlEbene; 1);;
            Set(varAuswahlID; varNeuID);;
            Set(varCtxB; varNeuID);;
            Set(varCtxK; 0);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);;
            Reset(txtPTextIO);;
            Reset(txtPTextNIO);;
            SetFocus(txtBName)
        )
    )
)
```

```diff
+            Reset(txtPTextIO);;
+            Reset(txtPTextNIO);;
```

**Kurz erklärt:** Neu ist `Reset(txtPTextIO)` und `Reset(txtPTextNIO)`: Die neuen Felder zeigen nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 3.3 · `btnGlNeuK.OnSelect`

**Pfad:** `scrEditor › conEdGl › conGlFuss › btnGlNeuK` → OnSelect

```
If(varSchreibbar && !varIsLoading && Now() >= varSperreBis;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(!varEntwurfOk;
        false;
        varCtxB = 0;
        Notify("Links zuerst einen Bereich antippen."; NotificationType.Warning);
        Set(varNeuID; IfError(Patch(RG_Kategorien; Defaults(RG_Kategorien); {Title: "Neue Kategorie"; BereichID: varCtxB; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colK; BereichID = varCtxB); RgReihenfolge); 0) + 10; Hinweis: ""; Aktiv: true; QuelleID: 0}).ID; 0));;
        If(varNeuID = 0;
            Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
            Collect(colK; LookUp(RG_Kategorien; ID = varNeuID));;
            Set(varAuswahlEbene; 2);;
            Set(varAuswahlID; varNeuID);;
            Set(varCtxB; varCtxB);;
            Set(varCtxK; varNeuID);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);;
            Reset(txtPTextIO);;
            Reset(txtPTextNIO);;
            SetFocus(txtKName)
        )
    )
)
```

```diff
+            Reset(txtPTextIO);;
+            Reset(txtPTextNIO);;
```

**Kurz erklärt:** Neu ist `Reset(txtPTextIO)` und `Reset(txtPTextNIO)`: Die neuen Felder zeigen nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 3.4 · `btnGlNeuP.OnSelect`

**Pfad:** `scrEditor › conEdGl › conGlFuss › btnGlNeuP` → OnSelect

```
If(varSchreibbar && !varIsLoading && Now() >= varSperreBis;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(!varEntwurfOk;
        false;
        varCtxK = 0;
        Notify("Links zuerst eine Kategorie antippen."; NotificationType.Warning);
        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0) + 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: "IONIO"}; Pflicht: true; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: If(varAuswahlEbene = 3 && LookUp(colP; ID = varAuswahlID).KategorieID = varCtxK; Coalesce(LookUp(colP; ID = varAuswahlID).Abschnitt; ""); ""); TextIO: ""; TextNIO: ""; NichtMessbar: false}).ID; 0));;
        If(varNeuID = 0;
            Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
            Collect(colP; LookUp(RG_Pruefpunkte; ID = varNeuID));;
            Set(varAuswahlEbene; 3);;
            Set(varAuswahlID; varNeuID);;
            Set(varCtxB; varCtxB);;
            Set(varCtxK; varCtxK);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);;
            Reset(txtPTextIO);;
            Reset(txtPTextNIO);;
            SetFocus(txtPFrage)
        )
    )
)
```

```diff
-        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihe …
+        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihe …
+            Reset(txtPTextIO);;
+            Reset(txtPTextNIO);;
```

**Kurz erklärt:** Neuer Prüfpunkt mit leeren Wörtern. Dazu das Zurücksetzen der neuen Eingabefelder.

**Nachprüfen:** endet auf `)`

### 3.5 · `btnPrZeile.OnSelect`

**Pfad:** `scrEditor › conEdRechts › galPr › btnPrZeile` → OnSelect

```
If(!varIsLoading && ThisItem.Ebene > 0;
    If(ThisItem.Ebene = 3;
        Set(varAuswahlEbene; 3);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.BerID);;
        Set(varCtxK; ThisItem.KatID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO);
    ThisItem.Ebene = 2;
        Set(varAuswahlEbene; 2);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.BerID);;
        Set(varCtxK; ThisItem.ID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO);
    ThisItem.Ebene = 1;
        Set(varAuswahlEbene; 1);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.ID);;
        Set(varCtxK; 0);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO)
    )
)
```

```diff
-        Reset(txtPAbschnitt);
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO);
-        Reset(txtPAbschnitt);
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO);
-        Reset(txtPAbschnitt)
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO)
```

**Kurz erklärt:** Neu ist `Reset(txtPTextIO)` und `Reset(txtPTextNIO)`: Die neuen Felder zeigen nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 3.6 · `ddKBereich.OnChange`

**Pfad:** `scrEditor › conEdMitte › conEdK › ddKBereich` → OnChange

```
If(!IsBlank(Self.Selected) && Self.Selected.ID <> LookUp(colK; ID = varAuswahlID).BereichID && varSchreibbar;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(varEntwurfOk;
    With({ziel: Self.Selected.ID};
        Set(varPatchFehler; false);;
        IfError(Patch(RG_Kategorien; LookUp(RG_Kategorien; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {BereichID: ziel; RgReihenfolge: Coalesce(Max(Filter(colK; BereichID = ziel); RgReihenfolge); 0) + 10}); Set(varPatchFehler; true));;
        ClearCollect(colK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = varFassung));;
        If(varPatchFehler; Notify("Verschieben hat nicht geklappt."; NotificationType.Error); Notify("Verschoben (ans Ende des Bereichs)."; NotificationType.Success));;
        Set(varAuswahlEbene; 2);;
        Set(varAuswahlID; varAuswahlID);;
        Set(varCtxB; ziel);;
        Set(varCtxK; varAuswahlID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO)
    ))
)
```

```diff
-        Reset(txtPAbschnitt)
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO)
```

**Kurz erklärt:** Neu ist `Reset(txtPTextIO)` und `Reset(txtPTextNIO)`: Die neuen Felder zeigen nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 3.7 · `ddPKategorie.OnChange`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPKategorie` → OnChange

```
If(!IsBlank(Self.Selected) && Self.Selected.ID <> LookUp(colP; ID = varAuswahlID).KategorieID && varSchreibbar;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(varEntwurfOk;
    With({ziel: Self.Selected.ID; abh: CountRows(Filter(colP; BedingungPunkt = varAuswahlID))};
        Set(varPatchFehler; false);;
        ForAll(Filter(colP; BedingungPunkt = varAuswahlID) As d; Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = d.ID && RundgangID = varRgID && Fassung = varFassung); {BedingungPunkt: 0; BedingungWert: ""}));;
        IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {KategorieID: ziel; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = ziel); RgReihenfolge); 0) + 10; BedingungPunkt: 0; BedingungWert: ""}); Set(varPatchFehler; true));;
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung));;
        If(varPatchFehler;
            Notify("Verschieben hat nicht geklappt."; NotificationType.Error);
            Notify("Verschoben (ans Ende der Kategorie)." & If(abh > 0; " " & abh & " Bedingung(en), die auf diese Frage zeigten, wurden entfernt."; ""); NotificationType.Success)
        );;
        Set(varAuswahlEbene; 3);;
        Set(varAuswahlID; varAuswahlID);;
        Set(varCtxB; LookUp(colK; ID = ziel).BereichID);;
        Set(varCtxK; ziel);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO)
    ))
)
```

```diff
-        Reset(txtPAbschnitt)
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO)
```

**Kurz erklärt:** Neu ist `Reset(txtPTextIO)` und `Reset(txtPTextNIO)`: Die neuen Felder zeigen nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

## Schritt 4 – Listen und Mehrere Fragen

### 4.1 · `galAkt.Items`

**Pfad:** `scrEditor › conAkt › conAktKarte › galAkt` → Items

```
Ungroup(
    Table(
        {T: ForAll(Filter(colP As p; IsBlank(LookUp(colAltP As a; a.ID = p.QuelleID))) As p; {Art: "neu"; Text: p.Title})};
        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) || Coalesce(p.Auswahlwerte; "") <> Coalesce(a.Auswahlwerte; "") || Coalesce(p.Einheit; "") <> Coalesce(a.Einheit; "") || Coalesce(p.MinWert; -999999) <> Coalesce(a.MinWert; -999999) || Coalesce(p.MaxWert; -999999) <> Coalesce(a.MaxWert; -999999) || Coalesce(p.Hinweis; "") <> Coalesce(a.Hinweis; "") || fnFotoWert(p.Foto.Value; Coalesce(p.FotoMoeglich; false)) <> fnFotoWert(a.Foto.Value; Coalesce(a.FotoMoeglich; false)) || Coalesce(p.KommentarPflicht; false) <> Coalesce(a.KommentarPflicht; false) || fnGrenzmodus(p.Grenzmodus.Value) <> fnGrenzmodus(a.Grenzmodus.Value) || Coalesce(p.BedingungWert; "") <> Coalesce(a.BedingungWert; "") || Coalesce(LookUp(colP As b0; b0.ID = p.BedingungPunkt).QuelleID; 0) <> Coalesce(a.BedingungPunkt; 0) || Coalesce(p.HinweisBildID; 0) <> Coalesce(a.HinweisBildID; 0) || Coalesce(LookUp(colK As k0; k0.ID = p.KategorieID).QuelleID; 0) <> a.KategorieID || Trim(Coalesce(p.Abschnitt; "")) <> Trim(Coalesce(a.Abschnitt; "")) || Coalesce(p.Kritisch; false) <> Coalesce(a.Kritisch; false) || Coalesce(p.KritischText; "") <> Coalesce(a.KritischText; "") || Coalesce(p.Ansprechpartner; "") <> Coalesce(a.Ansprechpartner; "") || Coalesce(p.Rueckfrage; false) <> Coalesce(a.Rueckfrage; false) || Coalesce(p.RueckfrageText; "") <> Coalesce(a.RueckfrageText; "") || Coalesce(p.TextIO; "") <> Coalesce(a.TextIO; "") || Coalesce(p.TextNIO; "") <> Coalesce(a.TextNIO; "") || Coalesce(p.NichtMessbar; false) <> Coalesce(a.NichtMessbar; false)))) As p; {Art: "geändert"; Text: p.Title})};
        {T: ForAll(Filter(colAltP As a; IsBlank(LookUp(colP As p; p.QuelleID = a.ID))) As a; {Art: "entfernt"; Text: a.Title})}
    );
    T
)
```

```diff
-        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coales …
+        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coales …
```

**Kurz erklärt:** Änderungen an Wörtern und „nicht messbar“ zählen als „geändert“.

**Nachprüfen:** endet auf `)`

### 4.2 · `btnMehrAnlegen.OnSelect`

**Pfad:** `scrEditor › conMehr › conMehrKarte › btnMehrAnlegen` → OnSelect

```
If(varSchreibbar && !varIsLoading && Now() >= varSperreBis;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    ClearCollect(colMehr; Filter(ForAll(Split(Substitute(txtMehr.Text; Char(13); ""); Char(10)) As z; {F: Left(Trim(z.Value); 255)}); F <> ""));;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(!varEntwurfOk;
        Set(varMehrereOffen; false);
        varCtxK = 0;
        Notify("Links zuerst eine Kategorie antippen."; NotificationType.Warning);
        IsEmpty(colMehr);
        Notify("Bitte mindestens eine Frage eintragen."; NotificationType.Warning);
        Set(varIsLoading; true);;
        ClearCollect(colMehrErg;
            With({basis: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0)};
                ForAll(Sequence(CountRows(colMehr)) As i;
                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: varMehrTyp}; Pflicht: varMehrPflicht; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: Left(Trim(txtMehrAbschnitt.Text); 255); TextIO: ""; TextNIO: ""; NichtMessbar: false}).ID; 0)}
                )
            )
        );;
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung));;
        If(CountRows(Filter(colMehrErg; Neu = 0)) > 0;
            Notify(CountRows(Filter(colMehrErg; Neu = 0)) & " Fragen konnten nicht angelegt werden. Bitte die Gliederung prüfen."; NotificationType.Error);
            Notify(CountRows(colMehrErg) & " Prüfpunkte angelegt."; NotificationType.Success);;
            Reset(txtMehr);;
            Reset(txtMehrAbschnitt);;
            Set(varMehrereOffen; false)
        );;
        Set(varIsLoading; false)
    )
)
```

```diff
-                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; Quell …
+                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; Quell …
```

**Kurz erklärt:** „Mehrere Fragen“ legt die neuen Felder leer an.

**Nachprüfen:** endet auf `)`

## Schritt 5 – Lange Formeln

### 5.1 · `btnEdEntf.OnSelect`

**Pfad:** `scrEditor › conEdMitte › conEdLeiste › btnEdEntf` → OnSelect

```
If(varSchreibbar && varAuswahlEbene > 0; If(!varIsLoading && Now() >= varSperreBis;
        If(varFrage <> "del" & varAuswahlEbene & "-" & varAuswahlID;
            Set(varFrage; "del" & varAuswahlEbene & "-" & varAuswahlID);;
            Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));
            Set(varFrage; "");;
            Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(varEntwurfOk;
    Set(varIsLoading; true);;
    If(varAuswahlEbene = 3;
        ForAll(Filter(colP; BedingungPunkt = varAuswahlID) As d; Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = d.ID && RundgangID = varRgID && Fassung = varFassung); {BedingungPunkt: 0; BedingungWert: ""}));;
        Remove(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung));
        varAuswahlEbene = 2;
        Remove(RG_Pruefpunkte; Filter(RG_Pruefpunkte; KategorieID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung));;
        Remove(RG_Kategorien; LookUp(RG_Kategorien; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung));
        varAuswahlEbene = 1;
        ForAll(Filter(colK; BereichID = varAuswahlID) As k; Remove(RG_Pruefpunkte; Filter(RG_Pruefpunkte; KategorieID = k.ID && RundgangID = varRgID && Fassung = varFassung)));;
        Remove(RG_Kategorien; Filter(RG_Kategorien; BereichID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung));;
        Remove(RG_Bereiche; LookUp(RG_Bereiche; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung))
    );;
    Concurrent(
        ClearCollect(colB; Filter(RG_Bereiche; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung))
    );;
    If((varAuswahlEbene = 3 && !IsBlank(LookUp(colP; ID = varAuswahlID))) || (varAuswahlEbene = 2 && !IsBlank(LookUp(colK; ID = varAuswahlID))) || (varAuswahlEbene = 1 && !IsBlank(LookUp(colB; ID = varAuswahlID)));
        Notify("Entfernen hat nicht geklappt. Bitte erneut versuchen."; NotificationType.Error);
        Notify("Entfernt."; NotificationType.Success)
    );;
    If(varAuswahlEbene = 3;
        Set(varAuswahlEbene; 2);;
        Set(varAuswahlID; varCtxK);;
        Set(varCtxB; varCtxB);;
        Set(varCtxK; varCtxK);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO);
        varAuswahlEbene = 2;
        Set(varAuswahlEbene; 1);;
        Set(varAuswahlID; varCtxB);;
        Set(varCtxB; varCtxB);;
        Set(varCtxK; 0);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO);
        Set(varAuswahlEbene; 0);;
        Set(varAuswahlID; 0);;
        Set(varCtxB; 0);;
        Set(varCtxK; 0);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO)
    );;
    Set(varIsLoading; false)
    )
        )
    ))
```

```diff
-        Reset(txtPAbschnitt);
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO);
-        Reset(txtPAbschnitt);
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO);
-        Reset(txtPAbschnitt)
+        Reset(txtPAbschnitt);;
+        Reset(txtPTextIO);;
+        Reset(txtPTextNIO)
```

**Kurz erklärt:** Neu ist `Reset(txtPTextIO)` und `Reset(txtPTextNIO)`: Die neuen Felder zeigen nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `))`

### 5.2 · `galPr.Items`

**Pfad:** `scrEditor › conEdRechts › galPr` → Items

```
Sort(
    Ungroup(
        Table(
            {T: Filter(Table({Art: "Fehler"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Der Rundgang hat noch keinen Bereich. → „+ Bereich“"}); IsEmpty(colB))};
            {T: ForAll(Filter(colB As b; IsEmpty(Filter(colK As k; k.BereichID = b.ID))) As b; {Art: "Fehler"; Ebene: 1; ID: b.ID; KatID: 0; BerID: b.ID; Text: "Bereich „" & b.Title & "“ hat keine Kategorie."})};
            {T: ForAll(Filter(colK As k; IsEmpty(Filter(colP As p; p.KategorieID = k.ID))) As k; {Art: "Fehler"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat keinen Prüfpunkt."})};
            {T: ForAll(Filter(colB As b; Trim(Coalesce(b.Title; "")) = "") As b; {Art: "Fehler"; Ebene: 1; ID: b.ID; KatID: 0; BerID: b.ID; Text: "Ein Bereich hat keinen Namen."})};
            {T: ForAll(Filter(colK As k; Trim(Coalesce(k.Title; "")) = "") As k; {Art: "Fehler"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Eine Kategorie hat keinen Namen."})};
            {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Title; "")) = "") As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Ein Prüfpunkt hat keine Frage."})};
            {T: ForAll(Filter(colP As p; (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerte(p.Auswahlwerte) < 2) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: mindestens zwei Antwortmöglichkeiten eintragen."})};
            {T: ForAll(Filter(colP As p; (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerteDoppelt(p.Auswahlwerte)) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: eine Antwortmöglichkeit steht doppelt da."})};
            {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && !IsBlank(p.MinWert) && !IsBlank(p.MaxWert) && p.MinWert > p.MaxWert) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: „ab“ ist größer als „bis“."})};
            {T: ForAll(Filter(ForAll(Filter(colP As p0; Coalesce(p0.BedingungPunkt; 0) <> 0) As p; With({a: LookUp(colP As a0; a0.ID = p.BedingungPunkt)}; {ID: p.ID; KategorieID: p.KategorieID; Title: p.Title; G: If(IsBlank(a) || a.KategorieID <> p.KategorieID; "Die Bedingung zeigt auf eine Frage außerhalb dieser Kategorie."; Coalesce(a.BedingungPunkt; 0) <> 0; "Die Frage der Bedingung hat selbst eine Bedingung (nur eine Ebene erlaubt)."; a.RgReihenfolge * 1000000 + a.ID > p.RgReihenfolge * 1000000 + p.ID; "Die Frage der Bedingung muss weiter oben stehen."; !fnBedGueltig(p.BedingungWert; a.Eingabetyp.Value; a.Auswahlwerte); "Der Wert der Bedingung passt nicht zu „" & a.Title & "“."; "")})); G <> "") As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: " & p.G})};
            {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && fnGrenzmodus(p.Grenzmodus.Value) <> "Mangel" && IsBlank(p.MinWert) && IsBlank(p.MaxWert)) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: „Außerhalb“ wirkt nur mit Grenzen (ab/bis)."})};
            {T: ForAll(Filter(colP As p; p.Foto.Value = "Bei Mangel Pflicht" && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: „Foto Pflicht bei Mangel“ wirkt nur bei i.O./n.i.O. und Zahl."})};
            {T: ForAll(Filter(colP As p; CountRows(Filter(colP As q; q.KategorieID = p.KategorieID && Lower(Trim(q.Title)) = Lower(Trim(p.Title)))) > 1) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“ steht in der Kategorie doppelt."})};
            {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Abschnitt; "")) <> "" && With({v: First(Sort(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 1000000 + q.ID < p.RgReihenfolge * 1000000 + p.ID); RgReihenfolge * 1000000 + ID; SortOrder.Descending))}; !IsBlank(v) && Lower(Trim(Coalesce(v.Abschnitt; ""))) <> Lower(Trim(p.Abschnitt))) && CountRows(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 1000000 + q.ID < p.RgReihenfolge * 1000000 + p.ID && Lower(Trim(Coalesce(q.Abschnitt; ""))) = Lower(Trim(p.Abschnitt)))) > 0) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Abschnitt „" & Trim(p.Abschnitt) & "“ ist unterbrochen: Die Fragen stehen nicht zusammen (bei „" & p.Title & "“). Mit ↑ ↓ zusammenschieben."})};
            {T: ForAll(Filter(colP As p; (Coalesce(p.Kritisch; false) || Coalesce(p.Rueckfrage; false)) && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Rückfrage und „kritisch“ wirken nur bei i.O./n.i.O. und Zahl."})};
            {T: ForAll(Filter(colP As p; Coalesce(p.Kritisch; false) && Trim(Coalesce(p.Ansprechpartner; "")) = "") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“ ist kritisch, aber ohne eigenen Ansprechpartner (es erscheinen nur die allgemeinen)."})};
            {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "IONIO" && (Trim(Coalesce(p.TextIO; "")) <> "" || Trim(Coalesce(p.TextNIO; "")) <> "")) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: eigene Knopf-Beschriftungen wirken nur bei i.O./n.i.O."})};
            {T: ForAll(Filter(colP As p; p.Title = "Neue Frage") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Eine Frage heißt noch „Neue Frage“."})};
            {T: ForAll(Filter(colK As k; CountRows(Filter(colP As p; p.KategorieID = k.ID)) > 30) As k; {Art: "Hinweis"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat über 30 Prüfpunkte (lange Seite für den Prüfer)."})};
            {T: Filter(Table({Art: "Hinweis"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Kein aktiver Plan: Der Rundgang erscheint nie auf der Startseite. → In der Übersicht „Plan“ tippen."}); !varIstVorlage && IsEmpty(Filter(colPlanR; Coalesce(Aktiv; false))))}
        );
        T
    );
    If(Art = "Fehler"; 0; 1)
)
```

```diff
+            {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "IONIO" && (Trim(Coalesce(p.TextIO; "")) <> "" || Trim(Coalesce(p.TextNIO; "")) <> "")) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK A …
```

**Kurz erklärt:** Hinweis, wenn eigene Wörter bei einem anderen Typ eingetragen sind.

**Nachprüfen:** endet auf `)`

### 5.3 · `tmrArbeit.OnTimerEnd`

**Pfad:** `scrEditor › tmrArbeit` → OnTimerEnd

```
Set(varArbeitStart; false);;
Set(varIsLoading; true);;
If(varJob = "vorbereiten";
    Set(varLadeText; "Rundgang wird für den Builder vorbereitet …");;
    Concurrent(Refresh(RG_Rundgaenge); Refresh(RG_Bereiche); Refresh(RG_Kategorien); Refresh(RG_Pruefpunkte));;
    Set(varRg; LookUp(RG_Rundgaenge; ID = varRgID));;
    ClearCollect(colVbB; Filter(RG_Bereiche; RundgangID = varRgID));;
    Clear(colVbK);;
    ForAll(colVbB As b; Collect(colVbK; Filter(RG_Kategorien; BereichID = b.ID)));;
    Clear(colVbP);;
    ForAll(colVbK As k; Collect(colVbP; Filter(RG_Pruefpunkte; KategorieID = k.ID)));;
    ClearCollect(colVbErg; ForAll(Filter(colVbB; IsBlank(Fassung)) As b; {Ok: !IsError(Patch(RG_Bereiche; LookUp(RG_Bereiche; ID = b.ID); {Fassung: 1; QuelleID: 0}))}));;
    Collect(colVbErg; ForAll(Filter(colVbK; IsBlank(Fassung) || IsBlank(RundgangID)) As k; {Ok: !IsError(Patch(RG_Kategorien; LookUp(RG_Kategorien; ID = k.ID); {Fassung: 1; RundgangID: varRgID; QuelleID: 0}))}));;
    Collect(colVbErg; ForAll(Filter(colVbP; IsBlank(Fassung) || IsBlank(RundgangID)) As p; {Ok: !IsError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = p.ID); {Fassung: 1; RundgangID: varRgID; QuelleID: 0}))}));;
    Set(varPatchFehler; CountRows(Filter(colVbErg; !Ok)) > 0);;
    If(!varPatchFehler;
        If(IsError(Patch(RG_Rundgaenge; LookUp(RG_Rundgaenge; ID = varRgID); {Fassung: 1; EntwurfFassung: 0; EntwurfVon: ""; Status: If(Coalesce(varRg.Aktiv; false); "Aktiv"; "Archiviert")})); Set(varPatchFehler; true))
    );;
    If(varPatchFehler;
        Notify("Vorbereiten unvollständig. Bitte den Rundgang erneut öffnen (das ist gefahrlos)."; NotificationType.Error);;
        Set(varJob; "zurueck");
        Set(varFassung; 1);;
        Set(varJob; varNach);;
        Set(varNach; "")
    )
);;
If(varJob = "neueFassung";
    Set(varLadeText; "Neue Fassung wird angelegt …");;
    Concurrent(Refresh(RG_Rundgaenge); Refresh(RG_Bereiche); Refresh(RG_Kategorien); Refresh(RG_Pruefpunkte));;
    Set(varRg; LookUp(RG_Rundgaenge; ID = varRgID));;
    If(Coalesce(varRg.EntwurfFassung; 0) > 0;
        Set(varFassung; varRg.EntwurfFassung);;
        Set(varSchreibbar; true);;
        Notify("Es gibt schon einen Entwurf – er wird geöffnet."; NotificationType.Information);;
        Set(varJob; "laden");
        ClearCollect(colAlleB; Filter(RG_Bereiche; RundgangID = varRgID));;
        Set(varZielF; Max(Coalesce(Max(colAlleB; Coalesce(Fassung; 0)); 0); Coalesce(First(Sort(Filter(RG_Kategorien; RundgangID = varRgID); Fassung; SortOrder.Descending)).Fassung; 0); Coalesce(First(Sort(Filter(RG_Pruefpunkte; RundgangID = varRgID); Fassung; SortOrder.Descending)).Fassung; 0); fnAktiveFassung(varRg.Fassung)) + 1);;
        Set(varPatchFehler; false);;
        IfError(Patch(RG_Rundgaenge; LookUp(RG_Rundgaenge; ID = varRgID); {EntwurfFassung: varZielF; EntwurfVon: User().FullName}); Set(varPatchFehler; true));;
        If(varPatchFehler;
            Notify("Die neue Fassung konnte nicht angelegt werden. Bitte erneut versuchen."; NotificationType.Error);;
            Set(varJob; "zurueck");
            ClearCollect(colQB; Filter(colAlleB; Coalesce(Fassung; 0) = fnAktiveFassung(varRg.Fassung)));;
            ClearCollect(colQK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = fnAktiveFassung(varRg.Fassung)));;
            ClearCollect(colQP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = fnAktiveFassung(varRg.Fassung)));;
            RemoveIf(colQB; !Coalesce(Aktiv; false));;
            RemoveIf(colQK; !Coalesce(Aktiv; false));;
            RemoveIf(colQP; !Coalesce(Aktiv; false));;
            RemoveIf(colQK; IsBlank(LookUp(colQB As b0; b0.ID = BereichID)));;
            RemoveIf(colQP; IsBlank(LookUp(colQK As k0; k0.ID = KategorieID)));;
            Set(varZielR; varRgID);;
            Set(varZielB; 0);;
            Set(varZielK; 0);;
            Set(varZielBAktiv; false);;
            Set(varKopieBehalteR; true);;
            Set(varKopieZusatz; "");;
            Set(varFassung; varZielF);;
            Set(varSchreibbar; true);;
            Set(varKopieNach; "laden");;
            Set(varJob; "kopie")
        )
    )
);;
If(varJob = "quelle";
    Set(varLadeText; "Rundgang wird kopiert …");;
    Concurrent(
        ClearCollect(colQB; Filter(RG_Bereiche; RundgangID = varQuelleR && Fassung = varQuelleF));
        ClearCollect(colQK; Filter(RG_Kategorien; RundgangID = varQuelleR && Fassung = varQuelleF));
        ClearCollect(colQP; Filter(RG_Pruefpunkte; RundgangID = varQuelleR && Fassung = varQuelleF))
    );;
    If(varQuelleNurAktiv;
        RemoveIf(colQB; !Coalesce(Aktiv; false));;
        RemoveIf(colQK; !Coalesce(Aktiv; false));;
        RemoveIf(colQP; !Coalesce(Aktiv; false));;
        RemoveIf(colQK; IsBlank(LookUp(colQB As b0; b0.ID = BereichID)));;
        RemoveIf(colQP; IsBlank(LookUp(colQK As k0; k0.ID = KategorieID)))
    );;
    Set(varZielB; 0);;
    Set(varZielK; 0);;
    Set(varZielBAktiv; false);;
    Set(varKopieBehalteR; true);;
    Set(varKopieZusatz; "");;
    Set(varKopieNach; "laden");;
    Set(varJob; "kopie")
);;
If(varJob = "kopie";
    Set(varLadeText; "Wird kopiert …");;
    ClearCollect(colMapB;
        With({qs: Sort(colQB; RgReihenfolge * 1000000 + ID)};
            ForAll(Sequence(CountRows(qs)) As i;
                With({q: Index(qs; i.Value)};
                    {Alt: q.ID;
                     Neu: IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: Left(q.Title & varKopieZusatz; 255); RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(colB; RgReihenfolge); 0) + i.Value * 10); Hinweis: q.Hinweis; Aktiv: varZielBAktiv; QuelleID: q.ID; Ausblenden: Coalesce(q.Ausblenden; false)}).ID; 0)}
                )
            )
        )
    );;
    ClearCollect(colMapK;
        With({qs: Sort(colQK; RgReihenfolge * 1000000 + ID)};
            ForAll(Sequence(CountRows(qs)) As i;
                With({q: Index(qs; i.Value)};
                    With({ziel: If(IsEmpty(colQB); varZielB; Coalesce(LookUp(colMapB; Alt = q.BereichID).Neu; 0))};
                        {Alt: q.ID;
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Kategorien; Defaults(RG_Kategorien); {Title: Left(q.Title & If(IsEmpty(colQB); varKopieZusatz; ""); 255); BereichID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQB) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colK; BereichID = varZielB); RgReihenfolge); 0) + i.Value * 10); Hinweis: q.Hinweis; Aktiv: true; QuelleID: q.ID}).ID; 0))}
                    )
                )
            )
        )
    );;
    ClearCollect(colMapP;
        With({qs: Sort(colQP; RgReihenfolge * 1000000 + ID)};
            ForAll(Sequence(CountRows(qs)) As i;
                With({q: Index(qs; i.Value)};
                    With({ziel: If(IsEmpty(colQK); varZielK; Coalesce(LookUp(colMapK; Alt = q.KategorieID).Neu; 0))};
                        {Alt: q.ID; BedAlt: Coalesce(q.BedingungPunkt; 0); BedWert: Coalesce(q.BedingungWert; ""); Ziel: ziel;
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQK) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colP; KategorieID = varZielK); RgReihenfolge); 0) + i.Value * 10); Aktiv: true; QuelleID: q.ID; Eingabetyp: {Value: Coalesce(q.Eingabetyp.Value; "IONIO")}; Pflicht: Coalesce(q.Pflicht; false); Auswahlwerte: q.Auswahlwerte; Einheit: q.Einheit; MinWert: q.MinWert; MaxWert: q.MaxWert; Hinweis: q.Hinweis; FotoMoeglich: Coalesce(q.FotoMoeglich; false); Foto: {Value: fnFotoWert(q.Foto.Value; Coalesce(q.FotoMoeglich; false))}; KommentarPflicht: Coalesce(q.KommentarPflicht; false); Grenzmodus: {Value: fnGrenzmodus(q.Grenzmodus.Value)}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: Coalesce(q.HinweisBildID; 0); Abschnitt: Coalesce(q.Abschnitt; ""); Kritisch: Coalesce(q.Kritisch; false); KritischText: Coalesce(q.KritischText; ""); Ansprechpartner: Coalesce(q.Ansprechpartner; ""); Rueckfrage: Coalesce(q.Rueckfrage; false); RueckfrageText: Coalesce(q.RueckfrageText; ""); TextIO: Coalesce(q.TextIO; ""); TextNIO: Coalesce(q.TextNIO; ""); NichtMessbar: Coalesce(q.NichtMessbar; false)}).ID; 0))}
                    )
                )
            )
        )
    );;
    ClearCollect(colBedErg;
        ForAll(Filter(colMapP; BedAlt <> 0 && Neu <> 0) As m;
            With({a: LookUp(colMapP As m2; m2.Alt = m.BedAlt)};
                With({neuA: If(!IsBlank(a) && a.Ziel = m.Ziel; a.Neu; IsBlank(a) && LookUp(colP As p0; p0.ID = m.BedAlt).KategorieID = m.Ziel; m.BedAlt; 0)};
                    {Ok: If(neuA = 0; true; !IsError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = m.Neu); {BedingungPunkt: neuA; BedingungWert: m.BedWert})))}
                )
            )
        )
    );;
    Set(varKopieFehler; CountRows(Filter(colMapB; Neu = 0)) + CountRows(Filter(colMapK; Neu = 0)) + CountRows(Filter(colMapP; Neu = 0)) + CountRows(Filter(colBedErg; !Ok)));;
    If(varKopieFehler > 0 && varKopieNach = "laden";
        If(Coalesce(LookUp(RG_Rundgaenge; ID = varZielR).Fassung; 0) = 0 || varZielF <> fnAktiveFassung(LookUp(RG_Rundgaenge; ID = varZielR).Fassung);
            Remove(RG_Pruefpunkte; Filter(RG_Pruefpunkte; RundgangID = varZielR && Fassung = varZielF));;
            Remove(RG_Kategorien; Filter(RG_Kategorien; RundgangID = varZielR && Fassung = varZielF));;
            Remove(RG_Bereiche; Filter(RG_Bereiche; RundgangID = varZielR && Fassung = varZielF))
        );;
        If(Coalesce(LookUp(RG_Rundgaenge; ID = varZielR).Fassung; 0) > 0 && varZielF <> fnAktiveFassung(LookUp(RG_Rundgaenge; ID = varZielR).Fassung);
            If(IsError(Patch(RG_Rundgaenge; LookUp(RG_Rundgaenge; ID = varZielR); {EntwurfFassung: 0; EntwurfVon: ""})); Set(varPatchFehler; true))
        );;
        Notify("Kopieren fehlgeschlagen (" & varKopieFehler & " Teile fehlen). Der Entwurf wurde zurückgenommen. Bitte erneut versuchen."; NotificationType.Error);;
        Set(varJob; "zurueck");
        varKopieFehler > 0;
        Notify("Kopieren unvollständig: " & varKopieFehler & " Teile fehlen. Bitte die Gliederung prüfen."; NotificationType.Error);;
        Set(varJob; varKopieNach);
        Notify("Kopiert: " & CountRows(colMapP) & " Prüfpunkte."; NotificationType.Success);;
        Set(varJob; varKopieNach)
    )
);;
If(varJob = "laden";
    Set(varLadeText; "Rundgang wird geladen …");;
    Concurrent(Refresh(RG_Rundgaenge); Refresh(RG_Bereiche); Refresh(RG_Kategorien); Refresh(RG_Pruefpunkte); Refresh(RG_Plan));;
    Set(varRg; LookUp(RG_Rundgaenge; ID = varRgID));;
    Set(varIstVorlage; fnStatus(varRg.Status; varRg.Aktiv) = "Vorlage");;
    Concurrent(
        ClearCollect(colB; Filter(RG_Bereiche; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung))
    );;
    ClearCollect(colPlanR; Filter(RG_Plan; RundgangID = varRgID));;
    Set(varAktivRest; false);;
    If(varSchreibbar && !varIstVorlage && Coalesce(varRg.EntwurfFassung; 0) <> varFassung;
        Set(varSchreibbar; false);;
        Notify("Dieser Entwurf ist nicht mehr offen. Er wird nur zum Lesen gezeigt."; NotificationType.Warning)
    );;
    If(varSchreibbar && !varIstVorlage && CountRows(Filter(colB; Coalesce(Aktiv; false))) > 0;
        Set(varSchreibbar; false);;
        Set(varAktivRest; true);;
        Notify("Das Aktivieren dieser Fassung ist unvollständig. Bitte oben „Aktivieren …“ erneut tippen."; NotificationType.Error)
    );;
    If(!varSchreibbar && !varAktivRest;
        RemoveIf(colB; !Coalesce(Aktiv; false));;
        RemoveIf(colK; !Coalesce(Aktiv; false));;
        RemoveIf(colP; !Coalesce(Aktiv; false));;
        RemoveIf(colK; IsBlank(LookUp(colB As b0; b0.ID = BereichID)));;
        RemoveIf(colP; IsBlank(LookUp(colK As k0; k0.ID = KategorieID)))
    );;
    Set(varGespeichertText; "");;
    With({b1: First(Sort(colB; RgReihenfolge * 1000000 + ID))};
        If(IsBlank(b1);
            Set(varAuswahlEbene; 0);;
            Set(varAuswahlID; 0);;
            Set(varCtxB; 0);;
            Set(varCtxK; 0);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);;
            Reset(txtPTextIO);;
            Reset(txtPTextNIO);
            Set(varAuswahlEbene; 1);;
            Set(varAuswahlID; b1.ID);;
            Set(varCtxB; b1.ID);;
            Set(varCtxK; 0);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);;
            Reset(txtPTextIO);;
            Reset(txtPTextNIO)
        )
    );;
    Set(varJob; "")
);;
If(varJob = "auswahl";
    Concurrent(
        ClearCollect(colB; Filter(RG_Bereiche; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung))
    );;
    If(!IsEmpty(colQB);
        With({n: First(colMapB).Neu}; If(n > 0; Set(varAuswahlEbene; 1);; Set(varAuswahlID; n);; Set(varCtxB; n);; Set(varCtxK; 0);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW);; Reset(txtPAbschnitt);; Reset(txtPTextIO);; Reset(txtPTextNIO)));
        !IsEmpty(colQK);
        With({n: First(colMapK).Neu}; If(n > 0; Set(varAuswahlEbene; 2);; Set(varAuswahlID; n);; Set(varCtxB; varZielB);; Set(varCtxK; n);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW);; Reset(txtPAbschnitt);; Reset(txtPTextIO);; Reset(txtPTextNIO)));
        With({n: First(colMapP).Neu}; If(n > 0; Set(varAuswahlEbene; 3);; Set(varAuswahlID; n);; Set(varCtxB; LookUp(colK; ID = varZielK).BereichID);; Set(varCtxK; varZielK);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW);; Reset(txtPAbschnitt);; Reset(txtPTextIO);; Reset(txtPTextNIO)))
    );;
    Set(varJob; "")
);;
If(varJob = "aktivieren";
    Set(varLadeText; "Fassung wird aktiviert …");;
    Concurrent(Refresh(RG_Rundgaenge); Refresh(RG_Bereiche); Refresh(RG_Kategorien));;
    Set(varRg; LookUp(RG_Rundgaenge; ID = varRgID));;
    If(Coalesce(varRg.EntwurfFassung; 0) <> varFassung;
        Notify("Dieser Entwurf wurde inzwischen schon aktiviert oder verworfen. Die Übersicht wird neu geladen."; NotificationType.Error);;
        Set(varJob; "zurueck");
        ClearCollect(colAktB; Filter(RG_Bereiche; RundgangID = varRgID));;
        ClearCollect(colAktK; Filter(RG_Kategorien; RundgangID = varRgID));;
        ClearCollect(colAltB; Filter(colAktB; Coalesce(Aktiv; false) && Coalesce(Fassung; 0) <> varFassung));;
        ClearCollect(colAltK; Filter(colAktK; Coalesce(Aktiv; false) && Coalesce(Fassung; 0) <> varFassung));;
        ClearCollect(colNeuB; Filter(colAktB; Coalesce(Fassung; 0) = varFassung));;
        ClearCollect(colAktErg; ForAll(colAltB As b; {Ok: !IsError(Patch(RG_Bereiche; LookUp(RG_Bereiche; ID = b.ID); {Aktiv: false}))}));;
        Collect(colAktErg; ForAll(colAltK As k; {Ok: !IsError(Patch(RG_Kategorien; LookUp(RG_Kategorien; ID = k.ID); {Aktiv: false}))}));;
        Set(varPatchFehler; CountRows(Filter(colAktErg; !Ok)) > 0);;
        If(!varPatchFehler;
            Collect(colAktErg; ForAll(colNeuB As b; {Ok: !IsError(Patch(RG_Bereiche; LookUp(RG_Bereiche; ID = b.ID); {Aktiv: true}))}));;
            Set(varPatchFehler; CountRows(Filter(colAktErg; !Ok)) > 0)
        );;
        Refresh(RG_Bereiche);;
        ClearCollect(colAktB; Filter(RG_Bereiche; RundgangID = varRgID));;
        If(!varPatchFehler && CountRows(Filter(colAktB; Coalesce(Aktiv; false) && Coalesce(Fassung; 0) <> varFassung)) = 0 && CountRows(Filter(colAktB; Coalesce(Aktiv; false) && Coalesce(Fassung; 0) = varFassung)) = CountRows(colNeuB);
            If(IsError(Patch(RG_Rundgaenge; LookUp(RG_Rundgaenge; ID = varRgID); {Fassung: varFassung; EntwurfFassung: 0; EntwurfVon: ""; Status: "Aktiv"; Aktiv: true})); Set(varPatchFehler; true));
            Set(varPatchFehler; true)
        );;
        If(varPatchFehler;
            Notify("Aktivieren unvollständig. Bitte noch einmal „Aktivieren …“ tippen – das ist gefahrlos."; NotificationType.Error);;
            Set(varSchreibbar; false);;
            Set(varAktivRest; true);;
            Set(varJob; "");
            Notify("Fassung " & varFassung & " ist aktiv. Laufende Rundgänge von heute werden mit der alten Fassung beendet."; NotificationType.Success);;
            Set(varJob; "zurueck")
        )
    )
);;
If(varJob = "zurueck";
    Set(varJob; "");;
    Set(varIsLoading; false);;
    Navigate(scrListe; ScreenTransition.None)
);;
Set(varIsLoading; false)
```

```diff
-                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgRei …
+                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgRei …
-            Reset(txtPAbschnitt);
+            Reset(txtPAbschnitt);;
+            Reset(txtPTextIO);;
+            Reset(txtPTextNIO);
-            Reset(txtPAbschnitt)
+            Reset(txtPAbschnitt);;
+            Reset(txtPTextIO);;
+            Reset(txtPTextNIO)
-        With({n: First(colMapB).Neu}; If(n > 0; Set(varAuswahlEbene; 1);; Set(varAuswahlID; n);; Set(varCtxB; n);; Set(varCtxK; 0);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(tx …
+        With({n: First(colMapB).Neu}; If(n > 0; Set(varAuswahlEbene; 1);; Set(varAuswahlID; n);; Set(varCtxB; n);; Set(varCtxK; 0);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(tx …
-        With({n: First(colMapK).Neu}; If(n > 0; Set(varAuswahlEbene; 2);; Set(varAuswahlID; n);; Set(varCtxB; varZielB);; Set(varCtxK; n);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; R …
-        With({n: First(colMapP).Neu}; If(n > 0; Set(varAuswahlEbene; 3);; Set(varAuswahlID; n);; Set(varCtxB; LookUp(colK; ID = varZielK).BereichID);; Set(varCtxK; varZielK);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Rese …
+        With({n: First(colMapK).Neu}; If(n > 0; Set(varAuswahlEbene; 2);; Set(varAuswahlID; n);; Set(varCtxB; varZielB);; Set(varCtxK; n);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; R …
+        With({n: First(colMapP).Neu}; If(n > 0; Set(varAuswahlEbene; 3);; Set(varAuswahlID; n);; Set(varCtxB; LookUp(colK; ID = varZielK).BereichID);; Set(varCtxK; varZielK);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Rese …
```

**Kurz erklärt:** Kopie/neue Fassung übernehmen die drei neuen Felder. Dazu das Zurücksetzen der neuen Eingabefelder.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

## Test

1. Prüfpunkt i.O./n.i.O. wählen → „durchgeführt“ / „nicht durchgeführt“ eintragen → Vorschau-Knöpfe heißen so.
2. Zahl-Prüfpunkt → „nicht messbar: nicht erlaubt“ antippen → „✓ erlaubt“, Vorschau nennt es. Schnell zweimal tippen → schaltet nur einmal um.
2b. „durchgeführt“/„nicht durchgeführt“ eintragen → Vorschau-Knöpfe werden breiter, nichts abgeschnitten. Mehr als 18 Zeichen lassen sich nicht eintippen.
3. Anderen Prüfpunkt wählen und zurück → Felder zeigen die richtigen Werte.
4. Aktivieren → Änderungsliste „geändert“. Neue Fassung → Werte noch da.

## Rückweg

Vorher-Fassungen im Anhang. `conPIonio`, `lblPNM`, `btnPNM` erst löschen, **nachdem** die Vorher-Fassungen drin sind (sonst werden die Formeln mit `Reset(txtPTextIO)` rot).

## Anhang – Vorher-Fassungen (Stand nach Paket 9)

**`lblKInfo.Text` vorher**

```
CountRows(Filter(colP; KategorieID = varAuswahlID)) & " Prüfpunkte." & Char(10) & Char(10) & "Eine Kategorie ist eine Seite im Rundgang: Der Prüfer füllt sie aus und speichert sie als Ganzes. Die Kategorien werden der Reihe nach freigeschaltet. Neuer Prüfpunkt: links „+ Prüfpunkt“."
```

**`conPRest.Y` vorher**

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; 232)
```

**`btnPNio.Y` vorher**

```
If((LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"); 360; (LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"); 350; 232) + 256
```

**`btnVsIO.Text` vorher**

```
"i.O."
```

**`btnVsNIO.Text` vorher**

```
"n.i.O."
```

**`btnVsIO.Width` vorher**

```
120
```

**`btnVsNIO.Width` vorher**

```
120
```

**`btnVsNIO.X` vorher**

```
144
```

**`lblVsRegeln.Text` vorher**

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "")
```

**`btnGlZeile.OnSelect` vorher**

```
If(!varIsLoading;
    If(ThisItem.Ebene = 3;
        Set(varAuswahlEbene; 3);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.BerID);;
        Set(varCtxK; ThisItem.KatID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);
    ThisItem.Ebene = 2;
        Set(varAuswahlEbene; 2);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.BerID);;
        Set(varCtxK; ThisItem.ID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);
    ThisItem.Ebene = 1;
        Set(varAuswahlEbene; 1);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.ID);;
        Set(varCtxK; 0);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt)
    )
)
```

**`btnGlNeuB.OnSelect` vorher**

```
If(varSchreibbar && !varIsLoading && Now() >= varSperreBis;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(!varEntwurfOk;
        false;
        false;
        Notify(""; NotificationType.Warning);
        Set(varNeuID; IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: "Neuer Bereich"; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(colB; RgReihenfolge); 0) + 10; Hinweis: ""; Aktiv: false; QuelleID: 0; Ausblenden: false}).ID; 0));;
        If(varNeuID = 0;
            Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
            Collect(colB; LookUp(RG_Bereiche; ID = varNeuID));;
            Set(varAuswahlEbene; 1);;
            Set(varAuswahlID; varNeuID);;
            Set(varCtxB; varNeuID);;
            Set(varCtxK; 0);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);;
            SetFocus(txtBName)
        )
    )
)
```

**`btnGlNeuK.OnSelect` vorher**

```
If(varSchreibbar && !varIsLoading && Now() >= varSperreBis;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(!varEntwurfOk;
        false;
        varCtxB = 0;
        Notify("Links zuerst einen Bereich antippen."; NotificationType.Warning);
        Set(varNeuID; IfError(Patch(RG_Kategorien; Defaults(RG_Kategorien); {Title: "Neue Kategorie"; BereichID: varCtxB; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colK; BereichID = varCtxB); RgReihenfolge); 0) + 10; Hinweis: ""; Aktiv: true; QuelleID: 0}).ID; 0));;
        If(varNeuID = 0;
            Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
            Collect(colK; LookUp(RG_Kategorien; ID = varNeuID));;
            Set(varAuswahlEbene; 2);;
            Set(varAuswahlID; varNeuID);;
            Set(varCtxB; varCtxB);;
            Set(varCtxK; varNeuID);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);;
            SetFocus(txtKName)
        )
    )
)
```

**`btnGlNeuP.OnSelect` vorher**

```
If(varSchreibbar && !varIsLoading && Now() >= varSperreBis;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(!varEntwurfOk;
        false;
        varCtxK = 0;
        Notify("Links zuerst eine Kategorie antippen."; NotificationType.Warning);
        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0) + 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: "IONIO"}; Pflicht: true; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: If(varAuswahlEbene = 3 && LookUp(colP; ID = varAuswahlID).KategorieID = varCtxK; Coalesce(LookUp(colP; ID = varAuswahlID).Abschnitt; ""); "")}).ID; 0));;
        If(varNeuID = 0;
            Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
            Collect(colP; LookUp(RG_Pruefpunkte; ID = varNeuID));;
            Set(varAuswahlEbene; 3);;
            Set(varAuswahlID; varNeuID);;
            Set(varCtxB; varCtxB);;
            Set(varCtxK; varCtxK);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);;
            SetFocus(txtPFrage)
        )
    )
)
```

**`btnPrZeile.OnSelect` vorher**

```
If(!varIsLoading && ThisItem.Ebene > 0;
    If(ThisItem.Ebene = 3;
        Set(varAuswahlEbene; 3);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.BerID);;
        Set(varCtxK; ThisItem.KatID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);
    ThisItem.Ebene = 2;
        Set(varAuswahlEbene; 2);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.BerID);;
        Set(varCtxK; ThisItem.ID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);
    ThisItem.Ebene = 1;
        Set(varAuswahlEbene; 1);;
        Set(varAuswahlID; ThisItem.ID);;
        Set(varCtxB; ThisItem.ID);;
        Set(varCtxK; 0);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt)
    )
)
```

**`ddKBereich.OnChange` vorher**

```
If(!IsBlank(Self.Selected) && Self.Selected.ID <> LookUp(colK; ID = varAuswahlID).BereichID && varSchreibbar;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(varEntwurfOk;
    With({ziel: Self.Selected.ID};
        Set(varPatchFehler; false);;
        IfError(Patch(RG_Kategorien; LookUp(RG_Kategorien; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {BereichID: ziel; RgReihenfolge: Coalesce(Max(Filter(colK; BereichID = ziel); RgReihenfolge); 0) + 10}); Set(varPatchFehler; true));;
        ClearCollect(colK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = varFassung));;
        If(varPatchFehler; Notify("Verschieben hat nicht geklappt."; NotificationType.Error); Notify("Verschoben (ans Ende des Bereichs)."; NotificationType.Success));;
        Set(varAuswahlEbene; 2);;
        Set(varAuswahlID; varAuswahlID);;
        Set(varCtxB; ziel);;
        Set(varCtxK; varAuswahlID);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt)
    ))
)
```

**`ddPKategorie.OnChange` vorher**

```
If(!IsBlank(Self.Selected) && Self.Selected.ID <> LookUp(colP; ID = varAuswahlID).KategorieID && varSchreibbar;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(varEntwurfOk;
    With({ziel: Self.Selected.ID; abh: CountRows(Filter(colP; BedingungPunkt = varAuswahlID))};
        Set(varPatchFehler; false);;
        ForAll(Filter(colP; BedingungPunkt = varAuswahlID) As d; Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = d.ID && RundgangID = varRgID && Fassung = varFassung); {BedingungPunkt: 0; BedingungWert: ""}));;
        IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {KategorieID: ziel; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = ziel); RgReihenfolge); 0) + 10; BedingungPunkt: 0; BedingungWert: ""}); Set(varPatchFehler; true));;
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung));;
        If(varPatchFehler;
            Notify("Verschieben hat nicht geklappt."; NotificationType.Error);
            Notify("Verschoben (ans Ende der Kategorie)." & If(abh > 0; " " & abh & " Bedingung(en), die auf diese Frage zeigten, wurden entfernt."; ""); NotificationType.Success)
        );;
        Set(varAuswahlEbene; 3);;
        Set(varAuswahlID; varAuswahlID);;
        Set(varCtxB; LookUp(colK; ID = ziel).BereichID);;
        Set(varCtxK; ziel);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt)
    ))
)
```

**`galAkt.Items` vorher**

```
Ungroup(
    Table(
        {T: ForAll(Filter(colP As p; IsBlank(LookUp(colAltP As a; a.ID = p.QuelleID))) As p; {Art: "neu"; Text: p.Title})};
        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) || Coalesce(p.Auswahlwerte; "") <> Coalesce(a.Auswahlwerte; "") || Coalesce(p.Einheit; "") <> Coalesce(a.Einheit; "") || Coalesce(p.MinWert; -999999) <> Coalesce(a.MinWert; -999999) || Coalesce(p.MaxWert; -999999) <> Coalesce(a.MaxWert; -999999) || Coalesce(p.Hinweis; "") <> Coalesce(a.Hinweis; "") || fnFotoWert(p.Foto.Value; Coalesce(p.FotoMoeglich; false)) <> fnFotoWert(a.Foto.Value; Coalesce(a.FotoMoeglich; false)) || Coalesce(p.KommentarPflicht; false) <> Coalesce(a.KommentarPflicht; false) || fnGrenzmodus(p.Grenzmodus.Value) <> fnGrenzmodus(a.Grenzmodus.Value) || Coalesce(p.BedingungWert; "") <> Coalesce(a.BedingungWert; "") || Coalesce(LookUp(colP As b0; b0.ID = p.BedingungPunkt).QuelleID; 0) <> Coalesce(a.BedingungPunkt; 0) || Coalesce(p.HinweisBildID; 0) <> Coalesce(a.HinweisBildID; 0) || Coalesce(LookUp(colK As k0; k0.ID = p.KategorieID).QuelleID; 0) <> a.KategorieID || Trim(Coalesce(p.Abschnitt; "")) <> Trim(Coalesce(a.Abschnitt; "")) || Coalesce(p.Kritisch; false) <> Coalesce(a.Kritisch; false) || Coalesce(p.KritischText; "") <> Coalesce(a.KritischText; "") || Coalesce(p.Ansprechpartner; "") <> Coalesce(a.Ansprechpartner; "") || Coalesce(p.Rueckfrage; false) <> Coalesce(a.Rueckfrage; false) || Coalesce(p.RueckfrageText; "") <> Coalesce(a.RueckfrageText; "")))) As p; {Art: "geändert"; Text: p.Title})};
        {T: ForAll(Filter(colAltP As a; IsBlank(LookUp(colP As p; p.QuelleID = a.ID))) As a; {Art: "entfernt"; Text: a.Title})}
    );
    T
)
```

**`btnMehrAnlegen.OnSelect` vorher**

```
If(varSchreibbar && !varIsLoading && Now() >= varSperreBis;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    ClearCollect(colMehr; Filter(ForAll(Split(Substitute(txtMehr.Text; Char(13); ""); Char(10)) As z; {F: Left(Trim(z.Value); 255)}); F <> ""));;
    Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(!varEntwurfOk;
        Set(varMehrereOffen; false);
        varCtxK = 0;
        Notify("Links zuerst eine Kategorie antippen."; NotificationType.Warning);
        IsEmpty(colMehr);
        Notify("Bitte mindestens eine Frage eintragen."; NotificationType.Warning);
        Set(varIsLoading; true);;
        ClearCollect(colMehrErg;
            With({basis: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0)};
                ForAll(Sequence(CountRows(colMehr)) As i;
                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: varMehrTyp}; Pflicht: varMehrPflicht; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: Left(Trim(txtMehrAbschnitt.Text); 255)}).ID; 0)}
                )
            )
        );;
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung));;
        If(CountRows(Filter(colMehrErg; Neu = 0)) > 0;
            Notify(CountRows(Filter(colMehrErg; Neu = 0)) & " Fragen konnten nicht angelegt werden. Bitte die Gliederung prüfen."; NotificationType.Error);
            Notify(CountRows(colMehrErg) & " Prüfpunkte angelegt."; NotificationType.Success);;
            Reset(txtMehr);;
            Reset(txtMehrAbschnitt);;
            Set(varMehrereOffen; false)
        );;
        Set(varIsLoading; false)
    )
)
```

**`btnEdEntf.OnSelect` vorher**

```
If(varSchreibbar && varAuswahlEbene > 0; If(!varIsLoading && Now() >= varSperreBis;
        If(varFrage <> "del" & varAuswahlEbene & "-" & varAuswahlID;
            Set(varFrage; "del" & varAuswahlEbene & "-" & varAuswahlID);;
            Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));
            Set(varFrage; "");;
            Refresh(RG_Rundgaenge);;
    Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
    If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
    If(varEntwurfOk;
    Set(varIsLoading; true);;
    If(varAuswahlEbene = 3;
        ForAll(Filter(colP; BedingungPunkt = varAuswahlID) As d; Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = d.ID && RundgangID = varRgID && Fassung = varFassung); {BedingungPunkt: 0; BedingungWert: ""}));;
        Remove(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung));
        varAuswahlEbene = 2;
        Remove(RG_Pruefpunkte; Filter(RG_Pruefpunkte; KategorieID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung));;
        Remove(RG_Kategorien; LookUp(RG_Kategorien; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung));
        varAuswahlEbene = 1;
        ForAll(Filter(colK; BereichID = varAuswahlID) As k; Remove(RG_Pruefpunkte; Filter(RG_Pruefpunkte; KategorieID = k.ID && RundgangID = varRgID && Fassung = varFassung)));;
        Remove(RG_Kategorien; Filter(RG_Kategorien; BereichID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung));;
        Remove(RG_Bereiche; LookUp(RG_Bereiche; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung))
    );;
    Concurrent(
        ClearCollect(colB; Filter(RG_Bereiche; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung))
    );;
    If((varAuswahlEbene = 3 && !IsBlank(LookUp(colP; ID = varAuswahlID))) || (varAuswahlEbene = 2 && !IsBlank(LookUp(colK; ID = varAuswahlID))) || (varAuswahlEbene = 1 && !IsBlank(LookUp(colB; ID = varAuswahlID)));
        Notify("Entfernen hat nicht geklappt. Bitte erneut versuchen."; NotificationType.Error);
        Notify("Entfernt."; NotificationType.Success)
    );;
    If(varAuswahlEbene = 3;
        Set(varAuswahlEbene; 2);;
        Set(varAuswahlID; varCtxK);;
        Set(varCtxB; varCtxB);;
        Set(varCtxK; varCtxK);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);
        varAuswahlEbene = 2;
        Set(varAuswahlEbene; 1);;
        Set(varAuswahlID; varCtxB);;
        Set(varCtxB; varCtxB);;
        Set(varCtxK; 0);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt);
        Set(varAuswahlEbene; 0);;
        Set(varAuswahlID; 0);;
        Set(varCtxB; 0);;
        Set(varCtxK; 0);;
        Set(varFrage; "");;
        Reset(txtBName);;
        Reset(txtKName);;
        Reset(ddKBereich);;
        Reset(txtPFrage);;
        Reset(txtPEinheit);;
        Reset(txtPMin);;
        Reset(txtPMax);;
        Reset(txtPWerte);;
        Reset(txtPHinweis);;
        Reset(ddPKategorie);;
        Reset(ddPBedA);;
        Reset(ddPBedW);;
        Reset(txtPAbschnitt)
    );;
    Set(varIsLoading; false)
    )
        )
    ))
```

**`galPr.Items` vorher**

```
Sort(
    Ungroup(
        Table(
            {T: Filter(Table({Art: "Fehler"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Der Rundgang hat noch keinen Bereich. → „+ Bereich“"}); IsEmpty(colB))};
            {T: ForAll(Filter(colB As b; IsEmpty(Filter(colK As k; k.BereichID = b.ID))) As b; {Art: "Fehler"; Ebene: 1; ID: b.ID; KatID: 0; BerID: b.ID; Text: "Bereich „" & b.Title & "“ hat keine Kategorie."})};
            {T: ForAll(Filter(colK As k; IsEmpty(Filter(colP As p; p.KategorieID = k.ID))) As k; {Art: "Fehler"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat keinen Prüfpunkt."})};
            {T: ForAll(Filter(colB As b; Trim(Coalesce(b.Title; "")) = "") As b; {Art: "Fehler"; Ebene: 1; ID: b.ID; KatID: 0; BerID: b.ID; Text: "Ein Bereich hat keinen Namen."})};
            {T: ForAll(Filter(colK As k; Trim(Coalesce(k.Title; "")) = "") As k; {Art: "Fehler"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Eine Kategorie hat keinen Namen."})};
            {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Title; "")) = "") As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Ein Prüfpunkt hat keine Frage."})};
            {T: ForAll(Filter(colP As p; (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerte(p.Auswahlwerte) < 2) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: mindestens zwei Antwortmöglichkeiten eintragen."})};
            {T: ForAll(Filter(colP As p; (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerteDoppelt(p.Auswahlwerte)) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: eine Antwortmöglichkeit steht doppelt da."})};
            {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && !IsBlank(p.MinWert) && !IsBlank(p.MaxWert) && p.MinWert > p.MaxWert) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: „ab“ ist größer als „bis“."})};
            {T: ForAll(Filter(ForAll(Filter(colP As p0; Coalesce(p0.BedingungPunkt; 0) <> 0) As p; With({a: LookUp(colP As a0; a0.ID = p.BedingungPunkt)}; {ID: p.ID; KategorieID: p.KategorieID; Title: p.Title; G: If(IsBlank(a) || a.KategorieID <> p.KategorieID; "Die Bedingung zeigt auf eine Frage außerhalb dieser Kategorie."; Coalesce(a.BedingungPunkt; 0) <> 0; "Die Frage der Bedingung hat selbst eine Bedingung (nur eine Ebene erlaubt)."; a.RgReihenfolge * 1000000 + a.ID > p.RgReihenfolge * 1000000 + p.ID; "Die Frage der Bedingung muss weiter oben stehen."; !fnBedGueltig(p.BedingungWert; a.Eingabetyp.Value; a.Auswahlwerte); "Der Wert der Bedingung passt nicht zu „" & a.Title & "“."; "")})); G <> "") As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: " & p.G})};
            {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && fnGrenzmodus(p.Grenzmodus.Value) <> "Mangel" && IsBlank(p.MinWert) && IsBlank(p.MaxWert)) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: „Außerhalb“ wirkt nur mit Grenzen (ab/bis)."})};
            {T: ForAll(Filter(colP As p; p.Foto.Value = "Bei Mangel Pflicht" && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: „Foto Pflicht bei Mangel“ wirkt nur bei i.O./n.i.O. und Zahl."})};
            {T: ForAll(Filter(colP As p; CountRows(Filter(colP As q; q.KategorieID = p.KategorieID && Lower(Trim(q.Title)) = Lower(Trim(p.Title)))) > 1) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“ steht in der Kategorie doppelt."})};
            {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Abschnitt; "")) <> "" && With({v: First(Sort(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 1000000 + q.ID < p.RgReihenfolge * 1000000 + p.ID); RgReihenfolge * 1000000 + ID; SortOrder.Descending))}; !IsBlank(v) && Lower(Trim(Coalesce(v.Abschnitt; ""))) <> Lower(Trim(p.Abschnitt))) && CountRows(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 1000000 + q.ID < p.RgReihenfolge * 1000000 + p.ID && Lower(Trim(Coalesce(q.Abschnitt; ""))) = Lower(Trim(p.Abschnitt)))) > 0) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Abschnitt „" & Trim(p.Abschnitt) & "“ ist unterbrochen: Die Fragen stehen nicht zusammen (bei „" & p.Title & "“). Mit ↑ ↓ zusammenschieben."})};
            {T: ForAll(Filter(colP As p; (Coalesce(p.Kritisch; false) || Coalesce(p.Rueckfrage; false)) && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Rückfrage und „kritisch“ wirken nur bei i.O./n.i.O. und Zahl."})};
            {T: ForAll(Filter(colP As p; Coalesce(p.Kritisch; false) && Trim(Coalesce(p.Ansprechpartner; "")) = "") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“ ist kritisch, aber ohne eigenen Ansprechpartner (es erscheinen nur die allgemeinen)."})};
            {T: ForAll(Filter(colP As p; p.Title = "Neue Frage") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Eine Frage heißt noch „Neue Frage“."})};
            {T: ForAll(Filter(colK As k; CountRows(Filter(colP As p; p.KategorieID = k.ID)) > 30) As k; {Art: "Hinweis"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat über 30 Prüfpunkte (lange Seite für den Prüfer)."})};
            {T: Filter(Table({Art: "Hinweis"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Kein aktiver Plan: Der Rundgang erscheint nie auf der Startseite. → In der Übersicht „Plan“ tippen."}); !varIstVorlage && IsEmpty(Filter(colPlanR; Coalesce(Aktiv; false))))}
        );
        T
    );
    If(Art = "Fehler"; 0; 1)
)
```

**`tmrArbeit.OnTimerEnd` vorher**

```
Set(varArbeitStart; false);;
Set(varIsLoading; true);;
If(varJob = "vorbereiten";
    Set(varLadeText; "Rundgang wird für den Builder vorbereitet …");;
    Concurrent(Refresh(RG_Rundgaenge); Refresh(RG_Bereiche); Refresh(RG_Kategorien); Refresh(RG_Pruefpunkte));;
    Set(varRg; LookUp(RG_Rundgaenge; ID = varRgID));;
    ClearCollect(colVbB; Filter(RG_Bereiche; RundgangID = varRgID));;
    Clear(colVbK);;
    ForAll(colVbB As b; Collect(colVbK; Filter(RG_Kategorien; BereichID = b.ID)));;
    Clear(colVbP);;
    ForAll(colVbK As k; Collect(colVbP; Filter(RG_Pruefpunkte; KategorieID = k.ID)));;
    ClearCollect(colVbErg; ForAll(Filter(colVbB; IsBlank(Fassung)) As b; {Ok: !IsError(Patch(RG_Bereiche; LookUp(RG_Bereiche; ID = b.ID); {Fassung: 1; QuelleID: 0}))}));;
    Collect(colVbErg; ForAll(Filter(colVbK; IsBlank(Fassung) || IsBlank(RundgangID)) As k; {Ok: !IsError(Patch(RG_Kategorien; LookUp(RG_Kategorien; ID = k.ID); {Fassung: 1; RundgangID: varRgID; QuelleID: 0}))}));;
    Collect(colVbErg; ForAll(Filter(colVbP; IsBlank(Fassung) || IsBlank(RundgangID)) As p; {Ok: !IsError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = p.ID); {Fassung: 1; RundgangID: varRgID; QuelleID: 0}))}));;
    Set(varPatchFehler; CountRows(Filter(colVbErg; !Ok)) > 0);;
    If(!varPatchFehler;
        If(IsError(Patch(RG_Rundgaenge; LookUp(RG_Rundgaenge; ID = varRgID); {Fassung: 1; EntwurfFassung: 0; EntwurfVon: ""; Status: If(Coalesce(varRg.Aktiv; false); "Aktiv"; "Archiviert")})); Set(varPatchFehler; true))
    );;
    If(varPatchFehler;
        Notify("Vorbereiten unvollständig. Bitte den Rundgang erneut öffnen (das ist gefahrlos)."; NotificationType.Error);;
        Set(varJob; "zurueck");
        Set(varFassung; 1);;
        Set(varJob; varNach);;
        Set(varNach; "")
    )
);;
If(varJob = "neueFassung";
    Set(varLadeText; "Neue Fassung wird angelegt …");;
    Concurrent(Refresh(RG_Rundgaenge); Refresh(RG_Bereiche); Refresh(RG_Kategorien); Refresh(RG_Pruefpunkte));;
    Set(varRg; LookUp(RG_Rundgaenge; ID = varRgID));;
    If(Coalesce(varRg.EntwurfFassung; 0) > 0;
        Set(varFassung; varRg.EntwurfFassung);;
        Set(varSchreibbar; true);;
        Notify("Es gibt schon einen Entwurf – er wird geöffnet."; NotificationType.Information);;
        Set(varJob; "laden");
        ClearCollect(colAlleB; Filter(RG_Bereiche; RundgangID = varRgID));;
        Set(varZielF; Max(Coalesce(Max(colAlleB; Coalesce(Fassung; 0)); 0); Coalesce(First(Sort(Filter(RG_Kategorien; RundgangID = varRgID); Fassung; SortOrder.Descending)).Fassung; 0); Coalesce(First(Sort(Filter(RG_Pruefpunkte; RundgangID = varRgID); Fassung; SortOrder.Descending)).Fassung; 0); fnAktiveFassung(varRg.Fassung)) + 1);;
        Set(varPatchFehler; false);;
        IfError(Patch(RG_Rundgaenge; LookUp(RG_Rundgaenge; ID = varRgID); {EntwurfFassung: varZielF; EntwurfVon: User().FullName}); Set(varPatchFehler; true));;
        If(varPatchFehler;
            Notify("Die neue Fassung konnte nicht angelegt werden. Bitte erneut versuchen."; NotificationType.Error);;
            Set(varJob; "zurueck");
            ClearCollect(colQB; Filter(colAlleB; Coalesce(Fassung; 0) = fnAktiveFassung(varRg.Fassung)));;
            ClearCollect(colQK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = fnAktiveFassung(varRg.Fassung)));;
            ClearCollect(colQP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = fnAktiveFassung(varRg.Fassung)));;
            RemoveIf(colQB; !Coalesce(Aktiv; false));;
            RemoveIf(colQK; !Coalesce(Aktiv; false));;
            RemoveIf(colQP; !Coalesce(Aktiv; false));;
            RemoveIf(colQK; IsBlank(LookUp(colQB As b0; b0.ID = BereichID)));;
            RemoveIf(colQP; IsBlank(LookUp(colQK As k0; k0.ID = KategorieID)));;
            Set(varZielR; varRgID);;
            Set(varZielB; 0);;
            Set(varZielK; 0);;
            Set(varZielBAktiv; false);;
            Set(varKopieBehalteR; true);;
            Set(varKopieZusatz; "");;
            Set(varFassung; varZielF);;
            Set(varSchreibbar; true);;
            Set(varKopieNach; "laden");;
            Set(varJob; "kopie")
        )
    )
);;
If(varJob = "quelle";
    Set(varLadeText; "Rundgang wird kopiert …");;
    Concurrent(
        ClearCollect(colQB; Filter(RG_Bereiche; RundgangID = varQuelleR && Fassung = varQuelleF));
        ClearCollect(colQK; Filter(RG_Kategorien; RundgangID = varQuelleR && Fassung = varQuelleF));
        ClearCollect(colQP; Filter(RG_Pruefpunkte; RundgangID = varQuelleR && Fassung = varQuelleF))
    );;
    If(varQuelleNurAktiv;
        RemoveIf(colQB; !Coalesce(Aktiv; false));;
        RemoveIf(colQK; !Coalesce(Aktiv; false));;
        RemoveIf(colQP; !Coalesce(Aktiv; false));;
        RemoveIf(colQK; IsBlank(LookUp(colQB As b0; b0.ID = BereichID)));;
        RemoveIf(colQP; IsBlank(LookUp(colQK As k0; k0.ID = KategorieID)))
    );;
    Set(varZielB; 0);;
    Set(varZielK; 0);;
    Set(varZielBAktiv; false);;
    Set(varKopieBehalteR; true);;
    Set(varKopieZusatz; "");;
    Set(varKopieNach; "laden");;
    Set(varJob; "kopie")
);;
If(varJob = "kopie";
    Set(varLadeText; "Wird kopiert …");;
    ClearCollect(colMapB;
        With({qs: Sort(colQB; RgReihenfolge * 1000000 + ID)};
            ForAll(Sequence(CountRows(qs)) As i;
                With({q: Index(qs; i.Value)};
                    {Alt: q.ID;
                     Neu: IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: Left(q.Title & varKopieZusatz; 255); RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(colB; RgReihenfolge); 0) + i.Value * 10); Hinweis: q.Hinweis; Aktiv: varZielBAktiv; QuelleID: q.ID; Ausblenden: Coalesce(q.Ausblenden; false)}).ID; 0)}
                )
            )
        )
    );;
    ClearCollect(colMapK;
        With({qs: Sort(colQK; RgReihenfolge * 1000000 + ID)};
            ForAll(Sequence(CountRows(qs)) As i;
                With({q: Index(qs; i.Value)};
                    With({ziel: If(IsEmpty(colQB); varZielB; Coalesce(LookUp(colMapB; Alt = q.BereichID).Neu; 0))};
                        {Alt: q.ID;
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Kategorien; Defaults(RG_Kategorien); {Title: Left(q.Title & If(IsEmpty(colQB); varKopieZusatz; ""); 255); BereichID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQB) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colK; BereichID = varZielB); RgReihenfolge); 0) + i.Value * 10); Hinweis: q.Hinweis; Aktiv: true; QuelleID: q.ID}).ID; 0))}
                    )
                )
            )
        )
    );;
    ClearCollect(colMapP;
        With({qs: Sort(colQP; RgReihenfolge * 1000000 + ID)};
            ForAll(Sequence(CountRows(qs)) As i;
                With({q: Index(qs; i.Value)};
                    With({ziel: If(IsEmpty(colQK); varZielK; Coalesce(LookUp(colMapK; Alt = q.KategorieID).Neu; 0))};
                        {Alt: q.ID; BedAlt: Coalesce(q.BedingungPunkt; 0); BedWert: Coalesce(q.BedingungWert; ""); Ziel: ziel;
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQK) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colP; KategorieID = varZielK); RgReihenfolge); 0) + i.Value * 10); Aktiv: true; QuelleID: q.ID; Eingabetyp: {Value: Coalesce(q.Eingabetyp.Value; "IONIO")}; Pflicht: Coalesce(q.Pflicht; false); Auswahlwerte: q.Auswahlwerte; Einheit: q.Einheit; MinWert: q.MinWert; MaxWert: q.MaxWert; Hinweis: q.Hinweis; FotoMoeglich: Coalesce(q.FotoMoeglich; false); Foto: {Value: fnFotoWert(q.Foto.Value; Coalesce(q.FotoMoeglich; false))}; KommentarPflicht: Coalesce(q.KommentarPflicht; false); Grenzmodus: {Value: fnGrenzmodus(q.Grenzmodus.Value)}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: Coalesce(q.HinweisBildID; 0); Abschnitt: Coalesce(q.Abschnitt; ""); Kritisch: Coalesce(q.Kritisch; false); KritischText: Coalesce(q.KritischText; ""); Ansprechpartner: Coalesce(q.Ansprechpartner; ""); Rueckfrage: Coalesce(q.Rueckfrage; false); RueckfrageText: Coalesce(q.RueckfrageText; "")}).ID; 0))}
                    )
                )
            )
        )
    );;
    ClearCollect(colBedErg;
        ForAll(Filter(colMapP; BedAlt <> 0 && Neu <> 0) As m;
            With({a: LookUp(colMapP As m2; m2.Alt = m.BedAlt)};
                With({neuA: If(!IsBlank(a) && a.Ziel = m.Ziel; a.Neu; IsBlank(a) && LookUp(colP As p0; p0.ID = m.BedAlt).KategorieID = m.Ziel; m.BedAlt; 0)};
                    {Ok: If(neuA = 0; true; !IsError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = m.Neu); {BedingungPunkt: neuA; BedingungWert: m.BedWert})))}
                )
            )
        )
    );;
    Set(varKopieFehler; CountRows(Filter(colMapB; Neu = 0)) + CountRows(Filter(colMapK; Neu = 0)) + CountRows(Filter(colMapP; Neu = 0)) + CountRows(Filter(colBedErg; !Ok)));;
    If(varKopieFehler > 0 && varKopieNach = "laden";
        If(Coalesce(LookUp(RG_Rundgaenge; ID = varZielR).Fassung; 0) = 0 || varZielF <> fnAktiveFassung(LookUp(RG_Rundgaenge; ID = varZielR).Fassung);
            Remove(RG_Pruefpunkte; Filter(RG_Pruefpunkte; RundgangID = varZielR && Fassung = varZielF));;
            Remove(RG_Kategorien; Filter(RG_Kategorien; RundgangID = varZielR && Fassung = varZielF));;
            Remove(RG_Bereiche; Filter(RG_Bereiche; RundgangID = varZielR && Fassung = varZielF))
        );;
        If(Coalesce(LookUp(RG_Rundgaenge; ID = varZielR).Fassung; 0) > 0 && varZielF <> fnAktiveFassung(LookUp(RG_Rundgaenge; ID = varZielR).Fassung);
            If(IsError(Patch(RG_Rundgaenge; LookUp(RG_Rundgaenge; ID = varZielR); {EntwurfFassung: 0; EntwurfVon: ""})); Set(varPatchFehler; true))
        );;
        Notify("Kopieren fehlgeschlagen (" & varKopieFehler & " Teile fehlen). Der Entwurf wurde zurückgenommen. Bitte erneut versuchen."; NotificationType.Error);;
        Set(varJob; "zurueck");
        varKopieFehler > 0;
        Notify("Kopieren unvollständig: " & varKopieFehler & " Teile fehlen. Bitte die Gliederung prüfen."; NotificationType.Error);;
        Set(varJob; varKopieNach);
        Notify("Kopiert: " & CountRows(colMapP) & " Prüfpunkte."; NotificationType.Success);;
        Set(varJob; varKopieNach)
    )
);;
If(varJob = "laden";
    Set(varLadeText; "Rundgang wird geladen …");;
    Concurrent(Refresh(RG_Rundgaenge); Refresh(RG_Bereiche); Refresh(RG_Kategorien); Refresh(RG_Pruefpunkte); Refresh(RG_Plan));;
    Set(varRg; LookUp(RG_Rundgaenge; ID = varRgID));;
    Set(varIstVorlage; fnStatus(varRg.Status; varRg.Aktiv) = "Vorlage");;
    Concurrent(
        ClearCollect(colB; Filter(RG_Bereiche; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung))
    );;
    ClearCollect(colPlanR; Filter(RG_Plan; RundgangID = varRgID));;
    Set(varAktivRest; false);;
    If(varSchreibbar && !varIstVorlage && Coalesce(varRg.EntwurfFassung; 0) <> varFassung;
        Set(varSchreibbar; false);;
        Notify("Dieser Entwurf ist nicht mehr offen. Er wird nur zum Lesen gezeigt."; NotificationType.Warning)
    );;
    If(varSchreibbar && !varIstVorlage && CountRows(Filter(colB; Coalesce(Aktiv; false))) > 0;
        Set(varSchreibbar; false);;
        Set(varAktivRest; true);;
        Notify("Das Aktivieren dieser Fassung ist unvollständig. Bitte oben „Aktivieren …“ erneut tippen."; NotificationType.Error)
    );;
    If(!varSchreibbar && !varAktivRest;
        RemoveIf(colB; !Coalesce(Aktiv; false));;
        RemoveIf(colK; !Coalesce(Aktiv; false));;
        RemoveIf(colP; !Coalesce(Aktiv; false));;
        RemoveIf(colK; IsBlank(LookUp(colB As b0; b0.ID = BereichID)));;
        RemoveIf(colP; IsBlank(LookUp(colK As k0; k0.ID = KategorieID)))
    );;
    Set(varGespeichertText; "");;
    With({b1: First(Sort(colB; RgReihenfolge * 1000000 + ID))};
        If(IsBlank(b1);
            Set(varAuswahlEbene; 0);;
            Set(varAuswahlID; 0);;
            Set(varCtxB; 0);;
            Set(varCtxK; 0);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt);
            Set(varAuswahlEbene; 1);;
            Set(varAuswahlID; b1.ID);;
            Set(varCtxB; b1.ID);;
            Set(varCtxK; 0);;
            Set(varFrage; "");;
            Reset(txtBName);;
            Reset(txtKName);;
            Reset(ddKBereich);;
            Reset(txtPFrage);;
            Reset(txtPEinheit);;
            Reset(txtPMin);;
            Reset(txtPMax);;
            Reset(txtPWerte);;
            Reset(txtPHinweis);;
            Reset(ddPKategorie);;
            Reset(ddPBedA);;
            Reset(ddPBedW);;
            Reset(txtPAbschnitt)
        )
    );;
    Set(varJob; "")
);;
If(varJob = "auswahl";
    Concurrent(
        ClearCollect(colB; Filter(RG_Bereiche; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colK; Filter(RG_Kategorien; RundgangID = varRgID && Fassung = varFassung));
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung))
    );;
    If(!IsEmpty(colQB);
        With({n: First(colMapB).Neu}; If(n > 0; Set(varAuswahlEbene; 1);; Set(varAuswahlID; n);; Set(varCtxB; n);; Set(varCtxK; 0);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW);; Reset(txtPAbschnitt)));
        !IsEmpty(colQK);
        With({n: First(colMapK).Neu}; If(n > 0; Set(varAuswahlEbene; 2);; Set(varAuswahlID; n);; Set(varCtxB; varZielB);; Set(varCtxK; n);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW);; Reset(txtPAbschnitt)));
        With({n: First(colMapP).Neu}; If(n > 0; Set(varAuswahlEbene; 3);; Set(varAuswahlID; n);; Set(varCtxB; LookUp(colK; ID = varZielK).BereichID);; Set(varCtxK; varZielK);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW);; Reset(txtPAbschnitt)))
    );;
    Set(varJob; "")
);;
If(varJob = "aktivieren";
    Set(varLadeText; "Fassung wird aktiviert …");;
    Concurrent(Refresh(RG_Rundgaenge); Refresh(RG_Bereiche); Refresh(RG_Kategorien));;
    Set(varRg; LookUp(RG_Rundgaenge; ID = varRgID));;
    If(Coalesce(varRg.EntwurfFassung; 0) <> varFassung;
        Notify("Dieser Entwurf wurde inzwischen schon aktiviert oder verworfen. Die Übersicht wird neu geladen."; NotificationType.Error);;
        Set(varJob; "zurueck");
        ClearCollect(colAktB; Filter(RG_Bereiche; RundgangID = varRgID));;
        ClearCollect(colAktK; Filter(RG_Kategorien; RundgangID = varRgID));;
        ClearCollect(colAltB; Filter(colAktB; Coalesce(Aktiv; false) && Coalesce(Fassung; 0) <> varFassung));;
        ClearCollect(colAltK; Filter(colAktK; Coalesce(Aktiv; false) && Coalesce(Fassung; 0) <> varFassung));;
        ClearCollect(colNeuB; Filter(colAktB; Coalesce(Fassung; 0) = varFassung));;
        ClearCollect(colAktErg; ForAll(colAltB As b; {Ok: !IsError(Patch(RG_Bereiche; LookUp(RG_Bereiche; ID = b.ID); {Aktiv: false}))}));;
        Collect(colAktErg; ForAll(colAltK As k; {Ok: !IsError(Patch(RG_Kategorien; LookUp(RG_Kategorien; ID = k.ID); {Aktiv: false}))}));;
        Set(varPatchFehler; CountRows(Filter(colAktErg; !Ok)) > 0);;
        If(!varPatchFehler;
            Collect(colAktErg; ForAll(colNeuB As b; {Ok: !IsError(Patch(RG_Bereiche; LookUp(RG_Bereiche; ID = b.ID); {Aktiv: true}))}));;
            Set(varPatchFehler; CountRows(Filter(colAktErg; !Ok)) > 0)
        );;
        Refresh(RG_Bereiche);;
        ClearCollect(colAktB; Filter(RG_Bereiche; RundgangID = varRgID));;
        If(!varPatchFehler && CountRows(Filter(colAktB; Coalesce(Aktiv; false) && Coalesce(Fassung; 0) <> varFassung)) = 0 && CountRows(Filter(colAktB; Coalesce(Aktiv; false) && Coalesce(Fassung; 0) = varFassung)) = CountRows(colNeuB);
            If(IsError(Patch(RG_Rundgaenge; LookUp(RG_Rundgaenge; ID = varRgID); {Fassung: varFassung; EntwurfFassung: 0; EntwurfVon: ""; Status: "Aktiv"; Aktiv: true})); Set(varPatchFehler; true));
            Set(varPatchFehler; true)
        );;
        If(varPatchFehler;
            Notify("Aktivieren unvollständig. Bitte noch einmal „Aktivieren …“ tippen – das ist gefahrlos."; NotificationType.Error);;
            Set(varSchreibbar; false);;
            Set(varAktivRest; true);;
            Set(varJob; "");
            Notify("Fassung " & varFassung & " ist aktiv. Laufende Rundgänge von heute werden mit der alten Fassung beendet."; NotificationType.Success);;
            Set(varJob; "zurueck")
        )
    )
);;
If(varJob = "zurueck";
    Set(varJob; "");;
    Set(varIsLoading; false);;
    Navigate(scrListe; ScreenTransition.None)
);;
Set(varIsLoading; false)
```

