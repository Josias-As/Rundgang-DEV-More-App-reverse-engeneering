# Baukasten-Paket 6 – Hinweis mit Beispielbild

Stand: 27.10.2026 · erzeugt mit `werkzeuge/baukasten.py` aus dem Export `2026-10-27_0909`.

## Kurzfassung

- Neue Bildbibliothek **RG_Hinweisbilder** und neue Zahlspalte **HinweisBildID** am Prüfpunkt (Id des Bilds in der Bibliothek, 0 = keins).
- Hat ein Punkt ein Bild, steht rechts oben in der Karte ein kleiner Knopf „Bild“ (64 px, die Frage wird nur 80 px schmaler). Tippen öffnet ein Fenster mit dem Bild in voller Breite.
- Statt „in der Karte aufklappen“ (Übergabe) ein Fenster: größeres Bild auf dem Tablet, keine wechselnde Kartenhöhe (Falle E-05). Bitte bestätigen.
- Das Bild wird erst beim Öffnen geladen (eine Abfrage), nicht für jede Karte.
- Vorab-Test (Schritt 6.3) klärt, ob die Vorschaubilder der Bibliothek in der App ankommen; sonst Abbruch ohne Änderung.

## Voraussetzungen

- Pakete 1–5 eingefügt und getestet.
- Die Blöcke sind aus dem Export 27.10.2026 09:09 (`frischerexport_20261027090933.zip`) erzeugt. Hat sich die App seitdem geändert, erst einen neuen Export schicken; der Generator bricht ab, wenn ein Vorher-Stand nicht mehr passt.

## Schritte

### Schritt 6.1 – Sicherung

Studio: oben **Speichern**. Dann make.powerapps.com → Apps → „Rundgang DEV“ → … → **Details → Versionen**: die oberste Versionsnummer notieren. Das ist der Rückweg auf Knopfdruck (Version wiederherstellen).

### Schritt 6.2 – SharePoint: Bibliothek und Spalte

IMS+ → Neu → **Dokumentbibliothek** „**RG_Hinweisbilder**“. Rechte wie die anderen RG-Bibliotheken (alle lesen). Ein Testbild hochladen (JPG/PNG), dessen **ID** notieren (Ansicht → Spalte ID einblenden).
RG_Pruefpunkte → **+ Spalte → Zahl**: **HinweisBildID**, 0 Dezimalstellen, Standardwert **0**.
Für den Test: Prüfpunkt Id 10 → HinweisBildID = ID des Testbilds. Nach dem Hochladen ein paar Minuten warten (SharePoint erzeugt die Vorschaubilder verzögert).
Danach in Studio: **Daten** → `RG_Pruefpunkte` → … → **Aktualisieren**.

### Schritt 6.3 – Datenquelle und Vorab-Test

Studio → **Daten → Daten hinzufügen → SharePoint → IMS+ → RG_Hinweisbilder** (die bestehende SharePoint-Verbindung wird benutzt, kein neuer Berechtigungsdialog erwartet; falls doch einer kommt: abbrechen und mir Bescheid geben). Danach `RG_Pruefpunkte` aktualisieren.
Vorab-Test: auf `scrKategorie` vorübergehend ein Bild-Steuerelement einfügen, Image = `LookUp(RG_Hinweisbilder; ID = <Test-ID>).Thumbnail.Large`. Zeigt es das Bild → weiter. Zeigt es nichts → **Abbruch**, Bild-Steuerelement löschen, mir Bescheid geben (Ausweg: Bildspalte in RG_Pruefpunkte). Teststeuerelement danach löschen.

### Schritt 6.4 – Kategorie öffnen

`scrKategorie.OnVisible`: Feld BildID, Fenster beim Öffnen zu.

**`scrKategorie.OnVisible`**

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

### Schritt 6.5 – Knopf in der Karte

`lblKaFrage.Width` ersetzen. Dann in `conKaKarte` `txtKaText` markieren und den YAML-Block einfügen.

**`lblKaFrage.Width`**

```
Parent.Width - 40 - If(ThisItem.BildID > 0; 80; 0)
```

**YAML `btnKaBild`** (englische Schreibweise, so wie es ist einfügen):

```yaml
- btnKaBild:
    Control: Classic/Button@2.2.0
    Properties:
      BorderColor: =clrPrimaer
      BorderThickness: =1
      Color: =clrPrimaer
      Fill: =clrKarte
      Font: =Font.'Segoe UI'
      Height: =34
      HoverColor: =clrPrimaer
      HoverFill: =clrPrimaerHell
      OnSelect: |-
        =Set(varBildFrage, ThisItem.Frage);
        Set(varBildID, ThisItem.BildID)
      PressedColor: =clrPrimaer
      PressedFill: =clrPrimaerHell
      RadiusBottomLeft: =8
      RadiusBottomRight: =8
      RadiusTopLeft: =8
      RadiusTopRight: =8
      Size: =14
      Text: ="Bild"
      Visible: =ThisItem.BildID > 0
      Width: =64
      X: =Parent.Width - 84
      Y: =10
```

Prüfen nach dem Schritt:
- `btnKaBild` liegt in `conKaKarte`, X = Parent.Width - 84, Y = 10, Höhe 34 (endet über `lblKaHinweis` bei Y 46).

### Schritt 6.6 – Bildfenster

Den Bildschirm `scrKategorie` in der Strukturansicht markieren und den YAML-Block einfügen. `conKaBild` muss in der Strukturansicht **ganz oben** stehen (vor `conKaFoto` und `conKaLaden`), sonst per Rechtsklick → **Nach vorne bringen**.

**YAML `conKaBild`** (englische Schreibweise, so wie es ist einfügen):

```yaml
- conKaBild:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      Fill: =RGBA(0, 0, 0, 0.45)
      Height: =Parent.Height
      Visible: =varBildID > 0
      Width: =Parent.Width
    Children:
    - btnKaBildSperre:
        Control: Classic/Button@2.2.0
        Properties:
          BorderThickness: =0
          Fill: =RGBA(0, 0, 0, 0)
          Height: =Parent.Height
          HoverFill: =RGBA(0, 0, 0, 0)
          PressedFill: =RGBA(0, 0, 0, 0)
          Text: =""
          Width: =Parent.Width
    - conKaBildKarte:
        Control: GroupContainer@1.5.0
        Variant: ManualLayout
        Properties:
          Fill: =clrKarte
          Height: =Min(Parent.Height - 32, 900)
          RadiusBottomLeft: =16
          RadiusBottomRight: =16
          RadiusTopLeft: =16
          RadiusTopRight: =16
          Width: =Parent.Width - 48
          X: =24
          Y: =(Parent.Height - Self.Height) / 2
        Children:
        - lblKaBildTitel:
            Control: Label@2.5.1
            Properties:
              Color: =clrText
              Font: =Font.'Segoe UI'
              FontWeight: =FontWeight.Semibold
              Height: =56
              Size: =18
              Text: ="Beispiel – " & varBildFrage
              Width: =Parent.Width - 40
              X: =20
              Y: =12
        - imgKaBild:
            Control: Image@2.2.3
            Properties:
              AccessibleLabel: ="Beispielbild zu " & varBildFrage
              Height: =Parent.Height - 76 - 96
              Image: =If(varBildID > 0, LookUp(RG_Hinweisbilder, ID = varBildID).Thumbnail.Large)
              ImagePosition: =ImagePosition.Fit
              Width: =Parent.Width - 40
              X: =20
              Y: =76
        - btnKaBildSchliessen:
            Control: Classic/Button@2.2.0
            Properties:
              BorderThickness: =0
              Color: =Color.White
              Fill: =clrPrimaer
              Font: =Font.'Segoe UI'
              Height: =56
              HoverFill: =ColorFade(clrPrimaer, -20%)
              OnSelect: =Set(varBildID, 0)
              PressedFill: =ColorFade(clrPrimaer, -35%)
              Size: =17
              Text: ="Schließen"
              Width: =200
              X: =Parent.Width - 220
              Y: =Parent.Height - 76
```

Prüfen nach dem Schritt:
- Beim Einfügen eines Containers bleiben die Kinder in ihm (Strukturansicht prüfen).

### Schritt 6.7 – App-Prüfung und Speichern

Studio → **App-Prüfung → Formeln**: muss **0** sein (Barrierefreiheit/Leistung wie bisher, siehe E-07/E-08). Dann **Speichern** (noch nicht veröffentlichen) und den Test unten in der **Vorschau** machen.
Bei einem Formelfehler: Fehlermeldung und Steuerelement notieren, nicht selbst umbauen, mir schicken.

## Test

| # | Klickfolge | erwartet |
|---|---|---|
| T6.1 | K1 öffnen | Karte von P10: rechts oben „Bild“, Fragetext endet davor (lange Frage: ggf. abgeschnitten wie bisher, nur 80 px früher) |
| T6.2 | „Bild“ tippen | Fenster mit Titel „Beispiel – …“ und Bild; Rest der App nicht tippbar |
| T6.3 | „Schließen“ | Fenster zu |
| T6.4 | Punkt ohne Bild | kein Knopf |
| T6.5 | Nur-Ansicht nach Abschluss | Knopf vorhanden, Bild lässt sich ansehen (Bild aus den heutigen Stammdaten) |
| T6.6 | HinweisBildID auf eine nicht vorhandene Id, aktualisieren, Vorschau neu | Fenster öffnet, Bildfläche leer, „Schließen“ geht |
| T6.7 | Am Tablet (veröffentlicht oder Studio im Tablet-Browser) | Bild erscheint auch dort |

Hinweis: Das Zurücksetzen des Fensters in OnVisible ist eine Absicherung; über die Oberfläche lässt sich die Kategorie bei offenem Fenster nicht verlassen (Hintergrund gesperrt).

## Rückweg

- Version wiederherstellen, oder `conKaBild` und `btnKaBild` löschen und die Vorher-Blöcke einfügen. Spalte und Bibliothek dürfen bleiben.

## Anhang – Vorher-Fassungen (für den Rückweg)

Ohne Kommentare, sonst zeichengleich mit dem Export. Standardwerte sind mit „(Standard)“ markiert.

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
                         Bewertung: Coalesce(Text(a.Bewertung); ""); WertText: Coalesce(Text(a.WertText); ""); WertZahl: Value(a.WertZahl); Kommentar: Coalesce(Text(a.Kommentar); ""); Fotos: Coalesce(Text(a.Fotos); ""); FotoModus: fnFotoModus(pp.Foto.Value; Coalesce(pp.FotoMoeglich; false)); KommentarPflicht: false; Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value); Warnung: Coalesce(IfError(Boolean(a.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet); false); false); Inaktiv: false}
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
                     Warnung: false;
                     Inaktiv: false}
                )
            )
        );;
        Collect(colAntworten;
            ForAll(Filter(t As j2; IsBlank(LookUp(colPP; ID = Value(j2.Value.PruefpunktID)))) As o;
                {PruefpunktID: Value(o.Value.PruefpunktID); Frage: Text(o.Value.Frage); Typ: Text(o.Value.Typ); Pflicht: false; Einheit: Coalesce(Text(o.Value.Einheit); ""); MinWert: Blank(); MaxWert: Blank(); Auswahl: ""; Hinweis: ""; Reihenfolge: 100000 + Value(o.Value.PruefpunktID);
                 Bewertung: Coalesce(Text(o.Value.Bewertung); ""); WertText: Coalesce(Text(o.Value.WertText); ""); WertZahl: Value(o.Value.WertZahl); Kommentar: Coalesce(Text(o.Value.Kommentar); ""); Fotos: Coalesce(Text(o.Value.Fotos); ""); FotoModus: "Aus"; KommentarPflicht: false; Grenzmodus: "Mangel"; Warnung: Coalesce(IfError(Boolean(o.Value.Warnung); false); false); BedID: 0; BedWert: ""; Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet); false); false); Inaktiv: true}
            )
        )
    )
);;
Set(varSprungRec; First(Sort(Filter(colAntworten As a; !a.Inaktiv && If(varNurLesen; !a.Ausgeblendet; With({b: LookUp(colAntworten As b0; b0.PruefpunktID = a.BedID)}; fnSichtbar(a.BedID; a.BedWert; !IsBlank(b); b.BedID; b.Inaktiv; b.Typ; b.Auswahl; b.Bewertung; b.WertText; b.WertZahl)))); Reihenfolge)));;
Reset(galKaPruefpunkte);;
Set(varIsLoading; false)
```

**`lblKaFrage.Width` vorher**

```
Parent.Width - 40
```

