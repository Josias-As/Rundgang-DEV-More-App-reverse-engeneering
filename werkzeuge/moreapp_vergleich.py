"""Vergleich MoreApp-Formular (abgeschriebene Screenshots) mit den MoreApp-PDF-Protokollen.
Aufruf: python3 -I werkzeuge/moreapp_vergleich.py  ->  arbeit/2026-11-03_MoreApp_Vergleich/abgleich.txt
Die Fragen aus den Bildern sind von Hand abgeschrieben (Bilder quellen/2026-11-03_MoreApp_Bilder/infrastruktur/01-16)."""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARB = os.path.join(REPO, "arbeit", "2026-11-03_MoreApp_Vergleich")
PDFS = ["2026-10-26_Infrastrukturrundgang_TGI_MMS", "2026-10-26_Haustechnikrundgang_TGI_MMS",
        "2026-10-28_Legionellen_Praevention_TGI_MMS", "2026-10-28_Sichtpruefung_Gefahrstoffschraenke_TGI_MMS"]

J = "IO"
Z = "ZAHL"
KOMP = [("Betriebsdruck", Z, "bar"), ("Betriebsstunden", Z, "h"), ("Temperatur", Z, "°C"), ("Kontrolle Druckluftfilter (Störungsfrei)", J, "")]
KM23 = [("Kontrolle Kühllamellen", J, ""), ("Wassertemperatur (Ausgang)", Z, "°C"), ("Betriebsstunden A1", Z, "h"),
        ("Betriebsstunden B1/ C1", Z, "h"), ("Kontrolle Störungsanzeige", J, "")]
BILDER = {
    "Infrastrukturraum (IS)": [
        ("", [("Sichtprüfung Heizungsanlage", J, ""), ("Zählerstand Wasseruhr", Z, "m³"),
              ("Druckmanometer Heizung (schwarz, 1,5 bis 2,0 bar)", Z, "bar")]),
        ("Kompressor 3", KOMP), ("Kompressor 2", KOMP), ("Kompressor 1", KOMP),
        ("Kältetrockner 1", [("Sichtprüfung Betriebszustand (im Grünen Bereich)", J, "")]),
        ("Kältetrockner 2", [("Sichtprüfung Betriebszustand (im Grünen Bereich)", J, "")]),
        ("Wasseraufbereitung (Jansen)", [("Kontrolle Vorrat Biozid", J, ""), ("Kontrolle Vorrat Korrosionsschutz", J, ""),
                                         ("Kontrolle Wasseraufbereitung (Störungsfrei)", J, "")]),
        ("Öwamat", [("Kontrolle Wasserqualität Öwamat (mit Teststreifen)", J, "")]),
        ("ONI Kühlanlage", [("Kontrolle Ordnung und Sauberkeit", J, ""), ("Druck Heizungspumpe (WR6) PCC71 (min. 2,0 bar)", Z, "bar"),
                            ("Kontrolle Siebkorbfilter 1 (ab 0,5 bar Reinigung)", J, ""), ("Kontrolle Siebkorbfilter 2 (ab 0,5 bar Reinigung)", J, ""),
                            ("Kontrolle Verschmutzung Pumpen (Lüfterräder)", J, ""), ("Kontrolle Schrägsitzfilter", J, ""),
                            ("Kontrolle Luftfilter Schaltschrank", J, ""), ("Zählerstand Wasseruhr über Tank", Z, "m³")]),
        ("Kältemschine 1 (Außenbereich/ Display im Infrastrukturraum)", [
            ("Kontrolle Kühlamellen", J, ""), ("Wassertemperatur (Ausgang)", Z, "°C"), ("Betriebsstunden C1", Z, "h"),
            ("Betriebsstunden C2", Z, "h"), ("Kontrolle Störungsanzeige", J, "")]),
        ("Kältemaschine 2 (Außenbereich)", KM23),
        ("Kältemaschine 3 (Außenbereich/ Display im Infrastrukturraum)", KM23),
    ],
    "Produktionshalle (Bilder 10-16)": [
        ("Sanitärräume (Herren WC)", [("Kontrolle Ordnung und Sauberkeit Herren WC", J, ""),
                                      ("Kontrolle Füllstand Seifenspender Herren WC (ggf. nachfüllen)", J, ""),
                                      ("Kontrolle Füllstand Handtuchpapierspender Herren WC (ggf. nachfüllen)", J, "")]),
        ("Sanitärräume (Damen WC)", [("Kontrolle Ordnung und Sauberkeit Damen WC", J, ""),
                                     ("Kontrolle Füllstand Seifenspender Damen WC (ggf. nachfüllen)", J, ""),
                                     ("Kontrolle Füllstand Handtuchpapierspender Damen WC (ggf. nachfüllen)", J, ""),
                                     ("Kontrolle Temperatur aller Durchlauferhitzer (mind. 60 °C)", J, "")]),
        ("Außenbereich", [("Kontrolle Ordnung und Sauberkeit (Wareneingang)", J, ""), ("Kontrolle Aschenbecher/ Beleuchtung (Wareneingang)", J, ""),
                          ("Kontrolle der Wartungsaufkleber an allen Abfallcontainern immer bei Austausch: Presscontainer nach UVV freigeprüft, Container/Mulden nach BGR186 freigeprüft", J, ""),
                          ("Kontrolle der Sicherung gegen Einschalten der Selbstpresscontainer (Schlüssel (w.v.) abgezogen, Not-Aus-Schalter gedrückt)", J, "")]),
        ("WZB", [("Kontrolle Ordnung und Sauberkeit", J, "")]),
        ("Analysebüro", [("Kontrolle Ordnung und Sauberkeit", J, "")]),
        ("Allgemein", [("Sichtprüfung Regal-Liftsystem", J, ""), ("Sichtprüfung Hochregale", J, ""),
                       ("Kontrolle destilliertes Wasser (Staplerstation)", J, ""), ("Kontrolle allgemeine Deckenbeleuchtung", J, ""),
                       ("Kontrolle Erste-Hilfe-Kästen / Pflasterboxen", J, ""), ("Kontrolle Gehörschutzboxen", J, "")]),
        ("Außenbereich (2)", [("Kontrolle Aschenbecher/ Beleuchtung (Tor 2)", J, ""), ("Kontrolle Ordnung und Sauberkeit (Containerbereich)", J, ""),
                              ("Kontrolle Beleuchtung (Tor 3)", J, ""), ("Kontrolle Beleuchtung (Tor 4)", J, ""),
                              ("Kontrolle Aschenbecher/ Beleuchtung (Tor 5)", J, ""), ("Kontrolle Beleuchtung (Tor 6)", J, ""),
                              ("Kontrolle Ordnung und Sauberkeit (Warenausgang)", J, "")]),
        ("Konfektion", [("Kontrolle Ordnung und Sauberkeit", J, "")]),
        ("Messstation", [("Kontrolle Funktion Staubsauger", J, "")]),
        ("Küchenbereich", [("Kontrolle Ordnung und Sauberkeit", J, "")]),
    ],
}


def norm(t):
    t = t.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    t = t.replace("kaeltemschine", "kaeltemaschine").replace("kuehlamellen", "kuehllamellen")
    return re.sub(r"[^a-z0-9]", "", t)


ANTWORT = re.compile(r"\s{2,}(nicht in Ordnung|in Ordnung|durchgeführt|-?[\d.,]+ ?[^\s:]*(?: [^\s:]+)?)$")


def pdf_text(name):
    """Fließtext des PDFs ohne Antworten (normalisiert) und Zahl der Antwortzeilen."""
    zeilen = [z.rstrip() for z in open(os.path.join(ARB, name + ".txt"), encoding="utf-8") if z.strip()]
    antworten, rest = 0, []
    for z in zeilen:
        if re.search(r"Datum:|Kalenderwoche|Adresse:|Kunde:", z):
            continue
        if ANTWORT.search(z) or re.fullmatch(r"\s{20,}(nicht in Ordnung|in Ordnung|durchgeführt|[\d.,]+ ?\S*( \S+)?)", z):
            antworten += 1
        rest.append(re.sub(r"\s{2,}(nicht in Ordnung|in Ordnung|durchgeführt)\s*$", " ", z))
    return norm(" ".join(rest)), antworten


def main():
    out = []
    pdf = {n: pdf_text(n) for n in PDFS}
    out.append("Abgleich über den Fragetext (Antworten zählen: siehe VERGLEICH, von Hand gezählt).")
    for teil, abschnitte in BILDER.items():
        n_ges = n_treffer = 0
        out += ["", "== " + teil]
        for ab, fragen in abschnitte:
            for frage, typ, einheit in fragen:
                n_ges += 1
                treffer = [n.split("_")[1] for n, (t, _) in pdf.items() if norm(frage) in t]
                if treffer:
                    n_treffer += 1
                out.append("  [%s] %-4s %-55s -> %s" % (ab[:28], typ, frage[:55], ", ".join(treffer) or "IN KEINEM PDF"))
        out.append("  Summe: %d Fragen in den Bildern, %d davon (Fragetext) in einem PDF" % (n_ges, n_treffer))
    open(os.path.join(ARB, "abgleich.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(l for l in out if not l.startswith("  [")))


if __name__ == "__main__":
    main()
