// Paket 23, Schritt A1 (SharePoint) – 06.11.2026
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter. Legt nur an, was fehlt. Löscht nichts.
// 1) RG_Rundgaenge: Spalte Testrundgang (Ja/Nein, Standard Nein)
// 2) Testrundgang = Ja nur bei Rundgängen, deren Name mit „ZZ Test“ beginnt (andere bleiben unberührt)
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
  const L = "/_api/web/lists/getbytitle('RG_Rundgaenge')";
  const log = [];
  const feldDa = async (f) => (await req("GET", L + "/fields?$select=InternalName&$filter=InternalName eq '" + f + "'")).value.length > 0;
  if (await feldDa("Testrundgang")) log.push("Testrundgang war schon da");
  else {
    await req("POST", L + "/fields/createfieldasxml", { parameters: { __metadata: { type: "SP.XmlSchemaFieldCreationInformation" }, SchemaXml: '<Field Type="Boolean" DisplayName="Testrundgang" Name="Testrundgang" StaticName="Testrundgang"><Default>0</Default></Field>', Options: 24 } }, true);
    if (!(await feldDa("Testrundgang"))) throw new Error("Testrundgang wurde mit anderem internen Namen angelegt – bitte melden");
    log.push("Testrundgang angelegt");
  }
  const rg = (await req("GET", L + "/items?$select=Id,Title,Testrundgang&$top=500")).value;
  for (const r of rg) {
    if ((r.Title || "").startsWith("ZZ Test") && !r.Testrundgang) {
      await req("POST", L + "/items(" + r.Id + ")", { Testrundgang: true }, false, { "IF-MATCH": "*", "X-HTTP-Method": "MERGE" });
      log.push("Testrundgang = Ja: " + r.Id + " " + r.Title);
    }
  }
  log.push("Nicht als Test markiert: " + rg.filter(r => !(r.Title || "").startsWith("ZZ Test")).map(r => r.Id + " " + r.Title).join(", "));
  console.log("FERTIG\n" + log.join("\n"));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken."));
