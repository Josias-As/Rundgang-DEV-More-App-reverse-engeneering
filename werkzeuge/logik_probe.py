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


def fnFotoModus(f, alt):
    if f in ("Aus", "Optional", "Pflicht"):
        return f
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
    return r


def fnFehltGrund(paket, typ, pflicht, bew, wt, wz, kom, foto, fanz, kpfl, gm, mi, ma):
    wert = (typ == "IONIO" and leer(bew)) or (typ == "AUSWAHL" and leer(wt)) or (typ == "ZAHL" and wz is None) \
        or (typ == "TEXT" and trim(wt) == "")
    if paket >= 5:
        wert = wert or (typ == "MEHRFACH" and trim(wt) == "") or (typ in ("DATUM", "DATUMZEIT") and leer(wt))
    if pflicht and wert:
        return "Wert"
    if paket >= 5 and typ == "DATUMZEIT" and not leer(wt) and len(wt) < 16:
        return "Uhrzeit"
    if paket >= 3 and typ == "ZAHL" and gm == "Sperren" and fnAusserhalb(wz, mi, ma):
        return "Bereich"
    if fnKommentarNoetig(paket, typ, bew, wt, wz, kpfl, gm, mi, ma) and trim(kom) == "":
        return "Kommentar"
    if foto == "Pflicht" and fanz < 1:
        return "Foto"
    return ""


def fnFehlt(paket, *args):
    return fnFehltGrund(paket, *args) != ""


def fnZahlBewertung(paket, z, mi, ma, gm):
    if paket < 3:
        return alt_fnZahlBewertung(z, mi, ma)
    if fnAusserhalb(z, mi, ma):
        return {"Warnen": "IO", "Sperren": ""}.get(gm, "NIO")
    return "IO"


def fnGrenzmodus(g):
    return g if g in ("Warnen", "Sperren") else "Mangel"


def fnBedPasst(w, bew, wt, wz):
    w2 = trim(w).lower()
    if w2 == "*":
        return fnBeantwortet(bew, wt, wz)
    return w2 == (bew or "").lower() or w2 == trim(wt).lower() or any(trim(s).lower() == w2 for s in (wt or "").split(";"))


def fnSichtbar(bid, w, gef, bbid, binaktiv, bbew, bwt, bwz):
    return bid == 0 or trim(w) == "" or not gef or bool(binaktiv) or bbid != 0 or fnBedPasst(w, bbew, bwt, bwz)


def fnDatumText(d, h, m, mit_zeit):
    if d is None:
        return ""
    return d + (" " + h + ":" + m if mit_zeit and h != "" and m != "" else "")


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
    (4, "Bedingung NIO, A ist n.i.O. -> B sichtbar", "sicht", (7, "NIO", True, 0, False, "NIO", "", None), True),
    (4, "Bedingung NIO, A ist i.O. -> B ausgeblendet", "sicht", (7, "NIO", True, 0, False, "IO", "", None), False),
    (4, "Bedingung NIO, A unbeantwortet -> B ausgeblendet", "sicht", (7, "NIO", True, 0, False, "", "", None), False),
    (4, "Bedingung klein geschrieben (nio)", "sicht", (7, "nio", True, 0, False, "NIO", "", None), True),
    (4, "Bedingung * und A hat Text", "sicht", (7, "*", True, 0, False, "", "abc", None), True),
    (4, "Bedingung * und A leer", "sicht", (7, "*", True, 0, False, "", "", None), False),
    (4, "Bedingung Auswahlwert", "sicht", (7, "defekt", True, 0, False, "", "defekt", None), True),
    (4, "Bedingung Wert in Mehrfachauswahl", "sicht", (7, "Leck", True, 0, False, "", "Riss; Leck", None), True),
    (4, "Fehlkonfiguration: Punkt A nicht in der Kategorie -> B sichtbar", "sicht", (99, "NIO", False, 0, False, "", "", None), True),
    (4, "Fehlkonfiguration: A selbst bedingt (Kette) -> B sichtbar", "sicht", (7, "NIO", True, 3, False, "IO", "", None), True),
    (4, "Fehlkonfiguration: Bedingungswert leer -> B sichtbar", "sicht", (7, "", True, 0, False, "IO", "", None), True),
    (4, "A deaktiviert (mitgeführt) -> B sichtbar", "sicht", (7, "NIO", True, 0, True, "IO", "", None), True),
    (4, "keine Bedingung (0) -> sichtbar", "sicht", (0, "", False, 0, False, "", "", None), True),
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
    (5, "fnDatumText Zeit ohne Minute", "datum", ("27.10.2026", "07", "", True), "27.10.2026"),
    (5, "fnDatumText ohne Datum", "datum", (None, "07", "05", True), ""),
]


def fuehre(paket, art, args):
    p = min(paket, 5)
    if art == "grund":
        return fnFehltGrund(p, *args)
    if art == "komm":
        return fnKommentarNoetig(p, *args)
    if art == "zahl":
        return fnZahlBewertung(p, *args)
    if art == "foto":
        return fnFotoModus(*args)
    if art == "links":
        return fnLinkAnzahl(*args)
    if art == "gm":
        return fnGrenzmodus(*args)
    if art == "sicht":
        return fnSichtbar(*args)
    if art == "datum":
        return fnDatumText(*args)
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
        for spaeter in range(paket, 7):
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
