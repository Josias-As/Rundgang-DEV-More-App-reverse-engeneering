// Paket 8–10, Schritt 1 (SharePoint) – 03.11.2026
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter.
// Legt nur an, was fehlt (doppeltes Ausführen schadet nicht). Löscht und benennt nichts um.
// 1) Liste RG_Ansprechpartner + Spalten Kontakt, Telefon, Hinweis, Allgemein, Aktiv + 3 Testzeilen (nur wenn Liste leer)
// 2) RG_Pruefpunkte: Kritisch, KritischText, Ansprechpartner, Rueckfrage, RueckfrageText
// 3) Testwerte nur im Probe-Rundgang „ZZ Test Infrastrukturrundgang“:
//    Prüfpunkt 39 (Batterieraum) kritisch + Rückfrage; Abschnitt für Kompressoren (Kat. 11) und Kältemaschinen (Kat. 14)
(async () => {
  const SITE = "https://technoformgroup.sharepoint.com/sites/IMSKonzept";
  const NM = "application/json;odata=nometadata", VB = "application/json;odata=verbose";
  const digest = (await (await fetch(SITE + "/_api/contextinfo", { method: "POST", headers: { Accept: NM } })).json()).FormDigestValue;
  const req = async (method, url, body, verbose, extra = {}) => {
    const t = verbose ? VB : NM;
    const r = await fetch(SITE + url, { method, headers: { Accept: t, "Content-Type": t, "X-RequestDigest": digest, ...extra }, body: body ? JSON.stringify(body) : undefined });
    if (!r.ok) throw new Error(method + " " + url + " → " + r.status + " " + (await r.text()).slice(0, 300));
    return r.status === 204 ? null : r.json();
  };
  const liste = (n) => "/_api/web/lists/getbytitle('" + n + "')";
  const log = [];

  const listeDa = async (n) => (await req("GET", "/_api/web/lists?$select=Title&$filter=Title eq '" + n + "'")).value.length > 0;
  const feldDa = async (l, f) => (await req("GET", liste(l) + "/fields?$select=InternalName&$filter=InternalName eq '" + f + "'")).value.length > 0;
  const feld = async (l, name, xml) => {
    if (await feldDa(l, name)) { log.push(l + "." + name + " war schon da"); return; }
    await req("POST", liste(l) + "/fields/createfieldasxml", { parameters: { __metadata: { type: "SP.XmlSchemaFieldCreationInformation" }, SchemaXml: xml, Options: 24 } }, true);
    if (!(await feldDa(l, name))) throw new Error(l + "." + name + " wurde mit anderem internen Namen angelegt – bitte melden");
    log.push(l + "." + name + " angelegt");
  };
  const txt = (n) => '<Field Type="Text" DisplayName="' + n + '" Name="' + n + '" StaticName="' + n + '" />';
  const note = (n) => '<Field Type="Note" DisplayName="' + n + '" Name="' + n + '" StaticName="' + n + '" NumLines="6" RichText="FALSE" />';
  const janein = (n, std) => '<Field Type="Boolean" DisplayName="' + n + '" Name="' + n + '" StaticName="' + n + '"><Default>' + std + '</Default></Field>';

  // 1) RG_Ansprechpartner
  const A = "RG_Ansprechpartner";
  if (!(await listeDa(A))) {
    await req("POST", "/_api/web/lists", { __metadata: { type: "SP.List" }, Title: A, BaseTemplate: 100, Description: "Rundgang: Ansprechpartner bei kritischen Mängeln" }, true);
    log.push(A + " angelegt");
  } else log.push(A + " war schon da");
  await feld(A, "Kontakt", txt("Kontakt"));
  await feld(A, "Telefon", txt("Telefon"));
  await feld(A, "Hinweis", note("Hinweis"));
  await feld(A, "Allgemein", janein("Allgemein", 0));
  await feld(A, "Aktiv", janein("Aktiv", 1));
  const vorhanden = (await req("GET", liste(A) + "/items?$select=Id,Title")).value;
  let elektrikerId = (vorhanden.find(x => x.Title === "Elektriker") || {}).Id;
  if (vorhanden.length === 0) {
    const neu = async (d) => (await req("POST", liste(A) + "/items", d)).Id;
    await neu({ Title: "Allgemein", Kontakt: "ZZ Test Leitstand", Telefon: "0000 Test", Hinweis: "ZZ Test – erscheint bei jedem kritischen Mangel.", Allgemein: true, Aktiv: true });
    elektrikerId = await neu({ Title: "Elektriker", Kontakt: "ZZ Test Elektro GmbH", Telefon: "0000 Test", Hinweis: "ZZ Test", Allgemein: false, Aktiv: true });
    await neu({ Title: "IT-Dienstleister", Kontakt: "ZZ Test IT", Telefon: "0000 Test", Hinweis: "ZZ Test", Allgemein: false, Aktiv: true });
    log.push(A + ": 3 Testzeilen angelegt");
  } else log.push(A + " hatte schon " + vorhanden.length + " Zeilen – keine Testzeilen angelegt");

  // 2) RG_Pruefpunkte
  const P = "RG_Pruefpunkte";
  await feld(P, "Kritisch", janein("Kritisch", 0));
  await feld(P, "KritischText", txt("KritischText"));
  await feld(P, "Ansprechpartner", txt("Ansprechpartner"));
  await feld(P, "Rueckfrage", janein("Rueckfrage", 0));
  await feld(P, "RueckfrageText", txt("RueckfrageText"));
  log.push("RG_Pruefpunkte.Abschnitt " + ((await feldDa(P, "Abschnitt")) ? "vorhanden" : "FEHLT – bitte melden"));

  // 3) Testwerte im Probe-Rundgang
  const merge = (id, d) => req("POST", liste(P) + "/items(" + id + ")", d, false, { "IF-MATCH": "*", "X-HTTP-Method": "MERGE" });
  const p39 = (await req("GET", liste(P) + "/items?$select=Id,Title,KategorieID&$filter=Id eq 39")).value[0];
  if (p39 && p39.KategorieID === 9) {
    await merge(39, { Kritisch: true, KritischText: "Anlage nicht weiter betreiben.", Ansprechpartner: elektrikerId ? String(elektrikerId) : "", Rueckfrage: true, RueckfrageText: "Normalerweise steht hier i.O." });
    log.push("Prüfpunkt 39 („" + p39.Title + "“): Kritisch + Rückfrage gesetzt, Ansprechpartner " + (elektrikerId || "–"));
  } else log.push("Prüfpunkt 39 nicht im Probe-Rundgang gefunden – nichts gesetzt");
  if (await feldDa(P, "Abschnitt")) {
    const pp = (await req("GET", liste(P) + "/items?$select=Id,Title,Abschnitt&$top=500&$filter=KategorieID eq 11 or KategorieID eq 14")).value;
    let n = 0;
    for (const p of pp) {
      const teil = p.Title.split(" – ");
      if (teil.length > 1 && !p.Abschnitt) { await merge(p.Id, { Abschnitt: teil[0] }); n++; }
    }
    log.push("Abschnitt gesetzt bei " + n + " Prüfpunkten (Kompressoren, Kältemaschinen)");
  }
  console.log("FERTIG\n" + log.join("\n"));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken."));
