"""Mutationstest der Builder-Prüfungen: absichtlich eingebaute Fehler müssen gefunden werden.
Aufruf: python3 -I werkzeuge/mutation_builder.py"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rg  # noqa: E402
import builder  # noqa: E402


def finde(name):
    for s in builder.SCREENS:
        for c, _ in builder.alle(s):
            if c.name == name:
                return c
    raise KeyError(name)


MUTATIONEN = [
    ("Variable ohne Startwert", "txtPFrage", "OnChange", lambda f: f.replace("varSchreibbar", "varSchreibbarX", 1), "Variablen ohne Startwert"),
    ("Spalte im Patch falsch", "btnGlNeuB", "OnSelect", lambda f: f.replace("Hinweis: \"\"", "Notiz: \"\"", 1), "nicht in RG_Bereiche"),
    ("Auswahlspalte ohne {Value:}", "btnGlNeuP", "OnSelect", lambda f: f.replace('Eingabetyp: {Value: "IONIO"}', 'Eingabetyp: "IONIO"', 1), "ohne {Value"),
    ("Klammer fehlt", "lblLiInfo", "Text", lambda f: f[:-1], "Klammern"),
    ("Steuerelement unbekannt", "btnGlNeuB", "OnSelect", lambda f: f.replace("SetFocus(txtBName)", "SetFocus(txtBNamen)", 1), "Steuerelement unbekannt"),
    ("Funktion mit falscher Argumentanzahl", "lblVsRegeln", "Text", lambda f: f.replace("fnGrenzText(", "fnGrenzText(1, ", 1), "Argumenten"),
    ("Sammlung nie gefüllt", "galGl", "Items", lambda f: f.replace("colB", "colBX", 1), "Sammlungen nie gefüllt"),
    ("Kommentar in Formel", "btnLiNeuLaden", "OnSelect", lambda f: f + "\n// Test", "Kommentar"),
    ("Feld nach Punkt falsch", "lblVsFrage", "Text", lambda f: f.replace(".Title", ".Titel_", 1), "unbekannte Felder nach Punkt"),
    ("Bildschirm unbekannt", "btnLiPlan", "OnSelect", lambda f: f.replace("Navigate(scrPlan", "Navigate(scrPlaene", 1), "Bildschirm unbekannt"),
    ("IfError mit Set als Wert (02.11.)", "btnLiVerwerfen", "OnSelect",
     lambda f: f.replace("If(!varPatchFehler, If(IsError(Patch(", "If(!varPatchFehler, IfError((Patch(", 1), "als Wert"),
    ("Label zu schmal (Innenabstand, 02.11.)", "lblPlAb", "Size", lambda f: "13", "FEHLER Label"),
    ("Überlappung in conEdP (Paket 27)", "btnPZahlMehr", "X", lambda f: "300", "überlappt"),
    ("Knöpfe berühren sich (Paket 27, alter Fehler)", "btnPZahlMehr", "X", lambda f: "316", "berührt"),
    ("Prüfpunkt unten abgeschnitten (Paket 27)", "btnPNio", "Y", lambda f: f.replace("+ 248", "+ 256"), "abgeschnitten"),
    ("Abschnitt fehlt in der Kopie", "tmrArbeit", "OnTimerEnd", lambda f: f.replace(', Abschnitt: Coalesce(q.Abschnitt, "")', "", 1), "Abschnitt"),
]


def main():
    app_ref = rg.App("2026-10-27_0909")
    f0, _, _, _ = builder.pruefen(app_ref)
    zeilen = ["Ausgangslage: %d Fehler" % f0]
    gefunden = 0
    for titel, ctl, prop, mut, erwartet in MUTATIONEN:
        c = finde(ctl)
        alt = copy.copy(c.props[prop])
        c.props[prop] = mut(alt)
        try:
            f, z, _, _ = builder.pruefen(app_ref)
            f3, z3 = builder.pruefe_label_auto()
            f4, z4 = builder.pruefe_rechtecke_edp()
            f, z = f + f3 + f4, z + z3 + z4
        except Exception as e:
            f, z = 1, ["Ausnahme: %s" % e]
        c.props[prop] = alt
        ok = f > 0 and any(erwartet in x for x in z)
        gefunden += ok
        zeilen.append("%-40s %s" % (titel, "gefunden" if ok else "NICHT GEFUNDEN"))
    zeilen.append("Ergebnis: %d/%d" % (gefunden, len(MUTATIONEN)))
    print("\n".join(zeilen))
    open(os.path.join(builder.AUS_ARB, "mutation.txt"), "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
    return 0 if gefunden == len(MUTATIONEN) and f0 == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
