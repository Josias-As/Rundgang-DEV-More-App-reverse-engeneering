# Paket 8 – Abschnitte und Bereich ausblendbar (Teil Builder)

Stand 02.11.2026. Erzeugt mit `werkzeuge/builder.py` + `werkzeuge/doc_paket8_builder.py` gegen den Builder-Stand nach F1–F4 (Export 02.11. + F1–F4 + deine Optik-Änderungen `lblPlAb/lblPlBis.Size` 10, `conPlTermine` X 980/Y 90).

## Kurzfassung

- **Abschnitt** (neue Textspalte `RG_Pruefpunkte.Abschnitt`): Prüfpunkte einer Kategorie lassen sich gruppieren (z. B. „Kompressor 1“). Im Builder: Feld „Abschnitt“ beim Prüfpunkt, Anzeige „Abschnitt › Frage“ in Gliederung und Vorschau, „Mehrere Fragen“ mit Abschnitt für alle, neuer Prüfpunkt übernimmt den Abschnitt, Kopie und Fassungen übernehmen ihn, Prüfhinweis bei unterbrochenem Abschnitt.
- **Bereich ausblenden** (neue Ja/Nein-Spalte `RG_Bereiche.Ausblenden`): Schalter beim Bereich. Die Rundgang-App zeigt den Namen dann nicht (dieser Teil kommt mit dem Export der Rundgang-App).
- Dazu Optik: 4 Texte, die knapp waren (Prüfung jetzt mit Innenabstand 5 + 5 px).
- Umfang: 2 SharePoint-Spalten, 7 neue Steuerelemente (3 Blöcke), 26 geänderte Properties in 4 Gruppen.
- Geprüft: Generator 0 Fehler (neu: Datenvertrag Kopie/Änderungsliste, Textbreiten mit Innenabstand), Mutation 13/13, Logik 27 Szenarien. **Nicht in Studio getestet.**

## Schritt 0 – SharePoint-Spalten (zuerst)

| Liste | Spalte | Typ | Standard |
|---|---|---|---|
| `RG_Pruefpunkte` | `Abschnitt` | Eine Textzeile | leer |
| `RG_Bereiche` | `Ausblenden` | Ja/Nein | Nein |

Danach im Builder: Daten → `RG_Pruefpunkte` und `RG_Bereiche` → ⋯ → **Aktualisieren**. Die Rundgang-App liest die Spalten erst mit ihrem Teil von Paket 8.

## Schritt 1 – neue Steuerelemente

### In `conPRest` (`scrEditor › conEdMitte › conEdP › conPRest`)

**Wo hin:** `conPRest` selbst markieren → Strg+V.

```yaml
- lblPAbschnitt:
    Control: Label@2.5.1
    Properties:
      Color: =clrTextGrau
      Font: =Font.'Segoe UI'
      Height: =20
      Size: =12
      Text: ="Abschnitt (optional)"
      Width: =176
      X: =352
      Y: =194
- txtPAbschnitt:
    Control: Classic/TextInput@2.3.2
    Properties:
      AccessibleLabel: ="Abschnitt innerhalb der Kategorie"
      BorderColor: =clrRahmen
      Color: =clrText
      Default: =Coalesce(LookUp(colP, ID = varAuswahlID).Abschnitt, "")
      DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)
      Fill: =clrKarte
      FocusedBorderColor: =clrPrimaer
      Font: =Font.'Segoe UI'
      Height: =36
      HintText: ="z. B. Kompressor 1"
      HoverBorderColor: =clrPrimaer
      OnChange: |-
        =If(Trim(Self.Text) <> Trim(Coalesce(LookUp(colP, ID = varAuswahlID).Abschnitt, "")),
            If(varSchreibbar && varAuswahlEbene = 3,
                Refresh(RG_Rundgaenge);
                Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                If(varEntwurfOk,
                    Set(varPatchFehler, false);
                    IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {Abschnitt: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));
                    If(varPatchFehler,
                        Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                        Patch(colP, LookUp(colP, ID = varAuswahlID), LookUp(RG_Pruefpunkte, ID = varAuswahlID));
                        Set(varGespeichertText, "Gespeichert " & Text(Now(), "hh:mm:ss"))
                    )
                )
            )
        )
      Size: =14
      Width: =176
      X: =352
      Y: =214
```

### In `conEdB` (`scrEditor › conEdMitte › conEdB`)

**Wo hin:** `conEdB` selbst markieren → Strg+V.

```yaml
- lblBZeigen:
    Control: Label@2.5.1
    Properties:
      Color: =clrTextGrau
      Font: =Font.'Segoe UI'
      Height: =20
      Size: =12
      Text: ="Name für den Prüfer"
      Width: =528
      X: =0
      Y: =72
- galBZeigen:
    Control: Gallery@2.15.0
    Variant: Vertical
    Properties:
      AccessibleLabel: ="Bereichsname zeigen"
      Height: =36
      Items: |-
        =Table({W: "zeigen", N: "zeigen"}, {W: "aus", N: "ausblenden"})
      ShowScrollbar: =false
      TemplatePadding: =0
      TemplateSize: =36
      Width: =300
      WrapCount: =2
      X: =0
      Y: =92
    Children:
      - btnBZeigen:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false), "aus", "zeigen"), clrPrimaer, clrRahmen)
            BorderThickness: =1
            Color: =If(ThisItem.W = If(Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false), "aus", "zeigen"), Color.White, clrText)
            DisabledBorderColor: =If(ThisItem.W = If(Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false), "aus", "zeigen"), clrPrimaer, clrRahmen)
            DisabledColor: =If(ThisItem.W = If(Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false), "aus", "zeigen"), clrPrimaer, clrTextGrau)
            DisabledFill: =If(ThisItem.W = If(Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false), "aus", "zeigen"), clrPrimaerHell, clrKarte)
            DisplayMode: =If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.Disabled)
            Fill: =If(ThisItem.W = If(Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false), "aus", "zeigen"), clrPrimaer, clrKarte)
            Font: =Font.'Segoe UI'
            Height: =32
            HoverColor: =If(ThisItem.W = If(Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false), "aus", "zeigen"), Color.White, clrText)
            HoverFill: =If(ThisItem.W = If(Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false), "aus", "zeigen"), ColorFade(clrPrimaer, -20%), clrPrimaerHell)
            OnSelect: |-
              =If((ThisItem.W = "aus") <> Coalesce(LookUp(colB, ID = varAuswahlID).Ausblenden, false),
                  If(varSchreibbar && varAuswahlEbene = 1,
                      Refresh(RG_Rundgaenge);
                      Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);
                      If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error));
                      If(varEntwurfOk,
                          Set(varPatchFehler, false);
                          IfError(Patch(RG_Bereiche, LookUp(RG_Bereiche, ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung), {Ausblenden: ThisItem.W = "aus"}), Set(varPatchFehler, true));
                          If(varPatchFehler,
                              Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                              Patch(colB, LookUp(colB, ID = varAuswahlID), LookUp(RG_Bereiche, ID = varAuswahlID));
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
```

### In `conMehrKarte` (`scrEditor › conMehr › conMehrKarte`)

**Wo hin:** `conMehrKarte` selbst markieren → Strg+V.

```yaml
- lblMehrAbschnitt:
    Control: Label@2.5.1
    Properties:
      Color: =clrTextGrau
      Font: =Font.'Segoe UI'
      Height: =20
      Size: =12
      Text: ="Abschnitt (optional)"
      Width: =188
      X: =448
      Y: =416
- txtMehrAbschnitt:
    Control: Classic/TextInput@2.3.2
    Properties:
      AccessibleLabel: ="Abschnitt für alle neuen Fragen"
      BorderColor: =clrRahmen
      Color: =clrText
      Default: =""
      DisplayMode: =DisplayMode.Edit
      Fill: =clrKarte
      FocusedBorderColor: =clrPrimaer
      Font: =Font.'Segoe UI'
      Height: =36
      HintText: ="z. B. Kompressor 1"
      HoverBorderColor: =clrPrimaer
      OnChange: =false
      Size: =14
      Width: =188
      X: =448
      Y: =436
```

## Schritt 2 – Optik und kleine Werte

### 2.1 · `lblGlHilfe.Height`

**Pfad:** `scrEditor › conEdGl › lblGlHilfe` → Height

```
36
```

```diff
-34
+36
```

**Kurz erklärt:** Optik/Wert.

**Nachprüfen:** endet auf `36`

### 2.2 · `lblBInfo.Y`

**Pfad:** `scrEditor › conEdMitte › conEdB › lblBInfo` → Y

```
140
```

```diff
-76
+140
```

**Kurz erklärt:** Optik/Wert.

**Nachprüfen:** endet auf `140`

### 2.3 · `lblBInfo.Height`

**Pfad:** `scrEditor › conEdMitte › conEdB › lblBInfo` → Height

```
180
```

```diff
-120
+180
```

**Kurz erklärt:** Optik/Wert.

**Nachprüfen:** endet auf `180`

### 2.4 · `lblBInfo.Text`

**Pfad:** `scrEditor › conEdMitte › conEdB › lblBInfo` → Text

```
"Enthält " & CountRows(Filter(colK; BereichID = varAuswahlID)) & " Kategorien und " & CountRows(Filter(colP; KategorieID in Filter(colK; BereichID = varAuswahlID).ID)) & " Prüfpunkte." & Char(10) & Char(10) & "Ein Bereich ist eine Überschrift im Rundgang (z. B. „Lagerhalle“). Darin liegen die Kategorien. Neue Kategorie: links „+ Kategorie“." & Char(10) & Char(10) & "„ausblenden“: Der Prüfer sieht nur die Kategorien. Sinnvoll, wenn der Rundgang nur einen Bereich hat."
```

```diff
-"Enthält " & CountRows(Filter(colK; BereichID = varAuswahlID)) & " Kategorien und " & CountRows(Filter(colP; KategorieID in Filter(colK; BereichID = varAuswahlID).ID)) & " Prüfpunkte." & Char(10) & Char(10) & "Ein Bereich ist eine Überschrift im Rundgang ( …
+"Enthält " & CountRows(Filter(colK; BereichID = varAuswahlID)) & " Kategorien und " & CountRows(Filter(colP; KategorieID in Filter(colK; BereichID = varAuswahlID).ID)) & " Prüfpunkte." & Char(10) & Char(10) & "Ein Bereich ist eine Überschrift im Rundgang ( …
```

**Kurz erklärt:** Erklärt „ausblenden“. Rückt nach unten, weil darüber der neue Schalter steht.

**Nachprüfen:** endet auf `er sieht nur die Kategorien. Sinnvoll, wenn der Rundgang nur einen Bereich hat."`

### 2.5 · `lblPKat.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › lblPKat` → Width

```
340
```

```diff
-528
+340
```

**Kurz erklärt:** Optik/Wert.

**Nachprüfen:** endet auf `340`

### 2.6 · `ddPKategorie.Width`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPKategorie` → Width

```
340
```

```diff
-528
+340
```

**Kurz erklärt:** Optik/Wert.

**Nachprüfen:** endet auf `340`

### 2.7 · `lblHolenLeer.Height`

**Pfad:** `scrEditor › conHolen › conHolenKarte › lblHolenLeer` → Height

```
48
```

```diff
-40
+48
```

**Kurz erklärt:** Optik/Wert.

**Nachprüfen:** endet auf `48`

### 2.8 · `lblMehrHilfe.Text`

**Pfad:** `scrEditor › conMehr › conMehrKarte › lblMehrHilfe` → Text

```
"Eine Frage pro Zeile – auch eine Spalte aus Excel einfügen."
```

```diff
-"Eine Frage pro Zeile. Du kannst auch eine Spalte aus Excel hineinkopieren."
+"Eine Frage pro Zeile – auch eine Spalte aus Excel einfügen."
```

**Kurz erklärt:** Kürzer, damit der Text in eine Zeile passt (Höhe 22).

**Nachprüfen:** endet auf `"Eine Frage pro Zeile – auch eine Spalte aus Excel einfügen."`

### 2.9 · `lblPlKopf3.Width`

**Pfad:** `scrPlan › lblPlKopf3` → Width

```
186
```

```diff
-170
+186
```

**Kurz erklärt:** Optik/Wert.

**Nachprüfen:** endet auf `186`

### 2.10 · `lblGlInfo.Text`

**Pfad:** `scrEditor › conEdGl › galGl › lblGlInfo` → Text

```
If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Info)
```

```diff
-If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Ebene = 3; ThisItem.Info; "")
+If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Info)
```

**Kurz erklärt:** Die Info-Spalte zeigt jetzt auch beim Bereich etwas an („ausgeblendet“).

**Nachprüfen:** endet auf `If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Info)`

### 2.11 · `lblHoInfo.Text`

**Pfad:** `scrEditor › conHolen › conHolenKarte › galHolen › lblHoInfo` → Text

```
If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Info)
```

```diff
-If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Ebene = 3; ThisItem.Info; "")
+If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Info)
```

**Kurz erklärt:** Wie lblGlInfo, im Fenster „Holen“.

**Nachprüfen:** endet auf `If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Info)`

## Schritt 3 – Anzeige des Abschnitts

### 3.1 · `galGl.Items`

**Pfad:** `scrEditor › conEdGl › galGl` → Items

```
Sort(
    Ungroup(
        Table(
            {T: ForAll(colB As b; {Ebene: 1; ID: b.ID; BerID: b.ID; KatID: 0; Titel: b.Title; Info: If(Coalesce(b.Ausblenden; false); "ausgeblendet"; ""); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000")})};
            {T: ForAll(colK As k; With({b: LookUp(colB As b1; b1.ID = k.BereichID)}; {Ebene: 2; ID: k.ID; BerID: k.BereichID; KatID: k.ID; Titel: k.Title; Info: Text(CountRows(Filter(colP As p1; p1.KategorieID = k.ID))); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000")}))};
            {T: ForAll(Filter(colP; KategorieID = varCtxK) As p; With({k: LookUp(colK As k1; k1.ID = p.KategorieID)}; With({b: LookUp(colB As b2; b2.ID = k.BereichID)}; {Ebene: 3; ID: p.ID; BerID: k.BereichID; KatID: p.KategorieID; Titel: If(Trim(Coalesce(p.Abschnitt; "")) = ""; p.Title; Trim(p.Abschnitt) & " › " & p.Title); Info: fnTypKurz(p.Eingabetyp.Value); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000") & Text(p.RgReihenfolge; "000000") & Text(p.ID; "000000")})))}
        );
        T
    );
    Schl
)
```

```diff
-            {T: ForAll(colB As b; {Ebene: 1; ID: b.ID; BerID: b.ID; KatID: 0; Titel: b.Title; Info: ""; Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000")})};
+            {T: ForAll(colB As b; {Ebene: 1; ID: b.ID; BerID: b.ID; KatID: 0; Titel: b.Title; Info: If(Coalesce(b.Ausblenden; false); "ausgeblendet"; ""); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000")})};
-            {T: ForAll(Filter(colP; KategorieID = varCtxK) As p; With({k: LookUp(colK As k1; k1.ID = p.KategorieID)}; With({b: LookUp(colB As b2; b2.ID = k.BereichID)}; {Ebene: 3; ID: p.ID; BerID: k.BereichID; KatID: p.KategorieID; Titel: p.Title; Info: fn …
+            {T: ForAll(Filter(colP; KategorieID = varCtxK) As p; With({k: LookUp(colK As k1; k1.ID = p.KategorieID)}; With({b: LookUp(colB As b2; b2.ID = k.BereichID)}; {Ebene: 3; ID: p.ID; BerID: k.BereichID; KatID: p.KategorieID; Titel: If(Trim(Coalesce( …
```

**Kurz erklärt:** Die Gliederung zeigt bei Prüfpunkten mit Abschnitt „Abschnitt › Frage“, bei ausgeblendeten Bereichen „ausgeblendet“.

**Nachprüfen:** endet auf `)`

### 3.2 · `galHolen.Items`

**Pfad:** `scrEditor › conHolen › conHolenKarte › galHolen` → Items

```
Sort(
    Ungroup(
        Table(
            {T: ForAll(colSrcB As b; {Ebene: 1; ID: b.ID; BerID: b.ID; KatID: 0; Titel: b.Title; Info: If(Coalesce(b.Ausblenden; false); "ausgeblendet"; ""); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000")})};
            {T: ForAll(colSrcK As k; With({b: LookUp(colSrcB As b1; b1.ID = k.BereichID)}; {Ebene: 2; ID: k.ID; BerID: k.BereichID; KatID: k.ID; Titel: k.Title; Info: Text(CountRows(Filter(colSrcP As p1; p1.KategorieID = k.ID))); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000")}))};
            {T: ForAll(colSrcP As p; With({k: LookUp(colSrcK As k1; k1.ID = p.KategorieID)}; With({b: LookUp(colSrcB As b2; b2.ID = k.BereichID)}; {Ebene: 3; ID: p.ID; BerID: k.BereichID; KatID: p.KategorieID; Titel: If(Trim(Coalesce(p.Abschnitt; "")) = ""; p.Title; Trim(p.Abschnitt) & " › " & p.Title); Info: fnTypKurz(p.Eingabetyp.Value); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000") & Text(p.RgReihenfolge; "000000") & Text(p.ID; "000000")})))}
        );
        T
    );
    Schl
)
```

```diff
-            {T: ForAll(colSrcB As b; {Ebene: 1; ID: b.ID; BerID: b.ID; KatID: 0; Titel: b.Title; Info: ""; Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000")})};
+            {T: ForAll(colSrcB As b; {Ebene: 1; ID: b.ID; BerID: b.ID; KatID: 0; Titel: b.Title; Info: If(Coalesce(b.Ausblenden; false); "ausgeblendet"; ""); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000")})};
-            {T: ForAll(colSrcP As p; With({k: LookUp(colSrcK As k1; k1.ID = p.KategorieID)}; With({b: LookUp(colSrcB As b2; b2.ID = k.BereichID)}; {Ebene: 3; ID: p.ID; BerID: k.BereichID; KatID: p.KategorieID; Titel: p.Title; Info: fnTypKurz(p.Eingabetyp.V …
+            {T: ForAll(colSrcP As p; With({k: LookUp(colSrcK As k1; k1.ID = p.KategorieID)}; With({b: LookUp(colSrcB As b2; b2.ID = k.BereichID)}; {Ebene: 3; ID: p.ID; BerID: k.BereichID; KatID: p.KategorieID; Titel: If(Trim(Coalesce(p.Abschnitt; "")) = "" …
```

**Kurz erklärt:** Wie die Gliederung, im Fenster „Holen“.

**Nachprüfen:** endet auf `)`

### 3.3 · `lblVsListe.Text`

**Pfad:** `scrEditor › conEdRechts › lblVsListe` → Text

```
If(varAuswahlEbene = 2; Concat(Sort(Filter(colP; KategorieID = varAuswahlID); RgReihenfolge * 1000000 + ID) As p; "• " & If(Trim(Coalesce(p.Abschnitt; "")) = ""; ""; Trim(p.Abschnitt) & " › ") & p.Title & "  (" & fnTypName(p.Eingabetyp.Value) & If(Coalesce(p.Pflicht; false); ", Pflicht"; "") & If(Coalesce(p.BedingungPunkt; 0) <> 0; ", bedingt"; "") & ")"; Char(10)); varAuswahlEbene = 1; Concat(Sort(Filter(colK; BereichID = varAuswahlID); RgReihenfolge * 1000000 + ID) As k; "• " & k.Title & "  (" & CountRows(Filter(colP; KategorieID = k.ID)) & " Prüfpunkte)"; Char(10)); "Links etwas antippen.")
```

```diff
-If(varAuswahlEbene = 2; Concat(Sort(Filter(colP; KategorieID = varAuswahlID); RgReihenfolge * 1000000 + ID) As p; "• " & p.Title & "  (" & fnTypName(p.Eingabetyp.Value) & If(Coalesce(p.Pflicht; false); ", Pflicht"; "") & If(Coalesce(p.BedingungPunkt; 0) <> …
+If(varAuswahlEbene = 2; Concat(Sort(Filter(colP; KategorieID = varAuswahlID); RgReihenfolge * 1000000 + ID) As p; "• " & If(Trim(Coalesce(p.Abschnitt; "")) = ""; ""; Trim(p.Abschnitt) & " › ") & p.Title & "  (" & fnTypName(p.Eingabetyp.Value) & If(Coalesce …
```

**Kurz erklärt:** Die Vorschau einer Kategorie zeigt den Abschnitt vor der Frage.

**Nachprüfen:** endet auf `colP; KategorieID = k.ID)) & " Prüfpunkte)"; Char(10)); "Links etwas antippen.")`

### 3.4 · `galAkt.Items`

**Pfad:** `scrEditor › conAkt › conAktKarte › galAkt` → Items

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

```diff
-        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) …
+        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) …
```

**Kurz erklärt:** Eine Änderung am Abschnitt zählt beim Aktivieren als „geändert“.

**Nachprüfen:** endet auf `)`

### 3.5 · `btnMehrAnlegen.OnSelect`

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

```diff
-                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; QuelleID: 0; Eingabetyp:  …
+                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; QuelleID: 0; Eingabetyp:  …
+            Reset(txtMehrAbschnitt);;
```

**Kurz erklärt:** „Mehrere Fragen“ setzt den Abschnitt aus dem neuen Feld für alle neuen Fragen.

**Nachprüfen:** endet auf `)`

## Schritt 4 – Auswahl wechseln (setzt das Abschnittsfeld zurück)

### 4.1 · `btnGlZeile.OnSelect`

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

```diff
-        Reset(ddPBedW);
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt);
-        Reset(ddPBedW);
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt);
-        Reset(ddPBedW)
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt)
```

**Kurz erklärt:** Neu ist `Reset(txtPAbschnitt)`. So zeigt das Abschnittsfeld nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 4.2 · `btnGlNeuB.OnSelect`

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
            SetFocus(txtBName)
        )
    )
)
```

```diff
-        Set(varNeuID; IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: "Neuer Bereich"; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(colB; RgReihenfolge); 0) + 10; Hinweis: ""; Aktiv: false; QuelleID: 0}).ID; 0));;
+        Set(varNeuID; IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: "Neuer Bereich"; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(colB; RgReihenfolge); 0) + 10; Hinweis: ""; Aktiv: false; QuelleID: 0; Ausblenden: false} …
+            Reset(txtPAbschnitt);;
```

**Kurz erklärt:** Neu ist `Reset(txtPAbschnitt)`. So zeigt das Abschnittsfeld nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 4.3 · `btnGlNeuK.OnSelect`

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
            SetFocus(txtKName)
        )
    )
)
```

```diff
+            Reset(txtPAbschnitt);;
```

**Kurz erklärt:** Neu ist `Reset(txtPAbschnitt)`. So zeigt das Abschnittsfeld nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 4.4 · `btnGlNeuP.OnSelect`

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

```diff
-        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0) + 10; Ak …
+        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0) + 10; Ak …
+            Reset(txtPAbschnitt);;
```

**Kurz erklärt:** Ein neuer Prüfpunkt übernimmt den Abschnitt des gerade gewählten Prüfpunkts (gleiche Kategorie).

**Nachprüfen:** endet auf `)`

### 4.5 · `btnPrZeile.OnSelect`

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

```diff
-        Reset(ddPBedW);
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt);
-        Reset(ddPBedW);
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt);
-        Reset(ddPBedW)
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt)
```

**Kurz erklärt:** Neu ist `Reset(txtPAbschnitt)`. So zeigt das Abschnittsfeld nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 4.6 · `ddKBereich.OnChange`

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
        Reset(txtPAbschnitt)
    ))
)
```

```diff
-        Reset(ddPBedW)
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt)
```

**Kurz erklärt:** Neu ist `Reset(txtPAbschnitt)`. So zeigt das Abschnittsfeld nach jedem Wechsel den richtigen Wert.

**Nachprüfen:** endet auf `)`

### 4.7 · `ddPKategorie.OnChange`

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
        Reset(txtPAbschnitt)
    ))
)
```

```diff
-        Reset(ddPBedW)
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt)
```

**Kurz erklärt:** Neu ist `Reset(txtPAbschnitt)`. So zeigt das Abschnittsfeld nach jedem Wechsel den richtigen Wert.

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

```diff
-        Reset(ddPBedW);
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt);
-        Reset(ddPBedW);
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt);
-        Reset(ddPBedW)
+        Reset(ddPBedW);;
+        Reset(txtPAbschnitt)
```

**Kurz erklärt:** Nur das Zurücksetzen des Abschnittsfelds nach dem Entfernen.

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
+            {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Abschnitt; "")) <> "" && With({v: First(Sort(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 1000000 + q.ID < p.RgReihenfolge * 1000000 + p.ID); RgReihenfolge * 1000000 + ID; Sor …
```

**Kurz erklärt:** Neuer Hinweis, wenn die Fragen eines Abschnitts nicht zusammenstehen (sonst stünde die Überschrift zweimal da).

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

```diff
-                     Neu: IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: Left(q.Title & varKopieZusatz; 255); RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(colB; RgReihenfolge); 0) + i …
+                     Neu: IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: Left(q.Title & varKopieZusatz; 255); RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(colB; RgReihenfolge); 0) + i …
-                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpt …
+                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpt …
-            Reset(ddPBedW);
+            Reset(ddPBedW);;
+            Reset(txtPAbschnitt);
-            Reset(ddPBedW)
+            Reset(ddPBedW);;
+            Reset(txtPAbschnitt)
-        With({n: First(colMapB).Neu}; If(n > 0; Set(varAuswahlEbene; 1);; Set(varAuswahlID; n);; Set(varCtxB; n);; Set(varCtxK; 0);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(t …
+        With({n: First(colMapB).Neu}; If(n > 0; Set(varAuswahlEbene; 1);; Set(varAuswahlID; n);; Set(varCtxB; n);; Set(varCtxK; 0);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(t …
-        With({n: First(colMapK).Neu}; If(n > 0; Set(varAuswahlEbene; 2);; Set(varAuswahlID; n);; Set(varCtxB; varZielB);; Set(varCtxK; n);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);;  …
-        With({n: First(colMapP).Neu}; If(n > 0; Set(varAuswahlEbene; 3);; Set(varAuswahlID; n);; Set(varCtxB; LookUp(colK; ID = varZielK).BereichID);; Set(varCtxK; varZielK);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Rese …
+        With({n: First(colMapK).Neu}; If(n > 0; Set(varAuswahlEbene; 2);; Set(varAuswahlID; n);; Set(varCtxB; varZielB);; Set(varCtxK; n);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);;  …
+        With({n: First(colMapP).Neu}; If(n > 0; Set(varAuswahlEbene; 3);; Set(varAuswahlID; n);; Set(varCtxB; LookUp(colK; ID = varZielK).BereichID);; Set(varCtxK; varZielK);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Rese …
```

**Kurz erklärt:** Kopie, neue Fassung und „Holen“ übernehmen Abschnitt und „Bereich ausblenden“. Dazu das Zurücksetzen des Abschnittsfelds.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

## Test (wenn du testest)

1. Prüfpunkt wählen, Abschnitt „Kompressor 1“ eintragen, Tab → Gliederung zeigt „Kompressor 1 › Frage“.
2. „+ Prüfpunkt“ → neuer Punkt hat denselben Abschnitt.
3. Zwei Punkte mit Abschnitt A, dazwischen einer mit B → Prüfung: Hinweis „Abschnitt … ist unterbrochen“.
4. Bereich wählen → „ausblenden“ → Gliederung zeigt beim Bereich „ausgeblendet“.
5. „Mehrere Fragen“ mit Abschnitt „Kältemaschine 1“ → alle neuen Fragen haben ihn.
6. Neue Fassung anlegen → Abschnitte und „ausgeblendet“ sind in der neuen Fassung noch da.

## Rückweg

Die Vorher-Fassungen stehen im Anhang. Die neuen Steuerelemente können gelöscht werden, die Spalten können bleiben. Achtung: Wenn `txtPAbschnitt` gelöscht wird, werden alle Formeln mit `Reset(txtPAbschnitt)` rot. Dann erst die Vorher-Fassungen einsetzen.

## Anhang – Vorher-Fassungen

### `lblGlHilfe.Height` (vorher)

```
34
```

### `lblBInfo.Y` (vorher)

```
76
```

### `lblBInfo.Height` (vorher)

```
120
```

### `lblBInfo.Text` (vorher)

```
"Enthält " & CountRows(Filter(colK; BereichID = varAuswahlID)) & " Kategorien und " & CountRows(Filter(colP; KategorieID in Filter(colK; BereichID = varAuswahlID).ID)) & " Prüfpunkte." & Char(10) & Char(10) & "Ein Bereich ist eine Überschrift im Rundgang (z. B. „Lagerhalle“). Darin liegen die Kategorien. Neue Kategorie: links „+ Kategorie“."
```

### `lblPKat.Width` (vorher)

```
528
```

### `ddPKategorie.Width` (vorher)

```
528
```

### `lblHolenLeer.Height` (vorher)

```
40
```

### `lblMehrHilfe.Text` (vorher)

```
"Eine Frage pro Zeile. Du kannst auch eine Spalte aus Excel hineinkopieren."
```

### `lblPlKopf3.Width` (vorher)

```
170
```

### `lblGlInfo.Text` (vorher)

```
If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Ebene = 3; ThisItem.Info; "")
```

### `lblHoInfo.Text` (vorher)

```
If(ThisItem.Ebene = 2; ThisItem.Info & " Pkt."; ThisItem.Ebene = 3; ThisItem.Info; "")
```

### `galGl.Items` (vorher)

```
Sort(
    Ungroup(
        Table(
            {T: ForAll(colB As b; {Ebene: 1; ID: b.ID; BerID: b.ID; KatID: 0; Titel: b.Title; Info: ""; Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000")})};
            {T: ForAll(colK As k; With({b: LookUp(colB As b1; b1.ID = k.BereichID)}; {Ebene: 2; ID: k.ID; BerID: k.BereichID; KatID: k.ID; Titel: k.Title; Info: Text(CountRows(Filter(colP As p1; p1.KategorieID = k.ID))); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000")}))};
            {T: ForAll(Filter(colP; KategorieID = varCtxK) As p; With({k: LookUp(colK As k1; k1.ID = p.KategorieID)}; With({b: LookUp(colB As b2; b2.ID = k.BereichID)}; {Ebene: 3; ID: p.ID; BerID: k.BereichID; KatID: p.KategorieID; Titel: p.Title; Info: fnTypKurz(p.Eingabetyp.Value); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000") & Text(p.RgReihenfolge; "000000") & Text(p.ID; "000000")})))}
        );
        T
    );
    Schl
)
```

### `galHolen.Items` (vorher)

```
Sort(
    Ungroup(
        Table(
            {T: ForAll(colSrcB As b; {Ebene: 1; ID: b.ID; BerID: b.ID; KatID: 0; Titel: b.Title; Info: ""; Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000")})};
            {T: ForAll(colSrcK As k; With({b: LookUp(colSrcB As b1; b1.ID = k.BereichID)}; {Ebene: 2; ID: k.ID; BerID: k.BereichID; KatID: k.ID; Titel: k.Title; Info: Text(CountRows(Filter(colSrcP As p1; p1.KategorieID = k.ID))); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000")}))};
            {T: ForAll(colSrcP As p; With({k: LookUp(colSrcK As k1; k1.ID = p.KategorieID)}; With({b: LookUp(colSrcB As b2; b2.ID = k.BereichID)}; {Ebene: 3; ID: p.ID; BerID: k.BereichID; KatID: p.KategorieID; Titel: p.Title; Info: fnTypKurz(p.Eingabetyp.Value); Schl: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000") & Text(p.RgReihenfolge; "000000") & Text(p.ID; "000000")})))}
        );
        T
    );
    Schl
)
```

### `lblVsListe.Text` (vorher)

```
If(varAuswahlEbene = 2; Concat(Sort(Filter(colP; KategorieID = varAuswahlID); RgReihenfolge * 1000000 + ID) As p; "• " & p.Title & "  (" & fnTypName(p.Eingabetyp.Value) & If(Coalesce(p.Pflicht; false); ", Pflicht"; "") & If(Coalesce(p.BedingungPunkt; 0) <> 0; ", bedingt"; "") & ")"; Char(10)); varAuswahlEbene = 1; Concat(Sort(Filter(colK; BereichID = varAuswahlID); RgReihenfolge * 1000000 + ID) As k; "• " & k.Title & "  (" & CountRows(Filter(colP; KategorieID = k.ID)) & " Prüfpunkte)"; Char(10)); "Links etwas antippen.")
```

### `galAkt.Items` (vorher)

```
Ungroup(
    Table(
        {T: ForAll(Filter(colP As p; IsBlank(LookUp(colAltP As a; a.ID = p.QuelleID))) As p; {Art: "neu"; Text: p.Title})};
        {T: ForAll(Filter(colP As p; With({a: LookUp(colAltP As a0; a0.ID = p.QuelleID)}; !IsBlank(a) && (p.Title <> a.Title || Coalesce(p.Eingabetyp.Value; "") <> Coalesce(a.Eingabetyp.Value; "") || Coalesce(p.Pflicht; false) <> Coalesce(a.Pflicht; false) || Coalesce(p.Auswahlwerte; "") <> Coalesce(a.Auswahlwerte; "") || Coalesce(p.Einheit; "") <> Coalesce(a.Einheit; "") || Coalesce(p.MinWert; -999999) <> Coalesce(a.MinWert; -999999) || Coalesce(p.MaxWert; -999999) <> Coalesce(a.MaxWert; -999999) || Coalesce(p.Hinweis; "") <> Coalesce(a.Hinweis; "") || fnFotoWert(p.Foto.Value; Coalesce(p.FotoMoeglich; false)) <> fnFotoWert(a.Foto.Value; Coalesce(a.FotoMoeglich; false)) || Coalesce(p.KommentarPflicht; false) <> Coalesce(a.KommentarPflicht; false) || fnGrenzmodus(p.Grenzmodus.Value) <> fnGrenzmodus(a.Grenzmodus.Value) || Coalesce(p.BedingungWert; "") <> Coalesce(a.BedingungWert; "") || Coalesce(LookUp(colP As b0; b0.ID = p.BedingungPunkt).QuelleID; 0) <> Coalesce(a.BedingungPunkt; 0) || Coalesce(p.HinweisBildID; 0) <> Coalesce(a.HinweisBildID; 0) || Coalesce(LookUp(colK As k0; k0.ID = p.KategorieID).QuelleID; 0) <> a.KategorieID))) As p; {Art: "geändert"; Text: p.Title})};
        {T: ForAll(Filter(colAltP As a; IsBlank(LookUp(colP As p; p.QuelleID = a.ID))) As a; {Art: "entfernt"; Text: a.Title})}
    );
    T
)
```

### `btnMehrAnlegen.OnSelect` (vorher)

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
                    {Neu: IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Index(colMehr; i.Value).F; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: basis + i.Value * 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: varMehrTyp}; Pflicht: varMehrPflicht; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0}).ID; 0)}
                )
            )
        );;
        ClearCollect(colP; Filter(RG_Pruefpunkte; RundgangID = varRgID && Fassung = varFassung));;
        If(CountRows(Filter(colMehrErg; Neu = 0)) > 0;
            Notify(CountRows(Filter(colMehrErg; Neu = 0)) & " Fragen konnten nicht angelegt werden. Bitte die Gliederung prüfen."; NotificationType.Error);
            Notify(CountRows(colMehrErg) & " Prüfpunkte angelegt."; NotificationType.Success);;
            Reset(txtMehr);;
            Set(varMehrereOffen; false)
        );;
        Set(varIsLoading; false)
    )
)
```

### `btnGlZeile.OnSelect` (vorher)

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
        Reset(ddPBedW);
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
        Reset(ddPBedW);
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
        Reset(ddPBedW)
    )
)
```

### `btnGlNeuB.OnSelect` (vorher)

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
        Set(varNeuID; IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: "Neuer Bereich"; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(colB; RgReihenfolge); 0) + 10; Hinweis: ""; Aktiv: false; QuelleID: 0}).ID; 0));;
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
            SetFocus(txtBName)
        )
    )
)
```

### `btnGlNeuK.OnSelect` (vorher)

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
            SetFocus(txtKName)
        )
    )
)
```

### `btnGlNeuP.OnSelect` (vorher)

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
        Set(varNeuID; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: "Neue Frage"; KategorieID: varCtxK; RundgangID: varRgID; Fassung: varFassung; RgReihenfolge: Coalesce(Max(Filter(colP; KategorieID = varCtxK); RgReihenfolge); 0) + 10; Aktiv: true; QuelleID: 0; Eingabetyp: {Value: "IONIO"}; Pflicht: true; Auswahlwerte: ""; Einheit: ""; Hinweis: ""; FotoMoeglich: false; Foto: {Value: "Aus"}; KommentarPflicht: false; Grenzmodus: {Value: "Mangel"}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: 0}).ID; 0));;
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
            SetFocus(txtPFrage)
        )
    )
)
```

### `btnPrZeile.OnSelect` (vorher)

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
        Reset(ddPBedW);
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
        Reset(ddPBedW);
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
        Reset(ddPBedW)
    )
)
```

### `ddKBereich.OnChange` (vorher)

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
        Reset(ddPBedW)
    ))
)
```

### `ddPKategorie.OnChange` (vorher)

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
        Reset(ddPBedW)
    ))
)
```

### `btnEdEntf.OnSelect` (vorher)

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
        Reset(ddPBedW);
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
        Reset(ddPBedW);
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
        Reset(ddPBedW)
    );;
    Set(varIsLoading; false)
    )
        )
    ))
```

### `galPr.Items` (vorher)

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
            {T: ForAll(Filter(colP As p; p.Title = "Neue Frage") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Eine Frage heißt noch „Neue Frage“."})};
            {T: ForAll(Filter(colK As k; CountRows(Filter(colP As p; p.KategorieID = k.ID)) > 30) As k; {Art: "Hinweis"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat über 30 Prüfpunkte (lange Seite für den Prüfer)."})};
            {T: Filter(Table({Art: "Hinweis"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Kein aktiver Plan: Der Rundgang erscheint nie auf der Startseite. → In der Übersicht „Plan“ tippen."}); !varIstVorlage && IsEmpty(Filter(colPlanR; Coalesce(Aktiv; false))))}
        );
        T
    );
    If(Art = "Fehler"; 0; 1)
)
```

### `tmrArbeit.OnTimerEnd` (vorher)

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
                     Neu: IfError(Patch(RG_Bereiche; Defaults(RG_Bereiche); {Title: Left(q.Title & varKopieZusatz; 255); RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(colB; RgReihenfolge); 0) + i.Value * 10); Hinweis: q.Hinweis; Aktiv: varZielBAktiv; QuelleID: q.ID}).ID; 0)}
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
                         Neu: If(ziel = 0; 0; IfError(Patch(RG_Pruefpunkte; Defaults(RG_Pruefpunkte); {Title: Left(q.Title & If(IsEmpty(colQK); varKopieZusatz; ""); 255); KategorieID: ziel; RundgangID: varZielR; Fassung: varZielF; RgReihenfolge: If(!IsEmpty(colQK) || varKopieBehalteR; q.RgReihenfolge; Coalesce(Max(Filter(colP; KategorieID = varZielK); RgReihenfolge); 0) + i.Value * 10); Aktiv: true; QuelleID: q.ID; Eingabetyp: {Value: Coalesce(q.Eingabetyp.Value; "IONIO")}; Pflicht: Coalesce(q.Pflicht; false); Auswahlwerte: q.Auswahlwerte; Einheit: q.Einheit; MinWert: q.MinWert; MaxWert: q.MaxWert; Hinweis: q.Hinweis; FotoMoeglich: Coalesce(q.FotoMoeglich; false); Foto: {Value: fnFotoWert(q.Foto.Value; Coalesce(q.FotoMoeglich; false))}; KommentarPflicht: Coalesce(q.KommentarPflicht; false); Grenzmodus: {Value: fnGrenzmodus(q.Grenzmodus.Value)}; BedingungPunkt: 0; BedingungWert: ""; HinweisBildID: Coalesce(q.HinweisBildID; 0)}).ID; 0))}
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
            Reset(ddPBedW);
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
            Reset(ddPBedW)
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
        With({n: First(colMapB).Neu}; If(n > 0; Set(varAuswahlEbene; 1);; Set(varAuswahlID; n);; Set(varCtxB; n);; Set(varCtxK; 0);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW)));
        !IsEmpty(colQK);
        With({n: First(colMapK).Neu}; If(n > 0; Set(varAuswahlEbene; 2);; Set(varAuswahlID; n);; Set(varCtxB; varZielB);; Set(varCtxK; n);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW)));
        With({n: First(colMapP).Neu}; If(n > 0; Set(varAuswahlEbene; 3);; Set(varAuswahlID; n);; Set(varCtxB; LookUp(colK; ID = varZielK).BereichID);; Set(varCtxK; varZielK);; Set(varFrage; "");; Reset(txtBName);; Reset(txtKName);; Reset(ddKBereich);; Reset(txtPFrage);; Reset(txtPEinheit);; Reset(txtPMin);; Reset(txtPMax);; Reset(txtPWerte);; Reset(txtPHinweis);; Reset(ddPKategorie);; Reset(ddPBedA);; Reset(ddPBedW)))
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

