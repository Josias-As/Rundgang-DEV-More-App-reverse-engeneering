// Prüfung des Konsolen-Skripts rundgaenge_anlegen.js ohne SharePoint (simulierte Antworten).
// Vergleicht jeden geschriebenen Eintrag unabhängig mit den Bildanalyse-CSVs (04_rundgang_*.csv).
const fs = require("fs"), path = require("path"), vm = require("vm");
const fehler = []; const F = (m) => fehler.push(m);

// ---- 1) Skript in Sandbox mit Fake-fetch ausführen ----
const posts = []; let nextId = 1000; const existing = { RG_Rundgaenge: [], RG_Zugangscodes: [], RG_Ansprechpartner: [] };
async function fakeFetch(url, opt = {}) {
  const liste = (url.match(/getbytitle\('([^']+)'\)/) || [])[1];
  const ok = (body) => ({ ok: true, status: 200, json: async () => body, text: async () => JSON.stringify(body) });
  if (url.endsWith("/_api/contextinfo")) return ok({ FormDigestValue: "x" });
  if ((opt.method || "GET") === "GET") return ok({ value: [] });
  const d = JSON.parse(opt.body); const id = ++nextId; posts.push({ liste, id, d }); return ok({ Id: id });
}
const code = process.env.PRUEF_CODE || fs.readFileSync(path.join(__dirname, "rundgaenge_anlegen.js"), "utf8");
const logs = [];
const ctx = { fetch: fakeFetch, console: { log: (...a) => logs.push(a.join(" ")), warn: (...a) => logs.push("WARN " + a.join(" ")), error: (...a) => logs.push("ERR " + a.join(" ")) }, JSON, String, Number, Promise };
vm.createContext(ctx);
const done = vm.runInContext(code, ctx);

setTimeout(() => {
  if (logs.some(l => /^ERR|WARN/.test(l))) F("Skript meldet: " + logs.join(" | "));
  // ---- 2) Unabhängige Soll-Daten aus der Bildanalyse ----
  const SRC = path.join(__dirname, "..", "2026-11-10_Bildanalyse");
  const lese = r => { const L = fs.readFileSync(path.join(SRC, "04_rundgang_" + r + ".csv"), "utf8").replace(/^﻿/, "").split(/\r?\n/).filter(x => x.trim());
    const H = L[0].replace("AbwMax (absolut|%)", "AbwMax").split("|"); return L.slice(1).map(l => { const f = l.split("|"); const o = {}; H.forEach((h, i) => o[h.split(" ")[0]] = (f[i] || "").trim()); return o; }); };
  const NAMEN = { infrastruktur: "Infrastrukturrundgang TGI MMS", brandschutz: "Brandschutzrundgang TGI MMS", haustechnik: "Haustechnikrundgang TGI MMS", legionellen: "Legionellen Prävention TGI MMS", gefahrstoffschraenke: "Sichtprüfung Gefahrstoffschränke TGI MMS" };
  const TAGE = { infrastruktur: [1, 3, 5], brandschutz: [1, 2, 3, 4, 5], haustechnik: [1], legionellen: [1], gefahrstoffschraenke: [1] };
  const norm = s => s.replace(/Kältemschine/g, "Kältemaschine").replace(/Kühlamellen/g, "Kühllamellen").replace(/::/g, ":").replace(/:\s*$/, "").trim();
  const num = s => s ? Number(s.replace(",", ".")) : undefined;

  const byList = l => posts.filter(p => p.liste === l);
  const rgPosts = byList("RG_Rundgaenge");
  if (rgPosts.length !== 5) F("Rundgänge: " + rgPosts.length + " statt 5");
  const code = byList("RG_Zugangscodes"), kon = byList("RG_Ansprechpartner");
  if (code.length !== 1 || code[0].d.Code !== "0000") F("Zugangscode-Platzhalter falsch");
  if (kon.length !== 1) F("Ansprechpartner-Platzhalter falsch");
  let gesamt = 0;
  for (const [key, name] of Object.entries(NAMEN)) {
    const soll = lese(key);
    const rg = rgPosts.find(p => p.d.Title === name); if (!rg) { F("Rundgang fehlt: " + name); continue; }
    const r = rg.d;
    if (!(r.Aktiv === true && r.Status === "Aktiv" && r.Fassung === 1 && r.EntwurfFassung === 0 && r.Testrundgang === true && r.Standort && r.Adresse && r.Auftraggeber)) F(name + ": Rundgang-Felder " + JSON.stringify(r));
    const ber = byList("RG_Bereiche").filter(p => p.d.RundgangID === rg.id);
    if (ber.length !== 1 || ber[0].d.Ausblenden !== true || ber[0].d.Fassung !== 1 || ber[0].d.Aktiv !== true) F(name + ": Bereich " + JSON.stringify(ber.map(b => b.d)));
    const kats = byList("RG_Kategorien").filter(p => p.d.RundgangID === rg.id);
    kats.forEach(k => { if (k.d.BereichID !== ber[0].id || k.d.Fassung !== 1 || k.d.Aktiv !== true) F(name + ": Kategorie " + k.d.Title); });
    const sollKats = [...new Set(soll.map(s => norm(s.Kategorie)))];
    const istKats = kats.sort((a, b) => a.d.RgReihenfolge - b.d.RgReihenfolge).map(k => k.d.Title);
    if (JSON.stringify(sollKats) !== JSON.stringify(istKats)) F(name + ": Kategorien Soll " + sollKats.join(" / ") + " ≠ Ist " + istKats.join(" / "));
    const pps = byList("RG_Pruefpunkte").filter(p => p.d.RundgangID === rg.id);
    // Reihenfolge: Kategorie-Reihenfolge, dann RgReihenfolge
    const kOrd = Object.fromEntries(kats.map(k => [k.id, k.d.RgReihenfolge]));
    pps.sort((a, b) => kOrd[a.d.KategorieID] - kOrd[b.d.KategorieID] || a.d.RgReihenfolge - b.d.RgReihenfolge);
    if (pps.length !== soll.length + 1) F(name + ": Prüfpunkte " + pps.length + " statt " + (soll.length + 1));
    gesamt += pps.length;
    soll.forEach((s, i) => {
      const p = pps[i] && pps[i].d; if (!p) return;
      const kat = kats.find(k => k.id === p.KategorieID).d.Title;
      const exp = { Title: norm(s.Frage), Eingabetyp: s.Typ, Kategorie: norm(s.Kategorie), Abschnitt: norm(s.Abschnitt), Einheit: s.Einheit, MinWert: num(s.Min), MaxWert: num(s.Max), TextIO: s.TextIO, TextNIO: s.TextNIO,
        Pflicht: !(key === "infrastruktur" && s.Tage === "Mo") };
      const ist = { Title: p.Title, Eingabetyp: p.Eingabetyp, Kategorie: kat, Abschnitt: p.Abschnitt, Einheit: p.Einheit, MinWert: p.MinWert, MaxWert: p.MaxWert, TextIO: p.TextIO, TextNIO: p.TextNIO, Pflicht: p.Pflicht };
      for (const f in exp) if ((exp[f] ?? "") !== (ist[f] ?? "")) F(name + " Nr " + s.Nr + " " + f + ": Soll „" + exp[f] + "“ Ist „" + ist[f] + "“");
      if (p.Fassungf !== 1 || p.QuelleID !== 0 || p.Aktiv !== true || p.Foto !== "Aus" || p.KommentarPflicht !== false || p.Rueckfrage !== false || p.NurSteigend !== false || p.NichtMessbar !== false) F(name + " Nr " + s.Nr + ": Standardfelder");
      if (s.Typ === "ZAHL" && p.Grenzmodus !== "Mangel") F(name + " Nr " + s.Nr + ": Grenzmodus " + p.Grenzmodus);
      const sollCode = key === "infrastruktur" && /Kältem.*1/.test(s.Abschnitt) && /Wassertemperatur|Betriebsstunden/.test(s.Frage);
      if ((p.ZugangscodeID === code[0].id) !== sollCode) F(name + " Nr " + s.Nr + ": Zugangscode " + p.ZugangscodeID);
      const sollKrit = key === "brandschutz" && /ÜE eingeschaltet/.test(s.Frage);
      if (p.Kritisch !== sollKrit || (sollKrit && p.Ansprechpartner !== String(kon[0].id)) || (!sollKrit && p.Ansprechpartner !== "")) F(name + " Nr " + s.Nr + ": Kritisch/Ansprechpartner");
      if (p.Pflicht === false && !/montags/.test(p.Hinweis)) F(name + " Nr " + s.Nr + ": freiwillig ohne Hinweis");
    });
    const last = pps[pps.length - 1] && pps[pps.length - 1].d;
    if (!last || last.Title !== "Bemerkungen" || last.Eingabetyp !== "TEXT" || last.Pflicht !== false) F(name + ": Bemerkungen am Ende fehlt");
    const pl = byList("RG_Plan").filter(p => p.d.RundgangID === rg.id).map(p => p.d.Wochentag);
    if (JSON.stringify(pl) !== JSON.stringify(TAGE[key])) F(name + ": Plan " + pl + " statt " + TAGE[key]);
    byList("RG_Plan").filter(p => p.d.RundgangID === rg.id).forEach(p => { if (p.d.StartMontag !== "2026-11-09" || p.d.ZyklusWochen !== 1 || p.d.Aktiv !== true) F(name + ": Plan-Felder"); });
  }
  // Keine unbekannten Felder
  const erlaubt = { RG_Pruefpunkte: "Title KategorieID RundgangID Fassungf QuelleID RgReihenfolge Aktiv Eingabetyp Pflicht Auswahlwerte Einheit Hinweis FotoMoeglich Foto KommentarPflicht Grenzmodus BedingungPunkt BedingungWert HinweisBildID Abschnitt Kritisch KritischText Ansprechpartner Rueckfrage RueckfrageText TextIO TextNIO NichtMessbar AbwProzent NurSteigend VergleichPunkt VergleichTol AnleitungID ZugangscodeID MinWert MaxWert",
    RG_Rundgaenge: "Title Beschreibung RgReihenfolge Aktiv Status Fassung EntwurfFassung EntwurfVon Testrundgang Standort Adresse Auftraggeber", RG_Bereiche: "Title RundgangID RgReihenfolge Aktiv Fassung QuelleID Ausblenden",
    RG_Kategorien: "Title BereichID RundgangID RgReihenfolge Aktiv Fassung QuelleID", RG_Plan: "Title RundgangID Wochentag ZyklusWochen StartMontag Aktiv", RG_Zugangscodes: "Title Code Hinweis Aktiv", RG_Ansprechpartner: "Title Kontakt Telefon Hinweis Allgemein Aktiv" };
  for (const p of posts) for (const k of Object.keys(p.d)) if (!erlaubt[p.liste].split(" ").includes(k)) F(p.liste + ": unbekanntes Feld " + k);
  console.log("POSTS " + posts.length + " · Prüfpunkte gesamt " + gesamt + " · Konsole: " + logs.join(" | ").slice(0, 400));
  console.log(fehler.length ? "FEHLER (" + fehler.length + "):\n" + fehler.join("\n") : "PRÜFUNG OK – 0 Abweichungen");
}, 500);
