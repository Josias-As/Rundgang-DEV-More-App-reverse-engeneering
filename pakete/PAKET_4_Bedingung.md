# Baukasten-Paket 4 – Bedingte Fragen

Stand: 27.10.2026 · erzeugt mit `werkzeuge/baukasten.py` aus dem Export `2026-10-27_0909`.

## Kurzfassung

- Zwei neue Spalten am Prüfpunkt B: **BedingungPunkt** (Id von Punkt A, gleiche Kategorie) und **BedingungWert** (z. B. NIO, IO, ein Auswahlwert, oder * = irgendeine Antwort).
- B erscheint und wird verlangt nur, wenn A den Wert hat. Sonst ist B unsichtbar, zählt nicht als offen und bekommt keine Fotos hochgeladen.
- Beim Speichern leert die App ausgeblendete Punkte (Werte, Kommentar, Foto-Links) und merkt sie im JSON als `Ausgeblendet` – keine Mängel, im Protokoll und in der Nur-Ansicht nicht sichtbar. Neue Fotos eines ausgeblendeten Punkts werden nicht hochgeladen.
- Fehlkonfiguration fällt sicher aus: A fehlt, A ist selbst bedingt (Kette), BedingungWert ist leer oder passt nicht zu A (z. B. Tippfehler, Wert, den es in A nicht gibt) → B wird immer gezeigt. Schreibweisen „i.O.“/„n.i.O.“, Groß-/Kleinschreibung und Leerzeichen sind egal.
- Zähler (x von y ausgefüllt, Balken, n.i.O.-Zahl, Noch offen, Sprung) zählen nur sichtbare Punkte.

## Voraussetzungen

- Pakete 1–3 eingefügt und getestet.
- Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt.

## Schritte

### Schritt 4.1 – Sicherung

Studio: oben **Speichern**. Dann make.powerapps.com → Apps → „Rundgang DEV“ → … → **Details → Versionen**: die oberste Versionsnummer notieren. Das ist der Rückweg auf Knopfdruck (Version wiederherstellen).

### Schritt 4.2 – SharePoint-Spalten anlegen

RG_Pruefpunkte:
- **BedingungPunkt** – Zahl, 0 Dezimalstellen, Standardwert **0** (0 = keine Bedingung)
- **BedingungWert** – Einzelne Textzeile, Standardwert leer
Gültige Bedingungswerte: bei A = i.O./n.i.O. oder Zahl: **IO** oder **NIO**; bei A = Auswahl/Mehrfachauswahl: einer der Auswahlwerte von A; bei jedem Typ: `*` (irgendeine Antwort). Bei Zahl-Punkten mit Grenzmodus Warnen ist ein Wert außerhalb „IO“ – dort Bedingungen auf NIO vermeiden.
Für den Test in K1: **A** = PX (i.O./n.i.O., Pflicht = Ja). Neuer Prüfpunkt **B** „ZZ Test Folgefrage Ursache“: TEXT, Pflicht = Ja, Aktiv = Ja, Foto = Optional, RgReihenfolge direkt hinter A, BedingungPunkt = Id von A, BedingungWert = **NIO**.
Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren** (sonst kennt die App die neue Spalte nicht und die Formeln in den nächsten Schritten zeigen Fehler).

### Schritt 4.3 – App.Formulas

Je Block: Steuerelement in der Strukturansicht markieren, Property oben links im Auswahlfeld wählen, in der Formelleiste **Strg+A**, dann den ganzen Block einfügen. Bis alle Blöcke dieses Pakets drin sind, können rote Fehler stehen (neue Funktionsköpfe passen erst zusammen, wenn alle Aufrufer ersetzt sind).
Neu: fnBedPasst, fnSichtbar.

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
fnFotoModus(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht"; f; alt; "Optional"; "Aus");;
fnFotoNeuErlaubt(bew: Text; foto: Text): Boolean = bew = "NIO" || foto = "Optional" || foto = "Pflicht";;
fnBeantwortet(bew: Text; wt: Text; wz: Number): Boolean = bew <> "" || Trim(wt) <> "" || !IsBlank(wz);;
fnAusserhalb(z: Number; mi: Number; ma: Number): Boolean = !IsBlank(z) && ((!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma));;
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz; mi; ma));;
fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "")); "Wert";
    typ = "ZAHL" && gmodus = "Sperren" && fnSperreGilt(mi; ma) && fnAusserhalb(wz; mi; ma); "Bereich";
    fnKommentarNoetig(typ; bew; wt; wz; kpfl; gmodus; mi; ma) && Trim(kom) = ""; "Kommentar";
    foto = "Pflicht" && fanz < 1; "Foto";
    ""
);;
fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w; "")); "."; ""); " "; ""));;
fnBedGueltig(w: Text; typ: Text; auswahl: Text): Boolean = With({n: fnBedNorm(w)}; n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnBedPasst(w: Text; bew: Text; wt: Text; wz: Number): Boolean = With({n: fnBedNorm(w)}; If(n = "*"; fnBeantwortet(bew; wt; wz); n = fnBedNorm(bew) || n = fnBedNorm(wt) || CountRows(Filter(Split(wt; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnSichtbar(bid: Number; w: Text; gef: Boolean; bBid: Number; bInaktiv: Boolean; bTyp: Text; bAuswahl: Text; bBew: Text; bWt: Text; bWz: Number): Boolean = bid = 0 || Trim(w) = "" || !gef || bInaktiv || bBid <> 0 || !fnBedGueltig(w; bTyp; bAuswahl) || fnBedPasst(w; bBew; bWt; bWz);;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

### Schritt 4.4 – Kategorie öffnen

`scrKategorie.OnVisible`: Felder BedID, BedWert, Ausgeblendet; Start-Sprung auf den ersten sichtbaren Punkt.

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
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); Inaktiv: false}
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
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); Inaktiv: true}
            )
        )
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
```

### Schritt 4.5 – Galerie und Zähler

Pfade: `galKaPruefpunkte` (Items) und die unsichtbaren `lblKaFehlendAnzahl`, `lblKaFehlend` liegen direkt auf `scrKategorie`; `lblKaUnter` in `conKaKopf`; `conKaBalkenWert` in `conKaBalken`; `lblKaStand` in `conKaFuss`.

**`galKaPruefpunkte.Items`**

```
Sort(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)
```

**`lblKaFehlendAnzahl.Text`**

```
CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert)))
```

**`lblKaFehlend.Text`**

```
Concat(Filter(Sort(colAntworten; Reihenfolge) As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert)) As z; z.Frage & Switch(fnFehltGrund(z.Typ; z.Pflicht; z.Bewertung; z.WertText; z.WertZahl; z.Kommentar; z.FotoModus; CountRows(Filter(colFotos; PruefpunktID = z.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(z.Fotos); z.KommentarPflicht; z.Grenzmodus; z.MinWert; z.MaxWert); "Kommentar"; " (Kommentar)"; "Foto"; " (Foto)"; "Bereich"; " (unzulässiger Wert)"; "Uhrzeit"; " (Uhrzeit)"; ""); "; ")
```

**`lblKaUnter.Text`**

```
varBereichName & "  ·  Kategorie " & varKatPos & " von " & CountRows(colKatListe) & If(varNurLesen; "  ·  nur Ansicht"; "  ·  " & (CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))) - Value(lblKaFehlendAnzahl.Text)) & " von " & CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))) & " ausgefüllt")
```

**`conKaBalkenWert.Width`**

```
Parent.Width * With({n: CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))))}; If(n = 0; 0; (n - Value(lblKaFehlendAnzahl.Text)) / n))
```

**`lblKaStand.Text`**

```
If(varNurLesen; "Nur Ansicht – der Rundgang ist nicht mehr in Arbeit."; Value(lblKaFehlendAnzahl.Text) = 0; "✓  Alles ausgefüllt" & With({n: CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && a.Bewertung = "NIO"))}; If(n > 0; " · " & n & " n.i.O."; "")); "Noch offen (" & lblKaFehlendAnzahl.Text & "): " & lblKaFehlend.Text)
```

### Schritt 4.6 – Speichern

`btnKaSpeichern.OnSelect`: Ausgeblendete leeren (inkl. Foto-Links) und markieren, vor dem Foto-Upload; Upload und Anhängen von Links nur für sichtbare Punkte; JSON mit `Ausgeblendet`.

**`btnKaSpeichern.OnSelect`**

```
If(
    Value(lblKaFehlendAnzahl.Text) > 0;
        Set(varZeigeFehlend; true);;
        Set(varSprungRec; First(Filter(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge) As a; If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert))));;
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
                IsBlank(erg) && CountRows(Filter(colKatListe As kl; kl.Position < varKatPos && IsBlank(LookUp(colErledigt As e; e.KategorieID = kl.KategorieID)))) > 0;
                    Notify("Bitte zuerst die vorherigen Kategorien abschließen."; NotificationType.Warning);
                ClearCollect(colVersteckt; ShowColumns(Filter(colAntworten As a; !a.Inaktiv && !(If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))); PruefpunktID));;
                UpdateIf(colAntworten; PruefpunktID in colVersteckt.PruefpunktID; {Bewertung: ""; WertText: ""; WertZahl: Blank(); Kommentar: ""; Fotos: ""; Ausgeblendet: true}; !Inaktiv && !(PruefpunktID in colVersteckt.PruefpunktID); {Ausgeblendet: false});;
                ClearCollect(colFotoNeu; Filter(colFotos As f0; IsBlank(f0.Url) && With({a: LookUp(colAntworten As a0; a0.PruefpunktID = f0.PruefpunktID)}; !a.Ausgeblendet && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus))));;
                ForAll(colFotoNeu As f;
                    Patch(colFotos; LookUp(colFotos; Nr = f.Nr);
                        {Url: With({ordner: fnArchivOrdner(durch.TagText; durch.TestDatensatz) & "/" & durch.Title}; If(IsError(aRG_Foto_hochladen.Run({contentBytes: f.Bild; name: f.Datei}; f.Datei; ordner; varDurchID; f.PruefpunktID; durch.TestDatensatz)); ""; fnSpUrl("RG_Fotos"; ordner & "/" & f.Datei)))})
                );;
                If(CountRows(Filter(colFotos As f1; IsBlank(f1.Url) && With({a: LookUp(colAntworten As a1; a1.PruefpunktID = f1.PruefpunktID)}; !a.Ausgeblendet && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)))) > 0;
                    Notify(CountRows(Filter(colFotos As f2; IsBlank(f2.Url) && With({a: LookUp(colAntworten As a2; a2.PruefpunktID = f2.PruefpunktID)}; !a.Ausgeblendet && fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)))) & " Foto(s) konnten nicht hochgeladen werden. Bitte „Speichern“ erneut tippen."; NotificationType.Error);
                    ForAll(Distinct(Filter(colFotos; !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID)); PruefpunktID) As d;
                        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = d.Value);
                            {Fotos: With({alt: LookUp(colAntworten; PruefpunktID = d.Value).Fotos; neu: Concat(Filter(colFotos; PruefpunktID = d.Value && !Uebernommen && !IsBlank(Url)); Url; " | ")};
                                If(IsBlank(alt); neu; alt & " | " & neu))})
                    );;
                    UpdateIf(colFotos; !Uebernommen && !IsBlank(Url); {Uebernommen: true});;
                    UpdateIf(colAntworten; !Inaktiv && !fnKommentarNoetig(Typ; Bewertung; WertText; WertZahl; KommentarPflicht; Grenzmodus; MinWert; MaxWert); {Kommentar: ""});;
                    Set(varAntwortJSON; JSON(ShowColumns(AddColumns(colAntworten; Warnung; Typ = "ZAHL" && Grenzmodus = "Warnen" && fnAusserhalb(WertZahl; MinWert; MaxWert)); PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet); JSONFormat.Compact));;
                    IfError(
                        Patch(RG_KategorieErgebnisse; If(IsBlank(erg); Defaults(RG_KategorieErgebnisse); erg);
                            {Title: varSchluesselK; DurchfuehrungID: varDurchID; TagText: durch.TagText; KategorieID: varKatID; Position: varKatPos; BereichName: varBereichName; KategorieName: varKatName; Antworten: varAntwortJSON; AnzahlNIO: CountRows(Filter(colAntworten; Bewertung = "NIO")); PrueferEmail: User().Email; PrueferName: User().FullName; GespeichertAm: Now(); TestDatensatz: durch.TestDatensatz});
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

### Schritt 4.7 – Protokoll

`htmProtokoll.HtmlText`: ausgeblendete Zeilen weglassen.

**`htmProtokoll.HtmlText`**

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
        " <span style='font-weight:400;color:#5F6370;font-size:13px'>" & fnHtml(e.BereichName) & " · " & fnHtml(e.PrueferName) & " · " & Text(e.GespeichertAm; "hh:mm") & "</span></h3>" &
        "<table style='width:100%;border-collapse:collapse;table-layout:fixed'>" &
        Concat(Filter(Table(ParseJSON(e.Antworten)); !Coalesce(IfError(Boolean(ThisRecord.Value.Ausgeblendet); false); false)) As a;
            With({b: Text(a.Value.Bewertung); k: Text(a.Value.Kommentar); fo: Text(a.Value.Fotos); w: Coalesce(IfError(Boolean(a.Value.Warnung); false); false)};
                "<tr style='border-bottom:1px solid #DADCE5;" & If(b = "NIO"; "background:#FCE8E6;"; "") & "'>" &
                "<td style='padding:6px 8px;width:46%'>" & fnHtml(Text(a.Value.Frage)) & "</td>" &
                "<td style='padding:6px 8px;width:64px;white-space:nowrap;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; w; "#9A5B00"; "#0F7B3F") & "'>" & Switch(b; "IO"; "i.O."; "NIO"; "n.i.O."; "") & "</td>" &
                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) & If(w; " <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>"; "") &
                If(IsBlank(k) || k = ""; ""; "<br><i style='color:" & If(b = "NIO"; "#B3261E"; "#5F6370") & "'>" & fnHtml(k) & "</i>") &
                If(IsBlank(fo) || fo = ""; ""; "<br>" & Concat(Split(fo; " | ") As s; "<a href='" & Trim(s.Value) & "'>Foto ›</a> ")) &
                "</td></tr>"
            )
        ) & "</table>"
    ) &
    If(IsBlank(d.ProtokollUrl); ""; "<p style='font-size:12px'>Archiv-PDF: <a href='" & d.ProtokollUrl & "'>" & fnHtml(d.Title) & ".pdf</a></p>") &
    "<p style='color:#5F6370;font-size:12px;margin-top:18px'>Erstellt mit der Rundgang-App · " & Text(varProtokollZeit; "dd.mm.yyyy hh:mm") & If(d.TestDatensatz; " · TESTDATEN"; "") & "</p></div>"
)
```

### Schritt 4.8 – App-Prüfung und Speichern

Studio → **App-Prüfung → Formeln**: muss **0** sein (Barrierefreiheit/Leistung wie bisher, siehe E-07/E-08). Dann **Speichern** (noch nicht veröffentlichen) und den Test unten in der **Vorschau** machen.
Bei einem Formelfehler: Fehlermeldung und Steuerelement notieren, nicht selbst umbauen, mir schicken.

## Test

Vorschau neu starten. Neue Durchführung (K1 noch nicht gespeichert) – sonst ist A schon gespeichert.

| # | Klickfolge | erwartet |
|---|---|---|
| T4.1 | K1 öffnen | B ist nicht zu sehen; Kopf „… von N ausgefüllt“ zählt B nicht |
| T4.2 | A auf n.i.O. | B erscheint direkt unter A; Fuß nennt A (Kommentar) und B |
| T4.3 | B Text „Leck“, an B ein Foto-Knopf (Optional) sichtbar | B nicht mehr offen |
| T4.4 | A zurück auf i.O. | B verschwindet, Liste rückt nach; Fuß ohne B |
| T4.5 | A wieder n.i.O. | B kommt mit „Leck“ zurück (noch nicht gespeichert, also nicht verloren) |
| T4.6 | A auf i.O., übrige Punkte ausfüllen, Speichern | „Gespeichert.“ |
| T4.7 | Zurück, K1 „Bearbeiten“, A auf n.i.O. | B erscheint **leer** (beim Speichern geleert) |
| T4.8 | A Kommentar „tropft“, B „Leck“, Speichern | „Gespeichert.“ |
| T4.9 | SharePoint: BedingungWert von B = **n.i.O.**; Vorschau neu starten, K1 „Bearbeiten“, A auf i.O. | B verschwindet (Schreibweise egal) |
| T4.10 | BedingungWert = **Rot**; Vorschau neu starten, K1 „Bearbeiten“ | B ist immer sichtbar (ungültiger Wert → sicherer Ausfall). Danach BedingungWert wieder **NIO** |
| T4.11 | Nur mit Abschluss (siehe Paket 1, B7), Stand T4.8: RG_Maengel, Protokoll, „Ansehen“ | Mangel nur für A; Protokoll und Nur-Ansicht zeigen B mit „Leck“ |
| T4.12 | Zweite Durchführung (anderer Tag, Nachholtag oder Testplan): K1 mit A = i.O. speichern, abschließen | Protokoll und Nur-Ansicht ohne B; kein Mangel |
| T4.13 | Eine vor Paket 4 gespeicherte Kategorie „Ansehen“ | unverändert (JSON ohne `Ausgeblendet` gilt als sichtbar) |

## Rückweg

- Version wiederherstellen oder Vorher-Blöcke einfügen (App.Formulas zuletzt).
- JSON mit `Ausgeblendet` stört die alte App nicht (Feld wird ignoriert); ausgeblendete Punkte stehen dann als leere Zeilen im Protokoll.
- Spalten dürfen bleiben; vor dem Rückweg BedingungPunkt der Testpunkte auf 0 setzen.

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
fnFotoModus(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht"; f; alt; "Optional"; "Aus");;
fnFotoNeuErlaubt(bew: Text; foto: Text): Boolean = bew = "NIO" || foto = "Optional" || foto = "Pflicht";;
fnBeantwortet(bew: Text; wt: Text; wz: Number): Boolean = bew <> "" || Trim(wt) <> "" || !IsBlank(wz);;
fnAusserhalb(z: Number; mi: Number; ma: Number): Boolean = !IsBlank(z) && ((!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma));;
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz; mi; ma));;
fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "")); "Wert";
    typ = "ZAHL" && gmodus = "Sperren" && fnSperreGilt(mi; ma) && fnAusserhalb(wz; mi; ma); "Bereich";
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

**`galKaPruefpunkte.Items` vorher**

```
Sort(Filter(colAntworten; !Inaktiv); Reihenfolge)
```

**`lblKaFehlendAnzahl.Text` vorher**

```
CountRows(Filter(colAntworten As a; !a.Inaktiv && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert)))
```

**`lblKaFehlend.Text` vorher**

```
Concat(Filter(Sort(colAntworten; Reihenfolge) As a; !a.Inaktiv && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert)) As z; z.Frage & Switch(fnFehltGrund(z.Typ; z.Pflicht; z.Bewertung; z.WertText; z.WertZahl; z.Kommentar; z.FotoModus; CountRows(Filter(colFotos; PruefpunktID = z.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(z.Fotos); z.KommentarPflicht; z.Grenzmodus; z.MinWert; z.MaxWert); "Kommentar"; " (Kommentar)"; "Foto"; " (Foto)"; "Bereich"; " (unzulässiger Wert)"; "Uhrzeit"; " (Uhrzeit)"; ""); "; ")
```

**`lblKaUnter.Text` vorher**

```
varBereichName & "  ·  Kategorie " & varKatPos & " von " & CountRows(colKatListe) & If(varNurLesen; "  ·  nur Ansicht"; "  ·  " & (CountRows(Filter(colAntworten; !Inaktiv)) - Value(lblKaFehlendAnzahl.Text)) & " von " & CountRows(Filter(colAntworten; !Inaktiv)) & " ausgefüllt")
```

**`conKaBalkenWert.Width` vorher**

```
Parent.Width * With({n: CountRows(Filter(colAntworten; !Inaktiv))}; If(n = 0; 0; (n - Value(lblKaFehlendAnzahl.Text)) / n))
```

**`lblKaStand.Text` vorher**

```
If(varNurLesen; "Nur Ansicht – der Rundgang ist nicht mehr in Arbeit."; Value(lblKaFehlendAnzahl.Text) = 0; "✓  Alles ausgefüllt" & With({n: CountRows(Filter(colAntworten; !Inaktiv && Bewertung = "NIO"))}; If(n > 0; " · " & n & " n.i.O."; "")); "Noch offen (" & lblKaFehlendAnzahl.Text & "): " & lblKaFehlend.Text)
```

**`btnKaSpeichern.OnSelect` vorher**

```
If(
    Value(lblKaFehlendAnzahl.Text) > 0;
        Set(varZeigeFehlend; true);;
        Set(varSprungRec; First(Filter(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge) As a; fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert))));;
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
                IsBlank(erg) && CountRows(Filter(colKatListe As kl; kl.Position < varKatPos && IsBlank(LookUp(colErledigt As e; e.KategorieID = kl.KategorieID)))) > 0;
                    Notify("Bitte zuerst die vorherigen Kategorien abschließen."; NotificationType.Warning);
                ClearCollect(colFotoNeu; Filter(colFotos As f0; IsBlank(f0.Url) && With({a: LookUp(colAntworten As a0; a0.PruefpunktID = f0.PruefpunktID)}; fnFotoNeuErlaubt(a.Bewertung; a.FotoModus))));;
                ForAll(colFotoNeu As f;
                    Patch(colFotos; LookUp(colFotos; Nr = f.Nr);
                        {Url: With({ordner: fnArchivOrdner(durch.TagText; durch.TestDatensatz) & "/" & durch.Title}; If(IsError(aRG_Foto_hochladen.Run({contentBytes: f.Bild; name: f.Datei}; f.Datei; ordner; varDurchID; f.PruefpunktID; durch.TestDatensatz)); ""; fnSpUrl("RG_Fotos"; ordner & "/" & f.Datei)))})
                );;
                If(CountRows(Filter(colFotos As f1; IsBlank(f1.Url) && With({a: LookUp(colAntworten As a1; a1.PruefpunktID = f1.PruefpunktID)}; fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)))) > 0;
                    Notify(CountRows(Filter(colFotos As f2; IsBlank(f2.Url) && With({a: LookUp(colAntworten As a2; a2.PruefpunktID = f2.PruefpunktID)}; fnFotoNeuErlaubt(a.Bewertung; a.FotoModus)))) & " Foto(s) konnten nicht hochgeladen werden. Bitte „Speichern“ erneut tippen."; NotificationType.Error);
                    ForAll(Distinct(Filter(colFotos; !Uebernommen && !IsBlank(Url)); PruefpunktID) As d;
                        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = d.Value);
                            {Fotos: With({alt: LookUp(colAntworten; PruefpunktID = d.Value).Fotos; neu: Concat(Filter(colFotos; PruefpunktID = d.Value && !Uebernommen && !IsBlank(Url)); Url; " | ")};
                                If(IsBlank(alt); neu; alt & " | " & neu))})
                    );;
                    UpdateIf(colFotos; !Uebernommen && !IsBlank(Url); {Uebernommen: true});;
                    UpdateIf(colAntworten; !Inaktiv && !fnKommentarNoetig(Typ; Bewertung; WertText; WertZahl; KommentarPflicht; Grenzmodus; MinWert; MaxWert); {Kommentar: ""});;
                    Set(varAntwortJSON; JSON(ShowColumns(AddColumns(colAntworten; Warnung; Typ = "ZAHL" && Grenzmodus = "Warnen" && fnAusserhalb(WertZahl; MinWert; MaxWert)); PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung); JSONFormat.Compact));;
                    IfError(
                        Patch(RG_KategorieErgebnisse; If(IsBlank(erg); Defaults(RG_KategorieErgebnisse); erg);
                            {Title: varSchluesselK; DurchfuehrungID: varDurchID; TagText: durch.TagText; KategorieID: varKatID; Position: varKatPos; BereichName: varBereichName; KategorieName: varKatName; Antworten: varAntwortJSON; AnzahlNIO: CountRows(Filter(colAntworten; Bewertung = "NIO")); PrueferEmail: User().Email; PrueferName: User().FullName; GespeichertAm: Now(); TestDatensatz: durch.TestDatensatz});
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
        " <span style='font-weight:400;color:#5F6370;font-size:13px'>" & fnHtml(e.BereichName) & " · " & fnHtml(e.PrueferName) & " · " & Text(e.GespeichertAm; "hh:mm") & "</span></h3>" &
        "<table style='width:100%;border-collapse:collapse;table-layout:fixed'>" &
        Concat(Table(ParseJSON(e.Antworten)) As a;
            With({b: Text(a.Value.Bewertung); k: Text(a.Value.Kommentar); fo: Text(a.Value.Fotos); w: Coalesce(IfError(Boolean(a.Value.Warnung); false); false)};
                "<tr style='border-bottom:1px solid #DADCE5;" & If(b = "NIO"; "background:#FCE8E6;"; "") & "'>" &
                "<td style='padding:6px 8px;width:46%'>" & fnHtml(Text(a.Value.Frage)) & "</td>" &
                "<td style='padding:6px 8px;width:64px;white-space:nowrap;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; w; "#9A5B00"; "#0F7B3F") & "'>" & Switch(b; "IO"; "i.O."; "NIO"; "n.i.O."; "") & "</td>" &
                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) & If(w; " <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>"; "") &
                If(IsBlank(k) || k = ""; ""; "<br><i style='color:" & If(b = "NIO"; "#B3261E"; "#5F6370") & "'>" & fnHtml(k) & "</i>") &
                If(IsBlank(fo) || fo = ""; ""; "<br>" & Concat(Split(fo; " | ") As s; "<a href='" & Trim(s.Value) & "'>Foto ›</a> ")) &
                "</td></tr>"
            )
        ) & "</table>"
    ) &
    If(IsBlank(d.ProtokollUrl); ""; "<p style='font-size:12px'>Archiv-PDF: <a href='" & d.ProtokollUrl & "'>" & fnHtml(d.Title) & ".pdf</a></p>") &
    "<p style='color:#5F6370;font-size:12px;margin-top:18px'>Erstellt mit der Rundgang-App · " & Text(varProtokollZeit; "dd.mm.yyyy hh:mm") & If(d.TestDatensatz; " · TESTDATEN"; "") & "</p></div>"
)
```

