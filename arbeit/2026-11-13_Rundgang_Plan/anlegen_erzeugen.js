// Erzeugt das Konsolen-Skript rundgaenge_anlegen.js aus PLAN_RUNDGAENGE.csv (Einsetz-Chat, 13.11.2026).
// Aufruf: node anlegen_erzeugen.js
const fs = require("fs"), path = require("path");
const L = fs.readFileSync(path.join(__dirname, "PLAN_RUNDGAENGE.csv"), "utf8").replace(/^﻿/, "").split(/\r?\n/).filter(x => x.trim());
const H = L[0].split("|");
const rows = L.slice(1).map(l => { const f = l.split("|"); if (f.length !== H.length) throw new Error("Spaltenzahl falsch: " + l.slice(0, 80)); const o = {}; H.forEach((h, i) => o[h] = f[i]); return o; });

const PH_KONTAKT = "PLATZHALTER Ansprechpartner BMZ";
const PH_CODE = "PLATZHALTER Bedienteil Kältemaschine 1";
const zahl = s => { s = (s || "").trim(); if (!s) return null; const n = Number(s.replace(",", ".")); if (!isFinite(n)) throw new Error("keine Zahl: " + s); return n; };

const META = {
  "Infrastrukturrundgang TGI MMS": { reihe: 10, tage: [1, 3, 5] },
  "Brandschutzrundgang TGI MMS": { reihe: 20, tage: [1, 2, 3, 4, 5] },
  "Haustechnikrundgang TGI MMS": { reihe: 30, tage: [1] },
  "Legionellen Prävention TGI MMS": { reihe: 40, tage: [1] },
  "Sichtprüfung Gefahrstoffschränke TGI MMS": { reihe: 50, tage: [1] },
};

const AUFBAU = [];
for (const r of rows) {
  let rg = AUFBAU.find(x => x.name === r.Rundgang);
  if (!rg) { if (!META[r.Rundgang]) throw new Error("unbekannter Rundgang " + r.Rundgang); rg = { name: r.Rundgang, ...META[r.Rundgang], bereich: r.Bereich, ausblenden: r.Bereich_ausblenden === "Ja", kategorien: [] }; AUFBAU.push(rg); }
  if (r.Bereich !== rg.bereich) throw new Error("mehr als ein Bereich in " + rg.name);
  let k = rg.kategorien.find(x => x.name === r.Kategorie);
  if (!k) { k = { name: r.Kategorie, punkte: [] }; rg.kategorien.push(k); }
  else if (rg.kategorien[rg.kategorien.length - 1] !== k) throw new Error("Kategorie nicht zusammenhängend: " + r.Kategorie);
  const ex = r.Extras || "";
  const p = {
    nr: r.Nr, Title: r.Frage, Eingabetyp: r.Typ, Pflicht: r.Pflicht === "Ja", Einheit: r.Einheit || "",
    MinWert: zahl(r.ab), MaxWert: zahl(r.bis),
    Grenzmodus: ({ "Mangel": "Mangel", "Hinweis + Grund": "Warnen", "nicht speicherbar": "Sperren" }[r["Außerhalb"]] || "Mangel"),
    Hinweis: r.Hinweis || "", Abschnitt: r.Abschnitt || "", TextIO: r.TextIO || "", TextNIO: r.TextNIO || "",
    Kritisch: /KRITISCH/.test(ex), KritischText: /KRITISCH/.test(ex) ? "Bitte sofort melden." : "",
    _kontakt: /KRITISCH/.test(ex), _code: /🔑/.test(ex),
  };
  if (!["IONIO", "ZAHL", "TEXT"].includes(p.Eingabetyp)) throw new Error("Typ " + p.Eingabetyp);
  if (p.Title.length > 255) throw new Error("Frage zu lang: " + p.Title);
  if (p.TextIO.length > 18 || p.TextNIO.length > 18) throw new Error("Knopfwort > 18: " + p.Title);
  if (p.Eingabetyp !== "ZAHL" && (p.MinWert !== null || p.MaxWert !== null)) throw new Error("Grenze ohne Zahl: " + p.Title);
  k.punkte.push(p);
}

const daten = JSON.stringify(AUFBAU);
const skript = `// Die 5 echten Rundgänge anlegen (Plan „am Original“, 13.11.2026) – erzeugt aus arbeit/2026-11-13_Rundgang_Plan/PLAN_RUNDGAENGE.csv
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter.
// Sicherheit: Bricht ab, wenn einer der 5 Rundgänge schon existiert. Ändert nichts Bestehendes (nur neue Einträge).
// Platzhalter „${PH_CODE}“ (RG_Zugangscodes) und „${PH_KONTAKT}“ (RG_Ansprechpartner) werden nur angelegt, wenn es sie noch nicht gibt.
(async () => {
  const SITE = "https://technoformgroup.sharepoint.com/sites/IMSKonzept";
  const H = { "Accept": "application/json;odata=nometadata", "Content-Type": "application/json;odata=nometadata" };
  const digest = (await (await fetch(SITE + "/_api/contextinfo", { method: "POST", headers: H })).json()).FormDigestValue;
  const L = (n) => "/_api/web/lists/getbytitle('" + n + "')/items";
  const get = async (url) => { const r = await fetch(SITE + url, { headers: H }); if (!r.ok) throw new Error(url + " → " + r.status); return (await r.json()).value; };
  const add = async (liste, d) => {
    const r = await fetch(SITE + L(liste), { method: "POST", headers: { ...H, "X-RequestDigest": digest }, body: JSON.stringify(d) });
    if (!r.ok) throw new Error(liste + " „" + d.Title + "“ → " + r.status + " " + (await r.text()).slice(0, 300));
    return (await r.json()).Id;
  };
  const AUFBAU = ${daten};
  const esc = (s) => s.replace(/'/g, "''");
  for (const rg of AUFBAU) if ((await get(L("RG_Rundgaenge") + "?$select=Id&$filter=Title eq '" + esc(rg.name) + "'")).length) { console.warn("ABBRUCH: „" + rg.name + "“ gibt es schon. Nichts angelegt."); return; }

  const log = [];
  let codeId = ((await get(L("RG_Zugangscodes") + "?$select=Id&$filter=Title eq '" + esc("${PH_CODE}") + "'"))[0] || {}).Id;
  if (!codeId) { codeId = await add("RG_Zugangscodes", { Title: "${PH_CODE}", Code: "0000", Hinweis: "Platzhalter – echten Code eintragen (Besprechung A3).", Aktiv: true }); log.push("Zugangscode-Platzhalter angelegt: ID " + codeId); } else log.push("Zugangscode-Platzhalter war schon da: ID " + codeId);
  let kontaktId = ((await get(L("RG_Ansprechpartner") + "?$select=Id&$filter=Title eq '" + esc("${PH_KONTAKT}") + "'"))[0] || {}).Id;
  if (!kontaktId) { kontaktId = await add("RG_Ansprechpartner", { Title: "${PH_KONTAKT}", Kontakt: "noch offen", Telefon: "", Hinweis: "Platzhalter – mit Verantwortlichen klären (Besprechung A1).", Allgemein: false, Aktiv: true }); log.push("Ansprechpartner-Platzhalter angelegt: ID " + kontaktId); } else log.push("Ansprechpartner-Platzhalter war schon da: ID " + kontaktId);

  const TAGE = ["", "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
  const ids = {};
  for (const rg of AUFBAU) {
    const rid = await add("RG_Rundgaenge", { Title: rg.name, Beschreibung: "Nachbau MoreApp „Objektrundgang TGI MMS“ (Plan am Original, 13.11.2026).", RgReihenfolge: rg.reihe, Aktiv: true, Status: "Aktiv", Fassung: 1, EntwurfFassung: 0, EntwurfVon: "", Testrundgang: true, Standort: "TGI MMS", Adresse: "Matthäus-Merian-Straße 6, 34253 Lohfelden", Auftraggeber: "Technoform Glass Insulation GmbH" });
    const bid = await add("RG_Bereiche", { Title: rg.bereich, RundgangID: rid, RgReihenfolge: 10, Aktiv: true, Fassung: 1, QuelleID: 0, Ausblenden: rg.ausblenden });
    ids[rg.name] = { rundgang: rid, bereich: bid, kategorien: 0, pruefpunkte: 0, plaene: 0 };
    let kNr = 0;
    for (const k of rg.kategorien) {
      const kid = await add("RG_Kategorien", { Title: k.name, BereichID: bid, RundgangID: rid, RgReihenfolge: ++kNr * 10, Aktiv: true, Fassung: 1, QuelleID: 0 });
      ids[rg.name].kategorien++;
      let pNr = 0;
      for (const p of k.punkte) {
        const d = { Title: p.Title, KategorieID: kid, RundgangID: rid, Fassungf: 1, QuelleID: 0, RgReihenfolge: ++pNr * 10, Aktiv: true,
          Eingabetyp: p.Eingabetyp, Pflicht: p.Pflicht, Auswahlwerte: "", Einheit: p.Einheit, Hinweis: p.Hinweis,
          FotoMoeglich: false, Foto: "Aus", KommentarPflicht: false, Grenzmodus: p.Grenzmodus, BedingungPunkt: 0, BedingungWert: "", HinweisBildID: 0,
          Abschnitt: p.Abschnitt, Kritisch: p.Kritisch, KritischText: p.KritischText, Ansprechpartner: p._kontakt ? String(kontaktId) : "",
          Rueckfrage: false, RueckfrageText: "", TextIO: p.TextIO, TextNIO: p.TextNIO, NichtMessbar: false, AbwProzent: false, NurSteigend: false,
          VergleichPunkt: 0, VergleichTol: 0, AnleitungID: 0, ZugangscodeID: p._code ? codeId : 0 };
        if (p.MinWert !== null) d.MinWert = p.MinWert;
        if (p.MaxWert !== null) d.MaxWert = p.MaxWert;
        await add("RG_Pruefpunkte", d);
        ids[rg.name].pruefpunkte++;
      }
    }
    for (const w of rg.tage) { await add("RG_Plan", { Title: TAGE[w] + " (" + rg.name + ")", RundgangID: rid, Wochentag: w, ZyklusWochen: 1, StartMontag: "2026-11-09", Aktiv: true }); ids[rg.name].plaene++; }
    log.push(rg.name + ": Rundgang " + rid + " · Bereich " + bid + " · " + ids[rg.name].kategorien + " Kategorien · " + ids[rg.name].pruefpunkte + " Prüfpunkte · " + ids[rg.name].plaene + " Pläne");
  }
  console.log("FERTIG\\n" + log.join("\\n"));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken. Bereits Angelegtes bleibt stehen (nicht nochmal ausführen, erst melden)."));
`;
fs.writeFileSync(path.join(__dirname, "rundgaenge_anlegen.js"), skript);

// ---- Prüf-Skript für danach (nur lesen) ----
const soll = AUFBAU.map(r => ({ name: r.name, tage: r.tage, kats: r.kategorien.map(k => [k.name, k.punkte.length]), titel: r.kategorien.flatMap(k => k.punkte.map(p => p.Title)) }));
const pruef = `// Nach dem Anlegen ausführen (IMS+ → F12 → Konsole). LIEST NUR, ändert nichts. Prüft die 5 Rundgänge gegen den Plan.
(async () => {
  const S = "https://technoformgroup.sharepoint.com/sites/IMSKonzept/_api/web/lists/getbytitle";
  const g = async (u) => (await (await fetch(S + u, { headers: { Accept: "application/json;odata=nometadata" } })).json()).value;
  const SOLL = ${JSON.stringify(soll)};
  const fehler = [], info = [];
  for (const s of SOLL) {
    const rg = await g("('RG_Rundgaenge')/items?$filter=Title eq '" + s.name.replace(/'/g, "''") + "'");
    if (rg.length !== 1) { fehler.push(s.name + ": " + rg.length + " Rundgänge gefunden"); continue; }
    const r = rg[0];
    if (!(r.Aktiv && r.Status === "Aktiv" && r.Fassung === 1 && r.Testrundgang === true)) fehler.push(s.name + ": Rundgang-Felder");
    const ber = await g("('RG_Bereiche')/items?$filter=RundgangID eq " + r.Id);
    const kat = (await g("('RG_Kategorien')/items?$filter=RundgangID eq " + r.Id + "&$top=500")).sort((a, b) => a.RgReihenfolge - b.RgReihenfolge);
    const pp = await g("('RG_Pruefpunkte')/items?$filter=RundgangID eq " + r.Id + "&$top=2000");
    const pl = await g("('RG_Plan')/items?$filter=RundgangID eq " + r.Id);
    if (ber.length !== 1 || ber[0].Fassung !== 1 || !ber[0].Aktiv) fehler.push(s.name + ": Bereich");
    const istKats = kat.map(k => [k.Title, pp.filter(p => p.KategorieID === k.Id).length]);
    if (JSON.stringify(istKats) !== JSON.stringify(s.kats)) fehler.push(s.name + ": Kategorien/Anzahl " + JSON.stringify(istKats));
    if (pp.some(p => p.Fassungf !== 1 || !p.Aktiv)) fehler.push(s.name + ": Prüfpunkt ohne Fassung 1/aktiv");
    const ord = Object.fromEntries(kat.map(k => [k.Id, k.RgReihenfolge]));
    const titel = pp.sort((a, b) => ord[a.KategorieID] - ord[b.KategorieID] || a.RgReihenfolge - b.RgReihenfolge).map(p => p.Title);
    if (JSON.stringify(titel) !== JSON.stringify(s.titel)) fehler.push(s.name + ": Fragen/Reihenfolge weichen ab");
    if (JSON.stringify(pl.map(p => p.Wochentag).sort()) !== JSON.stringify([...s.tage].sort())) fehler.push(s.name + ": Plan " + pl.map(p => p.Wochentag));
    info.push(s.name + ": ID " + r.Id + " · " + kat.length + " Kategorien · " + pp.length + " Prüfpunkte · Plan " + pl.map(p => p.Wochentag).join(","));
  }
  console.log((fehler.length ? "FEHLER:\\n" + fehler.join("\\n") : "PRÜFUNG OK") + "\\n" + info.join("\\n"));
})().catch(e => console.error("FEHLER: " + e.message));
`;
fs.writeFileSync(path.join(__dirname, "rundgaenge_pruefen.js"), pruef);
const sum = AUFBAU.map(r => r.name + ": " + r.kategorien.length + " Kat, " + r.kategorien.reduce((a, k) => a + k.punkte.length, 0) + " PP, Tage " + r.tage.join(","));
console.log(sum.join("\n"));
