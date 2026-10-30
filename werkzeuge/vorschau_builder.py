"""Sichtprüfung des Builders: zeichnet die Bildschirme aus builder.SCREENS mit den echten Positionen als HTML
(feste Texte, Beispielwerte für Formeln) und prüft Überlappungen gleichzeitig sichtbarer Geschwister.
Aufruf: python3 -I werkzeuge/vorschau_builder.py  ->  arbeit/2026-10-30_Builder/vorschau_*.html, ueberlappung.txt"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import builder  # noqa: E402

AUS = builder.AUS_ARB
W, H = 1366, 768
# Zustand für die Sichtprüfung: Editor mit gewähltem Prüfpunkt (Zahl), beschreibbar, keine Fenster offen
VERSTECKT = re.compile(r"^(con(Neu|Akt|Holen|Mehr|Bild)|con\w*Laden|tmr)")
SICHTBAR_ZUSTAND = {
    "varAuswahlEbene = 3": True, "varAuswahlEbene = 1": False, "varAuswahlEbene = 2": False, "varAuswahlEbene = 0": False,
    "varAuswahlEbene > 0": True, "varSchreibbar": True,
}


# Werte der mehrarmigen If-Formeln im Prüfzustand (Prüfpunkt „Zahl“, beschreibbar, keine Frage offen)
WERTE = {("conPRest", "Y"): "360", ("lblEdArt", "Width"): "130", ("txtVsWert", "Width"): "160"}
SICHT = {"lblEdName": False, "lblVsListe": False, "txtEdName": True}


def zahl(expr, pw, ph, sw=0, sh=0):
    e = expr.replace("Parent.TemplateWidth", str(pw)).replace("Parent.TemplateHeight", str(ph))
    e = e.replace("Parent.Width", str(pw)).replace("Parent.Height", str(ph)).replace("Self.Width", str(sw)).replace("Self.Height", str(sh))
    e = re.sub(r"If\(varSchreibbar, (\d+), (\d+)\)", r"\1", e)
    e = re.sub(r"If\([^()]*\), (\d+), (\d+)\)", r"\2", e)
    e = re.sub(r"Min\(([^,()]+), ([^,()]+)\)", r"min(\1, \2)", e)
    if re.fullmatch(r"[\d\s+\-*/().minx,]+", e):
        try:
            return float(eval(e, {"__builtins__": {}}, {"min": min}))  # noqa: S307 – nur Zahlen und + - * /
        except Exception:
            return None
    return None


def sichtbar(c):
    if c.name in SICHT:
        return SICHT[c.name]
    if VERSTECKT.match(c.name):
        return False
    v = c.props.get("Visible")
    if v is None or v == "true":
        return True
    if v == "false":
        return False
    if v in SICHTBAR_ZUSTAND:
        return SICHTBAR_ZUSTAND[v]
    if "ZAHL" in v and "Eingabetyp" in v and "AUSWAHL" not in v:
        return True
    if "Eingabetyp" in v:
        return False
    if "varFrage" in v or "IsEmpty" in v or "varAktivRest" in v and "||" not in v:
        return False
    return True


def text_von(c):
    t = c.props.get("Text", "")
    m = re.fullmatch(r'"([^"]*)"', t)
    if m:
        return m.group(1)
    m = re.search(r'"([^"]{2,40})"', t)
    return ("≈ " + m.group(1)) if m else ("[" + c.name + "]" if c.typ.startswith(("Label", "Classic/Button")) else "")


def zeichne(c, pw, ph, out, boxen, pfad, x0=0, y0=0):
    pr = dict(c.props)
    for (n, k), v in WERTE.items():
        if n == c.name:
            pr[k] = v
    c = builder.C(c.name, c.typ, pr, c.kinder)
    w = zahl(c.props.get("Width", str(pw)), pw, ph)
    h = zahl(c.props.get("Height", str(ph)), pw, ph)
    w = pw if w is None else w
    h = ph if h is None else h
    x = zahl(c.props.get("X", "0"), pw, ph, w, h)
    y = zahl(c.props.get("Y", "0"), pw, ph, w, h)
    x = 0 if x is None else x
    y = 0 if y is None else y
    farbe = {"GroupContainer": "#f4f5f9", "Gallery": "#ffffff", "Label": "transparent", "Classic/Button": "#171496",
             "Classic/TextInput": "#ffffff", "Classic/DropDown": "#ffffff", "Classic/DatePicker": "#ffffff", "Image": "#ddd"}
    art = c.typ.split("@")[0]
    fill = farbe.get(art, "#eee")
    if "Fill" in c.props and "clrPrimaer" == c.props["Fill"]:
        fill = "#171496"
    if c.props.get("Fill") == "clrKarte" or c.props.get("Fill", "").startswith("If(") and art == "Classic/Button":
        fill = "#ffffff"
    col = "#fff" if fill == "#171496" else "#1b1b1f"
    rahmen = "1px solid #c8cad3" if art not in ("Label",) else "none"
    if art == "Classic/Button" and c.props.get("Text") == '""':
        fill, rahmen = "transparent", "none"
    out.append('<div title="%s" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;border:%s;box-sizing:border-box;'
               'overflow:hidden;font:%dpx Segoe UI,Arial;color:%s;white-space:nowrap;display:flex;align-items:center;justify-content:%s">%s'
               % (html.escape(pfad + c.name), x, y, w, h, fill, rahmen, int(float(c.props.get("Size", "13")) * 1.333 * 0.8) if c.props.get("Size", "13").isdigit() else 13,
                  col, "center" if art == "Classic/Button" else "flex-start", html.escape(text_von(c))))
    boxen.append((pfad, c.name, x0 + x, y0 + y, w, h, art))
    kinder = [k for k in c.kinder if sichtbar(k)]
    if art == "Gallery":
        ts = zahl(c.props.get("TemplateSize", "40"), w, h) or 40
        wrap = int(c.props.get("WrapCount", "1"))
        tw = w / wrap
        for k in kinder:
            zeichne(k, tw, ts, out, boxen, pfad + c.name + "/", x0 + x, y0 + y)
    else:
        for k in kinder:
            zeichne(k, w, h, out, boxen, pfad + c.name + "/", x0 + x, y0 + y)
    out.append("</div>")


def ueberlappung(boxen):
    """Gleichzeitig sichtbare Geschwister, die sich überdecken (ohne volle Flächen wie Hintergrund-Knöpfe)."""
    z = []
    gruppen = {}
    for b in boxen:
        gruppen.setdefault(b[0], []).append(b)
    for pfad, gs in gruppen.items():
        for i, a in enumerate(gs):
            for b in gs[i + 1:]:
                if a[6] == "Label" and "Hinter" in a[1] or b[6] == "Label" and "Hinter" in b[1]:
                    continue
                if a[1].endswith(("Zeile", "Sperre")) or b[1].endswith(("Zeile", "Sperre")) or b[1] in ("btnBi",):
                    continue
                dx = min(a[2] + a[4], b[2] + b[4]) - max(a[2], b[2])
                dy = min(a[3] + a[5], b[3] + b[5]) - max(a[3], b[3])
                if dx > 2 and dy > 2:
                    z.append("  %-40s %s ↔ %s (%d × %d px)" % (pfad or "(Bildschirm)", a[1], b[1], dx, dy))
    return z


def main():
    berichte = []
    for s in builder.SCREENS:
        out, boxen = [], []
        for k in s.kinder:
            if sichtbar(k):
                zeichne(k, W, H, out, boxen, "")
        seite = ('<!doctype html><meta charset="utf-8"><title>Vorschau %s</title><body style="margin:0;background:#888">'
                 '<div style="position:relative;width:%dpx;height:%dpx;background:#f4f5f9;overflow:hidden">%s</div></body>' % (s.name, W, H, "".join(out)))
        open(os.path.join(AUS, "vorschau_%s.html" % s.name), "w", encoding="utf-8").write(seite)
        ue = ueberlappung(boxen)
        berichte.append("%s: %d Steuerelemente gezeichnet, %d Überlappungen" % (s.name, len(boxen), len(ue)))
        berichte += ue
    open(os.path.join(AUS, "ueberlappung.txt"), "w", encoding="utf-8").write("\n".join(berichte) + "\n")
    print("\n".join(berichte))


if __name__ == "__main__":
    main()
