# Baukasten-Paket 2 – Pflicht-Kommentar auch bei i.O. (pro Prüfpunkt)

Stand: 27.10.2026 · erzeugt mit `werkzeuge/baukasten.py` aus dem Export `2026-10-27_0909`.

## Kurzfassung

- Neue Ja/Nein-Spalte **KommentarPflicht** am Prüfpunkt (Standard Nein).
- Bei Ja verlangt die App einen Kommentar, sobald der Punkt beantwortet ist – auch bei i.O. (bei n.i.O. wie bisher immer).
- „Kommentar leeren beim Speichern“ (08:44) berücksichtigt das automatisch: bei KommentarPflicht bleibt der Kommentar auch bei i.O. erhalten.
- Hinweistext im Feld: „Kommentar (Pflicht)“ bei i.O., „Kommentar zum Mangel (Pflicht)“ bei n.i.O.
- Protokoll: Kommentar bei i.O. grau, bei n.i.O. rot wie bisher. Mängel unverändert (nur n.i.O.).

## Voraussetzungen

- Paket 1 ist eingefügt, getestet und gespeichert.
- Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt.

## Schritte

### Schritt 2.1 – Sicherung

Studio: oben **Speichern**. Dann make.powerapps.com → Apps → „Rundgang DEV“ → … → **Details → Versionen**: die oberste Versionsnummer notieren. Das ist der Rückweg auf Knopfdruck (Version wiederherstellen).

### Schritt 2.2 – SharePoint-Spalte anlegen

RG_Pruefpunkte → **+ Spalte hinzufügen → Ja/Nein**: Name **KommentarPflicht**, Standardwert **Nein**.
Für den Test: siehe Vorbereitung im Testbogen (zwei Punkte PK und PN).
Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren** (sonst kennt die App die neue Spalte nicht und die Formeln in den nächsten Schritten zeigen Fehler).

### Schritt 2.3 – App.Formulas

Je Block: Steuerelement in der Strukturansicht markieren, Property oben links im Auswahlfeld wählen, in der Formelleiste **Strg+A**, dann den ganzen Block einfügen. Bis alle Blöcke dieses Pakets drin sind, können rote Fehler stehen (neue Funktionsköpfe passen erst zusammen, wenn alle Aufrufer ersetzt sind).
Nur `fnKommentarNoetig` ändert sich; der Block ist trotzdem die ganze Property.

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
fnFotoNeuErlaubt(bew: Text; foto: Text): Boolean = bew = "NIO" || foto = "Optional" || foto = "Pflicht";;
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

### Schritt 2.4 – Kategorie öffnen

`scrKategorie.OnVisible`: `KommentarPflicht` kommt jetzt aus der Spalte.

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

### Schritt 2.5 – Kommentarfeld

`conKaKarte` → `txtKaKommentar`.

**`txtKaKommentar.HintText`**

```
If(ThisItem.Bewertung = "NIO"; "Kommentar zum Mangel (Pflicht)"; "Kommentar (Pflicht)")
```

**`txtKaKommentar.AccessibleLabel`**

```
If(ThisItem.Bewertung = "NIO"; "Kommentar zum Mangel: "; "Kommentar: ") & ThisItem.Frage
```

### Schritt 2.6 – Protokoll

`scrProtokoll` → `conPrInhalt` → `htmProtokoll`, Property **HtmlText**.

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
        Concat(Table(ParseJSON(e.Antworten)) As a;
            With({b: Text(a.Value.Bewertung); k: Text(a.Value.Kommentar); fo: Text(a.Value.Fotos)};
                "<tr style='border-bottom:1px solid #DADCE5;" & If(b = "NIO"; "background:#FCE8E6;"; "") & "'>" &
                "<td style='padding:6px 8px;width:46%'>" & fnHtml(Text(a.Value.Frage)) & "</td>" &
                "<td style='padding:6px 8px;width:64px;white-space:nowrap;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; "#0F7B3F") & "'>" & Switch(b; "IO"; "i.O."; "NIO"; "n.i.O."; "") & "</td>" &
                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) &
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

### Schritt 2.7 – App-Prüfung und Speichern

Studio → **App-Prüfung → Formeln**: muss **0** sein (Barrierefreiheit/Leistung wie bisher, siehe E-07/E-08). Dann **Speichern** (noch nicht veröffentlichen) und den Test unten in der **Vorschau** machen.
Bei einem Formelfehler: Fehlermeldung und Steuerelement notieren, nicht selbst umbauen, mir schicken.

## Test

Vorbereitung in RG_Pruefpunkte, danach Daten aktualisieren und Vorschau neu starten: P10 Foto = **Optional** (sonst blockiert die Foto-Pflicht das Speichern in der Vorschau). **K2** = die Kategorie nach K1. Dort: **PK** (i.O./n.i.O., Pflicht = Ja) KommentarPflicht = **Ja**; **PN** (i.O./n.i.O., Pflicht auf **Nein** stellen) KommentarPflicht = **Ja**; **PM** = ein anderer i.O./n.i.O.-Punkt ohne KommentarPflicht.

| # | Klickfolge | erwartet |
|---|---|---|
| T2.1 | Neue Durchführung starten (oder eine, in der K1 noch offen ist). K1: alles i.O., Speichern | K2 öffnet sich automatisch |
| T2.2 | PK auf i.O. | Kommentarfeld „Kommentar (Pflicht)“, rot umrandet; Fuß nennt „<PK> (Kommentar)“ |
| T2.3 | PN unbeantwortet lassen | PN steht nicht in „Noch offen“ |
| T2.4 | PK Kommentar „sauber“ | PK nicht mehr offen |
| T2.5 | PK auf n.i.O. | Hinweis wird „Kommentar zum Mangel (Pflicht)“, „sauber“ bleibt stehen |
| T2.6 | PK zurück auf i.O. | Hinweis „Kommentar (Pflicht)“, „sauber“ steht noch |
| T2.7 | PM: n.i.O. + Kommentar „weg“, dann i.O. | Kommentarfeld von PM verschwindet |
| T2.8 | Übrige Punkte ausfüllen, Speichern | „Gespeichert.“, die nächste offene Kategorie öffnet sich (falls es eine gibt) |
| T2.9 | Zurück zur Übersicht, K2 „Bearbeiten“ | PK i.O., Kommentarfeld mit „sauber“ sichtbar |
| T2.9a | PM auf n.i.O. tippen | Kommentarfeld von PM ist **leer** (beim Speichern geleert); PM zurück auf i.O., Zurück („Verwerfen? Erneut tippen“) |
| T2.10 | Nur mit Abschluss (siehe Paket 1, B7): Protokoll | „sauber“ grau kursiv beim i.O.-Punkt; kein Mangel für PK |

Aufräumen: PN wieder Pflicht = Ja (falls vorher so), Testdaten in den Papierkorb (nur TestDatensatz = Ja).

## Rückweg

- Version wiederherstellen oder die Vorher-Blöcke einfügen (App.Formulas zuletzt).
- Die Spalte darf bleiben. Gespeicherte i.O.-Kommentare bleiben im JSON und erscheinen nach dem Rückweg im Protokoll rot (alte Darstellung). **Achtung:** Wird eine solche Kategorie nach dem Rückweg erneut gespeichert, löscht „Kommentar leeren“ die i.O.-Kommentare (die Kommentarpflicht ist dann ja weg).

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
fnFotoNeuErlaubt(bew: Text; foto: Text): Boolean = bew = "NIO" || foto = "Optional" || foto = "Pflicht";;
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

**`txtKaKommentar.HintText` vorher**

```
"Kommentar zum Mangel (Pflicht)"
```

**`txtKaKommentar.AccessibleLabel` vorher**

```
"Kommentar zum Mangel: " & ThisItem.Frage
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
            With({b: Text(a.Value.Bewertung); k: Text(a.Value.Kommentar); fo: Text(a.Value.Fotos)};
                "<tr style='border-bottom:1px solid #DADCE5;" & If(b = "NIO"; "background:#FCE8E6;"; "") & "'>" &
                "<td style='padding:6px 8px;width:46%'>" & fnHtml(Text(a.Value.Frage)) & "</td>" &
                "<td style='padding:6px 8px;width:64px;white-space:nowrap;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; "#0F7B3F") & "'>" & Switch(b; "IO"; "i.O."; "NIO"; "n.i.O."; "") & "</td>" &
                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) &
                If(IsBlank(k) || k = ""; ""; "<br><i style='color:#B3261E'>" & fnHtml(k) & "</i>") &
                If(IsBlank(fo) || fo = ""; ""; "<br>" & Concat(Split(fo; " | ") As s; "<a href='" & Trim(s.Value) & "'>Foto ›</a> ")) &
                "</td></tr>"
            )
        ) & "</table>"
    ) &
    If(IsBlank(d.ProtokollUrl); ""; "<p style='font-size:12px'>Archiv-PDF: <a href='" & d.ProtokollUrl & "'>" & fnHtml(d.Title) & ".pdf</a></p>") &
    "<p style='color:#5F6370;font-size:12px;margin-top:18px'>Erstellt mit der Rundgang-App · " & Text(varProtokollZeit; "dd.mm.yyyy hh:mm") & If(d.TestDatensatz; " · TESTDATEN"; "") & "</p></div>"
)
```

