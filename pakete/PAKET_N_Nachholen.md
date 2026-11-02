# Paket N – Nachholen in der Rundgang-App (Stand 02.11.2026)

Erzeugt mit `werkzeuge/doc_app89.py`: Abgleich des Exports **02.11.2026 15:41** gegen den Soll-Stand nach Paket 1–7 (Export 27.10. 09:09 + Pakete 1–7 aus `baukasten.py`).

## Kurzfassung

- Pakete 1, 2, 4 und 6 sind fast vollständig drin, Paket 3 bis auf einen Rahmen.
- **Zwei Formeln sind im falschen Steuerelement gelandet:** `lblKaHinweis.Text` enthält den Foto-Hinweis, `lblKaAbstand.Text` die Fortschrittszeile. Dafür fehlen sie in `lblKaFotoHinweis` und `lblKaStand`.
- **Paket 5 (Mehrfach, Datum, Datum + Uhrzeit) fehlt ganz:** die fünf Steuerelemente und die Änderung an `App.Formulas`.
- **Paket 7 (Foto „Bei Mangel Pflicht“) fehlt.**
- Alles andere stimmt zeichengleich mit dem Soll überein (1154 Properties geprüft, 2 fehlen nur, weil Studio Standardwerte weglässt: btnKaFoto.PressedColor, imgKaBild.ImagePosition).
- Wichtig: Der Builder bietet die Typen Mehrfach/Datum und „Foto Pflicht bei Mangel“ schon an. Ohne dieses Paket versteht die Rundgang-App sie nicht.
- Umfang: 8 Properties, 5 Steuerelemente (4 per YAML, 1 per Menü), 2 Auswahlwerte in SharePoint. Danach folgt Paket 8+9.

## Schritt N.1 – SharePoint (zuerst)

- `RG_Pruefpunkte` → Spalte **Eingabetyp** → Auswahlmöglichkeiten **ergänzen**: **MEHRFACH**, **DATUM**, **DATUMZEIT** (nichts umbenennen).
- `RG_Pruefpunkte` → Spalte **Foto** → Auswahl **ergänzen**: **Bei Mangel Pflicht** (genau so).
- Aufgefallen: In `RG_Pruefpunkte` gibt es neben `Fassung` eine Spalte **`Fassungf`** (Tippfehler beim Anlegen?). Keine App benutzt sie. Wenn sie leer ist, kann sie gelöscht werden.
- Danach in der Rundgang-App: **Daten** → `RG_Pruefpunkte` → ⋯ → **Aktualisieren**.

## Schritt N.2 – zwei Formeln zurück ins richtige Steuerelement

### N.2.1 · `lblKaHinweis.Text`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaHinweis` → Text

```
ThisItem.Hinweis
```

**Das ändert sich:**

```diff
-If(varNurLesen; "Gespeicherte Fotos (nur Ansicht)."; LookUp(colAntworten; PruefpunktID = varFotoPP).FotoModus = "Pflicht"; "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren."; !fnFotoNeuErlaubt(LookUp(colAntworten; Pruefp …
+ThisItem.Hinweis
```

**Kurz erklärt:** **Reparatur:** Hier stand der Text von `lblKaFotoHinweis` (beim Einfügen von Paket 1 ins falsche Steuerelement geraten). Die Karte zeigt wieder den Hinweis des Prüfpunkts.

**Nachprüfen:** Ende der Formel: `ThisItem.Hinweis`

### N.2.2 · `lblKaAbstand.Text`

**Pfad:** `scrKategorie › galKaPruefpunkte › lblKaAbstand` → Text

```
ThisItem.Auswahl
```

**Das ändert sich:**

```diff
-If(varNurLesen; "Nur Ansicht – der Rundgang ist nicht mehr in Arbeit."; Value(lblKaFehlendAnzahl.Text) = 0; "✓  Alles ausgefüllt" & With({n: CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: Loo …
+ThisItem.Auswahl
```

**Kurz erklärt:** **Reparatur:** Hier stand der Text von `lblKaStand` (beim Einfügen von Paket 4 ins falsche Steuerelement geraten). `lblKaAbstand` ist nur ein Abstandhalter, Text wie im Original.

**Nachprüfen:** Ende der Formel: `ThisItem.Auswahl`

## Schritt N.3 – fehlende Formeln

### N.3.1 · `lblKaFotoHinweis.Text`

**Pfad:** `scrKategorie › conKaFoto › conKaFotoKarte › lblKaFotoHinweis` → Text

```
If(varNurLesen; "Gespeicherte Fotos (nur Ansicht)."; LookUp(colAntworten; PruefpunktID = varFotoPP).FotoModus = "Pflicht"; "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren."; LookUp(colAntworten; PruefpunktID = varFotoPP).FotoModus = "BeiMangel" && LookUp(colAntworten; PruefpunktID = varFotoPP).Bewertung = "NIO"; "Mangel: mindestens ein Foto Pflicht. Keine Personen fotografieren."; !fnFotoNeuErlaubt(LookUp(colAntworten; PruefpunktID = varFotoPP).Bewertung; LookUp(colAntworten; PruefpunktID = varFotoPP).FotoModus); "Neue Fotos nur bei n.i.O. oder Foto-Modus Optional/Pflicht."; "Keine Personen fotografieren. Fotos werden beim „Speichern“ hochgeladen.")
```

**Das ändert sich:**

```diff
-"Bitte keine Personen fotografieren. Neue Fotos werden beim „Speichern“ hochgeladen."
+If(varNurLesen; "Gespeicherte Fotos (nur Ansicht)."; LookUp(colAntworten; PruefpunktID = varFotoPP).FotoModus = "Pflicht"; "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren."; LookUp(colAntworten; PruefpunktID = varFotoPP …
```

**Kurz erklärt:** Fehlte (Paket 1 Schritt 1.9 + Paket 7): Hinweis im Foto-Fenster je nach Foto-Regel.

**Nachprüfen:** Ende der Formel: `nal/Pflicht."; "Keine Personen fotografieren. Fotos werden beim „Speichern“ hochgeladen.")`

### N.3.2 · `lblKaStand.Text`

**Pfad:** `scrKategorie › conKaFuss › lblKaStand` → Text

```
If(varNurLesen; "Nur Ansicht – der Rundgang ist nicht mehr in Arbeit."; Value(lblKaFehlendAnzahl.Text) = 0; "✓  Alles ausgefüllt" & With({n: CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && a.Bewertung = "NIO"))}; If(n > 0; " · " & n & " n.i.O."; "")); "Noch offen (" & lblKaFehlendAnzahl.Text & "): " & lblKaFehlend.Text)
```

**Das ändert sich:**

```diff
-If(varNurLesen; "Nur Ansicht – der Rundgang ist nicht mehr in Arbeit."; Value(lblKaFehlendAnzahl.Text) = 0; "✓  Alles ausgefüllt" & With({n: CountRows(Filter(colAntworten; !Inaktiv && Bewertung = "NIO"))}; If(n > 0; " · " & n & " n.i.O. …
+If(varNurLesen; "Nur Ansicht – der Rundgang ist nicht mehr in Arbeit."; Value(lblKaFehlendAnzahl.Text) = 0; "✓  Alles ausgefüllt" & With({n: CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: Loo …
```

**Kurz erklärt:** Fehlte (Paket 4 Schritt 4.5): Fortschrittszeile zählt nur sichtbare Fragen.

**Nachprüfen:** Ende der Formel: `n & " n.i.O."; "")); "Noch offen (" & lblKaFehlendAnzahl.Text & "): " & lblKaFehlend.Text)`

### N.3.3 · `txtKaZahl.BorderColor`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › txtKaZahl` → BorderColor

```
If(ThisItem.Bewertung = "NIO" || (!varNurLesen && ThisItem.Grenzmodus = "Sperren" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; If(varNurLesen; ThisItem.Warnung; fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrWarnung; clrRahmen)
```

**Das ändert sich:**

```diff
-If(ThisItem.Bewertung = "NIO"; clrFehler; clrRahmen)
+If(ThisItem.Bewertung = "NIO" || (!varNurLesen && ThisItem.Grenzmodus = "Sperren" && fnAusserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; If(varNurLesen; ThisItem.Warnung; fnAusserhalb(ThisItem.WertZahl; This …
```

**Kurz erklärt:** Fehlte (Paket 3 Schritt 3.5): Rahmen orange bei Warnen, rot bei Sperren/Mangel.

**Nachprüfen:** Ende der Formel: `Ausserhalb(ThisItem.WertZahl; ThisItem.MinWert; ThisItem.MaxWert)); clrWarnung; clrRahmen)`

### N.3.4 · `btnKaFoto.Text`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaFoto` → Text

```
With({n: CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos)};
    "📷 Foto" & If(n > 0; " (" & n & ")"; If((ThisItem.FotoModus = "Pflicht" || (ThisItem.FotoModus = "BeiMangel" && ThisItem.Bewertung = "NIO")) && !varNurLesen; " *"; ""))
)
```

**Das ändert sich:**

```diff
-    "📷 Foto" & If(n > 0; " (" & n & ")"; If(ThisItem.FotoModus = "Pflicht" && !varNurLesen; " *"; ""))
+    "📷 Foto" & If(n > 0; " (" & n & ")"; If((ThisItem.FotoModus = "Pflicht" || (ThisItem.FotoModus = "BeiMangel" && ThisItem.Bewertung = "NIO")) && !varNurLesen; " *"; ""))
```

**Kurz erklärt:** Fehlte (Paket 7): Stern bei „Foto Pflicht bei Mangel“.

**Nachprüfen:** Ende der Formel: `)`

### N.3.5 · `btnKaFoto.Visible`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaFoto` → Visible

```
fnLinkAnzahl(ThisItem.Fotos) > 0 || (!varNurLesen && (ThisItem.Bewertung = "NIO" || (ThisItem.FotoModus <> "Aus" && ThisItem.FotoModus <> "BeiMangel")))
```

**Das ändert sich:**

```diff
-fnLinkAnzahl(ThisItem.Fotos) > 0 || (!varNurLesen && (ThisItem.Bewertung = "NIO" || ThisItem.FotoModus <> "Aus"))
+fnLinkAnzahl(ThisItem.Fotos) > 0 || (!varNurLesen && (ThisItem.Bewertung = "NIO" || (ThisItem.FotoModus <> "Aus" && ThisItem.FotoModus <> "BeiMangel")))
```

**Kurz erklärt:** Fehlte (Paket 7): Foto-Knopf bei „Bei Mangel Pflicht“ erst nach n.i.O.

**Nachprüfen:** Ende der Formel: `.Bewertung = "NIO" || (ThisItem.FotoModus <> "Aus" && ThisItem.FotoModus <> "BeiMangel")))`

## Schritt N.4 – App.Formulas

Rot ist danach nichts zu erwarten (die neuen Teile werden nur von Paket 5/7 benutzt).

### N.4 · `App.Formulas`

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
fnKommentarNoetig(typ: Text; bew: Text; wt: Text; wz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew; wt; wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz; mi; ma));;
fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATUMZEIT") && wt = "")); "Wert";
    typ = "DATUMZEIT" && wt <> "" && Len(wt) < 16; "Uhrzeit";
    typ = "ZAHL" && gmodus = "Sperren" && fnSperreGilt(mi; ma) && fnAusserhalb(wz; mi; ma); "Bereich";
    fnKommentarNoetig(typ; bew; wt; wz; kpfl; gmodus; mi; ma) && Trim(kom) = ""; "Kommentar";
    (foto = "Pflicht" || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1; "Foto";
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

**Das ändert sich:**

```diff
-fnFotoModus(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht"; f; alt; "Optional"; "Aus");;
+fnFotoModus(f: Text; alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht"; f; f = "Bei Mangel Pflicht"; "BeiMangel"; alt; "Optional"; "Aus");;
-    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "")); "Wert";
+    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATUMZEIT") && wt = "")) …
+    typ = "DATUMZEIT" && wt <> "" && Len(wt) < 16; "Uhrzeit";
-    foto = "Pflicht" && fanz < 1; "Foto";
+    (foto = "Pflicht" || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1; "Foto";
+fnDatumText(d: Date; h: Text; m: Text; mitZeit: Boolean): Text = If(IsBlank(d); ""; Text(d; "dd.mm.yyyy") & If(mitZeit && h <> "" && m <> ""; " " & h & ":" & m; ""));;
```

**Kurz erklärt:** Fehlte: Paket 5 (Typen MEHRFACH/DATUM/DATUMZEIT in `fnFehltGrund`, neue `fnDatumText`) und Paket 7 (`fnFotoModus`, Foto bei Mangel).

**Nachprüfen:** Ende der Formel: `noformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;`

## Schritt N.5 – Paket 5 nachholen (Steuerelemente)

Unverändert aus `pakete/PAKET_5_Typen.md` (Schritt 5.4 und 5.5):

### Schritt N.5a – Datum, Uhrzeit und Leeren-Knopf (YAML)

In der Strukturansicht in `conKaKarte` das Steuerelement `txtKaText` markieren, dann den YAML-Block mit **Strg+V** einfügen (landet in derselben Karte). **Alle vier Blöcke zusammen** kopieren und einfügen (sie verweisen aufeinander; einzeln eingefügt stehen kurz rote Fehler).

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

### Schritt N.5b – Mehrfachauswahl (Kombinationsfeld über das Menü)

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


## Schritt N.6 – App-Prüfung

App-Prüfung → Formeln = **0**. Speichern. Dann Paket 8+9 (`pakete/PAKET_8_9_APP.md`).

## Test (wenn du testest)

Paket 5: Tests T5.x in `pakete/PAKET_5_Typen.md`. Paket 7: T7.1–T7.7 in `pakete/PAKET_7_FotoBeiMangel.md`. Reparatur: eine Karte mit Hinweis zeigt wieder den Hinweis (nicht den Foto-Text).

## Anhang – Vorher-Fassungen (aus dem Export)

**`lblKaHinweis.Text` vorher**

```
If(varNurLesen; "Gespeicherte Fotos (nur Ansicht)."; LookUp(colAntworten; PruefpunktID = varFotoPP).FotoModus = "Pflicht"; "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren."; !fnFotoNeuErlaubt(LookUp(colAntworten; PruefpunktID = varFotoPP).Bewertung; LookUp(colAntworten; PruefpunktID = varFotoPP).FotoModus); "Neue Fotos nur bei n.i.O. oder Foto-Modus Optional/Pflicht."; "Keine Personen fotografieren. Fotos werden beim „Speichern“ hochgeladen.")
```

**`lblKaAbstand.Text` vorher**

```
If(varNurLesen; "Nur Ansicht – der Rundgang ist nicht mehr in Arbeit."; Value(lblKaFehlendAnzahl.Text) = 0; "✓  Alles ausgefüllt" & With({n: CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && a.Bewertung = "NIO"))}; If(n > 0; " · " & n & " n.i.O."; "")); "Noch offen (" & lblKaFehlendAnzahl.Text & "): " & lblKaFehlend.Text)
```

**`lblKaFotoHinweis.Text` vorher**

```
"Bitte keine Personen fotografieren. Neue Fotos werden beim „Speichern“ hochgeladen."
```

**`lblKaStand.Text` vorher**

```
If(varNurLesen; "Nur Ansicht – der Rundgang ist nicht mehr in Arbeit."; Value(lblKaFehlendAnzahl.Text) = 0; "✓  Alles ausgefüllt" & With({n: CountRows(Filter(colAntworten; !Inaktiv && Bewertung = "NIO"))}; If(n > 0; " · " & n & " n.i.O."; "")); "Noch offen (" & lblKaFehlendAnzahl.Text & "): " & lblKaFehlend.Text)
```

**`txtKaZahl.BorderColor` vorher**

```
If(ThisItem.Bewertung = "NIO"; clrFehler; clrRahmen)
```

**`btnKaFoto.Text` vorher**

```
With({n: CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos)};
    "📷 Foto" & If(n > 0; " (" & n & ")"; If(ThisItem.FotoModus = "Pflicht" && !varNurLesen; " *"; ""))
)
```

**`btnKaFoto.Visible` vorher**

```
fnLinkAnzahl(ThisItem.Fotos) > 0 || (!varNurLesen && (ThisItem.Bewertung = "NIO" || ThisItem.FotoModus <> "Aus"))
```

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

