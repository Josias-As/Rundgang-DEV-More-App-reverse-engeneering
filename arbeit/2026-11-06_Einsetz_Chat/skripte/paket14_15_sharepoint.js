// Paket 14+15, Schritt 1 (SharePoint) – 06.11.2026
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter. Legt nur an, was fehlt. Löscht und ändert nichts.
// RG_Pruefpunkte: AbwMax (Zahl, leer), AbwProzent (Ja/Nein, Nein), NurSteigend (Ja/Nein, Nein), VergleichPunkt (Zahl, 0), VergleichTol (Zahl, 0)
(async () => {
  const SITE = "https://technoformgroup.sharepoint.com/sites/IMSKonzept";
  const NM = "application/json;odata=nometadata", VB = "application/json;odata=verbose";
  const digest = (await (await fetch(SITE + "/_api/contextinfo", { method: "POST", headers: { Accept: NM } })).json()).FormDigestValue;
  const req = async (method, url, body, verbose) => {
    const t = verbose ? VB : NM;
    const r = await fetch(SITE + url, { method, headers: { Accept: t, "Content-Type": t, "X-RequestDigest": digest }, body: body ? JSON.stringify(body) : undefined });
    if (!r.ok) throw new Error(method + " " + url + " → " + r.status + " " + (await r.text()).slice(0, 300));
    return r.status === 204 ? null : r.json();
  };
  const L = "/_api/web/lists/getbytitle('RG_Pruefpunkte')";
  const log = [];
  const feldDa = async (f) => (await req("GET", L + "/fields?$select=InternalName&$filter=InternalName eq '" + f + "'")).value.length > 0;
  const feld = async (name, xml) => {
    if (await feldDa(name)) { log.push(name + " war schon da"); return; }
    await req("POST", L + "/fields/createfieldasxml", { parameters: { __metadata: { type: "SP.XmlSchemaFieldCreationInformation" }, SchemaXml: xml, Options: 24 } }, true);
    if (!(await feldDa(name))) throw new Error(name + " wurde mit anderem internen Namen angelegt – bitte melden");
    log.push(name + " angelegt");
  };
  const zahl = (n, std) => '<Field Type="Number" DisplayName="' + n + '" Name="' + n + '" StaticName="' + n + '"' + (std === null ? " />" : "><Default>" + std + "</Default></Field>");
  const janein = (n) => '<Field Type="Boolean" DisplayName="' + n + '" Name="' + n + '" StaticName="' + n + '"><Default>0</Default></Field>';
  await feld("AbwMax", zahl("AbwMax", null));
  await feld("AbwProzent", janein("AbwProzent"));
  await feld("NurSteigend", janein("NurSteigend"));
  await feld("VergleichPunkt", zahl("VergleichPunkt", 0));
  await feld("VergleichTol", zahl("VergleichTol", 0));
  log.push("QuelleID " + ((await feldDa("QuelleID")) ? "vorhanden" : "FEHLT – bitte melden"));
  console.log("FERTIG\n" + log.join("\n"));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken."));
