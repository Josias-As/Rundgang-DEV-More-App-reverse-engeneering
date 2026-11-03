# Paket 14+15 – Rundgang-App: Abweichung zum letzten Rundgang, zwei Werte vergleichen

Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket14) und `werkzeuge/doc_paket14_15.py`. **Voraussetzung: Paket N, 8–10 und 12+16 eingefügt.**

## Kurzfassung

- **Paket 14 – Abweichung zum letzten Rundgang:** Bei einer Zahl lässt sich im Builder einstellen, wie stark sie vom letzten abgeschlossenen Rundgang abweichen darf (absolut oder in %), und/oder „Zählerstand: darf nicht kleiner werden“. Die Karte zeigt „zuletzt 7,6 (26.10.)“. Weicht der Wert stärker ab, wird die Zeile orange und eine **Begründung ist Pflicht**. Kein Mangel. Der erste Rundgang hat keinen Vergleich. Testläufe vergleichen nur mit Testläufen.
- **Paket 15 – zwei Werte vergleichen:** Eine Zahl kann mit einer anderen Zahl derselben Kategorie verglichen werden (z. B. zwei gleiche Geräte) mit erlaubtem Unterschied (0 = gleich). Weichen sie stärker ab, ist ebenfalls eine Begründung Pflicht.
- Protokoll: „(starke Abweichung zum letzten Mal, zuletzt 7,6, begründet)“ bzw. „(weicht von „…“ ab (7,2), begründet)“.
- Nach einer neuen Fassung findet die App den alten Wert über `QuelleID` (eine Fassung zurück). Lagen zwei Aktivierungen zwischen zwei Rundgängen, fehlt der Vergleich einmal.
- Umfang: 5 Spalten, 9 Properties (jede einmal), kein neues Steuerelement. Generator 0 Fehler, Mutation, Logik 103 Szenarien. **Nicht in Studio getestet. Nicht unabhängig geprüft.**

## Schritt 1 – SharePoint

`RG_Pruefpunkte`: `AbwMax` (Zahl, leer), `AbwProzent` (Ja/Nein, Nein), `NurSteigend` (Ja/Nein, Nein), `VergleichPunkt` (Zahl, 0), `VergleichTol` (Zahl, 0). Danach in der Rundgang-App: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**. (`QuelleID` gibt es schon, vom Builder.)

## Schritt 2 – Formeln und Laden

### 2.1 · `App.Formulas`

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
    typ = "DATUMZEIT" && wt <> "" && Len(wt) < 16; "Uhrzeit";
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
fnDatumText(d: Date; h: Text; m: Text; mitZeit: Boolean): Text = If(IsBlank(d); ""; Text(d; "dd.mm.yyyy") & If(mitZeit && h <> "" && m <> ""; " " & h & ":" & m; ""));;
fnAbweichung(z: Number; l: Number; mx: Number; proz: Boolean; steig: Boolean): Boolean = !IsBlank(z) && !IsBlank(l) && ((steig && z < l) || (!IsBlank(mx) && Abs(z - l) > If(proz; Abs(l) * mx / 100; mx)));;
fnVergleich(z: Number; w: Number; tol: Number): Boolean = !IsBlank(z) && !IsBlank(w) && Abs(z - w) > Coalesce(tol; 0);;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma; kritoffen) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

```diff
+fnAbweichung(z: Number; l: Number; mx: Number; proz: Boolean; steig: Boolean): Boolean = !IsBlank(z) && !IsBlank(l) && ((steig && z < l) || (!IsBlank(mx) && Abs(z - l) > If(proz; Abs(l) * mx / 100; mx)));;
+fnVergleich(z: Number; w: Number; tol: Number): Boolean = !IsBlank(z) && !IsBlank(w) && Abs(z - w) > Coalesce(tol; 0);;
```

**Kurz erklärt:** Zwei neue Funktionen: `fnAbweichung` (zum letzten Mal, absolut/%, Zähler) und `fnVergleich` (zwei Werte, Toleranz).

**Nachprüfen:** endet auf `p.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;`

### 2.2 · `scrKategorie.OnVisible`

**Pfad:** `scrKategorie` → OnVisible

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

```diff
+If(!varNurLesen && varLetzteFuer <> varDurchID && CountRows(Filter(colPP; !IsBlank(AbwMax) || Coalesce(NurSteigend; false))) > 0;
+    Set(varLetzteFuer; varDurchID);;
+    Set(varLetzteRg; varDurch.RundgangID);;
+    Set(varLetzteTest; varDurch.TestDatensatz);;
+    Set(varLetzteDurch; First(Sort(Filter(RG_Durchfuehrungen; RundgangID = varLetzteRg && Status = stAbgeschlossen && TestDatensatz = varLetzteTest); ID; SortOrder.Descending)));;
+    If(IsBlank(varLetzteDurch.ID);
+        Clear(colLetzte);
+        Set(varLetzteID; varLetzteDurch.ID);;
+        ClearCollect(colLetzte; Filter(Ungroup(ForAll(Filter(RG_KategorieErgebnisse; DurchfuehrungID = varLetzteID) As e; {T: ForAll(Table(ParseJSON(e.Antworten)) As j; {PP: Value(j.Value.PruefpunktID); Z: Value(j.Value.WertZahl)})}); T …
+    )
+);;
-                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFot …
+                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFot …
+                     KPflOrig: Coalesce(p.KommentarPflicht; false);
+                     Letzter: If(p.Eingabetyp.Value = "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend; false)); Coalesce(LookUp(colLetzte; PP = p.ID).Z; LookUp(colLetzte; PP = Coalesce(p.QuelleID; -1)).Z));
+                     LetzterTag: If(IsBlank(varLetzteDurch.TagText); ""; Text(DateValue(varLetzteDurch.TagText); "dd.mm."));
+                     AbwMax: p.AbwMax;
+                     AbwProzent: Coalesce(p.AbwProzent; false);
+                     NurSteigend: Coalesce(p.NurSteigend; false);
+                     VglID: Coalesce(p.VergleichPunkt; 0);
+                     VglTol: Coalesce(p.VergleichTol; 0);
+                     AbwText: "";
-                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); …
+                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); …
+If(!varNurLesen; ClearCollect(colVglTmp; ForAll(Filter(colAntworten As a0; !a0.Inaktiv && a0.Typ = "ZAHL" && (a0.VglID <> 0 || !IsBlank(a0.Letzter))) As a;
+        With({w: LookUp(colAntworten As o; o.PruefpunktID = a.VglID)};
+            {PP: a.PruefpunktID;
+             Abw: fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend);
+             Vgl: a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol);
+             Text: If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); If(a.NurSteigend && a.WertZahl < a.Letzter; "kleiner als beim letzten Mal"; "starke Abweichung zum letzten Mal"); "") & If(a.VglID <> 0 && …
+             KPfl: a.KPflOrig}
+        )
+    ));;
+    ForAll(colVglTmp As v; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = v.PP); {KommentarPflicht: v.KPfl || v.Abw || v.Vgl; AbwText: v.Text})));;
```

**Kurz erklärt:** Lädt einmal je Rundgang die Zahlen des letzten abgeschlossenen Laufs (nur wenn ein Prüfpunkt der Kategorie es braucht). Neue Felder in allen drei Zweigen. Danach wird für alle Zahlen bestimmt, ob eine Begründung nötig ist.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

## Schritt 3 – Eingabe und Speichern

### 3.1 · `txtKaZahl.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › txtKaZahl` → OnChange

```
With({z: IfError(Value(Self.Text); Blank())};
    With({b: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus)); war: ThisItem.Bewertung = "NIO" && ThisItem.KritischOk};
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; WertText: ""; Bewertung: b; KritischOk: b = "NIO" && war; KritischZeit: If(b = "NIO" && war; ThisItem.KritischZeit; "")});;
        If(b = "NIO"; If(ThisItem.Rueckfrage; Set(varRueckPP; ThisItem.PruefpunktID); ThisItem.Kritisch && !LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID).KritischOk; Set(varKritPP; ThisItem.PruefpunktID)); Set(varRueckPP; 0);; Set(varKritPP; 0))
    )
);;
ClearCollect(colVglTmp; ForAll(Filter(colAntworten As a0; !a0.Inaktiv && a0.Typ = "ZAHL" && (a0.VglID <> 0 || !IsBlank(a0.Letzter))) As a;
    With({w: LookUp(colAntworten As o; o.PruefpunktID = a.VglID)};
        {PP: a.PruefpunktID;
         Abw: fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend);
         Vgl: a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol);
         Text: If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); If(a.NurSteigend && a.WertZahl < a.Letzter; "kleiner als beim letzten Mal"; "starke Abweichung zum letzten Mal"); "") & If(a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol); If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); "; "; "") & "weicht von „" & w.Frage & "“ ab (" & Text(w.WertZahl) & ")"; "");
         KPfl: a.KPflOrig}
    )
));;
ForAll(colVglTmp As v; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = v.PP); {KommentarPflicht: v.KPfl || v.Abw || v.Vgl; AbwText: v.Text}));;
Set(varGeaendert; true)
```

```diff
+ClearCollect(colVglTmp; ForAll(Filter(colAntworten As a0; !a0.Inaktiv && a0.Typ = "ZAHL" && (a0.VglID <> 0 || !IsBlank(a0.Letzter))) As a;
+    With({w: LookUp(colAntworten As o; o.PruefpunktID = a.VglID)};
+        {PP: a.PruefpunktID;
+         Abw: fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend);
+         Vgl: a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol);
+         Text: If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); If(a.NurSteigend && a.WertZahl < a.Letzter; "kleiner als beim letzten Mal"; "starke Abweichung zum letzten Mal"); "") & If(a.VglID <> 0 && fnV …
+         KPfl: a.KPflOrig}
+    )
+));;
+ForAll(colVglTmp As v; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = v.PP); {KommentarPflicht: v.KPfl || v.Abw || v.Vgl; AbwText: v.Text}));;
```

**Kurz erklärt:** Nach jeder Eingabe werden Abweichung und Vergleich neu bestimmt (auch beim Partner-Punkt).

**Nachprüfen:** endet auf `Set(varGeaendert; true)`

### 3.2 · `btnKaNM.OnSelect`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaNM` → OnSelect

```
If(ThisItem.WertText = "nicht messbar";
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: ""});
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: "nicht messbar"; WertZahl: Blank(); Bewertung: ""; KritischOk: false; KritischZeit: ""; KritischVon: ""});;
    Set(varRueckPP; 0);;
    Set(varKritPP; 0);;
    Reset(txtKaZahl)
);;
ClearCollect(colVglTmp; ForAll(Filter(colAntworten As a0; !a0.Inaktiv && a0.Typ = "ZAHL" && (a0.VglID <> 0 || !IsBlank(a0.Letzter))) As a;
    With({w: LookUp(colAntworten As o; o.PruefpunktID = a.VglID)};
        {PP: a.PruefpunktID;
         Abw: fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend);
         Vgl: a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol);
         Text: If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); If(a.NurSteigend && a.WertZahl < a.Letzter; "kleiner als beim letzten Mal"; "starke Abweichung zum letzten Mal"); "") & If(a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol); If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); "; "; "") & "weicht von „" & w.Frage & "“ ab (" & Text(w.WertZahl) & ")"; "");
         KPfl: a.KPflOrig}
    )
));;
ForAll(colVglTmp As v; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = v.PP); {KommentarPflicht: v.KPfl || v.Abw || v.Vgl; AbwText: v.Text}));;
Set(varGeaendert; true)
```

```diff
+ClearCollect(colVglTmp; ForAll(Filter(colAntworten As a0; !a0.Inaktiv && a0.Typ = "ZAHL" && (a0.VglID <> 0 || !IsBlank(a0.Letzter))) As a;
+    With({w: LookUp(colAntworten As o; o.PruefpunktID = a.VglID)};
+        {PP: a.PruefpunktID;
+         Abw: fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend);
+         Vgl: a.VglID <> 0 && fnVergleich(a.WertZahl; w.WertZahl; a.VglTol);
+         Text: If(fnAbweichung(a.WertZahl; a.Letzter; a.AbwMax; a.AbwProzent; a.NurSteigend); If(a.NurSteigend && a.WertZahl < a.Letzter; "kleiner als beim letzten Mal"; "starke Abweichung zum letzten Mal"); "") & If(a.VglID <> 0 && fnV …
+         KPfl: a.KPflOrig}
+    )
+));;
+ForAll(colVglTmp As v; Patch(colAntworten; LookUp(colAntworten; PruefpunktID = v.PP); {KommentarPflicht: v.KPfl || v.Abw || v.Vgl; AbwText: v.Text}));;
```

**Kurz erklärt:** Wie txtKaZahl: „nicht messbar“ hebt eine Abweichung auf.

**Nachprüfen:** endet auf `Set(varGeaendert; true)`

### 3.3 · `btnKaSpeichern.OnSelect`

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
-                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit; Kr …
+                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit; Kr …
```

**Kurz erklärt:** Speichert „zuletzt“ und den Abweichungs-Text mit (Protokoll, Nur-Ansicht).

**Nachprüfen:** endet auf `)`

## Schritt 4 – Anzeige in der Karte

### 4.1 · `lblKaZahlInfo.Text`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaZahlInfo` → Text

```
Trim(ThisItem.Einheit & If(IsBlank(ThisItem.MinWert) && IsBlank(ThisItem.MaxWert); ""; "  ·  " & If(ThisItem.Grenzmodus = "Sperren" && fnSperreGilt(ThisItem.MinWert; ThisItem.MaxWert); "zulässig "; "Soll ") & If(IsBlank(ThisItem.MinWert); ""; "ab " & ThisItem.MinWert & " ") & If(IsBlank(ThisItem.MaxWert); ""; "bis " & ThisItem.MaxWert)) & If(ThisItem.Bewertung = "NIO"; "  ·  außerhalb des Sollbereichs"; varNurLesen; If(ThisItem.Warnung; "  ·  außerhalb, begründet"; ""); !fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert); ""; ThisItem.Grenzmodus = "Warnen"; If(Trim(ThisItem.Kommentar) = ""; "  ·  außerhalb, bitte begründen"; "  ·  außerhalb, begründet"); ThisItem.Grenzmodus = "Sperren"; "  ·  unzulässig, bitte prüfen"; "")) & If(IsBlank(ThisItem.Letzter); ""; "  ·  zuletzt " & Text(ThisItem.Letzter) & If(ThisItem.LetzterTag = ""; ""; " (" & ThisItem.LetzterTag & ")")) & If(ThisItem.AbwText = ""; ""; "  ·  " & ThisItem.AbwText & If(varNurLesen || Trim(ThisItem.Kommentar) <> ""; ", begründet"; ", bitte begründen"))
```

```diff
-Trim(ThisItem.Einheit & If(IsBlank(ThisItem.MinWert) && IsBlank(ThisItem.MaxWert); ""; "  ·  " & If(ThisItem.Grenzmodus = "Sperren" && fnSperreGilt(ThisItem.MinWert; ThisItem.MaxWert); "zulässig "; "Soll ") & If(IsBlank(ThisItem.MinWert …
+Trim(ThisItem.Einheit & If(IsBlank(ThisItem.MinWert) && IsBlank(ThisItem.MaxWert); ""; "  ·  " & If(ThisItem.Grenzmodus = "Sperren" && fnSperreGilt(ThisItem.MinWert; ThisItem.MaxWert); "zulässig "; "Soll ") & If(IsBlank(ThisItem.MinWert …
```

**Kurz erklärt:** Zeigt „zuletzt …“ und den Abweichungs-Text mit „bitte begründen“.

**Nachprüfen:** endet auf `NurLesen || Trim(ThisItem.Kommentar) <> ""; ", begründet"; ", bitte begründen"))`

### 4.2 · `lblKaZahlInfo.Color`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaZahlInfo` → Color

```
If(ThisItem.Bewertung = "NIO" || (!varNurLesen && ThisItem.Grenzmodus = "Sperren" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; If(varNurLesen; ThisItem.Warnung; fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)) || ThisItem.AbwText <> ""; clrWarnung; clrTextGrau)
```

```diff
-If(ThisItem.Bewertung = "NIO" || (!varNurLesen && ThisItem.Grenzmodus = "Sperren" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; If(varNurLesen; ThisItem.Warnung; fnAusserhalb(ThisItem.WertZahl; This …
+If(ThisItem.Bewertung = "NIO" || (!varNurLesen && ThisItem.Grenzmodus = "Sperren" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; If(varNurLesen; ThisItem.Warnung; fnAusserhalb(ThisItem.WertZahl; This …
```

**Kurz erklärt:** Orange bei Abweichung.

**Nachprüfen:** endet auf `.MinWert; ThisItem.MaxWert)) || ThisItem.AbwText <> ""; clrWarnung; clrTextGrau)`

### 4.3 · `lblKaZahlInfo.Size`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaZahlInfo` → Size

```
If(btnKaNM.Visible || !IsBlank(ThisItem.Letzter) || ThisItem.AbwText <> ""; 12; 14)
```

```diff
-If(btnKaNM.Visible; 12; 14)
+If(btnKaNM.Visible || !IsBlank(ThisItem.Letzter) || ThisItem.AbwText <> ""; 12; 14)
```

**Kurz erklärt:** Kleiner, wenn zusätzlicher Text da ist.

**Nachprüfen:** endet auf `btnKaNM.Visible || !IsBlank(ThisItem.Letzter) || ThisItem.AbwText <> ""; 12; 14)`

## Schritt 5 – Protokoll

### 5.1 · `htmProtokoll.HtmlText`

**Pfad:** `scrProtokoll › conPrInhalt › htmProtokoll` → HtmlText

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

```diff
-                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) & If(w; " <span style='color:#9A5B00'>(außerhalb So …
+                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) & If(w; " <span style='color:#9A5B00'>(außerhalb So …
```

**Kurz erklärt:** Protokoll nennt die Abweichung.

**Nachprüfen:** endet auf `)`

## Test (ZZ-Test-Rundgang, Zeitachse)

| # | Schritt | erwartet |
|---|---|---|
| T1 | Prüfpunkt Zahl: `AbwMax` = 0,5. Rundgang starten, Wert 7,6 eingeben, alles speichern, **abschließen** | erster Lauf: kein „zuletzt“ |
| T2 | Am nächsten Testtag (oder Rundgang zurücksetzen und neu starten) die Kategorie öffnen | Karte zeigt „zuletzt 7,6 (TT.MM.)“ |
| T3 | 7,9 eingeben | nichts Besonderes |
| T4 | 8,4 eingeben | orange „starke Abweichung zum letzten Mal, bitte begründen“, Kommentar Pflicht. Begründen, speichern, Protokoll nennt es |
| T5 | Zähler: `NurSteigend` = Ja, kleineren Wert als beim letzten Mal eingeben | „kleiner als beim letzten Mal“, Begründung Pflicht |
| T6 | Zwei Zahlen derselben Kategorie, bei B `VergleichPunkt` = ID von A, `VergleichTol` = 0,2. A = 7,6, B = 8,0 | B: „weicht von „A“ ab (7,6)“. A auf 7,9 ändern → Hinweis bei B verschwindet |
| T7 | B „nicht messbar“ | Vergleich entfällt, nur Begründung für „nicht messbar“ |

## Rückweg

Vorher-Fassungen im Anhang einsetzen. Spalten dürfen bleiben.

## Anhang – Vorher-Fassungen (Stand nach Paket 12+16)

**`App.Formulas` vorher**

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
    typ = "DATUMZEIT" && wt <> "" && Len(wt) < 16; "Uhrzeit";
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
fnDatumText(d: Date; h: Text; m: Text; mitZeit: Boolean): Text = If(IsBlank(d); ""; Text(d; "dd.mm.yyyy") & If(mitZeit && h <> "" && m <> ""; " " & h & ":" & m; ""));;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma; kritoffen) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

**`scrKategorie.OnVisible` vorher**

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
Set(varGespeichertBeimOeffnen; varErgebnis.GespeichertAm);;
With({t: If(IsBlank(varErgebnis.Antworten); Table(ParseJSON("[]")); Table(ParseJSON(varErgebnis.Antworten)))};
    If(varNurLesen && !IsEmpty(t);
        ClearCollect(colAntworten;
            ForAll(Sequence(CountRows(t)) As i;
                With({a: Index(t; i.Value).Value};
                    With({pp: LookUp(colPP; ID = Value(a.PruefpunktID))};
                        {PruefpunktID: Value(a.PruefpunktID); Frage: Text(a.Frage); Typ: Text(a.Typ); Pflicht: false; Einheit: Coalesce(Text(a.Einheit); ""); MinWert: pp.MinWert; MaxWert: pp.MaxWert; Auswahl: Coalesce(Text(a.WertText); ""); Hinweis: ""; Reihenfolge: i.Value;
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); BildID: Coalesce(pp.HinweisBildID; 0); Abschnitt: Trim(Coalesce(Text(a.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(a.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(a.KritischOk); false); false); KritischZeit: Coalesce(Text(a.KritischZeit); ""); KritischVon: Coalesce(Text(a.KritischVon); ""); TextIO: Coalesce(Text(a.TextIO); ""); TextNIO: Coalesce(Text(a.TextNIO); ""); NMErlaubt: false; Inaktiv: false}
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
                     Warnung: false;
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Warnung: Coalesce(IfError(Boolean(o.Value.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); BildID: 0; Abschnitt: Trim(Coalesce(Text(o.Value.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(o.Value.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(o.Value.KritischOk); false); false); KritischZeit: Coalesce(Text(o.Value.KritischZeit); ""); KritischVon: Coalesce(Text(o.Value.KritischVon); ""); TextIO: Coalesce(Text(o.Value.TextIO); ""); TextNIO: Coalesce(Text(o.Value.TextNIO); ""); NMErlaubt: false; Inaktiv: true}
            )
        )
    )
);;
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

**`txtKaZahl.OnChange` vorher**

```
With({z: IfError(Value(Self.Text); Blank())};
    With({b: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus)); war: ThisItem.Bewertung = "NIO" && ThisItem.KritischOk};
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; WertText: ""; Bewertung: b; KritischOk: b = "NIO" && war; KritischZeit: If(b = "NIO" && war; ThisItem.KritischZeit; "")});;
        If(b = "NIO"; If(ThisItem.Rueckfrage; Set(varRueckPP; ThisItem.PruefpunktID); ThisItem.Kritisch && !LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID).KritischOk; Set(varKritPP; ThisItem.PruefpunktID)); Set(varRueckPP; 0);; Set(varKritPP; 0))
    )
);;
Set(varGeaendert; true)
```

**`btnKaNM.OnSelect` vorher**

```
If(ThisItem.WertText = "nicht messbar";
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: ""});
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: "nicht messbar"; WertZahl: Blank(); Bewertung: ""; KritischOk: false; KritischZeit: ""; KritischVon: ""});;
    Set(varRueckPP; 0);;
    Set(varKritPP; 0);;
    Reset(txtKaZahl)
);;
Set(varGeaendert; true)
```

**`btnKaSpeichern.OnSelect` vorher**

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
                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit; KritischVon; TextIO; TextNIO); JSONFormat.Compact));;
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

**`lblKaZahlInfo.Text` vorher**

```
Trim(ThisItem.Einheit & If(IsBlank(ThisItem.MinWert) && IsBlank(ThisItem.MaxWert); ""; "  ·  " & If(ThisItem.Grenzmodus = "Sperren" && fnSperreGilt(ThisItem.MinWert; ThisItem.MaxWert); "zulässig "; "Soll ") & If(IsBlank(ThisItem.MinWert); ""; "ab " & ThisItem.MinWert & " ") & If(IsBlank(ThisItem.MaxWert); ""; "bis " & ThisItem.MaxWert)) & If(ThisItem.Bewertung = "NIO"; "  ·  außerhalb des Sollbereichs"; varNurLesen; If(ThisItem.Warnung; "  ·  außerhalb, begründet"; ""); !fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert); ""; ThisItem.Grenzmodus = "Warnen"; If(Trim(ThisItem.Kommentar) = ""; "  ·  außerhalb, bitte begründen"; "  ·  außerhalb, begründet"); ThisItem.Grenzmodus = "Sperren"; "  ·  unzulässig, bitte prüfen"; ""))
```

**`lblKaZahlInfo.Color` vorher**

```
If(ThisItem.Bewertung = "NIO" || (!varNurLesen && ThisItem.Grenzmodus = "Sperren" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; If(varNurLesen; ThisItem.Warnung; fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrWarnung; clrTextGrau)
```

**`lblKaZahlInfo.Size` vorher**

```
If(btnKaNM.Visible; 12; 14)
```

**`htmProtokoll.HtmlText` vorher**

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
                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) & If(w; " <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>"; "") &
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

