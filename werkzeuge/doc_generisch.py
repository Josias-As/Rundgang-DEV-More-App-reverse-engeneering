"""Allgemeiner Einbau-Dokument-Generator für App- und Builder-Pakete (ab Paket 18).
Teil App: Paket nr aus arbeit/2026-10-27_Baukasten/bloecke.json. Teil Builder: Differenz zweier builder-Stände (JSON)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402
import doc_app89  # noqa: E402
import rg  # noqa: E402
from doc_paket12_16 import block  # noqa: E402

BL = json.load(open(doc_app89.BLOECKE, encoding="utf-8"))
SNAP = os.path.join(rg.REPO, "arbeit", "2026-11-02_Paket8")


def app_teil(nr, erkl, sp_schritte, zusatz_vor=None):
    p = [q for q in BL["pakete"] if q["nr"] == nr][0]
    eltern = dict(rg.App(doc_app89.EXPORT).eltern)
    for n, i in BL["neue_controls"].items():
        eltern[n] = i["eltern"]
    alle = doc_app89.neue_bis(BL, nr)
    z = ["## Teil A – Rundgang DEV", "", "### A1 – SharePoint und Daten (zuerst)", ""] + sp_schritte + [""]
    z += zusatz_vor or []
    oben = [n for n in p["neu"] if alle[n]["eltern"] not in p["neu"]]
    for i, n in enumerate(oben, 1):
        wo = alle[n]["eltern"]
        if wo is None:
            z += ["### A2.%d – neuer Bildschirm `%s`" % (i, n), "", "**Wo hin:** einen Bildschirm markieren → Strg+V.", "", "```yaml",
                  "Screens:", "  %s:" % n, "    Properties:"]
            for k in sorted(alle[n]["props"]):
                w = doc_app89.yaml_wert(alle[n]["props"][k])
                zz = w.split("\n")
                z.append("      " + k + ": " + zz[0])
                z += ["      " + x for x in zz[1:]]
            z.append("    Children:")
            for k in [m for m, i2 in alle.items() if i2["eltern"] == n]:
                z += ["      " + x for x in doc_app89.yaml_block(k, alle)]
            z += ["```", ""]
        else:
            z += ["### A2.%d – neues Steuerelement `%s`" % (i, n), "", "**Wo hin:** in der Strukturansicht **`%s`** markieren → Strg+V." % wo, "",
                  "```yaml"] + doc_app89.yaml_block(n, alle) + ["```", ""]
    z += ["### A3 – geänderte Properties", ""]
    for i, c in enumerate(p["props"], 1):
        z += block("A3.%d" % i, c["key"], doc_app89.de(c["vorher"]), doc_app89.de(c["nachher"]), erkl.get(c["key"], ""), eltern)
    anh = []
    for c in p["props"]:
        anh += ["**Rundgang DEV `%s` vorher**" % c["key"], "", "```", doc_app89.de(c["vorher"]), "```", ""]
    return z, len(p["props"]), oben, anh


def builder_teil(vorher_json, nachher_json, erkl, sp_schritte, hinweise=None):
    bv = json.load(open(os.path.join(SNAP, vorher_json), encoding="utf-8"))
    bn = json.load(open(os.path.join(SNAP, nachher_json), encoding="utf-8")) if nachher_json else json.load(
        open(os.path.join(builder.AUS_ARB, "bloecke.json"), encoding="utf-8"))
    v, n = bv["props"], bn["props"]
    geaendert = sorted(k for k in n if k in v and v[k] != n[k])
    alt_ctl = {k.split(".")[0] for k in v}
    neu_ctl = {k.split(".")[0] for k in n} - alt_ctl
    eltern = bn["eltern"]
    oben = sorted(c for c in neu_ctl if eltern.get(c) not in neu_ctl)

    def finde(name):
        for s in builder.SCREENS:
            for c, _ in builder.alle(s):
                if c.name == name:
                    return c, s
        raise KeyError(name)
    z = ["## Teil B – Builder", "", "### B0 – Daten", ""] + sp_schritte + [""]
    for i, name in enumerate(oben, 1):
        c, s = finde(name)
        if c is s:
            z += ["### B1.%d – neuer Bildschirm `%s`" % (i, name), "", "**Wo hin:** einen Bildschirm markieren → Strg+V.", "",
                  "```yaml", builder.yaml_screen(c).rstrip("\n"), "```", ""]
        else:
            z += ["### B1.%d – neues Steuerelement `%s`" % (i, name), "", "**Wo hin:** **`%s`** markieren → Strg+V." % eltern.get(name, "?"), "",
                  "```yaml"] + builder.yaml_control(c, "") + ["```", ""]
        z += (hinweise or {}).get(name, [])
    for i, k in enumerate(geaendert, 1):
        z += block("B2.%d" % i, k, bv["de"][k], bn["de"][k], erkl.get(k, ""), eltern)
    anh = []
    for k in geaendert:
        anh += ["**Builder `%s` vorher**" % k, "", "```", bv["de"][k], "```", ""]
    return z, geaendert, oben, anh
