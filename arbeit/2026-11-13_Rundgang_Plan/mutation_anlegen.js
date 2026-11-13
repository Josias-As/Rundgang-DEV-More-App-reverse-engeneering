// Mutationstest: baut absichtlich Fehler ins Anlege-Skript (nur im Speicher) und prüft, ob pruefe_anlegen.js sie findet.
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const orig = fs.readFileSync(path.join(__dirname, "rundgaenge_anlegen.js"), "utf8");
const M = [
  ["Fragetext", '"Sichtprüfung Heizungsanlage"', '"Sichtprüfung Heizung"'],
  ["Grenze", '"MinWert":1.5', '"MinWert":1.6'],
  ["Fassungsspalte", "Fassungf: 1,", "Fassung: 1,"],
  ["Plan-Rhythmus", "ZyklusWochen: 1, StartMontag", "ZyklusWochen: 2, StartMontag"],
  ["Pflicht Montagsfrage", '"Pflicht":false', '"Pflicht":true'],
  ["Bereich sichtbar", "Ausblenden: rg.ausblenden", "Ausblenden: false"],
  ["Typ", '"Eingabetyp":"ZAHL"', '"Eingabetyp":"TEXT"'],
  ["Testrundgang", "Testrundgang: true", "Testrundgang: false"],
  ["Code fehlt", "ZugangscodeID: p._code ? codeId : 0", "ZugangscodeID: 0"],
  ["Kritisch fehlt", '"Kritisch":true', '"Kritisch":false'],
  ["Abschnitt", '"Abschnitt":"Kompressor 3"', '"Abschnitt":"Kompressor 4"'],
  ["Einheit", '"Einheit":"m³"', '"Einheit":"m3"'],
  ["Plan-Tag", '"tage":[1,3,5]', '"tage":[1,3]'],
];
let ok = 0;
for (const [n, a, b] of M) {
  if (!orig.includes(a)) { console.log("✗ " + n + ": Muster nicht gefunden"); continue; }
  const out = execFileSync("node", [path.join(__dirname, "pruefe_anlegen.js")], { env: { ...process.env, PRUEF_CODE: orig.replace(a, b) } }).toString();
  const erkannt = !/PRÜFUNG OK/.test(out); if (erkannt) ok++;
  console.log((erkannt ? "✓ erkannt: " : "✗ NICHT erkannt: ") + n);
}
console.log("Mutation " + ok + "/" + M.length);
