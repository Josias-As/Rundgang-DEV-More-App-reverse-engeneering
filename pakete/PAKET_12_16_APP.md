# Paket 12+16 – Rundgang-App: eigene Antwortwörter, „nicht messbar“

Stand 02.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket12, paket16) und `werkzeuge/doc_paket12_16.py`. **Voraussetzung: Paket N und Paket 8–10 eingefügt** (`PAKET_N_Nachholen.md`, `PAKET_8_9_10_APP.md`).

## Kurzfassung

- **Paket 12 – eigene Antwortwörter:** Bei i.O./n.i.O.-Fragen lassen sich die Knöpfe umbenennen, z. B. „durchgeführt“ / „nicht durchgeführt“ (Legionellen). Intern bleibt es i.O./n.i.O.: „nicht durchgeführt“ ergibt weiter einen Mangel. Leer = „i.O.“/„n.i.O.“ wie bisher. Protokoll zeigt die eigenen Wörter. Höchstens 18 Zeichen.
- **Paket 16 – „nicht messbar“:** Bei Zahlen, für die es im Builder erlaubt ist, gibt es den Knopf „nicht messbar“ (z. B. Anlage aus). Dann ist das Feld leer, die Frage gilt als beantwortet, aber eine **Begründung (Kommentar) ist Pflicht**. Im Protokoll steht „nicht messbar“ statt „0“. Kein Mangel.
- Umfang: 3 Spalten, 16 Properties (jede einmal), 1 neuer Knopf. Generator 0 Fehler, Mutation 12/12, Logik 91 Szenarien, unabhängig geprüft (9 Befunde eingearbeitet, `arbeit/2026-11-02_Paket12_16/pruefung_unabhaengig.md`). **Nicht in Studio getestet.**

## Schritt 1 – SharePoint

`RG_Pruefpunkte`: `TextIO` (Eine Textzeile), `TextNIO` (Eine Textzeile), `NichtMessbar` (Ja/Nein, Standard Nein). Danach in der Rundgang-App: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**.

## Schritt 2 – Laden, Formeln, Speichern

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
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma; kritoffen) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

```diff
- … s: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz; mi; ma));; …
+ … s: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (typ = "ZAHL" && wt = "nicht messbar") || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && f …
- … (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATUMZEIT") && …
+ … (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz) && wt = "") || (typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATU …
```

**Kurz erklärt:** „nicht messbar“ zählt als beantwortet (`fnFehltGrund`) und braucht einen Kommentar (`fnKommentarNoetig`).

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

```diff
- … Zeit); ""); KritischVon: Coalesce(Text(a.KritischVon); ""); Inaktiv: false} …
+ … Zeit); ""); KritischVon: Coalesce(Text(a.KritischVon); ""); TextIO: Coalesce(Text(a.TextIO); ""); TextNIO: Coalesce(Text(a.TextNIO); ""); NMErlaubt: false; Inaktiv: false} …
+                     TextIO: Trim(Coalesce(p.TextIO; ""));
+                     TextNIO: Trim(Coalesce(p.TextNIO; ""));
+                     NMErlaubt: Coalesce(p.NichtMessbar; false);
- Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Val …
+ Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Val …
```

**Kurz erklärt:** Neue Felder `TextIO`, `TextNIO`, `NMErlaubt` in allen drei Zweigen.

**Nachprüfen:** endet auf `Set(varIsLoading; false)`

### 2.3 · `btnKaSpeichern.OnSelect`

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

```diff
- … tt; AbsKopf; Kritisch; KritischOk; KritischZeit; KritischVon); JSONFormat.Compact));; …
+ … tt; AbsKopf; Kritisch; KritischOk; KritischZeit; KritischVon; TextIO; TextNIO); JSONFormat.Compact));; …
```

**Kurz erklärt:** Speichert die Knopf-Wörter mit (für Protokoll und Nur-Ansicht).

**Nachprüfen:** endet auf `)`

## Schritt 3 – Knöpfe i.O./n.i.O.

### 3.1 · `btnKaIO.Text`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaIO` → Text

```
If(Trim(ThisItem.TextIO) = ""; "i.O."; ThisItem.TextIO)
```

```diff
-"i.O."
+If(Trim(ThisItem.TextIO) = ""; "i.O."; ThisItem.TextIO)
```

**Kurz erklärt:** Eigenes Wort oder „i.O.“.

**Nachprüfen:** endet auf `If(Trim(ThisItem.TextIO) = ""; "i.O."; ThisItem.TextIO)`

### 3.2 · `btnKaNIO.Text`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaNIO` → Text

```
If(Trim(ThisItem.TextNIO) = ""; "n.i.O."; ThisItem.TextNIO)
```

```diff
-"n.i.O."
+If(Trim(ThisItem.TextNIO) = ""; "n.i.O."; ThisItem.TextNIO)
```

**Kurz erklärt:** Eigenes Wort oder „n.i.O.“.

**Nachprüfen:** endet auf `If(Trim(ThisItem.TextNIO) = ""; "n.i.O."; ThisItem.TextNIO)`

### 3.3 · `btnKaIO.Width`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaIO` → Width

```
If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 8; 260; 160)
```

```diff
- 160 (Standard)
+ If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 8; 260; 160)
```

**Kurz erklärt:** Breiter (250), wenn ein Wort länger als 8 Zeichen ist.

**Nachprüfen:** endet auf `If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 8; 260; 160)`

### 3.4 · `btnKaNIO.Width`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaNIO` → Width

```
If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 8; 260; 160)
```

```diff
- 160 (Standard)
+ If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 8; 260; 160)
```

**Kurz erklärt:** Wie btnKaIO.Width.

**Nachprüfen:** endet auf `If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 8; 260; 160)`

### 3.5 · `btnKaNIO.X`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaNIO` → X

```
36 + btnKaIO.Width
```

```diff
-196
+36 + btnKaIO.Width
```

**Kurz erklärt:** Steht immer 16 px rechts vom i.O.-Knopf.

**Nachprüfen:** endet auf `36 + btnKaIO.Width`

### 3.6 · `btnKaIO.Size`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaIO` → Size

```
If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 12; 14; 17)
```

```diff
-17
+If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 12; 14; 17)
```

**Kurz erklärt:** Schrift 14 statt 17 bei Wörtern über 12 Zeichen.

**Nachprüfen:** endet auf `If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 12; 14; 17)`

### 3.7 · `btnKaNIO.Size`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaNIO` → Size

```
If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 12; 14; 17)
```

```diff
-17
+If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 12; 14; 17)
```

**Kurz erklärt:** Wie btnKaIO.Size.

**Nachprüfen:** endet auf `If(Max(Len(ThisItem.TextIO); Len(ThisItem.TextNIO)) > 12; 14; 17)`

## Schritt 4 – Fenster mit dem eigenen Wort

### 4.1 · `lblKaRueckFrage.Text`

**Pfad:** `scrKategorie › conKaRueck › conKaRueckKarte › lblKaRueckFrage` → Text

```
With({r: LookUp(colAntworten; PruefpunktID = varRueckPP)}; r.Frage & Char(10) & "Ihre Antwort: " & If(r.Typ = "ZAHL"; Text(r.WertZahl) & " " & r.Einheit; If(Trim(r.TextNIO) = ""; "n.i.O."; r.TextNIO)))
```

```diff
-With({r: LookUp(colAntworten; PruefpunktID = varRueckPP)}; r.Frage & Char(10) & "Ihre Antwort: " & If(r.Typ = "ZAHL"; Text(r.WertZahl) & " " & r.Einheit; "n.i.O."))
+With({r: LookUp(colAntworten; PruefpunktID = varRueckPP)}; r.Frage & Char(10) & "Ihre Antwort: " & If(r.Typ = "ZAHL"; Text(r.WertZahl) & " " & r.Einheit; If(Trim(r.TextNIO) = ""; "n.i.O."; r.TextNIO)))
```

**Kurz erklärt:** Rückfrage zeigt das eigene Wort statt „n.i.O.“.

**Nachprüfen:** endet auf `t(r.WertZahl) & " " & r.Einheit; If(Trim(r.TextNIO) = ""; "n.i.O."; r.TextNIO)))`

### 4.2 · `btnKaKritVersehen.Text`

**Pfad:** `scrKategorie › conKaKrit › conKaKritKarte › btnKaKritVersehen` → Text

```
If(Trim(LookUp(colAntworten; PruefpunktID = varKritPP).TextNIO) = ""; "n.i.O."; LookUp(colAntworten; PruefpunktID = varKritPP).TextNIO) & " war ein Versehen – Antwort zurücknehmen"
```

```diff
-"n.i.O. war ein Versehen – Antwort zurücknehmen"
+If(Trim(LookUp(colAntworten; PruefpunktID = varKritPP).TextNIO) = ""; "n.i.O."; LookUp(colAntworten; PruefpunktID = varKritPP).TextNIO) & " war ein Versehen – Antwort zurücknehmen"
```

**Kurz erklärt:** „… war ein Versehen“ mit dem eigenen Wort.

**Nachprüfen:** endet auf ` PruefpunktID = varKritPP).TextNIO) & " war ein Versehen – Antwort zurücknehmen"`

## Schritt 5 – „nicht messbar“

### 5.1 · `txtKaZahl.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › txtKaZahl` → OnChange

```
With({z: IfError(Value(Self.Text); Blank())};
    With({b: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus)); war: ThisItem.Bewertung = "NIO" && ThisItem.KritischOk};
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; WertText: ""; Bewertung: b; KritischOk: b = "NIO" && war; KritischZeit: If(b = "NIO" && war; ThisItem.KritischZeit; "")});;
        If(b = "NIO"; If(ThisItem.Rueckfrage; Set(varRueckPP; ThisItem.PruefpunktID); ThisItem.Kritisch && !LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID).KritischOk; Set(varKritPP; ThisItem.PruefpunktID)); Set(varRueckPP; 0);; Set(varKritPP; 0))
    )
);;
Set(varGeaendert; true)
```

```diff
-        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; Bewertung: b; KritischOk: b = "NIO" && war; KritischZeit: If(b = "NIO" && war; ThisItem.KritischZeit; "")});;
+        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; WertText: ""; Bewertung: b; KritischOk: b = "NIO" && war; KritischZeit: If(b = "NIO" && war; ThisItem.KritischZeit; "")});;
```

**Kurz erklärt:** Eine eingetippte Zahl hebt „nicht messbar“ wieder auf.

**Nachprüfen:** endet auf `Set(varGeaendert; true)`

### 5.2 · `lblKaZahlInfo.Width`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaZahlInfo` → Width

```
Parent.Width - 256 - If(btnKaNM.Visible; 136; 0)
```

```diff
-Parent.Width - 256
+Parent.Width - 256 - If(btnKaNM.Visible; 136; 0)
```

**Kurz erklärt:** Macht Platz für den neuen Knopf.

**Nachprüfen:** endet auf `Parent.Width - 256 - If(btnKaNM.Visible; 136; 0)`

### 5.3 · `lblKaZahlInfo.Size`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaZahlInfo` → Size

```
If(btnKaNM.Visible; 12; 14)
```

```diff
-14
+If(btnKaNM.Visible; 12; 14)
```

**Kurz erklärt:** Etwas kleiner, solange der Knopf „nicht messbar“ da ist (sonst wird „… bitte begründen“ abgeschnitten).

**Nachprüfen:** endet auf `If(btnKaNM.Visible; 12; 14)`

### 5.4 · neuer Knopf `btnKaNM`

**Wo hin:** in der Strukturansicht `txtKaZahl` (in `conKaKarte`) markieren → Strg+V (landet in derselben Karte).

```yaml
- btnKaNM:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrTextGrau
      BorderThickness: =1
      Color: =If(ThisItem.WertText = "nicht messbar", Color.White, clrTextGrau)
      DisabledBorderColor: =clrTextGrau
      DisabledColor: =Self.Color
      DisabledFill: =Self.Fill
      DisplayMode: =If(varNurLesen, DisplayMode.View, DisplayMode.Edit)
      Fill: =If(ThisItem.WertText = "nicht messbar", clrTextGrau, clrKarte)
      Font: =Font.'Segoe UI'
      Height: =56
      HoverColor: =Self.Color
      HoverFill: =If(ThisItem.WertText = "nicht messbar", ColorFade(clrTextGrau, -15%), clrHintergrund)
      OnSelect: |-
        =If(ThisItem.WertText = "nicht messbar",
            Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: ""}),
            Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: "nicht messbar", WertZahl: Blank(), Bewertung: "", KritischOk: false, KritischZeit: "", KritischVon: ""});
            Set(varRueckPP, 0);
            Set(varKritPP, 0);
            Reset(txtKaZahl)
        );
        Set(varGeaendert, true)
      PressedColor: =Color.White
      PressedFill: =clrTextGrau
      RadiusBottomLeft: =8
      RadiusBottomRight: =8
      RadiusTopLeft: =8
      RadiusTopRight: =8
      Size: =13
      Text: =If(ThisItem.WertText = "nicht messbar", "✓ nicht messbar", "nicht messbar")
      Visible: =ThisItem.Typ = "ZAHL" && (ThisItem.NMErlaubt || ThisItem.WertText = "nicht messbar")
      Width: =120
      X: =Parent.Width - 140
      Y: =54 + If(ThisItem.Hinweis <> "", 24, 0)
```

**Nachprüfen (E-05):** `btnKaNM.Y` muss die Formel `54 + If(ThisItem.Hinweis <> ""; 24; 0)` sein, keine Zahl.

## Schritt 6 – Protokoll

### 6.1 · `htmProtokoll.HtmlText`

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

```diff
-                "<td style='padding:6px 8px;width:64px;white-space:nowrap;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; w; "#9A5B00"; "#0F7B3F") & "'>" & Switch(b; "IO"; "i.O."; "NIO"; "n.i.O."; "") & "</td>" &
+ "<td style='padding:6px 8px;width:110px;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; w; "#9A5B00"; "#0F7B3F") & "'>" & Switch(b; "IO"; fnHtml(Coalesce(If(Coal …
```

**Kurz erklärt:** Protokoll zeigt die eigenen Wörter, Spalte etwas breiter (110 px).

**Nachprüfen:** endet auf `)`

## Test (ZZ-Test-Rundgang)

| # | Schritt | erwartet |
|---|---|---|
| T1 | In SharePoint an einer i.O./n.i.O.-Frage `TextIO` = „durchgeführt“, `TextNIO` = „nicht durchgeführt“. Kategorie öffnen | Knöpfe heißen so, breiter |
| T2 | „nicht durchgeführt“ tippen | wie n.i.O.: Kommentar Pflicht, Mangel beim Abschluss |
| T3 | Speichern, Protokoll ansehen | Protokoll zeigt „nicht durchgeführt“ |
| T4 | Zahl-Frage mit `NichtMessbar` = Ja: „nicht messbar“ tippen | Feld leer, Knopf grau gefüllt „✓ nicht messbar“, „Noch offen … (Kommentar)“ |
| T5 | Begründung eintragen, speichern | gespeichert, Protokoll „nicht messbar“ + Begründung, kein Mangel |
| T6 | Kategorie neu öffnen, eine Zahl eintippen | „nicht messbar“ ist aufgehoben, Zahl gilt |
| T7 | Zahl-Frage ohne `NichtMessbar` | kein Knopf, alles wie bisher |
| T8 | Zahl-Frage mit Rückfrage: Wert außerhalb tippen und **ohne** das Feld zu verlassen „nicht messbar“ tippen | kein Fenster, Speichern verlangt nur die Begründung |
| T9 | Rückfrage bei „nicht durchgeführt“ | Fenster sagt „Ihre Antwort: nicht durchgeführt“ |

## Bekannt / Frage an den Planer

- „nicht messbar“ umgeht Grenzmodus „Sperren“ und „kritisch“ (es gibt keinen Wert). Gewollt? Sonst: „nicht messbar“ bei kritischen Punkten im Builder sperren.
- Wird „nicht messbar“ im Builder später abgeschaltet, bleibt ein schon gespeichertes „nicht messbar“ gültig. Der Knopf bleibt dann sichtbar, damit man es aufheben kann.

## Rückweg

Vorher-Fassungen im Anhang einsetzen, `btnKaNM` löschen. Spalten dürfen bleiben.

## Anhang – Vorher-Fassungen (Stand nach Paket 8–10)

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
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz; mi; ma));;
fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATUMZEIT") && wt = "")); "Wert";
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
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); BildID: Coalesce(pp.HinweisBildID; 0); Abschnitt: Trim(Coalesce(Text(a.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(a.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(a.KritischOk); false); false); KritischZeit: Coalesce(Text(a.KritischZeit); ""); KritischVon: Coalesce(Text(a.KritischVon); ""); Inaktiv: false}
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
                     Warnung: false;
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Warnung: Coalesce(IfError(Boolean(o.Value.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); BildID: 0; Abschnitt: Trim(Coalesce(Text(o.Value.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(o.Value.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(o.Value.KritischOk); false); false); KritischZeit: Coalesce(Text(o.Value.KritischZeit); ""); KritischVon: Coalesce(Text(o.Value.KritischVon); ""); Inaktiv: true}
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
                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit; KritischVon); JSONFormat.Compact));;
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

**`btnKaIO.Text` vorher**

```
"i.O."
```

**`btnKaNIO.Text` vorher**

```
"n.i.O."
```

**`btnKaIO.Width` vorher**

```
160 (Standard)
```

**`btnKaNIO.Width` vorher**

```
160 (Standard)
```

**`btnKaNIO.X` vorher**

```
196
```

**`btnKaIO.Size` vorher**

```
17
```

**`btnKaNIO.Size` vorher**

```
17
```

**`lblKaRueckFrage.Text` vorher**

```
With({r: LookUp(colAntworten; PruefpunktID = varRueckPP)}; r.Frage & Char(10) & "Ihre Antwort: " & If(r.Typ = "ZAHL"; Text(r.WertZahl) & " " & r.Einheit; "n.i.O."))
```

**`btnKaKritVersehen.Text` vorher**

```
"n.i.O. war ein Versehen – Antwort zurücknehmen"
```

**`txtKaZahl.OnChange` vorher**

```
With({z: IfError(Value(Self.Text); Blank())};
    With({b: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus)); war: ThisItem.Bewertung = "NIO" && ThisItem.KritischOk};
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; Bewertung: b; KritischOk: b = "NIO" && war; KritischZeit: If(b = "NIO" && war; ThisItem.KritischZeit; "")});;
        If(b = "NIO"; If(ThisItem.Rueckfrage; Set(varRueckPP; ThisItem.PruefpunktID); ThisItem.Kritisch && !LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID).KritischOk; Set(varKritPP; ThisItem.PruefpunktID)); Set(varRueckPP; 0);; Set(varKritPP; 0))
    )
);;
Set(varGeaendert; true)
```

**`lblKaZahlInfo.Width` vorher**

```
Parent.Width - 256
```

**`lblKaZahlInfo.Size` vorher**

```
14
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
                "<td style='padding:6px 8px;width:64px;white-space:nowrap;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; w; "#9A5B00"; "#0F7B3F") & "'>" & Switch(b; "IO"; "i.O."; "NIO"; "n.i.O."; "") & "</td>" &
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

