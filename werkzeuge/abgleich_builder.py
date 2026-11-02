"""Abgleich Builder: Studio-Export gegen den Generator-Stand (bloecke.json).
Aufruf: python3 -I werkzeuge/abgleich_builder.py <Export-Schlüssel> [bloecke.json]  ->  Liste der Abweichungen."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rg  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(f):
    return re.sub(r"\s+", " ", (f or "").strip())


def main():
    app = rg.App(sys.argv[1])
    quelle = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, "arbeit/2026-10-30_Builder/bloecke.json")
    soll = json.load(open(quelle, encoding="utf-8"))
    sp, typ = soll["props"], soll["typ"]
    ist = app.props
    zeilen = []
    fehlt_ctl = sorted({k.split(".")[0] for k in sp} - {k.split(".")[0] for k in ist} - {"App"})
    extra_ctl = sorted({k.split(".")[0] for k in ist} - {k.split(".")[0] for k in sp} - {"App", "Screen1"})
    zeilen.append("Steuerelemente fehlen in Studio: %d %s" % (len(fehlt_ctl), ", ".join(fehlt_ctl)))
    zeilen.append("Steuerelemente nur in Studio: %d %s" % (len(extra_ctl), ", ".join(extra_ctl)))
    for k in ("App.Formulas", "App.OnStart"):
        a, b = norm(rg.ohne_kommentare(sp.get(k, ""))), norm(rg.ohne_kommentare(ist.get(k, "")))
        zeilen.append("%s: %s" % (k, "gleich" if a == b else "ABWEICHUNG"))
    anders, fehlt = [], []
    for k, v in sorted(sp.items()):
        if k.startswith("App."):
            continue
        c = k.split(".")[0]
        if c in fehlt_ctl:
            continue
        if k not in ist:
            fehlt.append(k)
        elif norm(v) != norm(ist[k]):
            anders.append(k)
    zeilen.append("Properties fehlen in Studio (Standardwert?): %d" % len(fehlt))
    zeilen += ["  " + k for k in fehlt]
    zeilen.append("Properties mit anderem Inhalt: %d" % len(anders))
    for k in anders:
        zeilen.append("  " + k)
        zeilen.append("    soll: " + norm(sp[k])[:220])
        zeilen.append("    ist : " + norm(ist[k])[:220])
    print("\n".join(zeilen))


if __name__ == "__main__":
    main()
