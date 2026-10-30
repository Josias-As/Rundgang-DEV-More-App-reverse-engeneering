"""Logik-Gegenprobe des Rundgang-Builders: Python-Nachbildung der Abläufe (Stufen in tmrArbeit, Entfernen,
Verwerfen, Reaktivieren, Schreibprüfung CHECK) gegen die Leselogik der Rundgang-App (btnRgAktion, scrKategorie.OnVisible).
Keine Ausführung von Power Fx: Die Funktionen bilden die Formeln aus werkzeuge/builder.py Schritt für Schritt nach.
Aufruf: python3 -I werkzeuge/logik_builder.py  ->  arbeit/2026-10-30_Builder/logik_builder.txt"""
import os

AUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "arbeit", "2026-10-30_Builder")


class SP:
    """Die SharePoint-Listen als Python-Listen."""

    def __init__(self):
        self.n = 0
        self.rg, self.b, self.k, self.p = {}, [], [], []

    def neu(self, liste, **f):
        self.n += 1
        f["ID"] = self.n
        liste.append(f)
        return f


# ---------------------------------------------------------------- Rundgang-App (belegt aus dem Export)

def app_start(sp, r):
    if not sp.rg[r]["Aktiv"]:
        return None
    b = [x for x in sp.b if x["RundgangID"] == r and x["Aktiv"]]
    bid = {x["ID"]: x for x in b}
    k = [x for x in sp.k if x["Aktiv"] and x["BereichID"] in bid]
    k.sort(key=lambda x: bid[x["BereichID"]]["R"] * 10000 + x["R"])
    return [x["ID"] for x in k]


def app_kategorie(sp, kid):
    return sorted((x["R"], x["Title"]) for x in sp.p if x["KategorieID"] == kid and x["Aktiv"])


# ---------------------------------------------------------------- Builder

def fassung_aktiv(f):
    return f if (f or 0) > 0 else 1


def vorbereiten(sp, r):
    for x in sp.b:
        if x["RundgangID"] == r and x.get("Fassung") is None:
            x["Fassung"], x["QuelleID"] = 1, 0
    bids = {x["ID"] for x in sp.b if x["RundgangID"] == r}
    kids = set()
    for x in sp.k:
        if x["BereichID"] in bids:
            kids.add(x["ID"])
            if x.get("Fassung") is None or x.get("RundgangID") is None:
                x.update(Fassung=1, RundgangID=r, QuelleID=0)
    for x in sp.p:
        if x["KategorieID"] in kids and (x.get("Fassung") is None or x.get("RundgangID") is None):
            x.update(Fassung=1, RundgangID=r, QuelleID=0)
    g = sp.rg[r]
    g.update(Fassung=1, EntwurfFassung=0, Status="Aktiv" if g["Aktiv"] else "Archiviert")


def baum(sp, r, f, nur_aktive):
    b = [x for x in sp.b if x["RundgangID"] == r and x.get("Fassung") == f]
    k = [x for x in sp.k if x.get("RundgangID") == r and x.get("Fassung") == f]
    p = [x for x in sp.p if x.get("RundgangID") == r and x.get("Fassung") == f]
    if nur_aktive:
        b = [x for x in b if x["Aktiv"]]
        k = [x for x in k if x["Aktiv"]]
        p = [x for x in p if x["Aktiv"]]
        bid = {x["ID"] for x in b}
        k = [x for x in k if x["BereichID"] in bid]
        kid = {x["ID"] for x in k}
        p = [x for x in p if x["KategorieID"] in kid]
    return b, k, p


def kopie(sp, qb, qk, qp, ziel_r, ziel_f, ziel_b=0, ziel_k=0, behalte=False, zusatz="", colp=(), fehler_bei=None):
    """STUFE_KOPIE: Bereiche, Kategorien, Prüfpunkte anlegen, Zuordnung alt -> neu, Bedingungen nachziehen."""
    mb, mk, mp = {}, {}, []
    for i, q in enumerate(sorted(qb, key=lambda x: (x["R"], x["ID"])), 1):
        mb[q["ID"]] = sp.neu(sp.b, Title=q["Title"] + zusatz, RundgangID=ziel_r, Fassung=ziel_f, R=q["R"] if behalte else i * 10,
                             Aktiv=False, QuelleID=q["ID"])["ID"]
    for i, q in enumerate(sorted(qk, key=lambda x: (x["R"], x["ID"])), 1):
        ziel = ziel_b if not qb else mb.get(q["BereichID"], 0)
        mk[q["ID"]] = sp.neu(sp.k, Title=q["Title"], BereichID=ziel, RundgangID=ziel_r, Fassung=ziel_f,
                             R=q["R"] if (qb or behalte) else i * 10, Aktiv=True, QuelleID=q["ID"])["ID"] if ziel else 0
    for i, q in enumerate(sorted(qp, key=lambda x: (x["R"], x["ID"])), 1):
        ziel = ziel_k if not qk else mk.get(q["KategorieID"], 0)
        if fehler_bei == q["ID"]:
            neu = 0
        else:
            neu = sp.neu(sp.p, Title=q["Title"], KategorieID=ziel, RundgangID=ziel_r, Fassung=ziel_f, R=q["R"] if (qk or behalte) else i * 10,
                         Aktiv=True, QuelleID=q["ID"], Bed=0, BedWert="")["ID"] if ziel else 0
        mp.append({"Alt": q["ID"], "Neu": neu, "BedAlt": q.get("Bed") or 0, "BedWert": q.get("BedWert", ""), "Ziel": ziel})
    for m in mp:
        if m["BedAlt"] and m["Neu"]:
            a = next((x for x in mp if x["Alt"] == m["BedAlt"]), None)
            alt_a = next((x for x in colp if x["ID"] == m["BedAlt"]), None)
            if a and a["Ziel"] == m["Ziel"]:
                neu_a = a["Neu"]
            elif a is None and alt_a and alt_a["KategorieID"] == m["Ziel"]:
                neu_a = m["BedAlt"]
            else:
                neu_a = 0
            if neu_a:
                p = next(x for x in sp.p if x["ID"] == m["Neu"])
                p["Bed"], p["BedWert"] = neu_a, m["BedWert"]
    fehl = sum(1 for v in mb.values() if not v) + sum(1 for v in mk.values() if not v) + sum(1 for m in mp if not m["Neu"])
    return mb, mk, mp, fehl


def neue_fassung(sp, r, fehler_bei=None, nutzer="J"):
    g = sp.rg[r]
    if (g.get("EntwurfFassung") or 0) > 0:
        return g["EntwurfFassung"]
    fa = fassung_aktiv(g.get("Fassung"))
    ziel = max([x.get("Fassung") or 0 for x in sp.b if x["RundgangID"] == r] + [x.get("Fassung") or 0 for x in sp.k if x.get("RundgangID") == r]
               + [x.get("Fassung") or 0 for x in sp.p if x.get("RundgangID") == r] + [fa]) + 1
    g.update(EntwurfFassung=ziel, EntwurfVon=nutzer)
    qb, qk, qp = baum(sp, r, fa, True)
    _, _, _, fehl = kopie(sp, qb, qk, qp, r, ziel, behalte=True, fehler_bei=fehler_bei)
    if fehl:
        if (g.get("Fassung") or 0) == 0 or ziel != fassung_aktiv(g.get("Fassung")):
            entferne_fassung(sp, r, ziel)
        if (g.get("Fassung") or 0) > 0 and ziel != fassung_aktiv(g.get("Fassung")):
            g.update(EntwurfFassung=0, EntwurfVon="")
        return None
    return ziel


def entferne_fassung(sp, r, f):
    sp.p[:] = [x for x in sp.p if not (x.get("RundgangID") == r and x.get("Fassung") == f)]
    sp.k[:] = [x for x in sp.k if not (x.get("RundgangID") == r and x.get("Fassung") == f)]
    sp.b[:] = [x for x in sp.b if not (x["RundgangID"] == r and x.get("Fassung") == f)]


def check(sp, r, f, vorlage=False):
    """CHECK vor jeder Schreibstelle."""
    return vorlage or (sp.rg[r].get("EntwurfFassung") or 0) == f


def aktivieren(sp, r, f, abbruch_nach_bereichen=False):
    g = sp.rg[r]
    if (g.get("EntwurfFassung") or 0) != f:
        return "veraltet"
    for x in sp.b:
        if x["RundgangID"] == r and x["Aktiv"] and (x.get("Fassung") or 0) != f:
            x["Aktiv"] = False
    for x in sp.k:
        if x.get("RundgangID") == r and x["Aktiv"] and (x.get("Fassung") or 0) != f:
            x["Aktiv"] = False
    neu = [x for x in sp.b if x["RundgangID"] == r and x.get("Fassung") == f]
    for x in neu:
        x["Aktiv"] = True
    if abbruch_nach_bereichen:
        return "abbruch"
    ok = all(not (x["Aktiv"] and x.get("Fassung") != f) for x in sp.b if x["RundgangID"] == r) and \
        sum(1 for x in sp.b if x["RundgangID"] == r and x["Aktiv"] and x.get("Fassung") == f) == len(neu)
    if ok:
        g.update(Fassung=f, EntwurfFassung=0, EntwurfVon="", Status="Aktiv", Aktiv=True)
        return "ok"
    return "unvollständig"


def verwerfen(sp, r):
    g = sp.rg[r]
    f = g.get("EntwurfFassung") or 0
    aktiv_teil = any(x["Aktiv"] for x in sp.b if x["RundgangID"] == r and x.get("Fassung") == f)
    if f > 0 and f != fassung_aktiv(g.get("Fassung")) and not aktiv_teil:
        entferne_fassung(sp, r, f)
        g.update(EntwurfFassung=0, EntwurfVon="")
        return "verworfen"
    return "verweigert"


def reaktivieren(sp, r):
    sp.rg[r].update(Status="Aktiv", Aktiv=True)


def laden_schreibbar(sp, r, f, vorlage=False):
    """STUFE_LADEN: Entwurf nur beschreibbar, wenn er noch offen ist und kein Bereich schon aktiv ist."""
    if not vorlage and (sp.rg[r].get("EntwurfFassung") or 0) != f:
        return False, False
    b, _, _ = baum(sp, r, f, False)
    if not vorlage and any(x["Aktiv"] for x in b):
        return False, True
    return True, False


# ---------------------------------------------------------------- Testbestand wie in SharePoint (Altbestand ohne Fassung)

def bestand():
    sp = SP()
    sp.n = 0
    sp.rg[1] = {"Aktiv": True, "Status": None, "Fassung": None, "EntwurfFassung": None}
    sp.n = 1
    b1 = sp.neu(sp.b, Title="Halle", RundgangID=1, R=10, Aktiv=True)
    b2 = sp.neu(sp.b, Title="Büro", RundgangID=1, R=20, Aktiv=True)
    k1 = sp.neu(sp.k, Title="Lager", BereichID=b1["ID"], R=10, Aktiv=True)
    k2 = sp.neu(sp.k, Title="Alt", BereichID=b1["ID"], R=20, Aktiv=False)
    k3 = sp.neu(sp.k, Title="Küche", BereichID=b2["ID"], R=10, Aktiv=True)
    a = sp.neu(sp.p, Title="Sauber?", KategorieID=k1["ID"], R=10, Aktiv=True, Bed=0, BedWert="")
    sp.neu(sp.p, Title="Foto Schaden", KategorieID=k1["ID"], R=20, Aktiv=True, Bed=a["ID"], BedWert="NIO")
    sp.neu(sp.p, Title="inaktiv", KategorieID=k1["ID"], R=30, Aktiv=False, Bed=0, BedWert="")
    sp.neu(sp.p, Title="Kühlschrank", KategorieID=k3["ID"], R=10, Aktiv=True, Bed=0, BedWert="")
    sp.neu(sp.p, Title="Rest", KategorieID=k2["ID"], R=10, Aktiv=True, Bed=0, BedWert="")
    return sp


def main():
    erg = []

    def pruefe(name, bed):
        erg.append(("ok    " if bed else "FEHLER") + "  " + name)

    sp = bestand()
    vorher = app_start(sp, 1)
    vorbereiten(sp, 1)
    pruefe("S1 Vorbereiten ändert nichts an dem, was die Rundgang-App startet", app_start(sp, 1) == vorher)
    pruefe("S1 Vorbereiten setzt Fassung 1 und RundgangID an allen Zeilen", all(x.get("Fassung") == 1 for x in sp.b + sp.k + sp.p) and all(x.get("RundgangID") == 1 for x in sp.k + sp.p))
    durch_kats = app_start(sp, 1)
    durch_alt = {k: app_kategorie(sp, k) for k in durch_kats}
    f2 = neue_fassung(sp, 1)
    pruefe("S2 neue Fassung = 2, Entwurf am Rundgang", f2 == 2 and sp.rg[1]["EntwurfFassung"] == 2)
    b2, k2, p2 = baum(sp, 1, 2, False)
    pruefe("S2 Kopie nur aktive Teile (2 Bereiche, 2 Kategorien, 3 Prüfpunkte)", (len(b2), len(k2), len(p2)) == (2, 2, 3))
    pruefe("S2 Entwurfs-Bereiche inaktiv, Rundgang-App startet unverändert", all(not x["Aktiv"] for x in b2) and app_start(sp, 1) == durch_kats)
    neu_b = next(x for x in p2 if x["Title"] == "Foto Schaden")
    neu_a = next(x for x in p2 if x["Title"] == "Sauber?")
    pruefe("S3 Bedingung zeigt auf die neue Frage A der Fassung 2", neu_b["Bed"] == neu_a["ID"] and neu_b["BedWert"] == "NIO")
    neu_a["Title"] = "Sauber und ordentlich?"
    pruefe("S4 Änderung im Entwurf wirkt nicht auf die laufende Durchführung", {k: app_kategorie(sp, k) for k in durch_kats} == durch_alt)
    _, _, mp, _ = kopie(sp, [], [], [neu_b], 1, 2, ziel_k=neu_b["KategorieID"], zusatz=" (Kopie)", colp=p2)
    dup = next(x for x in sp.p if x["ID"] == mp[0]["Neu"])
    pruefe("S5 Duplizieren in derselben Kategorie behält die Bedingung auf A", dup["Bed"] == neu_a["ID"])
    k_kueche = next(x for x in k2 if x["Title"] == "Küche")
    _, _, mp, _ = kopie(sp, [], [], [neu_b], 1, 2, ziel_k=k_kueche["ID"], colp=p2)
    pruefe("S5 Kopie in eine andere Kategorie löscht die Bedingung", next(x for x in sp.p if x["ID"] == mp[0]["Neu"])["Bed"] == 0)
    pruefe("S6 Schreibprüfung: offener Entwurf darf schreiben", check(sp, 1, 2))
    pruefe("S7 Aktivieren ok", aktivieren(sp, 1, 2) == "ok")
    neue_kats = app_start(sp, 1)
    pruefe("S7 Start nach dem Aktivieren nimmt nur Kategorien der Fassung 2", all(next(x for x in sp.k if x["ID"] == k)["Fassung"] == 2 for k in neue_kats) and len(neue_kats) == 2)
    pruefe("S7 laufende Durchführung (Momentaufnahme) öffnet weiter die alten Fragen", {k: app_kategorie(sp, k) for k in durch_kats} == durch_alt)
    pruefe("S8 veraltetes Fenster: Schreibprüfung verweigert", not check(sp, 1, 2))
    pruefe("S8 veraltetes Fenster: Laden zeigt nur lesen", laden_schreibbar(sp, 1, 2) == (False, False))
    pruefe("S8 nochmal Aktivieren aus veraltetem Fenster: verweigert", aktivieren(sp, 1, 2) == "veraltet")
    f3 = neue_fassung(sp, 1)
    pruefe("S9 halbes Aktivieren (Abbruch vor dem Rundgang-Patch)", aktivieren(sp, 1, f3, abbruch_nach_bereichen=True) == "abbruch")
    pruefe("S9 Verwerfen einer teilweise aktiven Fassung: verweigert", verwerfen(sp, 1) == "verweigert" and baum(sp, 1, f3, False)[0])
    pruefe("S9 Laden erkennt den Zwischenstand", laden_schreibbar(sp, 1, f3) == (False, True))
    pruefe("S9 erneutes Aktivieren schließt ab", aktivieren(sp, 1, f3) == "ok" and sp.rg[1]["Fassung"] == f3)
    f4 = neue_fassung(sp, 1)
    vor_akt = app_start(sp, 1)
    pruefe("S10 Verwerfen eines normalen Entwurfs löscht nur dessen Zeilen", verwerfen(sp, 1) == "verworfen" and app_start(sp, 1) == vor_akt and not baum(sp, 1, f4, False)[0])
    ziel_vor = max(x["Fassung"] for x in sp.b + sp.k + sp.p)
    p_fehler = baum(sp, 1, sp.rg[1]["Fassung"], True)[2][0]["ID"]
    vor = app_start(sp, 1)
    pruefe("S11 Kopierfehler bei neuer Fassung: Entwurf zurückgenommen", neue_fassung(sp, 1, fehler_bei=p_fehler) is None
           and sp.rg[1]["EntwurfFassung"] == 0 and max(x["Fassung"] for x in sp.b + sp.k + sp.p) == ziel_vor and app_start(sp, 1) == vor)
    sp2 = bestand()
    sp2.rg[1]["Aktiv"] = False
    reaktivieren(sp2, 1)
    pruefe("S12 Reaktivieren lässt Fassung leer (Vorbereiten läuft danach noch)", sp2.rg[1]["Fassung"] is None)
    sp.rg[50] = {"Aktiv": False, "Status": "Entwurf", "Fassung": 0, "EntwurfFassung": 1}
    qb, qk, qp = baum(sp, 1, sp.rg[1]["Fassung"], True)
    _, _, _, fehl = kopie(sp, qb, qk, qp, 50, 1, behalte=True)
    pruefe("S13 Kopie als neuer Rundgang: nichts startbar vor dem Aktivieren", fehl == 0 and app_start(sp, 50) is None)
    pruefe("S13 Aktivieren des neuen Rundgangs", aktivieren(sp, 50, 1) == "ok" and len(app_start(sp, 50)) == 2 and app_start(sp, 1) == vor)
    pruefe("S14 Aktivieren des einen Rundgangs ändert den anderen nicht", app_start(sp, 1) == vor)
    sp.rg[60] = {"Aktiv": False, "Status": "Vorlage", "Fassung": 0, "EntwurfFassung": 1}
    pruefe("S15 Vorlagen-Rundgang wird nie gestartet", app_start(sp, 60) is None and check(sp, 60, 1, vorlage=True))
    fehler = sum(1 for z in erg if z.startswith("FEHLER"))
    erg.append("")
    erg.append("Szenarien: %d, Fehler: %d" % (len(erg) - 1, fehler))
    os.makedirs(AUS, exist_ok=True)
    open(os.path.join(AUS, "logik_builder.txt"), "w", encoding="utf-8").write("\n".join(erg) + "\n")
    print("\n".join(erg))
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
