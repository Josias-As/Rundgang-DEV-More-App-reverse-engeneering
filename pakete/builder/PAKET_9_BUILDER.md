# Paket 9 – Kritischer Mangel, Rückfrage, Ansprechpartner (Teil Builder)

Stand 02.11.2026. Erzeugt mit `werkzeuge/builder.py` + `werkzeuge/doc_paket9_builder.py`. **Voraussetzung: Paket 8 (Builder) vollständig eingefügt** (`PAKET_8_BUILDER.md`, Schritt 0–5). Die Formeln hier enthalten die Änderungen von Paket 8 schon.

## Kurzfassung

- Neuer Bildschirm **„Ansprechpartner“** (aus der Übersicht): Gewerk/Rolle, Kontakt (Name/Firma), Telefon, Hinweis, „bei jedem kritischen Mangel“, aktiv/inaktiv.
- Im Prüfpunkt-Editor unten ein Knopf **„Bei n.i.O.: …“**. Er öffnet ein Fenster: Rückfrage an/aus mit Text, kritisch ja/nein mit Text, Ansprechpartner antippen.
- Kopie, neue Fassung, Änderungsliste und Prüfung kennen die fünf neuen Felder.
- Umfang: neue Liste + 5 Spalten (gemeinsam mit der Rundgang-App), 1 neuer Bildschirm, 3 neue Blöcke im Editor/Übersicht, 5 geänderte Properties.
- Geprüft: Generator 0 Fehler (Datenvertrag, Textbreiten mit Innenabstand), Mutation 13/13, Logik 27 Szenarien. **Nicht in Studio getestet. Nicht unabhängig geprüft.**

## Schritt 0 – SharePoint und Datenquellen

Die Liste `RG_Ansprechpartner` und die 5 Spalten an `RG_Pruefpunkte` sind dieselben wie im App-Teil (`pakete/PAKET_8_9_APP.md`, Schritt 1). Nur einmal anlegen.

Im Builder: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**, dann **Daten hinzufügen** → SharePoint → IMS+ → `RG_Ansprechpartner`.

## Schritt 1 – App.OnStart

**Pfad:** App → OnStart. Ganze Formel ersetzen.

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

```diff
-Set(varVorlageNeu; Defaults(RG_Rundgaenge))
+Set(varVorlageNeu; Defaults(RG_Rundgaenge));;
+Set(varNioOffen; false);;
+Set(varKoID; 0)
```

**Kurz erklärt:** Zwei neue Startwerte: `varNioOffen` (Fenster „Bei n.i.O.“) und `varKoID` (gewählter Ansprechpartner).

## Schritt 2 – neuer Bildschirm „Ansprechpartner“

**Wo hin:** In der Strukturansicht einen Bildschirm markieren (z. B. `scrPlan`) → Strg+V. Studio legt `scrKontakte` mit allen Steuerelementen an.

```yaml
Screens:
  scrKontakte:
    Properties:
      Fill: =clrHintergrund
      OnVisible: |-
        =Set(varIsLoading, true);
        Set(varLadeText, "");
        Refresh(RG_Ansprechpartner);
        ClearCollect(colKoAlle, RG_Ansprechpartner);
        Set(varKoID, Coalesce(First(Sort(colKoAlle, Title)).ID, 0));
        Reset(txtKoRolle);
        Reset(txtKoName);
        Reset(txtKoTelefon);
        Reset(txtKoHinweis);
        Set(varIsLoading, false)
    Children:
      - conKoKopf:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrPrimaer
            Height: =64
            Width: =Parent.Width
          Children:
            - btnKoZurueck:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderThickness: =0
                  Color: =Color.White
                  DisabledBorderColor: =clrGesperrtHell
                  DisabledColor: =clrGesperrt
                  DisabledFill: =clrGesperrtHell
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =RGBA(255, 255, 255, 0.12)
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HoverColor: =Color.White
                  HoverFill: =RGBA(255, 255, 255, 0.24)
                  OnSelect: =If(!varIsLoading, Navigate(scrListe, ScreenTransition.None))
                  PressedColor: =Color.White
                  PressedFill: =RGBA(255, 255, 255, 0.32)
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =14
                  Text: ="← Übersicht"
                  Width: =140
                  X: =16
                  Y: =12
            - lblKoTitel:
                Control: Label@2.5.1
                Properties:
                  Color: =Color.White
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =64
                  Size: =20
                  Text: ="Ansprechpartner"
                  Width: =600
                  X: =172
                  Y: =0
      - lblKoHilfe:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =44
            Size: =13
            Text: |-
              ="Wer soll bei einem kritischen Mangel informiert werden? „bei jedem“ erscheint bei jedem kritischen Mangel. Nicht mehr gebraucht: auf „inaktiv“ stellen, nicht löschen."
            Width: =Parent.Width - 48
            X: =24
            Y: =72
      - btnKoNeu:
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
            OnSelect: |-
              =If(!varIsLoading && Now() >= varSperreBis,
                  Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));
                  Set(varNeuID, IfError(Patch(RG_Ansprechpartner, Defaults(RG_Ansprechpartner), {Title: "Neuer Ansprechpartner", Kontakt: "", Telefon: "", Hinweis: "", Allgemein: false, Aktiv: true}).ID, 0));
                  If(varNeuID = 0,
                      Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
                      Collect(colKoAlle, LookUp(RG_Ansprechpartner, ID = varNeuID));
                      Set(varKoID, varNeuID);
                      Reset(txtKoRolle);
                      Reset(txtKoName);
                      Reset(txtKoTelefon);
                      Reset(txtKoHinweis);
                      SetFocus(txtKoRolle)
                  )
              )
            PressedColor: =Color.White
            PressedFill: =ColorFade(clrPrimaer, -35%)
            RadiusBottomLeft: =6
            RadiusBottomRight: =6
            RadiusTopLeft: =6
            RadiusTopRight: =6
            Size: =14
            Text: ="+ Ansprechpartner"
            Width: =240
            X: =24
            Y: =124
      - galKo:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            AccessibleLabel: ="Ansprechpartner"
            Height: =Parent.Height - 196
            Items: =Sort(colKoAlle, If(Coalesce(Aktiv, false), "0", "1") & Lower(Title))
            ShowScrollbar: =true
            TemplatePadding: =0
            TemplateSize: =64
            Width: =520
            X: =24
            Y: =180
          Children:
            - lblKoHinter:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Fill: =If(ThisItem.ID = varKoID, clrPrimaerHell, Color.White)
                  Font: =Font.'Segoe UI'
                  Height: =Parent.TemplateHeight - 4
                  Size: =14
                  Text: =""
                  Width: =Parent.TemplateWidth
                  X: =0
                  Y: =0
            - lblKoRolle:
                Control: Label@2.5.1
                Properties:
                  Color: =If(Coalesce(ThisItem.Aktiv, false), clrText, clrTextGrau)
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =28
                  Size: =14
                  Text: =ThisItem.Title
                  Width: =Parent.TemplateWidth - 24
                  Wrap: =false
                  X: =12
                  Y: =4
            - lblKoName:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =24
                  Size: =12
                  Text: =Coalesce(ThisItem.Kontakt, "") & If(Trim(Coalesce(ThisItem.Telefon, "")) = "", "", "  ·  " & ThisItem.Telefon) & If(Coalesce(ThisItem.Allgemein, false), "  ·  bei jedem", "") & If(Coalesce(ThisItem.Aktiv, false), "", "  ·  inaktiv")
                  Width: =Parent.TemplateWidth - 24
                  Wrap: =false
                  X: =12
                  Y: =32
            - btnKoZeile:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderThickness: =0
                  Color: =Color.White
                  DisabledBorderColor: =clrGesperrtHell
                  DisabledColor: =clrGesperrt
                  DisabledFill: =RGBA(0, 0, 0, 0)
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =RGBA(0, 0, 0, 0)
                  Font: =Font.'Segoe UI'
                  Height: =Parent.TemplateHeight - 4
                  HoverColor: =Color.White
                  HoverFill: =RGBA(23, 20, 150, 0.06)
                  OnSelect: |-
                    =Set(varKoID, ThisItem.ID);
                    Reset(txtKoRolle);
                    Reset(txtKoName);
                    Reset(txtKoTelefon);
                    Reset(txtKoHinweis)
                  PressedColor: =Color.White
                  PressedFill: =RGBA(23, 20, 150, 0.12)
                  RadiusBottomLeft: =0
                  RadiusBottomRight: =0
                  RadiusTopLeft: =0
                  RadiusTopRight: =0
                  Size: =14
                  Text: =""
                  Width: =Parent.TemplateWidth
                  X: =0
                  Y: =0
      - lblKoLeer:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =48
            Size: =13
            Text: ="Noch keine Ansprechpartner. „+ Ansprechpartner“ legt einen an."
            Visible: =IsEmpty(colKoAlle) && !varIsLoading
            Width: =520
            X: =24
            Y: =190
      - conKoForm:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrHintergrund
            Height: =560
            Visible: =varKoID > 0
            Width: =Parent.Width - 592
            X: =568
            Y: =124
          Children:
            - lblKoRolleT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Gewerk / Rolle"
                  Width: =400
                  X: =0
                  Y: =0
            - txtKoRolle:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Gewerk oder Rolle"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colKoAlle, ID = varKoID).Title, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HintText: ="z. B. Elektriker"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colKoAlle, ID = varKoID).Title, "")),
                        If(varKoID > 0 && !varIsLoading,
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Ansprechpartner, LookUp(RG_Ansprechpartner, ID = varKoID), {Title: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colKoAlle, LookUp(colKoAlle, ID = varKoID), LookUp(RG_Ansprechpartner, ID = varKoID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =20
            - lblKoNameT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Name / Firma"
                  Width: =400
                  X: =0
                  Y: =72
            - txtKoName:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Name oder Firma"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colKoAlle, ID = varKoID).Kontakt, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HintText: ="z. B. Elektro Müller GmbH"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colKoAlle, ID = varKoID).Kontakt, "")),
                        If(varKoID > 0 && !varIsLoading,
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Ansprechpartner, LookUp(RG_Ansprechpartner, ID = varKoID), {Kontakt: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colKoAlle, LookUp(colKoAlle, ID = varKoID), LookUp(RG_Ansprechpartner, ID = varKoID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =92
            - lblKoTelT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Telefon"
                  Width: =400
                  X: =0
                  Y: =144
            - txtKoTelefon:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Telefon"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colKoAlle, ID = varKoID).Telefon, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HintText: ="z. B. 0561 123456"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colKoAlle, ID = varKoID).Telefon, "")),
                        If(varKoID > 0 && !varIsLoading,
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Ansprechpartner, LookUp(RG_Ansprechpartner, ID = varKoID), {Telefon: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colKoAlle, LookUp(colKoAlle, ID = varKoID), LookUp(RG_Ansprechpartner, ID = varKoID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =164
            - lblKoHinweisT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Hinweis (z. B. Erreichbarkeit)"
                  Width: =400
                  X: =0
                  Y: =216
            - txtKoHinweis:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Hinweis"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colKoAlle, ID = varKoID).Hinweis, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =80
                  HintText: |-
                    ="z. B. nach 16 Uhr: Bereitschaft 0170 …"
                  HoverBorderColor: =clrPrimaer
                  Mode: =TextMode.MultiLine
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colKoAlle, ID = varKoID).Hinweis, "")),
                        If(varKoID > 0 && !varIsLoading,
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Ansprechpartner, LookUp(RG_Ansprechpartner, ID = varKoID), {Hinweis: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colKoAlle, LookUp(colKoAlle, ID = varKoID), LookUp(RG_Ansprechpartner, ID = varKoID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =236
            - lblKoAllgT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Bei jedem kritischen Mangel zeigen"
                  Width: =400
                  X: =0
                  Y: =332
            - galKoAllg:
                Control: Gallery@2.15.0
                Variant: Vertical
                Properties:
                  AccessibleLabel: ="Bei jedem kritischen Mangel"
                  Height: =40
                  Items: |-
                    =Table({W: "nein", N: "nein"}, {W: "ja", N: "bei jedem"})
                  ShowScrollbar: =false
                  TemplatePadding: =0
                  TemplateSize: =40
                  Width: =300
                  WrapCount: =2
                  X: =0
                  Y: =352
                Children:
                  - btnKoAllg:
                      Control: Classic/Button@2.2.0
                      Properties:
                        BorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        BorderThickness: =1
                        Color: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "ja", "nein"), Color.White, clrText)
                        DisabledBorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        DisabledColor: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "ja", "nein"), clrPrimaer, clrTextGrau)
                        DisabledFill: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "ja", "nein"), clrPrimaerHell, clrKarte)
                        DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                        Fill: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "ja", "nein"), clrPrimaer, clrKarte)
                        Font: =Font.'Segoe UI'
                        Height: =36
                        HoverColor: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "ja", "nein"), Color.White, clrText)
                        HoverFill: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "ja", "nein"), ColorFade(clrPrimaer, -20%), clrPrimaerHell)
                        OnSelect: |-
                          =If((ThisItem.W = "ja") <> Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false),
                              If(varKoID > 0 && !varIsLoading,
                                  Set(varPatchFehler, false);
                                  IfError(Patch(RG_Ansprechpartner, LookUp(RG_Ansprechpartner, ID = varKoID), {Allgemein: ThisItem.W = "ja"}), Set(varPatchFehler, true));
                                  If(varPatchFehler,
                                      Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                      Patch(colKoAlle, LookUp(colKoAlle, ID = varKoID), LookUp(RG_Ansprechpartner, ID = varKoID))
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
            - lblKoAktivT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Status"
                  Width: =400
                  X: =0
                  Y: =408
            - galKoAktiv:
                Control: Gallery@2.15.0
                Variant: Vertical
                Properties:
                  AccessibleLabel: ="Status"
                  Height: =40
                  Items: |-
                    =Table({W: "ja", N: "aktiv"}, {W: "nein", N: "inaktiv"})
                  ShowScrollbar: =false
                  TemplatePadding: =0
                  TemplateSize: =40
                  Width: =300
                  WrapCount: =2
                  X: =0
                  Y: =428
                Children:
                  - btnKoAktiv:
                      Control: Classic/Button@2.2.0
                      Properties:
                        BorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        BorderThickness: =1
                        Color: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "ja", "nein"), Color.White, clrText)
                        DisabledBorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        DisabledColor: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "ja", "nein"), clrPrimaer, clrTextGrau)
                        DisabledFill: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "ja", "nein"), clrPrimaerHell, clrKarte)
                        DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                        Fill: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "ja", "nein"), clrPrimaer, clrKarte)
                        Font: =Font.'Segoe UI'
                        Height: =36
                        HoverColor: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "ja", "nein"), Color.White, clrText)
                        HoverFill: =If(ThisItem.W = If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "ja", "nein"), ColorFade(clrPrimaer, -20%), clrPrimaerHell)
                        OnSelect: |-
                          =If((ThisItem.W = "ja") <> Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false),
                              If(varKoID > 0 && !varIsLoading,
                                  Set(varPatchFehler, false);
                                  IfError(Patch(RG_Ansprechpartner, LookUp(RG_Ansprechpartner, ID = varKoID), {Aktiv: ThisItem.W = "ja"}), Set(varPatchFehler, true));
                                  If(varPatchFehler,
                                      Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                      Patch(colKoAlle, LookUp(colKoAlle, ID = varKoID), LookUp(RG_Ansprechpartner, ID = varKoID))
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
      - conKoLaden:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =RGBA(255, 255, 255, 0.7)
            Height: =Parent.Height
            Visible: =varIsLoading
            Width: =Parent.Width
          Children:
            - btnKoLadenSperre:
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
            - lblKoLadenText:
                Control: Label@2.5.1
                Properties:
                  Align: =Align.Center
                  Color: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =60
                  Size: =18
                  Text: =If(varLadeText = "", "Bitte warten …", varLadeText)
                  Width: =Parent.Width
                  X: =0
                  Y: =(Parent.Height - 60) / 2
```

**Nachprüfen:** `scrKontakte` ist da, kein `_1`. Rot ist nur `RG_Ansprechpartner`, falls die Datenquelle noch fehlt.

## Schritt 3 – Knopf in der Übersicht

**Wo hin:** **`scrListe`** markieren → Strg+V.

```yaml
- btnLiKontakte:
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
      Height: =44
      HoverColor: =clrPrimaer
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =If(!varIsLoading && Now() >= varSperreBis,
            Set(varFrage, "");
            Navigate(scrKontakte, ScreenTransition.None)
        )
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =14
      Text: ="Ansprechpartner"
      Width: =200
      X: =650
      Y: =84
```

## Schritt 4 – Knopf „Bei n.i.O.“ im Prüfpunkt-Editor

**Wo hin:** **`conEdP`** (`scrEditor › conEdMitte › conEdP`) markieren → Strg+V.

```yaml
- btnPNio:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), clrFehler, clrPrimaer)
      BorderThickness: =1
      Color: =If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), clrFehler, clrPrimaer)
      DisabledBorderColor: =clrGesperrtHell
      DisabledColor: =clrGesperrt
      DisabledFill: =clrGesperrtHell
      DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =32
      HoverColor: =clrPrimaer
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =If(!varIsLoading,
            ClearCollect(colKontakte, Filter(RG_Ansprechpartner, Aktiv = true));
            Reset(txtNioRueckText);
            Reset(txtNioKritText);
            Set(varNioOffen, true)
        )
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =13
      Text: |-
        =If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "⚠ ", "") & "Bei n.i.O.: " & If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false) || Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "Rückfrage", "") & If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false) && Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), " + ", "") & If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "kritisch", ""), "nichts Besonderes") & "  ›"
      Width: =528
      X: =0
      Y: =If((LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "ZAHL"), 360, (LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "AUSWAHL" || LookUp(colP, ID = varAuswahlID).Eingabetyp.Value = "MEHRFACH"), 350, 232) + 256
```

**Rot bis Schritt 5:** `txtNioRueckText`, `txtNioKritText` (kommen mit dem Fenster).

## Schritt 5 – Fenster „Bei n.i.O.“

**Wo hin:** **`scrEditor`** markieren → Strg+V. Danach ist nichts mehr rot.

```yaml
- conNio:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      BorderThickness: =0
      Fill: =RGBA(0, 0, 0, 0.45)
      Height: =Parent.Height
      Visible: =varNioOffen
      Width: =Parent.Width
    Children:
      - btnNioSperre:
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
      - conNioKarte:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrKarte
            Height: =640
            RadiusBottomLeft: =12
            RadiusBottomRight: =12
            RadiusTopLeft: =12
            RadiusTopRight: =12
            Width: =660
            X: =(Parent.Width - Self.Width) / 2
            Y: =(Parent.Height - Self.Height) / 2
          Children:
            - lblNioTitel:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =40
                  Size: =18
                  Text: ="Bei n.i.O."
                  Width: =612
                  X: =24
                  Y: =16
            - lblNioFrage:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =28
                  Size: =14
                  Text: =LookUp(colP, ID = varAuswahlID).Title
                  Width: =612
                  X: =24
                  Y: =56
            - lblNioRueck:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =24
                  Size: =13
                  Text: ="Rückfrage „Ist das wirklich so?“"
                  Width: =300
                  X: =24
                  Y: =92
            - galNioRueck:
                Control: Gallery@2.15.0
                Variant: Vertical
                Properties:
                  AccessibleLabel: ="Rückfrage"
                  Height: =36
                  Items: |-
                    =Table({W: "nein", N: "aus"}, {W: "ja", N: "an"})
                  ShowScrollbar: =false
                  TemplatePadding: =0
                  TemplateSize: =36
                  Width: =200
                  WrapCount: =2
                  X: =336
                  Y: =88
                Children:
                  - btnNioRueck:
                      Control: Classic/Button@2.2.0
                      Properties:
                        BorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        BorderThickness: =1
                        Color: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "ja", "nein"), Color.White, clrText)
                        DisabledBorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        DisabledColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "ja", "nein"), clrPrimaer, clrTextGrau)
                        DisabledFill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "ja", "nein"), clrPrimaerHell, clrKarte)
                        DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.Disabled)
                        Fill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "ja", "nein"), clrPrimaer, clrKarte)
                        Font: =Font.'Segoe UI'
                        Height: =32
                        HoverColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "ja", "nein"), Color.White, clrText)
                        HoverFill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false), "ja", "nein"), ColorFade(clrPrimaer, -20%), clrPrimaerHell)
                        OnSelect: |-
                          =If((ThisItem.W = "ja") <> Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false),
                              If(varSchreibbar && varAuswahlEbene = 3,
                                  Refresh(RG_Rundgaenge);
                                  Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                                  If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                                  If(varEntwurfOk,
                                      Set(varPatchFehler, false);
                                      IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {Rueckfrage: ThisItem.W = "ja"}), Set(varPatchFehler, true));
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
            - txtNioRueckText:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Text der Rückfrage"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colP, ID = varAuswahlID).RueckfrageText, "")
                  DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HintText: |-
                    ="Normalerweise … (leer: bei Zahlen die Grenzen)"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colP, ID = varAuswahlID).RueckfrageText, "")),
                        If(varSchreibbar && varAuswahlEbene = 3,
                            Refresh(RG_Rundgaenge);
                            Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                            If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                            If(varEntwurfOk,
                                Set(varPatchFehler, false);
                                IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {RueckfrageText: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                                If(varPatchFehler,
                                    Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                    Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                                    Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                                )
                            )
                        )
                    )
                  Size: =14
                  Visible: =Coalesce(LookUp(colP, ID = varAuswahlID).Rueckfrage, false)
                  Width: =612
                  X: =24
                  Y: =132
            - lblNioKrit:
                Control: Label@2.5.1
                Properties:
                  Color: =clrFehler
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =24
                  Size: =13
                  Text: ="Kritischer Mangel – sofort melden"
                  Width: =300
                  X: =24
                  Y: =192
            - galNioKrit:
                Control: Gallery@2.15.0
                Variant: Vertical
                Properties:
                  AccessibleLabel: ="Kritisch"
                  Height: =36
                  Items: |-
                    =Table({W: "nein", N: "nein"}, {W: "ja", N: "ja"})
                  ShowScrollbar: =false
                  TemplatePadding: =0
                  TemplateSize: =36
                  Width: =200
                  WrapCount: =2
                  X: =336
                  Y: =188
                Children:
                  - btnNioKrit:
                      Control: Classic/Button@2.2.0
                      Properties:
                        BorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        BorderThickness: =1
                        Color: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "ja", "nein"), Color.White, clrText)
                        DisabledBorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        DisabledColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "ja", "nein"), clrPrimaer, clrTextGrau)
                        DisabledFill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "ja", "nein"), clrPrimaerHell, clrKarte)
                        DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.Disabled)
                        Fill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "ja", "nein"), clrPrimaer, clrKarte)
                        Font: =Font.'Segoe UI'
                        Height: =32
                        HoverColor: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "ja", "nein"), Color.White, clrText)
                        HoverFill: =If(ThisItem.W = If(Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false), "ja", "nein"), ColorFade(clrPrimaer, -20%), clrPrimaerHell)
                        OnSelect: |-
                          =If((ThisItem.W = "ja") <> Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false),
                              If(varSchreibbar && varAuswahlEbene = 3,
                                  Refresh(RG_Rundgaenge);
                                  Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                                  If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                                  If(varEntwurfOk,
                                      Set(varPatchFehler, false);
                                      IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {Kritisch: ThisItem.W = "ja"}), Set(varPatchFehler, true));
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
            - txtNioKritText:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Text für den kritischen Mangel"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colP, ID = varAuswahlID).KritischText, "")
                  DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HintText: ="Was ist zu tun? z. B. Anlage nicht weiter betreiben"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colP, ID = varAuswahlID).KritischText, "")),
                        If(varSchreibbar && varAuswahlEbene = 3,
                            Refresh(RG_Rundgaenge);
                            Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                            If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                            If(varEntwurfOk,
                                Set(varPatchFehler, false);
                                IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {KritischText: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                                If(varPatchFehler,
                                    Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                    Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                                    Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                                )
                            )
                        )
                    )
                  Size: =14
                  Visible: =Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false)
                  Width: =612
                  X: =24
                  Y: =232
            - lblNioKontakte:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =24
                  Size: =12
                  Text: ="Ansprechpartner – antippen zum Auswählen"
                  Visible: =Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false)
                  Width: =612
                  X: =24
                  Y: =282
            - galNioKontakte:
                Control: Gallery@2.15.0
                Variant: Vertical
                Properties:
                  AccessibleLabel: ="Ansprechpartner"
                  Height: =220
                  Items: =Sort(colKontakte, If(Coalesce(Allgemein, false), 0, 1) & Lower(Title))
                  ShowScrollbar: =true
                  TemplatePadding: =0
                  TemplateSize: =44
                  Visible: =Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false)
                  Width: =612
                  X: =24
                  Y: =310
                Children:
                  - btnNioKontakt:
                      Control: Classic/Button@2.2.0
                      Properties:
                        Align: =Align.Left
                        BorderColor: =clrPrimaer
                        BorderThickness: =1
                        Color: =clrPrimaer
                        DisabledBorderColor: =clrGesperrtHell
                        DisabledColor: =clrGesperrt
                        DisabledFill: =clrGesperrtHell
                        DisplayMode: =If(varSchreibbar && !varIsLoading && !Coalesce(ThisItem.Allgemein, false), DisplayMode.Edit, DisplayMode.Disabled)
                        Fill: =clrKarte
                        Font: =Font.'Segoe UI'
                        Height: =40
                        HoverColor: =clrPrimaer
                        HoverFill: =clrPrimaerHell
                        OnSelect: |-
                          =If(!Coalesce(ThisItem.Allgemein, false),
                              With({ids: Filter(Split(Coalesce(LookUp(colP, ID = varAuswahlID).Ansprechpartner, ""), ";"), Trim(Value) <> "")},
                                  With({neu: If(Text(ThisItem.ID) in ids.Value, Concat(Filter(ids, Trim(Value) <> Text(ThisItem.ID)) As s, Trim(s.Value), ";"), Concat(ids As s2, Trim(s2.Value) & ";") & Text(ThisItem.ID))},
                                      If(varSchreibbar && varAuswahlEbene = 3,
                                          Refresh(RG_Rundgaenge);
                                          Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                                          If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                                          If(varEntwurfOk,
                                              Set(varPatchFehler, false);
                                              IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {Ansprechpartner: neu}), Set(varPatchFehler, true));
                                              If(varPatchFehler,
                                                  Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                                  Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                                                  Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                                              )
                                          )
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
                        Text: =If(Coalesce(ThisItem.Allgemein, false), "✓ ", If(Text(ThisItem.ID) in Filter(Split(Coalesce(LookUp(colP, ID = varAuswahlID).Ansprechpartner, ""), ";"), Trim(Value) <> "").Value, "✓ ", "○ ")) & ThisItem.Title & If(Trim(Coalesce(ThisItem.Kontakt, "")) = "", "", " – " & ThisItem.Kontakt) & If(Coalesce(ThisItem.Allgemein, false), "  (immer)", "")
                        Width: =Parent.TemplateWidth - 4
                        X: =0
                        Y: =2
            - lblNioLeer:
                Control: Label@2.5.1
                Properties:
                  Color: =clrFehler
                  Font: =Font.'Segoe UI'
                  Height: =48
                  Size: =13
                  Text: ="Noch keine Ansprechpartner. Lege sie in der Übersicht unter „Ansprechpartner“ an."
                  Visible: =Coalesce(LookUp(colP, ID = varAuswahlID).Kritisch, false) && IsEmpty(colKontakte)
                  Width: =612
                  X: =24
                  Y: =320
            - lblNioHinweis:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =40
                  Size: =12
                  Text: ="Wirkt bei n.i.O. und bei Zahlen außerhalb der Grenzen (Modus „Mangel“). Es wird nichts verschickt."
                  Width: =612
                  X: =24
                  Y: =532
            - btnNioFertig:
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
                  OnSelect: =Set(varNioOffen, false)
                  PressedColor: =Color.White
                  PressedFill: =ColorFade(clrPrimaer, -35%)
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =14
                  Text: ="Fertig"
                  Width: =160
                  X: =476
                  Y: =576
            - btnNioZu:
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
                  OnSelect: =Set(varNioOffen, false)
                  PressedColor: =clrPrimaer
                  PressedFill: =clrPrimaerHell
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =16
                  Text: ="✕"
                  Width: =40
                  X: =600
                  Y: =16
```

## Schritt 6 – geänderte Formeln

### 6.1 · `lblVsRegeln.Text`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › lblVsRegeln` → Text

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "")
```

```diff
-"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglic …
+"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglic …
```

**Kurz erklärt:** Die Vorschau nennt „Rückfrage“ und „KRITISCH“.

**Nachprüfen:** endet auf `h; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "")`

### 6.2 · `galAkt.Items`

**Pfad:** `scrEditor › conAkt › conAktKarte › galAkt` → Items

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

```diff
-        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coales …
+        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coales …
```

**Kurz erklärt:** Änderungen an Rückfrage/kritisch/Ansprechpartnern zählen beim Aktivieren als „geändert“.

**Nachprüfen:** endet auf `)`

### 6.3 · `galPr.Items`

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
+            {T: ForAll(Filter(colP As p; (Coalesce(p.Kritisch; false) || Coalesce(p.Rueckfrage; false)) && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; B …
+            {T: ForAll(Filter(colP As p; Coalesce(p.Kritisch; false) && Trim(Coalesce(p.Ansprechpartner; "")) = "") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).Bereic …
```

**Kurz erklärt:** Zwei neue Hinweise: Rückfrage/kritisch bei einem Typ, wo es nicht wirkt, und kritisch ohne eigenen Ansprechpartner.

**Nachprüfen:** endet auf `)`

### 6.4 · `tmrArbeit.OnTimerEnd`

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

```diff
-                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgRei …
+                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgRei …
```

**Kurz erklärt:** Kopie, neue Fassung und „Holen“ übernehmen die fünf neuen Felder.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

## Test (wenn du testest)

1. Übersicht → „Ansprechpartner“ → „+ Ansprechpartner“: „Elektriker“, Kontakt, Telefon. Zweiter: „Allgemein“, „bei jedem“ = ja.
2. Testrundgang bearbeiten → Prüfpunkt → „Bei n.i.O.: nichts Besonderes ›“ → Rückfrage an + Text, kritisch ja + Text, „Elektriker“ antippen (✓).
3. Knopf zeigt „⚠ Bei n.i.O.: Rückfrage + kritisch ›“ in Rot, Vorschau nennt beides.
4. Aktivieren → Änderungsliste zeigt den Punkt als „geändert“. Neue Fassung → Einstellungen sind noch da.
5. In der Rundgang-App (nach Paket 8+9 App): Ablauf aus `PAKET_8_9_APP.md`, Test T3–T7.

## Rückweg

Vorher-Fassungen im Anhang. `scrKontakte`, `btnLiKontakte`, `btnPNio`, `conNio` löschen. Liste und Spalten dürfen bleiben.

## Anhang – Vorher-Fassungen (Stand nach Paket 8)

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
Set(varVorlageNeu; Defaults(RG_Rundgaenge))
```

**`galAkt.Items` vorher**

```
Ungroup(
    Table(
        {T: ForAll(Filter(colP As p; IsBlank(LookUp(colAltP As a; a.ID = p.QuelleID))) As p; {Art: "neu"; Text: p.Title})};
        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) || Coalesce(p.Auswahlwerte; "") <> Coalesce(a.Auswahlwerte; "") || Coalesce(p.Einheit; "") <> Coalesce(a.Einheit; "") || Coalesce(p.MinWert; -999999) <> Coalesce(a.MinWert; -999999) || Coalesce(p.MaxWert; -999999) <> Coalesce(a.MaxWert; -999999) || Coalesce(p.Hinweis; "") <> Coalesce(a.Hinweis; "") || fnFotoWert(p.Foto.Value; Coalesce(p.FotoMoeglich; false)) <> fnFotoWert(a.Foto.Value; Coalesce(a.FotoMoeglich; false)) || Coalesce(p.KommentarPflicht; false) <> Coalesce(a.KommentarPflicht; false) || fnGrenzmodus(p.Grenzmodus.Value) <> fnGrenzmodus(a.Grenzmodus.Value) || Coalesce(p.BedingungWert; "") <> Coalesce(a.BedingungWert; "") || Coalesce(LookUp(colP As b0; b0.ID = p.BedingungPunkt).QuelleID; 0) <> Coalesce(a.BedingungPunkt; 0) || Coalesce(p.HinweisBildID; 0) <> Coalesce(a.HinweisBildID; 0) || Coalesce(LookUp(colK As k0; k0.ID = p.KategorieID).QuelleID; 0) <> a.KategorieID || Trim(Coalesce(p.Abschnitt; "")) <> Trim(Coalesce(a.Abschnitt; ""))))) As p; {Art: "geändert"; Text: p.Title})};
        {T: ForAll(Filter(colAltP As a; IsBlank(LookUp(colP As p; p.QuelleID = a.ID))) As a; {Art: "entfernt"; Text: a.Title})}
    );
    T
)
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
            {T: ForAll(Filter(colP As p; p.Title = "Neue Frage") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Eine Frage heißt noch „Neue Frage“."})};
            {T: ForAll(Filter(colK As k; CountRows(Filter(colP As p; p.KategorieID = k.ID)) > 30) As k; {Art: "Hinweis"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat über 30 Prüfpunkte (lange Seite für den Prüfer)."})};
            {T: Filter(Table({Art: "Hinweis"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Kein aktiver Plan: Der Rundgang erscheint nie auf der Startseite. → In der Übersicht „Plan“ tippen."}); !varIstVorlage && IsEmpty(Filter(colPlanR; Coalesce(Aktiv; false))))}
        );
        T
    );
    If(Art = "Fehler"; 0; 1)
)
```

**`lblVsRegeln.Text` vorher**

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "")
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
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQK) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colP; KategorieID = varZielK); RgReihenfolge); 0) + i.Value * 10); Aktiv: true; QuelleID: q.ID; Eingabetyp: {Value: Coalesce(q.Eingabetyp.Value; "IONIO")}; Pflicht: Coalesce(q.Pflicht; false); Auswahlwerte: q.Auswahlwerte; Einheit: q.Einheit; MinWert: q.MinWert; MaxWert: q.MaxWert; Hinweis: q.Hinweis; FotoMoeglich: Coalesce(q.FotoMoeglich; false); Foto: {Value: fnFotoWert(q.Foto.Value; Coalesce(q.FotoMoeglich; false))}; KommentarPflicht: Coalesce(q.KommentarPflicht; false); Grenzmodus: {Value: fnGrenzmodus(q.Grenzmodus.Value)}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: Coalesce(q.HinweisBildID; 0); Abschnitt: Coalesce(q.Abschnitt; "")}).ID; 0))}
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

