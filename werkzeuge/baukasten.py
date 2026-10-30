"""Baukasten-Pakete 1-7 für die Rundgang-App aus dem Export erzeugen und prüfen.

Aufruf:  python3 -I werkzeuge/baukasten.py <Export-Schlüssel> [--simulation-0844]
Jedes Paket baut auf dem Stand nach dem vorigen Paket auf. Jede Änderung ist eine exakte
Ersetzung im vorherigen Stand (Anker muss genau so oft vorkommen wie angegeben), sonst Abbruch.
Ergebnis: arbeit/2026-10-27_Baukasten/bloecke.json und pruefung_auto.txt
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rg  # noqa: E402

AUS = os.path.join(rg.REPO, "arbeit", "2026-10-27_Baukasten")


class Abbruch(Exception):
    pass


def rep(text, alt, neu, n=1, wo=""):
    c = text.count(alt)
    if c != n:
        raise Abbruch("Anker %dx statt %dx gefunden (%s): %r" % (c, n, wo, alt[:120]))
    return text.replace(alt, neu)


# ---------------------------------------------------------------- Bausteine (englisch)

def fotoanz(p):
    return ("CountRows(Filter(colFotos, PruefpunktID = {p}.PruefpunktID && !Uebernommen)) + fnLinkAnzahl({p}.Fotos)"
            .format(p=p))


def fehlt_args(p):
    return ("{p}.Typ, {p}.Pflicht, {p}.Bewertung, {p}.WertText, {p}.WertZahl, {p}.Kommentar, {p}.FotoModus, "
            + fotoanz(p) + ", {p}.KommentarPflicht, {p}.Grenzmodus, {p}.MinWert, {p}.MaxWert").format(p=p)


def fehlt(p):
    return "fnFehlt(" + fehlt_args(p) + ")"


def komm_args(p):
    return ("{p}.Typ, {p}.Bewertung, {p}.WertText, {p}.WertZahl, {p}.KommentarPflicht, {p}.Grenzmodus, "
            "{p}.MinWert, {p}.MaxWert").format(p=p)


def sicht(p):
    return ("If(varNurLesen, !{p}.Ausgeblendet, With({{b: LookUp(colAntworten As b0, b0.PruefpunktID = {p}.BedID)}}, "
            "fnSichtbar({p}.BedID, {p}.BedWert, !IsBlank(b), b.BedID, b.Inaktiv, b.Typ, b.Auswahl, b.Bewertung, b.WertText, b.WertZahl)))"
            .format(p=p))


GRUENDE = ('Switch(fnFehltGrund(' + fehlt_args("z") + '), "Kommentar", " (Kommentar)", "Foto", " (Foto)", '
           '"Bereich", " (unzulässiger Wert)", "Uhrzeit", " (Uhrzeit)", "")')


# ---------------------------------------------------------------- Zustand

class Stand:
    def __init__(self, app):
        self.app = app
        self.props = {k: v for k, v in app.props.items()}
        self.neue_controls = {}      # Name -> (Eltern, Typ)
        self.sp = []                 # angelegte Spalten (Liste, Name, Typ)
        self.neue_quellen = set()
        self.aenderungen = []        # je Paket

    def roh(self, k):
        return self.props[k]


def aendern(stand, paket, schritt, key, f):
    vorher = stand.props.get(key)
    if vorher is None:
        raise Abbruch("Property fehlt: " + key)
    basis = rg.ohne_kommentare(vorher)
    nachher = f(basis)
    if nachher == vorher:
        raise Abbruch("keine Änderung: " + key)
    stand.props[key] = nachher
    paket["props"].append({"key": key, "schritt": schritt, "vorher": vorher, "nachher": nachher})


def ganz(stand, paket, schritt, key, neu):
    aendern(stand, paket, schritt, key, lambda _: neu)


def standard_ersetzen(stand, paket, schritt, key, standard, neu):
    """Property steht nicht im Export (Studio lässt Standardwerte weg): Vorher = Standardwert."""
    if key in stand.props:
        raise Abbruch("Property ist nicht Standard: " + key)
    if key.split(".")[0] not in stand.app.typ:
        raise Abbruch("Steuerelement fehlt: " + key)
    stand.props[key] = neu
    paket["props"].append({"key": key, "schritt": schritt, "vorher": standard, "nachher": neu, "standard": True})


def neues_control(stand, paket, name, eltern, typ, props):
    if name in stand.app.typ or name in stand.neue_controls:
        raise Abbruch("Name schon vergeben: " + name)
    stand.neue_controls[name] = (eltern, typ)
    for k, v in props.items():
        stand.props[name + "." + k] = v
    paket["neu"].append(name)


# ---------------------------------------------------------------- Paket 1

UDF_P1 = r'''fnLinkAnzahl(t: Text): Number = CountRows(Filter(Split(Coalesce(t, ""), " | ") As s, Trim(s.Value) <> ""));
fnFotoModus(f: Text, alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht", f, alt, "Optional", "Aus");
fnFotoNeuErlaubt(bew: Text, foto: Text): Boolean = bew = "NIO" || foto = "Optional" || foto = "Pflicht";
fnBeantwortet(bew: Text, wt: Text, wz: Number): Boolean = bew <> "" || Trim(wt) <> "" || !IsBlank(wz);
fnAusserhalb(z: Number, mi: Number, ma: Number): Boolean = !IsBlank(z) && ((!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma));
fnKommentarNoetig(typ: Text, bew: Text, wt: Text, wz: Number, kpfl: Boolean, gmodus: Text, mi: Number, ma: Number): Boolean = bew = "NIO";
fnFehltGrund(typ: Text, pflicht: Boolean, bew: Text, wt: Text, wz: Number, kom: Text, foto: Text, fanz: Number, kpfl: Boolean, gmodus: Text, mi: Number, ma: Number): Text = If(
    pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = "")), "Wert",
    fnKommentarNoetig(typ, bew, wt, wz, kpfl, gmodus, mi, ma) && Trim(kom) = "", "Kommentar",
    foto = "Pflicht" && fanz < 1, "Foto",
    ""
);
fnFehlt(typ: Text, pflicht: Boolean, bew: Text, wt: Text, wz: Number, kom: Text, foto: Text, fanz: Number, kpfl: Boolean, gmodus: Text, mi: Number, ma: Number): Boolean = fnFehltGrund(typ, pflicht, bew, wt, wz, kom, foto, fanz, kpfl, gmodus, mi, ma) <> "";'''

ALT_FNFEHLT = 'fnFehlt(typ: Text, pflicht: Boolean, bew: Text, wt: Text, wz: Number, kom: Text): Boolean = (pflicht && ((typ = "IONIO" && bew = "") || (typ = "AUSWAHL" && wt = "") || (typ = "ZAHL" && IsBlank(wz)) || (typ = "TEXT" && Trim(wt) = ""))) || (bew = "NIO" && Trim(kom) = "");'


def paket1(st):
    p = {"nr": 1, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "Foto", "Auswahl"))

    def formulas(t):
        t = rep(t, ALT_FNFEHLT, UDF_P1, wo="App.Formulas fnFehlt")
        t = rep(t, "fnZahlBewertung(z: Number, mi: Number, ma: Number): Text = If(",
                "fnZahlBewertung(z: Number, mi: Number, ma: Number, gmodus: Text): Text = If(", wo="fnZahlBewertung")
        return t
    aendern(st, p, "1.3", "App.Formulas", formulas)

    def onvisible(t):
        t = rep(t, "FotoMoeglich: Coalesce(pp.FotoMoeglich, false), Inaktiv: false}",
                'FotoModus: fnFotoModus(pp.Foto.Value, Coalesce(pp.FotoMoeglich, false)), KommentarPflicht: false, Grenzmodus: "Mangel", Inaktiv: false}',
                wo="Nur-Ansicht")
        t = rep(t, 'Fotos: If(IsBlank(alt), "", Coalesce(Text(alt.Value.Fotos), "")),\n                     Inaktiv: false}',
                'Fotos: If(IsBlank(alt), "", Coalesce(Text(alt.Value.Fotos), "")),\n'
                '                     FotoModus: fnFotoModus(p.Foto.Value, Coalesce(p.FotoMoeglich, false)),\n'
                '                     KommentarPflicht: false,\n'
                '                     Grenzmodus: "Mangel",\n'
                '                     Inaktiv: false}', wo="Bearbeiten")
        t = rep(t, "fnZahlBewertung(Value(alt.Value.WertZahl), p.MinWert, p.MaxWert)",
                'fnZahlBewertung(Value(alt.Value.WertZahl), p.MinWert, p.MaxWert, "Mangel")', wo="Bewertung")
        t = rep(t, "FotoMoeglich: false, Inaktiv: true}",
                'FotoModus: "Aus", KommentarPflicht: false, Grenzmodus: "Mangel", Inaktiv: true}', wo="deaktivierte")
        return t
    aendern(st, p, "1.4", "scrKategorie.OnVisible", onvisible)

    aendern(st, p, "1.5", "txtKaZahl.OnChange",
            lambda t: rep(t, "fnZahlBewertung(z, ThisItem.MinWert, ThisItem.MaxWert)",
                          "fnZahlBewertung(z, ThisItem.MinWert, ThisItem.MaxWert, ThisItem.Grenzmodus)"))

    karte_bed = 'ThisItem.Bewertung = "NIO" || (varZeigeFehlend && ' + fehlt("ThisItem") + ')'
    ganz(st, p, "1.6", "conKaKarte.BorderColor", "If(" + karte_bed + ", clrFehler, clrRahmen)")
    ganz(st, p, "1.6", "conKaKarte.BorderThickness", "If(" + karte_bed + ", 2, 1)")
    ganz(st, p, "1.6", "conKaKarte.Height",
         '54 + If(ThisItem.Hinweis <> "", 24, 0) + 56 + If(txtKaKommentar.Visible || btnKaFoto.Visible, 68, 0) + 20')
    ganz(st, p, "1.6", "lblKaAbstand.Y", "conKaKarte.Y + conKaKarte.Height")
    ganz(st, p, "1.6", "txtKaKommentar.Visible",
         'If(varNurLesen, Trim(ThisItem.Kommentar) <> "" || ThisItem.Bewertung = "NIO", fnKommentarNoetig(' + komm_args("ThisItem") + '))')
    ganz(st, p, "1.6", "btnKaFoto.Visible",
         'fnLinkAnzahl(ThisItem.Fotos) > 0 || (!varNurLesen && (ThisItem.Bewertung = "NIO" || ThisItem.FotoModus <> "Aus"))')
    ganz(st, p, "1.6", "btnKaFoto.Y", '54 + If(ThisItem.Hinweis <> "", 24, 0) + 68')
    ganz(st, p, "1.6", "btnKaFoto.Text",
         'With({n: ' + fotoanz("ThisItem") + '},\n    "📷 Foto" & If(n > 0, " (" & n & ")", If(ThisItem.FotoModus = "Pflicht" && !varNurLesen, " *", ""))\n)')
    ganz(st, p, "1.6", "btnKaFoto.BorderColor", 'If(ThisItem.Bewertung = "NIO", clrFehler, clrPrimaer)')
    ganz(st, p, "1.6", "btnKaFoto.Color", 'If(ThisItem.Bewertung = "NIO", clrFehler, clrPrimaer)')
    ganz(st, p, "1.6", "btnKaFoto.HoverColor", "Self.Color")
    ganz(st, p, "1.6", "btnKaFoto.PressedColor", "Self.Color")
    ganz(st, p, "1.6", "btnKaFoto.HoverFill", 'If(ThisItem.Bewertung = "NIO", clrFehlerHell, clrPrimaerHell)')
    ganz(st, p, "1.6", "btnKaFoto.PressedFill", 'If(ThisItem.Bewertung = "NIO", clrFehlerHell, clrPrimaerHell)')

    ganz(st, p, "1.7", "lblKaFehlendAnzahl.Text",
         "CountRows(Filter(colAntworten As a, !a.Inaktiv && " + fehlt("a") + "))")
    ganz(st, p, "1.7", "lblKaFehlend.Text",
         "Concat(Filter(Sort(colAntworten, Reihenfolge) As a, !a.Inaktiv && " + fehlt("a") + ") As z, z.Frage & "
         + GRUENDE + ', "; ")')

    def speichern(t):
        t = rep(t, "Set(varSprungRec, First(Filter(Sort(Filter(colAntworten, !Inaktiv), Reihenfolge), fnFehlt(Typ, Pflicht, Bewertung, WertText, WertZahl, Kommentar))));",
                "Set(varSprungRec, First(Filter(Sort(Filter(colAntworten, !Inaktiv), Reihenfolge) As a, " + fehlt("a") + ")));",
                wo="Sprung")
        t = rep(t, 'a.Bewertung = "NIO" || Coalesce(LookUp(colPP, ID = a.PruefpunktID).FotoMoeglich, false)', "fnFotoNeuErlaubt(a.Bewertung, a.FotoModus)", n=3, wo="Upload")
        t = rep(t, 'UpdateIf(colAntworten, Bewertung <> "NIO", {Kommentar: ""})',
                'UpdateIf(colAntworten, !Inaktiv && !fnKommentarNoetig(Typ, Bewertung, WertText, WertZahl, KommentarPflicht, Grenzmodus, MinWert, MaxWert), {Kommentar: ""})',
                wo="Kommentar leeren (08:44)")
        return t
    aendern(st, p, "1.8", "btnKaSpeichern.OnSelect", speichern)

    ganz(st, p, "1.9", "lblKaFotoHinweis.Text",
         'If(varNurLesen, "Gespeicherte Fotos (nur Ansicht).", LookUp(colAntworten, PruefpunktID = varFotoPP).FotoModus = "Pflicht", "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren.", '
         '!fnFotoNeuErlaubt(LookUp(colAntworten, PruefpunktID = varFotoPP).Bewertung, LookUp(colAntworten, PruefpunktID = varFotoPP).FotoModus), "Neue Fotos nur bei n.i.O. oder Foto-Modus Optional/Pflicht.", '
         '"Keine Personen fotografieren. Fotos werden beim „Speichern“ hochgeladen.")')
    aendern(st, p, "1.9", "addKaFoto.Visible", lambda _: '!varNurLesen && With({a: LookUp(colAntworten, PruefpunktID = varFotoPP)}, fnFotoNeuErlaubt(a.Bewertung, a.FotoModus))')
    ganz(st, p, "1.9", "addKaFoto.Size", "18")
    standard_ersetzen(st, p, "1.9", "imgKaFotoNeu.Y", "0", "52")
    ganz(st, p, "1.9", "imgKaFotoNeu.Height", "Parent.TemplateHeight - 60")
    return p


# ---------------------------------------------------------------- Paket 2

def paket2(st):
    p = {"nr": 2, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "KommentarPflicht", "Ja/Nein"))
    aendern(st, p, "2.3", "App.Formulas", lambda t: rep(
        t, 'mi: Number, ma: Number): Boolean = bew = "NIO";',
        'mi: Number, ma: Number): Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew, wt, wz));'))
    aendern(st, p, "2.4", "scrKategorie.OnVisible", lambda t: rep(
        t, "                     KommentarPflicht: false,\n",
        "                     KommentarPflicht: Coalesce(p.KommentarPflicht, false),\n"))
    ganz(st, p, "2.5", "txtKaKommentar.HintText",
         'If(ThisItem.Bewertung = "NIO", "Kommentar zum Mangel (Pflicht)", "Kommentar (Pflicht)")')
    ganz(st, p, "2.5", "txtKaKommentar.AccessibleLabel",
         'If(ThisItem.Bewertung = "NIO", "Kommentar zum Mangel: ", "Kommentar: ") & ThisItem.Frage')
    aendern(st, p, "2.6", "htmProtokoll.HtmlText", lambda t: rep(
        t, "\"<br><i style='color:#B3261E'>\" & fnHtml(k)",
        "\"<br><i style='color:\" & If(b = \"NIO\", \"#B3261E\", \"#5F6370\") & \"'>\" & fnHtml(k)"))
    return p


# ---------------------------------------------------------------- Paket 3

def paket3(st):
    p = {"nr": 3, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "Grenzmodus", "Auswahl"))

    def formulas(t):
        t = rep(t, 'clrGesperrtHell = ColorValue("#EEF0F3");',
                'clrGesperrtHell = ColorValue("#EEF0F3");\nclrWarnung = ColorValue("#9A5B00");')
        t = rep(t, 'fnZahlBewertung(z: Number, mi: Number, ma: Number, gmodus: Text): Text = If(\n'
                   '    (!IsBlank(mi) && z < mi) || (!IsBlank(ma) && z > ma),\n    "NIO",\n    "IO"\n);',
                'fnZahlBewertung(z: Number, mi: Number, ma: Number, gmodus: Text): Text = If(\n'
                '    fnAusserhalb(z, mi, ma),\n    Switch(If(gmodus = "Sperren" && !fnSperreGilt(mi, ma), "Mangel", gmodus), "Warnen", "IO", "Sperren", "", "NIO"),\n    "IO"\n);\n'
                'fnGrenzmodus(g: Text): Text = If(g = "Warnen" || g = "Sperren", g, "Mangel");\n'
                'fnSperreGilt(mi: Number, ma: Number): Boolean = IsBlank(mi) || IsBlank(ma) || mi <= ma;')
        t = rep(t, 'Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew, wt, wz));',
                'Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew, wt, wz)) || (typ = "ZAHL" && gmodus = "Warnen" && fnAusserhalb(wz, mi, ma));')
        t = rep(t, '    fnKommentarNoetig(typ, bew, wt, wz, kpfl, gmodus, mi, ma) && Trim(kom) = "", "Kommentar",',
                '    typ = "ZAHL" && gmodus = "Sperren" && fnSperreGilt(mi, ma) && fnAusserhalb(wz, mi, ma), "Bereich",\n'
                '    fnKommentarNoetig(typ, bew, wt, wz, kpfl, gmodus, mi, ma) && Trim(kom) = "", "Kommentar",')
        return t
    aendern(st, p, "3.3", "App.Formulas", formulas)

    def onvisible(t):
        t = rep(t, 'fnZahlBewertung(Value(alt.Value.WertZahl), p.MinWert, p.MaxWert, "Mangel")',
                "fnZahlBewertung(Value(alt.Value.WertZahl), p.MinWert, p.MaxWert, fnGrenzmodus(p.Grenzmodus.Value))")
        t = rep(t, '                     Grenzmodus: "Mangel",\n',
                "                     Grenzmodus: fnGrenzmodus(p.Grenzmodus.Value),\n")
        t = rep(t, 'KommentarPflicht: false, Grenzmodus: "Mangel", Inaktiv: false}',
                "KommentarPflicht: false, Grenzmodus: fnGrenzmodus(pp.Grenzmodus.Value), Warnung: Coalesce(IfError(Boolean(a.Warnung), false), false), Inaktiv: false}")
        t = rep(t, "                     Grenzmodus: fnGrenzmodus(p.Grenzmodus.Value),\n",
                "                     Grenzmodus: fnGrenzmodus(p.Grenzmodus.Value),\n                     Warnung: false,\n")
        t = rep(t, 'KommentarPflicht: false, Grenzmodus: "Mangel", Inaktiv: true}',
                'KommentarPflicht: false, Grenzmodus: "Mangel", Warnung: Coalesce(IfError(Boolean(o.Value.Warnung), false), false), Inaktiv: true}')
        return t
    aendern(st, p, "3.4", "scrKategorie.OnVisible", onvisible)

    aussen = "fnAusserhalb(ThisItem.WertZahl, ThisItem.MinWert, ThisItem.MaxWert)"
    ganz(st, p, "3.5", "lblKaZahlInfo.Text",
         'Trim(ThisItem.Einheit & If(IsBlank(ThisItem.MinWert) && IsBlank(ThisItem.MaxWert), "", "  ·  " & If(ThisItem.Grenzmodus = "Sperren" && fnSperreGilt(ThisItem.MinWert, ThisItem.MaxWert), "zulässig ", "Soll ") & If(IsBlank(ThisItem.MinWert), "", "ab " & ThisItem.MinWert & " ") & If(IsBlank(ThisItem.MaxWert), "", "bis " & ThisItem.MaxWert)) & '
         'If(ThisItem.Bewertung = "NIO", "  ·  außerhalb des Sollbereichs", varNurLesen, If(ThisItem.Warnung, "  ·  außerhalb, begründet", ""), !' + aussen + ', "", '
         'ThisItem.Grenzmodus = "Warnen", If(Trim(ThisItem.Kommentar) = "", "  ·  außerhalb, bitte begründen", "  ·  außerhalb, begründet"), ThisItem.Grenzmodus = "Sperren", "  ·  unzulässig, bitte prüfen", ""))')
    farbe = ('If(ThisItem.Bewertung = "NIO" || (!varNurLesen && ThisItem.Grenzmodus = "Sperren" && ' + aussen + '), clrFehler, '
             'If(varNurLesen, ThisItem.Warnung, ' + aussen + '), clrWarnung, {sonst})')
    ganz(st, p, "3.5", "lblKaZahlInfo.Color", farbe.format(sonst="clrTextGrau"))
    ganz(st, p, "3.5", "txtKaZahl.BorderColor", farbe.format(sonst="clrRahmen"))

    def speichern3(t):
        anker = 'UpdateIf(colAntworten, !Inaktiv && !fnKommentarNoetig(Typ, Bewertung, WertText, WertZahl, KommentarPflicht, Grenzmodus, MinWert, MaxWert), {Kommentar: ""});'
        i = t.index(anker)
        einzug = t[t.rfind("\n", 0, i) + 1:i]
        t = rep(t, anker, anker + "\n" + einzug + 'UpdateIf(colAntworten, !Inaktiv, {Warnung: Typ = "ZAHL" && Grenzmodus = "Warnen" && fnAusserhalb(WertZahl, MinWert, MaxWert)});', wo="Warnung setzen")
        t = rep(t, "ShowColumns(colAntworten, PruefpunktID, Frage, Typ, Bewertung, WertZahl, WertText, Einheit, Kommentar, Fotos), JSONFormat.Compact)",
                "ShowColumns(colAntworten, PruefpunktID, Frage, Typ, Bewertung, WertZahl, WertText, Einheit, Kommentar, Fotos, Warnung), JSONFormat.Compact)", wo="JSON Warnung")
        return t
    aendern(st, p, "3.6", "btnKaSpeichern.OnSelect", speichern3)

    def protokoll(t):
        t = rep(t, "With({b: Text(a.Value.Bewertung), k: Text(a.Value.Kommentar), fo: Text(a.Value.Fotos)},",
                "With({b: Text(a.Value.Bewertung), k: Text(a.Value.Kommentar), fo: Text(a.Value.Fotos), w: Coalesce(IfError(Boolean(a.Value.Warnung), false), false)},")
        t = rep(t, 'color:" & If(b = "NIO", "#B3261E", "#0F7B3F")', 'color:" & If(b = "NIO", "#B3261E", w, "#9A5B00", "#0F7B3F")')
        t = rep(t, "fnHtml(Text(a.Value.Einheit))) &",
                "fnHtml(Text(a.Value.Einheit))) & If(w, \" <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>\", \"\") &")
        return t
    aendern(st, p, "3.7", "htmProtokoll.HtmlText", protokoll)
    return p


# ---------------------------------------------------------------- Paket 4

UDF_P4 = r'''fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w, "")), ".", ""), " ", ""));
fnBedGueltig(w: Text, typ: Text, auswahl: Text): Boolean = With({n: fnBedNorm(w)}, n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl, ";") As s, fnBedNorm(s.Value) = n)) > 0));
fnBedPasst(w: Text, bew: Text, wt: Text, wz: Number): Boolean = With({n: fnBedNorm(w)}, If(n = "*", fnBeantwortet(bew, wt, wz), n = fnBedNorm(bew) || n = fnBedNorm(wt) || CountRows(Filter(Split(wt, ";") As s, fnBedNorm(s.Value) = n)) > 0));
fnSichtbar(bid: Number, w: Text, gef: Boolean, bBid: Number, bInaktiv: Boolean, bTyp: Text, bAuswahl: Text, bBew: Text, bWt: Text, bWz: Number): Boolean = bid = 0 || Trim(w) = "" || !gef || bInaktiv || bBid <> 0 || !fnBedGueltig(w, bTyp, bAuswahl) || fnBedPasst(w, bBew, bWt, bWz);'''


def paket4(st):
    p = {"nr": 4, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "BedingungPunkt", "Zahl"))
    st.sp.append(("RG_Pruefpunkte", "BedingungWert", "Text"))
    aendern(st, p, "4.3", "App.Formulas", lambda t: rep(
        t, 'fnFehlt(typ: Text, pflicht: Boolean,', UDF_P4 + '\nfnFehlt(typ: Text, pflicht: Boolean,'))

    def onvisible(t):
        t = rep(t, 'Warnung: Coalesce(IfError(Boolean(a.Warnung), false), false), Inaktiv: false}',
                'Warnung: Coalesce(IfError(Boolean(a.Warnung), false), false), BedID: 0, BedWert: "", '
                'Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet), false), false), Inaktiv: false}')
        t = rep(t, "                     Grenzmodus: fnGrenzmodus(p.Grenzmodus.Value),\n",
                "                     Grenzmodus: fnGrenzmodus(p.Grenzmodus.Value),\n"
                "                     BedID: Coalesce(p.BedingungPunkt, 0),\n"
                '                     BedWert: Coalesce(p.BedingungWert, ""),\n'
                "                     Ausgeblendet: false,\n")
        t = rep(t, 'Warnung: Coalesce(IfError(Boolean(o.Value.Warnung), false), false), Inaktiv: true}',
                'Warnung: Coalesce(IfError(Boolean(o.Value.Warnung), false), false), BedID: 0, BedWert: "", '
                'Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet), false), false), Inaktiv: true}')
        t = rep(t, "Set(varSprungRec, First(Sort(Filter(colAntworten, !Inaktiv), Reihenfolge)));",
                "Set(varSprungRec, First(Sort(Filter(colAntworten As a, !a.Inaktiv && " + sicht("a") + "), Reihenfolge)));")
        return t
    aendern(st, p, "4.4", "scrKategorie.OnVisible", onvisible)

    ganz(st, p, "4.5", "galKaPruefpunkte.Items",
         "Sort(Filter(colAntworten As a, !a.Inaktiv && " + sicht("a") + "), Reihenfolge)")
    ganz(st, p, "4.5", "lblKaFehlendAnzahl.Text",
         "CountRows(Filter(colAntworten As a, !a.Inaktiv && " + sicht("a") + " && " + fehlt("a") + "))")
    ganz(st, p, "4.5", "lblKaFehlend.Text",
         "Concat(Filter(Sort(colAntworten, Reihenfolge) As a, !a.Inaktiv && " + sicht("a") + " && " + fehlt("a")
         + ") As z, z.Frage & " + GRUENDE + ', "; ")')
    sichtbar_n = "CountRows(Filter(colAntworten As a, !a.Inaktiv && " + sicht("a") + "))"
    aendern(st, p, "4.5", "lblKaUnter.Text", lambda t: rep(t, "CountRows(Filter(colAntworten, !Inaktiv))", sichtbar_n, n=2))
    aendern(st, p, "4.5", "conKaBalkenWert.Width", lambda t: rep(t, "CountRows(Filter(colAntworten, !Inaktiv))", sichtbar_n))
    aendern(st, p, "4.5", "lblKaStand.Text", lambda t: rep(
        t, 'CountRows(Filter(colAntworten, !Inaktiv && Bewertung = "NIO"))',
        'CountRows(Filter(colAntworten As a, !a.Inaktiv && ' + sicht("a") + ' && a.Bewertung = "NIO"))'))

    def speichern(t):
        t = rep(t, "Set(varSprungRec, First(Filter(Sort(Filter(colAntworten, !Inaktiv), Reihenfolge) As a, " + fehlt("a") + ")));",
                "Set(varSprungRec, First(Filter(Sort(Filter(colAntworten, !Inaktiv), Reihenfolge) As a, " + sicht("a") + " && " + fehlt("a") + ")));",
                wo="Sprung")
        anker = "ClearCollect(colFotoNeu, Filter(colFotos As f0,"
        i = t.index(anker)
        zeile_start = t.rfind("\n", 0, i) + 1
        einzug = t[zeile_start:i]
        neu = ("ClearCollect(colVersteckt, ShowColumns(Filter(colAntworten As a, !a.Inaktiv && !(" + sicht("a") + ")), PruefpunktID));\n"
               + einzug + anker)
        t = rep(t, anker, neu, wo="Ausgeblendete bestimmen vor Upload")
        t = rep(t, "fnFotoNeuErlaubt(a.Bewertung, a.FotoModus)", "!(a.PruefpunktID in colVersteckt.PruefpunktID) && fnFotoNeuErlaubt(a.Bewertung, a.FotoModus)", n=3, wo="Upload")
        t = rep(t, "ForAll(Distinct(Filter(colFotos, !Uebernommen && !IsBlank(Url)), PruefpunktID) As d,",
                "ForAll(Distinct(Filter(colFotos, !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID)), PruefpunktID) As d,", wo="Links anhängen")
        t = rep(t, "UpdateIf(colFotos, !Uebernommen && !IsBlank(Url), {Uebernommen: true});",
                "UpdateIf(colFotos, !Uebernommen && !IsBlank(Url) && !(PruefpunktID in colVersteckt.PruefpunktID), {Uebernommen: true});", wo="Übernommen")
        anker2 = "Set(varAntwortJSON, JSON(ShowColumns(colAntworten, PruefpunktID, Frage, Typ, Bewertung, WertZahl, WertText, Einheit, Kommentar, Fotos, Warnung), JSONFormat.Compact));"
        i = t.index(anker2)
        einzug = t[t.rfind("\n", 0, i) + 1:i]
        t = rep(t, anker2,
                'ClearCollect(colSpeichern, ForAll(colAntworten As r, If(r.PruefpunktID in colVersteckt.PruefpunktID, '
                'Patch(r, {Bewertung: "", WertText: "", WertZahl: Blank(), Kommentar: "", Fotos: "", Warnung: false, Ausgeblendet: true}), '
                'r.Inaktiv, r, Patch(r, {Ausgeblendet: false}))));\n' + einzug +
                "Set(varAntwortJSON, JSON(ShowColumns(colSpeichern, PruefpunktID, Frage, Typ, Bewertung, WertZahl, WertText, Einheit, Kommentar, Fotos, Warnung, Ausgeblendet), JSONFormat.Compact));",
                wo="JSON aus Kopie")
        t = rep(t, 'AnzahlNIO: CountRows(Filter(colAntworten, Bewertung = "NIO"))', 'AnzahlNIO: CountRows(Filter(colSpeichern, Bewertung = "NIO"))', wo="AnzahlNIO")
        return t
    aendern(st, p, "4.6", "btnKaSpeichern.OnSelect", speichern)

    aendern(st, p, "4.7", "htmProtokoll.HtmlText", lambda t: rep(
        t, "Concat(Table(ParseJSON(e.Antworten)) As a,",
        "Concat(Filter(Table(ParseJSON(e.Antworten)), !Coalesce(IfError(Boolean(ThisRecord.Value.Ausgeblendet), false), false)) As a,"))
    return p


# ---------------------------------------------------------------- Paket 5

def paket5(st):
    p = {"nr": 5, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "Eingabetyp (+MEHRFACH, DATUM, DATUMZEIT)", "Auswahl"))

    def formulas(t):
        t = rep(t, '(typ = "TEXT" && Trim(wt) = "")), "Wert",',
                '(typ = "TEXT" && Trim(wt) = "") || (typ = "MEHRFACH" && Trim(wt) = "") || ((typ = "DATUM" || typ = "DATUMZEIT") && wt = "")), "Wert",\n'
                '    typ = "DATUMZEIT" && wt <> "" && Len(wt) < 16, "Uhrzeit",')
        t = rep(t, 'fnFehlt(typ: Text, pflicht: Boolean,',
                'fnDatumText(d: Date, h: Text, m: Text, mitZeit: Boolean): Text = If(IsBlank(d), "", Text(d, "dd.mm.yyyy") & If(mitZeit && h <> "" && m <> "", " " & h & ":" & m, ""));\n'
                'fnFehlt(typ: Text, pflicht: Boolean,')
        return t
    aendern(st, p, "5.3", "App.Formulas", formulas)

    zeile = '54 + If(ThisItem.Hinweis <> "", 24, 0)'
    patch = ('Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {{WertText: '
             'fnDatumText({d}, Coalesce({h}, ""), Coalesce({m}, ""), ThisItem.Typ = "DATUMZEIT")}});\nSet(varGeaendert, true)')
    neues_control(st, p, "cboKaMehrfach", "conKaKarte", "Classic/ComboBox (Studio: Einfügen)", {
        "Items": 'Filter(ForAll(Split(ThisItem.Auswahl, ";") As s, {Value: Trim(s.Value)}), ThisRecord.Value <> "")',
        "DisplayFields": '["Value"]',
        "SearchFields": '["Value"]',
        "SelectMultiple": "true",
        "IsSearchable": "false",
        "DefaultSelectedItems": 'Filter(ForAll(Split(ThisItem.WertText, ";") As s, {Value: Trim(s.Value)}), ThisRecord.Value <> "")',
        "OnChange": 'Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: Concat(Filter(ForAll(Split(ThisItem.Auswahl, ";") As s, {Value: Trim(s.Value)}) As i, i.Value <> "" && i.Value in Self.SelectedItems.Value), Value, "; ")});\nSet(varGeaendert, true)',
        "InputTextPlaceholder": '"Auswählen (mehrere möglich)"',
        "AccessibleLabel": '"Mehrfachauswahl: " & ThisItem.Frage',
        "DisplayMode": "If(varNurLesen, DisplayMode.View, DisplayMode.Edit)",
        "Visible": 'ThisItem.Typ = "MEHRFACH"',
        "BorderColor": "clrRahmen",
        "ChevronBackground": "clrPrimaer",
        "ChevronFill": "Color.White",
        "SelectionFill": "clrPrimaer",
        "SelectionColor": "Color.White",
        "Font": "Font.'Segoe UI'",
        "Size": "16",
        "X": "20",
        "Y": zeile,
        "Width": "Min(460, Parent.Width - 40)",
        "Height": "56",
    })
    neues_control(st, p, "dpKaDatum", "conKaKarte", "Classic/DatePicker@2.6.0", {
        "AccessibleLabel": '"Datum: " & ThisItem.Frage',
        "BorderColor": "clrRahmen",
        "Color": "clrText",
        "DefaultDate": 'If(Len(ThisItem.WertText) >= 10, IfError(DateValue(Left(ThisItem.WertText, 10), "de-DE"), Blank()), Blank())',
        "DisplayMode": "If(varNurLesen, DisplayMode.View, DisplayMode.Edit)",
        "Font": "Font.'Segoe UI'",
        "Height": "56",
        "IconBackground": "clrPrimaer",
        "IconFill": "Color.White",
        "InputTextPlaceholder": '"Datum wählen"',
        "OnChange": patch.format(d="Self.SelectedDate", h="ddKaStunde.Selected.Value", m="ddKaMinute.Selected.Value"),
        "Size": "16",
        "StartOfWeek": "StartOfWeek.Monday",
        "Visible": 'ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT"',
        "Width": "240",
        "X": "20",
        "Y": zeile,
    })
    for name, liste, x, pos, eigen in (("ddKaStunde", "Sequence(24, 0)", "272", "12", "Stunde"),
                                         ("ddKaMinute", "Sequence(60, 0)", "388", "15", "Minute")):
        if name == "ddKaStunde":
            ch = patch.format(d="dpKaDatum.SelectedDate", h="Self.Selected.Value", m="ddKaMinute.Selected.Value")
        else:
            ch = patch.format(d="dpKaDatum.SelectedDate", h="ddKaStunde.Selected.Value", m="Self.Selected.Value")
        neues_control(st, p, name, "conKaKarte", "Classic/DropDown@2.3.1", {
            "AccessibleLabel": '"' + eigen + ': " & ThisItem.Frage',
            "AllowEmptySelection": "true",
            "BorderColor": "clrRahmen",
            "ChevronBackground": "clrPrimaer",
            "ChevronFill": "Color.White",
            "ChevronHoverBackground": "ColorFade(clrPrimaer, -20%)",
            "ChevronHoverFill": "Color.White",
            "Color": "clrText",
            "Default": 'If(Len(ThisItem.WertText) >= 16, Mid(ThisItem.WertText, ' + pos + ', 2), "")',
            "DisplayMode": "If(varNurLesen, DisplayMode.View, IsBlank(dpKaDatum.SelectedDate), DisplayMode.Disabled, DisplayMode.Edit)",
            "Fill": "clrKarte",
            "Font": "Font.'Segoe UI'",
            "Height": "56",
            "HoverFill": "clrPrimaerHell",
            "Items": "ForAll(" + liste + ' As s, {Value: Text(s.Value, "00")})',
            "Items.Value": "Value",
            "OnChange": ch,
            "PaddingLeft": "12",
            "PressedColor": "Color.White",
            "PressedFill": "clrPrimaer",
            "SelectionColor": "Color.White",
            "SelectionFill": "clrPrimaer",
            "Size": "16",
            "Visible": 'ThisItem.Typ = "DATUMZEIT"',
            "Width": "104",
            "X": x,
            "Y": zeile,
        })
    neues_control(st, p, "btnKaDatumLeeren", "conKaKarte", "Classic/Button@2.2.0", {
        "BorderColor": "clrRahmen",
        "BorderThickness": "1",
        "Color": "clrTextGrau",
        "Fill": "clrKarte",
        "Font": "Font.'Segoe UI'",
        "Height": "56",
        "HoverColor": "clrText",
        "HoverFill": "clrPrimaerHell",
        "OnSelect": 'Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: ""});\nReset(dpKaDatum);\nReset(ddKaStunde);\nReset(ddKaMinute);\nSet(varGeaendert, true)',
        "PressedColor": "clrText",
        "PressedFill": "clrPrimaerHell",
        "RadiusBottomLeft": "8", "RadiusBottomRight": "8", "RadiusTopLeft": "8", "RadiusTopRight": "8",
        "Size": "16",
        "Text": '"✕"',
        "Visible": '!varNurLesen && (ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && ThisItem.WertText <> ""',
        "Width": "56",
        "X": 'If(ThisItem.Typ = "DATUMZEIT", 504, 272)',
        "Y": zeile,
    })
    return p


# ---------------------------------------------------------------- Paket 6

def paket6(st):
    p = {"nr": 6, "props": [], "neu": []}
    st.sp.append(("RG_Hinweisbilder", "(neue Dokumentbibliothek)", "Bibliothek"))
    st.sp.append(("RG_Pruefpunkte", "HinweisBildID", "Zahl"))
    st.neue_quellen.add("RG_Hinweisbilder")

    def onvisible(t):
        t = rep(t, "Set(varFotoPP, 0);\n", "Set(varFotoPP, 0);\nSet(varBildID, 0);\n")
        t = rep(t, 'Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet), false), false), Inaktiv: false}',
                'Ausgeblendet: Coalesce(IfError(Boolean(a.Ausgeblendet), false), false), BildID: Coalesce(pp.HinweisBildID, 0), Inaktiv: false}')
        t = rep(t, "                     Ausgeblendet: false,\n",
                "                     Ausgeblendet: false,\n                     BildID: Coalesce(p.HinweisBildID, 0),\n")
        t = rep(t, 'Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet), false), false), Inaktiv: true}',
                'Ausgeblendet: Coalesce(IfError(Boolean(o.Value.Ausgeblendet), false), false), BildID: 0, Inaktiv: true}')
        return t
    aendern(st, p, "6.4", "scrKategorie.OnVisible", onvisible)
    ganz(st, p, "6.5", "lblKaFrage.Width", "Parent.Width - 40 - If(ThisItem.BildID > 0, 80, 0)")

    neues_control(st, p, "btnKaBild", "conKaKarte", "Classic/Button@2.2.0", {
        "BorderColor": "clrPrimaer",
        "BorderThickness": "1",
        "Color": "clrPrimaer",
        "Fill": "clrKarte",
        "Font": "Font.'Segoe UI'",
        "Height": "34",
        "HoverColor": "clrPrimaer",
        "HoverFill": "clrPrimaerHell",
        "OnSelect": "Set(varBildFrage, ThisItem.Frage);\nSet(varBildID, ThisItem.BildID)",
        "PressedColor": "clrPrimaer",
        "PressedFill": "clrPrimaerHell",
        "RadiusBottomLeft": "8", "RadiusBottomRight": "8", "RadiusTopLeft": "8", "RadiusTopRight": "8",
        "Size": "14",
        "Text": '"Bild"',
        "Visible": "ThisItem.BildID > 0",
        "Width": "64",
        "X": "Parent.Width - 84",
        "Y": "10",
    })
    neues_control(st, p, "conKaBild", "scrKategorie", "GroupContainer@1.5.0", {
        "Fill": "RGBA(0, 0, 0, 0.45)", "Height": "Parent.Height", "Visible": "varBildID > 0", "Width": "Parent.Width"})
    neues_control(st, p, "btnKaBildSperre", "conKaBild", "Classic/Button@2.2.0", {
        "BorderThickness": "0", "Fill": "RGBA(0, 0, 0, 0)", "Height": "Parent.Height", "HoverFill": "RGBA(0, 0, 0, 0)",
        "PressedFill": "RGBA(0, 0, 0, 0)", "Text": '""', "Width": "Parent.Width"})
    neues_control(st, p, "conKaBildKarte", "conKaBild", "GroupContainer@1.5.0", {
        "Fill": "clrKarte", "Height": "Min(Parent.Height - 32, 900)",
        "RadiusBottomLeft": "16", "RadiusBottomRight": "16", "RadiusTopLeft": "16", "RadiusTopRight": "16",
        "Width": "Parent.Width - 48", "X": "24", "Y": "(Parent.Height - Self.Height) / 2"})
    neues_control(st, p, "lblKaBildTitel", "conKaBildKarte", "Label@2.5.1", {
        "Color": "clrText", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "64",
        "Size": "16", "Text": '"Beispiel – " & varBildFrage', "Width": "Parent.Width - 40", "X": "20", "Y": "12"})
    neues_control(st, p, "imgKaBild", "conKaBildKarte", "Image@2.2.3", {
        "AccessibleLabel": '"Beispielbild zu " & varBildFrage',
        "Height": "Parent.Height - 84 - 96", "Image": "If(varBildID > 0, LookUp(RG_Hinweisbilder, ID = varBildID).Thumbnail.Large)",
        "ImagePosition": "ImagePosition.Fit", "Width": "Parent.Width - 40", "X": "20", "Y": "84"})
    neues_control(st, p, "btnKaBildSchliessen", "conKaBildKarte", "Classic/Button@2.2.0", {
        "BorderThickness": "0", "Color": "Color.White", "Fill": "clrPrimaer", "Font": "Font.'Segoe UI'", "Height": "56",
        "HoverFill": "ColorFade(clrPrimaer, -20%)", "OnSelect": "Set(varBildID, 0)", "PressedFill": "ColorFade(clrPrimaer, -35%)",
        "Size": "17", "Text": '"Schließen"', "Width": "200", "X": "Parent.Width - 220", "Y": "Parent.Height - 76"})
    return p


# ---------------------------------------------------------------- Paket 7

def paket7(st):
    p = {"nr": 7, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "Foto (+Bei Mangel Pflicht)", "Auswahl"))

    def formulas(t):
        t = rep(t, 'fnFotoModus(f: Text, alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht", f, alt, "Optional", "Aus");',
                'fnFotoModus(f: Text, alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht", f, f = "Bei Mangel Pflicht", "BeiMangel", alt, "Optional", "Aus");')
        t = rep(t, '    foto = "Pflicht" && fanz < 1, "Foto",',
                '    (foto = "Pflicht" || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1, "Foto",')
        return t
    aendern(st, p, "7.2", "App.Formulas", formulas)
    aendern(st, p, "7.3", "btnKaFoto.Visible", lambda t: rep(
        t, 'ThisItem.FotoModus <> "Aus"', '(ThisItem.FotoModus <> "Aus" && ThisItem.FotoModus <> "BeiMangel")'))
    aendern(st, p, "7.3", "btnKaFoto.Text", lambda t: rep(
        t, 'ThisItem.FotoModus = "Pflicht" && !varNurLesen',
        '(ThisItem.FotoModus = "Pflicht" || (ThisItem.FotoModus = "BeiMangel" && ThisItem.Bewertung = "NIO")) && !varNurLesen'))
    aendern(st, p, "7.3", "lblKaFotoHinweis.Text", lambda t: rep(
        t, 'LookUp(colAntworten, PruefpunktID = varFotoPP).FotoModus = "Pflicht", "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren.",',
        'LookUp(colAntworten, PruefpunktID = varFotoPP).FotoModus = "Pflicht", "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren.", '
        'LookUp(colAntworten, PruefpunktID = varFotoPP).FotoModus = "BeiMangel" && LookUp(colAntworten, PruefpunktID = varFotoPP).Bewertung = "NIO", '
        '"Mangel: mindestens ein Foto Pflicht. Keine Personen fotografieren.",'))
    return p


PAKETE = [paket1, paket2, paket3, paket4, paket5, paket6, paket7]


# ---------------------------------------------------------------- Prüfungen

BUILTINS = set("""If Set Not And Or CountRows Filter LookUp Sort SortByColumns First Last Coalesce IsBlank IsEmpty Blank Text
Value Trim Lower Upper Len Left Mid Right Split Concat ForAll Sequence Index Table ParseJSON JSON JSONFormat With Patch
Collect ClearCollect Clear Remove UpdateIf Distinct ShowColumns AddColumns DropColumns Notify NotificationType Navigate
ScreenTransition Refresh Concurrent IfError IsError Reset Select Launch Now Today DateAdd DateDiff DateValue TimeUnit
Switch Max Min Sum RoundDown Mod Defaults User GUID Substitute StartsWith Color ColorValue ColorFade RGBA DisplayMode
Font FontWeight Align Parent Self ThisItem ThisRecord true false Boolean StartOfWeek Weekday ISOWeekNum ImagePosition
Ungroup Date Number DateTime As in Compact Error Warning Success Information None Edit View Disabled White Semibold
Days Seconds Minutes Monday Fill Fit Large Thumbnail LayoutDirection LayoutOverflow Vertical Scroll DropShadow Light
Ascending Descending SortOrder Transparent Black Normal Bold Center Right Left Data LoadingSpinner Medium Small Full""".split())


def namen_der_app(stand):
    alle = "\n".join(stand.props.values())
    s = rg.ausserhalb_strings(alle)
    variablen = set(re.findall(r"\bSet\(\s*(\w+)", s))
    sammlungen = set(re.findall(r"\b(?:ClearCollect|Collect)\(\s*(\w+)", s))
    formeln = stand.props["App.Formulas"]
    udfs = set(re.findall(r"(?m)^\s*;?\s*(\w+)\s*\([^()]*\)\s*:\s*\w+\s*=", formeln)) | set(re.findall(r";\s*(\w+)\s*\([^()]*\)\s*:\s*\w+\s*=", formeln))
    params = set(re.findall(r"(\w+)\s*:\s*(?:Text|Number|Boolean|Date|DateTime)\b", formeln))
    benannt = set(re.findall(r"(?m)^(\w+)\s*=", formeln))
    felder = set(re.findall(r"(\w+)\s*:", s))
    aliase = set(re.findall(r"\bAs\s+(\w+)", s)) | set(re.findall(r"\bAddColumns\(\s*\w+\s*,\s*(\w+)", s))
    quellen = set(stand.app.spalten) | stand.neue_quellen
    spalten = set()
    for cols in stand.app.spalten.values():
        spalten |= set(cols)
    for _, name, _ in stand.sp:
        spalten.add(name.split(" ")[0])
    controls = set(stand.app.typ) | set(stand.neue_controls)
    return {"variablen": variablen, "sammlungen": sammlungen, "udfs": udfs, "params": params, "benannt": benannt,
            "felder": felder, "aliase": aliase, "quellen": quellen, "spalten": spalten, "controls": controls}


def pruefe(stand, pakete):
    zeilen = []
    fehler = 0
    n = namen_der_app(stand)
    bekannt = set().union(*n.values()) | BUILTINS
    for p in pakete:
        zeilen.append("== Paket %d: %d Properties, neue Steuerelemente: %s" % (p["nr"], len(p["props"]), ", ".join(p["neu"]) or "-"))
        eintraege = [(c["key"], c["nachher"]) for c in p["props"]]
        for name in p["neu"]:
            for k, v in stand.props.items():
                if k.startswith(name + "."):
                    eintraege.append((k, v))
        for key, f in eintraege:
            probleme = []
            if not rg.klammern_ok(f):
                probleme.append("Klammern")
            if rg.ohne_kommentare(f) != "\n".join(z.rstrip() for z in f.split("\n") if z.strip() != "") or "//" in rg.ausserhalb_strings(f):
                probleme.append("Kommentar")
            try:
                de = rg.to_de(f)
                if rg.from_de(de) != f:
                    probleme.append("Rückübersetzung")
            except ValueError as e:
                probleme.append(str(e))
            unbekannt = sorted(b for b in rg.bezeichner(f) if b not in bekannt)
            if unbekannt:
                probleme.append("unbekannte Namen: " + ", ".join(unbekannt))
            ctl = key.split(".")[0]
            if ctl not in n["controls"] and ctl != "App":
                probleme.append("Steuerelement fehlt: " + ctl)
            for spalte in ("Foto", "Grenzmodus", "Eingabetyp"):
                for m in re.finditer(r"\bp{1,2}\." + spalte + r"\b(?!\.Value)", rg.ausserhalb_strings(f)):
                    probleme.append("Auswahlspalte ohne .Value: " + m.group(0))
            for spalte in ("FotoMoeglich", "KommentarPflicht"):
                for m in re.finditer(r"\bp{1,2}\." + spalte + r"\b", rg.ausserhalb_strings(f)):
                    vor = rg.ausserhalb_strings(f)[max(0, m.start() - 9):m.start()]
                    if "Coalesce(" not in vor:
                        probleme.append("Ja/Nein ohne Coalesce: " + m.group(0))
            if "FotoMoeglich" in f and key not in ("scrKategorie.OnVisible",):
                probleme.append("FotoMoeglich außerhalb OnVisible")
            fehler += len(probleme)
            zeilen.append("  %-32s %s" % (key, "ok" if not probleme else "FEHLER: " + "; ".join(probleme)))
    fehler_s, zeilen_s = pruefe_schema(stand, pakete)
    fehler += fehler_s
    zeilen += zeilen_s
    rest = [k for k, v in stand.props.items() if re.search(r"\bfnFehlt\(", v) and k != "App.Formulas"]
    for k in rest:
        args = None
        for m in re.finditer(r"\bfnFehlt\(", rg.ausserhalb_strings(stand.props[k])):
            s = rg.ausserhalb_strings(stand.props[k])
            tiefe, i = 0, m.end() - 1
            for j in range(i, len(s)):
                if s[j] == "(":
                    tiefe += 1
                elif s[j] == ")":
                    tiefe -= 1
                    if tiefe == 0:
                        args = s[i + 1:j]
                        break
            stufe, anz = 0, 1
            for ch in args:
                if ch in "({[":
                    stufe += 1
                elif ch in ")}]":
                    stufe -= 1
                elif ch == "," and stufe == 0:
                    anz += 1
            if anz != 12:
                fehler += 1
                zeilen.append("  FEHLER fnFehlt mit %d statt 12 Argumenten in %s" % (anz, k))
    zeilen.append("Aufrufe fnFehlt im Endstand: " + ", ".join(sorted(rest)))
    return fehler, zeilen


def datensatz_schluessel(text, start):
    """Schlüssel des Datensatz-Literals ab der öffnenden Klammer start (nur oberste Ebene)."""
    s = rg.ausserhalb_strings(text)
    tiefe, schl, i = 0, [], start
    token = ""
    while i < len(s):
        ch = s[i]
        if ch in "({[":
            tiefe += 1
            if tiefe == 1:
                token = ""
                i += 1
                continue
        elif ch in ")}]":
            tiefe -= 1
            if tiefe == 0:
                break
        if tiefe == 1:
            if ch == ":":
                schl.append(token.strip().split()[-1] if token.strip() else "")
                token = ""
            elif ch == ",":
                token = ""
            else:
                token += ch
        i += 1
    return schl


def antwort_felder(onvisible):
    """Feldlisten der drei Datensatz-Literale, die colAntworten füllen."""
    s = rg.ausserhalb_strings(onvisible)
    listen = []
    for m in re.finditer(r"\{PruefpunktID:", s):
        listen.append(datensatz_schluessel(onvisible, m.start()))
    return listen


ANTWORT_KEYS = ("conKaKarte", "galKaPruefpunkte.Items", "lblKaFehlend", "lblKaUnter", "lblKaStand", "conKaBalkenWert",
                "btnKaSpeichern", "lblKaFotoHinweis")


def pruefe_schema(stand, pakete):
    zeilen, fehler = [], 0
    pp_spalten = set(stand.app.spalten["RG_Pruefpunkte"]) | {n.split(" ")[0] for l, n, _ in stand.sp if l == "RG_Pruefpunkte"}
    stand_zwischen = {}
    for p in pakete:
        for c in p["props"]:
            stand_zwischen[c["key"]] = c["nachher"]
        ov = stand_zwischen.get("scrKategorie.OnVisible")
        if ov is None:
            continue
        listen = antwort_felder(ov)
        mengen = [set(l) for l in listen]
        if len(mengen) != 3 or any(m != mengen[0] for m in mengen):
            fehler += 1
            zeilen.append("  FEHLER Paket %d: colAntworten-Felder der drei Zweige ungleich: %s" % (
                p["nr"], [sorted(m ^ mengen[0]) for m in mengen]))
        else:
            zeilen.append("  Paket %d: colAntworten hat in allen drei Zweigen dieselben %d Felder" % (p["nr"], len(mengen[0])))
        felder = mengen[0] if mengen else set()
        for m in re.finditer(r"\bpp?\.(\w+)", rg.ausserhalb_strings(ov)):
            if m.group(1) not in pp_spalten:
                fehler += 1
                zeilen.append("  FEHLER Paket %d: Spalte %s nicht in RG_Pruefpunkte" % (p["nr"], m.group(0)))
        pruefen = [(c["key"], c["nachher"]) for c in p["props"]]
        for name in p["neu"]:
            if stand.neue_controls[name][0] == "conKaKarte":
                pruefen += [(k, v) for k, v in stand.props.items() if k.startswith(name + ".")]
        for key, f in pruefen:
            ctl = key.split(".")[0]
            if not (key.startswith(ANTWORT_KEYS) or stand.app.eltern.get(ctl) == "conKaKarte"
                    or (ctl in stand.neue_controls and stand.neue_controls[ctl][0] == "conKaKarte")):
                continue
            for m in re.finditer(r"\b(ThisItem|a|b|z|b0)\.(\w+)", rg.ausserhalb_strings(f)):
                if m.group(2) not in felder:
                    fehler += 1
                    zeilen.append("  FEHLER Paket %d %s: Feld %s nicht in colAntworten" % (p["nr"], key, m.group(0)))
    return fehler, zeilen


EM = {" ": 0.274, "i": 0.229, "l": 0.229, "j": 0.229, "I": 0.27, ".": 0.25, ",": 0.25, ":": 0.25, ";": 0.25,
      "!": 0.3, "|": 0.25, "'": 0.2, "f": 0.3, "t": 0.33, "r": 0.35, "(": 0.3, ")": 0.3, "-": 0.38, "–": 0.5,
      "·": 0.25, "*": 0.4, "„": 0.35, "“": 0.35, '"': 0.4, "m": 0.86, "w": 0.75, "M": 0.88, "W": 0.95, "°": 0.4}


def textbreite(text, size):
    em = 0.0
    for ch in text:
        if ch in EM:
            em += EM[ch]
        elif ch.isdigit():
            em += 0.559
        elif ch.islower():
            em += 0.53
        elif ch.isupper():
            em += 0.64
        elif ord(ch) > 0x2000:
            em += 1.25
        else:
            em += 0.6
    return em * size * 1.333


# (Steuerelement, Text, Schriftgröße, verfügbare Breite in px, erlaubte Zeilen, Innenabstand links+rechts)
# Breiten bei Tablet-Hochformat 768: Karte = 768 - 48 = 720, Fotofenster-Karte = 720
TEXTE = [
    ("btnKaFoto", "📷 Foto (10)", 15, 144, 1, 20),
    ("btnKaFoto", "📷 Foto *", 15, 144, 1, 20),
    ("lblKaFotoHinweis", "Foto Pflicht: mindestens ein Foto. Keine Personen fotografieren.", 13, 680, 1, 10),
    ("lblKaFotoHinweis", "Keine Personen fotografieren. Fotos werden beim „Speichern“ hochgeladen.", 13, 680, 1, 10),
    ("addKaFoto", "Foto aufnehmen / auswählen", 18, 680, 1, 20),
    ("txtKaKommentar (Hinweis)", "Kommentar zum Mangel (Pflicht)", 16, 524, 1, 24),
    ("txtKaKommentar (Hinweis)", "Kommentar (Pflicht)", 16, 524, 1, 24),
    ("lblKaZahlInfo", "Betriebsstunden  ·  Soll ab 1000 bis 99999  ·  außerhalb des Sollbereichs", 14, 464, 2, 10),
    ("lblKaZahlInfo", "Betriebsstunden  ·  Soll ab 1000 bis 99999  ·  außerhalb, bitte begründen", 14, 464, 2, 10),
    ("lblKaZahlInfo", "Betriebsstunden  ·  Soll ab 1000 bis 99999  ·  unzulässig, bitte prüfen", 14, 464, 2, 10),
    ("cboKaMehrfach (Platzhalter)", "Auswählen (mehrere möglich)", 16, 460, 1, 60),
    ("btnKaBild", "Bild", 14, 64, 1, 20),
    ("btnKaDatumLeeren", "✕", 16, 56, 1, 20),
    ("btnKaBildSchliessen", "Schließen", 17, 200, 1, 20),
    ("lblKaFotoHinweis", "Mangel: mindestens ein Foto Pflicht. Keine Personen fotografieren.", 13, 680, 1, 10),
    ("lblKaBildTitel", "Beispiel – ZZ Test Thermometer Serverraum (Foto der Anzeige) prüfen", 16, 680, 2, 10),
]


def pruefe_texte():
    zeilen, fehler = [], 0
    for ctl, text, size, breite, zeilen_max, pad in TEXTE:
        b = textbreite(text, size) * 1.1
        noetig = int(b // max(1, breite - pad)) + 1
        ok = noetig <= zeilen_max
        fehler += not ok
        zeilen.append("  %-28s %4.0f px (+10 %%) / %d px, %d Zeile(n) nötig, erlaubt %d  %s  %r" % (
            ctl, b, breite - pad, noetig, zeilen_max, "ok" if ok else "FEHLER", text))
    return fehler, zeilen


def main():
    schluessel = sys.argv[1]
    simulation = "--simulation-0844" in sys.argv
    app = rg.App(schluessel)
    st = Stand(app)
    hinweise = []
    if "UpdateIf(colAntworten" not in st.props["btnKaSpeichern.OnSelect"]:
        if not simulation:
            raise Abbruch("Export enthält die Änderung von 08:44 (UpdateIf … Kommentar) nicht. Frischen Export einlesen.")
        t = st.props["btnKaSpeichern.OnSelect"]
        i = t.index("Set(varAntwortJSON")
        z = t.rfind("\n", 0, i) + 1
        st.props["btnKaSpeichern.OnSelect"] = t[:i] + 'UpdateIf(colAntworten, Bewertung <> "NIO", {Kommentar: ""});\n' + t[z:i] + t[i:]
        hinweise.append("SIMULATION: UpdateIf von 08:44 vor Set(varAntwortJSON eingefügt (nur Entwurf).")
    pakete = []
    for f in PAKETE:
        pakete.append(f(st))
    fehler, zeilen = pruefe(st, pakete)
    f2, z2 = pruefe_texte()
    fehler += f2
    zeilen += ["Textbreiten (Segoe UI, Schätzung je Zeichenart, Punkt -> Pixel x 1,333):"] + z2
    os.makedirs(AUS, exist_ok=True)
    daten = {"export": schluessel, "simulation": simulation, "hinweise": hinweise, "sp": st.sp,
             "pakete": pakete,
             "neue_controls": {k: {"eltern": e, "typ": t, "props": {pk.split(".", 1)[1]: v for pk, v in st.props.items() if pk.split(".", 1)[0] == k}}
                               for k, (e, t) in st.neue_controls.items()}}
    json.dump(daten, open(os.path.join(AUS, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    text = "\n".join(hinweise + zeilen + ["", "Fehler gesamt: %d" % fehler])
    open(os.path.join(AUS, "pruefung_auto.txt"), "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 1 if fehler else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Abbruch as e:
        print("ABBRUCH:", e)
        sys.exit(2)
