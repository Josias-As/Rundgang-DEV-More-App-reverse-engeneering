# Baukasten-Paket 3 – Zahlengrenzen pro Prüfpunkt: Mangel, Warnen oder Sperren

Stand: 27.10.2026 · erzeugt mit `werkzeuge/baukasten.py` aus dem Export `2026-10-27_0724` **(ENTWURF: Simulation der Änderung von 08:44, vor dem Einfügen mit dem frischen Export neu erzeugen)**.

## Kurzfassung

- Neue Auswahlspalte **Grenzmodus** am Prüfpunkt: Mangel (Standard = wie heute), Warnen, Sperren.
- **Mangel:** Wert außerhalb Min/Max → n.i.O., Kommentar Pflicht, Mangel beim Abschluss (unverändert).
- **Warnen:** Wert außerhalb → orange Hinweis „außerhalb, bitte begründen“, Kommentar Pflicht, Bewertung i.O., **kein** Mangel.
- **Sperren:** Wert außerhalb → rot „unzulässig, bitte prüfen“, Speichern geht erst mit einem Wert im Bereich (für Tippfehler-Grenzen).
- Annahme (bitte bestätigen): „Warnen“ verlangt eine Begründung, weil Josias Kontrollen statt Abkürzungen will.

## Voraussetzungen

- Paket 1 und 2 sind eingefügt und getestet.

## Schritte

### Schritt 3.1 – Sicherung

Studio: oben **Speichern**. Dann make.powerapps.com → Apps → „Rundgang DEV“ → … → **Details → Versionen**: die oberste Versionsnummer notieren. Das ist der Rückweg auf Knopfdruck (Version wiederherstellen).

### Schritt 3.2 – SharePoint-Spalte anlegen

RG_Pruefpunkte → **+ Spalte hinzufügen → Auswahl**: Name **Grenzmodus**, Auswahlmöglichkeiten **Mangel**, **Warnen**, **Sperren**, Standardwert **Mangel**, keine Mehrfachauswahl.
Für den Test: drei Zahl-Prüfpunkte mit Min/Max (oder einen nacheinander umstellen): Grenzmodus Mangel / Warnen / Sperren.
Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren** (sonst kennt die App die neue Spalte nicht und die Formeln in den nächsten Schritten zeigen Fehler).

### Schritt 3.3 – App.Formulas

Je Block: Steuerelement in der Strukturansicht markieren, Property oben links im Auswahlfeld wählen, in der Formelleiste **Strg+A**, dann den ganzen Block einfügen. Bis alle Blöcke dieses Pakets drin sind, können rote Fehler stehen (neue Funktionsköpfe passen erst zusammen, wenn alle Aufrufer ersetzt sind).
Neu: Farben clrWarnung/clrWarnungHell, fnGrenzmodus; geändert: fnZahlBewertung, fnKommentarNoetig, fnFehltGrund.

**`App.Formulas`**

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
clrWarnungHell = ColorValue("#FFF3E0");;
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
    Switch(gmodus; "Warnen"; "IO"; "Sperren"; ""; "NIO");
    "IO"
);;
fnGrenzmodus(g: Text): Text = If(g = "Warnen" || g = "Sperren"; g; "Mangel");;
fnHtml(t: Text): Text = Substitute(Substitute(Substitute(Substitute(Substitute(t; "&"; "&amp;"); "<"; "&lt;"); ">"; "&gt;"); """"; "&quot;"); "'"; "&#39;");;
cfgAdmins = Coalesce(LookUp(RG_Konfiguration; Title = "Admins").Wert; "");;
fnLinkAnzahl(t: Text): Number = CountRows(Filter(Split(Coalesce(t; ""); " | ") As s; Trim(s.Value) <> ""));;
fnFotoModus(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht"; f; alt; "Optional"; "Aus");;
fnBeantwortet(bew: Text; wt: Text; wz: Number): Boolean = bew <> "" || Trim(wt) <> "" || !IsBlank(wz);;
fnAusserhalb(z: Number; mi: Number; ma: Number): Boolean = !IsBlank(z) && ((!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma));;
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz; mi; ma));;
fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "")); "Wert";
    typ = "ZAHL" && gmodus = "Sperren" && fnAusserhalb(wz; mi; ma); "Bereich";
    fnKommentarNoetig(typ; bew; wt; wz; kpfl; gmodus; mi; ma) && Trim(kom) = ""; "Kommentar";
    foto = "Pflicht" && fanz < 1; "Foto";
    ""
);;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

### Schritt 3.4 – Kategorie öffnen

`scrKategorie.OnVisible`: Grenzmodus aus der Spalte, Bewertung gespeicherter Zahlen mit dem Grenzmodus.

**`scrKategorie.OnVisible`**

```
Set(varIsLoading; true);;
Set(varZurueckFrage; false);;
Set(varAlleIOFrage; false);;
Set(varZeigeFehlend; false);;
Set(varFotoPP; 0);;
Clear(colFotos);;
Set(varGeaendert; false);;
Set(varSchluesselK; "D" & varDurchID & "-K" & varKatID);;
Set(varNurLesen; varDurch.Status <> stInArbeit);;
Refresh(RG_KategorieErgebnisse);;
Concurrent(
    ClearCollect(colPP; Filter(RG_Pruefpunkte; KategorieID = varKatID && Aktiv = true));
    Set(varErgebnis; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK))
);;
Set(varGespeichertBeimOeffnen; varErgebnis.GespeichertAm);;
With({t: If(IsBlank(varErgebnis.Antworten); Table(ParseJSON("[]")); Table(ParseJSON(varErgebnis.Antworten)))};
    If(varNurLesen && !IsEmpty(t);
        ClearCollect(colAntworten;
            ForAll(Sequence(CountRows(t)) As i;
                With({a: Index(t; i.Value).Value};
                    With({pp: LookUp(colPP; ID = Value(a.PruefpunktID))};
                        {PruefpunktID: Value(a.PruefpunktID); Frage: Text(a.Frage); Typ: Text(a.Typ); Pflicht: false; Einheit: Coalesce(Text(a.Einheit); ""); MinWert: pp.MinWert; MaxWert: pp.MaxWert; Auswahl: Coalesce(Text(a.WertText); ""); Hinweis: ""; Reihenfolge: i.Value;
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Inaktiv: false}
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
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Inaktiv: true}
            )
        )
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
```

### Schritt 3.5 – Anzeige am Zahlenfeld

`conKaKarte` → `lblKaZahlInfo`, `txtKaZahl`.

**`lblKaZahlInfo.Text`**

```
Trim(ThisItem.Einheit & If(IsBlank(ThisItem.MinWert) && IsBlank(ThisItem.MaxWert); ""; "  ·  Soll " & If(IsBlank(ThisItem.MinWert); ""; "ab " & ThisItem.MinWert & " ") & If(IsBlank(ThisItem.MaxWert); ""; "bis " & ThisItem.MaxWert)) & If(ThisItem.Bewertung = "NIO"; "  ·  außerhalb des Sollbereichs"; !fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert); ""; ThisItem.Grenzmodus = "Warnen"; "  ·  außerhalb, bitte begründen"; ThisItem.Grenzmodus = "Sperren"; "  ·  unzulässig, bitte prüfen"; ""))
```

**`lblKaZahlInfo.Color`**

```
If(ThisItem.Bewertung = "NIO" || (ThisItem.Grenzmodus = "Sperren" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; ThisItem.Grenzmodus = "Warnen" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert); clrWarnung; clrTextGrau)
```

**`txtKaZahl.BorderColor`**

```
If(ThisItem.Bewertung = "NIO" || (ThisItem.Grenzmodus = "Sperren" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; ThisItem.Grenzmodus = "Warnen" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert); clrWarnung; clrRahmen)
```

### Schritt 3.6 – App-Prüfung und Speichern

Studio → **App-Prüfung → Formeln**: muss **0** sein (Barrierefreiheit/Leistung wie bisher, siehe E-07/E-08). Dann **Speichern** (noch nicht veröffentlichen) und den Test unten in der **Vorschau** machen.
Bei einem Formelfehler: Fehlermeldung und Steuerelement notieren, nicht selbst umbauen, mir schicken.

## Test

Prüfpunkt mit Soll 6–16 °C (wie T11 im Testprotokoll).

| # | Klickfolge | erwartet |
|---|---|---|
| T3.1 | Grenzmodus Mangel: 18,5 eingeben | wie heute: rot „außerhalb des Sollbereichs“, Kommentar Pflicht, Karte rot |
| T3.2 | Grenzmodus Warnen: 18,5 | orange „außerhalb, bitte begründen“, Rahmen orange, Kommentarfeld „Kommentar (Pflicht)“, Karte **nicht** rot umrandet |
| T3.3 | Kommentar „Fühler defekt“, Speichern | „Gespeichert.“ |
| T3.4 | Grenzmodus Sperren: 18,5 | rot „unzulässig, bitte prüfen“, Fuß „Noch offen (1): … (unzulässiger Wert)“, Speichern springt zum Punkt |
| T3.5 | 12 eingeben | Hinweis weg, Speichern möglich |
| T3.6 | Grenzwert genau 6 | im Bereich (i.O.) |
| T3.7 | Abschluss → Protokoll und RG_Maengel | Mangel nur für T3.1; T3.3 als i.O. mit grauem Kommentar |
| T3.8 | Grenzmodus leer lassen (alter Punkt) | wie Mangel |

## Rückweg

- Version wiederherstellen oder Vorher-Blöcke einfügen (App.Formulas zuletzt). Spalte darf bleiben.

## Anhang – Vorher-Fassungen (für den Rückweg)

Ohne Kommentare, sonst zeichengleich mit dem Export. Standardwerte sind mit „(Standard)“ markiert.

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
    (!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma);
    "NIO";
    "IO"
);;
fnHtml(t: Text): Text = Substitute(Substitute(Substitute(Substitute(Substitute(t; "&"; "&amp;"); "<"; "&lt;"); ">"; "&gt;"); """"; "&quot;"); "'"; "&#39;");;
cfgAdmins = Coalesce(LookUp(RG_Konfiguration; Title = "Admins").Wert; "");;
fnLinkAnzahl(t: Text): Number = CountRows(Filter(Split(Coalesce(t; ""); " | ") As s; Trim(s.Value) <> ""));;
fnFotoModus(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht"; f; alt; "Optional"; "Aus");;
fnBeantwortet(bew: Text; wt: Text; wz: Number): Boolean = bew <> "" || Trim(wt) <> "" || !IsBlank(wz);;
fnAusserhalb(z: Number; mi: Number; ma: Number): Boolean = !IsBlank(z) && ((!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma));;
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew; wt; wz));;
fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "")); "Wert";
    fnKommentarNoetig(typ; bew; wt; wz; kpfl; gmodus; mi; ma) && Trim(kom) = ""; "Kommentar";
    foto = "Pflicht" && fanz < 1; "Foto";
    ""
);;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma) <> "";;
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
Clear(colFotos);;
Set(varGeaendert; false);;
Set(varSchluesselK; "D" & varDurchID & "-K" & varKatID);;
Set(varNurLesen; varDurch.Status <> stInArbeit);;
Refresh(RG_KategorieErgebnisse);;
Concurrent(
    ClearCollect(colPP; Filter(RG_Pruefpunkte; KategorieID = varKatID && Aktiv = true));
    Set(varErgebnis; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK))
);;
Set(varGespeichertBeimOeffnen; varErgebnis.GespeichertAm);;
With({t: If(IsBlank(varErgebnis.Antworten); Table(ParseJSON("[]")); Table(ParseJSON(varErgebnis.Antworten)))};
    If(varNurLesen && !IsEmpty(t);
        ClearCollect(colAntworten;
            ForAll(Sequence(CountRows(t)) As i;
                With({a: Index(t; i.Value).Value};
                    With({pp: LookUp(colPP; ID = Value(a.PruefpunktID))};
                        {PruefpunktID: Value(a.PruefpunktID); Frage: Text(a.Frage); Typ: Text(a.Typ); Pflicht: false; Einheit: Coalesce(Text(a.Einheit); ""); MinWert: pp.MinWert; MaxWert: pp.MaxWert; Auswahl: Coalesce(Text(a.WertText); ""); Hinweis: ""; Reihenfolge: i.Value;
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: "Mangel"; Inaktiv: false}
                    )
                )
            )
        );
        ClearCollect(colAntworten;
            ForAll(Sort(colPP; RgReihenfolge) As p;
                With({alt: LookUp(t As j; Value(j.Value.PruefpunktID) = p.ID)};
                    {PruefpunktID: p.ID; Frage: p.Title; Typ: p.Eingabetyp.Value; Pflicht: p.Pflicht; Einheit: Coalesce(p.Einheit; ""); MinWert: p.MinWert; MaxWert: p.MaxWert; Auswahl: Coalesce(p.Auswahlwerte; ""); Hinweis: Coalesce(p.Hinweis; ""); Reihenfolge: p.RgReihenfolge;
                     Bewertung: If(IsBlank(alt); ""; p.Eingabetyp.Value = "ZAHL" && !IsBlank(alt.Value.WertZahl); fnZahlBewertung(Value(alt.Value.WertZahl); p.MinWert; p.MaxWert; "Mangel"); Coalesce(Text(alt.Value.Bewertung); ""));
                     WertText: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.WertText); ""));
                     WertZahl: If(IsBlank(alt); Blank(); Value(alt.Value.WertZahl));
                     Kommentar: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.Kommentar); ""));
                     Fotos: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.Fotos); ""));
                     FotoModus: fnFotoModus(p.Foto.Value; Coalesce(p.FotoMoeglich; false));
                     KommentarPflicht: Coalesce(p.KommentarPflicht; false);
                     Grenzmodus: "Mangel";
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Inaktiv: true}
            )
        )
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
```

**`lblKaZahlInfo.Text` vorher**

```
Trim(ThisItem.Einheit & If(IsBlank(ThisItem.MinWert) && IsBlank(ThisItem.MaxWert); ""; "  ·  Soll " & If(IsBlank(ThisItem.MinWert); ""; "ab " & ThisItem.MinWert & " ") & If(IsBlank(ThisItem.MaxWert); ""; "bis " & ThisItem.MaxWert)) & If(ThisItem.Bewertung = "NIO"; "  ·  außerhalb des Sollbereichs"; ""))
```

**`lblKaZahlInfo.Color` vorher**

```
If(ThisItem.Bewertung = "NIO"; clrFehler; clrTextGrau)
```

**`txtKaZahl.BorderColor` vorher**

```
If(ThisItem.Bewertung = "NIO"; clrFehler; clrRahmen)
```

