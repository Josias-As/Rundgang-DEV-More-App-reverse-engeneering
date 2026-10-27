"""Erzeugt aus arbeit/2026-10-27_Baukasten/bloecke.json die Paketdokumente und Prüfberichte in pakete/.
Aufruf: python3 -I werkzeuge/doc_baukasten.py"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rg  # noqa: E402
from baukasten_text import PAKET_TEXT, PRUEF_TEXT, RUNDE1, UEBERSICHT  # noqa: E402

AUS = os.path.join(rg.REPO, "pakete")
ARB = os.path.join(rg.REPO, "arbeit", "2026-10-27_Baukasten")


def de(f):
    return rg.to_de(f)


def yaml_wert(v):
    v = "=" + v
    if "\n" in v or ": " in v or " #" in v or "{" in v:
        return "|-\n" + "\n".join("  " + z for z in v.split("\n"))
    return v


def yaml_block(name, info, alle, tiefe=0):
    e = "    " * tiefe
    z = [e + "- " + name + ":", e + "    Control: " + info["typ"]]
    if info["typ"].startswith("GroupContainer"):
        z.append(e + "    Variant: ManualLayout")
    z.append(e + "    Properties:")
    for k in sorted(info["props"]):
        w = yaml_wert(info["props"][k])
        if w.startswith("|-"):
            zeilen = w.split("\n")
            z.append(e + "      " + k + ": " + zeilen[0])
            z += [e + "      " + x for x in zeilen[1:]]
        else:
            z.append(e + "      " + k + ": " + w)
    kinder = [n for n, i in alle.items() if i["eltern"] == name]
    if kinder:
        z.append(e + "    Children:")
        for k in kinder:
            z += yaml_block(k, alle[k], alle, tiefe + 1)
    return z


def block(titel, inhalt, sprache=""):
    return ["**" + titel + "**", "", "```" + sprache, inhalt, "```", ""]


def paket_doc(d, p, nr):
    t = PAKET_TEXT[nr]
    z = ["# Baukasten-Paket %d – %s" % (nr, t["titel"]), ""]
    z += ["Stand: %s · erzeugt mit `werkzeuge/baukasten.py` aus dem Export `%s`%s." % (
        t.get("datum", "27.10.2026"), d["export"],
        " **(ENTWURF: Simulation der Änderung von 08:44, vor dem Einfügen mit dem frischen Export neu erzeugen)**" if d["simulation"] else ""), ""]
    z += ["## Kurzfassung", ""] + ["- " + x for x in t["kurz"]] + [""]
    z += ["## Voraussetzungen", ""] + ["- " + x for x in t["voraus"]] + [""]
    z += ["## Schritte", ""]
    props = {c["schritt"]: [] for c in p["props"]}
    for c in p["props"]:
        props[c["schritt"]].append(c)
    for s in t["schritte"]:
        z += ["### Schritt %s – %s" % (s["nr"], s["titel"]), ""]
        if s.get("text"):
            z += s["text"] + [""]
        for c in props.get(s["nr"], []):
            z += block("`%s`" % c["key"], de(c["nachher"]))
        for name in s.get("yaml", []):
            alle = d["neue_controls"]
            z += ["**YAML `%s`** (englische Schreibweise, so wie es ist einfügen):" % name, "", "```yaml"]
            z += yaml_block(name, alle[name], alle)
            z += ["```", ""]
        for name in s.get("einzeln", []):
            info = d["neue_controls"][name]
            z += ["Properties von `%s` (Formelleiste, deutsch):" % name, ""]
            for k in info["props"]:
                z += block("`%s.%s`" % (name, k), de(info["props"][k]))
        if s.get("pruefen"):
            z += ["Prüfen nach dem Schritt:"] + ["- " + x for x in s["pruefen"]] + [""]
    z += ["## Test", ""] + t["test"] + [""]
    z += ["## Rückweg", ""] + t["rueck"] + [""]
    z += ["## Anhang – Vorher-Fassungen (für den Rückweg)", "",
          "Ohne Kommentare, sonst zeichengleich mit dem Export. Standardwerte sind mit „(Standard)“ markiert.", ""]
    for c in p["props"]:
        if c.get("standard"):
            z += ["**`%s`** (Standard): `%s`" % (c["key"], c["vorher"]), ""]
        else:
            z += block("`%s` vorher" % c["key"], de(rg.ohne_kommentare(c["vorher"])))
    return "\n".join(z)


def pruef_doc(d, p, nr, auto, logik):
    t = PRUEF_TEXT[nr]
    z = ["# Prüfung Baukasten-Paket %d – %s" % (nr, PAKET_TEXT[nr]["titel"]), ""]
    z += ["Export: `%s`%s. Kennzeichnung: **belegt** (maschinell/Export), **geschlussfolgert**, **UNSICHER** (nur in Studio prüfbar)." % (
        d["export"], " – **Simulation der Änderung von 08:44, vor dem Einfügen mit dem frischen Export wiederholen**" if d["simulation"] else ""), ""]
    abschnitt = []
    drin = False
    for zeile in auto.split("\n"):
        if zeile.startswith("== Paket %d:" % nr):
            drin = True
            abschnitt.append(zeile)
            continue
        if drin and zeile.startswith("== "):
            break
        if drin:
            abschnitt.append(zeile)
    schema = [x for x in auto.split("\n") if x.strip().startswith("Paket %d:" % nr) or ("FEHLER Paket %d" % nr) in x]
    z += ["## a) Namenscheck (maschinell, belegt)", "",
          "Jede Property im Paket wurde gegen den Export geprüft: Klammern, keine Kommentare, Rückübersetzung deutsch → englisch zeichengleich, "
          "jeder Bezeichner ist Steuerelement, Variable, Sammlung, Funktion, Liste, Spalte, Feld oder Alias der App bzw. wird im Paket angelegt.", "", "```"]
    z += abschnitt + schema + ["```", ""]
    z += ["## b) Typcheck", ""] + t["b"] + [""]
    z += ["## c) Reihenfolge", ""] + t["c"] + [""]
    z += ["## d) Auswirkungsliste", "", "| Stelle | betroffen | wie |", "|---|---|---|"]
    z += ["| %s | %s | %s |" % x for x in t["d"]] + [""]
    z += ["## e) Szenarien", "", "| Szenario | erwartetes Ergebnis | Beleg |", "|---|---|---|"]
    z += ["| %s | %s | %s |" % x for x in t["e"]] + [""]
    probe = [x for x in logik.split("\n") if x.startswith("P%d " % nr)]
    if probe:
        z += ["Logik-Gegenprobe der Funktionen (`werkzeuge/logik_probe.py`, Python-Nachbildung der Formeln, keine Ausführung von Power Fx):", "", "```"]
        z += probe + ["```", ""]
    z += ["## f) Studio-Fallen", ""] + ["- " + x for x in t["f"]] + [""]
    z += ["## g) Lauffähigkeit", ""] + t["g"] + [""]
    if RUNDE1.get(nr):
        z += ["## Unabhängige Prüfung – Runde 1 und Umgang", "", "| Befund | Umgang |", "|---|---|"]
        z += ["| %s | %s |" % x for x in RUNDE1[nr]] + [""]
    z += ["## Offene Befunde", ""] + (t.get("offen") or ["Keine."]) + [""]
    return "\n".join(z)


def main():
    d = json.load(open(os.path.join(ARB, "bloecke.json"), encoding="utf-8"))
    auto = open(os.path.join(ARB, "pruefung_auto.txt"), encoding="utf-8").read()
    logik = open(os.path.join(ARB, "logik_probe.txt"), encoding="utf-8").read()
    os.makedirs(AUS, exist_ok=True)
    for i, p in enumerate(d["pakete"], start=1):
        name = PAKET_TEXT[i]["datei"]
        open(os.path.join(AUS, "PAKET_%d_%s.md" % (i, name)), "w", encoding="utf-8").write(paket_doc(d, p, i) + "\n")
        open(os.path.join(AUS, "PRUEFUNG_%d_%s.md" % (i, name)), "w", encoding="utf-8").write(pruef_doc(d, p, i, auto, logik) + "\n")
    zeilen = UEBERSICHT(d)
    open(os.path.join(AUS, "BAUKASTEN_UEBERSICHT.md"), "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
    json.dump(d, open(os.path.join(AUS, "stand_baukasten.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben:", sorted(os.listdir(AUS)))


if __name__ == "__main__":
    main()
