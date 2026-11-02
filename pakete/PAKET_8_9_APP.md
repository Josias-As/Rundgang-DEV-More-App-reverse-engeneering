# Paket 8+9 – Rundgang-App: Abschnitte, Bereich ausblenden, Rückfrage, kritischer Mangel

Stand 02.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (Paket 8 und 9 als Zustandskette mit exakten Ankern) und `werkzeuge/doc_app89.py`. Voraussetzung: **Paket N** (`pakete/PAKET_N_Nachholen.md`) ist eingefügt. Dann ist dein Stand zeichengleich mit dem Stand, auf dem dieses Paket aufbaut (maschinell geprüft).

## Kurzfassung

- **Abschnitte:** Über der ersten Frage eines Abschnitts steht eine Überschrift (z. B. „Kompressor 1“). Protokoll und Mängel nennen den Abschnitt.
- **Bereich ausblenden:** Im Builder ausgeblendete Bereiche erscheinen nicht mehr als Überschrift (gilt für Rundgänge, die danach gestartet werden).
- **Rückfrage:** Bei n.i.O. (oder Zahl außerhalb, Modus Mangel) fragt die App „Ist das wirklich so?“ mit dem normalen Wert. „Nein“ nimmt die Antwort zurück.
- **Kritischer Mangel:** rotes Fenster über den ganzen Bildschirm mit den Ansprechpartnern (Name, Telefon, Hinweis). Nur „Ich habe Bescheid gegeben“ oder „war ein Versehen“. Ohne Bestätigung lässt sich die Kategorie nicht speichern. Protokoll und Mangel nennen die Bestätigung. **Es wird nichts verschickt.**
- Eingestellt wird alles im Builder (Paket 9 Builder-Teil folgt). Bis dahin: Spalten direkt in SharePoint setzen.
- Umfang: 15 Properties (jede einmal in der Endfassung), 30 neue Steuerelemente in 3 Blöcken, 1 neue Liste, 5 neue Spalten.
- Geprüft: Generator 0 Fehler (Namen, Klammern, Rückübersetzung, gleiche Felder in allen drei Zweigen von colAntworten, 13 Argumente in jedem fnFehlt-Aufruf). **Nicht in Studio getestet. Nicht unabhängig geprüft.**

## Schritt 1 – SharePoint und Datenquelle

1. **Neue Liste `RG_Ansprechpartner`** (SharePoint, IMS+). Spalten: `Title` (vorhanden, = Gewerk/Rolle, z. B. „Elektriker“), `Name` (Eine Textzeile), `Telefon` (Eine Textzeile), `Hinweis` (Mehrere Textzeilen, nur Text), `Allgemein` (Ja/Nein, Standard Nein), `Aktiv` (Ja/Nein, Standard Ja).
   Testzeilen: „Allgemein“ (Allgemein = Ja), „Elektriker“, „IT-Dienstleister“.
2. **`RG_Pruefpunkte`** neue Spalten: `Kritisch` (Ja/Nein, Standard Nein), `KritischText` (Eine Textzeile), `Ansprechpartner` (Eine Textzeile, IDs aus `RG_Ansprechpartner` mit `;` getrennt), `Rueckfrage` (Ja/Nein, Standard Nein), `RueckfrageText` (Eine Textzeile). `Abschnitt` gibt es schon.
3. Rundgang-App: **Daten** → `RG_Pruefpunkte` und `RG_Bereiche` → ⋯ → **Aktualisieren**, dann **Daten hinzufügen** → SharePoint → IMS+ → `RG_Ansprechpartner`.
4. Zum Testen an einem ZZ-Test-Prüfpunkt in SharePoint: `Kritisch` = Ja, `KritischText` = „Anlage nicht weiter betreiben.“, `Ansprechpartner` = ID von „Elektriker“, `Rueckfrage` = Ja, `RueckfrageText` = „Normalerweise steht hier i.O.“.

**Rot ab hier bis Schritt 4:** Nach Schritt 2 sind die Aufrufe von `fnFehlt` rot (13 statt 12 Argumente), bis Schritt 3/4 sie ersetzen. Das ist erwartet.

## Schritt 2 – Laden und Formeln

### 2.1 · `scrKategorie.OnVisible`

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
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); BildID: Coalesce(pp.HinweisBildID; 0); Abschnitt: Trim(Coalesce(Text(a.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(a.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(a.KritischOk); false); false); KritischZeit: Coalesce(Text(a.KritischZeit); ""); Inaktiv: false}
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
                     Warnung: false;
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Warnung: Coalesce(IfError(Boolean(o.Value.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); BildID: 0; Abschnitt: Trim(Coalesce(Text(o.Value.Abschnitt); "")); AbsKopf: false; Kritisch: Coalesce(IfError(Boolean(o.Value.Kritisch); false); false); KritischText: ""; Ansprechpartner: ""; Rueckfrage: false; RueckfrageText: ""; KritischOk: Coalesce(IfError(Boolean(o.Value.KritischOk); false); false); KritischZeit: Coalesce(Text(o.Value.KritischZeit); ""); Inaktiv: true}
            )
        )
    )
);;
ClearCollect(colAbsTmp; ShowColumns(Filter(colAntworten; !Inaktiv && Abschnitt <> ""); PruefpunktID; Reihenfolge; Abschnitt; BedID));;
ForAll(colAbsTmp As t;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = t.PruefpunktID);
        {AbsKopf: With({g: Filter(colAbsTmp As u; Lower(u.Abschnitt) = Lower(t.Abschnitt))};
            If(IsEmpty(Filter(g As u1; u1.BedID = 0)); t.Reihenfolge = Min(g; Reihenfolge); t.BedID = 0 && t.Reihenfolge = Min(Filter(g As u2; u2.BedID = 0); Reihenfolge)))}
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
```

**Das ändert sich:**

```diff
+Set(varRueckPP; 0);;
+Set(varKritPP; 0);;
-    Set(varErgebnis; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK))
+    Set(varErgebnis; LookUp(RG_KategorieErgebnisse; Title = varSchluesselK));
+    ClearCollect(colKontakte; Filter(RG_Ansprechpartner; Aktiv = true))
-                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFot …
+                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFot …
+                     Abschnitt: Trim(Coalesce(p.Abschnitt; ""));
+                     AbsKopf: false;
+                     Kritisch: Coalesce(p.Kritisch; false);
+                     KritischText: Coalesce(p.KritischText; "");
+                     Ansprechpartner: Coalesce(p.Ansprechpartner; "");
+                     Rueckfrage: Coalesce(p.Rueckfrage; false);
+                     RueckfrageText: Coalesce(p.RueckfrageText; "");
+                     KritischOk: If(IsBlank(alt); false; Coalesce(IfError(Boolean(alt.Value.KritischOk); false); false));
+                     KritischZeit: If(IsBlank(alt); ""; Coalesce(Text(alt.Value.KritischZeit); ""));
-                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); …
+                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); …
+    )
+);;
+ClearCollect(colAbsTmp; ShowColumns(Filter(colAntworten; !Inaktiv && Abschnitt <> ""); PruefpunktID; Reihenfolge; Abschnitt; BedID));;
+ForAll(colAbsTmp As t;
+    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = t.PruefpunktID);
+        {AbsKopf: With({g: Filter(colAbsTmp As u; Lower(u.Abschnitt) = Lower(t.Abschnitt))};
+            If(IsEmpty(Filter(g As u1; u1.BedID = 0)); t.Reihenfolge = Min(g; Reihenfolge); t.BedID = 0 && t.Reihenfolge = Min(Filter(g As u2; u2.BedID = 0); Reihenfolge)))}
```

**Kurz erklärt:** Lädt die Ansprechpartner, setzt die beiden Fenster zurück, neue Felder in allen drei Zweigen (Abschnitt, Kopf-Kennzeichen, kritisch, Rückfrage, Bestätigung). Danach wird je Abschnitt die erste Frage als Überschrift-Träger markiert (bevorzugt eine ohne Bedingung).

**Nachprüfen:** Ende der Formel: `Set(varIsLoading; false)`

### 2.2 · `App.Formulas`

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

**Das ändert sich:**

```diff
-fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Text = If(
+fnFehltGrund(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Text = If(
+    kritoffen && bew = "NIO"; "Kritisch";
-fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom; foto; fanz; kpfl; gm …
+fnFehlt(typ: Text; pflicht: Boolean; bew: Text; wt: Text; wz: Number; kom: Text; foto: Text; fanz: Number; kpfl: Boolean; gmodus: Text; mi: Number; ma: Number; kritoffen: Boolean): Boolean = fnFehltGrund(typ; pflicht; bew; wt; wz; kom;  …
```

**Kurz erklärt:** `fnFehltGrund`/`fnFehlt` bekommen ein 13. Argument: kritischer Mangel noch nicht bestätigt → „fehlt“ (Grund „Kritisch“).

**Nachprüfen:** Ende der Formel: `noformgroup.sharepoint.com/sites/IMSKonzept/" & bib & "/" & Substitute(pfad; " "; "%20");;`

## Schritt 3 – Auslöser und „Noch offen“

### 3.1 · `btnKaNIO.OnSelect`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › btnKaNIO` → OnSelect

```
With({neu: If(ThisItem.Bewertung = "NIO"; ""; "NIO")};
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {Bewertung: neu; KritischOk: false; KritischZeit: ""});;
    If(neu = "NIO"; If(ThisItem.Rueckfrage; Set(varRueckPP; ThisItem.PruefpunktID); ThisItem.Kritisch && !LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID).KritischOk; Set(varKritPP; ThisItem.PruefpunktID)))
);;
Set(varGeaendert; true)
```

**Das ändert sich:**

```diff
-Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {Bewertung: If(ThisItem.Bewertung = "NIO"; ""; "NIO")});;
+With({neu: If(ThisItem.Bewertung = "NIO"; ""; "NIO")};
+    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {Bewertung: neu; KritischOk: false; KritischZeit: ""});;
+    If(neu = "NIO"; If(ThisItem.Rueckfrage; Set(varRueckPP; ThisItem.PruefpunktID); ThisItem.Kritisch && !LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID).KritischOk; Set(varKritPP; ThisItem.PruefpunktID)))
+);;
```

**Kurz erklärt:** Bei neuem n.i.O.: erst Rückfrage (wenn eingestellt), sonst gleich die kritische Meldung (wenn eingestellt). Zurücknehmen löscht die Bestätigung.

**Nachprüfen:** Ende der Formel: `Set(varGeaendert; true)`

### 3.2 · `txtKaZahl.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › txtKaZahl` → OnChange

```
With({z: IfError(Value(Self.Text); Blank())};
    With({b: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus)); war: ThisItem.Bewertung = "NIO" && ThisItem.KritischOk};
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; Bewertung: b; KritischOk: b = "NIO" && war; KritischZeit: If(b = "NIO" && war; ThisItem.KritischZeit; "")});;
        If(b = "NIO"; If(ThisItem.Rueckfrage; Set(varRueckPP; ThisItem.PruefpunktID); ThisItem.Kritisch && !LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID).KritischOk; Set(varKritPP; ThisItem.PruefpunktID)))
    )
);;
Set(varGeaendert; true)
```

**Das ändert sich:**

```diff
-    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; Bewertung: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus))})
+    With({b: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus)); war: ThisItem.Bewertung = "NIO" && ThisItem.KritischOk};
+        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; Bewertung: b; KritischOk: b = "NIO" && war; KritischZeit: If(b = "NIO" && war; ThisItem.KritischZeit; "")});;
+        If(b = "NIO"; If(ThisItem.Rueckfrage; Set(varRueckPP; ThisItem.PruefpunktID); ThisItem.Kritisch && !LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID).KritischOk; Set(varKritPP; ThisItem.PruefpunktID)))
+    )
```

**Kurz erklärt:** Wie bei n.i.O.: Zahl außerhalb (Mangel) löst Rückfrage bzw. kritische Meldung aus. Eine schon gegebene Bestätigung bleibt, solange es n.i.O. bleibt.

**Nachprüfen:** Ende der Formel: `Set(varGeaendert; true)`

### 3.3 · `lblKaFehlendAnzahl.Text`

**Pfad:** `scrKategorie › lblKaFehlendAnzahl` → Text

```
CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert; a.Kritisch && !a.KritischOk)))
```

**Das ändert sich:**

```diff
-CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewe …
+CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewe …
```

**Kurz erklärt:** Zählt einen unbestätigten kritischen Mangel als offen.

**Nachprüfen:** Ende der Formel: `s); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert; a.Kritisch && !a.KritischOk)))`

### 3.4 · `lblKaFehlend.Text`

**Pfad:** `scrKategorie › lblKaFehlend` → Text

```
Concat(Filter(Sort(colAntworten; Reihenfolge) As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert; a.Kritisch && !a.KritischOk)) As z; If(z.Abschnitt = ""; ""; z.Abschnitt & " › ") & z.Frage & Switch(fnFehltGrund(z.Typ; z.Pflicht; z.Bewertung; z.WertText; z.WertZahl; z.Kommentar; z.FotoModus; CountRows(Filter(colFotos; PruefpunktID = z.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(z.Fotos); z.KommentarPflicht; z.Grenzmodus; z.MinWert; z.MaxWert; z.Kritisch && !z.KritischOk); "Kommentar"; " (Kommentar)"; "Foto"; " (Foto)"; "Bereich"; " (unzulässiger Wert)"; "Uhrzeit"; " (Uhrzeit)"; "Kritisch"; " (kritisch: Bescheid bestätigen)"; ""); "; ")
```

**Das ändert sich:**

```diff
-Concat(Filter(Sort(colAntworten; Reihenfolge) As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b …
+Concat(Filter(Sort(colAntworten; Reihenfolge) As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b …
```

**Kurz erklärt:** „Noch offen“ nennt den Abschnitt vor der Frage (bei gleichen Fragen in mehreren Abschnitten wichtig) und „(kritisch: Bescheid bestätigen)“.

**Nachprüfen:** Ende der Formel: `ert)"; "Uhrzeit"; " (Uhrzeit)"; "Kritisch"; " (kritisch: Bescheid bestätigen)"; ""); "; ")`

### 3.5 · `conKaKarte.BorderColor`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte` → BorderColor

```
If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos); ThisItem.KommentarPflicht; ThisItem.Grenzmodus; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Kritisch && !ThisItem.KritischOk)); clrFehler; clrRahmen)
```

**Das ändert sich:**

```diff
-If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = Thi …
+If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = Thi …
```

**Kurz erklärt:** Rahmen „fehlt“ auch bei unbestätigtem kritischem Mangel.

**Nachprüfen:** Ende der Formel: `Wert; ThisItem.MaxWert; ThisItem.Kritisch && !ThisItem.KritischOk)); clrFehler; clrRahmen)`

### 3.6 · `conKaKarte.BorderThickness`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte` → BorderThickness

```
If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos); ThisItem.KommentarPflicht; ThisItem.Grenzmodus; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Kritisch && !ThisItem.KritischOk)); 2; 1)
```

**Das ändert sich:**

```diff
-If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = Thi …
+If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = Thi …
```

**Kurz erklärt:** Wie BorderColor.

**Nachprüfen:** Ende der Formel: `us; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Kritisch && !ThisItem.KritischOk)); 2; 1)`

## Schritt 4 – Speichern

### 4.1 · `btnKaSpeichern.OnSelect`

**Pfad:** `scrKategorie › conKaFuss › btnKaSpeichern` → OnSelect

```
If(
    Value(lblKaFehlendAnzahl.Text) > 0;
        Set(varZeigeFehlend; true);;
        Set(varSprungRec; First(Filter(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge) As a; If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert; a.Kritisch && !a.KritischOk))));;
        If(varSprungRec.Kritisch && varSprungRec.Bewertung = "NIO" && !varSprungRec.KritischOk; Set(varKritPP; varSprungRec.PruefpunktID));;
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
                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit); JSONFormat.Compact));;
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

**Das ändert sich:**

```diff
-        Set(varSprungRec; First(Filter(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge) As a; If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); …
+        Set(varSprungRec; First(Filter(Sort(Filter(colAntworten; !Inaktiv); Reihenfolge) As a; If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); …
+        If(varSprungRec.Kritisch && varSprungRec.Bewertung = "NIO" && !varSprungRec.KritischOk; Set(varKritPP; varSprungRec.PruefpunktID));;
-                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet); JSONFormat.Compact));;
+                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet; Abschnitt; AbsKopf; Kritisch; KritischOk; KritischZeit); J …
```

**Kurz erklärt:** Speichert Abschnitt und Bestätigung im JSON. Fehlt nur noch die Bestätigung eines kritischen Mangels, öffnet „Speichern“ das rote Fenster wieder.

**Nachprüfen:** Ende der Formel: `)`

## Schritt 5 – Abschnitt-Überschrift in der Karte

### 5.1 · `conKaKarte.Y`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte` → Y

```
If(ThisItem.AbsKopf; 52; 8)
```

**Das ändert sich:**

```diff
-8
+If(ThisItem.AbsKopf; 52; 8)
```

**Kurz erklärt:** Platz für die Abschnitt-Überschrift über der Karte.

**Nachprüfen:** Ende der Formel: `If(ThisItem.AbsKopf; 52; 8)`

### 5.2 · neues Steuerelement `lblKaAbschnitt`

**Wo hin:** **`lblKaAbstand`** in der Strukturansicht markieren → Strg+V (landet als Geschwister in der Galerievorlage).

```yaml
- lblKaAbschnitt:
    Control: Label@2.5.1
    Properties:
      Color: =clrPrimaer
      Font: =Font.'Segoe UI'
      FontWeight: =FontWeight.Semibold
      Height: =If(ThisItem.AbsKopf, 44, 0)
      Size: =17
      Text: =ThisItem.Abschnitt
      VerticalAlign: =VerticalAlign.Bottom
      Visible: =ThisItem.AbsKopf
      Width: =Parent.TemplateWidth - 56
      X: =28
      Y: =8
```

**Nachprüfen (E-05):** `lblKaAbschnitt.Height` muss die Formel `If(ThisItem.AbsKopf; 44; 0)` sein, keine Zahl. Sonst von Hand einsetzen.

## Schritt 6 – Bereich ausblenden

### 6.1 · `btnRgAktion.OnSelect`

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
                    Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: ISOWeekNum(varTag); Wochentag: Weekday(varTag; StartOfWeek.Monday); Status: stInArbeit; AnzahlKategorien: CountRows(colKatBau); KategorieListe: JSON(colKatBau; JSONFormat.Compact); PrueferEmail: User().Email; PrueferName: User().FullName; StartZeit: Now(); TestDatensatz: StartsWith(ThisItem.Title; "ZZ Test")});
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

**Das ändert sich:**

```diff
-                With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName; LookUp(b As be3; be3.ID = BereichID).Title); BReihe *  …
+                With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName; If(Coalesce(LookUp(b As be3; be3.ID = BereichID).Ausbl …
```

**Kurz erklärt:** Beim Start: ausgeblendete Bereiche bekommen einen leeren Namen.

**Nachprüfen:** Ende der Formel: `)`

### 6.2 · `galRuKategorien.Items`

**Pfad:** `scrRundgang › galRuKategorien` → Items

```
With({liste: AddColumns(colKatListe; Erledigt; !IsBlank(LookUp(colErledigt As e; e.KategorieID = KategorieID)))};
    Sort(
        AddColumns(liste;
            Zustand; If(Erledigt; "erledigt"; Position = Min(Filter(liste As l; !l.Erledigt); Position); "naechste"; "gesperrt");
            ErsteImBereich; BereichName <> "" && Position = Min(Filter(liste As l2; l2.BereichName = BereichName); Position);
            NIO; Coalesce(LookUp(colErledigt As e2; e2.KategorieID = KategorieID).AnzahlNIO; 0)
        );
        Position
    )
)
```

**Das ändert sich:**

```diff
-            ErsteImBereich; Position = Min(Filter(liste As l2; l2.BereichName = BereichName); Position);
+            ErsteImBereich; BereichName <> "" && Position = Min(Filter(liste As l2; l2.BereichName = BereichName); Position);
```

**Kurz erklärt:** Bereichs-Überschrift nur, wenn der Bereich einen Namen hat.

**Nachprüfen:** Ende der Formel: `)`

### 6.3 · `lblKaUnter.Text`

**Pfad:** `scrKategorie › conKaKopf › lblKaUnter` → Text

```
If(varBereichName = ""; ""; varBereichName & "  ·  ") & "Kategorie " & varKatPos & " von " & CountRows(colKatListe) & If(varNurLesen; "  ·  nur Ansicht"; "  ·  " & (CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))) - Value(lblKaFehlendAnzahl.Text)) & " von " & CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))) & " ausgefüllt")
```

**Das ändert sich:**

```diff
-varBereichName & "  ·  Kategorie " & varKatPos & " von " & CountRows(colKatListe) & If(varNurLesen; "  ·  nur Ansicht"; "  ·  " & (CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAnt …
+If(varBereichName = ""; ""; varBereichName & "  ·  ") & "Kategorie " & varKatPos & " von " & CountRows(colKatListe) & If(varNurLesen; "  ·  nur Ansicht"; "  ·  " & (CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Au …
```

**Kurz erklärt:** Kopfzeile ohne Bereichsnamen, wenn er ausgeblendet ist.

**Nachprüfen:** Ende der Formel: `ID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))) & " ausgefüllt")`

## Schritt 7 – Protokoll und Mängel

### 7.1 · `htmProtokoll.HtmlText`

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
                "<td style='padding:6px 8px;width:64px;white-space:nowrap;font-weight:600;color:" & If(b = "NIO"; "#B3261E"; w; "#9A5B00"; "#0F7B3F") & "'>" & Switch(b; "IO"; "i.O."; "NIO"; "n.i.O."; "") & "</td>" &
                "<td style='padding:6px 8px'>" & fnHtml(Text(a.Value.WertText)) & If(IsBlank(a.Value.WertZahl); ""; Text(Value(a.Value.WertZahl)) & " " & fnHtml(Text(a.Value.Einheit))) & If(w; " <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>"; "") &
                If(IsBlank(k) || k = ""; ""; "<br><i style='color:" & If(b = "NIO"; "#B3261E"; "#5F6370") & "'>" & fnHtml(k) & "</i>") &
                If(b = "NIO" && Coalesce(IfError(Boolean(a.Value.Kritisch); false); false); "<br><b style='color:#B3261E'>KRITISCH – " & If(Coalesce(IfError(Boolean(a.Value.KritischOk); false); false); "Bescheid gegeben, bestätigt von " & fnHtml(e.PrueferName) & " um " & fnHtml(Coalesce(Text(a.Value.KritischZeit); "")); "nicht bestätigt") & "</b>"; "") &
                If(IsBlank(fo) || fo = ""; ""; "<br>" & Concat(Split(fo; " | ") As s; "<a href='" & Trim(s.Value) & "'>Foto ›</a> ")) &
                "</td></tr>"
            )
        ) & "</table>"
    ) &
    If(IsBlank(d.ProtokollUrl); ""; "<p style='font-size:12px'>Archiv-PDF: <a href='" & d.ProtokollUrl & "'>" & fnHtml(d.Title) & ".pdf</a></p>") &
    "<p style='color:#5F6370;font-size:12px;margin-top:18px'>Erstellt mit der Rundgang-App · " & Text(varProtokollZeit; "dd.mm.yyyy hh:mm") & If(d.TestDatensatz; " · TESTDATEN"; "") & "</p></div>"
)
```

**Das ändert sich:**

```diff
-        " <span style='font-weight:400;color:#5F6370;font-size:13px'>" & fnHtml(e.BereichName) & " · " & fnHtml(e.PrueferName) & " · " & Text(e.GespeichertAm; "hh:mm") & "</span></h3>" &
+        " <span style='font-weight:400;color:#5F6370;font-size:13px'>" & If(e.BereichName = ""; ""; fnHtml(e.BereichName) & " · ") & fnHtml(e.PrueferName) & " · " & Text(e.GespeichertAm; "hh:mm") & "</span></h3>" &
+                If(Coalesce(IfError(Boolean(a.Value.AbsKopf); false); false); "<tr><td colspan='3' style='padding:12px 8px 4px 8px;font-weight:600;color:#171496'>" & fnHtml(Text(a.Value.Abschnitt)) & "</td></tr>"; "") &
+                If(b = "NIO" && Coalesce(IfError(Boolean(a.Value.Kritisch); false); false); "<br><b style='color:#B3261E'>KRITISCH – " & If(Coalesce(IfError(Boolean(a.Value.KritischOk); false); false); "Bescheid gegeben, bestätigt von " …
```

**Kurz erklärt:** Protokoll: Abschnitt-Überschriften, Bereichsname nur wenn nicht ausgeblendet, Zeile „KRITISCH – Bescheid gegeben, bestätigt von … um …“.

**Nachprüfen:** Ende der Formel: `)`

### 7.2 · `btnRuAbschluss.OnSelect`

**Pfad:** `scrRundgang › conRuFuss › btnRuAbschluss` → OnSelect

```
If(!varIsLoading && Now() >= varSperreBis;
    If(!varAbschlussFrage;
        Set(varAbschlussFrage; true);;
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
                        IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSoll)}); Set(varPatchFehler; true));;
                        Refresh(RG_Durchfuehrungen);;
                        Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));;
                        If(varDurch.Status = stAbgeschlossen;
                            Notify("Rundgang abgeschlossen · " & CountRows(colMaengelSoll) & " Mängel erfasst. Protokoll wird archiviert …"; NotificationType.Success);;
                                Set(varArchivStart; false);;
                                Navigate(scrProtokoll; ScreenTransition.None);
                            Notify("Der Abschluss wurde nicht bestätigt. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error)
                        )
                    )
                )
            )
        );;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
    )
)
```

**Das ändert sich:**

```diff
-                                     Frage: Left(Text(n.Value.Frage); 255);
+                                     Frage: Left(If(Coalesce(Text(n.Value.Abschnitt); "") = ""; ""; Text(n.Value.Abschnitt) & " › ") & Text(n.Value.Frage); 255);
-                                     Kommentar: Coalesce(Text(n.Value.Kommentar); "");
+                                     Kommentar: If(Coalesce(IfError(Boolean(n.Value.Kritisch); false); false); "KRITISCH – Bescheid gegeben " & Coalesce(Text(n.Value.KritischZeit); "") & ". "; "") & Coalesce(Text(n.Value.Kommentar); "");
```

**Kurz erklärt:** Mängel: Frage mit Abschnitt („Kompressor 1 › Betriebsdruck“), Kommentar beginnt bei kritisch mit „KRITISCH – Bescheid gegeben hh:mm.“

**Nachprüfen:** Ende der Formel: `)`

## Schritt 8 – Fenster „Ist das wirklich so?“

### 8.1 · neues Steuerelement `conKaRueck`

**Wo hin:** **`scrKategorie`** (den Bildschirm) markieren → Strg+V. Der Block landet ganz oben und liegt damit über allem.

```yaml
- conKaRueck:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      Fill: =RGBA(0, 0, 0, 0.45)
      Height: =Parent.Height
      Visible: =varRueckPP > 0
      Width: =Parent.Width
    Children:
    - btnKaRueckSperre:
        Control: Classic/Button@2.2.0
        Properties:
          BorderThickness: =0
          Fill: =RGBA(0, 0, 0, 0)
          Height: =Parent.Height
          HoverFill: =RGBA(0, 0, 0, 0)
          PressedFill: =RGBA(0, 0, 0, 0)
          Text: =""
          Width: =Parent.Width
    - conKaRueckKarte:
        Control: GroupContainer@1.5.0
        Variant: ManualLayout
        Properties:
          Fill: =clrKarte
          Height: =440
          RadiusBottomLeft: =16
          RadiusBottomRight: =16
          RadiusTopLeft: =16
          RadiusTopRight: =16
          Width: =Parent.Width - 48
          X: =24
          Y: =(Parent.Height - Self.Height) / 2
        Children:
        - lblKaRueckTitel:
            Control: Label@2.5.1
            Properties:
              Color: =clrText
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =48
              Size: =21
              Text: ="Ist das wirklich so?"
              Width: =Parent.Width - 48
              X: =24
              Y: =20
        - lblKaRueckFrage:
            Control: Label@2.5.1
            Properties:
              Color: =clrText
              Font: =Font.'Segoe UI'
              Height: =96
              Size: =17
              Text: |-
                =With({r: LookUp(colAntworten, PruefpunktID = varRueckPP)}, r.Frage & Char(10) & "Ihre Antwort: " & If(r.Typ = "ZAHL", Text(r.WertZahl) & " " & r.Einheit, "n.i.O."))
              VerticalAlign: =VerticalAlign.Top
              Width: =Parent.Width - 48
              X: =24
              Y: =76
        - lblKaRueckNormal:
            Control: Label@2.5.1
            Properties:
              Color: =clrWarnung
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =120
              Size: =17
              Text: |-
                =With({r: LookUp(colAntworten, PruefpunktID = varRueckPP)}, If(Trim(r.RueckfrageText) <> "", r.RueckfrageText, r.Typ = "ZAHL" && (!IsBlank(r.MinWert) || !IsBlank(r.MaxWert)), "Normalerweise: " & If(IsBlank(r.MinWert), "", "ab " & Text(r.MinWert) & " ") & If(IsBlank(r.MaxWert), "", "bis " & Text(r.MaxWert) & " ") & r.Einheit, "Bitte noch einmal genau nachsehen."))
              VerticalAlign: =VerticalAlign.Top
              Width: =Parent.Width - 48
              X: =24
              Y: =180
        - btnKaRueckNein:
            Control: Classic/Button@2.2.0
            Properties:
              BorderColor: =clrPrimaer
              BorderThickness: =1
              Color: =clrPrimaer
              Fill: =clrKarte
              Font: =Font.'Segoe UI'
              Height: =64
              HoverColor: =clrPrimaer
              HoverFill: =clrPrimaerHell
              OnSelect: |-
                =Patch(colAntworten, LookUp(colAntworten, PruefpunktID = varRueckPP), {Bewertung: "", WertZahl: Blank(), KritischOk: false, KritischZeit: ""});
                Set(varRueckPP, 0);
                Set(varGeaendert, true)
              PressedColor: =clrPrimaer
              PressedFill: =clrPrimaerHell
              RadiusBottomLeft: =10
              RadiusBottomRight: =10
              RadiusTopLeft: =10
              RadiusTopRight: =10
              Size: =17
              Text: ="Nein, korrigieren"
              Width: =(Parent.Width - 64) / 2
              X: =24
              Y: =Parent.Height - 88
        - btnKaRueckJa:
            Control: Classic/Button@2.2.0
            Properties:
              BorderThickness: =0
              Color: =Color.White
              Fill: =clrPrimaer
              Font: =Font.'Segoe UI'
              Height: =64
              HoverFill: =ColorFade(clrPrimaer, -20%)
              OnSelect: |-
                =With({r: LookUp(colAntworten, PruefpunktID = varRueckPP)},
                    Set(varRueckPP, 0);
                    If(r.Kritisch && !r.KritischOk, Set(varKritPP, r.PruefpunktID))
                )
              PressedFill: =ColorFade(clrPrimaer, -35%)
              RadiusBottomLeft: =10
              RadiusBottomRight: =10
              RadiusTopLeft: =10
              RadiusTopRight: =10
              Size: =17
              Text: ="Ja, stimmt"
              Width: =(Parent.Width - 64) / 2
              X: =40 + (Parent.Width - 64) / 2
              Y: =Parent.Height - 88
```

**Nachprüfen:** liegt direkt unter `scrKategorie`, ganz oben in der Liste, kein `_1`.

## Schritt 9 – Fenster „Kritischer Mangel“

### 9.1 · neues Steuerelement `conKaKrit`

**Wo hin:** **`scrKategorie`** (den Bildschirm) markieren → Strg+V. Der Block landet ganz oben und liegt damit über allem.

```yaml
- conKaKrit:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      Fill: =RGBA(179, 38, 30, 0.55)
      Height: =Parent.Height
      Visible: =varKritPP > 0
      Width: =Parent.Width
    Children:
    - btnKaKritSperre:
        Control: Classic/Button@2.2.0
        Properties:
          BorderThickness: =0
          Fill: =RGBA(0, 0, 0, 0)
          Height: =Parent.Height
          HoverFill: =RGBA(0, 0, 0, 0)
          PressedFill: =RGBA(0, 0, 0, 0)
          Text: =""
          Width: =Parent.Width
    - conKaKritKarte:
        Control: GroupContainer@1.5.0
        Variant: ManualLayout
        Properties:
          BorderColor: =clrFehler
          BorderThickness: =4
          Fill: =clrKarte
          Height: =Min(Parent.Height - 48, 820)
          RadiusBottomLeft: =16
          RadiusBottomRight: =16
          RadiusTopLeft: =16
          RadiusTopRight: =16
          Width: =Parent.Width - 48
          X: =24
          Y: =(Parent.Height - Self.Height) / 2
        Children:
        - lblKaKritTitel:
            Control: Label@2.5.1
            Properties:
              Align: =Align.Center
              Color: =Color.White
              Fill: =clrFehler
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =72
              Size: =21
              Text: ="⚠ Kritischer Mangel – sofort melden"
              Width: =Parent.Width
              X: =0
              Y: =0
        - lblKaKritFrage:
            Control: Label@2.5.1
            Properties:
              Color: =clrText
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =64
              Size: =18
              Text: =LookUp(colAntworten, PruefpunktID = varKritPP).Frage
              VerticalAlign: =VerticalAlign.Top
              Width: =Parent.Width - 48
              X: =24
              Y: =88
        - lblKaKritText:
            Control: Label@2.5.1
            Properties:
              Color: =clrFehler
              Font: =Font.'Segoe UI'
              Height: =84
              Size: =17
              Text: =Coalesce(LookUp(colAntworten, PruefpunktID = varKritPP).KritischText, "")
              VerticalAlign: =VerticalAlign.Top
              Width: =Parent.Width - 48
              X: =24
              Y: =152
        - lblKaKritMelden:
            Control: Label@2.5.1
            Properties:
              Color: =clrText
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =32
              Size: =16
              Text: ="Bitte jetzt Bescheid geben bei:"
              Width: =Parent.Width - 48
              X: =24
              Y: =244
        - galKaKritKontakte:
            Control: Gallery@2.15.0
            Variant: Vertical
            Properties:
              AccessibleLabel: ="Ansprechpartner"
              Height: =Parent.Height - 280 - 172
              Items: =If(varKritPP > 0, Sort(Filter(colKontakte As k, Coalesce(k.Allgemein, false) || CountRows(Filter(Split(Coalesce(LookUp(colAntworten, PruefpunktID = varKritPP).Ansprechpartner, ""), ";") As s, Trim(s.Value) = Text(k.ID))) > 0), If(Coalesce(Allgemein, false), 1, 0)), Filter(colKontakte, false))
              ShowScrollbar: =true
              TemplatePadding: =0
              TemplateSize: =92
              Width: =Parent.Width - 48
              X: =24
              Y: =280
            Children:
            - lblKaKritRolle:
                Control: Label@2.5.1
                Properties:
                  Color: =clrFehler
                  Font: =Font.'Segoe UI'
                  FontWeight: =FontWeight.Semibold
                  Height: =28
                  Size: =15
                  Text: =ThisItem.Title
                  Width: =Parent.TemplateWidth
                  X: =0
                  Y: =4
            - lblKaKritName:
                Control: Label@2.5.1
                Properties:
                  Color: =clrText
                  Font: =Font.'Segoe UI'
                  Height: =30
                  Size: =17
                  Text: =Coalesce(ThisItem.Name, "") & If(Trim(Coalesce(ThisItem.Telefon, "")) = "", "", "  ·  ☎ " & ThisItem.Telefon)
                  Width: =Parent.TemplateWidth
                  X: =0
                  Y: =32
            - lblKaKritHinweis:
                Control: Label@2.5.1
                Properties:
                  Color: =clrTextGrau
                  Font: =Font.'Segoe UI'
                  Height: =26
                  Size: =13
                  Text: =Coalesce(ThisItem.Hinweis, "")
                  Width: =Parent.TemplateWidth
                  Wrap: =false
                  X: =0
                  Y: =62
        - lblKaKritLeer:
            Control: Label@2.5.1
            Properties:
              Color: =clrFehler
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =64
              Size: =16
              Text: ="Keine Ansprechpartner hinterlegt. Bitte die Schichtleitung bzw. den Vorgesetzten informieren."
              Visible: =IsEmpty(galKaKritKontakte.AllItems)
              Width: =Parent.Width - 48
              X: =24
              Y: =284
        - btnKaKritOk:
            Control: Classic/Button@2.2.0
            Properties:
              BorderThickness: =0
              Color: =Color.White
              Fill: =clrFehler
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =68
              HoverFill: =ColorFade(clrFehler, -15%)
              OnSelect: |-
                =Patch(colAntworten, LookUp(colAntworten, PruefpunktID = varKritPP), {KritischOk: true, KritischZeit: Text(Now(), "hh:mm")});
                Set(varKritPP, 0);
                Set(varGeaendert, true)
              PressedFill: =ColorFade(clrFehler, -30%)
              RadiusBottomLeft: =10
              RadiusBottomRight: =10
              RadiusTopLeft: =10
              RadiusTopRight: =10
              Size: =19
              Text: ="Ich habe Bescheid gegeben"
              Width: =Parent.Width - 48
              X: =24
              Y: =Parent.Height - 160
        - btnKaKritVersehen:
            Control: Classic/Button@2.2.0
            Properties:
              BorderColor: =clrTextGrau
              BorderThickness: =1
              Color: =clrTextGrau
              Fill: =clrKarte
              Font: =Font.'Segoe UI'
              Height: =56
              HoverColor: =clrText
              HoverFill: =clrHintergrund
              OnSelect: |-
                =Patch(colAntworten, LookUp(colAntworten, PruefpunktID = varKritPP), {Bewertung: "", WertZahl: Blank(), KritischOk: false, KritischZeit: ""});
                Set(varKritPP, 0);
                Set(varGeaendert, true)
              PressedColor: =clrText
              PressedFill: =clrHintergrund
              RadiusBottomLeft: =10
              RadiusBottomRight: =10
              RadiusTopLeft: =10
              RadiusTopRight: =10
              Size: =15
              Text: ="n.i.O. war ein Versehen – Antwort zurücknehmen"
              Width: =Parent.Width - 48
              X: =24
              Y: =Parent.Height - 80
```

**Nachprüfen:** liegt direkt unter `scrKategorie`, ganz oben in der Liste, kein `_1`.

## Test (Zeitachse, nur ZZ-Test-Rundgang)

| # | Schritt | erwartet |
|---|---|---|
| T1 | Im Builder zwei Prüfpunkten derselben Kategorie Abschnitt „Kompressor 1“ geben, aktivieren. Rundgang heute starten, Kategorie öffnen | Überschrift „Kompressor 1“ über der ersten der beiden Fragen |
| T2 | Bereich im Builder ausblenden, aktivieren, Rundgang **neu starten** (am Testtag zurücksetzen) | Rundgangsübersicht ohne Bereichs-Überschrift, Kopfzeile ohne Bereich |
| T3 | Prüfpunkt mit Rückfrage: n.i.O. | Fenster „Ist das wirklich so?“ mit Text. „Nein, korrigieren“ → Antwort leer |
| T4 | n.i.O., „Ja, stimmt“ (Punkt auch kritisch) | rotes Fenster mit „Elektriker“ und „Allgemein“ |
| T5 | Im roten Fenster nichts tun, App neu laden, Kategorie öffnen, Speichern | „Noch offen … (kritisch: Bescheid bestätigen)“, rotes Fenster kommt wieder |
| T6 | „Ich habe Bescheid gegeben“, Kommentar, Speichern | gespeichert. Protokoll: „KRITISCH – Bescheid gegeben, bestätigt von … um …“ |
| T7 | Rundgang abschließen | Mangel: Frage mit Abschnitt, Kommentar beginnt mit „KRITISCH – Bescheid gegeben“ |
| T8 | Zahl mit Grenzen und Rückfrage: Wert außerhalb | Rückfrage „Normalerweise: ab … bis …“ |

## Rückweg

Vorher-Fassungen im Anhang einsetzen, die zwei Fenster und `lblKaAbschnitt` löschen. Spalten und Liste dürfen bleiben.

## Anhang – Vorher-Fassungen (= Stand nach Paket N)

**`scrKategorie.OnVisible` vorher**

```
Set(varIsLoading; true);;
Set(varZurueckFrage; false);;
Set(varAlleIOFrage; false);;
Set(varZeigeFehlend; false);;
Set(varFotoPP; 0);;
Set(varBildID; 0);;
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
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); BildID: Coalesce(pp.HinweisBildID; 0); Inaktiv: false}
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
                     Warnung: false;
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Warnung: Coalesce(IfError(Boolean(o.Value.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); BildID: 0; Inaktiv: true}
            )
        )
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
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

**`btnKaNIO.OnSelect` vorher**

```
Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {Bewertung: If(ThisItem.Bewertung = "NIO"; ""; "NIO")});;
Set(varGeaendert; true)
```

**`txtKaZahl.OnChange` vorher**

```
With({z: IfError(Value(Self.Text); Blank())};
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertZahl: z; Bewertung: If(IsBlank(z); ""; fnZahlBewertung(z; ThisItem.MinWert; ThisItem.MaxWert; ThisItem.Grenzmodus))})
);;
Set(varGeaendert; true)
```

**`lblKaFehlendAnzahl.Text` vorher**

```
CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert)))
```

**`lblKaFehlend.Text` vorher**

```
Concat(Filter(Sort(colAntworten; Reihenfolge) As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))) && fnFehlt(a.Typ; a.Pflicht; a.Bewertung; a.WertText; a.WertZahl; a.Kommentar; a.FotoModus; CountRows(Filter(colFotos; PruefpunktID = a.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(a.Fotos); a.KommentarPflicht; a.Grenzmodus; a.MinWert; a.MaxWert)) As z; z.Frage & Switch(fnFehltGrund(z.Typ; z.Pflicht; z.Bewertung; z.WertText; z.WertZahl; z.Kommentar; z.FotoModus; CountRows(Filter(colFotos; PruefpunktID = z.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(z.Fotos); z.KommentarPflicht; z.Grenzmodus; z.MinWert; z.MaxWert); "Kommentar"; " (Kommentar)"; "Foto"; " (Foto)"; "Bereich"; " (unzulässiger Wert)"; "Uhrzeit"; " (Uhrzeit)"; ""); "; ")
```

**`conKaKarte.BorderColor` vorher**

```
If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos); ThisItem.KommentarPflicht; ThisItem.Grenzmodus; ThisItem.MinWert; ThisItem.MaxWert)); clrFehler; clrRahmen)
```

**`conKaKarte.BorderThickness` vorher**

```
If(ThisItem.Bewertung = "NIO" || (varZeigeFehlend && fnFehlt(ThisItem.Typ; ThisItem.Pflicht; ThisItem.Bewertung; ThisItem.WertText; ThisItem.WertZahl; ThisItem.Kommentar; ThisItem.FotoModus; CountRows(Filter(colFotos; PruefpunktID = ThisItem.PruefpunktID && !Uebernommen)) + fnLinkAnzahl(ThisItem.Fotos); ThisItem.KommentarPflicht; ThisItem.Grenzmodus; ThisItem.MinWert; ThisItem.MaxWert)); 2; 1)
```

**`btnKaSpeichern.OnSelect` vorher**

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
                    Set(varAntwortJSON; JSON(ShowColumns(colSpeichern; PruefpunktID; Frage; Typ; Bewertung; WertZahl; WertText; Einheit; Kommentar; Fotos; Warnung; Ausgeblendet); JSONFormat.Compact));;
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

**`conKaKarte.Y` vorher**

```
8
```

**`btnRgAktion.OnSelect` vorher**

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
                With({kk: Sort(AddColumns(Filter(k As kat; CountRows(Filter(b As be; be.ID = kat.BereichID)) > 0); BReihe; LookUp(b As be2; be2.ID = BereichID).RgReihenfolge; BName; LookUp(b As be3; be3.ID = BereichID).Title); BReihe * 10000 + RgReihenfolge)};
                    ClearCollect(colKatBau; ForAll(Sequence(CountRows(kk)) As s; With({z: Index(kk; s.Value)}; {KategorieID: z.ID; Position: s.Value; BereichName: z.BName; KategorieName: z.Title})))
                )
            );;
            If(CountRows(colKatBau) = 0;
                Notify("Für diesen Rundgang sind keine aktiven Kategorien hinterlegt."; NotificationType.Error);
                IfError(
                    Patch(RG_Durchfuehrungen; Defaults(RG_Durchfuehrungen); {Title: varSchluessel; RundgangID: varRgID; RundgangName: ThisItem.Title; TagText: varTagText; KW: ISOWeekNum(varTag); Wochentag: Weekday(varTag; StartOfWeek.Monday); Status: stInArbeit; AnzahlKategorien: CountRows(colKatBau); KategorieListe: JSON(colKatBau; JSONFormat.Compact); PrueferEmail: User().Email; PrueferName: User().FullName; StartZeit: Now(); TestDatensatz: StartsWith(ThisItem.Title; "ZZ Test")});
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

**`galRuKategorien.Items` vorher**

```
With({liste: AddColumns(colKatListe; Erledigt; !IsBlank(LookUp(colErledigt As e; e.KategorieID = KategorieID)))};
    Sort(
        AddColumns(liste;
            Zustand; If(Erledigt; "erledigt"; Position = Min(Filter(liste As l; !l.Erledigt); Position); "naechste"; "gesperrt");
            ErsteImBereich; Position = Min(Filter(liste As l2; l2.BereichName = BereichName); Position);
            NIO; Coalesce(LookUp(colErledigt As e2; e2.KategorieID = KategorieID).AnzahlNIO; 0)
        );
        Position
    )
)
```

**`lblKaUnter.Text` vorher**

```
varBereichName & "  ·  Kategorie " & varKatPos & " von " & CountRows(colKatListe) & If(varNurLesen; "  ·  nur Ansicht"; "  ·  " & (CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))) - Value(lblKaFehlendAnzahl.Text)) & " von " & CountRows(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl))))) & " ausgefüllt")
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

**`btnRuAbschluss.OnSelect` vorher**

```
If(!varIsLoading && Now() >= varSperreBis;
    If(!varAbschlussFrage;
        Set(varAbschlussFrage; true);;
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
                                     Frage: Left(Text(n.Value.Frage); 255);
                                     Wert: Left(Coalesce(Text(n.Value.WertText); "") & If(IsBlank(n.Value.WertZahl); ""; Text(Value(n.Value.WertZahl)) & " " & Coalesce(Text(n.Value.Einheit); "")); 255);
                                     Kommentar: Coalesce(Text(n.Value.Kommentar); "");
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
                        IfError(Patch(RG_Durchfuehrungen; LookUp(RG_Durchfuehrungen; ID = varDurchID); {Status: stAbgeschlossen; EndeZeit: Now(); AnzahlNIO: CountRows(colMaengelSoll)}); Set(varPatchFehler; true));;
                        Refresh(RG_Durchfuehrungen);;
                        Set(varDurch; LookUp(RG_Durchfuehrungen; ID = varDurchID));;
                        If(varDurch.Status = stAbgeschlossen;
                            Notify("Rundgang abgeschlossen · " & CountRows(colMaengelSoll) & " Mängel erfasst. Protokoll wird archiviert …"; NotificationType.Success);;
                                Set(varArchivStart; false);;
                                Navigate(scrProtokoll; ScreenTransition.None);
                            Notify("Der Abschluss wurde nicht bestätigt. Bitte erneut versuchen." & If(varPatchFehler; " (SharePoint hat einen Schreibfehler gemeldet – Verbindung prüfen.)"; ""); NotificationType.Error)
                        )
                    )
                )
            )
        );;
        Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
        Set(varIsLoading; false)
    )
)
```

