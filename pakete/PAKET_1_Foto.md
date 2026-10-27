# Baukasten-Paket 1 – Foto-Modus pro Prüfpunkt (Aus / Optional / Pflicht)

Stand: 27.10.2026 · erzeugt mit `werkzeuge/baukasten.py` aus dem Export `2026-10-27_0724` **(ENTWURF: Simulation der Änderung von 08:44, vor dem Einfügen mit dem frischen Export neu erzeugen)**.

## Kurzfassung

- Neue Auswahlspalte **Foto** am Prüfpunkt: Aus, Optional, Pflicht. Leere Spalte = wie bisher (FotoMoeglich Ja → Optional, sonst Aus).
- Bei **Pflicht** lässt sich die Kategorie erst mit mindestens einem Foto speichern („Noch offen: … (Foto)“, Sprung, rote Karte).
- Der Fehler „FotoMoeglich kam aus colAntworten nicht an“ ist an der Ursache behoben: Der Bearbeiten-Zweig in `scrKategorie.OnVisible` legte das Feld nicht an. Jetzt haben alle drei Zweige dieselben Felder (maschinell geprüft). Kein `LookUp(colPP; …)` mehr nötig.
- Grundlage für Paket 2 und 3: die Prüfregel steckt in einer Funktion (`fnFehltGrund`), die Antworten tragen schon die Felder `KommentarPflicht` und `Grenzmodus` (vorerst fest: aus / Mangel). Am Verhalten ändert das nichts.
- Nebenbei: Foto-Knopf blau statt rot, wenn der Punkt nicht n.i.O. ist; ✕ im Foto-Fenster liegt nicht mehr unter dem Bild; Knopftext „Foto aufnehmen / auswählen“ normal groß; in der Nur-Ansicht erscheint der Foto-Knopf nur, wenn wirklich Fotos gespeichert sind.

## Voraussetzungen

- Frischer Export nach dem Stand von 27.10. 08:44 eingelesen (dieses Dokument wurde daraus erzeugt, siehe Kopfzeile).
- Die App ist gespeichert, nichts halb eingefügt.

## Schritte

### Schritt 1.1 – Sicherung

Studio: oben **Speichern**. Dann make.powerapps.com → Apps → „Rundgang DEV“ → … → **Details → Versionen**: die oberste Versionsnummer notieren. Das ist der Rückweg auf Knopfdruck (Version wiederherstellen).

### Schritt 1.2 – SharePoint-Spalte anlegen

IMS+ → Liste **RG_Pruefpunkte** → **+ Spalte hinzufügen → Auswahl**:
- Name: **Foto** (genau so)
- Auswahlmöglichkeiten (je eine Zeile): **Aus**, **Optional**, **Pflicht**
- Standardwert: **Aus** · Mehrfachauswahl: **Nein** · Werte erforderlich: **Nein**
- **FotoMoeglich nicht löschen und nicht umbenennen.** Vorhandene Zeilen bleiben leer, die App liest leer wie bisher.
Für den Test: Prüfpunkt **Id 10** (Thermometer) → Foto = **Pflicht**. Einen zweiten i.O./n.i.O.-Punkt derselben Kategorie → Foto = **Optional**.
Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren** (sonst kennt die App die neue Spalte nicht und die Formeln in den nächsten Schritten zeigen Fehler).

### Schritt 1.3 – App.Formulas

Je Block: Steuerelement in der Strukturansicht markieren, Property oben links im Auswahlfeld wählen, in der Formelleiste **Strg+A**, dann den ganzen Block einfügen. Bis alle Blöcke dieses Pakets drin sind, können rote Fehler stehen (neue Funktionsköpfe passen erst zusammen, wenn alle Aufrufer ersetzt sind).
`App` markieren, Property **Formulas**. Ganzer Inhalt wird ersetzt (neu: fnLinkAnzahl, fnFotoModus, fnBeantwortet, fnAusserhalb, fnKommentarNoetig, fnFehltGrund; fnFehlt mit 12 Werten; fnZahlBewertung mit 4. Wert).

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
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO";;
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

### Schritt 1.4 – Kategorie öffnen: Felder der Antworten

`scrKategorie` markieren, Property **OnVisible**.

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
                     KommentarPflicht: false;
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

### Schritt 1.5 – Zahlenfeld

**`txtKaZahl.OnChange`**

```
With({z: IfError(Value(Self.Text); Blank())};
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; Bewertung: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus))})
);;
Set(varGeaendert; true)
```

### Schritt 1.6 – Karte, Kommentar und Foto-Knopf

Alle Steuerelemente liegen in `galKaPruefpunkte` → `conKaKarte` (Karte) bzw. direkt in der Galerievorlage (`lblKaAbstand`).

**`conKaKarte.BorderColor`**

```
If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos); ThisItem.KommentarPflicht; ThisItem.Grenzmodus; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; clrRahmen)
```

**`conKaKarte.BorderThickness`**

```
If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos); ThisItem.KommentarPflicht; ThisItem.Grenzmodus; ThisItem.MinWert; ThisItem.MaxWert)); 2; 1)
```

**`conKaKarte.Height`**

```
54 + If(ThisItem.Hinweis <> ""; 24; 0) + 56 + If(txtKaKommentar.Visible || btnKaFoto.Visible; 68; 0) + 20
```

**`lblKaAbstand.Y`**

```
conKaKarte.Y + conKaKarte.Height
```

**`txtKaKommentar.Visible`**

```
If(varNurLesen; Trim(ThisItem.Kommentar) <> "" || ThisItem.Bewertung = "NIO"; fnKommentarNoetig(ThisItem.Typ; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.KommentarPflicht; ThisItem.Grenzmodus; ThisItem.MinWert; ThisItem.MaxWert))
```

**`btnKaFoto.Visible`**

```
If(varNurLesen; fnLinkAnzahl(ThisItem.Fotos) > 0; ThisItem.Bewertung = "NIO" || ThisItem.FotoModus <> "Aus")
```

**`btnKaFoto.Y`**

```
54 + If(ThisItem.Hinweis <> ""; 24; 0) + 68
```

**`btnKaFoto.Text`**

```
With({n: CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos)};
    "📷 Foto" & If(n > 0; " (" & n & ")"; If(ThisItem.FotoModus = "Pflicht" && !varNurLesen; " *"; ""))
)
```

**`btnKaFoto.BorderColor`**

```
If(ThisItem.Bewertung = "NIO"; clrFehler; clrPrimaer)
```

**`btnKaFoto.Color`**

```
If(ThisItem.Bewertung = "NIO"; clrFehler; clrPrimaer)
```

**`btnKaFoto.HoverColor`**

```
Self.Color
```

**`btnKaFoto.PressedColor`**

```
Self.Color
```

**`btnKaFoto.HoverFill`**

```
If(ThisItem.Bewertung = "NIO"; clrFehlerHell; clrPrimaerHell)
```

**`btnKaFoto.PressedFill`**

```
If(ThisItem.Bewertung = "NIO"; clrFehlerHell; clrPrimaerHell)
```

Prüfen nach dem Schritt:
- Karte eines Punkts mit Foto = Pflicht ist höher und zeigt rechts unten „📷 Foto *“ (blau).
- Y von `btnKaFoto` steht als Formel da, nicht als Zahl (E-05).

### Schritt 1.7 – Zähler „Noch offen“ (unsichtbare Labels)

`lblKaFehlendAnzahl` und `lblKaFehlend` liegen direkt auf `scrKategorie` (unsichtbar).

**`lblKaFehlendAnzahl.Text`**

```
CountRows(Filter(colAntworten As a; !a.Inaktiv && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert)))
```

**`lblKaFehlend.Text`**

```
Concat(Filter(Sort(colAntworten; Reihenfolge) As a; !a.Inaktiv && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert)) As z; z.Frage & Switch(fnFehltGrund(z.Typ; z.Pflicht; z.Bewertung; z.WertText; z.WertZahl; z.Kommentar; z.FotoModus; CountRows(Filter(colFotos; PruefpunktID = z.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(z.Fotos); z.KommentarPflicht; z.Grenzmodus; z.MinWert; z.MaxWert); "Kommentar"; " (Kommentar)"; "Foto"; " (Foto)"; "Bereich"; " (unzulässiger Wert)"; "Uhrzeit"; " (Uhrzeit)"; ""); "; ")
```

### Schritt 1.8 – Speichern

`conKaFuss` → `btnKaSpeichern`, Property **OnSelect**. Gegenüber vorher: Sprung zum ersten offenen Punkt mit der neuen Prüfregel, Upload-Bedingung liest `FotoModus` (statt `LookUp(colPP; …).FotoMoeglich`), „Kommentar leeren“ (08:44) über `fnKommentarNoetig` (heute gleiches Ergebnis: nur bei n.i.O. bleibt der Kommentar). Kommentare im alten Code entfallen.

**`btnKaSpeichern.OnSelect`**

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
                ClearCollect(colFotoNeu; Filter(colFotos As f0; IsBlank(f0.Url) && With({a: LookUp(colAntworten As a0; a0.PruefpunktID = f0.PruefpunktID)}; a.Bewertung = "NIO" || a.FotoModus <> "Aus")));;
                ForAll(colFotoNeu As f;
                    Patch(colFotos; LookUp(colFotos; Nr = f.Nr);
                        {Url: With({ordner: fnArchivOrdner(durch.TagText; durch.TestDatensatz) & "/" & durch.Title}; If(IsError(aRG_Foto_hochladen.Run({contentBytes: f.Bild; name: f.Datei}; f.Datei; ordner; varDurchID; f.PruefpunktID; durch.TestDatensatz)); ""; fnSpUrl("RG_Fotos"; ordner & "/" & f.Datei)))})
                );;
                If(CountRows(Filter(colFotos As f1; IsBlank(f1.Url) && With({a: LookUp(colAntworten As a1; a1.PruefpunktID = f1.PruefpunktID)}; a.Bewertung = "NIO" || a.FotoModus <> "Aus"))) > 0;
                    Notify(CountRows(Filter(colFotos As f2; IsBlank(f2.Url) && With({a: LookUp(colAntworten As a2; a2.PruefpunktID = f2.PruefpunktID)}; a.Bewertung = "NIO" || a.FotoModus <> "Aus"))) & " Foto(s) konnten nicht hochgeladen werden. Bitte „Speichern“ erneut tippen."; NotificationType.Error);
                    ForAll(Distinct(Filter(colFotos; !Uebernommen && !IsBlank(Url)); PruefpunktID) As d;
                        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = d.Value);
                            {Fotos: With({alt: LookUp(colAntworten; PruefpunktID = d.Value).Fotos; neu: Concat(Filter(colFotos; PruefpunktID = d.Value && !Uebernommen && !IsBlank(Url)); Url; " | ")};
                                If(IsBlank(alt); neu; alt & " | " & neu))})
                    );;
                    UpdateIf(colFotos; !Uebernommen && !IsBlank(Url); {Uebernommen: true});;
                    UpdateIf(colAntworten; !fnKommentarNoetig(Typ; Bewertung; WertText; WertZahl; KommentarPflicht; Grenzmodus; MinWert; MaxWert); {Kommentar: ""});;
                    Set(varAntwortJSON; JSON(ShowColumns(colAntworten; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos); JSONFormat.Compact));;
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

### Schritt 1.9 – Foto-Fenster

`conKaFoto` → `conKaFotoKarte` → `lblKaFotoHinweis`, `addKaFoto`, und in `galKaFotoNeu` das Bild `imgKaFotoNeu` (Bild beginnt unter dem ✕-Knopf, damit das ✕ immer tippbar ist, egal wie die Ebenen liegen).

**`lblKaFotoHinweis.Text`**

```
If(LookUp(colAntworten; PruefpunktID = varFotoPP).FotoModus = "Pflicht"; "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren."; "Keine Personen fotografieren. Fotos werden beim „Speichern“ hochgeladen.")
```

**`addKaFoto.Size`**

```
18
```

**`imgKaFotoNeu.Y`**

```
52
```

**`imgKaFotoNeu.Height`**

```
Parent.TemplateHeight - 60
```

### Schritt 1.10 – App-Prüfung und Speichern

Studio → **App-Prüfung → Formeln**: muss **0** sein (Barrierefreiheit/Leistung wie bisher, siehe E-07/E-08). Dann **Speichern** (noch nicht veröffentlichen) und den Test unten in der **Vorschau** machen.
Bei einem Formelfehler: Fehlermeldung und Steuerelement notieren, nicht selbst umbauen, mir schicken.

## Test

Zeitachse in der Studio-Vorschau mit dem Test-Rundgang „ZZ Test Objektrundgang TCC“ (Tag mit Plan oder Nachholtag; laufende Durchführung D13 darf fortgesetzt werden). Foto-Auswahl selbst testet Josias am Tablet (die Datei-Auswahl der Vorschau ist für die Automation nicht bedienbar).

| # | Klickfolge | erwartet |
|---|---|---|
| T1.1 | Kategorie 1 öffnen | Thermometer-Karte: „📷 Foto *“ blau umrandet, Karte höher. Optional-Punkt: „📷 Foto“. Übrige Punkte: kein Foto-Knopf. |
| T1.2 | Alle Punkte ausfüllen, kein Foto | Fuß: „Noch offen (1): ZZ Test Thermometer … (Foto)“, Knopf „Offene Punkte ↓“ |
| T1.3 | „Offene Punkte ↓“ tippen | Liste springt zur Thermometer-Karte, Karte rot umrandet |
| T1.4 | Foto-Knopf tippen | Fenster: Hinweis „Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren.“ einzeilig, Knopf „Foto aufnehmen / auswählen“ normal groß |
| T1.5 | (Tablet) Foto wählen, ✕ antippen, erneut wählen, „Fertig“ | ✕ entfernt das Foto; danach Knopf „📷 Foto (1)“, Fuß „✓ Alles ausgefüllt“ |
| T1.6 | Einen anderen Punkt auf n.i.O. | Kommentarfeld links, roter „📷 Foto“ rechts in einer Zeile; zurück auf i.O. → beides weg, Karte wieder niedrig |
| T1.7 | n.i.O. + Kommentar „test“ → wieder i.O. → Speichern | „Gespeichert.“; nächste Kategorie öffnet sich. (08:44-Verhalten: Kommentar wird nicht gespeichert) |
| T1.8 | (Tablet) Bibliothek RG_Fotos → TEST/2026/10/R…/ | Datei `D…-K…-P10-xxxxxxxx.jpg` vorhanden |
| T1.9 | Kategorie 1 wieder öffnen (Bearbeiten) | Thermometer „📷 Foto (1)“ ohne „*“; Speichern ohne neues Foto möglich |
| T1.10 | Prüfpunkt Id 10: Foto leer lassen, FotoMoeglich = Ja; Kategorie neu öffnen | verhält sich wie Optional (Knopf da, nicht Pflicht) |
| T1.11 | Rundgang abschließen → Ansehen → Kategorie 1 | Nur-Ansicht: Thermometer zeigt „📷 Foto (1)“ (öffnet die gespeicherten Fotos); n.i.O.-Punkt ohne Foto zeigt keinen Foto-Knopf; Kommentar sichtbar, wo einer gespeichert ist |
| T1.12 | Protokoll | wie bisher; T1.7-Punkt ohne Kommentar |

Danach: Foto bei Id 10 wieder auf den gewünschten Wert setzen. Testdaten wie gewohnt aufräumen (Papierkorb, nur TestDatensatz = Ja).

## Rückweg

- **Am schnellsten:** make.powerapps.com → Details → Versionen → notierte Version **Wiederherstellen**.
- **Einzeln:** die Vorher-Blöcke aus dem Anhang einfügen, zuerst alle Steuerelemente, **App.Formulas zuletzt**. Danach App-Prüfung = 0.
- Die Spalte **Foto** kann stehen bleiben (die alte App liest sie nicht). Gespeicherte Ergebnisse sind nicht betroffen (das JSON hat kein neues Feld).

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
fnZahlBewertung(z: Number; mi: Number; ma: Number): Text = If(
    (!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma);
    "NIO";
    "IO"
);;
fnHtml(t: Text): Text = Substitute(Substitute(Substitute(Substitute(Substitute(t; "&"; "&amp;"); "<"; "&lt;"); ">"; "&gt;"); """"; "&quot;"); "'"; "&#39;");;
cfgAdmins = Coalesce(LookUp(RG_Konfiguration; Title = "Admins").Wert; "");;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text): Boolean = (pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = ""))) || (bew = "NIO" && Trim(kom) = "");;
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
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoMoeglich: Coalesce(pp.FotoMoeglich; false); Inaktiv: false}
                    )
                )
            )
        );
        ClearCollect(colAntworten;
            ForAll(Sort(colPP; RgReihenfolge) As p;
                With({alt: LookUp(t As j; Value(j.Value.PruefpunktID) = p.ID)};
                    {PruefpunktID: p.ID; Frage: p.Title; Typ: p.Eingabetyp.Value; Pflicht: p.Pflicht; Einheit: Coalesce(p.Einheit; ""); MinWert: p.MinWert; MaxWert: p.MaxWert; Auswahl: Coalesce(p.Auswahlwerte; ""); Hinweis: Coalesce(p.Hinweis; ""); Reihenfolge: p.RgReihenfolge;
                     Bewertung: If(IsBlank(alt); ""; p.Eingabetyp.Value = "ZAHL" && !IsBlank(alt.Value.WertZahl); fnZahlBewertung(Value(alt.Value.WertZahl); p.MinWert; p.MaxWert); Coalesce(Text(alt.Value.Bewertung); ""));
                     WertText: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.WertText); ""));
                     WertZahl: If(IsBlank(alt); Blank(); Value(alt.Value.WertZahl));
                     Kommentar: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.Kommentar); ""));
                     Fotos: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.Fotos); ""));
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoMoeglich: false; Inaktiv: true}
            )
        )
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
```

**`txtKaZahl.OnChange` vorher**

```
With({z: IfError(Value(Self.Text); Blank())};
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; Bewertung: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert))})
);;
Set(varGeaendert; true)
```

**`conKaKarte.BorderColor` vorher**

```
If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar)); clrFehler; clrRahmen)
```

**`conKaKarte.BorderThickness` vorher**

```
If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar)); 2; 1)
```

**`conKaKarte.Height` vorher**

```
54 + If(ThisItem.Hinweis <> ""; 24; 0) + 56 + If(ThisItem.Bewertung = "NIO"; 68; If(Coalesce(LookUp(colPP; ID = ThisItem.PruefpunktID).FotoMoeglich; false); 64; 0)) + 20
```

**`lblKaAbstand.Y` vorher**

```
8 + 54 + If(ThisItem.Hinweis <> ""; 24; 0) + 56 + If(ThisItem.Bewertung = "NIO"; 68; 0) + 20
```

**`txtKaKommentar.Visible` vorher**

```
ThisItem.Bewertung = "NIO"
```

**`btnKaFoto.Visible` vorher**

```
ThisItem.Bewertung = "NIO" || Coalesce(LookUp(colPP; ID = ThisItem.PruefpunktID).FotoMoeglich; false)
```

**`btnKaFoto.Y` vorher**

```
54 + If(ThisItem.Hinweis <> ""; 24; 0) + If(ThisItem.Bewertung = "NIO"; 68; 56)
```

**`btnKaFoto.Text` vorher**

```
With({n: CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID)) + If(IsBlank(ThisItem.Fotos); 0; CountRows(Split(ThisItem.Fotos; " | ")))};
    "📷 Foto" & If(n > 0; " (" & n & ")"; "")
)
```

**`btnKaFoto.BorderColor` vorher**

```
clrFehler
```

**`btnKaFoto.Color` vorher**

```
clrFehler
```

**`btnKaFoto.HoverColor` vorher**

```
clrFehler
```

**`btnKaFoto.PressedColor` vorher**

```
clrFehler
```

**`btnKaFoto.HoverFill` vorher**

```
clrFehlerHell
```

**`btnKaFoto.PressedFill` vorher**

```
clrFehlerHell
```

**`lblKaFehlendAnzahl.Text` vorher**

```
CountRows(Filter(colAntworten; !Inaktiv && fnFehlt(Typ; Pflicht; Bewertung; WertText; WertZahl; Kommentar)))
```

**`lblKaFehlend.Text` vorher**

```
Concat(Filter(Sort(colAntworten; Reihenfolge); !Inaktiv && fnFehlt(Typ; Pflicht; Bewertung; WertText; WertZahl; Kommentar)); Frage & If(Bewertung = "NIO" && Trim(Kommentar) = ""; " (Kommentar)"; ""); "; ")
```

**`btnKaSpeichern.OnSelect` vorher**

```
If(
    Value(lblKaFehlendAnzahl.Text) > 0;
        Set(varZeigeFehlend; true);;
        Set(varSprungRec; First(Filter(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge); fnFehlt(Typ; Pflicht; Bewertung; WertText; WertZahl; Kommentar))));;
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
                ClearCollect(colFotoNeu; Filter(colFotos As f0; IsBlank(f0.Url) && With({a: LookUp(colAntworten As a0; a0.PruefpunktID = f0.PruefpunktID)}; a.Bewertung = "NIO" || Coalesce(LookUp(colPP; ID = a.PruefpunktID).FotoMoeglich; false))));;
                ForAll(colFotoNeu As f;
                    Patch(colFotos; LookUp(colFotos; Nr = f.Nr);
                        {Url: With({ordner: fnArchivOrdner(durch.TagText; durch.TestDatensatz) & "/" & durch.Title}; If(IsError(aRG_Foto_hochladen.Run({contentBytes: f.Bild; name: f.Datei}; f.Datei; ordner; varDurchID; f.PruefpunktID; durch.TestDatensatz)); ""; fnSpUrl("RG_Fotos"; ordner & "/" & f.Datei)))})
                );;
                If(CountRows(Filter(colFotos As f1; IsBlank(f1.Url) && With({a: LookUp(colAntworten As a1; a1.PruefpunktID = f1.PruefpunktID)}; a.Bewertung = "NIO" || Coalesce(LookUp(colPP; ID = a.PruefpunktID).FotoMoeglich; false)))) > 0;
                    Notify(CountRows(Filter(colFotos As f2; IsBlank(f2.Url) && With({a: LookUp(colAntworten As a2; a2.PruefpunktID = f2.PruefpunktID)}; a.Bewertung = "NIO" || Coalesce(LookUp(colPP; ID = a.PruefpunktID).FotoMoeglich; false)))) & " Foto(s) konnten nicht hochgeladen werden. Bitte „Speichern“ erneut tippen."; NotificationType.Error);
                    ForAll(Distinct(Filter(colFotos; !Uebernommen && !IsBlank(Url)); PruefpunktID) As d;
                        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = d.Value);
                            {Fotos: With({alt: LookUp(colAntworten; PruefpunktID = d.Value).Fotos; neu: Concat(Filter(colFotos; PruefpunktID = d.Value && !Uebernommen && !IsBlank(Url)); Url; " | ")};
                                If(IsBlank(alt); neu; alt & " | " & neu))})
                    );;
                    UpdateIf(colFotos; !Uebernommen && !IsBlank(Url); {Uebernommen: true});;
                    UpdateIf(colAntworten; Bewertung <> "NIO"; {Kommentar: ""});;
                    Set(varAntwortJSON; JSON(ShowColumns(colAntworten; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos); JSONFormat.Compact));;
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

**`lblKaFotoHinweis.Text` vorher**

```
"Bitte keine Personen fotografieren. Neue Fotos werden beim „Speichern“ hochgeladen."
```

**`addKaFoto.Size` vorher**

```
25
```

**`imgKaFotoNeu.Y`** (Standard): `0`

**`imgKaFotoNeu.Height` vorher**

```
Parent.TemplateHeight - 8
```

