# Paket 25 – Rückbau Prüferauswahl (echte Anmeldung statt Gerätekonto)

Stand 09.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket25), `werkzeuge/builder.py`, `werkzeuge/doc_paket25.py`. Vorher = Export 09.11. 14:09 (DEV) bzw. 14:09 (Builder) – die vom Einsetz-Chat geänderte Fassung (A17) ist berücksichtigt; alle Vorher-Fassungen sind zeichengleich mit dem Export.

## Kurzfassung

- Entscheidung 09.11.: Jeder meldet sich mit seiner echten Mail an. Die **Prüferauswahl aus Paket 11 fällt weg**, Prüfer ist wieder überall `User()` (wie vor Paket 11).
- **Bleibt:** Unterschrift (Pflicht beim Abschließen, `RG_Unterschriften`, Link/Name/Zeit an der Durchführung) und Kopfdaten (Standort/Adresse/Auftraggeber). Unter der Unterschrift steht jetzt der angemeldete Name.
- **Weg:** `conPwWahl` (Rundgang DEV), `scrPruefer` + `btnKoPruefer` (Builder), Datenquellen `RG_Pruefer` und Office 365-Benutzer (beide Apps).
- **Dazu Reparatur Builder:** Beim Einsetzen von Paket 23 ist die neue Formel für `btnPNio.OnSelect` in `btnNioKontakt.OnSelect` gelandet (Export 09.11.). Folge: Antippen eines Ansprechpartners im Fenster „Bei n.i.O.“ öffnet das Fenster neu, statt ihn an-/abzuwählen.
- Der Generator prüft, dass danach **keine** Formel mehr auf `varPruefer`, `varPrWahl`, `colPrueferAlle`, `RG_Pruefer`, `Office365Users`, `conPwWahl` oder dessen Kinder verweist. Neu: Prüfung gegen `IfError(…; Set(…))` als `If`-Zweig auch für Rundgang DEV (A17), Mutation 13/13.
- Umfang: DEV 10 Properties + 1 Container löschen + 2 Datenquellen; Builder 1 Bildschirm + 1 Knopf löschen, 2 Properties reparieren, 2 Datenquellen. **Nicht in Studio getestet.**

## Teil A – Rundgang DEV

### A1 – SharePoint und Daten (zuerst)

Keine neuen Spalten. Die Liste `RG_Pruefer` und die Spalte `Geraetekonto` dürfen in SharePoint bleiben (werden nicht mehr benutzt).
**Reihenfolge:** erst A3 (Formeln), dann A4 (Löschen), dann A5 (Datenquellen). Sonst wird es rot.

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
Set(varUnterschriftOffen; false);;
Set(varUnterschriftDa; false);;
Set(varUnterschriftBild; "");;
Set(varUnterschriftUrl; "")
```

```diff
-Set(varPruefer; {Name: ""; Email: ""});;
-Set(varPrWahl; true);;
```

**Kurz erklärt:** Startwerte `varPruefer`/`varPrWahl` entfallen. Die Startwerte der Unterschrift bleiben.

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
    ClearCollect(colPlan; Filter(RG_Plan; Aktiv = true))
);;
Select(btnStartTagLaden)
```

```diff
-    ClearCollect(colPlan; Filter(RG_Plan; Aktiv = true));
-    ClearCollect(colPrueferAlle; RG_Pruefer)
+    ClearCollect(colPlan; Filter(RG_Plan; Aktiv = true))
```

**Kurz erklärt:** Die Prüferliste wird nicht mehr geladen.

**Nachprüfen:** endet auf `Select(btnStartTagLaden)`

### A3.3 · `lblStartNutzer.Text`

**Pfad:** `scrStart › conStartKopf › lblStartNutzer` → Text

```
User().FullName & If(cfgTestmodus; "  ·  TESTMODUS"; "")
```

```diff
-If(Coalesce(varPruefer.Email; "") = ""; "Kein Prüfer gewählt"; varPruefer.Name & "  ·  wechseln ›") & If(cfgTestmodus; "  ·  TESTMODUS"; "")
+User().FullName & If(cfgTestmodus; "  ·  TESTMODUS"; "")
```

**Kurz erklärt:** Oben rechts wieder der angemeldete Name (wie vor Paket 11).

**Nachprüfen:** endet auf `User().FullName & If(cfgTestmodus; "  ·  TESTMODUS"; "")`

### A3.4 · `lblStartNutzer.OnSelect`

**Pfad:** `scrStart › conStartKopf › lblStartNutzer` → OnSelect

```
false
```

```diff
-If(!varIsLoading; Set(varPrWahl; true))
+false
```

**Kurz erklärt:** Antippen tut nichts mehr (Standardwert `false`).

**Nachprüfen:** endet auf `false`

### A3.5 · `btnRgAktion.OnSelect`

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
-If(Coalesce(varPruefer.Email; "") = "";
-    Set(varPrWahl; true);
-    If(!varIsLoading && Now() >= varSperreBis;
-        Set(varIsLoading; true);;
-        Set(varPatchFehler; false);;
-        Set(varRgID; ThisItem.ID);;
-        Set(varSchluessel; "R" & ThisItem.ID & "-" & varTagText);;
-        Refresh(RG_Durchfuehrungen);;
-        Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
-        If(varDurchID = 0;
-            If(DateDiff(varTag; varHeute; TimeUnit.Days) < 0 || DateDiff(varTag; varHeute; TimeUnit.Days) > cfgNachholTage;
-                Notify("Für diesen Tag kann kein Rundgang gestartet werden."; NotificationType.Error);
-                With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k: Filter(RG_Kategorien; Aktiv = true)};
- With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; B …
-                        ClearCollect(colKatBau; ForAll(Sequence(CountRows(kk)) As s; With({z: Index(kk; s.Value)}; {KategorieID: z.ID; Position: s.Value; BereichName: z.BName; KategorieName: z.Title})))
-                    )
+If(!varIsLoading && Now() >= varSperreBis;
+    Set(varIsLoading; true);;
+    Set(varPatchFehler; false);;
+    Set(varRgID; ThisItem.ID);;
+    Set(varSchluessel; "R" & ThisItem.ID & "-" & varTagText);;
+    Refresh(RG_Durchfuehrungen);;
+    Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
+    If(varDurchID = 0;
+        If(DateDiff(varTag; varHeute; TimeUnit.Days) < 0 || DateDiff(varTag; varHeute; TimeUnit.Days) > cfgNachholTage;
+            Notify("Für diesen Tag kann kein Rundgang gestartet werden."; NotificationType.Error);
+            With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k: Filter(RG_Kategorien; Aktiv = true)};
+ With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName …
+                    ClearCollect(colKatBau; ForAll(Sequence(CountRows(kk)) As s; With({z: Index(kk; s.Value)}; {KategorieID: z.ID; Position: s.Value; BereichName: z.BName; KategorieName: z.Title})))
+                )
+            );;
+            If(CountRows(colKatBau) = 0;
+                Notify("Für diesen Rundgang sind keine aktiven Kategorien hinterlegt."; NotificationType.Error);
+                IfError(
+ Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: ISOWe …
+                    Set(varPatchFehler; true)
-                If(CountRows(colKatBau) = 0;
-                    Notify("Für diesen Rundgang sind keine aktiven Kategorien hinterlegt."; NotificationType.Error);
-                    IfError(
- Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: I …
-                        Set(varPatchFehler; true)
-                    );;
-                    Refresh(RG_Durchfuehrungen);;
-                    Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
-                    If(varDurchID = 0; Notify("Der Rundgang konnte nicht gestartet werden. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error))
-                )
+                Refresh(RG_Durchfuehrungen);;
+                Set(varDurchID; Coalesce(LookUp(RG_Durchfuehrungen; Title = varSchluessel).ID; 0));;
+                If(varDurchID = 0; Notify("Der Rundgang konnte nicht gestartet werden. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error))
-        );;
-        If(varDurchID > 0; Navigate(scrRundgang; ScreenTransition.None));;
-        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
-        Set(varIsLoading; false)
-    )
+        )
+    );;
+    If(varDurchID > 0; Navigate(scrRundgang; ScreenTransition.None));;
+    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+    Set(varIsLoading; false)
```

**Kurz erklärt:** Wieder genau wie vor Paket 11: Prüfer = angemeldete Person (`User()`), keine Prüfer-Abfrage, `Geraetekonto` wird nicht mehr geschrieben.

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

```diff
- … ows(Filter(colSpeichern; Bewertung = "NIO")); PrueferEmail: varPruefer.Email; PrueferName: varPruefer.Name; GespeichertAm: Now(); TestDatensatz: durch.TestDatensatz}); …
+ … ows(Filter(colSpeichern; Bewertung = "NIO")); PrueferEmail: User().Email; PrueferName: User().FullName; GespeichertAm: Now(); TestDatensatz: durch.TestDatensatz}); …
```

**Kurz erklärt:** Prüfer der Kategorie wieder `User()`.

**Nachprüfen:** endet auf `)`

### A3.7 · `btnKaKritOk.OnSelect`

**Pfad:** `scrKategorie › conKaKrit › conKaKritKarte › btnKaKritOk` → OnSelect

```
If(LookUp(colAntworten; PruefpunktID = varKritPP).Bewertung = "NIO"; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = varKritPP); {KritischOk: true; KritischZeit: Text(Now(); "dd.mm.yyyy hh:mm"); KritischVon: User().FullName}));;
Set(varKritPP; 0);;
Set(varGeaendert; true)
```

```diff
-If(LookUp(colAntworten; PruefpunktID = varKritPP).Bewertung = "NIO"; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = varKritPP); {KritischOk: true; KritischZeit: Text(Now(); "dd.mm.yyyy hh:mm"); KritischVon: varPruefer.Name}));;
+If(LookUp(colAntworten; PruefpunktID = varKritPP).Bewertung = "NIO"; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = varKritPP); {KritischOk: true; KritischZeit: Text(Now(); "dd.mm.yyyy hh:mm"); KritischVon: User().FullName}));;
```

**Kurz erklärt:** „Bescheid gegeben“ wieder mit `User().FullName`.

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
                        With({datei: "Unterschrift-D" & varDurchID & "-" & Text(Now(); "yyyymmdd-hhmmss") & ".png"; ordner: fnArchivOrdner(varDurch.TagText; varDurch.TestDatensatz) & "/" & varDurch.Title};
                            Set(varUnterschriftUrl; If(IsError(aRG_Foto_hochladen.Run({contentBytes: penRuUnterschrift.Image; name: datei}; datei; ordner; varDurchID; 0; varDurch.TestDatensatz)); ""; fnSpUrl("RG_Fotos"; ordner & "/" & datei)))
                        );;
                        IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSoll); UnterschriftUrl: varUnterschriftUrl; UnterschriftName: User().FullName; UnterschriftZeit: Now()}); Set(varPatchFehler; true));;
                        If(!varPatchFehler && IsBlank(LookUp(RG_Unterschriften; DurchfuehrungID = varDurchID).ID);
                            If(IsError(Patch(RG_Unterschriften; Defaults(RG_Unterschriften); {Title: "D" & varDurchID; DurchfuehrungID: varDurchID; Bild: varUnterschriftBild})); Set(varPatchFehler; true))
                        );;
                        Refresh(RG_Durchfuehrungen);;
                        Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));;
                        If(varDurch.Status = stAbgeschlossen;
                            Notify("Rundgang abgeschlossen · " & CountRows(colMaengelSoll) & " Mängel erfasst. Protokoll wird archiviert …" & If(varUnterschriftUrl = ""; " (Unterschrift-Datei nicht hochgeladen, steht aber im Protokoll.)"; ""); NotificationType.Success);;
                                Set(varUnterschriftOffen; false);;
                                Set(varArchivStart; false);;
                                Navigate(scrProtokoll; ScreenTransition.None);
                            Notify("Der Abschluss wurde nicht bestätigt. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error)
                        )
                    )
                )
            )
        );;
        Set(varUnterschriftOffen; false);;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
    )
)
```

```diff
-    If(!varAbschlussFrage && Coalesce(varPruefer.Email; "") = "";
-        Notify("Kein Prüfer gewählt. Bitte auf der Startseite oben rechts den Prüfer wählen."; NotificationType.Warning);
-        !varAbschlussFrage;
+    If(!varAbschlussFrage;
- {Title: m.Title; DurchfuehrungID: varDurchID; PruefpunktID: m.PruefpunktID; RundgangName: varDurch.RundgangName; BereichName: m.BereichName; Kategor …
+ {Title: m.Title; DurchfuehrungID: varDurchID; PruefpunktID: m.PruefpunktID; RundgangName: varDurch.RundgangName; BereichName: m.BereichName; Kategor …
- IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSol …
+ IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSol …
-                                Set(varPruefer; {Name: ""; Email: ""});;
-                                Set(varPrWahl; true);;
```

**Kurz erklärt:** Unterschrift bleibt. Entfernt: die Meldung „Kein Prüfer gewählt“ und das Zurücksetzen des Prüfers nach dem Abschluss. `FestgestelltVon` und `UnterschriftName` wieder aus `User()`. Die Korrektur A17 (`If(IsError(Patch(RG_Unterschriften …)))`) ist enthalten.

**Nachprüfen:** endet auf `)`

### A3.9 · `lblRuUText.Text`

**Pfad:** `scrRundgang › conRuUnterschrift › conRuUKarte › lblRuUText` → Text

```
"Mit der Unterschrift schließt " & User().FullName & " den Rundgang ab. Danach sind keine Änderungen mehr möglich."
```

```diff
-"Mit der Unterschrift schließt " & varPruefer.Name & " den Rundgang ab. Danach sind keine Änderungen mehr möglich."
+"Mit der Unterschrift schließt " & User().FullName & " den Rundgang ab. Danach sind keine Änderungen mehr möglich."
```

**Kurz erklärt:** Name aus `User()`.

**Nachprüfen:** endet auf `User().FullName & " den Rundgang ab. Danach sind keine Änderungen mehr möglich."`

### A3.10 · `lblRuUName.Text`

**Pfad:** `scrRundgang › conRuUnterschrift › conRuUKarte › lblRuUName` → Text

```
User().FullName & "  ·  " & Text(Today(); "dd.mm.yyyy")
```

```diff
-varPruefer.Name & "  ·  " & Text(Today(); "dd.mm.yyyy")
+User().FullName & "  ·  " & Text(Today(); "dd.mm.yyyy")
```

**Kurz erklärt:** Name aus `User()`.

**Nachprüfen:** endet auf `User().FullName & "  ·  " & Text(Today(); "dd.mm.yyyy")`

### A4 – löschen

In der Strukturansicht von `scrStart` **`conPwWahl`** löschen (mit allen Kindern: `lblPwTitel`, `lblPwHinweis`, `galPwListe`, `btnPwName`, `lblPwLeer`, `lblPwSuchT`, `txtPwSuche`, `galPwSuche`, `btnPwTreffer`, `btnPwZu`).

### A5 – Datenquellen entfernen

Daten → `RG_Pruefer` → ⋯ → **Entfernen**; Daten → **Office 365-Benutzer** (`Office365Users`) → ⋯ → **Entfernen**. Danach App-Prüfung: 0 Fehler erwartet.

## Teil B – Builder

### B1 – Reparatur (Fehleinfügung aus Paket 23)

### B1.1 · `btnNioKontakt.OnSelect`

**Pfad:** `scrEditor › conNio › conNioKarte › galNioKontakte › btnNioKontakt` → OnSelect

```
If(!Coalesce(ThisItem.Allgemein; false);
    With({ids: Filter(Split(Coalesce(LookUp(colP; ID = varAuswahlID).Ansprechpartner; ""); ";"); Trim(Value) <> "")};
        With({neu: If(Text(ThisItem.ID) in ids.Value; Concat(Filter(ids; Trim(Value) <> Text(ThisItem.ID)) As s; Trim(s.Value); ";"); Concat(ids As s2; Trim(s2.Value) & ";") & Text(ThisItem.ID))};
            If(varSchreibbar && varAuswahlEbene = 3;
                Refresh(RG_Rundgaenge);;
                Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
                If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
                If(varEntwurfOk;
                    Set(varPatchFehler; false);;
                    IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {Ansprechpartner: neu}); Set(varPatchFehler; true));;
                    If(varPatchFehler;
                        Notify("Nicht gespeichert. Bitte erneut versuchen."; NotificationType.Error);
                        Patch(colP; LookUp(colP; ID = varAuswahlID); LookUp(RG_Pruefpunkte; ID = varAuswahlID));;
                        Set(varGespeichertText; "Gespeichert " & Text(Now(); "hh:mm:ss"))
                    )
                )
            )
        )
    )
)
```

**Nachprüfen:** endet auf `)`

**Kurz erklärt:** Wieder: Antippen nimmt den Ansprechpartner auf bzw. heraus (Formel aus Paket 9). Hier stand die Öffnen-Formel von `btnPNio`.

### B1.2 · `btnPNio.OnSelect`

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

**Nachprüfen:** endet auf `)`

**Kurz erklärt:** Öffnet „Bei n.i.O.“ und liest alle Ansprechpartner frisch (auch inaktive, zum Entfernen) – das war der eigentliche Schritt aus Paket 23.

### B2 – löschen

- Bildschirm **`scrPruefer`** löschen (falls schon eingefügt).
- In `scrKontakte › conKoKopf` den Knopf **`btnKoPruefer`** löschen (falls schon eingefügt).
- Daten → `RG_Pruefer` und **Office365-Benutzer** (deutsch `'Office365-Benutzer'`) → ⋯ → Entfernen.

### B3 – Kopfdaten im Plan (bleiben)

Im Export 09.11. fehlen die Kopfdaten-Felder (Paket 11 B1.2–B1.9: `lblPlKopfT`, `lblPlStandortT`, `txtPlStandort`, `lblPlAdresseT`, `txtPlAdresse`, `lblPlAuftragT`, `txtPlAuftrag`; B2.1 `galPl.Height`). Wenn sie in Studio noch nicht da sind (oder nicht veröffentlicht): aus `pakete/PAKET_11_PRUEFER_UNTERSCHRIFT.md` B1.2–B1.9 und B2.1 einfügen – unverändert gültig.

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | App starten | kein „Wer prüft?“; oben rechts der eigene Name |
| T2 | Rundgang starten, Kategorie speichern | `PrueferName`/`PrueferEmail` = angemeldete Person; `Geraetekonto` leer |
| T3 | Kritischer Mangel → Bescheid gegeben | im JSON `KritischVon` = eigener Name; Protokoll „KRITISCH – Bescheid gegeben, bestätigt von <Name>“ |
| T4 | Abschließen | Unterschriftsfeld mit eigenem Namen; Protokoll unten Unterschrift + Name; Mängel `FestgestelltVon` = eigene Mail |
| T4b | „Rundgang abschließen“ → Unterschrift → Abbrechen → erneut „Rundgang abschließen“ | Feld wieder leer, Abschluss erst nach neuer Unterschrift |
| T4c | „Unterschreiben und abschließen“ zweimal schnell | nur ein Abschluss, Mängel nicht doppelt |
| T5 | Nach dem Abschluss zur Startseite | keine Prüferauswahl |
| T6 | App-Prüfung beider Apps | 0 Fehler |
| T7 | Builder: Prüfpunkt › Bei n.i.O. › Ansprechpartner antippen | ✓/○ wechselt, Fenster bleibt offen |
| T8 | Builder: Plan eines Rundgangs | unten Kopfdaten-Felder |

## Rückweg

Erst die Datenquellen `RG_Pruefer` und Office 365-Benutzer wieder hinzufügen, dann `conPwWahl` aus Paket 11 (A2.1) einfügen, dann die Vorher-Fassungen. Builder: `scrPruefer`/`btnKoPruefer` aus Paket 11.

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
Set(varArchivStart; false);;
Set(varPruefer; {Name: ""; Email: ""});;
Set(varPrWahl; true);;
Set(varUnterschriftOffen; false);;
Set(varUnterschriftDa; false);;
Set(varUnterschriftBild; "");;
Set(varUnterschriftUrl; "")
```

**Rundgang DEV `scrStart.OnVisible` vorher**

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

**Rundgang DEV `lblStartNutzer.Text` vorher**

```
If(Coalesce(varPruefer.Email; "") = ""; "Kein Prüfer gewählt"; varPruefer.Name & "  ·  wechseln ›") & If(cfgTestmodus; "  ·  TESTMODUS"; "")
```

**Rundgang DEV `lblStartNutzer.OnSelect` vorher**

```
If(!varIsLoading; Set(varPrWahl; true))
```

**Rundgang DEV `btnRgAktion.OnSelect` vorher**

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

**Rundgang DEV `btnKaKritOk.OnSelect` vorher**

```
If(LookUp(colAntworten; PruefpunktID = varKritPP).Bewertung = "NIO"; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = varKritPP); {KritischOk: true; KritischZeit: Text(Now(); "dd.mm.yyyy hh:mm"); KritischVon: varPruefer.Name}));;
Set(varKritPP; 0);;
Set(varGeaendert; true)
```

**Rundgang DEV `btnRuAbschluss.OnSelect` vorher**

```
If(!varIsLoading && Now() >= varSperreBis;
    If(!varAbschlussFrage && Coalesce(varPruefer.Email; "") = "";
        Notify("Kein Prüfer gewählt. Bitte auf der Startseite oben rechts den Prüfer wählen."; NotificationType.Warning);
        !varAbschlussFrage;
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
                        IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSoll); UnterschriftUrl: varUnterschriftUrl; UnterschriftName: varPruefer.Name; UnterschriftZeit: Now()}); Set(varPatchFehler; true));;
                        If(!varPatchFehler && IsBlank(LookUp(RG_Unterschriften; DurchfuehrungID = varDurchID).ID);
                            If(IsError(Patch(RG_Unterschriften; Defaults(RG_Unterschriften); {Title: "D" & varDurchID; DurchfuehrungID: varDurchID; Bild: varUnterschriftBild})); Set(varPatchFehler; true))
                        );;
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
        Set(varUnterschriftOffen; false);;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
    )
)
```

**Rundgang DEV `lblRuUText.Text` vorher**

```
"Mit der Unterschrift schließt " & varPruefer.Name & " den Rundgang ab. Danach sind keine Änderungen mehr möglich."
```

**Rundgang DEV `lblRuUName.Text` vorher**

```
varPruefer.Name & "  ·  " & Text(Today(); "dd.mm.yyyy")
```

