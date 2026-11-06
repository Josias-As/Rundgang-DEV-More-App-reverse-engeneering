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


# ---------------------------------------------------------------- Paket 8 (Abschnitte, Bereich ausblenden) – App-Teil

ABS_KOPF = ('ClearCollect(colAbsTmp, ShowColumns(Filter(colAntworten, !Inaktiv && !Ausgeblendet && Abschnitt <> ""), PruefpunktID, Reihenfolge, Abschnitt, BedID));\n'
            'ForAll(colAbsTmp As t,\n'
            '    Patch(colAntworten, LookUp(colAntworten, PruefpunktID = t.PruefpunktID),\n'
            '        {AbsKopf: With({g: Filter(colAbsTmp As u, Lower(u.Abschnitt) = Lower(t.Abschnitt))},\n'
            '            If(IsEmpty(Filter(g As u1, u1.BedID = 0)), t.Reihenfolge * 1000000 + t.PruefpunktID = Min(g, Reihenfolge * 1000000 + PruefpunktID), '
            't.BedID = 0 && t.Reihenfolge * 1000000 + t.PruefpunktID = Min(Filter(g As u2, u2.BedID = 0), Reihenfolge * 1000000 + PruefpunktID)))}\n'
            '    )\n'
            ');\n')
ABS_SPEICHERN = ('ClearCollect(colAbsTmp, ShowColumns(Filter(colSpeichern, !Inaktiv && !Ausgeblendet && Abschnitt <> ""), PruefpunktID, Reihenfolge, Abschnitt));\n'
                 'UpdateIf(colSpeichern, AbsKopf, {AbsKopf: false});\n'
                 'ForAll(colAbsTmp As t,\n'
                 '    Patch(colSpeichern, LookUp(colSpeichern, PruefpunktID = t.PruefpunktID),\n'
                 '        {AbsKopf: t.Reihenfolge * 1000000 + t.PruefpunktID = Min(Filter(colAbsTmp As u, Lower(u.Abschnitt) = Lower(t.Abschnitt)), Reihenfolge * 1000000 + PruefpunktID)}\n'
                 '    )\n'
                 ');\n')
ABS_FRAGE = lambda p: 'If({p}.Abschnitt = "", "", {p}.Abschnitt & " › ") & {p}.Frage'.format(p=p)  # noqa: E731


def paket8(st):
    p = {"nr": 8, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "Abschnitt", "Text"))
    st.sp.append(("RG_Bereiche", "Ausblenden", "Ja/Nein"))

    def onvisible(t):
        t = rep(t, 'BildID: Coalesce(pp.HinweisBildID, 0), Inaktiv: false}',
                'BildID: Coalesce(pp.HinweisBildID, 0), Abschnitt: Trim(Coalesce(Text(a.Abschnitt), "")), AbsKopf: false, Inaktiv: false}')
        t = rep(t, "                     BildID: Coalesce(p.HinweisBildID, 0),\n",
                "                     BildID: Coalesce(p.HinweisBildID, 0),\n                     Abschnitt: Trim(Coalesce(p.Abschnitt, \"\")),\n                     AbsKopf: false,\n")
        t = rep(t, 'BildID: 0, Inaktiv: true}', 'BildID: 0, Abschnitt: Trim(Coalesce(Text(o.Value.Abschnitt), "")), AbsKopf: false, Inaktiv: true}')
        t = rep(t, "Set(varSprungRec, First(", ABS_KOPF + "Set(varSprungRec, First(")
        return t
    aendern(st, p, "8.3", "scrKategorie.OnVisible", onvisible)
    def speichern8(t):
        t = rep(t, "Einheit, Kommentar, Fotos, Warnung, Ausgeblendet), JSONFormat.Compact)",
                "Einheit, Kommentar, Fotos, Warnung, Ausgeblendet, Abschnitt, AbsKopf), JSONFormat.Compact)")
        i = t.index("Set(varAntwortJSON")
        z = t.rfind("\n", 0, i) + 1
        einr = t[z:i]
        return t[:z] + einr + ABS_SPEICHERN.rstrip("\n").replace("\n", "\n" + einr) + "\n" + t[z:]
    aendern(st, p, "8.4", "btnKaSpeichern.OnSelect", speichern8)
    ganz(st, p, "8.5", "conKaKarte.Y", "If(ThisItem.AbsKopf, 52, 8)")
    neues_control(st, p, "lblKaAbschnitt", "galKaPruefpunkte", "Label@2.5.1", {
        "Color": "clrPrimaer", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "If(ThisItem.AbsKopf, 44, 0)",
        "Size": "17", "Text": "ThisItem.Abschnitt", "Visible": "ThisItem.AbsKopf", "Width": "Parent.TemplateWidth - 56",
        "X": "28", "Y": "8", "VerticalAlign": "VerticalAlign.Bottom"})
    aendern(st, p, "8.6", "lblKaFehlend.Text", lambda t: rep(t, " As z, z.Frage & Switch(", " As z, " + ABS_FRAGE("z") + " & Switch("))
    aendern(st, p, "8.7", "htmProtokoll.HtmlText", lambda t: rep(
        t, """                "<tr style='border-bottom:1px solid #DADCE5;" & If(b = "NIO", "background:#FCE8E6;", "") & "'>" &""",
        """                If(Coalesce(IfError(Boolean(a.Value.AbsKopf), false), false), "<tr><td colspan='3' style='padding:12px 8px 4px 8px;font-weight:600;color:#171496'>" & fnHtml(Text(a.Value.Abschnitt)) & "</td></tr>", "") &
                "<tr style='border-bottom:1px solid #DADCE5;" & If(b = "NIO", "background:#FCE8E6;", "") & "'>" &"""))
    aendern(st, p, "8.7", "htmProtokoll.HtmlText", lambda t: rep(
        t, """fnHtml(e.BereichName) & " · " & fnHtml(e.PrueferName)""",
        """If(e.BereichName = "", "", fnHtml(e.BereichName) & " · ") & fnHtml(e.PrueferName)"""))
    aendern(st, p, "8.8", "btnRuAbschluss.OnSelect", lambda t: rep(
        t, "Frage: Left(Text(n.Value.Frage), 255),",
        'Frage: Left(If(Coalesce(Text(n.Value.Abschnitt), "") = "", "", Text(n.Value.Abschnitt) & " › ") & Text(n.Value.Frage), 255),'))
    aendern(st, p, "8.9", "btnRgAktion.OnSelect", lambda t: rep(
        t, "BName, LookUp(b As be3, be3.ID = BereichID).Title)",
        'BName, If(Coalesce(LookUp(b As be3, be3.ID = BereichID).Ausblenden, false), "", LookUp(b As be4, be4.ID = BereichID).Title))'))
    aendern(st, p, "8.10", "galRuKategorien.Items", lambda t: rep(
        t, "ErsteImBereich, Position = Min(", 'ErsteImBereich, BereichName <> "" && Position = Min('))
    aendern(st, p, "8.11", "lblKaUnter.Text", lambda t: rep(
        t, 'varBereichName & "  ·  Kategorie " & varKatPos', 'If(varBereichName = "", "", varBereichName & "  ·  ") & "Kategorie " & varKatPos'))
    return p


# ---------------------------------------------------------------- Paket 9 (Rückfrage, kritischer Mangel, Ansprechpartner) – App-Teil

def fnfehlt_erweitern(t):
    """Jeden Aufruf fnFehlt(…)/fnFehltGrund(…) mit 12 Argumenten um das 13. Argument (kritisch, nicht bestätigt) ergänzen."""
    s = rg.ausserhalb_strings(t)
    if len(s) != len(t):
        s = None
    out, i = [], 0
    for m in re.finditer(r"\bfnFehlt(?:Grund)?\(", t):
        if m.start() < i:
            continue
        tiefe, j, args = 0, m.end() - 1, []
        start = m.end()
        for j in range(m.end() - 1, len(t)):
            ch = t[j]
            if ch == '"':
                continue
            if ch in "({[":
                tiefe += 1
            elif ch in ")}]":
                tiefe -= 1
                if tiefe == 0:
                    args.append(t[start:j])
                    break
            elif ch == "," and tiefe == 1:
                args.append(t[start:j])
                start = j + 1
        if len(args) != 12:
            raise Abbruch("fnFehlt mit %d Argumenten" % len(args))
        pref = args[0].strip().rsplit(".", 1)[0]
        out.append(t[i:j] + ", %s.Kritisch && !%s.KritischOk" % (pref, pref))
        i = j
    out.append(t[i:])
    return "".join(out)


UDF_P9 = ('fnFehltGrund(typ: Text, pflicht: Boolean, bew: Text, wt: Text, wz: Number, kom: Text, foto: Text, fanz: Number, kpfl: Boolean, gmodus: Text, mi: Number, ma: Number, kritoffen: Boolean): Text = If(',
          'fnFehlt(typ: Text, pflicht: Boolean, bew: Text, wt: Text, wz: Number, kom: Text, foto: Text, fanz: Number, kpfl: Boolean, gmodus: Text, mi: Number, ma: Number, kritoffen: Boolean): Boolean = fnFehltGrund(typ, pflicht, bew, wt, wz, kom, foto, fanz, kpfl, gmodus, mi, ma, kritoffen) <> "";')

RUECK_R = "LookUp(colAntworten, PruefpunktID = varRueckPP)"
KRIT_R = "LookUp(colAntworten, PruefpunktID = varKritPP)"
NACH_NIO = ('If(ThisItem.Rueckfrage, Set(varRueckPP, ThisItem.PruefpunktID), ThisItem.Kritisch && !LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID).KritischOk, '
            'Set(varKritPP, ThisItem.PruefpunktID))')


def paket9(st):
    p = {"nr": 9, "props": [], "neu": []}
    st.sp.append(("RG_Ansprechpartner", "(neue Liste: Title, Kontakt, Telefon, Hinweis, Allgemein, Aktiv)", "Liste"))
    for name in ("Kontakt", "Telefon", "Allgemein"):
        st.sp.append(("RG_Ansprechpartner", name, "Spalte"))
    for name, typ in (("Kritisch", "Ja/Nein"), ("KritischText", "Text"), ("Ansprechpartner", "Text"), ("Rueckfrage", "Ja/Nein"), ("RueckfrageText", "Text")):
        st.sp.append(("RG_Pruefpunkte", name, typ))
    st.neue_quellen.add("RG_Ansprechpartner")

    def formulas(t):
        t = rep(t, 'fnFehltGrund(typ: Text, pflicht: Boolean, bew: Text, wt: Text, wz: Number, kom: Text, foto: Text, fanz: Number, kpfl: Boolean, gmodus: Text, mi: Number, ma: Number): Text = If(',
                UDF_P9[0])
        t = rep(t, '    (foto = "Pflicht" || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1, "Foto",\n',
                '    (foto = "Pflicht" || (foto = "BeiMangel" && bew = "NIO")) && fanz < 1, "Foto",\n    kritoffen && bew = "NIO", "Kritisch",\n')
        t = rep(t, 'fnFehlt(typ: Text, pflicht: Boolean, bew: Text, wt: Text, wz: Number, kom: Text, foto: Text, fanz: Number, kpfl: Boolean, gmodus: Text, mi: Number, ma: Number): Boolean = fnFehltGrund(typ, pflicht, bew, wt, wz, kom, foto, fanz, kpfl, gmodus, mi, ma) <> "";',
                UDF_P9[1])
        return t
    aendern(st, p, "9.3", "App.Formulas", formulas)

    def onvisible(t):
        t = rep(t, "Set(varBildID, 0);\n", "Set(varBildID, 0);\nSet(varRueckPP, 0);\nSet(varKritPP, 0);\n")
        t = rep(t, "    Set(varErgebnis, LookUp(RG_KategorieErgebnisse, Title = varSchluesselK))\n",
                "    Set(varErgebnis, LookUp(RG_KategorieErgebnisse, Title = varSchluesselK)),\n    ClearCollect(colKontakte, Filter(RG_Ansprechpartner, Aktiv = true))\n")
        t = rep(t, 'AbsKopf: false, Inaktiv: false}',
                'AbsKopf: false, Kritisch: Coalesce(IfError(Boolean(a.Kritisch), false), false), KritischText: "", Ansprechpartner: "", Rueckfrage: false, RueckfrageText: "", '
                'KritischOk: Coalesce(IfError(Boolean(a.KritischOk), false), false), KritischZeit: Coalesce(Text(a.KritischZeit), ""), KritischVon: Coalesce(Text(a.KritischVon), ""), Inaktiv: false}')
        t = rep(t, "                     AbsKopf: false,\n",
                "                     AbsKopf: false,\n"
                "                     Kritisch: Coalesce(p.Kritisch, false),\n"
                "                     KritischText: Coalesce(p.KritischText, \"\"),\n"
                "                     Ansprechpartner: Coalesce(p.Ansprechpartner, \"\"),\n"
                "                     Rueckfrage: Coalesce(p.Rueckfrage, false),\n"
                "                     RueckfrageText: Coalesce(p.RueckfrageText, \"\"),\n"
                "                     KritischOk: If(IsBlank(alt), false, Coalesce(IfError(Boolean(alt.Value.KritischOk), false), false)),\n"
                "                     KritischZeit: If(IsBlank(alt), \"\", Coalesce(Text(alt.Value.KritischZeit), \"\")),\n"
                "                     KritischVon: If(IsBlank(alt), \"\", Coalesce(Text(alt.Value.KritischVon), \"\")),\n")
        t = rep(t, 'AbsKopf: false, Inaktiv: true}',
                'AbsKopf: false, Kritisch: Coalesce(IfError(Boolean(o.Value.Kritisch), false), false), KritischText: "", Ansprechpartner: "", Rueckfrage: false, RueckfrageText: "", '
                'KritischOk: Coalesce(IfError(Boolean(o.Value.KritischOk), false), false), KritischZeit: Coalesce(Text(o.Value.KritischZeit), ""), KritischVon: Coalesce(Text(o.Value.KritischVon), ""), Inaktiv: true}')
        return t
    aendern(st, p, "9.4", "scrKategorie.OnVisible", onvisible)
    ganz(st, p, "9.5", "btnKaNIO.OnSelect",
         'With({neu: If(ThisItem.Bewertung = "NIO", "", "NIO")},\n'
         '    Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {Bewertung: neu, KritischOk: false, KritischZeit: ""});\n'
         '    If(neu = "NIO", ' + NACH_NIO + ', Set(varRueckPP, 0); Set(varKritPP, 0))\n'
         ');\n'
         'Set(varGeaendert, true)')
    ganz(st, p, "9.5", "txtKaZahl.OnChange",
         'With({z: IfError(Value(Self.Text), Blank())},\n'
         '    With({b: If(IsBlank(z), "", fnZahlBewertung(z, ThisItem.MinWert, ThisItem.MaxWert, ThisItem.Grenzmodus)), war: ThisItem.Bewertung = "NIO" && ThisItem.KritischOk},\n'
         '        Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertZahl: z, Bewertung: b, KritischOk: b = "NIO" && war, KritischZeit: If(b = "NIO" && war, ThisItem.KritischZeit, "")});\n'
         '        If(b = "NIO", ' + NACH_NIO + ', Set(varRueckPP, 0); Set(varKritPP, 0))\n'
         '    )\n'
         ');\n'
         'Set(varGeaendert, true)')

    def speichern(t):
        t = rep(t, "Ausgeblendet, Abschnitt, AbsKopf), JSONFormat.Compact)", "Ausgeblendet, Abschnitt, AbsKopf, Kritisch, KritischOk, KritischZeit, KritischVon), JSONFormat.Compact)")
        t = rep(t, "If(\n    Value(lblKaFehlendAnzahl.Text) > 0,\n",
                "If(\n    varRueckPP > 0 || varKritPP > 0,\n        Notify(\"Bitte zuerst die offene Frage im Fenster beantworten.\", NotificationType.Warning),\n    Value(lblKaFehlendAnzahl.Text) > 0,\n")
        t = rep(t, "        Reset(galKaPruefpunkte),\n    !varIsLoading && Now() >= varSperreBis,",
                "        Set(varKritPP, Coalesce(First(Sort(Filter(colAntworten As a, !a.Inaktiv && a.Bewertung = \"NIO\" && a.Kritisch && !a.KritischOk && " + sicht("a") + "), Reihenfolge)).PruefpunktID, 0));\n"
                "        Reset(galKaPruefpunkte),\n    !varIsLoading && Now() >= varSperreBis,")
        return fnfehlt_erweitern(t)
    aendern(st, p, "9.6", "btnKaSpeichern.OnSelect", speichern)
    for key in ("lblKaFehlendAnzahl.Text", "conKaKarte.BorderColor", "conKaKarte.BorderThickness"):
        aendern(st, p, "9.6", key, fnfehlt_erweitern)
    aendern(st, p, "9.6", "lblKaFehlend.Text", lambda t: rep(fnfehlt_erweitern(t), '"Uhrzeit", " (Uhrzeit)", "")', '"Uhrzeit", " (Uhrzeit)", "Kritisch", " (kritisch: Bescheid bestätigen)", "")'))
    aendern(st, p, "9.7", "htmProtokoll.HtmlText", lambda t: rep(
        t, """                If(IsBlank(fo) || fo = "", "", "<br>" & Concat(""",
        """                If(b = "NIO" && Coalesce(IfError(Boolean(a.Value.Kritisch), false), false), "<br><b style='color:#B3261E'>KRITISCH – " & If(Coalesce(IfError(Boolean(a.Value.KritischOk), false), false), "Bescheid gegeben, bestätigt von " & fnHtml(Coalesce(Text(a.Value.KritischVon), e.PrueferName)) & " am " & fnHtml(Coalesce(Text(a.Value.KritischZeit), "")), "nicht bestätigt") & "</b>", "") &
                If(IsBlank(fo) || fo = "", "", "<br>" & Concat("""))
    aendern(st, p, "9.8", "btnRuAbschluss.OnSelect", lambda t: rep(
        t, 'Kommentar: Coalesce(Text(n.Value.Kommentar), ""),',
        'Kommentar: If(Coalesce(IfError(Boolean(n.Value.Kritisch), false), false), "KRITISCH – Bescheid gegeben " & Coalesce(Text(n.Value.KritischZeit), "") & ". ", "") & Coalesce(Text(n.Value.Kommentar), ""),'))

    # Fenster Rückfrage
    neues_control(st, p, "conKaRueck", "scrKategorie", "GroupContainer@1.5.0", {
        "Fill": "RGBA(0, 0, 0, 0.45)", "Height": "Parent.Height", "Visible": 'varRueckPP > 0 && ' + RUECK_R + '.Bewertung = "NIO"', "Width": "Parent.Width"})
    neues_control(st, p, "btnKaRueckSperre", "conKaRueck", "Classic/Button@2.2.0", {
        "BorderThickness": "0", "Fill": "RGBA(0, 0, 0, 0)", "Height": "Parent.Height", "HoverFill": "RGBA(0, 0, 0, 0)",
        "PressedFill": "RGBA(0, 0, 0, 0)", "Text": '""', "Width": "Parent.Width"})
    neues_control(st, p, "conKaRueckKarte", "conKaRueck", "GroupContainer@1.5.0", {
        "Fill": "clrKarte", "Height": "470", "RadiusBottomLeft": "16", "RadiusBottomRight": "16", "RadiusTopLeft": "16", "RadiusTopRight": "16",
        "Width": "Parent.Width - 48", "X": "24", "Y": "(Parent.Height - Self.Height) / 2"})
    neues_control(st, p, "lblKaRueckTitel", "conKaRueckKarte", "Label@2.5.1", {
        "Color": "clrText", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "48", "Size": "21",
        "Text": '"Ist das wirklich so?"', "Width": "Parent.Width - 48", "X": "24", "Y": "20"})
    neues_control(st, p, "lblKaRueckFrage", "conKaRueckKarte", "Label@2.5.1", {
        "Color": "clrText", "Font": "Font.'Segoe UI'", "Height": "124", "Size": "17", "VerticalAlign": "VerticalAlign.Top",
        "Text": 'With({r: ' + RUECK_R + '}, r.Frage & Char(10) & "Ihre Antwort: " & If(r.Typ = "ZAHL", Text(r.WertZahl) & " " & r.Einheit, "n.i.O."))',
        "Width": "Parent.Width - 48", "X": "24", "Y": "76"})
    neues_control(st, p, "lblKaRueckNormal", "conKaRueckKarte", "Label@2.5.1", {
        "Color": "clrWarnung", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "140", "Size": "17", "VerticalAlign": "VerticalAlign.Top",
        "Text": 'With({r: ' + RUECK_R + '}, If(Trim(r.RueckfrageText) <> "", r.RueckfrageText, r.Typ = "ZAHL" && (!IsBlank(r.MinWert) || !IsBlank(r.MaxWert)), '
                '"Normalerweise: " & If(IsBlank(r.MinWert), "", "ab " & Text(r.MinWert) & " ") & If(IsBlank(r.MaxWert), "", "bis " & Text(r.MaxWert) & " ") & r.Einheit, '
                '"Bitte noch einmal genau nachsehen."))',
        "Width": "Parent.Width - 48", "X": "24", "Y": "208"})
    neues_control(st, p, "btnKaRueckNein", "conKaRueckKarte", "Classic/Button@2.2.0", {
        "BorderColor": "clrPrimaer", "BorderThickness": "1", "Color": "clrPrimaer", "Fill": "clrKarte", "Font": "Font.'Segoe UI'", "Height": "64",
        "HoverColor": "clrPrimaer", "HoverFill": "clrPrimaerHell", "PressedColor": "clrPrimaer", "PressedFill": "clrPrimaerHell",
        "OnSelect": 'Patch(colAntworten, ' + RUECK_R + ', {Bewertung: "", WertZahl: Blank(), KritischOk: false, KritischZeit: ""});\nSet(varRueckPP, 0);\nSet(varGeaendert, true)',
        "RadiusBottomLeft": "10", "RadiusBottomRight": "10", "RadiusTopLeft": "10", "RadiusTopRight": "10", "Size": "17",
        "Text": '"Nein, korrigieren"', "Width": "(Parent.Width - 64) / 2", "X": "24", "Y": "Parent.Height - 88"})
    neues_control(st, p, "btnKaRueckJa", "conKaRueckKarte", "Classic/Button@2.2.0", {
        "BorderThickness": "0", "Color": "Color.White", "Fill": "clrPrimaer", "Font": "Font.'Segoe UI'", "Height": "64",
        "HoverFill": "ColorFade(clrPrimaer, -20%)", "PressedFill": "ColorFade(clrPrimaer, -35%)",
        "OnSelect": 'With({r: ' + RUECK_R + '},\n    Set(varRueckPP, 0);\n    If(r.Bewertung = "NIO" && r.Kritisch && !r.KritischOk, Set(varKritPP, r.PruefpunktID))\n)',
        "RadiusBottomLeft": "10", "RadiusBottomRight": "10", "RadiusTopLeft": "10", "RadiusTopRight": "10", "Size": "17",
        "Text": '"Ja, stimmt"', "Width": "(Parent.Width - 64) / 2", "X": "40 + (Parent.Width - 64) / 2", "Y": "Parent.Height - 88"})

    # Fenster kritischer Mangel
    kontakte = ('If(varKritPP > 0, Sort(Filter(colKontakte As k, Coalesce(k.Allgemein, false) || CountRows(Filter(Split(Coalesce(' + KRIT_R + '.Ansprechpartner, ""), ";") As s, '
                'Trim(s.Value) = Text(k.ID))) > 0), If(Coalesce(Allgemein, false), 1, 0)), Filter(colKontakte, false))')
    neues_control(st, p, "conKaKrit", "scrKategorie", "GroupContainer@1.5.0", {
        "Fill": "RGBA(179, 38, 30, 0.55)", "Height": "Parent.Height", "Visible": 'varKritPP > 0 && ' + KRIT_R + '.Bewertung = "NIO"', "Width": "Parent.Width"})
    neues_control(st, p, "btnKaKritSperre", "conKaKrit", "Classic/Button@2.2.0", {
        "BorderThickness": "0", "Fill": "RGBA(0, 0, 0, 0)", "Height": "Parent.Height", "HoverFill": "RGBA(0, 0, 0, 0)",
        "PressedFill": "RGBA(0, 0, 0, 0)", "Text": '""', "Width": "Parent.Width"})
    neues_control(st, p, "conKaKritKarte", "conKaKrit", "GroupContainer@1.5.0", {
        "BorderColor": "clrFehler", "BorderThickness": "4", "Fill": "clrKarte", "Height": "Min(Parent.Height - 48, 820)",
        "RadiusBottomLeft": "16", "RadiusBottomRight": "16", "RadiusTopLeft": "16", "RadiusTopRight": "16",
        "Width": "Parent.Width - 48", "X": "24", "Y": "(Parent.Height - Self.Height) / 2"})
    neues_control(st, p, "lblKaKritTitel", "conKaKritKarte", "Label@2.5.1", {
        "Align": "Align.Center", "Color": "Color.White", "Fill": "clrFehler", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold",
        "Height": "72", "Size": "21", "Text": '"⚠ Kritischer Mangel – sofort melden"', "Width": "Parent.Width", "X": "0", "Y": "0"})
    neues_control(st, p, "lblKaKritFrage", "conKaKritKarte", "Label@2.5.1", {
        "Color": "clrText", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "92", "Size": "18", "VerticalAlign": "VerticalAlign.Top",
        "Text": KRIT_R + ".Frage", "Width": "Parent.Width - 48", "X": "24", "Y": "84"})
    neues_control(st, p, "lblKaKritText", "conKaKritKarte", "Label@2.5.1", {
        "Color": "clrFehler", "Font": "Font.'Segoe UI'", "Height": "96", "Size": "17", "VerticalAlign": "VerticalAlign.Top",
        "Text": 'Coalesce(' + KRIT_R + '.KritischText, "")', "Width": "Parent.Width - 48", "X": "24", "Y": "180"})
    neues_control(st, p, "lblKaKritMelden", "conKaKritKarte", "Label@2.5.1", {
        "Color": "clrText", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "32", "Size": "16",
        "Text": '"Bitte jetzt Bescheid geben bei:"', "Width": "Parent.Width - 48", "X": "24", "Y": "280"})
    neues_control(st, p, "galKaKritKontakte", "conKaKritKarte", "Gallery@2.15.0", {
        "AccessibleLabel": '"Ansprechpartner"', "Height": "Parent.Height - 316 - 172", "Items": kontakte, "ShowScrollbar": "true",
        "TemplatePadding": "0", "TemplateSize": "112", "Width": "Parent.Width - 48", "X": "24", "Y": "316"})
    neues_control(st, p, "lblKaKritRolle", "galKaKritKontakte", "Label@2.5.1", {
        "Color": "clrFehler", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "28", "Size": "15",
        "Text": "ThisItem.Title", "Width": "Parent.TemplateWidth", "X": "0", "Y": "4"})
    neues_control(st, p, "lblKaKritName", "galKaKritKontakte", "Label@2.5.1", {
        "Color": "clrText", "Font": "Font.'Segoe UI'", "Height": "30", "Size": "17",
        "Text": 'Coalesce(ThisItem.Kontakt, "") & If(Trim(Coalesce(ThisItem.Telefon, "")) = "", "", "  ·  ☎ " & ThisItem.Telefon)',
        "Width": "Parent.TemplateWidth", "X": "0", "Y": "32"})
    neues_control(st, p, "lblKaKritHinweis", "galKaKritKontakte", "Label@2.5.1", {
        "Color": "clrTextGrau", "Font": "Font.'Segoe UI'", "Height": "44", "Size": "13", "Text": 'Coalesce(ThisItem.Hinweis, "")',
        "VerticalAlign": "VerticalAlign.Top", "Width": "Parent.TemplateWidth", "X": "0", "Y": "62"})
    neues_control(st, p, "lblKaKritLeer", "conKaKritKarte", "Label@2.5.1", {
        "Color": "clrFehler", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "64", "Size": "16",
        "Text": '"Keine Ansprechpartner hinterlegt. Bitte die Schichtleitung bzw. den Vorgesetzten informieren."',
        "Visible": "IsEmpty(galKaKritKontakte.AllItems)", "Width": "Parent.Width - 48", "X": "24", "Y": "320"})
    neues_control(st, p, "btnKaKritOk", "conKaKritKarte", "Classic/Button@2.2.0", {
        "BorderThickness": "0", "Color": "Color.White", "Fill": "clrFehler", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "68",
        "HoverFill": "ColorFade(clrFehler, -15%)", "PressedFill": "ColorFade(clrFehler, -30%)",
        "OnSelect": 'If(' + KRIT_R + '.Bewertung = "NIO", Patch(colAntworten, ' + KRIT_R + ', {KritischOk: true, KritischZeit: Text(Now(), "dd.mm.yyyy hh:mm"), KritischVon: User().FullName}));\nSet(varKritPP, 0);\nSet(varGeaendert, true)',
        "RadiusBottomLeft": "10", "RadiusBottomRight": "10", "RadiusTopLeft": "10", "RadiusTopRight": "10", "Size": "19",
        "Text": '"Ich habe Bescheid gegeben"', "Width": "Parent.Width - 48", "X": "24", "Y": "Parent.Height - 160"})
    neues_control(st, p, "btnKaKritVersehen", "conKaKritKarte", "Classic/Button@2.2.0", {
        "BorderColor": "clrTextGrau", "BorderThickness": "1", "Color": "clrTextGrau", "Fill": "clrKarte", "Font": "Font.'Segoe UI'", "Height": "56",
        "HoverColor": "clrText", "HoverFill": "clrHintergrund", "PressedColor": "clrText", "PressedFill": "clrHintergrund",
        "OnSelect": 'Patch(colAntworten, ' + KRIT_R + ', {Bewertung: "", WertZahl: Blank(), KritischOk: false, KritischZeit: ""});\nSet(varKritPP, 0);\nSet(varGeaendert, true)',
        "RadiusBottomLeft": "10", "RadiusBottomRight": "10", "RadiusTopLeft": "10", "RadiusTopRight": "10", "Size": "15",
        "Text": '"n.i.O. war ein Versehen – Antwort zurücknehmen"', "Width": "Parent.Width - 48", "X": "24", "Y": "Parent.Height - 80"})
    return p


# ---------------------------------------------------------------- Paket 10 (Kategorien in beliebiger Reihenfolge)

def paket10(st):
    p = {"nr": 10, "props": [], "neu": []}
    aendern(st, p, "10.2", "btnKaSpeichern.OnSelect", lambda t: rep(
        t, "                IsBlank(erg) && CountRows(Filter(colKatListe As kl, kl.Position < varKatPos && IsBlank(LookUp(colErledigt As e, e.KategorieID = kl.KategorieID)))) > 0,\n"
           "                    Notify(\"Bitte zuerst die vorherigen Kategorien abschließen.\", NotificationType.Warning),\n", ""))
    aendern(st, p, "10.3", "galRuKategorien.Items", lambda t: rep(t, '"naechste", "gesperrt")', '"naechste", "offen")'))
    aendern(st, p, "10.3", "lblRuSymbol.Text", lambda t: rep(t, '"▶", "🔒")', '"▶", "○")'))
    aendern(st, p, "10.3", "lblRuSymbol.Color", lambda t: rep(t, '"naechste", clrPrimaer, clrGesperrt)', '"naechste", clrPrimaer, clrTextGrau)'))
    aendern(st, p, "10.3", "lblRuKatZustand.Text", lambda t: rep(t, '"Gesperrt – erst die vorherige Kategorie abschließen")', '"Offen")'))
    aendern(st, p, "10.3", "btnRuOeffnen.Text", lambda t: rep(t, '"naechste", "Öffnen", "Gesperrt")', '"naechste", "Öffnen", "Öffnen")'))
    return p


# ---------------------------------------------------------------- Paket 12 (eigene Antwortwörter für i.O./n.i.O.)

WORT = lambda feld, std: 'If(Trim(ThisItem.%s) = "", "%s", ThisItem.%s)' % (feld, std, feld)  # noqa: E731
KNOPF_BREITE = 'If(Max(Len(ThisItem.TextIO), Len(ThisItem.TextNIO)) > 8, 260, 160)'
KNOPF_GROESSE = 'If(Max(Len(ThisItem.TextIO), Len(ThisItem.TextNIO)) > 12, 14, 17)'


def paket12(st):
    p = {"nr": 12, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "TextIO", "Text"))
    st.sp.append(("RG_Pruefpunkte", "TextNIO", "Text"))

    def onvisible(t):
        t = rep(t, 'KritischVon: Coalesce(Text(a.KritischVon), ""), Inaktiv: false}',
                'KritischVon: Coalesce(Text(a.KritischVon), ""), TextIO: Coalesce(Text(a.TextIO), ""), TextNIO: Coalesce(Text(a.TextNIO), ""), Inaktiv: false}')
        t = rep(t, "                     KritischVon: If(IsBlank(alt), \"\", Coalesce(Text(alt.Value.KritischVon), \"\")),\n",
                "                     KritischVon: If(IsBlank(alt), \"\", Coalesce(Text(alt.Value.KritischVon), \"\")),\n"
                "                     TextIO: Trim(Coalesce(p.TextIO, \"\")),\n"
                "                     TextNIO: Trim(Coalesce(p.TextNIO, \"\")),\n")
        t = rep(t, 'KritischVon: Coalesce(Text(o.Value.KritischVon), ""), Inaktiv: true}',
                'KritischVon: Coalesce(Text(o.Value.KritischVon), ""), TextIO: Coalesce(Text(o.Value.TextIO), ""), TextNIO: Coalesce(Text(o.Value.TextNIO), ""), Inaktiv: true}')
        return t
    aendern(st, p, "12.3", "scrKategorie.OnVisible", onvisible)
    aendern(st, p, "12.4", "btnKaSpeichern.OnSelect", lambda t: rep(
        t, "KritischZeit, KritischVon), JSONFormat.Compact)", "KritischZeit, KritischVon, TextIO, TextNIO), JSONFormat.Compact)"))
    ganz(st, p, "12.5", "btnKaIO.Text", WORT("TextIO", "i.O."))
    ganz(st, p, "12.5", "btnKaNIO.Text", WORT("TextNIO", "n.i.O."))
    standard_ersetzen(st, p, "12.5", "btnKaIO.Width", "160", KNOPF_BREITE)
    standard_ersetzen(st, p, "12.5", "btnKaNIO.Width", "160", KNOPF_BREITE)
    ganz(st, p, "12.5", "btnKaNIO.X", "36 + btnKaIO.Width")
    ganz(st, p, "12.5", "btnKaIO.Size", KNOPF_GROESSE)
    ganz(st, p, "12.5", "btnKaNIO.Size", KNOPF_GROESSE)
    aendern(st, p, "12.7", "lblKaRueckFrage.Text", lambda t: rep(t, ', "n.i.O."))', ', If(Trim(r.TextNIO) = "", "n.i.O.", r.TextNIO)))'))
    ganz(st, p, "12.7", "btnKaKritVersehen.Text", 'If(Trim(' + KRIT_R + '.TextNIO) = "", "n.i.O.", ' + KRIT_R + '.TextNIO) & " war ein Versehen – Antwort zurücknehmen"')
    aendern(st, p, "12.6", "htmProtokoll.HtmlText", lambda t: rep(
        t, """<td style='padding:6px 8px;width:64px;white-space:nowrap;font-weight:600;color:" & If(b = "NIO", "#B3261E", w, "#9A5B00", "#0F7B3F") & "'>" & Switch(b, "IO", "i.O.", "NIO", "n.i.O.", "") & "</td>""",
        """<td style='padding:6px 8px;width:110px;font-weight:600;color:" & If(b = "NIO", "#B3261E", w, "#9A5B00", "#0F7B3F") & "'>" & Switch(b, "IO", fnHtml(Coalesce(If(Coalesce(Text(a.Value.TextIO), "") = "", Blank(), Text(a.Value.TextIO)), "i.O.")), "NIO", fnHtml(Coalesce(If(Coalesce(Text(a.Value.TextNIO), "") = "", Blank(), Text(a.Value.TextNIO)), "n.i.O.")), "") & "</td>"""))
    return p


# ---------------------------------------------------------------- Paket 16 („nicht messbar“ bei Zahlen)

NM = '"nicht messbar"'


def paket16(st):
    p = {"nr": 16, "props": [], "neu": []}
    st.sp.append(("RG_Pruefpunkte", "NichtMessbar", "Ja/Nein"))

    def formulas(t):
        t = rep(t, '(typ = "ZAHL" && IsBlank(wz))', '(typ = "ZAHL" && IsBlank(wz) && wt = "")')
        t = rep(t, 'Boolean = bew = "NIO" || (kpfl && fnBeantwortet(bew, wt, wz))',
                'Boolean = bew = "NIO" || (typ = "ZAHL" && wt = ' + NM + ') || (kpfl && fnBeantwortet(bew, wt, wz))')
        return t
    aendern(st, p, "16.3", "App.Formulas", formulas)

    def onvisible(t):
        t = rep(t, 'TextNIO: Coalesce(Text(a.TextNIO), ""), Inaktiv: false}', 'TextNIO: Coalesce(Text(a.TextNIO), ""), NMErlaubt: false, Inaktiv: false}')
        t = rep(t, "                     TextNIO: Trim(Coalesce(p.TextNIO, \"\")),\n",
                "                     TextNIO: Trim(Coalesce(p.TextNIO, \"\")),\n                     NMErlaubt: Coalesce(p.NichtMessbar, false),\n")
        t = rep(t, 'TextNIO: Coalesce(Text(o.Value.TextNIO), ""), Inaktiv: true}', 'TextNIO: Coalesce(Text(o.Value.TextNIO), ""), NMErlaubt: false, Inaktiv: true}')
        return t
    aendern(st, p, "16.4", "scrKategorie.OnVisible", onvisible)
    aendern(st, p, "16.5", "txtKaZahl.OnChange", lambda t: rep(t, "{WertZahl: z, Bewertung: b,", '{WertZahl: z, WertText: "", Bewertung: b,'))
    aendern(st, p, "16.5", "lblKaZahlInfo.Width", lambda t: rep(t, "Parent.Width - 256", "Parent.Width - 256 - If(btnKaNM.Visible, 136, 0)"))
    aendern(st, p, "16.5", "lblKaZahlInfo.Size", lambda t: rep(t, "14", "If(btnKaNM.Visible, 12, 14)"))
    neues_control(st, p, "btnKaNM", "conKaKarte", "Classic/Button@2.2.0", {
        "BorderColor": "clrTextGrau", "BorderThickness": "1",
        "Color": 'If(ThisItem.WertText = ' + NM + ', Color.White, clrTextGrau)',
        "DisabledColor": "Self.Color", "DisabledFill": "Self.Fill", "DisabledBorderColor": "clrTextGrau",
        "DisplayMode": "If(varNurLesen, DisplayMode.View, DisplayMode.Edit)",
        "Fill": 'If(ThisItem.WertText = ' + NM + ', clrTextGrau, clrKarte)', "Font": "Font.'Segoe UI'", "Height": "56",
        "HoverColor": "Self.Color", "HoverFill": 'If(ThisItem.WertText = ' + NM + ', ColorFade(clrTextGrau, -15%), clrHintergrund)',
        "OnSelect": 'If(ThisItem.WertText = ' + NM + ',\n'
                    '    Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: ""}),\n'
                    '    Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: ' + NM + ', WertZahl: Blank(), Bewertung: "", KritischOk: false, KritischZeit: "", KritischVon: ""});\n'
                    '    Set(varRueckPP, 0);\n'
                    '    Set(varKritPP, 0);\n'
                    '    Reset(txtKaZahl)\n'
                    ');\n'
                    'Set(varGeaendert, true)',
        "PressedColor": "Color.White", "PressedFill": "clrTextGrau",
        "RadiusBottomLeft": "8", "RadiusBottomRight": "8", "RadiusTopLeft": "8", "RadiusTopRight": "8",
        "Size": "13", "Text": 'If(ThisItem.WertText = ' + NM + ', "✓ nicht messbar", "nicht messbar")',
        "Visible": 'ThisItem.Typ = "ZAHL" && (ThisItem.NMErlaubt || ThisItem.WertText = ' + NM + ')',
        "Width": "120", "X": "Parent.Width - 140", "Y": '54 + If(ThisItem.Hinweis <> "", 24, 0)'})
    return p


# ---------------------------------------------------------------- Paket 14+15 (Abweichung zum letzten Rundgang, zwei Werte vergleichen)

UDF_P14 = ('fnAbweichung(z: Number, l: Number, mx: Number, proz: Boolean, steig: Boolean): Boolean = !IsBlank(z) && !IsBlank(l) && '
           '((steig && z < l) || (!IsBlank(mx) && Round(Abs(z - l), 6) > Round(If(proz, Abs(l) * mx / 100, mx), 6)));\n'
           'fnVergleich(z: Number, w: Number, tol: Number): Boolean = !IsBlank(z) && !IsBlank(w) && Round(Abs(z - w), 6) > Round(Coalesce(tol, 0), 6);')
REKALK = ('ClearCollect(colVglTmp, ForAll(Filter(colAntworten As a0, !a0.Inaktiv && a0.Typ = "ZAHL" && (a0.VglID <> 0 || !IsBlank(a0.Letzter))) As a,\n'
          '    With({w: LookUp(colAntworten As o, o.PruefpunktID = a.VglID)},\n'
          '        {PP: a.PruefpunktID,\n'
          '         Abw: fnAbweichung(a.WertZahl, a.Letzter, a.AbwMax, a.AbwProzent, a.NurSteigend),\n'
          '         Vgl: a.VglID <> 0 && fnVergleich(a.WertZahl, w.WertZahl, a.VglTol),\n'
          '         Text: If(fnAbweichung(a.WertZahl, a.Letzter, a.AbwMax, a.AbwProzent, a.NurSteigend), If(a.NurSteigend && a.WertZahl < a.Letzter, "kleiner als beim letzten Mal", "starke Abweichung zum letzten Mal"), "") & '
          'If(a.VglID <> 0 && fnVergleich(a.WertZahl, w.WertZahl, a.VglTol), If(fnAbweichung(a.WertZahl, a.Letzter, a.AbwMax, a.AbwProzent, a.NurSteigend), "; ", "") & "weicht von „" & w.Frage & "“ ab (" & Text(w.WertZahl) & ")", ""),\n'
          '         KPfl: a.KPflOrig}\n'
          '    )\n'
          '));\n'
          'ForAll(colVglTmp As v, Patch(colAntworten, LookUp(colAntworten, PruefpunktID = v.PP), {KommentarPflicht: v.KPfl || v.Abw || v.Vgl, AbwText: v.Text}))')
LETZTE_LADEN = ('If(!varNurLesen && varLetzteFuer <> varDurchID && CountRows(Filter(colPP, !IsBlank(AbwMax) || Coalesce(NurSteigend, false))) > 0,\n'
                '    Set(varLetzteFuer, varDurchID);\n'
                '    Set(varLetzteRg, varDurch.RundgangID);\n'
                '    Set(varLetzteTest, varDurch.TestDatensatz);\n'
                '    Set(varLetzteTag, varDurch.TagText);\n'
                '    Refresh(RG_Durchfuehrungen);\n'
                '    ClearCollect(colLetzteKand, FirstN(Sort(Filter(RG_Durchfuehrungen, RundgangID = varLetzteRg && Status = stAbgeschlossen && TestDatensatz = varLetzteTest), TagText, SortOrder.Descending), 20));\n'
                '    Set(varLetzteDurch, First(Sort(Filter(colLetzteKand, DateValue(TagText) < DateValue(varLetzteTag)), TagText, SortOrder.Descending)));\n'
                '    If(IsBlank(varLetzteDurch.ID),\n'
                '        Clear(colLetzte),\n'
                '        Set(varLetzteID, varLetzteDurch.ID);\n'
                '        ClearCollect(colLetzte, Filter(Ungroup(ForAll(Filter(RG_KategorieErgebnisse, DurchfuehrungID = varLetzteID) As e, '
                '{T: ForAll(Table(ParseJSON(e.Antworten)) As j, {PP: Value(j.Value.PruefpunktID), Z: Value(j.Value.WertZahl)})}), T), !IsBlank(Z)))\n'
                '    )\n'
                ');\n')
LETZTER_P = ('If(p.Eingabetyp.Value = "ZAHL" && (!IsBlank(p.AbwMax) || Coalesce(p.NurSteigend, false)), '
             'Coalesce(LookUp(colLetzte, PP = p.ID).Z, LookUp(colLetzte, PP = Coalesce(p.QuelleID, -1)).Z))')


def paket14(st):
    p = {"nr": 14, "props": [], "neu": []}
    for name, typ in (("AbwMax", "Zahl"), ("AbwProzent", "Ja/Nein"), ("NurSteigend", "Ja/Nein"), ("VergleichPunkt", "Zahl"), ("VergleichTol", "Zahl")):
        st.sp.append(("RG_Pruefpunkte", name, typ))
    st.sp.append(("RG_Pruefpunkte", "QuelleID (vorhanden, vom Builder)", "Zahl"))
    aendern(st, p, "14.3", "App.Formulas", lambda t: rep(
        t, "fnFehlt(typ: Text,", UDF_P14 + "\nfnFehlt(typ: Text,"))

    def onvisible(t):
        t = rep(t, ");\nSet(varGespeichertBeimOeffnen, varErgebnis.GespeichertAm);\n",
                ");\n" + LETZTE_LADEN + "Set(varGespeichertBeimOeffnen, varErgebnis.GespeichertAm);\n")
        t = rep(t, 'NMErlaubt: false, Inaktiv: false}',
                'NMErlaubt: false, KPflOrig: false, Letzter: Value(a.Letzter), LetzterTag: Coalesce(Text(a.LetzterTag), ""), AbwMax: Blank(), AbwProzent: false, '
                'NurSteigend: false, VglID: 0, VglTol: 0, AbwText: Coalesce(Text(a.AbwText), ""), Inaktiv: false}')
        t = rep(t, "                     NMErlaubt: Coalesce(p.NichtMessbar, false),\n",
                "                     NMErlaubt: Coalesce(p.NichtMessbar, false),\n"
                "                     KPflOrig: Coalesce(p.KommentarPflicht, false),\n"
                "                     Letzter: " + LETZTER_P + ",\n"
                "                     LetzterTag: If(IsBlank(varLetzteDurch.TagText), \"\", Text(DateValue(varLetzteDurch.TagText), \"dd.mm.\")),\n"
                "                     AbwMax: p.AbwMax,\n"
                "                     AbwProzent: Coalesce(p.AbwProzent, false),\n"
                "                     NurSteigend: Coalesce(p.NurSteigend, false),\n"
                "                     VglID: Coalesce(p.VergleichPunkt, 0),\n"
                "                     VglTol: Coalesce(p.VergleichTol, 0),\n"
                "                     AbwText: \"\",\n")
        t = rep(t, 'NMErlaubt: false, Inaktiv: true}',
                'NMErlaubt: false, KPflOrig: false, Letzter: Value(o.Value.Letzter), LetzterTag: Coalesce(Text(o.Value.LetzterTag), ""), AbwMax: Blank(), AbwProzent: false, '
                'NurSteigend: false, VglID: 0, VglTol: 0, AbwText: Coalesce(Text(o.Value.AbwText), ""), Inaktiv: true}')
        t = rep(t, "ClearCollect(colAbsTmp,", "If(!varNurLesen, " + REKALK.replace("\n", "\n    ") + ");\nClearCollect(colAbsTmp,")
        return t
    aendern(st, p, "14.4", "scrKategorie.OnVisible", onvisible)
    aendern(st, p, "14.5", "btnKaSpeichern.OnSelect", lambda t: rep(
        t, "TextIO, TextNIO), JSONFormat.Compact)", "TextIO, TextNIO, Letzter, LetzterTag, AbwText), JSONFormat.Compact)"))
    aendern(st, p, "14.6", "txtKaZahl.OnChange", lambda t: rep(t, ");\nSet(varGeaendert, true)", ");\n" + REKALK + ";\nSet(varGeaendert, true)"))
    aendern(st, p, "14.6", "btnKaNM.OnSelect", lambda t: rep(t, ");\nSet(varGeaendert, true)", ");\n" + REKALK + ";\nSet(varGeaendert, true)"))
    aendern(st, p, "14.6", "btnKaRueckNein.OnSelect", lambda t: rep(t, "Set(varRueckPP, 0);\nSet(varGeaendert, true)", "Set(varRueckPP, 0);\n" + REKALK + ";\nSet(varGeaendert, true)"))
    aendern(st, p, "14.6", "btnKaKritVersehen.OnSelect", lambda t: rep(t, "Set(varKritPP, 0);\nSet(varGeaendert, true)", "Set(varKritPP, 0);\n" + REKALK + ";\nSet(varGeaendert, true)"))
    aendern(st, p, "14.7", "lblKaZahlInfo.Height", lambda t: rep(t, "56", "If(btnKaNM.Visible || !IsBlank(ThisItem.Letzter) || ThisItem.AbwText <> \"\", 64, 56)"))
    aendern(st, p, "14.7", "lblKaZahlInfo.Text", lambda t: t + ' & If(IsBlank(ThisItem.Letzter), "", "  ·  zuletzt " & Text(ThisItem.Letzter) & If(ThisItem.LetzterTag = "", "", " (" & ThisItem.LetzterTag & ")")) & '
            'If(ThisItem.AbwText = "", "", "  ·  " & ThisItem.AbwText & If(varNurLesen || Trim(ThisItem.Kommentar) <> "", ", begründet", ", bitte begründen"))')
    aendern(st, p, "14.7", "lblKaZahlInfo.Color", lambda t: rep(t, "), clrWarnung, clrTextGrau)", ") || ThisItem.AbwText <> \"\", clrWarnung, clrTextGrau)"))
    aendern(st, p, "14.7", "lblKaZahlInfo.Size", lambda t: rep(t, "If(btnKaNM.Visible, 12, 14)", "If(btnKaNM.Visible || !IsBlank(ThisItem.Letzter) || ThisItem.AbwText <> \"\", 12, 14)"))
    aendern(st, p, "14.8", "htmProtokoll.HtmlText", lambda t: rep(
        t, """If(w, " <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>", "") &""",
        """If(w, " <span style='color:#9A5B00'>(außerhalb Soll, begründet)</span>", "") & If(Coalesce(Text(a.Value.AbwText), "") = "", "", " <span style='color:#9A5B00'>(" & fnHtml(Text(a.Value.AbwText)) & If(IsBlank(a.Value.Letzter), "", ", zuletzt " & Text(Value(a.Value.Letzter))) & ", begründet)</span>") &"""))
    return p


# ---------------------------------------------------------------- Paket 17 (Archiv vergangener Rundgänge)

def _knopf(art, **kw):
    if art == "primaer":
        p = {"BorderThickness": "0", "Color": "Color.White", "Fill": "clrPrimaer", "HoverFill": "ColorFade(clrPrimaer, -20%)",
             "PressedFill": "ColorFade(clrPrimaer, -35%)", "HoverColor": "Color.White", "PressedColor": "Color.White"}
    else:
        p = {"BorderColor": "clrPrimaer", "BorderThickness": "1", "Color": "clrPrimaer", "Fill": "clrKarte", "HoverFill": "clrPrimaerHell",
             "PressedFill": "clrPrimaerHell", "HoverColor": "clrPrimaer", "PressedColor": "clrPrimaer"}
    p.update({"Font": "Font.'Segoe UI'", "RadiusBottomLeft": "8", "RadiusBottomRight": "8", "RadiusTopLeft": "8", "RadiusTopRight": "8",
              "DisabledFill": "clrGesperrtHell", "DisabledColor": "clrGesperrt", "DisabledBorderColor": "clrGesperrtHell"})
    p.update(kw)
    return p


def _label(**kw):
    p = {"Font": "Font.'Segoe UI'", "Color": "clrText", "Size": "14"}
    p.update(kw)
    return p


AR_LISTE = ('Filter(colArchiv As d, (varArTest || !Coalesce(d.TestDatensatz, false)) && (varArOffen || d.Status = stAbgeschlossen) && '
            '(!varArNurNio || Coalesce(d.AnzahlNIO, 0) > 0))')
AR_SUCHEN = ('If(!varIsLoading,\n'
             '    Set(varIsLoading, true);\n'
             '    Set(varArVon, Coalesce(dpArVon.SelectedDate, DateAdd(Today(), -3, TimeUnit.Months)));\n'
             '    Set(varArBis, DateAdd(Coalesce(dpArBis.SelectedDate, Today()), 1, TimeUnit.Days));\n'
             '    Set(varArRg, Coalesce(ddArRg.Selected.ID, 0));\n'
             '    Refresh(RG_Durchfuehrungen);\n'
             '    If(varArRg = 0,\n'
             '        ClearCollect(colArchiv, Sort(Filter(RG_Durchfuehrungen, StartZeit >= varArVon && StartZeit < varArBis), StartZeit, SortOrder.Descending)),\n'
             '        ClearCollect(colArchiv, Sort(Filter(RG_Durchfuehrungen, StartZeit >= varArVon && StartZeit < varArBis && RundgangID = varArRg), StartZeit, SortOrder.Descending))\n'
             '    );\n'
             '    If(CountRows(colArchiv) >= 2000, Notify("Sehr viele Rundgänge im Zeitraum – es werden höchstens 2000 angezeigt. Bitte den Zeitraum verkleinern.", NotificationType.Warning));\n'
             '    Set(varIsLoading, false)\n'
             ')')


def paket17(st):
    p = {"nr": 17, "props": [], "neu": []}
    aendern(st, p, "17.2", "btnRuZurueck.OnSelect", lambda t: rep(
        t, "Navigate(scrStart, ScreenTransition.None)", "If(varAusArchiv, Navigate(scrArchiv, ScreenTransition.None), Navigate(scrStart, ScreenTransition.None))"))
    aendern(st, p, "17.2", "scrStart.OnVisible", lambda t: rep(t, "Set(varIsLoading, true);\n", "Set(varIsLoading, true);\nSet(varAusArchiv, false);\n"))
    ganz(st, p, "17.2", "lblStartListeTitel.Width", "Parent.Width - 232")
    ganz(st, p, "17.2", "btnRuZurueck.Text", 'If(varAusArchiv, "‹  Archiv", "‹  Übersicht")')
    aendern(st, p, "17.2", "scrProtokoll.OnVisible", lambda t: rep(
        t, "Set(varArchivStart, varDurch.Status = stAbgeschlossen && IsBlank(varDurch.ProtokollUrl))",
        "Set(varArchivStart, !varAusArchiv && varDurch.Status = stAbgeschlossen && IsBlank(varDurch.ProtokollUrl))"))
    neues_control(st, p, "btnStartArchiv", "scrStart", "Classic/Button@2.2.0", _knopf(
        "sekundaer", Height="40", Size="15", Text='"🗂 Archiv"', Width="184", X="Parent.Width - 208", Y="216",
        DisplayMode="If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)",
        OnSelect="If(!varIsLoading, Navigate(scrArchiv, ScreenTransition.None))"))
    neues_control(st, p, "scrArchiv", None, "Screen", {
        "Fill": "clrHintergrund",
        "OnVisible": ("Set(varArTest, Coalesce(varArTest, false));\nSet(varArOffen, Coalesce(varArOffen, false));\nSet(varArNurNio, Coalesce(varArNurNio, false));\n"
                      "If(IsEmpty(colArRg), ClearCollect(colArRg, Sort(ShowColumns(RG_Rundgaenge, ID, Title), Title)));\n"
                      "If(IsEmpty(colArchiv) || !varAusArchiv, Select(btnArSuchen))")})
    neues_control(st, p, "conArKopf", "scrArchiv", "GroupContainer@1.5.0", {"Fill": "clrPrimaer", "Height": "96", "Width": "Parent.Width"})
    neues_control(st, p, "btnArZurueck", "conArKopf", "Classic/Button@2.2.0", _knopf(
        "primaer", Fill="RGBA(255, 255, 255, 0.14)", HoverFill="RGBA(255, 255, 255, 0.26)", PressedFill="RGBA(255, 255, 255, 0.34)",
        Height="52", Size="16", Text='"← Start"', Width="140", X="24", Y="22",
        OnSelect="If(!varIsLoading,\n    Set(varAusArchiv, false);\n    Navigate(scrStart, ScreenTransition.None)\n)"))
    neues_control(st, p, "lblArTitel", "conArKopf", "Label@2.5.1", _label(
        Color="Color.White", FontWeight="FontWeight.Semibold", Height="96", Size="24", Text='"Archiv"', Width="Parent.Width - 200", X="180", Y="0"))
    neues_control(st, p, "lblArVon", "scrArchiv", "Label@2.5.1", _label(Color="clrTextGrau", Height="24", Size="13", Text='"von"', Width="220", X="24", Y="108"))
    neues_control(st, p, "dpArVon", "scrArchiv", "Classic/DatePicker@2.6.0", {
        "AccessibleLabel": '"Zeitraum von"', "BorderColor": "clrRahmen", "Color": "clrText", "DefaultDate": "DateAdd(Today(), -3, TimeUnit.Months)",
        "Font": "Font.'Segoe UI'", "Format": "DateTimeFormat.ShortDate", "Height": "52", "IconBackground": "clrPrimaer", "IconFill": "Color.White",
        "Size": "15", "StartOfWeek": "StartOfWeek.Monday", "Width": "220", "X": "24", "Y": "132"})
    neues_control(st, p, "lblArBis", "scrArchiv", "Label@2.5.1", _label(Color="clrTextGrau", Height="24", Size="13", Text='"bis"', Width="220", X="260", Y="108"))
    neues_control(st, p, "dpArBis", "scrArchiv", "Classic/DatePicker@2.6.0", {
        "AccessibleLabel": '"Zeitraum bis"', "BorderColor": "clrRahmen", "Color": "clrText", "DefaultDate": "Today()",
        "Font": "Font.'Segoe UI'", "Format": "DateTimeFormat.ShortDate", "Height": "52", "IconBackground": "clrPrimaer", "IconFill": "Color.White",
        "Size": "15", "StartOfWeek": "StartOfWeek.Monday", "Width": "220", "X": "260", "Y": "132"})
    neues_control(st, p, "btnArSuchen", "scrArchiv", "Classic/Button@2.2.0", _knopf(
        "primaer", Height="52", Size="16", Text='"Suchen"', Width="Parent.Width - 520", X="496", Y="132",
        DisplayMode="If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)", OnSelect=AR_SUCHEN))
    neues_control(st, p, "ddArRg", "scrArchiv", "Classic/DropDown@2.3.1", {
        "AccessibleLabel": '"Rundgang"', "BorderColor": "clrRahmen", "BorderThickness": "1", "ChevronBackground": "clrPrimaer", "ChevronFill": "Color.White",
        "Color": "clrText", "Default": '"Alle Rundgänge"', "Fill": "clrKarte", "Font": "Font.'Segoe UI'", "Height": "52",
        "Items": 'Ungroup(Table({T: Table({ID: 0, Title: "Alle Rundgänge"})}, {T: colArRg}), T)', "Items.Value": "Title",
        "PaddingLeft": "12", "Size": "15", "Width": "Parent.Width - 48", "X": "24", "Y": "196"})
    for i, (name, var, text) in enumerate((("btnArNurNio", "varArNurNio", "nur mit Mängeln"), ("btnArOffen", "varArOffen", "auch offene"),
                                           ("btnArTest", "varArTest", "Testläufe"))):
        neues_control(st, p, name, "scrArchiv", "Classic/Button@2.2.0", _knopf(
            "sekundaer", Height="44", Size="14", Text='If(%s, "✓ ", "○ ") & "%s"' % (var, text),
            Fill="If(%s, clrPrimaerHell, clrKarte)" % var, Width="(Parent.Width - 64) / 3", X="24 + %d * ((Parent.Width - 64) / 3 + 8)" % i, Y="260",
            OnSelect="Set(%s, !%s)" % (var, var)))
    neues_control(st, p, "lblArAnzahl", "scrArchiv", "Label@2.5.1", _label(
        Color="clrTextGrau", Height="28", Size="13", Width="Parent.Width - 48", X="24", Y="312",
        Text='CountRows(' + AR_LISTE + ') & " Rundgänge · " & Text(varArVon, "dd.mm.yyyy") & " bis " & Text(DateAdd(varArBis, -1, TimeUnit.Days), "dd.mm.yyyy")'))
    neues_control(st, p, "galArListe", "scrArchiv", "Gallery@2.15.0", {
        "AccessibleLabel": '"Vergangene Rundgänge"', "Height": "Parent.Height - 344", "Items": AR_LISTE, "ShowScrollbar": "true",
        "TemplatePadding": "0", "TemplateSize": "104", "Width": "Parent.Width", "X": "0", "Y": "344"})
    neues_control(st, p, "conArKarte", "galArListe", "GroupContainer@1.5.0", {
        "BorderColor": 'If(ThisItem.Status = stAbgeschlossen, clrRahmen, clrWarnung)', "BorderThickness": "1", "Fill": "clrKarte",
        "Height": "Parent.TemplateHeight - 12", "RadiusBottomLeft": "12", "RadiusBottomRight": "12", "RadiusTopLeft": "12", "RadiusTopRight": "12",
        "Width": "Parent.TemplateWidth - 48", "X": "24", "Y": "6"})
    neues_control(st, p, "lblArName", "conArKarte", "Label@2.5.1", _label(
        FontWeight="FontWeight.Semibold", Height="32", Size="16", Text='ThisItem.RundgangName & If(Coalesce(ThisItem.TestDatensatz, false), "  · Test", "")',
        Width="Parent.Width - 236", X="20", Y="10", Wrap="false"))
    neues_control(st, p, "lblArInfo", "conArKarte", "Label@2.5.1", _label(
        Color='If(Coalesce(ThisItem.AnzahlNIO, 0) > 0, clrFehler, clrTextGrau)', Height="50", Size="13", VerticalAlign="VerticalAlign.Top",
        Text=('fnTagAnzeige(DateValue(ThisItem.TagText)) & Char(10) & Coalesce(ThisItem.PrueferName, "") & "  ·  " & '
              'If(ThisItem.Status = stAbgeschlossen, Coalesce(ThisItem.AnzahlNIO, 0) & " n.i.O.", "nicht abgeschlossen")'),
        Width="Parent.Width - 236", X="20", Y="40"))
    neues_control(st, p, "btnArPdf", "conArKarte", "Classic/Button@2.2.0", _knopf(
        "sekundaer", Height="40", Size="14", Text='"PDF"', Width="80", X="Parent.Width - 196", Y="(Parent.Height - 40) / 2",
        Visible='!IsBlank(ThisItem.ProtokollUrl)', OnSelect="Launch(ThisItem.ProtokollUrl)"))
    neues_control(st, p, "btnArOeffnen", "conArKarte", "Classic/Button@2.2.0", _knopf(
        "primaer", Height="40", Size="14", Text='"Ansehen"', Width="100", X="Parent.Width - 108", Y="(Parent.Height - 40) / 2",
        DisplayMode="If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)",
        OnSelect=('If(ThisItem.Status <> stAbgeschlossen,\n'
                  '    Notify("Nicht abgeschlossene Rundgänge setzt du auf der Startseite am jeweiligen Tag fort.", NotificationType.Information),\n'
                  '    Set(varRgID, ThisItem.RundgangID);\n'
                  '    Set(varDurchID, ThisItem.ID);\n'
                  '    Set(varWeiter, false);\n'
                  '    Set(varAusArchiv, true);\n'
                  '    Navigate(scrRundgang, ScreenTransition.None)\n'
                  ')')))
    neues_control(st, p, "lblArLeer", "scrArchiv", "Label@2.5.1", _label(
        Color="clrTextGrau", Height="60", Size="15", Text='"Keine Rundgänge im gewählten Zeitraum."', Width="Parent.Width - 48", X="24", Y="360",
        Visible="IsEmpty(galArListe.AllItems) && !varIsLoading"))
    neues_control(st, p, "conArLaden", "scrArchiv", "GroupContainer@1.5.0", {
        "Fill": "RGBA(244, 245, 249, 0.75)", "Height": "Parent.Height", "Visible": "varIsLoading", "Width": "Parent.Width"})
    neues_control(st, p, "lblArLaden", "conArLaden", "Label@2.5.1", _label(
        Align="Align.Center", Color="clrPrimaer", FontWeight="FontWeight.Semibold", Height="40", Size="18", Text='"Bitte warten …"',
        Width="Parent.Width", X="0", Y="(Parent.Height - 40) / 2"))
    return p


# ---------------------------------------------------------------- Paket 13 (Anleitung im ⓘ-Fenster)

def paket13(st):
    p = {"nr": 13, "props": [], "neu": []}
    st.sp.append(("RG_Anleitungen", "(neue Liste: Title, Anleitung, Aktiv)", "Liste"))
    st.sp.append(("RG_Anleitungen", "Anleitung", "Spalte"))
    st.sp.append(("RG_Pruefpunkte", "AnleitungID", "Zahl"))
    st.neue_quellen.add("RG_Anleitungen")

    def onvisible(t):
        t = rep(t, "Set(varBildID, 0);\n", "Set(varBildID, 0);\nSet(varInfoID, 0);\n")
        t = rep(t, "Refresh(RG_KategorieErgebnisse);\nConcurrent(\n", "Refresh(RG_KategorieErgebnisse);\nRefresh(RG_Anleitungen);\nConcurrent(\n")
        t = rep(t, "    ClearCollect(colKontakte, Filter(RG_Ansprechpartner, Aktiv = true))\n);",
                "    ClearCollect(colKontakte, Filter(RG_Ansprechpartner, Aktiv = true)),\n    ClearCollect(colAnlAktivApp, ShowColumns(Filter(RG_Anleitungen, Aktiv = true), ID))\n);")
        t = rep(t, 'AbwText: Coalesce(Text(a.AbwText), ""), Inaktiv: false}', 'AbwText: Coalesce(Text(a.AbwText), ""), AnlID: If(IsBlank(LookUp(colAnlAktivApp, ID = Coalesce(pp.AnleitungID, 0))), 0, pp.AnleitungID), Inaktiv: false}')
        t = rep(t, "                     AbwText: \"\",\n", "                     AbwText: \"\",\n                     AnlID: If(IsBlank(LookUp(colAnlAktivApp, ID = Coalesce(p.AnleitungID, 0))), 0, p.AnleitungID),\n")
        t = rep(t, 'AbwText: Coalesce(Text(o.Value.AbwText), ""), Inaktiv: true}', 'AbwText: Coalesce(Text(o.Value.AbwText), ""), AnlID: 0, Inaktiv: true}')
        return t
    aendern(st, p, "13.3", "scrKategorie.OnVisible", onvisible)
    aendern(st, p, "13.4", "lblKaFrage.Width", lambda t: rep(t, "If(ThisItem.BildID > 0, 80, 0)", "If(ThisItem.BildID > 0, 80, 0) - If(ThisItem.AnlID > 0, 64, 0)"))
    neues_control(st, p, "btnKaInfo", "conKaKarte", "Classic/Button@2.2.0", {
        "BorderColor": "clrPrimaer", "BorderThickness": "1", "Color": "clrPrimaer", "Fill": "clrKarte", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold",
        "Height": "40", "HoverColor": "clrPrimaer", "HoverFill": "clrPrimaerHell", "PressedColor": "clrPrimaer", "PressedFill": "clrPrimaerHell",
        "OnSelect": "Set(varInfoFrage, ThisItem.Frage);\nSet(varInfoBild, ThisItem.BildID);\nSet(varInfo, LookUp(RG_Anleitungen, ID = ThisItem.AnlID));\n"
                    "If(IsBlank(varInfo.ID), Notify(\"Die Anleitung wurde nicht gefunden.\", NotificationType.Warning), Set(varInfoID, ThisItem.AnlID))",
        "RadiusBottomLeft": "20", "RadiusBottomRight": "20", "RadiusTopLeft": "20", "RadiusTopRight": "20", "Size": "16", "Text": '"ⓘ"',
        "Visible": "ThisItem.AnlID > 0", "Width": "40", "X": "Parent.Width - 60 - If(ThisItem.BildID > 0, 80, 0)", "Y": "7"})
    neues_control(st, p, "conKaInfo", "scrKategorie", "GroupContainer@1.5.0", {
        "Fill": "RGBA(0, 0, 0, 0.45)", "Height": "Parent.Height", "Visible": "varInfoID > 0", "Width": "Parent.Width"})
    neues_control(st, p, "btnKaInfoSperre", "conKaInfo", "Classic/Button@2.2.0", {
        "BorderThickness": "0", "Fill": "RGBA(0, 0, 0, 0)", "Height": "Parent.Height", "HoverFill": "RGBA(0, 0, 0, 0)",
        "PressedFill": "RGBA(0, 0, 0, 0)", "Text": '""', "Width": "Parent.Width"})
    neues_control(st, p, "conKaInfoKarte", "conKaInfo", "GroupContainer@1.5.0", {
        "Fill": "clrKarte", "Height": "Min(Parent.Height - 32, 1000)",
        "RadiusBottomLeft": "16", "RadiusBottomRight": "16", "RadiusTopLeft": "16", "RadiusTopRight": "16",
        "Width": "Parent.Width - 48", "X": "24", "Y": "(Parent.Height - Self.Height) / 2"})
    neues_control(st, p, "lblKaInfoTitel", "conKaInfoKarte", "Label@2.5.1", {
        "Color": "clrPrimaer", "Font": "Font.'Segoe UI'", "FontWeight": "FontWeight.Semibold", "Height": "40", "Size": "19",
        "Text": '"ⓘ " & varInfo.Title', "Width": "Parent.Width - 40", "Wrap": "false", "X": "20", "Y": "14"})
    neues_control(st, p, "lblKaInfoFrage", "conKaInfoKarte", "Label@2.5.1", {
        "Color": "clrTextGrau", "Font": "Font.'Segoe UI'", "Height": "28", "Size": "13", "Text": '"zu: " & varInfoFrage',
        "Width": "Parent.Width - 40", "Wrap": "false", "X": "20", "Y": "54"})
    neues_control(st, p, "lblKaInfoText", "conKaInfoKarte", "Label@2.5.1", {
        "Color": "clrText", "Font": "Font.'Segoe UI'", "Height": "If(varInfoBild > 0, (Parent.Height - 180) * 0.55, Parent.Height - 180)",
        "Overflow": "Overflow.Scroll", "Size": "16", "Text": 'Coalesce(varInfo.Anleitung, "")', "VerticalAlign": "VerticalAlign.Top",
        "Width": "Parent.Width - 40", "X": "20", "Y": "88"})
    neues_control(st, p, "imgKaInfo", "conKaInfoKarte", "Image@2.2.3", {
        "AccessibleLabel": '"Beispielbild zu " & varInfoFrage',
        "Height": "(Parent.Height - 180) * 0.45 - 8", "Image": "If(varInfoID > 0 && varInfoBild > 0, LookUp(RG_Hinweisbilder, ID = varInfoBild).Thumbnail.Large)",
        "ImagePosition": "ImagePosition.Fit", "Visible": "varInfoBild > 0", "Width": "Parent.Width - 40", "X": "20",
        "Y": "96 + (Parent.Height - 180) * 0.55"})
    neues_control(st, p, "btnKaInfoSchliessen", "conKaInfoKarte", "Classic/Button@2.2.0", {
        "BorderThickness": "0", "Color": "Color.White", "Fill": "clrPrimaer", "Font": "Font.'Segoe UI'", "Height": "56",
        "HoverFill": "ColorFade(clrPrimaer, -20%)", "OnSelect": "Set(varInfoID, 0)", "PressedFill": "ColorFade(clrPrimaer, -35%)",
        "RadiusBottomLeft": "10", "RadiusBottomRight": "10", "RadiusTopLeft": "10", "RadiusTopRight": "10",
        "Size": "17", "Text": '"Schließen"', "Width": "200", "X": "Parent.Width - 220", "Y": "Parent.Height - 76"})
    return p


# ---------------------------------------------------------------- Paket 19 (Fix: Eingaben anderer Typen überschreiben WertText)
# Befund 03.11. (Studio-Test nach N + 8-10): Datum springt zurück. Ursache (geschlussfolgert): Ändert sich ThisItem.WertText,
# setzen die unsichtbaren cboKaMehrfach/ddKaAuswahl ihre Auswahl neu und ihr OnChange schreibt "" zurück.
# Abhilfe: jede Schreibstelle schreibt nur beim eigenen Typ und nur bei echter Änderung.

def _nur_typ(t, bedingung):
    t = t.rstrip()
    zeilen = t.split("\n")
    return "If(" + bedingung + ",\n" + "\n".join("    " + z for z in zeilen) + "\n)"


def paket19(st):
    p = {"nr": 19, "props": [], "neu": []}
    mehr_neu = ('Concat(Filter(ForAll(Split(ThisItem.Auswahl, ";") As s, {Value: Trim(s.Value)}) As i, '
                'i.Value <> "" && i.Value in Self.SelectedItems.Value), Value, "; ")')
    alt_cbo = ("Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: " + mehr_neu + "});\n"
               "Set(varGeaendert, true)")
    if rg.ohne_kommentare(st.props["cboKaMehrfach.OnChange"]).strip() != alt_cbo:
        raise Abbruch("Anker cboKaMehrfach.OnChange weicht ab")
    ganz(st, p, "19.1", "cboKaMehrfach.OnChange",
         "With({neu: " + mehr_neu + "},\n"
         "    If(ThisItem.Typ = \"MEHRFACH\" && !varNurLesen && neu <> ThisItem.WertText,\n"
         "        Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: neu});\n"
         "        Set(varGeaendert, true)\n"
         "    )\n"
         ")")
    aendern(st, p, "19.2", "ddKaAuswahl.OnChange", lambda t: _nur_typ(
        t, 'ThisItem.Typ = "AUSWAHL" && !varNurLesen && Coalesce(Self.Selected.Value, "") <> ThisItem.WertText'))
    dat = '(ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen'
    for i, k in enumerate(["dpKaDatum.OnChange", "ddKaStunde.OnChange", "ddKaMinute.OnChange"], 3):
        aendern(st, p, "19.%d" % i, k, lambda t: _nur_typ(t, dat))
    aendern(st, p, "19.6", "txtKaText.OnChange", lambda t: _nur_typ(
        t, 'ThisItem.Typ = "TEXT" && !varNurLesen && Self.Text <> ThisItem.WertText'))
    return p


# ---------------------------------------------------------------- Paket 20 (Fix: Uhrzeit bei DATUMZEIT lässt sich nicht setzen)
# Befund 03.11. (Studio nach 19): Stunde wählen -> fnDatumText schreibt ohne Minute nur das Datum, Default der Stunde
# liest Len < 16 -> Stunde springt zurück. Abhilfe: Teilzeit mit Platzhalter "--" speichern ("03.11.2026 08:--"),
# Defaults lesen nur echte Ziffern, fnFehltGrund meldet "Uhrzeit", solange ein "-" drin ist.

def paket20(st):
    p = {"nr": 20, "props": [], "neu": []}

    def formeln(t):
        t = rep(t, 'If(mitZeit && h <> "" && m <> "", " " & h & ":" & m, "")',
                'If(mitZeit && (h <> "" || m <> ""), " " & If(h = "", "--", h) & ":" & If(m = "", "--", m), "")')
        t = rep(t, 'typ = "DATUMZEIT" && wt <> "" && Len(wt) < 16, "Uhrzeit"',
                'typ = "DATUMZEIT" && wt <> "" && (Len(wt) < 16 || "-" in wt), "Uhrzeit"')
        return t
    aendern(st, p, "20.1", "App.Formulas", formeln)
    aendern(st, p, "20.2", "ddKaStunde.Default", lambda t: rep(
        t, 'If(Len(ThisItem.WertText) >= 16, Mid(ThisItem.WertText, 12, 2), "")',
        'If(Len(ThisItem.WertText) >= 16 && Mid(ThisItem.WertText, 12, 2) <> "--", Mid(ThisItem.WertText, 12, 2), "")'))
    aendern(st, p, "20.3", "ddKaMinute.Default", lambda t: rep(
        t, 'If(Len(ThisItem.WertText) >= 16, Mid(ThisItem.WertText, 15, 2), "")',
        'If(Len(ThisItem.WertText) >= 16 && Mid(ThisItem.WertText, 15, 2) <> "--", Mid(ThisItem.WertText, 15, 2), "")'))
    return p


# ---------------------------------------------------------------- Paket 21 (Fix: Uhrzeit, zweiter Anlauf)
# Befund 03.11. (Studio nach 20): Stunde springt weiter zurück, WertText bleibt nur Datum. Vermutung Einsetz-Chat (passt):
# Nach dem Patch feuert dpKaDatum.OnChange erneut und baut den Text aus den (leeren) Nachbarfeldern neu.
# Abhilfe: Jedes Feld ändert nur seinen Teil, den Rest liest es aus ThisItem.WertText, und schreibt nur bei echter Änderung.

TEIL_H = 'If(Len(ThisItem.WertText) >= 16, Mid(ThisItem.WertText, 12, 2), "--")'
TEIL_M = 'If(Len(ThisItem.WertText) >= 16, Mid(ThisItem.WertText, 15, 2), "--")'


def paket21(st):
    p = {"nr": 21, "props": [], "neu": []}
    patch = "Patch(colAntworten, LookUp(colAntworten, PruefpunktID = ThisItem.PruefpunktID), {WertText: %s});\n        Set(varGeaendert, true)"
    ganz(st, p, "21.1", "dpKaDatum.OnChange",
         "With({h: " + TEIL_H + ", m: " + TEIL_M + "},\n"
         "    If((ThisItem.Typ = \"DATUM\" || ThisItem.Typ = \"DATUMZEIT\") && !varNurLesen && Coalesce(Text(Self.SelectedDate, \"dd.mm.yyyy\"), \"\") <> Left(ThisItem.WertText, 10),\n"
         "        " + patch % 'fnDatumText(Self.SelectedDate, If(h = "--", "", h), If(m = "--", "", m), ThisItem.Typ = "DATUMZEIT")' + "\n"
         "    )\n)")
    for nr, key, eigen, anderer, links in ((2, "ddKaStunde.OnChange", TEIL_H, TEIL_M, True), (3, "ddKaMinute.OnChange", TEIL_M, TEIL_H, False)):
        neu_t = 'If(neu = "--" && rest = "--", "", " " & %s)' % ('neu & ":" & rest' if links else 'rest & ":" & neu')
        ganz(st, p, "21.%d" % nr, key,
             "With({neu: If(Coalesce(Self.Selected.Value, \"\") = \"\", \"--\", Self.Selected.Value), alt: " + eigen + ", rest: " + anderer + "},\n"
             "    If(ThisItem.Typ = \"DATUMZEIT\" && !varNurLesen && Len(ThisItem.WertText) >= 10 && neu <> alt,\n"
             "        " + patch % ("Left(ThisItem.WertText, 10) & " + neu_t) + "\n"
             "    )\n)")
    return p


# ---------------------------------------------------------------- Paket 22 (Hinweis „mehrere möglich“ an der Frage)

def paket22(st):
    p = {"nr": 22, "props": [], "neu": []}
    aendern(st, p, "22.1", "lblKaFrage.Text", lambda t: rep(
        t, 'ThisItem.Frage & If(ThisItem.Pflicht, "  *", "")',
        'ThisItem.Frage & If(ThisItem.Pflicht, "  *", "") & If(ThisItem.Typ = "MEHRFACH", "  (mehrere möglich)", "")'))
    return p


# ---------------------------------------------------------------- Paket 23 (A8 Banner „Nicht abgeschlossen“, A11 Testkennung)
OFFEN_F = 'Filter(colOffenAlt, DateValue(TagText) < varHeute && !Coalesce(TestDatensatz, false))'
OFFEN_L = 'SortByColumns(' + OFFEN_F + ', "TagText", SortOrder.Ascending, "ID", SortOrder.Ascending)'
OFFEN_I = 'Min(Max(Coalesce(varOffenNr, 1), 1), CountRows(l))'


def paket23(st):
    p = {"nr": 23, "props": [], "neu": []}
    st.sp.append(("RG_Rundgaenge", "Testrundgang", "Ja/Nein"))
    aendern(st, p, "23.2", "btnStartTagLaden.OnSelect", lambda t: rep(rep(t, "RundgangID, RundgangName, TagText))", "RundgangID, RundgangName, TagText, TestDatensatz))"),
        "\n);\nSet(varIsLoading, false)", "\n);\nSet(varOffenNr, 1);\nSet(varIsLoading, false)"))
    ganz(st, p, "23.3", "conStartOffen.Visible", "CountRows(" + OFFEN_F + ") > 0")
    ganz(st, p, "23.3", "lblStartOffen.Text",
         "With({l: " + OFFEN_L + "},\n"
         "    If(CountRows(l) = 0, \"\",\n"
         "        With({i: " + OFFEN_I + "},\n"
         "            With({o: Index(l, i)},\n"
         "                \"⚠  Nicht abgeschlossen: \" & o.RundgangName & \" vom \" & Text(DateValue(o.TagText), \"dd.mm.yyyy\") & If(CountRows(l) > 1, \"  (\" & i & \"/\" & CountRows(l) & \")\", \"\")\n"
         "            )\n        )\n    )\n)")
    ganz(st, p, "23.3", "lblStartOffen.Width", "If(CountRows(" + OFFEN_F + ") > 1, Parent.Width - 380, Parent.Width - 260)")
    ganz(st, p, "23.3", "btnStartOffen.OnSelect",
         "If(!varIsLoading,\n"
         "    With({l: " + OFFEN_L + "},\n"
         "        If(CountRows(l) > 0,\n"
         "            With({o: Index(l, " + OFFEN_I + ")},\n"
         "                Set(varTag, DateValue(o.TagText));\n"
         "                Set(varTagText, o.TagText);\n"
         "                Set(varRgID, o.RundgangID);\n"
         "                Set(varSchluessel, o.Title);\n"
         "                Set(varDurchID, o.ID);\n"
         "                Navigate(scrRundgang, ScreenTransition.None)\n"
         "            )\n        )\n    )\n)")
    neues_control(st, p, "btnStartOffenWeiter", "conStartOffen", "Classic/Button@2.2.0", _knopf(
        "sekundaer", BorderColor="clrFehler", Color="clrFehler", HoverColor="clrFehler", PressedColor="clrFehler",
        HoverFill="clrFehlerHell", PressedFill="clrFehlerHell", Fill="Color.White",
        Height="56", Size="14", Text='"Weiter ›"', Width="120", X="Parent.Width - 356", Y="20",
        Visible="CountRows(" + OFFEN_F + ") > 1",
        DisplayMode="If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)",
        OnSelect="With({n: CountRows(" + OFFEN_F + ")},\n    Set(varOffenNr, If(Coalesce(varOffenNr, 1) >= n, 1, Coalesce(varOffenNr, 1) + 1))\n)"))
    aendern(st, p, "23.4", "btnRgAktion.OnSelect", lambda t: rep(
        t, 'TestDatensatz: StartsWith(ThisItem.Title, "ZZ Test")', "TestDatensatz: Coalesce(ThisItem.Testrundgang, false)"))
    return p


PAKETE = [paket1, paket2, paket3, paket4, paket5, paket6, paket7, paket8, paket9, paket10, paket19, paket20, paket21, paket22, paket12, paket16, paket14, paket17, paket13, paket23]


# ---------------------------------------------------------------- Prüfungen

BUILTINS = set("""If Set Not And Or CountRows Filter LookUp Sort SortByColumns First Last Coalesce IsBlank IsEmpty Blank Text
Value Trim Lower Upper Len Left Mid Right Split Concat ForAll Sequence Index Table ParseJSON JSON JSONFormat With Patch
Collect ClearCollect Clear Remove UpdateIf Distinct ShowColumns AddColumns DropColumns Notify NotificationType Navigate
ScreenTransition Refresh Concurrent IfError IsError Reset Select Launch Now Today DateAdd DateDiff DateValue TimeUnit
Switch Max Min Sum RoundDown Mod Defaults User GUID Substitute StartsWith Color ColorValue ColorFade RGBA DisplayMode
Font FontWeight Align Parent Self ThisItem ThisRecord true false Boolean StartOfWeek Weekday ISOWeekNum ImagePosition
Ungroup Date Number DateTime As in Compact Error Warning Success Information None Edit View Disabled White Semibold
Days Seconds Minutes Monday Fill Fit Large Thumbnail LayoutDirection LayoutOverflow Vertical Scroll DropShadow Light
Ascending Descending SortOrder Transparent Black Normal Bold Center Right Left Data LoadingSpinner Medium Small Full
VerticalAlign Top Bottom Char Abs Round FirstN Months ShortDate DateTimeFormat Launch Overflow Scroll""".split())


def addcolumns_namen(s):
    """Spaltennamen aus AddColumns(Tabelle, Name1, Ausdruck1, Name2, Ausdruck2, …)."""
    namen = set()
    for m in re.finditer(r"\bAddColumns\(", s):
        tiefe, start, args = 0, m.end(), []
        for j in range(m.end() - 1, len(s)):
            ch = s[j]
            if ch in "({[":
                tiefe += 1
            elif ch in ")}]":
                tiefe -= 1
                if tiefe == 0:
                    args.append(s[start:j])
                    break
            elif ch == "," and tiefe == 1:
                args.append(s[start:j])
                start = j + 1
        namen |= {a.strip() for a in args[1::2] if re.fullmatch(r"\s*\w+\s*", a)}
    return namen


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
    aliase = set(re.findall(r"\bAs\s+(\w+)", s)) | set(re.findall(r"\bAddColumns\(\s*\w+\s*,\s*(\w+)", s)) | addcolumns_namen(s)
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
            soll = 13 if "kritoffen" in stand.props["App.Formulas"] else 12
            if anz != soll:
                fehler += 1
                zeilen.append("  FEHLER fnFehlt mit %d statt %d Argumenten in %s" % (anz, soll, k))
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
        spaeter = {c["key"] for q in pakete[pakete.index(p) + 1:] for c in q["props"]}
        for name in p["neu"]:
            if stand.neue_controls[name][0] == "conKaKarte":
                pruefen += [(k, v) for k, v in stand.props.items() if k.startswith(name + ".") and k not in spaeter]
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
    ("btnStartOffenWeiter", "Weiter ›", 14, 120, 1, 20),
    ("lblStartOffen", "⚠  Nicht abgeschlossen: Infrastrukturrundgang TGI vom 02.11.2026  (2/5)", 14, 768 - 380, 2, 0),
    ("lblStartOffen", "⚠  Nicht abgeschlossen: Haustechnik Rundgang Lohfelden vom 02.11.2026", 14, 768 - 260, 2, 0),
    ("lblKaFrage", "ZZ Test Mängelarten  *  (mehrere möglich)", 17, 540, 1, 10),
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
