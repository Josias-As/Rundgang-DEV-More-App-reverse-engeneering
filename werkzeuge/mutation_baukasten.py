"""Mutationstest der Prüfungen in baukasten.py: jeder eingebaute Fehler muss gefunden werden.
Aufruf: python3 -I werkzeuge/mutation_baukasten.py <Export-Schlüssel> [--simulation-0844]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baukasten as b  # noqa: E402
import rg  # noqa: E402

MUTATIONEN = [
    ("Feld fehlt in einem Zweig (wie der Fehler vom 27.10.)", "scrKategorie.OnVisible", "                     KommentarPflicht: Coalesce(p.KommentarPflicht, false),\n", ""),
    ("Auswahlspalte ohne .Value", "scrKategorie.OnVisible", "fnGrenzmodus(p.Grenzmodus.Value)", "fnGrenzmodus(p.Grenzmodus)"),
    ("Ja/Nein ohne Coalesce", "scrKategorie.OnVisible", "Coalesce(p.KommentarPflicht, false)", "p.KommentarPflicht"),
    ("Kommentar in Formel", "lblKaFehlendAnzahl.Text", "CountRows(", "// Zähler\nCountRows("),
    ("unbekannter Name", "btnKaFoto.Visible", "fnLinkAnzahl(ThisItem.Fotos) > 0", "fnLinkAnzahlX(ThisItem.Fotos) > 0"),
    ("fnFehlt mit 11 Argumenten", "conKaKarte.BorderColor", ", ThisItem.MinWert, ThisItem.MaxWert)", ", ThisItem.MinWert)"),
    ("Klammer fehlt", "txtKaKommentar.Visible", "ThisItem.MaxWert))", "ThisItem.MaxWert)"),
    ("Feld nicht in colAntworten", "btnKaFoto.Text", "ThisItem.FotoModus", "ThisItem.FotoModu"),
    ("FotoMoeglich außerhalb OnVisible", "btnKaFoto.Visible", 'ThisItem.FotoModus <> "Aus"', "ThisItem.FotoMoeglich"),
]


def main():
    schl = sys.argv[1]
    sim = "--simulation-0844" in sys.argv
    gefunden = 0
    for text, key, alt, neu in MUTATIONEN:
        app = rg.App(schl)
        st = b.Stand(app)
        if sim and "UpdateIf(colAntworten" not in st.props["btnKaSpeichern.OnSelect"]:
            t = st.props["btnKaSpeichern.OnSelect"]
            i = t.index("Set(varAntwortJSON")
            z = t.rfind("\n", 0, i) + 1
            st.props["btnKaSpeichern.OnSelect"] = t[:i] + 'UpdateIf(colAntworten, Bewertung <> "NIO", {Kommentar: ""});\n' + t[z:i] + t[i:]
        pakete = [f(st) for f in b.PAKETE]
        treffer = False
        for p in pakete:
            for c in p["props"]:
                if c["key"] == key and alt in c["nachher"]:
                    c["nachher"] = c["nachher"].replace(alt, neu, 1)
                    st.props[key] = c["nachher"] if st.props[key] == c["nachher"].replace(neu, alt, 1) else st.props[key]
                    treffer = True
                    break
            if treffer:
                break
        if not treffer:
            print("NICHT ANWENDBAR:", text)
            continue
        fehler, zeilen = b.pruefe(st, pakete)
        ok = fehler > 0
        gefunden += ok
        print("%-55s %s" % (text, "gefunden (%d)" % fehler if ok else "NICHT GEFUNDEN"))
    print("Ergebnis: %d/%d" % (gefunden, len(MUTATIONEN)))
    return 0 if gefunden == len(MUTATIONEN) else 1


if __name__ == "__main__":
    sys.exit(main())
