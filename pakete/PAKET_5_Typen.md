# Baukasten-Paket 5 – Neue Typen: Mehrfachauswahl, Datum, Datum + Uhrzeit

Stand: 27.10.2026 · erzeugt mit `werkzeuge/baukasten.py` aus dem Export `2026-10-27_0909`.

## Kurzfassung

- Eingabetyp bekommt drei neue Werte: **MEHRFACH**, **DATUM**, **DATUMZEIT**.
- MEHRFACH: Kombinationsfeld mit den Auswahlwerten (wie AUSWAHL, Trennzeichen „;“), mehrere wählbar, gespeichert als „Wert1; Wert2“.
- DATUM: Datumsauswahl, gespeichert als „TT.MM.JJJJ“. DATUMZEIT: dazu Stunde und Minute, gespeichert als „TT.MM.JJJJ hh:mm“.
- Pflicht wie bei anderen Typen; „nur Datum ohne Uhrzeit“ zählt bei DATUMZEIT immer als offen („(Uhrzeit)“).
- Protokoll und Mängel zeigen den Text so, wie er gespeichert ist – dort ändert sich nichts. Bedingungen (Paket 4) können auf einen Wert der Mehrfachauswahl zeigen.

## Voraussetzungen

- Pakete 1–4 eingefügt und getestet.
- Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt.

## Schritte

### Schritt 5.1 – Sicherung

Studio: oben **Speichern**. Dann make.powerapps.com → Apps → „Rundgang DEV“ → … → **Details → Versionen**: die oberste Versionsnummer notieren. Das ist der Rückweg auf Knopfdruck (Version wiederherstellen).

### Schritt 5.2 – SharePoint: Auswahlwerte ergänzen

RG_Pruefpunkte → Spalte **Eingabetyp** → Spalteneinstellungen → Bearbeiten → Auswahlmöglichkeiten **ergänzen** (nichts umbenennen oder löschen): **MEHRFACH**, **DATUM**, **DATUMZEIT**. Standardwert unverändert lassen.
Pflegeregel: den Typ eines schon benutzten Prüfpunkts nicht ändern (alte Antworten passen nicht zum neuen Typ), sondern einen neuen Punkt anlegen und den alten deaktivieren.
Für den Test in K1: drei neue Prüfpunkte (Pflicht = Ja): **M** „ZZ Test Mängelarten“ MEHRFACH mit Auswahlwerte `Riss;Leck;Korrosion`, **D** „ZZ Test Datum letzte Wartung“ DATUM, **DZ** „ZZ Test Ablesezeit“ DATUMZEIT. Dazu **F** „ZZ Test Folge Leck“ (TEXT, Pflicht = Ja) mit BedingungPunkt = Id von M, BedingungWert = **Leck**.
Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren** (damit die App die neuen Auswahlwerte kennt).

### Schritt 5.3 – App.Formulas

Je Block: Steuerelement in der Strukturansicht markieren, Property oben links im Auswahlfeld wählen, in der Formelleiste **Strg+A**, dann den ganzen Block einfügen. Bis alle Blöcke dieses Pakets drin sind, können rote Fehler stehen (neue Funktionsköpfe passen erst zusammen, wenn alle Aufrufer ersetzt sind).
fnFehltGrund kennt die neuen Typen, neu: fnDatumText.

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
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATUMZEIT") && wt = "")); "Wert";
    typ = "DATUMZEIT" && wt <> "" && Len(wt) < 16; "Uhrzeit";
    typ = "ZAHL" && gmodus = "Sperren" && fnSperreGilt(mi; ma) && fnAusserhalb(wz; mi; ma); "Bereich";
    fnKommentarNoetig(typ; bew; wt; wz; kpfl; gmodus; mi; ma) && Trim(kom) = ""; "Kommentar";
    foto = "Pflicht" && fanz < 1; "Foto";
    ""
);;
fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w; "")); "."; ""); " "; ""));;
fnBedGueltig(w: Text; typ: Text; auswahl: Text): Boolean = With({n: fnBedNorm(w)}; n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnBedPasst(w: Text; bew: Text; wt: Text; wz: Number): Boolean = With({n: fnBedNorm(w)}; If(n = "*"; fnBeantwortet(bew; wt; wz); n = fnBedNorm(bew) || n = fnBedNorm(wt) || CountRows(Filter(Split(wt; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnSichtbar(bid: Number; w: Text; gef: Boolean; bBid: Number; bInaktiv: Boolean; bTyp: Text; bAuswahl: Text; bBew: Text; bWt: Text; bWz: Number): Boolean = bid = 0 || Trim(w) = "" || !gef || bInaktiv || bBid <> 0 || !fnBedGueltig(w; bTyp; bAuswahl) || fnBedPasst(w; bBew; bWt; bWz);;
fnDatumText(d: Date; h: Text; m: Text; mitZeit: Boolean): Text = If(IsBlank(d); ""; Text(d; "dd.mm.yyyy") & If(mitZeit && h <> "" && m <> ""; " " & h & ":" & m; ""));;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

### Schritt 5.4 – Datum, Uhrzeit und Leeren-Knopf (YAML)

In der Strukturansicht in `conKaKarte` das Steuerelement `txtKaText` markieren, dann den YAML-Block mit **Strg+V** einfügen (landet in derselben Karte). Drei Blöcke nacheinander oder zusammen.

**YAML `dpKaDatum`** (englische Schreibweise, so wie es ist einfügen):

```yaml
- dpKaDatum:
    Control: Classic/DatePicker@2.6.0
    Properties:
      AccessibleLabel: |-
        ="Datum: " & ThisItem.Frage
      BorderColor: =clrRahmen
      Color: =clrText
      DefaultDate: =If(Len(ThisItem.WertText) >= 10, IfError(DateValue(Left(ThisItem.WertText, 10), "de-DE"), Blank()), Blank())
      DisplayMode: =If(varNurLesen, DisplayMode.View, DisplayMode.Edit)
      Font: =Font.'Segoe UI'
      Height: =56
      IconBackground: =clrPrimaer
      IconFill: =Color.White
      InputTextPlaceholder: ="Datum wählen"
      OnChange: |-
        =Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: fnDatumText(Self.SelectedDate, Coalesce(ddKaStunde.Selected.Value, ""), Coalesce(ddKaMinute.Selected.Value, ""), ThisItem.Typ = "DATUMZEIT")});
        Set(varGeaendert, true)
      Size: =16
      StartOfWeek: =StartOfWeek.Monday
      Visible: =ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT"
      Width: =240
      X: =20
      Y: =54 + If(ThisItem.Hinweis <> "", 24, 0)
```

**YAML `ddKaStunde`** (englische Schreibweise, so wie es ist einfügen):

```yaml
- ddKaStunde:
    Control: Classic/DropDown@2.3.1
    Properties:
      AccessibleLabel: |-
        ="Stunde: " & ThisItem.Frage
      AllowEmptySelection: =true
      BorderColor: =clrRahmen
      ChevronBackground: =clrPrimaer
      ChevronFill: =Color.White
      ChevronHoverBackground: =ColorFade(clrPrimaer, -20%)
      ChevronHoverFill: =Color.White
      Color: =clrText
      Default: =If(Len(ThisItem.WertText) >= 16, Mid(ThisItem.WertText, 12, 2), "")
      DisplayMode: =If(varNurLesen, DisplayMode.View, IsBlank(dpKaDatum.SelectedDate), DisplayMode.Disabled, DisplayMode.Edit)
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =56
      HoverFill: =clrPrimaerHell
      Items: |-
        =ForAll(Sequence(24, 0) As s, {Value: Text(s.Value, "00")})
      Items.Value: =Value
      OnChange: |-
        =Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: fnDatumText(dpKaDatum.SelectedDate, Coalesce(Self.Selected.Value, ""), Coalesce(ddKaMinute.Selected.Value, ""), ThisItem.Typ = "DATUMZEIT")});
        Set(varGeaendert, true)
      PaddingLeft: =12
      PressedColor: =Color.White
      PressedFill: =clrPrimaer
      SelectionColor: =Color.White
      SelectionFill: =clrPrimaer
      Size: =16
      Visible: =ThisItem.Typ = "DATUMZEIT"
      Width: =104
      X: =272
      Y: =54 + If(ThisItem.Hinweis <> "", 24, 0)
```

**YAML `ddKaMinute`** (englische Schreibweise, so wie es ist einfügen):

```yaml
- ddKaMinute:
    Control: Classic/DropDown@2.3.1
    Properties:
      AccessibleLabel: |-
        ="Minute: " & ThisItem.Frage
      AllowEmptySelection: =true
      BorderColor: =clrRahmen
      ChevronBackground: =clrPrimaer
      ChevronFill: =Color.White
      ChevronHoverBackground: =ColorFade(clrPrimaer, -20%)
      ChevronHoverFill: =Color.White
      Color: =clrText
      Default: =If(Len(ThisItem.WertText) >= 16, Mid(ThisItem.WertText, 15, 2), "")
      DisplayMode: =If(varNurLesen, DisplayMode.View, IsBlank(dpKaDatum.SelectedDate), DisplayMode.Disabled, DisplayMode.Edit)
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =56
      HoverFill: =clrPrimaerHell
      Items: |-
        =ForAll(Sequence(60, 0) As s, {Value: Text(s.Value, "00")})
      Items.Value: =Value
      OnChange: |-
        =Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: fnDatumText(dpKaDatum.SelectedDate, Coalesce(ddKaStunde.Selected.Value, ""), Coalesce(Self.Selected.Value, ""), ThisItem.Typ = "DATUMZEIT")});
        Set(varGeaendert, true)
      PaddingLeft: =12
      PressedColor: =Color.White
      PressedFill: =clrPrimaer
      SelectionColor: =Color.White
      SelectionFill: =clrPrimaer
      Size: =16
      Visible: =ThisItem.Typ = "DATUMZEIT"
      Width: =104
      X: =388
      Y: =54 + If(ThisItem.Hinweis <> "", 24, 0)
```

**YAML `btnKaDatumLeeren`** (englische Schreibweise, so wie es ist einfügen):

```yaml
- btnKaDatumLeeren:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrRahmen
      BorderThickness: =1
      Color: =clrTextGrau
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =56
      HoverColor: =clrText
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: ""});
        Reset(dpKaDatum);
        Reset(ddKaStunde);
        Reset(ddKaMinute);
        Set(varGeaendert, true)
      PressedColor: =clrText
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =8
      RadiusBottomRight: =8
      RadiusTopLeft: =8
      RadiusTopRight: =8
      Size: =16
      Text: ="✕"
      Visible: =!varNurLesen && (ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && ThisItem.WertText <> ""
      Width: =56
      X: =If(ThisItem.Typ = "DATUMZEIT", 504, 272)
      Y: =54 + If(ThisItem.Hinweis <> "", 24, 0)
```

Prüfen nach dem Schritt:
- Alle vier liegen in `conKaKarte` (Strukturansicht).
- Y steht als Formel `54 + If(ThisItem.Hinweis <> ""; 24; 0)` da, nicht als Zahl (E-05) – sonst per Formelleiste setzen.
- Die Namen sind genau `dpKaDatum`, `ddKaStunde`, `ddKaMinute`, `btnKaDatumLeeren` (Studio hängt bei Doppelungen „_1“ an).

### Schritt 5.5 – Mehrfachauswahl (Kombinationsfeld über das Menü)

Für das klassische Kombinationsfeld kenne ich die Steuerelement-Version in dieser Umgebung nicht sicher, deshalb ohne YAML:
1. Strukturansicht: `conKaKarte` markieren.
2. **Einfügen → Klassisch → Kombinationsfeld** (nicht das moderne Kombinationsfeld unter „Eingabe“). Es muss **in** `conKaKarte` landen.
3. Umbenennen in **cboKaMehrfach**.
4. Die folgenden Properties setzen (je ganze Property ersetzen):

Properties von `cboKaMehrfach` (Formelleiste, deutsch):

**`cboKaMehrfach.Items`**

```
Filter(ForAll(Split(ThisItem.Auswahl; ";") As s; {Value: Trim(s.Value)}); ThisRecord.Value <> "")
```

**`cboKaMehrfach.DisplayFields`**

```
["Value"]
```

**`cboKaMehrfach.SearchFields`**

```
["Value"]
```

**`cboKaMehrfach.SelectMultiple`**

```
true
```

**`cboKaMehrfach.IsSearchable`**

```
false
```

**`cboKaMehrfach.DefaultSelectedItems`**

```
Filter(ForAll(Split(ThisItem.WertText; ";") As s; {Value: Trim(s.Value)}); ThisRecord.Value <> "")
```

**`cboKaMehrfach.OnChange`**

```
Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Concat(Filter(ForAll(Split(ThisItem.Auswahl; ";") As s; {Value: Trim(s.Value)}) As i; i.Value <> "" && i.Value in Self.SelectedItems.Value); Value; "; ")});;
Set(varGeaendert; true)
```

**`cboKaMehrfach.InputTextPlaceholder`**

```
"Auswählen (mehrere möglich)"
```

**`cboKaMehrfach.AccessibleLabel`**

```
"Mehrfachauswahl: " & ThisItem.Frage
```

**`cboKaMehrfach.DisplayMode`**

```
If(varNurLesen; DisplayMode.View; DisplayMode.Edit)
```

**`cboKaMehrfach.Visible`**

```
ThisItem.Typ = "MEHRFACH"
```

**`cboKaMehrfach.BorderColor`**

```
clrRahmen
```

**`cboKaMehrfach.ChevronBackground`**

```
clrPrimaer
```

**`cboKaMehrfach.ChevronFill`**

```
Color.White
```

**`cboKaMehrfach.SelectionFill`**

```
clrPrimaer
```

**`cboKaMehrfach.SelectionColor`**

```
Color.White
```

**`cboKaMehrfach.Font`**

```
Font.'Segoe UI'
```

**`cboKaMehrfach.Size`**

```
16
```

**`cboKaMehrfach.X`**

```
20
```

**`cboKaMehrfach.Y`**

```
54 + If(ThisItem.Hinweis <> ""; 24; 0)
```

**`cboKaMehrfach.Width`**

```
Min(460; Parent.Width - 40)
```

**`cboKaMehrfach.Height`**

```
56
```

Prüfen nach dem Schritt:
- `cboKaMehrfach` liegt in `conKaKarte`.
- Y ist eine Formel (E-05).

### Schritt 5.6 – App-Prüfung und Speichern

Studio → **App-Prüfung → Formeln**: muss **0** sein (Barrierefreiheit/Leistung wie bisher, siehe E-07/E-08). Dann **Speichern** (noch nicht veröffentlichen) und den Test unten in der **Vorschau** machen.
Bei einem Formelfehler: Fehlermeldung und Steuerelement notieren, nicht selbst umbauen, mir schicken.

## Test

| # | Klickfolge | erwartet |
|---|---|---|
| T5.1 | K1 öffnen | M: Kombinationsfeld „Auswählen (mehrere möglich)“; D: Datumsauswahl „Datum wählen“; DZ: Datum + zwei Listen (Stunde, Minute, noch gesperrt); F nicht sichtbar. Andere Typen unverändert |
| T5.2 | Nichts davon ausfüllen | Fuß zählt M, D, DZ als offen |
| T5.3 | M: Korrosion, dann Riss wählen | M erledigt (gespeichert wird „Riss; Korrosion“ in der Reihenfolge der Auswahlwerte) |
| T5.4 | M zusätzlich Leck | F erscheint (Bedingung auf einen Wert der Mehrfachauswahl) |
| T5.5 | F „x“, D Datum wählen | erledigt; rechts neben D ein „✕“ |
| T5.6 | D „✕“ | Datum wieder leer, D offen; dann Datum erneut wählen |
| T5.7 | DZ: nur Datum | Stunde/Minute werden wählbar; Fuß „… (Uhrzeit)“ |
| T5.8 | DZ Stunde 07, Minute 05 | erledigt |
| T5.9 | Übrige Pflichtpunkte von K1 ausfüllen, Speichern | „Gespeichert.“, die nächste offene Kategorie öffnet sich |
| T5.10 | Zurück, K1 „Bearbeiten“ | M zeigt Riss, Leck, Korrosion; D und DZ („TT.MM.JJJJ 07:05“) stehen da; F mit „x“. „Zurück“ fragt **nicht** „Verwerfen?“ (UNSICHER: falls doch, Befund melden – Auswahlfelder lösen dann OnChange beim Laden aus) |
| T5.11 | DZ Datum ändern, ohne zu speichern Zurück („Verwerfen? Erneut tippen“), K1 erneut öffnen | alter gespeicherter Wert steht wieder da (keine Restwerte) |
| T5.12 | Nur mit Abschluss (siehe Paket 1, B7): Protokoll, „Ansehen“ | „Riss; Leck; Korrosion“, „TT.MM.JJJJ“, „TT.MM.JJJJ 07:05“ in der Wertspalte; keine Mängel durch diese Punkte; Nur-Ansicht zeigt die Werte, nicht änderbar, kein „✕“ |

## Rückweg

- Version wiederherstellen, oder: die vier neuen Steuerelemente löschen und App.Formulas aus dem Anhang einfügen.
- Prüfpunkte mit den neuen Typen vorher deaktivieren (die alte App kennt die Typen nicht und würde sie nicht anzeigen, aber Pflicht-Prüfung würde sie nicht verlangen).

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
fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w; "")); "."; ""); " "; ""));;
fnBedGueltig(w: Text; typ: Text; auswahl: Text): Boolean = With({n: fnBedNorm(w)}; n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnBedPasst(w: Text; bew: Text; wt: Text; wz: Number): Boolean = With({n: fnBedNorm(w)}; If(n = "*"; fnBeantwortet(bew; wt; wz); n = fnBedNorm(bew) || n = fnBedNorm(wt) || CountRows(Filter(Split(wt; ";") As s; fnBedNorm(s.Value) = n)) > 0));;
fnSichtbar(bid: Number; w: Text; gef: Boolean; bBid: Number; bInaktiv: Boolean; bTyp: Text; bAuswahl: Text; bBew: Text; bWt: Text; bWz: Number): Boolean = bid = 0 || Trim(w) = "" || !gef || bInaktiv || bBid <> 0 || !fnBedGueltig(w; bTyp; bAuswahl) || fnBedPasst(w; bBew; bWt; bWz);;
fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gmodus; mi; ma) <> "";;
fnDateiname(t: Text): Text = Trim(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(t; "\"; "-"); "/"; "-"); ":"; "-"); "*"; ""); "?"; ""); """"; ""); "<"; ""); ">"; ""); "|"; "-"); "#"; ""); "%"; ""); "'"; ""));;
fnArchivOrdner(tag: Text; test: Boolean): Text = If(test; "TEST/"; "") & Left(tag; 4) & "/" & Mid(tag; 6; 2);;fnSpUrl(bib: Text; pfad: Text): Text = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;
```

