"""Abgleich Rundgang-App: Studio-Export gegen die Paketkette aus baukasten.py.
Aufruf: python3 -I werkzeuge/abgleich_app.py <Export-Schlüssel>  ->  arbeit/<datum>_Abgleich_<Schlüssel>/abgleich_app.txt
Je Paket: wie viele seiner Properties im Export den Stand nach dem Paket haben (eingefügt), den Stand davor (fehlt) oder keinen (abweichend)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baukasten  # noqa: E402
import rg  # noqa: E402


def norm(f):
    return re.sub(r"\s+", " ", rg.ohne_kommentare(f or "").strip())


def staende():
    app0 = rg.App("2026-10-27_0909")
    st = baukasten.Stand(app0)
    aus = [("Export 0909", dict(st.props))]
    for f in baukasten.PAKETE:
        f(st)
        aus.append((f.__name__, dict(st.props)))
    return aus


def main():
    schl = sys.argv[1]
    ex = rg.App(schl).props
    st = staende()
    z = ["Abgleich Export %s gegen die Paketkette (%s)" % (schl, " → ".join(n for n, _ in st[1:])), ""]
    alle_abw = {}
    for i in range(1, len(st)):
        name, nach = st[i]
        vor = st[i - 1][1]
        keys = sorted(k for k in set(vor) | set(nach) if norm(vor.get(k)) != norm(nach.get(k)))
        drin = [k for k in keys if norm(ex.get(k)) == norm(nach.get(k))]
        fehlt = [k for k in keys if norm(ex.get(k)) == norm(vor.get(k)) and k not in drin]
        sonst = [k for k in keys if k not in drin and k not in fehlt]
        z.append("%-8s %3d Properties: eingefügt %3d, fehlt %3d, abweichend %3d" % (name, len(keys), len(drin), len(fehlt), len(sonst)))
        for k in fehlt:
            z.append("           fehlt:      " + k)
        for k in sonst:
            z.append("           abweichend: " + k)
            alle_abw[k] = name
    letzter = st[-1][1]
    nur_ex = sorted(k for k in ex if k not in letzter)
    z += ["", "Nur im Export (in keinem Paketstand): %d" % len(nur_ex)] + ["  " + k for k in nur_ex]
    gleich_0909 = [k for k in ex if k in st[0][1] and norm(ex[k]) == norm(st[0][1][k])]
    z += ["", "Properties im Export: %d, davon unverändert seit 0909: %d" % (len(ex), len(gleich_0909))]
    ziel = os.path.join(rg.REPO, "arbeit", "2026-11-03_Abgleich_Exporte")
    os.makedirs(ziel, exist_ok=True)
    open(os.path.join(ziel, "abgleich_app.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    print("\n".join(z))


if __name__ == "__main__":
    main()
