"""Rundgang-Builder: neue Canvas-App (Tablet quer 1366 x 768) aus Python-Bausteinen erzeugen und prüfen.

Aufruf: python3 -I werkzeuge/builder.py
Ergebnis: pakete/builder/ (YAML je Bildschirm, App.Formulas und App.OnStart deutsch) und
arbeit/2026-10-30_Builder/ (bloecke.json, pruefung.txt).
Formeln werden englisch geschrieben (YAML-Schreibweise) und für die Formelleiste nach deutsch übersetzt.
"""
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rg  # noqa: E402
from baukasten import textbreite  # noqa: E402

AUS_PAKET = os.path.join(rg.REPO, "pakete", "builder")
AUS_ARB = os.path.join(rg.REPO, "arbeit", "2026-10-30_Builder")

FONT = "Font.'Segoe UI'"
CUR = "LookUp(colP, ID = varAuswahlID)"
CURK = "LookUp(colK, ID = varAuswahlID)"
CURB = "LookUp(colB, ID = varAuswahlID)"
LOCK = "Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds))"
FREI = "!varIsLoading && Now() >= varSperreBis"
CHECK = ('Refresh(RG_Rundgaenge);\n'
         'Set(varEntwurfOk, varIstVorlage || Coalesce(LookUp(RG_Rundgaenge, ID = varRgID).EntwurfFassung, 0) = varFassung);\n'
         'If(!varEntwurfOk, Set(varSchreibbar, false); Notify("Dieser Entwurf ist nicht mehr offen (inzwischen aktiviert oder verworfen). Nichts wurde geändert. Bitte zur Übersicht.", NotificationType.Error))')
SICHER = " && RundgangID = varRgID && Fassung = varFassung"
EDIT = "If(varSchreibbar && !varIsLoading, DisplayMode.Edit, DisplayMode.View)"
BTN_DM = "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)"
NEU_SPALTEN = {
    "RG_Rundgaenge": {"Status": "Text", "Fassung": "Zahl", "EntwurfFassung": "Zahl", "EntwurfVon": "Text"},
    "RG_Bereiche": {"Fassung": "Zahl", "QuelleID": "Zahl"},
    "RG_Kategorien": {"RundgangID": "Zahl", "Fassung": "Zahl", "QuelleID": "Zahl"},
    "RG_Pruefpunkte": {"RundgangID": "Zahl", "Fassung": "Zahl", "QuelleID": "Zahl",
                       "Foto": "Auswahl", "KommentarPflicht": "Ja/Nein", "Grenzmodus": "Auswahl",
                       "BedingungPunkt": "Zahl", "BedingungWert": "Text", "HinweisBildID": "Zahl"},
}
AUSWAHL_SPALTEN = {"Eingabetyp", "Foto", "Grenzmodus"}
QUELLEN = ["RG_Rundgaenge", "RG_Bereiche", "RG_Kategorien", "RG_Pruefpunkte", "RG_Plan", "RG_Durchfuehrungen", "RG_Hinweisbilder"]

# ---------------------------------------------------------------- App.Formulas und App.OnStart

FORMULAS = r'''clrPrimaer = ColorValue("#171496");
clrPrimaerHell = ColorValue("#E8E8F7");
clrHintergrund = ColorValue("#F4F5F9");
clrKarte = Color.White;
clrRahmen = ColorValue("#DADCE5");
clrText = ColorValue("#1B1B1F");
clrTextGrau = ColorValue("#5F6370");
clrErfolg = ColorValue("#0F7B3F");
clrErfolgHell = ColorValue("#E3F4EA");
clrFehler = ColorValue("#B3261E");
clrFehlerHell = ColorValue("#FCE8E6");
clrWarnung = ColorValue("#9A5B00");
clrWarnungHell = ColorValue("#FFF4E0");
clrGesperrt = ColorValue("#9AA0A6");
clrGesperrtHell = ColorValue("#EEF0F3");
cfgBildBibliothek = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/RG_Hinweisbilder";
fnStatus(s: Text, aktiv: Boolean): Text = If(s = "Vorlage", "Vorlage", aktiv, "Aktiv", s = "Entwurf", "Entwurf", "Archiviert");
fnAktiveFassung(f: Number): Number = If(Coalesce(f, 0) > 0, f, 1);
fnTypName(t: Text): Text = Switch(t, "IONIO", "i.O. / n.i.O.", "ZAHL", "Zahl", "AUSWAHL", "Auswahl", "MEHRFACH", "Mehrfachauswahl", "TEXT", "Text", "DATUM", "Datum", "DATUMZEIT", "Datum + Uhrzeit", t);
fnTypKurz(t: Text): Text = Switch(t, "IONIO", "i.O./n.i.O.", "ZAHL", "Zahl", "AUSWAHL", "Auswahl", "MEHRFACH", "Mehrfach", "TEXT", "Text", "DATUM", "Datum", "DATUMZEIT", "Datum+Zeit", t);
fnFotoWert(f: Text, alt: Boolean): Text = If(f = "Aus" || f = "Optional" || f = "Pflicht" || f = "Bei Mangel Pflicht", f, alt, "Optional", "Aus");
fnFotoText(f: Text): Text = Switch(f, "Optional", "Foto freiwillig", "Pflicht", "Foto immer Pflicht", "Bei Mangel Pflicht", "Foto Pflicht bei Mangel", "kein Foto (bei n.i.O. möglich)");
fnGrenzmodus(g: Text): Text = If(g = "Warnen" || g = "Sperren", g, "Mangel");
fnGrenzText(mi: Number, ma: Number, einheit: Text): Text = If(IsBlank(mi) && IsBlank(ma), "keine Grenzen", "i.O. " & If(IsBlank(mi), "", "ab " & Text(mi)) & If(IsBlank(mi) || IsBlank(ma), "", " ") & If(IsBlank(ma), "", "bis " & Text(ma)) & If(Trim(Coalesce(einheit, "")) = "", "", " " & einheit));
fnWerte(t: Text): Number = CountRows(Filter(Split(Coalesce(t, ""), ";") As s, Trim(s.Value) <> ""));
fnWerteDoppelt(t: Text): Boolean = CountRows(Distinct(Filter(Split(Coalesce(t, ""), ";") As s, Trim(s.Value) <> ""), Lower(Trim(Value)))) < fnWerte(t);
fnBedNorm(w: Text): Text = Lower(Substitute(Substitute(Trim(Coalesce(w, "")), ".", ""), " ", ""));
fnBedGueltig(w: Text, typ: Text, auswahl: Text): Boolean = With({n: fnBedNorm(w)}, n = "*" || ((typ = "IONIO" || typ = "ZAHL") && (n = "io" || n = "nio")) || ((typ = "AUSWAHL" || typ = "MEHRFACH") && CountRows(Filter(Split(auswahl, ";") As s, fnBedNorm(s.Value) = n)) > 0));
fnBedText(w: Text): Text = Switch(fnBedNorm(w), "nio", "n.i.O. (Mangel)", "io", "i.O.", "*", "beantwortet", Trim(Coalesce(w, "")));
fnWochentag(n: Number): Text = Switch(n, 1, "Montag", 2, "Dienstag", 3, "Mittwoch", 4, "Donnerstag", 5, "Freitag", 6, "Samstag", 7, "Sonntag", "?");
fnZyklus(z: Number): Text = If(Coalesce(z, 1) <= 1, "jede Woche", "alle " & z & " Wochen");
fnMontag(d: Date): DateTime = DateAdd(d, 1 - Weekday(d, StartOfWeek.Monday), TimeUnit.Days);
fnPlanPasst(start: DateTime, bis: DateTime, wt: Number, zyklus: Number, d: Date): Boolean = With({t: DateDiff(start, d, TimeUnit.Days)}, !IsBlank(start) && Weekday(d, StartOfWeek.Monday) = wt && t >= 0 && (IsBlank(bis) || DateDiff(d, bis, TimeUnit.Days) >= 0) && Mod(RoundDown(t / 7, 0), Max(1, zyklus)) = 0);'''

ONSTART_VARS = [
    ("varIsLoading", "false"), ("varLadeText", '""'), ("varSperreBis", "Now()"), ("varPatchFehler", "false"),
    ("varJob", '""'), ("varNach", '""'), ("varKopieNach", '""'), ("varArbeitStart", "false"),
    ("varRgID", "0"), ("varRg", "Defaults(RG_Rundgaenge)"), ("varFassung", "0"), ("varSchreibbar", "false"),
    ("varIstVorlage", "false"), ("varAuswahlEbene", "0"), ("varAuswahlID", "0"), ("varCtxB", "0"), ("varCtxK", "0"),
    ("varFrage", '""'), ("varGespeichertText", '""'), ("varAlleZeigen", "false"), ("varNeuOffen", "false"),
    ("varNeuLeer", "true"), ("varNeuRg", "Defaults(RG_Rundgaenge)"), ("varNeuID", "0"), ("varHolenOffen", "false"),
    ("varHolenEbene", "0"), ("varHolenID", "0"), ("varMehrereOffen", "false"), ("varMehrTyp", '"IONIO"'),
    ("varMehrPflicht", "true"), ("varBildOffen", "false"), ("varAktivOffen", "false"), ("varZielR", "0"),
    ("varZielF", "0"), ("varZielB", "0"), ("varZielK", "0"), ("varZielBAktiv", "false"), ("varKopieBehalteR", "false"),
    ("varKopieZusatz", '""'), ("varKopieFehler", "0"), ("varQuelleR", "0"), ("varQuelleF", "0"),
    ("varQuelleNurAktiv", "false"), ("varHeuteLaeuft", "false"), ("varPlanRgID", "0"),
    ("varPlanRg", "Defaults(RG_Rundgaenge)"), ("varEntwurfOk", "true"), ("varAktivRest", "false"), ("varVorlageNeu", "Defaults(RG_Rundgaenge)"),
]
ONSTART = ";\n".join("Set(%s, %s)" % kv for kv in ONSTART_VARS)

# ---------------------------------------------------------------- Bausteine (Formeln)


def sel(e, i, b, k):
    """Auswahl in der Gliederung setzen und Eingaben zurücksetzen."""
    return ("Set(varAuswahlEbene, {e});\nSet(varAuswahlID, {i});\nSet(varCtxB, {b});\nSet(varCtxK, {k});\nSet(varFrage, \"\");\n"
            "Reset(txtBName);\nReset(txtKName);\nReset(ddKBereich);\nReset(txtPFrage);\nReset(txtPEinheit);\nReset(txtPMin);\n"
            "Reset(txtPMax);\nReset(txtPWerte);\nReset(txtPHinweis);\nReset(ddPKategorie);\nReset(ddPBedA);\nReset(ddPBedW)").format(e=e, i=i, b=b, k=k)


def patch_feld(ds, col, felder, idx="varAuswahlID"):
    """Ein Feld eines Datensatzes im Entwurf speichern (frisch gelesen) und die Sammlung nachziehen."""
    e = {"RG_Bereiche": "1", "RG_Kategorien": "2", "RG_Pruefpunkte": "3"}[ds]
    return ("If(varSchreibbar && varAuswahlEbene = " + e + ",\n"
            "    " + CHECK.replace("\n", "\n    ") + ";\n"
            "    If(varEntwurfOk,\n"
            "        Set(varPatchFehler, false);\n"
            "        IfError(Patch(DS, LookUp(DS, ID = IDX" + SICHER + "), FELDER), Set(varPatchFehler, true));\n"
            "        If(varPatchFehler,\n"
            "            Notify(\"Nicht gespeichert. Bitte erneut versuchen.\", NotificationType.Error),\n"
            "            Patch(COL, LookUp(COL, ID = IDX), LookUp(DS, ID = IDX));\n"
            "            Set(varGespeichertText, \"Gespeichert \" & Text(Now(), \"hh:mm:ss\"))\n"
            "        )\n"
            "    )\n"
            ")").replace("FELDER", felder).replace("DS", ds).replace("COL", col).replace("IDX", idx)


def laden_baum(ziel_b="colB", ziel_k="colK", ziel_p="colP", r="varRgID", f="varFassung"):
    return ("Concurrent(\n"
            "    ClearCollect({b}, Filter(RG_Bereiche, RundgangID = {r} && Fassung = {f})),\n"
            "    ClearCollect({k}, Filter(RG_Kategorien, RundgangID = {r} && Fassung = {f})),\n"
            "    ClearCollect({p}, Filter(RG_Pruefpunkte, RundgangID = {r} && Fassung = {f}))\n"
            ")").format(b=ziel_b, k=ziel_k, p=ziel_p, r=r, f=f)


def nur_aktive(b, k, p):
    return ("RemoveIf({b}, !Coalesce(Aktiv, false));\nRemoveIf({k}, !Coalesce(Aktiv, false));\nRemoveIf({p}, !Coalesce(Aktiv, false));\n"
            "RemoveIf({k}, IsBlank(LookUp({b} As b0, b0.ID = BereichID)));\n"
            "RemoveIf({p}, IsBlank(LookUp({k} As k0, k0.ID = KategorieID)))").format(b=b, k=k, p=p)


ORD = "RgReihenfolge * 1000000 + ID"

NEUER_PUNKT = ('Aktiv: true, QuelleID: 0, Eingabetyp: {{Value: {typ}}}, Pflicht: {pfl}, Auswahlwerte: "", Einheit: "", Hinweis: "", '
               'FotoMoeglich: false, Foto: {{Value: "Aus"}}, KommentarPflicht: false, Grenzmodus: {{Value: "Mangel"}}, '
               'BedingungPunkt: 0, BedingungWert: "", HinweisBildID: 0')


def quelle_laden(s):
    """Quell-Rundgang für „Holen“ in colSrcB/K/P laden (s = Datensatz aus colRg)."""
    return ("With({{s: {s}}},\n"
            "    With({{f: If(fnStatus(s.Status, s.Aktiv) = \"Entwurf\" || fnStatus(s.Status, s.Aktiv) = \"Vorlage\", Coalesce(s.EntwurfFassung, 1), fnAktiveFassung(s.Fassung)), "
            "nur: !(fnStatus(s.Status, s.Aktiv) = \"Entwurf\" || fnStatus(s.Status, s.Aktiv) = \"Vorlage\")}},\n"
            "        Concurrent(\n"
            "            ClearCollect(colSrcB, Filter(RG_Bereiche, RundgangID = s.ID && Fassung = f)),\n"
            "            ClearCollect(colSrcK, Filter(RG_Kategorien, RundgangID = s.ID && Fassung = f)),\n"
            "            ClearCollect(colSrcP, Filter(RG_Pruefpunkte, RundgangID = s.ID && Fassung = f))\n"
            "        );\n"
            "        If(nur,\n"
            "            RemoveIf(colSrcB, !Coalesce(Aktiv, false));\n"
            "            RemoveIf(colSrcK, !Coalesce(Aktiv, false));\n"
            "            RemoveIf(colSrcP, !Coalesce(Aktiv, false))\n"
            "        )\n"
            "    )\n"
            ");\n"
            "Set(varHolenEbene, 0);\n"
            "Set(varHolenID, 0)").format(s=s)


def baum_items(b, k, p, nur_offen):
    """Gliederung als flache Tabelle: Bereich (1), Kategorie (2), Prüfpunkt (3), sortiert über einen Textschlüssel."""
    pf = 'Filter({p}, KategorieID = varCtxK)'.format(p=p) if nur_offen else p
    return ("Sort(\n"
            "    Ungroup(\n"
            "        Table(\n"
            "            {{T: ForAll({b} As b, {{Ebene: 1, ID: b.ID, BerID: b.ID, KatID: 0, Titel: b.Title, Info: \"\", "
            "Schl: Text(b.RgReihenfolge, \"000000\") & Text(b.ID, \"000000\")}})}},\n"
            "            {{T: ForAll({k} As k, With({{b: LookUp({b} As b1, b1.ID = k.BereichID)}}, {{Ebene: 2, ID: k.ID, BerID: k.BereichID, KatID: k.ID, Titel: k.Title, "
            "Info: Text(CountRows(Filter({p} As p1, p1.KategorieID = k.ID))), "
            "Schl: Text(b.RgReihenfolge, \"000000\") & Text(b.ID, \"000000\") & Text(k.RgReihenfolge, \"000000\") & Text(k.ID, \"000000\")}}))}},\n"
            "            {{T: ForAll({pf} As p, With({{k: LookUp({k} As k1, k1.ID = p.KategorieID)}}, With({{b: LookUp({b} As b2, b2.ID = k.BereichID)}}, "
            "{{Ebene: 3, ID: p.ID, BerID: k.BereichID, KatID: p.KategorieID, Titel: p.Title, Info: fnTypKurz(p.Eingabetyp.Value), "
            "Schl: Text(b.RgReihenfolge, \"000000\") & Text(b.ID, \"000000\") & Text(k.RgReihenfolge, \"000000\") & Text(k.ID, \"000000\") & "
            "Text(p.RgReihenfolge, \"000000\") & Text(p.ID, \"000000\")}})))}}\n"
            "        ),\n"
            "        T\n"
            "    ),\n"
            "    Schl\n"
            ")").format(b=b, k=k, p=p, pf=pf)


def zweimal(schluessel, aktion, sperre=True):
    """Bestätigung durch zweites Tippen, mit 1-s-Sperre gegen Doppelklick."""
    return ("If({frei},\n"
            "    If(varFrage <> {s},\n"
            "        Set(varFrage, {s});\n"
            "        {lock},\n"
            "        Set(varFrage, \"\");\n"
            "        {a}\n"
            "    )\n"
            ")").format(frei=FREI, s=schluessel, lock=LOCK, a=aktion)


# ---------------------------------------------------------------- Arbeits-Zeitgeber (alle längeren Abläufe)

STUFE_VORBEREITEN = '''If(varJob = "vorbereiten",
    Set(varLadeText, "Rundgang wird für den Builder vorbereitet …");
    Concurrent(Refresh(RG_Rundgaenge), Refresh(RG_Bereiche), Refresh(RG_Kategorien), Refresh(RG_Pruefpunkte));
    Set(varRg, LookUp(RG_Rundgaenge, ID = varRgID));
    ClearCollect(colVbB, Filter(RG_Bereiche, RundgangID = varRgID));
    Clear(colVbK);
    ForAll(colVbB As b, Collect(colVbK, Filter(RG_Kategorien, BereichID = b.ID)));
    Clear(colVbP);
    ForAll(colVbK As k, Collect(colVbP, Filter(RG_Pruefpunkte, KategorieID = k.ID)));
    ClearCollect(colVbErg, ForAll(Filter(colVbB, IsBlank(Fassung)) As b, {Ok: !IsError(Patch(RG_Bereiche, LookUp(RG_Bereiche, ID = b.ID), {Fassung: 1, QuelleID: 0}))}));
    Collect(colVbErg, ForAll(Filter(colVbK, IsBlank(Fassung) || IsBlank(RundgangID)) As k, {Ok: !IsError(Patch(RG_Kategorien, LookUp(RG_Kategorien, ID = k.ID), {Fassung: 1, RundgangID: varRgID, QuelleID: 0}))}));
    Collect(colVbErg, ForAll(Filter(colVbP, IsBlank(Fassung) || IsBlank(RundgangID)) As p, {Ok: !IsError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = p.ID), {Fassung: 1, RundgangID: varRgID, QuelleID: 0}))}));
    Set(varPatchFehler, CountRows(Filter(colVbErg, !Ok)) > 0);
    If(!varPatchFehler,
        IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varRgID), {Fassung: 1, EntwurfFassung: 0, EntwurfVon: "", Status: If(Coalesce(varRg.Aktiv, false), "Aktiv", "Archiviert")}), Set(varPatchFehler, true))
    );
    If(varPatchFehler,
        Notify("Vorbereiten unvollständig. Bitte den Rundgang erneut öffnen (das ist gefahrlos).", NotificationType.Error);
        Set(varJob, "zurueck"),
        Set(varFassung, 1);
        Set(varJob, varNach);
        Set(varNach, "")
    )
);
'''

STUFE_NEUE_FASSUNG = '''If(varJob = "neueFassung",
    Set(varLadeText, "Neue Fassung wird angelegt …");
    Concurrent(Refresh(RG_Rundgaenge), Refresh(RG_Bereiche), Refresh(RG_Kategorien), Refresh(RG_Pruefpunkte));
    Set(varRg, LookUp(RG_Rundgaenge, ID = varRgID));
    If(Coalesce(varRg.EntwurfFassung, 0) > 0,
        Set(varFassung, varRg.EntwurfFassung);
        Set(varSchreibbar, true);
        Notify("Es gibt schon einen Entwurf – er wird geöffnet.", NotificationType.Information);
        Set(varJob, "laden"),
        ClearCollect(colAlleB, Filter(RG_Bereiche, RundgangID = varRgID));
        Set(varZielF, Max(Coalesce(Max(colAlleB, Coalesce(Fassung, 0)), 0), Coalesce(First(Sort(Filter(RG_Kategorien, RundgangID = varRgID), Fassung, SortOrder.Descending)).Fassung, 0), Coalesce(First(Sort(Filter(RG_Pruefpunkte, RundgangID = varRgID), Fassung, SortOrder.Descending)).Fassung, 0), fnAktiveFassung(varRg.Fassung)) + 1);
        Set(varPatchFehler, false);
        IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varRgID), {EntwurfFassung: varZielF, EntwurfVon: User().FullName}), Set(varPatchFehler, true));
        If(varPatchFehler,
            Notify("Die neue Fassung konnte nicht angelegt werden. Bitte erneut versuchen.", NotificationType.Error);
            Set(varJob, "zurueck"),
            ClearCollect(colQB, Filter(colAlleB, Coalesce(Fassung, 0) = fnAktiveFassung(varRg.Fassung)));
            ClearCollect(colQK, Filter(RG_Kategorien, RundgangID = varRgID && Fassung = fnAktiveFassung(varRg.Fassung)));
            ClearCollect(colQP, Filter(RG_Pruefpunkte, RundgangID = varRgID && Fassung = fnAktiveFassung(varRg.Fassung)));
            ''' + nur_aktive("colQB", "colQK", "colQP").replace("\n", "\n            ") + ''';
            Set(varZielR, varRgID);
            Set(varZielB, 0);
            Set(varZielK, 0);
            Set(varZielBAktiv, false);
            Set(varKopieBehalteR, true);
            Set(varKopieZusatz, "");
            Set(varFassung, varZielF);
            Set(varSchreibbar, true);
            Set(varKopieNach, "laden");
            Set(varJob, "kopie")
        )
    )
);
'''

STUFE_QUELLE = '''If(varJob = "quelle",
    Set(varLadeText, "Rundgang wird kopiert …");
    ''' + laden_baum("colQB", "colQK", "colQP", "varQuelleR", "varQuelleF").replace("\n", "\n    ") + ''';
    If(varQuelleNurAktiv,
        ''' + nur_aktive("colQB", "colQK", "colQP").replace("\n", "\n        ") + '''
    );
    Set(varZielB, 0);
    Set(varZielK, 0);
    Set(varZielBAktiv, false);
    Set(varKopieBehalteR, true);
    Set(varKopieZusatz, "");
    Set(varKopieNach, "laden");
    Set(varJob, "kopie")
);
'''

STUFE_KOPIE = '''If(varJob = "kopie",
    Set(varLadeText, "Wird kopiert …");
    ClearCollect(colMapB,
        With({qs: Sort(colQB, RgReihenfolge * 1000000 + ID)},
            ForAll(Sequence(CountRows(qs)) As i,
                With({q: Index(qs, i.Value)},
                    {Alt: q.ID,
                     Neu: IfError(Patch(RG_Bereiche, Defaults(RG_Bereiche), {Title: Left(q.Title & varKopieZusatz, 255), RundgangID: varZielR, Fassung: varZielF, RgReihenfolge: If(varKopieBehalteR, q.RgReihenfolge, Coalesce(Max(colB, RgReihenfolge), 0) + i.Value * 10), Hinweis: q.Hinweis, Aktiv: varZielBAktiv, QuelleID: q.ID}).ID, 0)}
                )
            )
        )
    );
    ClearCollect(colMapK,
        With({qs: Sort(colQK, RgReihenfolge * 1000000 + ID)},
            ForAll(Sequence(CountRows(qs)) As i,
                With({q: Index(qs, i.Value)},
                    With({ziel: If(IsEmpty(colQB), varZielB, Coalesce(LookUp(colMapB, Alt = q.BereichID).Neu, 0))},
                        {Alt: q.ID,
                         Neu: If(ziel = 0, 0, IfError(Patch(RG_Kategorien, Defaults(RG_Kategorien), {Title: Left(q.Title & If(IsEmpty(colQB), varKopieZusatz, ""), 255), BereichID: ziel, RundgangID: varZielR, Fassung: varZielF, RgReihenfolge: If(!IsEmpty(colQB) || varKopieBehalteR, q.RgReihenfolge, Coalesce(Max(Filter(colK, BereichID = varZielB), RgReihenfolge), 0) + i.Value * 10), Hinweis: q.Hinweis, Aktiv: true, QuelleID: q.ID}).ID, 0))}
                    )
                )
            )
        )
    );
    ClearCollect(colMapP,
        With({qs: Sort(colQP, RgReihenfolge * 1000000 + ID)},
            ForAll(Sequence(CountRows(qs)) As i,
                With({q: Index(qs, i.Value)},
                    With({ziel: If(IsEmpty(colQK), varZielK, Coalesce(LookUp(colMapK, Alt = q.KategorieID).Neu, 0))},
                        {Alt: q.ID, BedAlt: Coalesce(q.BedingungPunkt, 0), BedWert: Coalesce(q.BedingungWert, ""), Ziel: ziel,
                         Neu: If(ziel = 0, 0, IfError(Patch(RG_Pruefpunkte, Defaults(RG_Pruefpunkte), {Title: Left(q.Title & If(IsEmpty(colQK), varKopieZusatz, ""), 255), KategorieID: ziel, RundgangID: varZielR, Fassung: varZielF, RgReihenfolge: If(!IsEmpty(colQK) || varKopieBehalteR, q.RgReihenfolge, Coalesce(Max(Filter(colP, KategorieID = varZielK), RgReihenfolge), 0) + i.Value * 10), Aktiv: true, QuelleID: q.ID, Eingabetyp: {Value: Coalesce(q.Eingabetyp.Value, "IONIO")}, Pflicht: Coalesce(q.Pflicht, false), Auswahlwerte: q.Auswahlwerte, Einheit: q.Einheit, MinWert: q.MinWert, MaxWert: q.MaxWert, Hinweis: q.Hinweis, FotoMoeglich: Coalesce(q.FotoMoeglich, false), Foto: {Value: fnFotoWert(q.Foto.Value, Coalesce(q.FotoMoeglich, false))}, KommentarPflicht: Coalesce(q.KommentarPflicht, false), Grenzmodus: {Value: fnGrenzmodus(q.Grenzmodus.Value)}, BedingungPunkt: 0, BedingungWert: "", HinweisBildID: Coalesce(q.HinweisBildID, 0)}).ID, 0))}
                    )
                )
            )
        )
    );
    ClearCollect(colBedErg,
        ForAll(Filter(colMapP, BedAlt <> 0 && Neu <> 0) As m,
            With({a: LookUp(colMapP As m2, m2.Alt = m.BedAlt)},
                With({neuA: If(!IsBlank(a) && a.Ziel = m.Ziel, a.Neu, IsBlank(a) && LookUp(colP As p0, p0.ID = m.BedAlt).KategorieID = m.Ziel, m.BedAlt, 0)},
                    {Ok: If(neuA = 0, true, !IsError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = m.Neu), {BedingungPunkt: neuA, BedingungWert: m.BedWert})))}
                )
            )
        )
    );
    Set(varKopieFehler, CountRows(Filter(colMapB, Neu = 0)) + CountRows(Filter(colMapK, Neu = 0)) + CountRows(Filter(colMapP, Neu = 0)) + CountRows(Filter(colBedErg, !Ok)));
    If(varKopieFehler > 0 && varKopieNach = "laden",
        If(Coalesce(LookUp(RG_Rundgaenge, ID = varZielR).Fassung, 0) = 0 || varZielF <> fnAktiveFassung(LookUp(RG_Rundgaenge, ID = varZielR).Fassung),
            Remove(RG_Pruefpunkte, Filter(RG_Pruefpunkte, RundgangID = varZielR && Fassung = varZielF));
            Remove(RG_Kategorien, Filter(RG_Kategorien, RundgangID = varZielR && Fassung = varZielF));
            Remove(RG_Bereiche, Filter(RG_Bereiche, RundgangID = varZielR && Fassung = varZielF))
        );
        If(Coalesce(LookUp(RG_Rundgaenge, ID = varZielR).Fassung, 0) > 0 && varZielF <> fnAktiveFassung(LookUp(RG_Rundgaenge, ID = varZielR).Fassung),
            IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varZielR), {EntwurfFassung: 0, EntwurfVon: ""}), Set(varPatchFehler, true))
        );
        Notify("Kopieren fehlgeschlagen (" & varKopieFehler & " Teile fehlen). Der Entwurf wurde zurückgenommen. Bitte erneut versuchen.", NotificationType.Error);
        Set(varJob, "zurueck"),
        varKopieFehler > 0,
        Notify("Kopieren unvollständig: " & varKopieFehler & " Teile fehlen. Bitte die Gliederung prüfen.", NotificationType.Error);
        Set(varJob, varKopieNach),
        Notify("Kopiert: " & CountRows(colMapP) & " Prüfpunkte.", NotificationType.Success);
        Set(varJob, varKopieNach)
    )
);
'''

STUFE_LADEN = '''If(varJob = "laden",
    Set(varLadeText, "Rundgang wird geladen …");
    Concurrent(Refresh(RG_Rundgaenge), Refresh(RG_Bereiche), Refresh(RG_Kategorien), Refresh(RG_Pruefpunkte), Refresh(RG_Plan));
    Set(varRg, LookUp(RG_Rundgaenge, ID = varRgID));
    Set(varIstVorlage, fnStatus(varRg.Status, varRg.Aktiv) = "Vorlage");
    ''' + laden_baum().replace("\n", "\n    ") + ''';
    ClearCollect(colPlanR, Filter(RG_Plan, RundgangID = varRgID));
    Set(varAktivRest, false);
    If(varSchreibbar && !varIstVorlage && Coalesce(varRg.EntwurfFassung, 0) <> varFassung,
        Set(varSchreibbar, false);
        Notify("Dieser Entwurf ist nicht mehr offen. Er wird nur zum Lesen gezeigt.", NotificationType.Warning)
    );
    If(varSchreibbar && !varIstVorlage && CountRows(Filter(colB, Coalesce(Aktiv, false))) > 0,
        Set(varSchreibbar, false);
        Set(varAktivRest, true);
        Notify("Das Aktivieren dieser Fassung ist unvollständig. Bitte oben „Aktivieren …“ erneut tippen.", NotificationType.Error)
    );
    If(!varSchreibbar && !varAktivRest,
        ''' + nur_aktive("colB", "colK", "colP").replace("\n", "\n        ") + '''
    );
    Set(varGespeichertText, "");
    With({b1: First(Sort(colB, RgReihenfolge * 1000000 + ID))},
        If(IsBlank(b1),
            ''' + sel("0", "0", "0", "0").replace("\n", "\n            ") + ''',
            ''' + sel("1", "b1.ID", "b1.ID", "0").replace("\n", "\n            ") + '''
        )
    );
    Set(varJob, "")
);
'''

STUFE_AUSWAHL = '''If(varJob = "auswahl",
    ''' + laden_baum().replace("\n", "\n    ") + ''';
    If(!IsEmpty(colQB),
        With({n: First(colMapB).Neu}, If(n > 0, ''' + sel("1", "n", "n", "0").replace("\n", " ") + ''')),
        !IsEmpty(colQK),
        With({n: First(colMapK).Neu}, If(n > 0, ''' + sel("2", "n", "varZielB", "n").replace("\n", " ") + ''')),
        With({n: First(colMapP).Neu}, If(n > 0, ''' + sel("3", "n", "LookUp(colK, ID = varZielK).BereichID", "varZielK").replace("\n", " ") + '''))
    );
    Set(varJob, "")
);
'''

STUFE_AKTIVIEREN = '''If(varJob = "aktivieren",
    Set(varLadeText, "Fassung wird aktiviert …");
    Concurrent(Refresh(RG_Rundgaenge), Refresh(RG_Bereiche), Refresh(RG_Kategorien));
    Set(varRg, LookUp(RG_Rundgaenge, ID = varRgID));
    If(Coalesce(varRg.EntwurfFassung, 0) <> varFassung,
        Notify("Dieser Entwurf wurde inzwischen schon aktiviert oder verworfen. Die Übersicht wird neu geladen.", NotificationType.Error);
        Set(varJob, "zurueck"),
        ClearCollect(colAktB, Filter(RG_Bereiche, RundgangID = varRgID));
        ClearCollect(colAktK, Filter(RG_Kategorien, RundgangID = varRgID));
        ClearCollect(colAltB, Filter(colAktB, Coalesce(Aktiv, false) && Coalesce(Fassung, 0) <> varFassung));
        ClearCollect(colAltK, Filter(colAktK, Coalesce(Aktiv, false) && Coalesce(Fassung, 0) <> varFassung));
        ClearCollect(colNeuB, Filter(colAktB, Coalesce(Fassung, 0) = varFassung));
        ClearCollect(colAktErg, ForAll(colAltB As b, {Ok: !IsError(Patch(RG_Bereiche, LookUp(RG_Bereiche, ID = b.ID), {Aktiv: false}))}));
        Collect(colAktErg, ForAll(colAltK As k, {Ok: !IsError(Patch(RG_Kategorien, LookUp(RG_Kategorien, ID = k.ID), {Aktiv: false}))}));
        Set(varPatchFehler, CountRows(Filter(colAktErg, !Ok)) > 0);
        If(!varPatchFehler,
            Collect(colAktErg, ForAll(colNeuB As b, {Ok: !IsError(Patch(RG_Bereiche, LookUp(RG_Bereiche, ID = b.ID), {Aktiv: true}))}));
            Set(varPatchFehler, CountRows(Filter(colAktErg, !Ok)) > 0)
        );
        Refresh(RG_Bereiche);
        ClearCollect(colAktB, Filter(RG_Bereiche, RundgangID = varRgID));
        If(!varPatchFehler && CountRows(Filter(colAktB, Coalesce(Aktiv, false) && Coalesce(Fassung, 0) <> varFassung)) = 0 && CountRows(Filter(colAktB, Coalesce(Aktiv, false) && Coalesce(Fassung, 0) = varFassung)) = CountRows(colNeuB),
            IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varRgID), {Fassung: varFassung, EntwurfFassung: 0, EntwurfVon: "", Status: "Aktiv", Aktiv: true}), Set(varPatchFehler, true)),
            Set(varPatchFehler, true)
        );
        If(varPatchFehler,
            Notify("Aktivieren unvollständig. Bitte noch einmal „Aktivieren …“ tippen – das ist gefahrlos.", NotificationType.Error);
            Set(varSchreibbar, false);
            Set(varAktivRest, true);
            Set(varJob, ""),
            Notify("Fassung " & varFassung & " ist aktiv. Laufende Rundgänge von heute werden mit der alten Fassung beendet.", NotificationType.Success);
            Set(varJob, "zurueck")
        )
    )
);
'''

STUFE_ZURUECK = '''If(varJob = "zurueck",
    Set(varJob, "");
    Set(varIsLoading, false);
    Navigate(scrListe, ScreenTransition.None)
);
Set(varIsLoading, false)'''

TIMER_ARBEIT = ("Set(varArbeitStart, false);\nSet(varIsLoading, true);\n" + STUFE_VORBEREITEN + STUFE_NEUE_FASSUNG + STUFE_QUELLE
                + STUFE_KOPIE + STUFE_LADEN + STUFE_AUSWAHL + STUFE_AKTIVIEREN + STUFE_ZURUECK)

# ---------------------------------------------------------------- Prüfregeln (Items von galPr)


def regel(art, ebene, id_, kat, ber, text):
    return '{{Art: "{a}", Ebene: {e}, ID: {i}, KatID: {k}, BerID: {b}, Text: {t}}}'.format(a=art, e=ebene, i=id_, k=kat, b=ber, t=text)


BER_VON_P = "LookUp(colK As k9, k9.ID = p.KategorieID).BereichID"
P_REGEL = lambda art, text: regel(art, 3, "p.ID", "p.KategorieID", BER_VON_P, text)  # noqa: E731

REGELN = [
    'Filter(Table(' + regel("Fehler", 0, 0, 0, 0, '"Der Rundgang hat noch keinen Bereich. → „+ Bereich“"') + '), IsEmpty(colB))',
    'ForAll(Filter(colB As b, IsEmpty(Filter(colK As k, k.BereichID = b.ID))) As b, ' + regel("Fehler", 1, "b.ID", 0, "b.ID", '"Bereich „" & b.Title & "“ hat keine Kategorie."') + ')',
    'ForAll(Filter(colK As k, IsEmpty(Filter(colP As p, p.KategorieID = k.ID))) As k, ' + regel("Fehler", 2, "k.ID", "k.ID", "k.BereichID", '"Kategorie „" & k.Title & "“ hat keinen Prüfpunkt."') + ')',
    'ForAll(Filter(colB As b, Trim(Coalesce(b.Title, "")) = "") As b, ' + regel("Fehler", 1, "b.ID", 0, "b.ID", '"Ein Bereich hat keinen Namen."') + ')',
    'ForAll(Filter(colK As k, Trim(Coalesce(k.Title, "")) = "") As k, ' + regel("Fehler", 2, "k.ID", "k.ID", "k.BereichID", '"Eine Kategorie hat keinen Namen."') + ')',
    'ForAll(Filter(colP As p, Trim(Coalesce(p.Title, "")) = "") As p, ' + P_REGEL("Fehler", '"Ein Prüfpunkt hat keine Frage."') + ')',
    'ForAll(Filter(colP As p, (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerte(p.Auswahlwerte) < 2) As p, '
    + P_REGEL("Fehler", '"„" & p.Title & "“: mindestens zwei Antwortmöglichkeiten eintragen."') + ')',
    'ForAll(Filter(colP As p, (p.Eingabetyp.Value = "AUSWAHL" || p.Eingabetyp.Value = "MEHRFACH") && fnWerteDoppelt(p.Auswahlwerte)) As p, '
    + P_REGEL("Fehler", '"„" & p.Title & "“: eine Antwortmöglichkeit steht doppelt da."') + ')',
    'ForAll(Filter(colP As p, p.Eingabetyp.Value = "ZAHL" && !IsBlank(p.MinWert) && !IsBlank(p.MaxWert) && p.MinWert > p.MaxWert) As p, '
    + P_REGEL("Fehler", '"„" & p.Title & "“: „ab“ ist größer als „bis“."') + ')',
    'ForAll(Filter(ForAll(Filter(colP As p0, Coalesce(p0.BedingungPunkt, 0) <> 0) As p, With({a: LookUp(colP As a0, a0.ID = p.BedingungPunkt)}, '
    '{ID: p.ID, KategorieID: p.KategorieID, Title: p.Title, G: If(IsBlank(a) || a.KategorieID <> p.KategorieID, "Die Bedingung zeigt auf eine Frage außerhalb dieser Kategorie.", '
    'Coalesce(a.BedingungPunkt, 0) <> 0, "Die Frage der Bedingung hat selbst eine Bedingung (nur eine Ebene erlaubt).", '
    'a.RgReihenfolge * 1000000 + a.ID > p.RgReihenfolge * 1000000 + p.ID, "Die Frage der Bedingung muss weiter oben stehen.", '
    '!fnBedGueltig(p.BedingungWert, a.Eingabetyp.Value, a.Auswahlwerte), "Der Wert der Bedingung passt nicht zu „" & a.Title & "“.", "")})), G <> "") As p, '
    + P_REGEL("Fehler", '"„" & p.Title & "“: " & p.G') + ')',
    'ForAll(Filter(colP As p, p.Eingabetyp.Value = "ZAHL" && fnGrenzmodus(p.Grenzmodus.Value) <> "Mangel" && IsBlank(p.MinWert) && IsBlank(p.MaxWert)) As p, '
    + P_REGEL("Hinweis", '"„" & p.Title & "“: „Außerhalb“ wirkt nur mit Grenzen (ab/bis)."') + ')',
    'ForAll(Filter(colP As p, p.Foto.Value = "Bei Mangel Pflicht" && p.Eingabetyp.Value <> "IONIO" && p.Eingabetyp.Value <> "ZAHL") As p, '
    + P_REGEL("Hinweis", '"„" & p.Title & "“: „Foto Pflicht bei Mangel“ wirkt nur bei i.O./n.i.O. und Zahl."') + ')',
    'ForAll(Filter(colP As p, CountRows(Filter(colP As q, q.KategorieID = p.KategorieID && Lower(Trim(q.Title)) = Lower(Trim(p.Title)))) > 1) As p, '
    + P_REGEL("Hinweis", '"„" & p.Title & "“ steht in der Kategorie doppelt."') + ')',
    'ForAll(Filter(colP As p, p.Title = "Neue Frage") As p, ' + P_REGEL("Hinweis", '"Eine Frage heißt noch „Neue Frage“."') + ')',
    'ForAll(Filter(colK As k, CountRows(Filter(colP As p, p.KategorieID = k.ID)) > 30) As k, '
    + regel("Hinweis", 2, "k.ID", "k.ID", "k.BereichID", '"Kategorie „" & k.Title & "“ hat über 30 Prüfpunkte (lange Seite für den Prüfer)."') + ')',
    'Filter(Table(' + regel("Hinweis", 0, 0, 0, 0, '"Kein aktiver Plan: Der Rundgang erscheint nie auf der Startseite. → In der Übersicht „Plan“ tippen."')
    + '), !varIstVorlage && IsEmpty(Filter(colPlanR, Coalesce(Aktiv, false))))',
]

PRUEF_ITEMS = ("Sort(\n    Ungroup(\n        Table(\n" + ",\n".join("            {T: " + r + "}" for r in REGELN)
               + "\n        ),\n        T\n    ),\n    If(Art = \"Fehler\", 0, 1)\n)")
FEHLER_ANZ = 'CountRows(Filter(galPr.AllItems, Art = "Fehler"))'
HINWEIS_ANZ = 'CountRows(Filter(galPr.AllItems, Art = "Hinweis"))'

# Änderungsübersicht (Aktivieren)
P_GEAENDERT = ('p.Title <> a.Title || Coalesce(p.Eingabetyp.Value, "") <> Coalesce(a.Eingabetyp.Value, "") || Coalesce(p.Pflicht, false) <> Coalesce(a.Pflicht, false) || '
               'Coalesce(p.Auswahlwerte, "") <> Coalesce(a.Auswahlwerte, "") || Coalesce(p.Einheit, "") <> Coalesce(a.Einheit, "") || '
               'Coalesce(p.MinWert, -999999) <> Coalesce(a.MinWert, -999999) || Coalesce(p.MaxWert, -999999) <> Coalesce(a.MaxWert, -999999) || '
               'Coalesce(p.Hinweis, "") <> Coalesce(a.Hinweis, "") || fnFotoWert(p.Foto.Value, Coalesce(p.FotoMoeglich, false)) <> fnFotoWert(a.Foto.Value, Coalesce(a.FotoMoeglich, false)) || '
               'Coalesce(p.KommentarPflicht, false) <> Coalesce(a.KommentarPflicht, false) || fnGrenzmodus(p.Grenzmodus.Value) <> fnGrenzmodus(a.Grenzmodus.Value) || '
               'Coalesce(p.BedingungWert, "") <> Coalesce(a.BedingungWert, "") || Coalesce(LookUp(colP As b0, b0.ID = p.BedingungPunkt).QuelleID, 0) <> Coalesce(a.BedingungPunkt, 0) || '
               'Coalesce(p.HinweisBildID, 0) <> Coalesce(a.HinweisBildID, 0) || Coalesce(LookUp(colK As k0, k0.ID = p.KategorieID).QuelleID, 0) <> a.KategorieID')
AKT_ITEMS = ('Ungroup(\n    Table(\n'
             '        {T: ForAll(Filter(colP As p, IsBlank(LookUp(colAltP As a, a.ID = p.QuelleID))) As p, {Art: "neu", Text: p.Title})},\n'
             '        {T: ForAll(Filter(colP As p, With({a: LookUp(colAltP As a0, a0.ID = p.QuelleID)}, !IsBlank(a) && (' + P_GEAENDERT + '))) As p, {Art: "geändert", Text: p.Title})},\n'
             '        {T: ForAll(Filter(colAltP As a, IsBlank(LookUp(colP As p, p.QuelleID = a.ID))) As a, {Art: "entfernt", Text: a.Title})}\n'
             '    ),\n    T\n)')

# ---------------------------------------------------------------- Steuerelemente


class C:
    def __init__(self, name, typ, props, kinder=None, variante=None):
        self.name, self.typ, self.props, self.kinder = name, typ, dict(props), list(kinder or [])
        self.variante = variante or ("ManualLayout" if typ.startswith("GroupContainer") else ("Vertical" if typ.startswith("Gallery") else None))


def con(name, props, kinder):
    p = {"BorderThickness": "0"}
    p.update(props)
    return C(name, "GroupContainer@1.5.0", p, kinder)


def lbl(name, text, x, y, w, h, size=14, color="clrText", bold=False, **kw):
    p = {"Text": text, "X": x, "Y": y, "Width": w, "Height": h, "Size": str(size), "Color": color, "Font": FONT}
    if bold:
        p["FontWeight"] = "FontWeight.Semibold"
    p.update(kw)
    return C(name, "Label@2.5.1", p)


def radius(r):
    return {"RadiusBottomLeft": str(r), "RadiusBottomRight": str(r), "RadiusTopLeft": str(r), "RadiusTopRight": str(r)}


def btn(name, text, x, y, w, h, onselect, art="primaer", size=14, **kw):
    if art == "primaer":
        p = {"Fill": "clrPrimaer", "Color": "Color.White", "HoverFill": "ColorFade(clrPrimaer, -20%)", "PressedFill": "ColorFade(clrPrimaer, -35%)",
             "HoverColor": "Color.White", "PressedColor": "Color.White", "BorderThickness": "0"}
    elif art == "gefahr":
        p = {"Fill": "clrKarte", "Color": "clrFehler", "HoverFill": "clrFehlerHell", "PressedFill": "clrFehlerHell",
             "HoverColor": "clrFehler", "PressedColor": "clrFehler", "BorderColor": "clrFehler", "BorderThickness": "1"}
    elif art == "kopf":
        p = {"Fill": "RGBA(255, 255, 255, 0.12)", "Color": "Color.White", "HoverFill": "RGBA(255, 255, 255, 0.24)", "PressedFill": "RGBA(255, 255, 255, 0.32)",
             "HoverColor": "Color.White", "PressedColor": "Color.White", "BorderThickness": "0"}
    else:
        p = {"Fill": "clrKarte", "Color": "clrPrimaer", "HoverFill": "clrPrimaerHell", "PressedFill": "clrPrimaerHell",
             "HoverColor": "clrPrimaer", "PressedColor": "clrPrimaer", "BorderColor": "clrPrimaer", "BorderThickness": "1"}
    p.update({"Text": text, "X": x, "Y": y, "Width": w, "Height": h, "OnSelect": onselect, "Size": str(size), "Font": FONT,
              "DisplayMode": BTN_DM, "DisabledFill": "clrGesperrtHell", "DisabledColor": "clrGesperrt", "DisabledBorderColor": "clrGesperrtHell"})
    p.update(radius(6))
    p.update(kw)
    return C(name, "Classic/Button@2.2.0", p)


def txt(name, default, onchange, x, y, w, h, hint, label, multi=False, zahl=False, **kw):
    p = {"Default": default, "OnChange": onchange, "X": x, "Y": y, "Width": w, "Height": h, "HintText": hint,
         "AccessibleLabel": label, "Font": FONT, "Size": "14", "Color": "clrText", "BorderColor": "clrRahmen",
         "HoverBorderColor": "clrPrimaer", "FocusedBorderColor": "clrPrimaer", "Fill": "clrKarte", "DisplayMode": EDIT}
    if multi:
        p["Mode"] = "TextMode.MultiLine"
    if zahl:
        p["Format"] = "TextFormat.Number"
    p.update(kw)
    return C(name, "Classic/TextInput@2.3.2", p)


def dd(name, items, wert, default, onchange, x, y, w, h, label, **kw):
    p = {"Items": items, "Items.Value": wert, "Default": default, "OnChange": onchange, "X": x, "Y": y, "Width": w, "Height": h,
         "AccessibleLabel": label, "Font": FONT, "Size": "14", "Color": "clrText", "Fill": "clrKarte", "BorderColor": "clrRahmen",
         "BorderThickness": "1", "ChevronBackground": "clrPrimaer", "ChevronFill": "Color.White",
         "ChevronHoverBackground": "ColorFade(clrPrimaer, -20%)", "ChevronHoverFill": "Color.White", "HoverFill": "clrPrimaerHell",
         "PressedColor": "Color.White", "PressedFill": "clrPrimaer", "SelectionColor": "Color.White", "SelectionFill": "clrPrimaer",
         "PaddingLeft": "10", "DisplayMode": EDIT}
    p.update(kw)
    return C(name, "Classic/DropDown@2.3.1", p)


def dp(name, default, onchange, x, y, w, h, label, **kw):
    p = {"DefaultDate": default, "OnChange": onchange, "X": x, "Y": y, "Width": w, "Height": h, "AccessibleLabel": label,
         "Font": FONT, "Size": "14", "Color": "clrText", "BorderColor": "clrRahmen", "IconBackground": "clrPrimaer",
         "IconFill": "Color.White", "StartOfWeek": "StartOfWeek.Monday", "Format": "DateTimeFormat.ShortDate",
         "DisplayMode": BTN_DM}
    p.update(kw)
    return C(name, "Classic/DatePicker@2.6.0", p)


def gal(name, items, x, y, w, h, size, kinder, label, wrap=1, **kw):
    p = {"Items": items, "X": x, "Y": y, "Width": w, "Height": h, "TemplateSize": str(size), "TemplatePadding": "0",
         "AccessibleLabel": label, "ShowScrollbar": "true"}
    if wrap > 1:
        p["WrapCount"] = str(wrap)
        p["ShowScrollbar"] = "false"
    p.update(kw)
    return C(name, "Gallery@2.15.0", p, kinder)


def optionen(name, items, ist, onselect, x, y, w, anzahl, label, h=40, size=13, aktiv=EDIT, visible=None, zeilen=1):
    """Segment-Auswahl als Galerie: ein Knopf je Option, gewählte Option gefüllt."""
    sel_ = "ThisItem.W = " + ist
    knopf = C("btn" + name[3:], "Classic/Button@2.2.0", dict({
        "Text": "ThisItem.N", "X": "0", "Y": "0", "Width": "Parent.TemplateWidth - 6", "Height": str(h - 4), "Size": str(size), "Font": FONT,
        "Fill": "If(%s, clrPrimaer, clrKarte)" % sel_, "Color": "If(%s, Color.White, clrText)" % sel_,
        "HoverFill": "If(%s, ColorFade(clrPrimaer, -20%%), clrPrimaerHell)" % sel_, "HoverColor": "If(%s, Color.White, clrText)" % sel_,
        "PressedFill": "ColorFade(clrPrimaer, -35%)", "PressedColor": "Color.White",
        "DisabledFill": "If(%s, clrPrimaerHell, clrKarte)" % sel_, "DisabledColor": "If(%s, clrPrimaer, clrTextGrau)" % sel_,
        "DisabledBorderColor": "If(%s, clrPrimaer, clrRahmen)" % sel_,
        "BorderColor": "If(%s, clrPrimaer, clrRahmen)" % sel_, "BorderThickness": "1",
        "DisplayMode": aktiv.replace("DisplayMode.View", "DisplayMode.Disabled"), "OnSelect": onselect}, **radius(6)))
    p = {}
    if visible:
        p["Visible"] = visible
    return gal(name, items, x, y, w, str(h * zeilen), "%d" % h, [knopf], label, wrap=anzahl, **p)


def overlay(name, sichtbar, karte_w, karte_h, kinder, titel, zu):
    """Vollbild-Fenster: dunkler Hintergrund sperrt den Rest der App."""
    return con(name, {"Fill": "RGBA(0, 0, 0, 0.45)", "Width": "Parent.Width", "Height": "Parent.Height", "Visible": sichtbar}, [
        btn("btn" + name[3:] + "Sperre", '""', "0", "0", "Parent.Width", "Parent.Height", "false", art="kopf",
            Fill="RGBA(0, 0, 0, 0)", HoverFill="RGBA(0, 0, 0, 0)", PressedFill="RGBA(0, 0, 0, 0)", DisabledFill="RGBA(0, 0, 0, 0)",
            DisplayMode="DisplayMode.Edit", **radius(0)),
        con("con" + name[3:] + "Karte", dict({"Fill": "clrKarte", "Width": str(karte_w), "Height": str(karte_h),
                                              "X": "(Parent.Width - Self.Width) / 2", "Y": "(Parent.Height - Self.Height) / 2"}, **radius(12)),
            [lbl("lbl" + name[3:] + "Titel", titel, "24", "16", str(karte_w - 48), "40", size=18, bold=True)] + kinder
            + ([btn("btn" + name[3:] + "Zu", '"✕"', str(karte_w - 60), "16", "40", "40", zu, art="sekundaer", size=16)] if zu else [])),
    ])


def laden_overlay(name):
    return con(name, {"Fill": "RGBA(255, 255, 255, 0.7)", "Width": "Parent.Width", "Height": "Parent.Height", "Visible": "varIsLoading"}, [
        btn("btn" + name[3:] + "Sperre", '""', "0", "0", "Parent.Width", "Parent.Height", "false", art="kopf",
            Fill="RGBA(0, 0, 0, 0)", HoverFill="RGBA(0, 0, 0, 0)", PressedFill="RGBA(0, 0, 0, 0)", DisabledFill="RGBA(0, 0, 0, 0)",
            DisplayMode="DisplayMode.Edit", **radius(0)),
        lbl("lbl" + name[3:] + "Text", 'If(varLadeText = "", "Bitte warten …", varLadeText)', "0", "(Parent.Height - 60) / 2",
            "Parent.Width", "60", size=18, color="clrPrimaer", bold=True, Align="Align.Center"),
    ])


# ---------------------------------------------------------------- Bildschirm 1: Übersicht

ST = "fnStatus(ThisItem.Status, ThisItem.Aktiv)"
OEFFNEN = ("Set(varArbeitStart, false);\nSet(varIsLoading, true);\nSet(varLadeText, \"\");\n"
           "Navigate(scrEditor, ScreenTransition.None)")

LI_BEARBEITEN = ("If(" + FREI + ",\n"
                 "    " + LOCK + ";\n"
                 "    If(" + ST + " = \"Entwurf\" || Coalesce(ThisItem.EntwurfFassung, 0) > 0,\n"
                 "        Set(varFrage, \"\");\n"
                 "        Set(varRgID, ThisItem.ID);\n"
                 "        Set(varFassung, Coalesce(ThisItem.EntwurfFassung, 1));\n"
                 "        Set(varSchreibbar, true);\n"
                 "        Set(varJob, \"laden\");\n"
                 "        " + OEFFNEN.replace("\n", "\n        ") + ",\n"
                 "        varFrage <> \"fassung\" & ThisItem.ID,\n"
                 "        Set(varFrage, \"fassung\" & ThisItem.ID),\n"
                 "        Set(varFrage, \"\");\n"
                 "        Set(varRgID, ThisItem.ID);\n"
                 "        Set(varFassung, 0);\n"
                 "        Set(varSchreibbar, true);\n"
                 "        Set(varNach, \"neueFassung\");\n"
                 "        Set(varJob, If(Coalesce(ThisItem.Fassung, 0) = 0, \"vorbereiten\", \"neueFassung\"));\n"
                 "        " + OEFFNEN.replace("\n", "\n        ") + "\n"
                 "    )\n"
                 ")")

LI_ANSEHEN = ("If(" + FREI + ",\n"
              "    Set(varFrage, \"\");\n"
              "    Set(varRgID, ThisItem.ID);\n"
              "    Set(varFassung, fnAktiveFassung(ThisItem.Fassung));\n"
              "    Set(varSchreibbar, false);\n"
              "    Set(varNach, \"laden\");\n"
              "    Set(varJob, If(Coalesce(ThisItem.Fassung, 0) = 0, \"vorbereiten\", \"laden\"));\n"
              "    " + OEFFNEN.replace("\n", "\n    ") + "\n"
              ")")

LI_NEU_LADEN = ("Set(varIsLoading, true);\nConcurrent(Refresh(RG_Rundgaenge), Refresh(RG_Plan));\n"
                "Concurrent(ClearCollect(colRg, RG_Rundgaenge), ClearCollect(colPlanAlle, RG_Plan));\nSet(varIsLoading, false)")

LI_AKTION = ("If(" + FREI + ",\n"
             "    If(varFrage <> \"aktion\" & ThisItem.ID,\n"
             "        Set(varFrage, \"aktion\" & ThisItem.ID);\n"
             "        " + LOCK + ";\n"
             "        If(" + ST + " = \"Aktiv\",\n"
             "            With({d: LookUp(RG_Durchfuehrungen, Title = \"R\" & ThisItem.ID & \"-\" & Text(Today(), \"yyyy-mm-dd\"))}, Set(varHeuteLaeuft, !IsBlank(d) && d.Status <> \"Abgeschlossen\"))\n"
             "        ),\n"
             "        Set(varFrage, \"\");\n"
             "        Set(varIsLoading, true);\n"
             "        Set(varPatchFehler, false);\n"
             "        If(" + ST + " = \"Aktiv\",\n"
             "            IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = ThisItem.ID), {Status: \"Archiviert\", Aktiv: false}), Set(varPatchFehler, true)),\n"
             "            " + ST + " = \"Archiviert\",\n"
             "            IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = ThisItem.ID), {Status: \"Aktiv\", Aktiv: true}), Set(varPatchFehler, true)),\n"
             "            " + ST + " = \"Entwurf\" && Coalesce(LookUp(RG_Rundgaenge, ID = ThisItem.ID).Fassung, 0) = 0 && !Coalesce(LookUp(RG_Rundgaenge, ID = ThisItem.ID).Aktiv, false),\n"
             "            IfError(Remove(RG_Pruefpunkte, Filter(RG_Pruefpunkte, RundgangID = ThisItem.ID)), Set(varPatchFehler, true));\n"
             "            IfError(Remove(RG_Kategorien, Filter(RG_Kategorien, RundgangID = ThisItem.ID)), Set(varPatchFehler, true));\n"
             "            IfError(Remove(RG_Bereiche, Filter(RG_Bereiche, RundgangID = ThisItem.ID)), Set(varPatchFehler, true));\n"
             "            IfError(Remove(RG_Plan, Filter(RG_Plan, RundgangID = ThisItem.ID)), Set(varPatchFehler, true));\n"
             "            If(!varPatchFehler, IfError(Remove(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = ThisItem.ID)), Set(varPatchFehler, true)))\n"
             "        );\n"
             "        If(varPatchFehler, Notify(\"Das hat nicht geklappt. Bitte erneut versuchen.\", NotificationType.Error), Notify(\"Erledigt.\", NotificationType.Success));\n"
             "        " + LI_NEU_LADEN.replace("\n", "\n        ") + "\n"
             "    )\n"
             ")")

LI_VERWERFEN = zweimal('"verwerfen" & ThisItem.ID',
                       "Set(varIsLoading, true);\n"
                       "        Set(varPatchFehler, false);\n"
                       "        With({f: Coalesce(LookUp(RG_Rundgaenge, ID = ThisItem.ID).EntwurfFassung, 0)},\n"
                       "            If(f > 0 && f <> fnAktiveFassung(ThisItem.Fassung) && CountRows(Filter(Filter(RG_Bereiche, RundgangID = ThisItem.ID && Fassung = f), Coalesce(Aktiv, false))) = 0,\n"
                       "                IfError(Remove(RG_Pruefpunkte, Filter(RG_Pruefpunkte, RundgangID = ThisItem.ID && Fassung = f)), Set(varPatchFehler, true));\n"
                       "                IfError(Remove(RG_Kategorien, Filter(RG_Kategorien, RundgangID = ThisItem.ID && Fassung = f)), Set(varPatchFehler, true));\n"
                       "                IfError(Remove(RG_Bereiche, Filter(RG_Bereiche, RundgangID = ThisItem.ID && Fassung = f)), Set(varPatchFehler, true)),\n"
                       "                f > 0,\n"
                       "                Notify(\"Diese Fassung ist schon teilweise aktiv und wird nicht gelöscht. Bitte „Bearbeiten“ und dann „Aktivieren …“ erneut tippen.\", NotificationType.Error);\n"
                       "                Set(varPatchFehler, true)\n"
                       "            )\n"
                       "        );\n"
                       "        If(!varPatchFehler, IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = ThisItem.ID), {EntwurfFassung: 0, EntwurfVon: \"\"}), Set(varPatchFehler, true)));\n"
                       "        If(varPatchFehler, Notify(\"Verwerfen unvollständig. Bitte erneut versuchen.\", NotificationType.Error), Notify(\"Entwurf verworfen.\", NotificationType.Success));\n"
                       "        " + LI_NEU_LADEN.replace("\n", "\n        "))

PLAN_TEXT = ('With({pl: Filter(colPlanAlle, RundgangID = ThisItem.ID && Coalesce(Aktiv, false))}, '
             'If(IsEmpty(pl), "kein Plan", "Plan: " & Concat(pl As x, Left(fnWochentag(x.Wochentag), 2) & " " & fnZyklus(x.ZyklusWochen), ", ")))')
LI_INFO = ('If(' + ST + ' = "Entwurf", "noch nie aktiviert", "aktive Fassung " & fnAktiveFassung(ThisItem.Fassung)) & "  ·  " & ' + PLAN_TEXT
           + ' & If(Coalesce(ThisItem.EntwurfFassung, 0) > 0 && ' + ST + ' <> "Entwurf", "  ·  Entwurf Fassung " & ThisItem.EntwurfFassung & " in Arbeit" & If(Coalesce(ThisItem.EntwurfVon, "") <> "", " (" & ThisItem.EntwurfVon & ")", ""), "")')
LI_FRAGE = ('Switch(varFrage,\n'
            '    "fassung" & ThisItem.ID, "Nochmal tippen: Es entsteht ein Entwurf (neue Fassung). Der laufende Rundgang bleibt unverändert, bis du ihn aktivierst.",\n'
            '    "aktion" & ThisItem.ID, If(' + ST + ' = "Aktiv", If(varHeuteLaeuft, "Achtung: Heute läuft noch ein Rundgang. Archiviert erscheint er nicht mehr auf der Startseite. Nochmal tippen zum Archivieren.", "Nochmal tippen: Der Rundgang erscheint nicht mehr auf der Startseite."), '
            + ST + ' = "Archiviert", "Nochmal tippen: Der Rundgang erscheint wieder auf der Startseite (laut Plan).", "Nochmal tippen: Der Entwurf wird mit allen Bereichen, Kategorien, Prüfpunkten und Planzeilen gelöscht."),\n'
            '    "verwerfen" & ThisItem.ID, "Nochmal tippen: Der Entwurf wird gelöscht. Die aktive Fassung bleibt.",\n'
            '    ""\n)')

FARBE_STATUS = 'Switch(%s, "Aktiv", clrErfolg%s, "Entwurf", clrWarnung%s, clrTextGrau%s)'

li_karte = con("conLiKarte", dict({"Fill": "clrKarte", "BorderColor": "clrRahmen",
                                    "BorderThickness": "1", "X": "0", "Y": "4", "Width": "Parent.TemplateWidth", "Height": "Parent.TemplateHeight - 8"}, **radius(8)), [
    lbl("lblLiName", "ThisItem.Title", "120", "8", "406", "30", size=17, bold=True),
    lbl("lblLiStatus", ST, "16", "11", "96", "24", size=12, color=FARBE_STATUS % (ST, "", "", ""), Align="Align.Center",
        Fill=(FARBE_STATUS % (ST, "Hell", "Hell", "")).replace("clrTextGrau)", "clrGesperrtHell)")),
    lbl("lblLiInfo", LI_INFO, "16", "40", "510", "40", size=12, color="clrTextGrau", VerticalAlign="VerticalAlign.Top"),
    lbl("lblLiFrage", LI_FRAGE, "16", "84", "Parent.Width - 32", "22", size=12, color="clrWarnung", bold=True,
        Visible='Len(Self.Text) > 0'),
    btn("btnLiBearbeiten", 'If(varFrage = "fassung" & ThisItem.ID, "Neue Fassung?", "Bearbeiten")', "Parent.Width - 186", "16", "170", "44", LI_BEARBEITEN),
    btn("btnLiAnsehen", '"Ansehen"', "Parent.Width - 304", "16", "110", "44", LI_ANSEHEN, art="sekundaer",
        Visible=ST + ' = "Aktiv" || ' + ST + ' = "Archiviert"'),
    btn("btnLiPlan", '"Plan"', "Parent.Width - 402", "16", "90", "44",
        "If(" + FREI + ",\n    Set(varFrage, \"\");\n    Set(varPlanRgID, ThisItem.ID);\n    Navigate(scrPlan, ScreenTransition.None)\n)", art="sekundaer"),
    btn("btnLiAktion", 'If(varFrage = "aktion" & ThisItem.ID, "Wirklich?", Switch(' + ST + ', "Aktiv", "Archivieren", "Archiviert", "Reaktivieren", "Löschen"))',
        "Parent.Width - 560", "16", "150", "44", LI_AKTION, art="gefahr"),
    btn("btnLiVerwerfen", 'If(varFrage = "verwerfen" & ThisItem.ID, "Wirklich?", "Entwurf verwerfen")', "Parent.Width - 758", "16", "190", "44",
        LI_VERWERFEN, art="gefahr", Visible="Coalesce(ThisItem.EntwurfFassung, 0) > 0 && " + ST + ' <> "Entwurf"'),
])

NEU_ANLEGEN = ("If(" + FREI + ",\n"
               "    " + LOCK + ";\n"
               "    If(Trim(txtNeuName.Text) = \"\",\n"
               "        Notify(\"Bitte einen Namen eingeben.\", NotificationType.Warning),\n"
               "        !IsBlank(LookUp(colRg, Lower(Trim(Title)) = Lower(Trim(txtNeuName.Text)))),\n"
               "        Notify(\"Diesen Namen gibt es schon.\", NotificationType.Warning),\n"
               "        !varNeuLeer && IsBlank(ddNeuQuelle.Selected),\n"
               "        Notify(\"Bitte den Rundgang wählen, der kopiert werden soll.\", NotificationType.Warning),\n"
               "        Set(varIsLoading, true);\n"
               "        Set(varPatchFehler, false);\n"
               "        IfError(Patch(RG_Rundgaenge, Defaults(RG_Rundgaenge), {Title: Left(Trim(txtNeuName.Text), 255), Beschreibung: \"\", RgReihenfolge: Coalesce(Max(colRg, RgReihenfolge), 0) + 10, Aktiv: false, Status: \"Entwurf\", Fassung: 0, EntwurfFassung: 1, EntwurfVon: User().FullName}), Set(varPatchFehler, true));\n"
               "        Refresh(RG_Rundgaenge);\n"
               "        Set(varNeuRg, First(Sort(Filter(RG_Rundgaenge, Title = Left(Trim(txtNeuName.Text), 255)), ID, SortOrder.Descending)));\n"
               "        If(varPatchFehler || IsBlank(varNeuRg.ID),\n"
               "            Set(varIsLoading, false);\n"
               "            Notify(\"Anlegen fehlgeschlagen. Bitte erneut versuchen.\", NotificationType.Error),\n"
               "            Set(varNeuOffen, false);\n"
               "            Set(varRgID, varNeuRg.ID);\n"
               "            Set(varFassung, 1);\n"
               "            Set(varSchreibbar, true);\n"
               "            If(varNeuLeer,\n"
               "                Set(varJob, \"laden\"),\n"
               "                With({s: ddNeuQuelle.Selected},\n"
               "                    Set(varQuelleR, s.ID);\n"
               "                    Set(varQuelleF, If(fnStatus(s.Status, s.Aktiv) = \"Entwurf\", Coalesce(s.EntwurfFassung, 1), fnAktiveFassung(s.Fassung)));\n"
               "                    Set(varQuelleNurAktiv, fnStatus(s.Status, s.Aktiv) <> \"Entwurf\")\n"
               "                );\n"
               "                Set(varZielR, varNeuRg.ID);\n"
               "                Set(varZielF, 1);\n"
               "                Set(varJob, \"quelle\")\n"
               "            );\n"
               "            Reset(txtNeuName);\n"
               "            " + OEFFNEN.replace("\n", "\n            ") + "\n"
               "        )\n"
               "    )\n"
               ")")

VORLAGEN_PUNKTE = [
    # (Kategorie 1-3, Frage, Typ, Pflicht, Foto, Einheit, Min, Max, Grenzmodus, Auswahlwerte)
    (1, "Bereich sauber und ordentlich?", "IONIO", "true", "Bei Mangel Pflicht", "", "-999999", "-999999", "Mangel", ""),
    (1, "Keine Schäden sichtbar?", "IONIO", "true", "Bei Mangel Pflicht", "", "-999999", "-999999", "Mangel", ""),
    (1, "Fluchtweg und Notausgang frei?", "IONIO", "true", "Bei Mangel Pflicht", "", "-999999", "-999999", "Mangel", ""),
    (1, "Zustand", "AUSWAHL", "true", "Aus", "", "-999999", "-999999", "Mangel", "gut;mäßig;schlecht"),
    (2, "Temperatur", "ZAHL", "true", "Aus", "°C", "15", "25", "Warnen", ""),
    (2, "Zählerstand", "ZAHL", "true", "Aus", "", "-999999", "-999999", "Mangel", ""),
    (2, "Anzahl im Regal", "ZAHL", "true", "Bei Mangel Pflicht", "Stück", "100", "1000", "Mangel", ""),
    (3, "Datum der letzten Wartung", "DATUM", "true", "Aus", "", "-999999", "-999999", "Mangel", ""),
    (3, "Schäden an", "MEHRFACH", "false", "Aus", "", "-999999", "-999999", "Mangel", "Boden;Wand;Decke;Tür;Fenster"),
    (3, "Bemerkung", "TEXT", "false", "Aus", "", "-999999", "-999999", "Mangel", ""),
]
VORLAGEN_TABELLE = "Table(\n" + ",\n".join(
    '                    {{K: {0}, R: {r}, T: "{1}", Typ: "{2}", Pfl: {3}, Foto: "{4}", Einh: "{5}", Mi: {6}, Ma: {7}, Gm: "{8}", W: "{9}"}}'.format(*v, r=(i + 1) * 10)
    for i, v in enumerate(VORLAGEN_PUNKTE)) + "\n                )"

LI_VORLAGEN = ("If(" + FREI + ",\n"
               "    " + LOCK + ";\n"
               "    Set(varFrage, \"\");\n"
               "    If(IsBlank(LookUp(colRg, Status = \"Vorlage\")),\n"
               "        Set(varIsLoading, true);\n"
               "        Set(varPatchFehler, false);\n"
               "        IfError(Patch(RG_Rundgaenge, Defaults(RG_Rundgaenge), {Title: \"Vorlagen (Builder)\", Beschreibung: \"Vorlagen für den Rundgang-Builder. Wird nie aktiviert.\", RgReihenfolge: 99999, Aktiv: false, Status: \"Vorlage\", Fassung: 0, EntwurfFassung: 1, EntwurfVon: \"\"}), Set(varPatchFehler, true));\n"
               "        Refresh(RG_Rundgaenge);\n"
               "        Set(varVorlageNeu, LookUp(RG_Rundgaenge, Status = \"Vorlage\"));\n"
               "        If(!varPatchFehler && !IsBlank(varVorlageNeu.ID),\n"
               "            With({b: Patch(RG_Bereiche, Defaults(RG_Bereiche), {Title: \"Vorlagen\", RundgangID: varVorlageNeu.ID, Fassung: 1, RgReihenfolge: 10, Hinweis: \"\", Aktiv: false, QuelleID: 0})},\n"
               "                With({k1: Patch(RG_Kategorien, Defaults(RG_Kategorien), {Title: \"Sichtprüfung\", BereichID: b.ID, RundgangID: varVorlageNeu.ID, Fassung: 1, RgReihenfolge: 10, Hinweis: \"\", Aktiv: true, QuelleID: 0})},\n"
               "                With({k2: Patch(RG_Kategorien, Defaults(RG_Kategorien), {Title: \"Messwerte\", BereichID: b.ID, RundgangID: varVorlageNeu.ID, Fassung: 1, RgReihenfolge: 20, Hinweis: \"\", Aktiv: true, QuelleID: 0})},\n"
               "                With({k3: Patch(RG_Kategorien, Defaults(RG_Kategorien), {Title: \"Sonstiges\", BereichID: b.ID, RundgangID: varVorlageNeu.ID, Fassung: 1, RgReihenfolge: 30, Hinweis: \"\", Aktiv: true, QuelleID: 0})},\n"
               "                ForAll(" + VORLAGEN_TABELLE + " As v,\n"
               "                    Patch(RG_Pruefpunkte, Defaults(RG_Pruefpunkte), {Title: v.T, KategorieID: Switch(v.K, 1, k1.ID, 2, k2.ID, k3.ID), RundgangID: varVorlageNeu.ID, Fassung: 1, RgReihenfolge: v.R, Aktiv: true, QuelleID: 0, Eingabetyp: {Value: v.Typ}, Pflicht: v.Pfl, Auswahlwerte: v.W, Einheit: v.Einh, MinWert: If(v.Mi = -999999, Blank(), v.Mi), MaxWert: If(v.Ma = -999999, Blank(), v.Ma), Hinweis: \"\", FotoMoeglich: false, Foto: {Value: v.Foto}, KommentarPflicht: false, Grenzmodus: {Value: v.Gm}, BedingungPunkt: 0, BedingungWert: \"\", HinweisBildID: 0})\n"
               "                ))))\n"
               "            )\n"
               "        );\n"
               "        " + LI_NEU_LADEN.replace("\n", "\n        ") + "\n"
               "    );\n"
               "    If(IsBlank(LookUp(colRg, Status = \"Vorlage\")),\n"
               "        Notify(\"Die Vorlagen konnten nicht angelegt werden.\", NotificationType.Error),\n"
               "        Set(varRgID, LookUp(colRg, Status = \"Vorlage\").ID);\n"
               "        Set(varFassung, Coalesce(LookUp(colRg, Status = \"Vorlage\").EntwurfFassung, 1));\n"
               "        Set(varSchreibbar, true);\n"
               "        Set(varJob, \"laden\");\n"
               "        " + OEFFNEN.replace("\n", "\n        ") + "\n"
               "    )\n"
               ")")

LI_ITEMS = ('Sort(Filter(colRg, fnStatus(Status, Aktiv) <> "Vorlage" && (varAlleZeigen || fnStatus(Status, Aktiv) <> "Archiviert")), '
            'Switch(fnStatus(Status, Aktiv), "Entwurf", "1", "Aktiv", "2", "3") & Lower(Title))')

scr_liste = C("scrListe", "Screen", {
    "Fill": "clrHintergrund",
    "OnVisible": "Set(varIsLoading, true);\nSet(varLadeText, \"\");\nSet(varFrage, \"\");\nSet(varNeuOffen, false);\n"
                 "Concurrent(Refresh(RG_Rundgaenge), Refresh(RG_Plan));\n"
                 "Concurrent(ClearCollect(colRg, RG_Rundgaenge), ClearCollect(colPlanAlle, RG_Plan));\nSet(varIsLoading, false)",
}, [
    con("conLiKopf", {"Fill": "clrPrimaer", "Width": "Parent.Width", "Height": "64"}, [
        lbl("lblLiTitel", '"Rundgang-Builder"', "24", "0", "500", "64", size=22, color="Color.White", bold=True),
        lbl("lblLiNutzer", "User().FullName", "Parent.Width - 424", "0", "400", "64", size=13, color="Color.White", Align="Align.Right"),
    ]),
    btn("btnLiNeu", '"+ Neuer Rundgang"', "24", "84", "220", "44",
        "If(" + FREI + ",\n    Set(varFrage, \"\");\n    Set(varNeuLeer, true);\n    Reset(txtNeuName);\n    Set(varNeuOffen, true)\n)"),
    btn("btnLiVorlagen", '"Vorlagen bearbeiten"', "256", "84", "220", "44", LI_VORLAGEN, art="sekundaer"),
    btn("btnLiNeuLaden", '"↻ Neu laden"', "488", "84", "150", "44", LI_NEU_LADEN, art="sekundaer"),
    btn("btnLiAlle", 'If(varAlleZeigen, "✓ Archivierte zeigen", "Archivierte zeigen")', "Parent.Width - 264", "84", "240", "44",
        "Set(varAlleZeigen, !varAlleZeigen);\nSet(varFrage, \"\")", art="sekundaer"),
    gal("galLi", LI_ITEMS, "24", "144", "Parent.Width - 48", "Parent.Height - 160", 116, [li_karte], '"Rundgänge"'),
    lbl("lblLiLeer", '"Noch keine Rundgänge. Lege mit „+ Neuer Rundgang“ den ersten an."', "24", "160", "Parent.Width - 48", "40",
        size=15, color="clrTextGrau", Visible="IsEmpty(galLi.AllItems) && !varIsLoading"),
    overlay("conNeu", "varNeuOffen", 600, 420, [
        lbl("lblNeuName", '"Name des Rundgangs"', "24", "68", "552", "24", size=13, color="clrTextGrau"),
        txt("txtNeuName", '""', "false", "24", "94", "552", "44", '"z. B. Objektrundgang Halle 3"', '"Name des neuen Rundgangs"',
            DisplayMode="DisplayMode.Edit"),
        lbl("lblNeuArt", '"Wie anfangen?"', "24", "150", "552", "24", size=13, color="clrTextGrau"),
        optionen("galNeuArt", 'Table({W: "leer", N: "Leer anfangen"}, {W: "kopie", N: "Kopie eines Rundgangs"})',
                 'If(varNeuLeer, "leer", "kopie")', 'Set(varNeuLeer, ThisItem.W = "leer")', "24", "176", "552", 2, '"Wie anfangen"',
                 h=44, size=14, aktiv="DisplayMode.Edit"),
        dd("ddNeuQuelle", 'Sort(Filter(colRg, fnStatus(Status, Aktiv) <> "Vorlage" && (Coalesce(Fassung, 0) > 0 || fnStatus(Status, Aktiv) = "Entwurf")), Lower(Title))',
           "Title", '""', "false", "24", "232", "552", "44", '"Rundgang, der kopiert wird"', Visible="!varNeuLeer",
           DisplayMode="DisplayMode.Edit", AllowEmptySelection="true"),
        lbl("lblNeuHilfe", 'If(varNeuLeer, "Du startest mit einem leeren Rundgang und legst Bereiche, Kategorien und Prüfpunkte an.", '
            '"Die Kopie übernimmt Bereiche, Kategorien und Prüfpunkte der aktiven Fassung. Der Plan wird nicht kopiert. Noch nie geöffnete alte Rundgänge erscheinen erst nach einmal „Ansehen“.")',
            "24", "284", "552", "60", size=12, color="clrTextGrau"),
        btn("btnNeuAbbrechen", '"Abbrechen"', "24", "352", "160", "48", "Set(varNeuOffen, false)", art="sekundaer"),
        btn("btnNeuAnlegen", '"Anlegen"', "416", "352", "160", "48", NEU_ANLEGEN),
    ], '"Neuer Rundgang"', "Set(varNeuOffen, false)"),
    laden_overlay("conLiLaden"),
])


# ---------------------------------------------------------------- Bildschirm 2: Editor

def ind(text, n):
    return text.replace("\n", "\n" + " " * n)


SPRUNG = ('If(ThisItem.Ebene = 3,\n    ' + ind(sel("3", "ThisItem.ID", "ThisItem.BerID", "ThisItem.KatID"), 4) + ',\n'
          'ThisItem.Ebene = 2,\n    ' + ind(sel("2", "ThisItem.ID", "ThisItem.BerID", "ThisItem.ID"), 4) + ',\n'
          'ThisItem.Ebene = 1,\n    ' + ind(sel("1", "ThisItem.ID", "ThisItem.ID", "0"), 4) + '\n)')
GL_SELECT = "If(!varIsLoading,\n    " + ind(SPRUNG, 4) + "\n)"
GL_FEHLER = ('CountRows(Filter(galPr.AllItems As e, e.Art = "Fehler" && ((e.Ebene = ThisItem.Ebene && e.ID = ThisItem.ID) || '
             '(ThisItem.Ebene = 2 && e.KatID = ThisItem.ID) || (ThisItem.Ebene = 1 && e.BerID = ThisItem.ID)))) > 0')
GL_GEWAEHLT = "ThisItem.Ebene = varAuswahlEbene && ThisItem.ID = varAuswahlID"


def baum_zeilen(prefix, gewaehlt, onselect, info, fehler):
    """Vorlage einer Baumzeile: Hintergrund, Text, Info, Warnzeichen, darüber ein durchsichtiger Knopf."""
    kinder = [
        lbl("lbl%sHinter" % prefix, '""', "0", "0", "Parent.TemplateWidth", "Parent.TemplateHeight",
            Fill="If(%s, clrPrimaerHell, Color.White)" % gewaehlt),
        lbl("lbl%sText" % prefix,
            'If(ThisItem.Ebene = 1, "▾ " & ThisItem.Titel, ThisItem.Ebene = 2, "      " & ThisItem.Titel, "            • " & ThisItem.Titel)',
            "8", "0", "Parent.TemplateWidth - 126", "Parent.TemplateHeight", size=13,
            FontWeight="If(ThisItem.Ebene < 3, FontWeight.Semibold, FontWeight.Normal)",
            Color="If(ThisItem.Ebene = 1, clrPrimaer, clrText)", Wrap="false"),
        lbl("lbl%sInfo" % prefix, info, "Parent.TemplateWidth - 114", "0", "90", "Parent.TemplateHeight", size=11, color="clrTextGrau",
            Align="Align.Right"),
    ]
    if fehler:
        kinder.append(lbl("lbl%sFehler" % prefix, 'If(%s, "⚠", "")' % fehler, "Parent.TemplateWidth - 22", "0", "20",
                          "Parent.TemplateHeight", size=13, color="clrFehler", bold=True))
    kinder.append(btn("btn%sZeile" % prefix, '""', "0", "0", "Parent.TemplateWidth", "Parent.TemplateHeight", onselect, art="kopf",
                      Fill="RGBA(0, 0, 0, 0)", HoverFill="RGBA(23, 20, 150, 0.06)", PressedFill="RGBA(23, 20, 150, 0.12)",
                      DisabledFill="RGBA(0, 0, 0, 0)", **radius(0)))
    return kinder


GL_INFO = 'If(ThisItem.Ebene = 2, ThisItem.Info & " Pkt.", ThisItem.Ebene = 3, ThisItem.Info, "")'


def neu_eintrag(ds, col, felder, ebene, b, k, fokus, bedingung, meldung):
    return ("If(varSchreibbar && " + FREI + ",\n"
            "    " + LOCK + ";\n"
            "    " + ind(CHECK, 4) + ";\n"
            "    If(!varEntwurfOk,\n        false,\n        " + bedingung + ",\n"
            "        Notify(\"" + meldung + "\", NotificationType.Warning),\n"
            "        Set(varNeuID, IfError(Patch(" + ds + ", Defaults(" + ds + "), {" + felder + "}).ID, 0));\n"
            "        If(varNeuID = 0,\n"
            "            Notify(\"Anlegen fehlgeschlagen. Bitte erneut versuchen.\", NotificationType.Error),\n"
            "            Collect(" + col + ", LookUp(" + ds + ", ID = varNeuID));\n"
            "            " + ind(sel(ebene, "varNeuID", b, k), 12) + ";\n"
            "            SetFocus(" + fokus + ")\n"
            "        )\n"
            "    )\n"
            ")")


NEU_B = neu_eintrag("RG_Bereiche", "colB",
                    'Title: "Neuer Bereich", RundgangID: varRgID, Fassung: varFassung, RgReihenfolge: Coalesce(Max(colB, RgReihenfolge), 0) + 10, Hinweis: "", Aktiv: false, QuelleID: 0',
                    "1", "varNeuID", "0", "txtBName", "false", "")
NEU_K = neu_eintrag("RG_Kategorien", "colK",
                    'Title: "Neue Kategorie", BereichID: varCtxB, RundgangID: varRgID, Fassung: varFassung, RgReihenfolge: Coalesce(Max(Filter(colK, BereichID = varCtxB), RgReihenfolge), 0) + 10, Hinweis: "", Aktiv: true, QuelleID: 0',
                    "2", "varCtxB", "varNeuID", "txtKName", "varCtxB = 0", "Links zuerst einen Bereich antippen.")
NEU_P = neu_eintrag("RG_Pruefpunkte", "colP",
                    'Title: "Neue Frage", KategorieID: varCtxK, RundgangID: varRgID, Fassung: varFassung, RgReihenfolge: Coalesce(Max(Filter(colP, KategorieID = varCtxK), RgReihenfolge), 0) + 10, '
                    + NEUER_PUNKT.format(typ='"IONIO"', pfl="true"),
                    "3", "varCtxB", "varCtxK", "txtPFrage", "varCtxK = 0", "Links zuerst eine Kategorie antippen.")


def umsort(ds, col, sibs, d):
    return ("With({cur: LookUp(" + col + ", ID = varAuswahlID)},\n"
            "    With({s: Sort(" + sibs + ", RgReihenfolge * 1000000 + ID)},\n"
            "        With({pos: CountRows(Filter(s, RgReihenfolge * 1000000 + ID < cur.RgReihenfolge * 1000000 + cur.ID)) + 1},\n"
            "            If(pos + (" + d + ") < 1 || pos + (" + d + ") > CountRows(s),\n"
            "                Notify(\"Steht schon ganz " + ("oben" if d == "-1" else "unten") + ".\", NotificationType.Information),\n"
            "                ClearCollect(colUmsort, Filter(ForAll(Sequence(CountRows(s)) As i, With({x: Index(s, If(i.Value = pos, pos + (" + d + "), i.Value = pos + (" + d + "), pos, i.Value))}, {ID: x.ID, Alt: x.RgReihenfolge, Neu: i.Value * 10})), Alt <> Neu));\n"
            "                ClearCollect(colUmsortErg, ForAll(colUmsort As u, {Ok: !IsError(Patch(" + ds + ", LookUp(" + ds + ", ID = u.ID" + SICHER + "), {RgReihenfolge: u.Neu}))}));\n"
            "                ForAll(colUmsort As u, Patch(" + col + ", LookUp(" + col + ", ID = u.ID), {RgReihenfolge: u.Neu}));\n"
            "                If(CountRows(Filter(colUmsortErg, !Ok)) > 0, Notify(\"Reihenfolge nicht vollständig gespeichert. Bitte den Rundgang neu öffnen.\", NotificationType.Error))\n"
            "            )\n"
            "        )\n"
            "    )\n"
            ")")


def schieben(d):
    return ("If(varSchreibbar && " + FREI + ",\n"
            "    " + LOCK + ";\n"
            "    " + ind(CHECK, 4) + ";\n"
            "    If(!varEntwurfOk,\n        false,\n        varAuswahlEbene = 1,\n"
            "        " + ind(umsort("RG_Bereiche", "colB", "colB", d), 8) + ",\n"
            "        varAuswahlEbene = 2,\n"
            "        " + ind(umsort("RG_Kategorien", "colK", "Filter(colK, BereichID = cur.BereichID)", d), 8) + ",\n"
            "        varAuswahlEbene = 3,\n"
            "        " + ind(umsort("RG_Pruefpunkte", "colP", "Filter(colP, KategorieID = cur.KategorieID)", d), 8) + "\n"
            "    )\n"
            ")")


DUPLIZIEREN = ("If(varSchreibbar && varAuswahlEbene > 0 && " + FREI + ",\n"
               "    " + LOCK + ";\n"
               "    " + ind(CHECK, 4) + ";\n"
               "    If(varEntwurfOk,\n"
               "    ClearCollect(colQB, Filter(colB, varAuswahlEbene = 1 && ID = varAuswahlID));\n"
               "    ClearCollect(colQK, Filter(colK, (varAuswahlEbene = 2 && ID = varAuswahlID) || (varAuswahlEbene = 1 && BereichID = varAuswahlID)));\n"
               "    ClearCollect(colQP, Filter(colP, (varAuswahlEbene = 3 && ID = varAuswahlID) || KategorieID in colQK.ID));\n"
               "    Set(varZielR, varRgID);\n    Set(varZielF, varFassung);\n    Set(varZielB, varCtxB);\n    Set(varZielK, varCtxK);\n"
               "    Set(varZielBAktiv, false);\n    Set(varKopieBehalteR, false);\n    Set(varKopieZusatz, \" (Kopie)\");\n"
               "    Set(varKopieNach, \"auswahl\");\n    Set(varJob, \"kopie\");\n    Set(varIsLoading, true);\n    Set(varArbeitStart, true)\n"
               "    )\n"
               ")")

DEL_KEY = '"del" & varAuswahlEbene & "-" & varAuswahlID'
ENTFERNEN = ("If(varSchreibbar && varAuswahlEbene > 0, " + ind(zweimal(DEL_KEY,
             CHECK + ";\nIf(varEntwurfOk,\n"
             "Set(varIsLoading, true);\n"
             "If(varAuswahlEbene = 3,\n"
             "    ForAll(Filter(colP, BedingungPunkt = varAuswahlID) As d, Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = d.ID" + SICHER + "), {BedingungPunkt: 0, BedingungWert: \"\"}));\n"
             "    Remove(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID" + SICHER + ")),\n"
             "    varAuswahlEbene = 2,\n"
             "    Remove(RG_Pruefpunkte, Filter(RG_Pruefpunkte, KategorieID = varAuswahlID" + SICHER + "));\n"
             "    Remove(RG_Kategorien, LookUp(RG_Kategorien, ID = varAuswahlID" + SICHER + ")),\n"
             "    varAuswahlEbene = 1,\n"
             "    ForAll(Filter(colK, BereichID = varAuswahlID) As k, Remove(RG_Pruefpunkte, Filter(RG_Pruefpunkte, KategorieID = k.ID" + SICHER + ")));\n"
             "    Remove(RG_Kategorien, Filter(RG_Kategorien, BereichID = varAuswahlID" + SICHER + "));\n"
             "    Remove(RG_Bereiche, LookUp(RG_Bereiche, ID = varAuswahlID" + SICHER + "))\n"
             ");\n"
             + laden_baum() + ";\n"
             "If((varAuswahlEbene = 3 && !IsBlank(LookUp(colP, ID = varAuswahlID))) || (varAuswahlEbene = 2 && !IsBlank(LookUp(colK, ID = varAuswahlID))) || (varAuswahlEbene = 1 && !IsBlank(LookUp(colB, ID = varAuswahlID))),\n"
             "    Notify(\"Entfernen hat nicht geklappt. Bitte erneut versuchen.\", NotificationType.Error),\n"
             "    Notify(\"Entfernt.\", NotificationType.Success)\n"
             ");\n"
             "If(varAuswahlEbene = 3,\n    " + ind(sel("2", "varCtxK", "varCtxB", "varCtxK"), 4) + ",\n"
             "    varAuswahlEbene = 2,\n    " + ind(sel("1", "varCtxB", "varCtxB", "0"), 4) + ",\n"
             "    " + ind(sel("0", "0", "0", "0"), 4) + "\n"
             ");\n"
             "Set(varIsLoading, false)\n)"), 4) + ")")
ENTF_TEXT = ('If(varAuswahlEbene = 1, "Entfernt den Bereich mit " & CountRows(Filter(colK, BereichID = varAuswahlID)) & " Kategorien und " & '
             'CountRows(Filter(colP, KategorieID in Filter(colK, BereichID = varAuswahlID).ID)) & " Prüfpunkten. Nochmal tippen.", '
             'varAuswahlEbene = 2, "Entfernt die Kategorie mit " & CountRows(Filter(colP, KategorieID = varAuswahlID)) & " Prüfpunkten. Nochmal tippen.", '
             '"Entfernt den Prüfpunkt. Nochmal tippen.")')

PP = lambda f: patch_feld("RG_Pruefpunkte", "colP", f)  # noqa: E731

TYP_ITEMS = ('Table({W: "IONIO", N: "✓ i.O./n.i.O."}, {W: "ZAHL", N: "123 Zahl"}, {W: "AUSWAHL", N: "☰ Auswahl"}, {W: "MEHRFACH", N: "☑ Mehrfach"}, '
             '{W: "TEXT", N: "Aa Text"}, {W: "DATUM", N: "📅 Datum"}, {W: "DATUMZEIT", N: "📅 + Uhrzeit"})')
FOTO_ITEMS = ('Table({W: "Aus", N: "kein Foto (bei n.i.O. möglich)"}, {W: "Optional", N: "Foto freiwillig"}, {W: "Pflicht", N: "Foto immer Pflicht"}, '
              '{W: "Bei Mangel Pflicht", N: "Foto Pflicht bei Mangel (n.i.O.)"})')
FOTO_IST = 'fnFotoWert(%s.Foto.Value, Coalesce(%s.FotoMoeglich, false))' % (CUR, CUR)
A_N = lambda a: '%(a)s.Title & If(CountRows(Filter(colP As x, x.KategorieID = %(a)s.KategorieID && x.Title = %(a)s.Title)) > 1, " (#" & %(a)s.ID & ")", "")' % {"a": a}  # noqa: E731
BED_A_BASIS = ('ForAll(Sort(Filter(colP As a, a.KategorieID = ' + CUR + '.KategorieID && a.ID <> varAuswahlID && '
               'Coalesce(a.BedingungPunkt, 0) = 0 && a.RgReihenfolge * 1000000 + a.ID < ' + CUR + '.RgReihenfolge * 1000000 + varAuswahlID), RgReihenfolge * 1000000 + ID) As a, {ID: a.ID, N: ' + A_N("a") + '})')
BED_A_UNG = ('Coalesce(' + CUR + '.BedingungPunkt, 0) <> 0 && IsBlank(LookUp(' + BED_A_BASIS + ', ID = ' + CUR + '.BedingungPunkt))')
BED_A_UNG_N = 'Coalesce(LookUp(colP, ID = ' + CUR + '.BedingungPunkt).Title, "Frage #" & ' + CUR + '.BedingungPunkt) & " (ungültig)"'
BED_A_ITEMS = ('Ungroup(Table({T: Table({ID: 0, N: "— immer zeigen —"})}, {T: ' + BED_A_BASIS + '}, '
               '{T: Filter(Table({ID: Coalesce(' + CUR + '.BedingungPunkt, 0), N: ' + BED_A_UNG_N + '}), ' + BED_A_UNG + ')}), T)')
BED_GESPERRT = '!IsBlank(LookUp(colP As d, d.BedingungPunkt = varAuswahlID))'
BED_A_CHANGE = ('If(!IsBlank(Self.Selected) && Self.Selected.ID <> Coalesce(' + CUR + '.BedingungPunkt, 0),\n    '
                + ind(PP('{BedingungPunkt: Self.Selected.ID, BedingungWert: If(Self.Selected.ID = 0, "", With({a: LookUp(colP, ID = Self.Selected.ID)}, '
                         'If(a.Eingabetyp.Value = "IONIO" || a.Eingabetyp.Value = "ZAHL", "NIO", (a.Eingabetyp.Value = "AUSWAHL" || a.Eingabetyp.Value = "MEHRFACH") && fnWerte(a.Auswahlwerte) > 0, '
                         'Trim(First(Filter(Split(a.Auswahlwerte, ";"), Trim(Value) <> "")).Value), "*")))}'), 4) + ';\n    Reset(ddPBedW)\n)')
BED_W_BASIS = ('With({a: LookUp(colP, ID = ' + CUR + '.BedingungPunkt)}, If(a.Eingabetyp.Value = "IONIO" || a.Eingabetyp.Value = "ZAHL", '
               'Table({W: "NIO", N: "n.i.O. (Mangel)"}, {W: "IO", N: "i.O."}, {W: "*", N: "beantwortet"}), '
               'a.Eingabetyp.Value = "AUSWAHL" || a.Eingabetyp.Value = "MEHRFACH", '
               'Ungroup(Table({T: ForAll(Filter(Split(Coalesce(a.Auswahlwerte, ""), ";") As s, Trim(s.Value) <> "") As s, {W: Trim(s.Value), N: Trim(s.Value)})}, {T: Table({W: "*", N: "beantwortet"})}), T), '
               'Table({W: "*", N: "beantwortet"})))')
BED_W_ITEMS = ('Ungroup(Table({T: ' + BED_W_BASIS + '}, {T: Filter(Table({W: Coalesce(' + CUR + '.BedingungWert, ""), N: Trim(Coalesce(' + CUR + '.BedingungWert, "")) & " (passt nicht)"}), '
               'Trim(Coalesce(' + CUR + '.BedingungWert, "")) <> "" && IsBlank(LookUp(' + BED_W_BASIS + ', fnBedNorm(W) = fnBedNorm(' + CUR + '.BedingungWert))))}), T)')
KAT_N = lambda k: ('LookUp(colB As b0, b0.ID = %(k)s.BereichID).Title & " › " & %(k)s.Title & If(CountRows(Filter(colK As x, x.Title = %(k)s.Title)) > 1, " (#" & %(k)s.ID & ")", "")' % {"k": k})  # noqa: E731
KAT_ITEMS = ('Sort(ForAll(colK As k, With({b: LookUp(colB As b0, b0.ID = k.BereichID)}, {ID: k.ID, N: ' + KAT_N("k") + ', '
             'S: Text(b.RgReihenfolge, "000000") & Text(b.ID, "000000") & Text(k.RgReihenfolge, "000000") & Text(k.ID, "000000")})), S)')
P_VERSCHIEBEN = ('If(!IsBlank(Self.Selected) && Self.Selected.ID <> ' + CUR + '.KategorieID && varSchreibbar,\n'
                 '    ' + ind(CHECK, 4) + ';\n    If(varEntwurfOk,\n'
                 '    With({ziel: Self.Selected.ID, abh: CountRows(Filter(colP, BedingungPunkt = varAuswahlID))},\n'
                 '        Set(varPatchFehler, false);\n'
                 '        ForAll(Filter(colP, BedingungPunkt = varAuswahlID) As d, Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = d.ID' + SICHER + '), {BedingungPunkt: 0, BedingungWert: ""}));\n'
                 '        IfError(Patch(RG_Pruefpunkte, LookUp(RG_Pruefpunkte, ID = varAuswahlID' + SICHER + '), {KategorieID: ziel, RgReihenfolge: Coalesce(Max(Filter(colP, KategorieID = ziel), RgReihenfolge), 0) + 10, BedingungPunkt: 0, BedingungWert: ""}), Set(varPatchFehler, true));\n'
                 '        ClearCollect(colP, Filter(RG_Pruefpunkte, RundgangID = varRgID && Fassung = varFassung));\n'
                 '        If(varPatchFehler,\n'
                 '            Notify("Verschieben hat nicht geklappt.", NotificationType.Error),\n'
                 '            Notify("Verschoben (ans Ende der Kategorie)." & If(abh > 0, " " & abh & " Bedingung(en), die auf diese Frage zeigten, wurden entfernt.", ""), NotificationType.Success)\n'
                 '        );\n'
                 '        ' + ind(sel("3", "varAuswahlID", "LookUp(colK, ID = ziel).BereichID", "ziel"), 8) + '\n'
                 '    ))\n'
                 ')')
K_VERSCHIEBEN = ('If(!IsBlank(Self.Selected) && Self.Selected.ID <> ' + CURK + '.BereichID && varSchreibbar,\n'
                 '    ' + ind(CHECK, 4) + ';\n    If(varEntwurfOk,\n'
                 '    With({ziel: Self.Selected.ID},\n'
                 '        Set(varPatchFehler, false);\n'
                 '        IfError(Patch(RG_Kategorien, LookUp(RG_Kategorien, ID = varAuswahlID' + SICHER + '), {BereichID: ziel, RgReihenfolge: Coalesce(Max(Filter(colK, BereichID = ziel), RgReihenfolge), 0) + 10}), Set(varPatchFehler, true));\n'
                 '        ClearCollect(colK, Filter(RG_Kategorien, RundgangID = varRgID && Fassung = varFassung));\n'
                 '        If(varPatchFehler, Notify("Verschieben hat nicht geklappt.", NotificationType.Error), Notify("Verschoben (ans Ende des Bereichs).", NotificationType.Success));\n'
                 '        ' + ind(sel("2", "varAuswahlID", "ziel", "varAuswahlID"), 8) + '\n'
                 '    ))\n'
                 ')')

ZAHL_FELD = lambda feld, ctl: ('With({v: If(Trim(Self.Text) = "", Blank(), IfError(Value(Self.Text), Blank()))},\n'  # noqa: E731
                               '    If(Trim(Self.Text) <> "" && IsBlank(v),\n'
                               '        Notify("Bitte eine Zahl eingeben.", NotificationType.Warning);\n'
                               '        Reset(' + ctl + '),\n'
                               '        Text(v) <> Text(' + CUR + '.' + feld + '),\n'
                               '        ' + ind(PP('{' + feld + ': v}'), 8) + '\n'
                               '    )\n'
                               ')')

ist_typ = lambda *t: "(" + " || ".join('%s.Eingabetyp.Value = "%s"' % (CUR, x) for x in t) + ")"  # noqa: E731
REST_Y = 'If(%s, 360, %s, 350, 232)' % (ist_typ("ZAHL"), ist_typ("AUSWAHL", "MEHRFACH"))


ed_p = con("conEdP", {"X": "16", "Y": "56", "Width": "528", "Height": "Parent.Height - 56", "Fill": "clrHintergrund",
                      "Visible": "varAuswahlEbene = 3"}, [
    lbl("lblPFrage", '"Frage"', "0", "0", "528", "20", size=12, color="clrTextGrau"),
    txt("txtPFrage", 'Coalesce(%s.Title, "")' % CUR,
        'If(Trim(Self.Text) = "",\n    Reset(txtPFrage),\n    Self.Text <> %s.Title,\n    %s\n)' % (CUR, ind(PP('{Title: Left(Trim(Self.Text), 255)}'), 4)),
        "0", "20", "528", "40", '"Frage, z. B. Lager sauber?"', '"Frage des Prüfpunkts"'),
    lbl("lblPTyp", '"Was tut der Prüfer?"', "0", "68", "528", "20", size=12, color="clrTextGrau"),
    optionen("galPTyp", TYP_ITEMS, CUR + ".Eingabetyp.Value",
             'If(ThisItem.W <> %s.Eingabetyp.Value,\n    %s\n)' % (CUR, ind(PP('{Eingabetyp: {Value: ThisItem.W}}'), 4)),
             "0", "88", "528", 4, '"Eingabetyp"', h=36, size=12, zeilen=2),
    lbl("lblPPflicht", '"Antwort"', "0", "168", "256", "20", size=12, color="clrTextGrau"),
    optionen("galPPflicht", 'Table({W: "ja", N: "Pflicht"}, {W: "nein", N: "freiwillig"})', 'If(Coalesce(%s.Pflicht, false), "ja", "nein")' % CUR,
             'If((ThisItem.W = "ja") <> Coalesce(%s.Pflicht, false),\n    %s\n)' % (CUR, ind(PP('{Pflicht: ThisItem.W = "ja"}'), 4)),
             "0", "188", "256", 2, '"Pflicht"', h=36, size=13),
    lbl("lblPKomm", '"Kommentar Pflicht"', "272", "168", "256", "20", size=12, color="clrTextGrau"),
    optionen("galPKomm", 'Table({W: "mangel", N: "bei Mangel"}, {W: "immer", N: "immer"})', 'If(Coalesce(%s.KommentarPflicht, false), "immer", "mangel")' % CUR,
             'If((ThisItem.W = "immer") <> Coalesce(%s.KommentarPflicht, false),\n    %s\n)' % (CUR, ind(PP('{KommentarPflicht: ThisItem.W = "immer"}'), 4)),
             "272", "188", "256", 2, '"Kommentar"', h=36, size=13),
    con("conPZahl", {"X": "0", "Y": "232", "Width": "528", "Height": "120", "Fill": "clrHintergrund", "Visible": ist_typ("ZAHL")}, [
        lbl("lblPEinheit", '"Einheit"', "0", "0", "140", "20", size=12, color="clrTextGrau"),
        lbl("lblPMin", '"i.O. ab"', "152", "0", "120", "20", size=12, color="clrTextGrau"),
        lbl("lblPMax", '"i.O. bis"', "284", "0", "120", "20", size=12, color="clrTextGrau"),
        txt("txtPEinheit", 'Coalesce(%s.Einheit, "")' % CUR,
            'If(Trim(Self.Text) <> Coalesce(%s.Einheit, ""),\n    %s\n)' % (CUR, ind(PP('{Einheit: Trim(Self.Text)}'), 4)),
            "0", "20", "140", "36", '"z. B. °C"', '"Einheit"'),
        txt("txtPMin", 'If(IsBlank(%s.MinWert), "", Text(%s.MinWert))' % (CUR, CUR), ZAHL_FELD("MinWert", "txtPMin"),
            "152", "20", "120", "36", '"leer = keine"', '"Untere Grenze"', zahl=True),
        txt("txtPMax", 'If(IsBlank(%s.MaxWert), "", Text(%s.MaxWert))' % (CUR, CUR), ZAHL_FELD("MaxWert", "txtPMax"),
            "284", "20", "120", "36", '"leer = keine"', '"Obere Grenze"', zahl=True),
        lbl("lblPGrenz", '"Wert außerhalb der Grenzen ergibt"', "0", "62", "528", "20", size=12, color="clrTextGrau"),
        optionen("galPGrenz", 'Table({W: "Mangel", N: "Mangel"}, {W: "Warnen", N: "Hinweis + Grund"}, {W: "Sperren", N: "nicht speicherbar"})',
                 'fnGrenzmodus(%s.Grenzmodus.Value)' % CUR,
                 'If(ThisItem.W <> fnGrenzmodus(%s.Grenzmodus.Value),\n    %s\n)' % (CUR, ind(PP('{Grenzmodus: {Value: ThisItem.W}}'), 4)),
                 "0", "82", "528", 3, '"Grenzmodus"', h=36, size=12),
    ]),
    con("conPWerte", {"X": "0", "Y": "232", "Width": "528", "Height": "110", "Fill": "clrHintergrund", "Visible": ist_typ("AUSWAHL", "MEHRFACH")}, [
        lbl("lblPWerte", '"Antwortmöglichkeiten – eine pro Zeile"', "0", "0", "528", "20", size=12, color="clrTextGrau"),
        txt("txtPWerte", 'Concat(Filter(Split(Coalesce(%s.Auswahlwerte, ""), ";"), Trim(Value) <> "") As s, Trim(s.Value), Char(10))' % CUR,
            'With({neu: Concat(Filter(ForAll(Split(Substitute(Self.Text, Char(13), ""), Char(10)) As z, {W: Trim(Substitute(z.Value, ";", ","))}), W <> "") As w, w.W, ";")},\n'
            '    If(neu <> Coalesce(%s.Auswahlwerte, ""),\n        %s\n    )\n)' % (CUR, ind(PP('{Auswahlwerte: neu}'), 8)),
            "0", "20", "528", "86", '"gut" & Char(10) & "mäßig" & Char(10) & "schlecht"', '"Antwortmöglichkeiten, eine pro Zeile"', multi=True),
    ]),
    con("conPRest", {"X": "0", "Y": REST_Y, "Width": "528", "Height": "250", "Fill": "clrHintergrund"}, [
        lbl("lblPFoto", '"Foto"', "0", "0", "528", "20", size=12, color="clrTextGrau"),
        dd("ddPFoto", FOTO_ITEMS, "N", 'LookUp(%s, W = %s).N' % (FOTO_ITEMS, FOTO_IST),
           'If(!IsBlank(Self.Selected) && Self.Selected.W <> %s,\n    %s\n)' % (FOTO_IST, ind(PP('{Foto: {Value: Self.Selected.W}}'), 4)),
           "0", "20", "528", "36", '"Foto-Regel"'),
        lbl("lblPBed", 'If(%s, "Keine Bedingung möglich: Andere Fragen hängen von dieser ab.", "Nur zeigen, wenn …")' % BED_GESPERRT,
            "0", "62", "528", "20", size=12, color="clrTextGrau"),
        dd("ddPBedA", BED_A_ITEMS, "N",
           'If(Coalesce(%s.BedingungPunkt, 0) = 0, "— immer zeigen —", ' % CUR + BED_A_UNG + ', ' + BED_A_UNG_N + ', With({a: LookUp(colP, ID = ' + CUR + '.BedingungPunkt)}, ' + A_N("a") + '))',
           BED_A_CHANGE, "0", "82", "300", "36", '"Bedingung: Frage"',
           DisplayMode='If(varSchreibbar && !varIsLoading && !%s, DisplayMode.Edit, DisplayMode.Disabled)' % BED_GESPERRT),
        dd("ddPBedW", BED_W_ITEMS, "N", 'Coalesce(LookUp(' + BED_W_ITEMS + ', fnBedNorm(W) = fnBedNorm(%s.BedingungWert)).N, fnBedText(%s.BedingungWert))' % (CUR, CUR),
           'If(!IsBlank(Self.Selected) && fnBedNorm(Self.Selected.W) <> fnBedNorm(%s.BedingungWert),\n    %s\n)' % (CUR, ind(PP('{BedingungWert: Self.Selected.W}'), 4)),
           "312", "82", "216", "36", '"Bedingung: Wert"', Visible='Coalesce(%s.BedingungPunkt, 0) <> 0' % CUR),
        lbl("lblPHinweis", '"Hinweis für den Prüfer"', "0", "124", "340", "20", size=12, color="clrTextGrau"),
        txt("txtPHinweis", 'Coalesce(%s.Hinweis, "")' % CUR,
            'If(Self.Text <> Coalesce(%s.Hinweis, ""),\n    %s\n)' % (CUR, ind(PP('{Hinweis: Self.Text}'), 4)),
            "0", "144", "340", "44", '"optional, z. B. Wo steht das Thermometer?"', '"Hinweis"', multi=True, Size="13"),
        lbl("lblPBild", '"Beispielbild"', "352", "124", "176", "20", size=12, color="clrTextGrau"),
        btn("btnPBild", 'If(Coalesce(%s.HinweisBildID, 0) > 0, "Bild ändern", "Bild wählen")' % CUR, "352", "144", "124", "44",
            "Set(varBildOffen, true)", art="sekundaer", size=13, DisplayMode=EDIT.replace("DisplayMode.View", "DisplayMode.Disabled")),
        C("imgPBild", "Image@2.2.3", {"X": "484", "Y": "144", "Width": "44", "Height": "44", "ImagePosition": "ImagePosition.Fill",
                                      "AccessibleLabel": '"Gewähltes Beispielbild"',
                                      "Image": 'If(varAuswahlEbene = 3 && Coalesce(%s.HinweisBildID, 0) > 0, LookUp(RG_Hinweisbilder, ID = %s.HinweisBildID).Thumbnail.Small)' % (CUR, CUR)}),
        lbl("lblPKat", '"Gehört zur Kategorie"', "0", "194", "528", "20", size=12, color="clrTextGrau"),
        dd("ddPKategorie", KAT_ITEMS, "N",
           'With({k: LookUp(colK, ID = %s.KategorieID)}, ' % CUR + KAT_N("k") + ')',
           P_VERSCHIEBEN, "0", "214", "528", "36", '"Kategorie (verschieben)"'),
    ]),
])

ed_b = con("conEdB", {"X": "16", "Y": "56", "Width": "528", "Height": "Parent.Height - 56", "Fill": "clrHintergrund", "Visible": "varAuswahlEbene = 1"}, [
    lbl("lblBName", '"Name des Bereichs"', "0", "0", "528", "20", size=12, color="clrTextGrau"),
    txt("txtBName", 'Coalesce(%s.Title, "")' % CURB,
        'If(Trim(Self.Text) = "",\n    Reset(txtBName),\n    Self.Text <> %s.Title,\n    %s\n)' % (CURB, ind(patch_feld("RG_Bereiche", "colB", '{Title: Left(Trim(Self.Text), 255)}'), 4)),
        "0", "20", "528", "40", '"z. B. Lagerhalle"', '"Name des Bereichs"'),
    lbl("lblBInfo", '"Enthält " & CountRows(Filter(colK, BereichID = varAuswahlID)) & " Kategorien und " & CountRows(Filter(colP, KategorieID in Filter(colK, BereichID = varAuswahlID).ID)) & " Prüfpunkte." & Char(10) & Char(10) & '
        '"Ein Bereich ist eine Überschrift im Rundgang (z. B. „Lagerhalle“). Darin liegen die Kategorien. Neue Kategorie: links „+ Kategorie“."',
        "0", "76", "528", "120", size=13, color="clrTextGrau", VerticalAlign="VerticalAlign.Top"),
])

ed_k = con("conEdK", {"X": "16", "Y": "56", "Width": "528", "Height": "Parent.Height - 56", "Fill": "clrHintergrund", "Visible": "varAuswahlEbene = 2"}, [
    lbl("lblKName", '"Name der Kategorie"', "0", "0", "528", "20", size=12, color="clrTextGrau"),
    txt("txtKName", 'Coalesce(%s.Title, "")' % CURK,
        'If(Trim(Self.Text) = "",\n    Reset(txtKName),\n    Self.Text <> %s.Title,\n    %s\n)' % (CURK, ind(patch_feld("RG_Kategorien", "colK", '{Title: Left(Trim(Self.Text), 255)}'), 4)),
        "0", "20", "528", "40", '"z. B. Teilelager"', '"Name der Kategorie"'),
    lbl("lblKBereich", '"Gehört zum Bereich"', "0", "72", "528", "20", size=12, color="clrTextGrau"),
    dd("ddKBereich", 'Sort(ForAll(colB As b, {ID: b.ID, N: b.Title & If(CountRows(Filter(colB As x, x.Title = b.Title)) > 1, " (#" & b.ID & ")", ""), S: Text(b.RgReihenfolge, "000000") & Text(b.ID, "000000")}), S)', "N",
       'With({b: LookUp(colB, ID = %s.BereichID)}, b.Title & If(CountRows(Filter(colB As x, x.Title = b.Title)) > 1, " (#" & b.ID & ")", ""))' % CURK, K_VERSCHIEBEN, "0", "92", "528", "36", '"Bereich (verschieben)"'),
    lbl("lblKInfo", 'CountRows(Filter(colP, KategorieID = varAuswahlID)) & " Prüfpunkte." & Char(10) & Char(10) & '
        '"Eine Kategorie ist eine Seite im Rundgang: Der Prüfer füllt sie aus und speichert sie als Ganzes. Die Kategorien werden der Reihe nach freigeschaltet. Neuer Prüfpunkt: links „+ Prüfpunkt“."',
        "0", "140", "528", "140", size=13, color="clrTextGrau", VerticalAlign="VerticalAlign.Top"),
])

ed_leer = con("conEdLeer", {"X": "16", "Y": "56", "Width": "528", "Height": "300", "Fill": "clrHintergrund", "Visible": "varAuswahlEbene = 0"}, [
    lbl("lblLeerHilfe", 'If(!varSchreibbar, "Links einen Bereich, eine Kategorie oder einen Prüfpunkt antippen.", IsEmpty(colB), '
        '"So geht es:" & Char(10) & "1. Links „+ Bereich“ (z. B. Lagerhalle)." & Char(10) & "2. „+ Kategorie“ (z. B. Teilelager) – eine Seite für den Prüfer." & Char(10) & '
        '"3. „+ Prüfpunkt“ oder „Mehrere Fragen …“ oder „Aus Vorlage holen …“." & Char(10) & "4. Rechts unten zeigt die Prüfung, was noch fehlt. Dann oben „Aktivieren“.", '
        '"Links einen Bereich, eine Kategorie oder einen Prüfpunkt antippen.")',
        "0", "0", "528", "240", size=14, color="clrText", VerticalAlign="VerticalAlign.Top"),
])

ed_leiste = con("conEdLeiste", {"X": "0", "Y": "0", "Width": "Parent.Width", "Height": "52", "Fill": "clrHintergrund", "Visible": "varAuswahlEbene > 0"}, [
    lbl("lblEdArt", 'If(Left(varFrage, 3) = "del", ' + ENTF_TEXT + ', Switch(varAuswahlEbene, 1, "Bereich", 2, "Kategorie", "Prüfpunkt"))',
        "16", "0", 'If(Left(varFrage, 3) = "del", 360, 130)', "52", size=16, bold=True,
        Color='If(Left(varFrage, 3) = "del", clrWarnung, clrText)', Size='If(Left(varFrage, 3) = "del", 12, 16)'),
    btn("btnEdHoch", '"↑"', "150", "6", "44", "40", schieben("-1"), art="sekundaer", size=16,
        Visible='varSchreibbar && Left(varFrage, 3) <> "del"'),
    btn("btnEdRunter", '"↓"', "200", "6", "44", "40", schieben("1"), art="sekundaer", size=16,
        Visible='varSchreibbar && Left(varFrage, 3) <> "del"'),
    btn("btnEdDupl", '"Duplizieren"', "252", "6", "120", "40", DUPLIZIEREN, art="sekundaer", size=13,
        Visible='varSchreibbar && Left(varFrage, 3) <> "del"'),
    btn("btnEdEntf", 'If(varFrage = ' + DEL_KEY + ', "Ja, entfernen", "Entfernen")', "384", "6", "160", "40", ENTFERNEN, art="gefahr", size=13,
        Visible="varSchreibbar"),
])

# rechte Spalte: Vorschau und Prüfung
VS_REGELN = ('"• " & If(Coalesce(%(c)s.Pflicht, false), "Pflichtfrage", "freiwillig") & Char(10) & "• " & fnFotoText(%(f)s) & Char(10) & '
             '"• Kommentar " & If(Coalesce(%(c)s.KommentarPflicht, false), "immer Pflicht", "Pflicht bei Mangel") & '
             'If(%(c)s.Eingabetyp.Value = "ZAHL", Char(10) & "• " & fnGrenzText(%(c)s.MinWert, %(c)s.MaxWert, %(c)s.Einheit) & If(IsBlank(%(c)s.MinWert) && IsBlank(%(c)s.MaxWert), "", ", außerhalb: " & '
             'Switch(fnGrenzmodus(%(c)s.Grenzmodus.Value), "Warnen", "Hinweis + Begründung", "Sperren", "nicht speicherbar", "Mangel")), "") & '
             'If(Coalesce(%(c)s.BedingungPunkt, 0) <> 0, Char(10) & "• nur sichtbar, wenn „" & LookUp(colP, ID = %(c)s.BedingungPunkt).Title & "“ = " & fnBedText(%(c)s.BedingungWert), "") & '
             'If(Coalesce(%(c)s.HinweisBildID, 0) > 0, Char(10) & "• mit Beispielbild", "")') % {"c": CUR, "f": FOTO_IST}

vs_karte = con("conVsKarte", dict({"X": "16", "Y": "40", "Width": "Parent.Width - 32", "Height": "300", "Fill": "clrKarte", "BorderColor": "clrRahmen",
                                   "BorderThickness": "1", "Visible": "varAuswahlEbene = 3"}, **radius(8)), [
    lbl("lblVsFrage", '%s.Title & If(Coalesce(%s.Pflicht, false), " *", "")' % (CUR, CUR), "16", "8", "Parent.Width - 32", "44", size=15, bold=True),
    lbl("lblVsHinweis", 'Coalesce(%s.Hinweis, "")' % CUR, "16", "52", "Parent.Width - 32", "22", size=12, color="clrTextGrau", Wrap="false"),
    btn("btnVsIO", '"i.O."', "16", "80", "120", "44", "false", art="sekundaer", DisplayMode="DisplayMode.Disabled",
        DisabledFill="clrErfolgHell", DisabledColor="clrErfolg", DisabledBorderColor="clrErfolg", Visible=ist_typ("IONIO")),
    btn("btnVsNIO", '"n.i.O."', "144", "80", "120", "44", "false", art="sekundaer", DisplayMode="DisplayMode.Disabled",
        DisabledFill="clrFehlerHell", DisabledColor="clrFehler", DisabledBorderColor="clrFehler", Visible=ist_typ("IONIO")),
    txt("txtVsWert", '""', "false", "16", "80", 'If(%s, 160, Parent.Width - 32)' % ist_typ("ZAHL"), "44", 'If(%s, "Wert", "Eingabe")' % ist_typ("ZAHL"),
        '"Vorschau Eingabe"', DisplayMode="DisplayMode.Disabled", Visible=ist_typ("ZAHL", "TEXT")),
    lbl("lblVsEinheit", 'Coalesce(%s.Einheit, "")' % CUR, "184", "80", "Parent.Width - 200", "44", size=14, Visible=ist_typ("ZAHL")),
    dd("ddVsAuswahl", 'Filter(Split(Coalesce(%s.Auswahlwerte, ""), ";"), Trim(Value) <> "")' % CUR, "Value", '""', "false", "16", "80",
       "Parent.Width - 32", "44", '"Vorschau Auswahl"', DisplayMode="DisplayMode.Edit", AllowEmptySelection="true", Visible=ist_typ("AUSWAHL")),
    lbl("lblVsMehr", 'Concat(Filter(Split(Coalesce(%s.Auswahlwerte, ""), ";"), Trim(Value) <> "") As s, "☐ " & Trim(s.Value), Char(10))' % CUR,
        "16", "80", "Parent.Width - 32", "84", size=13, VerticalAlign="VerticalAlign.Top", Visible=ist_typ("MEHRFACH")),
    lbl("lblVsDatum", '"📅 TT.MM.JJJJ" & If(%s, "     🕒 hh : mm", "")' % ist_typ("DATUMZEIT"), "16", "80", "Parent.Width - 32", "44", size=14,
        Visible=ist_typ("DATUM", "DATUMZEIT")),
    lbl("lblVsRegeln", VS_REGELN, "16", "170", "Parent.Width - 32", "124", size=12, color="clrTextGrau", VerticalAlign="VerticalAlign.Top"),
])

ed_rechts = con("conEdRechts", {"X": "940", "Y": "64", "Width": "Parent.Width - 940", "Height": "Parent.Height - 64", "Fill": "clrKarte",
                                "BorderColor": "clrRahmen", "BorderThickness": "1"}, [
    lbl("lblVsTitel", 'Switch(varAuswahlEbene, 3, "Vorschau – so sieht es der Prüfer", 2, "Diese Seite enthält", 1, "Dieser Bereich enthält", "Vorschau")',
        "16", "6", "Parent.Width - 32", "30", size=14, bold=True),
    vs_karte,
    lbl("lblVsListe", 'If(varAuswahlEbene = 2, Concat(Sort(Filter(colP, KategorieID = varAuswahlID), RgReihenfolge * 1000000 + ID) As p, "• " & p.Title & "  (" & fnTypName(p.Eingabetyp.Value) & If(Coalesce(p.Pflicht, false), ", Pflicht", "") & If(Coalesce(p.BedingungPunkt, 0) <> 0, ", bedingt", "") & ")", Char(10)), '
        'varAuswahlEbene = 1, Concat(Sort(Filter(colK, BereichID = varAuswahlID), RgReihenfolge * 1000000 + ID) As k, "• " & k.Title & "  (" & CountRows(Filter(colP, KategorieID = k.ID)) & " Prüfpunkte)", Char(10)), '
        '"Links etwas antippen.")',
        "16", "40", "Parent.Width - 32", "300", size=13, VerticalAlign="VerticalAlign.Top", Overflow="Overflow.Scroll",
        Visible="varAuswahlEbene <> 3"),
    lbl("lblPrTitel", '"Prüfung: " & If(' + FEHLER_ANZ + ' = 0, "keine Fehler", ' + FEHLER_ANZ + ' & " Fehler") & If(' + HINWEIS_ANZ + ' > 0, ", " & ' + HINWEIS_ANZ + ' & " Hinweise", "")',
        "16", "350", "Parent.Width - 32", "30", size=14, bold=True, Color='If(' + FEHLER_ANZ + ' > 0, clrFehler, clrErfolg)'),
    gal("galPr", PRUEF_ITEMS, "16", "384", "Parent.Width - 32", "Parent.Height - 392", 52, [
        lbl("lblPrPunkt", '"●"', "0", "0", "20", "Parent.TemplateHeight", size=12, Color='If(ThisItem.Art = "Fehler", clrFehler, clrWarnung)'),
        lbl("lblPrText", "ThisItem.Text", "22", "0", "Parent.TemplateWidth - 26", "Parent.TemplateHeight", size=12),
        btn("btnPrZeile", '""', "0", "0", "Parent.TemplateWidth", "Parent.TemplateHeight", "If(!varIsLoading && ThisItem.Ebene > 0,\n    " + ind(SPRUNG, 4) + "\n)",
            art="kopf", Fill="RGBA(0, 0, 0, 0)", HoverFill="RGBA(23, 20, 150, 0.06)", PressedFill="RGBA(23, 20, 150, 0.12)",
            DisabledFill="RGBA(0, 0, 0, 0)", **radius(0)),
    ], '"Prüfung des Rundgangs"'),
    lbl("lblPrLeer", '"Alles in Ordnung ✓"', "16", "384", "Parent.Width - 32", "40", size=13, color="clrErfolg", Visible="IsEmpty(galPr.AllItems)"),
])

# linke Spalte: Gliederung
ed_links = con("conEdGl", {"X": "0", "Y": "64", "Width": "380", "Height": "Parent.Height - 64", "Fill": "clrKarte",
                           "BorderColor": "clrRahmen", "BorderThickness": "1"}, [
    lbl("lblGlTitel", '"Gliederung"', "16", "6", "200", "28", size=15, bold=True),
    lbl("lblGlHilfe", '"Antippen zum Bearbeiten. Prüfpunkte erscheinen unter der gewählten Kategorie."', "16", "32", "348", "34", size=11, color="clrTextGrau"),
    gal("galGl", baum_items("colB", "colK", "colP", True), "0", "68", "Parent.Width", "Parent.Height - 68 - If(varSchreibbar, 108, 0)", 40,
        baum_zeilen("Gl", GL_GEWAEHLT, GL_SELECT, GL_INFO, GL_FEHLER), '"Gliederung des Rundgangs"'),
    con("conGlFuss", {"X": "0", "Y": "Parent.Height - 108", "Width": "Parent.Width", "Height": "108", "Fill": "clrKarte", "Visible": "varSchreibbar"}, [
        btn("btnGlNeuB", '"+ Bereich"', "12", "8", "104", "40", NEU_B, size=13),
        btn("btnGlNeuK", '"+ Kategorie"', "122", "8", "120", "40", NEU_K, size=13,
            DisplayMode="If(varIsLoading || varCtxB = 0, DisplayMode.Disabled, DisplayMode.Edit)"),
        btn("btnGlNeuP", '"+ Prüfpunkt"', "248", "8", "120", "40", NEU_P, size=13,
            DisplayMode="If(varIsLoading || varCtxK = 0, DisplayMode.Disabled, DisplayMode.Edit)"),
        btn("btnGlMehrere", '"Mehrere Fragen"', "12", "56", "172", "40",
            "If(" + FREI + " && varCtxK > 0,\n    Set(varMehrTyp, \"IONIO\");\n    Set(varMehrPflicht, true);\n    Reset(txtMehr);\n    Set(varMehrereOffen, true),\n    varCtxK = 0,\n    Notify(\"Links zuerst eine Kategorie antippen.\", NotificationType.Warning)\n)",
            art="sekundaer", size=13),
        btn("btnGlHolen", '"Aus Vorlage holen"', "192", "56", "176", "40",
            "If(" + FREI + ",\n    Set(varHolenOffen, true);\n    Reset(ddHolenQuelle);\n    " + ind(quelle_laden('LookUp(colRg, fnStatus(Status, Aktiv) = "Vorlage")'), 4) + "\n)",
            art="sekundaer", size=13),
    ]),
])

# Kopfzeile des Editors
AKT_OEFFNEN = ("If(" + FREI + ",\n"
               "    If(" + FEHLER_ANZ + " > 0,\n"
               "        Notify(\"Erst die \" & " + FEHLER_ANZ + " & \" Fehler beheben (rechts unten, rot).\", NotificationType.Warning),\n"
               "        Set(varIsLoading, true);\n"
               "        With({fa: If(fnStatus(varRg.Status, varRg.Aktiv) = \"Entwurf\", 0, fnAktiveFassung(varRg.Fassung))},\n"
               "            ClearCollect(colAltP, Filter(RG_Pruefpunkte, RundgangID = varRgID && Fassung = fa))\n"
               "        );\n"
               "        RemoveIf(colAltP, !Coalesce(Aktiv, false));\n"
               "        With({d: LookUp(RG_Durchfuehrungen, Title = \"R\" & varRgID & \"-\" & Text(Today(), \"yyyy-mm-dd\"))}, Set(varHeuteLaeuft, !IsBlank(d) && d.Status <> \"Abgeschlossen\"));\n"
               "        Set(varIsLoading, false);\n"
               "        Set(varAktivOffen, true)\n"
               "    )\n"
               ")")
NAME_AENDERN = ('If(varSchreibbar && Trim(Self.Text) <> "" && Self.Text <> varRg.Title,\n'
                '    If(!IsBlank(LookUp(colRg, ID <> varRgID && Lower(Trim(Title)) = Lower(Trim(Self.Text)))),\n'
                '        Notify("Diesen Namen gibt es schon.", NotificationType.Warning);\n'
                '        Reset(txtEdName),\n'
                '        Set(varPatchFehler, false);\n'
                '        IfError(Patch(RG_Rundgaenge, LookUp(RG_Rundgaenge, ID = varRgID), {Title: Left(Trim(Self.Text), 255)}), Set(varPatchFehler, true));\n'
                '        If(varPatchFehler, Notify("Name nicht gespeichert.", NotificationType.Error), Set(varRg, LookUp(RG_Rundgaenge, ID = varRgID)); Set(varGespeichertText, "Name gespeichert " & Text(Now(), "hh:mm:ss")); Notify("Der Name gilt sofort, auch für die aktive Fassung.", NotificationType.Information))\n'
                '    ),\n'
                '    Trim(Self.Text) = "",\n'
                '    Reset(txtEdName)\n'
                ')')
ED_STATUS = ('If(varAktivRest, "Aktivieren von Fassung " & varFassung & " unvollständig – bitte erneut aktivieren", varIstVorlage, "Vorlagen – Änderungen gelten sofort", varSchreibbar, "Entwurf Fassung " & varFassung & '
             'If(fnStatus(varRg.Status, varRg.Aktiv) = "Entwurf", " · noch nie aktiviert", " · aktiv ist Fassung " & fnAktiveFassung(varRg.Fassung)), '
             '"Ansicht der aktiven Fassung " & varFassung & " (nur lesen)") & Char(10) & varGespeichertText')

ed_kopf = con("conEdKopf", {"Fill": "clrPrimaer", "Width": "Parent.Width", "Height": "64"}, [
    btn("btnEdZurueck", '"← Übersicht"', "16", "12", "140", "40",
        "If(!varIsLoading,\n    Set(varFrage, \"\");\n    Navigate(scrListe, ScreenTransition.None)\n)", art="kopf"),
    txt("txtEdName", "varRg.Title", NAME_AENDERN, "168", "12", "360", "40", '"Name des Rundgangs"', '"Name des Rundgangs"',
        Visible="varSchreibbar && !varIstVorlage", Size="15"),
    lbl("lblEdName", "varRg.Title", "168", "12", "360", "40", size=17, color="Color.White", bold=True, Visible="!(varSchreibbar && !varIstVorlage)"),
    lbl("lblEdStatus", ED_STATUS, "540", "4", "420", "56", size=12, color="Color.White"),
    lbl("lblEdPruefZahl", 'If(' + FEHLER_ANZ + ' > 0, ' + FEHLER_ANZ + ' & " Fehler", "keine Fehler")', "Parent.Width - 400", "12", "180", "40",
        size=13, color="Color.White", Align="Align.Right", Visible="(varSchreibbar && !varIstVorlage) || varAktivRest"),
    btn("btnEdAktivieren", '"Aktivieren …"', "Parent.Width - 206", "12", "190", "40", AKT_OEFFNEN, art="sekundaer",
        Visible="(varSchreibbar && !varIstVorlage) || varAktivRest", Fill='If(' + FEHLER_ANZ + ' > 0, clrGesperrtHell, clrKarte)',
        Color='If(' + FEHLER_ANZ + ' > 0, clrTextGrau, clrPrimaer)'),
    btn("btnEdBearbeiten", '"Neue Fassung bearbeiten"', "Parent.Width - 286", "12", "270", "40",
        "If(" + FREI + ",\n    " + LOCK + ";\n    Set(varSchreibbar, true);\n    Set(varJob, \"neueFassung\");\n    Set(varIsLoading, true);\n    Set(varArbeitStart, true)\n)",
        art="sekundaer", Visible='!varSchreibbar && !varAktivRest && fnStatus(varRg.Status, varRg.Aktiv) <> "Entwurf"'),
])

# Fenster: Aktivieren
AKT_N = lambda art: 'CountRows(Filter(galAkt.AllItems, Art = "%s"))' % art  # noqa: E731
con_akt = overlay("conAkt", "varAktivOffen", 680, 600, [
    lbl("lblAktText", 'If(fnStatus(varRg.Status, varRg.Aktiv) = "Entwurf", "Erste Fassung: " & CountRows(colB) & " Bereiche, " & CountRows(colK) & " Kategorien, " & CountRows(colP) & " Prüfpunkte.", '
        '"Gegenüber der aktiven Fassung " & fnAktiveFassung(varRg.Fassung) & ": " & ' + AKT_N("neu") + ' & " neu, " & ' + AKT_N("geändert") + ' & " geändert, " & ' + AKT_N("entfernt") + ' & " entfernt (Prüfpunkte).")',
        "24", "64", "632", "48", size=14),
    gal("galAkt", AKT_ITEMS, "24", "116", "632", "220", 30, [
        lbl("lblAktArt", "ThisItem.Art", "0", "0", "96", "30", size=12, bold=True,
            Color='Switch(ThisItem.Art, "neu", clrErfolg, "entfernt", clrFehler, clrWarnung)'),
        lbl("lblAktZeile", "ThisItem.Text", "100", "0", "Parent.TemplateWidth - 104", "30", size=12, Wrap="false"),
    ], '"Änderungen"', Visible='fnStatus(varRg.Status, varRg.Aktiv) <> "Entwurf"'),
    lbl("lblAktHinweise",
        '"• Ab dem nächsten Start eines Rundgangs gilt die neue Fassung." & '
        'If(fnStatus(varRg.Status, varRg.Aktiv) = "Archiviert", Char(10) & "• Der Rundgang ist archiviert und wird damit wieder aktiv.", "") & '
        'If(varHeuteLaeuft, Char(10) & "• Heute läuft noch ein Rundgang mit der alten Fassung. Er wird mit der alten Fassung beendet.", "") & '
        'If(IsEmpty(Filter(colPlanR, Coalesce(Aktiv, false))), Char(10) & "• Es gibt noch keinen aktiven Plan: Der Rundgang erscheint erst auf der Startseite, wenn du einen Plan anlegst.", "") & '
        'If(' + HINWEIS_ANZ + ' > 0, Char(10) & "• Die Prüfung zeigt " & ' + HINWEIS_ANZ + ' & " Hinweis(e). Sie verhindern das Aktivieren nicht.", "")',
        "24", "344", "632", "160", size=13, color="clrText", VerticalAlign="VerticalAlign.Top"),
    btn("btnAktAbbrechen", '"Abbrechen"', "24", "528", "180", "48", "Set(varAktivOffen, false)", art="sekundaer"),
    btn("btnAktJetzt", '"Jetzt aktivieren"', "456", "528", "200", "48",
        "If(" + FREI + ",\n    " + LOCK + ";\n    Set(varAktivOffen, false);\n    Set(varJob, \"aktivieren\");\n    Set(varIsLoading, true);\n    Set(varArbeitStart, true)\n)"),
], '"Fassung " & varFassung & " aktivieren"', "Set(varAktivOffen, false)")

# Fenster: Aus Vorlage oder anderem Rundgang holen
HOLEN = ("If(" + FREI + " && varHolenID > 0 && varSchreibbar,\n"
         "    " + LOCK + ";\n"
         "    " + ind(CHECK, 4) + ";\n"
         "    If(!varEntwurfOk,\n        Set(varHolenOffen, false),\n        varHolenEbene = 3 && varCtxK = 0,\n"
         "        Notify(\"Links zuerst eine Kategorie antippen, in die der Prüfpunkt soll.\", NotificationType.Warning),\n"
         "        varHolenEbene = 2 && varCtxB = 0,\n"
         "        Notify(\"Links zuerst einen Bereich antippen, in den die Kategorie soll.\", NotificationType.Warning),\n"
         "        ClearCollect(colQB, Filter(colSrcB, varHolenEbene = 1 && ID = varHolenID));\n"
         "        ClearCollect(colQK, Filter(colSrcK, (varHolenEbene = 2 && ID = varHolenID) || (varHolenEbene = 1 && BereichID = varHolenID)));\n"
         "        ClearCollect(colQP, Filter(colSrcP, (varHolenEbene = 3 && ID = varHolenID) || KategorieID in colQK.ID));\n"
         "        Set(varZielR, varRgID);\n        Set(varZielF, varFassung);\n        Set(varZielB, varCtxB);\n        Set(varZielK, varCtxK);\n"
         "        Set(varZielBAktiv, false);\n        Set(varKopieBehalteR, false);\n        Set(varKopieZusatz, \"\");\n"
         "        Set(varKopieNach, \"auswahl\");\n        Set(varJob, \"kopie\");\n        Set(varIsLoading, true);\n        Set(varArbeitStart, true)\n"
         "    )\n"
         ")")
HOLEN_ZIEL = ('Switch(varHolenEbene, 3, If(varCtxK > 0, "Ziel: Kategorie „" & LookUp(colK, ID = varCtxK).Title & "“ (ans Ende)", "Ziel fehlt: links zuerst eine Kategorie antippen"), '
              '2, If(varCtxB > 0, "Ziel: Bereich „" & LookUp(colB, ID = varCtxB).Title & "“ (ans Ende)", "Ziel fehlt: links zuerst einen Bereich antippen"), '
              '1, "Ziel: dieser Rundgang (ans Ende)", "Unten einen Bereich, eine Kategorie oder einen Prüfpunkt antippen.")')
con_holen = overlay("conHolen", "varHolenOffen", 920, 640, [
    lbl("lblHolenQuelle", '"Woher?"', "24", "64", "420", "20", size=12, color="clrTextGrau"),
    dd("ddHolenQuelle", 'Sort(Filter(colRg, ID <> varRgID && (Coalesce(Fassung, 0) > 0 || fnStatus(Status, Aktiv) = "Entwurf" || fnStatus(Status, Aktiv) = "Vorlage")), '
       'If(fnStatus(Status, Aktiv) = "Vorlage", "0", "1") & Lower(Title))', "Title",
       'Coalesce(LookUp(colRg, fnStatus(Status, Aktiv) = "Vorlage").Title, "")',
       "If(!IsBlank(Self.Selected),\n    " + ind(quelle_laden("Self.Selected"), 4) + "\n)", "24", "84", "420", "40", '"Quelle: Vorlagen oder anderer Rundgang"',
       DisplayMode="DisplayMode.Edit"),
    lbl("lblHolenZiel", HOLEN_ZIEL, "460", "76", "436", "56", size=13, Color='If(StartsWith(Self.Text, "Ziel fehlt"), clrFehler, clrText)'),
    gal("galHolen", baum_items("colSrcB", "colSrcK", "colSrcP", False), "24", "140", "872", "400", 36,
        baum_zeilen("Ho", "ThisItem.Ebene = varHolenEbene && ThisItem.ID = varHolenID",
                    "Set(varHolenEbene, ThisItem.Ebene);\nSet(varHolenID, ThisItem.ID)", GL_INFO, None),
        '"Bausteine zum Übernehmen"'),
    lbl("lblHolenLeer", '"Hier ist nichts. Oben eine andere Quelle wählen. Vorlagen legst du in der Übersicht mit „Vorlagen bearbeiten“ an."',
        "24", "150", "872", "40", size=13, color="clrTextGrau", Visible="IsEmpty(galHolen.AllItems)"),
    btn("btnHolenSchliessen", '"Schließen"', "24", "568", "180", "48", "Set(varHolenOffen, false)", art="sekundaer"),
    btn("btnHolenUebernehmen", 'Switch(varHolenEbene, 1, "Bereich übernehmen", 2, "Kategorie übernehmen", 3, "Prüfpunkt übernehmen", "Übernehmen")',
        "636", "568", "260", "48", HOLEN, DisplayMode="If(varIsLoading || varHolenID = 0, DisplayMode.Disabled, DisplayMode.Edit)"),
], '"Aus Vorlage oder anderem Rundgang holen"', "Set(varHolenOffen, false)")

# Fenster: Mehrere Prüfpunkte
MEHR_N = 'CountRows(Filter(Split(Substitute(txtMehr.Text, Char(13), ""), Char(10)), Trim(Value) <> ""))'
MEHR_ANLEGEN = ("If(varSchreibbar && " + FREI + ",\n"
                "    " + LOCK + ";\n"
                "    ClearCollect(colMehr, Filter(ForAll(Split(Substitute(txtMehr.Text, Char(13), \"\"), Char(10)) As z, {F: Left(Trim(z.Value), 255)}), F <> \"\"));\n"
                "    " + ind(CHECK, 4) + ";\n"
                "    If(!varEntwurfOk,\n        Set(varMehrereOffen, false),\n        varCtxK = 0,\n"
                "        Notify(\"Links zuerst eine Kategorie antippen.\", NotificationType.Warning),\n"
                "        IsEmpty(colMehr),\n"
                "        Notify(\"Bitte mindestens eine Frage eintragen.\", NotificationType.Warning),\n"
                "        Set(varIsLoading, true);\n"
                "        ClearCollect(colMehrErg,\n"
                "            With({basis: Coalesce(Max(Filter(colP, KategorieID = varCtxK), RgReihenfolge), 0)},\n"
                "                ForAll(Sequence(CountRows(colMehr)) As i,\n"
                "                    {Neu: IfError(Patch(RG_Pruefpunkte, Defaults(RG_Pruefpunkte), {Title: Index(colMehr, i.Value).F, KategorieID: varCtxK, RundgangID: varRgID, Fassung: varFassung, RgReihenfolge: basis + i.Value * 10, "
                + NEUER_PUNKT.format(typ="varMehrTyp", pfl="varMehrPflicht") + "}).ID, 0)}\n"
                "                )\n"
                "            )\n"
                "        );\n"
                "        ClearCollect(colP, Filter(RG_Pruefpunkte, RundgangID = varRgID && Fassung = varFassung));\n"
                "        If(CountRows(Filter(colMehrErg, Neu = 0)) > 0,\n"
                "            Notify(CountRows(Filter(colMehrErg, Neu = 0)) & \" Fragen konnten nicht angelegt werden. Bitte die Gliederung prüfen.\", NotificationType.Error),\n"
                "            Notify(CountRows(colMehrErg) & \" Prüfpunkte angelegt.\", NotificationType.Success);\n"
                "            Reset(txtMehr);\n"
                "            Set(varMehrereOffen, false)\n"
                "        );\n"
                "        Set(varIsLoading, false)\n"
                "    )\n"
                ")")
con_mehr = overlay("conMehr", "varMehrereOffen", 660, 600, [
    lbl("lblMehrHilfe", '"Eine Frage pro Zeile. Du kannst auch eine Spalte aus Excel hineinkopieren."', "24", "64", "612", "22", size=13, color="clrTextGrau"),
    txt("txtMehr", '""', "false", "24", "90", "612", "250", '"Lager sauber?" & Char(10) & "Regale beschriftet?" & Char(10) & "Fluchtweg frei?"', '"Fragen, eine pro Zeile"',
        multi=True, DisplayMode="DisplayMode.Edit"),
    lbl("lblMehrTyp", '"Art für alle"', "24", "348", "300", "20", size=12, color="clrTextGrau"),
    optionen("galMehrTyp", 'Table({W: "IONIO", N: "i.O./n.i.O."}, {W: "ZAHL", N: "Zahl"}, {W: "TEXT", N: "Text"})', "varMehrTyp",
             "Set(varMehrTyp, ThisItem.W)", "24", "368", "612", 3, '"Art der neuen Prüfpunkte"', h=40, size=13, aktiv="DisplayMode.Edit"),
    lbl("lblMehrPfl", '"Antwort"', "24", "416", "300", "20", size=12, color="clrTextGrau"),
    optionen("galMehrPfl", 'Table({W: "ja", N: "Pflicht"}, {W: "nein", N: "freiwillig"})', 'If(varMehrPflicht, "ja", "nein")',
             'Set(varMehrPflicht, ThisItem.W = "ja")', "24", "436", "408", 2, '"Pflicht"', h=40, size=13, aktiv="DisplayMode.Edit"),
    lbl("lblMehrZiel", '"Ziel: Kategorie „" & LookUp(colK, ID = varCtxK).Title & "“ (ans Ende). Alles Weitere stellst du danach je Prüfpunkt ein."',
        "24", "484", "612", "40", size=12, color="clrTextGrau"),
    btn("btnMehrAbbrechen", '"Abbrechen"', "24", "532", "180", "48", "Set(varMehrereOffen, false)", art="sekundaer"),
    btn("btnMehrAnlegen", '"Anlegen (" & ' + MEHR_N + ' & ")"', "416", "532", "220", "48", MEHR_ANLEGEN),
], '"Mehrere Prüfpunkte anlegen"', "Set(varMehrereOffen, false)")

# Fenster: Beispielbild
con_bild = overlay("conBild", "varBildOffen", 980, 620, [
    gal("galBild", 'If(varBildOffen, Sort(RG_Hinweisbilder, ID, SortOrder.Descending), Filter(RG_Hinweisbilder, ID = -1))', "24", "64", "932", "460", 152, [
        C("imgBi", "Image@2.2.3", {"X": "6", "Y": "6", "Width": "Parent.TemplateWidth - 12", "Height": "110", "ImagePosition": "ImagePosition.Fit",
                                   "Image": "ThisItem.Thumbnail.Small", "AccessibleLabel": '"Bild " & ThisItem.ID'}),
        lbl("lblBi", '"Bild " & ThisItem.ID & If(ThisItem.ID = Coalesce(' + CUR + '.HinweisBildID, 0), "  ✓", "")', "6", "118", "Parent.TemplateWidth - 12", "28",
            size=12, Align="Align.Center"),
        btn("btnBi", '""', "0", "0", "Parent.TemplateWidth", "Parent.TemplateHeight",
            PP('{HinweisBildID: ThisItem.ID}') + ";\nSet(varBildOffen, false)", art="kopf",
            Fill="RGBA(0, 0, 0, 0)", HoverFill="RGBA(23, 20, 150, 0.08)", PressedFill="RGBA(23, 20, 150, 0.16)", DisabledFill="RGBA(0, 0, 0, 0)",
            BorderThickness='If(ThisItem.ID = Coalesce(' + CUR + '.HinweisBildID, 0), 3, 0)', BorderColor="clrPrimaer", **radius(0)),
    ], '"Beispielbilder"', wrap=6),
    lbl("lblBildLeer", '"Noch keine Bilder in RG_Hinweisbilder. „Bilder hochladen“ öffnet die Bibliothek, danach „Neu laden“."',
        "24", "80", "932", "40", size=13, color="clrTextGrau", Visible="IsEmpty(galBild.AllItems)"),
    btn("btnBildKeins", '"Kein Bild"', "24", "548", "160", "48", PP('{HinweisBildID: 0}') + ";\nSet(varBildOffen, false)", art="sekundaer"),
    btn("btnBildHochladen", '"Bilder hochladen ↗"', "196", "548", "220", "48", "Launch(cfgBildBibliothek)", art="sekundaer"),
    btn("btnBildNeuLaden", '"↻ Neu laden"', "428", "548", "160", "48", "Refresh(RG_Hinweisbilder)", art="sekundaer"),
    btn("btnBildSchliessen", '"Schließen"', "796", "548", "160", "48", "Set(varBildOffen, false)"),
], '"Beispielbild wählen (anklicken)"', "Set(varBildOffen, false)")

tmr_arbeit = C("tmrArbeit", "Timer@2.1.0", {"Duration": "100", "Start": "varArbeitStart", "OnTimerEnd": TIMER_ARBEIT, "Visible": "false",
                                            "X": "0", "Y": "0", "Width": "10", "Height": "10"})

scr_editor = C("scrEditor", "Screen", {
    "Fill": "clrHintergrund",
    "OnVisible": "Set(varAktivOffen, false);\nSet(varHolenOffen, false);\nSet(varMehrereOffen, false);\nSet(varBildOffen, false);\n"
                 "If(varJob <> \"\", Set(varIsLoading, true); Set(varArbeitStart, true))",
}, [
    ed_kopf,
    ed_links,
    con("conEdMitte", {"X": "380", "Y": "64", "Width": "560", "Height": "Parent.Height - 64", "Fill": "clrHintergrund"},
        [ed_leiste, ed_leer, ed_b, ed_k, ed_p]),
    ed_rechts,
    tmr_arbeit,
    con_akt, con_holen, con_mehr, con_bild,
    laden_overlay("conEdLaden"),
])


# ---------------------------------------------------------------- Bildschirm 3: Plan

def patch_plan(felder):
    return ("Set(varPatchFehler, false);\n"
            "IfError(Patch(RG_Plan, LookUp(RG_Plan, ID = ThisItem.ID), " + felder + "), Set(varPatchFehler, true));\n"
            "If(varPatchFehler,\n"
            "    Notify(\"Nicht gespeichert. Bitte erneut versuchen.\", NotificationType.Error),\n"
            "    Patch(colPlanR, LookUp(colPlanR, ID = ThisItem.ID), LookUp(RG_Plan, ID = ThisItem.ID))\n"
            ")")


TAGE = 'Table({W: 1, N: "Montag"}, {W: 2, N: "Dienstag"}, {W: 3, N: "Mittwoch"}, {W: 4, N: "Donnerstag"}, {W: 5, N: "Freitag"}, {W: 6, N: "Samstag"}, {W: 7, N: "Sonntag"})'
ZYKLEN = 'Table({W: 1, N: "jede Woche"}, {W: 2, N: "alle 2 Wochen"}, {W: 3, N: "alle 3 Wochen"}, {W: 4, N: "alle 4 Wochen"})'
PL_AKTIV = "Coalesce(ThisItem.Aktiv, false)"
TERMINE = ('FirstN(Filter(ForAll(Sequence(120, 0) As i, {D: DateAdd(Today(), i.Value, TimeUnit.Days)}), '
           'CountRows(Filter(colPlanR As p, Coalesce(p.Aktiv, false) && fnPlanPasst(p.StartMontag, p.GueltigBis, p.Wochentag, p.ZyklusWochen, D))) > 0), 12)')

pl_karte = con("conPlKarte", dict({"Fill": "If(%s, clrKarte, clrGesperrtHell)" % PL_AKTIV, "BorderColor": "clrRahmen", "BorderThickness": "1",
                                   "X": "0", "Y": "4", "Width": "Parent.TemplateWidth", "Height": "Parent.TemplateHeight - 8"}, **radius(8)), [
    dd("ddPlTag", TAGE, "N", "fnWochentag(ThisItem.Wochentag)",
       "If(!IsBlank(Self.Selected) && Self.Selected.W <> ThisItem.Wochentag,\n    " + ind(patch_plan('{Wochentag: Self.Selected.W, Title: Left(varPlanRg.Title & " – " & Self.Selected.N, 255)}'), 4) + "\n)",
       "16", "14", "180", "40", '"Wochentag"', DisplayMode=BTN_DM),
    dd("ddPlZyklus", ZYKLEN, "N", "fnZyklus(ThisItem.ZyklusWochen)",
       "If(!IsBlank(Self.Selected) && Self.Selected.W <> Coalesce(ThisItem.ZyklusWochen, 1),\n    " + ind(patch_plan('{ZyklusWochen: Self.Selected.W}'), 4) + "\n)",
       "204", "14", "190", "40", '"Rhythmus"', DisplayMode=BTN_DM),
    lbl("lblPlAb", '"ab"', "400", "14", "26", "40", size=13, color="clrTextGrau"),
    dp("dpPlStart", "ThisItem.StartMontag",
       "If(!IsBlank(Self.SelectedDate) && fnMontag(Self.SelectedDate) <> ThisItem.StartMontag,\n    " + ind(patch_plan('{StartMontag: fnMontag(Self.SelectedDate)}'), 4) + "\n)",
       "428", "14", "150", "40", '"Startwoche (es zählt der Montag)"'),
    lbl("lblPlBis", '"bis"', "584", "14", "30", "40", size=13, color="clrTextGrau"),
    dp("dpPlBis", "ThisItem.GueltigBis",
       "If(!IsBlank(Self.SelectedDate) && Self.SelectedDate <> ThisItem.GueltigBis,\n    " + ind(patch_plan('{GueltigBis: Self.SelectedDate}'), 4) + "\n)",
       "616", "14", "150", "40", '"Gültig bis (leer = unbegrenzt)"', InputTextPlaceholder='"unbegrenzt"'),
    btn("btnPlBisWeg", '"✕"', "770", "14", "36", "40",
        "If(!IsBlank(ThisItem.GueltigBis),\n    " + ind(patch_plan('{GueltigBis: Blank()}'), 4) + ";\n    Reset(dpPlBis)\n)", art="sekundaer", size=13),
    btn("btnPlAktiv", 'If(%s, "aktiv", "pausiert")' % PL_AKTIV, "814", "14", "100", "40", patch_plan('{Aktiv: !%s}' % PL_AKTIV),
        art="sekundaer", size=13, Fill='If(%s, clrErfolgHell, clrKarte)' % PL_AKTIV, Color='If(%s, clrErfolg, clrTextGrau)' % PL_AKTIV,
        BorderColor='If(%s, clrErfolg, clrRahmen)' % PL_AKTIV),
])

PL_NEU = ("If(" + FREI + ",\n"
          "    " + LOCK + ";\n"
          "    Set(varPatchFehler, false);\n"
          "    IfError(Patch(RG_Plan, Defaults(RG_Plan), {Title: Left(varPlanRg.Title & \" – Montag\", 255), RundgangID: varPlanRgID, Wochentag: 1, ZyklusWochen: 1, StartMontag: fnMontag(Today()), Aktiv: true}), Set(varPatchFehler, true));\n"
          "    ClearCollect(colPlanR, Filter(RG_Plan, RundgangID = varPlanRgID));\n"
          "    If(varPatchFehler, Notify(\"Anlegen fehlgeschlagen.\", NotificationType.Error))\n"
          ")")

scr_plan = C("scrPlan", "Screen", {
    "Fill": "clrHintergrund",
    "OnVisible": "Set(varIsLoading, true);\nSet(varLadeText, \"\");\nConcurrent(Refresh(RG_Plan), Refresh(RG_Rundgaenge));\n"
                 "Set(varPlanRg, LookUp(RG_Rundgaenge, ID = varPlanRgID));\nClearCollect(colPlanR, Filter(RG_Plan, RundgangID = varPlanRgID));\nSet(varIsLoading, false)",
}, [
    con("conPlKopf", {"Fill": "clrPrimaer", "Width": "Parent.Width", "Height": "64"}, [
        btn("btnPlZurueck", '"← Übersicht"', "16", "12", "140", "40", "If(!varIsLoading, Navigate(scrListe, ScreenTransition.None))", art="kopf"),
        lbl("lblPlTitel", '"Plan – " & varPlanRg.Title', "172", "0", "900", "64", size=20, color="Color.White", bold=True),
    ]),
    lbl("lblPlHinweis", '"Wann ist der Rundgang dran? Änderungen gelten sofort, auch für einen aktiven Rundgang." & '
        'If(!Coalesce(varPlanRg.Aktiv, false), " Der Rundgang ist nicht aktiv: Er erscheint erst nach dem Aktivieren auf der Startseite.", "")',
        "24", "72", "Parent.Width - 48", "44", size=13, color="clrTextGrau"),
    lbl("lblPlKopf1", '"Wochentag"', "40", "116", "180", "24", size=12, color="clrTextGrau"),
    lbl("lblPlKopf2", '"Rhythmus"', "228", "116", "180", "24", size=12, color="clrTextGrau"),
    lbl("lblPlKopf3", '"Startwoche (Montag)"', "452", "116", "170", "24", size=12, color="clrTextGrau"),
    lbl("lblPlKopf4", '"Gültig bis"', "640", "116", "150", "24", size=12, color="clrTextGrau"),
    lbl("lblPlKopf5", '"Status"', "838", "116", "100", "24", size=12, color="clrTextGrau"),
    gal("galPl", "Sort(colPlanR, ID)", "24", "140", "934", "Parent.Height - 220", 72, [pl_karte], '"Planzeilen"'),
    lbl("lblPlLeer", '"Noch kein Plan. „+ Termin hinzufügen“ legt einen an (Montag, jede Woche)."', "24", "150", "934", "40",
        size=14, color="clrTextGrau", Visible="IsEmpty(colPlanR) && !varIsLoading"),
    btn("btnPlNeu", '"+ Termin hinzufügen"', "24", "Parent.Height - 68", "240", "48", PL_NEU),
    con("conPlTermine", dict({"X": "982", "Y": "116", "Width": "Parent.Width - 1006", "Height": "Parent.Height - 140", "Fill": "clrKarte",
                              "BorderColor": "clrRahmen", "BorderThickness": "1"}, **radius(8)), [
        lbl("lblPlTermineTitel", '"Nächste Termine"', "16", "8", "Parent.Width - 32", "32", size=15, bold=True),
        gal("galPlTermine", TERMINE, "16", "44", "Parent.Width - 32", "Parent.Height - 52", 34, [
            lbl("lblPlTermin", 'Text(ThisItem.D, "dddd, dd.mm.yyyy", "de-DE") & If(ThisItem.D = Today(), "  (heute)", "")', "0", "0",
                "Parent.TemplateWidth", "34", size=13),
        ], '"Nächste Termine"'),
        lbl("lblPlKeine", '"Keine Termine in den nächsten 120 Tagen."', "16", "48", "Parent.Width - 32", "40", size=13, color="clrTextGrau",
            Visible="IsEmpty(galPlTermine.AllItems)"),
    ]),
    laden_overlay("conPlLaden"),
])

SCREENS = [scr_liste, scr_editor, scr_plan]


# ---------------------------------------------------------------- Ausgabe

def alle(c, eltern=None, out=None):
    out = [] if out is None else out
    out.append((c, eltern))
    for k in c.kinder:
        alle(k, c.name, out)
    return out


PLAIN = re.compile(r"^[^\n\t]*$")


def yaml_wert(v):
    s = "=" + v
    if PLAIN.match(s) and ": " not in s and " #" not in s and not s.endswith(":") and s == s.strip():
        return [s], False
    return s.split("\n"), True


def yaml_props(props, e):
    z = []
    for k in sorted(props):
        zeilen, block = yaml_wert(props[k])
        if block:
            z.append(e + k + ": |-")
            z += [e + "  " + x for x in zeilen]
        else:
            z.append(e + k + ": " + zeilen[0])
    return z


def yaml_control(c, e):
    z = [e + "- " + c.name + ":", e + "    Control: " + c.typ]
    if c.variante:
        z.append(e + "    Variant: " + c.variante)
    z.append(e + "    Properties:")
    z += yaml_props(c.props, e + "      ")
    if c.kinder:
        z.append(e + "    Children:")
        for k in c.kinder:
            z += yaml_control(k, e + "      ")
    return z


def yaml_screen(s):
    z = ["Screens:", "  " + s.name + ":", "    Properties:"]
    z += yaml_props(s.props, "      ")
    z.append("    Children:")
    for k in s.kinder:
        z += yaml_control(k, "      ")
    return "\n".join(z) + "\n"


# ---------------------------------------------------------------- Prüfungen

BUILTINS = set("""If Set Not And Or CountRows Filter LookUp Sort First Last Coalesce IsBlank IsEmpty Blank Text Value Trim Lower Upper Len
Left Mid Right Split Concat ForAll Sequence Index Table With Patch Collect ClearCollect Clear Remove RemoveIf Distinct Notify
NotificationType Navigate ScreenTransition Refresh Concurrent IfError IsError Reset Select SetFocus Launch Now Today DateAdd DateDiff
TimeUnit Switch Max Min RoundDown Mod Defaults User GUID Substitute StartsWith Color ColorValue ColorFade RGBA DisplayMode Font
FontWeight Align Parent Self ThisItem ThisRecord true false Boolean StartOfWeek Weekday Ungroup Date Number DateTime As in Error
Warning Success Information None Edit View Disabled White Semibold Normal Days Seconds Monday Fit Fill Small Thumbnail FirstN Char
SortOrder Descending Ascending Center Right VerticalAlign Top Overflow Scroll TextMode MultiLine TextFormat DateTimeFormat ShortDate
Text FullName Email Value ImagePosition""".split())
MEMBER_OK = set("""Value ID Title Text Selected SelectedDate AllItems Thumbnail Small Large Error Warning Success Information None
Edit View Disabled White Semibold Normal Days Seconds Monday Fit Fill Descending Ascending Center Right Top Scroll MultiLine Number
ShortDate FullName Email TemplateWidth TemplateHeight Width Height Data Black Transparent Middle Left""".split())
FUNKTIONEN = dict((m.group(1), len([x for x in m.group(2).split(",") if x.strip()]))
                  for m in re.finditer(r"(?m)^(fn\w+)\(([^)]*)\)\s*:\s*\w+\s*=", FORMULAS))
BENANNT = set(re.findall(r"(?m)^(\w+)\s*=", FORMULAS))


def args_zaehlen(f, name):
    s = rg.ausserhalb_strings(f)
    erg = []
    for m in re.finditer(r"\b" + name + r"\(", s):
        tiefe, i, anz, start = 0, m.end() - 1, 1, m.end()
        for j in range(i, len(s)):
            ch = s[j]
            if ch in "({[":
                tiefe += 1
            elif ch in ")}]":
                tiefe -= 1
                if tiefe == 0:
                    if s[start:j].strip() == "":
                        anz = 0
                    break
            elif ch == "," and tiefe == 1:
                anz += 1
        erg.append(anz)
    return erg


def patch_records(f):
    """(Liste, Felder) für jedes Patch(RG_…, …, {…}) bzw. Patch(RG_…, Defaults(…), {…})."""
    s = rg.ausserhalb_strings(f)
    out = []
    for m in re.finditer(r"\bPatch\(\s*(RG_\w+)\s*,", s):
        tiefe, i = 0, m.start() + len("Patch")
        args, start = [], m.end()
        for j in range(i, len(s)):
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
        letzter = args[-1].strip() if args else ""
        if letzter.startswith("{"):
            felder = re.findall(r"(?:^\{|,)\s*(\w+)\s*:", letzter)
            tiefe2, top = 0, []
            tok = ""
            for ch in letzter[1:-1]:
                if ch in "({[":
                    tiefe2 += 1
                elif ch in ")}]":
                    tiefe2 -= 1
                if tiefe2 == 0 and ch == ",":
                    top.append(tok)
                    tok = ""
                else:
                    tok += ch
            top.append(tok)
            felder = [t.split(":", 1)[0].strip() for t in top if ":" in t]
            werte = {t.split(":", 1)[0].strip(): t.split(":", 1)[1].strip() for t in top if ":" in t}
            out.append((m.group(1), felder, werte))
        elif letzter.startswith("ForAll("):
            for fm in re.finditer(r"\{(\w+)\s*:", letzter):
                out.append((m.group(1), [fm.group(1)], {}))
    return out


def pruefen(app_ref):
    zeilen, fehler = [], 0
    kontrollen = []
    for s in SCREENS:
        kontrollen += alle(s)
    namen = [c.name for c, _ in kontrollen]
    doppelt = sorted({n for n in namen if namen.count(n) > 1})
    if doppelt:
        fehler += len(doppelt)
        zeilen.append("FEHLER doppelte Namen: " + ", ".join(doppelt))
    props = {"App.Formulas": FORMULAS, "App.OnStart": ONSTART}
    for c, _ in kontrollen:
        for k, v in c.props.items():
            props[c.name + "." + k] = v
    gesamt = "\n".join(props.values())
    s_ges = rg.ausserhalb_strings(gesamt)
    gesetzt = set(re.findall(r"\bSet\(\s*(\w+)", s_ges))
    onstart = {k for k, _ in ONSTART_VARS}
    sammlungen = set(re.findall(r"\b(?:ClearCollect|Collect)\(\s*(\w+)", s_ges))
    felder = set(re.findall(r"(\w+)\s*:", s_ges))
    aliase = set(re.findall(r"\bAs\s+(\w+)", s_ges)) | set(re.findall(r"\bWith\(\s*\{\s*(\w+)\s*:", s_ges))
    for m in re.finditer(r"\bWith\(\s*\{([^{}]*)\}", s_ges):
        aliase |= set(re.findall(r"(\w+)\s*:", m.group(1)))
    params = set()
    for m in re.finditer(r"(?m)^fn\w+\(([^)]*)\)", FORMULAS):
        params |= set(re.findall(r"(\w+)\s*:", m.group(1)))
    spalten = set()
    for q in QUELLEN:
        spalten |= set(app_ref.spalten.get(q, {}))
    for q, cols in NEU_SPALTEN.items():
        spalten |= set(cols)
    spalten |= {"Thumbnail"}
    bekannt = BUILTINS | set(namen) | gesetzt | sammlungen | felder | aliase | params | set(FUNKTIONEN) | BENANNT | set(QUELLEN) | spalten
    # 1) je Property
    for key, f in props.items():
        p = []
        if not rg.klammern_ok(f):
            p.append("Klammern")
        if "//" in rg.ausserhalb_strings(f):
            p.append("Kommentar")
        try:
            if rg.from_de(rg.to_de(f)) != f:
                p.append("Rückübersetzung")
        except ValueError as e:
            p.append(str(e))
        unb = sorted(b for b in rg.bezeichner(f) if b not in bekannt)
        if unb:
            p.append("unbekannte Namen: " + ", ".join(unb))
        for fn, n in FUNKTIONEN.items():
            for a in args_zaehlen(f, fn):
                if a != n and not (key == "App.Formulas"):
                    p.append("%s mit %d statt %d Argumenten" % (fn, a, n))
        if p:
            fehler += len(p)
            zeilen.append("FEHLER %-36s %s" % (key, "; ".join(p)))
    # 2) Variablen und Sammlungen
    gelesen_var = set(re.findall(r"\b(var[A-Z]\w*)", s_ges))
    ohne_start = sorted(gelesen_var - onstart)
    if ohne_start:
        fehler += len(ohne_start)
        zeilen.append("FEHLER Variablen ohne Startwert in App.OnStart: " + ", ".join(ohne_start))
    nie_gesetzt = sorted(gelesen_var - gesetzt)
    if nie_gesetzt:
        fehler += len(nie_gesetzt)
        zeilen.append("FEHLER Variablen nie gesetzt: " + ", ".join(nie_gesetzt))
    gelesen_col = set(re.findall(r"\b(col[A-Z]\w*)", s_ges))
    nie_gefuellt = sorted(gelesen_col - sammlungen)
    if nie_gefuellt:
        fehler += len(nie_gefuellt)
        zeilen.append("FEHLER Sammlungen nie gefüllt: " + ", ".join(nie_gefuellt))
    # 3) Steuerelement-Verweise
    for m in re.finditer(r"\b((?:txt|dd|gal|btn|lbl|con|dp|img|tmr)[A-Z]\w*)\b", s_ges):
        if m.group(1) not in namen:
            fehler += 1
            zeilen.append("FEHLER Steuerelement unbekannt: " + m.group(1))
    for scr in re.findall(r"Navigate\((\w+)", s_ges):
        if scr not in namen:
            fehler += 1
            zeilen.append("FEHLER Bildschirm unbekannt: " + scr)
    # 4) Patch-Felder gegen die Spalten der Liste
    n_patch = 0
    for key, f in props.items():
        for liste, fl, werte in patch_records(f):
            cols = set(app_ref.spalten.get(liste, {})) | set(NEU_SPALTEN.get(liste, {}))
            for feld in fl:
                n_patch += 1
                if feld not in cols:
                    fehler += 1
                    zeilen.append("FEHLER %s: Feld %s nicht in %s" % (key, feld, liste))
                if feld in AUSWAHL_SPALTEN and werte and not werte.get(feld, "").startswith("{Value:"):
                    fehler += 1
                    zeilen.append("FEHLER %s: Auswahlspalte %s ohne {Value: …}" % (key, feld))
    zeilen.append("Patch-Felder geprüft: %d" % n_patch)
    # 5) Mitgliedsnamen nach Punkt
    mitglieder = set(re.findall(r"(?<=[\w)\]])\.([A-Za-z_]\w*)", re.sub(r"\d+\.\d+", "0", s_ges)))
    erlaubt = MEMBER_OK | spalten | felder
    unb = sorted(m for m in mitglieder if m not in erlaubt)
    if unb:
        fehler += len(unb)
        zeilen.append("FEHLER unbekannte Felder nach Punkt: " + ", ".join(unb))
    # 6) YAML zurücklesen
    for s in SCREENS:
        txt_ = yaml_screen(s)
        daten = yaml.safe_load(txt_)
        sc = daten["Screens"][s.name]

        def vergleiche(knoten, c):
            n = 0
            for k, v in c.props.items():
                if knoten["Properties"].get(k) != "=" + v:
                    raise ValueError("YAML weicht ab: %s.%s" % (c.name, k))
                n += 1
            for kk, ck in zip(knoten.get("Children") or [], c.kinder):
                (name, inhalt), = kk.items()
                if name != ck.name:
                    raise ValueError("Reihenfolge: " + name)
                n += vergleiche(inhalt, ck)
            return n
        anz = vergleiche(sc, s)
        zeilen.append("YAML %s: %d Properties zeichengleich zurückgelesen" % (s.name, anz))
    return fehler, zeilen, props, kontrollen


# Textbreiten: (Steuerelement, Text, Größe, Breite in px, Innenabstand, Zeilen)
TEXTE = [
    ("btnLiNeu", "+ Neuer Rundgang", 14, 220, 20, 1), ("btnLiVorlagen", "Vorlagen bearbeiten", 14, 220, 20, 1),
    ("btnLiNeuLaden", "↻ Neu laden", 14, 150, 20, 1), ("btnLiAlle", "✓ Archivierte zeigen", 14, 240, 20, 1),
    ("btnLiBearbeiten", "Neue Fassung?", 14, 170, 20, 1), ("btnLiAnsehen", "Ansehen", 14, 110, 20, 1), ("btnLiPlan", "Plan", 14, 90, 20, 1),
    ("btnLiAktion", "Reaktivieren", 14, 150, 20, 1), ("btnLiAktion", "Archivieren", 14, 150, 20, 1), ("btnLiVerwerfen", "Entwurf verwerfen", 14, 190, 20, 1),
    ("lblLiStatus", "Archiviert", 12, 96, 8, 1),
    ("lblLiInfo", "aktive Fassung 12  ·  Plan: Mo jede Woche, Do alle 2 Wochen  ·  Entwurf Fassung 13 in Arbeit (Josias Assefaw)", 12, 510, 0, 2),
    ("lblLiFrage", "Achtung: Heute läuft noch ein Rundgang. Archiviert erscheint er nicht mehr auf der Startseite. Nochmal tippen zum Archivieren.", 12, 1286, 0, 1),
    ("galNeuArt", "Kopie eines Rundgangs", 14, 276 - 6, 20, 1),
    ("btnEdZurueck", "← Übersicht", 14, 140, 20, 1), ("btnEdAktivieren", "Aktivieren …", 14, 190, 20, 1),
    ("btnEdBearbeiten", "Neue Fassung bearbeiten", 14, 270, 20, 1), ("lblLiName", "Objektrundgang TCC Halle 3 Nord", 17, 406, 0, 1),
    ("lblEdStatus", "Entwurf Fassung 12 · aktiv ist Fassung 11", 12, 420, 0, 1),
    ("btnGlNeuB", "+ Bereich", 13, 104, 16, 1), ("btnGlNeuK", "+ Kategorie", 13, 120, 16, 1), ("btnGlNeuP", "+ Prüfpunkt", 13, 120, 16, 1),
    ("btnGlMehrere", "Mehrere Fragen", 13, 172, 16, 1), ("btnGlHolen", "Aus Vorlage holen", 13, 176, 16, 1),
    ("lblGlInfo", "i.O./n.i.O.", 11, 90, 0, 1), ("lblGlInfo", "Datum+Zeit", 11, 90, 0, 1), ("lblGlInfo", "Mehrfach", 11, 90, 0, 1),
    ("btnEdDupl", "Duplizieren", 13, 120, 16, 1), ("btnEdEntf", "Ja, entfernen", 13, 160, 16, 1),
    ("lblEdArt (Frage)", "Entfernt den Bereich mit 12 Kategorien und 140 Prüfpunkten. Nochmal tippen.", 12, 360, 0, 3),
    ("galPTyp", "✓ i.O./n.i.O.", 12, 132 - 6, 16, 1), ("galPTyp", "📅 + Uhrzeit", 12, 132 - 6, 16, 1), ("galPTyp", "☑ Mehrfach", 12, 132 - 6, 16, 1),
    ("galPGrenz", "nicht speicherbar", 12, 176 - 6, 16, 1), ("galPGrenz", "Hinweis + Grund", 12, 176 - 6, 16, 1),
    ("galPKomm", "bei Mangel", 13, 128 - 6, 16, 1), ("galPPflicht", "freiwillig", 13, 128 - 6, 16, 1),
    ("ddPFoto", "Foto Pflicht bei Mangel (n.i.O.)", 14, 528, 60, 1), ("ddPFoto", "kein Foto (bei n.i.O. möglich)", 14, 528, 60, 1),
    ("lblPBed", "Keine Bedingung möglich: Andere Fragen hängen von dieser ab.", 12, 528, 0, 1),
    ("lblPGrenz", "Wert außerhalb der Grenzen ergibt", 12, 528, 0, 1), ("lblPWerte", "Antwortmöglichkeiten – eine pro Zeile", 12, 528, 0, 1),
    ("btnPBild", "Bild ändern", 13, 124, 16, 1),
    ("lblVsTitel", "Vorschau – so sieht es der Prüfer", 14, 394, 0, 1),
    ("lblPrTitel", "Prüfung: 12 Fehler, 3 Hinweise", 14, 394, 0, 1),
    ("btnHolenUebernehmen", "Kategorie übernehmen", 14, 260, 20, 1), ("btnAktJetzt", "Jetzt aktivieren", 14, 200, 20, 1),
    ("btnMehrAnlegen", "Anlegen (120)", 14, 220, 20, 1), ("galMehrTyp", "i.O./n.i.O.", 13, 204 - 6, 16, 1),
    ("btnBildHochladen", "Bilder hochladen ↗", 14, 220, 20, 1), ("btnPlNeu", "+ Termin hinzufügen", 14, 240, 20, 1),
    ("btnPlAktiv", "pausiert", 13, 110, 16, 1), ("ddPlTag", "Donnerstag", 14, 180, 60, 1), ("ddPlZyklus", "alle 4 Wochen", 14, 190, 60, 1),
    ("lblPlTermin", "Donnerstag, 31.12.2026  (heute)", 13, 328, 0, 1), ("lblPlKopf3", "Startwoche (Montag)", 12, 170, 0, 1),
    ("lblNeuTitel", "Neuer Rundgang", 18, 552, 0, 1), ("lblHolenTitel", "Aus Vorlage oder anderem Rundgang holen", 18, 872 - 60, 0, 1),
    ("lblMehrTitel", "Mehrere Prüfpunkte anlegen", 18, 612 - 60, 0, 1), ("lblBildTitel", "Beispielbild wählen (anklicken)", 18, 932 - 60, 0, 1),
    ("lblAktTitel", "Fassung 12 aktivieren", 18, 632 - 60, 0, 1),
]


def pruefe_texte():
    zeilen, fehler = [], 0
    for ctl, text, size, breite, pad, zmax in TEXTE:
        b = textbreite(text, size) * 1.1
        noetig = int(b // max(1, breite - pad)) + 1
        ok = noetig <= zmax
        fehler += not ok
        zeilen.append("  %-22s %4.0f px (+10 %%) / %4d px, %d Zeile(n), erlaubt %d  %s  %r" % (ctl, b, breite - pad, noetig, zmax, "ok" if ok else "FEHLER", text))
    return fehler, zeilen


def delegation(props):
    """Alle Abfragen auf SharePoint-Listen zum Nachlesen (Delegation)."""
    z = []
    for key, f in props.items():
        for m in re.finditer(r"\b(Filter|LookUp)\(\s*(RG_\w+)\s*,([^;\n]{0,140})", f):
            z.append("  %-30s %s(%s,%s" % (key, m.group(1), m.group(2), m.group(3)[:110]))
    return z


def main():
    app_ref = rg.App("2026-10-27_0909")
    fehler, zeilen, props, kontrollen = pruefen(app_ref)
    f2, z2 = pruefe_texte()
    fehler += f2
    zeilen += ["", "Textbreiten (Segoe UI, Schätzung je Zeichenart, Punkt -> Pixel x 1,333):"] + z2
    zeilen += ["", "Abfragen auf SharePoint (Delegation nachlesen):"] + delegation(props)
    os.makedirs(AUS_PAKET, exist_ok=True)
    os.makedirs(AUS_ARB, exist_ok=True)
    for s in SCREENS:
        open(os.path.join(AUS_PAKET, s.name + ".yaml"), "w", encoding="utf-8").write(yaml_screen(s))
    open(os.path.join(AUS_PAKET, "App.Formulas.txt"), "w", encoding="utf-8").write(rg.to_de(FORMULAS) + "\n")
    open(os.path.join(AUS_PAKET, "App.OnStart.txt"), "w", encoding="utf-8").write(rg.to_de(ONSTART) + "\n")
    stat = {"screens": [s.name for s in SCREENS], "steuerelemente": len(kontrollen) - len(SCREENS), "properties": len(props),
            "variablen": len(ONSTART_VARS), "funktionen": sorted(FUNKTIONEN), "neue_spalten": NEU_SPALTEN,
            "quellen": QUELLEN}
    json.dump({"stat": stat, "props": props, "de": {k: rg.to_de(v) for k, v in props.items()},
               "typ": {c.name: c.typ for c, _ in kontrollen}, "eltern": {c.name: e for c, e in kontrollen}},
              open(os.path.join(AUS_ARB, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    kopf = ["Rundgang-Builder: %d Bildschirme, %d Steuerelemente, %d Properties, %d Variablen, %d Funktionen" % (
        len(SCREENS), stat["steuerelemente"], len(props), len(ONSTART_VARS), len(FUNKTIONEN))]
    text = "\n".join(kopf + zeilen + ["", "Fehler gesamt: %d" % fehler])
    open(os.path.join(AUS_ARB, "pruefung.txt"), "w", encoding="utf-8").write(text + "\n")
    print("\n".join(kopf + [z for z in zeilen if "FEHLER" in z or z.startswith("YAML") or z.startswith("Patch")] + ["Fehler gesamt: %d" % fehler]))
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
