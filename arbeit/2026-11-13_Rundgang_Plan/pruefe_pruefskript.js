// Testet rundgaenge_pruefen.js: erst anlegen simulieren (Speicher), dann Prüf-Skript dagegen laufen lassen – korrekt und mit Fehler.
const fs = require("fs"), path = require("path"), vm = require("vm");
const store = {}; let nextId = 2000;
const ok = (b) => ({ ok: true, status: 200, json: async () => b, text: async () => JSON.stringify(b) });
async function fetchFake(url, opt = {}) {
  const liste = (url.match(/getbytitle\('([^']+)'\)/) || [])[1];
  if (url.endsWith("/_api/contextinfo")) return ok({ FormDigestValue: "x" });
  if ((opt.method || "GET") === "POST") { const d = JSON.parse(opt.body); const id = ++nextId; (store[liste] = store[liste] || []).push({ ...d, Id: id }); return ok({ Id: id }); }
  let rows = store[liste] || [];
  const f = decodeURIComponent(url).match(/\$filter=([^&]+)/);
  if (f) { const m1 = f[1].match(/^Title eq '(.*)'$/), m2 = f[1].match(/^RundgangID eq (\d+)$/);
    if (m1) rows = rows.filter(r => r.Title === m1[1].replace(/''/g, "'")); else if (m2) rows = rows.filter(r => r.RundgangID === +m2[1]); }
  return ok({ value: rows.map(r => ({ ...r })) });
}
const run = (file, transform) => new Promise(res => { const logs = []; const ctx = { fetch: fetchFake, console: { log: (...a) => logs.push(a.join(" ")), warn: (...a) => logs.push(a.join(" ")), error: (...a) => logs.push(a.join(" ")) }, JSON, String, Number, Object, Promise };
  vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(__dirname, file), "utf8"), ctx); setTimeout(() => res(logs.join("\n")), 800); });
(async () => {
  console.log("Anlegen: " + (await run("rundgaenge_anlegen.js")).split("\n")[0]);
  const a = await run("rundgaenge_pruefen.js"); console.log("Prüfen (korrekt): " + a.split("\n")[0]);
  const pp = store.RG_Pruefpunkte; const x = pp.find(p => p.Title === "Zählerstand Gaszähler S3"); x.Title = "Zählerstand Gaszähler S9";
  const b = await run("rundgaenge_pruefen.js"); console.log("Prüfen (Fehler eingebaut): " + b.split("\n").slice(0, 2).join(" | "));
  x.Title = "Zählerstand Gaszähler S3"; store.RG_Plan.pop();
  const c = await run("rundgaenge_pruefen.js"); console.log("Prüfen (Plan fehlt): " + c.split("\n").slice(0, 2).join(" | "));
})();
