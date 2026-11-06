# Paket 11 – Prüfer wählen, Unterschrift, Kopfdaten

Stand 06.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket11), `werkzeuge/builder.py`, `werkzeuge/doc_paket11.py`. Voraussetzung: Paket 23 und 18 in beiden Apps.

## Kurzfassung

- **Gerätekonto:** Das iPad bleibt mit einem gemeinsamen Konto angemeldet. Wer prüft, wählt beim Start seinen Namen: oben die Liste `RG_Pruefer` (ein Tipp), darunter **„Andere Person suchen“** im Firmenverzeichnis (Vertretung). Über die Suche gewählte Personen kommen automatisch in `RG_Pruefer`. Keine PIN.
- Überall, wo bisher `User()` den Prüfer lieferte (Durchführung, Kategorie, Mängel, „Bescheid gegeben“), steht jetzt die gewählte Person. Das Gerätekonto wird in `Geraetekonto` mitgeschrieben.
- **Unterschrift Pflicht:** „Rundgang abschließen“ öffnet ein Unterschriftsfeld, darunter Name, Datum, Uhrzeit. Erst „Unterschreiben und abschließen“ schließt ab. Die Unterschrift wird als PNG in `RG_Fotos` abgelegt (Testablage wie Fotos), Bild und Link stehen an der Durchführung, im Protokoll und im Archiv-PDF.
- **Danach ist kein Prüfer mehr gewählt:** Zurück auf der Startseite erscheint wieder die Auswahl.
- **Kopfdaten:** Je Rundgang im Builder unter **Plan** unten Standort, Adresse, Auftraggeber (optional). Protokollkopf: Rundgang, Standort · Adresse, Auftraggeber, Datum mit KW, Prüfer.
- **Builder:** Prüferliste unter Übersicht › Ansprechpartner › **👤 Prüfer** (Liste, aktiv/inaktiv, Personensuche aus dem Firmenverzeichnis).
- Umfang: App 9 Properties + 21 neue Steuerelemente (davon die Stifteingabe über das Menü); Builder 1 Properties + `btnKoPruefer`, `lblPlAdresseT`, `lblPlAuftragT`, `lblPlKopfT`, `lblPlStandortT`, `scrPruefer`, `txtPlAdresse`, `txtPlAuftrag`, `txtPlStandort`. Generatoren 0 Fehler, Mutation 12/12 und 13/13, Textbreiten geprüft. **Nicht in Studio getestet.**
- **UNSICHER (Vorab-Tests):** U1 `OnSelect` der Stifteingabe beim Zeichnen; U2 Flow `aRG_Foto_hochladen` nimmt `penRuUnterschrift.Image` wie ein Foto an; U3 das Bild (Daten-URL) erscheint im Archiv-PDF; U4 Länge der Daten-URL in `UnterschriftBild` (mehrzeiliger Text) – bei Fehler „Schreibfehler“ beim Abschluss.

## Teil A – Rundgang DEV

### A1 – SharePoint und Daten (zuerst)

- Neue Liste **`RG_Pruefer`**: `Title` (vorhanden, = Name), `Email` (Eine Textzeile), `Aktiv` (Ja/Nein, Standard Ja).
- `RG_Rundgaenge`: neue Spalten **`Standort`**, **`Adresse`**, **`Auftraggeber`** (je Eine Textzeile).
- `RG_Durchfuehrungen`: neue Spalten **`UnterschriftBild`** (Mehrere Textzeilen, **nur Text**, keine Längenbegrenzung), **`UnterschriftUrl`** (Mehrere Textzeilen, nur Text), **`UnterschriftName`** (Eine Textzeile), **`UnterschriftZeit`** (Datum und Uhrzeit), **`Geraetekonto`** (Eine Textzeile).
- Rundgang DEV: Daten → `RG_Rundgaenge` und `RG_Durchfuehrungen` → ⋯ → Aktualisieren; Daten hinzufügen → SharePoint → IMS+ → `RG_Pruefer`; Daten hinzufügen → **„Office 365-Benutzer“** (Connector `Office365Users`).
- **Für IT/Michael (vor dem Test):** Das gemeinsame Gerätekonto braucht eine Power-Apps-Lizenz, Zugriff auf beide Apps, Schreibrechte auf IMS+ (alle RG-Listen und `RG_Fotos`) und muss den Connector **Office 365-Benutzer** verwenden dürfen (DLP-Richtlinie der Umgebung: Office 365 Users in derselben Gruppe wie SharePoint). Beim ersten Start fragt die App einmal nach der Zustimmung für den Connector – mit dem Gerätekonto bestätigen.
- **Wichtig:** `varIstAdmin` (Admin-Funktionen) hängt weiter am angemeldeten Konto (`User()`), also am Gerätekonto. Soll das Gerätekonto keine Admin-Rechte haben, nicht in `cfgAdmins` eintragen.

### A2.1 – neues Steuerelement `conPwWahl`

**Wo hin:** in der Strukturansicht **`scrStart`** markieren → Strg+V.

```yaml
- conPwWahl:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      Fill: =clrHintergrund
      Height: =Parent.Height
      Visible: =varPrWahl || Coalesce(varPruefer.Email, "") = ""
      Width: =Parent.Width
    Children:
    - lblPwTitel:
        Control: Label@2.5.1
        Properties:
          Color: =clrPrimaer
          Font: =Font.'Segoe UI'
          FontWeight: =FontWeight.Semibold
          Height: =48
          Size: =24
          Text: ="Wer prüft?"
          Width: =Parent.Width - 48
          X: =24
          Y: =32
    - lblPwHinweis:
        Control: Label@2.5.1
        Properties:
          Color: =clrTextGrau
          Font: =Font.'Segoe UI'
          Height: =48
          Size: =14
          Text: ="Bitte deinen Namen antippen. Nach dem Abschließen eines Rundgangs wird neu gefragt."
          VerticalAlign: =VerticalAlign.Top
          Width: =Parent.Width - 48
          X: =24
          Y: =84
    - galPwListe:
        Control: Gallery@2.15.0
        Variant: Vertical
        Properties:
          AccessibleLabel: ="Prüfer"
          Height: =420
          Items: =Sort(Filter(colPrueferAlle, Coalesce(Aktiv, false)), Lower(Title))
          ShowScrollbar: =true
          TemplatePadding: =0
          TemplateSize: =68
          Width: =Parent.Width
          X: =0
          Y: =140
        Children:
        - btnPwName:
            Control: Classic/Button@2.2.0
            Properties:
              Align: =Align.Left
              BorderColor: =clrPrimaer
              BorderThickness: =1
              Color: =clrPrimaer
              DisabledBorderColor: =clrGesperrtHell
              DisabledColor: =clrGesperrt
              DisabledFill: =clrGesperrtHell
              Fill: =clrKarte
              Font: =Font.'Segoe UI'
              Height: =Parent.TemplateHeight - 12
              HoverColor: =clrPrimaer
              HoverFill: =clrPrimaerHell
              OnSelect: |-
                =If(!varIsLoading && Now() >= varSperreBis,
                    Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));
                    Set(varPruefer, {Name: ThisItem.Title, Email: Lower(ThisItem.Email)});
                    Reset(txtPwSuche);
                    Set(varPrWahl, false)
                )
              PaddingLeft: =20
              PressedColor: =clrPrimaer
              PressedFill: =clrPrimaerHell
              RadiusBottomLeft: =8
              RadiusBottomRight: =8
              RadiusTopLeft: =8
              RadiusTopRight: =8
              Size: =18
              Text: =ThisItem.Title & If(Lower(ThisItem.Email) = Lower(Coalesce(varPruefer.Email, "")), "   ✓", "")
              Width: =Parent.TemplateWidth - 48
              X: =24
              Y: =6
    - lblPwLeer:
        Control: Label@2.5.1
        Properties:
          Color: =clrTextGrau
          Font: =Font.'Segoe UI'
          Height: =48
          Size: =14
          Text: ="Noch niemand in der Prüferliste. Unten nach dem Namen suchen."
          Visible: =IsEmpty(Filter(colPrueferAlle, Coalesce(Aktiv, false)))
          Width: =Parent.Width - 48
          X: =24
          Y: =150
    - lblPwSuchT:
        Control: Label@2.5.1
        Properties:
          Color: =clrText
          Font: =Font.'Segoe UI'
          FontWeight: =FontWeight.Semibold
          Height: =28
          Size: =15
          Text: ="Andere Person suchen (z. B. Vertretung)"
          Width: =Parent.Width - 48
          X: =24
          Y: =576
    - txtPwSuche:
        Control: Classic/TextInput@2.3.2
        Properties:
          AccessibleLabel: ="Name suchen"
          BorderColor: =clrRahmen
          Color: =clrText
          Default: =""
          DelayOutput: =true
          FocusedBorderColor: =clrPrimaer
          Font: =Font.'Segoe UI'
          Height: =56
          HintText: ="Name eingeben (mind. 3 Buchstaben)"
          HoverBorderColor: =clrPrimaer
          RadiusBottomLeft: =8
          RadiusBottomRight: =8
          RadiusTopLeft: =8
          RadiusTopRight: =8
          Size: =16
          Width: =Parent.Width - 48
          X: =24
          Y: =608
    - galPwSuche:
        Control: Gallery@2.15.0
        Variant: Vertical
        Properties:
          AccessibleLabel: ="Suchergebnisse"
          Height: =Parent.Height - 676 - 96
          Items: |-
            =If(varPrWahl || Coalesce(varPruefer.Email, "") = "", If(Len(Trim(txtPwSuche.Text)) >= 3, Filter(Office365Users.SearchUserV2({searchTerm: Trim(txtPwSuche.Text), top: 15, isSearchTermRequired: true}).value, !IsBlank(Mail) && AccountEnabled)))
          ShowScrollbar: =true
          TemplatePadding: =0
          TemplateSize: =64
          Width: =Parent.Width
          X: =0
          Y: =676
        Children:
        - btnPwTreffer:
            Control: Classic/Button@2.2.0
            Properties:
              Align: =Align.Left
              BorderColor: =clrPrimaer
              BorderThickness: =1
              Color: =clrPrimaer
              DisabledBorderColor: =clrGesperrtHell
              DisabledColor: =clrGesperrt
              DisabledFill: =clrGesperrtHell
              Fill: =clrKarte
              Font: =Font.'Segoe UI'
              Height: =Parent.TemplateHeight - 10
              HoverColor: =clrPrimaer
              HoverFill: =clrPrimaerHell
              OnSelect: |-
                =If(!varIsLoading && Now() >= varSperreBis,
                    Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));
                    Set(varPruefer, {Name: ThisItem.DisplayName, Email: Lower(ThisItem.Mail)});
                    If(IsBlank(LookUp(colPrueferAlle, Lower(Email) = Lower(ThisItem.Mail))),
                        IfError(Patch(RG_Pruefer, Defaults(RG_Pruefer), {Title: ThisItem.DisplayName, Email: Lower(ThisItem.Mail), Aktiv: true}), Notify("In die Prüferliste konnte nicht gespeichert werden – du prüfst trotzdem unter diesem Namen.", NotificationType.Warning));
                        Refresh(RG_Pruefer);
                        ClearCollect(colPrueferAlle, RG_Pruefer)
                    );
                    Reset(txtPwSuche);
                    Set(varPrWahl, false)
                )
              PaddingLeft: =20
              PressedColor: =clrPrimaer
              PressedFill: =clrPrimaerHell
              RadiusBottomLeft: =8
              RadiusBottomRight: =8
              RadiusTopLeft: =8
              RadiusTopRight: =8
              Size: =15
              Text: =ThisItem.DisplayName & If(Coalesce(ThisItem.Department, "") = "", "", "  ·  " & ThisItem.Department)
              Width: =Parent.TemplateWidth - 48
              X: =24
              Y: =5
    - btnPwZu:
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
          Height: =56
          HoverColor: =clrPrimaer
          HoverFill: =clrPrimaerHell
          OnSelect: =Set(varPrWahl, false)
          PressedColor: =clrPrimaer
          PressedFill: =clrPrimaerHell
          RadiusBottomLeft: =8
          RadiusBottomRight: =8
          RadiusTopLeft: =8
          RadiusTopRight: =8
          Size: =16
          Text: ="Schließen"
          Visible: =!(Coalesce(varPruefer.Email, "") = "")
          Width: =200
          X: =Parent.Width - 224
          Y: =Parent.Height - 80
```

### A2.2 – neues Steuerelement `conRuUnterschrift`

**Wo hin:** in der Strukturansicht **`scrRundgang`** markieren → Strg+V.

```yaml
- conRuUnterschrift:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      Fill: =RGBA(0, 0, 0, 0.45)
      Height: =Parent.Height
      Visible: =varUnterschriftOffen
      Width: =Parent.Width
    Children:
    - btnRuUSperre:
        Control: Classic/Button@2.2.0
        Properties:
          BorderThickness: =0
          Fill: =RGBA(0, 0, 0, 0)
          Height: =Parent.Height
          HoverFill: =RGBA(0, 0, 0, 0)
          PressedFill: =RGBA(0, 0, 0, 0)
          Text: =""
          Width: =Parent.Width
    - conRuUKarte:
        Control: GroupContainer@1.5.0
        Variant: ManualLayout
        Properties:
          Fill: =clrKarte
          Height: =600
          RadiusBottomLeft: =16
          RadiusBottomRight: =16
          RadiusTopLeft: =16
          RadiusTopRight: =16
          Width: =Parent.Width - 64
          X: =32
          Y: =(Parent.Height - Self.Height) / 2
        Children:
        - lblRuUTitel:
            Control: Label@2.5.1
            Properties:
              Color: =clrPrimaer
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =40
              Size: =20
              Text: ="Unterschrift"
              Width: =Parent.Width - 40
              X: =20
              Y: =14
        - lblRuUText:
            Control: Label@2.5.1
            Properties:
              Color: =clrTextGrau
              Font: =Font.'Segoe UI'
              Height: =48
              Size: =14
              Text: ="Mit der Unterschrift schließt " & varPruefer.Name & " den Rundgang ab. Danach sind keine Änderungen mehr möglich."
              VerticalAlign: =VerticalAlign.Top
              Width: =Parent.Width - 40
              X: =20
              Y: =56
        - lblRuUName:
            Control: Label@2.5.1
            Properties:
              Color: =clrText
              Font: =Font.'Segoe UI'
              Height: =28
              Size: =14
              Text: =varPruefer.Name & "  ·  " & Text(Now(), "dd.mm.yyyy hh:mm")
              Width: =Parent.Width - 40
              X: =20
              Y: =428
        - btnRuULoeschen:
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
              Height: =52
              HoverColor: =clrPrimaer
              HoverFill: =clrPrimaerHell
              OnSelect: |-
                =Reset(penRuUnterschrift);
                Set(varUnterschriftDa, false)
              PressedColor: =clrPrimaer
              PressedFill: =clrPrimaerHell
              RadiusBottomLeft: =8
              RadiusBottomRight: =8
              RadiusTopLeft: =8
              RadiusTopRight: =8
              Size: =15
              Text: ="Löschen"
              Width: =140
              X: =20
              Y: =Parent.Height - 76
        - btnRuUAbbrechen:
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
              Height: =52
              HoverColor: =clrPrimaer
              HoverFill: =clrPrimaerHell
              OnSelect: |-
                =Set(varUnterschriftOffen, false);
                Set(varAbschlussFrage, false)
              PressedColor: =clrPrimaer
              PressedFill: =clrPrimaerHell
              RadiusBottomLeft: =8
              RadiusBottomRight: =8
              RadiusTopLeft: =8
              RadiusTopRight: =8
              Size: =15
              Text: ="Abbrechen"
              Width: =150
              X: =172
              Y: =Parent.Height - 76
        - btnRuUOk:
            Control: Classic/Button@2.2.0
            Properties:
              BorderThickness: =0
              Color: =Color.White
              DisabledBorderColor: =clrGesperrtHell
              DisabledColor: =clrGesperrt
              DisabledFill: =clrGesperrtHell
              DisplayMode: =If(varUnterschriftDa && !varIsLoading, DisplayMode.Edit, DisplayMode.Disabled)
              Fill: =clrPrimaer
              Font: =Font.'Segoe UI'
              Height: =52
              HoverColor: =Color.White
              HoverFill: =ColorFade(clrPrimaer, -20%)
              OnSelect: |-
                =If(varUnterschriftDa && !varIsLoading,
                    Set(varUnterschriftBild, With({j: JSON(penRuUnterschrift.Image, JSONFormat.IncludeBinaryData)}, Mid(j, 2, Len(j) - 2)));
                    Set(varUnterschriftUrl, "");
                    Set(varAbschlussFrage, true);
                    Select(btnRuAbschluss)
                )
              PressedColor: =Color.White
              PressedFill: =ColorFade(clrPrimaer, -35%)
              RadiusBottomLeft: =8
              RadiusBottomRight: =8
              RadiusTopLeft: =8
              RadiusTopRight: =8
              Size: =15
              Text: ="Unterschreiben und abschließen"
              Width: =Parent.Width - 354
              X: =334
              Y: =Parent.Height - 76
```

**Stifteingabe (über das Menü, ohne YAML):** In der Strukturansicht `conRuUKarte` markieren → **Einfügen → Eingabe → Stifteingabe**. Es muss **in** `conRuUKarte` landen. Umbenennen in **`penRuUnterschrift`**. Dann diese Properties setzen (Formelleiste, ganze Property):

- `X`: `20`
- `Y`: `116`
- `Width`: `Parent.Width - 40`
- `Height`: `300`
- `OnSelect`: `Set(varUnterschriftDa; true)`
- `Fill`: `Color.White`
- `Color`: `clrText`
- `BorderColor`: `clrRahmen`
- `BorderThickness`: `1`

**Vorab-Test (Pflicht, U1):** In der Vorschau auf der Stifteingabe zeichnen → `varUnterschriftDa` muss `true` werden (Variablen-Ansicht). Bleibt es `false`, löst das Zeichnen kein `OnSelect` aus – dann melden; der Knopf „Unterschreiben und abschließen“ bliebe gesperrt.

### A3 – geänderte Properties

### A3.1 · `App.OnStart`

**Pfad:** `App` → OnStart

```
Set(varHeute; Today());;
Set(varTag; Today());;
Set(varTagText; Text(Today(); "yyyy-mm-dd"));;
Set(varIsLoading; false);;
Set(varSperreBis; Now());;
Set(varPatchFehler; false);;
Set(varRgID; 0);;
Set(varSchluessel; "");;
Set(varDurchID; 0);;
Set(varDurch; Defaults(RG_Durchfuehrungen));;
Set(varKatID; 0);;
Set(varKatPos; 0);;
Set(varKatName; "");;
Set(varBereichName; "");;
Set(varSchluesselK; "");;
Set(varErgebnis; Defaults(RG_KategorieErgebnisse));;
Set(varNachlese; Defaults(RG_KategorieErgebnisse));;
Set(varGespeichertBeimOeffnen; Defaults(RG_KategorieErgebnisse).GespeichertAm);;
Set(varAntwortJSON; "");;
Set(varNurLesen; false);;
Set(varAbschlussFrage; false);;
Set(varZurueckFrage; false);;
Set(varGeaendert; false);;
Set(varAlleIOFrage; false);;
Set(varProtokollZeit; Now());;
Set(varIstAdmin; CountRows(Filter(Split(Lower(cfgAdmins); ";") As a; Trim(a.Value) = Lower(User().Email))) > 0);;
Set(varZuruecksetzenFrage; false);;
Set(varWeiter; false);;
Set(varZeigeFehlend; false);;
Set(varFotoPP; 0);;
Set(varArchivStart; false);;
Set(varPruefer; {Name: ""; Email: ""});;
Set(varPrWahl; true);;
Set(varUnterschriftOffen; false);;
Set(varUnterschriftDa; false);;
Set(varUnterschriftBild; "");;
Set(varUnterschriftUrl; "")
```

```diff
-Set(varArchivStart; false)
+Set(varArchivStart; false);;
+Set(varPruefer; {Name: ""; Email: ""});;
+Set(varPrWahl; true);;
+Set(varUnterschriftOffen; false);;
+Set(varUnterschriftDa; false);;
+Set(varUnterschriftBild; "");;
+Set(varUnterschriftUrl; "")
```

**Kurz erklärt:** Startwerte für den gewählten Prüfer (`varPruefer`) und die Unterschrift. Beim Start ist niemand gewählt → die Prüferauswahl erscheint.

**Nachprüfen:** endet auf `Set(varUnterschriftUrl; "")`

### A3.2 · `scrStart.OnVisible`

**Pfad:** `scrStart` → OnVisible

```
Set(varIsLoading; true);;
Set(varAusArchiv; false);;
If(IsBlank(varHeute) || varHeute <> Today(); Set(varHeute; Today());; Set(varTag; Today()));;
Set(varTagText; Text(varTag; "yyyy-mm-dd"));;
Concurrent(
    ClearCollect(colRundgaenge; Filter(RG_Rundgaenge; Aktiv = true));
    ClearCollect(colPlan; Filter(RG_Plan; Aktiv = true));
    ClearCollect(colPrueferAlle; RG_Pruefer)
);;
Select(btnStartTagLaden)
```

```diff
-    ClearCollect(colPlan; Filter(RG_Plan; Aktiv = true))
+    ClearCollect(colPlan; Filter(RG_Plan; Aktiv = true));
+    ClearCollect(colPrueferAlle; RG_Pruefer)
```

**Kurz erklärt:** Liest die Prüferliste (`colPrueferAlle`).

**Nachprüfen:** endet auf `Select(btnStartTagLaden)`

### A3.3 · `lblStartNutzer.Text`

**Pfad:** `scrStart › conStartKopf › lblStartNutzer` → Text

```
If(Coalesce(varPruefer.Email; "") = ""; "Kein Prüfer gewählt"; varPruefer.Name & "  ·  wechseln ›") & If(cfgTestmodus; "  ·  TESTMODUS"; "")
```

```diff
-User().FullName & If(cfgTestmodus; "  ·  TESTMODUS"; "")
+If(Coalesce(varPruefer.Email; "") = ""; "Kein Prüfer gewählt"; varPruefer.Name & "  ·  wechseln ›") & If(cfgTestmodus; "  ·  TESTMODUS"; "")
```

**Kurz erklärt:** Oben rechts steht der gewählte Prüfer statt des Gerätekontos.

**Nachprüfen:** endet auf `"; varPruefer.Name & "  ·  wechseln ›") & If(cfgTestmodus; "  ·  TESTMODUS"; "")`

### A3.4 · `lblStartNutzer.OnSelect`

**Pfad:** `scrStart › conStartKopf › lblStartNutzer` → OnSelect

```
If(!varIsLoading; Set(varPrWahl; true))
```

```diff
-false
+If(!varIsLoading; Set(varPrWahl; true))
```

**Kurz erklärt:** Antippen öffnet die Prüferauswahl (Prüfer wechseln).

**Nachprüfen:** endet auf `If(!varIsLoading; Set(varPrWahl; true))`

### A3.5 · `btnRgAktion.OnSelect`

**Pfad:** `scrStart › galStartRundgaenge › conRgKarte › btnRgAktion` → OnSelect

```
If(Coalesce(varPruefer.Email; "") = "";
    Set(varPrWahl; true);
    If(!varIsLoading && Now() >= varSperreBis;
        Set(varIsLoading; true);;
        Set(varPatchFehler; false);;
        Set(varRgID; ThisItem.ID);;
        Set(varSchluessel; "R" & ThisItem.ID & "-" & varTagText);;
        Refresh(RG_Durchfuehrungen);;
        Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
        If(varDurchID = 0;
            If(DateDiff(varTag; varHeute; TimeUnit.Days) < 0 || DateDiff(varTag; varHeute; TimeUnit.Days) > cfgNachholTage;
                Notify("Für diesen Tag kann kein Rundgang gestartet werden."; NotificationType.Error);
                With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k: Filter(RG_Kategorien; Aktiv = true)};
                    With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName; If(Coalesce(LookUp(b As be3; be3.ID = BereichID).Ausblenden; false); ""; LookUp(b As be4; be4.ID = BereichID).Title)); BReihe * 10000 + RgReihenfolge)};
                        ClearCollect(colKatBau; ForAll(Sequence(CountRows(kk)) As s; With({z: Index(kk; s.Value)}; {KategorieID: z.ID; Position: s.Value; BereichName: z.BName; KategorieName: z.Title})))
                    )
                );;
                If(CountRows(colKatBau) = 0;
                    Notify("Für diesen Rundgang sind keine aktiven Kategorien hinterlegt."; NotificationType.Error);
                    IfError(
                        Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: ISOWeekNum(varTag); Wochentag: Weekday(varTag; StartOfWeek.Monday); Status: stInArbeit; AnzahlKategorien: CountRows(colKatBau); KategorieListe: JSON(colKatBau; JSONFormat.Compact); PrueferEmail: varPruefer.Email; PrueferName: varPruefer.Name; Geraetekonto: User().Email; StartZeit: Now(); TestDatensatz: Coalesce(ThisItem.Testrundgang; false)});
                        Set(varPatchFehler; true)
                    );;
                    Refresh(RG_Durchfuehrungen);;
                    Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
                    If(varDurchID = 0; Notify("Der Rundgang konnte nicht gestartet werden. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error))
                )
            )
        );;
        If(varDurchID > 0; Navigate(scrRundgang; ScreenTransition.None));;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
    )
)
```

```diff
-If(!varIsLoading && Now() >= varSperreBis;
-    Set(varIsLoading; true);;
-    Set(varPatchFehler; false);;
-    Set(varRgID; ThisItem.ID);;
-    Set(varSchluessel; "R" & ThisItem.ID & "-" & varTagText);;
-    Refresh(RG_Durchfuehrungen);;
-    Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
-    If(varDurchID = 0;
-        If(DateDiff(varTag; varHeute; TimeUnit.Days) < 0 || DateDiff(varTag; varHeute; TimeUnit.Days) > cfgNachholTage;
-            Notify("Für diesen Tag kann kein Rundgang gestartet werden."; NotificationType.Error);
-            With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k: Filter(RG_Kategorien; Aktiv = true)};
- With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName …
-                    ClearCollect(colKatBau; ForAll(Sequence(CountRows(kk)) As s; With({z: Index(kk; s.Value)}; {KategorieID: z.ID; Position: s.Value; BereichName: z.BName; KategorieName: z.Title})))
+If(Coalesce(varPruefer.Email; "") = "";
+    Set(varPrWahl; true);
+    If(!varIsLoading && Now() >= varSperreBis;
+        Set(varIsLoading; true);;
+        Set(varPatchFehler; false);;
+        Set(varRgID; ThisItem.ID);;
+        Set(varSchluessel; "R" & ThisItem.ID & "-" & varTagText);;
+        Refresh(RG_Durchfuehrungen);;
+        Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
+        If(varDurchID = 0;
+            If(DateDiff(varTag; varHeute; TimeUnit.Days) < 0 || DateDiff(varTag; varHeute; TimeUnit.Days) > cfgNachholTage;
+                Notify("Für diesen Tag kann kein Rundgang gestartet werden."; NotificationType.Error);
+                With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k: Filter(RG_Kategorien; Aktiv = true)};
+ With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; B …
+                        ClearCollect(colKatBau; ForAll(Sequence(CountRows(kk)) As s; With({z: Index(kk; s.Value)}; {KategorieID: z.ID; Position: s.Value; BereichName: z.BName; KategorieName: z.Title})))
+                    )
+                );;
+                If(CountRows(colKatBau) = 0;
+                    Notify("Für diesen Rundgang sind keine aktiven Kategorien hinterlegt."; NotificationType.Error);
+                    IfError(
+ Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: I …
+                        Set(varPatchFehler; true)
+                    );;
+                    Refresh(RG_Durchfuehrungen);;
+                    Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
+                    If(varDurchID = 0; Notify("Der Rundgang konnte nicht gestartet werden. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error))
-            );;
-            If(CountRows(colKatBau) = 0;
-                Notify("Für diesen Rundgang sind keine aktiven Kategorien hinterlegt."; NotificationType.Error);
-                IfError(
- Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: ISOWe …
-                    Set(varPatchFehler; true)
-                );;
-                Refresh(RG_Durchfuehrungen);;
-                Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
-                If(varDurchID = 0; Notify("Der Rundgang konnte nicht gestartet werden. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error))
-        )
-    );;
-    If(varDurchID > 0; Navigate(scrRundgang; ScreenTransition.None));;
-    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
-    Set(varIsLoading; false)
+        );;
+        If(varDurchID > 0; Navigate(scrRundgang; ScreenTransition.None));;
+        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+        Set(varIsLoading; false)
+    )
```

**Kurz erklärt:** Ohne gewählten Prüfer öffnet sich die Auswahl. Sonst wie bisher, aber Prüfer = gewählte Person; das Gerätekonto wird in `Geraetekonto` mitgeschrieben.

**Nachprüfen:** endet auf `)`

### A3.6 · `btnKaSpeichern.OnSelect`

**Pfad:** `scrKategorie › conKaFuss › btnKaSpeichern` → OnSelect

```
If(
    varRueckPP > 0 || varKritPP > 0;
        Notify("Bitte zuerst die offene Frage im Fenster beantworten."; NotificationType.Warning);
    Value(lblKaFehlendAnzahl.Text) > 0;
        Set(varZeigeFehlend; true);;
        Set(varSprungRec; First(Filter(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge) As a; If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert; a.Kritisch && !a.KritischOk))));;
        Set(varKritPP; Coalesce(First(Sort(Filter(colAntworten As a; !a.Inaktiv && a.Bewertung = "NIO" && a.Kritisch && !a.KritischOk && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)).PruefpunktID; 0));;
        Reset(galKaPruefpunkte);
    !varIsLoading && Now() >= varSperreBis;
        Set(varIsLoading; true);;
        Set(varPatchFehler; false);;
        Concurrent(Refresh(RG_Durchfuehrungen); Refresh(RG_KategorieErgebnisse));;
        Concurrent(
            ClearCollect(colErledigt; ShowColumns(Filter(RG_KategorieErgebnisse; DurchfuehrungID = varDurchID); ID; KategorieID; AnzahlNIO; GespeichertAm; PrueferName));
            Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID))
        );;
        With({durch: varDurch; erg: LookUp(RG_KategorieErgebnisse; Title = varSchluesselK)};
            If(
                CountRows(Filter(colAntworten; !Inaktiv)) = 0;
                    Notify("Diese Kategorie hat keine aktiven Prüfpunkte. Bitte die Stammdaten prüfen lassen."; NotificationType.Error);
                Value(lblKaFehlendAnzahl.Text) > 0;
                    Notify("Bitte noch ausfüllen: " & lblKaFehlend.Text; NotificationType.Warning);
                durch.Status <> stInArbeit;
                    Notify("Der Rundgang ist nicht mehr in Arbeit – Änderungen sind nicht möglich."; NotificationType.Error);
                !IsBlank(erg) && erg.GespeichertAm <> varGespeichertBeimOeffnen;
                    Notify("Diese Kategorie wurde inzwischen von " & erg.PrueferName & " gespeichert. Bitte zurück und neu öffnen."; NotificationType.Error);
                ClearCollect(colVersteckt; ShowColumns(Filter(colAntworten As a; !a.Inaktiv && !(If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))); PruefpunktID));;
                ClearCollect(colFotoNeu; Filter(colFotos As f0; IsBlank(f0.Url) && With({a: LookUp(colAntworten As a0; a0.PruefpunktID = f0.PruefpunktID)}; !(a.PruefpunktID in colVersteckt.PruefpunktID) && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus))));;
                ForAll(colFotoNeu As f;
                    Patch(colFotos; LookUp(colFotos; Nr = f.Nr);
                        {Url: With({ordner: fnArchivOrdner(durch.TagText; durch.TestDatensatz) & "/" & durch.Title}; If(IsError(aRG_Foto_hochladen.Run({contentBytes: f.Bild; name: f.Datei}; f.Datei; ordner; varDurchID; f.PruefpunktID; durch.TestDatensatz)); ""; fnSpUrl("RG_Fotos"; ordner & "/" & f.Datei)))})
                );;
                If(CountRows(Filter(colFotos As f1; IsBlank(f1.Url) && With({a: LookUp(colAntworten As a1; a1.PruefpunktID = f1.PruefpunktID)}; !(a.PruefpunktID in colVersteckt.PruefpunktID) && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)))) > 0;
                    Notify(CountRows(Filter(colFotos As f2; IsBlank(f2.Url) && With({a: LookUp(colAntworten As a2; a2.PruefpunktID = f2.PruefpunktID)}; !(a.PruefpunktID in colVersteckt.PruefpunktID) && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)))) & " Foto(s) konnten nicht hochgeladen werden. Bitte „Speichern“ erneut tippen."; NotificationType.Error);
                    ForAll(Distinct(Filter(colFotos; !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID)); PruefpunktID) As d;
                        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = d.Value);
                            {Fotos: With({alt: LookUp(colAntworten; PruefpunktID = d.Value).Fotos; neu: Concat(Filter(colFotos; PruefpunktID = d.Value && !Uebernommen && !IsBlank(Url)); Url; " | ")};
                                If(IsBlank(alt); neu; alt & " | " & neu))})
                    );;
                    UpdateIf(colFotos; !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID); {Uebernommen: true});;
                    UpdateIf(colAntworten; !Inaktiv && !fnKommentarNoetig(Typ; Bewertung; WertText; WertZahl; KommentarPflicht; Grenzmodus; MinWert; MaxWert); {Kommentar: ""});;
                    UpdateIf(colAntworten; !Inaktiv; {Warnung: Typ = "ZAHL" && Grenzmodus = "Warnen" && fnAusserhalb(WertZahl; MinWert; MaxWert)});;
                    ClearCollect(colSpeichern; ForAll(colAntworten As r; If(r.PruefpunktID in colVersteckt.PruefpunktID; Patch(r; {Bewertung: ""; WertText: ""; WertZahl: Blank(); Kommentar: ""; Fotos: ""; Warnung: false; Ausgeblendet: true}); r.Inaktiv; r; Patch(r; {Ausgeblendet: false}))));;
                    ClearCollect(colAbsTmp; ShowColumns(Filter(colSpeichern; !Inaktiv && !Ausgeblendet && Abschnitt <> ""); PruefpunktID; Reihenfolge; Abschnitt));;
                    UpdateIf(colSpeichern; AbsKopf; {AbsKopf: false});;
                    ForAll(colAbsTmp As t;
                        Patch(colSpeichern; LookUp(colSpeichern; PruefpunktID = t.PruefpunktID);
                            {AbsKopf: t.Reihenfolge * 1000000 + t.PruefpunktID = Min(Filter(colAbsTmp As u; Lower(u.Abschnitt) = Lower(t.Abschnitt)); Reihenfolge * 1000000 + PruefpunktID)}
                        )
                    );;
                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit; KritischVon; TextIO; TextNIO; Letzter; LetzterTag; AbwText); JSONFormat.Compact));;
                    IfError(
                        Patch(RG_KategorieErgebnisse; If(IsBlank(erg); Defaults(RG_KategorieErgebnisse); erg);
                            {Title: varSchluesselK; DurchfuehrungID: varDurchID; TagText: durch.TagText; KategorieID: varKatID; Position: varKatPos; BereichName: varBereichName; KategorieName: varKatName; Antworten: varAntwortJSON; AnzahlNIO: CountRows(Filter(colSpeichern; Bewertung = "NIO")); PrueferEmail: varPruefer.Email; PrueferName: varPruefer.Name; GespeichertAm: Now(); TestDatensatz: durch.TestDatensatz});
                        Set(varPatchFehler; true)
                    );;
                    Refresh(RG_KategorieErgebnisse);;
                    Set(varNachlese; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK));;
                    If(varNachlese.Antworten = varAntwortJSON;
                        Set(varGeaendert; false);;
                        Clear(colFotos);;
                        Notify("Gespeichert."; NotificationType.Success);;
                        Set(varWeiter; true);;
                        Navigate(scrRundgang; ScreenTransition.None);
                        Notify("Speichern wurde nicht bestätigt. Bitte erneut tippen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error)
                    )
                )
            )
        );;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
)
```

```diff
- … ows(Filter(colSpeichern; Bewertung = "NIO")); PrueferEmail: User().Email; PrueferName: User().FullName; GespeichertAm: Now(); TestDatensatz: durch.TestDatensatz}); …
+ … ows(Filter(colSpeichern; Bewertung = "NIO")); PrueferEmail: varPruefer.Email; PrueferName: varPruefer.Name; GespeichertAm: Now(); TestDatensatz: durch.TestDatensatz}); …
```

**Kurz erklärt:** Prüfer der Kategorie = gewählte Person (statt `User()`).

**Nachprüfen:** endet auf `)`

### A3.7 · `btnKaKritOk.OnSelect`

**Pfad:** `scrKategorie › conKaKrit › conKaKritKarte › btnKaKritOk` → OnSelect

```
If(LookUp(colAntworten; PruefpunktID = varKritPP).Bewertung = "NIO"; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = varKritPP); {KritischOk: true; KritischZeit: Text(Now(); "dd.mm.yyyy hh:mm"); KritischVon: varPruefer.Name}));;
Set(varKritPP; 0);;
Set(varGeaendert; true)
```

```diff
-If(LookUp(colAntworten; PruefpunktID = varKritPP).Bewertung = "NIO"; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = varKritPP); {KritischOk: true; KritischZeit: Text(Now(); "dd.mm.yyyy hh:mm"); KritischVon: User().FullName}));;
+If(LookUp(colAntworten; PruefpunktID = varKritPP).Bewertung = "NIO"; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = varKritPP); {KritischOk: true; KritischZeit: Text(Now(); "dd.mm.yyyy hh:mm"); KritischVon: varPruefer.Name}));;
```

**Kurz erklärt:** „Bescheid gegeben“ mit dem Namen der gewählten Person.

**Nachprüfen:** endet auf `Set(varGeaendert; true)`

### A3.8 · `btnRuAbschluss.OnSelect`

**Pfad:** `scrRundgang › conRuFuss › btnRuAbschluss` → OnSelect

```
If(!varIsLoading && Now() >= varSperreBis;
    If(!varAbschlussFrage;
        Set(varUnterschriftDa; false);;
        Reset(penRuUnterschrift);;
        Set(varUnterschriftOffen; true);;
        Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));
        Set(varAbschlussFrage; false);;
        Set(varIsLoading; true);;
        Set(varPatchFehler; false);;
        Concurrent(Refresh(RG_Durchfuehrungen); Refresh(RG_KategorieErgebnisse));;
        Concurrent(
            Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));
            ClearCollect(colErgAlle; Filter(RG_KategorieErgebnisse; DurchfuehrungID = varDurchID))
        );;
        If(IsError(ClearCollect(colKatListe; ForAll(Table(ParseJSON(varDurch.KategorieListe)) As j; {KategorieID: Value(j.Value.KategorieID); Position: Value(j.Value.Position); BereichName: Text(j.Value.BereichName); KategorieName: Text(j.Value.KategorieName)}))); Clear(colKatListe));;
        If(
            !(varDurch.Status in [stInArbeit; stAbschluss]);
                Notify("Dieser Rundgang ist bereits abgeschlossen."; NotificationType.Information);
            CountRows(colKatListe) = 0 || CountRows(colKatListe) <> varDurch.AnzahlKategorien;
                Notify("Die Kategorienliste dieses Rundgangs ist unvollständig. Bitte zurück und erneut öffnen."; NotificationType.Error);
            CountRows(Filter(colKatListe As kl; IsBlank(LookUp(colErgAlle As e; e.KategorieID = kl.KategorieID)))) > 0;
                Notify("Es sind noch nicht alle Kategorien gespeichert."; NotificationType.Warning);
            If(varDurch.Status = stInArbeit && IsError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbschluss})); Set(varPatchFehler; true));;
            Refresh(RG_Durchfuehrungen);;
            Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));;
            If(varDurch.Status <> stAbschluss;
                Notify("Der Rundgang konnte nicht in den Abschluss gesetzt werden. Bitte erneut tippen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error);
                Refresh(RG_KategorieErgebnisse);;
                ClearCollect(colErgAlle; Filter(RG_KategorieErgebnisse; DurchfuehrungID = varDurchID));;
                If(IsError(
                    ClearCollect(colMaengelSoll;
                        Filter(Ungroup(
                            ForAll(Filter(colErgAlle; AnzahlNIO > 0) As e3;
                                {Zeilen: ForAll(Filter(Table(ParseJSON(e3.Antworten)) As a; Text(a.Value.Bewertung) = "NIO") As n;
                                    {Title: "D" & varDurchID & "-P" & Value(n.Value.PruefpunktID);
                                     PruefpunktID: Value(n.Value.PruefpunktID);
                                     BereichName: e3.BereichName;
                                     KategorieName: e3.KategorieName;
                                     Frage: Left(If(Coalesce(Text(n.Value.Abschnitt); "") = ""; ""; Text(n.Value.Abschnitt) & " › ") & Text(n.Value.Frage); 255);
                                     Wert: Left(Coalesce(Text(n.Value.WertText); "") & If(IsBlank(n.Value.WertZahl); ""; Text(Value(n.Value.WertZahl)) & " " & Coalesce(Text(n.Value.Einheit); "")); 255);
                                     Kommentar: If(Coalesce(IfError(Boolean(n.Value.Kritisch); false); false); "KRITISCH – Bescheid gegeben " & Coalesce(Text(n.Value.KritischZeit); "") & ". "; "") & Coalesce(Text(n.Value.Kommentar); "");
                             FotoUrls: Coalesce(Text(n.Value.Fotos); "")})}
                            );
                            Zeilen
                        ); !IsBlank(PruefpunktID))
                    ));
                    Clear(colMaengelSoll)
                );;
                If(Sum(colErgAlle; AnzahlNIO) <> CountRows(colMaengelSoll);
                    Notify("Die Mängel ließen sich nicht vollständig aus den Antworten ermitteln (" & CountRows(colMaengelSoll) & " von " & Sum(colErgAlle; AnzahlNIO) & "). Bitte den Rundgang melden."; NotificationType.Error);
                    Refresh(RG_Maengel);;
                    ClearCollect(colMaengelIst; ShowColumns(Filter(RG_Maengel; DurchfuehrungID = varDurchID); Title));;
                    IfError(
                        Collect(RG_Maengel;
                            ForAll(Filter(colMaengelSoll As s; IsBlank(LookUp(colMaengelIst As i; i.Title = s.Title))) As m;
                                {Title: m.Title; DurchfuehrungID: varDurchID; PruefpunktID: m.PruefpunktID; RundgangName: varDurch.RundgangName; BereichName: m.BereichName; KategorieName: m.KategorieName; Frage: m.Frage; Wert: m.Wert; Kommentar: m.Kommentar; FotoUrls: m.FotoUrls; FestgestelltAm: Now(); FestgestelltVon: varPruefer.Email; Status: {Value: "Offen"}; TestDatensatz: varDurch.TestDatensatz})
                        );
                        Set(varPatchFehler; true)
                    );;
                    Concurrent(Refresh(RG_Maengel); Refresh(RG_KategorieErgebnisse); Refresh(RG_Durchfuehrungen));;
                    Concurrent(
                        ClearCollect(colMaengelIst; ShowColumns(Filter(RG_Maengel; DurchfuehrungID = varDurchID); Title));
                        ClearCollect(colErgJetzt; ShowColumns(Filter(RG_KategorieErgebnisse; DurchfuehrungID = varDurchID); ID; GespeichertAm))
                    );;
                    If(
                        CountRows(Filter(colMaengelSoll As s2; IsBlank(LookUp(colMaengelIst As i2; i2.Title = s2.Title)))) > 0;
                            Notify("Die Mängel konnten nicht vollständig gespeichert werden. Bitte „Rundgang abschließen“ erneut tippen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error);
                        Concat(Sort(colErgJetzt; ID); ID & "@" & Text(GespeichertAm; "yyyy-mm-dd hh:mm:ss"); ";") <> Concat(Sort(colErgAlle; ID); ID & "@" & Text(GespeichertAm; "yyyy-mm-dd hh:mm:ss"); ";");
                            Notify("Während des Abschlusses wurde eine Kategorie gespeichert. Bitte „Rundgang abschließen“ erneut tippen."; NotificationType.Warning);
                        LookUp(RG_Durchfuehrungen; ID = varDurchID).Status <> stAbschluss;
                    Notify("Der Abschluss wurde inzwischen zurückgesetzt. Bitte die Übersicht neu öffnen."; NotificationType.Warning);
                        With({datei: "Unterschrift-D" & varDurchID & "-" & Text(Now(); "yyyymmdd-hhmmss") & ".png"; ordner: fnArchivOrdner(varDurch.TagText; varDurch.TestDatensatz) & "/" & varDurch.Title};
                            Set(varUnterschriftUrl; If(IsError(aRG_Foto_hochladen.Run({contentBytes: penRuUnterschrift.Image; name: datei}; datei; ordner; varDurchID; 0; varDurch.TestDatensatz)); ""; fnSpUrl("RG_Fotos"; ordner & "/" & datei)))
                        );;
                        IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSoll); UnterschriftBild: varUnterschriftBild; UnterschriftUrl: varUnterschriftUrl; UnterschriftName: varPruefer.Name; UnterschriftZeit: Now()}); Set(varPatchFehler; true));;
                        Refresh(RG_Durchfuehrungen);;
                        Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));;
                        If(varDurch.Status = stAbgeschlossen;
                            Notify("Rundgang abgeschlossen · " & CountRows(colMaengelSoll) & " Mängel erfasst. Protokoll wird archiviert …" & If(varUnterschriftUrl = ""; " (Unterschrift-Datei nicht hochgeladen, steht aber im Protokoll.)"; ""); NotificationType.Success);;
                                Set(varUnterschriftOffen; false);;
                                Set(varPruefer; {Name: ""; Email: ""});;
                                Set(varPrWahl; true);;
                                Set(varArchivStart; false);;
                                Navigate(scrProtokoll; ScreenTransition.None);
                            Notify("Der Abschluss wurde nicht bestätigt. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error)
                        )
                    )
                )
            )
        );;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
    )
)
```

```diff
-        Set(varAbschlussFrage; true);;
+        Set(varUnterschriftDa; false);;
+        Reset(penRuUnterschrift);;
+        Set(varUnterschriftOffen; true);;
- {Title: m.Title; DurchfuehrungID: varDurchID; PruefpunktID: m.PruefpunktID; RundgangName: varDurch.RundgangName; BereichName: m.BereichName; Kategor …
+ {Title: m.Title; DurchfuehrungID: varDurchID; PruefpunktID: m.PruefpunktID; RundgangName: varDurch.RundgangName; BereichName: m.BereichName; Kategor …
-                        IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSoll)}); Set(varPatchFehler; true));;
+                        With({datei: "Unterschrift-D" & varDurchID & "-" & Text(Now(); "yyyymmdd-hhmmss") & ".png"; ordner: fnArchivOrdner(varDurch.TagText; varDurch.TestDatensatz) & "/" & varDurch.Title};
+ Set(varUnterschriftUrl; If(IsError(aRG_Foto_hochladen.Run({contentBytes: penRuUnterschrift.Image; name: datei}; datei; ordner; varDurchID; 0; varDurch.T …
+                        );;
+ IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSol …
-                            Notify("Rundgang abgeschlossen · " & CountRows(colMaengelSoll) & " Mängel erfasst. Protokoll wird archiviert …"; NotificationType.Success);;
+ Notify("Rundgang abgeschlossen · " & CountRows(colMaengelSoll) & " Mängel erfasst. Protokoll wird archiviert …" & If(varUnterschriftUrl = ""; " (Untersc …
+                                Set(varUnterschriftOffen; false);;
+                                Set(varPruefer; {Name: ""; Email: ""});;
+                                Set(varPrWahl; true);;
```

**Kurz erklärt:** Erstes Tippen öffnet die Unterschrift (statt „Wirklich abschließen?“). Nach der Unterschrift läuft der bisherige Abschluss; zusätzlich: Unterschrift als PNG in `RG_Fotos` (Testablage wie Fotos), Bild und Link an der Durchführung, `FestgestelltVon` = gewählte Person. Danach ist kein Prüfer mehr gewählt.

**Nachprüfen:** endet auf `)`

### A3.9 · `htmProtokoll.HtmlText`

**Pfad:** `scrProtokoll › conPrInhalt › htmProtokoll` → HtmlText

```
With({d: varDurch; r: LookUp(RG_Rundgaenge; ID = varDurch.RundgangID)};
    "<div style='font-family:Segoe UI,Arial,sans-serif;font-size:14px;color:#1B1B1F'>" &
    "<div style='background:#171496;color:#ffffff;padding:14px 16px'>" &
        "<div style='font-size:20px;font-weight:600'>" & fnHtml(d.RundgangName) & "</div>" &
        If(Trim(Coalesce(r.Standort; "") & Coalesce(r.Adresse; "")) = ""; ""; "<div>" & fnHtml(Trim(Coalesce(r.Standort; "") & If(Coalesce(r.Standort; "") <> "" && Coalesce(r.Adresse; "") <> ""; " · "; "") & Coalesce(r.Adresse; ""))) & "</div>") &
        If(Trim(Coalesce(r.Auftraggeber; "")) = ""; ""; "<div>Auftraggeber: " & fnHtml(r.Auftraggeber) & "</div>") &
        "<div>" & fnTagAnzeige(DateValue(d.TagText)) & " · Prüfer: " & fnHtml(d.PrueferName) & "</div>" &
        "<div>Status: " & d.Status & " · Beginn " & Text(d.StartZeit; "hh:mm") & If(IsBlank(d.EndeZeit); ""; " · Ende " & Text(d.EndeZeit; "hh:mm")) & " · <b>" & Coalesce(d.AnzahlNIO; 0) & " n.i.O.</b></div>" &
    "</div>" &
    Concat(Sort(colErgProt; Position) As e;
        "<h3 style='margin:18px 0 6px 0;font-size:16px;color:#171496'>" & e.Position & ". " & fnHtml(e.KategorieName) &
        " <span style='font-weight:400;color:#5F6370;font-size:13px'>" & If(e.BereichName = ""; ""; fnHtml(e.BereichName) & " · ") & fnHtml(e.PrueferName) & " · " & Text(e.GespeichertAm; "hh:mm") & "</span></h3>" &
        "<table style='width:100%;border-collapse:collapse;table-layout:fixed'>" &
        Concat(Filter(Table(ParseJSON(e.Antworten)); !Coalesce(IfError(Boolean(ThisRecord.Value.Ausgeblendet); false); false)) As a;
            With({b: Text(a.Value.Bewertung); k: Text(a.Value.Kommentar); fo: Text(a.Value.Fotos); w: Coalesce(IfError(Boolean(a.Value.Warnung); false); false)};
                If(Coalesce(IfError(Boolean(a.Value.AbsKopf); false); false); "<tr><td colspan='3' style='padding:12px 8px 4px 8px;font-weight:600;color:#171496'>" & fnHtml(Text(a.Value.Abschnitt)) & "</td></tr>"; "") &
                "<tr style='border-bottom:1px solid #DADCE5;" & If(b = "NIO"; "background:#FCE8E6;"; "") & "'>" &
                "<td style='padding:6px 8px;width:46%'>" & fnHtml(Text(a.Value.Frage)) & "</td>" &
                "<td style='padding:6px 8px;width:110px;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; w; "#9A5B00"; "#0F7B3F") & "'>" & Switch(b; "IO"; fnHtml(Coalesce(If(Coalesce(Text(a.Value.TextIO); "") = ""; Blank(); Text(a.Value.TextIO)); "i.O.")); "NIO"; fnHtml(Coalesce(If(Coalesce(Text(a.Value.TextNIO); "") = ""; Blank(); Text(a.Value.TextNIO)); "n.i.O.")); "") & "</td>" &
                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) & If(w; " <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>"; "") & If(Coalesce(Text(a.Value.AbwText); "") = ""; ""; " <span style='color:#9A5B00'>(" & fnHtml(Text(a.Value.AbwText)) & If(IsBlank(a.Value.Letzter); ""; ", zuletzt " & Text(Value(a.Value.Letzter))) & ", begründet)</span>") &
                If(IsBlank(k) || k = ""; ""; "<br><i style='color:" & If(b = "NIO"; "#B3261E"; "#5F6370") & "'>" & fnHtml(k) & "</i>") &
                If(b = "NIO" && Coalesce(IfError(Boolean(a.Value.Kritisch); false); false); "<br><b style='color:#B3261E'>KRITISCH – " & If(Coalesce(IfError(Boolean(a.Value.KritischOk); false); false); "Bescheid gegeben, bestätigt von " & fnHtml(Coalesce(Text(a.Value.KritischVon); e.PrueferName)) & " am " & fnHtml(Coalesce(Text(a.Value.KritischZeit); "")); "nicht bestätigt") & "</b>"; "") &
                If(IsBlank(fo) || fo = ""; ""; "<br>" & Concat(Split(fo; " | ") As s; "<a href='" & Trim(s.Value) & "'>Foto ›</a> ")) &
                "</td></tr>"
            )
        ) & "</table>"
    ) &
    If(Coalesce(d.UnterschriftBild; "") = ""; ""; "<div style='margin-top:22px'><img src='" & d.UnterschriftBild & "' style='height:90px'>" &
        "<div style='border-top:1px solid #1B1B1F;width:300px;padding-top:4px;font-size:12px'>" & fnHtml(Coalesce(d.UnterschriftName; d.PrueferName)) & " · " & Text(d.UnterschriftZeit; "dd.mm.yyyy hh:mm") & "</div></div>") &
    If(IsBlank(d.ProtokollUrl); ""; "<p style='font-size:12px'>Archiv-PDF: <a href='" & d.ProtokollUrl & "'>" & fnHtml(d.Title) & ".pdf</a></p>") &
    "<p style='color:#5F6370;font-size:12px;margin-top:18px'>Erstellt mit der Rundgang-App · " & Text(varProtokollZeit; "dd.mm.yyyy hh:mm") & If(d.TestDatensatz; " · TESTDATEN"; "") & "</p></div>"
)
```

```diff
-With({d: varDurch};
+With({d: varDurch; r: LookUp(RG_Rundgaenge; ID = varDurch.RundgangID)};
+ If(Trim(Coalesce(r.Standort; "") & Coalesce(r.Adresse; "")) = ""; ""; "<div>" & fnHtml(Trim(Coalesce(r.Standort; "") & If(Coalesce(r.Standort; "") <> "" && Coalesce(r.Adres …
+        If(Trim(Coalesce(r.Auftraggeber; "")) = ""; ""; "<div>Auftraggeber: " & fnHtml(r.Auftraggeber) & "</div>") &
+    If(Coalesce(d.UnterschriftBild; "") = ""; ""; "<div style='margin-top:22px'><img src='" & d.UnterschriftBild & "' style='height:90px'>" &
+        "<div style='border-top:1px solid #1B1B1F;width:300px;padding-top:4px;font-size:12px'>" & fnHtml(Coalesce(d.UnterschriftName; d.PrueferName)) & " · " & Text(d.UnterschriftZeit; "dd.mm.yyyy hh:mm") & "</div></div>") &
```

**Kurz erklärt:** Kopf: Standort · Adresse, Auftraggeber (wenn gepflegt), dann wie bisher Datum mit KW und Prüfer. Unten: Unterschrift mit Name, Datum, Uhrzeit (auch im Archiv-PDF).

**Nachprüfen:** endet auf `)`

## Teil B – Builder

### B0 – Daten

Spalten und Liste aus A1 (nur einmal anlegen). Builder: `RG_Rundgaenge` aktualisieren, `RG_Pruefer` und **Office 365-Benutzer** hinzufügen.

### B1.1 – neues Steuerelement `btnKoPruefer`

**Wo hin:** **`conKoKopf`** markieren → Strg+V.

```yaml
- btnKoPruefer:
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
      OnSelect: =If(!varIsLoading, Navigate(scrPruefer, ScreenTransition.None))
      PressedColor: =Color.White
      PressedFill: =RGBA(255, 255, 255, 0.32)
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =14
      Text: ="👤 Prüfer ›"
      Width: =180
      X: =Parent.Width - 196
      Y: =12
```

### B1.2 – neues Steuerelement `lblPlAdresseT`

**Wo hin:** **`scrPlan`** markieren → Strg+V.

```yaml
- lblPlAdresseT:
    Control: Label@2.5.1
    Properties:
      Color: =clrTextGrau
      Font: =Font.'Segoe UI'
      Height: =20
      Size: =12
      Text: ="Adresse"
      Width: =320
      X: =336
      Y: =Parent.Height - 128
```

### B1.3 – neues Steuerelement `lblPlAuftragT`

**Wo hin:** **`scrPlan`** markieren → Strg+V.

```yaml
- lblPlAuftragT:
    Control: Label@2.5.1
    Properties:
      Color: =clrTextGrau
      Font: =Font.'Segoe UI'
      Height: =20
      Size: =12
      Text: ="Auftraggeber (optional)"
      Width: =290
      X: =668
      Y: =Parent.Height - 128
```

### B1.4 – neues Steuerelement `lblPlKopfT`

**Wo hin:** **`scrPlan`** markieren → Strg+V.

```yaml
- lblPlKopfT:
    Control: Label@2.5.1
    Properties:
      Color: =clrText
      Font: =Font.'Segoe UI'
      FontWeight: =FontWeight.Semibold
      Height: =24
      Size: =13
      Text: ="Kopfdaten für das Protokoll"
      Width: =600
      X: =24
      Y: =Parent.Height - 154
```

### B1.5 – neues Steuerelement `lblPlStandortT`

**Wo hin:** **`scrPlan`** markieren → Strg+V.

```yaml
- lblPlStandortT:
    Control: Label@2.5.1
    Properties:
      Color: =clrTextGrau
      Font: =Font.'Segoe UI'
      Height: =20
      Size: =12
      Text: ="Standort"
      Width: =300
      X: =24
      Y: =Parent.Height - 128
```

### B1.6 – neuer Bildschirm `scrPruefer`

**Wo hin:** einen Bildschirm markieren → Strg+V.

```yaml
Screens:
  scrPruefer:
    Properties:
      Fill: =clrHintergrund
      OnVisible: |-
        =Set(varIsLoading, true);
        Set(varLadeText, "");
        Refresh(RG_Pruefer);
        ClearCollect(colPfAlle, RG_Pruefer);
        Reset(txtPfSuche);
        Set(varIsLoading, false)
    Children:
      - conPfKopf:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrPrimaer
            Height: =64
            Width: =Parent.Width
          Children:
            - btnPfZurueck:
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
                  OnSelect: =If(!varIsLoading, Navigate(scrKontakte, ScreenTransition.None))
                  PressedColor: =Color.White
                  PressedFill: =RGBA(255, 255, 255, 0.32)
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =14
                  Text: ="← Ansprechpartner"
                  Width: =210
                  X: =16
                  Y: =12
            - lblPfTitelKopf:
                Control: Label@2.5.1
                Properties:
                  Color: =Color.White
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =64
                  Size: =20
                  Text: ="Prüfer"
                  Width: =600
                  X: =242
                  Y: =0
      - lblPfHilfe:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =44
            Size: =13
            Text: |-
              ="Diese Personen erscheinen in der Rundgang-App zum Antippen. Jeder Mitarbeiter darf prüfen: Vertretungen sucht der Prüfer dort selbst, sie kommen dann automatisch hierher. Nicht mehr gebraucht: auf „inaktiv“ tippen (nicht löschen)."
            Width: =Parent.Width - 48
            X: =24
            Y: =72
      - galPf:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            AccessibleLabel: ="Prüfer"
            Height: =Parent.Height - 140
            Items: =Sort(colPfAlle, If(Coalesce(Aktiv, false), "0", "1") & Lower(Title))
            ShowScrollbar: =true
            TemplatePadding: =0
            TemplateSize: =60
            Width: =620
            X: =24
            Y: =124
          Children:
            - lblPfName:
                Control: Label@2.5.1
                Properties:
                  Color: =If(Coalesce(ThisItem.Aktiv, false), clrText, clrTextGrau)
                  Font: =Font.'Segoe UI'
                  Height: =Parent.TemplateHeight - 4
                  Size: =14
                  Text: =ThisItem.Title & "  ·  " & Coalesce(ThisItem.Email, "")
                  Width: =Parent.TemplateWidth - 160
                  Wrap: =false
                  X: =12
                  Y: =0
            - btnPfAktiv:
                Control: Classic/Button@2.2.0
                Properties:
                  BorderColor: =clrPrimaer
                  BorderThickness: =1
                  Color: =clrPrimaer
                  DisabledBorderColor: =clrGesperrtHell
                  DisabledColor: =clrGesperrt
                  DisabledFill: =clrGesperrtHell
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =If(Coalesce(ThisItem.Aktiv, false), clrPrimaerHell, clrKarte)
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HoverColor: =clrPrimaer
                  HoverFill: =clrPrimaerHell
                  OnSelect: |-
                    =If(!varIsLoading && Now() >= varSperreBis,
                        Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));
                        Set(varPatchFehler, false);
                        IfError(Patch(RG_Pruefer, LookUp(RG_Pruefer, ID = ThisItem.ID), {Aktiv: !Coalesce(ThisItem.Aktiv, false)}), Set(varPatchFehler, true));
                        If(varPatchFehler,
                            Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                            Patch(colPfAlle, LookUp(colPfAlle, ID = ThisItem.ID), LookUp(RG_Pruefer, ID = ThisItem.ID))
                        )
                    )
                  PressedColor: =clrPrimaer
                  PressedFill: =clrPrimaerHell
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =13
                  Text: =If(Coalesce(ThisItem.Aktiv, false), "aktiv", "inaktiv")
                  Width: =128
                  X: =Parent.TemplateWidth - 140
                  Y: =8
      - lblPfLeer:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =48
            Size: =13
            Text: ="Noch keine Prüfer. Rechts nach Namen suchen."
            Visible: =IsEmpty(colPfAlle) && !varIsLoading
            Width: =620
            X: =24
            Y: =134
      - lblPfSuchT:
          Control: Label@2.5.1
          Properties:
            Color: =clrText
            Font: =Font.'Segoe UI'
            FontWeight: =FontWeight.Semibold
            Height: =24
            Size: =13
            Text: ="Person aus dem Firmenverzeichnis hinzufügen"
            Width: =Parent.Width - 692
            X: =668
            Y: =124
      - txtPfSuche:
          Control: Classic/TextInput@2.3.2
          Properties:
            AccessibleLabel: ="Name suchen"
            BorderColor: =clrRahmen
            Color: =clrText
            Default: =""
            DelayOutput: =true
            DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
            Fill: =clrKarte
            FocusedBorderColor: =clrPrimaer
            Font: =Font.'Segoe UI'
            Height: =44
            HintText: ="Name eingeben (mind. 3 Buchstaben)"
            HoverBorderColor: =clrPrimaer
            OnChange: =false
            Size: =14
            Width: =Parent.Width - 692
            X: =668
            Y: =152
      - galPfSuche:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            AccessibleLabel: ="Suchergebnisse"
            Height: =Parent.Height - 220
            Items: |-
              =If(Len(Trim(txtPfSuche.Text)) >= 3, Filter(Office365Users.SearchUserV2({searchTerm: Trim(txtPfSuche.Text), top: 15, isSearchTermRequired: true}).value, !IsBlank(Mail) && AccountEnabled))
            ShowScrollbar: =true
            TemplatePadding: =0
            TemplateSize: =56
            Width: =Parent.Width - 692
            X: =668
            Y: =204
          Children:
            - btnPfNeu:
                Control: Classic/Button@2.2.0
                Properties:
                  Align: =Align.Left
                  BorderColor: =clrPrimaer
                  BorderThickness: =1
                  Color: =clrPrimaer
                  DisabledBorderColor: =clrGesperrtHell
                  DisabledColor: =clrGesperrt
                  DisabledFill: =clrGesperrtHell
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  Font: =Font.'Segoe UI'
                  Height: =48
                  HoverColor: =clrPrimaer
                  HoverFill: =clrPrimaerHell
                  OnSelect: |-
                    =If(!varIsLoading && Now() >= varSperreBis,
                        Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));
                        With({e: Lower(ThisItem.Mail), alt: LookUp(colPfAlle, Lower(Email) = Lower(ThisItem.Mail))},
                            Set(varPatchFehler, false);
                            If(IsBlank(alt),
                                If(IsError(Patch(RG_Pruefer, Defaults(RG_Pruefer), {Title: ThisItem.DisplayName, Email: e, Aktiv: true})), Set(varPatchFehler, true)),
                                !Coalesce(alt.Aktiv, false),
                                If(IsError(Patch(RG_Pruefer, LookUp(RG_Pruefer, ID = alt.ID), {Aktiv: true})), Set(varPatchFehler, true))
                            );
                            Refresh(RG_Pruefer);
                            ClearCollect(colPfAlle, RG_Pruefer);
                            If(varPatchFehler, Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error), Notify(ThisItem.DisplayName & " ist in der Prüferliste.", NotificationType.Success))
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
                  Text: ="+ " & ThisItem.DisplayName & If(Coalesce(ThisItem.Department, "") = "", "", "  ·  " & ThisItem.Department)
                  Width: =Parent.TemplateWidth
                  X: =0
                  Y: =4
      - conPfLaden:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =RGBA(255, 255, 255, 0.7)
            Height: =Parent.Height
            Visible: =varIsLoading
            Width: =Parent.Width
          Children:
            - btnPfLadenSperre:
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
            - lblPfLadenText:
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

### B1.7 – neues Steuerelement `txtPlAdresse`

**Wo hin:** **`scrPlan`** markieren → Strg+V.

```yaml
- txtPlAdresse:
    Control: Classic/TextInput@2.3.2
    Properties:
      AccessibleLabel: ="Adresse"
      BorderColor: =clrRahmen
      Color: =clrText
      Default: =Coalesce(varPlanRg.Adresse, "")
      DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
      Fill: =clrKarte
      FocusedBorderColor: =clrPrimaer
      Font: =Font.'Segoe UI'
      Height: =40
      HintText: ="z. B. Matthäus-Merian-Straße 6, 34253 Lohfelden"
      HoverBorderColor: =clrPrimaer
      OnChange: |-
        =If(varPlanRgID > 0 && !varIsLoading && Trim(Self.Text) <> Trim(Coalesce(varPlanRg.Adresse, "")),
            Set(varPatchFehler, false);
            IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varPlanRgID), {Adresse: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
            If(varPatchFehler,
                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                Refresh(RG_Rundgaenge);
                Set(varPlanRg, LookUp(RG_Rundgaenge, ID = varPlanRgID));
                Patch(colRg, LookUp(colRg, ID = varPlanRgID), varPlanRg)
            )
        )
      Size: =14
      Width: =320
      X: =336
      Y: =Parent.Height - 108
```

### B1.8 – neues Steuerelement `txtPlAuftrag`

**Wo hin:** **`scrPlan`** markieren → Strg+V.

```yaml
- txtPlAuftrag:
    Control: Classic/TextInput@2.3.2
    Properties:
      AccessibleLabel: ="Auftraggeber"
      BorderColor: =clrRahmen
      Color: =clrText
      Default: =Coalesce(varPlanRg.Auftraggeber, "")
      DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
      Fill: =clrKarte
      FocusedBorderColor: =clrPrimaer
      Font: =Font.'Segoe UI'
      Height: =40
      HintText: ="optional"
      HoverBorderColor: =clrPrimaer
      OnChange: |-
        =If(varPlanRgID > 0 && !varIsLoading && Trim(Self.Text) <> Trim(Coalesce(varPlanRg.Auftraggeber, "")),
            Set(varPatchFehler, false);
            IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varPlanRgID), {Auftraggeber: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
            If(varPatchFehler,
                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                Refresh(RG_Rundgaenge);
                Set(varPlanRg, LookUp(RG_Rundgaenge, ID = varPlanRgID));
                Patch(colRg, LookUp(colRg, ID = varPlanRgID), varPlanRg)
            )
        )
      Size: =14
      Width: =290
      X: =668
      Y: =Parent.Height - 108
```

### B1.9 – neues Steuerelement `txtPlStandort`

**Wo hin:** **`scrPlan`** markieren → Strg+V.

```yaml
- txtPlStandort:
    Control: Classic/TextInput@2.3.2
    Properties:
      AccessibleLabel: ="Standort"
      BorderColor: =clrRahmen
      Color: =clrText
      Default: =Coalesce(varPlanRg.Standort, "")
      DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
      Fill: =clrKarte
      FocusedBorderColor: =clrPrimaer
      Font: =Font.'Segoe UI'
      Height: =40
      HintText: ="z. B. TGI Lohfelden"
      HoverBorderColor: =clrPrimaer
      OnChange: |-
        =If(varPlanRgID > 0 && !varIsLoading && Trim(Self.Text) <> Trim(Coalesce(varPlanRg.Standort, "")),
            Set(varPatchFehler, false);
            IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varPlanRgID), {Standort: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
            If(varPatchFehler,
                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                Refresh(RG_Rundgaenge);
                Set(varPlanRg, LookUp(RG_Rundgaenge, ID = varPlanRgID));
                Patch(colRg, LookUp(colRg, ID = varPlanRgID), varPlanRg)
            )
        )
      Size: =14
      Width: =300
      X: =24
      Y: =Parent.Height - 108
```

### B2.1 · `galPl.Height`

**Pfad:** `scrPlan › galPl` → Height

```
Parent.Height - 300
```

```diff
-Parent.Height - 220
+Parent.Height - 300
```

**Kurz erklärt:** Platz für die Kopfdaten unten.

**Nachprüfen:** endet auf `Parent.Height - 300`

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | App neu starten | Vollbild „Wer prüft?“; ohne Auswahl geht nichts |
| T2 | „Andere Person suchen“: 3 Buchstaben eines Kollegen | Treffer mit Abteilung; antippen → Startseite, oben „Name · wechseln ›“; Kollege steht jetzt in `RG_Pruefer` |
| T3 | Name oben antippen → anderen wählen | Wechsel ohne Neustart |
| T4 | Rundgang starten, Kategorie speichern | `PrueferName`/`PrueferEmail` = gewählte Person, `Geraetekonto` = Gerätekonto |
| T5 | „Rundgang abschließen“ | Unterschriftsfeld; Knopf gesperrt bis gezeichnet; „Löschen“ leert; „Abbrechen“ schließt ohne Abschluss |
| T6 | Unterschreiben und abschließen | Protokoll unten mit Unterschrift, Name, Datum, Uhrzeit; PNG im Ordner des Laufs (`TEST/…` bei Testrundgang); `UnterschriftUrl` gefüllt |
| T7 | Zurück zur Startseite | „Wer prüft?“ erscheint wieder |
| T8 | Builder › Plan: Standort/Adresse/Auftraggeber eintragen | Protokollkopf zeigt sie (neu geöffnetes Protokoll) |
| T9 | Builder › Ansprechpartner › 👤 Prüfer: Person suchen, „+“; Eintrag inaktiv | erscheint/verschwindet in der App-Auswahl (nach Neustart der Startseite) |
| T10 | Archiv-PDF des Laufs öffnen | Unterschrift sichtbar (U3) |

## Rückweg

Vorher-Fassungen einsetzen; neue Steuerelemente und Bildschirm löschen. Listen/Spalten dürfen bleiben.

## Anhang – Vorher-Fassungen

**Rundgang DEV `App.OnStart` vorher**

```
Set(varHeute; Today());;
Set(varTag; Today());;
Set(varTagText; Text(Today(); "yyyy-mm-dd"));;
Set(varIsLoading; false);;
Set(varSperreBis; Now());;
Set(varPatchFehler; false);;
Set(varRgID; 0);;
Set(varSchluessel; "");;
Set(varDurchID; 0);;
Set(varDurch; Defaults(RG_Durchfuehrungen));;
Set(varKatID; 0);;
Set(varKatPos; 0);;
Set(varKatName; "");;
Set(varBereichName; "");;
Set(varSchluesselK; "");;
Set(varErgebnis; Defaults(RG_KategorieErgebnisse));;
Set(varNachlese; Defaults(RG_KategorieErgebnisse));;
Set(varGespeichertBeimOeffnen; Defaults(RG_KategorieErgebnisse).GespeichertAm);;
Set(varAntwortJSON; "");;
Set(varNurLesen; false);;
Set(varAbschlussFrage; false);;
Set(varZurueckFrage; false);;
Set(varGeaendert; false);;
Set(varAlleIOFrage; false);;
Set(varProtokollZeit; Now());;
Set(varIstAdmin; CountRows(Filter(Split(Lower(cfgAdmins); ";") As a; Trim(a.Value) = Lower(User().Email))) > 0);;
Set(varZuruecksetzenFrage; false);;
Set(varWeiter; false);;
Set(varZeigeFehlend; false);;
Set(varFotoPP; 0);;
Set(varArchivStart; false)
```

**Rundgang DEV `scrStart.OnVisible` vorher**

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

**Rundgang DEV `lblStartNutzer.Text` vorher**

```
User().FullName & If(cfgTestmodus; "  ·  TESTMODUS"; "")
```

**Rundgang DEV `lblStartNutzer.OnSelect` vorher**

```
false
```

**Rundgang DEV `btnRgAktion.OnSelect` vorher**

```
If(!varIsLoading && Now() >= varSperreBis;
    Set(varIsLoading; true);;
    Set(varPatchFehler; false);;
    Set(varRgID; ThisItem.ID);;
    Set(varSchluessel; "R" & ThisItem.ID & "-" & varTagText);;
    Refresh(RG_Durchfuehrungen);;
    Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
    If(varDurchID = 0;
        If(DateDiff(varTag; varHeute; TimeUnit.Days) < 0 || DateDiff(varTag; varHeute; TimeUnit.Days) > cfgNachholTage;
            Notify("Für diesen Tag kann kein Rundgang gestartet werden."; NotificationType.Error);
            With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k: Filter(RG_Kategorien; Aktiv = true)};
                With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName; If(Coalesce(LookUp(b As be3; be3.ID = BereichID).Ausblenden; false); ""; LookUp(b As be4; be4.ID = BereichID).Title)); BReihe * 10000 + RgReihenfolge)};
                    ClearCollect(colKatBau; ForAll(Sequence(CountRows(kk)) As s; With({z: Index(kk; s.Value)}; {KategorieID: z.ID; Position: s.Value; BereichName: z.BName; KategorieName: z.Title})))
                )
            );;
            If(CountRows(colKatBau) = 0;
                Notify("Für diesen Rundgang sind keine aktiven Kategorien hinterlegt."; NotificationType.Error);
                IfError(
                    Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: ISOWeekNum(varTag); Wochentag: Weekday(varTag; StartOfWeek.Monday); Status: stInArbeit; AnzahlKategorien: CountRows(colKatBau); KategorieListe: JSON(colKatBau; JSONFormat.Compact); PrueferEmail: User().Email; PrueferName: User().FullName; StartZeit: Now(); TestDatensatz: Coalesce(ThisItem.Testrundgang; false)});
                    Set(varPatchFehler; true)
                );;
                Refresh(RG_Durchfuehrungen);;
                Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
                If(varDurchID = 0; Notify("Der Rundgang konnte nicht gestartet werden. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error))
            )
        )
    );;
    If(varDurchID > 0; Navigate(scrRundgang; ScreenTransition.None));;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
)
```

**Rundgang DEV `btnKaSpeichern.OnSelect` vorher**

```
If(
    varRueckPP > 0 || varKritPP > 0;
        Notify("Bitte zuerst die offene Frage im Fenster beantworten."; NotificationType.Warning);
    Value(lblKaFehlendAnzahl.Text) > 0;
        Set(varZeigeFehlend; true);;
        Set(varSprungRec; First(Filter(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge) As a; If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert; a.Kritisch && !a.KritischOk))));;
        Set(varKritPP; Coalesce(First(Sort(Filter(colAntworten As a; !a.Inaktiv && a.Bewertung = "NIO" && a.Kritisch && !a.KritischOk && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)).PruefpunktID; 0));;
        Reset(galKaPruefpunkte);
    !varIsLoading && Now() >= varSperreBis;
        Set(varIsLoading; true);;
        Set(varPatchFehler; false);;
        Concurrent(Refresh(RG_Durchfuehrungen); Refresh(RG_KategorieErgebnisse));;
        Concurrent(
            ClearCollect(colErledigt; ShowColumns(Filter(RG_KategorieErgebnisse; DurchfuehrungID = varDurchID); ID; KategorieID; AnzahlNIO; GespeichertAm; PrueferName));
            Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID))
        );;
        With({durch: varDurch; erg: LookUp(RG_KategorieErgebnisse; Title = varSchluesselK)};
            If(
                CountRows(Filter(colAntworten; !Inaktiv)) = 0;
                    Notify("Diese Kategorie hat keine aktiven Prüfpunkte. Bitte die Stammdaten prüfen lassen."; NotificationType.Error);
                Value(lblKaFehlendAnzahl.Text) > 0;
                    Notify("Bitte noch ausfüllen: " & lblKaFehlend.Text; NotificationType.Warning);
                durch.Status <> stInArbeit;
                    Notify("Der Rundgang ist nicht mehr in Arbeit – Änderungen sind nicht möglich."; NotificationType.Error);
                !IsBlank(erg) && erg.GespeichertAm <> varGespeichertBeimOeffnen;
                    Notify("Diese Kategorie wurde inzwischen von " & erg.PrueferName & " gespeichert. Bitte zurück und neu öffnen."; NotificationType.Error);
                ClearCollect(colVersteckt; ShowColumns(Filter(colAntworten As a; !a.Inaktiv && !(If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))); PruefpunktID));;
                ClearCollect(colFotoNeu; Filter(colFotos As f0; IsBlank(f0.Url) && With({a: LookUp(colAntworten As a0; a0.PruefpunktID = f0.PruefpunktID)}; !(a.PruefpunktID in colVersteckt.PruefpunktID) && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus))));;
                ForAll(colFotoNeu As f;
                    Patch(colFotos; LookUp(colFotos; Nr = f.Nr);
                        {Url: With({ordner: fnArchivOrdner(durch.TagText; durch.TestDatensatz) & "/" & durch.Title}; If(IsError(aRG_Foto_hochladen.Run({contentBytes: f.Bild; name: f.Datei}; f.Datei; ordner; varDurchID; f.PruefpunktID; durch.TestDatensatz)); ""; fnSpUrl("RG_Fotos"; ordner & "/" & f.Datei)))})
                );;
                If(CountRows(Filter(colFotos As f1; IsBlank(f1.Url) && With({a: LookUp(colAntworten As a1; a1.PruefpunktID = f1.PruefpunktID)}; !(a.PruefpunktID in colVersteckt.PruefpunktID) && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)))) > 0;
                    Notify(CountRows(Filter(colFotos As f2; IsBlank(f2.Url) && With({a: LookUp(colAntworten As a2; a2.PruefpunktID = f2.PruefpunktID)}; !(a.PruefpunktID in colVersteckt.PruefpunktID) && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)))) & " Foto(s) konnten nicht hochgeladen werden. Bitte „Speichern“ erneut tippen."; NotificationType.Error);
                    ForAll(Distinct(Filter(colFotos; !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID)); PruefpunktID) As d;
                        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = d.Value);
                            {Fotos: With({alt: LookUp(colAntworten; PruefpunktID = d.Value).Fotos; neu: Concat(Filter(colFotos; PruefpunktID = d.Value && !Uebernommen && !IsBlank(Url)); Url; " | ")};
                                If(IsBlank(alt); neu; alt & " | " & neu))})
                    );;
                    UpdateIf(colFotos; !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID); {Uebernommen: true});;
                    UpdateIf(colAntworten; !Inaktiv && !fnKommentarNoetig(Typ; Bewertung; WertText; WertZahl; KommentarPflicht; Grenzmodus; MinWert; MaxWert); {Kommentar: ""});;
                    UpdateIf(colAntworten; !Inaktiv; {Warnung: Typ = "ZAHL" && Grenzmodus = "Warnen" && fnAusserhalb(WertZahl; MinWert; MaxWert)});;
                    ClearCollect(colSpeichern; ForAll(colAntworten As r; If(r.PruefpunktID in colVersteckt.PruefpunktID; Patch(r; {Bewertung: ""; WertText: ""; WertZahl: Blank(); Kommentar: ""; Fotos: ""; Warnung: false; Ausgeblendet: true}); r.Inaktiv; r; Patch(r; {Ausgeblendet: false}))));;
                    ClearCollect(colAbsTmp; ShowColumns(Filter(colSpeichern; !Inaktiv && !Ausgeblendet && Abschnitt <> ""); PruefpunktID; Reihenfolge; Abschnitt));;
                    UpdateIf(colSpeichern; AbsKopf; {AbsKopf: false});;
                    ForAll(colAbsTmp As t;
                        Patch(colSpeichern; LookUp(colSpeichern; PruefpunktID = t.PruefpunktID);
                            {AbsKopf: t.Reihenfolge * 1000000 + t.PruefpunktID = Min(Filter(colAbsTmp As u; Lower(u.Abschnitt) = Lower(t.Abschnitt)); Reihenfolge * 1000000 + PruefpunktID)}
                        )
                    );;
                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit; KritischVon; TextIO; TextNIO; Letzter; LetzterTag; AbwText); JSONFormat.Compact));;
                    IfError(
                        Patch(RG_KategorieErgebnisse; If(IsBlank(erg); Defaults(RG_KategorieErgebnisse); erg);
                            {Title: varSchluesselK; DurchfuehrungID: varDurchID; TagText: durch.TagText; KategorieID: varKatID; Position: varKatPos; BereichName: varBereichName; KategorieName: varKatName; Antworten: varAntwortJSON; AnzahlNIO: CountRows(Filter(colSpeichern; Bewertung = "NIO")); PrueferEmail: User().Email; PrueferName: User().FullName; GespeichertAm: Now(); TestDatensatz: durch.TestDatensatz});
                        Set(varPatchFehler; true)
                    );;
                    Refresh(RG_KategorieErgebnisse);;
                    Set(varNachlese; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK));;
                    If(varNachlese.Antworten = varAntwortJSON;
                        Set(varGeaendert; false);;
                        Clear(colFotos);;
                        Notify("Gespeichert."; NotificationType.Success);;
                        Set(varWeiter; true);;
                        Navigate(scrRundgang; ScreenTransition.None);
                        Notify("Speichern wurde nicht bestätigt. Bitte erneut tippen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error)
                    )
                )
            )
        );;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
)
```

**Rundgang DEV `btnKaKritOk.OnSelect` vorher**

```
If(LookUp(colAntworten; PruefpunktID = varKritPP).Bewertung = "NIO"; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = varKritPP); {KritischOk: true; KritischZeit: Text(Now(); "dd.mm.yyyy hh:mm"); KritischVon: User().FullName}));;
Set(varKritPP; 0);;
Set(varGeaendert; true)
```

**Rundgang DEV `btnRuAbschluss.OnSelect` vorher**

```
If(!varIsLoading && Now() >= varSperreBis;
    If(!varAbschlussFrage;
        Set(varAbschlussFrage; true);;
        Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));
        Set(varAbschlussFrage; false);;
        Set(varIsLoading; true);;
        Set(varPatchFehler; false);;
        Concurrent(Refresh(RG_Durchfuehrungen); Refresh(RG_KategorieErgebnisse));;
        Concurrent(
            Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));
            ClearCollect(colErgAlle; Filter(RG_KategorieErgebnisse; DurchfuehrungID = varDurchID))
        );;
        If(IsError(ClearCollect(colKatListe; ForAll(Table(ParseJSON(varDurch.KategorieListe)) As j; {KategorieID: Value(j.Value.KategorieID); Position: Value(j.Value.Position); BereichName: Text(j.Value.BereichName); KategorieName: Text(j.Value.KategorieName)}))); Clear(colKatListe));;
        If(
            !(varDurch.Status in [stInArbeit; stAbschluss]);
                Notify("Dieser Rundgang ist bereits abgeschlossen."; NotificationType.Information);
            CountRows(colKatListe) = 0 || CountRows(colKatListe) <> varDurch.AnzahlKategorien;
                Notify("Die Kategorienliste dieses Rundgangs ist unvollständig. Bitte zurück und erneut öffnen."; NotificationType.Error);
            CountRows(Filter(colKatListe As kl; IsBlank(LookUp(colErgAlle As e; e.KategorieID = kl.KategorieID)))) > 0;
                Notify("Es sind noch nicht alle Kategorien gespeichert."; NotificationType.Warning);
            If(varDurch.Status = stInArbeit && IsError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbschluss})); Set(varPatchFehler; true));;
            Refresh(RG_Durchfuehrungen);;
            Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));;
            If(varDurch.Status <> stAbschluss;
                Notify("Der Rundgang konnte nicht in den Abschluss gesetzt werden. Bitte erneut tippen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error);
                Refresh(RG_KategorieErgebnisse);;
                ClearCollect(colErgAlle; Filter(RG_KategorieErgebnisse; DurchfuehrungID = varDurchID));;
                If(IsError(
                    ClearCollect(colMaengelSoll;
                        Filter(Ungroup(
                            ForAll(Filter(colErgAlle; AnzahlNIO > 0) As e3;
                                {Zeilen: ForAll(Filter(Table(ParseJSON(e3.Antworten)) As a; Text(a.Value.Bewertung) = "NIO") As n;
                                    {Title: "D" & varDurchID & "-P" & Value(n.Value.PruefpunktID);
                                     PruefpunktID: Value(n.Value.PruefpunktID);
                                     BereichName: e3.BereichName;
                                     KategorieName: e3.KategorieName;
                                     Frage: Left(If(Coalesce(Text(n.Value.Abschnitt); "") = ""; ""; Text(n.Value.Abschnitt) & " › ") & Text(n.Value.Frage); 255);
                                     Wert: Left(Coalesce(Text(n.Value.WertText); "") & If(IsBlank(n.Value.WertZahl); ""; Text(Value(n.Value.WertZahl)) & " " & Coalesce(Text(n.Value.Einheit); "")); 255);
                                     Kommentar: If(Coalesce(IfError(Boolean(n.Value.Kritisch); false); false); "KRITISCH – Bescheid gegeben " & Coalesce(Text(n.Value.KritischZeit); "") & ". "; "") & Coalesce(Text(n.Value.Kommentar); "");
                             FotoUrls: Coalesce(Text(n.Value.Fotos); "")})}
                            );
                            Zeilen
                        ); !IsBlank(PruefpunktID))
                    ));
                    Clear(colMaengelSoll)
                );;
                If(Sum(colErgAlle; AnzahlNIO) <> CountRows(colMaengelSoll);
                    Notify("Die Mängel ließen sich nicht vollständig aus den Antworten ermitteln (" & CountRows(colMaengelSoll) & " von " & Sum(colErgAlle; AnzahlNIO) & "). Bitte den Rundgang melden."; NotificationType.Error);
                    Refresh(RG_Maengel);;
                    ClearCollect(colMaengelIst; ShowColumns(Filter(RG_Maengel; DurchfuehrungID = varDurchID); Title));;
                    IfError(
                        Collect(RG_Maengel;
                            ForAll(Filter(colMaengelSoll As s; IsBlank(LookUp(colMaengelIst As i; i.Title = s.Title))) As m;
                                {Title: m.Title; DurchfuehrungID: varDurchID; PruefpunktID: m.PruefpunktID; RundgangName: varDurch.RundgangName; BereichName: m.BereichName; KategorieName: m.KategorieName; Frage: m.Frage; Wert: m.Wert; Kommentar: m.Kommentar; FotoUrls: m.FotoUrls; FestgestelltAm: Now(); FestgestelltVon: User().Email; Status: {Value: "Offen"}; TestDatensatz: varDurch.TestDatensatz})
                        );
                        Set(varPatchFehler; true)
                    );;
                    Concurrent(Refresh(RG_Maengel); Refresh(RG_KategorieErgebnisse); Refresh(RG_Durchfuehrungen));;
                    Concurrent(
                        ClearCollect(colMaengelIst; ShowColumns(Filter(RG_Maengel; DurchfuehrungID = varDurchID); Title));
                        ClearCollect(colErgJetzt; ShowColumns(Filter(RG_KategorieErgebnisse; DurchfuehrungID = varDurchID); ID; GespeichertAm))
                    );;
                    If(
                        CountRows(Filter(colMaengelSoll As s2; IsBlank(LookUp(colMaengelIst As i2; i2.Title = s2.Title)))) > 0;
                            Notify("Die Mängel konnten nicht vollständig gespeichert werden. Bitte „Rundgang abschließen“ erneut tippen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error);
                        Concat(Sort(colErgJetzt; ID); ID & "@" & Text(GespeichertAm; "yyyy-mm-dd hh:mm:ss"); ";") <> Concat(Sort(colErgAlle; ID); ID & "@" & Text(GespeichertAm; "yyyy-mm-dd hh:mm:ss"); ";");
                            Notify("Während des Abschlusses wurde eine Kategorie gespeichert. Bitte „Rundgang abschließen“ erneut tippen."; NotificationType.Warning);
                        LookUp(RG_Durchfuehrungen; ID = varDurchID).Status <> stAbschluss;
                    Notify("Der Abschluss wurde inzwischen zurückgesetzt. Bitte die Übersicht neu öffnen."; NotificationType.Warning);
                        IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSoll)}); Set(varPatchFehler; true));;
                        Refresh(RG_Durchfuehrungen);;
                        Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));;
                        If(varDurch.Status = stAbgeschlossen;
                            Notify("Rundgang abgeschlossen · " & CountRows(colMaengelSoll) & " Mängel erfasst. Protokoll wird archiviert …"; NotificationType.Success);;
                                Set(varArchivStart; false);;
                                Navigate(scrProtokoll; ScreenTransition.None);
                            Notify("Der Abschluss wurde nicht bestätigt. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error)
                        )
                    )
                )
            )
        );;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
    )
)
```

**Rundgang DEV `htmProtokoll.HtmlText` vorher**

```
With({d: varDurch};
    "<div style='font-family:Segoe UI,Arial,sans-serif;font-size:14px;color:#1B1B1F'>" &
    "<div style='background:#171496;color:#ffffff;padding:14px 16px'>" &
        "<div style='font-size:20px;font-weight:600'>" & fnHtml(d.RundgangName) & "</div>" &
        "<div>" & fnTagAnzeige(DateValue(d.TagText)) & " · Prüfer: " & fnHtml(d.PrueferName) & "</div>" &
        "<div>Status: " & d.Status & " · Beginn " & Text(d.StartZeit; "hh:mm") & If(IsBlank(d.EndeZeit); ""; " · Ende " & Text(d.EndeZeit; "hh:mm")) & " · <b>" & Coalesce(d.AnzahlNIO; 0) & " n.i.O.</b></div>" &
    "</div>" &
    Concat(Sort(colErgProt; Position) As e;
        "<h3 style='margin:18px 0 6px 0;font-size:16px;color:#171496'>" & e.Position & ". " & fnHtml(e.KategorieName) &
        " <span style='font-weight:400;color:#5F6370;font-size:13px'>" & If(e.BereichName = ""; ""; fnHtml(e.BereichName) & " · ") & fnHtml(e.PrueferName) & " · " & Text(e.GespeichertAm; "hh:mm") & "</span></h3>" &
        "<table style='width:100%;border-collapse:collapse;table-layout:fixed'>" &
        Concat(Filter(Table(ParseJSON(e.Antworten)); !Coalesce(IfError(Boolean(ThisRecord.Value.Ausgeblendet); false); false)) As a;
            With({b: Text(a.Value.Bewertung); k: Text(a.Value.Kommentar); fo: Text(a.Value.Fotos); w: Coalesce(IfError(Boolean(a.Value.Warnung); false); false)};
                If(Coalesce(IfError(Boolean(a.Value.AbsKopf); false); false); "<tr><td colspan='3' style='padding:12px 8px 4px 8px;font-weight:600;color:#171496'>" & fnHtml(Text(a.Value.Abschnitt)) & "</td></tr>"; "") &
                "<tr style='border-bottom:1px solid #DADCE5;" & If(b = "NIO"; "background:#FCE8E6;"; "") & "'>" &
                "<td style='padding:6px 8px;width:46%'>" & fnHtml(Text(a.Value.Frage)) & "</td>" &
                "<td style='padding:6px 8px;width:110px;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; w; "#9A5B00"; "#0F7B3F") & "'>" & Switch(b; "IO"; fnHtml(Coalesce(If(Coalesce(Text(a.Value.TextIO); "") = ""; Blank(); Text(a.Value.TextIO)); "i.O.")); "NIO"; fnHtml(Coalesce(If(Coalesce(Text(a.Value.TextNIO); "") = ""; Blank(); Text(a.Value.TextNIO)); "n.i.O.")); "") & "</td>" &
                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) & If(w; " <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>"; "") & If(Coalesce(Text(a.Value.AbwText); "") = ""; ""; " <span style='color:#9A5B00'>(" & fnHtml(Text(a.Value.AbwText)) & If(IsBlank(a.Value.Letzter); ""; ", zuletzt " & Text(Value(a.Value.Letzter))) & ", begründet)</span>") &
                If(IsBlank(k) || k = ""; ""; "<br><i style='color:" & If(b = "NIO"; "#B3261E"; "#5F6370") & "'>" & fnHtml(k) & "</i>") &
                If(b = "NIO" && Coalesce(IfError(Boolean(a.Value.Kritisch); false); false); "<br><b style='color:#B3261E'>KRITISCH – " & If(Coalesce(IfError(Boolean(a.Value.KritischOk); false); false); "Bescheid gegeben, bestätigt von " & fnHtml(Coalesce(Text(a.Value.KritischVon); e.PrueferName)) & " am " & fnHtml(Coalesce(Text(a.Value.KritischZeit); "")); "nicht bestätigt") & "</b>"; "") &
                If(IsBlank(fo) || fo = ""; ""; "<br>" & Concat(Split(fo; " | ") As s; "<a href='" & Trim(s.Value) & "'>Foto ›</a> ")) &
                "</td></tr>"
            )
        ) & "</table>"
    ) &
    If(IsBlank(d.ProtokollUrl); ""; "<p style='font-size:12px'>Archiv-PDF: <a href='" & d.ProtokollUrl & "'>" & fnHtml(d.Title) & ".pdf</a></p>") &
    "<p style='color:#5F6370;font-size:12px;margin-top:18px'>Erstellt mit der Rundgang-App · " & Text(varProtokollZeit; "dd.mm.yyyy hh:mm") & If(d.TestDatensatz; " · TESTDATEN"; "") & "</p></div>"
)
```

**Builder `galPl.Height` vorher**

```
Parent.Height - 220
```

