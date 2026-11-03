# Paket 14+15 – Builder: Verlauf und Vergleich bei Zahlen

Stand 03.11.2026. Erzeugt mit `werkzeuge/builder.py` und `werkzeuge/doc_paket14_15.py`. **Voraussetzung: Builder-Pakete 8, 9, 12+16 eingefügt.**

## Kurzfassung

- **Paket 14 – Abweichung zum letzten Rundgang:** Bei einer Zahl lässt sich im Builder einstellen, wie stark sie vom letzten abgeschlossenen Rundgang abweichen darf (absolut oder in %), und/oder „Zählerstand: darf nicht kleiner werden“. Die Karte zeigt „zuletzt 7,6 (26.10.)“. Weicht der Wert stärker ab, wird die Zeile orange und eine **Begründung ist Pflicht**. Kein Mangel. Der erste Rundgang hat keinen Vergleich. Testläufe vergleichen nur mit Testläufen.
- **Paket 15 – zwei Werte vergleichen:** Eine Zahl kann mit einer anderen Zahl derselben Kategorie verglichen werden (z. B. zwei gleiche Geräte) mit erlaubtem Unterschied (0 = gleich). Weichen sie stärker ab, ist ebenfalls eine Begründung Pflicht.
- Protokoll: „(starke Abweichung zum letzten Mal, zuletzt 7,6, begründet)“ bzw. „(weicht von „…“ ab (7,2), begründet)“.
- Nach einer neuen Fassung findet die App den alten Wert über `QuelleID` (eine Fassung zurück). Lagen zwei Aktivierungen zwischen zwei Rundgängen, fehlt der Vergleich einmal.
- Im Prüfpunkt-Editor bei Zahlen ein Knopf **„Verlauf/Vergleich ›“** neben „Wert außerhalb der Grenzen ergibt“. Er öffnet ein Fenster: höchste Abweichung (absolut/%), „Zählerstand: darf nicht kleiner werden“, Vergleichs-Prüfpunkt (nur Zahlen derselben Kategorie) und erlaubter Unterschied.
- Kopie und neue Fassung schreiben den Vergleichs-Verweis auf die neue Frage um (wie bei Bedingungen). Entfernen/Verschieben löst ihn.
- Umfang: 5 Spalten (dieselben wie in der Rundgang-App), 2 neue Blöcke, 11 geänderte Properties. Generator 0 Fehler, Mutation 13/13. **Nicht in Studio getestet. Nicht unabhängig geprüft.**

## Schritt 0 – SharePoint

Die fünf Spalten aus `PAKET_14_15_APP.md`, Schritt 1 (nur einmal anlegen). Im Builder: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**.

## Schritt 1 – neue Steuerelemente

### 1a · Knopf „Verlauf/Vergleich“

**Wo hin:** **`conPZahl`** (`scrEditor › conEdMitte › conEdP › conPZahl`) markieren → Strg+V.

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
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =26
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
      Text: |-
        =If(!IsBlank(LookUp(colP, ID = varAuswahlID).AbwMax) || Coalesce(LookUp(colP, ID = varAuswahlID).NurSteigend, false) || Coalesce(LookUp(colP, ID = varAuswahlID).VergleichPunkt, 0) <> 0, "Verlauf/Vergleich: an  ›", "Verlauf/Vergleich  ›")
      Width: =212
      X: =316
      Y: =56
```

**Rot bis 1b:** `txtZaAbwMax`, `txtZaTol`, `ddZaVgl`, `varZaOffen` (bis Schritt 2).

### 1b · Fenster „Verlauf und Vergleich“

**Wo hin:** **`scrEditor`** markieren → Strg+V (liegt dann über allem; `conEdLaden` danach wieder ganz nach oben schieben: `conEdLaden` markieren → ⋯ → Neu anordnen → Ganz nach vorne).

```yaml
- conZa:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      BorderThickness: =0
      Fill: =RGBA(0, 0, 0, 0.45)
      Height: =Parent.Height
      Visible: =varZaOffen
      Width: =Parent.Width
    Children:
      - btnZaSperre:
          Control: Classic/Button@2.2.0
          Properties:
            BorderThickness: =0
            Color: =Color.White
            DisabledBorderColor: =clrGesperrtHell
            DisabledColor: =clrGesperrt
            DisabledFill: =RGBA(0, 0, 0, 0)
            DisplayMode: =DisplayMode.Edit
            Fill: =RGBA(0, 0, 0, 0)
            Font: =Font.'Segoe UI'
            Height: =Parent.Height
            HoverColor: =Color.White
            HoverFill: =RGBA(0, 0, 0, 0)
            OnSelect: =false
            PressedColor: =Color.White
            PressedFill: =RGBA(0, 0, 0, 0)
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: =14
            Text: =""
            Width: =Parent.Width
            X: =0
            Y: =0
      - conZaKarte:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrKarte
            Height: =560
            RadiusBottomLeft: =12
            RadiusBottomRight: =12
            RadiusTopLeft: =12
            RadiusTopRight: =12
            Width: =620
            X: =(Parent.Width - Self.Width) / 2
            Y: =(Parent.Height - Self.Height) / 2
          Children:
            - lblZaTitel:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =40
                  Size: =18
                  Text: ="Verlauf und Vergleich"
                  Width: =572
                  X: =24
                  Y: =16
            - lblZaFrage:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =28
                  Size: =14
                  Text: =LookUp(colP, ID = varAuswahlID).Title
                  Width: =572
                  X: =24
                  Y: =56
            - lblZaAbw:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =24
                  Size: =13
                  Text: ="Abweichung zum letzten Rundgang"
                  Width: =572
                  X: =24
                  Y: =92
            - lblZaAbwMax:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="höchstens (leer = aus)"
                  Width: =200
                  X: =24
                  Y: =120
            - txtZaAbwMax:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Höchste Abweichung zum letzten Rundgang"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =If(IsBlank(LookUp(colP, ID = varAuswahlID).AbwMax), "", Text(LookUp(colP, ID = varAuswahlID).AbwMax))
                  DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Format: =TextFormat.Number
                  Height: =36
                  HintText: ="z. B. 0,5"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =With({v: If(Trim(Self.Text) = "", Blank(), IfError(Value(Self.Text), Blank()))},
                        If(Trim(Self.Text) <> "" && IsBlank(v),
                            Notify("Bitte eine Zahl eingeben.", NotificationType.Warning);
                            Reset(txtZaAbwMax),
                            Text(v) <> Text(LookUp(colP, ID = varAuswahlID).AbwMax),
                            If(varSchreibbar && varAuswahlEbene = 3,
                                Refresh(RG_Rundgaenge);
                                Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                                If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                                If(varEntwurfOk,
                                    Set(varPatchFehler, false);
                                    IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {AbwMax: v}), Set(varPatchFehler, true));
                                    If(varPatchFehler,
                                        Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                        Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                                        Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                                    )
                                )
                            )
                        )
                    )
                  Size: =14
                  Width: =160
                  X: =24
                  Y: =140
            - galZaArt:
                Control: Gallery@2.15.0
                Variant: Vertical
                Properties:
                  AccessibleLabel: ="Abweichung absolut oder in Prozent"
                  Height: =36
                  Items: |-
                    =Table({W: "abs", N: "absolut"}, {W: "proz", N: "in %"})
                  ShowScrollbar: =false
                  TemplatePadding: =0
                  TemplateSize: =36
                  Width: =240
                  WrapCount: =2
                  X: =196
                  Y: =140
                Children:
                  - btnZaArt:
                      Control: Classic/Button@2.2.0
                      Properties:
                        BorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false), "proz", "abs"), clrPrimaer, clrRahmen)
                        BorderThickness: =1
                        Color: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false), "proz", "abs"), Color.White, clrText)
                        DisabledBorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false), "proz", "abs"), clrPrimaer, clrRahmen)
                        DisabledColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false), "proz", "abs"), clrPrimaer, clrTextGrau)
                        DisabledFill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false), "proz", "abs"), clrPrimaerHell, clrKarte)
                        DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.Disabled)
                        Fill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false), "proz", "abs"), clrPrimaer, clrKarte)
                        Font: =Font.'Segoe UI'
                        Height: =32
                        HoverColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false), "proz", "abs"), Color.White, clrText)
                        HoverFill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false), "proz", "abs"), ColorFade(clrPrimaer, -20%), clrPrimaerHell)
                        OnSelect: |-
                          =If((ThisItem.W = "proz") <> Coalesce(LookUp(colP, ID = varAuswahlID).AbwProzent, false),
                              If(varSchreibbar && varAuswahlEbene = 3,
                                  Refresh(RG_Rundgaenge);
                                  Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                                  If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                                  If(varEntwurfOk,
                                      Set(varPatchFehler, false);
                                      IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {AbwProzent: ThisItem.W = "proz"}), Set(varPatchFehler, true));
                                      If(varPatchFehler,
                                          Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                          Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                                          Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                                      )
                                  )
                              )
                          )
                        PressedColor: =Color.White
                        PressedFill: =ColorFade(clrPrimaer, -35%)
                        RadiusBottomLeft: =6
                        RadiusBottomRight: =6
                        RadiusTopLeft: =6
                        RadiusTopRight: =6
                        Size: =13
                        Text: =ThisItem.N
                        Width: =Parent.TemplateWidth - 6
                        X: =0
                        Y: =0
            - btnZaSteigend:
                Control: Classic/Button@2.2.0
                Properties:
                  Align: =Align.Left
                  BorderColor: =clrPrimaer
                  BorderThickness: =1
                  Color: =clrPrimaer
                  DisabledBorderColor: =clrGesperrtHell
                  DisabledColor: =clrGesperrt
                  DisabledFill: =clrGesperrtHell
                  DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.Disabled)
                  Fill: =clrKarte
                  Font: =Font.'Segoe UI'
                  Height: =36
                  HoverColor: =clrPrimaer
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
                                IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {NurSteigend: !Coalesce(LookUp(colP, ID = varAuswahlID).NurSteigend, false)}), Set(varPatchFehler, true));
                                If(varPatchFehler,
                                    Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                    Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                                    Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                                )
                            )
                        )
                    )
                  PaddingLeft: =12
                  PressedColor: =clrPrimaer
                  PressedFill: =clrPrimaerHell
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =13
                  Text: |-
                    =If(Coalesce(LookUp(colP, ID = varAuswahlID).NurSteigend, false), "✓ ", "○ ") & "Zählerstand: darf nicht kleiner werden"
                  Width: =420
                  X: =24
                  Y: =188
            - lblZaVgl:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =24
                  Size: =13
                  Text: ="Mit anderem Prüfpunkt vergleichen (gleiche Kategorie)"
                  Width: =572
                  X: =24
                  Y: =244
            - ddZaVgl:
                Control: Classic/DropDown@2.3.1
                Properties:
                  AccessibleLabel: ="Vergleichs-Prüfpunkt"
                  BorderColor: =clrRahmen
                  BorderThickness: =1
                  ChevronBackground: =clrPrimaer
                  ChevronFill: =Color.White
                  ChevronHoverBackground: =ColorFade(clrPrimaer, -20%)
                  ChevronHoverFill: =Color.White
                  Color: =clrText
                  Default: |-
                    =If(Coalesce(LookUp(colP, ID = varAuswahlID).VergleichPunkt, 0) = 0, "— kein Vergleich —", With({a: LookUp(colP, ID = LookUp(colP, ID = varAuswahlID).VergleichPunkt)}, a.Title & If(CountRows(Filter(colP As x, x.KategorieID = a.KategorieID && x.Title = a.Title)) > 1, " (#" & a.ID & ")", "")))
                  DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
                  Fill: =clrKarte
                  Font: =Font.'Segoe UI'
                  Height: =36
                  HoverFill: =clrPrimaerHell
                  Items: |-
                    =Ungroup(Table({T: Table({ID: 0, N: "— kein Vergleich —"})}, {T: ForAll(Sort(Filter(colP As a, a.KategorieID = LookUp(colP, ID = varAuswahlID).KategorieID && a.ID <> varAuswahlID && a.Eingabetyp.Value = "ZAHL"), RgReihenfolge * 1000000 + ID) As a, {ID: a.ID, N: a.Title & If(CountRows(Filter(colP As x, x.KategorieID = a.KategorieID && x.Title = a.Title)) > 1, " (#" & a.ID & ")", "")})}), T)
                  Items.Value: =N
                  OnChange: |-
                    =If(!IsBlank(Self.Selected) && Self.Selected.ID <> Coalesce(LookUp(colP, ID = varAuswahlID).VergleichPunkt, 0),
                        If(varSchreibbar && varAuswahlEbene = 3,
                            Refresh(RG_Rundgaenge);
                            Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                            If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                            If(varEntwurfOk,
                                Set(varPatchFehler, false);
                                IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {VergleichPunkt: Self.Selected.ID}), Set(varPatchFehler, true));
                                If(varPatchFehler,
                                    Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                    Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                                    Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                                )
                            )
                        )
                    )
                  PaddingLeft: =10
                  PressedColor: =Color.White
                  PressedFill: =clrPrimaer
                  SelectionColor: =Color.White
                  SelectionFill: =clrPrimaer
                  Size: =14
                  Width: =572
                  X: =24
                  Y: =272
            - lblZaTol:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="erlaubter Unterschied (0 = gleich)"
                  Width: =300
                  X: =24
                  Y: =316
            - txtZaTol:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Erlaubter Unterschied"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =If(IsBlank(LookUp(colP, ID = varAuswahlID).VergleichTol), "", Text(LookUp(colP, ID = varAuswahlID).VergleichTol))
                  DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Format: =TextFormat.Number
                  Height: =36
                  HintText: ="z. B. 0,2"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =With({v: If(Trim(Self.Text) = "", Blank(), IfError(Value(Self.Text), Blank()))},
                        If(Trim(Self.Text) <> "" && IsBlank(v),
                            Notify("Bitte eine Zahl eingeben.", NotificationType.Warning);
                            Reset(txtZaTol),
                            Text(v) <> Text(LookUp(colP, ID = varAuswahlID).VergleichTol),
                            If(varSchreibbar && varAuswahlEbene = 3,
                                Refresh(RG_Rundgaenge);
                                Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                                If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                                If(varEntwurfOk,
                                    Set(varPatchFehler, false);
                                    IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {VergleichTol: v}), Set(varPatchFehler, true));
                                    If(varPatchFehler,
                                        Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                        Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                                        Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                                    )
                                )
                            )
                        )
                    )
                  Size: =14
                  Width: =160
                  X: =24
                  Y: =336
            - lblZaHinweis:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =88
                  Size: =12
                  Text: ="Weicht ein Wert ab, muss der Prüfer begründen (Kommentar). Es entsteht kein Mangel. Der Vergleich mit dem letzten Rundgang beginnt ab dem zweiten Rundgang."
                  VerticalAlign: =VerticalAlign.Top
                  Width: =572
                  X: =24
                  Y: =396
            - btnZaFertig:
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
                  Height: =44
                  HoverColor: =Color.White
                  HoverFill: =ColorFade(clrPrimaer, -20%)
                  OnSelect: =Set(varZaOffen, false)
                  PressedColor: =Color.White
                  PressedFill: =ColorFade(clrPrimaer, -35%)
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =14
                  Text: ="Fertig"
                  Width: =160
                  X: =436
                  Y: =496
            - btnZaZu:
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
                  OnSelect: =Set(varZaOffen, false)
                  PressedColor: =clrPrimaer
                  PressedFill: =clrPrimaerHell
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =16
                  Text: ="✕"
                  Width: =40
                  X: =560
                  Y: =16
```

## Schritt 2 – Start und kleine Werte

### 2.1 · `App.OnStart`

**Pfad:** `App` → OnStart

```
Set(varIsLoading; false);;
Set(varLadeText; "");;
Set(varSperreBis; Now());;
Set(varPatchFehler; false);;
Set(varJob; "");;
Set(varNach; "");;
Set(varKopieNach; "");;
Set(varArbeitStart; false);;
Set(varRgID; 0);;
Set(varRg; Defaults(RG_Rundgaenge));;
Set(varFassung; 0);;
Set(varSchreibbar; false);;
Set(varIstVorlage; false);;
Set(varAuswahlEbene; 0);;
Set(varAuswahlID; 0);;
Set(varCtxB; 0);;
Set(varCtxK; 0);;
Set(varFrage; "");;
Set(varGespeichertText; "");;
Set(varAlleZeigen; false);;
Set(varNeuOffen; false);;
Set(varNeuLeer; true);;
Set(varNeuRg; Defaults(RG_Rundgaenge));;
Set(varNeuID; 0);;
Set(varHolenOffen; false);;
Set(varHolenEbene; 0);;
Set(varHolenID; 0);;
Set(varMehrereOffen; false);;
Set(varMehrTyp; "IONIO");;
Set(varMehrPflicht; true);;
Set(varBildOffen; false);;
Set(varAktivOffen; false);;
Set(varZielR; 0);;
Set(varZielF; 0);;
Set(varZielB; 0);;
Set(varZielK; 0);;
Set(varZielBAktiv; false);;
Set(varKopieBehalteR; false);;
Set(varKopieZusatz; "");;
Set(varKopieFehler; 0);;
Set(varQuelleR; 0);;
Set(varQuelleF; 0);;
Set(varQuelleNurAktiv; false);;
Set(varHeuteLaeuft; false);;
Set(varPlanRgID; 0);;
Set(varPlanRg; Defaults(RG_Rundgaenge));;
Set(varEntwurfOk; true);;
Set(varAktivRest; false);;
Set(varVorlageNeu; Defaults(RG_Rundgaenge));;
Set(varNioOffen; false);;
Set(varKoID; 0);;
Set(varZaOffen; false)
```

```diff
-Set(varKoID; 0)
+Set(varKoID; 0);;
+Set(varZaOffen; false)
```

**Kurz erklärt:** Neuer Startwert `varZaOffen` (Fenster „Verlauf und Vergleich“).

**Nachprüfen:** endet auf `Set(varZaOffen; false)`

### 2.2 · `scrEditor.OnVisible`

**Pfad:** `scrEditor` → OnVisible

```
Set(varAktivOffen; false);;
Set(varHolenOffen; false);;
Set(varMehrereOffen; false);;
Set(varBildOffen; false);;
Set(varZaOffen; false);;
If(varJob <> ""; Set(varIsLoading; true);; Set(varArbeitStart; true))
```

```diff
+Set(varZaOffen; false);;
```

**Kurz erklärt:** Schließt das neue Fenster beim Öffnen des Editors.

**Nachprüfen:** endet auf `If(varJob <> ""; Set(varIsLoading; true);; Set(varArbeitStart; true))`

### 2.3 · `lblPGrenz.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPZahl › lblPGrenz` → Width

```
300
```

```diff
-528
+300
```

**Kurz erklärt:** Macht Platz für den neuen Knopf „Verlauf/Vergleich“.

**Nachprüfen:** endet auf `300`

### 2.4 · `lblVsRegeln.Text`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › lblVsRegeln` → Text

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NichtMessbar; false); Char(10) & "• „nicht messbar“ erlaubt (dann Begründung Pflicht)"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && !IsBlank(LookUp(colP; ID = varAuswahlID).AbwMax); Char(10) & "• höchstens " & Text(LookUp(colP; ID = varAuswahlID).AbwMax) & If(Coalesce(LookUp(colP; ID = varAuswahlID).AbwProzent; false); " %"; "") & " Abweichung zum letzten Rundgang"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NurSteigend; false); Char(10) & "• Zählerstand: darf nicht kleiner werden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).VergleichPunkt; 0) <> 0; Char(10) & "• Vergleich mit „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).VergleichPunkt).Title & "“ (± " & Text(Coalesce(LookUp(colP; ID = varAuswahlID).VergleichTol; 0)) & ")"; "")
```

```diff
-"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglic …
+"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglic …
```

**Kurz erklärt:** Vorschau nennt Abweichung, Zähler und Vergleich.

**Nachprüfen:** endet auf `± " & Text(Coalesce(LookUp(colP; ID = varAuswahlID).VergleichTol; 0)) & ")"; "")`

## Schritt 3 – Neue Prüfpunkte und Verschieben

### 3.1 · `btnGlNeuP.OnSelect`

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
        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0) + 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: "IONIO"}; Pflicht: true; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: If(varAuswahlEbene = 3 && LookUp(colP; ID = varAuswahlID).KategorieID = varCtxK; Coalesce(LookUp(colP; ID = varAuswahlID).Abschnitt; ""); ""); TextIO: ""; TextNIO: ""; NichtMessbar: false; AbwProzent: false; NurSteigend: false; VergleichPunkt: 0; VergleichTol: 0}).ID; 0));;
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
```

**Kurz erklärt:** Neuer Prüfpunkt mit leeren Vergleichsfeldern.

**Nachprüfen:** endet auf `)`

### 3.2 · `btnMehrAnlegen.OnSelect`

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
                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: varMehrTyp}; Pflicht: varMehrPflicht; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: Left(Trim(txtMehrAbschnitt.Text); 255); TextIO: ""; TextNIO: ""; NichtMessbar: false; AbwProzent: false; NurSteigend: false; VergleichPunkt: 0; VergleichTol: 0}).ID; 0)}
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

**Kurz erklärt:** Wie btnGlNeuP.

**Nachprüfen:** endet auf `)`

### 3.3 · `ddPKategorie.OnChange`

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
        ForAll(Filter(colP; VergleichPunkt = varAuswahlID) As d2; Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = d2.ID && RundgangID = varRgID && Fassung = varFassung); {VergleichPunkt: 0}));;
        IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {KategorieID: ziel; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = ziel); RgReihenfolge); 0) + 10; BedingungPunkt: 0; BedingungWert: ""; VergleichPunkt: 0}); Set(varPatchFehler; true));;
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
-        IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {KategorieID: ziel; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = ziel); RgReihenfolge); 0) + 10;  …
+        ForAll(Filter(colP; VergleichPunkt = varAuswahlID) As d2; Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = d2.ID && RundgangID = varRgID && Fassung = varFassung); {VergleichPunkt: 0}));;
+        IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {KategorieID: ziel; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = ziel); RgReihenfolge); 0) + 10;  …
```

**Kurz erklärt:** Beim Verschieben in eine andere Kategorie entfällt der Vergleich (er gilt nur innerhalb einer Kategorie).

**Nachprüfen:** endet auf `)`

## Schritt 4 – Listen

### 4.1 · `galAkt.Items`

**Pfad:** `scrEditor › conAkt › conAktKarte › galAkt` → Items

```
Ungroup(
    Table(
        {T: ForAll(Filter(colP As p; IsBlank(LookUp(colAltP As a; a.ID = p.QuelleID))) As p; {Art: "neu"; Text: p.Title})};
        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) || Coalesce(p.Auswahlwerte; "") <> Coalesce(a.Auswahlwerte; "") || Coalesce(p.Einheit; "") <> Coalesce(a.Einheit; "") || Coalesce(p.MinWert; -999999) <> Coalesce(a.MinWert; -999999) || Coalesce(p.MaxWert; -999999) <> Coalesce(a.MaxWert; -999999) || Coalesce(p.Hinweis; "") <> Coalesce(a.Hinweis; "") || fnFotoWert(p.Foto.Value; Coalesce(p.FotoMoeglich; false)) <> fnFotoWert(a.Foto.Value; Coalesce(a.FotoMoeglich; false)) || Coalesce(p.KommentarPflicht; false) <> Coalesce(a.KommentarPflicht; false) || fnGrenzmodus(p.Grenzmodus.Value) <> fnGrenzmodus(a.Grenzmodus.Value) || Coalesce(p.BedingungWert; "") <> Coalesce(a.BedingungWert; "") || Coalesce(LookUp(colP As b0; b0.ID = p.BedingungPunkt).QuelleID; 0) <> Coalesce(a.BedingungPunkt; 0) || Coalesce(p.HinweisBildID; 0) <> Coalesce(a.HinweisBildID; 0) || Coalesce(LookUp(colK As k0; k0.ID = p.KategorieID).QuelleID; 0) <> a.KategorieID || Trim(Coalesce(p.Abschnitt; "")) <> Trim(Coalesce(a.Abschnitt; "")) || Coalesce(p.Kritisch; false) <> Coalesce(a.Kritisch; false) || Coalesce(p.KritischText; "") <> Coalesce(a.KritischText; "") || Coalesce(p.Ansprechpartner; "") <> Coalesce(a.Ansprechpartner; "") || Coalesce(p.Rueckfrage; false) <> Coalesce(a.Rueckfrage; false) || Coalesce(p.RueckfrageText; "") <> Coalesce(a.RueckfrageText; "") || Coalesce(p.TextIO; "") <> Coalesce(a.TextIO; "") || Coalesce(p.TextNIO; "") <> Coalesce(a.TextNIO; "") || Coalesce(p.NichtMessbar; false) <> Coalesce(a.NichtMessbar; false) || Coalesce(p.AbwMax; -999999) <> Coalesce(a.AbwMax; -999999) || Coalesce(p.AbwProzent; false) <> Coalesce(a.AbwProzent; false) || Coalesce(p.NurSteigend; false) <> Coalesce(a.NurSteigend; false) || Coalesce(p.VergleichTol; 0) <> Coalesce(a.VergleichTol; 0) || Coalesce(LookUp(colP As v0; v0.ID = p.VergleichPunkt).QuelleID; 0) <> Coalesce(a.VergleichPunkt; 0)))) As p; {Art: "geändert"; Text: p.Title})};
        {T: ForAll(Filter(colAltP As a; IsBlank(LookUp(colP As p; p.QuelleID = a.ID))) As a; {Art: "entfernt"; Text: a.Title})}
    );
    T
)
```

```diff
-        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coales …
+        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coales …
```

**Kurz erklärt:** Änderungen an den neuen Feldern zählen als „geändert“ (Vergleichspunkt über QuelleID).

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
        ForAll(Filter(colP; VergleichPunkt = varAuswahlID) As d2; Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = d2.ID && RundgangID = varRgID && Fassung = varFassung); {VergleichPunkt: 0}));;
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
+        ForAll(Filter(colP; VergleichPunkt = varAuswahlID) As d2; Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = d2.ID && RundgangID = varRgID && Fassung = varFassung); {VergleichPunkt: 0}));;
```

**Kurz erklärt:** Wird ein Prüfpunkt entfernt, verlieren Prüfpunkte, die mit ihm verglichen werden, den Verweis.

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
            {T: ForAll(Filter(colP As p; Coalesce(p.VergleichPunkt; 0) <> 0 && With({w: LookUp(colP As w0; w0.ID = p.VergleichPunkt)}; IsBlank(w) || w.ID = p.ID || w.KategorieID <> p.KategorieID || w.Eingabetyp.Value <> "ZAHL" || p.Eingabetyp.Value <> "ZAHL")) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Der Vergleich zeigt auf keine Zahl-Frage derselben Kategorie."})};
            {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend; false))) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Verlauf/Vergleich wirkt nur bei Zahlen."})};
            {T: ForAll(Filter(colP As p; !IsBlank(p.AbwMax) && p.AbwMax < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: höchste Abweichung darf nicht negativ sein."})};
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
+            {T: ForAll(Filter(colP As p; Coalesce(p.VergleichPunkt; 0) <> 0 && With({w: LookUp(colP As w0; w0.ID = p.VergleichPunkt)}; IsBlank(w) || w.ID = p.ID || w.KategorieID <> p.KategorieID || w.Eingabetyp.Value <> "ZAHL" || p.Eing …
+            {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend; false))) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.Katego …
+            {T: ForAll(Filter(colP As p; !IsBlank(p.AbwMax) && p.AbwMax < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: höchste A …
```

**Kurz erklärt:** Fehler, wenn der Vergleich auf keine Zahl derselben Kategorie zeigt oder die Abweichung negativ ist. Hinweis bei anderem Typ.

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
                        {Alt: q.ID; BedAlt: Coalesce(q.BedingungPunkt; 0); BedWert: Coalesce(q.BedingungWert; ""); VglAlt: Coalesce(q.VergleichPunkt; 0); Ziel: ziel;
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQK) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colP; KategorieID = varZielK); RgReihenfolge); 0) + i.Value * 10); Aktiv: true; QuelleID: q.ID; Eingabetyp: {Value: Coalesce(q.Eingabetyp.Value; "IONIO")}; Pflicht: Coalesce(q.Pflicht; false); Auswahlwerte: q.Auswahlwerte; Einheit: q.Einheit; MinWert: q.MinWert; MaxWert: q.MaxWert; Hinweis: q.Hinweis; FotoMoeglich: Coalesce(q.FotoMoeglich; false); Foto: {Value: fnFotoWert(q.Foto.Value; Coalesce(q.FotoMoeglich; false))}; KommentarPflicht: Coalesce(q.KommentarPflicht; false); Grenzmodus: {Value: fnGrenzmodus(q.Grenzmodus.Value)}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: Coalesce(q.HinweisBildID; 0); Abschnitt: Coalesce(q.Abschnitt; ""); Kritisch: Coalesce(q.Kritisch; false); KritischText: Coalesce(q.KritischText; ""); Ansprechpartner: Coalesce(q.Ansprechpartner; ""); Rueckfrage: Coalesce(q.Rueckfrage; false); RueckfrageText: Coalesce(q.RueckfrageText; ""); TextIO: Coalesce(q.TextIO; ""); TextNIO: Coalesce(q.TextNIO; ""); NichtMessbar: Coalesce(q.NichtMessbar; false); AbwMax: q.AbwMax; AbwProzent: Coalesce(q.AbwProzent; false); NurSteigend: Coalesce(q.NurSteigend; false); VergleichPunkt: 0; VergleichTol: q.VergleichTol}).ID; 0))}
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
    ClearCollect(colVglErg;
        ForAll(Filter(colMapP; VglAlt <> 0 && Neu <> 0) As m;
            With({a: LookUp(colMapP As m2; m2.Alt = m.VglAlt)};
                With({neuA: If(!IsBlank(a) && a.Ziel = m.Ziel; a.Neu; IsBlank(a) && LookUp(colP As p0; p0.ID = m.VglAlt).KategorieID = m.Ziel; m.VglAlt; 0)};
                    {Ok: If(neuA = 0; true; !IsError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = m.Neu); {VergleichPunkt: neuA})))}
                )
            )
        )
    );;
    Set(varKopieFehler; CountRows(Filter(colMapB; Neu = 0)) + CountRows(Filter(colMapK; Neu = 0)) + CountRows(Filter(colMapP; Neu = 0)) + CountRows(Filter(colBedErg; !Ok)) + CountRows(Filter(colVglErg; !Ok)));;
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
-                        {Alt: q.ID; BedAlt: Coalesce(q.BedingungPunkt; 0); BedWert: Coalesce(q.BedingungWert; ""); Ziel: ziel;
-                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgRei …
+                        {Alt: q.ID; BedAlt: Coalesce(q.BedingungPunkt; 0); BedWert: Coalesce(q.BedingungWert; ""); VglAlt: Coalesce(q.VergleichPunkt; 0); Ziel: ziel;
+                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgRei …
-    Set(varKopieFehler; CountRows(Filter(colMapB; Neu = 0)) + CountRows(Filter(colMapK; Neu = 0)) + CountRows(Filter(colMapP; Neu = 0)) + CountRows(Filter(colBedErg; !Ok)));;
+    ClearCollect(colVglErg;
+        ForAll(Filter(colMapP; VglAlt <> 0 && Neu <> 0) As m;
+            With({a: LookUp(colMapP As m2; m2.Alt = m.VglAlt)};
+                With({neuA: If(!IsBlank(a) && a.Ziel = m.Ziel; a.Neu; IsBlank(a) && LookUp(colP As p0; p0.ID = m.VglAlt).KategorieID = m.Ziel; m.VglAlt; 0)};
+                    {Ok: If(neuA = 0; true; !IsError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = m.Neu); {VergleichPunkt: neuA})))}
+                )
+            )
+        )
+    );;
+    Set(varKopieFehler; CountRows(Filter(colMapB; Neu = 0)) + CountRows(Filter(colMapK; Neu = 0)) + CountRows(Filter(colMapP; Neu = 0)) + CountRows(Filter(colBedErg; !Ok)) + CountRows(Filter(colVglErg; !Ok)));;
```

**Kurz erklärt:** Kopie/neue Fassung übernehmen die fünf Felder. Der Vergleichs-Verweis wird wie die Bedingung auf die neue Frage umgeschrieben.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

## Test

1. Zahl-Prüfpunkt → „Verlauf/Vergleich ›“ → höchstens 0,5, absolut → Vorschau „höchstens 0,5 Abweichung …“, Knopf „Verlauf/Vergleich: an“.
2. Zweiten Zahl-Prüfpunkt derselben Kategorie als Vergleich wählen, Unterschied 0,2 → Vorschau nennt ihn.
3. Neue Fassung anlegen → im Entwurf zeigt der Vergleich auf die **neue** Frage (Vorschau-Titel gleich, Prüfung ohne Fehler).
4. Den Vergleichs-Partner entfernen → Vergleich ist weg, keine Fehlermeldung.

## Rückweg

Vorher-Fassungen im Anhang einsetzen, dann `btnPZahlMehr` und `conZa` löschen.

## Anhang – Vorher-Fassungen (Stand nach Paket 12+16)

**`App.OnStart` vorher**

```
Set(varIsLoading; false);;
Set(varLadeText; "");;
Set(varSperreBis; Now());;
Set(varPatchFehler; false);;
Set(varJob; "");;
Set(varNach; "");;
Set(varKopieNach; "");;
Set(varArbeitStart; false);;
Set(varRgID; 0);;
Set(varRg; Defaults(RG_Rundgaenge));;
Set(varFassung; 0);;
Set(varSchreibbar; false);;
Set(varIstVorlage; false);;
Set(varAuswahlEbene; 0);;
Set(varAuswahlID; 0);;
Set(varCtxB; 0);;
Set(varCtxK; 0);;
Set(varFrage; "");;
Set(varGespeichertText; "");;
Set(varAlleZeigen; false);;
Set(varNeuOffen; false);;
Set(varNeuLeer; true);;
Set(varNeuRg; Defaults(RG_Rundgaenge));;
Set(varNeuID; 0);;
Set(varHolenOffen; false);;
Set(varHolenEbene; 0);;
Set(varHolenID; 0);;
Set(varMehrereOffen; false);;
Set(varMehrTyp; "IONIO");;
Set(varMehrPflicht; true);;
Set(varBildOffen; false);;
Set(varAktivOffen; false);;
Set(varZielR; 0);;
Set(varZielF; 0);;
Set(varZielB; 0);;
Set(varZielK; 0);;
Set(varZielBAktiv; false);;
Set(varKopieBehalteR; false);;
Set(varKopieZusatz; "");;
Set(varKopieFehler; 0);;
Set(varQuelleR; 0);;
Set(varQuelleF; 0);;
Set(varQuelleNurAktiv; false);;
Set(varHeuteLaeuft; false);;
Set(varPlanRgID; 0);;
Set(varPlanRg; Defaults(RG_Rundgaenge));;
Set(varEntwurfOk; true);;
Set(varAktivRest; false);;
Set(varVorlageNeu; Defaults(RG_Rundgaenge));;
Set(varNioOffen; false);;
Set(varKoID; 0)
```

**`scrEditor.OnVisible` vorher**

```
Set(varAktivOffen; false);;
Set(varHolenOffen; false);;
Set(varMehrereOffen; false);;
Set(varBildOffen; false);;
If(varJob <> ""; Set(varIsLoading; true);; Set(varArbeitStart; true))
```

**`lblPGrenz.Width` vorher**

```
528
```

**`lblVsRegeln.Text` vorher**

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NichtMessbar; false); Char(10) & "• „nicht messbar“ erlaubt (dann Begründung Pflicht)"; "")
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
        Reset(txtPAbschnitt);;
        Reset(txtPTextIO);;
        Reset(txtPTextNIO)
    ))
)
```

**`galAkt.Items` vorher**

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

