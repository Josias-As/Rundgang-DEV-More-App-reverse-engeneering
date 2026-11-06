# Paket 23 – Banner „Nicht abgeschlossen“, Testkennung, Ansprechpartner, Entfernen-Warnung

Stand 06.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket23), `werkzeuge/builder.py` und `werkzeuge/doc_paket23.py`. Voraussetzung: alle Pakete bis 13 in beiden Apps (Stand Einsetz-Chat 06.11.).

## Kurzfassung

- **A8 (App):** Der rote Hinweis „Nicht abgeschlossen“ auf der Startseite zeigt keine Testläufe mehr. Gibt es mehrere offene Läufe, blättert **„Weiter ›“** durch alle, „Öffnen“ öffnet den angezeigten.
- **A11 (App + Builder):** Test ist ein Rundgang jetzt über die neue Spalte **`Testrundgang`**, nicht mehr über den Namen „ZZ Test“. Pflegen im Builder unter **Plan → „○ Testrundgang“**; die Übersicht zeigt „· Testrundgang“. Gilt für **neue** Läufe; bestehende Läufe behalten ihr `TestDatensatz`.
- **A7 (Builder):** Im Fenster „Bei n.i.O.“ erscheinen eingetragene, aber inaktive Ansprechpartner („inaktiv – entfernen“) und lassen sich herausnehmen. Unter „Ansprechpartner“ steht je Eintrag, bei wie vielen kritischen Prüfpunkten in wie vielen Rundgängen er eingetragen ist; inaktiv + verwendet ist rot.
- **A6 (Builder):** Beim Entfernen eines Prüfpunkts warnt der Text, wenn andere Fragen über Bedingung oder Vergleich davon abhängen.
- **A1:** Der Generator schreibt in der deutschen Formelleiste jetzt `.Miniaturansicht.` statt `.Thumbnail.` (Paket 13 und alle späteren). In YAML-Blöcken bleibt der interne Name `Thumbnail` (wie im Export).
- Umfang: App 6 Properties + 1 Knopf + 1 Spalte; Builder 8 Properties + btnPlTest, lblKoNutzung. Generatoren 0 Fehler, Mutation 12/12 und 13/13, Textbreiten geprüft. **Nicht in Studio getestet, nicht unabhängig geprüft.**

## Teil A – Rundgang DEV

### A1 – SharePoint (zuerst)

- `RG_Rundgaenge`: neue Spalte **`Testrundgang`** (Ja/Nein, Standard **Nein**).
- Danach bei den Test-Rundgängen auf **Ja** setzen: „ZZ Test Infrastrukturrundgang“ (ID 3), „ZZ Test Funktionsrundgang“ (ID 4) und alle weiteren ZZ-Test-Rundgänge (im Builder unter „Plan“ → „○ Testrundgang“, oder in der Liste). **Ohne diesen Schritt zählen neue Läufe dieser Rundgänge als echt.**
- Rundgang DEV: Daten → `RG_Rundgaenge` → ⋯ → Aktualisieren.

### A2 – Properties

### A2.1 · `btnStartTagLaden.OnSelect`

**Pfad:** `scrStart › btnStartTagLaden` → OnSelect

```
Set(varIsLoading; true);;
Concurrent(Refresh(RG_Durchfuehrungen); Refresh(RG_KategorieErgebnisse));;
Concurrent(
    ClearCollect(colDurchTag; Filter(RG_Durchfuehrungen; TagText = varTagText));
    ClearCollect(colErgTag; ShowColumns(Filter(RG_KategorieErgebnisse; TagText = varTagText); DurchfuehrungID; KategorieID));
    ClearCollect(colOffenAlt; ShowColumns(Filter(RG_Durchfuehrungen; Status = stInArbeit || Status = stAbschluss); ID; Title; RundgangID; RundgangName; TagText; TestDatensatz))
);;
Set(varIsLoading; false)
```

```diff
-    ClearCollect(colOffenAlt; ShowColumns(Filter(RG_Durchfuehrungen; Status = stInArbeit || Status = stAbschluss); ID; Title; RundgangID; RundgangName; TagText))
+    ClearCollect(colOffenAlt; ShowColumns(Filter(RG_Durchfuehrungen; Status = stInArbeit || Status = stAbschluss); ID; Title; RundgangID; RundgangName; TagText; TestDatensatz))
```

**Kurz erklärt:** Liest zu den offenen Läufen auch `TestDatensatz` mit (nur eine Spalte mehr in `ShowColumns`).

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

### A2.2 · `conStartOffen.Visible`

**Pfad:** `scrStart › conStartOffen` → Visible

```
CountRows(Filter(colOffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false))) > 0
```

```diff
-CountRows(Filter(colOffenAlt; DateValue(TagText) < varHeute)) > 0
+CountRows(Filter(colOffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false))) > 0
```

**Kurz erklärt:** Der Hinweis erscheint nur für echte offene Läufe vor heute. Testläufe zählen nicht mehr.

**Nachprüfen:** endet auf `OffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false))) > 0`

### A2.3 · `lblStartOffen.Text`

**Pfad:** `scrStart › conStartOffen › lblStartOffen` → Text

```
With({l: Sort(Filter(colOffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false)); TagText)};
    If(CountRows(l) = 0; "";
        With({i: Min(Max(Coalesce(varOffenNr; 1); 1); CountRows(l))};
            With({o: Index(l; i)};
                "⚠  Nicht abgeschlossen: " & o.RundgangName & " vom " & Text(DateValue(o.TagText); "dd.mm.yyyy") & If(CountRows(l) > 1; "  (" & i & "/" & CountRows(l) & ")"; "")
            )
        )
    )
)
```

```diff
-With({o: First(Sort(Filter(colOffenAlt; DateValue(TagText) < varHeute); TagText)); n: CountRows(Filter(colOffenAlt; DateValue(TagText) < varHeute))};
-    "⚠  Nicht abgeschlossen: " & o.RundgangName & " vom " & Text(DateValue(o.TagText); "dd.mm.yyyy") & If(n > 1; " (und " & (n - 1) & " weitere)"; ""))
+With({l: Sort(Filter(colOffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false)); TagText)};
+    If(CountRows(l) = 0; "";
+        With({i: Min(Max(Coalesce(varOffenNr; 1); 1); CountRows(l))};
+            With({o: Index(l; i)};
+                "⚠  Nicht abgeschlossen: " & o.RundgangName & " vom " & Text(DateValue(o.TagText); "dd.mm.yyyy") & If(CountRows(l) > 1; "  (" & i & "/" & CountRows(l) & ")"; "")
+            )
+        )
+    )
+)
```

**Kurz erklärt:** Zeigt den gewählten offenen Lauf. Bei mehreren steht „(2/5)“ dahinter.

**Nachprüfen:** endet auf `)`

### A2.4 · `lblStartOffen.Width`

**Pfad:** `scrStart › conStartOffen › lblStartOffen` → Width

```
If(CountRows(Filter(colOffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false))) > 1; Parent.Width - 380; Parent.Width - 260)
```

```diff
-Parent.Width - 260
+If(CountRows(Filter(colOffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false))) > 1; Parent.Width - 380; Parent.Width - 260)
```

**Kurz erklärt:** Platz für den neuen Knopf „Weiter ›“, wenn es mehrere gibt.

**Nachprüfen:** endet auf `& !Coalesce(TestDatensatz; false))) > 1; Parent.Width - 380; Parent.Width - 260)`

### A2.5 · `btnStartOffen.OnSelect`

**Pfad:** `scrStart › conStartOffen › btnStartOffen` → OnSelect

```
If(!varIsLoading;
    With({l: Sort(Filter(colOffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false)); TagText)};
        If(CountRows(l) > 0;
            With({o: Index(l; Min(Max(Coalesce(varOffenNr; 1); 1); CountRows(l)))};
                Set(varTag; DateValue(o.TagText));;
                Set(varTagText; o.TagText);;
                Set(varRgID; o.RundgangID);;
                Set(varSchluessel; o.Title);;
                Set(varDurchID; o.ID);;
                Navigate(scrRundgang; ScreenTransition.None)
            )
        )
    )
)
```

```diff
-    With({o: First(Sort(Filter(colOffenAlt; DateValue(TagText) < varHeute); TagText))};
-        If(!IsBlank(o);
-            Set(varTag; DateValue(o.TagText));;
-            Set(varTagText; o.TagText);;
-            Set(varRgID; o.RundgangID);;
-            Set(varSchluessel; o.Title);;
-            Set(varDurchID; o.ID);;
-            Navigate(scrRundgang; ScreenTransition.None)
+    With({l: Sort(Filter(colOffenAlt; DateValue(TagText) < varHeute && !Coalesce(TestDatensatz; false)); TagText)};
+        If(CountRows(l) > 0;
+            With({o: Index(l; Min(Max(Coalesce(varOffenNr; 1); 1); CountRows(l)))};
+                Set(varTag; DateValue(o.TagText));;
+                Set(varTagText; o.TagText);;
+                Set(varRgID; o.RundgangID);;
+                Set(varSchluessel; o.Title);;
+                Set(varDurchID; o.ID);;
+                Navigate(scrRundgang; ScreenTransition.None)
+            )
```

**Kurz erklärt:** „Öffnen“ öffnet den gerade angezeigten Lauf (nicht mehr immer den ältesten).

**Nachprüfen:** endet auf `)`

### A2.6 · `btnRgAktion.OnSelect`

**Pfad:** `scrStart › galStartRundgaenge › conRgKarte › btnRgAktion` → OnSelect

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

```diff
- … eferName: User().FullName; StartZeit: Now(); TestDatensatz: StartsWith(ThisItem.Title; "ZZ Test")}); …
+ … eferName: User().FullName; StartZeit: Now(); TestDatensatz: Coalesce(ThisItem.Testrundgang; false)}); …
```

**Kurz erklärt:** **A11:** Ein Lauf ist Test, wenn der Rundgang die neue Spalte `Testrundgang` = Ja hat. Der Name („ZZ Test“) spielt keine Rolle mehr. Sonst unverändert.

**Nachprüfen:** endet auf `)`

### A3 – neuer Knopf „Weiter ›“

**Wo hin:** in der Strukturansicht **`conStartOffen`** markieren → Strg+V.

```yaml
- btnStartOffenWeiter:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrFehler
      BorderThickness: =1
      Color: =clrFehler
      DisabledBorderColor: =clrGesperrtHell
      DisabledColor: =clrGesperrt
      DisabledFill: =clrGesperrtHell
      DisplayMode: =If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)
      Fill: =Color.White
      Font: =Font.'Segoe UI'
      Height: =56
      HoverColor: =clrFehler
      HoverFill: =clrFehlerHell
      OnSelect: |-
        =With({n: CountRows(Filter(colOffenAlt, DateValue(TagText) < varHeute && !Coalesce(TestDatensatz, false)))},
            Set(varOffenNr, If(Coalesce(varOffenNr, 1) >= n, 1, Coalesce(varOffenNr, 1) + 1))
        )
      PressedColor: =clrFehler
      PressedFill: =clrFehlerHell
      RadiusBottomLeft: =8
      RadiusBottomRight: =8
      RadiusTopLeft: =8
      RadiusTopRight: =8
      Size: =14
      Text: ="Weiter ›"
      Visible: =CountRows(Filter(colOffenAlt, DateValue(TagText) < varHeute && !Coalesce(TestDatensatz, false))) > 1
      Width: =120
      X: =Parent.Width - 356
      Y: =20
```

## Teil B – Builder

### B0 – Daten

Spalte aus A1. Builder: Daten → `RG_Rundgaenge` → ⋯ → Aktualisieren.

### B1 – neues Steuerelement `btnPlTest`

**Wo hin:** **`conPlKopf`** markieren → Strg+V.

```yaml
- btnPlTest:
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
      OnSelect: |-
        =If(!varIsLoading && Now() >= varSperreBis && varPlanRgID > 0,
            Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));
            Set(varPatchFehler, false);
            IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varPlanRgID), {Testrundgang: !Coalesce(varPlanRg.Testrundgang, false)}), Set(varPatchFehler, true));
            If(varPatchFehler,
                Notify("Nicht gespeichert. Bitte erneut versuchen.", NotificationType.Error),
                Set(varPlanRg, LookUp(RG_Rundgaenge, ID = varPlanRgID));
                Patch(colRg, LookUp(colRg, ID = varPlanRgID), varPlanRg);
                Notify(If(Coalesce(varPlanRg.Testrundgang, false), "Testrundgang: Neue Läufe zählen als Testdaten.", "Kein Testrundgang mehr: Neue Läufe zählen als echte Rundgänge."), NotificationType.Success)
            )
        )
      PressedColor: =Color.White
      PressedFill: =RGBA(255, 255, 255, 0.32)
      RadiusBottomLeft: =6
      RadiusBottomRight: =6
      RadiusTopLeft: =6
      RadiusTopRight: =6
      Size: =14
      Text: =If(Coalesce(varPlanRg.Testrundgang, false), "✓ Testrundgang", "○ Testrundgang")
      Width: =220
      X: =Parent.Width - 236
      Y: =12
```

### B1 – neues Steuerelement `lblKoNutzung`

**Wo hin:** **`conKoForm`** markieren → Strg+V.

```yaml
- lblKoNutzung:
    Control: Label@2.5.1
    Properties:
      Color: =If(!Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false) && CountRows(Filter(colKoNutz As u, (";" & Text(varKoID) & ";") in (";" & Substitute(Coalesce(u.Ansprechpartner, ""), " ", "") & ";"))) > 0, clrFehler, clrTextGrau)
      Font: =Font.'Segoe UI'
      Height: =64
      Size: =12
      Text: |-
        =If(Coalesce(LookUp(colKoAlle, ID = varKoID).Allgemein, false), "Erscheint bei jedem kritischen Mangel.", With({n: CountRows(Filter(colKoNutz As u, (";" & Text(varKoID) & ";") in (";" & Substitute(Coalesce(u.Ansprechpartner, ""), " ", "") & ";"))), r: CountRows(Distinct(Filter(colKoNutz As u, (";" & Text(varKoID) & ";") in (";" & Substitute(Coalesce(u.Ansprechpartner, ""), " ", "") & ";")), RundgangID))}, If(n = 0, "Noch bei keinem kritischen Prüfpunkt eingetragen.", "Eingetragen bei " & n & " kritischen Prüfpunkt" & If(n = 1, "", "en") & " in " & r & " Rundgang" & If(r = 1, "", "en") & "." & If(Coalesce(LookUp(colKoAlle, ID = varKoID).Aktiv, false), "", " Inaktiv: Prüfer sehen ihn dort nicht mehr. Im Prüfpunkt unter „Bei n.i.O.“ entfernen."))))
      VerticalAlign: =VerticalAlign.Top
      Width: =Parent.Width
      X: =0
      Y: =480
```

### B2.1 · `btnNioKontakt.Text`

**Pfad:** `scrEditor › conNio › conNioKarte › galNioKontakte › btnNioKontakt` → Text

```
If(Coalesce(ThisItem.Allgemein; false); "✓ "; If(Text(ThisItem.ID) in Filter(Split(Coalesce(LookUp(colP; ID = varAuswahlID).Ansprechpartner; ""); ";"); Trim(Value) <> "").Value; "✓ "; "○ ")) & ThisItem.Title & If(Trim(Coalesce(ThisItem.Kontakt; "")) = ""; ""; " – " & ThisItem.Kontakt) & If(Coalesce(ThisItem.Allgemein; false); "  (immer)"; "") & If(Coalesce(ThisItem.Aktiv; false); ""; "  (inaktiv – entfernen)")
```

```diff
- … ) & If(Coalesce(ThisItem.Allgemein; false); "  (immer)"; "") …
+ … ) & If(Coalesce(ThisItem.Allgemein; false); "  (immer)"; "") & If(Coalesce(ThisItem.Aktiv; false); ""; "  (inaktiv – entfernen)") …
```

**Kurz erklärt:** **A7:** Kennzeichnet inaktive mit „(inaktiv – entfernen)“. Antippen nimmt sie heraus.

**Nachprüfen:** endet auf `mmer)"; "") & If(Coalesce(ThisItem.Aktiv; false); ""; "  (inaktiv – entfernen)")`

### B2.2 · `btnPNio.OnSelect`

**Pfad:** `scrEditor › conEdMitte › conEdP › btnPNio` → OnSelect

```
If(!varIsLoading;
    Refresh(RG_Ansprechpartner);;
    ClearCollect(colKontakte; RG_Ansprechpartner);;
    Reset(txtNioRueckText);;
    Reset(txtNioKritText);;
    Set(varNioOffen; true)
)
```

```diff
-    ClearCollect(colKontakte; Filter(RG_Ansprechpartner; Aktiv = true));;
+    Refresh(RG_Ansprechpartner);;
+    ClearCollect(colKontakte; RG_Ansprechpartner);;
```

**Kurz erklärt:** **A7:** Das Fenster liest die Ansprechpartner frisch und vollständig (auch inaktive).

**Nachprüfen:** endet auf `)`

### B2.3 · `galNioKontakte.Items`

**Pfad:** `scrEditor › conNio › conNioKarte › galNioKontakte` → Items

```
Sort(Filter(colKontakte; Coalesce(Aktiv; false) || Text(ID) in Filter(Split(Coalesce(LookUp(colP; ID = varAuswahlID).Ansprechpartner; ""); ";"); Trim(Value) <> "").Value); If(Coalesce(Aktiv; false); "0"; "1") & If(Coalesce(Allgemein; false); "0"; "1") & Lower(Title))
```

```diff
-Sort(colKontakte; If(Coalesce(Allgemein; false); 0; 1) & Lower(Title))
+ Sort(Filter(colKontakte; Coalesce(Aktiv; false) || Text(ID) in Filter(Split(Coalesce(LookUp(colP; ID = varAuswahlID).Ansprechpartner; ""); ";"); Trim(Value) <> "").Value); If(Coale …
```

**Kurz erklärt:** **A7:** Zeigt auch inaktive Ansprechpartner, **wenn** sie an diesem Prüfpunkt eingetragen sind (unten, zum Entfernen).

**Nachprüfen:** endet auf `iv; false); "0"; "1") & If(Coalesce(Allgemein; false); "0"; "1") & Lower(Title))`

### B2.4 · `lblEdArt.Text`

**Pfad:** `scrEditor › conEdMitte › conEdLeiste › lblEdArt` → Text

```
If(Left(varFrage; 3) = "del"; If(varAuswahlEbene = 1; "Entfernt den Bereich mit " & CountRows(Filter(colK; BereichID = varAuswahlID)) & " Kategorien und " & CountRows(Filter(colP; KategorieID in Filter(colK; BereichID = varAuswahlID).ID)) & " Prüfpunkten. Nochmal tippen."; varAuswahlEbene = 2; "Entfernt die Kategorie mit " & CountRows(Filter(colP; KategorieID = varAuswahlID)) & " Prüfpunkten. Nochmal tippen."; With({n: CountRows(Filter(colP; BedingungPunkt = varAuswahlID || VergleichPunkt = varAuswahlID))}; If(n > 0; "Achtung: " & n & If(n = 1; " Frage hängt"; " Fragen hängen") & " davon ab: Bedingung bzw. Vergleich fällt weg. Nochmal tippen."; "Entfernt den Prüfpunkt. Nochmal tippen."))); Switch(varAuswahlEbene; 1; "Bereich"; 2; "Kategorie"; "Prüfpunkt"))
```

```diff
- … gorieID = varAuswahlID)) & " Prüfpunkten. Nochmal tippen."; "Entfernt den Prüfpunkt. Nochmal tippen."); Switch(varAuswahlEbene; 1; "Bereich"; 2; "Kategorie"; "Prüfpunkt")) …
+ … gorieID = varAuswahlID)) & " Prüfpunkten. Nochmal tippen."; With({n: CountRows(Filter(colP; BedingungPunkt = varAuswahlID || VergleichPunkt = varAuswahlID))}; If(n > 0; "Achtung: " …
```

**Kurz erklärt:** **A6:** Beim Entfernen eines Prüfpunkts steht dabei, wie viele Fragen davon abhängen (Bedingung oder Vergleich). Die fallen beim Entfernen weg – das war schon so, jetzt sieht man es vorher.

**Nachprüfen:** endet auf `tippen."))); Switch(varAuswahlEbene; 1; "Bereich"; 2; "Kategorie"; "Prüfpunkt"))`

### B2.5 · `lblLiInfo.Text`

**Pfad:** `scrListe › galLi › conLiKarte › lblLiInfo` → Text

```
If(fnStatus(ThisItem.Status; ThisItem.Aktiv) = "Entwurf"; "noch nie aktiviert"; "aktive Fassung " & fnAktiveFassung(ThisItem.Fassung)) & "  ·  " & With({pl: Filter(colPlanAlle; RundgangID = ThisItem.ID && Coalesce(Aktiv; false))}; If(IsEmpty(pl); "kein Plan"; "Plan: " & Concat(pl As x; Left(fnWochentag(x.Wochentag); 2) & " " & fnZyklus(x.ZyklusWochen); ", "))) & If(Coalesce(ThisItem.EntwurfFassung; 0) > 0 && fnStatus(ThisItem.Status; ThisItem.Aktiv) <> "Entwurf"; "  ·  Entwurf Fassung " & ThisItem.EntwurfFassung & " in Arbeit" & If(Coalesce(ThisItem.EntwurfVon; "") <> ""; " (" & ThisItem.EntwurfVon & ")"; ""); "") & If(Coalesce(ThisItem.Testrundgang; false); "  ·  Testrundgang"; "")
```

```diff
- … rfVon; "") <> ""; " (" & ThisItem.EntwurfVon & ")"; ""); "") …
+ … rfVon; "") <> ""; " (" & ThisItem.EntwurfVon & ")"; ""); "") & If(Coalesce(ThisItem.Testrundgang; false); "  ·  Testrundgang"; "") …
```

**Kurz erklärt:** **A11:** Zeigt „· Testrundgang“ in der Übersicht.

**Nachprüfen:** endet auf `; ""); "") & If(Coalesce(ThisItem.Testrundgang; false); "  ·  Testrundgang"; "")`

### B2.6 · `lblNioLeer.Visible`

**Pfad:** `scrEditor › conNio › conNioKarte › lblNioLeer` → Visible

```
Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false) && IsEmpty(Filter(colKontakte; Coalesce(Aktiv; false)))
```

```diff
-Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false) && IsEmpty(colKontakte)
+Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false) && IsEmpty(Filter(colKontakte; Coalesce(Aktiv; false)))
```

**Kurz erklärt:** **A7:** „Noch keine Ansprechpartner“ zählt nur aktive.

**Nachprüfen:** endet auf `wahlID).Kritisch; false) && IsEmpty(Filter(colKontakte; Coalesce(Aktiv; false)))`

### B2.7 · `lblPlHinweis.Text`

**Pfad:** `scrPlan › lblPlHinweis` → Text

```
"Wann ist der Rundgang dran? Änderungen gelten sofort, auch für einen aktiven Rundgang." & If(!Coalesce(varPlanRg.Aktiv; false); " Der Rundgang ist nicht aktiv: Er erscheint erst nach dem Aktivieren auf der Startseite."; "") & If(Coalesce(varPlanRg.Testrundgang; false); " Testrundgang: Läufe zählen als Testdaten (eigener Ordner, nicht im Hinweis „Nicht abgeschlossen“)."; "")
```

```diff
-"Wann ist der Rundgang dran? Änderungen gelten sofort, auch für einen aktiven Rundgang." & If(!Coalesce(varPlanRg.Aktiv; false); " Der Rundgang ist nicht aktiv: Er erscheint erst nach dem Aktivieren auf der Startseite."; "")
+ … erscheint erst nach dem Aktivieren auf der Startseite."; "") & If(Coalesce(varPlanRg.Testrundgang; false); " Testrundgang: Läufe zählen als Testdaten (eigener Ordner, nicht im Hinw …
```

**Kurz erklärt:** **A11:** Hinweis, was „Testrundgang“ bewirkt.

**Nachprüfen:** endet auf `en als Testdaten (eigener Ordner, nicht im Hinweis „Nicht abgeschlossen“)."; "")`

### B2.8 · `scrKontakte.OnVisible`

**Pfad:** `scrKontakte` → OnVisible

```
Set(varIsLoading; true);;
Set(varLadeText; "");;
Concurrent(Refresh(RG_Ansprechpartner); Refresh(RG_Pruefpunkte));;
ClearCollect(colKoAlle; RG_Ansprechpartner);;
ClearCollect(colKoNutz; ShowColumns(Filter(RG_Pruefpunkte; Aktiv = true && Kritisch = true); Ansprechpartner; RundgangID));;
Set(varKoID; Coalesce(First(Sort(colKoAlle; Title)).ID; 0));;
Reset(txtKoRolle);;
Reset(txtKoName);;
Reset(txtKoTelefon);;
Reset(txtKoHinweis);;
Set(varIsLoading; false)
```

```diff
-Refresh(RG_Ansprechpartner);;
+Concurrent(Refresh(RG_Ansprechpartner); Refresh(RG_Pruefpunkte));;
+ClearCollect(colKoNutz; ShowColumns(Filter(RG_Pruefpunkte; Aktiv = true && Kritisch = true); Ansprechpartner; RundgangID));;
```

**Kurz erklärt:** **A7:** Liest zusätzlich, an welchen kritischen Prüfpunkten wer eingetragen ist (`colKoNutz`).

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | Start (heute) mit den ZZ-Test-Läufen 18, 20–22 offen | kein roter Hinweis für diese |
| T2 | zwei echte offene Läufe an früheren Tagen | Hinweis „… (1/2)“, „Weiter ›“ → „(2/2)“, „Öffnen“ öffnet den angezeigten |
| T3 | Builder: Plan → „○ Testrundgang“ | „✓ Testrundgang“, Übersicht „· Testrundgang“ |
| T4 | App: Lauf dieses Rundgangs starten | `TestDatensatz` = Ja (Konsole/Liste), Protokoll „TESTDATEN“, Fotos unter `TEST/` |
| T5 | Rundgang mit Namen „ZZ Test …“, Testrundgang = Nein | Lauf zählt als echt (Absicht) |
| T6 | Builder: Ansprechpartner inaktiv stellen, der an einem kritischen Prüfpunkt hängt | rote Zeile „Eingetragen bei 1 …“; im Prüfpunkt „Bei n.i.O.“: „(inaktiv – entfernen)“, antippen → weg |
| T7 | Builder: Prüfpunkt entfernen, an dem eine Bedingung hängt | Warntext „Achtung: 1 Frage hängt davon ab …“ |

## Rückweg

Vorher-Fassungen einsetzen, `btnStartOffenWeiter`, `btnPlTest`, `lblKoNutzung` löschen. Spalte darf bleiben.

## Anhang – Vorher-Fassungen

**Rundgang DEV `btnStartTagLaden.OnSelect` vorher**

```
Set(varIsLoading; true);;
Concurrent(Refresh(RG_Durchfuehrungen); Refresh(RG_KategorieErgebnisse));;
Concurrent(
    ClearCollect(colDurchTag; Filter(RG_Durchfuehrungen; TagText = varTagText));
    ClearCollect(colErgTag; ShowColumns(Filter(RG_KategorieErgebnisse; TagText = varTagText); DurchfuehrungID; KategorieID));
    ClearCollect(colOffenAlt; ShowColumns(Filter(RG_Durchfuehrungen; Status = stInArbeit || Status = stAbschluss); ID; Title; RundgangID; RundgangName; TagText))
);;
Set(varIsLoading; false)
```

**Rundgang DEV `conStartOffen.Visible` vorher**

```
CountRows(Filter(colOffenAlt; DateValue(TagText) < varHeute)) > 0
```

**Rundgang DEV `lblStartOffen.Text` vorher**

```
With({o: First(Sort(Filter(colOffenAlt; DateValue(TagText) < varHeute); TagText)); n: CountRows(Filter(colOffenAlt; DateValue(TagText) < varHeute))};
    "⚠  Nicht abgeschlossen: " & o.RundgangName & " vom " & Text(DateValue(o.TagText); "dd.mm.yyyy") & If(n > 1; " (und " & (n - 1) & " weitere)"; ""))
```

**Rundgang DEV `lblStartOffen.Width` vorher**

```
Parent.Width - 260
```

**Rundgang DEV `btnStartOffen.OnSelect` vorher**

```
If(!varIsLoading;
    With({o: First(Sort(Filter(colOffenAlt; DateValue(TagText) < varHeute); TagText))};
        If(!IsBlank(o);
            Set(varTag; DateValue(o.TagText));;
            Set(varTagText; o.TagText);;
            Set(varRgID; o.RundgangID);;
            Set(varSchluessel; o.Title);;
            Set(varDurchID; o.ID);;
            Navigate(scrRundgang; ScreenTransition.None)
        )
    )
)
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
                    Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: ISOWeekNum(varTag); Wochentag: Weekday(varTag; StartOfWeek.Monday); Status: stInArbeit; AnzahlKategorien: CountRows(colKatBau); KategorieListe: JSON(colKatBau; JSONFormat.Compact); PrueferEmail: User().Email; PrueferName: User().FullName; StartZeit: Now(); TestDatensatz: StartsWith(ThisItem.Title; "ZZ Test")});
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

**Builder `btnNioKontakt.Text` vorher**

```
If(Coalesce(ThisItem.Allgemein; false); "✓ "; If(Text(ThisItem.ID) in Filter(Split(Coalesce(LookUp(colP; ID = varAuswahlID).Ansprechpartner; ""); ";"); Trim(Value) <> "").Value; "✓ "; "○ ")) & ThisItem.Title & If(Trim(Coalesce(ThisItem.Kontakt; "")) = ""; ""; " – " & ThisItem.Kontakt) & If(Coalesce(ThisItem.Allgemein; false); "  (immer)"; "")
```

**Builder `btnPNio.OnSelect` vorher**

```
If(!varIsLoading;
    ClearCollect(colKontakte; Filter(RG_Ansprechpartner; Aktiv = true));;
    Reset(txtNioRueckText);;
    Reset(txtNioKritText);;
    Set(varNioOffen; true)
)
```

**Builder `galNioKontakte.Items` vorher**

```
Sort(colKontakte; If(Coalesce(Allgemein; false); 0; 1) & Lower(Title))
```

**Builder `lblEdArt.Text` vorher**

```
If(Left(varFrage; 3) = "del"; If(varAuswahlEbene = 1; "Entfernt den Bereich mit " & CountRows(Filter(colK; BereichID = varAuswahlID)) & " Kategorien und " & CountRows(Filter(colP; KategorieID in Filter(colK; BereichID = varAuswahlID).ID)) & " Prüfpunkten. Nochmal tippen."; varAuswahlEbene = 2; "Entfernt die Kategorie mit " & CountRows(Filter(colP; KategorieID = varAuswahlID)) & " Prüfpunkten. Nochmal tippen."; "Entfernt den Prüfpunkt. Nochmal tippen."); Switch(varAuswahlEbene; 1; "Bereich"; 2; "Kategorie"; "Prüfpunkt"))
```

**Builder `lblLiInfo.Text` vorher**

```
If(fnStatus(ThisItem.Status; ThisItem.Aktiv) = "Entwurf"; "noch nie aktiviert"; "aktive Fassung " & fnAktiveFassung(ThisItem.Fassung)) & "  ·  " & With({pl: Filter(colPlanAlle; RundgangID = ThisItem.ID && Coalesce(Aktiv; false))}; If(IsEmpty(pl); "kein Plan"; "Plan: " & Concat(pl As x; Left(fnWochentag(x.Wochentag); 2) & " " & fnZyklus(x.ZyklusWochen); ", "))) & If(Coalesce(ThisItem.EntwurfFassung; 0) > 0 && fnStatus(ThisItem.Status; ThisItem.Aktiv) <> "Entwurf"; "  ·  Entwurf Fassung " & ThisItem.EntwurfFassung & " in Arbeit" & If(Coalesce(ThisItem.EntwurfVon; "") <> ""; " (" & ThisItem.EntwurfVon & ")"; ""); "")
```

**Builder `lblNioLeer.Visible` vorher**

```
Coalesce(LookUp(colP; ID = varAuswahlID).Kritisch; false) && IsEmpty(colKontakte)
```

**Builder `lblPlHinweis.Text` vorher**

```
"Wann ist der Rundgang dran? Änderungen gelten sofort, auch für einen aktiven Rundgang." & If(!Coalesce(varPlanRg.Aktiv; false); " Der Rundgang ist nicht aktiv: Er erscheint erst nach dem Aktivieren auf der Startseite."; "")
```

**Builder `scrKontakte.OnVisible` vorher**

```
Set(varIsLoading; true);;
Set(varLadeText; "");;
Refresh(RG_Ansprechpartner);;
ClearCollect(colKoAlle; RG_Ansprechpartner);;
Set(varKoID; Coalesce(First(Sort(colKoAlle; Title)).ID; 0));;
Reset(txtKoRolle);;
Reset(txtKoName);;
Reset(txtKoTelefon);;
Reset(txtKoHinweis);;
Set(varIsLoading; false)
```

