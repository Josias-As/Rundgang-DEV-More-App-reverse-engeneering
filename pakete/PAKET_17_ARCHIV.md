# Paket 17 – Rundgang-App: Archiv vergangener Rundgänge

Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket17) und `werkzeuge/doc_paket17.py`. **Voraussetzung: Paket N, 8–10, 12+16, 14+15 eingefügt** (es baut auf deren Stand auf; inhaltlich hängt es nur an `btnRuZurueck`, `scrStart`).

## Kurzfassung

- Neuer Bildschirm **„Archiv“** (Knopf „🗂 Archiv“ auf der Startseite). Zeitraum (Standard: letzte 3 Monate), Rundgang (alle oder einer), Schalter „nur mit Mängeln“, „auch offene“, „Testläufe“.
- Liste: Rundgang, Tag mit KW, Prüfer, Anzahl n.i.O. **„Ansehen“** öffnet den Rundgang wie gewohnt nur zum Lesen (Kategorien, Protokoll). **„PDF“** öffnet das archivierte Protokoll, wenn es eins gibt. „Zurück“ führt wieder ins Archiv.
- Offene (nicht abgeschlossene) Rundgänge werden nur angezeigt. Fortsetzen geht wie bisher über die Startseite am jeweiligen Tag.
- Daten: nur lesen. SharePoint filtert nach Zeitraum und Rundgang (delegierbar), der Rest in der App. Höchstens 500 je Suche.
- Umfang: 1 neuer Bildschirm, 1 neuer Knopf, 3 Properties. Keine neuen Spalten. Generator 0 Fehler. **Nicht in Studio getestet. Nicht unabhängig geprüft.**

## Schritt 1 – Bildschirm „Archiv“

**Wo hin:** In der Strukturansicht einen Bildschirm markieren (z. B. `scrProtokoll`) → Strg+V. Studio legt `scrArchiv` an.

```yaml
Screens:
  scrArchiv:
    Properties:
      Fill: =clrHintergrund
      OnVisible: |-
        =Set(varArTest, Coalesce(varArTest, false));
        Set(varArOffen, Coalesce(varArOffen, false));
        Set(varArNurNio, Coalesce(varArNurNio, false));
        If(IsEmpty(colArRg), ClearCollect(colArRg, Sort(ShowColumns(RG_Rundgaenge, ID, Title), Title)));
        If(IsEmpty(colArchiv), Select(btnArSuchen))
    Children:
      - conArKopf:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            Fill: =clrPrimaer
            Height: =96
            Width: =Parent.Width
          Children:
          - btnArZurueck:
              Control: Classic/Button@2.2.0
              Properties:
                BorderThickness: =0
                Color: =Color.White
                DisabledBorderColor: =clrGesperrtHell
                DisabledColor: =clrGesperrt
                DisabledFill: =clrGesperrtHell
                Fill: =RGBA(255, 255, 255, 0.14)
                Font: =Font.'Segoe UI'
                Height: =52
                HoverColor: =Color.White
                HoverFill: =RGBA(255, 255, 255, 0.26)
                OnSelect: |-
                  =If(!varIsLoading,
                      Set(varAusArchiv, false);
                      Navigate(scrStart, ScreenTransition.None)
                  )
                PressedColor: =Color.White
                PressedFill: =RGBA(255, 255, 255, 0.34)
                RadiusBottomLeft: =8
                RadiusBottomRight: =8
                RadiusTopLeft: =8
                RadiusTopRight: =8
                Size: =16
                Text: ="← Start"
                Width: =140
                X: =24
                Y: =22
          - lblArTitel:
              Control: Label@2.5.1
              Properties:
                Color: =Color.White
                Font: =Font.'Segoe UI'
                FontWeight: =FontWeight.Semibold
                Height: =96
                Size: =24
                Text: ="Archiv"
                Width: =Parent.Width - 200
                X: =180
                Y: =0
      - lblArVon:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =24
            Size: =13
            Text: ="von"
            Width: =220
            X: =24
            Y: =108
      - dpArVon:
          Control: Classic/DatePicker@2.6.0
          Properties:
            AccessibleLabel: ="Zeitraum von"
            BorderColor: =clrRahmen
            Color: =clrText
            DefaultDate: =DateAdd(Today(), -3, TimeUnit.Months)
            Font: =Font.'Segoe UI'
            Format: =DateTimeFormat.ShortDate
            Height: =52
            IconBackground: =clrPrimaer
            IconFill: =Color.White
            Size: =15
            StartOfWeek: =StartOfWeek.Monday
            Width: =220
            X: =24
            Y: =132
      - lblArBis:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =24
            Size: =13
            Text: ="bis"
            Width: =220
            X: =260
            Y: =108
      - dpArBis:
          Control: Classic/DatePicker@2.6.0
          Properties:
            AccessibleLabel: ="Zeitraum bis"
            BorderColor: =clrRahmen
            Color: =clrText
            DefaultDate: =Today()
            Font: =Font.'Segoe UI'
            Format: =DateTimeFormat.ShortDate
            Height: =52
            IconBackground: =clrPrimaer
            IconFill: =Color.White
            Size: =15
            StartOfWeek: =StartOfWeek.Monday
            Width: =220
            X: =260
            Y: =132
      - btnArSuchen:
          Control: Classic/Button@2.2.0
          Properties:
            BorderThickness: =0
            Color: =Color.White
            DisabledBorderColor: =clrGesperrtHell
            DisabledColor: =clrGesperrt
            DisabledFill: =clrGesperrtHell
            DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
            Fill: =clrPrimaer
            Font: =Font.'Segoe UI'
            Height: =52
            HoverColor: =Color.White
            HoverFill: =ColorFade(clrPrimaer, -20%)
            OnSelect: |-
              =If(!varIsLoading,
                  Set(varIsLoading, true);
                  Set(varArVon, Coalesce(dpArVon.SelectedDate, DateAdd(Today(), -3, TimeUnit.Months)));
                  Set(varArBis, DateAdd(Coalesce(dpArBis.SelectedDate, Today()), 1, TimeUnit.Days));
                  Set(varArRg, Coalesce(ddArRg.Selected.ID, 0));
                  Refresh(RG_Durchfuehrungen);
                  If(varArRg = 0,
                      ClearCollect(colArchiv, Sort(Filter(RG_Durchfuehrungen, StartZeit >= varArVon && StartZeit < varArBis), StartZeit, SortOrder.Descending)),
                      ClearCollect(colArchiv, Sort(Filter(RG_Durchfuehrungen, StartZeit >= varArVon && StartZeit < varArBis && RundgangID = varArRg), StartZeit, SortOrder.Descending))
                  );
                  If(CountRows(colArchiv) >= 500, Notify("Sehr viele Rundgänge im Zeitraum – es werden höchstens 500 angezeigt. Bitte den Zeitraum verkleinern.", NotificationType.Warning));
                  Set(varIsLoading, false)
              )
            PressedColor: =Color.White
            PressedFill: =ColorFade(clrPrimaer, -35%)
            RadiusBottomLeft: =8
            RadiusBottomRight: =8
            RadiusTopLeft: =8
            RadiusTopRight: =8
            Size: =16
            Text: ="Suchen"
            Width: =Parent.Width - 520
            X: =496
            Y: =132
      - ddArRg:
          Control: Classic/DropDown@2.3.1
          Properties:
            AccessibleLabel: ="Rundgang"
            BorderColor: =clrRahmen
            BorderThickness: =1
            ChevronBackground: =clrPrimaer
            ChevronFill: =Color.White
            Color: =clrText
            Default: ="Alle Rundgänge"
            Fill: =clrKarte
            Font: =Font.'Segoe UI'
            Height: =52
            Items: |-
              =Ungroup(Table({T: Table({ID: 0, Title: "Alle Rundgänge"})}, {T: colArRg}), T)
            Items.Value: =Title
            PaddingLeft: =12
            Size: =15
            Width: =Parent.Width - 48
            X: =24
            Y: =196
      - btnArNurNio:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =clrPrimaer
            BorderThickness: =1
            Color: =clrPrimaer
            DisabledBorderColor: =clrGesperrtHell
            DisabledColor: =clrGesperrt
            DisabledFill: =clrGesperrtHell
            Fill: =If(varArNurNio, clrPrimaerHell, clrKarte)
            Font: =Font.'Segoe UI'
            Height: =44
            HoverColor: =clrPrimaer
            HoverFill: =clrPrimaerHell
            OnSelect: =Set(varArNurNio, !varArNurNio)
            PressedColor: =clrPrimaer
            PressedFill: =clrPrimaerHell
            RadiusBottomLeft: =8
            RadiusBottomRight: =8
            RadiusTopLeft: =8
            RadiusTopRight: =8
            Size: =14
            Text: =If(varArNurNio, "✓ ", "○ ") & "nur mit Mängeln"
            Width: =(Parent.Width - 64) / 3
            X: =24 + 0 * ((Parent.Width - 64) / 3 + 8)
            Y: =260
      - btnArOffen:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =clrPrimaer
            BorderThickness: =1
            Color: =clrPrimaer
            DisabledBorderColor: =clrGesperrtHell
            DisabledColor: =clrGesperrt
            DisabledFill: =clrGesperrtHell
            Fill: =If(varArOffen, clrPrimaerHell, clrKarte)
            Font: =Font.'Segoe UI'
            Height: =44
            HoverColor: =clrPrimaer
            HoverFill: =clrPrimaerHell
            OnSelect: =Set(varArOffen, !varArOffen)
            PressedColor: =clrPrimaer
            PressedFill: =clrPrimaerHell
            RadiusBottomLeft: =8
            RadiusBottomRight: =8
            RadiusTopLeft: =8
            RadiusTopRight: =8
            Size: =14
            Text: =If(varArOffen, "✓ ", "○ ") & "auch offene"
            Width: =(Parent.Width - 64) / 3
            X: =24 + 1 * ((Parent.Width - 64) / 3 + 8)
            Y: =260
      - btnArTest:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =clrPrimaer
            BorderThickness: =1
            Color: =clrPrimaer
            DisabledBorderColor: =clrGesperrtHell
            DisabledColor: =clrGesperrt
            DisabledFill: =clrGesperrtHell
            Fill: =If(varArTest, clrPrimaerHell, clrKarte)
            Font: =Font.'Segoe UI'
            Height: =44
            HoverColor: =clrPrimaer
            HoverFill: =clrPrimaerHell
            OnSelect: =Set(varArTest, !varArTest)
            PressedColor: =clrPrimaer
            PressedFill: =clrPrimaerHell
            RadiusBottomLeft: =8
            RadiusBottomRight: =8
            RadiusTopLeft: =8
            RadiusTopRight: =8
            Size: =14
            Text: =If(varArTest, "✓ ", "○ ") & "Testläufe"
            Width: =(Parent.Width - 64) / 3
            X: =24 + 2 * ((Parent.Width - 64) / 3 + 8)
            Y: =260
      - lblArAnzahl:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =28
            Size: =13
            Text: =CountRows(Filter(colArchiv As d, (varArTest || !Coalesce(d.TestDatensatz, false)) && (varArOffen || d.Status = stAbgeschlossen) && (!varArNurNio || Coalesce(d.AnzahlNIO, 0) > 0))) & " Rundgänge · " & Text(varArVon, "dd.mm.yyyy") & " bis " & Text(DateAdd(varArBis, -1, TimeUnit.Days), "dd.mm.yyyy")
            Width: =Parent.Width - 48
            X: =24
            Y: =312
      - galArListe:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            AccessibleLabel: ="Vergangene Rundgänge"
            Height: =Parent.Height - 344
            Items: =Filter(colArchiv As d, (varArTest || !Coalesce(d.TestDatensatz, false)) && (varArOffen || d.Status = stAbgeschlossen) && (!varArNurNio || Coalesce(d.AnzahlNIO, 0) > 0))
            ShowScrollbar: =true
            TemplatePadding: =0
            TemplateSize: =104
            Width: =Parent.Width
            X: =0
            Y: =344
          Children:
          - conArKarte:
              Control: GroupContainer@1.5.0
              Variant: ManualLayout
              Properties:
                BorderColor: =If(ThisItem.Status = stAbgeschlossen, clrRahmen, clrWarnung)
                BorderThickness: =1
                Fill: =clrKarte
                Height: =Parent.TemplateHeight - 12
                RadiusBottomLeft: =12
                RadiusBottomRight: =12
                RadiusTopLeft: =12
                RadiusTopRight: =12
                Width: =Parent.TemplateWidth - 48
                X: =24
                Y: =6
              Children:
              - lblArName:
                  Control: Label@2.5.1
                  Properties:
                    Color: =clrText
                    Font: =Font.'Segoe UI'
                    FontWeight: =FontWeight.Semibold
                    Height: =32
                    Size: =16
                    Text: =ThisItem.RundgangName & If(Coalesce(ThisItem.TestDatensatz, false), "  · Test", "")
                    Width: =Parent.Width - 236
                    Wrap: =false
                    X: =20
                    Y: =10
              - lblArInfo:
                  Control: Label@2.5.1
                  Properties:
                    Color: =If(Coalesce(ThisItem.AnzahlNIO, 0) > 0, clrFehler, clrTextGrau)
                    Font: =Font.'Segoe UI'
                    Height: =44
                    Size: =13
                    Text: =fnTagAnzeige(DateValue(ThisItem.TagText)) & Char(10) & Coalesce(ThisItem.PrueferName, "") & "  ·  " & If(ThisItem.Status = stAbgeschlossen, Coalesce(ThisItem.AnzahlNIO, 0) & " n.i.O.", "nicht abgeschlossen")
                    VerticalAlign: =VerticalAlign.Top
                    Width: =Parent.Width - 236
                    X: =20
                    Y: =42
              - btnArPdf:
                  Control: Classic/Button@2.2.0
                  Properties:
                    BorderColor: =clrPrimaer
                    BorderThickness: =1
                    Color: =clrPrimaer
                    DisabledBorderColor: =clrGesperrtHell
                    DisabledColor: =clrGesperrt
                    DisabledFill: =clrGesperrtHell
                    Fill: =clrKarte
                    Font: =Font.'Segoe UI'
                    Height: =40
                    HoverColor: =clrPrimaer
                    HoverFill: =clrPrimaerHell
                    OnSelect: =Launch(ThisItem.ProtokollUrl)
                    PressedColor: =clrPrimaer
                    PressedFill: =clrPrimaerHell
                    RadiusBottomLeft: =8
                    RadiusBottomRight: =8
                    RadiusTopLeft: =8
                    RadiusTopRight: =8
                    Size: =14
                    Text: ="PDF"
                    Visible: =!IsBlank(ThisItem.ProtokollUrl)
                    Width: =80
                    X: =Parent.Width - 196
                    Y: =(Parent.Height - 40) / 2
              - btnArOeffnen:
                  Control: Classic/Button@2.2.0
                  Properties:
                    BorderThickness: =0
                    Color: =Color.White
                    DisabledBorderColor: =clrGesperrtHell
                    DisabledColor: =clrGesperrt
                    DisabledFill: =clrGesperrtHell
                    DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                    Fill: =clrPrimaer
                    Font: =Font.'Segoe UI'
                    Height: =40
                    HoverColor: =Color.White
                    HoverFill: =ColorFade(clrPrimaer, -20%)
                    OnSelect: |-
                      =If(ThisItem.Status <> stAbgeschlossen,
                          Notify("Nicht abgeschlossene Rundgänge setzt du auf der Startseite am jeweiligen Tag fort.", NotificationType.Information),
                          Set(varRgID, ThisItem.RundgangID);
                          Set(varDurchID, ThisItem.ID);
                          Set(varWeiter, false);
                          Set(varAusArchiv, true);
                          Navigate(scrRundgang, ScreenTransition.None)
                      )
                    PressedColor: =Color.White
                    PressedFill: =ColorFade(clrPrimaer, -35%)
                    RadiusBottomLeft: =8
                    RadiusBottomRight: =8
                    RadiusTopLeft: =8
                    RadiusTopRight: =8
                    Size: =14
                    Text: ="Ansehen"
                    Width: =100
                    X: =Parent.Width - 108
                    Y: =(Parent.Height - 40) / 2
      - lblArLeer:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =60
            Size: =15
            Text: ="Keine Rundgänge im gewählten Zeitraum."
            Visible: =IsEmpty(galArListe.AllItems) && !varIsLoading
            Width: =Parent.Width - 48
            X: =24
            Y: =360
      - conArLaden:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            Fill: =RGBA(244, 245, 249, 0.75)
            Height: =Parent.Height
            Visible: =varIsLoading
            Width: =Parent.Width
          Children:
          - lblArLaden:
              Control: Label@2.5.1
              Properties:
                Align: =Align.Center
                Color: =clrPrimaer
                Font: =Font.'Segoe UI'
                FontWeight: =FontWeight.Semibold
                Height: =40
                Size: =18
                Text: ="Bitte warten …"
                Width: =Parent.Width
                X: =0
                Y: =(Parent.Height - 40) / 2
```

**Nachprüfen (E-05):** In `galArListe › conArKarte` müssen `Height` (`Parent.TemplateHeight - 12`) und bei den Knöpfen `Y` Formeln sein, keine Zahlen.

## Schritt 2 – Knopf auf der Startseite

**Wo hin:** **`scrStart`** markieren → Strg+V.

```yaml
- btnStartArchiv:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrPrimaer
      BorderThickness: =1
      Color: =clrPrimaer
      DisabledBorderColor: =clrGesperrtHell
      DisabledColor: =clrGesperrt
      DisabledFill: =clrGesperrtHell
      DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =40
      HoverColor: =clrPrimaer
      HoverFill: =clrPrimaerHell
      OnSelect: =If(!varIsLoading, Navigate(scrArchiv, ScreenTransition.None))
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =8
      RadiusBottomRight: =8
      RadiusTopLeft: =8
      RadiusTopRight: =8
      Size: =15
      Text: ="🗂 Archiv"
      Width: =184
      X: =Parent.Width - 208
      Y: =216
```

## Schritt 3 – drei Properties

### 3.1 · `btnRuZurueck.OnSelect`

**Pfad:** `scrRundgang › conRuKopf › btnRuZurueck` → OnSelect

```
If(varAusArchiv; Navigate(scrArchiv; ScreenTransition.None); Navigate(scrStart; ScreenTransition.None))
```

```diff
-Navigate(scrStart; ScreenTransition.None)
+If(varAusArchiv; Navigate(scrArchiv; ScreenTransition.None); Navigate(scrStart; ScreenTransition.None))
```

**Kurz erklärt:** Wer aus dem Archiv kommt, landet mit „Zurück“ wieder im Archiv.

**Nachprüfen:** endet auf `te(scrArchiv; ScreenTransition.None); Navigate(scrStart; ScreenTransition.None))`

### 3.2 · `scrStart.OnVisible`

**Pfad:** `scrStart` → OnVisible

```
Set(varIsLoading; true);;
Set(varAusArchiv; false);;
If(IsBlank(varHeute) || varHeute <> Today(); Set(varHeute; Today());; Set(varTag; Today()));;
Set(varTagText; Text(varTag; "yyyy-mm-dd"));;
Concurrent(
    ClearCollect(colRundgaenge; Filter(RG_Rundgaenge; Aktiv = true));
    ClearCollect(colPlan; Filter(RG_Plan; Aktiv = true))
);;
Select(btnStartTagLaden)
```

```diff
+Set(varAusArchiv; false);;
```

**Kurz erklärt:** Auf der Startseite gilt man nicht mehr als „aus dem Archiv“.

**Nachprüfen:** endet auf `Select(btnStartTagLaden)`

### 3.3 · `lblStartListeTitel.Width`

**Pfad:** `scrStart › lblStartListeTitel` → Width

```
Parent.Width - 232
```

```diff
-Parent.Width - 48
+Parent.Width - 232
```

**Kurz erklärt:** Macht Platz für den Knopf „Archiv“.

**Nachprüfen:** endet auf `Parent.Width - 232`

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | Startseite → „🗂 Archiv“ | Liste der abgeschlossenen Rundgänge der letzten 3 Monate, neueste zuerst. Testläufe nicht dabei |
| T2 | „Testläufe“ antippen | ZZ-Test-Läufe erscheinen mit „· Test“ |
| T3 | Rundgang wählen, Zeitraum ändern, „Suchen“ | nur dieser Rundgang im Zeitraum |
| T4 | „nur mit Mängeln“ | nur Läufe mit n.i.O. (rote Zeile) |
| T5 | „Ansehen“ | Rundgangsübersicht, Kategorien nur zum Lesen, „Protokoll“ geht. „Zurück“ → wieder im Archiv |
| T6 | „PDF“ (wenn vorhanden) | archiviertes PDF öffnet sich |
| T7 | „auch offene“ → offenen Lauf „Ansehen“ | Hinweis „… auf der Startseite fortsetzen“ |

## Rückweg

`scrArchiv` und `btnStartArchiv` löschen, die drei Vorher-Fassungen einsetzen.

## Anhang – Vorher-Fassungen

**`btnRuZurueck.OnSelect` vorher**

```
Navigate(scrStart; ScreenTransition.None)
```

**`scrStart.OnVisible` vorher**

```
Set(varIsLoading; true);;
If(IsBlank(varHeute) || varHeute <> Today(); Set(varHeute; Today());; Set(varTag; Today()));;
Set(varTagText; Text(varTag; "yyyy-mm-dd"));;
Concurrent(
    ClearCollect(colRundgaenge; Filter(RG_Rundgaenge; Aktiv = true));
    ClearCollect(colPlan; Filter(RG_Plan; Aktiv = true))
);;
Select(btnStartTagLaden)
```

**`lblStartListeTitel.Width` vorher**

```
Parent.Width - 48
```

