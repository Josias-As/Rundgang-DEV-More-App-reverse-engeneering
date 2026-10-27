"""Rundgang-App: Export laden, Formeln de/en umwandeln, Namen und Klammern prüfen.
Aufruf immer mit python3 -I. Formeln werden englisch ohne führendes '=' gehalten."""
import json
import os
import re
import shutil
import zipfile

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTPACKT = os.path.join(REPO, "arbeit", "_entpackt")

EXPORTE = {
    "2026-10-27_0724": "quellen/2026-10-27_Export/RundgangApp_20261027072413.zip",
}


def _entpacke_zip(z, ziel):
    with zipfile.ZipFile(z) as zf:
        for info in zf.infolist():
            name = info.filename.replace("\\", "/")
            if name.endswith("/"):
                continue
            pfad = os.path.join(ziel, name)
            os.makedirs(os.path.dirname(pfad), exist_ok=True)
            with zf.open(info) as q, open(pfad, "wb") as d:
                shutil.copyfileobj(q, d)


def entpacke(schluessel):
    ziel = os.path.join(ENTPACKT, schluessel)
    msapp_ziel = os.path.join(ziel, "msapp")
    if not os.path.isdir(msapp_ziel):
        _entpacke_zip(os.path.join(REPO, EXPORTE[schluessel]), os.path.join(ziel, "paket"))
        msapp = None
        for wurzel, _, dateien in os.walk(os.path.join(ziel, "paket")):
            for d in dateien:
                if d.endswith(".msapp"):
                    msapp = os.path.join(wurzel, d)
        _entpacke_zip(msapp, msapp_ziel)
    return msapp_ziel


class App:
    def __init__(self, schluessel):
        self.schluessel = schluessel
        self.ordner = entpacke(schluessel)
        self.props = {}
        self.typ = {}
        self.eltern = {}
        self.screen = {}
        self.reihenfolge = []
        src = os.path.join(self.ordner, "Src")
        for d in sorted(os.listdir(src)):
            if not d.endswith(".pa.yaml") or d.startswith("_"):
                continue
            daten = yaml.safe_load(open(os.path.join(src, d), encoding="utf-8"))
            if "App" in daten:
                self._props("App", daten["App"].get("Properties", {}))
                self.typ["App"] = "App"
            for sname, s in (daten.get("Screens") or {}).items():
                self.typ[sname] = "Screen"
                self.screen[sname] = sname
                self._props(sname, s.get("Properties", {}))
                self._walk(s.get("Children", []), sname, sname)
        self.spalten = self._lade_spalten()

    def _props(self, ctrl, props):
        for k, v in (props or {}).items():
            v = "" if v is None else str(v)
            if v.startswith("="):
                v = v[1:]
            self.props[ctrl + "." + k] = v
            self.reihenfolge.append(ctrl + "." + k)

    def _walk(self, kinder, eltern, screen):
        for k in kinder or []:
            for name, c in k.items():
                self.typ[name] = c.get("Control", "")
                self.eltern[name] = eltern
                self.screen[name] = screen
                self._props(name, c.get("Properties", {}))
                self._walk(c.get("Children", []), name, screen)

    def _lade_spalten(self):
        d = json.load(open(os.path.join(self.ordner, "References", "DataSources.json"), encoding="utf-8"))
        out = {}
        for ds in d["DataSources"]:
            cols = {}
            m = ds.get("DataEntityMetadataJson") or {}
            for v in (m.values() if isinstance(m, dict) else []):
                try:
                    s = json.loads(v)["schema"]["items"]["properties"]
                except Exception:
                    continue
                for c, p in s.items():
                    t = p.get("type", "")
                    f = p.get("format", "")
                    if p.get("x-ms-capabilities", {}).get("filterFunctions") is None and t == "object":
                        pass
                    cols[c] = (t + (":" + f if f else "")).strip(":")
                    dn = p.get("title")
                    if dn and dn != c:
                        cols[dn] = cols[c]
            out[ds["Name"]] = cols
        return out

    def get(self, schluessel):
        return self.props[schluessel]

    def steuerelemente(self):
        return set(self.typ)


def _string_ende(f, i):
    ch = f[i]
    j = i + 1
    while j < len(f):
        if f[j] == ch:
            if j + 1 < len(f) and f[j + 1] == ch:
                j += 2
                continue
            return j
        j += 1
    raise ValueError("offene Zeichenkette bei %d" % i)


def ohne_kommentare(f):
    """// bis Zeilenende entfernen (außerhalb von Zeichenketten). Zeilen, die dadurch leer werden, entfallen."""
    out = []
    i, n = 0, len(f)
    while i < n:
        ch = f[i]
        if ch in "\"'":
            j = _string_ende(f, i)
            out.append(f[i:j + 1])
            i = j + 1
            continue
        if f.startswith("//", i):
            j = f.find("\n", i)
            i = n if j < 0 else j
            continue
        out.append(ch)
        i += 1
    zeilen = [z.rstrip() for z in "".join(out).split("\n")]
    return "\n".join(z for z in zeilen if z.strip() != "")


def hat_kommentar(f):
    return ohne_kommentare(f) != "\n".join(z.rstrip() for z in f.split("\n") if z.strip() != "")


def to_de(f, kommentare=False):
    out = []
    i, n = 0, len(f)
    while i < n:
        ch = f[i]
        if ch in "\"'":
            j = _string_ende(f, i)
            out.append(f[i:j + 1])
            i = j + 1
            continue
        if f.startswith("//", i):
            if not kommentare:
                raise ValueError("Kommentar in Formel")
            j = f.find("\n", i)
            j = n if j < 0 else j
            out.append(f[i:j])
            i = j
            continue
        if ch == ";":
            out.append(";;")
        elif ch == ",":
            out.append(";")
        elif ch == "." and i > 0 and f[i - 1].isdigit() and i + 1 < n and f[i + 1].isdigit():
            k = i - 1
            while k >= 0 and f[k].isdigit():
                k -= 1
            out.append("," if (k < 0 or not (f[k].isalnum() or f[k] == "_")) else ".")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def from_de(f):
    out = []
    i, n = 0, len(f)
    while i < n:
        ch = f[i]
        if ch in "\"'":
            j = _string_ende(f, i)
            out.append(f[i:j + 1])
            i = j + 1
            continue
        if f.startswith(";;", i):
            out.append(";")
            i += 2
            continue
        if ch == ";":
            out.append(",")
        elif ch == "," and i > 0 and f[i - 1].isdigit() and i + 1 < n and f[i + 1].isdigit():
            out.append(".")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def ausserhalb_strings(f):
    out = []
    i, n = 0, len(f)
    while i < n:
        if f[i] == '"':
            j = _string_ende(f, i)
            out.append('""')
            i = j + 1
        elif f[i] == "'":
            j = _string_ende(f, i)
            out.append(f[i:j + 1])
            i = j + 1
        else:
            out.append(f[i])
            i += 1
    return "".join(out)


def klammern_ok(f):
    s = ausserhalb_strings(f)
    paare = {")": "(", "}": "{", "]": "["}
    stapel = []
    for ch in s:
        if ch in "({[":
            stapel.append(ch)
        elif ch in paare:
            if not stapel or stapel[-1] != paare[ch]:
                return False
            stapel.pop()
    return not stapel


def bezeichner(f):
    """Alle Bezeichner außerhalb von Zeichenketten (ohne Punkt-Felder)."""
    s = ausserhalb_strings(f)
    s = re.sub(r"'[^']*'", " ", s)
    return set(re.findall(r"(?<![\w.])([A-Za-zÄÖÜäöüß_][\w]*)", s))


def ws(s):
    return re.sub(r"\s+", "", s)
