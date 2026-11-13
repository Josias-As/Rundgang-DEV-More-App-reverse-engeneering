// Erzeugt den Bauplan der 5 echten Rundgänge aus den Bildanalyse-CSVs + Planungsregeln (Einsetz-Chat, 13.11.2026).
// Aufruf: node plan_erzeugen.js  (im Ordner arbeit/2026-11-13_Rundgang_Plan)
const fs = require("fs"), path = require("path");
const SRC = path.join(__dirname, "..", "2026-11-10_Bildanalyse");
const lese = r => {
  const L = fs.readFileSync(path.join(SRC, "04_rundgang_" + r + ".csv"), "utf8").replace(/^﻿/, "").split(/\r?\n/).filter(x => x.trim());
  const H = L[0].replace("AbwMax (absolut|%)", "AbwMax (absolut/%)").split("|"); const ix = n => H.findIndex(h => h.startsWith(n));
  return L.slice(1).map(l => {
    const f = l.split("|"); const g = n => { const i = ix(n); return i >= 0 ? (f[i] || "").trim() : ""; };
    return { nr: +g("Nr"), kat: g("Kategorie"), abs: g("Abschnitt"), frage: g("Frage"), typ: g("Typ"), ein: g("Einheit"), min: g("Min"), max: g("Max"), gm: g("Grenzmodus"), tio: g("TextIO"), tnio: g("TextNIO"), tage: g("Tage"), quelle: g("Quelle"), sich: g("Sicherheit") };
  });
};

// ---------- Text-Bereinigung (dokumentiert) ----------
const tipp = [["Kältemschine", "Kältemaschine"], ["Kühlamellen", "Kühllamellen"], ["::", ":"]];
function sauber(t) {
  let s = t; const aend = [];
  for (const [a, b] of tipp) if (s.includes(a)) { s = s.split(a).join(b); aend.push("Tippfehler „" + a + "“ → „" + b + "“"); }
  s = s.replace(/:\s*$/, "");
  return { s: s.trim(), aend };
}

// ---------- Planungsregeln ----------
// Standard je Prüfpunkt: Pflicht Ja, Foto „kein Foto (bei n.i.O. möglich)“, Kommentar „Pflicht bei Mangel“, Grenzmodus Mangel.
function planen(rg, p) {
  const r = { ...p, pflicht: "Ja", foto: "Aus", komm: "bei Mangel", hinweis: "", extras: [], aend: [], grund: [] };
  const t = sauber(p.frage); r.frage = t.s; r.aend.push(...t.aend);
  const ta = sauber(p.abs); r.abs = ta.s; ta.aend.forEach(a => r.aend.push("Abschnitt: " + a));
  r.kat = sauber(p.kat).s;
  r.min = p.min; r.max = p.max; r.gm = p.typ === "ZAHL" ? (p.gm || "Mangel") : "";
  const f = r.frage.toLowerCase();
  if (p.typ === "ZAHL") {
    if (/zählerstand|betriebsstunden/.test(f)) { r.extras.push("nur steigend"); r.grund.push("Zähler kann nicht kleiner werden → fängt Tippfehler ab"); r.aend.push("neu: nur steigend"); }
    if (rg === "infrastruktur" && [49, 54, 56, 62, 67].includes(p.nr)) { r.extras.push("nicht messbar erlaubt"); r.grund.push("PDF 26.10. zeigt 0 (Gerät aus/keine Anzeige) → ehrliche Antwort statt 0"); r.aend.push("neu: nicht messbar erlaubt"); }
  }
  // Plausibilitätsgrenzen (Warnen) für Zahlen ohne Soll – geraten, nur Hinweis + Begründung, sperrt nie
  if (p.typ === "ZAHL" && !p.min && !p.max) {
    const pl = (mi, ma, w) => { r.min = mi; r.max = ma; r.gm = "Warnen"; r.grund.push("Plausibilität " + mi + "–" + ma + " (" + w + ") – GERATEN; außerhalb nur Hinweis + Begründung, kein Mangel, sperrt nie"); r.aend.push("neu: Plausibilitätsgrenze (Hinweis + Grund)"); };
    if (/^betriebsdruck/.test(f)) pl("4", "13", "Kompressor-Betriebsdruck");
    else if (/^temperatur$/.test(f) && /kompressor/i.test(r.abs)) pl("0", "110", "Kompressor; PDF 26.10.: 19/31/92 °C");
    else if (/wassertemperatur/.test(f)) pl("0", "30", "Kaltwasser Ausgang Kältemaschine");
    else if (/temperatur klimaanlage/.test(f)) pl("10", "35", "Raumtemperatur");
    else if (/füllung stickstoffflasche/.test(f)) pl("0", "300", "Flaschendruck");
  }
  // Rückfrage bei typischen „normalerweise ok“-Punkten (Kontrolle gegen Vertipper)
  const rf = (txt) => { r.extras.push("Rückfrage: „" + txt + "“"); r.grund.push("verhindert versehentliches n.i.O. bei Anlagen, die praktisch immer laufen"); r.aend.push("neu: Rückfrage"); };
  if (/störungsfrei|störungsanzeige/.test(f)) rf("Normalerweise ist die Anlage störungsfrei.");
  if (/im grünen bereich/.test(f)) rf("Normalerweise steht die Anzeige im grünen Bereich.");
  // Kritisch: Brandmeldezentrale / ÜE aus
  if (rg === "brandschutz" && /üe eingeschaltet/.test(f)) {
    r.extras.push("KRITISCH: „Brandmeldezentrale nicht zugänglich oder Übertragung zur Feuerwehr aus – sofort melden.“ Ansprechpartner: Brandschutzbeauftragter, Haustechnik-Leitung (Einträge noch anlegen)");
    r.grund.push("Ist die ÜE aus, geht ein Brandalarm nicht an die Feuerwehr – in MoreApp nicht vorhanden, Vorschlag"); r.aend.push("neu: kritisch");
  }
  // Zugangscode Kältemaschine 1 (Bedienteil)
  if (rg === "infrastruktur" && /kältemaschine 1/i.test(r.abs) && /wassertemperatur|betriebsstunden/.test(f)) {
    r.extras.push("🔑 Zugangscode „Bedienteil Kältemaschine 1“ (Wert trägt Josias ein)");
    r.grund.push("MoreApp zeigt den Code rot über dem Block (belegt) – bei uns erst nach Antippen sichtbar");
  }
  // Montags-Fragen: in Infrastruktur an allen Tagen, aber freiwillig
  if (rg === "infrastruktur" && p.tage === "Mo") { r.pflicht = "Nein"; r.hinweis = "Nur montags ablesen (in MoreApp nur am Montag). An anderen Tagen leer lassen."; r.aend.push("freiwillig statt Pflicht (nur Mo nötig)"); r.grund.push("„lieber mehr drin“: Frage ist an jedem Infrastruktur-Tag da; Pflicht wäre Mi/Fr falsch"); }
  // Brandschutz: Frage mit eingebauter Ausnahme trennen
  if (/^lagergut und abfall/.test(f)) { r.frage = "Lagergut und Abfall im Abstand von den Außenwänden abgestellt (5 m)"; r.hinweis = "Aufgrund der baulichen Gegebenheiten kann die 5 Meter Vorgabe nicht eingehalten werden."; r.aend.push("Satz 2 als Hinweis statt im Fragetext"); }
  // Haustechnik: Trinkwasser spülen → durchgeführt
  if (rg === "haustechnik" && /spülen der trinkwasser/i.test(p.abs) && !/rücksprache/.test(f)) {
    r.tio = "durchgeführt"; r.tnio = "nicht durchgeführt"; r.hinweis = "ca. 1–2 Minuten pro Entnahmestelle spülen."; r.abs = "Spülen der Trinkwasserleitungen";
    r.aend.push("Knöpfe „durchgeführt / nicht durchgeführt“ statt i.O./n.i.O.", "Zeitangabe aus Abschnitt als Hinweis"); r.grund.push("wie Legionellen: es wird eine Tätigkeit bestätigt, kein Zustand");
  }
  if (rg === "haustechnik" && /rücksprache mit kunde/.test(f)) {
    r.frage = "Rücksprache mit Kunde, ob Reinigungszustand zufriedenstellend"; r.tio = "zufriedenstellend"; r.tnio = "nicht zufrieden"; r.hinweis = "Wenn nicht: im Kommentar näher dokumentieren (wird als Mangel erfasst)."; r.abs = "Reinigung";
    r.aend.push("eigener Abschnitt „Reinigung“", "Knöpfe „zufriedenstellend / nicht zufrieden“", "Klammertext als Hinweis"); r.grund.push("gehört nicht zum Spülen; „Mängelprotokoll“ = bei uns Kommentar + Mangel");
  }
  if (rg === "haustechnik" && /sofort entfernen lassen/.test(f)) { r.frage = "Kontrolle der Beschaffenheit auf Verschmutzung"; r.hinweis = "Verschmutzungen sofort entfernen lassen!"; r.aend.push("Klammer-Anweisung als Hinweis"); }
  if (rg === "legionellen") { r.hinweis = "10 Minuten Wasser mit mind. 60 °C durchlaufen lassen."; r.frage = r.frage.replace(/\s*\(10 Minuten.*\)\s*$/, ""); r.aend.push("Klammer-Anweisung als Hinweis"); }
  if (rg === "gefahrstoffschraenke") { r.abs = r.abs.replace(/\s*Service Nr\.\/ Barcode:\s*/, " · Service-Nr. "); r.grund.push("Quelle nur PDF 28.10. (Unterformular nicht fotografiert)"); }
  if (p.typ === "IONIO" && /min\. 1 karton|mind\. 60 °c/.test(f)) r.grund.push("Grenze steht im Text, MoreApp fragt aber i.O./n.i.O. → bleibt i.O./n.i.O.");
  return r;
}

// ---------- Gliederung je Rundgang ----------
const GL = {
  infrastruktur: { name: "Infrastrukturrundgang TGI MMS", plan: "Mo, Mi, Fr – jede Woche", aus: false, kat: (p) => {
    if (p.kat === "Batterieraum") return ["Batterieraum", "Batterieraum"];
    if (p.kat === "Infrastrukturraum") { const n = p.nr; return ["Infrastrukturraum", n <= 16 ? "Heizung und Kompressoren" : n <= 22 ? "Kältetrockner und Wasseraufbereitung" : n <= 30 ? "ONI Kühlanlage" : "Kältemaschinen"]; }
    if (p.kat === "Produktionshalle") return ["Produktionshalle", p.nr <= 54 ? "Produktionshalle – Räume und Klima" : "Produktionshalle – Zähler, Tore, Technik"];
    return ["Büro 1. OG", "Serverraum"]; } },
  brandschutz: { name: "Brandschutzrundgang TGI MMS", plan: "Mo–Fr – jede Woche", aus: true, kat: (p) => {
    if (/Brandmelde/.test(p.kat)) return ["Brandschutz", "Brandmeldezentrale (BMZ)"];
    if (/Infrastrukturraum/.test(p.kat)) return ["Brandschutz", "Infrastrukturraum / Produktionshalle"];
    if (p.kat === "Produktionshalle") return ["Brandschutz", p.nr <= 17 ? "Produktionshalle – Sanitär, Außenbereich, Büros" : "Produktionshalle – Hallenbereich und Tore"];
    return ["Brandschutz", "Brandschutz allgemein"]; } },
  haustechnik: { name: "Haustechnikrundgang TGI MMS", plan: "Mo – jede Woche", aus: true, kat: (p) => {
    if (p.kat === "Büro 1. OG") return ["Haustechnik", /Allgemein/.test(p.abs) ? "Büro 1. OG" : "Büro 1. OG – Küche und Besucher-WCs"];
    if (p.kat === "Allgemein") return ["Haustechnik", "Trinkwasser und Reinigung"];
    return ["Haustechnik", p.kat]; } },
  legionellen: { name: "Legionellen Prävention TGI MMS", plan: "Mo – jede Woche (MoreApp: Mittwoch, s. E3)", aus: true, kat: () => ["Legionellen", "Legionellen Prävention"] },
  gefahrstoffschraenke: { name: "Sichtprüfung Gefahrstoffschränke TGI MMS", plan: "Mo – jede Woche (MoreApp: Mittwoch, s. E3)", aus: true, kat: () => ["Gefahrstoffschränke", "Gefahrstoffschränke"] },
};

const md = [], csv = ["Rundgang|Bereich|Bereich_ausblenden|Kategorie|Abschnitt|Nr|Frage|Typ|Pflicht|Einheit|ab|bis|Außerhalb|Foto|Kommentar|Hinweis|TextIO|TextNIO|Extras|Änderung ggü. MoreApp|Begründung|Quelle|Sicherheit"];
const zus = {};
for (const rg of Object.keys(GL)) {
  const g = GL[rg]; const P = lese(rg).map(p => planen(rg, p));
  P.forEach(p => { const [b, k] = g.kat(p); p.ber = b; p.k = k; });
  const last = P[P.length - 1];
  P.push({ nr: "+1", ber: last.ber, k: last.k, abs: "Abschluss", frage: "Bemerkungen", typ: "TEXT", pflicht: "Nein", ein: "", min: "", max: "", gm: "", foto: "Aus", komm: "bei Mangel", hinweis: "Freiwillig: alles, was sonst nirgends hinpasst.", tio: "", tnio: "", extras: [], aend: ["neu: entspricht „Bemerkungen:“ am Ende des MoreApp-Formulars"], grund: ["MoreApp hat am Ende ein freies Bemerkungsfeld (belegt MD 124814)"], quelle: "MD 124814", sich: "belegt" });
  const kats = [...new Set(P.map(p => p.ber + " › " + p.k))];
  zus[rg] = { name: g.name, n: P.length, kats: kats.map(k => k + " (" + P.filter(p => p.ber + " › " + p.k === k).length + ")") };
  md.push("## " + g.name, "", "- **Plan:** " + g.plan, "- **Bereich-Überschrift:** " + (g.aus ? "ausgeblendet" : "sichtbar (Batterieraum, Infrastrukturraum, Produktionshalle, Büro 1. OG)"), "- **Kopfdaten:** Standort „TGI MMS“ · Adresse „Matthäus-Merian-Straße 6, 34253 Lohfelden“ · Auftraggeber „Technoform Glass Insulation GmbH“", "- **Testrundgang:** Ja (bis Inbetriebnahme)", "- **Gliederung:** " + zus[rg].kats.join(" · "), "");
  let kk = "";
  for (const p of P) {
    const key = p.ber + " › " + p.k;
    if (key !== kk) { kk = key; md.push("", "### " + key, "", "| Nr | Abschnitt | Frage (so in die App) | Typ | Pflicht | Einheit | ab | bis | außerhalb | Hinweis | Extras | Änderung ggü. MoreApp |", "|---|---|---|---|---|---|---|---|---|---|---|---|"); }
    const typT = p.typ === "IONIO" ? (p.tio ? "i.O./n.i.O. („" + p.tio + "“ / „" + p.tnio + "“)" : "i.O./n.i.O.") : ({ ZAHL: "Zahl", TEXT: "Text" }[p.typ] || p.typ);
    const gm = p.typ === "ZAHL" && (p.min || p.max) ? ({ Mangel: "Mangel", Warnen: "Hinweis + Grund", Sperren: "nicht speicherbar" }[p.gm]) : "";
    md.push("| " + [p.nr, p.abs, p.frage, typT, p.pflicht, p.ein, p.min, p.max, gm, p.hinweis, p.extras.join("<br>"), p.aend.join("; ")].map(x => String(x || "").replace(/\|/g, "/")).join(" | ") + " |");
    csv.push([g.name, p.ber, g.aus ? "Ja" : "Nein", p.k, p.abs, p.nr, p.frage, p.typ, p.pflicht, p.ein, p.min, p.max, gm, "kein Foto (bei n.i.O. möglich)", "Pflicht bei Mangel", p.hinweis, p.tio, p.tnio, p.extras.join("; "), p.aend.join("; "), p.grund.join("; "), p.quelle, p.sich].map(x => String(x || "").replace(/\|/g, "/")).join("|"));
  }
  md.push("");
}
fs.writeFileSync(path.join(__dirname, "plan_tabellen.md"), md.join("\n"));
fs.writeFileSync(path.join(__dirname, "PLAN_RUNDGAENGE.csv"), "﻿" + csv.join("\n"));
console.log(JSON.stringify(zus, null, 1));
