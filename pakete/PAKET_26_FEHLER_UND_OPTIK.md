# Paket 26 – Fehler aus dem Testlauf (A3, A5, A9, A10, A12, A13, A14) und Builder-Optik

Stand 13.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket26), `werkzeuge/builder.py`, `werkzeuge/doc_paket26.py`. Vorher = Export 13.11. 12:58 (DEV) bzw. 12:59 (Builder), Kette bis Paket 25 + 24. Alle Vorher-Fassungen sind zeichengleich mit dem Export, **außer** `btnRgAktion.OnSelect` (Fehleinfügung, siehe A3.1).

## Kurzfassung

- **A3 (hoch):** Beim Start eines Laufs kommen nur Kategorien mit mindestens einem aktiven Prüfpunkt hinein. Vorher blieb so ein Lauf für immer offen.
- **A5 (hoch):** „Foto Pflicht“ sperrt eine freiwillige, unbeantwortete Frage nicht mehr.
- **A9 (hoch):** Antworten zu inaktiven Prüfpunkten zählen nicht mehr als n.i.O./Mangel.
- **A10:** Kategorien werden nur aus dem eigenen Rundgang gelesen (Zeilenlimit).
- **A12 (Builder):** Typwechsel weg von „Zahl“ löscht den Vergleich; die Prüfung meldet ihn nur noch bei Zahlen.
- **A13 (Builder):** Neuer Fehler für eine Bedingung „n.i.O.“ an einer Zahl, die nie n.i.O. wird.
- **A14 (beide):** Plan-Wochen zählen ab dem Montag der Startwoche.
- **Builder-Optik:** keine leeren orangen Punkte mehr in der Prüfliste, „Aktivieren …“ grün (bei Fehlern grau und gesperrt), „Gehört zur Kategorie“ zeigt nur den Kategorienamen.
- **Reparatur DEV:** In `btnRgAktion.OnSelect` steht im Export die Formel von `btnKaSpeichern`. A3.1 ersetzt sie ganz.
- **Bewusst nicht drin:** C25 (alle typfremden Felder beim Typwechsel leeren). Ein versehentlicher Typwechsel würde sonst Grenzen/Einheit löschen. Nur der Vergleich wird geleert, weil nur er das Aktivieren sperrt.
- Umfang: DEV 3 Properties, Builder 14 Properties, keine neuen Steuerelemente, keine Daten. Generatoren 0 Fehler, Mutation 13/13 und 13/13, Logik-Probe 124 Szenarien (A5, A14), Builder-Logik 27. **Nicht in Studio getestet.**

## Teil A – Rundgang DEV

### A1 – SharePoint und Daten (zuerst)

Keine neuen Spalten oder Listen.

**Vorab prüfen (Strukturansicht `scrKategorie`):** Im Export 13.11. sind `btnKaBild` und `conKaBild` (mit `btnKaBildSperre`, `conKaBildKarte`) noch da. Falls sie in Studio schon gelöscht sind: nichts tun (der Export zeigt nur die veröffentlichte Fassung). Sonst jetzt löschen (Paket 24) – sie würden das ⓘ überdecken.

### A3 – geänderte Properties

### A3.1 · `btnRgAktion.OnSelect`

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
            With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k1: Filter(RG_Kategorien; RundgangID = varRgID && Aktiv = true); p1: ShowColumns(Filter(RG_Pruefpunkte; RundgangID = varRgID && Aktiv = true); KategorieID)};
            With({k: If(IsEmpty(k1); Filter(RG_Kategorien; Aktiv = true); k1)};
                With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0 && (IsEmpty(p1) || !IsBlank(LookUp(p1 As pp; pp.KategorieID = kat.ID)))); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName; If(Coalesce(LookUp(b As be3; be3.ID = BereichID).Ausblenden; false); ""; LookUp(b As be4; be4.ID = BereichID).Title)); BReihe * 10000 + RgReihenfolge)};
                    ClearCollect(colKatBau; ForAll(Sequence(CountRows(kk)) As s; With({z: Index(kk; s.Value)}; {KategorieID: z.ID; Position: s.Value; BereichName: z.BName; KategorieName: z.Title})))
                )
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
-            With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k: Filter(RG_Kategorien; Aktiv = true)};
- With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName …
+            With({b: Filter(RG_Bereiche; RundgangID = varRgID && Aktiv = true); k1: Filter(RG_Kategorien; RundgangID = varRgID && Aktiv = true); p1: ShowColumns(Filter(RG_Pruefpunkte; RundgangID = varRgID && Aktiv = true); KategorieID)};
+            With({k: If(IsEmpty(k1); Filter(RG_Kategorien; Aktiv = true); k1)};
+ With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0 && (IsEmpty(p1) || !IsBlank(LookUp(p1 As pp; pp.KategorieID = kat.I …
+            )
```

**Kurz erklärt:** **Reparatur + A3 + A10.** Im Export 13.11. steht hier die Formel von `btnKaSpeichern` (Fehleinfügung bei Paket 25). Deshalb die **ganze** Property ersetzen, auch wenn sie anders aussieht als die Vorher-Fassung. Neu: Kategorien werden nur aus **diesem** Rundgang gelesen (`RundgangID = varRgID`, A10). Beim Start werden nur Kategorien aufgenommen, die mindestens einen aktiven Prüfpunkt haben (A3). Für Altbestand ohne `RundgangID` an Kategorien/Prüfpunkten gilt die alte Regel weiter (dann alle aktiven Kategorien bzw. ohne Prüfpunkt-Filter).

**Nachprüfen:** endet auf `)`

### A3.2 · `btnKaSpeichern.OnSelect`

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
                    ClearCollect(colSpeichern; ForAll(Filter(colAntworten; !Inaktiv) As r; If(r.PruefpunktID in colVersteckt.PruefpunktID; Patch(r; {Bewertung: ""; WertText: ""; WertZahl: Blank(); Kommentar: ""; Fotos: ""; Warnung: false; Ausgeblendet: true}); Patch(r; {Ausgeblendet: false}))));;
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
- ClearCollect(colSpeichern; ForAll(colAntworten As r; If(r.PruefpunktID in colVersteckt.PruefpunktID; Patch(r; {Bewertung: ""; WertText: ""; WertZahl: Blank(); K …
+ ClearCollect(colSpeichern; ForAll(Filter(colAntworten; !Inaktiv) As r; If(r.PruefpunktID in colVersteckt.PruefpunktID; Patch(r; {Bewertung: ""; WertText: ""; We …
```

**Kurz erklärt:** **A9.** Antworten zu inzwischen inaktiven Prüfpunkten (`Inaktiv`) kommen nicht mehr in `colSpeichern`: Sie werden nicht mehr mitgeschrieben, nicht gezählt (AnzahlNIO) und nicht als Mangel angelegt. Schon früher gespeicherte Antworten bleiben in SharePoint unverändert. Sonst wie bisher.

**Nachprüfen:** endet auf `)`

### A3.3 · `App.Formulas`

**Pfad:** `App` → Formulas

```
clrPrimaer = ColorValue("#171496");;
clrPrimaerHell = ColorValue("#E8E8F7");;
clrHintergrund = ColorValue("#F4F5F9");;
clrKarte = Color.White;;
clrRahmen = ColorValue("#DADCE5");;
clrText = ColorValue("#1B1B1F");;
clrTextGrau = ColorValue("#5F6370");;
clrErfolg = ColorValue("#0F7B3F");;
clrErfolgHell = ColorValue("#E3F4EA");;
clrFehler = ColorValue("#B3261E");;
clrFehlerHell = ColorValue("#FCE8E6");;
clrGesperrt = ColorValue("#9AA0A6");;
clrGesperrtHell = ColorValue("#EEF0F3");;
clrWarnung = ColorValue("#9A5B00");;
stInArbeit = "InArbeit";;
stAbschluss = "Abschluss";;
stAbgeschlossen = "Abgeschlossen";;
cfgNachholTage = Max(
    0;
    Coalesce(
        Value(
            LookUp(
                RG_Konfiguration;
                Title = "NachholTage"
            ).Wert
        );
        0
    )
);;
cfgTestmodus = Coalesce(
    LookUp(
        RG_Konfiguration;
        Title = "Testmodus"
    ).Wert;
    "Ja"
) <> "Nein";;
cfgTestadresse = Coalesce(
    LookUp(
        RG_Konfiguration;
        Title = "Testadresse"
    ).Wert;
    ""
);;
cfgEmpfaenger = Coalesce(
    LookUp(
        RG_Konfiguration;
        Title = "Empfaenger"
    ).Wert;
    ""
);;
fnTagAnzeige(d: Date): Text = Text(
    d;
    "dddd, dd.mm.yyyy";
    "de-DE"
) & " · KW " & ISOWeekNum(d);;
fnTagLabel(d: Date; heute: Date): Text = Switch(
    DateDiff(
        d;
        heute;
        TimeUnit.Days
    );
    0;
    "Heute – ";
    1;
    "Gestern – ";
    ""
) & fnTagAnzeige(d);;
fnPlanPasst(start: DateTime; bis: DateTime; wt: Number; zyklus: Number; d: Date): Boolean = With(
    {
        t: DateDiff(
            DateAdd(start; 1 - Weekday(start; StartOfWeek.Monday); TimeUnit.Days);
            d;
            TimeUnit.Days
        );
        t0: DateDiff(
            start;
            d;
            TimeUnit.Days
        )
    };
    !IsBlank(start) && Weekday(
        d;
        StartOfWeek.Monday
    ) = wt && t0 >= 0 && (IsBlank(bis) || DateDiff(
        d;
        bis;
        TimeUnit.Days
    ) >= 0) && Mod(
        RoundDown(
            t / 7;
            0
        );
        Max(
            1;
            zyklus
        )
    ) = 0
);;
fnZahlBewertung(z: Number; mi: Number; ma: Number; gmodus: Text): Text = If(
    fnAusserhalb(z; mi; ma);
    Switch(If(gmodus = "Sperren" && !fnSperreGilt(mi; ma); "Mangel"; gmodus); "Warnen"; "IO"; "Sperren"; ""; "NIO");
    "IO"
);;
fnGrenzmodus(g: Text): Text = If(g = "Warnen" || g = "Sperren"; g; "Mangel");;
fnSperreGilt(mi: Number; ma: Number): Boolean = IsBlank(mi) || IsBlank(ma) || mi <= ma;;
fnHtml(t: Text): Text = Substitute(Substitute(Substitute(Substitute(Substitute(t; "&"; "&amp;"); "<"; "&lt;"); ">"; "&gt;"); """"; "&quot;"); "'"; "&#39;");;
cfgAdmins = Coalesce(LookUp(RG_Konfiguration; Title = "Admins").Wert; "");;
fnLinkAnzahl(t: Text): Number = CountRows(Filter(Split(Coalesce(t; ""); " | ") As s; Trim(s.Value) <> ""));;
fnFotoModus(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht"; f; f = "Bei Mangel Pflicht"; "BeiMangel"; alt; "Optional"; "Aus");;
fnFotoNeuErlaubt(bew: Text; foto: Text): Boolean = bew = "NIO" || foto = "Optional" || foto = "Pflicht";;
fnBeantwortet(bew: Text; wt: Text; wz: Number): Boolean = bew <> "" || Trim(wt) <> "" || !IsBlank(wz);;
fnAusserhalb(z: Number; mi: Number; ma: Number): Boolean = !IsBlank(z) && ((!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma));;
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (typ = "ZAHL" && wt = "nicht messbar") || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz; mi; ma));;
fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz) && wt = "") || (typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATUMZEIT") && wt = "")); "Wert";
    typ = "DATUMZEIT" && wt <> "" && (Len(wt) < 16 || "-" in wt); "Uhrzeit";
    typ = "ZAHL" && gmodus = "Sperren" && fnSperreGilt(mi; ma) && fnAusserhalb(wz; mi; ma); "Bereich";
    fnKommentarNoetig(typ; bew; wt; wz; kpfl; gmodus; mi; ma) && Trim(kom) = ""; "Kommentar";
    ((foto = "Pflicht" && (pflicht || bew <> "" || Trim(wt) <> "" || !IsBlank(wz))) || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1; "Foto";
    kritoffen && bew = "NIO"; "Kritisch";
    ""
);;
fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w; "")); "."; ""); " "; ""));;
fnBedGueltig(w: Text; typ: Text; auswahl: Text): Boolean = With({n: fnBedNorm(w)}; n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnBedPasst(w: Text; bew: Text; wt: Text; wz: Number): Boolean = With({n: fnBedNorm(w)}; If(n = "*"; fnBeantwortet(bew; wt; wz); n = fnBedNorm(bew) || n = fnBedNorm(wt) || CountRows(Filter(Split(wt; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnSichtbar(bid: Number; w: Text; gef: Boolean; bBid: Number; bInaktiv: Boolean; bTyp: Text; bAuswahl: Text; bBew: Text; bWt: Text; bWz: Number): Boolean = bid = 0 || Trim(w) = "" || !gef || bInaktiv || bBid <> 0 || !fnBedGueltig(w; bTyp; bAuswahl) || fnBedPasst(w; bBew; bWt; bWz);;
fnDatumText(d: Date; h: Text; m: Text; mitZeit: Boolean): Text = If(IsBlank(d); ""; Text(d; "dd.mm.yyyy") & If(mitZeit && (h <> "" || m <> ""); " " & If(h = ""; "--"; h) & ":" & If(m = ""; "--"; m); ""));;
fnAbweichung(z: Number; l: Number; mx: Number; proz: Boolean; steig: Boolean): Boolean = !IsBlank(z) && !IsBlank(l) && ((steig && z < l) || (!IsBlank(mx) && Round(Abs(z - l); 6) > Round(If(proz; Abs(l) * mx / 100; mx); 6)));;
fnVergleich(z: Number; w: Number; tol: Number): Boolean = !IsBlank(z) && !IsBlank(w) && Round(Abs(z - w); 6) > Round(Coalesce(tol; 0); 6);;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma; kritoffen) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

```diff
+            DateAdd(start; 1 - Weekday(start; StartOfWeek.Monday); TimeUnit.Days);
+            d;
+            TimeUnit.Days
+        );
+        t0: DateDiff(
-    ) = wt && t >= 0 && (IsBlank(bis) || DateDiff(
+    ) = wt && t0 >= 0 && (IsBlank(bis) || DateDiff(
-    (foto = "Pflicht" || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1; "Foto";
+    ((foto = "Pflicht" && (pflicht || bew <> "" || Trim(wt) <> "" || !IsBlank(wz))) || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1; "Foto";
```

**Kurz erklärt:** **A5:** `fnFehltGrund` verlangt bei „Foto Pflicht“ ein Foto nur noch, wenn die Frage Pflicht ist oder beantwortet wurde (freiwillige, unbeantwortete Frage sperrt nicht mehr). „Foto bei Mangel“ unverändert. **A14:** `fnPlanPasst` zählt die Wochen ab dem **Montag der Startwoche**, fällig erst ab dem Startdatum selbst.

**Nachprüfen:** endet auf `p.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;`

## Teil B – Builder

### B0 – Daten

Keine neuen Daten.
**Voraussetzung:** Die Lage-Werte aus Paket 24 (B2.1–B2.19, `conPRest`) sind eingesetzt. Im Export 13.11. fehlen sie noch (Texte drin, Positionen nicht). Erst danach prüfen, ob in `conPRest` noch etwas abgeschnitten ist: Laut Generator passen alle Beschriftungen (Textbreiten-Prüfung mit Innenabstand).

### B2.1 · `App.Formulas`

**Pfad:** `App` → Formulas

```
clrPrimaer = ColorValue("#171496");;
clrPrimaerHell = ColorValue("#E8E8F7");;
clrHintergrund = ColorValue("#F4F5F9");;
clrKarte = Color.White;;
clrRahmen = ColorValue("#DADCE5");;
clrText = ColorValue("#1B1B1F");;
clrTextGrau = ColorValue("#5F6370");;
clrErfolg = ColorValue("#0F7B3F");;
clrErfolgHell = ColorValue("#E3F4EA");;
clrFehler = ColorValue("#B3261E");;
clrFehlerHell = ColorValue("#FCE8E6");;
clrWarnung = ColorValue("#9A5B00");;
clrWarnungHell = ColorValue("#FFF4E0");;
clrGesperrt = ColorValue("#9AA0A6");;
clrGesperrtHell = ColorValue("#EEF0F3");;
cfgBildBibliothek = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/RG_Hinweisbilder";;
fnStatus(s: Text; aktiv: Boolean): Text = If(s = "Vorlage"; "Vorlage"; aktiv; "Aktiv"; s = "Entwurf"; "Entwurf"; "Archiviert");;
fnAktiveFassung(f: Number): Number = If(Coalesce(f; 0) > 0; f; 1);;
fnTypName(t: Text): Text = Switch(t; "IONIO"; "i.O. / n.i.O."; "ZAHL"; "Zahl"; "AUSWAHL"; "Auswahl"; "MEHRFACH"; "Mehrfachauswahl"; "TEXT"; "Text"; "DATUM"; "Datum"; "DATUMZEIT"; "Datum + Uhrzeit"; t);;
fnTypKurz(t: Text): Text = Switch(t; "IONIO"; "i.O./n.i.O."; "ZAHL"; "Zahl"; "AUSWAHL"; "Auswahl"; "MEHRFACH"; "Mehrfach"; "TEXT"; "Text"; "DATUM"; "Datum"; "DATUMZEIT"; "Datum+Zeit"; t);;
fnFotoWert(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht" || f = "Bei Mangel Pflicht"; f; alt; "Optional"; "Aus");;
fnFotoText(f: Text): Text = Switch(f; "Optional"; "Foto freiwillig"; "Pflicht"; "Foto immer Pflicht"; "Bei Mangel Pflicht"; "Foto Pflicht bei Mangel"; "kein Foto (bei n.i.O. möglich)");;
fnGrenzmodus(g: Text): Text = If(g = "Warnen" || g = "Sperren"; g; "Mangel");;
fnGrenzText(mi: Number; ma: Number; einheit: Text): Text = If(IsBlank(mi) && IsBlank(ma); "keine Grenzen"; "i.O. " & If(IsBlank(mi); ""; "ab " & Text(mi)) & If(IsBlank(mi) || IsBlank(ma); ""; " ") & If(IsBlank(ma); ""; "bis " & Text(ma)) & If(Trim(Coalesce(einheit; "")) = ""; ""; " " & einheit));;
fnWerte(t: Text): Number = CountRows(Filter(Split(Coalesce(t; ""); ";") As s; Trim(s.Value) <> ""));;
fnWerteDoppelt(t: Text): Boolean = CountRows(Distinct(Filter(Split(Coalesce(t; ""); ";") As s; Trim(s.Value) <> ""); Lower(Trim(Value)))) < fnWerte(t);;
fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w; "")); "."; ""); " "; ""));;
fnBedGueltig(w: Text; typ: Text; auswahl: Text): Boolean = With({n: fnBedNorm(w)}; n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnBedText(w: Text): Text = Switch(fnBedNorm(w); "nio"; "n.i.O. (Mangel)"; "io"; "i.O."; "*"; "beantwortet"; Trim(Coalesce(w; "")));;
fnWochentag(n: Number): Text = Switch(n; 1; "Montag"; 2; "Dienstag"; 3; "Mittwoch"; 4; "Donnerstag"; 5; "Freitag"; 6; "Samstag"; 7; "Sonntag"; "?");;
fnZyklus(z: Number): Text = If(Coalesce(z; 1) <= 1; "jede Woche"; "alle " & z & " Wochen");;
fnMontag(d: Date): DateTime = DateAdd(d; 1 - Weekday(d; StartOfWeek.Monday); TimeUnit.Days);;
fnPlanPasst(start: DateTime; bis: DateTime; wt: Number; zyklus: Number; d: Date): Boolean = With({t0: DateDiff(start; d; TimeUnit.Days); t: DateDiff(DateAdd(start; 1 - Weekday(start; StartOfWeek.Monday); TimeUnit.Days); d; TimeUnit.Days)}; !IsBlank(start) && Weekday(d; StartOfWeek.Monday) = wt && t0 >= 0 && (IsBlank(bis) || DateDiff(d; bis; TimeUnit.Days) >= 0) && Mod(RoundDown(t / 7; 0); Max(1; zyklus)) = 0);;
```

```diff
- … ime; wt: Number; zyklus: Number; d: Date): Boolean = With({t: DateDiff(start; d; TimeUnit.Days)}; !IsBlank(start) && Weekday(d; StartOfWeek.Monday) = wt && t >= 0 && (IsBlank(bis) …
+ … ime; wt: Number; zyklus: Number; d: Date): Boolean = With({t0: DateDiff(start; d; TimeUnit.Days); t: DateDiff(DateAdd(start; 1 - Weekday(start; StartOfWeek.Monday); TimeUnit.Days); …
```

**Kurz erklärt:** **A14:** `fnPlanPasst` wie in Rundgang DEV (Wochen ab Montag der Startwoche, fällig erst ab Startdatum). Der Plan-Bildschirm setzt bei neuen Terminen schon einen Montag; Altdaten können aber einen anderen Tag haben.

**Nachprüfen:** endet auf `(d; bis; TimeUnit.Days) >= 0) && Mod(RoundDown(t / 7; 0); Max(1; zyklus)) = 0);;`

### B2.2 · `btnEdAktivieren.BorderThickness`

**Pfad:** `scrEditor › conEdKopf › btnEdAktivieren` → BorderThickness

```
0
```

```diff
-1
+0
```

**Kurz erklärt:** Kein Rahmen.

**Nachprüfen:** endet auf `0`

### B2.3 · `btnEdAktivieren.Color`

**Pfad:** `scrEditor › conEdKopf › btnEdAktivieren` → Color

```
Color.White
```

```diff
-If(CountRows(Filter(galPr.AllItems; Art = "Fehler")) > 0; clrTextGrau; clrPrimaer)
+Color.White
```

**Kurz erklärt:** Weiße Schrift.

**Nachprüfen:** endet auf `Color.White`

### B2.4 · `btnEdAktivieren.DisplayMode`

**Pfad:** `scrEditor › conEdKopf › btnEdAktivieren` → DisplayMode

```
If(varIsLoading || CountRows(Filter(galPr.AllItems; Art = "Fehler")) > 0; DisplayMode.Disabled; DisplayMode.Edit)
```

```diff
-If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
+If(varIsLoading || CountRows(Filter(galPr.AllItems; Art = "Fehler")) > 0; DisplayMode.Disabled; DisplayMode.Edit)
```

**Kurz erklärt:** Bei Fehlern **gesperrt** (grau, Farben aus `DisabledFill`/`DisabledColor`). Der Hinweis „Erst die Fehler beheben“ entfällt dadurch; die Fehlerzahl steht links daneben.

**Nachprüfen:** endet auf `er(galPr.AllItems; Art = "Fehler")) > 0; DisplayMode.Disabled; DisplayMode.Edit)`

### B2.5 · `btnEdAktivieren.Fill`

**Pfad:** `scrEditor › conEdKopf › btnEdAktivieren` → Fill

```
clrErfolg
```

```diff
-If(CountRows(Filter(galPr.AllItems; Art = "Fehler")) > 0; clrGesperrtHell; clrKarte)
+clrErfolg
```

**Kurz erklärt:** Grün, wenn aktivierbar.

**Nachprüfen:** endet auf `clrErfolg`

### B2.6 · `btnEdAktivieren.HoverColor`

**Pfad:** `scrEditor › conEdKopf › btnEdAktivieren` → HoverColor

```
Color.White
```

```diff
-clrPrimaer
+Color.White
```

**Kurz erklärt:** Weiß.

**Nachprüfen:** endet auf `Color.White`

### B2.7 · `btnEdAktivieren.HoverFill`

**Pfad:** `scrEditor › conEdKopf › btnEdAktivieren` → HoverFill

```
ColorFade(clrErfolg; -20%)
```

```diff
-clrPrimaerHell
+ColorFade(clrErfolg; -20%)
```

**Kurz erklärt:** Dunkleres Grün beim Darüberfahren.

**Nachprüfen:** endet auf `ColorFade(clrErfolg; -20%)`

### B2.8 · `btnEdAktivieren.PressedColor`

**Pfad:** `scrEditor › conEdKopf › btnEdAktivieren` → PressedColor

```
Color.White
```

```diff
-clrPrimaer
+Color.White
```

**Kurz erklärt:** Weiß.

**Nachprüfen:** endet auf `Color.White`

### B2.9 · `btnEdAktivieren.PressedFill`

**Pfad:** `scrEditor › conEdKopf › btnEdAktivieren` → PressedFill

```
ColorFade(clrErfolg; -35%)
```

```diff
-clrPrimaerHell
+ColorFade(clrErfolg; -35%)
```

**Kurz erklärt:** Noch dunkler beim Drücken.

**Nachprüfen:** endet auf `ColorFade(clrErfolg; -35%)`

### B2.10 · `btnPTyp.OnSelect`

**Pfad:** `scrEditor › conEdMitte › conEdP › galPTyp › btnPTyp` → OnSelect

```
If(ThisItem.W <> LookUp(colP; ID = varAuswahlID).Eingabetyp.Value;
    If(varSchreibbar && varAuswahlEbene = 3;
        Refresh(RG_Rundgaenge);;
        Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
        If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
        If(varEntwurfOk;
            Set(varPatchFehler; false);;
            IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {Eingabetyp: {Value: ThisItem.W}; VergleichPunkt: If(ThisItem.W = "ZAHL"; Coalesce(LookUp(colP; ID = varAuswahlID).VergleichPunkt; 0); 0)}); Set(varPatchFehler; true));;
            If(varPatchFehler;
                Notify("Nicht gespeichert. Bitte erneut versuchen."; NotificationType.Error);
                Patch(colP; LookUp(colP; ID = varAuswahlID); LookUp(RG_Pruefpunkte; ID = varAuswahlID));;
                Set(varGespeichertText; "Gespeichert " & Text(Now(); "hh:mm:ss"))
            )
        )
    )
)
```

```diff
-            IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {Eingabetyp: {Value: ThisItem.W}}); Set(varPatchFehler; true));;
+ … D && Fassung = varFassung); {Eingabetyp: {Value: ThisItem.W}; VergleichPunkt: If(ThisItem.W = "ZAHL"; Coalesce(LookUp(colP; ID = varAuswahlID).VergleichPunkt; 0); 0)}); Set(varPatc …
```

**Kurz erklärt:** **A12.** Beim Wechsel des Eingabetyps weg von „Zahl“ wird der Vergleich (`VergleichPunkt`) auf 0 gesetzt. Damit sperrt kein unsichtbarer Vergleich mehr das Aktivieren.

**Nachprüfen:** endet auf `)`

### B2.11 · `ddPKategorie.Default`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPKategorie` → Default

```
With({k: LookUp(colK; ID = LookUp(colP; ID = varAuswahlID).KategorieID)}; k.Title & If(CountRows(Filter(colK As x; x.Title = k.Title)) > 1; " · " & LookUp(colB As b0; b0.ID = k.BereichID).Title & If(CountRows(Filter(colK As x; x.Title = k.Title && x.BereichID = k.BereichID)) > 1; " #" & k.ID; ""); ""))
```

```diff
-With({k: LookUp(colK; ID = LookUp(colP; ID = varAuswahlID).KategorieID)}; LookUp(colB As b0; b0.ID = k.BereichID).Title & " › " & k.Title & If(CountRows(Filter(colK As x; x.Title = k.Title)) > 1; " (#" & k.ID & ")"; ""))
+ … p(colK; ID = LookUp(colP; ID = varAuswahlID).KategorieID)}; k.Title & If(CountRows(Filter(colK As x; x.Title = k.Title)) > 1; " · " & LookUp(colB As b0; b0.ID = k.BereichID).Title …
```

**Kurz erklärt:** Gleiche Anzeige wie die Liste (muss zur Liste passen).

**Nachprüfen:** endet auf ` x; x.Title = k.Title && x.BereichID = k.BereichID)) > 1; " #" & k.ID; ""); ""))`

### B2.12 · `ddPKategorie.Items`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPKategorie` → Items

```
Sort(ForAll(colK As k; With({b: LookUp(colB As b0; b0.ID = k.BereichID)}; {ID: k.ID; N: k.Title & If(CountRows(Filter(colK As x; x.Title = k.Title)) > 1; " · " & LookUp(colB As b0; b0.ID = k.BereichID).Title & If(CountRows(Filter(colK As x; x.Title = k.Title && x.BereichID = k.BereichID)) > 1; " #" & k.ID; ""); ""); S: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000")})); S)
```

```diff
- … {b: LookUp(colB As b0; b0.ID = k.BereichID)}; {ID: k.ID; N: LookUp(colB As b0; b0.ID = k.BereichID).Title & " › " & k.Title & If(CountRows(Filter(colK As x; x.Title = k.Title)) > 1 …
+ … {b: LookUp(colB As b0; b0.ID = k.BereichID)}; {ID: k.ID; N: k.Title & If(CountRows(Filter(colK As x; x.Title = k.Title)) > 1; " · " & LookUp(colB As b0; b0.ID = k.BereichID).Title …
```

**Kurz erklärt:** Nur noch der **Kategoriename**. Der Bereich steht nur dabei, wenn es den Namen mehrmals gibt („Name · Bereich“), bei Doppelten im selben Bereich zusätzlich „#ID“.

**Nachprüfen:** endet auf `(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000")})); S)`

### B2.13 · `ddPKategorie.Size`

**Pfad:** `scrEditor › conEdMitte › conEdP › conPRest › ddPKategorie` → Size

```
13
```

```diff
-14
+13
```

**Kurz erklärt:** Schrift 13 statt 14, damit längere Namen passen.

**Nachprüfen:** endet auf `13`

### B2.14 · `galPr.Items`

**Pfad:** `scrEditor › conEdRechts › galPr` → Items

```
Sort(
    Filter(
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
                {T: ForAll(Filter(ForAll(Filter(colP As p0; Coalesce(p0.BedingungPunkt; 0) <> 0) As p; With({a: LookUp(colP As a0; a0.ID = p.BedingungPunkt)}; {ID: p.ID; KategorieID: p.KategorieID; Title: p.Title; G: If(IsBlank(a) || a.KategorieID <> p.KategorieID; "Die Bedingung zeigt auf eine Frage außerhalb dieser Kategorie."; Coalesce(a.BedingungPunkt; 0) <> 0; "Die Frage der Bedingung hat selbst eine Bedingung (nur eine Ebene erlaubt)."; a.RgReihenfolge * 1000000 + a.ID > p.RgReihenfolge * 1000000 + p.ID; "Die Frage der Bedingung muss weiter oben stehen."; !fnBedGueltig(p.BedingungWert; a.Eingabetyp.Value; a.Auswahlwerte); "Der Wert der Bedingung passt nicht zu „" & a.Title & "“."; a.Eingabetyp.Value = "ZAHL" && fnBedNorm(p.BedingungWert) = "nio" && (fnGrenzmodus(a.Grenzmodus.Value) <> "Mangel" || (IsBlank(a.MinWert) && IsBlank(a.MaxWert))); "Bedingung „n.i.O.“: „" & a.Title & "“ wird nie n.i.O. (keine Grenzen ab/bis oder „Außerhalb“ ist nicht „Mangel“). Die Frage erschiene nie."; "")})); G <> "") As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: " & p.G})};
                {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && fnGrenzmodus(p.Grenzmodus.Value) <> "Mangel" && IsBlank(p.MinWert) && IsBlank(p.MaxWert)) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: „Außerhalb“ wirkt nur mit Grenzen (ab/bis)."})};
                {T: ForAll(Filter(colP As p; p.Foto.Value = "Bei Mangel Pflicht" && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: „Foto Pflicht bei Mangel“ wirkt nur bei i.O./n.i.O. und Zahl."})};
                {T: ForAll(Filter(colP As p; CountRows(Filter(colP As q; q.KategorieID = p.KategorieID && Lower(Trim(q.Title)) = Lower(Trim(p.Title)))) > 1) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“ steht in der Kategorie doppelt."})};
                {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Abschnitt; "")) <> "" && With({v: First(Sort(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 1000000 + q.ID < p.RgReihenfolge * 1000000 + p.ID); RgReihenfolge * 1000000 + ID; SortOrder.Descending))}; !IsBlank(v) && Lower(Trim(Coalesce(v.Abschnitt; ""))) <> Lower(Trim(p.Abschnitt))) && CountRows(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 1000000 + q.ID < p.RgReihenfolge * 1000000 + p.ID && Lower(Trim(Coalesce(q.Abschnitt; ""))) = Lower(Trim(p.Abschnitt)))) > 0) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Abschnitt „" & Trim(p.Abschnitt) & "“ ist unterbrochen: Die Fragen stehen nicht zusammen (bei „" & p.Title & "“). Mit ↑ ↓ zusammenschieben."})};
                {T: ForAll(Filter(colP As p; (Coalesce(p.Kritisch; false) || Coalesce(p.Rueckfrage; false)) && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Rückfrage und „kritisch“ wirken nur bei i.O./n.i.O. und Zahl."})};
                {T: ForAll(Filter(colP As p; Coalesce(p.Kritisch; false) && Trim(Coalesce(p.Ansprechpartner; "")) = "") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“ ist kritisch, aber ohne eigenen Ansprechpartner (es erscheinen nur die allgemeinen)."})};
                {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "IONIO" && (Trim(Coalesce(p.TextIO; "")) <> "" || Trim(Coalesce(p.TextNIO; "")) <> "")) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: eigene Knopf-Beschriftungen wirken nur bei i.O./n.i.O."})};
                {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && Coalesce(p.VergleichPunkt; 0) <> 0 && With({w: LookUp(colP As w0; w0.ID = p.VergleichPunkt)}; IsBlank(w) || w.ID = p.ID || w.KategorieID <> p.KategorieID || w.Eingabetyp.Value <> "ZAHL")) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Der Vergleich zeigt auf keine Zahl-Frage derselben Kategorie."})};
                {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend; false) || Coalesce(p.VergleichPunkt; 0) <> 0)) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Verlauf/Vergleich wirkt nur bei Zahlen (wird ignoriert)."})};
                {T: ForAll(Filter(colP As p; !IsBlank(p.AbwMax) && p.AbwMax < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: höchste Abweichung darf nicht negativ sein."})};
                {T: ForAll(Filter(colP As p; !IsBlank(p.VergleichTol) && p.VergleichTol < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: erlaubter Unterschied darf nicht negativ sein."})};
                {T: ForAll(Filter(colP As p; Coalesce(p.AnleitungID; 0) > 0 && IsBlank(LookUp(colAnlAktiv As n0; n0.ID = p.AnleitungID))) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: Die gewählte Anleitung gibt es nicht mehr oder sie ist inaktiv."})};
                {T: ForAll(Filter(colP As p; p.Title = "Neue Frage") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Eine Frage heißt noch „Neue Frage“."})};
                {T: ForAll(Filter(colK As k; CountRows(Filter(colP As p; p.KategorieID = k.ID)) > 30) As k; {Art: "Hinweis"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat über 30 Prüfpunkte (lange Seite für den Prüfer)."})};
                {T: Filter(Table({Art: "Hinweis"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Kein aktiver Plan: Der Rundgang erscheint nie auf der Startseite. → In der Übersicht „Plan“ tippen."}); !varIstVorlage && IsEmpty(Filter(colPlanR; Coalesce(Aktiv; false))))}
            );
            T
        );
        (Art = "Fehler" || Art = "Hinweis") && Trim(Coalesce(Text; "")) <> ""
    );
    If(Art = "Fehler"; 0; 1)
)
```

```diff
-    Ungroup(
-        Table(
-            {T: Filter(Table({Art: "Fehler"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Der Rundgang hat noch keinen Bereich. → „+ Bereich“"}); IsEmpty(colB))};
-            {T: ForAll(Filter(colB As b; IsEmpty(Filter(colK As k; k.BereichID = b.ID))) As b; {Art: "Fehler"; Ebene: 1; ID: b.ID; KatID: 0; BerID: b.ID; Text: "Bereich „" & b.Title & "“ hat keine Kategorie."})};
-            {T: ForAll(Filter(colK As k; IsEmpty(Filter(colP As p; p.KategorieID = k.ID))) As k; {Art: "Fehler"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat keinen Prüfpunkt."})};
-            {T: ForAll(Filter(colB As b; Trim(Coalesce(b.Title; "")) = "") As b; {Art: "Fehler"; Ebene: 1; ID: b.ID; KatID: 0; BerID: b.ID; Text: "Ein Bereich hat keinen Namen."})};
-            {T: ForAll(Filter(colK As k; Trim(Coalesce(k.Title; "")) = "") As k; {Art: "Fehler"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Eine Kategorie hat keinen Namen."})};
- {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Title; "")) = "") As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.Kateg …
- {T: ForAll(Filter(colP As p; (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerte(p.Auswahlwerte) < 2) As p; {Art: "Fehler"; Ebene: 3; ID: p.I …
- {T: ForAll(Filter(colP As p; (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerteDoppelt(p.Auswahlwerte)) As p; {Art: "Fehler"; Ebene: 3; ID: …
- {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && !IsBlank(p.MinWert) && !IsBlank(p.MaxWert) && p.MinWert > p.MaxWert) As p; {Art: "Fehler"; Ebene: 3; ID: p.I …
- {T: ForAll(Filter(ForAll(Filter(colP As p0; Coalesce(p0.BedingungPunkt; 0) <> 0) As p; With({a: LookUp(colP As a0; a0.ID = p.BedingungPunkt)}; {ID: p.ID; KategorieID: p …
- {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && fnGrenzmodus(p.Grenzmodus.Value) <> "Mangel" && IsBlank(p.MinWert) && IsBlank(p.MaxWert)) As p; {Art: "Hinwe …
- {T: ForAll(Filter(colP As p; p.Foto.Value = "Bei Mangel Pflicht" && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; ID: …
- {T: ForAll(Filter(colP As p; CountRows(Filter(colP As q; q.KategorieID = p.KategorieID && Lower(Trim(q.Title)) = Lower(Trim(p.Title)))) > 1) As p; {Art: "Hinweis"; Eben …
- {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Abschnitt; "")) <> "" && With({v: First(Sort(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 1000000 + …
- {T: ForAll(Filter(colP As p; (Coalesce(p.Kritisch; false) || Coalesce(p.Rueckfrage; false)) && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art …
- {T: ForAll(Filter(colP As p; Coalesce(p.Kritisch; false) && Trim(Coalesce(p.Ansprechpartner; "")) = "") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; …
- {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "IONIO" && (Trim(Coalesce(p.TextIO; "")) <> "" || Trim(Coalesce(p.TextNIO; "")) <> "")) As p; {Art: "Hinweis"; Ebene: …
- {T: ForAll(Filter(colP As p; Coalesce(p.VergleichPunkt; 0) <> 0 && With({w: LookUp(colP As w0; w0.ID = p.VergleichPunkt)}; IsBlank(w) || w.ID = p.ID || w.KategorieID <> …
- {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend; false))) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p …
- {T: ForAll(Filter(colP As p; !IsBlank(p.AbwMax) && p.AbwMax < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.Kat …
- {T: ForAll(Filter(colP As p; !IsBlank(p.VergleichTol) && p.VergleichTol < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k …
- {T: ForAll(Filter(colP As p; Coalesce(p.AnleitungID; 0) > 0 && IsBlank(LookUp(colAnlAktiv As n0; n0.ID = p.AnleitungID))) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; Kat …
-            {T: ForAll(Filter(colP As p; p.Title = "Neue Frage") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "Eine Frage heißt noch „Neue Frage“."})};
- {T: ForAll(Filter(colK As k; CountRows(Filter(colP As p; p.KategorieID = k.ID)) > 30) As k; {Art: "Hinweis"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: …
- {T: Filter(Table({Art: "Hinweis"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Kein aktiver Plan: Der Rundgang erscheint nie auf der Startseite. → In der Übersicht „Plan …
+    Filter(
+        Ungroup(
+            Table(
+                {T: Filter(Table({Art: "Fehler"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Der Rundgang hat noch keinen Bereich. → „+ Bereich“"}); IsEmpty(colB))};
+                {T: ForAll(Filter(colB As b; IsEmpty(Filter(colK As k; k.BereichID = b.ID))) As b; {Art: "Fehler"; Ebene: 1; ID: b.ID; KatID: 0; BerID: b.ID; Text: "Bereich „" & b.Title & "“ hat keine Kategorie."})};
+                {T: ForAll(Filter(colK As k; IsEmpty(Filter(colP As p; p.KategorieID = k.ID))) As k; {Art: "Fehler"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Kategorie „" & k.Title & "“ hat keinen Prüfpunkt."})};
+                {T: ForAll(Filter(colB As b; Trim(Coalesce(b.Title; "")) = "") As b; {Art: "Fehler"; Ebene: 1; ID: b.ID; KatID: 0; BerID: b.ID; Text: "Ein Bereich hat keinen Namen."})};
+                {T: ForAll(Filter(colK As k; Trim(Coalesce(k.Title; "")) = "") As k; {Art: "Fehler"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Text: "Eine Kategorie hat keinen Namen."})};
+ {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Title; "")) = "") As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.K …
+ {T: ForAll(Filter(colP As p; (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerte(p.Auswahlwerte) < 2) As p; {Art: "Fehler"; Ebene: 3; ID: …
+ {T: ForAll(Filter(colP As p; (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerteDoppelt(p.Auswahlwerte)) As p; {Art: "Fehler"; Ebene: 3; …
+ {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && !IsBlank(p.MinWert) && !IsBlank(p.MaxWert) && p.MinWert > p.MaxWert) As p; {Art: "Fehler"; Ebene: 3; ID: …
+ {T: ForAll(Filter(ForAll(Filter(colP As p0; Coalesce(p0.BedingungPunkt; 0) <> 0) As p; With({a: LookUp(colP As a0; a0.ID = p.BedingungPunkt)}; {ID: p.ID; KategorieI …
+ {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && fnGrenzmodus(p.Grenzmodus.Value) <> "Mangel" && IsBlank(p.MinWert) && IsBlank(p.MaxWert)) As p; {Art: "H …
+ {T: ForAll(Filter(colP As p; p.Foto.Value = "Bei Mangel Pflicht" && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; {Art: "Hinweis"; Ebene: 3; …
+ {T: ForAll(Filter(colP As p; CountRows(Filter(colP As q; q.KategorieID = p.KategorieID && Lower(Trim(q.Title)) = Lower(Trim(p.Title)))) > 1) As p; {Art: "Hinweis"; …
+ {T: ForAll(Filter(colP As p; Trim(Coalesce(p.Abschnitt; "")) <> "" && With({v: First(Sort(Filter(colP As q; q.KategorieID = p.KategorieID && q.RgReihenfolge * 10000 …
+ {T: ForAll(Filter(colP As p; (Coalesce(p.Kritisch; false) || Coalesce(p.Rueckfrage; false)) && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p; …
+ {T: ForAll(Filter(colP As p; Coalesce(p.Kritisch; false) && Trim(Coalesce(p.Ansprechpartner; "")) = "") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.Kategori …
+ {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "IONIO" && (Trim(Coalesce(p.TextIO; "")) <> "" || Trim(Coalesce(p.TextNIO; "")) <> "")) As p; {Art: "Hinweis"; Eb …
+ {T: ForAll(Filter(colP As p; p.Eingabetyp.Value = "ZAHL" && Coalesce(p.VergleichPunkt; 0) <> 0 && With({w: LookUp(colP As w0; w0.ID = p.VergleichPunkt)}; IsBlank(w) …
+ {T: ForAll(Filter(colP As p; p.Eingabetyp.Value <> "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend; false) || Coalesce(p.VergleichPunkt; 0) <> 0)) As p; {Ar …
+ {T: ForAll(Filter(colP As p; !IsBlank(p.AbwMax) && p.AbwMax < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p …
+ {T: ForAll(Filter(colP As p; !IsBlank(p.VergleichTol) && p.VergleichTol < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k …
+ {T: ForAll(Filter(colP As p; Coalesce(p.AnleitungID; 0) > 0 && IsBlank(LookUp(colAnlAktiv As n0; n0.ID = p.AnleitungID))) As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; …
+ {T: ForAll(Filter(colP As p; p.Title = "Neue Frage") As p; {Art: "Hinweis"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieI …
+ {T: ForAll(Filter(colK As k; CountRows(Filter(colP As p; p.KategorieID = k.ID)) > 30) As k; {Art: "Hinweis"; Ebene: 2; ID: k.ID; KatID: k.ID; BerID: k.BereichID; Te …
+ {T: Filter(Table({Art: "Hinweis"; Ebene: 0; ID: 0; KatID: 0; BerID: 0; Text: "Kein aktiver Plan: Der Rundgang erscheint nie auf der Startseite. → In der Übersicht „ …
+            );
+            T
-        T
+        (Art = "Fehler" || Art = "Hinweis") && Trim(Coalesce(Text; "")) <> ""
```

**Kurz erklärt:** **Leere orange Punkte:** `Ungroup` liefert für jede Regel ohne Treffer eine **leere Zeile** (Art leer → Farbe Orange, Text leer). Jetzt werden nur Zeilen mit Art „Fehler“/„Hinweis“ und Text gezeigt. **A12:** Der Vergleich wird nur bei Zahl-Fragen geprüft; steht er an einer anderen Frage, kommt nur ein Hinweis. **A13:** Neuer Fehler, wenn eine Bedingung „n.i.O.“ auf eine Zahl-Frage zeigt, die nie n.i.O. werden kann (keine Grenzen ab/bis oder „Außerhalb“ = Hinweis/nicht speicherbar).

**Nachprüfen:** endet auf `)`

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | Testdaten: im Testrundgang bei einer Kategorie alle Prüfpunkte in SharePoint auf Aktiv = Nein; DEV: Lauf starten | diese Kategorie fehlt in der Liste, der Lauf lässt sich abschließen (A3) |
| T2 | DEV: Startseite → Rundgang starten | Kategorien wie bisher, nur aus diesem Rundgang (A10) |
| T3 | DEV: freiwillige Frage mit „Foto Pflicht“ leer lassen, Kategorie speichern | speichert ohne Foto (A5) |
| T4 | DEV: dieselbe Frage beantworten, kein Foto | „Foto“ fehlt, Speichern gesperrt (A5) |
| T5 | Builder: Prüfpunkt n.i.O. beantworten lassen, dann im Builder inaktiv; im laufenden Lauf Kategorie speichern | AnzahlNIO zählt ihn nicht, kein Mangel (A9) |
| T6 | Builder: Zahl-Frage mit Vergleich → Typ auf i.O./n.i.O. | Vergleich leer, Prüfliste ohne Fehler, Aktivieren grün (A12) |
| T7 | Builder: Bedingung „n.i.O.“ auf eine Zahl ohne Grenzen | roter Fehler „… wird nie n.i.O. …“, Aktivieren grau; Grenze „bis“ eintragen → Fehler weg (A13) |
| T8 | Plan: Start Mi, alle 2 Wochen Mo | erster Termin ist der Montag 12 Tage nach dem Start (Woche 2 ab Montag der Startwoche), nicht der Montag davor (A14) |
| T9 | Builder: Rundgang ohne Fehler und Hinweise | „Prüfung: keine Fehler“, darunter „Alles in Ordnung ✓“, **keine** orangen Punkte |
| T10 | Builder: „Aktivieren …“ mit/ohne Fehler, Maus darüber, drücken | ohne Fehler grün/weiß, dunkler bei Maus/Druck; mit Fehler grau, nicht klickbar |
| T11 | Builder: Prüfpunkt → „Gehört zur Kategorie“ | nur Kategoriename; bei gleichem Namen in zwei Bereichen „Name · Bereich“ |

## Rückweg

Vorher-Fassungen aus dem Anhang einsetzen. Für `btnRgAktion.OnSelect` die Vorher-Fassung aus dem Anhang nehmen (nicht den Export-Stand, der ist falsch).

## Anhang – Vorher-Fassungen

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

**Rundgang DEV `App.Formulas` vorher**

```
clrPrimaer = ColorValue("#171496");;
clrPrimaerHell = ColorValue("#E8E8F7");;
clrHintergrund = ColorValue("#F4F5F9");;
clrKarte = Color.White;;
clrRahmen = ColorValue("#DADCE5");;
clrText = ColorValue("#1B1B1F");;
clrTextGrau = ColorValue("#5F6370");;
clrErfolg = ColorValue("#0F7B3F");;
clrErfolgHell = ColorValue("#E3F4EA");;
clrFehler = ColorValue("#B3261E");;
clrFehlerHell = ColorValue("#FCE8E6");;
clrGesperrt = ColorValue("#9AA0A6");;
clrGesperrtHell = ColorValue("#EEF0F3");;
clrWarnung = ColorValue("#9A5B00");;
stInArbeit = "InArbeit";;
stAbschluss = "Abschluss";;
stAbgeschlossen = "Abgeschlossen";;
cfgNachholTage = Max(
    0;
    Coalesce(
        Value(
            LookUp(
                RG_Konfiguration;
                Title = "NachholTage"
            ).Wert
        );
        0
    )
);;
cfgTestmodus = Coalesce(
    LookUp(
        RG_Konfiguration;
        Title = "Testmodus"
    ).Wert;
    "Ja"
) <> "Nein";;
cfgTestadresse = Coalesce(
    LookUp(
        RG_Konfiguration;
        Title = "Testadresse"
    ).Wert;
    ""
);;
cfgEmpfaenger = Coalesce(
    LookUp(
        RG_Konfiguration;
        Title = "Empfaenger"
    ).Wert;
    ""
);;
fnTagAnzeige(d: Date): Text = Text(
    d;
    "dddd, dd.mm.yyyy";
    "de-DE"
) & " · KW " & ISOWeekNum(d);;
fnTagLabel(d: Date; heute: Date): Text = Switch(
    DateDiff(
        d;
        heute;
        TimeUnit.Days
    );
    0;
    "Heute – ";
    1;
    "Gestern – ";
    ""
) & fnTagAnzeige(d);;
fnPlanPasst(start: DateTime; bis: DateTime; wt: Number; zyklus: Number; d: Date): Boolean = With(
    {
        t: DateDiff(
            start;
            d;
            TimeUnit.Days
        )
    };
    !IsBlank(start) && Weekday(
        d;
        StartOfWeek.Monday
    ) = wt && t >= 0 && (IsBlank(bis) || DateDiff(
        d;
        bis;
        TimeUnit.Days
    ) >= 0) && Mod(
        RoundDown(
            t / 7;
            0
        );
        Max(
            1;
            zyklus
        )
    ) = 0
);;
fnZahlBewertung(z: Number; mi: Number; ma: Number; gmodus: Text): Text = If(
    fnAusserhalb(z; mi; ma);
    Switch(If(gmodus = "Sperren" && !fnSperreGilt(mi; ma); "Mangel"; gmodus); "Warnen"; "IO"; "Sperren"; ""; "NIO");
    "IO"
);;
fnGrenzmodus(g: Text): Text = If(g = "Warnen" || g = "Sperren"; g; "Mangel");;
fnSperreGilt(mi: Number; ma: Number): Boolean = IsBlank(mi) || IsBlank(ma) || mi <= ma;;
fnHtml(t: Text): Text = Substitute(Substitute(Substitute(Substitute(Substitute(t; "&"; "&amp;"); "<"; "&lt;"); ">"; "&gt;"); """"; "&quot;"); "'"; "&#39;");;
cfgAdmins = Coalesce(LookUp(RG_Konfiguration; Title = "Admins").Wert; "");;
fnLinkAnzahl(t: Text): Number = CountRows(Filter(Split(Coalesce(t; ""); " | ") As s; Trim(s.Value) <> ""));;
fnFotoModus(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht"; f; f = "Bei Mangel Pflicht"; "BeiMangel"; alt; "Optional"; "Aus");;
fnFotoNeuErlaubt(bew: Text; foto: Text): Boolean = bew = "NIO" || foto = "Optional" || foto = "Pflicht";;
fnBeantwortet(bew: Text; wt: Text; wz: Number): Boolean = bew <> "" || Trim(wt) <> "" || !IsBlank(wz);;
fnAusserhalb(z: Number; mi: Number; ma: Number): Boolean = !IsBlank(z) && ((!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma));;
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (typ = "ZAHL" && wt = "nicht messbar") || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz; mi; ma));;
fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz) && wt = "") || (typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATUMZEIT") && wt = "")); "Wert";
    typ = "DATUMZEIT" && wt <> "" && (Len(wt) < 16 || "-" in wt); "Uhrzeit";
    typ = "ZAHL" && gmodus = "Sperren" && fnSperreGilt(mi; ma) && fnAusserhalb(wz; mi; ma); "Bereich";
    fnKommentarNoetig(typ; bew; wt; wz; kpfl; gmodus; mi; ma) && Trim(kom) = ""; "Kommentar";
    (foto = "Pflicht" || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1; "Foto";
    kritoffen && bew = "NIO"; "Kritisch";
    ""
);;
fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w; "")); "."; ""); " "; ""));;
fnBedGueltig(w: Text; typ: Text; auswahl: Text): Boolean = With({n: fnBedNorm(w)}; n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnBedPasst(w: Text; bew: Text; wt: Text; wz: Number): Boolean = With({n: fnBedNorm(w)}; If(n = "*"; fnBeantwortet(bew; wt; wz); n = fnBedNorm(bew) || n = fnBedNorm(wt) || CountRows(Filter(Split(wt; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnSichtbar(bid: Number; w: Text; gef: Boolean; bBid: Number; bInaktiv: Boolean; bTyp: Text; bAuswahl: Text; bBew: Text; bWt: Text; bWz: Number): Boolean = bid = 0 || Trim(w) = "" || !gef || bInaktiv || bBid <> 0 || !fnBedGueltig(w; bTyp; bAuswahl) || fnBedPasst(w; bBew; bWt; bWz);;
fnDatumText(d: Date; h: Text; m: Text; mitZeit: Boolean): Text = If(IsBlank(d); ""; Text(d; "dd.mm.yyyy") & If(mitZeit && (h <> "" || m <> ""); " " & If(h = ""; "--"; h) & ":" & If(m = ""; "--"; m); ""));;
fnAbweichung(z: Number; l: Number; mx: Number; proz: Boolean; steig: Boolean): Boolean = !IsBlank(z) && !IsBlank(l) && ((steig && z < l) || (!IsBlank(mx) && Round(Abs(z - l); 6) > Round(If(proz; Abs(l) * mx / 100; mx); 6)));;
fnVergleich(z: Number; w: Number; tol: Number): Boolean = !IsBlank(z) && !IsBlank(w) && Round(Abs(z - w); 6) > Round(Coalesce(tol; 0); 6);;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma; kritoffen) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

**Builder `App.Formulas` vorher**

```
clrPrimaer = ColorValue("#171496");;
clrPrimaerHell = ColorValue("#E8E8F7");;
clrHintergrund = ColorValue("#F4F5F9");;
clrKarte = Color.White;;
clrRahmen = ColorValue("#DADCE5");;
clrText = ColorValue("#1B1B1F");;
clrTextGrau = ColorValue("#5F6370");;
clrErfolg = ColorValue("#0F7B3F");;
clrErfolgHell = ColorValue("#E3F4EA");;
clrFehler = ColorValue("#B3261E");;
clrFehlerHell = ColorValue("#FCE8E6");;
clrWarnung = ColorValue("#9A5B00");;
clrWarnungHell = ColorValue("#FFF4E0");;
clrGesperrt = ColorValue("#9AA0A6");;
clrGesperrtHell = ColorValue("#EEF0F3");;
cfgBildBibliothek = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/RG_Hinweisbilder";;
fnStatus(s: Text; aktiv: Boolean): Text = If(s = "Vorlage"; "Vorlage"; aktiv; "Aktiv"; s = "Entwurf"; "Entwurf"; "Archiviert");;
fnAktiveFassung(f: Number): Number = If(Coalesce(f; 0) > 0; f; 1);;
fnTypName(t: Text): Text = Switch(t; "IONIO"; "i.O. / n.i.O."; "ZAHL"; "Zahl"; "AUSWAHL"; "Auswahl"; "MEHRFACH"; "Mehrfachauswahl"; "TEXT"; "Text"; "DATUM"; "Datum"; "DATUMZEIT"; "Datum + Uhrzeit"; t);;
fnTypKurz(t: Text): Text = Switch(t; "IONIO"; "i.O./n.i.O."; "ZAHL"; "Zahl"; "AUSWAHL"; "Auswahl"; "MEHRFACH"; "Mehrfach"; "TEXT"; "Text"; "DATUM"; "Datum"; "DATUMZEIT"; "Datum+Zeit"; t);;
fnFotoWert(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht" || f = "Bei Mangel Pflicht"; f; alt; "Optional"; "Aus");;
fnFotoText(f: Text): Text = Switch(f; "Optional"; "Foto freiwillig"; "Pflicht"; "Foto immer Pflicht"; "Bei Mangel Pflicht"; "Foto Pflicht bei Mangel"; "kein Foto (bei n.i.O. möglich)");;
fnGrenzmodus(g: Text): Text = If(g = "Warnen" || g = "Sperren"; g; "Mangel");;
fnGrenzText(mi: Number; ma: Number; einheit: Text): Text = If(IsBlank(mi) && IsBlank(ma); "keine Grenzen"; "i.O. " & If(IsBlank(mi); ""; "ab " & Text(mi)) & If(IsBlank(mi) || IsBlank(ma); ""; " ") & If(IsBlank(ma); ""; "bis " & Text(ma)) & If(Trim(Coalesce(einheit; "")) = ""; ""; " " & einheit));;
fnWerte(t: Text): Number = CountRows(Filter(Split(Coalesce(t; ""); ";") As s; Trim(s.Value) <> ""));;
fnWerteDoppelt(t: Text): Boolean = CountRows(Distinct(Filter(Split(Coalesce(t; ""); ";") As s; Trim(s.Value) <> ""); Lower(Trim(Value)))) < fnWerte(t);;
fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w; "")); "."; ""); " "; ""));;
fnBedGueltig(w: Text; typ: Text; auswahl: Text): Boolean = With({n: fnBedNorm(w)}; n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnBedText(w: Text): Text = Switch(fnBedNorm(w); "nio"; "n.i.O. (Mangel)"; "io"; "i.O."; "*"; "beantwortet"; Trim(Coalesce(w; "")));;
fnWochentag(n: Number): Text = Switch(n; 1; "Montag"; 2; "Dienstag"; 3; "Mittwoch"; 4; "Donnerstag"; 5; "Freitag"; 6; "Samstag"; 7; "Sonntag"; "?");;
fnZyklus(z: Number): Text = If(Coalesce(z; 1) <= 1; "jede Woche"; "alle " & z & " Wochen");;
fnMontag(d: Date): DateTime = DateAdd(d; 1 - Weekday(d; StartOfWeek.Monday); TimeUnit.Days);;
fnPlanPasst(start: DateTime; bis: DateTime; wt: Number; zyklus: Number; d: Date): Boolean = With({t: DateDiff(start; d; TimeUnit.Days)}; !IsBlank(start) && Weekday(d; StartOfWeek.Monday) = wt && t >= 0 && (IsBlank(bis) || DateDiff(d; bis; TimeUnit.Days) >= 0) && Mod(RoundDown(t / 7; 0); Max(1; zyklus)) = 0);;
```

**Builder `btnEdAktivieren.BorderThickness` vorher**

```
1
```

**Builder `btnEdAktivieren.Color` vorher**

```
If(CountRows(Filter(galPr.AllItems; Art = "Fehler")) > 0; clrTextGrau; clrPrimaer)
```

**Builder `btnEdAktivieren.DisplayMode` vorher**

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**Builder `btnEdAktivieren.Fill` vorher**

```
If(CountRows(Filter(galPr.AllItems; Art = "Fehler")) > 0; clrGesperrtHell; clrKarte)
```

**Builder `btnEdAktivieren.HoverColor` vorher**

```
clrPrimaer
```

**Builder `btnEdAktivieren.HoverFill` vorher**

```
clrPrimaerHell
```

**Builder `btnEdAktivieren.PressedColor` vorher**

```
clrPrimaer
```

**Builder `btnEdAktivieren.PressedFill` vorher**

```
clrPrimaerHell
```

**Builder `btnPTyp.OnSelect` vorher**

```
If(ThisItem.W <> LookUp(colP; ID = varAuswahlID).Eingabetyp.Value;
    If(varSchreibbar && varAuswahlEbene = 3;
        Refresh(RG_Rundgaenge);;
        Set(varEntwurfOk; varIstVorlage || Coalesce(LookUp(RG_Rundgaenge; ID = varRgID).EntwurfFassung; 0) = varFassung);;
        If(!varEntwurfOk; Set(varSchreibbar; false);; Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht."; NotificationType.Error));;
        If(varEntwurfOk;
            Set(varPatchFehler; false);;
            IfError(Patch(RG_Pruefpunkte; LookUp(RG_Pruefpunkte; ID = varAuswahlID && RundgangID = varRgID && Fassung = varFassung); {Eingabetyp: {Value: ThisItem.W}}); Set(varPatchFehler; true));;
            If(varPatchFehler;
                Notify("Nicht gespeichert. Bitte erneut versuchen."; NotificationType.Error);
                Patch(colP; LookUp(colP; ID = varAuswahlID); LookUp(RG_Pruefpunkte; ID = varAuswahlID));;
                Set(varGespeichertText; "Gespeichert " & Text(Now(); "hh:mm:ss"))
            )
        )
    )
)
```

**Builder `ddPKategorie.Default` vorher**

```
With({k: LookUp(colK; ID = LookUp(colP; ID = varAuswahlID).KategorieID)}; LookUp(colB As b0; b0.ID = k.BereichID).Title & " › " & k.Title & If(CountRows(Filter(colK As x; x.Title = k.Title)) > 1; " (#" & k.ID & ")"; ""))
```

**Builder `ddPKategorie.Items` vorher**

```
Sort(ForAll(colK As k; With({b: LookUp(colB As b0; b0.ID = k.BereichID)}; {ID: k.ID; N: LookUp(colB As b0; b0.ID = k.BereichID).Title & " › " & k.Title & If(CountRows(Filter(colK As x; x.Title = k.Title)) > 1; " (#" & k.ID & ")"; ""); S: Text(b.RgReihenfolge; "000000") & Text(b.ID; "000000") & Text(k.RgReihenfolge; "000000") & Text(k.ID; "000000")})); S)
```

**Builder `ddPKategorie.Size` vorher**

```
14
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
            {T: ForAll(Filter(colP As p; !IsBlank(p.VergleichTol) && p.VergleichTol < 0) As p; {Art: "Fehler"; Ebene: 3; ID: p.ID; KatID: p.KategorieID; BerID: LookUp(colK As k9; k9.ID = p.KategorieID).BereichID; Text: "„" & p.Title & "“: erlaubter Unterschied darf nicht negativ sein."})};
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

