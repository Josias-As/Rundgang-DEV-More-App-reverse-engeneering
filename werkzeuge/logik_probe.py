"""Gegenprobe der App.Formulas-Funktionen der Baukasten-Pakete in Python.

Die Funktionen bilden die Power-Fx-Formeln aus bloecke.json Zeile für Zeile nach (None = Blank).
Geprüft werden: (1) Rückwärtsgleichheit mit dem alten fnFehlt/fnZahlBewertung für alle Kombinationen,
die es vor den Paketen gab, (2) die Szenarien je Paket mit erwartetem Ergebnis.
Aufruf: python3 -I werkzeuge/logik_probe.py  -> arbeit/2026-10-27_Baukasten/logik_probe.txt
"""
import itertools
import os

AUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "arbeit", "2026-10-27_Baukasten")


def leer(x):
    return x is None or x == ""


def trim(x):
    return "" if x is None else str(x).strip()


# ---------------------------------------------------------------- alter Stand (Export)

def alt_fnFehlt(typ, pflicht, bew, wt, wz, kom):
    return (pflicht and ((typ == "IONIO" and leer(bew)) or (typ == "AUSWAHL" and leer(wt))
                         or (typ == "ZAHL" and wz is None) or (typ == "TEXT" and trim(wt) == ""))) \
        or (bew == "NIO" and trim(kom) == "")


def alt_fnZahlBewertung(z, mi, ma):
    return "NIO" if ((mi is not None and z < mi) or (ma is not None and z > ma)) else "IO"


# ---------------------------------------------------------------- neue Funktionen (Stand nach Paket n)

def fnLinkAnzahl(t):
    return len([s for s in (t or "").split(" | ") if s.strip() != ""])


def fnFotoModus(f, alt, paket=7):
    if f in ("Aus", "Optional", "Pflicht"):
        return f
    if paket >= 7 and f == "Bei Mangel Pflicht":
        return "BeiMangel"
    return "Optional" if alt else "Aus"


def fnBeantwortet(bew, wt, wz):
    return not leer(bew) or trim(wt) != "" or wz is not None


def fnAusserhalb(z, mi, ma):
    return z is not None and ((mi is not None and z < mi) or (ma is not None and z > ma))


def fnKommentarNoetig(paket, typ, bew, wt, wz, kpfl, gm, mi, ma):
    r = bew == "NIO"
    if paket >= 2:
        r = r or (kpfl and fnBeantwortet(bew, wt, wz))
    if paket >= 3:
        r = r or (typ == "ZAHL" and gm == "Warnen" and fnAusserhalb(wz, mi, ma))
    if paket >= 16:
        r = r or (typ == "ZAHL" and wt == "nicht messbar")
    return r


def fnFehltGrund(paket, typ, pflicht, bew, wt, wz, kom, foto, fanz, kpfl, gm, mi, ma, kritoffen=False):
    wert = (typ == "IONIO" and leer(bew)) or (typ == "AUSWAHL" and leer(wt)) or (typ == "ZAHL" and wz is None and (paket < 16 or leer(wt))) \
        or (typ == "TEXT" and trim(wt) == "")
    if paket >= 5:
        wert = wert or (typ == "MEHRFACH" and trim(wt) == "") or (typ in ("DATUM", "DATUMZEIT") and leer(wt))
    if pflicht and wert:
        return "Wert"
    if paket >= 5 and typ == "DATUMZEIT" and not leer(wt) and (len(wt) < 16 or (paket >= 20 and "-" in wt)):
        return "Uhrzeit"
    if paket >= 3 and typ == "ZAHL" and gm == "Sperren" and fnSperreGilt(mi, ma) and fnAusserhalb(wz, mi, ma):
        return "Bereich"
    if fnKommentarNoetig(paket, typ, bew, wt, wz, kpfl, gm, mi, ma) and trim(kom) == "":
        return "Kommentar"
    if (foto == "Pflicht" or (paket >= 7 and foto == "BeiMangel" and bew == "NIO")) and fanz < 1:
        return "Foto"
    if paket >= 9 and kritoffen and bew == "NIO":
        return "Kritisch"
    return ""


def fnAbweichung(z, l, mx, proz, steig):
    if z is None or l is None:
        return False
    if steig and z < l:
        return True
    return mx is not None and round(abs(z - l), 6) > round(abs(l) * mx / 100 if proz else mx, 6)


def fnVergleich(z, w, tol):
    return z is not None and w is not None and round(abs(z - w), 6) > round(tol or 0, 6)


def fnFehlt(paket, *args):
    return fnFehltGrund(paket, *args) != ""


def fnSperreGilt(mi, ma):
    return mi is None or ma is None or mi <= ma


def fnFotoNeuErlaubt(bew, foto):
    return bew == "NIO" or foto in ("Optional", "Pflicht")


def fnZahlBewertung(paket, z, mi, ma, gm):
    if paket < 3:
        return alt_fnZahlBewertung(z, mi, ma)
    if fnAusserhalb(z, mi, ma):
        g = "Mangel" if (gm == "Sperren" and not fnSperreGilt(mi, ma)) else gm
        return {"Warnen": "IO", "Sperren": ""}.get(g, "NIO")
    return "IO"


def fnGrenzmodus(g):
    return g if g in ("Warnen", "Sperren") else "Mangel"


def fnBedNorm(w):
    return trim(w).replace(".", "").replace(" ", "").lower()


def fnBedGueltig(w, typ, auswahl):
    n = fnBedNorm(w)
    return n == "*" or (typ in ("IONIO", "ZAHL") and n in ("io", "nio")) or \
        (typ in ("AUSWAHL", "MEHRFACH") and any(fnBedNorm(s) == n for s in (auswahl or "").split(";")))


def fnBedPasst(w, bew, wt, wz):
    n = fnBedNorm(w)
    if n == "*":
        return fnBeantwortet(bew, wt, wz)
    return n == fnBedNorm(bew) or n == fnBedNorm(wt) or any(fnBedNorm(s) == n for s in (wt or "").split(";"))


def fnSichtbar(bid, w, gef, bbid, binaktiv, btyp, bauswahl, bbew, bwt, bwz):
    return bid == 0 or trim(w) == "" or not gef or bool(binaktiv) or bbid != 0 or not fnBedGueltig(w, btyp, bauswahl) \
        or fnBedPasst(w, bbew, bwt, bwz)


def fnDatumText(d, h, m, mit_zeit):
    if d is None:
        return ""
    return d + (" " + (h or "--") + ":" + (m or "--") if mit_zeit and (h != "" or m != "") else "")



def uhr_ablauf(schritte):
    """Paket 21: Folge von Eingaben (("D", "02.11.2026") / ("H", "08") / ("M", "30"), "" = abgewählt) auf WertText einer DATUMZEIT-Karte.
    Nach jedem Schreiben feuern alle drei OnChange erneut mit ihrem Default (Neuzeichnen) – das darf nichts ändern."""
    wt = ""

    def teil(i):
        return wt[i:i + 2] if len(wt) >= 16 else "--"

    def datum(d):
        nonlocal wt
        if (d or "") != wt[:10]:
            h, m = teil(11), teil(14)
            wt = fnDatumText(d or None, "" if h == "--" else h, "" if m == "--" else m, True)

    def zeit(wert, eigen, rest_i, links):
        nonlocal wt
        neu = wert or "--"
        if len(wt) >= 10 and neu != teil(eigen):
            rest = teil(rest_i)
            wt = wt[:10] + ("" if neu == "--" and rest == "--" else " " + (neu + ":" + rest if links else rest + ":" + neu))

    def neuzeichnen():
        d = wt[:10] if len(wt) >= 10 else ""
        h = teil(11) if teil(11) != "--" else ""
        m = teil(14) if teil(14) != "--" else ""
        datum(d)
        zeit(h, 11, 14, True)
        zeit(m, 14, 11, False)

    for art, wert in schritte:
        {"D": datum, "H": lambda w: zeit(w, 11, 14, True), "M": lambda w: zeit(w, 14, 11, False)}[art](wert)
        vorher = wt
        neuzeichnen()
        if wt != vorher:
            return "INSTABIL " + vorher + " -> " + wt
    return wt


# ---------------------------------------------------------------- Prüfungen

def rueckwaerts():
    """Für alle Kombinationen des alten Wertebereichs: neues fnFehlt (Foto Aus, keine Kommentarpflicht,
    Grenzmodus Mangel) == altes fnFehlt, in jedem Paketstand."""
    typen = ["IONIO", "AUSWAHL", "ZAHL", "TEXT"]
    bews = ["", "IO", "NIO"]
    wts = ["", " ", "x"]
    wzs = [None, 0, 5.5]
    koms = ["", " ", "k"]
    n = 0
    for paket in range(1, 7):
        for typ, pfl, bew, wt, wz, kom in itertools.product(typen, [True, False], bews, wts, wzs, koms):
            a = alt_fnFehlt(typ, pfl, bew, wt, wz, kom)
            b = fnFehlt(min(paket, 5), typ, pfl, bew, wt, wz, kom, "Aus", 0, False, "Mangel", None, None)
            assert a == b, (paket, typ, pfl, bew, wt, wz, kom, a, b)
            n += 1
        for z, mi, ma in itertools.product([-1, 0, 5, 10, 11], [None, 0, 5], [None, 5, 10]):
            assert alt_fnZahlBewertung(z, mi, ma) == fnZahlBewertung(min(paket, 5), z, mi, ma, "Mangel")
            n += 1
    return n


SZENARIEN = [
    # (Paket, Beschreibung, Funktion, Argumente, Erwartung)
    (1, "Foto Pflicht, kein Foto, sonst alles ausgefüllt", "grund", ("IONIO", True, "IO", "", None, "", "Pflicht", 0, False, "Mangel", None, None), "Foto"),
    (1, "Foto Pflicht, 1 neues Foto (colFotos)", "grund", ("IONIO", True, "IO", "", None, "", "Pflicht", 1, False, "Mangel", None, None), ""),
    (1, "Foto Pflicht, Foto schon gespeichert (Link)", "grund", ("IONIO", True, "IO", "", None, "", "Pflicht", fnLinkAnzahl("https://x/a.jpg"), False, "Mangel", None, None), ""),
    (1, "Foto Pflicht, Punkt nicht Pflicht und unbeantwortet", "grund", ("IONIO", False, "", "", None, "", "Pflicht", 0, False, "Mangel", None, None), "Foto"),
    (1, "Foto Optional, kein Foto", "grund", ("IONIO", True, "IO", "", None, "", "Optional", 0, False, "Mangel", None, None), ""),
    (1, "n.i.O. ohne Kommentar und Foto Pflicht ohne Foto: Kommentar zuerst", "grund", ("IONIO", True, "NIO", "", None, "", "Pflicht", 0, False, "Mangel", None, None), "Kommentar"),
    (1, "Pflicht-Wert fehlt vor allem anderen", "grund", ("IONIO", True, "", "", None, "", "Pflicht", 0, False, "Mangel", None, None), "Wert"),
    (1, "fnFotoModus: Spalte leer, FotoMoeglich Ja -> Optional", "foto", ("", True), "Optional"),
    (1, "fnFotoModus: Spalte leer, FotoMoeglich Nein -> Aus", "foto", (None, False), "Aus"),
    (1, "fnFotoModus: Spalte Aus schlägt FotoMoeglich Ja", "foto", ("Aus", True), "Aus"),
    (1, "fnLinkAnzahl leer", "links", ("",), 0),
    (1, "fnLinkAnzahl zwei Links", "links", ("u1 | u2",), 2),
    (2, "Kommentarpflicht, i.O., kein Kommentar", "grund", ("IONIO", True, "IO", "", None, "", "Aus", 0, True, "Mangel", None, None), "Kommentar"),
    (2, "Kommentarpflicht, i.O., mit Kommentar", "grund", ("IONIO", True, "IO", "", None, "ok", "Aus", 0, True, "Mangel", None, None), ""),
    (2, "Kommentarpflicht, optionaler Punkt unbeantwortet", "grund", ("IONIO", False, "", "", None, "", "Aus", 0, True, "Mangel", None, None), ""),
    (2, "Kommentarpflicht, Text-Punkt mit Eingabe ohne Kommentar", "grund", ("TEXT", False, "", "abc", None, "", "Aus", 0, True, "Mangel", None, None), "Kommentar"),
    (2, "ohne Kommentarpflicht, i.O. ohne Kommentar", "grund", ("IONIO", True, "IO", "", None, "", "Aus", 0, False, "Mangel", None, None), ""),
    (2, "Kommentar leeren beim Speichern: i.O. ohne Pflicht -> leeren", "komm", ("IONIO", "IO", "", None, False, "Mangel", None, None), False),
    (2, "Kommentar leeren beim Speichern: i.O. mit Pflicht -> behalten", "komm", ("IONIO", "IO", "", None, True, "Mangel", None, None), True),
    (3, "Mangel: 18,5 bei Soll 6–16 -> n.i.O.", "zahl", (18.5, 6, 16, "Mangel"), "NIO"),
    (3, "Warnen: 18,5 bei Soll 6–16 -> i.O. (kein Mangel)", "zahl", (18.5, 6, 16, "Warnen"), "IO"),
    (3, "Sperren: 18,5 bei Soll 6–16 -> unbewertet", "zahl", (18.5, 6, 16, "Sperren"), ""),
    (3, "Warnen: Wert im Bereich -> i.O.", "zahl", (10, 6, 16, "Warnen"), "IO"),
    (3, "Warnen außerhalb: Kommentar Pflicht", "grund", ("ZAHL", True, "IO", "", 18.5, "", "Aus", 0, False, "Warnen", 6, 16), "Kommentar"),
    (3, "Warnen außerhalb mit Kommentar: vollständig", "grund", ("ZAHL", True, "IO", "", 18.5, "Fühler defekt", "Aus", 0, False, "Warnen", 6, 16), ""),
    (3, "Sperren außerhalb: unzulässig, Speichern gesperrt", "grund", ("ZAHL", True, "", "", 18.5, "", "Aus", 0, False, "Sperren", 6, 16), "Bereich"),
    (3, "Sperren außerhalb mit Kommentar: trotzdem gesperrt", "grund", ("ZAHL", True, "", "", 18.5, "x", "Aus", 0, False, "Sperren", 6, 16), "Bereich"),
    (3, "Sperren im Bereich: vollständig", "grund", ("ZAHL", True, "IO", "", 10, "", "Aus", 0, False, "Sperren", 6, 16), ""),
    (3, "Grenze genau auf Min (6) ist im Bereich", "zahl", (6, 6, 16, "Mangel"), "IO"),
    (3, "fnGrenzmodus: leere Spalte -> Mangel", "gm", ("",), "Mangel"),
    (3, "fnGrenzmodus: unbekannter Wert -> Mangel", "gm", ("warnen ",), "Mangel"),
    (4, "Bedingung NIO, A ist n.i.O. -> B sichtbar", "sicht", (7, "NIO", True, 0, False, "IONIO", "", "NIO", "", None), True),
    (4, "Bedingung NIO, A ist i.O. -> B ausgeblendet", "sicht", (7, "NIO", True, 0, False, "IONIO", "", "IO", "", None), False),
    (4, "Bedingung NIO, A unbeantwortet -> B ausgeblendet", "sicht", (7, "NIO", True, 0, False, "IONIO", "", "", "", None), False),
    (4, "Bedingung klein geschrieben (nio)", "sicht", (7, "nio", True, 0, False, "IONIO", "", "NIO", "", None), True),
    (4, "Bedingung * und A hat Text", "sicht", (7, "*", True, 0, False, "TEXT", "", "", "abc", None), True),
    (4, "Bedingung * und A leer", "sicht", (7, "*", True, 0, False, "TEXT", "", "", "", None), False),
    (4, "Bedingung Auswahlwert", "sicht", (7, "defekt", True, 0, False, "AUSWAHL", "ok;defekt", "", "defekt", None), True),
    (4, "Bedingung Wert in Mehrfachauswahl", "sicht", (7, "Leck", True, 0, False, "MEHRFACH", "Riss;Leck;Korrosion", "", "Riss; Leck", None), True),
    (4, "Fehlkonfiguration: Punkt A nicht in der Kategorie -> B sichtbar", "sicht", (99, "NIO", False, 0, False, "IONIO", "", "", "", None), True),
    (4, "Fehlkonfiguration: A selbst bedingt (Kette) -> B sichtbar", "sicht", (7, "NIO", True, 3, False, "IONIO", "", "IO", "", None), True),
    (4, "Fehlkonfiguration: Bedingungswert leer -> B sichtbar", "sicht", (7, "", True, 0, False, "IONIO", "", "IO", "", None), True),
    (4, "A deaktiviert (mitgeführt) -> B sichtbar", "sicht", (7, "NIO", True, 0, True, "IONIO", "", "IO", "", None), True),
    (4, "keine Bedingung (0) -> sichtbar", "sicht", (0, "", False, 0, False, "IONIO", "", "", "", None), True),
    (4, "Schreibweise n.i.O. wie NIO", "sicht", (7, "n.i.O.", True, 0, False, "IONIO", "", "NIO", "", None), True),
    (4, "Schreibweise i.O. bei A n.i.O. -> ausgeblendet", "sicht", (7, "i.O.", True, 0, False, "IONIO", "", "NIO", "", None), False),
    (4, "Tippfehler im Bedingungswert (Rot bei i.O./n.i.O.) -> B sichtbar", "sicht", (7, "Rot", True, 0, False, "IONIO", "", "IO", "", None), True),
    (4, "Liste als Bedingungswert (Rot;Gelb) -> B sichtbar", "sicht", (7, "Rot;Gelb", True, 0, False, "AUSWAHL", "Rot;Gelb;Grün", "", "Rot", None), True),
    (4, "Auswahlwert, den es in A nicht gibt -> B sichtbar", "sicht", (7, "kaputt", True, 0, False, "AUSWAHL", "ok;defekt", "", "ok", None), True),
    (4, "Auswahlwert passt nicht (A = ok) -> ausgeblendet", "sicht", (7, "defekt", True, 0, False, "AUSWAHL", "ok;defekt", "", "ok", None), False),
    (4, "Bedingung NIO bei Text-Punkt A (ungültig) -> B sichtbar", "sicht", (7, "NIO", True, 0, False, "TEXT", "", "", "abc", None), True),
    (1, "fnFotoNeuErlaubt: i.O. und Aus -> nein", "neu", ("IO", "Aus"), False),
    (1, "fnFotoNeuErlaubt: n.i.O. und Aus -> ja", "neu", ("NIO", "Aus"), True),
    (1, "fnFotoNeuErlaubt: i.O. und Optional -> ja", "neu", ("IO", "Optional"), True),
    (3, "Sperren mit Min > Max: wie Mangel (n.i.O.), nicht gesperrt", "zahl", (12, 16, 6, "Sperren"), "NIO"),
    (3, "Sperren mit Min > Max: kein Bereich-Fehler, Kommentar verlangt", "grund", ("ZAHL", True, "NIO", "", 12, "", "Aus", 0, False, "Sperren", 16, 6), "Kommentar"),
    (3, "Sperren nur Max gesetzt, Wert darüber", "grund", ("ZAHL", True, "", "", 200, "", "Aus", 0, False, "Sperren", None, 150), "Bereich"),
    (3, "Dezimalzahl 16,01 bei Max 16 -> außerhalb", "zahl", (16.01, 6, 16, "Mangel"), "NIO"),
    (3, "Warnen ohne Min/Max: nie außerhalb", "grund", ("ZAHL", True, "IO", "", 999, "", "Aus", 0, False, "Warnen", None, None), ""),
    (5, "Mehrfach Pflicht leer", "grund", ("MEHRFACH", True, "", "", None, "", "Aus", 0, False, "Mangel", None, None), "Wert"),
    (5, "Mehrfach Pflicht zwei Werte", "grund", ("MEHRFACH", True, "", "a; b", None, "", "Aus", 0, False, "Mangel", None, None), ""),
    (5, "Datum Pflicht leer", "grund", ("DATUM", True, "", "", None, "", "Aus", 0, False, "Mangel", None, None), "Wert"),
    (5, "Datum gesetzt", "grund", ("DATUM", True, "", "27.10.2026", None, "", "Aus", 0, False, "Mangel", None, None), ""),
    (5, "Datum+Uhrzeit nur Datum", "grund", ("DATUMZEIT", True, "", "27.10.2026", None, "", "Aus", 0, False, "Mangel", None, None), "Uhrzeit"),
    (5, "Datum+Uhrzeit optional, nur Datum -> trotzdem unvollständig", "grund", ("DATUMZEIT", False, "", "27.10.2026", None, "", "Aus", 0, False, "Mangel", None, None), "Uhrzeit"),
    (5, "Datum+Uhrzeit vollständig", "grund", ("DATUMZEIT", True, "", "27.10.2026 07:05", None, "", "Aus", 0, False, "Mangel", None, None), ""),
    (5, "Datum+Uhrzeit optional leer", "grund", ("DATUMZEIT", False, "", "", None, "", "Aus", 0, False, "Mangel", None, None), ""),
    (5, "fnDatumText nur Datum (DATUM)", "datum", ("27.10.2026", "07", "05", False), "27.10.2026"),
    (5, "fnDatumText Datum + Zeit", "datum", ("27.10.2026", "07", "05", True), "27.10.2026 07:05"),
    (5, "fnDatumText Zeit ohne Minute (ab 20 mit Platzhalter)", "datum", ("27.10.2026", "07", "", True), "27.10.2026 07:--"),
    (21, "Uhr: Datum, Stunde, Minute", "uhr", ([("D", "02.11.2026"), ("H", "08"), ("M", "30")],), "02.11.2026 08:30"),
    (21, "Uhr: Datum, nur Stunde", "uhr", ([("D", "02.11.2026"), ("H", "08")],), "02.11.2026 08:--"),
    (21, "Uhr: Minute vor Stunde", "uhr", ([("D", "02.11.2026"), ("M", "30"), ("H", "08")],), "02.11.2026 08:30"),
    (21, "Uhr: Datum ändern behält Uhrzeit", "uhr", ([("D", "02.11.2026"), ("H", "08"), ("M", "30"), ("D", "03.11.2026")],), "03.11.2026 08:30"),
    (21, "Uhr: Stunde abwählen", "uhr", ([("D", "02.11.2026"), ("H", "08"), ("M", "30"), ("H", "")],), "02.11.2026 --:30"),
    (21, "Uhr: beides abwählen -> nur Datum", "uhr", ([("D", "02.11.2026"), ("H", "08"), ("H", "")],), "02.11.2026"),
    (21, "Uhr: Stunde ohne Datum wird ignoriert", "uhr", ([("H", "08")],), ""),
    (21, "Uhr: Datum löschen", "uhr", ([("D", "02.11.2026"), ("H", "08"), ("D", "")],), ""),
    (20, "fnDatumText Minute ohne Stunde", "datum", ("27.10.2026", "", "30", True), "27.10.2026 --:30"),
    (20, "Datum+Uhrzeit nur Stunde -> Uhrzeit fehlt", "grund", ("DATUMZEIT", True, "", "27.10.2026 07:--", None, "", "Aus", 0, False, "Mangel", None, None), "Uhrzeit"),
    (20, "Datum+Uhrzeit nur Minute -> Uhrzeit fehlt", "grund", ("DATUMZEIT", False, "", "27.10.2026 --:30", None, "", "Aus", 0, False, "Mangel", None, None), "Uhrzeit"),
    (5, "fnDatumText ohne Datum", "datum", (None, "07", "05", True), ""),
    (7, "fnFotoModus: Bei Mangel Pflicht -> BeiMangel", "foto", ("Bei Mangel Pflicht", False), "BeiMangel"),
    (7, "Bei Mangel Pflicht, i.O., kein Foto -> vollständig", "grund", ("IONIO", True, "IO", "", None, "", "BeiMangel", 0, False, "Mangel", None, None), ""),
    (7, "Bei Mangel Pflicht, n.i.O. mit Kommentar, kein Foto -> Foto", "grund", ("IONIO", True, "NIO", "", None, "Riss", "BeiMangel", 0, False, "Mangel", None, None), "Foto"),
    (7, "Bei Mangel Pflicht, n.i.O. mit Kommentar und Foto -> vollständig", "grund", ("IONIO", True, "NIO", "", None, "Riss", "BeiMangel", 1, False, "Mangel", None, None), ""),
    (7, "Bei Mangel Pflicht, n.i.O. ohne Kommentar -> Kommentar zuerst", "grund", ("IONIO", True, "NIO", "", None, "", "BeiMangel", 0, False, "Mangel", None, None), "Kommentar"),
    (7, "Bei Mangel Pflicht, Zahl außerhalb (Mangel) mit Kommentar ohne Foto -> Foto", "grund", ("ZAHL", True, "NIO", "", 50, "zu wenig", "BeiMangel", 0, False, "Mangel", 100, 1000), "Foto"),
    (7, "Bei Mangel Pflicht, Zahl außerhalb bei Warnen (i.O.) -> kein Foto nötig", "grund", ("ZAHL", True, "IO", "", 50, "Grund", "BeiMangel", 0, False, "Warnen", 100, 1000), ""),
    (7, "Bei Mangel Pflicht, unbeantwortet optional -> nichts fehlt", "grund", ("IONIO", False, "", "", None, "", "BeiMangel", 0, False, "Mangel", None, None), ""),
    (7, "fnFotoNeuErlaubt: i.O. und BeiMangel -> nein", "neu", ("IO", "BeiMangel"), False),
    (7, "fnFotoNeuErlaubt: n.i.O. und BeiMangel -> ja", "neu", ("NIO", "BeiMangel"), True),
    (9, "kritisch: n.i.O. mit Kommentar, nicht bestätigt", "grund", ("IONIO", True, "NIO", "", None, "k", "Aus", 0, False, "Mangel", None, None, True), "Kritisch"),
    (9, "kritisch: n.i.O. mit Kommentar, bestätigt", "grund", ("IONIO", True, "NIO", "", None, "k", "Aus", 0, False, "Mangel", None, None, False), ""),
    (9, "kritisch: Antwort i.O. braucht keine Bestätigung", "grund", ("IONIO", True, "IO", "", None, "", "Aus", 0, False, "Mangel", None, None, True), ""),
    (9, "kritisch: Kommentar fehlt geht vor Bestätigung", "grund", ("IONIO", True, "NIO", "", None, "", "Aus", 0, False, "Mangel", None, None, True), "Kommentar"),
    (9, "kritisch: Zahl außerhalb (Mangel), unbestätigt", "grund", ("ZAHL", True, "NIO", "", 12, "k", "Aus", 0, False, "Mangel", 0, 10, True), "Kritisch"),
    (16, "nicht messbar, Pflicht, ohne Kommentar", "grund", ("ZAHL", True, "", "nicht messbar", None, "", "Aus", 0, False, "Mangel", 0, 10), "Kommentar"),
    (16, "nicht messbar mit Begründung", "grund", ("ZAHL", True, "", "nicht messbar", None, "Anlage aus", "Aus", 0, False, "Mangel", 0, 10), ""),
    (16, "Zahl leer, Pflicht -> Wert fehlt (unverändert)", "grund", ("ZAHL", True, "", "", None, "", "Aus", 0, False, "Mangel", 0, 10), "Wert"),
    (16, "Zahl 5 innerhalb, kein Kommentar nötig (unverändert)", "grund", ("ZAHL", True, "IO", "", 5, "", "Aus", 0, False, "Mangel", 0, 10), ""),
    (16, "fnKommentarNoetig: nicht messbar -> ja", "komm", ("ZAHL", "", "nicht messbar", None, False, "Mangel", 0, 10), True),
    (14, "Abweichung: 7,6 -> 7,9 bei max 0,5 absolut", "abw", (7.9, 7.6, 0.5, False, False), False),
    (14, "Abweichung: 7,6 -> 8,2 bei max 0,5 absolut", "abw", (8.2, 7.6, 0.5, False, False), True),
    (14, "Abweichung: 100 -> 109 bei max 10 %", "abw", (109, 100, 10, True, False), False),
    (14, "Abweichung: 100 -> 111 bei max 10 %", "abw", (111, 100, 10, True, False), True),
    (14, "Zähler: 5000 -> 4999 (nur steigend, ohne Max)", "abw", (4999, 5000, None, False, True), True),
    (14, "Zähler: 5000 -> 5600 (nur steigend, ohne Max)", "abw", (5600, 5000, None, False, True), False),
    (14, "kein letzter Wert (erster Lauf)", "abw", (8.2, None, 0.5, False, True), False),
    (14, "kein Wert eingegeben", "abw", (None, 7.6, 0.5, False, False), False),
    (14, "Vergleich: 7,6 und 7,7 bei Toleranz 0,2", "vgl", (7.6, 7.7, 0.2), False),
    (14, "Vergleich: 7,6 und 8,0 bei Toleranz 0,2", "vgl", (7.6, 8.0, 0.2), True),
    (14, "Vergleich: Toleranz 0 = exakt gleich", "vgl", (5, 5, 0), False),
    (14, "Vergleich: anderer Wert fehlt noch", "vgl", (5, None, 0), False),
    (14, "Vergleich: 1,1 und 0,8 bei Toleranz 0,3 (Gleitkomma-Grenze)", "vgl", (1.1, 0.8, 0.3), False),
]


def fuehre(paket, art, args):
    p = paket if paket >= 7 else min(paket, 5)
    if art == "grund":
        return fnFehltGrund(p, *args)
    if art == "komm":
        return fnKommentarNoetig(p, *args)
    if art == "zahl":
        return fnZahlBewertung(p, *args)
    if art == "foto":
        return fnFotoModus(*args, paket=p)
    if art == "links":
        return fnLinkAnzahl(*args)
    if art == "gm":
        return fnGrenzmodus(*args)
    if art == "sicht":
        return fnSichtbar(*args)
    if art == "datum":
        return fnDatumText(*args)
    if art == "neu":
        return fnFotoNeuErlaubt(*args)
    if art == "uhr":
        return uhr_ablauf(*args)
    if art == "abw":
        return fnAbweichung(*args)
    if art == "vgl":
        return fnVergleich(*args)
    raise ValueError(art)


def main():
    n = rueckwaerts()
    zeilen = ["Rückwärtsgleichheit: %d Kombinationen gleich (fnFehlt alt = neu bei Foto Aus/keine Kommentarpflicht/Mangel, "
              "fnZahlBewertung alt = neu bei Mangel), in allen Paketständen" % n, ""]
    fehler = 0
    for paket, text, art, args, erwartet in SZENARIEN:
        ist = fuehre(paket, art, args)
        ok = ist == erwartet
        fehler += not ok
        zeilen.append("P%d  %-4s  %-70s erwartet %-12r ist %r" % (paket, "ok" if ok else "FEHLER", text, erwartet, ist))
    # spätere Pakete dürfen frühere Szenarien nicht brechen
    for paket, text, art, args, erwartet in SZENARIEN:
        for spaeter in sorted({paket, 7, 9, 14, 16} - set(range(0, paket))):
            if fuehre(spaeter, art, args) != erwartet:
                fehler += 1
                zeilen.append("FEHLER: Szenario P%d '%s' ändert sich in Paket %d" % (paket, text, spaeter))
    zeilen.append("")
    zeilen.append("Szenarien: %d, Fehler: %d" % (len(SZENARIEN), fehler))
    os.makedirs(AUS, exist_ok=True)
    open(os.path.join(AUS, "logik_probe.txt"), "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
    print("\n".join(zeilen))
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
