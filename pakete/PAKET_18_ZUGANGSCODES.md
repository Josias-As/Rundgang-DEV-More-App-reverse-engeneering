# Paket 18 – Zugangscodes (Bedien-Codes, erst nach Antippen sichtbar)

Stand 06.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket18), `werkzeuge/builder.py`, `werkzeuge/doc_paket18.py`. Voraussetzung: Paket 23 in beiden Apps.

## Kurzfassung

- Eigene Liste `RG_Zugangscodes`. Im Builder am Prüfpunkt über den Knopf **🔑** neben dem Hinweis zuordnen; Codes pflegen unter Übersicht › Anleitungen › **Zugangscodes**.
- In der Rundgang-App: runder Knopf **🔑** oben rechts in der Karte. Erst nach Antippen öffnet sich ein Fenster mit dem Code (groß) und dem Hinweis. Der Code wird erst dann gelesen.
- **Nie** im Protokoll, PDF, in Mängeln oder im JSON: Der Code liegt nur in der Liste und in einer Variablen, solange das Fenster offen ist.
- Echte Passwörter kommen nicht in die App: Code leer lassen und im Hinweis z. B. „Code bei der IT (Herr …)“ eintragen.
- Umfang: App 2 Properties + Knopf + Fenster; Builder 7 Properties + `btnAnCodes`, `btnPCode`, `conPCodeFenster`, `scrCodes`. Generatoren 0 Fehler, Mutation 12/12 und 13/13. **Nicht in Studio getestet.**

## Teil A – Rundgang DEV

### A1 – SharePoint und Daten (zuerst)

- Neue Liste **`RG_Zugangscodes`**: `Title` (vorhanden, = Bezeichnung), `Code` (Eine Textzeile), `Hinweis` (Mehrere Textzeilen, nur Text), `Aktiv` (Ja/Nein, Standard Ja).
- **Berechtigung:** Lesen für alle Prüfer (wie die anderen RG-Listen). Bedien-Codes sind damit für jeden mit Listenzugriff in SharePoint lesbar – deshalb nie echte Passwörter.
- `RG_Pruefpunkte`: neue Spalte **`ZugangscodeID`** (Zahl, Standard 0).
- Rundgang DEV: Daten → `RG_Pruefpunkte` → ⋯ → Aktualisieren, dann Daten hinzufügen → SharePoint → IMS+ → `RG_Zugangscodes`.

**Kurzzeitig rot (erwartet):** `btnKaCode` nennt `ThisItem.CodeID`, das erst A3.1 (`scrKategorie.OnVisible`) anlegt.

### A2.1 – neues Steuerelement `btnKaCode`

**Wo hin:** in der Strukturansicht **`conKaKarte`** markieren → Strg+V.

```yaml
- btnKaCode:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrPrimaer
      BorderThickness: =1
      Color: =clrPrimaer
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =40
      HoverColor: =clrPrimaer
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =Refresh(RG_Zugangscodes);
        Set(varCode, LookUp(RG_Zugangscodes, ID = ThisItem.CodeID));
        If(IsBlank(varCode.ID) || !Coalesce(varCode.Aktiv, false),
            Notify("Für diesen Prüfpunkt ist kein Code hinterlegt.", NotificationType.Warning),
            Set(varCodeFrage, ThisItem.Frage);
            Set(varCodeOffen, true)
        )
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =20
      RadiusBottomRight: =20
      RadiusTopLeft: =20
      RadiusTopRight: =20
      Size: =15
      Text: ="🔑"
      Visible: =ThisItem.CodeID > 0
      Width: =40
      X: =Parent.Width - 60 - If(ThisItem.BildID > 0, 80, 0) - If(ThisItem.AnlID > 0, 48, 0)
      Y: =7
```

### A2.2 – neues Steuerelement `conKaCode`

**Wo hin:** in der Strukturansicht **`scrKategorie`** markieren → Strg+V.

```yaml
- conKaCode:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      Fill: =RGBA(0, 0, 0, 0.45)
      Height: =Parent.Height
      Visible: =varCodeOffen
      Width: =Parent.Width
    Children:
    - btnKaCodeSperre:
        Control: Classic/Button@2.2.0
        Properties:
          BorderThickness: =0
          Fill: =RGBA(0, 0, 0, 0)
          Height: =Parent.Height
          HoverFill: =RGBA(0, 0, 0, 0)
          PressedFill: =RGBA(0, 0, 0, 0)
          Text: =""
          Width: =Parent.Width
    - conKaCodeKarte:
        Control: GroupContainer@1.5.0
        Variant: ManualLayout
        Properties:
          Fill: =clrKarte
          Height: =360
          RadiusBottomLeft: =16
          RadiusBottomRight: =16
          RadiusTopLeft: =16
          RadiusTopRight: =16
          Width: =Parent.Width - 96
          X: =48
          Y: =(Parent.Height - Self.Height) / 2
        Children:
        - lblKaCodeTitel:
            Control: Label@2.5.1
            Properties:
              Color: =clrPrimaer
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =40
              Size: =19
              Text: =If(varCodeOffen, "🔑 " & varCode.Title, "")
              Width: =Parent.Width - 40
              Wrap: =false
              X: =20
              Y: =14
        - lblKaCodeFrage:
            Control: Label@2.5.1
            Properties:
              Color: =clrTextGrau
              Font: =Font.'Segoe UI'
              Height: =28
              Size: =13
              Text: |-
                ="zu: " & varCodeFrage
              Width: =Parent.Width - 40
              Wrap: =false
              X: =20
              Y: =54
        - lblKaCodeWert:
            Control: Label@2.5.1
            Properties:
              Align: =Align.Center
              Color: =clrText
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =72
              Size: =34
              Text: =If(varCodeOffen && Trim(Coalesce(varCode.Code, "")) <> "", varCode.Code, "—")
              Width: =Parent.Width - 40
              X: =20
              Y: =96
        - lblKaCodeHinweis:
            Control: Label@2.5.1
            Properties:
              Color: =clrTextGrau
              Font: =Font.'Segoe UI'
              Height: =84
              Size: =14
              Text: =If(varCodeOffen, Coalesce(varCode.Hinweis, ""), "")
              VerticalAlign: =VerticalAlign.Top
              Width: =Parent.Width - 40
              X: =20
              Y: =180
        - btnKaCodeSchliessen:
            Control: Classic/Button@2.2.0
            Properties:
              BorderThickness: =0
              Color: =Color.White
              Fill: =clrPrimaer
              Font: =Font.'Segoe UI'
              Height: =56
              HoverFill: =ColorFade(clrPrimaer, -20%)
              OnSelect: =Set(varCodeOffen, false)
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

### A3 – geänderte Properties

### A3.1 · `scrKategorie.OnVisible`

**Pfad:** `scrKategorie` → OnVisible

```
Set(varIsLoading; true);;
Set(varZurueckFrage; false);;
Set(varAlleIOFrage; false);;
Set(varZeigeFehlend; false);;
Set(varFotoPP; 0);;
Set(varBildID; 0);;
Set(varInfoID; 0);;
Set(varCodeOffen; false);;
Set(varRueckPP; 0);;
Set(varKritPP; 0);;
Clear(colFotos);;
Set(varGeaendert; false);;
Set(varSchluesselK; "D" & varDurchID & "-K" & varKatID);;
Set(varNurLesen; varDurch.Status <> stInArbeit);;
Refresh(RG_KategorieErgebnisse);;
Refresh(RG_Anleitungen);;
Concurrent(
    ClearCollect(colPP; Filter(RG_Pruefpunkte; KategorieID = varKatID && Aktiv = true));
    Set(varErgebnis; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK));
    ClearCollect(colKontakte; Filter(RG_Ansprechpartner; Aktiv = true));
    ClearCollect(colAnlAktivApp; ShowColumns(Filter(RG_Anleitungen; Aktiv = true); ID))
);;
If(!varNurLesen && varLetzteFuer <> varDurchID && CountRows(Filter(colPP; !IsBlank(AbwMax) || Coalesce(NurSteigend; false))) > 0;
    Set(varLetzteFuer; varDurchID);;
    Set(varLetzteRg; varDurch.RundgangID);;
    Set(varLetzteTest; varDurch.TestDatensatz);;
    Set(varLetzteTag; varDurch.TagText);;
    Refresh(RG_Durchfuehrungen);;
    ClearCollect(colLetzteKand; FirstN(Sort(Filter(RG_Durchfuehrungen; RundgangID = varLetzteRg && Status = stAbgeschlossen && TestDatensatz = varLetzteTest); TagText; SortOrder.Descending); 20));;
    Set(varLetzteDurch; First(Sort(Filter(colLetzteKand; DateValue(TagText) < DateValue(varLetzteTag)); TagText; SortOrder.Descending)));;
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
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); BildID: Coalesce(pp.HinweisBildID; 0); Abschnitt: Trim(Coalesce(Text(a.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(a.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(a.KritischOk); false); false); KritischZeit: Coalesce(Text(a.KritischZeit); ""); KritischVon: Coalesce(Text(a.KritischVon); ""); TextIO: Coalesce(Text(a.TextIO); ""); TextNIO: Coalesce(Text(a.TextNIO); ""); NMErlaubt: false; KPflOrig: false; Letzter: Value(a.Letzter); LetzterTag: Coalesce(Text(a.LetzterTag); ""); AbwMax: Blank(); AbwProzent: false; NurSteigend: false; VglID: 0; VglTol: 0; AbwText: Coalesce(Text(a.AbwText); ""); AnlID: If(IsBlank(LookUp(colAnlAktivApp; ID = Coalesce(pp.AnleitungID; 0))); 0; pp.AnleitungID); CodeID: Coalesce(pp.ZugangscodeID; 0); Inaktiv: false}
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
                     AnlID: If(IsBlank(LookUp(colAnlAktivApp; ID = Coalesce(p.AnleitungID; 0))); 0; p.AnleitungID);
                     CodeID: Coalesce(p.ZugangscodeID; 0);
                     Warnung: false;
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Warnung: Coalesce(IfError(Boolean(o.Value.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); BildID: 0; Abschnitt: Trim(Coalesce(Text(o.Value.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(o.Value.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(o.Value.KritischOk); false); false); KritischZeit: Coalesce(Text(o.Value.KritischZeit); ""); KritischVon: Coalesce(Text(o.Value.KritischVon); ""); TextIO: Coalesce(Text(o.Value.TextIO); ""); TextNIO: Coalesce(Text(o.Value.TextNIO); ""); NMErlaubt: false; KPflOrig: false; Letzter: Value(o.Value.Letzter); LetzterTag: Coalesce(Text(o.Value.LetzterTag); ""); AbwMax: Blank(); AbwProzent: false; NurSteigend: false; VglID: 0; VglTol: 0; AbwText: Coalesce(Text(o.Value.AbwText); ""); AnlID: 0; CodeID: 0; Inaktiv: true}
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
+Set(varCodeOffen; false);;
- Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); " …
+ Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); " …
+                     CodeID: Coalesce(p.ZugangscodeID; 0);
- Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Val …
+ Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Val …
```

**Kurz erklärt:** Neues Feld `CodeID` in allen drei Zweigen von `colAntworten` (nicht im JSON – `btnKaSpeichern` speichert nur ausgewählte Spalten). Das Code-Fenster ist beim Öffnen zu.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

### A3.2 · `lblKaFrage.Width`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaFrage` → Width

```
Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0) - If(ThisItem.CodeID > 0; 48; 0)
```

```diff
-Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0)
+Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0) - If(ThisItem.CodeID > 0; 48; 0)
```

**Kurz erklärt:** Platz für den 🔑-Knopf.

**Nachprüfen:** endet auf `dID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0) - If(ThisItem.CodeID > 0; 48; 0)`

## Teil B – Builder

### B0 – Daten

Liste und Spalte aus A1 (nur einmal anlegen). Builder: `RG_Pruefpunkte` aktualisieren, `RG_Zugangscodes` hinzufügen.

### B1.1 – neues Steuerelement `btnAnCodes`

**Wo hin:** **`conAnKopf`** markieren → Strg+V.

```yaml
- btnAnCodes:
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
      OnSelect: =If(!varIsLoading, Navigate(scrCodes, ScreenTransition.None))
      PressedColor: =Color.White
      PressedFill: =RGBA(255, 255, 255, 0.32)
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =14
      Text: ="🔑 Zugangscodes ›"
      Width: =220
      X: =Parent.Width - 236
      Y: =12
```

### B1.2 – neues Steuerelement `btnPCode`

**Wo hin:** **`conPRest`** markieren → Strg+V.

```yaml
- btnPCode:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrPrimaer
      BorderThickness: =1
      Color: =clrPrimaer
      DisabledBorderColor: =clrGesperrtHell
      DisabledColor: =clrGesperrt
      DisabledFill: =clrGesperrtHell
      DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
      Fill: =If(Coalesce(LookUp(colP, ID = varAuswahlID).ZugangscodeID, 0) > 0, clrPrimaerHell, clrKarte)
      Font: =Font.'Segoe UI'
      Height: =44
      HoverColor: =clrPrimaer
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =If(!varIsLoading,
            Refresh(RG_Zugangscodes);
            Reset(ddPCode);
            Set(varCodeOffen, true)
        )
      PaddingLeft: =2
      PaddingRight: =2
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =13
      Text: ="🔑"
      Width: =48
      X: =298
      Y: =144
```

### B1.3 – neues Steuerelement `conPCodeFenster`

**Wo hin:** **`scrEditor`** markieren → Strg+V.

```yaml
- conPCodeFenster:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      BorderThickness: =0
      Fill: =RGBA(0, 0, 0, 0.45)
      Height: =Parent.Height
      Visible: =varCodeOffen
      Width: =Parent.Width
    Children:
      - btnPCodeFensterSperre:
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
      - conPCodeFensterKarte:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrKarte
            Height: =360
            RadiusBottomLeft: =12
            RadiusBottomRight: =12
            RadiusTopLeft: =12
            RadiusTopRight: =12
            Width: =620
            X: =(Parent.Width - Self.Width) / 2
            Y: =(Parent.Height - Self.Height) / 2
          Children:
            - lblPCodeFensterTitel:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =40
                  Size: =18
                  Text: ="Zugangscode"
                  Width: =572
                  X: =24
                  Y: =16
            - lblPCodeFrage:
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
            - lblPCodeT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Zugangscode (z. B. Bedien-Code einer Anlage)"
                  Width: =572
                  X: =24
                  Y: =96
            - ddPCode:
                Control: Classic/DropDown@2.3.1
                Properties:
                  AccessibleLabel: ="Zugangscode"
                  BorderColor: =clrRahmen
                  BorderThickness: =1
                  ChevronBackground: =clrPrimaer
                  ChevronFill: =Color.White
                  ChevronHoverBackground: =ColorFade(clrPrimaer, -20%)
                  ChevronHoverFill: =Color.White
                  Color: =clrText
                  Default: |-
                    =With({akt: Sort(ShowColumns(Filter(RG_Zugangscodes, Aktiv = true), ID, Title), Title), cur: Coalesce(LookUp(colP, ID = varAuswahlID).ZugangscodeID, 0)}, If(cur = 0, "— keine —", IsBlank(LookUp(akt As a2, a2.ID = cur)), Coalesce(LookUp(RG_Zugangscodes, ID = cur).Title, "Code #" & cur) & " (inaktiv oder gelöscht)", With({n: LookUp(akt As a3, a3.ID = cur)}, n.Title & If(CountRows(Filter(akt As d, d.Title = n.Title)) > 1, " (#" & n.ID & ")", ""))))
                  DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
                  Fill: =clrKarte
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HoverFill: =clrPrimaerHell
                  Items: |-
                    =With({akt: Sort(ShowColumns(Filter(RG_Zugangscodes, Aktiv = true), ID, Title), Title), cur: Coalesce(LookUp(colP, ID = varAuswahlID).ZugangscodeID, 0)}, Ungroup(Table({T: Table({ID: 0, N: "— keine —"})}, {T: ForAll(akt As n, {ID: n.ID, N: n.Title & If(CountRows(Filter(akt As d, d.Title = n.Title)) > 1, " (#" & n.ID & ")", "")})}, {T: Filter(Table({ID: cur, N: Coalesce(LookUp(RG_Zugangscodes, ID = cur).Title, "Code #" & cur) & " (inaktiv oder gelöscht)"}), cur <> 0 && IsBlank(LookUp(akt As a2, a2.ID = cur)))}), T))
                  Items.Value: =N
                  OnChange: |-
                    =If(!IsBlank(Self.Selected) && Self.Selected.ID <> Coalesce(LookUp(colP, ID = varAuswahlID).ZugangscodeID, 0),
                        If(varSchreibbar && varAuswahlEbene = 3,
                            Refresh(RG_Rundgaenge);
                            Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                            If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                            If(varEntwurfOk,
                                Set(varPatchFehler, false);
                                IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {ZugangscodeID: Self.Selected.ID}), Set(varPatchFehler, true));
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
                  Y: =116
            - lblPCodeHinweis:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =100
                  Size: =12
                  Text: |-
                    ="Der Prüfer sieht den Code erst nach Antippen von 🔑. Er steht nie im Protokoll, im PDF oder in Mängeln. Echte Passwörter (Netzwerk, Server, Admin) nicht eintragen – stattdessen im Hinweis „Code bei …“. Codes anlegen: Übersicht › Anleitungen › Zugangscodes."
                  VerticalAlign: =VerticalAlign.Top
                  Width: =572
                  X: =24
                  Y: =168
            - btnPCodeFertig:
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
                  OnSelect: =Set(varCodeOffen, false)
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
                  Y: =292
            - btnPCodeFensterZu:
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
                  OnSelect: =Set(varCodeOffen, false)
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

### B1.4 – neuer Bildschirm `scrCodes`

**Wo hin:** einen Bildschirm markieren → Strg+V.

```yaml
Screens:
  scrCodes:
    Properties:
      Fill: =clrHintergrund
      OnVisible: |-
        =Set(varIsLoading, true);
        Set(varLadeText, "");
        Refresh(RG_Zugangscodes);
        ClearCollect(colZcAlle, RG_Zugangscodes);
        Set(varZcID, Coalesce(First(Sort(colZcAlle, If(Coalesce(Aktiv, false), "0", "1") & Lower(Title))).ID, 0));
        Reset(txtZcTitel);
        Reset(txtZcCode);
        Reset(txtZcHinweis);
        Set(varIsLoading, false)
    Children:
      - conZcKopf:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrPrimaer
            Height: =64
            Width: =Parent.Width
          Children:
            - btnZcZurueck:
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
                  OnSelect: =If(!varIsLoading, Navigate(scrAnleitungen, ScreenTransition.None))
                  PressedColor: =Color.White
                  PressedFill: =RGBA(255, 255, 255, 0.32)
                  RadiusBottomLeft: =6
                  RadiusBottomRight: =6
                  RadiusTopLeft: =6
                  RadiusTopRight: =6
                  Size: =14
                  Text: ="← Anleitungen"
                  Width: =170
                  X: =16
                  Y: =12
            - lblZcTitelKopf:
                Control: Label@2.5.1
                Properties:
                  Color: =Color.White
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =64
                  Size: =20
                  Text: ="Zugangscodes"
                  Width: =600
                  X: =202
                  Y: =0
      - lblZcHilfe:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =44
            Size: =13
            Text: ="Nur Bedien-Codes von Anlagen. Der Prüfer sieht sie erst nach Antippen von 🔑, nie im Protokoll. Echte Passwörter nicht eintragen – dafür nur einen Hinweis wie „Code bei der IT“ (Feld Code leer lassen)."
            Width: =Parent.Width - 48
            X: =24
            Y: =72
      - btnZcNeu:
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
                  Set(varNeuID, IfError(Patch(RG_Zugangscodes, Defaults(RG_Zugangscodes), {Title: "Neuer Code", Code: "", Hinweis: "", Aktiv: true}).ID, 0));
                  If(varNeuID = 0,
                      Notify("Anlegen fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
                      Collect(colZcAlle, LookUp(RG_Zugangscodes, ID = varNeuID));
                      Set(varZcID, varNeuID);
                      Reset(txtZcTitel);
                      Reset(txtZcCode);
                      Reset(txtZcHinweis);
                      SetFocus(txtZcTitel)
                  )
              )
            PressedColor: =Color.White
            PressedFill: =ColorFade(clrPrimaer, -35%)
            RadiusBottomLeft: =6
            RadiusBottomRight: =6
            RadiusTopLeft: =6
            RadiusTopRight: =6
            Size: =14
            Text: ="+ Zugangscode"
            Width: =220
            X: =24
            Y: =124
      - galZc:
          Control: Gallery@2.15.0
          Variant: Vertical
          Properties:
            AccessibleLabel: ="Zugangscodes"
            Height: =Parent.Height - 196
            Items: =Sort(colZcAlle, If(Coalesce(Aktiv, false), "0", "1") & Lower(Title))
            ShowScrollbar: =true
            TemplatePadding: =0
            TemplateSize: =56
            Width: =420
            X: =24
            Y: =180
          Children:
            - lblZcHinter:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Fill: =If(ThisItem.ID = varZcID, clrPrimaerHell, Color.White)
                  Font: =Font.'Segoe UI'
                  Height: =Parent.TemplateHeight - 4
                  Size: =14
                  Text: =""
                  Width: =Parent.TemplateWidth
                  X: =0
                  Y: =0
            - lblZcZeile:
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
            - btnZcZeile:
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
                    =Set(varZcID, ThisItem.ID);
                    Reset(txtZcTitel);
                    Reset(txtZcCode);
                    Reset(txtZcHinweis)
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
      - lblZcLeer:
          Control: Label@2.5.1
          Properties:
            Color: =clrTextGrau
            Font: =Font.'Segoe UI'
            Height: =48
            Size: =13
            Text: ="Noch keine Zugangscodes. „+ Zugangscode“ legt einen an."
            Visible: =IsEmpty(colZcAlle) && !varIsLoading
            Width: =420
            X: =24
            Y: =190
      - conZcForm:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =clrHintergrund
            Height: =400
            Visible: =varZcID > 0
            Width: =Parent.Width - 492
            X: =468
            Y: =124
          Children:
            - lblZcTitelT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Bezeichnung"
                  Width: =400
                  X: =0
                  Y: =0
            - txtZcTitel:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Bezeichnung"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colZcAlle, ID = varZcID).Title, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HintText: ="z. B. Bedienteil Kältemaschine 1"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colZcAlle, ID = varZcID).Title, "")),
                        If(varZcID > 0 && !varIsLoading && !IsBlank(LookUp(RG_Zugangscodes, ID = varZcID).ID),
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Zugangscodes, LookUp(RG_Zugangscodes, ID = varZcID), {Title: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colZcAlle, LookUp(colZcAlle, ID = varZcID), LookUp(RG_Zugangscodes, ID = varZcID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =20
            - lblZcCodeT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Code"
                  Width: =400
                  X: =0
                  Y: =72
            - txtZcCode:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Code"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colZcAlle, ID = varZcID).Code, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =40
                  HintText: ="z. B. 1234 (leer lassen, wenn nur ein Hinweis)"
                  HoverBorderColor: =clrPrimaer
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colZcAlle, ID = varZcID).Code, "")),
                        If(varZcID > 0 && !varIsLoading && !IsBlank(LookUp(RG_Zugangscodes, ID = varZcID).ID),
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Zugangscodes, LookUp(RG_Zugangscodes, ID = varZcID), {Code: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colZcAlle, LookUp(colZcAlle, ID = varZcID), LookUp(RG_Zugangscodes, ID = varZcID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =92
            - lblZcHinweisT:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =20
                  Size: =12
                  Text: ="Hinweis (z. B. „Code bei der IT“)"
                  Width: =400
                  X: =0
                  Y: =144
            - txtZcHinweis:
                Control: Classic/TextInput@2.3.2
                Properties:
                  AccessibleLabel: ="Hinweis"
                  BorderColor: =clrRahmen
                  Color: =clrText
                  Default: =Coalesce(LookUp(colZcAlle, ID = varZcID).Hinweis, "")
                  DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                  Fill: =clrKarte
                  FocusedBorderColor: =clrPrimaer
                  Font: =Font.'Segoe UI'
                  Height: =80
                  HintText: ="optional"
                  HoverBorderColor: =clrPrimaer
                  Mode: =TextMode.MultiLine
                  OnChange: |-
                    =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colZcAlle, ID = varZcID).Hinweis, "")),
                        If(varZcID > 0 && !varIsLoading && !IsBlank(LookUp(RG_Zugangscodes, ID = varZcID).ID),
                            Set(varPatchFehler, false);
                            IfError(Patch(RG_Zugangscodes, LookUp(RG_Zugangscodes, ID = varZcID), {Hinweis: Trim(Self.Text)}), Set(varPatchFehler, true));
                            If(varPatchFehler,
                                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                Patch(colZcAlle, LookUp(colZcAlle, ID = varZcID), LookUp(RG_Zugangscodes, ID = varZcID))
                            )
                        )
                    )
                  Size: =14
                  Width: =Parent.Width
                  X: =0
                  Y: =164
            - galZcAktiv:
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
                  Y: =260
                Children:
                  - btnZcAktiv:
                      Control: Classic/Button@2.2.0
                      Properties:
                        BorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        BorderThickness: =1
                        Color: =If(ThisItem.W = If(Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false), "ja", "nein"), Color.White, clrText)
                        DisabledBorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false), "ja", "nein"), clrPrimaer, clrRahmen)
                        DisabledColor: =If(ThisItem.W = If(Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false), "ja", "nein"), clrPrimaer, clrTextGrau)
                        DisabledFill: =If(ThisItem.W = If(Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false), "ja", "nein"), clrPrimaerHell, clrKarte)
                        DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
                        Fill: =If(ThisItem.W = If(Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false), "ja", "nein"), clrPrimaer, clrKarte)
                        Font: =Font.'Segoe UI'
                        Height: =36
                        HoverColor: =If(ThisItem.W = If(Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false), "ja", "nein"), Color.White, clrText)
                        HoverFill: =If(ThisItem.W = If(Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false), "ja", "nein"), ColorFade(clrPrimaer, -20%), clrPrimaerHell)
                        OnSelect: |-
                          =If((ThisItem.W = "ja") <> Coalesce(LookUp(colZcAlle, ID = varZcID).Aktiv, false),
                              If(varZcID > 0 && !varIsLoading && !IsBlank(LookUp(RG_Zugangscodes, ID = varZcID).ID),
                                  Set(varPatchFehler, false);
                                  IfError(Patch(RG_Zugangscodes, LookUp(RG_Zugangscodes, ID = varZcID), {Aktiv: ThisItem.W = "ja"}), Set(varPatchFehler, true));
                                  If(varPatchFehler,
                                      Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                                      Patch(colZcAlle, LookUp(colZcAlle, ID = varZcID), LookUp(RG_Zugangscodes, ID = varZcID))
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
      - conZcLaden:
          Control: GroupContainer@1.5.0
          Variant: ManualLayout
          Properties:
            BorderThickness: =0
            Fill: =RGBA(255, 255, 255, 0.7)
            Height: =Parent.Height
            Visible: =varIsLoading
            Width: =Parent.Width
          Children:
            - btnZcLadenSperre:
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
            - lblZcLadenText:
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

### B2.1 · `App.OnStart`

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
Set(varCodeOffen; false);;
Set(varZcID; 0);;
Set(varEntwurfOk; true);;
Set(varAktivRest; false);;
Set(varVorlageNeu; Defaults(RG_Rundgaenge));;
Set(varNioOffen; false);;
Set(varKoID; 0);;
Set(varZaOffen; false);;
Set(varAnID; 0)
```

```diff
+Set(varCodeOffen; false);;
+Set(varZcID; 0);;
```

**Kurz erklärt:** Startwerte `varCodeOffen`, `varZcID`.

**Nachprüfen:** endet auf `Set(varAnID; 0)`

### B2.2 · `btnGlNeuP.OnSelect`

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
        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0) + 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: "IONIO"}; Pflicht: true; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: If(varAuswahlEbene = 3 && LookUp(colP; ID = varAuswahlID).KategorieID = varCtxK; Coalesce(LookUp(colP; ID = varAuswahlID).Abschnitt; ""); ""); TextIO: ""; TextNIO: ""; NichtMessbar: false; AbwProzent: false; NurSteigend: false; VergleichPunkt: 0; VergleichTol: 0; AnleitungID: 0; ZugangscodeID: 0}).ID; 0));;
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
- … d: false; VergleichPunkt: 0; VergleichTol: 0; AnleitungID: 0}).ID; 0));; …
+ … d: false; VergleichPunkt: 0; VergleichTol: 0; AnleitungID: 0; ZugangscodeID: 0}).ID; 0));; …
```

**Kurz erklärt:** Neuer Prüfpunkt ohne Code.

**Nachprüfen:** endet auf `)`

### B2.3 · `btnMehrAnlegen.OnSelect`

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
                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: varMehrTyp}; Pflicht: varMehrPflicht; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0; Abschnitt: Left(Trim(txtMehrAbschnitt.Text); 255); TextIO: ""; TextNIO: ""; NichtMessbar: false; AbwProzent: false; NurSteigend: false; VergleichPunkt: 0; VergleichTol: 0; AnleitungID: 0; ZugangscodeID: 0}).ID; 0)}
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
- … d: false; VergleichPunkt: 0; VergleichTol: 0; AnleitungID: 0}).ID; 0)} …
+ … d: false; VergleichPunkt: 0; VergleichTol: 0; AnleitungID: 0; ZugangscodeID: 0}).ID; 0)} …
```

**Kurz erklärt:** Wie btnGlNeuP.

**Nachprüfen:** endet auf `)`

### B2.4 · `galAkt.Items`

**Pfad:** `scrEditor › conAkt › conAktKarte › galAkt` → Items

```
Ungroup(
    Table(
        {T: ForAll(Filter(colP As p; IsBlank(LookUp(colAltP As a; a.ID = p.QuelleID))) As p; {Art: "neu"; Text: p.Title})};
        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) || Coalesce(p.Auswahlwerte; "") <> Coalesce(a.Auswahlwerte; "") || Coalesce(p.Einheit; "") <> Coalesce(a.Einheit; "") || Coalesce(p.MinWert; -999999) <> Coalesce(a.MinWert; -999999) || Coalesce(p.MaxWert; -999999) <> Coalesce(a.MaxWert; -999999) || Coalesce(p.Hinweis; "") <> Coalesce(a.Hinweis; "") || fnFotoWert(p.Foto.Value; Coalesce(p.FotoMoeglich; false)) <> fnFotoWert(a.Foto.Value; Coalesce(a.FotoMoeglich; false)) || Coalesce(p.KommentarPflicht; false) <> Coalesce(a.KommentarPflicht; false) || fnGrenzmodus(p.Grenzmodus.Value) <> fnGrenzmodus(a.Grenzmodus.Value) || Coalesce(p.BedingungWert; "") <> Coalesce(a.BedingungWert; "") || Coalesce(LookUp(colP As b0; b0.ID = p.BedingungPunkt).QuelleID; 0) <> Coalesce(a.BedingungPunkt; 0) || Coalesce(p.HinweisBildID; 0) <> Coalesce(a.HinweisBildID; 0) || Coalesce(LookUp(colK As k0; k0.ID = p.KategorieID).QuelleID; 0) <> a.KategorieID || Trim(Coalesce(p.Abschnitt; "")) <> Trim(Coalesce(a.Abschnitt; "")) || Coalesce(p.Kritisch; false) <> Coalesce(a.Kritisch; false) || Coalesce(p.KritischText; "") <> Coalesce(a.KritischText; "") || Coalesce(p.Ansprechpartner; "") <> Coalesce(a.Ansprechpartner; "") || Coalesce(p.Rueckfrage; false) <> Coalesce(a.Rueckfrage; false) || Coalesce(p.RueckfrageText; "") <> Coalesce(a.RueckfrageText; "") || Coalesce(p.TextIO; "") <> Coalesce(a.TextIO; "") || Coalesce(p.TextNIO; "") <> Coalesce(a.TextNIO; "") || Coalesce(p.NichtMessbar; false) <> Coalesce(a.NichtMessbar; false) || Coalesce(p.AbwMax; -999999) <> Coalesce(a.AbwMax; -999999) || Coalesce(p.AbwProzent; false) <> Coalesce(a.AbwProzent; false) || Coalesce(p.NurSteigend; false) <> Coalesce(a.NurSteigend; false) || Coalesce(p.VergleichTol; 0) <> Coalesce(a.VergleichTol; 0) || Coalesce(LookUp(colP As v0; v0.ID = p.VergleichPunkt).QuelleID; 0) <> Coalesce(a.VergleichPunkt; 0) || Coalesce(p.AnleitungID; 0) <> Coalesce(a.AnleitungID; 0) || Coalesce(p.ZugangscodeID; 0) <> Coalesce(a.ZugangscodeID; 0)))) As p; {Art: "geändert"; Text: p.Title})};
        {T: ForAll(Filter(colAltP As a; IsBlank(LookUp(colP As p; p.QuelleID = a.ID))) As a; {Art: "entfernt"; Text: a.Title})}
    );
    T
)
```

```diff
- … || Coalesce(p.AnleitungID; 0) <> Coalesce(a.AnleitungID; 0)))) As p; {Art: "geändert"; Text: p.Title})}; …
+ … || Coalesce(p.AnleitungID; 0) <> Coalesce(a.AnleitungID; 0) || Coalesce(p.ZugangscodeID; 0) <> Coalesce(a.ZugangscodeID; 0)))) As p; {Art: "geändert"; Text: p.Title})}; …
```

**Kurz erklärt:** Änderung des Codes zählt als „geändert“.

**Nachprüfen:** endet auf `)`

### B2.5 · `lblVsRegeln.Text`

**Pfad:** `scrEditor › conEdRechts › conVsKarte › lblVsRegeln` → Text

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NichtMessbar; false); Char(10) & "• „nicht messbar“ erlaubt (dann Begründung Pflicht)"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && !IsBlank(LookUp(colP; ID = varAuswahlID).AbwMax); Char(10) & "• höchstens " & Text(LookUp(colP; ID = varAuswahlID).AbwMax) & If(Coalesce(LookUp(colP; ID = varAuswahlID).AbwProzent; false); " %"; "") & " Abweichung zum letzten Rundgang"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NurSteigend; false); Char(10) & "• Zählerstand: darf nicht kleiner werden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).VergleichPunkt; 0) <> 0; Char(10) & "• Vergleich mit „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).VergleichPunkt).Title & "“ (± " & Text(Coalesce(LookUp(colP; ID = varAuswahlID).VergleichTol; 0)) & ")"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).AnleitungID; 0) > 0; Char(10) & "• ⓘ Anleitung „" & Coalesce(LookUp(RG_Anleitungen; ID = LookUp(colP; ID = varAuswahlID).AnleitungID).Title; "?") & "“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).ZugangscodeID; 0) > 0; Char(10) & "• 🔑 Zugangscode „" & Coalesce(LookUp(RG_Zugangscodes; ID = LookUp(colP; ID = varAuswahlID).ZugangscodeID).Title; "?") & "“ (erst nach Antippen sichtbar)"; "")
```

```diff
- … colP; ID = varAuswahlID).AnleitungID).Title; "?") & "“"; "") …
+ … colP; ID = varAuswahlID).AnleitungID).Title; "?") & "“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).ZugangscodeID; 0) > 0; Char(10) & "• 🔑 Zugangscode „" & Coalesce(LookUp(R …
```

**Kurz erklärt:** Vorschau nennt den Zugangscode.

**Nachprüfen:** endet auf `arAuswahlID).ZugangscodeID).Title; "?") & "“ (erst nach Antippen sichtbar)"; "")`

### B2.6 · `tmrArbeit.OnTimerEnd`

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
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQK) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colP; KategorieID = varZielK); RgReihenfolge); 0) + i.Value * 10); Aktiv: true; QuelleID: q.ID; Eingabetyp: {Value: Coalesce(q.Eingabetyp.Value; "IONIO")}; Pflicht: Coalesce(q.Pflicht; false); Auswahlwerte: q.Auswahlwerte; Einheit: q.Einheit; MinWert: q.MinWert; MaxWert: q.MaxWert; Hinweis: q.Hinweis; FotoMoeglich: Coalesce(q.FotoMoeglich; false); Foto: {Value: fnFotoWert(q.Foto.Value; Coalesce(q.FotoMoeglich; false))}; KommentarPflicht: Coalesce(q.KommentarPflicht; false); Grenzmodus: {Value: fnGrenzmodus(q.Grenzmodus.Value)}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: Coalesce(q.HinweisBildID; 0); Abschnitt: Coalesce(q.Abschnitt; ""); Kritisch: Coalesce(q.Kritisch; false); KritischText: Coalesce(q.KritischText; ""); Ansprechpartner: Coalesce(q.Ansprechpartner; ""); Rueckfrage: Coalesce(q.Rueckfrage; false); RueckfrageText: Coalesce(q.RueckfrageText; ""); TextIO: Coalesce(q.TextIO; ""); TextNIO: Coalesce(q.TextNIO; ""); NichtMessbar: Coalesce(q.NichtMessbar; false); AbwMax: q.AbwMax; AbwProzent: Coalesce(q.AbwProzent; false); NurSteigend: Coalesce(q.NurSteigend; false); VergleichPunkt: 0; VergleichTol: q.VergleichTol; AnleitungID: Coalesce(q.AnleitungID; 0); ZugangscodeID: Coalesce(q.ZugangscodeID; 0)}).ID; 0))}
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
    Refresh(RG_Anleitungen);;
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
- … Tol: q.VergleichTol; AnleitungID: Coalesce(q.AnleitungID; 0)}).ID; 0))} …
+ … Tol: q.VergleichTol; AnleitungID: Coalesce(q.AnleitungID; 0); ZugangscodeID: Coalesce(q.ZugangscodeID; 0)}).ID; 0))} …
```

**Kurz erklärt:** Kopie/neue Fassung übernehmen den Code.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

### B2.7 · `txtPHinweis.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › txtPHinweis` → Width

```
292
```

```diff
-340
+292
```

**Kurz erklärt:** Etwas schmaler für den 🔑-Knopf daneben.

**Nachprüfen:** endet auf `292`

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | Builder: Anleitungen › Zugangscodes › „+ Zugangscode“: „Bedienteil Kältemaschine 1“, Code 1234 | Eintrag in der Liste |
| T2 | Prüfpunkt öffnen › 🔑 › Code wählen › Fertig | 🔑 hellblau, Vorschau „• 🔑 Zugangscode …“ |
| T3 | Rundgang DEV: Kategorie öffnen | 🔑 rechts oben in der Karte; Code nirgends sichtbar |
| T4 | 🔑 antippen | Fenster mit „1234“ und Hinweis, Schließen |
| T5 | Kategorie speichern, Protokoll ansehen | Code steht nirgends (auch nicht im JSON `Antworten` der Liste) |
| T6 | Code im Builder inaktiv stellen → App 🔑 | „kein Code hinterlegt“ |
| T7 | Code ohne Wert, nur Hinweis „Code bei der IT“ | Fenster zeigt „—“ und den Hinweis |
| T8 | Code in SharePoint löschen → App 🔑 | „kein Code hinterlegt“; Builder-Auswahl zeigt „… (inaktiv oder gelöscht)“ |
| T9 | Prüfpunkt mit Bild + ⓘ + 🔑 | drei Knöpfe nebeneinander, Frage gekürzt, nichts überlappt |

## Rückweg

Vorher-Fassungen einsetzen; neue Steuerelemente löschen. Liste/Spalte dürfen bleiben.

## Anhang – Vorher-Fassungen

**Rundgang DEV `scrKategorie.OnVisible` vorher**

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
Refresh(RG_Anleitungen);;
Concurrent(
    ClearCollect(colPP; Filter(RG_Pruefpunkte; KategorieID = varKatID && Aktiv = true));
    Set(varErgebnis; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK));
    ClearCollect(colKontakte; Filter(RG_Ansprechpartner; Aktiv = true));
    ClearCollect(colAnlAktivApp; ShowColumns(Filter(RG_Anleitungen; Aktiv = true); ID))
);;
If(!varNurLesen && varLetzteFuer <> varDurchID && CountRows(Filter(colPP; !IsBlank(AbwMax) || Coalesce(NurSteigend; false))) > 0;
    Set(varLetzteFuer; varDurchID);;
    Set(varLetzteRg; varDurch.RundgangID);;
    Set(varLetzteTest; varDurch.TestDatensatz);;
    Set(varLetzteTag; varDurch.TagText);;
    Refresh(RG_Durchfuehrungen);;
    ClearCollect(colLetzteKand; FirstN(Sort(Filter(RG_Durchfuehrungen; RundgangID = varLetzteRg && Status = stAbgeschlossen && TestDatensatz = varLetzteTest); TagText; SortOrder.Descending); 20));;
    Set(varLetzteDurch; First(Sort(Filter(colLetzteKand; DateValue(TagText) < DateValue(varLetzteTag)); TagText; SortOrder.Descending)));;
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
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); BildID: Coalesce(pp.HinweisBildID; 0); Abschnitt: Trim(Coalesce(Text(a.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(a.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(a.KritischOk); false); false); KritischZeit: Coalesce(Text(a.KritischZeit); ""); KritischVon: Coalesce(Text(a.KritischVon); ""); TextIO: Coalesce(Text(a.TextIO); ""); TextNIO: Coalesce(Text(a.TextNIO); ""); NMErlaubt: false; KPflOrig: false; Letzter: Value(a.Letzter); LetzterTag: Coalesce(Text(a.LetzterTag); ""); AbwMax: Blank(); AbwProzent: false; NurSteigend: false; VglID: 0; VglTol: 0; AbwText: Coalesce(Text(a.AbwText); ""); AnlID: If(IsBlank(LookUp(colAnlAktivApp; ID = Coalesce(pp.AnleitungID; 0))); 0; pp.AnleitungID); Inaktiv: false}
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
                     AnlID: If(IsBlank(LookUp(colAnlAktivApp; ID = Coalesce(p.AnleitungID; 0))); 0; p.AnleitungID);
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

**Rundgang DEV `lblKaFrage.Width` vorher**

```
Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0) - If(ThisItem.AnlID > 0; 64; 0)
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
Set(varZaOffen; false);;
Set(varAnID; 0)
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

**Builder `galAkt.Items` vorher**

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

**Builder `lblVsRegeln.Text` vorher**

```
"• " & If(Coalesce(LookUp(colP; ID = varAuswahlID).Pflicht; false); "Pflichtfrage"; "freiwillig") & Char(10) & "• " & fnFotoText(fnFotoWert(LookUp(colP; ID = varAuswahlID).Foto.Value; Coalesce(LookUp(colP; ID = varAuswahlID).FotoMoeglich; false))) & Char(10) & "• Kommentar " & If(Coalesce(LookUp(colP; ID = varAuswahlID).KommentarPflicht; false); "immer Pflicht"; "Pflicht bei Mangel") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL"; Char(10) & "• " & fnGrenzText(LookUp(colP; ID = varAuswahlID).MinWert; LookUp(colP; ID = varAuswahlID).MaxWert; LookUp(colP; ID = varAuswahlID).Einheit) & If(IsBlank(LookUp(colP; ID = varAuswahlID).MinWert) && IsBlank(LookUp(colP; ID = varAuswahlID).MaxWert); ""; ", außerhalb: " & Switch(fnGrenzmodus(LookUp(colP; ID = varAuswahlID).Grenzmodus.Value); "Warnen"; "Hinweis + Begründung"; "Sperren"; "nicht speicherbar"; "Mangel")); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).BedingungPunkt; 0) <> 0; Char(10) & "• nur sichtbar, wenn „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).BedingungPunkt).Title & "“ = " & fnBedText(LookUp(colP; ID = varAuswahlID).BedingungWert); "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).HinweisBildID; 0) > 0; Char(10) & "• mit Beispielbild"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Rueckfrage; false); Char(10) & "• bei n.i.O. Rückfrage „Ist das wirklich so?“"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false); Char(10) & "• bei n.i.O. KRITISCH: rotes Fenster, sofort melden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NichtMessbar; false); Char(10) & "• „nicht messbar“ erlaubt (dann Begründung Pflicht)"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && !IsBlank(LookUp(colP; ID = varAuswahlID).AbwMax); Char(10) & "• höchstens " & Text(LookUp(colP; ID = varAuswahlID).AbwMax) & If(Coalesce(LookUp(colP; ID = varAuswahlID).AbwProzent; false); " %"; "") & " Abweichung zum letzten Rundgang"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).NurSteigend; false); Char(10) & "• Zählerstand: darf nicht kleiner werden"; "") & If(LookUp(colP; ID = varAuswahlID).Eingabetyp.Value = "ZAHL" && Coalesce(LookUp(colP; ID = varAuswahlID).VergleichPunkt; 0) <> 0; Char(10) & "• Vergleich mit „" & LookUp(colP; ID = LookUp(colP; ID = varAuswahlID).VergleichPunkt).Title & "“ (± " & Text(Coalesce(LookUp(colP; ID = varAuswahlID).VergleichTol; 0)) & ")"; "") & If(Coalesce(LookUp(colP; ID = varAuswahlID).AnleitungID; 0) > 0; Char(10) & "• ⓘ Anleitung „" & Coalesce(LookUp(RG_Anleitungen; ID = LookUp(colP; ID = varAuswahlID).AnleitungID).Title; "?") & "“"; "")
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
    Refresh(RG_Anleitungen);;
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

**Builder `txtPHinweis.Width` vorher**

```
340
```

