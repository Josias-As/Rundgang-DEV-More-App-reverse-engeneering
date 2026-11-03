# Paket 13 – Anleitungen im ⓘ-Fenster (Rundgang-App + Builder)

Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket13), `werkzeuge/builder.py` und `werkzeuge/doc_paket13.py`. **Voraussetzung:** Rundgang-App bis Paket 17 eingefügt, Builder bis Paket 14+15.

## Kurzfassung

- **Anleitungen:** Eine neue Liste `RG_Anleitungen` (Titel, Text beliebig lang, aktiv). Eine Anleitung kann an vielen Prüfpunkten hängen.
- **Prüfer:** An Prüfpunkten mit Anleitung steht ein runder Knopf **ⓘ**. Er öffnet ein großes Fenster mit dem Text (scrollbar) und, falls vorhanden, dem Beispielbild.
- **Builder:** neuer Bildschirm „Anleitungen“ (anlegen, ändern, inaktiv stellen) und im Prüfpunkt das Feld „Anleitung“ neben „Foto“. Die Foto-Auswahl hat dafür kürzere Texte (gleiche Werte).
- Bewusst nicht gebaut: Foto-Aufnahme im ⓘ-Fenster (Pflicht-Fotos bleiben sichtbar in der Karte – „Prüfer sind nicht verlässlich“).
- Umfang: 1 Liste, 1 Spalte. Rundgang-App 2 Properties + 2 Blöcke. Builder 1 Bildschirm, 2 Blöcke, 11 Properties. Generatoren 0 Fehler. **Nicht in Studio getestet. Nicht unabhängig geprüft.**

## Teil A – Rundgang-App

### A1 – SharePoint

- Neue Liste **`RG_Anleitungen`**: `Title` (vorhanden), `Anleitung` (Mehrere Textzeilen, **nur Text**), `Aktiv` (Ja/Nein, Standard Ja). Berechtigung wie die anderen RG-Listen.
- `RG_Pruefpunkte`: neue Spalte `AnleitungID` (Zahl, Standard 0).
- Rundgang-App: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**, dann **Daten hinzufügen** → SharePoint → IMS+ → `RG_Anleitungen`.

### A2 – zwei Properties

### A2.1 · `scrKategorie.OnVisible`

**Pfad:** `scrKategorie` → OnVisible

```
Set(varIsLoading; true);;
Set(varZurueckFrage; false);;
Set(varAlleIOFrage; false);;
Set(varZeigeFehlend; false);;
Set(varFotoPP; 0);;
Set(varBildID; 0);;
Set(varInfoID; 0);;
Set(varRueckPP; 0);;
Set(varKritPP; 0);;
Clear(colFotos);;
Set(varGeaendert; false);;
Set(varSchluesselK; "D" & varDurchID & "-K" & varKatID);;
Set(varNurLesen; varDurch.Status <> stInArbeit);;
Refresh(RG_KategorieErgebnisse);;
Concurrent(
    ClearCollect(colPP; Filter(RG_Pruefpunkte; KategorieID = varKatID && Aktiv = true));
    Set(varErgebnis; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK));
    ClearCollect(colKontakte; Filter(RG_Ansprechpartner; Aktiv = true))
);;
If(!varNurLesen && varLetzteFuer <> varDurchID && CountRows(Filter(colPP; !IsBlank(AbwMax) || Coalesce(NurSteigend; false))) > 0;
    Set(varLetzteFuer; varDurchID);;
    Set(varLetzteRg; varDurch.RundgangID);;
    Set(varLetzteTest; varDurch.TestDatensatz);;
    Set(varLetzteDurch; First(Sort(Filter(RG_Durchfuehrungen; RundgangID = varLetzteRg && Status = stAbgeschlossen && TestDatensatz = varLetzteTest); ID; SortOrder.Descending)));;
    If(IsBlank(varLetzteDurch.ID);
        Clear(colLetzte);
        Set(varLetzteID; varLetzteDurch.ID);;
        ClearCollect(colLetzte; Filter(Ungroup(ForAll(Filter(RG_KategorieErgebnisse; DurchfuehrungID = varLetzteID) As e; {T: ForAll(Table(ParseJSON(e.Antworten)) As j; {PP: Value(j.Value.PruefpunktID); Z: Value(j.Value.WertZahl)})}); T); !IsBlank(Z)))
    )
);;
Set(varGespeichertBeimOeffnen; varErgebnis.GespeichertAm);;
With({t: If(IsBlank(varErgebnis.Antworten); Table(ParseJSON("[]")); Table(ParseJSON(varErgebnis.Antworten)))};
    If(varNurLesen && !IsEmpty(t);
        ClearCollect(colAntworten;
            ForAll(Sequence(CountRows(t)) As i;
                With({a: Index(t; i.Value).Value};
                    With({pp: LookUp(colPP; ID = Value(a.PruefpunktID))};
                        {PruefpunktID: Value(a.PruefpunktID); Frage: Text(a.Frage); Typ: Text(a.Typ); Pflicht: false; Einheit: Coalesce(Text(a.Einheit); ""); MinWert: pp.MinWert; MaxWert: pp.MaxWert; Auswahl: Coalesce(Text(a.WertText); ""); Hinweis: ""; Reihenfolge: i.Value;
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); BildID: Coalesce(pp.HinweisBildID; 0); Abschnitt: Trim(Coalesce(Text(a.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(a.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(a.KritischOk); false); false); KritischZeit: Coalesce(Text(a.KritischZeit); ""); KritischVon: Coalesce(Text(a.KritischVon); ""); TextIO: Coalesce(Text(a.TextIO); ""); TextNIO: Coalesce(Text(a.TextNIO); ""); NMErlaubt: false; KPflOrig: false; Letzter: Value(a.Letzter); LetzterTag: Coalesce(Text(a.LetzterTag); ""); AbwMax: Blank(); AbwProzent: false; NurSteigend: false; VglID: 0; VglTol: 0; AbwText: Coalesce(Text(a.AbwText); ""); AnlID: Coalesce(pp.AnleitungID; 0); Inaktiv: false}
                    )
                )
            )
        );
        ClearCollect(colAntworten;
            ForAll(Sort(colPP; RgReihenfolge) As p;
                With({alt: LookUp(t As j; Value(j.Value.PruefpunktID) = p.ID)};
                    {PruefpunktID: p.ID; Frage: p.Title; Typ: p.Eingabetyp.Value; Pflicht: p.Pflicht; Einheit: Coalesce(p.Einheit; ""); MinWert: p.MinWert; MaxWert: p.MaxWert; Auswahl: Coalesce(p.Auswahlwerte; ""); Hinweis: Coalesce(p.Hinweis; ""); Reihenfolge: p.RgReihenfolge;
                     Bewertung: If(IsBlank(alt); ""; p.Eingabetyp.Value = "ZAHL" && !IsBlank(alt.Value.WertZahl); fnZahlBewertung(Value(alt.Value.WertZahl); p.MinWert; p.MaxWert; fnGrenzmodus(p.Grenzmodus.Value)); Coalesce(Text(alt.Value.Bewertung); ""));
                     WertText: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.WertText); ""));
                     WertZahl: If(IsBlank(alt); Blank(); Value(alt.Value.WertZahl));
                     Kommentar: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.Kommentar); ""));
                     Fotos: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.Fotos); ""));
                     FotoModus: fnFotoModus(p.Foto.Value; Coalesce(p.FotoMoeglich; false));
                     KommentarPflicht: Coalesce(p.KommentarPflicht; false);
                     Grenzmodus: fnGrenzmodus(p.Grenzmodus.Value);
                     BedID: Coalesce(p.BedingungPunkt; 0);
                     BedWert: Coalesce(p.BedingungWert; "");
                     Ausgeblendet: false;
                     BildID: Coalesce(p.HinweisBildID; 0);
                     Abschnitt: Trim(Coalesce(p.Abschnitt; ""));
                     AbsKopf: false;
                     Kritisch: Coalesce(p.Kritisch; false);
                     KritischText: Coalesce(p.KritischText; "");
                     Ansprechpartner: Coalesce(p.Ansprechpartner; "");
                     Rueckfrage: Coalesce(p.Rueckfrage; false);
                     RueckfrageText: Coalesce(p.RueckfrageText; "");
                     KritischOk: If(IsBlank(alt); false; Coalesce(IfError(Boolean(alt.Value.KritischOk); false); false));
                     KritischZeit: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.KritischZeit); ""));
                     KritischVon: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.KritischVon); ""));
                     TextIO: Trim(Coalesce(p.TextIO; ""));
                     TextNIO: Trim(Coalesce(p.TextNIO; ""));
                     NMErlaubt: Coalesce(p.NichtMessbar; false);
                     KPflOrig: Coalesce(p.KommentarPflicht; false);
                     Letzter: If(p.Eingabetyp.Value = "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend; false)); Coalesce(LookUp(colLetzte; PP = p.ID).Z; LookUp(colLetzte; PP = Coalesce(p.QuelleID; -1)).Z));
                     LetzterTag: If(IsBlank(varLetzteDurch.TagText); ""; Text(DateValue(varLetzteDurch.TagText); "dd.mm."));
                     AbwMax: p.AbwMax;
                     AbwProzent: Coalesce(p.AbwProzent; false);
                     NurSteigend: Coalesce(p.NurSteigend; false);
                     VglID: Coalesce(p.VergleichPunkt; 0);
                     VglTol: Coalesce(p.VergleichTol; 0);
                     AbwText: "";
                     AnlID: Coalesce(p.AnleitungID; 0);
                     Warnung: false;
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Warnung: Coalesce(IfError(Boolean(o.Value.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); BildID: 0; Abschnitt: Trim(Coalesce(Text(o.Value.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(o.Value.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(o.Value.KritischOk); false); false); KritischZeit: Coalesce(Text(o.Value.KritischZeit); ""); KritischVon: Coalesce(Text(o.Value.KritischVon); ""); TextIO: Coalesce(Text(o.Value.TextIO); ""); TextNIO: Coalesce(Text(o.Value.TextNIO); ""); NMErlaubt: false; KPflOrig: false; Letzter: Value(o.Value.Letzter); LetzterTag: Coalesce(Text(o.Value.LetzterTag); ""); AbwMax: Blank(); AbwProzent: false; NurSteigend: false; VglID: 0; VglTol: 0; AbwText: Coalesce(Text(o.Value.AbwText); ""); AnlID: 0; Inaktiv: true}
            )
        )
    )
);;
If(!varNurLesen; ClearCollect(colVglTmp; ForAll(Filter(colAntworten As a0; !a0.Inaktiv && a0.Typ = "ZAHL" && (a0.VglID <> 0 || !IsBlank(a0.Letzter))) As a;
        With({w: LookUp(colAntworten As o; o.PruefpunktID = a.VglID)};
            {PP: a.PruefpunktID;
             Abw: fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend);
             Vgl: a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol);
             Text: If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); If(a.NurSteigend && a.WertZahl < a.Letzter; "kleiner als beim letzten Mal"; "starke Abweichung zum letzten Mal"); "") & If(a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol); If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); "; "; "") & "weicht von „" & w.Frage & "“ ab (" & Text(w.WertZahl) & ")"; "");
             KPfl: a.KPflOrig}
        )
    ));;
    ForAll(colVglTmp As v; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = v.PP); {KommentarPflicht: v.KPfl || v.Abw || v.Vgl; AbwText: v.Text})));;
ClearCollect(colAbsTmp; ShowColumns(Filter(colAntworten; !Inaktiv && !Ausgeblendet && Abschnitt <> ""); PruefpunktID; Reihenfolge; Abschnitt; BedID));;
ForAll(colAbsTmp As t;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = t.PruefpunktID);
        {AbsKopf: With({g: Filter(colAbsTmp As u; Lower(u.Abschnitt) = Lower(t.Abschnitt))};
            If(IsEmpty(Filter(g As u1; u1.BedID = 0)); t.Reihenfolge * 1000000 + t.PruefpunktID = Min(g; Reihenfolge * 1000000 + PruefpunktID); t.BedID = 0 && t.Reihenfolge * 1000000 + t.PruefpunktID = Min(Filter(g As u2; u2.BedID = 0); Reihenfolge * 1000000 + PruefpunktID)))}
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
```

```diff
+Set(varInfoID; 0);;
-                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFot …
+                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFot …
+                     AnlID: Coalesce(p.AnleitungID; 0);
-                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); …
+                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); …
```

**Kurz erklärt:** Neues Feld `AnlID` in allen drei Zweigen. Das ⓘ-Fenster ist beim Öffnen zu.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

### A2.2 · `lblKaFrage.Width`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaFrage` → Width

```
Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0)
```

```diff
-Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0)
+Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0)
```

**Kurz erklärt:** Platz für den ⓘ-Knopf.

**Nachprüfen:** endet auf `rent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0)`

### A3 – Knopf ⓘ in der Karte

**Wo hin:** in der Strukturansicht `btnKaBild` (in `conKaKarte`) markieren → Strg+V.

```yaml
- btnKaInfo:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrPrimaer
      BorderThickness: =1
      Color: =clrPrimaer
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      FontWeight: =FontWeight.Semibold
      Height: =34
      HoverColor: =clrPrimaer
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =Set(varInfoFrage, ThisItem.Frage);
        Set(varInfoBild, ThisItem.BildID);
        Set(varInfo, LookUp(RG_Anleitungen, ID = ThisItem.AnlID));
        If(IsBlank(varInfo.ID), Notify("Die Anleitung wurde nicht gefunden.", NotificationType.Warning), Set(varInfoID, ThisItem.AnlID))
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =17
      RadiusBottomRight: =17
      RadiusTopLeft: =17
      RadiusTopRight: =17
      Size: =16
      Text: ="ⓘ"
      Visible: =ThisItem.AnlID > 0
      Width: =48
      X: =Parent.Width - 68 - If(ThisItem.BildID > 0, 80, 0)
      Y: =10
```

**Nachprüfen (E-05):** `btnKaInfo.X` ist eine Formel.

### A4 – Fenster

**Wo hin:** **`scrKategorie`** markieren → Strg+V (liegt dann über allem).

```yaml
- conKaInfo:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      Fill: =RGBA(0, 0, 0, 0.45)
      Height: =Parent.Height
      Visible: =varInfoID > 0
      Width: =Parent.Width
    Children:
    - btnKaInfoSperre:
        Control: Classic/Button@2.2.0
        Properties:
          BorderThickness: =0
          Fill: =RGBA(0, 0, 0, 0)
          Height: =Parent.Height
          HoverFill: =RGBA(0, 0, 0, 0)
          PressedFill: =RGBA(0, 0, 0, 0)
          Text: =""
          Width: =Parent.Width
    - conKaInfoKarte:
        Control: GroupContainer@1.5.0
        Variant: ManualLayout
        Properties:
          Fill: =clrKarte
          Height: =Min(Parent.Height - 32, 1000)
          RadiusBottomLeft: =16
          RadiusBottomRight: =16
          RadiusTopLeft: =16
          RadiusTopRight: =16
          Width: =Parent.Width - 48
          X: =24
          Y: =(Parent.Height - Self.Height) / 2
        Children:
        - lblKaInfoTitel:
            Control: Label@2.5.1
            Properties:
              Color: =clrPrimaer
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =40
              Size: =19
              Text: ="ⓘ " & varInfo.Title
              Width: =Parent.Width - 40
              Wrap: =false
              X: =20
              Y: =14
        - lblKaInfoFrage:
            Control: Label@2.5.1
            Properties:
              Color: =clrTextGrau
              Font: =Font.'Segoe UI'
              Height: =28
              Size: =13
              Text: |-
                ="zu: " & varInfoFrage
              Width: =Parent.Width - 40
              Wrap: =false
              X: =20
              Y: =54
        - lblKaInfoText:
            Control: Label@2.5.1
            Properties:
              Color: =clrText
              Font: =Font.'Segoe UI'
              Height: =If(varInfoBild > 0, (Parent.Height - 180) * 0.55, Parent.Height - 180)
              Overflow: =Overflow.Scroll
              Size: =16
              Text: =Coalesce(varInfo.Anleitung, "")
              VerticalAlign: =VerticalAlign.Top
              Width: =Parent.Width - 40
              X: =20
              Y: =88
        - imgKaInfo:
            Control: Image@2.2.3
            Properties:
              AccessibleLabel: ="Beispielbild zu " & varInfoFrage
              Height: =(Parent.Height - 180) * 0.45 - 8
              Image: =If(varInfoID > 0 && varInfoBild > 0, LookUp(RG_Hinweisbilder, ID = varInfoBild).Thumbnail.Large)
              ImagePosition: =ImagePosition.Fit
              Visible: =varInfoBild > 0
              Width: =Parent.Width - 40
              X: =20
              Y: =96 + (Parent.Height - 180) * 0.55
        - btnKaInfoSchliessen:
            Control: Classic/Button@2.2.0
            Properties:
              BorderThickness: =0
              Color: =Color.White
              Fill: =clrPrimaer
              Font: =Font.'Segoe UI'
              Height: =56
              HoverFill: =ColorFade(clrPrimaer, -20%)
              OnSelect: =Set(varInfoID, 0)
              PressedFill: =ColorFade(clrPrimaer, -35%)
              RadiusBottomLeft: =10
              RadiusBottomRight: =10
              RadiusTopLeft: =10
              RadiusTopRight: =10
              Size: =17
              Text: ="Schließen"
              Width: =200
              X: =Parent.Width - 220
              Y: =Parent.Height - 76
```

## Teil B – Builder

### B0 – Daten

Liste und Spalte aus A1 (nur einmal anlegen). Builder: `RG_Pruefpunkte` aktualisieren, `RG_Anleitungen` hinzufügen.

### B1 – Bildschirm „Anleitungen“

**Wo hin:** einen Bildschirm markieren (z. B. `scrKontakte`) → Strg+V.

```yaml
Screens:
  scrAnleitungen:
    Properties:
      Fill: =clrHintergrund
      OnVisible: |-
        =Set(varIsLoading, true);
        Set(varLadeText, "");
        Refresh(RG_Anleitungen);
        ClearCollect(colAnAlle, RG_Anleitungen);
        Set(varAnID, Coalesce(First(Sort(colAnAlle, Title)).ID, 0));
        Reset(txtAnTitel);
        Reset(txtAnText);
        Set(varIsLoading, false)
    Children:
      - conAnKopf:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrPrimaer
            Height: =64
            Width: =Parent.Width
          Children:
            - btnAnZurueck:
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
            - lblAnTitelKopf:
                Control: Label@2.5.1
                Properties:
                  Color: =Color.White
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =64
                  Size: =20
                  Text: ="Anleitungen"
                  Width: =600
                  X: =172
                  Y: =0
      - lblAnHilfe:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =44
            Size: =13
            Text: |-
              ="Längere Texte, die der Prüfer über ⓘ öffnet. Eine Anleitung kann bei vielen Prüfpunkten hängen. Zuordnen im Prüfpunkt unter „Anleitung“. Nicht mehr gebraucht: inaktiv stellen."
            Width: =Parent.Width - 48
            X: =24
            Y: =72
      - btnAnNeu:
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
                  Set(varNeuID, IfError(Patch(RG_Anleitungen, Defaults(RG_Anleitungen), {Title: "Neue Anleitung", Anleitung: "", Aktiv: true}).ID, 0));
                  If(varNeuID = 0,
                      Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
                      Collect(colAnAlle, LookUp(RG_Anleitungen, ID = varNeuID));
                      Set(varAnID, varNeuID);
                      Reset(txtAnTitel);
                      Reset(txtAnText);
                      SetFocus(txtAnTitel)
                  )
              )
            PressedColor: =Color.White
            PressedFill: =ColorFade(clrPrimaer, -35%)
            RadiusBottomLeft: =6
            RadiusBottomRight: =6
            RadiusTopLeft: =6
            RadiusTopRight: =6
            Size: =14
            Text: ="+ Anleitung"
            Width: =220
            X: =24
            Y: =124
      - galAn:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            AccessibleLabel: ="Anleitungen"
            Height: =Parent.Height - 196
            Items: =Sort(colAnAlle, If(Coalesce(Aktiv, false), "0", "1") & Lower(Title))
            ShowScrollbar: =true
            TemplatePadding: =0
            TemplateSize: =56
            Width: =420
            X: =24
            Y: =180
          Children:
            - lblAnHinter:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Fill: =If(ThisItem.ID = varAnID, clrPrimaerHell, Color.White)
                  Font: =Font.'Segoe UI'
                  Height: =Parent.TemplateHeight - 4
                  Size: =14
                  Text: =""
                  Width: =Parent.TemplateWidth
                  X: =0
                  Y: =0
            - lblAnZeile:
                Control: Label@2.5.1
                Properties:
                  Color: =If(Coalesce(ThisItem.Aktiv, false), clrText, clrTextGrau)
                  Font: =Font.'Segoe UI'
                  Height: =Parent.TemplateHeight - 4
                  Size: =14
                  Text: =ThisItem.Title & If(Coalesce(ThisItem.Aktiv, false), "", "  · inaktiv")
                  Width: =Parent.TemplateWidth - 24
                  Wrap: =false
                  X: =12
                  Y: =0
            - btnAnZeile:
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
                    =Set(varAnID, ThisItem.ID);
                    Reset(txtAnTitel);
                    Reset(txtAnText)
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
      - lblAnLeer:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =48
            Size: =13
            Text: ="Noch keine Anleitungen. „+ Anleitung“ legt eine an."
            Visible: =IsEmpty(colAnAlle) && !varIsLoading
            Width: =420
            X: =24
            Y: =190
      - conAnForm:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrHintergrund
            Height: =Parent.Height - 140
            Visible: =varAnID > 0
            Width: =Parent.Width - 492
            X: =468
            Y: =124
          Children:
            - lblAnTitelT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Titel"
                  Width: =400
                  X: =0
                  Y: =0
            - txtAnTitel:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Titel der Anleitung"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colAnAlle, ID = varAnID).Title, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HintText: ="z. B. Kompressor ablesen"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =If(Trim(Self.Text) <> "" && Trim(Self.Text) <> Trim(Coalesce(LookUp(colAnAlle, ID = varAnID).Title, "")),
                        If(varAnID > 0 && !varIsLoading,
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Anleitungen, LookUp(RG_Anleitungen, ID = varAnID), {Title: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colAnAlle, LookUp(colAnAlle, ID = varAnID), LookUp(RG_Anleitungen, ID = varAnID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =20
            - lblAnTextT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Text (beliebig lang, Absätze mit Enter)"
                  Width: =400
                  X: =0
                  Y: =72
            - txtAnText:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Text der Anleitung"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colAnAlle, ID = varAnID).Anleitung, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =Parent.Height - 160
                  HintText: ="Schritt für Schritt …"
                  HoverBorderColor: =clrPrimaer
                  Mode: =TextMode.MultiLine
                  OnChange: |-
                    =If(Self.Text <> Coalesce(LookUp(colAnAlle, ID = varAnID).Anleitung, ""),
                        If(varAnID > 0 && !varIsLoading,
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Anleitungen, LookUp(RG_Anleitungen, ID = varAnID), {Anleitung: Self.Text}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colAnAlle, LookUp(colAnAlle, ID = varAnID), LookUp(RG_Anleitungen, ID = varAnID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =92
            - galAnAktiv:
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
                  Y: =Parent.Height - 56
                Children:
                  - btnAnAktiv:
                      Control: Classic/Button@2.2.0
                      Properties:
                        BorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        BorderThickness: =1
                        Color: =If(ThisItem.W = If(Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false), "ja", "nein"), Color.White, clrText)
                        DisabledBorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        DisabledColor: =If(ThisItem.W = If(Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false), "ja", "nein"), clrPrimaer, clrTextGrau)
                        DisabledFill: =If(ThisItem.W = If(Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false), "ja", "nein"), clrPrimaerHell, clrKarte)
                        DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                        Fill: =If(ThisItem.W = If(Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false), "ja", "nein"), clrPrimaer, clrKarte)
                        Font: =Font.'Segoe UI'
                        Height: =36
                        HoverColor: =If(ThisItem.W = If(Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false), "ja", "nein"), Color.White, clrText)
                        HoverFill: =If(ThisItem.W = If(Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false), "ja", "nein"), ColorFade(clrPrimaer, -20%), clrPrimaerHell)
                        OnSelect: |-
                          =If((ThisItem.W = "ja") <> Coalesce(LookUp(colAnAlle, ID = varAnID).Aktiv, false),
                              If(varAnID > 0 && !varIsLoading,
                                  Set(varPatchFehler, false);
                                  IfError(Patch(RG_Anleitungen, LookUp(RG_Anleitungen, ID = varAnID), {Aktiv: ThisItem.W = "ja"}), Set(varPatchFehler, true));
                                  If(varPatchFehler,
                                      Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                      Patch(colAnAlle, LookUp(colAnAlle, ID = varAnID), LookUp(RG_Anleitungen, ID = varAnID))
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
      - conAnLaden:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =RGBA(255, 255, 255, 0.7)
            Height: =Parent.Height
            Visible: =varIsLoading
            Width: =Parent.Width
          Children:
            - btnAnLadenSperre:
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
            - lblAnLadenText:
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

### B2 – Knopf in der Übersicht

**Wo hin:** **`scrListe`** markieren → Strg+V.

```yaml
- btnLiAnleitungen:
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
            Navigate(scrAnleitungen, ScreenTransition.None)
        )
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =14
      Text: ="Anleitungen"
      Width: =180
      X: =862
      Y: =84
```

### B3 – Feld „Anleitung“ im Prüfpunkt

**Wo hin:** **`conPRest`** (`scrEditor › conEdMitte › conEdP › conPRest`) markieren → Strg+V.

```yaml
- lblPAnl:
    Control: Label@2.5.1
    Properties:
      Color: =clrTextGrau
      Font: =Font.'Segoe UI'
      Height: =20
      Size: =12
      Text: ="Anleitung (ⓘ beim Prüfer)"
      Width: =256
      X: =272
      Y: =0
- ddPAnl:
    Control: Classic/DropDown@2.3.1
    Properties:
      AccessibleLabel: ="Anleitung"
      BorderColor: =clrRahmen
      BorderThickness: =1
      ChevronBackground: =clrPrimaer
      ChevronFill: =Color.White
      ChevronHoverBackground: =ColorFade(clrPrimaer, -20%)
      ChevronHoverFill: =Color.White
      Color: =clrText
      Default: =If(Coalesce(LookUp(colP, ID = varAuswahlID).AnleitungID, 0) = 0, "— keine —", Coalesce(LookUp(RG_Anleitungen, ID = LookUp(colP, ID = varAuswahlID).AnleitungID).Title, "(fehlt)"))
      DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =36
      HoverFill: =clrPrimaerHell
      Items: |-
        =Ungroup(Table({T: Table({ID: 0, Title: "— keine —"})}, {T: Sort(ShowColumns(Filter(RG_Anleitungen, Aktiv = true), ID, Title), Title)}), T)
      Items.Value: =Title
      OnChange: |-
        =If(!IsBlank(Self.Selected) && Self.Selected.ID <> Coalesce(LookUp(colP, ID = varAuswahlID).AnleitungID, 0),
            If(varSchreibbar && varAuswahlEbene = 3,
                Refresh(RG_Rundgaenge);
                Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                If(varEntwurfOk,
                    Set(varPatchFehler, false);
                    IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {AnleitungID: Self.Selected.ID}), Set(varPatchFehler, true));
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
      Width: =256
      X: =272
      Y: =20
```

**Kurzzeitig normal:** `ddPAnl` liegt über der Foto-Auswahl, bis B4 sie schmaler macht.

### B4 – Start und Foto/Anleitung

### B4.1 · `App.OnStart`

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
Set(varZaOffen; false);;
Set(varAnID; 0)
```

```diff
-Set(varZaOffen; false)
+Set(varZaOffen; false);;
+Set(varAnID; 0)
```

**Kurz erklärt:** Neuer Startwert `varAnID` (gewählte Anleitung).

**Nachprüfen:** endet auf `Set(varAnID; 0)`

### B4.2 · `lblPFoto.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPFoto` → Width

```
256
```

```diff
-528
+256
```

**Kurz erklärt:** Halbe Breite, daneben „Anleitung“.

**Nachprüfen:** endet auf `256`

### B4.3 · `ddPFoto.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPFoto` → Width

```
256
```

```diff
-528
+256
```

**Kurz erklärt:** Halbe Breite.

**Nachprüfen:** endet auf `256`

### B4.4 · `ddPFoto.Items`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPFoto` → Items

```
Table({W: "Aus"; N: "kein Foto"}; {W: "Optional"; N: "Foto freiwillig"}; {W: "Pflicht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto bei Mangel"})
```

```diff
-Table({W: "Aus"; N: "kein Foto (bei n.i.O. möglich)"}; {W: "Optional"; N: "Foto freiwillig"}; {W: "Pflicht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto Pflicht bei Mangel (n.i.O.)"})
+Table({W: "Aus"; N: "kein Foto"}; {W: "Optional"; N: "Foto freiwillig"}; {W: "Pflicht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto bei Mangel"})
```

**Kurz erklärt:** Kürzere Texte (gleiche Werte): „kein Foto“, „Foto freiwillig“, „Foto immer Pflicht“, „Foto bei Mangel“.

**Nachprüfen:** endet auf `cht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto bei Mangel"})`

### B4.5 · `ddPFoto.Default`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPFoto` → Default

```
LookUp(Table({W: "Aus"; N: "kein Foto"}; {W: "Optional"; N: "Foto freiwillig"}; {W: "Pflicht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto bei Mangel"}); W = fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))).N
```

```diff
-LookUp(Table({W: "Aus"; N: "kein Foto (bei n.i.O. möglich)"}; {W: "Optional"; N: "Foto freiwillig"}; {W: "Pflicht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto Pflicht bei Mangel (n.i.O.)"}); W = fnFotoWert(LookUp(colP; …
+LookUp(Table({W: "Aus"; N: "kein Foto"}; {W: "Optional"; N: "Foto freiwillig"}; {W: "Pflicht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto bei Mangel"}); W = fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coales …
```

**Kurz erklärt:** Wie Items.

**Nachprüfen:** endet auf `D).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))).N`

### B5 – Vorschau, neue Prüfpunkte, Liste

### B5.1 · `lblVsRegeln.Text`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › lblVsRegeln` → Text

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NichtMessbar; false); Char(10) & "• „nicht messbar“ erlaubt (dann Begründung Pflicht)"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && !IsBlank(LookUp(colP; ID = varAuswahlID).AbwMax); Char(10) & "• höchstens " & Text(LookUp(colP; ID = varAuswahlID).AbwMax) & If(Coalesce(LookUp(colP; ID = varAuswahlID).AbwProzent; false); " %"; "") & " Abweichung zum letzten Rundgang"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NurSteigend; false); Char(10) & "• Zählerstand: darf nicht kleiner werden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).VergleichPunkt; 0) <> 0; Char(10) & "• Vergleich mit „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).VergleichPunkt).Title & "“ (± " & Text(Coalesce(LookUp(colP; ID = varAuswahlID).VergleichTol; 0)) & ")"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).AnleitungID; 0) > 0; Char(10) & "• ⓘ Anleitung „" & Coalesce(LookUp(RG_Anleitungen; ID = LookUp(colP; ID = varAuswahlID).AnleitungID).Title; "?") & "“"; "")
```

```diff
-"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglic …
+"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglic …
```

**Kurz erklärt:** Vorschau nennt die Anleitung.

**Nachprüfen:** endet auf `tungen; ID = LookUp(colP; ID = varAuswahlID).AnleitungID).Title; "?") & "“"; "")`

### B5.2 · `btnGlNeuP.OnSelect`

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
        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0) + 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: "IONIO"}; Pflicht: true; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: If(varAuswahlEbene = 3 && LookUp(colP; ID = varAuswahlID).KategorieID = varCtxK; Coalesce(LookUp(colP; ID = varAuswahlID).Abschnitt; ""); ""); TextIO: ""; TextNIO: ""; NichtMessbar: false; AbwProzent: false; NurSteigend: false; VergleichPunkt: 0; VergleichTol: 0; AnleitungID: 0}).ID; 0));;
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

**Kurz erklärt:** Neuer Prüfpunkt ohne Anleitung.

**Nachprüfen:** endet auf `)`

### B5.3 · `btnMehrAnlegen.OnSelect`

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
                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: varMehrTyp}; Pflicht: varMehrPflicht; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: Left(Trim(txtMehrAbschnitt.Text); 255); TextIO: ""; TextNIO: ""; NichtMessbar: false; AbwProzent: false; NurSteigend: false; VergleichPunkt: 0; VergleichTol: 0; AnleitungID: 0}).ID; 0)}
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

### B5.4 · `galAkt.Items`

**Pfad:** `scrEditor › conAkt › conAktKarte › galAkt` → Items

```
Ungroup(
    Table(
        {T: ForAll(Filter(colP As p; IsBlank(LookUp(colAltP As a; a.ID = p.QuelleID))) As p; {Art: "neu"; Text: p.Title})};
        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) || Coalesce(p.Auswahlwerte; "") <> Coalesce(a.Auswahlwerte; "") || Coalesce(p.Einheit; "") <> Coalesce(a.Einheit; "") || Coalesce(p.MinWert; -999999) <> Coalesce(a.MinWert; -999999) || Coalesce(p.MaxWert; -999999) <> Coalesce(a.MaxWert; -999999) || Coalesce(p.Hinweis; "") <> Coalesce(a.Hinweis; "") || fnFotoWert(p.Foto.Value; Coalesce(p.FotoMoeglich; false)) <> fnFotoWert(a.Foto.Value; Coalesce(a.FotoMoeglich; false)) || Coalesce(p.KommentarPflicht; false) <> Coalesce(a.KommentarPflicht; false) || fnGrenzmodus(p.Grenzmodus.Value) <> fnGrenzmodus(a.Grenzmodus.Value) || Coalesce(p.BedingungWert; "") <> Coalesce(a.BedingungWert; "") || Coalesce(LookUp(colP As b0; b0.ID = p.BedingungPunkt).QuelleID; 0) <> Coalesce(a.BedingungPunkt; 0) || Coalesce(p.HinweisBildID; 0) <> Coalesce(a.HinweisBildID; 0) || Coalesce(LookUp(colK As k0; k0.ID = p.KategorieID).QuelleID; 0) <> a.KategorieID || Trim(Coalesce(p.Abschnitt; "")) <> Trim(Coalesce(a.Abschnitt; "")) || Coalesce(p.Kritisch; false) <> Coalesce(a.Kritisch; false) || Coalesce(p.KritischText; "") <> Coalesce(a.KritischText; "") || Coalesce(p.Ansprechpartner; "") <> Coalesce(a.Ansprechpartner; "") || Coalesce(p.Rueckfrage; false) <> Coalesce(a.Rueckfrage; false) || Coalesce(p.RueckfrageText; "") <> Coalesce(a.RueckfrageText; "") || Coalesce(p.TextIO; "") <> Coalesce(a.TextIO; "") || Coalesce(p.TextNIO; "") <> Coalesce(a.TextNIO; "") || Coalesce(p.NichtMessbar; false) <> Coalesce(a.NichtMessbar; false) || Coalesce(p.AbwMax; -999999) <> Coalesce(a.AbwMax; -999999) || Coalesce(p.AbwProzent; false) <> Coalesce(a.AbwProzent; false) || Coalesce(p.NurSteigend; false) <> Coalesce(a.NurSteigend; false) || Coalesce(p.VergleichTol; 0) <> Coalesce(a.VergleichTol; 0) || Coalesce(LookUp(colP As v0; v0.ID = p.VergleichPunkt).QuelleID; 0) <> Coalesce(a.VergleichPunkt; 0) || Coalesce(p.AnleitungID; 0) <> Coalesce(a.AnleitungID; 0)))) As p; {Art: "geändert"; Text: p.Title})};
        {T: ForAll(Filter(colAltP As a; IsBlank(LookUp(colP As p; p.QuelleID = a.ID))) As a; {Art: "entfernt"; Text: a.Title})}
    );
    T
)
```

```diff
-        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coales …
+        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coales …
```

**Kurz erklärt:** Änderung der Anleitung zählt als „geändert“.

**Nachprüfen:** endet auf `)`

### B6 – Lange Formeln

### B6.1 · `galPr.Items`

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
            {T: ForAll(Filter(colP As p; Coalesce(p.AnleitungID; 0) > 0 && IsBlank(LookUp(colAnlAktiv As n0; n0.ID = p.AnleitungID))) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Die gewählte Anleitung gibt es nicht mehr oder sie ist inaktiv."})};
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
+            {T: ForAll(Filter(colP As p; Coalesce(p.AnleitungID; 0) > 0 && IsBlank(LookUp(colAnlAktiv As n0; n0.ID = p.AnleitungID))) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.K …
```

**Kurz erklärt:** Hinweis, wenn die Anleitung fehlt oder inaktiv ist.

**Nachprüfen:** endet auf `)`

### B6.2 · `tmrArbeit.OnTimerEnd`

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
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQK) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colP; KategorieID = varZielK); RgReihenfolge); 0) + i.Value * 10); Aktiv: true; QuelleID: q.ID; Eingabetyp: {Value: Coalesce(q.Eingabetyp.Value; "IONIO")}; Pflicht: Coalesce(q.Pflicht; false); Auswahlwerte: q.Auswahlwerte; Einheit: q.Einheit; MinWert: q.MinWert; MaxWert: q.MaxWert; Hinweis: q.Hinweis; FotoMoeglich: Coalesce(q.FotoMoeglich; false); Foto: {Value: fnFotoWert(q.Foto.Value; Coalesce(q.FotoMoeglich; false))}; KommentarPflicht: Coalesce(q.KommentarPflicht; false); Grenzmodus: {Value: fnGrenzmodus(q.Grenzmodus.Value)}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: Coalesce(q.HinweisBildID; 0); Abschnitt: Coalesce(q.Abschnitt; ""); Kritisch: Coalesce(q.Kritisch; false); KritischText: Coalesce(q.KritischText; ""); Ansprechpartner: Coalesce(q.Ansprechpartner; ""); Rueckfrage: Coalesce(q.Rueckfrage; false); RueckfrageText: Coalesce(q.RueckfrageText; ""); TextIO: Coalesce(q.TextIO; ""); TextNIO: Coalesce(q.TextNIO; ""); NichtMessbar: Coalesce(q.NichtMessbar; false); AbwMax: q.AbwMax; AbwProzent: Coalesce(q.AbwProzent; false); NurSteigend: Coalesce(q.NurSteigend; false); VergleichPunkt: 0; VergleichTol: q.VergleichTol; AnleitungID: Coalesce(q.AnleitungID; 0)}).ID; 0))}
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
    ClearCollect(colAnlAktiv; ShowColumns(Filter(RG_Anleitungen; Aktiv = true); ID));;
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
+    ClearCollect(colAnlAktiv; ShowColumns(Filter(RG_Anleitungen; Aktiv = true); ID));;
```

**Kurz erklärt:** Kopie/neue Fassung übernehmen die Anleitung. Beim Laden werden die aktiven Anleitungen für die Prüfung gelesen.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

## Test

1. Builder → „Anleitungen“ → „+ Anleitung“: Titel „Kompressor ablesen“, Text mit mehreren Absätzen.
2. Prüfpunkt → „Anleitung“ wählen → Vorschau „ⓘ Anleitung …“. Aktivieren (oder in der Vorlage/im Entwurf).
3. Rundgang-App: Kategorie öffnen → ⓘ neben der Frage → Fenster mit Text (bei langem Text scrollen), Beispielbild darunter, „Schließen“.
4. Anleitung im Builder inaktiv stellen → Prüfung zeigt den Hinweis.

## Rückweg

Vorher-Fassungen im Anhang einsetzen, dann die neuen Steuerelemente und den Bildschirm löschen. Liste/Spalte dürfen bleiben.

## Anhang – Vorher-Fassungen

**Rundgang-App `scrKategorie.OnVisible` vorher**

```
Set(varIsLoading; true);;
Set(varZurueckFrage; false);;
Set(varAlleIOFrage; false);;
Set(varZeigeFehlend; false);;
Set(varFotoPP; 0);;
Set(varBildID; 0);;
Set(varRueckPP; 0);;
Set(varKritPP; 0);;
Clear(colFotos);;
Set(varGeaendert; false);;
Set(varSchluesselK; "D" & varDurchID & "-K" & varKatID);;
Set(varNurLesen; varDurch.Status <> stInArbeit);;
Refresh(RG_KategorieErgebnisse);;
Concurrent(
    ClearCollect(colPP; Filter(RG_Pruefpunkte; KategorieID = varKatID && Aktiv = true));
    Set(varErgebnis; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK));
    ClearCollect(colKontakte; Filter(RG_Ansprechpartner; Aktiv = true))
);;
If(!varNurLesen && varLetzteFuer <> varDurchID && CountRows(Filter(colPP; !IsBlank(AbwMax) || Coalesce(NurSteigend; false))) > 0;
    Set(varLetzteFuer; varDurchID);;
    Set(varLetzteRg; varDurch.RundgangID);;
    Set(varLetzteTest; varDurch.TestDatensatz);;
    Set(varLetzteDurch; First(Sort(Filter(RG_Durchfuehrungen; RundgangID = varLetzteRg && Status = stAbgeschlossen && TestDatensatz = varLetzteTest); ID; SortOrder.Descending)));;
    If(IsBlank(varLetzteDurch.ID);
        Clear(colLetzte);
        Set(varLetzteID; varLetzteDurch.ID);;
        ClearCollect(colLetzte; Filter(Ungroup(ForAll(Filter(RG_KategorieErgebnisse; DurchfuehrungID = varLetzteID) As e; {T: ForAll(Table(ParseJSON(e.Antworten)) As j; {PP: Value(j.Value.PruefpunktID); Z: Value(j.Value.WertZahl)})}); T); !IsBlank(Z)))
    )
);;
Set(varGespeichertBeimOeffnen; varErgebnis.GespeichertAm);;
With({t: If(IsBlank(varErgebnis.Antworten); Table(ParseJSON("[]")); Table(ParseJSON(varErgebnis.Antworten)))};
    If(varNurLesen && !IsEmpty(t);
        ClearCollect(colAntworten;
            ForAll(Sequence(CountRows(t)) As i;
                With({a: Index(t; i.Value).Value};
                    With({pp: LookUp(colPP; ID = Value(a.PruefpunktID))};
                        {PruefpunktID: Value(a.PruefpunktID); Frage: Text(a.Frage); Typ: Text(a.Typ); Pflicht: false; Einheit: Coalesce(Text(a.Einheit); ""); MinWert: pp.MinWert; MaxWert: pp.MaxWert; Auswahl: Coalesce(Text(a.WertText); ""); Hinweis: ""; Reihenfolge: i.Value;
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); BildID: Coalesce(pp.HinweisBildID; 0); Abschnitt: Trim(Coalesce(Text(a.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(a.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(a.KritischOk); false); false); KritischZeit: Coalesce(Text(a.KritischZeit); ""); KritischVon: Coalesce(Text(a.KritischVon); ""); TextIO: Coalesce(Text(a.TextIO); ""); TextNIO: Coalesce(Text(a.TextNIO); ""); NMErlaubt: false; KPflOrig: false; Letzter: Value(a.Letzter); LetzterTag: Coalesce(Text(a.LetzterTag); ""); AbwMax: Blank(); AbwProzent: false; NurSteigend: false; VglID: 0; VglTol: 0; AbwText: Coalesce(Text(a.AbwText); ""); Inaktiv: false}
                    )
                )
            )
        );
        ClearCollect(colAntworten;
            ForAll(Sort(colPP; RgReihenfolge) As p;
                With({alt: LookUp(t As j; Value(j.Value.PruefpunktID) = p.ID)};
                    {PruefpunktID: p.ID; Frage: p.Title; Typ: p.Eingabetyp.Value; Pflicht: p.Pflicht; Einheit: Coalesce(p.Einheit; ""); MinWert: p.MinWert; MaxWert: p.MaxWert; Auswahl: Coalesce(p.Auswahlwerte; ""); Hinweis: Coalesce(p.Hinweis; ""); Reihenfolge: p.RgReihenfolge;
                     Bewertung: If(IsBlank(alt); ""; p.Eingabetyp.Value = "ZAHL" && !IsBlank(alt.Value.WertZahl); fnZahlBewertung(Value(alt.Value.WertZahl); p.MinWert; p.MaxWert; fnGrenzmodus(p.Grenzmodus.Value)); Coalesce(Text(alt.Value.Bewertung); ""));
                     WertText: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.WertText); ""));
                     WertZahl: If(IsBlank(alt); Blank(); Value(alt.Value.WertZahl));
                     Kommentar: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.Kommentar); ""));
                     Fotos: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.Fotos); ""));
                     FotoModus: fnFotoModus(p.Foto.Value; Coalesce(p.FotoMoeglich; false));
                     KommentarPflicht: Coalesce(p.KommentarPflicht; false);
                     Grenzmodus: fnGrenzmodus(p.Grenzmodus.Value);
                     BedID: Coalesce(p.BedingungPunkt; 0);
                     BedWert: Coalesce(p.BedingungWert; "");
                     Ausgeblendet: false;
                     BildID: Coalesce(p.HinweisBildID; 0);
                     Abschnitt: Trim(Coalesce(p.Abschnitt; ""));
                     AbsKopf: false;
                     Kritisch: Coalesce(p.Kritisch; false);
                     KritischText: Coalesce(p.KritischText; "");
                     Ansprechpartner: Coalesce(p.Ansprechpartner; "");
                     Rueckfrage: Coalesce(p.Rueckfrage; false);
                     RueckfrageText: Coalesce(p.RueckfrageText; "");
                     KritischOk: If(IsBlank(alt); false; Coalesce(IfError(Boolean(alt.Value.KritischOk); false); false));
                     KritischZeit: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.KritischZeit); ""));
                     KritischVon: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.KritischVon); ""));
                     TextIO: Trim(Coalesce(p.TextIO; ""));
                     TextNIO: Trim(Coalesce(p.TextNIO; ""));
                     NMErlaubt: Coalesce(p.NichtMessbar; false);
                     KPflOrig: Coalesce(p.KommentarPflicht; false);
                     Letzter: If(p.Eingabetyp.Value = "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend; false)); Coalesce(LookUp(colLetzte; PP = p.ID).Z; LookUp(colLetzte; PP = Coalesce(p.QuelleID; -1)).Z));
                     LetzterTag: If(IsBlank(varLetzteDurch.TagText); ""; Text(DateValue(varLetzteDurch.TagText); "dd.mm."));
                     AbwMax: p.AbwMax;
                     AbwProzent: Coalesce(p.AbwProzent; false);
                     NurSteigend: Coalesce(p.NurSteigend; false);
                     VglID: Coalesce(p.VergleichPunkt; 0);
                     VglTol: Coalesce(p.VergleichTol; 0);
                     AbwText: "";
                     Warnung: false;
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Warnung: Coalesce(IfError(Boolean(o.Value.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); BildID: 0; Abschnitt: Trim(Coalesce(Text(o.Value.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(o.Value.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(o.Value.KritischOk); false); false); KritischZeit: Coalesce(Text(o.Value.KritischZeit); ""); KritischVon: Coalesce(Text(o.Value.KritischVon); ""); TextIO: Coalesce(Text(o.Value.TextIO); ""); TextNIO: Coalesce(Text(o.Value.TextNIO); ""); NMErlaubt: false; KPflOrig: false; Letzter: Value(o.Value.Letzter); LetzterTag: Coalesce(Text(o.Value.LetzterTag); ""); AbwMax: Blank(); AbwProzent: false; NurSteigend: false; VglID: 0; VglTol: 0; AbwText: Coalesce(Text(o.Value.AbwText); ""); Inaktiv: true}
            )
        )
    )
);;
If(!varNurLesen; ClearCollect(colVglTmp; ForAll(Filter(colAntworten As a0; !a0.Inaktiv && a0.Typ = "ZAHL" && (a0.VglID <> 0 || !IsBlank(a0.Letzter))) As a;
        With({w: LookUp(colAntworten As o; o.PruefpunktID = a.VglID)};
            {PP: a.PruefpunktID;
             Abw: fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend);
             Vgl: a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol);
             Text: If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); If(a.NurSteigend && a.WertZahl < a.Letzter; "kleiner als beim letzten Mal"; "starke Abweichung zum letzten Mal"); "") & If(a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol); If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); "; "; "") & "weicht von „" & w.Frage & "“ ab (" & Text(w.WertZahl) & ")"; "");
             KPfl: a.KPflOrig}
        )
    ));;
    ForAll(colVglTmp As v; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = v.PP); {KommentarPflicht: v.KPfl || v.Abw || v.Vgl; AbwText: v.Text})));;
ClearCollect(colAbsTmp; ShowColumns(Filter(colAntworten; !Inaktiv && !Ausgeblendet && Abschnitt <> ""); PruefpunktID; Reihenfolge; Abschnitt; BedID));;
ForAll(colAbsTmp As t;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = t.PruefpunktID);
        {AbsKopf: With({g: Filter(colAbsTmp As u; Lower(u.Abschnitt) = Lower(t.Abschnitt))};
            If(IsEmpty(Filter(g As u1; u1.BedID = 0)); t.Reihenfolge * 1000000 + t.PruefpunktID = Min(g; Reihenfolge * 1000000 + PruefpunktID); t.BedID = 0 && t.Reihenfolge * 1000000 + t.PruefpunktID = Min(Filter(g As u2; u2.BedID = 0); Reihenfolge * 1000000 + PruefpunktID)))}
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
```

**Rundgang-App `lblKaFrage.Width` vorher**

```
Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0)
```

**Builder `App.OnStart` vorher**

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

**Builder `lblPFoto.Width` vorher**

```
528
```

**Builder `ddPFoto.Width` vorher**

```
528
```

**Builder `ddPFoto.Items` vorher**

```
Table({W: "Aus"; N: "kein Foto (bei n.i.O. möglich)"}; {W: "Optional"; N: "Foto freiwillig"}; {W: "Pflicht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto Pflicht bei Mangel (n.i.O.)"})
```

**Builder `ddPFoto.Default` vorher**

```
LookUp(Table({W: "Aus"; N: "kein Foto (bei n.i.O. möglich)"}; {W: "Optional"; N: "Foto freiwillig"}; {W: "Pflicht"; N: "Foto immer Pflicht"}; {W: "Bei Mangel Pflicht"; N: "Foto Pflicht bei Mangel (n.i.O.)"}); W = fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))).N
```

**Builder `lblVsRegeln.Text` vorher**

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NichtMessbar; false); Char(10) & "• „nicht messbar“ erlaubt (dann Begründung Pflicht)"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && !IsBlank(LookUp(colP; ID = varAuswahlID).AbwMax); Char(10) & "• höchstens " & Text(LookUp(colP; ID = varAuswahlID).AbwMax) & If(Coalesce(LookUp(colP; ID = varAuswahlID).AbwProzent; false); " %"; "") & " Abweichung zum letzten Rundgang"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NurSteigend; false); Char(10) & "• Zählerstand: darf nicht kleiner werden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).VergleichPunkt; 0) <> 0; Char(10) & "• Vergleich mit „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).VergleichPunkt).Title & "“ (± " & Text(Coalesce(LookUp(colP; ID = varAuswahlID).VergleichTol; 0)) & ")"; "")
```

**Builder `btnGlNeuP.OnSelect` vorher**

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

**Builder `btnMehrAnlegen.OnSelect` vorher**

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

**Builder `galAkt.Items` vorher**

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

**Builder `galPr.Items` vorher**

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

**Builder `tmrArbeit.OnTimerEnd` vorher**

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

